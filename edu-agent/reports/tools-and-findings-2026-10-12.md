# گزارش ابزارها و یافته‌ها برای ایجنت مستقل بعدی

تاریخ: 2026-10-12 · مخزن: `Kimfandogh7/Repo` (عمومی) · شاخه‌ی کاری: `arena/758efc2d-repo`

این گزارش برای یک ایجنت مستقل نوشته شده که مغز خودش را دارد. هدفش دادن اطلاعات است: چه ابزارهایی پیدا شد، چه چیزی واقعاً اندازه‌گیری شد، چه چیزی فقط بررسی شد، و چه تجربه‌هایی در عمل به دست آمد. تصمیم‌گیری با خود ایجنت است.

---

## ۱. خلاصه‌ی یافته‌ها

1. **برای ASR فارسی روی CPU، Shenava Koochik v1.0 (sherpa-onnx) بهترین نتیجه‌ی اندازه‌گیری‌شده است:** WER ۹٫۵۲٪ روی ۱۲ کلیپ FLEURS فارسی، RTF حدود ۰٫۰۱ تا ۰٫۰۵ روی ۲ vCPU. Whisper medium با WER ۳۱٫۸۵٪ و RTF ۰٫۹۶ در همان شرایط بسیار کندتر و کم‌دقت‌تر بود. نمونه کوچک است، پس این عدد قطعی نیست.
2. **VLM کوچک (SmolVLM2-500M) روی CPU کند است:** روی ۲ vCPU حدود ۳٫۴ برابر زمان واقعی. یعنی برای تحلیل تصویری ساعت‌ها ویدیو روی یک runner محدود، کافی نیست. کیفیت توصیف روی ویدیوی واقعی سنجیده نشده.
3. **مدل‌های Gemma 3n برای فارسی مناسب نیستند.** در بنچمارک PARSA-Bench، حدود ۱۲ تا ۱۳٪ جمله‌ها در حلقه‌ی تکرار گیر کردند و همین‌ها ۸۲ تا ۸۶٪ از میانگین WER را ساختند.
4. **Actions برای سرویس دائمی محدودیت دارد:** هر job حداکثر ۶ ساعت است. در مخزن عمومی runnerهای استاندارد رایگان‌اند. در مخزن خصوصی، اجرای ۲۴ ساعته حدود ۲۴۷ دلار در ماه برای ۴۳٬۲۰۰ دقیقه (با ۲٬۰۰۰ دقیقه‌ی رایگان و نرخ ۰٫۰۰۶ دلار) هزینه دارد.
5. **قوانین تلگرام برای AI محدودکننده است:** شرایط محتوای تلگرام (از ۳ فوریه‌ی ۲۰۲۶) استفاده از داده‌های پلتفرم برای توسعه یا استقرار مدل‌های AI را منع کرده است، مگر برای راه‌اندازی ربات یا با رضایت صریح همه‌ی کاربران مربوط. این موضوع روی مسیرهای تحلیل کانال‌های عمومی اثر مستقیم دارد.

---

## ۲. ابزارها و مدل‌ها

### گفتار و ASR فارسی

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| sherpa-onnx ۱٫۱۳٫۸ | github.com/k2-fsa/sherpa-onnx | Apache-2.0 | **تست شد**. پشتیبانی از Persian NeMo CTC از نسخه‌ی ۱٫۱۳٫۵. |
| Shenava Koochik v1.0 (CTC) | `Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx` | Apache-2.0 | **تست شد**: WER ۹٫۵۲٪ |
| Shenava Koochik v1.5 (RNNT) | `Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx` | Apache-2.0 | **تست شد**: WER ۱۰٫۱۲٪ |
| faster-whisper (small، medium) | github.com/SYSTRAN/faster-whisper | مشخص نشد | **تست شد**: WER به ترتیب ۵۶٫۲۵٪ و ۳۱٫۸۵٪ |
| Nimaone/nemotron-asr-streaming-farsi-onnx | huggingface.co/Nimaone/nemotron-asr-streaming-farsi-onnx | مشخص نشد | بررسی شد. مدل ۶۰۰ میلیونی streaming، WER ۲۷٫۹ تا ۲۹٫۶٪ روی تست خودش |
| alifarrokh/persian-asr | huggingface.co/alifarrokh/persian-asr | مشخص نشد | بررسی شد. wav2vec2 XLS-R 300M با WER ۲۷٫۹۲٪ بدون LM |
| anti-vocale (issue #105) | github.com/RisorseArtificiali/anti-vocale | مشخص نشد | بررسی شد. Shenava v1.5 در اپ موبایل با WER ۱۵٫۹٪ روی ۱۰ کلیپ |
| persian-speech-toolkit | github.com/Omidbn2000/persian-speech-toolkit | بدون لایسنس (مدل‌ها Apache-2.0) | بررسی شد. VAD + Shenava + TTS |
| FLEURS fa_ir | huggingface.co/datasets/google/fleurs | مشخص نشد | **استفاده شد** برای تست |

### بنچمارک‌ها و مقالات

- **PSRB** (arxiv 2505.21230): ۳٬۳۷۲ کلیپ. بهترین نتیجه از Avanegar (تجاری، CER ۸٫۷۵٪)، و بهترین متن‌باز Faster-Whisper با WER ۳۳٫۹۳٪.
- **PARSA-Bench** (arxiv 2603.14456): بنچمارک مدل‌های صوتی-زبانی فارسی. Qwen3-Omni-30B بهترین ASR متن‌باز است ولی بزرگ است. Gemma 3n در فارسی تکرار حلقه‌ای دارد.
- **PESTE-Benchmark** (ArmanJR): فهرست ۸۲ مدل ASR فارسی روی Hugging Face تا ۱ اوت ۲۰۲۶.

### ویدیو و تصویر (VLM)

| ابزار / مدل | لایسنس | وضعیت |
|---|---|---|
| SmolVLM2-500M-Video-Instruct | مشخص نشد (ادعا: Apache-2.0) | **تست شد**: حدود ۳٫۴ برابر زمان واقعی روی ۲ vCPU |
| Qwen2.5-Omni-3B GGUF (ggml-org) | مشخص نشد | بررسی شد. صدا و تصویر، بدون ویدیو. گزارش‌ها از توهم روی صوت طولانی حرف می‌زنند |
| llama.cpp-omni (tc-mb) | MIT | بررسی شد |
| Gemma 3n | - | برای فارسی مناسب نیست |

### ربات، گیت‌وی و تلگرام

| ابزار | لایسنس | وضعیت |
|---|---|---|
| python-telegram-bot ۲۱٫۶ | - | **استفاده شد**. نصب و import تست شد، اجرای زنده نشد |
| Hermes Agent (NousResearch) | MIT | بررسی شد. Gateway تلگرام، حافظه، skill، cron |
| OpenClaw | مشخص نشد | بررسی شد. سقف media تلگرام ۵ MB |
| openclaw-channel-telegram-userbot | MIT | بررسی شد. کانال MTProto |
| telecrawl (openclaw) | MIT | بررسی شد. خواندن Telegram Desktop tdata |
| tdlib/telegram-bot-api (Local Bot API) | BSL-1.0 | بررسی شد. برای فایل‌های بزرگ‌تر از ۲۰ MB، نیاز به api_id و api_hash |
| GeiserX/Telegram-Archive | GPL-3.0 | بررسی شد. بک‌آپ اکانت با Telethon |
| FALKON-CODE/Telegram-Mirror | مشخص نشد | بررسی شد. relay کانال عمومی با t.me/s در Actions |

### استنتاج و معماری (تحقیق)

- **antirez/ds4:** ایده‌های قابل استفاده: کش نتایج با کلید hash محتوا، و overlap کردن I/O و محاسبه. به Metal یا CUDA و ۹۶ تا ۱۲۸ GB RAM نیاز دارد، پس مستقیم قابل استفاده نیست.
- **Anemll/ds4-ssd:** کش prefix با کلید SHA1 که بین ری‌استارت‌ها بماند.

### ساخت پاورپوینت و دک (native)

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| ppt-master | github.com/hugohe3/ppt-master | MIT | **استفاده شد**. اسلایدهای SVG به pptx بومی با انتقال و انیمیشن تبدیل می‌شوند. نصب با `edu-agent/tools/pptx/setup.sh` (کلون در `edu-agent/vendor/`، که در این checkout نیست). دستورکار در `tools/pptx/RECIPE.md` |
| python-pptx | github.com/scanny/python-pptx | MIT | **استفاده شد**. ساخت نمودار بومی و بازنویسی روابط تصویر در `tools/deck/finale_build.py` |
| morph (انتقال Morph پاورپوینت) | - | - | **استفاده شد**. ۵ اسلاید با زنجیره‌ی morph در `artifacts/morph/morph.pptx` (معیار کیفیت) |
| LibreOffice Impress + poppler | - | MPL-2.0 (LibreOffice) | **استفاده شد**. رندر pptx به PNG در `.github/workflows/deckrender.yml` |
| `tools/pptx/qa_overlap.py` | در repo | - | **استفاده شد**. QC همپوشانی و لی‌اوت |
| `tools/pptx/profile.py` | در repo | - | **استفاده شد**. پروفایل رنگ و تصویر اسلاید |
| matplotlib | - | PSF | **استفاده شد**. نمودار مقایسه‌ی گیت‌وی (`telegram-pipeline/docs/make_gateway_chart.py`) |

### سه‌بعدی و تصویر

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| Blender (bpy) | apt `blender` | GPL | **استفاده شد**. ساخت ماشین F1 رویه‌ای در `tools/3d/build_f1_car.py` و turntable در `render_turntable.py` (workflow: `f1car.yml`) |
| TripoSR | github.com/VAST-AI-Research/TripoSR | MIT | **آزمایش شد** با `tools/3d/mesh_from_image.py` و `run_pipeline.sh` (workflow: `render3d.yml`). مسیر کنار گذاشته شد |
| rembg | github.com/danielgatis/rembg | MIT | **استفاده شد** برای حذف پس‌زمینه‌ی تصویر پیش از TripoSR |
| shim torchmcubes | در repo | - | **استفاده شد** (`tools/3d/shim/torchmcubes.py`) |
| Florence-2-base | huggingface.co/microsoft/Florence-2-base | بررسی نشد | **استفاده شد** برای توصیف تصویر در `.github/workflows/vision.yml` (خروجی: `refs/deck_desc.json`) |

### ویدیو، مرورگر و صدای کمکی

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| Playwright (1.48.0) + Chromium | github.com/microsoft/playwright | Apache-2.0 | **استفاده شد**. رندر کتاب و دک در `persianbook.yml`، `netbrowse.yml`، `netexport.yml` |
| Edge TTS (edge-tts) | github.com/rany2/edge-tts | بررسی نشد | **استفاده شد**. روایت فارسی در `tools/tts.py` و `persianbook.yml` (با `uv run --with edge-tts`) |
| uv | github.com/astral-sh/uv | MIT/Apache-2.0 | **استفاده شد** برای اجرای اسکریپت‌ها بدون نصب دائمی |
| tesseract-ocr | github.com/tesseract-ocr/tesseract | Apache-2.0 | **استفاده شد** برای OCR فریم‌های ویدیو در `fetch-refs.yml` |
| tikwm API | tikwm.com | مشخص نشد | **استفاده شد** برای دانلود ویدیوی تیک‌تاک در `fetch-refs.yml` (ویدیوهای placeplate و yerra) |
| showtime | در repo (vendor، gitignored) | مشخص نشد | **استفاده شد** برای رندر ویدیوی آموزشی در `showtime.yml` |

### ابزارهای پایه

- **git و gh:** commit، push، workflow و issue روی GitHub. **استفاده شد.**
- **GitHub Actions:** اجرای Blender، TripoSR، Florence، VLM، ASR و رندرها روی runnerهای اوبونتو. **استفاده شد.** کارهای سنگین‌تر از ۶ ساعت ممکن نیست.
- **ffmpeg:** استخراج صدا، استخراج فریم، تکه‌کردن و برش ویدیو. **استفاده شد.**
- **Pillow، numpy، soundfile، jiwer:** پردازش تصویر و صوت و محاسبه‌ی WER. **استفاده شد.**
- **Google Drive:** آپلود فایل در My Drive ریشه. **استفاده شد.** دانلود جزئی با هدر `Range` ممکن است.

---

## ۳. نتایج اندازه‌گیری‌شده

### ASR فارسی

| مدل | WER | RTF | یادداشت |
|---|---|---|---|
| faster-whisper small (int8) | 56.25٪ | 0.565 | ۲ vCPU |
| faster-whisper medium (int8) | 31.85٪ | 0.964 | ۲ vCPU |
| Shenava Koochik v1.0 (CTC) | **9.52٪** | 0.013 تا 0.045 | RTF شامل زمان لود مدل است |
| Shenava Koochik v1.5 (RNNT) | 10.12٪ | 0.018 | |

محدودیت‌ها: ۱۲ کلیپ، گفتار خوانده‌شده، بدون ارزیابی ITN و اعداد فارسی. تفاوت v1.0 و v1.5 معنادار نیست.

### VLM

- ویدیوی ۳ دقیقه‌ای، ۶۱۲ ثانیه با ۳ بخش ۶۰ ثانیه‌ای و ۸ فریم هر بخش. روی ۲ vCPU.
- خروجی روی ویدیوی تست رنگی عمومی بود.
- تخمین بدون تست: حالت ۴ فریم هر ۵ دقیقه حدود ۲۰ دقیقه پردازش برای هر ساعت ویدیو.

---

## ۴. تجربه‌ها و تله‌ها

1. `workflow_dispatch` روی شاخه‌ی غیرپیش‌فرض خطای 404 می‌دهد. برای تست، از trigger روی `push` به مسیر مشخص استفاده کنید.
2. لاگ‌های Actions برای این مخزن قابل خواندن نبودند. نتیجه را در فایل داخل مخزن نوشتیم و commit کردیم. این روش کار کرد.
3. datasets-server برای `google/fleurs` fa_ir خطای 500 داد. فایل‌های خام از `resolve/main` کار کردند.
4. `wave` استاندارد پایتون WAV با float32 (tag 3) را نمی‌خواند. `soundfile` کار کرد.
5. `sherpa_onnx.read_wave` در sherpa-onnx ۱٫۱۳٫۸ وجود ندارد.
6. streaming در sherpa-onnx برای NeMo CTC باگ fbank داشت (issue #4003 و PR #4004: WER از ~۴۰٪ به ~۱۱٫۶٪). مسیر offline درست بود.
7. torch از index CPU و torchvision از PyPI ناسازگار شدند. هر دو را از `https://download.pytorch.org/whl/cpu` نصب کنید.
8. SmolVLM2 برای ویدیو به `torchvision.io.read_video` نیاز دارد که در torchvision جدید نیست. فریم JPEG با ffmpeg کار کرد. `num2words`، `pillow` و `av` هم لازم بودند.
9. `gh repo edit --accept-visibility-change-consequences` در این نسخه‌ی gh وجود ندارد.
10. یک اجرای بعدی `results.json` را بازنویسی کرد و نتیجه‌ی Whisper پاک شد. نتیجه‌ی کامل در `asr-test/out/summary.md` است.
11. عدد RTF در ابتدا با زمان لود مدل قاطی شد. برای عدد دقیق، زمان decode را جدا اندازه بگیرید.

---

## ۵. وضعیت باز

- **ربات تلگرام:** کد در `edu-agent/telegram-bot/` هست ولی فعال نیست. نیاز به merge روی شاخه‌ی پیش‌فرض، تنظیم secrets و تست زنده دارد.
- **VLM:** وصل به ربات نشده. برای حالت «کامل» (هر ۶۰ ثانیه، ۸ فریم) هر job شش‌ساعته فقط حدود ۱٫۵ ساعت ویدیو را پوشش می‌دهد. نیاز به صف کار پس‌زمینه دارد.
- **تحلیل کانال‌های عمومی:** مالک این مسیر را انتخاب کرد، با اطلاع از شرایط تلگرام. ماژولی ساخته نشده است.
- **Local Bot API:** برای فایل‌های بزرگ‌تر از ۲۰ MB پیاده نشده.
- **ارزیابی ASR:** روی نمونه‌ی بزرگ‌تر و صدای ویدیو انجام نشده.

---

## ۶. زمینه‌ی مالک

- زبان کار فارسی است.
- پرسش‌ها باید کوتاه و ساده، با گزینه‌ی مشخص باشند.
- برای تحقیق، جستجوی عمیق (حدود ۳۰ دقیقه) و منبع مشخص مورد انتظار است.
- API فروشنده‌ها (vendor API) مورد نظر نیست؛ مدل‌ها و ابزارهای باز ترجیح داده می‌شوند.
- ویدیوهای مرجع را مالک دیده و سبک را از روی ویدیو گرفته است.
- نتیجه‌ها باید روی remote باشند، چون sandbox ممکن است ریست شود.
