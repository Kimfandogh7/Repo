# تحقیق: اتصال ایجنت به تلگرام (2026-10-12)

هدف: ایجنت از طریق تلگرام (۱) فایل/تصویر/ویدیو را بگیرد و ببیند و بشنود، (۲) فایل‌های بزرگ (Drive یا خود تلگرام) را پردازش کند، (۳) کانال‌های عمومی را بررسی کند، (۴) کارهای دیگر تلگرام را انجام دهد.

## ۱. سه لایه‌ی دسترسی به تلگرام

| لایه | چه کاری می‌کند | محدودیت مهم | منبع |
|---|---|---|---|
| **Bot API** (`api.telegram.org`) | بات با توکن BotFather. پیام خصوصی و گروه | دانلود فایل فقط **تا ۲۰ MB**؛ آپلود تا ۵۰ MB. بات **تاریخچه‌ی کانال عمومی را نمی‌بیند** مگر ادمین کانال باشد | [Bot API](https://core.telegram.org/bots/api)، [getFile](https://gramio.dev/telegram/methods/getfile) |
| **Local Bot API server** (`telegram-bot-api --local`) | همان Bot API روی سرور خودتان | دانلود و آپلود تا **۲ GB**؛ `getFile` مسیر محلی برمی‌گرداند. نیاز به `api_id` و `api_hash` از my.telegram.org | [Bot API – Local server](https://core.telegram.org/bots/api)، [bigmike](https://bigmike.help/en/devops/local-telegram-bot-api-advantages-limitations-of-the-standard-api-and-set-eb4a3b/) |
| **MTProto کاربر** (Telethon / Pyrogram / gotd) | با حساب واقعی لاگین می‌کند. می‌تواند هر کانال عمومی را پس از resolve کردن @username بخواند، جستجو کند، مدیا دانلود کند | **ریسک بَن حساب**؛ FloodWait؛ ToS (بخش زیر) | [Telethon FAQ/docs](https://docs.teleproto.dev/faq)، [Stack Overflow](https://stackoverflow.com/questions/52736324/how-to-get-channel-updates-with-telegram-robot) |
| **Web preview** (`t.me/s/<channel>`) | HTML عمومی بدون لاگین؛ حدود ۲۰ پست آخر؛ `?before=` برای صفحات قدیمی‌تر | فقط متن و thumbnail. **ویدیوی کامل دانلود نمی‌شود** | [DEV community](https://dev.to/yuhehe/how-to-scrape-public-telegram-channels-without-an-api-key-step-by-step-1d91) |

**نتیجه‌ی کلیدی:** بات (Bot API) نمی‌تواند کانال عمومی دلخواه را بخواند. برای «بررسی کانال عمومی با هر فایل» یا حساب کاربر (MTProto) لازم است، یا web preview برای متن و لیست پست‌ها.

## ۲. محدودیت شرایط استفاده (مهم‌ترین یافته)

از [صفحه‌ی رسمی Telegram API Terms of Service](https://core.telegram.org/api/terms):

- **بند ۱.۵:** استفاده از API تابع «Terms of Service for Content Licensing and AI Scraping» است. **ممنوع است داده‌ی به‌دست‌آمده از پلتفرم تلگرام را برای آموزش، fine-tune، یا «توسعه، بهبود، یا deployment» هوش مصنوعی و مدل‌های ML به کار بَرد.**
  - این مستقیم به کار ما مربوط است: خواندن کانال عمومی و دادن محتوا به یک LLM یا vision model می‌تواند زیر این بند بیفتد. **این را فقط با نظر حقوقی/کاربر تصمیم بگیریم.** من تفسیر قطعی نمی‌کنم.
  - محتوای پیام‌هایی که **کاربر مستقیماً برای بات می‌فرستد** (از طریق Bot API) ریسک کمتری دارد، ولی متن ToS را دوباره بررسی کنید.
- **بند ۲.۳:** نام اپ نباید کلمه‌ی «Telegram» را داشته باشد (مگر با «Unofficial»). یعنی اسم پروژه‌ی ما نباید `telegram-…` باشد.
- **صفحه‌ی obtaining api_id:** «حساب‌هایی که از کلاینت‌های غیررسمی وارد می‌شوند به‌طور خودکار **تحت مشاهده** قرار می‌گیرند». استفاده برای flood/spam/تقلب بازدید = بَن دائمی.
- **بند ۴.۲:** نقض → قطع دسترسی API بعد از ۱۰ روز.

## ۳. ریسک حساب (userbot)

- [Telethon docs](https://media.readthedocs.org/pdf/telethon/stable/telethon.pdf): کتابخانه را فقط روی حساب‌های قدیمی و «جاافتاده» استفاده کنید؛ دانلود موازی توصیه نمی‌شود چون FloodWait زودتر می‌آید.
- [teleproto FAQ](https://docs.teleproto.dev/faq): FloodWait را بخوابید و تکرار سریع نکنید. «از شماره‌ای استفاده کنید که از دست دادنش برایتان مهم نیست».
- گزارش‌های کاربران (Reddit، مه ۲۰۲۶): حساب‌های جدید که با API کار کردند بَن شدند؛ حساب‌های قدیمی‌تر کمتر محدود شدند. این شواهد غیررسمی‌اند.
- **پیشنهاد:** یک حساب تست جدا (شماره‌ی مجزا) با سرعت بسیار پایین. هرگز حساب اصلی.

## ۴. پروژه‌های متن‌باز موجود (Clone & Improve)

### الف) ایجنت کامل با کانال تلگرام
- **OpenClaw** (MIT): gateway خودمیزبان. کانال تلگرام با grammY، long polling پیش‌فرض، عکس/آلبوم/صوت/ویدیو/استیکر، `apiRoot` برای Local Bot API، `trustedLocalFileRoots`. نیاز به Node 22+ و pnpm. [docs/channels/telegram.md](https://github.com/openclaw/openclaw/blob/main/docs/channels/telegram.md)، [openclaw.ai](https://openclaw.ai/)
- **Hermes Agent** (Nous Research، MIT، Python): Telegram/Discord/Slack/WhatsApp/Signal/Email، حافظه‌ی پایدار، cron طبیعی، subagent، vision، TTS، **رونویسی خودکار voice memo**، ۷ backend اجرا (local/Docker/SSH/Modal…). [hermes-agent.nousresearch.com](https://hermes-agent.nousresearch.com/)، [dedimax](https://www.dedimax.com/en/blog/hermes-agent-a-new-self-hosted-ai-agent-from-nous-research)
  - برای این repo (Python) انطباق بهتری دارد.

### ب) MCP سرور برای حساب کاربر (خواندن کانال/دانلود مدیا)
- **chigwell/telegram-mcp** (Telethon): بیشترین قابلیت؛ **`TELEGRAM_ALLOWED_CHAT_IDS`** (allowlist کانال)؛ مسیرهای فایل safe-by-default؛ **رونویسی voice با Groq/OpenAI/whisper/Telegram** با کش SQLite؛ sanitize برای prompt-injection؛ `TELEGRAM_EXPOSED_TOOLS=read-only`. آخرین commit: ۱۲ اکتبر ۲۰۲۶. [GitHub](https://github.com/chigwell/telegram-mcp)
- **0xMRK95/telegram-mcp-server**: `scan_channels_content` برای اسکن دسته‌ای کانال‌ها با timeout و خروجی JSON. [GitHub](https://github.com/0xMRK95/telegram-mcp-server)
- **adlandh/telegram-mcp** (Go): read-only پیش‌فرض، HTTP فقط loopback با Bearer، سقف دانلود ۲۰۰ MB، بدون ارسال پیام. [GitHub](https://github.com/adlandh/telegram-mcp)
- **m0n0x41d/telegram-mcp**: `read_messages_since` برای خواندن پنجره‌ی جدید بعد از یک message ID. [GitHub](https://github.com/m0n0x41d/telegram-mcp)
- **better-telegram-mcp**: دو حالت bot و user، OTP وب، Docker HTTP. [GitHub](https://github.com/n24q02m/better-telegram-mcp)

**License هیچ‌کدام را هنوز بررسی نکرده‌ام** (در صفحه‌ی chigwell فقط ابتدای صفحه خوانده شد). قبل از clone باید LICENSE را چک کنیم.

## ۵. فهم ویدیو، تصویر و صوت (متن‌باز، قابل اجرا روی CPU/GPU)

| کار | مدل/ابزار | نکته | منبع |
|---|---|---|---|
| **صوت → متن** | faster-whisper (MIT، CTranslate2) | int8 روی CPU؛ مدل `small` برای یک کلیپ ۱۳ دقیقه‌ای حدود ۱m42s روی ۸ thread. `large-v3-turbo` (809M) تعادل خوب کیفیت/سرعت | [README](https://github.com/SYSTRAN/faster-whisper) |
| **فریم‌گیری** | ffmpeg (scene detection یا ۱ fps) | ویدیو ۱۰ دقیقه‌ای با ۱ fps = ۶۰۰ فریم؛ باید سقف گذاشت (مثلاً scene-change + سقف ۶۰) | — |
| **ویدیو-LLM کوچک** | SmolVLM2 256M / 500M / 2.2B Video-Instruct (Apache 2.0) | 500M: Video-MME **42.2**، حدود **1.8 GB** GPU RAM؛ 2.2B: Video-MME **52.1**. فریم‌های ~۵۰ تایی به‌صورت multi-image؛ **صدا ندارد** → با Whisper ترکیب شود | [HF README](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct/blob/9d094b4096848ed218717acab682a1e08036240a/README.md)، [HF blog](https://huggingface.co/blog/vlms-2025) |
| **ویدیو-LLM قوی‌تر** | Qwen2.5-VL 3B/7B | Video-MME (بدون زیرنویس): 7B = **65.1**؛ 3B = 61.5؛ ویدیوی بیش از یک ساعت؛ زمان مطلق در encoding. **Qwen Research License** برای 7B (3B را جدا چک کنید). نیاز به GPU | [Qwen2.5-VL report](https://arxiv.org/pdf/2502.13923)، [HF card](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct) |
| **ویدیو + صدا با هم** | Qwen2.5-Omni 3B/7B | Video-MME بدون زیرنویس، 7B = 64.3؛ با زیرنویس 72.4 | [GitHub](https://github.com/qwenlm/qwen2.5-omni) |
| **تصویر/OCR/کپشن** | Florence-2 (MIT)، و vision workflow موجود در ریپو | قبلاً در این پروژه استفاده شده | `VISION.md` |

**مسیر پیشنهادی برای «ویدیو را کامل ببیند و بشنود»:**
1. ffmpeg: استخراج صدا + فریم‌های scene-change با timestamp
2. faster-whisper: transcript با timestamp
3. SmolVLM2 یا Qwen2.5-VL روی فریم‌ها (با timestamp)
4. ادغام در یک timeline JSON → خلاصه با LLM متنی
5. خروجی: زمان‌بندی رویدادها + متن گفته‌شده + توصیف تصویری

**هشدار محیط:** sandbox ما فقط ۲ CPU و ۳ GB RAM دارد. GitHub Actions (تقریباً ۷.۹ GB RAM طبق تجربه‌ی قبلی) برای مدل‌های ۲B+ کند است. این مسیرها روی Actions تست می‌شوند، نه sandbox.

## ۶. Google Drive به‌عنوان منبع فایل

- Drive API با `files.get?alt=media` و هدر `Range: bytes=…` دانلود جزئی/قابل‌ازسرگیری می‌دهد ([Gist](https://gist.github.com/tanaikech/dfdad37859d591526b2fba8fb4390cf5)). `MediaIoBaseDownload` در پایتون Range را ندارد.
- ffmpeg می‌تواند مستقیماً از URL با هدر Authorization بخواند و نیازی به دانلود کامل نباشد.
- کانکتور Google Drive در این گفتگو فعال است. اما `download_file` محتوا را base64 برمی‌گرداند و برای فایل بزرگ مناسب نیست؛ برای فایل بزرگ `return_download_url=true` لازم است.

## ۷. محدودیت شبکه‌ی sandbox

sandbox فقط به github.com، api.github.com، codeload، registry.npmjs.org، pypi.org و files.pythonhosted.org دسترسی دارد. **api.telegram.org و MTProto به‌طور مستقیم از sandbox در دسترس نیستند.** پس تست زنده‌ی تلگرام فقط روی GitHub Actions (که دسترسی دارد) یا روی سرور شما ممکن است، مثل Florence.

## ۸. تصمیم‌های لازم از کاربر

1. **کجا بات همیشه روشن باشد؟** GitHub Actions حداکثر ۶ ساعت اجرا دارد و برای bot دائمی مناسب نیست. گزینه‌ها: سرور/VPS شخصی یا Docker روی سیستم خودتان.
2. **حساب MTProto:** آیا حساب تست جدا با شماره‌ی خودتان ایجاد می‌کنید؟ (api_id و api_hash از my.telegram.org، فقط توسط خودتان. من آن‌ها را در چت نمی‌گیرم؛ باید به‌عنوان GitHub Secret یا env روی سرور تنظیم شود.)
3. **با توجه به بند ۱.۵ ToS:** آیا فقط از **Bot API** (فایل‌هایی که کاربر به بات می‌فرستد) استفاده کنیم، یا خواندن کانال عمومی هم لازم است؟ ریسک حقوقی و حساب را شما تصمیم بگیرید.
4. **نقطه‌ی شروع:** Hermes (Python، پایه‌ی مناسب‌تر برای این repo) یا OpenClaw (Node، بالغ‌تر در Telegram)؟

## ۹. پیشنهاد فاز بعدی (برای بعد از تأیید)

- **فاز ۱ (کم‌ریسک):** بات Bot API + Local Bot API در Docker. کاربر فایل تا ۲ GB می‌فرستد؛ ایجنت آن را دانلود، فریم/صدا استخراج، و تحلیل می‌کند. تست روی Actions با یک فایل نمونه.
- **فاز ۲:** Drive ↔ Telegram: لینک Drive یا فایل بزرگ → استریم با Range → همان pipeline.
- **فاز ۳ (پرریسک، فقط با تأیید):** MCP حساب تست برای خواندن کانال‌های allowlist (chigwell/telegram-mcp با `TELEGRAM_ALLOWED_CHAT_IDS`).
- **همیشه:** QA خودکار، زمان‌بندی FloodWait، کش، و نگه‌داشتن هیچ کلید یا session در ریپو.

## منابع

- Telegram API ToS: https://core.telegram.org/api/terms
- Creating your Telegram app: https://core.telegram.org/api/obtaining_api_id
- Bot API: https://core.telegram.org/bots/api
- Bots FAQ: https://core.telegram.org/bots/faq
- Local Bot API (توضیح در bigmike): https://bigmike.help/en/devops/local-telegram-bot-api-advantages-limitations-of-the-standard-api-and-set-eb4a3b/
- chigwell/telegram-mcp: https://github.com/chigwell/telegram-mcp
- OpenClaw Telegram docs: https://github.com/openclaw/openclaw/blob/main/docs/channels/telegram.md
- Hermes Agent: https://hermes-agent.nousresearch.com/
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- SmolVLM2: https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct
- Qwen2.5-VL report: https://arxiv.org/pdf/2502.13923
- Qwen2.5-Omni: https://github.com/qwenlm/qwen2.5-omni
- Google Drive partial download (Gist): https://gist.github.com/tanaikech/dfdad37859d591526b2fba8fb4390cf5
