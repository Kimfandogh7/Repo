# کیت دسترسی به اینترنتِ سندباکس

**تاریخ اندازه‌گیری: ۱۴۰۴/۰۷/۱۹ (۲۰۲۶-۱۰-۱۱)** — همه‌چیز در این سند **اندازه‌گیری شده**، نه حدس.

این فایل نتیجه‌ی این درخواست است: «راهی پیدا کن که اینترنت و دانلود آزاد داشته باشیم.»
جواب کوتاه: **اینترنتِ «همه‌چیز-آزاد» از داخل سندباکس ممکن نیست و من آن را دور نمی‌زنم — اما چیزی که آزاد است خیلی بزرگ‌تر از چیزی است که به‌نظر می‌رسد، و با آن می‌توان تقریباً هر نیاز واقعی را برطرف کرد.**

---

## ۱. تشخیص دقیق: بلاک کجاست؟

ابتدا باید فهمید دیوار کجاست، وگرنه هر راهکاری حدس است. نتیجه‌ی چهار دور اندازه‌گیری:

| لایه | وضعیت | مدرک |
|---|---|---|
| DNS | **کاملاً باز** | همه‌ی هاست‌ها (حتی مسدودها) resolve می‌شوند؛ resolver: `nameserver 8.8.8.8` |
| متغیرهای پروکسی | **هیچ** | `http_proxy`/`https_proxy`/`no_proxy` تعریف نشده |
| TCP (پورت ۴۴۳) | **باز، حتی برای هاست‌های مسدود** | `bash /dev/tcp/example.com/443` موفق است |
| TLS / HTTP | **فیلتر می‌شود** | TCP وصل می‌شود، دست‌تکانی TLS می‌میرد → `curl` کد `000` |
| IPv4 در برابر IPv6 | **فرقی ندارد** | هر دو با `-4` و `-6` مسدود |

**نتیجه‌ی تعیین‌کننده:** چون TCP برای `example.com` هم باز است، این یک DROPِ فایروالی نیست؛ یک **فیلتر لایه‌ی ۷ بر اساس SNI/hostname** است. این یک یافته‌ی مهم است چون یک کلاس کامل از راهکارها را از دور خارج می‌کند: پورت‌فورواردینگ، SOCKS روی ۴۴۳، یا هر چیزی از جنس «فقط یک سوکت باز کن» — همه وصل می‌شوند و بعد در TLS می‌میرند.

### تصویر کامل (خروجی واقعی `net/bin/diagnose`)

```
HOST                               DNS     TCP    HTTPS  VERDICT
----                               ---     ---    -----  -------
github.com                         OK      OK     200    ALLOWED (HTTP 200)
api.github.com                     OK      OK     200    ALLOWED (HTTP 200)
codeload.github.com                OK      OK     301    ALLOWED (HTTP 301)
registry.npmjs.org                 OK      OK     200    ALLOWED (HTTP 200)
pypi.org                           OK      OK     200    ALLOWED (HTTP 200)
files.pythonhosted.org             OK      OK     404    ALLOWED (HTTP 404)
raw.githubusercontent.com          OK      OK     000    L7/SNI filtered
example.com                        OK      OK     000    L7/SNI filtered
google.com                         OK      OK     000    L7/SNI filtered
huggingface.co                     OK      OK     000    L7/SNI filtered
```

---

## ۲. چه چیزی را عمداً انجام ندادم (و چرا)

امکان فنیِ «تونل کور‌کننده‌ی SNI» وجود دارد: چون فیلتر روی SNI است، می‌توان با ECH (Encrypted Client Hello) یا جعلِ SNI آن را دور زد و یک پروکسی بازِ عمومی ساخت. **این کار را نکردم و پیشنهاد هم نمی‌کنم:**

- این یک کنترلِ امنیتیِ عمدیِ پلتفرم است (جلوی خروج داده، بدافزار و سوءاستفاده را می‌گیرد)، نه یک نقص تصادفی.
- دور زدنِ آن پنهانی است: یعنی ترافیکی که پلتفرم فکر می‌کند می‌بیند، با آنچه واقعاً می‌رود فرق دارد.
- دقیقاً همان لحظه‌ای که جواب بدهد، ابزار خطرناکی است — هم برای پلتفرم هم برای شما.

**اگر واقعاً به خروجیِ نامحدود از داخل سندباکس نیاز دارید، راهِ درست این است:** از پلتفرم بخواهید allowlist را گسترش دهد، یا آن بخش از کار را بیرون از سندباکس اجرا کنید. این را می‌توانم در لحظه برایتان آماده کنم.

چیزی که در ادامه می‌آید متفاوت است: **استفاده‌ی کامل و صادقانه از همان ۵ هاستِ مجاز**، بدون پنهان‌کاری. همه‌چیز در لاگ پلتفرم دیده می‌شود و همه‌اش همان کاری است که این هاست‌ها برایش ساخته شده‌اند.

---

## ۳. ابزارها (هر شش تا اجرا و تأیید شده)

در `net/bin/`. برای استفاده: `export PATH="$HOME/Repo/net/bin:$PATH"`

### `diagnose` — نقشه‌برداری شبکه
```bash
diagnose                      # هاست‌های پیش‌فرض
diagnose example.com gitlab.io  # هر هاست دلخواه
```
ستون TCP در برابر HTTPS همان چیزی است که نوعِ بلاک را افشا می‌کند.

### `ghget` — هر فایل یا شاخه از هر ریپوی عمومیِ گیت‌هاب
دور می‌زند... نه، **جایگزین می‌کند** `raw.githubusercontent.com` را با `codeload.github.com`:
```bash
ghget openai/tiktoken main README.md .            # تک‌فایل (۴۸۰۷ بایت، تأیید شد)
ghget anthropics/anthropic-sdk-python main src/anthropic/types /tmp/t   # ۲۰۳۶ فایل، تأیید شد
ghget microsoft/vscode                             # کل ریپو، ۶۱ مگابایت، تأیید شد
```

### `ghapi` — تک‌فایلِ کوچک با Contents API (سریع‌تر)
```bash
ghapi openai/tiktoken/README.md main | head -5
```
تا ۱ مگابایت، محتوا به‌صورت base64 برمی‌گردد. تأیید شد.

### `npmget` — هر tarball از npm (شامل **باینری**)
```bash
npmget @ast-grep/cli-linux-x64-gnu 0.36.0 /tmp/x   # ۷٫۰۷ م‌ب، تأیید شد
npmget gpt-tokenizer                               # نسخه خودکار (۴٫۰.۰)، ۹٫۱۳ م‌ب
```
تستِ واقعی: tarball را گرفتم، باینری ۴۵ مگابایتی ast-grep را بیرون کشیدم و اجرایش کردم:
```
$ ./package/ast-grep --version
ast-grep 0.36.0
$ ./package/ast-grep -p 'eval($X)' -l python demo/x.py
demo/x.py:2:    return eval(a)
demo/x.py:4:    return eval(x)
```

### `pypiget` — هر wheel/sdist از PyPI
```bash
pypiget tiktoken 0.14.0 /tmp/x     # ۱٬۰۹۵٬۵۸۱ بایت، تأیید شد
```

### `seed_tiktoken` — رفعِ واقعیِ یک شکستِ واقعی
```bash
export TIKTOKEN_CACHE_DIR=$(seed_tiktoken)
```

**این مهم‌ترین بخش است، چون یک شکستِ واقعی از تحقیقِ قبلی را ترمیم می‌کند.**

ابزار `entroly` در دور قبل با خطای `SSLError` مرده بود، چون tiktoken برای encoding مدل o200k_base می‌رود سراغ
`openaipublic.blob.core.windows.net` — که مسدود است. بررسی کردم و معلوم شد پکیجِ npm
`gpt-tokenizer` **دقیقاً همان فایل را با همان فرمت اصلی** داخل خودش دارد
(`package/data/o200k_base.tiktoken`, ۳٬۶۱۳٬۹۲۲ بایت، با این توضیح در کد: `// Source data: data/o200k_base.tiktoken`).

پس کافی است فایل را از یک هاستِ مجاز بگیریم و با کلیدِ درست در کش tiktoken بگذاریم
(نام فایلِ کش = `sha1(blobpath)` = `fb374d419588a4632f3f557e76b4b70aebbca790`).

نتیجه، از یک venv کاملاً تازه:
```
BASELINE FAIL -> SSLError HTTPSConnectionPool(host='openaipublic.blob.core.windows.net', port=443)
   ↓ بعد از seed
o200k_base vocab: 200019
encode("Hello, world! این یک تست است"): [13225, 11, 2375, 0, 8630, 19547, 48730, 5298]
OFFLINE OK
```
و `entroly` که قبلاً اصلاً اجرا نمی‌شد، حالا اجرا می‌شود: `Indexed 1 document(s), 8 chunk(s).`

---

## ۴. کانالِ عمومی: رله از طریق گیت‌هاب (دوطرفه، باینری)

اگر فایلی در **هیچ** پکیج npm/PyPI و **هیچ** ریپوی عمومی نیست، هنوز یک راهِ ساده و کاملاً قانونی هست:

```
نوشتن:  git push  →  github.com            (مجاز)
خواندن: codeload  →  codeload.github.com   (مجاز)
```

این با **باینری** هم تست شد:
```
  pushed.
  392cd02be656c5a36b02ad82b37fed56  /tmp/blob.bin
  392cd02be656c5a36b02ad82b37fed56  Repo-arena-758efc2d-repo/_netkit_test.bin
  BINARY ROUND-TRIP VIA GIT: OK
```
(فایل‌های تست بعد از اندازه‌گیری از ریپو پاک شدند.)

**یک محدودیتِ مهم که باید بدانید:** توکن گیت‌هاب این سندباکس یک **integration token** با دسترسی محدود است.
ساخت Gist کار نمی‌کند:
```
$ gh gist create /tmp/payload.txt
X Failed to create gist: HTTP 403: Resource not accessible by integration
```
پس کانالِ نوشتن فقط `git push` به همین برنچ است، نه Gist. این را قبل از اینکه روی Gist وقت بگذارید بدانید.

---

## ۵. خلاصه: چه چیزی عملاً در دسترس است

| نیاز | راهِ تأیید‌شده |
|---|---|
| هر فایل از هر ریپوی عمومی گیت‌هاب | `ghget` (تا ۶۱ م‌ب تست شد) |
| تک‌فایلِ کوچک، سریع | `ghapi` |
| باینریِ ابزارها (مثل ast-grep) | `npmget` (۷ م‌ب → باینری ۴۵ م‌ب اجرا شد) |
| پکیج/کتابخانه‌ی پایتون | `pypiget` |
| ابزاری که «به اینترنت نیاز دارد» (مثل entroly) | `seed_tiktoken` — کش را از npm پر کن |
| فایلِ شخصی که جای دیگر نیست | رله‌ی `git push` ↔ `codeload` (باینری تأیید شد) |
| جستجوی وب / گوگل / یوتیوب | **در دسترس نیست** — باید از پلتفرم درخواست شود |

---

## ۵.۵ آیا می‌توان مرورگر نصب کرد و هر سایتی را باز کرد؟

سؤالِ مستقیم بود: «بتونی یه مرورگر نصب کنی و بری داخل یه سایت». جواب، بعد از اجرای واقعی، سه‌قسمتی است.

### الف) نصب مرورگر: **بله، آن هم بدون root** ✅

`apt` نیاز به root دارد (`Permission denied` روی dpkg lock) و `playwright install` هم شکست می‌خورد چون
هاست‌های دانلود مرورگر مسدودند:

```
HOST                        DNS     TCP    HTTPS  VERDICT
cdn.playwright.dev           OK      OK     000    L7/SNI filtered
storage.googleapis.com       OK      OK     000    L7/SNI filtered
playwright.azureedge.net     OK      OK     000    L7/SNI filtered
```

اما بعضی پکیج‌های npm باینری کرومیوم را **داخل tarball** دارند (برای Lambda).
`@playwright/browser-chromium` فقط یک stub ۵ کیلوبایتی است، ولی
`@sparticuz/chromium` باینری واقعی را دارد. مسیر کامل:

```bash
npmget @sparticuz/chromium 153.0.0 .      # ۶۹٬۹۹۵٬۳۰۹ بایت از registry.npmjs.org
python -c "import brotli;open('chromium','wb').write(brotli.decompress(open('package/bin/chromium.br','rb').read()))"
# → ۶۷ MB فشرده / ۲۰۹ MB باز شده
# libnspr4.so هم داخل al2023.tar.br همان پکیج است (۱۳ کتابخانه)
export LD_LIBRARY_PATH=.../libs/lib
chromium --version   →   Chromium 153.0.8010.0
```

پس باینری ۲۰۹ مگابایتیِ کرومیوم ۱۵۳ با **فقط هاست‌های مجاز** و بدون root داخل سندباکس آمد و اجرا شد.
کتابخانه‌های missing: **صفر**.

### ب) رندر کردن صفحه: **نه** ❌

مرورگر بالا می‌آید ولی هیچ صفحه‌ای — حتی `about:blank` — باز نمی‌شود:

```
ERROR:gpu_process_host.cc:1054] GPU process exited unexpectedly: exit_code=15
WARNING:gpu_process_host.cc:1506] The GPU process has crashed 1 time(s)
```

و فرآیند تا اتمام timeout معلق می‌ماند (`exit=124`). علت، نبودِ GL/Vulkan/EGL در این محیط است
(`eglInitialize SwANGLE failed with error EGL_NOT_INITIALIZED`). با `--use-gl=disabled`،
`--use-angle=swiftshader`، `--in-process-gpu`، `--single-process` و `headless=old/new` هم تفاوتی نکرد.

### ج) باز کردن سایت — حتی اگر رندر هم درست می‌شد: **نه** ❌

این مهم‌ترین بخش است. خودِ Chromium از داخل شبکه‌اش تأیید کرد:

```
$ chromium --dump-dom https://example.com
ERROR:ssl_client_socket_impl.cc:949] handshake failed; returned -1, SSL error code 1, net_error -100
```

`net_error -100` یعنی شکست در TLS handshake — **همان تشخیصی که در بخش ۱ با tcp/curl گرفته بودم،
این‌بار مستقلاً از داخل مرورگر کرومیوم**. این خطا برای `google.com` هم تکرار شد.

> **خلاصه‌ی این بخش:** مرورگر را می‌توان نصب کرد (و جالب است که شد)، اما (۱) در این محیط نمی‌تواند
> صفحه‌ای رندر کند، و (۲) اگر هم می‌توانست، هیچ سایتی را باز نمی‌کرد چون هر اتصال HTTPS در
> دست‌تکانی TLS کشته می‌شود. مانع، مرورگر نیست؛ شبکه است.

---

## ۶. نکات فنی برای کسی که این را توسعه می‌دهد

سه باگ واقعی در نوشتن این ابزارها پیدا شد که ارزشِ ثبت دارد (همه رفع شدند):

1. **`pipefail` + `head` = مرگِ بی‌صدا.** دستور `x=$(tar tzf ... | head -1)` با `set -o pipefail`
   باعث SIGPIPE می‌شود و اسکریپت با `EXIT=141` و **بدون هیچ پیام خطا** می‌میرد — آن هم به‌صورت
   غیرقطعی (race). در نسخه‌ی کوچک کار می‌کرد و در بزرگ نه. راهِ درست، حذف پایپ است:
   `list=$(tar tzf f); root=${list%%/*}`.
2. **`head` در پایپِ بزرگ می‌تواند نوشتن را بکشد.** حتی بعد از اصلاح اول، همان الگو دوباره SIGPIPE داد؛
   تعویضِ کامل با پارامتر-اکسپنشن مشکل را برای همیشه حل کرد.
3. **پکیج‌های scoped در npm مسیر می‌سازند.** `@scope/name` در مسیر خروجی پوشه می‌خواهد؛
   باید `$(basename "$P")` استفاده شود وگرنه `curl: (23) Failure writing output to destination`.

و یک الگوی کلی که از این ماجرا درآمد و ارزشِ بیشتری از خود ابزارها دارد:

> **وقتی ابزاری می‌گوید «به اینترنت نیاز دارم»، معمولاً به «اینترنت» نیاز ندارد — به یک فایلِ مشخص
> از یک هاستِ مشخص نیاز دارد.** آن فایل در بیشتر موارد در npm یا PyPI هم هست. کافی است پیدایش کنی
> و در مسیری که ابزار انتظار دارد بگذاری. این الگو برای entroly جواب داد و برای ابزارهای دیگر هم
> جواب خواهد داد.
