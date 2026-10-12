# وضعیت نصب ابزارها در sandbox (2026-10-12)

این فایل نتیجه‌ی نصب واقعی است، نه ادعا. هر ردیف با یکی از این برچسب‌ها ثبت شده: **نصب و تست شد**، **نصب شد (تست نشد)**، **مسدود** (علت ذکر شده).

محیط: Python 3.11.2، ۲ vCPU، ۳ GB RAM، بدون GPU. دسترسی شبکه از sandbox فقط به `pypi.org`، `files.pythonhosted.org`، `registry.npmjs.org`، `github.com`، `codeload.github.com` و `api.github.com` است. `huggingface.co`، apt، `download.pytorch.org`، `cdn.playwright.dev`، `release-assets.githubusercontent.com` (CDN دانلود Release گیت‌هاب) و `speech.platform.bing.com` در دسترس نیستند.

## Python (venv: `/home/user/.venv-edu`)

| ابزار | وضعیت | نکته |
|---|---|---|
| sherpa-onnx 1.13.8 | نصب و import شد | مدل‌های Shenava از Hugging Face گرفته می‌شوند؛ HF در sandbox بسته است |
| faster-whisper 1.2.1 | نصب و import شد | مدل Whisper هم از HF است |
| python-pptx 1.0.2 | نصب و import شد | |
| torch 2.14.1 + torchvision 0.29.1 | نصب و import شد | wheel از PyPI است و پکیج‌های CUDA را هم می‌آورد؛ روی CPU اجرا می‌شود و GPU استفاده نمی‌کند |
| transformers 5.19.0 + huggingface_hub | نصب و import شد | وزن مدل‌ها از HF گرفته نشد |
| rembg 2.0.85 | import شد | مدل `u2net.onnx` از GitHub Release می‌آید و CDN بسته است: **مسدود** |
| TripoSR (کد + وابستگی‌ها) | import شد | با shim موجود در `edu-agent/tools/3d/shim` (torchmcubes). وزن‌ها از HF: **مسدود** |
| python-telegram-bot 22.8 | نصب و import شد | GPL-3.0 |
| playwright 1.63.0 | نصب شد | دانلود مرورگر پلی‌رایت مسدود است. با chromium از npm کار کرد (پایین‌تر) |
| edge-tts 7.2.8 | نصب شد؛ اجرا **مسدود** | endpoint مایکروسافت (`speech.platform.bing.com`) در sandbox بسته است |
| imageio-ffmpeg 0.6.0 | نصب شد | ffmpeg 7.0.2 static در `/home/user/bin/ffmpeg` |
| uv 0.13.0 | نصب شد | دانلود Python 3.12 از GitHub مسدود است |
| ppt-master | نصب شد و `svg_to_pptx.py --help` اجرا شد | در `edu-agent/vendor/ppt-master` (gitignored) |
| persian-speech-toolkit | requirements نصب شد | |
| PESTE-Benchmark 2.1.0 | کتابخانه نصب شد؛ CLI **مسدود** | پروژه Python ≥3.12 می‌خواهد؛ نصب Python 3.12 از GitHub مسدود است |
| Telegram-Archive | requirements نصب شد؛ پکیج **مسدود** | پکیج Python ≥3.14 می‌خواهد |
| Blender (bpy 4.4.0) | pip نصب شد؛ import **مسدود** | کتابخانه‌های سیستمی X11 (`libXrender`) نیست و apt بسته است |
| hermes-agent 0.19.0 | نصب شد در `/home/user/.venv-hermes` و `hermes --help` کار کرد | |

## Node (`/home/user/npm-tools`)

| ابزار | وضعیت | نکته |
|---|---|---|
| openclaw (npm) | نصب شد؛ `openclaw --version` = 2026.9.2 | نسخه‌ی npm با کلون GitHub (2026.10.2) یکی نیست |
| clawgram | npm install و build موفق | MIT |
| openclaw-channel-telegram-userbot | npm install موفق | MIT (بدون build) |
| @sparticuz/chromium 153.0.0 | نصب شد؛ **Playwright با آن launch شد** | باینری در `/home/user/bin/chromium-sparticuz`؛ کتابخانه‌ها و SwiftShader از همان پکیج استخراج شد. اجرا: `. /home/user/bin/env-edu.sh` |

## باینری‌های ساخته‌شده از سورس

| ابزار | وضعیت | نکته |
|---|---|---|
| llama.cpp-omni | **`llama-cli` ساخته شد**؛ `libomni.so` و `libmtmd.so` هم ساخته شدند | این فورک target `llama-server` ندارد. برای Linux یک وصله‌ی محلی روی `F_NOCACHE` (فقط macOS) اعمال شد. در `third_party` است، نه در مخزن |
| ds4 (`make cpu`) | ساخته شد؛ `./ds4 --help` کار کرد | CPU؛ مسیرهای CUDA/Metal/ROCm کامپایل نشدند |
| telecrawl v0.5.0 | **مسدود** | دانلود باینری از Release با EOF شکست خورد (CDN). Go هم نصب نیست؛ سورس فقط با codeload در دسترس است |
| telegram-bot-api (tdlib) | **مسدود** | هدرهای OpenSSL و zlib نیستند و apt بسته است |
| tesseract | **مسدود** | apt بسته است |
| Blender (binary) | **مسدود** | apt بسته است؛ فقط bpy از PyPI نصب شد |

## سورس‌ها (clone در `/home/user/third_party`، بدون نصب)

anti-vocale (اپ Flutter؛ SDK در دسترس نیست)، Telegram-Mirror (فقط اسکریپت)، Qwen2.5-Omni (وزن‌ها از HF)، TripoSR (وزن‌ها از HF)، PESTE، Telegram-Archive، tdlib، openclaw (کلون)، hermes-agent (کلون).

## مدل‌های Hugging Face (مسدود در sandbox)

Shenava Koochik (v1.0 و v1.5)، SmolVLM2، Florence-2، Nimaone، FC-Fa، Qwen2.5-Omni GGUF، وزن‌های TripoSR و u2net برای rembg. این مدل‌ها در GitHub Actions دانلود شده‌اند (`persian-asr.yml`، `vlm-test.yml`، `vision.yml`)، جایی که HF باز است.

## بازتولید

`edu-agent/tools/install_all.sh` مراحل نصب را به ترتیب اجرا می‌کند. مرحله‌ی llama.cpp-omni نیاز به وصله‌ی Linux دارد که خود اسکریپت اعمال می‌کند. مرحله‌ی telecrawl دستی است.
