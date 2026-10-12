"""Telegram bot: transcribes audio and video that users send to it, on CPU only.

Pipeline per file: Bot API download -> ffmpeg (mono 16 kHz WAV, PART_SECONDS parts)
-> Shenava Koochik v1.0 (Persian CTC via sherpa-onnx) -> timestamped transcript.

Only the Bot API is used, and users send files to the bot themselves. Telegram's
terms forbid using platform data for AI outside what is needed to run a bot, so
do not add channel scraping or MTProto collection here.

Env:
  TELEGRAM_BOT_TOKEN         required (GitHub secret)
  TELEGRAM_ALLOWED_USER_IDS  comma-separated numeric ids; empty = refuse everyone
  MAX_FILE_MB                default 19 (Bot API download cap is 20 MB)
  PART_SECONDS               default 300
"""
import asyncio
import glob
import logging
import os
import shutil
import subprocess
import tempfile
import time

import numpy as np
import sherpa_onnx
import soundfile as sf
from huggingface_hub import snapshot_download
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
log = logging.getLogger("tgbot")

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ALLOWED = {int(x) for x in os.environ.get("TELEGRAM_ALLOWED_USER_IDS", "").replace(" ", "").split(",") if x.isdigit()}
MAX_FILE_MB = float(os.environ.get("MAX_FILE_MB", "19"))
PART_SECONDS = int(os.environ.get("PART_SECONDS", "300"))
SHENAVA_REPO = "Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx"

_recognizer = None
_lock = asyncio.Semaphore(1)  # one CPU-heavy job at a time


def get_recognizer():
    """Load the Persian CTC model once. The first call downloads it from Hugging Face."""
    global _recognizer
    if _recognizer is None:
        local = snapshot_download(repo_id=SHENAVA_REPO, cache_dir="/tmp/hf_cache")
        model = sorted(glob.glob(os.path.join(local, "**", "model*.onnx"), recursive=True))[0]
        tokens = sorted(glob.glob(os.path.join(local, "**", "tokens.txt"), recursive=True))[0]
        _recognizer = sherpa_onnx.OfflineRecognizer.from_nemo_ctc(
            model=model, tokens=tokens, num_threads=os.cpu_count() or 2,
            decoding_method="greedy_search")
        log.info("Shenava loaded from %s", local)
    return _recognizer


def to_wav_parts(src, workdir):
    """Extract audio as mono 16 kHz and split it into PART_SECONDS chunks."""
    pattern = os.path.join(workdir, "part_%03d.wav")
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000",
         "-f", "segment", "-segment_time", str(PART_SECONDS), "-c:a", "pcm_s16le", pattern],
        check=True)
    return sorted(glob.glob(os.path.join(workdir, "part_*.wav")))


def transcribe_parts(parts):
    rec = get_recognizer()
    out = []
    for i, p in enumerate(parts):
        samples, sr = sf.read(p, dtype="float32")
        st = rec.create_stream()
        st.accept_waveform(sr, np.asarray(samples, dtype=np.float32))
        rec.decode_stream(st)
        start = i * PART_SECONDS
        stamp = f"[{start // 60:02d}:{start % 60:02d}]"
        out.append(f"{stamp} {st.result.text.strip()}")
    return "\n".join(out)


def process_file(src):
    workdir = tempfile.mkdtemp(prefix="tg_")
    try:
        parts = to_wav_parts(src, workdir)
        return transcribe_parts(parts)
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def allowed(update: Update) -> bool:
    return update.effective_user is not None and update.effective_user.id in ALLOWED


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        await update.message.reply_text(f"دسترسی ندارید. شناسه شما: {update.effective_user.id}")
        return
    await update.message.reply_text(
        "فایل صوتی یا ویدیویی بفرستید تا متن فارسی آن را برگردانم. "
        "حداکثر حجم فایل حدود ۱۹ مگابایت است.")


async def cmd_whoami(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"شناسه شما: {update.effective_user.id}")


async def on_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not allowed(update):
        await msg.reply_text(f"دسترسی ندارید. شناسه شما: {update.effective_user.id}")
        return
    media = msg.video or msg.audio or msg.voice or msg.video_note or msg.document
    if media is None:
        return
    if msg.document and not (msg.document.mime_type or "").startswith(("audio/", "video/")):
        await msg.reply_text("این نوع فایل پشتیبانی نمی‌شود؛ فقط صوت و ویدیو.")
        return
    size_mb = (media.file_size or 0) / 1024 / 1024
    if size_mb > MAX_FILE_MB:
        await msg.reply_text(
            f"فایل {size_mb:.0f} مگابایتی از سقف ربات API ({MAX_FILE_MB:.0f} مگابایت) بزرگ‌تر است. "
            "برای فایل‌های بزرگ باید Local Bot API راه بیندازیم.")
        return
    status = await msg.reply_text("در حال پردازش… (روی CPU ممکن است چند دقیقه طول بکشد)")
    await context.bot.send_chat_action(msg.chat_id, ChatAction.TYPING)
    t0 = time.time()
    tmp = tempfile.mkdtemp(prefix="tgin_")
    try:
        tgfile = await media.get_file()
        src = os.path.join(tmp, "input")
        await tgfile.download_to_drive(src)
        async with _lock:
            text = await asyncio.to_thread(process_file, src)
        elapsed = time.time() - t0
        header = f"متن ({elapsed:.0f} ثانیه پردازش):\n"
        if len(header) + len(text) <= 3900:
            await msg.reply_text(header + (text or "(گفتاری پیدا نشد)"))
        else:
            out_path = os.path.join(tmp, "transcript.txt")
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)
            with open(out_path, "rb") as f:
                await msg.reply_document(f, filename="transcript.txt", caption="متن کامل")
    except Exception as e:  # report the error and keep serving
        log.exception("processing failed")
        await msg.reply_text(f"خطا در پردازش: {e!r}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
        try:
            await status.delete()
        except Exception:
            pass


def main():
    if not TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN is not set")
    if not ALLOWED:
        log.warning("TELEGRAM_ALLOWED_USER_IDS is empty: only /whoami works")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("whoami", cmd_whoami))
    app.add_handler(MessageHandler(
        filters.VIDEO | filters.AUDIO | filters.VOICE | filters.VIDEO_NOTE | filters.Document.ALL,
        on_media))
    log.info("polling started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
