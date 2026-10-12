# گزارش ابزارها و یافته‌ها برای ایجنت مستقل بعدی

تاریخ: 2026-10-12 · مخزن: `Kimfandogh7/Repo` (عمومی) · شاخه‌ی کاری: `arena/758efc2d-repo`

این گزارش یک کاتالوگ است: ابزارها، منابع، نتیجه‌های اندازه‌گیری‌شده، و تجربه‌های عملی. هر ادعا با وضعیتش علامت خورده: **تست شد** (روی این مخزن اجرا شد)، **بررسی شد** (از منبع اولیه خوانده شد)، یا **بررسی نشد** (هنوز با منبع تأیید نشده). تصمیم‌گیری با خود ایجنت است.

---

## ۱. خلاصه‌ی یافته‌ها

1. **برای ASR فارسی روی CPU، Shenava Koochik v1.0 (sherpa-onnx CTC) بهترین نتیجه‌ی اندازه‌گیری‌شده‌ی این مخزن است:** WER ۹٫۵۲٪ روی ۱۲ کلیپ FLEURS فارسی، RTF حدود ۰٫۰۱ تا ۰٫۰۵ روی ۲ vCPU. Whisper medium با WER ۳۱٫۸۵٪ و RTF ۰٫۹۶ در همان شرایط کندتر و کم‌دقت‌تر بود.
   **هشدار نمونه:** ۱۲ کلیپ کم است. در بنچمارک بزرگ‌تر PESTE (۸۷۱ کلیپ FLEURS fa_ir، روی GPU)، مدل Shenava-Rizeh v1.0 (خانواده‌ی نزدیک ولی نه همان Koochik) WER ۱۵٫۵۵٪ گرفت و Whisper medium (openai) WER ۴۳٫۱۶٪. پس عدد ۹٫۵۲٪ احتمالاً خوش‌بینانه است و این مقایسه‌ها فقط برای جهت‌یابی‌اند.
2. **VLM کوچک (SmolVLM2-500M) روی CPU کند است:** روی ۲ vCPU حدود ۳٫۴ برابر زمان واقعی. برای تحلیل ساعت‌ها ویدیو روی یک runner محدود کافی نیست. کیفیت توصیف روی ویدیوی واقعی سنجیده نشده.
3. **Gemma 3n برای ASR فارسی مناسب نیست.** در PARSA-Bench (جدول ۱۲ ضمیمه‌ی E)، Gemma-3n-E2B در ۱۱٫۶٪ و Gemma-3n-E4B در ۱۳٫۴٪ از utteranceها گرفتار حلقه‌ی تکرار شدند. این utteranceها ۸۲٪ و ۸۶٪ از میانگین WER مدل را ساختند. Qwen3-Omni-30B و سه مدل تجاری در همان بنچمارک هیچ collapse نداشتند.
4. **Actions برای سرویس دائمی محدودیت دارد:** هر job حداکثر ۶ ساعت اجرا می‌شود (مستندات رسمی GitHub). runnerهای استاندارد برای مخزن عمومی رایگان‌اند (larger runnerها برای مخزن عمومی رایگان نیستند). در مخزن خصوصی، اجرای ۲۴ ساعته‌ی ~۴۳٬۲۰۰ دقیقه‌ای با ۲٬۰۰۰ دقیقه‌ی رایگان و نرخ ۰٫۰۰۶ دلار (Linux 2-core) حدود ۲۴۷ دلار در ماه می‌شود.
5. **شرایط محتوای تلگرام برای AI محدودکننده است:** Terms of Service for Content Licensing (نسخه‌ی ۲۰۲۶؛ روز دقیق در صفحه‌ی بررسی‌شده نبود) استفاده از داده‌ی پلتفرم برای توسعه، آموزش یا استقرار مدل‌های AI را منع می‌کند. استثنا فقط برای راه‌اندازی ربات یا کلاینت مطابق API ToS، یا با رضایت صریح، آگاهانه و مداوم همه‌ی کاربران مربوط است. این موضوع مستقیم روی تحلیل کانال‌های عمومی اثر دارد.

---

## ۲. ابزارها و مدل‌ها

### گفتار و ASR فارسی

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| sherpa-onnx ۱٫۱۳٫۸ | github.com/k2-fsa/sherpa-onnx | Apache-2.0 (بررسی شد) | **تست شد**. پشتیبانی Persian NeMo CTC از نسخه‌ی ۱٫۱۳٫۵ |
| Shenava Koochik v1.0 (CTC) | `Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx` | Apache-2.0 (کارت مدل بررسی شد) | **تست شد**: WER ۹٫۵۲٪ روی ۱۲ کلیپ. کارت مدل: غیرفعال‌کردن per-feature normalization لازم است |
| Shenava Koochik v1.5 (RNNT) | `Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx` | Apache-2.0 (بررسی شد) | **تست شد**: WER ۱۰٫۱۲٪ روی ۱۲ کلیپ |
| faster-whisper (small، medium) | github.com/SYSTRAN/faster-whisper | MIT (بررسی شد) | **تست شد**: WER به ترتیب ۵۶٫۲۵٪ و ۳۱٫۸۵٪ |
| Nimaone/nemotron-asr-streaming-farsi-onnx | huggingface.co/Nimaone/nemotron-asr-streaming-farsi-onnx | OpenMDW-1.1 (مشتق mehdi-hf/nemotron-asr-streaming-farsi، بررسی شد) | بررسی شد، **تست نشد**. کارت مدل: WER ۲۷٫۹٪ (fp32) و ۲۹٫۶٪ (int8) روی یک کلیپ مکالمه‌ای ۱۴۳ ثانیه‌ای. روی همان کلیپ Shenava Koochik 114M به ۳۴٫۷٪ رسیده (گزارش کارت مدل). پس «بهترین» بودن فقط روی آن کلیپ و به گزارش نویسنده است |
| alifarrokh/persian-asr | github.com/alifarrokh/persian-asr | بررسی نشد | بررسی شد. wav2vec2-xls-r-300m-fa با WER ۲۷٫۹۲٪ بدون LM روی تست نویسنده. **لینک HF در نسخه‌ی قبلی (huggingface.co/alifarrokh/persian-asr) ۴۰۴ می‌دهد.** در PESTE، نسخه‌ی HF با نام `alifarokh/wav2vec2-xls-r-300m-fa` روی FLEURS کامل WER ۳۶٫۳۶٪ گرفت (مجموعه‌ی تست دیگر) |
| anti-vocale (issue #105) | github.com/RisorseArtificiali/anti-vocale | بررسی نشد | بررسی شد (issue بسته‌شده در ۲۰۲۶-۰۹-۱۸). Shenava v1.5 در اپ موبایل: WER ۱۵٫۹٪ روی ۱۰ کلیپ FLEURS فارسی با نرمال‌ساز استاندارد، و ۱۳٫۳٪ با نرمال‌سازی آگاه از ZWNJ |
| persian-speech-toolkit | github.com/Omidbn2000/persian-speech-toolkit | **فایل LICENSE ندارد** (API: ۴۰۴) | بررسی شد. README به Shenava و Mana-Persian-Piper (TTS) ارجاع می‌دهد. مدل‌های وابسته: Apache-2.0 (طبق کارت‌ها) |
| FLEURS fa_ir | huggingface.co/datasets/google/fleurs | بررسی نشد | **استفاده شد** برای تست. datasets-server برای این زیرمجموعه خطای ۵۰۰ داد؛ فایل‌های خام از `resolve/main` گرفته شد |

### بنچمارک‌ها و مقالات

- **PSRB** (arXiv 2505.21230، لایسنس مقاله CC BY-NC-SA 4.0): **بررسی شد**. ۳٬۳۷۲ کلیپ، میانگین ۱۱ ثانیه، ۱۰٫۴ ساعت. جدول ۴ مقاله: Avanegar (تجاری) CER ۸٫۷۵٪ و WER ۱۹٫۳۰٪؛ Chirp v2 (تجاری چندزبانه) WER ۱۹٫۹۲٪؛ بهترین متن‌باز Faster-Whisper large-v3 با CER ۱۳٫۷۲٪ و WER ۳۳٫۹۳٪. **محدودیت لایسنس:** غیرتجاری.
- **PARSA-Bench** (arXiv 2603.14456، CC BY 4.0، نسخه‌ی v2): **بررسی شد**. ۱۶ وظیفه، ۸ مدل صوتی-زبانی. یافته‌ها: مدل‌های متنی روی بیشتر وظایف از معادل صوتی بهترند؛ شعر (سبک و وزن) استثنا است و صوت بهتر عمل می‌کند. Qwen3-Omni-30B در جدول ۱۲ بدون collapse است. Gemma-3n-E2B در paralinguistics نزدیک شانس است (بخش ۶٫۶). Gemma-3n-E4B روی speech understanding از Qwen2.5-Omni-7B بهتر شد (بخش ۶٫۷). **برتری Qwen3-Omni-30B به‌عنوان «بهترین ASR متن‌باز» بررسی نشد**؛ جدول ۳ کامل خوانده نشد. بخش اخلاق: مجموعه برای پژوهش غیرتجاری.
- **PESTE-Benchmark** (github.com/ArmanJR/PESTE-Benchmark، نسخه‌ی ۲٫۱٫۰): **بررسی شد**. فایل `asr-models-on-hf.md` می‌گوید: **۸۲ مخزن HF مرتبط با ASR فارسی تا ۱ اوت ۲۰۲۶** (۶۸ مخزن مخصوص فارسی و ۱۴ مدل چندزبانه). جدول رتبه‌بندی روی FLEURS fa_ir (۸۷۱ کلیپ، GPU RTX 6000 Ada، CER اصلی):
  - whisper-persian-v4 (nezamisafa): CER ۴٫۹۷٪، WER ۱۳٫۱۸٪ (رتبه‌ی ۱)
  - visualears-fastconformer-fa (Reza2kn): CER ۵٫۱۸٪، WER ۱۵٫۵۲٪
  - Shenava-Rizeh v1.0 (Reza2kn): CER ۶٫۴۰٪، WER ۱۵٫۵۵٪
  - whisper-large-v3: CER ۵٫۹۷٪، WER ۲۰٫۳۷٪
  - Qwen3-ASR-1.7B: CER ۸٫۹۲٪، WER ۲۴٫۱۰٪
  - whisper-small (openai): WER ۶۱٫۳۰٪؛ whisper-medium (openai): WER ۴۳٫۱۶٪
  - nvidia-fastconformer-fa: CER ۲۶٫۴۶٪، WER ۴۴٫۶۱٪
  - **Shenava Koochik (v1.0 یا v1.5) در جدول ۴۲ مدل نیست.** لایسنس PESTE: بررسی نشد.

### ویدیو و تصویر (VLM)

| ابزار / مدل | لایسنس | وضعیت |
|---|---|---|
| SmolVLM2-500M-Video-Instruct | Apache-2.0 (کارت مدل بررسی شد) | **تست شد**: ~۳٫۴ برابر زمان واقعی روی ۲ vCPU |
| Qwen2.5-Omni-3B GGUF (ggml-org) | در کارت دیده نشد | بررسی شد. ورودی‌ها: متن، صوت، تصویر، **بدون ویدیو**. ادعای توهم روی صوت طولانی تأیید نشد |
| llama.cpp-omni (tc-mb) | MIT (بررسی شد) | بررسی شد. موتور omni با full-duplex |
| Florence-2-base (microsoft) | بررسی نشد | **استفاده شد** برای توصیف تصویر (`vision.yml`، خروجی `refs/deck_desc.json`) |
| Gemma 3n | بررسی نشد | برای ASR فارسی مناسب نیست (یافته‌ی ۱) |

### ربات، گیت‌وی و تلگرام

| ابزار | لایسنس | وضعیت |
|---|---|---|
| python-telegram-bot ۲۱٫۶ | **GPL-3.0** (API ریپو بررسی شد) | **استفاده شد**. نصب و import تست شد، اجرای زنده نشد. نکته: کد ربات GPL می‌گیرد |
| Hermes Agent (NousResearch) | MIT (بررسی شد) | بررسی شد. Gateway تلگرام، allowlist، STT، Local Bot API |
| OpenClaw (openclaw/openclaw) | MIT (README بررسی شد) | بررسی شد. سقف ورودی media تلگرام ۵ MB (از مستندات، بازبینی نشد) |
| overpod/openclaw-channel-telegram-userbot | MIT (README) | بررسی شد. Userbot با GramJS روی MTProto |
| openclaw/telecrawl | بررسی نشد | بررسی شد. CLI با Go که آرشیو tdata/Postbox دسکتاپ را به SQLite می‌برد (ربات نیست) |
| tdlib/telegram-bot-api (Local Bot API) | BSL-1.0 (بررسی شد) | بررسی شد. برای فایل‌های بزرگ‌تر از ۲۰ MB، نیاز به api_id و api_hash |
| GeiserX/Telegram-Archive | GPL-3.0 (بررسی شد) | بررسی شد. بک‌آپ اکانت با Telethon و viewer محلی |
| FALKON-CODE/Telegram-Mirror | **فایل LICENSE ندارد** (API: ۴۰۴) | بررسی شد. relay کانال عمومی با t.me/s در Actions |

### استنتاج و معماری (تحقیق)

- **antirez/ds4:** موتور استنتاج محلی برای Metal، CUDA و ROCm (README بررسی شد). ایده‌های قابل استفاده: کش نتیجه با کلید hash محتوا، و overlap کردن I/O با محاسبه. عدد RAM مورد نیاز در این بررسی تأیید نشد، ولی به سخت‌افزار GPU یا حافظه‌ی زیاد وابسته است؛ استفاده‌ی مستقیم روی CPU ساده نیست.
- **Anemll/ds4-ssd:** کش prefix با کلید SHA1 که بین ری‌استارت‌ها بماند.

### ساخت پاورپوینت و دک (native)

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| ppt-master | github.com/hugohe3/ppt-master | MIT (بررسی شد) | **استفاده شد**. تبدیل اسلایدهای SVG به pptx بومی با انتقال و انیمیشن. نصب با `edu-agent/tools/pptx/setup.sh` (کلون در `edu-agent/vendor/`، که در این checkout نیست). دستورکار در `tools/pptx/RECIPE.md` |
| python-pptx | github.com/scanny/python-pptx | MIT (بررسی شد) | **استفاده شد**. نمودار بومی و بازنویسی روابط تصویر در `tools/deck/finale_build.py` |
| morph (انتقال Morph پاورپوینت) | - | - | **استفاده شد**. ۵ اسلاید با زنجیره‌ی morph در `artifacts/morph/morph.pptx` (معیار کیفیت) |
| LibreOffice Impress + poppler | - | بررسی نشد | **استفاده شد**. رندر pptx به PNG در `.github/workflows/deckrender.yml` |
| `tools/pptx/qa_overlap.py` | در repo | - | **استفاده شد**. QC همپوشانی و لی‌اوت |
| `tools/pptx/profile.py` | در repo | - | **استفاده شد**. پروفایل رنگ و تصویر اسلاید |
| matplotlib | - | بررسی نشد | **استفاده شد**. نمودار مقایسه‌ی گیت‌وی (`telegram-pipeline/docs/make_gateway_chart.py`) |

### سه‌بعدی و تصویر

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| Blender (bpy) | apt `blender` | GPL (بررسی نشد) | **استفاده شد**. ساخت ماشین F1 رویه‌ای در `tools/3d/build_f1_car.py` و turntable در `render_turntable.py` (workflow: `f1car.yml`) |
| TripoSR | github.com/VAST-AI-Research/TripoSR | MIT (بررسی شد) | **آزمایش شد** با `tools/3d/mesh_from_image.py` و `run_pipeline.sh` (workflow: `render3d.yml`). این مسیر کنار گذاشته شد |
| rembg | github.com/danielgatis/rembg | MIT (بررسی شد) | **استفاده شد** برای حذف پس‌زمینه‌ی تصویر پیش از TripoSR |
| shim torchmcubes | در repo | - | **استفاده شد** (`tools/3d/shim/torchmcubes.py`) |

### ویدیو، مرورگر و ابزارهای کمکی

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| Playwright (1.48.0) + Chromium | github.com/microsoft/playwright | بررسی نشد | **استفاده شد**. رندر کتاب و دک در `persianbook.yml`، `netbrowse.yml`، `netexport.yml` |
| edge-tts | github.com/rany2/edge-tts | **LGPL-3.0** (فایل `srt_composer.py` با MIT؛ بررسی شد) | **استفاده شد**. روایت فارسی در `tools/tts.py` و `persianbook.yml` (با `uv run --with edge-tts`) |
| uv | github.com/astral-sh/uv | بررسی نشد | **استفاده شد** برای اجرای اسکریپت‌ها بدون نصب دائمی |
| tesseract-ocr | github.com/tesseract-ocr/tesseract | بررسی نشد | **استفاده شد** برای OCR فریم‌های ویدیو در `fetch-refs.yml` |
| tikwm API | tikwm.com | بررسی نشد | **استفاده شد** برای دانلود ویدیوی تیک‌تاک در `fetch-refs.yml` (ویدیوهای placeplate و yerra) |
| showtime | در repo (vendor، gitignored) | بررسی نشد | **استفاده شد** برای رندر ویدیوی آموزشی در `showtime.yml` |

### ابزارهای پایه

- **git و gh:** commit، push، workflow و issue روی GitHub. **استفاده شد.**
- **GitHub Actions:** اجرای Blender، TripoSR، Florence، VLM، ASR و رندرها روی runnerهای اوبونتو. **استفاده شد.** job بیشتر از ۶ ساعت اجرا نمی‌شود.
- **ffmpeg:** استخراج صدا، استخراج فریم، تکه‌کردن و برش ویدیو. **استفاده شد.**
- **Pillow، numpy، soundfile، jiwer:** پردازش تصویر و صوت و محاسبه‌ی WER. **استفاده شد.**
- **Google Drive:** آپلود فایل در My Drive ریشه. **استفاده شد.** دانلود جزئی با هدر `Range` ممکن است.

---

## ۳. نتایج اندازه‌گیری‌شده

### ASR فارسی (۱۲ کلیپ FLEURS fa_ir، ۲۰۷ ثانیه، ۲ vCPU)

| مدل | WER | RTF | یادداشت |
|---|---|---|---|
| faster-whisper small (int8) | 56.25٪ | 0.565 | |
| faster-whisper medium (int8) | 31.85٪ | 0.964 | |
| Shenava Koochik v1.0 (CTC) | **9.52٪** | 0.013 تا 0.045 | RTF شامل زمان لود مدل است |
| Shenava Koochik v1.5 (RNNT) | 10.12٪ | 0.018 | |

جدول کامل: `edu-agent/telegram-pipeline/asr-test/out/summary.md`.

**مقایسه با بنچمارک بزرگ‌تر (PESTE، ۸۷۱ کلیپ):** Whisper small و medium در نمونه‌ی ما (۵۶٪ و ۳۲٪) بهتر از PESTE (۶۱٪ و ۴۳٪) شدند، پس نمونه‌ی ۱۲ کلیپی احتمالاً آسان‌تر بوده است. این دو عدد را با هم قیاس نکنید؛ برای قضاوت نهایی روی Shenava، همان مجموعه‌ی بزرگ‌تر لازم است.

محدودیت‌ها: ۱۲ کلیپ، گفتار خوانده‌شده، بدون ارزیابی ITN و اعداد فارسی. تفاوت v1.0 و v1.5 معنادار نیست.

### VLM

- ویدیوی ۳ دقیقه‌ای، ۶۱۲ ثانیه با ۳ بخش ۶۰ ثانیه‌ای و ۸ فریم هر بخش، روی ۲ vCPU. خروجی: `edu-agent/telegram-bot/vlm-test/out/result.txt`.
- خروجی روی ویدیوی تست رنگی عمومی بود.
- تخمین بدون تست: حالت سبک‌تر (۴ فریم هر ۵ دقیقه) حدود ۲۰ دقیقه پردازش برای هر ساعت ویدیو. این عدد تست نشده است.

---

## ۴. تجربه‌ها و تله‌ها

1. `workflow_dispatch` روی شاخه‌ی غیرپیش‌فرض خطای 404 داد. برای تست، trigger روی `push` به مسیر مشخص کار کرد.
2. لاگ‌های Actions برای این مخزن با `gh run view --log` قابل خواندن نبود (EOF). نتیجه را در فایل داخل مخزن نوشتیم و commit کردیم. این روش کار کرد.
3. datasets-server برای `google/fleurs` fa_ir خطای 500 داد. فایل‌های خام از `resolve/main` کار کردند.
4. `wave` استاندارد پایتون WAV با float32 (format tag 3) را نمی‌خواند. `soundfile` کار کرد.
5. `sherpa_onnx.read_wave` در sherpa-onnx ۱٫۱۳٫۸ وجود ندارد. از `soundfile` استفاده شد.
6. streaming در sherpa-onnx برای NeMo CTC باگ fbank داشت (issue #4003 و PR #4004). در گزارش قبلی آمده بود WER از ~۴۰٪ به ~۱۱٫۶٪ رسید؛ این عدد در این بررسی بازبینی نشد. مسیر offline درست بود.
7. torch از index CPU و torchvision از PyPI ناسازگار شدند. این مشکل با نصب هر دو از `https://download.pytorch.org/whl/cpu` حل شد.
8. SmolVLM2 برای ویدیو به `torchvision.io.read_video` نیاز دارد که در torchvision جدید نیست. فریم JPEG با ffmpeg کار کرد. `num2words`، `pillow` و `av` هم لازم بودند.
9. `gh repo edit --accept-visibility-change-consequences` در این نسخه‌ی gh وجود ندارد. تغییر visibility با همان دسترسی‌های sandbox ممکن نبود؛ مخزن از قبل عمومی بود.
10. یک اجرای بعدی `results.json` را بازنویسی کرد و نتیجه‌ی Whisper پاک شد. نتیجه‌ی کامل در `asr-test/out/summary.md` است.
11. عدد RTF در ابتدا با زمان لود مدل قاطی شد. برای عدد دقیق، زمان decode را جدا اندازه بگیرید.
12. شماره‌ی PR/issue و نام ریپو را از جستجو به‌تنهایی نگیرید. در این بررسی، لینک HF یک مدل (alifarrokh) ۴۰۴ داد و نام نزدیک دیگری (alifarokh) در بنچمارک بود. قبل از ارجاع، API یا صفحه‌ی ریپو را باز کنید.

---

## ۵. وضعیت باز

- **ربات تلگرام:** کد در `edu-agent/telegram-bot/` هست ولی فعال نیست. نیاز به merge روی شاخه‌ی پیش‌فرض، تنظیم secrets و تست زنده دارد. فعلاً متوقف است.
- **VLM:** وصل به ربات نشده. حالت «کامل» (هر ۶۰ ثانیه، ۸ فریم) هر job شش‌ساعته فقط حدود ۱٫۵ ساعت ویدیو را پوشش می‌دهد. برای ویدیوهای طولانی‌تر به صف کار پس‌زمینه نیاز دارد.
- **تحلیل کانال‌های عمومی:** مالک این مسیر را با اطلاع از شرایط تلگرام انتخاب کرد. ماژولی ساخته نشده است.
- **Local Bot API:** برای فایل‌های بزرگ‌تر از ۲۰ MB پیاده نشده.
- **ارزیابی ASR:** روی مجموعه‌ی بزرگ‌تر (مثلاً ۸۷۱ کلیپ FLEURS) و روی صدای ویدیو انجام نشده.
- **لایسنس‌های «بررسی نشد»:** Florence-2، Qwen2.5-Omni GGUF، PESTE، anti-vocale، telecrawl، Playwright، uv، tesseract، tikwm، showtime، و FLEURS. قبل از استفاده‌ی تجاری یا انتشار، هرکدام را از منبع اولیه تأیید کنید.
- **بنچمارک‌های بررسی‌نشده:** جدول ۳ مقاله‌ی PARSA (برتری Qwen3-Omni به‌عنوان بهترین ASR متن‌باز) و عددهای PSRB برای Gemma و Qwen (در این گزارش نیامده‌اند).

---

## ۶. زمینه‌ی مالک (گزارش، نه قانون)

- زبان کار فارسی است.
- ترجیح مالک: پرسش‌های کوتاه و ساده با گزینه‌ی مشخص.
- برای تحقیق، جستجوی عمیق (حدود ۳۰ دقیقه) و منبع مشخص مورد انتظار است.
- مالک vendor API نمی‌خواهد؛ مدل‌ها و ابزارهای باز ترجیح داده می‌شوند.
- ویدیوهای مرجع را مالک دیده و سبک را از روی ویدیو گرفته است.
- نتیجه‌ها روی remote ذخیره شده‌اند، چون sandbox ممکن است ریست شود.
