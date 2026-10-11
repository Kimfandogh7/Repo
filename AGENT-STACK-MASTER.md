# کتابِ جامع ارتقای ایجنت: پژوهش + کیت نصب + نتایج تست سخت‌گیرانه

**تاریخ:** ۲۰۲۶-۱۰-۱۱ · **نسخه:** ۱.۰ · یک فایلِ واحد (ادغام دو دور پژوهش + نتایج تست واقعی)

> این فایل جایگزین دو فایل قبلی است و **همه چیز** را در خود دارد:
> ① نقشه پژوهشی (مقالات، بنچمارک‌ها، تبارشناسی شکست) · ② کیت نصب عملیاتی ·
> ③ **نتایج تست‌های سخت‌گیرانه‌ای که واقعاً روی ماشین اجرا شد** (نه نقل قول از سازنده).

---

## فهرست

1. [چارچوب مفهومی: ایجنت = مدل + هارنس](#1)
2. [نتایج تست‌های سخت‌گیرانه (بخش طلایی)](#2)
3. [کاتالوگ کامل پروژه‌ها](#3)
4. [کیت نصب](#4)
5. [کاهش خطا، حلقه‌های کیفیت و Verification](#5)
6. [مقالات کلیدی](#6)
7. [منابع دنبال‌کردن](#7)
8. [نقشه راه پیشنهادی](#8)
9. [پیوست: بازتولید تست‌ها](#9)

---

<a name="1"></a>
## ۱. چارچوب مفهومی: ایجنت = مدل + هارنس (Harness)

بزرگترین تغییر نگاهِ ۲۰۲۶: **بیشترِ پیشرفت از خودِ مدل نمی‌آید، از لایه‌ی دورِ مدل می‌آید.**
تعریف رسمی از `ai-boost/awesome-harness-engineering` (۴.۸k⭐):

> «مهندسی هارنس، دیسیپلینِ طراحیِ داربستِ دور ایجنت است: تحویل کانتکست، رابط ابزارها، مصنوعات برنامه‌ریزی، حلقه‌های verification، سیستم حافظه و سندباکس. هر کامپوننتی اینجا هست چون مدل به‌تنهایی نمی‌تواند انجامش دهد — و بهترین هارنس‌ها می‌دانند این کامپوننت‌ها با بهتر شدن مدل حذف خواهند شد.»

**۱۲ لایه‌ای که می‌توان روی هرکدام کار کرد:**

| # | لایه | سؤال |
|---|------|------|
| 1 | مدل پایه | چقدر باهوش است؟ |
| 2 | حافظه | چیزی یادش می‌ماند؟ |
| 3 | کانتکست/فشرده‌سازی | چه می‌بیند؟ چقدر هزینه دارد؟ |
| 4 | ابزارها و MCP | به چه دسترسی دارد؟ |
| 5 | مهارت‌ها و AGENTS.md | بلد است کارها را «چطور» انجام دهد؟ |
| 6 | برنامه‌ریزی/تجزیه | می‌تواند کار بزرگ را خرد کند؟ |
| 7 | ارکستراسیون | می‌تواند موازی کار کند؟ |
| 8 | Verification | می‌فهمد کار درست انجام شده؟ |
| 9 | دوام/بازیابی | اگر کرش کند از سر می‌گیرد؟ |
| 10 | امنیت/سندباکس | چه بلایی می‌تواند سر سیستم بیاورد؟ |
| 11 | ارزیابی/مشاهده‌پذیری | می‌فهمی کجا خراب کرده؟ |
| 12 | خودبهبودی/RL | با تجربه بهتر می‌شود؟ |

---

<a name="2"></a>
## ۲. 🎯 نتایج تست‌های سخت‌گیرانه (بخش طلایی)

> **روش:** یک محیط ایزوله (Python 3.11 / Node 22) ساخته شد و هر ابزار نصب و **واقعاً اجرا** شد.
> اندازه‌گیریِ توکن با **شمارشگر واقعی cl100k_base** (از طریق `js-tiktoken` که داده را داخل بسته دارد، چون `tiktoken` باید فایل BPE را از اینترنت بگیرد).
> برای هر ابزار یک «کنترل منفی» هم طراحی شد تا مطمئن شویم ابزار فقط مُهر تأیید نمی‌زند.
>
> ⚠️ **محدودیتِ صادقانه:** این سندباکس فقط به `github.com`، `api.github.com`، `registry.npmjs.org` و `pypi.org` دسترسی دارد. پس ابزارهایی که باینریِ Rust از GitHub Releases می‌گیرند، یا به کلید API / داکر / GPU نیاز دارند، **در اینجا قابل تست نبودند** — و این دقیقاً با برچسب «قابل‌تست‌نبود» مشخص شده، نه با نمره‌ی قبولی.

### ۲.۱ خلاصه‌ی یک‌نگاه

| ابزار | نسخه | حکم | دلیل |
|---|---|---|---|
| **uv** | 0.13 | ✅ **PASS** | ساخت venv + نصب بسته واقعی |
| **ast-grep** | 0.50 | ✅ **PASS** | جستجوی ساختاری روی AST، هر دو تابع را یافت |
| **dotenvx** | 2.34 | ✅ **PASS** | رمزگذاری؛ متنِ صریح در فایل پنهان ماند؛ `get` مقدار را درست برگرداند |
| **pydantic-ai** | 2.55 | ✅ **PASS** | اجرای واقعی ایجنت آفلاین با `TestModel` + فراخوانی ابزار |
| **DSPy** | 3.4 | ✅ **PASS** | ساخت Signature + استنتاج با `DummyLM` |
| **DeepEval** | 4.2 | ✅ **PASS** | متریک قطعی: نمونه مثبت True، نمونه منفی False |
| **promptfoo** | 0.124 | ✅ **PASS** | ارزیابی کامل + **کنترل منفی: شکست‌ها را هم درست گزارش داد** |
| **litellm** | 1.104 | ✅ **PASS** | اپلیکیشن proxy با ۸۰ route بالا آمد |
| **sequential-thinking** (MCP) | 2026.8.31 | ✅ **PASS** | دست‌دهی stdio + فراخوانی واقعی ابزار + ردیابی بازنگری |
| **firecrawl-mcp** | 3.29 | ✅ **PASS**‌(جزئی) | دست‌دهی + ۲۷ ابزار؛ اجرا بدون کلید اما وابسته به شبکه‌ی خودش |
| **tavily-mcp** | 0.22 | ✅ **PASS**‌(جزئی) | دست‌دهی + ۵ ابزار، حالت بدون‌کلید |
| **skills** (۳ مخزن) | — | ✅ **PASS** | ۷۳ فایل SKILL.md؛ **۳۵/۳۵ منطبق با spec** |
| **smolagents / mem0ai / graphiti-core / verifiers / opik** | — | 🟡 **فقط import** | نصب و import شدند؛ عملکردِ اصلی به مدل/پایگاه‌داده/کلید نیاز دارد |
| **Serena** | آخرین git | 🟠 **نیمه‌شکسته** | ۲۳ ابزار را درست expose می‌کند، ولی **language server پایتون بالا نمی‌آید** (پایین را ببین) |
| **headroom-ai** | 0.40 | 🔴 **ادعا تأیید نشد** | **۰٫۰٪ فشرده‌سازی** روی هر ۴ سناریوی واقعی |
| **entroly** | 1.0.86 | 🔴 **شکست** | آفلاین کرش می‌کند؛ جایی هم که اجرا شد ۰٪ کاهش + از دست دادن نشانگرهای بحرانی |
| **sqz** | 2.0.0 | 🔴 **شکست** | نصب pip فقط یک wrapper است؛ باینری از GitHub Releases (بلاک) |
| **mcpm** | 2.15 | 🔴 **شکست** | `ImportError: cannot import name 'AnyFunction' from 'mcp.types'` |
| **context-mode / token-optimizer-mcp** | — | 🔴 **شکست** | خطای کامپایل نیتیوِ `better-sqlite3` |
| **rtk** (PyPI) | 0.3.14 | 🔴 **تصادفِ اسمی** | این پکیج اصلاً آن پروژه نیست |
| **claude-mem** | 1.0.3 | 🟠 **قابل‌تست‌نبود** | اجرایی ندارد؛ پلاگینِ Claude Code است |
| **exa-mcp-server** | 3.4.2 | 🟠 **قابل‌تست‌نبود** | بدون `EXA_API_KEY` خارج می‌شود |
| mise / devbox / flox / pkgx | — | ⬜ **نصب‌نشدنی اینجا** | باینری از هاست‌های بلاک |
| E2B / Daytona / Modal | — | ⬜ **قابل‌تست‌نبود** | سرویس ابری |

---

### ۲.۲ 🔴 مهم‌ترین یافته: headroom ادعای اصلی‌اش را در عمل محقق نکرد

headroom (۷۴,۹۲۸⭐) می‌گوید «خروجی ابزارها را فشرده می‌کند، ۲۰٪ توکن کمتر برای coding agent، ۶۰–۹۵٪ برای JSON».
آن را روی چهار ورودی واقعی و با **شمارشگر توکنِ واقعی** آزمودم:

| سناریو | توکن قبل | توکن بعد | کاهش | handler تشخیص‌داده‌شده |
|---|---|---|---|---|
| Payload JSON (۲۰۰ رکورد) | ۲۰٬۵۱۲ | ۲۰٬۵۱۲ | **۰٫۰٪** | json |
| لاگ برنامه (۲۰۰ خط) | ۱٬۹۹۹ | ۱٬۹۹۹ | **۰٫۰٪** | **noop** |
| خروجی pytest | ۵۸ | ۵۸ | **۰٫۰٪** | **noop** |
| سورس پایتون | ۱٬۹۸۰ | ۱٬۹۸۰ | **۰٫۰٪** | code |

سه مسیرِ مختلف را امتحان کردم تا منصفانه باشد:
- `UniversalCompressor` با تنظیمات پیش‌فرض → **۰٪**
- `UniversalCompressor` با `use_kompress=True` → **۰٪**
- API سطح‌بالای `headroom.compress(messages)` (مسیر مستند) → `tokens_before == tokens_after`، **۰٪**

**دو علت ریشه‌ای پیدا کردم:**
1. **فقط دو handler ثبت شده**: کد منبع نشان می‌دهد `UniversalCompressor` تنها برای `JSON` و `CODE` handler دارد. با اینکه enum شامل `LOG` و `DIFF` و `MARKDOWN` هم هست، **هیچ handlerی برای آن‌ها ثبت نشده** — یعنی دقیقاً جایی که ایجنت‌ها بیشترین توکن را هدر می‌دهند (خروجی شل، لاگ تست، `git status`) اصلاً دست نمی‌خورد.
2. **kompress در دسترس نیست**: پیامِ خطا می‌گوید به `onnxruntime` یا `torch` نیاز دارد. حتی پس از نصب `onnxruntime` نسخه‌ی ۱.۳۱، همچنان همان خطا را داد و فشرده‌سازی غیرفعال ماند.

> **قضاوت منصفانه:** ممکن است حالتِ `headroom proxy` (که به یک endpoint واقعی LLM وصل می‌شود) نتایج متفاوتی بدهد — بدون کلید API نتوانستم آن را تست کنم. اما نمی‌توان ادعای «۲۰٪/۶۰-۹۵٪» را از کتابخانه بیرون کشید، و برای خروجیِ شل اصلاً handlerی وجود ندارد.
> **توصیه:** نصب نکنید، مگر اینکه خودتان با اندازه‌گیری روی کارِ واقعی‌تان تأیید کنید.

---

### ۲.۳ 🔴 entroly: وابستگی سخت به اینترنت + از دست دادن اطلاعات بحرانی

`entroly compress` در محیط آفلاین با این خطا شکست خورد:

```
HTTPSConnectionPool(host='openaipublic.blob.core.windows.net'):
  Max retries exceeded — /encodings/o200k_base.tiktoken
```

یعنی برای شمارش توکن، هنگام اجرا از اینترنت فایل می‌گیرد. در دو سناریویی که اجرا شد هم **۰٪ کاهش** داشت و **نشانگرهای بحرانی را از دست داد** (مثلاً رشته‌ی `FAILED` و `AssertionError` در خروجی نماند) — که برای ابزاری که قرار است خروجی تست را خلاصه کند، بدترین نوع خطاست.

---

### ۲.۴ 🔴 سه شکستِ نصب که ارزش دانستن دارند

| ابزار | خطای دقیق | معنا |
|---|---|---|
| **sqz** | `Failed to download sqz from https://github.com/ojuschugh1/sqz/releases/download/...` | بسته‌ی pip فقط یک لانچر است؛ باینری Rust را از GitHub Releases می‌گیرد |
| **mcpm** | `ImportError: cannot import name 'AnyFunction' from 'mcp.types'` | شکستِ وابستگی با نسخه‌ی فعلیِ `mcp` — همان ابزاری که قرار است مدیریتِ MCP را ساده کند، خودش با MCP نمی‌سازد |
| **context-mode / token-optimizer-mcp** | `npm error path .../node_modules/better-sqlite3` | کامپایل نیتیو شکست خورد؛ نصب روی سیستم تمیز جواب نمی‌دهد |

**و یک تله‌ی واقعی:** بسته‌ی `rtk` روی PyPI (نسخه ۰.۳.۱۴) اصلاً `rtk-ai/rtk` نیست — یک کتابخانه‌ی GPIO به نام «RTk.GPIO Python Library» است. اگر کسی `pip install rtk` بزند، چیزی کاملاً بی‌ربط نصب می‌کند.

---

### ۲.۵ 🟠 Serena: ۲۳ ابزار عالی، ولی language server پایتون شکست دارد

**چه چیز تأیید شد:** نصب شد و سرور MCP با ۲۳ ابزار بالا آمد، از جمله دقیقاً همان ابزارهایی که وعده داده بود:
`find_symbol`، `find_referencing_symbols`، `find_implementations`، `find_declaration`، `replace_symbol_body`، `insert_after_symbol`، `rename_symbol`، `safe_delete_symbol`، `get_symbols_overview`، `get_diagnostics_for_file`، به‌علاوه ابزارهای حافظه (`write_memory`/`read_memory`/`list_memories`) و `activate_project`.

**چه شکست خورد:** فعال‌سازی پروژه با این خطا رد شد:
`LanguageServerManagerInitialisationError: Failed to start 1 language server(s): python: ...`

**علت‌الریشه را پیدا کردم** (نه حدس):
- سرور زبان پایتون در Serena همان **basedpyright** است که با فلگ `--stdio` اجرا می‌شود.
- basedpyright نسخه‌ی **۱.۴۰.۲** دیگر این فلگ را قبول نمی‌کند: `Unexpected option --stdio. basedpyright --help for usage`
- نتیجه: پروسه بلافاصله خارج می‌شود → `LanguageServerTerminatedException`.

> **معنا:** روی ماشینی که basedpyright به نسخه‌ی ۱.۴۰+ ارتقا یافته، لایه‌ی «درک معنایی کد» در Serena عملاً کار نمی‌کند تا وقتی نسخه پین شود. این یک شکستِ سازگاریِ واقعی است، نه مشکلِ سندباکس.
> **توصیه:** قبل از تکیه بر Serena، روی پروژه‌ی خودتان `find_symbol` را امتحان کنید؛ اگر language server بالا نیامد، نسخه‌ی basedpyright را پین کنید.

---

### ۲.۶ ✅ ابزارهایی که واقعاً کار کردند (با مدرک)

**promptfoo — کنترلِ منفی هم گذراند.**
یک ارزیابی ساختم که در آن پاسخِ provider عمداً اشتباه بود، تا ببینم آیا promptfoo شکست را گزارش می‌دهد یا فقط مُهر تأیید می‌زند:

```
Results:  0 passed (0%)   ✗ 2 failed (100%)   0 errors
```
یعنی درست گزارش می‌دهد. (خیلی از ابزارهای ارزیابی در این آزمون رد می‌شوند.)

**DeepEval — متریک قطعی:**
نمونه‌ی مثبت → `success: True`؛ نمونه‌ی منفی (خروجی `5` به‌جای `4`) → `negative-case success: False`.

**dotenvx — رمزگذاری واقعی:**
فایل `.env` پس از encrypt دیگر شامل مقدارِ صریح نبود، و `dotenvx get SECRET_TOKEN` مقدار را صحیح برگرداند.

**ast-grep — جستجوی ساختاری:**
روی یک فایل نمونه، هر دو تعریف تابع (یکی در سطح ماژول، یکی متدِ کلاس) را با تشخیص دقیق سطر/ستون یافت.
⚠️ نکته‌ی کاربردی: در نسخه‌ی ۰.۵۰ قانون باید حتماً فیلد `kind` داشته باشد؛ بدون آن خطا می‌دهد: `Rule must specify a set of AST kinds to match`.

**sequential-thinking — فراخوانی واقعی ابزار:**
```
tool: sequentialthinking  →  {"thoughtNumber": 2, "totalThoughts": 3,
                              "nextThoughtNeeded": true, "branches": [],
                              "thoughtHistoryLength": 2}
```
بازنگری (revision) هم درست کار کرد.
⚠️ **اما صادقانه:** همان‌طور که منابع پژوهشی هم می‌گفتند، این سرور **هیچ استدلالی انجام نمی‌دهد** — فقط یک اسکچ‌پدِ بیرونی با state-tracking قطعی است. ارزشش در «بیرونی کردنِ زنجیره‌ی فکر» است، نه در باهوش‌تر شدن.

**litellm:** اپلیکیشن FastAPI با ۸۰ route بالا آمد.
⚠️ نکته: هنگام اجرا سعی می‌کند نقشه‌ی قیمت مدل‌ها را از `raw.githubusercontent.com` بگیرد و در محیط بلاک به نسخه‌ی محلی برمی‌گردد — یعنی در محیط ایزوله قیمت‌ها ممکن است قدیمی باشند.

**مهارت‌ها (skills):** سه مخزن کلون شد و فایل‌ها با spec تطبیق داده شد:

| مخزن | تعداد SKILL.md | کل فایل‌ها |
|---|---|---|
| `obra/superpowers` | ۱۵ | ۲۶۶ |
| `anthropics/skills` | ۲۰ | ۴۷۲ |
| `mattpocock/skills` | ۳۸ | ۲۱۶ |

از ۳۵ فایل نمونه‌برداری‌شده، **۳۵ تا (۱۰۰٪)** دارای frontmatter معتبر با `name` و `description` بودند — یعنی استاندارد واقعاً رعایت می‌شود، نه فقط ادعا.

---

<a name="3"></a>
## ۳. کاتالوگ کامل پروژه‌ها

*(ستاره‌ها از GitHub API روی ۲۰۲۶-۱۰-۱۰/۱۱؛ وضعیت نگهداری از روی تاریخ آخرین کامیت)*

### ۳.۱ حافظه

| پروژه | ⭐ | آخرین آپدیت | نقطه قوت | نقطه ضعف |
|---|---|---|---|---|
| [`mem0ai/mem0`](https://github.com/mem0ai/mem0) | ۶۶٬۹۵۵ | فعال | بزرگترین کامیونیتی، استخراج خودکار fact | گراف پولی؛ بنچمارک‌ها بحث‌برانگیز |
| [`topoteretes/cognee`](https://github.com/topoteretes/cognee) | ۳۱٬۹۷۲ | فعال | گراف + وکتور، local-first | پیچیدگی عملیاتی |
| [`getzep/graphiti`](https://github.com/getzep/graphiti) | ۳۱٬۶۲۸ | فعال | **گراف دانش زمان‌مند (bi-temporal)** | نیاز به گراف‌دی‌بی خارجی |
| [`supermemoryai/supermemory`](https://github.com/supermemoryai/supermemory) | ۳۱٬۱۸۴ | فعال | MCP-first، بهینه برای coding agent | — |
| [`letta-ai/letta`](https://github.com/letta-ai/letta) | ۲۵٬۰۹۶ | فعال | **ران‌تایم کامل**؛ مدل خودش حافظه‌اش را ویرایش می‌کند | سخت embed می‌شود |
| [`thedotmack/claude-mem`](https://github.com/thedotmack/claude-mem) | ۹۹٬۲۲۹ | فعال | حافظه‌ی جلسه‌ای برای coding agent | ترند سریع — خودتان بسنجید |
| [`langchain-ai/langmem`](https://github.com/langchain-ai/langmem) | ۱٬۷۰۰ | فعال | کتابخانه، native برای LangGraph | کوچک |

⚠️ **میدان مینِ بنچمارک:** mem0 خودش ۹۳٪ روی LongMemEval گزارش می‌دهد؛ اندازه‌گیری‌های مستقل ۵۸–۶۶٪ نشان می‌دهند.
**پروب خودتان را بسازید:** یک فکت مشخص را اول جلسه بگویید، جلسه را از آستانه‌ی compaction رد کنید، بعد دقیقاً همان فکت را بپرسید.

### ۳.۲ مهارت‌ها، استانداردها و spec

| استاندارد | ریپو | ⭐ | کاربرد |
|---|---|---|---|
| **AGENTS.md** | [`agentsmd/agents.md`](https://github.com/agentsmd/agents.md) | ۲۴٬۸۶۴ | کانتکستِ پروژه؛ تحت نظر Agentic AI Foundation (Linux Foundation)؛ خوانده‌شده توسط ۳۰+ ابزار |
| **Agent Skills (SKILL.md)** | [`anthropics/skills`](https://github.com/anthropics/skills) | ۱۸۰٬۳۳۹ | قابلیت رویه‌ایِ قابل‌حمل؛ استاندارد باز (agentskills.io) |
| **Spec-Driven** | [`github/spec-kit`](https://github.com/github/spec-kit) | ۱۴۰٬۷۳۴ | constitution → spec → plan → tasks؛ شامل نشانگر `[NEEDS CLARIFICATION]` |

**قانون طلایی (از اندازه‌گیری Vercel):** قانونی که برای همه‌چیز صدق می‌کند → AGENTS.md (یک ایندکس فشرده داخل AGENTS.md **۱۰۰٪** جواب داد در برابر ۷۹٪ برای Skill). روالِ تخصصی → Skill.

⚠️ **امنیت:** گزارش‌ها از **۳۶٪ مهارت‌های آلوده به prompt injection** خبر می‌دهند و مهارت‌ها می‌توانند اسکریپت اجرا کنند. قبل از نصب SKILL.md را بخوانید و با [`snyk/agent-scan`](https://github.com/snyk/agent-scan) (۳٬۱۳۲⭐) اسکن کنید.

### ۳.۳ ران‌تایم و فریم‌ورک

| پروژه | ⭐ | آخرین آپدیت | وضعیت |
|---|---|---|---|
| [`openclaw/openclaw`](https://github.com/openclaw/openclaw) | ۳۹۱٬۶۲۱ | فعال | ایجنت عمومی چندپلتفرمه |
| [`anthropics/claude-code`](https://github.com/anthropics/claude-code) | ۱۵۰٬۰۶۷ | فعال | مرجعِ عملیِ طراحی هارنس |
| [`openai/codex`](https://github.com/openai/codex) | ۱۲۸٬۵۴۷ | فعال | ایجنت ترمینال سبک |
| [`OpenHands/OpenHands`](https://github.com/OpenHands/OpenHands) | ۹۰٬۵۱۹ | فعال | پلتفرم توسعه‌ی ایجنتی |
| [`lobehub/lobehub`](https://github.com/lobehub/lobehub) | ۸۳٬۱۱۱ | فعال | «Chief Agent Operator»: تیم ایجنت‌ها ۷×۲۴ |
| [`cline/cline`](https://github.com/cline/cline) | ۷۰٬۱۲۵ | فعال | SDK / افزونه / CLI |
| [`ruvnet/ruflo`](https://github.com/ruvnet/ruflo) | ۷۴٬۲۸۷ | فعال | هارنس swarm چندبازیکنه |
| [`agno-agi/agno`](https://github.com/agno-agi/agno) | ۴۲٬۶۵۲ | فعال | پلتفرم ساخت/اجرا |
| [`langchain-ai/langgraph`](https://github.com/langchain-ai/langgraph) | ۴۳٬۰۲۵ | فعال | گراف + checkpointing |
| [`mastra-ai/mastra`](https://github.com/mastra-ai/mastra) | ۲۸٬۶۹۴ | فعال | TypeScript-first |
| [`huggingface/smolagents`](https://github.com/huggingface/smolagents) | ۲۹٬۷۷۴ | فعال | «ایجنت‌هایی که با کد فکر می‌کنند» |
| [`openai/openai-agents-python`](https://github.com/openai/openai-agents-python) | ۲۹٬۹۵۵ | فعال | سبک و قدرتمند |
| [`pydantic/pydantic-ai`](https://github.com/pydantic/pydantic-ai) | ۲۰٬۵۳۵ | فعال | ✅ تست‌شده: اجرای آفلاین موفق |
| [`google/adk-python`](https://github.com/google/adk-python) | ۲۱٬۷۷۰ | فعال | ADK گوگل |
| [`microsoft/agent-framework`](https://github.com/microsoft/agent-framework) | ۱۴٬۰۴۸ | فعال | فریم‌ورک مایکروسافت |
| [`microsoft/autogen`](https://github.com/microsoft/autogen) | ۶۱٬۳۴۳ | ⚠️ ۲۰۲۶-۰۴-۱۵ | **۵ ماه بدون آپدیت** |
| [`FoundationAgents/MetaGPT`](https://github.com/FoundationAgents/MetaGPT) | ۷۰٬۷۹۶ | ⚠️ ۲۰۲۶-۰۱-۲۱ | **۹ ماه بدون آپدیت** |

🚩 AutoGen و MetaGPT — دو ستون قدیمی چند-ایجنتی — دیگر فعالانه نگهداری نمی‌شوند.

### ۳.۴ دسترسی به جهان و ابزارها

| پروژه | ⭐ | کاربرد | نتیجه تست |
|---|---|---|---|
| [`oraios/serena`](https://github.com/oraios/serena) | ۳۰٬۱۷۱ | جستجوی معناییِ کد با LSP | 🟠 ۲۳ ابزار OK، LS پایتون شکست |
| [`ast-grep/ast-grep`](https://github.com/ast-grep/ast-grep) | ۱۶٬۱۸۸ | جستجو/بازنویسی ساختاری روی AST | ✅ PASS |
| [`modelcontextprotocol/servers`](https://github.com/modelcontextprotocol/servers) | ۹۱٬۱۲۸ | سرورهای مرجع (شامل sequential-thinking) | ✅ PASS |
| [`Panniantong/Agent-Reach`](https://github.com/Panniantong/Agent-Reach) | ۹۵٬۴۷۷ | خواندن توییتر/ردیت/یوتیوب/گیت‌هاب بدون هزینه API | ⬜ تست‌نشده |
| [`firecrawl/firecrawl`](https://github.com/firecrawl/firecrawl) | ۱۹۰٬۲۲۰ | داده‌ی وب تمیز (تا ۹۴٪ توکن کمتر به‌ازای صفحه) | ✅ MCP دست‌دهی OK |
| [`browser-use/browser-use`](https://github.com/browser-use/browser-use) | ۱۱۷٬۵۷۰ | ایجنت مرورگر | ⬜ |
| [`microsoft/fara`](https://github.com/microsoft/fara) | ۶٬۲۱۵ | مدل‌های computer-use + ابزار verification | ⬜ |

### ۳.۵ خودبهبودی، RL و ارزیابی

| پروژه | ⭐ | نکته | نتیجه تست |
|---|---|---|---|
| [`gepa-ai/gepa`](https://github.com/gepa-ai/gepa) | ۶٬۹۳۵ | تکامل پرامپت با بازتاب روی trace؛ تا ۲۰٪ بهتر از GRPO با ۳۵× rollout کمتر | ⬜ |
| [`stanfordnlp/dspy`](https://github.com/stanfordnlp/dspy) | ۳۸٬۵۸۴ | «برنامه‌نویسی نه پرامپت‌نویسی» | ✅ PASS (آفلاین) |
| [`microsoft/agent-lightning`](https://github.com/microsoft/agent-lightning) | ۱۸٬۶۴۵ | RL برای هر ایجنت بدون بازنویسی کد | ⬜ |
| [`PrimeIntellect-ai/verifiers`](https://github.com/PrimeIntellect-ai/verifiers) | ۴٬۶۹۳ | محیط‌های RL + eval | ✅ import OK |
| [`promptfoo/promptfoo`](https://github.com/promptfoo/promptfoo) | ۲۵٬۸۷۸ | تست + red teaming در CI | ✅ **PASS + کنترل منفی** |
| [`confident-ai/deepeval`](https://github.com/confident-ai/deepeval) | ۱۸٬۷۳۴ | وسیع‌ترین کتابخانه متریک | ✅ PASS |
| [`comet-ml/opik`](https://github.com/comet-ml/opik) | ۲۲٬۴۹۴ | ردیابی + بهینه‌سازی خودکار | 🟡 CLI و import OK |
| [`langfuse/langfuse`](https://github.com/langfuse/langfuse) | ۳۵٬۶۱۶ | همه‌کاره، MIT، خود-میزبان | ⬜ |
| [`Arize-ai/phoenix`](https://github.com/Arize-ai/phoenix) | ۱۱٬۷۸۰ | OTel-native خالص | ⬜ |
| [`llm-as-a-verifier/llm-as-a-verifier`](https://github.com/llm-as-a-verifier/llm-as-a-verifier) | ۳٬۳۱۲ | امتیازدهی ریزدانه روی توزیع logprob | ⬜ |
| [`BerriAI/litellm`](https://github.com/BerriAI/litellm) | ۶۰٬۹۱۰ | gateway یکپارچه برای ۱۰۰+ مدل | ✅ PASS (۸۰ route) |

### ۳.۶ مدیریت محیط و نصب برنامه

| ابزار | ⭐ | کاربرد | نتیجه تست |
|---|---|---|---|
| [`jdx/mise`](https://github.com/jdx/mise) | ۳۴٬۸۹۰ | نسخه‌ی ابزارها + env + task runner در یک فایل | ⬜ نصب‌نشدنی اینجا |
| [`astral-sh/uv`](https://github.com/astral-sh/uv) | ۹۰٬۵۸۹ | مدیریت بسته/پروژه پایتون، ۱۰–۱۰۰× سریع‌تر | ✅ **PASS** |
| [`jetify-com/devbox`](https://github.com/jetify-com/devbox) | ۱۲٬۳۹۷ | محیط‌های قابل‌پیش‌بینی بر پایه nix | ⬜ |
| [`dotenvx/dotenvx`](https://github.com/dotenvx/dotenvx) | ۵٬۸۳۲ | مدیریت امن کلیدها | ✅ **PASS** |
| [`pkgxdev/pkgx`](https://github.com/pkgxdev/pkgx) | ۹٬۹۲۱ | اجرای هرچیز بدون نصب سراسری | ⬜ |
| [`flox/flox`](https://github.com/flox/flox) | ۴٬۱۷۰ | محیط‌های قطعی و قابل اشتراک | ⬜ |
| [`devcontainers/cli`](https://github.com/devcontainers/cli) | ۲٬۹۸۳ | محیط کانتینری استاندارد | ⬜ (نیاز به داکر) |
| [`docker/mcp-gateway`](https://github.com/docker/mcp-gateway) | ۱٬۵۹۰ | مدیریت سرورهای MCP | ⬜ (نیاز به داکر) |

### ۳.۷ اجرای پایدار و سندباکس

| ابزار | ⭐ | مدل | چه‌وقت |
|---|---|---|---|
| [`temporalio/sdk-python`](https://github.com/temporalio/sdk-python) | ۱٬۲۱۴ | journal/replay | سازمانی، تسک‌های هفته‌ها تا سال‌ها |
| [`restatedev/restate`](https://github.com/restatedev/restate) | ۴٬۵۴۲ | journal + state، **یک باینری** | کمترین اوپس |
| [`dbos-inc/dbos-transact-py`](https://github.com/dbos-inc/dbos-transact-py) | ۱٬۶۱۹ | checkpoint در Postgres | **اگر Postgres دارید** |
| [`e2b-dev/E2B`](https://github.com/e2b-dev/E2B) | ۱۴٬۲۷۱ | **Firecracker microVM** | کدِ کاملاً غیرقابل‌اعتماد |
| [`daytonaio/daytona`](https://github.com/daytonaio/daytona) | ۷۱٬۵۷۵ | کانتینر، persistent | جلسات طولانی/stateful |
| Modal Sandboxes | — | gVisor | مقیاس بسیار بالا + GPU |

قانون: **کدِ کاملاً غیرقابل‌اعتماد → microVM. کدی که خودتان کنترل می‌کنید ولی خط‌به‌خطش را نه → gVisor.**

---

<a name="4"></a>
## ۴. کیت نصب (بر اساسِ آنچه واقعاً کار کرد)

### سطح ۱ — امروز، ۳۰ دقیقه (فقط چیزهای تست‌شده)

```bash
# ۱) مدیریت محیط — تست‌شده ✅
pip install uv
uv venv .venv && uv pip install <بسته>        # ۱۰-۱۰۰× سریع‌تر از pip

# ۲) جستجوی ساختاری در کد — تست‌شده ✅
npm i -g @ast-grep/cli
# نکته: در نسخه ۰.۵۰ قانون باید فیلد kind داشته باشد
#   id: find-defs
#   language: python
#   rule:
#     kind: function_definition
#     pattern: def $N($$$)

# ۳) تفکر مرحله‌ای — تست‌شده ✅ (هزینه صفر)
npx -y @modelcontextprotocol/server-sequential-thinking

# ۴) مدیریت امن کلیدها — تست‌شده ✅
npm i -g @dotenvx/dotenvx && dotenvx encrypt

# ۵) دو فایل متنی که بیشترین اثر را دارند (بدون نصب)
#    AGENTS.md  (زیر ۵۰۰ توکن!)  +  تعریف صریحِ «تمام شد» برای هر تسک
```

### سطح ۲ — هفته اول

```bash
# ارزیابی و کیفیت — تست‌شده ✅
npm i -g promptfoo                 # تست + red teaming در CI
pip install deepeval               # متریک‌های آماده

# یکپارچه‌سازی مدل‌ها — تست‌شده ✅
pip install 'litellm[proxy]'       # gateway برای ۱۰۰+ مدل + بودجه‌بندی + fallback

# مهارت‌ها — تست‌شده ✅ (۱۰۰٪ منطبق با spec)
git clone --depth 1 https://github.com/anthropics/skills.git
git clone --depth 1 https://github.com/obra/superpowers.git
```

### سطح ۳ — بااحتیاط

```bash
pip install dspy gepa              # خودبهبودی (اول روی تک-ایجنت؛ روی چند-ایجنتی نامطمئن است)
uv tool install serena-agent       # عالی اما ابتدا find_symbol را روی پروژه‌ی خودتان امتحان کنید
```

---

<a name="5"></a>
## ۵. کاهش خطا، حلقه‌های کیفیت و Verification

### ۵.۱ تبارشناسی شکست (MAST، NeurIPS 2025 — تحلیل ۱٬۶۰۰+ تِرَس، ۱۴ مد، κ=۰.۸۸)

| دسته | سهم | بدترین موارد |
|---|---|---|
| **طراحی و مشخصات** | **۴۱٫۸٪** | تکرار گام (۱۵٫۷٪)، ندانستن شرط پایان (۱۲٫۴٪)، نافرمانی از مشخصات (۱۱٫۸٪) |
| **عدم هم‌راستایی بین ایجنت‌ها** | **۳۶٫۹٪** | عدم تطابق استدلال-عمل (۱۳٫۲٪)، نپرسیدن ابهام (۶٫۸٪)، فروپاشی کانتکست |
| **شکستِ verification** | **۲۱٫۳٪** | verification نادرست (۹٫۱٪)، خاتمه‌ی زودهنگام (۶٫۲٪) |

**بینش کلیدی: ~۷۹٪ شکست‌ها از مشخصات بد و هماهنگیِ خراب است، نه از مدل.**
نرخ شکست کلی سیستم‌های چند-ایجنتی: **۴۱٪ تا ۸۶٫۷٪**. یک پایپ‌لاین ساده‌لوحانه خطا را حدود **۱۷ برابر** سریع‌تر از تک-ایجنت انباشته می‌کند.

### ۵.۲ حلقه‌ی کیفیتِ پیشنهادی (سه لایه، از ارزان به گران)

| لایه | کار | ابزار |
|---|---|---|
| ۱. خود-بازبینی | ابزارهای `think_about_*` سرِنا؛ تعریف صریحِ «تمام شد»؛ builder ≠ validator | رایگان |
| ۲.Verification قطعی | تست/لینتر/تایپ‌چک بعد از هر گام (hook)؛ تستِ مبتنی بر خاصیت (صحت ۸۲٫۷٪ در برابر ۷۷٫۳٪ برای «قضاوت خود ایجنت») | رایگان |
| ۳. ارزیابی در CI | promptfoo (تأییدشده) / DeepEval / Opik با ربریک ۵بعدی | نصب |

### ۵.۳ ⚠️ قانون حیاتی: داورِ LLM مرجع نیست

- داورهای همراهِ بنچمارک‌های وب تا **۴۵٪ مثبت کاذب** دارند.
- ایجنت‌ها می‌توانند فقط با بازنویسیِ **لحنِ** زنجیره‌ی استدلال (بدون تغییر عمل!) نرخ مثبت کاذب را **تا ۹۰٪** بالا ببرند.
- توافقِ دو داور **تکرارپذیری** را اندازه می‌گیرد، نه درستی را.
- مدل‌ها نمی‌توانند تشخیص دهند کدام معیار اصلاً نیاز به داور دارد (arXiv 2610.04699): Opus برچسب مرزیِ خودش را در **۳۳٪** موارد عوض می‌کند (در برابر ۵٪ روی کنترل‌ها).

> **داور = مشاور. خروجی باید از یک بررسی قطعی رد شود.**

### ۵.۴ امنیت (OWASP Top 10 for Agentic Applications ۲۰۲۶)

چک‌لیستِ یک‌بعدازظهری:
1. فهرستِ همه‌ی سرورهای MCP؛ حذف ناشناس‌ها
2. تأیید انسانی برای عملیات نوشتنی
3. اسکن توضیحات ابزار با `agent-scan` در CI
4. **پین کردن نسخه** + هش کردن تعریف ابزار (ضدِ rug pull)
5. allowlist برای دستوراتی که کلاینت spawn می‌کند
6. لاگ کامل ورودی/خروجی ابزارها
7. مسدود کردن IPهای private/link-local در egress + اجبار IMDSv2

---

<a name="6"></a>
## ۶. مقالات کلیدی (arXiv)

| شناسه | موضوع | عدد کلیدی |
|---|---|---|
| 2511.09030 | **MAKER** — تسک یک‌میلیون‌گامی با صفر خطا | تجزیه افراطی + رأی‌گیری + red-flag؛ هزینه خطی |
| 2505.22954 | **Darwin Gödel Machine** (ICLR 2026) | ۲۰٪→۵۰٪ روی SWE-bench با ویرایشِ خود |
| 2603.19461 | **Hyperagents** | مکانیزمِ بهبود، خودش قابل بهبود است |
| 2506.12928 | Test-time scaling برای ایجنت‌ها | BoN + قاضی list-wise: ۵۵٫۷۶→۶۳٫۰۳ روی GAIA |
| 2602.12276 | **CATTS** — scaling برای وب‌ایجنت | مقیاس‌دهی یکنواخت saturate می‌شود |
| 2601.15808 | **DeepVerifier** (ACL'26 Findings) | ربریک مبتنی بر taxonomy؛ +۱۲–۴۸٪ F1 |
| 2607.05391 | **LLM-as-a-Verifier** | امتیازدهی ریزدانه روی توزیع logprob |
| 2609.02246 | «LLM-as-a-Judge Is Not an Oracle» | ۱۱ مدِ شکست؛ چارچوب PROCTOR |
| 2610.04699 | «Not Self-Decidable» | مدل‌ها نمی‌فهمند کِی به داور نیاز است |
| 2504.21798 | **SWE-smith** | ۵۰k تسک مصنوعی از ۱۲۸ ریپو |
| 2606.16038 | **Open-SWE-Traces** | ۲۰۷٬۴۸۹ ترِک در ۹ زبان |

*یافته‌ی ایمنیِ مهم (فوریه ۲۰۲۶): یک جامعه‌ی ایجنتی نمی‌تواند همزمان خود-تکامل‌یابنده، ایزوله از داده‌ی خارجی و ناوردا در ایمنی باشد — **دو تا از سه تا**.*
**برداشت:** هر سیستم خودبهبود باید یک حلقه‌ی verification بیرونی داشته باشد که خود ایجنت نتواند تغییرش دهد.

---

<a name="7"></a>
## ۷. منابع دنبال‌کردن

**متمرکز و باکیفیت:**
- [`ai-boost/awesome-harness-engineering`](https://github.com/ai-boost/awesome-harness-engineering) (۴٫۸k⭐) — بهترین نقطه شروع، ساختارمند بر اساس لایه‌های هارنس
- [`VoltAgent/awesome-agent-skills`](https://github.com/VoltAgent/awesome-agent-skills) (۳۵٫۵k⭐) — کاتالوگ مهارت‌ها
- `anthropic.com/engineering` (*Writing effective tools for agents*، *Effective harnesses for long-running agents*، *Advanced tool use*) — بسیار بالاتر از وبلاگ‌ها
- arXiv `cs.AI`

**کشف ترند:** GitHub Trending · topicهای `token-optimization` و `agent-skills` · Hacker News · Product Hunt · r/LocalLLaMA · خبرنامه‌های AlphaSignal/TLDR/Latent Space

**یوتیوب:** IndyDevDan (~۱۳۵k، الگوهای ضدهیاهو: builder-validator، موازی‌سازی، meta-agent) · Cole Medin (~۲۱۳k، ایجنت‌های production) · LangChain (رسمی) · Anthropic/OpenAI (رسمی) · AI Jason (~۲۲۵k)

**تیک‌تاک/اینستاگرام — ⚠️ صادقانه:** این دو برای یادگیریِ مهندسی ایجنت ضعیف‌اند؛ بیشتر بازاریابیِ اتوماسیون‌اند تا عمق فنی. ارزششان فقط **سیگنالِ ترندِ مصرفی** است. پرتکرارها در ۲۰۲۶: Riley Brown (@rileybrown.ai، ~۶۳۷k) · Brand Nat (~۴۴۶k) · Justin Fineberg (~۲۸۹k) · @theclarkgary (~۱۵۵k). هر ابزاری را که نشان می‌دهند از گیت‌هاب/مستندات رسمی تأیید کنید.

---

<a name="8"></a>
## ۸. نقشه راه (بر اساس تست، نه ادعا)

**هفته ۱ — اندازه‌گیری کنید، بعد تغییر دهید**
۱. ۲۰ تسک واقعی از کار خودتان + لاگِ توکن/زمان/خطا
۲. ربریک ۵بعدی (صحت، جامعیت، بهره‌وری ابزار، پایبندی به محدودیت، کیفیت منبع)
۳. AGENTS.md زیر ۵۰۰ توکن + تعریف صریحِ «تمام شد»

**هفته ۲–۳ — ارزان‌ترین ارتقاها**
۴. دستورات quiet + `.claudeignore` (بدون نصب، فوری)
۵. `uv` برای مدیریت محیط (تست‌شده ✅)
۶. `ast-grep` برای جستجوی کد (تست‌شده ✅)
۷. مهارت‌ها از `anthropics/skills` (تست‌شده ✅)

**ماه ۲ — کیفیت و استقلال**
۸. `promptfoo` در CI (تست‌شده ✅) + `deepeval` برای متریک‌ها (تست‌شده ✅)
۹. حلقه‌ی verification سه‌لایه
۱۰. `litellm` برای routing و کنترل هزینه (تست‌شده ✅)

**ماه ۳ — پیشرفته**
۱۱. `dspy`/`gepa` برای خودبهبودی (با verification بیرونی!)
۱۲. Serena — **فقط اگر** `find_symbol` روی پروژه‌ی شما کار کرد
۱۳. امنیت: `agent-scan` در CI + پین کردن ابزارها

---

<a name="9"></a>
## ۹. پیوست: بازتولید تست‌ها

محیط: Python 3.11.2 / Node 22.22.3. سه اسکریپت اصلی:

| اسکریپت | چه می‌کند |
|---|---|
| `bench_compression.py` | خروجی ابزارِ واقعی می‌سازد (git status، pytest، npm install، JSON، build log)، قبل/بعد را با cl100k_base می‌شمارد، و چک می‌کند نشانگرهای بحرانی (FAIL/AssertionError) زنده مانده‌اند یا نه |
| `test_mcp.py` | دست‌دهی واقعی stdio با سرورهای MCP (initialize → tools/list → tools/call) |
| `test_functional.py` | تست عملکردی آفلاین برای uv، ast-grep، dotenvx، pydantic-ai، dspy، deepeval، litellm و… |

**نکاتِ بازتولید که وقتِ من را گرفت و برای شما صرفه‌جویی می‌کند:**
- `tiktoken` هنگام اجرا فایل BPE از `openaipublic.blob.core.windows.net` می‌گیرد؛ برای محیط ایزوله از `js-tiktoken` (داده داخل بسته) استفاده کنید.
- نصب دسته‌ای با `pip` در این مجموعه با خطای «resolution too deep» شکست خورد (۱۴ دقیقه، هیچ نصبی). با `uv pip install` همان مجموعه در **۷ ثانیه** نصب شد.
- نام پکیج Serena روی PyPI/GitHub `serena-agent` است، نه `serena`.
- Serena برای اجرای language server به `uv`/`uvx` در `PATH` نیاز دارد.
- ast-grep ۰.۵۰ در قانون YAML حتماً باید `kind` داشته باشد.

---

### جمع‌بندی در ۶ جمله

1. **مدل را عوض نکن، هارنس را عوض کن.**
2. **۸۰٪ شکست‌ها مشخصات و هماهنگی‌اند، نه هوش** — «تعریفِ تمام‌شده» بنویس.
3. **کوچک کن، بازنویسی نکن** (بازنویسیِ پیشوند، کش را می‌کشد).
4. **داورِ LLM مشاور است، نه مرجع** — همیشه یک بررسی قطعی بالاسرش باشد.
5. **تست سخت‌گیرانه نشان داد چند تا از پرستاره‌ترین ابزارها ادعایشان را در عمل محقق نمی‌کنند** (headroom ۰٪، entroly وابسته به اینترنت، mcpm/context-mode نصب نمی‌شوند، Serena با basedpyright جدید شکست دارد).
6. **ارزان‌ترین و مطمئن‌ترین ارتقاها نیازی به نصب ندارند:** AGENTS.mdِ کوتاه، تعریفِ «تمام شد»، و دستورات quiet.
