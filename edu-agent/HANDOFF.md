# کاتالوگ ریپوها، ابزارها و نتایج برای ایجنت بعدی

تاریخ: 2026-10-12 · شاخه: `arena/758efc2d-repo` · مخزن: `Kimfandogh7/Repo` (عمومی؛ `isPrivate=false`)

این فایل یک کاتالوگ است، نه مجموعه دستور. ایجنت بعدی مغز مستقل دارد و خودش تصمیم می‌گیرد. هر ریپو، مدل، ابزار و نتیجه‌ای که این‌جا آمده، با وضعیت آن (تست شده، فقط بررسی شده، یا استفاده نشده) ثبت شده است.

قبل از کار، شاخه‌ی محلی را همگام کنید: `git fetch && git merge --ff-only origin/arena/758efc2d-repo`. در این نشست شاخه‌ی محلی یک بار عقب مانده بود.

---

## ۱. وضعیت مخزن

- مخزن عمومی است. تغییر visibility در این نشست 403 داد، ولی بعداً معلوم شد قبلاً عمومی شده است.
- تاریخچه‌ی مخزن فریم‌های ویدیوی تیک‌تاک (`refs/dense/placeplate/`) را دارد. مالک حذف آن‌ها از تاریخچه را رد کرده است.
- Workflowها در `.github/workflows/`. workflow_dispatch فقط روی شاخه‌ی پیش‌فرض کار می‌کند؛ روی شاخه‌ی کاری از trigger روی push استفاده شده است.

---

## ۲. ریپوهای اوپن‌سورس و ابزارهای خارجی

### الف) گفتار و ASR فارسی (تست شده)

| ابزار / مدل | منبع | لایسنس | وضعیت در این کار |
|---|---|---|---|
| sherpa-onnx | github.com/k2-fsa/sherpa-onnx | Apache-2.0 | **استفاده شد** (نسخه‌ی `1.13.8` روی PyPI). از نسخه‌ی ۱٫۱۳٫۵ مدل‌های Persian NeMo CTC را دارد. |
| Shenava Koochik v1.0 (sherpa-onnx) | `Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx` | Apache-2.0 | **بهترین نتیجه‌ی تست شده**: WER ۹٫۵۲٪. فایل‌ها: `model.onnx`، `tokens.txt`. |
| Shenava Koochik v1.5 (RNNT) | `Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx` | Apache-2.0 | **تست شد**: WER ۱۰٫۱۲٪. |
| Shenava Koochik v1.0 ONNX fp16 | `Reza2kn/Shenava-Koochik-v1.0-ONNX-fp16` | Apache-2.0 | فقط بررسی شد. |
| Nimaone/nemotron-asr-streaming-farsi-onnx | `huggingface.co/Nimaone/nemotron-asr-streaming-farsi-onnx` | مشخص نشد | فقط بررسی شد. مدل ۶۰۰ میلیونی streaming؛ WER ۲۷٫۹ تا ۲۹٫۶٪ روی تست خودش، RTF ۰٫۳۵ تا ۰٫۳۹ روی i7 نسل چهارم. |
| faster-whisper (SYSTRAN) | github.com/SYSTRAN/faster-whisper | مشخص نشد | **تست شد** (small و medium، int8). |
| Persian wav2vec2 XLS-R 300M | `alifarrokh/persian-asr` | مشخص نشد | فقط بررسی شد: WER ۲۷٫۹۲٪ (بدون LM). |
| nvidia/stt_fa_fastconformer_hybrid_large | Hugging Face | مشخص نشد | فقط بررسی شد. |
| speechbrain/asr-whisper-large-v2-commonvoice-fa | Hugging Face | مشخص نشد | فقط بررسی شد: WER ۳۱٫۷۵٪ روی CommonVoice 10. |
| persian-speech-toolkit | github.com/Omidbn2000/persian-speech-toolkit | بدون لایسنس (مدل‌ها Apache-2.0) | فقط بررسی شد. Shenava + Silero VAD + TTS فارسی. |
| anti-vocale (issue #105) | github.com/RisorseArtificiali/anti-vocale/issues/105 | مشخص نشد | فقط بررسی شد: Shenava v1.5 روی ۱۰ کلیپ FLEURS، WER ۱۵٫۹٪ (۱۳٫۳٪ با نرمال‌سازی ZWNJ). |
| FLEURS fa_ir | `google/fleurs` | CC-BY-4.0 (تأیید نشده) | **استفاده شد**: `data/fa_ir/test.tsv` و `audio/test.tar.gz`. |

### ب) بنچمارک‌ها و مقالات فارسی

- **PSRB** (arxiv 2505.21230): بنچمارک ASR فارسی با ۳٬۳۷۲ کلیپ. بهترین نتیجه از Avanegar (تجاری، CER ۸٫۷۵٪، WER ۱۹٫۳٪). Faster-Whisper بهترین متن‌باز با WER ۳۳٫۹۳٪.
- **PARSA-Bench** (arxiv 2603.14456): بنچمارک مدل‌های صوتی-زبانی فارسی. Qwen3-Omni-30B بهترین ASR متن‌باز است، ولی بزرگ است. Gemma 3n E2B و E4B در فارسی دچار حلقه‌ی تکرار شدند (حدود ۱۲ تا ۱۳٪ جمله‌ها، که ۸۲ تا ۸۶٪ از میانگین WER را ساختند).
- **ArmanJR/PESTE-Benchmark** (`asr-models-on-hf.md`): فهرست ۸۲ مدل ASR فارسی روی Hugging Face تا ۱ اوت ۲۰۲۶.
- **Interspeech 2025 (Hameed et al.)**: ASR برای زبان‌های کم‌منبع خاورمیانه، مقایسه‌ی Whisper و مدل‌های monolingual.

### پ) ویدیو و تصویر (VLM)

| ابزار / مدل | منبع | لایسنس | وضعیت |
|---|---|---|---|
| **SmolVLM2-500M-Video-Instruct** | `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` | Apache-2.0 (در کارت مدل تأیید نشد) | **تست شد**. روی ۲ vCPU حدود ۳٫۴ برابر زمان واقعی. |
| SmolVLM2 (حداکثر ۶۴ فریم) | گفتگوی Hugging Face | - | گفته شد که ویدیو تا ۶۴ فریم نمونه‌برداری می‌شود. |
| Qwen2.5-Omni-3B GGUF (ggml-org) | `ggml-org/Qwen2.5-Omni-3B-GGUF` | مشخص نشد | فقط بررسی شد. ورودی صوت و تصویر دارد، ویدیو ندارد. در llama.cpp گزارش شده که روی صوت طولانی توهم می‌زند. |
| Qwen2.5-Omni | github.com/QwenLM/Qwen2.5-Omni | Apache-2.0 (ریپو) | فقط بررسی شد. |
| llama.cpp-omni | github.com/tc-mb/llama.cpp-omni | MIT | فقط بررسی شد. |
| Gemma 3n | Google | - | **برای فارسی توصیه نمی‌شود** (بخش ۲ب). |

### ت) ربات، گیت‌وی و تلگرام

| ابزار | منبع | لایسنس | وضعیت |
|---|---|---|---|
| python-telegram-bot ۲۱٫۶ | PyPI | - | **استفاده شد** در `edu-agent/telegram-bot/bot.py`. نصب و import تست شد؛ اجرای زنده نشد. |
| Hermes Agent | github.com/NousResearch/hermes-agent | MIT | بررسی شد. Gateway تلگرام، حافظه، skill، cron. نصب سریع پیشنهادی Nous Portal است. |
| OpenClaw | docs.openclaw.ai | مشخص نشد (ریپوی هسته تأیید نشد) | بررسی شد. سقف media تلگرام ۵ MB. پیش‌فرض‌ها OpenAI/Gemini. |
| overpod/openclaw-channel-telegram-userbot | github.com/overpod/openclaw-channel-telegram-userbot | MIT | بررسی شد. کانال MTProto برای OpenClaw. |
| openclaw/telecrawl | github.com/openclaw/telecrawl | MIT | بررسی شد. خواندن Telegram Desktop tdata. |
| tdlib/telegram-bot-api (Local Bot API) | github.com/tdlib/telegram-bot-api | BSL-1.0 | بررسی شد. برای فایل‌های بزرگ‌تر از ۲۰ MB، نیاز به api_id و api_hash دارد. پیاده نشد. |
| GeiserX/Telegram-Archive | github.com/GeiserX/Telegram-Archive | GPL-3.0 | بررسی شد. بک‌آپ اکانت با Telethon. |
| FALKON-CODE/Telegram-Mirror | github.com/FALKON-CODE/Telegram-Mirror | مشخص نشد | **بررسی شد**. relay کانال عمومی با t.me/s در Actions؛ تقسیم فایل به ۹۵ MB. |
| ffmpeg | ffmpeg.org | LGPL/GPL | **استفاده شد** برای استخراج صدا، تکه‌کردن و برش ویدیو. |

### ث) استنتاج و معماری (تحقیق)

- **antirez/ds4** (github.com/antirez/ds4): موتور استنتاج DeepSeek. ایده‌های قابل استفاده: کش نتایج روی دیسک با کلید hash محتوا، و overlap کردن I/O و محاسبه. نیاز به Metal، CUDA یا ROCm و ۹۶ تا ۱۲۸ GB RAM دارد، پس مستقیم قابل استفاده نیست.
- **Anemll/ds4-ssd** (docs/DWARFSTAR4_REFERENCE.md): کش prefix با کلید SHA1 که بین ری‌استارت‌ها بماند.
- **dwarfstar.sh** (گزارش benchmark): حالت streaming از SSD «ظرفیت با هزینه‌ی سرعت» است.

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
| `edu-agent/vendor/ppt-master/` | سورس ۱۶:۹ و عمودی Phase 4 و 5 | قبلی |
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

محدودیت‌ها: نمونه کوچک است، گفتار خوانده‌شده است، ITN و اعداد فارسی بررسی نشده، و RTF در یک اجرا با زمان لود مدل قاطی شده است.

### VLM (SmolVLM2-500M)

- یک ویدیوی ۳ دقیقه‌ای، ۶۱۲ ثانیه، با ۳ بخش ۶۰ ثانیه‌ای و ۸ فریم هر بخش. روی ۲ vCPU.
- خروجی روی ویدیوی تست رنگی عمومی بود. روی ویدیوی واقعی سنجیده نشده.
- تخمین، تأیید نشده: حالت ۴ فریم هر ۵ دقیقه حدود ۲۰ دقیقه پردازش برای هر ساعت ویدیو.

### هزینه‌ی GitHub Actions

- runnerهای استاندارد در مخزن عمومی رایگان‌اند.
- در مخزن خصوصی، ۲٬۰۰۰ دقیقه‌ی رایگان در ماه و بعد از آن ۰٫۰۰۶ دلار برای هر دقیقه‌ی Linux 2-core ([منبع](https://cicdcalculator.com/github-actions-free-tier)). اجرای ۲۴ ساعته (حدود ۴۳٬۲۰۰ دقیقه) حدود ۲۴۷ دلار در ماه است.
- هر job حداکثر ۶ ساعت اجرا می‌شود.

### Telegram: قوانین

- [شرایط محتوای و AI تلگرام](https://telegram.org/tos/content-licensing): استفاده از داده‌های پلتفرم برای توسعه، آموزش، بنچمارک یا استقرار مدل‌های AI را منع کرده است. استثنا: داده‌ی لازم برای راه‌اندازی یک ربات یا کلاینت قانونی، یا رضایت صریح همه‌ی کاربران مربوط در همان چت.
- [شرایط API تلگرام](https://core.telegram.org/api/terms) بند ۱٫۵ همین را تکرار می‌کند.
- این شرایط در ۳ فوریه‌ی ۲۰۲۶ اضافه شده است ([Open Terms Archive](https://opentermsarchive.org/en/memos/telegram-prohibits-collecting-data-for-ai-use/)).

---

## ۴. نکته‌های فنی که در عمل دیده شد

- `workflow_dispatch` روی شاخه‌ی غیرپیش‌فرض خطای 404 می‌دهد.
- `gh run view --log` و API لاگ Actions برای این مخزن خالی برگشت. نتیجه را در فایل داخل مخزن نوشتیم و commit کردیم.
- datasets-server برای `google/fleurs` fa_ir خطای 500 داد. فایل‌های خام از `resolve/main` کار کردند.
- `wave` استاندارد پایتون WAV با فرمت float32 (tag 3) را نمی‌خواند؛ `soundfile` کار کرد.
- در `sherpa-onnx` 1.13.8 تابع `sherpa_onnx.read_wave` وجود ندارد.
- streaming در sherpa-onnx برای مدل‌های NeMo CTC باگ fbank داشت (issue #4003 و PR #4004: WER از ~۴۰٪ به ~۱۱٫۶٪). مسیر offline درست بود.
- torch از index CPU و torchvision از PyPI ناسازگار بودند و `operator torchvision::nms does not exist` داد. هر دو را از یک index نصب کنید.
- SmolVLM2 processor ویدیو به `torchvision.io.read_video` نیاز دارد که در torchvision جدید نیست. فریم JPEG از ffmpeg کار کرد. همچنین `num2words`، `pillow` و `av` لازم بود.
- `gh repo edit --accept-visibility-change-consequences` در این نسخه‌ی gh وجود ندارد.
- شاخه‌ی محلی ممکن است عقب باشد؛ قبل از کار fetch کنید.
- اجرای `results.json` بعدی Whisper را پاک کرد. نتایج کامل در `out/summary.md` است.

---

## ۵. وضعیت باز

- **ربات تلگرام:** کد هست ولی فعال نیست. فعال‌سازی نیاز به merge روی شاخه‌ی پیش‌فرض، secrets (`TELEGRAM_BOT_TOKEN`، `TELEGRAM_ALLOWED_USER_IDS`) و تست زنده دارد. محدودیت ۲۰ MB Bot API باقی است.
- **VLM:** حالت «کامل» (هر ۶۰ ثانیه، ۸ فریم) انتخاب مالک بود، ولی با سرعت ۳٫۴ برابر زمان واقعی، هر job شش‌ساعته فقط حدود ۱٫۵ ساعت ویدیو را پوشش می‌دهد. وصل به ربات و صف پس‌زمینه انجام نشده.
- **تحلیل کانال‌های عمومی:** مالک این مسیر را انتخاب کرد، با اطلاع از شرایط بالا. ماژولی برای آن ساخته نشده است. اگر ادامه داده شود، باید MTProto جدا باشد و تنظیم مجدد قانونی جداگانه با مالک لازم است.
- **Local Bot API:** برای فایل‌های بزرگ‌تر از ۲۰ MB، پیاده نشده.
- **ارزیابی ASR:** روی نمونه‌ی بزرگ‌تر و صدای ویدیوی واقعی انجام نشده. ITN و اعداد فارسی هم سنجیده نشده‌اند.
- **دک‌ها و کار سه‌بعدی قبلی:** مالک آن‌ها را بسته اعلام کرده است.

---

## ۶. زمینه‌ی مالک

- زبان کار: فارسی.
- مالک ترجیح می‌دهد پرسش‌ها کوتاه و ساده، با گزینه‌های مشخص، پرسیده شوند.
- برای تحقیق، جستجوی عمیق (حدود ۳۰ دقیقه) و منبع مشخص مورد انتظار است.
- مالک API فروشنده‌ها (vendor API) را نمی‌خواهد؛ مدل‌ها و ابزارهای باز ترجیح داده می‌شوند.
- ویدیوهای مرجع (placeplate و yerra) را مالک خودش دیده و سبک را از روی ویدیو گرفته است، نه از snippet.
- نتیجه‌ها باید در مخزن و روی remote باشند، چون sandbox ممکن است ریست شود.
- مالک نمی‌خواهد قوانین به شکل دستور به ایجنت داده شوند؛ این فایل فقط اطلاعات است.
