# tools


## 2026-10-11T03:02:44Z

* entroly: حتی با بودجه ۹۴٪ هیچ chunk ای برنمی‌گرداند (Selected: 0) — استفاده نشود

## 2026-10-11T03:02:44Z

* سرنا/ basedpyright: basedpyright 1.40 دیگر --stdio قبول نمی‌کند و Serena روی پایتون می‌شکند

## 2026-10-11T03:02:44Z

* headroom-ai: صفر درصد فشرده‌سازی در همه مسیرها (فقط JSON و CODE هندلر دارد)

## 2026-10-11T03:02:44Z

* ابزارهایی که کار می‌کنند: uv, ast-grep, promptfoo, DeepEval, DSPy, litellm, firecrawl-mcp, tavily-mcp

## 2026-10-11T03:03:30Z

* شکست‌ها: entroly (۰ chunk در بودجه بالا)، headroom-ai (۰٪ فشرده‌سازی)، Serena (basedpyright)، mcpm (ImportError)، sqz/rtk (باینری مسدود)

## 2026-10-11T03:03:30Z

* شکست در نصب: context-mode و token-optimizer-mcp (build بومی better-sqlite3 شکست می‌خورد)

## 2026-10-11T11:59:34Z

* دستور timeout در این سندباکس باعث خطای shell می‌شود — از پارامترِ timeoutِ ابزار استفاده کن، نه دستورِ timeout

## 2026-10-11T11:59:34Z

* Actions: workflow باید permissions: contents: write داشته باشد وگرنه git push با ۴۰۳ رد می‌شود؛ فیلترِ paths شامل خودِ فایلِ workflow نیست

## 2026-10-11T11:59:34Z

* تله: git reset --mixed فایل‌های جدید را در working tree نمی‌سازد و بعدش git add -A آن‌ها را به عنوان «حذف» ثبت می‌کند. از git show origin/branch:path استفاده کن
