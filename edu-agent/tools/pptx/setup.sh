#!/usr/bin/env bash
# نصبِ ppt-master — مولدِ اسلایدِ بومی (native) با انتقال و انیمیشن
# منبع: github.com/hugohe3/ppt-master  (MIT)
#
# استفاده:
#   bash edu-agent/tools/pptx/setup.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
VENDOR="$ROOT/edu-agent/vendor"
DEST="$VENDOR/ppt-master"

echo "==> کلون کردن ppt-master"
mkdir -p "$VENDOR"
if [ -d "$DEST/.git" ]; then
  git -C "$DEST" pull --ff-only -q
else
  rm -rf "$DEST"
  git clone --depth 1 https://github.com/hugohe3/ppt-master.git "$DEST"
fi

echo "==> نصب وابستگی‌های پایتون"
pip install --break-system-packages -q -r "$DEST/skills/ppt-master/requirements.txt"

echo "==> وابستگی‌های پیش‌نمایش (رندر کردن اسلاید به PNG)"
pip install --break-system-packages -q svglib reportlab

echo
echo "نصب شد: $DEST"
echo "مهارت (برای اینکه ایجنت بخواند): $DEST/skills/ppt-master/SKILL.md"
