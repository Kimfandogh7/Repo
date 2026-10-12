# تحقیق دور دوم: پروژه‌های متن‌باز برای دسترسی کامل ایجنت به کانال‌های تلگرام + فهم کامل ویدیو (2026-10-12)

> دور اول (`telegram-agent.md`) زودهنگام بود و فقط بخش Telegram را دید. این دور از چند منبع (GitHub، Hugging Face، Reddit، داک‌های رسمی OpenClaw/Hermes، arXiv) جمع شده است.
> **licenseها:** فقط جایی که در صفحه‌ی منبع دیدم نوشته شده. بقیه «نامشخص — باید قبل از استفاده چک شود».

## الف) دسترسی به محتوای کانال (عمومی و خصوصی) با حساب کاربر

کانال خصوصی فقط وقتی قابل خواندن است که حساب شما عضو آن باشد. Bot API هم برای کانال خصوصی جز با ادمین بودن بات راه ندارد.

| پروژه | چه می‌کند | license | نکته |
|---|---|---|---|
| **GeiserX/Telegram-Archive** | بک‌آپ افزایشی کامل کانال/گروه از جمله media، **ویرایش‌ها و پیام‌های حذف‌شده**، واکنش‌ها، pinned، poll، topic، و voice transcription از طریق سرویس رونویسی. Web viewer و export به JSON. Docker یا pip. با Telethon | GPL-3.0-or-later | **بهترین گزینه برای «آرشیو یک‌بار، تحلیل محلی»**: ایجنت از SQLite محلی می‌خواند و دیگر دائم به تلگرام درخواست نمی‌زند. [repo](https://github.com/GeiserX/Telegram-Archive) |
| **iyear/tdl** (و fork `xbin5678/telegram-tdl`) | دانلود سریع از کانال‌های عمومی و خصوصی (با لینک یا JSON خروجی Desktop)، آپلود، و export مدیا. با سشن Desktop یا QR لاگین می‌کند | **AGPL-3.0** | AGPL یعنی اگر آن را در سرویس شبکه‌ای به کار ببرید، باید کد شما هم منتشر شود. برای مصرف شخصی مشکلی نیست. [repo](https://github.com/xbin5678/telegram-tdl) |
| **ffimnsr/tw-dl** (Rust) | دانلود از لینک‌های عمومی و خصوصی (`t.me/c/…`)، batch با checkpoint و resume، **`--include-comments`** (کامنت‌های زیر پست)، metadata sidecar، hook بعد از هر دانلود | **MIT** | مناسب‌ترین CLI برای یک ایجنت، چون خروجی JSON و hook دارد. [repo](https://github.com/ffimnsr/tw-dl) |
| **zckyachmd/telegram-media-downloader** | مانیتور realtime کانال‌ها، backfill با فیلتر تاریخ، چند حساب، صف دوگانه، auto-forward، داشبورد وب، Docker | **MIT** | Node 22+. برای «دائم کانال را نگه دار» مناسب است. [repo](https://github.com/zckyachmd/telegram-media-downloader) |
| **Dineshkarthik/telegram_media_downloader** | دانلود از کانال‌های خصوصی حتی با no-forward (طبق Reddit؛ تست نشده) | نامشخص | پرستاره ولی نامطمئن. |
| **kavidu-dilhara/tgdl** | CLI با فیلتر نوع/اندازه، download-link | نامشخص | PyPI: `tgdl` |

### MCP سرور برای حساب کاربر (ایجنت مستقیماً بخواند)

| پروژه | قابلیت خواندن | license | نکته |
|---|---|---|---|
| **bstuff/telegram-mcp** (teleproto) | `get_history` با فیلتر، `search_messages`، `get_replies` (کامنت‌ها)، `list_media` + `download_media`، **`chat_digest`** (آمار)، `get_unread` **بدون mark-read**، `TELEGRAM_MCP_READ_ONLY=1` | نامشخص | **بهترین ابزار خواندن read-only** برای ایجنت. [repo](https://github.com/bstuff/telegram-mcp) |
| **chigwell/telegram-mcp** (Telethon) | گسترده‌ترین (ده‌ها ابزار)، `TELEGRAM_ALLOWED_CHAT_IDS` (allowlist کانال)، `TELEGRAM_EXPOSED_TOOLS=read-only`، مسیر فایل safe-by-default، voice transcription با کش، sanitize برای prompt-injection. commit امروز | نامشخص (باید چک شود) | اگر allowlist و read-only را اجباری کنیم، مناسب‌ترین است. [repo](https://github.com/chigwell/telegram-mcp) |
| **0xMRK95/telegram-mcp-server** | `scan_channels_content` (اسکن دسته‌ای کانال‌ها با timeout و خروجی JSON) | نامشخص | برای «بررسی چند کانال» مفید است. [repo](https://github.com/0xMRK95/telegram-mcp-server) |
| **Schimmilab/telegram-mcp-server** | `get_recent_media`، `download_media`، `search_messages` سراسری، با `chat_id` در نتیجه | نامشخص | README آلمانی؛ ساده. [repo](https://github.com/Schimmilab/telegram-mcp-server) |
| **mcp-telegram/mcp-telegram** (GramJS) | ۱۸۲ ابزار؛ read، download، stories، forum topics، transcription | نامشخص | بیش‌ازحد بزرگ؛ سطح ریسک بالا (گزینه‌های write زیاد). |
| **sparfenyuk/mcp-telegram** | read-only، download media | نامشخص | ساده و محافظه‌کارانه. |
| **adlandh/telegram-mcp** (Go) | read-only پیش‌فرض، HTTP فقط loopback با Bearer، سقف دانلود ۲۰۰ MB | نامشخص | امنیت خوب؛ ارسال پیام ندارد. |

**رد شد:** `n24q02m/better-telegram-mcp` در ۲۰۲۶-۰۹-۱۳ **archive** شده و دیگر نگه‌داری نمی‌شود.

## ب) فهم کامل ویدیو: تصویر + صدا + زمان‌بندی

### ب۱) الگوهای آماده (agent skill / pipeline)

| پروژه | روش | license | نکته |
|---|---|---|---|
| **bradautomates/claude-video** (`/watch`) | yt-dlp → استخراج فریم (keyframe / scene-change / uncapped) → captions اگر باشد، وگرنه Whisper → فریم‌ها و transcript با timestamp به مدل میزبان داده می‌شود | **MIT** | بیش از ۵ هزار ستاره؛ موتور صدا Groq/OpenAI. **نقص برای ما:** Whisper API و فهم تصویر به مدل هاست وابسته است. [repo](https://github.com/bradautomates/claude-video) |
| **UbiqWare/claude-video** (fork) | همان + whisper.cpp محلی با large-v3-turbo چندزبانه | MIT | برای اجرای کاملاً محلی مناسب‌تر. [repo](https://github.com/UbiqWare/claude-video) |
| **MarcinDudekDev/video-caption** | فریم با ffmpeg (پیش‌فرض ۲ fps) → هر فریم با VLM محلی (qwen3-vl:4b با Ollama) همراه context گفتار → Whisper large-v3-turbo → **merge بر اساس timestamp** → JSON. ۵۶ آزمایش، ادعای صفر hallucination روی ۷۹۰ اجرا | **MIT** | **نزدیک‌ترین به خواسته‌ی «تصویر و صدا با هم»** و خروجی ساختاریافته. Apple Silicon (mlx) تنظیم شده؛ engine=`ollama` روی لینوکس هم هست. [repo](https://github.com/MarcinDudekDev/video-caption) |
| **SalZaki/video-analysis-workbench** | ffmpeg frames + whisper-cpp محلی، برای Claude Code | نامشخص | کاملاً offline. |
| **stevederico/video-understanding** | frames با timestamp + Whisper SRT → `understanding.md` که visuals و speech را کنار هم می‌گذارد | نامشخص | ساده و قابل ادغام. |
| **AI-Video-Transcriber** (wendy7756) | yt-dlp + faster-whisper + خلاصه‌سازی | نامشخص | بیشتر برای transcript/خلاصه است، نه تصویر. |

### ب۲) مدل‌های متن‌باز که ویدیو (و گاهی صدا) را مستقیم می‌فهمند

| مدل | ورودی | license | وزن/سخت‌افزار | امتیاز یا نکته | منبع |
|---|---|---|---|---|---|
| **OmniAgent-RL-7B** (ICML 2026) | ویدیو + صدا + تصویر، **با حلقه‌ی Observe-Think-Act** (`get_frames`، `get_audio`، `get_clip`) | کد **Apache-2.0**؛ وزن روی Qwen2.5-Omni-7B | 7B؛ به GPU نیاز دارد یا کوانتیزه | LVBench **50.5** با ۷۳٪ فریم کمتر از Qwen2.5-VL-72B (47.3)؛ DailyOmni +4.7. **ایده‌آل برای ویدیوی بلند** چون فقط بخش لازم را نگاه می‌کند. | [code](https://github.com/HarryHsing/OmniAgent)، [HF](https://huggingface.co/harryhsing/OmniAgent-RL-7B) |
| **Gemma 3n E2B / E4B** (Google) | متن + **تصویر + ویدیو (فریم) + صدا** | Gemma license (نه Apache) | E4B حدود ۴B مؤثر؛ `ollama gemma3n:e4b` حدود ۷.۵ GB (Q4) | **تنها مدل کوچک یکپارچه‌ای که صدا و تصویر را با هم دارد** و برای CPU/لپ‌تاپ طراحی شده. کیفیت ویدیو را باید روی نمونه‌ی خودمان بسنجیم. | [HF](https://huggingface.co/google/gemma-3n-E4B)، [HF blog](https://huggingface.co/blog/gemma3n) |
| **Qwen3-Omni-30B-A3B** (Alibaba) | متن، تصویر، صدا تا ۴۰ دقیقه، ویدیو + صدا | Qwen License | BF16: **۷۹–۱۴۵ GB VRAM** برای ۱۵–۱۲۰ ثانیه ویدیو؛ ۴-bit حدود ۱۷–۲۵ GB | بهترین open omni در جدول‌ها (Video-MME بدون زیرنویس ۷۰.۵؛ MMAU ۷۷.۵). **روی GitHub Actions غیرممکن.** | [HF](https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct)، [arXiv](https://arxiv.org/html/2509.17765v1) |
| **Qwen2.5-VL-3B / 7B** | ویدیو با time-encoding | 3B: نامشخص؛ 7B: Qwen Research License | 7B؛ GPU | Video-MME بدون زیرنویس: 7B = 65.1، 3B = 61.5 | [arXiv](https://arxiv.org/pdf/2502.13923) |
| **SmolVLM2** 256M / 500M / 2.2B | ویدیو (فریم به صورت multi-image)، **بدون صدا** | **Apache-2.0** | 500M ≈ 1.8 GB GPU RAM | Video-MME: 500M = 42.2، 2.2B = 52.1. **کوچک‌ترین مدل ویدیویی.** صدا را باید با Whisper بدهیم. | [HF](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) |
| **Qwen2.5-Omni-7B** | ویدیو + صدا | Qwen | 7B | پایه‌ی OmniAgent؛ Video-MME بدون زیرنویس 64.3 | [GitHub](https://github.com/qwenlm/qwen2.5-omni) |

**یادداشت درباره‌ی Qwen3.5-Omni و Qwen3.8-Omni-Flash:** فقط در وبلاگ‌ها و جدول‌های vendor-reported دیدم. **وزن بازِ آن‌ها تأیید نشد؛ حساب نمی‌کنم.**

### ب۳) صدا (شنیدن)

| ابزار | license | نکته |
|---|---|---|
| **faster-whisper** | MIT | CTranslate2؛ int8 روی CPU. مدل small روی CPU ۱۳ دقیقه صدا را در ~۱m42s با ۸ thread. large-v3-turbo (۸۰۹M) تعادل بهتر کیفیت/سرعت |
| **whisper.cpp** | MIT | C++؛ برای لپ‌تاپ و ARM؛ fork claude-video از آن استفاده می‌کند |
| **Gemma 3n / Qwen-Omni / OmniAgent** | بالا | صدای مستقیم بدون Whisper (کیفیت صوت محیطی در Qwen3-Omni: ۵۵.۹ در برابر تصویر ۶۲.۱) |

## ج) ایجنت/گیت‌وی که خودش تلگرام، رسانه و cron دارد

| پروژه | license | تلگرام | رسانه و ویدیو | نکته |
|---|---|---|---|---|
| **Hermes Agent** (Nous Research) | **MIT**، Python | Telegram، Discord، Slack، WhatsApp، Signal، Email؛ ۲۰+ پلتفرم | رونویسی خودکار voice، vision، TTS، cron، subagent، ۷ backend اجرا (local/Docker/SSH/Modal…)؛ MCP | با Python این repo همخوان است. [site](https://hermes-agent.nousresearch.com/) |
| **OpenClaw** | **MIT**، Node 22+ | grammY؛ long polling؛ عکس/آلبوم/صوت/ویدیو؛ `apiRoot` برای Local Bot API؛ `trustedLocalFileRoots` | **Media understanding** با provider و **CLI محلی** (مثلاً whisper یا gemini CLI به‌عنوان fallback). ویدیو فقط با Google Gemini API آماده است؛ برای ما باید CLI محلی یا backend خودمان را وصل کنیم | مستندات کامل. [docs](https://docs.openclaw.ai/tools/media-overview)، [media understanding](https://docs.openclaw.kr/nodes/media-understanding) |
| **Untether** | نامشخص | بات bridge بین agent و تلگرام با voice و file transfer | — | در awesome-telegram معرفی شده؛ بررسی نشد. |

**نکته مهم درباره‌ی OpenClaw:** مستندات OpenClaw برای فهم ویدیو به‌صورت پیش‌فرض Gemini API را می‌خواهد. قانون ما «بدون vendor API» است، پس باید آن قسمت را با یک backend محلی جایگزین کنیم (CLI/HTTP به SmolVLM2 یا Gemma 3n یا OmniAgent). این یک نقطه‌ی اتصال مشخص است و پیاده‌سازی آن ساده است.

## د) Google Drive به‌عنوان منبع فایل بزرگ

- Drive API با `alt=media` و هدر `Range` دانلود جزئی و resume می‌دهد. `MediaIoBaseDownload` در پایتون Range ندارد ([Gist](https://gist.github.com/tanaikech/dfdad37859d591526b2fba8fb4390cf5)).
- ffmpeg می‌تواند از URL با هدر Authorization مستقیم بخواند و نیازی به دانلود کامل ندارد.
- کانکتور Google Drive در گفتگو فعال است. `download_file` برای فایل بزرگ مناسب نیست؛ باید `return_download_url=true` استفاده شود.

## ه) نتیجه: آیا یک پروژه‌ی واحد وجود دارد؟

**نه.** هیچ‌کدام از موارد بالا همه‌ی زنجیره را پوشش نمی‌دهد:
1. دسترسی حساب به کانال خصوصی/عمومی + دانلود همه‌ی مدیا + کامنت‌ها → Telegram-Archive یا tw-dl / tdl
2. آرشیو و جست‌وجو و خواندن ایجنت → bstuff یا chigwell MCP (read-only)
3. فهم ویدیو کامل (تصویر + صدا + زمان) → video-caption (ساختار) + Gemma 3n یا OmniAgent (فهم) + faster-whisper (صدا)
4. گیت‌وی تلگرام، cron، حافظه → Hermes یا OpenClaw
5. فایل بزرگ از Drive → Range streaming

یعنی باید **۴ جزء را به هم وصل کنیم**. هیچ‌کدام به‌تنهایی «هر چیزی را کامل» نمی‌بیند.

## و) محدودیت‌های واقعی (نه تبلیغاتی)

- **ToS تلگرام، بند ۱.۵:** استفاده از داده‌ی تلگرام برای «توسعه یا deployment هوش مصنوعی» ممنوع است. **این شامل همه‌ی پروژه‌های بالاست** (همه از همان MTProto استفاده می‌کنند). این را کاربر باید تصمیم بگیرد.
- **ریسک حساب:** حساب کاربر با FloodWait و بَن روبه‌روست. Telegram-Archive و tw-dl با تنظیمات محافظه‌کارانه می‌آیند ولی ریسک صفر نیست.
- **CPU و RAM:** runner گیت‌هاب حدود ۸ GB RAM دارد (تجربه‌ی قبلی). OmniAgent-7B و Qwen3-Omni روی آن اجرا نمی‌شوند. Gemma 3n E4B (Q4) و SmolVLM2-500M و faster-whisper small/turbo شدنی هستند.
- **ویدیوی بلند (بیش از ۱ ساعت):** «کامل دیدن» یعنی نمونه‌برداری هوشمند + transcript + درخواست کلیپ. OmniAgent دقیقاً همین را انجام می‌دهد؛ بقیه فقط نمونه‌برداری ثابت دارند.
- **sandbox:** فقط GitHub/npm/PyPI. تست MTProto و Bot API فقط روی Actions یا سرور.

## ز) سؤال‌هایی که قبل از پیاده‌سازی باید جواب داده شوند

1. آیا حساب تست جدا برای خواندن کانال‌ها داریم؟ (api_id/api_hash باید خود کاربر بگیرد.)
2. آیا خواندن کانال‌های عمومی/خصوصی با پیش‌زمینه‌ی ToS §۱.۵ مشکلی ندارد؟ (تصمیم حقوقی کاربر)
3. مدل فهم ویدیو: Gemma 3n E4B (سبک، صدا+تصویر) یا OmniAgent-7B (دقیق‌تر، سنگین‌تر، فقط با GPU)؟
4. ایجنت گیت‌وی: Hermes (Python) یا OpenClaw (Node)؟
5. کجا اجرا شود؟ (VPS یا سیستم خودتان؛ Actions برای سرویس دائمی مناسب نیست.)

## منابع

- Telegram-Archive: https://github.com/GeiserX/Telegram-Archive
- iyear/tdl: https://github.com/xbin5678/telegram-tdl (fork، License AGPL-3.0)
- tw-dl: https://github.com/ffimnsr/tw-dl
- zckyachmd/telegram-media-downloader: https://github.com/zckyachmd/telegram-media-downloader
- bstuff/telegram-mcp: https://github.com/bstuff/telegram-mcp
- chigwell/telegram-mcp: https://github.com/chigwell/telegram-mcp
- 0xMRK95/telegram-mcp-server: https://github.com/0xMRK95/telegram-mcp-server
- mcp-telegram/mcp-telegram: https://github.com/mcp-telegram/mcp-telegram
- sparfenyuk/mcp-telegram: https://github.com/sparfenyuk/mcp-telegram
- claude-video: https://github.com/bradautomates/claude-video
- UbiqWare fork (whisper.cpp): https://github.com/UbiqWare/claude-video
- video-caption: https://github.com/MarcinDudekDev/video-caption
- OmniAgent: https://github.com/HarryHsing/OmniAgent ، https://huggingface.co/harryhsing/OmniAgent-RL-7B
- Gemma 3n: https://huggingface.co/google/gemma-3n-E4B ، https://huggingface.co/blog/gemma3n
- Qwen3-Omni: https://github.com/QwenLM/Qwen3-Omni ، https://huggingface.co/Qwen/Qwen3-Omni-30B-A3B-Instruct
- Qwen2.5-VL report: https://arxiv.org/pdf/2502.13923
- SmolVLM2: https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- Hermes Agent: https://hermes-agent.nousresearch.com/
- OpenClaw: https://docs.openclaw.ai/tools/media-overview ، https://github.com/openclaw/openclaw/blob/main/docs/channels/telegram.md
- Telegram API ToS: https://core.telegram.org/api/terms
- Telethon entities: https://docs.telethon.dev/en/stable/concepts/entities.html
- Drive partial download: https://gist.github.com/tanaikech/dfdad37859d591526b2fba8fb4390cf5
- awesome-telegram: https://github.com/ebertti/awesome-telegram
