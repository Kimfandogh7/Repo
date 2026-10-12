"""Describe video segments on CPU with SmolVLM2-500M-Video-Instruct (Apache-2.0).

Each segment is a short clip (default 60 s) cut from the source video. The model
samples up to MAX_FRAMES frames from it and writes a short English description.
English output is intentional: the model's Persian is weak, and the transcript
(Shenava) is already Persian.

Env:
  VLM_MODEL       default HuggingFaceTB/SmolVLM2-500M-Video-Instruct
  VLM_MAX_FRAMES  default 8 frames per segment
  VLM_SEG_SECONDS default 60
"""
import glob
import os
import subprocess
import tempfile
import time

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

MODEL = os.environ.get("VLM_MODEL", "HuggingFaceTB/SmolVLM2-500M-Video-Instruct")
MAX_FRAMES = int(os.environ.get("VLM_MAX_FRAMES", "8"))
SEG_SECONDS = int(os.environ.get("VLM_SEG_SECONDS", "60"))

_processor = None
_model = None


def load():
    global _processor, _model
    if _model is None:
        torch.set_num_threads(os.cpu_count() or 2)
        _processor = AutoProcessor.from_pretrained(MODEL)
        _model = AutoModelForImageTextToText.from_pretrained(MODEL, torch_dtype=torch.float32).eval()
    return _processor, _model


def cut_segments(src, workdir):
    """Split the video into SEG_SECONDS clips (video only, re-encoded small for speed)."""
    pattern = os.path.join(workdir, "seg_%04d.mp4")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-an", "-vf", "scale=-2:360",
         "-f", "segment", "-segment_time", str(SEG_SECONDS), "-reset_timestamps", "1",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", pattern],
        check=True)
    return sorted(glob.glob(os.path.join(workdir, "seg_*.mp4")))


def describe_clip(path):
    processor, model = load()
    messages = [{
        "role": "user",
        "content": [
            {"type": "video", "path": path},
            {"type": "text", "text": "Describe what happens in this video in two short sentences."},
        ],
    }]
    inputs = processor.apply_chat_template(
        messages, add_generation_prompt=True, tokenize=True,
        return_dict=True, return_tensors="pt", max_frames=MAX_FRAMES)
    with torch.inference_mode():
        out = model.generate(**inputs, do_sample=False, max_new_tokens=80)
    text = processor.batch_decode(out, skip_special_tokens=True)[0]
    # The decoded text contains the whole prompt; keep only the assistant reply.
    return text.split("Assistant:")[-1].strip()


def describe_video(src):
    """Return lines like '[mm:ss] description' for every segment, plus timing info."""
    workdir = tempfile.mkdtemp(prefix="vlm_")
    t0 = time.time()
    lines = []
    for i, seg in enumerate(cut_segments(src, workdir)):
        start = i * SEG_SECONDS
        lines.append(f"[{start // 60:02d}:{start % 60:02d}] {describe_clip(seg)}")
    return "\n".join(lines), time.time() - t0


if __name__ == "__main__":
    import sys
    text, secs = describe_video(sys.argv[1])
    print(text)
    print(f"elapsed_seconds={secs:.1f}")
