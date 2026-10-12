# یادداشت انتقال به ایجنت اصلی

تاریخ: 2026-10-12 · شاخه: `arena/758efc2d-repo` · مخزن: `Kimfandogh7/Repo` (الان عمومی است؛ `isPrivate=false` با دسترسی ADMIN)

این فایل خلاصه‌ی کاری است که در این نشست انجام شد، نتایج اندازه‌گیری‌شده، تجربه‌هایی که باید تکرار نشوند، و کارهای باز. قبل از هر کاری، `git fetch && git merge --ff-only origin/arena/758efc2d-repo` را اجرا کنید. در این نشست، شاخه‌ی محلی یک بار عقب بود.

---

## ۱. قوانین کار با کاربر (از گفتگوها)

- همیشه به فارسی جواب بده. جواب کوتاه و مستقیم باشد.
- سؤال‌ها را ساده و کوتاه با `ask_user` بپرس (حداکثر ۳ تا ۴ گزینه). وقتی کاربر گفت «نمیدونم»، خودت تصمیم بگیر و جلو برو.
- برای تحقیق: حدود ۳۰ دقیقه جستجوی عمیق، منبع مشخص با لینک، و پرهیز از خلاصه‌ی سطحی. کاربر قبلاً کار سطحی را «کم‌کاری» خوانده است.
- «نمی‌تونم» جواب نیست. اگر راهی هست، آن را امتحان کن.
- همه‌چیز را روی remote push کن. sandbox ممکن است ریست شود.
- کاربر گفته: هیچ API فروشنده‌ای (vendor API) استفاده نشود. فقط مدل‌هایی که در دسترس‌اند.
- دک (deck) بسته است. کاربر آن را رد کرد و دوباره باز نکن مگر درخواست جدید بدهد.
- ساختار دیدن ویدیو: ویدیوهای مرجع را واقعاً دانلود و تماشا کن، نه از روی snippet جستجو.
- کیفیت دک‌ها: کف کیفیت `edu-agent/artifacts/morph/morph.pptx` است (۵ اسلاید، morph chain واقعی، نمودار بومی). هر خروجی جدید نباید از آن ساده‌تر باشد.
- هر دک قبل از تحویل باید QC خودکار لی‌اوت داشته باشد (`edu-agent/tools/pptx/qa_overlap.py`).
- ایجنت تصویر نمی‌بیند. رندرها را عددی بررسی کن.
- هشدار `rebase --ours`: در rebase، `--ours` به upstream اشاره می‌کند، نه به شاخه‌ی خودت.

---

## ۲. کارهای این نشست

### الف) تست ASR فارسی (کامل شد)

- مجموعه داده: FLEURS fa_ir، ۱۲ کلیپ تست، ۲۰۷ ثانیه صدا. روی runner دو vCPU گیت‌هاب.
- نتایج (اندازه‌گیری‌شده، در `edu-agent/telegram-pipeline/asr-test/out/summary.md`):

| مدل | WER | RTF |
|---|---|---|
| faster-whisper small (int8) | 56.25٪ | 0.565 |
| faster-whisper medium (int8) | 31.85٪ | 0.964 |
| Shenava Koochik v1.0 (CTC، sherpa-onnx) | **9.52٪** | 0.013 تا 0.045 |
| Shenava Koochik v1.5 (RNNT، sherpa-onnx) | 10.12٪ | 0.018 |

- نتیجه: Shenava حدود ۳ برابر دقیق‌تر و ۲۰ برابر سریع‌تر از Whisper medium است.
- محدودیت: ۱۲ کلیپ گفتار خوانده‌شده است، نه صدای ویدیوی واقعی. عدد WER تا وقتی نمونه بزرگ‌تر نشده، قطعی نیست. نرمال‌سازی: حذف اعراب، ZWNJ به فاصله، حذف علامت، یکسان‌سازی ی/ک عربی.
- مدل‌ها: `Reza2kn/Shenava-Koochik-v1.0-sherpa-onnx` (فایل `model.onnx` و `tokens.txt`) و `Reza2kn/Shenava-Koochik-v1.5-RNNT-sherpa-onnx`. مجوز Apache-2.0.
- اسکریپت: `edu-agent/telegram-pipeline/asr-test/persian_asr_test.py`. workflow: `.github/workflows/persian-asr.yml`.

### ب) تحقیق درباره‌ی Telegram و معماری (کامل شد، اجرا نشد)

- بررسی `FALKON-CODE/Telegram-Mirror`: یک relay عمومی کانال از طریق t.me/s در Actions است. فقط کانال عمومی می‌بیند و تحلیل ویدیو ندارد. ایده‌ی قابل استفاده: تکه‌کردن فایل‌ها به ۹۵ MB و استفاده از مخزن به عنوان storage.
- ایده‌های ds4 که به کار می‌آیند: کش نتیجه‌ی تحلیل روی دیسک با کلید hash محتوا، و overlap کردن I/O با محاسبه. ds4 به Metal/CUDA و ۹۶–۱۲۸ GB RAM نیاز دارد، پس مستقیم قابل استفاده نیست.
- گزارش‌های تحقیق: `edu-agent/research/telegram-agent.md` و `telegram-agent-round2.md`.

### پ) انتخاب رابط ربات (چارت انجام شد)

- چارت: `edu-agent/telegram-pipeline/docs/gateway_comparison.png` (با اسکریپت `make_gateway_chart.py`).
- Hermes Agent: MIT، پیش‌فرض Nous Portal. OpenClaw: پیش‌فرض‌ها OpenAI/Gemini، سقف media تلگرام ۵ MB.
- انتخاب کاربر: **ربات کوچک خودمان**.

### ت) ربات تلگرام (کد نوشته شد، فعال نیست)

- `edu-agent/telegram-bot/bot.py`: python-telegram-bot ۲۱٫۶، دریافت صوت/ویدیو از Bot API، ffmpeg به WAV mono 16k در تکه‌های ۵ دقیقه‌ای، سپس Shenava، خروجی با زمان‌بندی. فقط کاربران در `TELEGRAM_ALLOWED_USER_IDS`.
- `.github/workflows/telegram-bot.yml`: هر ۶ ساعت، `timeout -s INT 340m`، `concurrency` با `cancel-in-progress: false`. دلیل: job در Actions حداکثر ۶ ساعت است.
- `edu-agent/telegram-bot/README.md`: راه‌اندازی.
- تست زنده نشده (sandbox به Telegram و Hugging Face دسترسی ندارد).
- **فعال‌سازی:** workflow زمان‌بندی‌شده فقط روی شاخه‌ی پیش‌فرض کار می‌کند. باید merge شود (یا PR باز شود). secrets لازم: `TELEGRAM_BOT_TOKEN` و `TELEGRAM_ALLOWED_USER_IDS`. توکن را هرگز در چت نخواهید.
- محدودیت Bot API: فایل‌های بالای ~۲۰ MB دانلود نمی‌شوند. Local Bot API (با api_id/api_hash از my.telegram.org، لایسنس BSL-1.0) راه حل است ولی پیاده نشده.

### ث) VLM برای ویدیو (تست انجام شد، وصل نشد)

- مدل: `HuggingFaceTB/SmolVLM2-500M-Video-Instruct` (Apache-2.0). کد: `edu-agent/telegram-bot/vlm_describe.py`.
- روش: برش ویدیو به بخش‌های ۶۰ ثانیه‌ای، ۸ فریم JPEG از هر بخش، توصیف انگلیسی.
- نتیجه اندازه‌گیری‌شده: ویدیوی ۳ دقیقه‌ای، ۶۱۲ ثانیه روی ۲ vCPU. یعنی حدود **۳٫۴ برابر زمان واقعی**. برای یک ساعت ویدیو حدود ۳٫۴ ساعت لازم است. یک job شش‌ساعته فقط حدود ۱٫۵ ساعت ویدیو را پوشش می‌دهد.
- کیفیت توصیف: روی ویدیوی تست رنگی، توصیف عمومی بود. روی ویدیوی واقعی سنجیده نشده.
- تخمین (تأیید نشده): حالت سبک‌تر (هر ۵ دقیقه، ۴ فریم) حدود ۲۰ دقیقه پردازش برای هر ساعت ویدیو.
- کاربر حالت «کامل» (هر ۶۰ ثانیه، ۸ فریم) را انتخاب کرد. اما به ربات وصل نشده و نیاز به صف کار پس‌زمینه دارد.
- workflow تست: `.github/workflows/vlm-test.yml` (trigger روی push به مسیرهای مربوط؛ نتیجه در `edu-agent/telegram-bot/vlm-test/out/`).

### ج) مخزن

- وضعیت مخزن: عمومی است. درخواست تغییر visibility در این نشست 403 داد، ولی بعداً معلوم شد مخزن قبلاً عمومی شده است.
- فایل‌های تیک‌تاک (فریم‌های placeplate در `refs/dense/placeplate/`) در تاریخچه هستند. کاربر حذف از تاریخچه را رد کرد.
- هزینه Actions: مخزن عمومی با runnerهای استاندارد رایگان است. در مخزن خصوصی، اجرای ۲۴ ساعته حدود ۲۴۷ دلار در ماه می‌شود.

---

## ۳. تجربه‌ها و تله‌ها (باید تکرار نشوند)

1. **workflow_dispatch فقط روی شاخه‌ی پیش‌فرض کار می‌کند.** روی شاخه‌ی کاری خطای 404 می‌گیرید. برای تست روی شاخه‌ی کاری از trigger روی `push` به مسیر مشخص استفاده کنید.
2. **لاگ Actions قابل خواندن نبود** (`gh run view --log` و API خالی برمی‌گردند). راه کار: خروجی و خطا را در فایل داخل مخزن بنویسید و commit کنید (`out/results.json`، `out/error.txt`)، سپس فایل را بخوانید.
3. **datasets-server برای `google/fleurs` fa_ir خطای 500 داد.** به جای آن از `test.tsv` و `audio/test.tar.gz` (با `resolve/main`، به صورت stream) استفاده کنید.
4. **`wave` استاندارد پایتون WAV با فرمت float32 (tag 3) را نمی‌خواند.** از `soundfile` استفاده کنید.
5. **در `sherpa-onnx` 1.13.8 تابع `sherpa_onnx.read_wave` وجود ندارد.** همین را با `soundfile` حل کنید.
6. **sherpa-onnx برای Persian NeMo CTC از نسخه ۱٫۱۳٫۵ به بعد است.** مسیر offline اصلاح شده است. مسیر streaming در issue #4003 / PR #4004 باگ fbank داشت (WER از ~۴۰٪ به ~۱۱٫۶٪). اگر streaming لازم شد، نسخه‌ی اصلاح‌شده را بررسی کنید.
7. **Gemma 3n برای فارسی بد است.** در PARSA-Bench، مدل‌های E2B و E4B تا ۸۶٪ جمله‌ها را در حلقه‌ی تکرار گیر انداختند.
8. **GitHub Actions حداکثر ۶ ساعت به ازای هر job** اجرا می‌کند. هر سرویس دائمی باید به تکه‌های زمانی تقسیم شود.
9. **نسخه‌های torch / torchvision باید از یک index باشند.** نصب torch از index CPU و torchvision از PyPI باعث `operator torchvision::nms does not exist` شد. هر دو را با هم از `https://download.pytorch.org/whl/cpu` نصب کنید.
10. **SmolVLM2 پردازشگر ویدیو به `torchvision.io.read_video` نیاز دارد که در torchvision جدید نیست.** راه کار: فریم‌ها را با ffmpeg به JPEG تبدیل کنید و به‌صورت `{"type":"image","path":...}` بدهید. همچنین پکیج‌های `num2words`، `pillow` و `av` لازم‌اند.
11. **شاخه‌ی محلی ممکن است عقب باشد.** اول `git fetch` و `git merge --ff-only` انجام دهید.
12. **`gh repo edit --accept-visibility-change-consequences` در این نسخه‌ی gh وجود ندارد.**
13. **نتایج Whisper در `results.json` پاک شدند** چون اجرای بعدی فقط Shenava را اجرا کرد. فایل `summary.md` را مبنا قرار دهید.
14. **عدد RTF در ابتدا با زمان لود مدل قاطی می‌شود.** برای اعداد دقیق، زمان decode را جدا اندازه بگیرید.

---

## ۴. کارهای باز (به ترتیب پیشنهادی)

1. **تصمیم VLM:** حالت «کامل» را پیاده کنید و محدودیت ۱٫۵ ساعت در هر job را گزارش دهید، یا حالت سبک را تست کنید. با ویدیوی واقعی کیفیت توصیف را بسنجید.
2. **اتصال VLM به ربات:** صف کار پس‌زمینه (چون پردازش ساعت‌ها طول می‌کشد). یک job جدا برای ویدیوهای طولانی‌تر از ۶۰ دقیقه‌ای.
3. **فعال‌سازی ربات:** merge یا PR، سپس تنظیم secrets توسط کاربر، و تست زنده با یک فایل کوتاه.
4. **مسیر تحلیل کانال‌های عمومی:** **ساخته نشده.** شرایط محتوای تلگرام (Feb 2026) استفاده از داده‌های پلتفرم برای AI را منع کرده است. کاربر با آگاهی از این موضوع گفت «تحلیل کانال‌ها هم»، ولی هنوز تأیید مجدد و جداگانه لازم است. ماژول MTProto جدا خواهد بود. کاری برای دور زدن تشخیص تلگرام نکن.
5. **Local Bot API** برای فایل‌های بزرگ‌تر از ۲۰ MB (اختیاری).
6. **ارزیابی ASR** روی نمونه‌ی بزرگ‌تر و صدای ویدیوی واقعی؛ بررسی اعداد فارسی و ITN.
7. **دک‌ها و کار سه‌بعدی قبلی** (`edu-agent/artifacts/finale/`، `edu-agent/artifacts/morph/`، `edu-agent/tools/3d/build_f1_car.py`): کار بسته است. فقط با درخواست جدید کاربر ادامه دهید.

---

## ۵. فهرست فایل‌های این نشست

| مسیر | کاربرد |
|---|---|
| `edu-agent/telegram-pipeline/asr-test/persian_asr_test.py` | تست ASR فارسی (Whisper و Shenava) |
| `edu-agent/telegram-pipeline/asr-test/out/summary.md` | جدول نهایی نتایج ASR |
| `.github/workflows/persian-asr.yml` | workflow تست ASR |
| `edu-agent/telegram-pipeline/docs/gateway_comparison.png` | چارت مقایسه‌ی رابط‌ها |
| `edu-agent/telegram-bot/bot.py` | ربات تلگرام (فعال نیست) |
| `edu-agent/telegram-bot/README.md` | راه‌اندازی ربات |
| `edu-agent/telegram-bot/requirements.txt` | وابستگی‌های ربات |
| `.github/workflows/telegram-bot.yml` | اجرای ربات هر ۶ ساعت |
| `edu-agent/telegram-bot/vlm_describe.py` | توصیف ویدیو با SmolVLM2 |
| `.github/workflows/vlm-test.yml` | تست سرعت VLM |
| `edu-agent/telegram-bot/vlm-test/out/result.txt` | خروجی تست VLM |
| `edu-agent/research/telegram-agent*.md` | گزارش‌های تحقیق |
| `edu-agent/HANDOFF.md` | همین فایل |
