#!/usr/bin/env bash
# نصب ابزارهای edu-agent در محیط sandbox (CPU، بدون GPU).
# مسیرهای بیرون از مخزن: venv و clone ها در /home/user. فقط vendor/ppt-master داخل مخزن است (gitignored).
# هر مرحله مستقل است؛ خطا در یک مرحله، بقیه را متوقف نمی‌کند.
# وضعیت هر ابزار و محدودیت‌ها: edu-agent/tools/INSTALL_STATUS.md
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TP=/home/user/third_party
V=/home/user/.venv-edu
step(){ echo "##### $1"; }

step "venv اصلی"
[ -d $V ] || python3 -m venv $V
. $V/bin/activate
pip install -q --upgrade pip
pip install -q sherpa-onnx faster-whisper jiwer soundfile numpy pillow av num2words python-pptx matplotlib svglib reportlab edge-tts uv "python-telegram-bot==22.8" rembg playwright imageio-ffmpeg bpy transformers huggingface_hub torch torchvision pytest cmake ninja

step "clone ریپوهای GitHub (بیرون از مخزن)"
mkdir -p $TP && cd $TP
for r in hugohe3/ppt-master Omidbn2000/persian-speech-toolkit alifarrokh/persian-asr ArmanJR/PESTE-Benchmark RisorseArtificiali/anti-vocale GeiserX/Telegram-Archive FALKON-CODE/Telegram-Mirror NousResearch/hermes-agent overpod/openclaw-channel-telegram-userbot d3pre5s/clawgram tc-mb/llama.cpp-omni antirez/ds4 Anemll/ds4-ssd VAST-AI-Research/TripoSR tdlib/telegram-bot-api QwenLM/Qwen2.5-Omni openclaw/openclaw; do
  n=$(basename $r); [ -d $n ] || git clone -q --depth 1 https://github.com/$r.git $n || echo "FAIL clone $r"
done

step "ppt-master در edu-agent/vendor و وابستگی‌ها"
mkdir -p $ROOT/edu-agent/vendor && rm -rf $ROOT/edu-agent/vendor/ppt-master && cp -r $TP/ppt-master $ROOT/edu-agent/vendor/ppt-master
pip install -q -r $TP/ppt-master/skills/ppt-master/requirements.txt

step "وابستگی‌های ASR فارسی، TripoSR، Telegram-Archive"
pip install -q -r $TP/persian-speech-toolkit/requirements.txt
pip install -q telethon python-socks APScheduler python-dotenv cryptg
pip install -q omegaconf einops trimesh moderngl xatlas imageio huggingface-hub gradio
# torch را دوباره روی نسخه‌ی سازگار با torchvision قفل کنید (requirements قبلی آن را پایین می‌آورد)
pip install -q "torch==2.14.1" "torchvision==0.29.1"

step "PESTE (نیازمند Python 3.12؛ فقط کتابخانه با --ignore-requires-python نصب می‌شود، CLI روی 3.11 اجرا نمی‌شود)"
pip install -q --ignore-requires-python $TP/PESTE-Benchmark || echo "FAIL PESTE"

step "hermes-agent در venv جدا"
python3 -m venv /home/user/.venv-hermes && /home/user/.venv-hermes/bin/pip install -q hermes-agent

step "ffmpeg از imageio-ffmpeg"
mkdir -p /home/user/bin && ln -sf "$(python -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')" /home/user/bin/ffmpeg

step "Chromium برای Playwright (@sparticuz/chromium از npm؛ CDN پلی‌رایت در sandbox بسته است)"
mkdir -p /home/user/npm-tools && cd /home/user/npm-tools && npm install --no-audit --no-fund @sparticuz/chromium@153.0.0
node -e "
const fs=require('fs'),zlib=require('zlib'),b='node_modules/@sparticuz/chromium/bin/';
for (const [src,dst] of [['chromium.br','/home/user/bin/chromium-sparticuz'],['al2023.tar.br','/home/user/bin/al2023.tar'],['swiftshader.tar.br','/home/user/bin/swiftshader.tar']])
  fs.writeFileSync(dst, zlib.brotliDecompressSync(fs.readFileSync(b+src)));
" && chmod +x /home/user/bin/chromium-sparticuz && mkdir -p /home/user/bin/al2023 && tar xf /home/user/bin/al2023.tar -C /home/user/bin/al2023 && tar xf /home/user/bin/swiftshader.tar -C /home/user/bin/

step "OpenClaw و افزونه‌های Node"
cd /home/user/npm-tools && npm install --no-audit --no-fund openclaw
cd $TP/clawgram && npm install --no-audit --no-fund && npm run build
cd $TP/openclaw-channel-telegram-userbot && npm install --no-audit --no-fund

step "llama.cpp-omni (وصله‌ی Linux برای F_NOCACHE؛ فقط macOS است)"
cd $TP/llama.cpp-omni && grep -q "define F_NOCACHE" src/llama-moe-slot.cpp || sed -i '0,/#include/s//#ifndef F_NOCACHE\n#define F_NOCACHE -1\n#endif\n#include/' src/llama-moe-slot.cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release -DLLAMA_CURL=OFF && cmake --build build -j2 --target llama-cli

step "ds4 (CPU)"
cd $TP/ds4 && make cpu

step "telecrawl: باینری از GitHub Release (CDN از sandbox بسته است؛ Go هم نصب نیست)"
echo "نیاز به دستی یا Actions دارد"
echo "DONE"
