# کاتالوگ ریپوها، ابزارها و نتایج برای ایجنت بعدی

تاریخ: 2026-10-12 · شاخه: `arena/758efc2d-repo` · مخزن: `Kimfandogh7/Repo` (عمومی؛ `isPrivate=false`)

این فایل یک کاتالوگ است، نه مجموعه دستور. ایجنت بعدی مغز مستقل دارد و خودش تصمیم می‌گیرد. هر ریپو، مدل، ابزار و نتیجه‌ای که این‌جا آمده، با وضعیت آن ثبت شده است: **تست شد** (روی این مخزن اجرا شد)، **بررسی شد** (از منبع اولیه خوانده شد)، یا **بررسی نشد** (هنوز با منبع تأیید نشده). نسخه‌ی کامل‌تر با جزئیات بیشتر: `edu-agent/reports/tools-and-findings-2026-10-12.md`.

قبل از کار، شاخه‌ی محلی را همگام کنید: `git fetch && git merge --ff-only origin/arena/758efc2d-repo`. در این نشست شاخه‌ی محلی یک بار عقب مانده بود.

---

## ۱. وضعیت مخزن

- مخزن عمومی است. تغییر visibility در این نشست 403 داد، ولی بعداً معلوم شد قبلاً عمومی شده است.
- تاریخچه‌ی مخزن فریم‌های ویدیوی تیک‌تاک (`refs/dense/placeplate/`) را دارد. مالک حذف آن‌ها از تاریخچه را رد کرده است.
- Workflowها در `.github/workflows/`. workflow_dispatch فقط روی شاخه‌ی پیش‌فرض کار می‌کند؛ روی شاخه‌ی کاری از trigger روی push استفاده شده است.

---

## ۲. ریپوهای اوپن‌سورس و ابزارهای خارجی

### الف) گفتار و ASR فارسی

| ابزار / مدل | منبع | لایسنس | وضعیت در این کار |
|---|---|---|---|
| sherpa-onnx | github.com/k2-fsa/sherpa-onnx | Apache-2.0 (بررسی شد) | **استفاده شد** (نسخه‌ی `1.13.8` روی PyPI). از نسخه‌ی ۱٫۱۳٫۵ مدل‌های Persian NeMo CTC را دارد. |
| Shenava Koochik v1.0 (sherpa-onnx) | `Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx` | Apache-2.0 (کارت مدل بررسی شد) | **تست شد**: WER ۹٫۵۲٪ روی ۱۲ کلیپ. کارت: غیرفعال‌کردن per-feature normalization لازم است. |
| Shenava Koochik v1.5 (RNNT) | `Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx` | Apache-2.0 (بررسی شد) | **تست شد**: WER ۱۰٫۱۲٪ روی ۱۲ کلیپ. |
| Shenava Koochik v1.0 ONNX fp16 | `Reza2kn/Shenava-Koochik-v1.0-ONNX-fp16` | بررسی نشد | فقط دیده شد. |
| Nimaone/nemotron-asr-streaming-farsi-onnx | `huggingface.co/Nimaone/nemotron-asr-streaming-farsi-onnx` | OpenMDW-1.1 (کارت بررسی شد؛ مشتق mehdi-hf/nemotron-asr-streaming-farsi) | بررسی شد، **تست نشد**. کارت: WER ۲۷٫۹٪ (fp32) و ۲۹٫۶٪ (int8) روی یک کلیپ مکالمه‌ای ۱۴۳ ثانیه‌ای. روی همان کلیپ، Shenava Koochik 114M به ۳۴٫۷٪ رسیده (گزارش کارت). «بهترین» بودن فقط روی آن کلیپ و به گزارش نویسنده است. |
| faster-whisper (SYSTRAN) | github.com/SYSTRAN/faster-whisper | MIT (README بررسی شد) | **تست شد** (small و medium، int8). |
| alifarrokh/persian-asr | `github.com/alifarrokh/persian-asr` | بررسی نشد | بررسی شد: wav2vec2-xls-r-300m-fa با WER ۲۷٫۹۲٪ بدون LM روی تست نویسنده. **لینک HF قبلی (`huggingface.co/alifarrokh/persian-asr`) ۴۰۴ می‌دهد.** در PESTE نسخه‌ی HF (`alifarokh/wav2vec2-xls-r-300m-fa`) روی FLEURS کامل WER ۳۶٫۳۶٪ گرفت. |
| anti-vocale (issue #105) | github.com/RisorseArtificiali/anti-vocale | بررسی نشد | بررسی شد: Shenava v1.5 در اپ موبایل، WER ۱۵٫۹٪ روی ۱۰ کلیپ FLEURS با نرمال‌ساز استاندارد؛ ۱۳٫۳٪ با نرمال‌سازی ZWNJ. |
| persian-speech-toolkit | github.com/Omidbn2000/persian-speech-toolkit | **فایل LICENSE ندارد** (API: ۴۰۴) | بررسی شد. README به Shenava و Mana-Persian-Piper (TTS) ارجاع می‌دهد. مدل‌های وابسته: Apache-2.0 (طبق کارت‌ها). |
| nvidia/stt_fa_fastconformer_hybrid_large (FC-Fa) | Hugging Face | بررسی نشد | در PESTE روی FLEURS کامل: WER ۴۴٫۶۱٪، CER ۲۶٫۴۶٪. در PSRB: CER ۱۹٫۴۲٪، WER ۴۴٫۸۵٪ (CTC). |
| speechbrain/asr-whisper-large-v2-commonvoice-fa | Hugging Face | بررسی نشد | ادعای WER ۳۱٫۷۵٪ روی CommonVoice 10 از کارت؛ بازبینی نشد. |
| FLEURS fa_ir | `google/fleurs` | بررسی نشد | **استفاده شد**: `data/fa_ir/test.tsv` و `audio/test.tar.gz` از `resolve/main`. datasets-server خطای 500 داد. |

### ب) بنچمارک‌ها و مقالات فارسی

- **PSRB** (arXiv 2505.21230، CC BY-NC-SA 4.0؛ بررسی شد): ۳٬۳۷۲ کلیپ، میانگین ۱۱ ثانیه، ۱۰٫۴ ساعت. Avanegar (تجاری) CER ۸٫۷۵٪ و WER ۱۹٫۳۰٪؛ Chirp v2 WER ۱۹٫۹۲٪؛ بهترین متن‌باز Faster-Whisper large-v3 با CER ۱۳٫۷۲٪ و WER ۳۳٫۹۳٪. **لایسنس غیرتجاری است.**
- **PARSA-Bench** (arXiv 2603.14456، CC BY 4.0؛ بررسی شد): ۱۶ وظیفه، ۸ مدل صوتی-زبانی. مدل‌های متنی روی بیشتر وظایف بهتر از معادل صوتی‌اند. در ASR، Gemma-3n-E2B در ۱۱٫۶٪ و Gemma-3n-E4B در ۱۳٫۴٪ از utteranceها حلقه‌ی تکرار داشتند و این‌ها ۸۲٪ و ۸۶٪ از میانگین WER را ساختند (جدول ۱۲). Qwen3-Omni-30B و سه مدل تجاری collapse نداشتند. **«بهترین ASR متن‌باز بودن Qwen3-Omni» بررسی نشد.**
- **PESTE-Benchmark** (github.com/ArmanJR/PESTE-Benchmark؛ v2.1.0؛ بررسی شد): فایل `asr-models-on-hf.md` می‌گوید **۸۲ مخزن HF مرتبط با ASR فارسی تا ۱ اوت ۲۰۲۶** (۶۸ مخصوص فارسی، ۱۴ چندزبانه). جدول رتبه‌بندی روی FLEURS fa_ir (۸۷۱ کلیپ، GPU، CER اصلی): whisper-persian-v4 CER ۴٫۹۷٪؛ visualears-fastconformer-fa CER ۵٫۱۸٪؛ Shenava-Rizeh v1.0 CER ۶٫۴۰٪ و WER ۱۵٫۵۵٪؛ whisper-large-v3 WER ۲۰٫۳۷٪؛ Qwen3-ASR-1.7B WER ۲۴٫۱۰٪؛ whisper-medium (openai) WER ۴۳٫۱۶٪؛ whisper-small (openai) WER ۶۱٫۳۰٪. **Shenava Koochik در این جدول نیست.** لایسنس PESTE: بررسی نشد.

### پ) ویدیو و تصویر (VLM)

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| **SmolVLM2-500M-Video-Instruct** | `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` | Apache-2.0 (کارت مدل بررسی شد) | **تست شد**. روی ۲ vCPU حدود ۳٫۴ برابر زمان واقعی. |
| SmolVLM2 (حداکثر ۶۴ فریم) | گفتگوی Hugging Face | - | گفته شد که ویدیو تا ۶۴ فریم نمونه‌برداری می‌شود (منبع ثانویه). |
| Qwen2.5-Omni-3B GGUF (ggml-org) | `ggml-org/Qwen2.5-Omni-3B-GGUF` | در کارت دیده نشد | بررسی شد. ورودی متن، صوت و تصویر؛ **بدون ویدیو**. ادعای توهم روی صوت طولانی تأیید نشد. |
| Qwen2.5-Omni | github.com/QwenLM/Qwen2.5-Omni | بررسی نشد | فقط دیده شد. |
| llama.cpp-omni | github.com/tc-mb/llama.cpp-omni | MIT (بررسی شد) | موتور omni با full-duplex. |
| Florence-2-base | `microsoft/Florence-2-base` | بررسی نشد | **استفاده شد** برای توصیف تصویر در `vision.yml`. |
| Gemma 3n | Google | - | **برای ASR فارسی مناسب نیست** (بخش ۲ب). |

### ت) ربات، گیت‌وی و تلگرام

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| python-telegram-bot ۲۱٫۶ | github.com/python-telegram-bot/python-telegram-bot | **GPL-3.0** (API ریپو بررسی شد) | **استفاده شد** در `edu-agent/telegram-bot/bot.py`. نصب و import تست شد؛ اجرای زنده نشد. کد ربات GPL می‌گیرد. |
| Hermes Agent | github.com/NousResearch/hermes-agent | MIT (بررسی شد) | بررسی شد. Gateway تلگرام، حافظه، skill، cron. |
| OpenClaw | github.com/openclaw/openclaw | MIT (README بررسی شد) | بررسی شد. سقف ورودی media تلگرام ۵ MB (از مستندات، بازبینی نشد). |
| overpod/openclaw-channel-telegram-userbot | github.com/overpod/openclaw-channel-telegram-userbot | MIT (README بررسی شد) | بررسی شد. Userbot با GramJS روی MTProto. |
| openclaw/telecrawl | github.com/openclaw/telecrawl | بررسی نشد | بررسی شد. CLI با Go که آرشیو tdata و Postbox دسکتاپ را به SQLite می‌برد. ربات نیست. |
| tdlib/telegram-bot-api (Local Bot API) | github.com/tdlib/telegram-bot-api | BSL-1.0 (بررسی شد) | بررسی شد. برای فایل‌های بزرگ‌تر از ۲۰ MB، نیاز به api_id و api_hash. پیاده نشد. |
| GeiserX/Telegram-Archive | github.com/GeiserX/Telegram-Archive | GPL-3.0 (بررسی شد) | بررسی شد. بک‌آپ اکانت با Telethon و viewer محلی. |
| FALKON-CODE/Telegram-Mirror | github.com/FALKON-CODE/Telegram-Mirror | **فایل LICENSE ندارد** (API: ۴۰۴) | بررسی شد. relay کانال عمومی با t.me/s در Actions. |
| ffmpeg | ffmpeg.org | LGPL/GPL | **استفاده شد** برای استخراج صدا، تکه‌کردن و برش ویدیو. |

### ث) استنتاج و معماری (تحقیق)

- **antirez/ds4** (github.com/antirez/ds4؛ README بررسی شد): موتور استنتاج محلی برای Metal، CUDA و ROCm. ایده‌های قابل استفاده: کش نتایج روی دیسک با کلید hash محتوا، و overlap کردن I/O و محاسبه. عدد RAM مورد نیاز تأیید نشد؛ استفاده‌ی مستقیم روی CPU ساده نیست.
- **Anemll/ds4-ssd**: کش prefix با کلید SHA1 که بین ری‌استارت‌ها بماند.
- **dwarfstar.sh** (گزارش benchmark): حالت streaming از SSD؛ بررسی نشد.

### ج) ابزارهای داخل همین مخزن

| مسیر | کاربرد | وضعیت |
|---|---|---|
| `edu-agent/telegram-pipeline/asr-test/persian_asr_test.py` | تست ASR فارسی برای Whisper و Shenava | استفاده شد |
| `edu-agent/telegram-pipeline/asr-test/out/summary.md` | جدول نهایی ASR | کامل |
| `edu-agent/telegram-pipeline/docs/make_gateway_chart.py` | چارت مقایسه‌ی رابط‌ها | کامل |
| `edu-agent/telegram-bot/bot.py` | ربات تلگرام (Shenava + ffmpeg) | نوشته شد، فعال نیست |
| `edu-agent/telegram-bot/vlm_describe.py` | توصیف ویدیو با SmolVLM2 (فریم JPEG) | تست شد، وصل نشد |
| `edu-agent/telegram-bot/README.md` | راه‌اندازی ربات | کامل |
| `.github/workflows/persian-asr.yml` | workflow تست ASR | استفاده شد |
| `.github/workflows/telegram-bot.yml` | ربات هر ۶ ساعت (concurrency) | فعال نیست |
| `.github/workflows/vlm-test.yml` | تست سرعت VLM | استفاده شد |
| `edu-agent/tools/deck/finale_build.py` | ساخت دک نهایی ۵ اسلایدی | قبلی |
| `edu-agent/tools/pptx/qa_overlap.py`، `profile.py` | QC لی‌اوت | قبلی |
| `edu-agent/tools/3d/build_f1_car.py` | ساخت ماشین F1 در Blender | قبلی |
| `edu-agent/tools/3d/` (TripoSR، `shim/torchmcubes.py`) | مسیر TripoSR | کنار گذاشته شده |
| `edu-agent/vendor/ppt-master/` | سورس ۱۶:۹ و عمودی Phase 4 و 5 | در این checkout نیست؛ `setup.sh` کلون می‌کند |
| `VISION.md` | مستند خط لوله‌ی دید برای اسلایدها | قبلی |
| `.github/workflows/deckrender.yml`، `vision.yml`، `f1car.yml` | رندر و توصیف با Florence | قبلی |
| `edu-agent/artifacts/morph/morph.pptx` | نمونه‌ی کف کیفیت دک (۵ اسلاید) | مرجع |

---

## ۳. نتایج اندازه‌گیری‌شده

### ASR فارسی (FLEURS fa_ir، ۱۲ کلیپ، ۲۰۷ ثانیه، ۲ vCPU)

| مدل | WER | RTF |
|---|---|---|
| faster-whisper small (int8) | 56.25٪ | 0.565 |
| faster-whisper medium (int8) | 31.85٪ | 0.964 |
| Shenava Koochik v1.0 (CTC، sherpa-onnx) | 9.52٪ | 0.013 تا 0.045 |
| Shenava Koochik v1.5 (RNNT، sherpa-onnx) | 10.12٪ | 0.018 |

محدودیت‌ها: نمونه کوچک است و احتمالاً آسان‌تر از مجموعه‌ی کامل. در PESTE (۸۷۱ کلیپ، GPU) Whisper small و medium به ترتیب ۶۱٫۳٪ و ۴۳٫۲٪ WER داشتند؛ پس قیاس مستقیم ممکن نیست. گفتار خوانده‌شده است، ITN و اعداد فارسی بررسی نشده، و RTF در یک اجرا با زمان لود مدل قاطی شده است. Shenava-Rizeh v1.0 (نزدیک‌ترین مدل در PESTE) WER ۱۵٫۵۵٪ گرفت، پس ۹٫۵۲٪ روی ۱۲ کلیپ احتمالاً خوش‌بینانه است.

### VLM (SmolVLM2-500M)

- یک ویدیوی ۳ دقیقه‌ای، ۶۱۲ ثانیه، با ۳ بخش ۶۰ ثانیه‌ای و ۸ فریم هر بخش. روی ۲ vCPU.
- خروجی روی ویدیوی تست رنگی عمومی بود. روی ویدیوی واقعی سنجیده نشده.
- تخمین، تأیید نشده: حالت ۴ فریم هر ۵ دقیقه حدود ۲۰ دقیقه پردازش برای هر ساعت ویدیو.

### هزینه‌ی GitHub Actions (مستندات رسمی)

- هر job حداکثر ۶ ساعت اجرا می‌شود ([Actions limits](https://docs.github.com/en/actions/reference/limits)).
- runnerهای استاندارد در مخزن عمومی رایگان‌اند؛ larger runnerها برای مخزن عمومی رایگان نیستند ([Actions runner pricing](https://docs.github.com/en/billing/reference/actions-runner-pricing)).
- در مخزن خصوصی، برای Linux 2-core نرخ ۰٫۰۰۶ دلار در دقیقه است؛ سهمیه‌ی رایگان ۲٬۰۰۰ دقیقه در ماه (جدول GitHub Free). اجرای ۲۴ ساعته (~۴۳٬۲۰۰ دقیقه) حدود ۲۴۷ دلار در ماه می‌شود (محاسبه: (۴۳٬۲۰۰ − ۲٬۰۰۰) × ۰٫۰۰۶).

### Telegram: قوانین

- [شرایط محتوای و AI تلگرام](https://telegram.org/tos/content-licensing): استفاده از داده‌های پلتفرم برای توسعه، آموزش، بنچمارک یا استقرار مدل‌های AI را منع کرده است. استثنا: داده‌ی لازم برای راه‌اندازی یک ربات یا کلاینت قانونی، یا رضایت صریح، آگاهانه و مداوم همه‌ی کاربران مربوط در همان چت یا کانال.
- شرایط API تلگرام (بند ۱٫۵) همین را تکرار می‌کند ([core.telegram.org/api/terms](https://core.telegram.org/api/terms)). بند ۱٫۵ در این بررسی باز نشد.
- این تغییر در ۲۰۲۶ ثبت شده است ([Open Terms Archive](https://opentermsarchive.org/en/memos/telegram-prohibits-collecting-data-for-ai-use/)). روز دقیق تأیید نشد.

---

## ۴. نکته‌های فنی که در عمل دیده شد

- `workflow_dispatch` روی شاخه‌ی غیرپیش‌فرض خطای 404 می‌دهد. برای تست، trigger روی `push` کار کرد.
- `gh run view --log` و API لاگ Actions برای این مخزن خالی برگشت. نتیجه را در فایل داخل مخزن نوشتیم و commit کردیم.
- datasets-server برای `google/fleurs` fa_ir خطای 500 داد. فایل‌های خام از `resolve/main` کار کردند.
- `wave` استاندارد پایتون WAV با فرمت float32 (tag 3) را نمی‌خواند؛ `soundfile` کار کرد.
- در `sherpa-onnx` 1.13.8 تابع `sherpa_onnx.read_wave` وجود ندارد.
- streaming در sherpa-onnx برای مدل‌های NeMo CTC باگ fbank داشت (issue #4003 و PR #4004). در گزارش قبلی آمده بود WER از ~۴۰٪ به ~۱۱٫۶٪ رسید؛ بازبینی نشد. مسیر offline درست بود.
- torch از index CPU و torchvision از PyPI ناسازگار بودند. هر دو را از یک index نصب کنید.
- SmolVLM2 processor ویدیو به `torchvision.io.read_video` نیاز دارد که در torchvision جدید نیست. فریم JPEG از ffmpeg کار کرد. همچنین `num2words`، `pillow` و `av` لازم بود.
- `gh repo edit --accept-visibility-change-consequences` در این نسخه‌ی gh وجود ندارد.
- شماره‌ی ریپو یا لینک را از جستجو به‌تنهایی نگیرید. لینک HF (`alifarrokh/persian-asr`) ۴۰۴ داد و نام نزدیک دیگری (`alifarokh`) در بنچمارک بود. قبل از ارجاع، صفحه‌ی ریپو یا API را باز کنید.
- اجرای `results.json` بعدی Whisper را پاک کرد. نتایج کامل در `out/summary.md` است.

---

## ۵. وضعیت باز

- **ربات تلگرام:** کد هست ولی فعال نیست. فعال‌سازی نیاز به merge روی شاخه‌ی پیش‌فرض، secrets (`TELEGRAM_BOT_TOKEN`، `TELEGRAM_ALLOWED_USER_IDS`) و تست زنده دارد. محدودیت ۲۰ MB Bot API باقی است.
- **VLM:** حالت «کامل» (هر ۶۰ ثانیه، ۸ فریم) انتخاب مالک بود، ولی با سرعت ۳٫۴ برابر زمان واقعی، هر job شش‌ساعته فقط حدود ۱٫۵ ساعت ویدیو را پوشش می‌دهد. وصل به ربات و صف پس‌زمینه انجام نشده.
- **تحلیل کانال‌های عمومی:** مالک این مسیر را انتخاب کرد، با اطلاع از شرایط بالا. ماژولی برای آن ساخته نشده است. اگر ادامه داده شود، باید MTProto جدا باشد و تأیید حقوقی جداگانه لازم است.
- **Local Bot API:** برای فایل‌های بزرگ‌تر از ۲۰ MB، پیاده نشده.
- **ارزیابی ASR:** روی مجموعه‌ی بزرگ‌تر و صدای ویدیوی واقعی انجام نشده. ITN و اعداد فارسی هم سنجیده نشده‌اند.
- **لایسنس‌های «بررسی نشد»:** Florence-2، Qwen2.5-Omni، PESTE، anti-vocale، telecrawl، FLEURS، Shenava v1.0 ONNX fp16، و FC-Fa. قبل از استفاده‌ی تجاری یا انتشار، هرکدام را از منبع اولیه تأیید کنید.
- **دک‌ها و کار سه‌بعدی قبلی:** مالک آن‌ها را بسته اعلام کرده است.

---

## ۶. زمینه‌ی مالک

- زبان کار: فارسی.
- ترجیح مالک: پرسش‌های کوتاه و ساده با گزینه‌ی مشخص.
- برای تحقیق، جستجوی عمیق (حدود ۳۰ دقیقه) و منبع مشخص مورد انتظار است.
- مالک API فروشنده‌ها (vendor API) را نمی‌خواهد؛ مدل‌ها و ابزارهای باز ترجیح داده می‌شوند.
- ویدیوهای مرجع (placeplate و yerra) را مالک خودش دیده و سبک را از روی ویدیو گرفته است، نه از snippet.
- نتیجه‌ها باید در مخزن و روی remote باشند، چون sandbox ممکن است ریست شود.
- این فایل کاتالوگ است، نه قانون. مالک نمی‌خواهد قوانین به شکل دستور به ایجنت داده شود.
