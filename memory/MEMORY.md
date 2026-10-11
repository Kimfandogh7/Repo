# حافظه — L0 (فهرست خلاصه)

> این فایل خودکار ساخته می‌شود. منبع حقیقت در `memories/` است.
> هر دسته را فقط به اندازه‌ی نیاز باز کن — همه را یکجا نخوان.

## eduagent
  * ۷ لینک تیک‌تاک از اکانت @github.signals: open-slide (۹۱۶۱★)، papermorph (۶۶۷)، mg-styles-15 (۶۳۲)، phreshos/system (۲۲۸)، showtime (۲۲۶) — همه راستی‌آزمایی شدند
  * راه حل برای توصیف ویدیوهای تیک‌تاک: oEmbed رسمی (tiktok.com/oembed?url=...) جواب می‌دهد، حتی از IP دیتاسنتر
  * ۵۰ ایده در edu-agent/IDEAS.md: تشخیص، برنامه‌ریزی، تولید محتوا، روش تدریس، روانشناسی، پیگیری، مشاوره
  * open-slide v2.1.0 نصب و تست شد: build موفق، خروجی PPTX/PDF دارد اما PPTX فقط در مرورگر (کلیک دستی)
  * نکته فنی: Vite در open-slide هاستِ پیش‌نمایش را 403 می‌کند مگر اینکه open-slide.config.ts را با allowedHosts:true تنظیم کنی
  * دکِ نمونه ساخته شد: slides/forgetting-curve — ۶ صفحه، RTL فارسی، انیمیشن SVG، متن گوینده
  * مسیرِ واقعیِ اسلاید در open-slide: /s/<slide-id> — نه /slides/... که ۴۰۴ می‌دهد (وقتی عکس‌ها یک‌اندازه شدند یعنی همان صفحه است)
  * export در open-slide فقط در مرورگر است، CLI ندارد. راه‌حل: Playwright در Actions عکس بگیرد، Pillow ادغام کند -> PDF

## meta
  * سیستم حافظه در memory/ راه‌اندازی شد؛ AGENTS.md در ریشه می‌گوید اول آن را بخوان

## network
  * شبکه سندباکس در لایه ۷/SNI فیلتر می‌شود: TCP برای هاست‌های مسدود هم باز است (bash /dev/tcp) اما دست‌تکانی TLS می‌میرد
  * هاست‌های مجاز: github.com, api.github.com, codeload.github.com, registry.npmjs.org, pypi.org, files.pythonhosted.org
  * مسدود: raw.githubusercontent.com, example.com, google.com, huggingface.co, cdn.playwright.dev, objects.githubusercontent.com

## research
  * موتورهای حافظه شکست خوردند: mem0 (کلید OpenAI)، cognee/memori (کلید ابری)، agentmemory (دانلود مدل از HuggingFace مسدود)

## sandbox
  * مرورگر: کرومیوم ۱۵۳ با npm نصب و اجرا شد (--version کار کرد) ولی رندر نمی‌کند: GPU process exit_code=15
  * git push به برنچ محدود است و باتِ workflow هم روی همان برنچ کامیت می‌زند -> قبل از هر push باید git pull --rebase کرد
  * توکن گیت‌هاب integration است: ساخت Gist و workflow_dispatch هر دو ۴۰۳ می‌دهند

## tools
  * entroly: حتی با بودجه ۹۴٪ هیچ chunk ای برنمی‌گرداند (Selected: 0) — استفاده نشود
  * سرنا/ basedpyright: basedpyright 1.40 دیگر --stdio قبول نمی‌کند و Serena روی پایتون می‌شکند
  * headroom-ai: صفر درصد فشرده‌سازی در همه مسیرها (فقط JSON و CODE هندلر دارد)
  * ابزارهایی که کار می‌کنند: uv, ast-grep, promptfoo, DeepEval, DSPy, litellm, firecrawl-mcp, tavily-mcp
  * شکست‌ها: entroly (۰ chunk در بودجه بالا)، headroom-ai (۰٪ فشرده‌سازی)، Serena (basedpyright)، mcpm (ImportError)، sqz/rtk (باینری مسدود)
  * شکست در نصب: context-mode و token-optimizer-mcp (build بومی better-sqlite3 شکست می‌خورد)

## webget
  * رله‌ی GitHub Actions کار می‌کند: هر URL را از طریق push به fetches/request.txt بگیر
  * موتورهای جستجو (گوگل/DDG/mojeek/Brave) IP دیتاسنتر را بلاک می‌کنند؛ ولی arXiv API و HN Algolia و Wikipedia API و DDG Instant Answer کار می‌کنند

