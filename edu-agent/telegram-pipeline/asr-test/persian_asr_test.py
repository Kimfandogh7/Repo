"""Persian ASR check for the Telegram video pipeline.

Pulls a few FLEURS Persian (fa_ir) test clips through the Hugging Face
datasets-server, transcribes them with faster-whisper (CPU, int8) for each
model size, and reports WER per model plus real-time factor.

Runs on GitHub Actions (outbound to huggingface.co is allowed there).
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

import jiwer
try:
    from faster_whisper import WhisperModel
except ImportError:  # faster-whisper optional when MODELS is empty
    WhisperModel = None

N_CLIPS = int(os.environ.get("N_CLIPS", "12"))
MODELS = [m for m in os.environ.get("MODELS", "small,medium").split(",") if m]
OUT_DIR = os.environ.get("OUT_DIR", "edu-agent/telegram-pipeline/asr-test/out")
os.makedirs(OUT_DIR, exist_ok=True)

FLEURS = "https://huggingface.co/datasets/google/fleurs/resolve/main/data/fa_ir"


def fetch_clips(n):
    """Stream the first n FLEURS fa_ir test clips (tsv + tar.gz streamed, stops early)."""
    import tarfile
    with urllib.request.urlopen(f"{FLEURS}/test.tsv", timeout=120) as r:
        lines = r.read().decode("utf-8").splitlines()[:n]
    want = {}
    for line in lines:
        cols = line.split("\t")
        # FLEURS tsv: id, file_name, raw_transcription, transcription, ...
        want[cols[1]] = cols[2]
    print(f"tsv rows selected: {len(want)}", flush=True)
    got = []
    with urllib.request.urlopen(f"{FLEURS}/audio/test.tar.gz", timeout=300) as r:
        with tarfile.open(fileobj=r, mode="r|gz") as tf:
            for m in tf:
                base = os.path.basename(m.name)
                if base in want and m.isfile():
                    data = tf.extractfile(m).read()
                    path = f"/tmp/fa_{len(got):02d}.wav"
                    with open(path, "wb") as f:
                        f.write(data)
                    got.append((path, want[base]))
                    if len(got) >= n:
                        break
    print(f"clips extracted: {len(got)}", flush=True)
    return got


def norm(text):
    text = re.sub(r"[\u064B-\u065F\u0670]", "", text)  # Arabic diacritics
    text = text.replace("\u200c", " ").replace("ي", "ی").replace("ك", "ک")
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


SHENAVA_REPOS = [
    "Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx",
    "Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx",
]


def load_shenava(repo):
    """Download a Shenava sherpa-onnx export and build an offline recognizer.

    Logs the file listing to OUT_DIR so the layout can be inspected from the repo.
    """
    import glob
    from huggingface_hub import snapshot_download
    import sherpa_onnx
    local = snapshot_download(repo_id=repo, cache_dir="/tmp/hf_cache")
    files = sorted(os.path.relpath(p, local) for p in glob.glob(os.path.join(local, "**", "*"), recursive=True) if os.path.isfile(p))
    with open(os.path.join(OUT_DIR, f"files_{repo.split('/')[1]}.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(files))
    def pick(pattern):
        hits = [p for p in glob.glob(os.path.join(local, "**", pattern), recursive=True)]
        return sorted(hits, key=lambda p: ("int8" not in p, len(p)))[0] if hits else None
    tokens = pick("tokens.txt")
    enc = pick("encoder*.onnx")
    if enc:  # transducer (RNNT) export
        dec, joi = pick("decoder*.onnx"), pick("joiner*.onnx")
        rec = sherpa_onnx.OfflineRecognizer.from_transducer(
            encoder=enc, decoder=dec, joiner=joi, tokens=tokens,
            model_type="nemo_transducer", num_threads=os.cpu_count() or 2,
            decoding_method="greedy_search", feature_dim=80)
    else:  # CTC export
        model = pick("model*.onnx") or pick("*.onnx")
        rec = sherpa_onnx.OfflineRecognizer.from_nemo_ctc(
            model=model, tokens=tokens, num_threads=os.cpu_count() or 2,
            decoding_method="greedy_search")
    return rec


def run_shenava(clips):
    import wave
    import numpy as np
    import sherpa_onnx  # noqa: F401
    last_err = None
    for repo in SHENAVA_REPOS:
        try:
            rec = load_shenava(repo)
        except Exception as e:  # try the next export
            last_err = f"{repo}: {e!r}"
            print("shenava load failed:", last_err, flush=True)
            continue
        refs, hyps, audio_secs = [], [], 0.0
        t0 = time.time()
        for path, ref in clips:
            with wave.open(path, "rb") as w:
                sr = w.getframerate()
                raw = w.readframes(w.getnframes())
                audio_secs += w.getnframes() / sr
            samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            st = rec.create_stream()
            st.accept_waveform(sr, samples)
            rec.decode_stream(st)
            refs.append(norm(ref))
            hyps.append(norm(st.result.text))
        elapsed = time.time() - t0
        wer = jiwer.wer(refs, hyps)
        tag = "shenava_" + repo.split("/")[1].replace("Shenava-Koochik-", "koochik_").replace("-sherpa-onnx", "").replace("-RNNT", "")
        with open(os.path.join(OUT_DIR, f"hyp_{tag}.txt"), "w", encoding="utf-8") as f:
            for r_, h_ in zip(refs, hyps):
                f.write(f"REF: {r_}\nHYP: {h_}\n\n")
        return tag, {"wer": round(wer * 100, 2), "rtf": round(elapsed / audio_secs, 3),
                     "audio_seconds": round(audio_secs, 1), "clips": len(clips), "repo": repo}
    raise RuntimeError("no Shenava export loaded: " + str(last_err))


def main():
    clips = fetch_clips(N_CLIPS)
    total_audio = 0.0
    results = {}
    for name in MODELS:
        model = WhisperModel(name, device="cpu", compute_type="int8",
                             cpu_threads=os.cpu_count() or 2)
        refs, hyps = [], []
        t0 = time.time()
        audio_secs = 0.0
        for path, ref in clips:
            segs, info = model.transcribe(path, language="fa", beam_size=1,
                                          vad_filter=False)
            hyp = " ".join(s.text for s in segs)
            audio_secs += info.duration
            refs.append(norm(ref))
            hyps.append(norm(hyp))
        elapsed = time.time() - t0
        total_audio = audio_secs
        wer = jiwer.wer(refs, hyps)
        results[name] = {
            "wer": round(wer * 100, 2),
            "rtf": round(elapsed / audio_secs, 3),
            "audio_seconds": round(audio_secs, 1),
            "clips": len(clips),
        }
        with open(os.path.join(OUT_DIR, f"hyp_{name}.txt"), "w", encoding="utf-8") as f:
            for r_, h_ in zip(refs, hyps):
                f.write(f"REF: {r_}\nHYP: {h_}\n\n")
        print(name, results[name], flush=True)
    if os.environ.get("SHENAVA", "1") == "1":
        try:
            tag, res = run_shenava(clips)
            results[tag] = res
            print(tag, res, flush=True)
        except Exception as e:
            import traceback
            with open(os.path.join(OUT_DIR, "shenava_error.txt"), "w", encoding="utf-8") as f:
                f.write(traceback.format_exc())
            print("shenava failed:", e, flush=True)
    with open(os.path.join(OUT_DIR, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("| model | WER % | RTF | audio s |\n|---|---|---|---|\n")
            for k, v in results.items():
                f.write(f"| {k} | {v['wer']} | {v['rtf']} | {v['audio_seconds']} |\n")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    import traceback
    try:
        sys.exit(main())
    except SystemExit:
        raise
    except BaseException:
        err = traceback.format_exc()
        print(err, flush=True)
        with open(os.path.join(OUT_DIR, "error.txt"), "w", encoding="utf-8") as f:
            f.write(err)
        sys.exit(1)
