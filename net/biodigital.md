# BioDigital — شناساییِ کامل (اندازه‌گیری‌شده، ۱۴۰۴/۰۷/۱۹)

## سایت چیست

**BioDigital Human** — پلتفرم آناتومی/بیماریِ سه‌بعدیِ تعاملی.
مشتریانش: Wolters Kluwer، American Cancer Society، Novartis، J&J، NYU School of Medicine.

| آدرس | نقش |
|---|---|
| `https://www.biodigital.com` | سایتِ اصلی (بازاریابی) |
| **`https://human.biodigital.com/login/create`** | **صفحه‌ی ساخت حساب** |
| `https://human.biodigital.com/` | خودِ اپلیکیشن |
| `https://developer.biodigital.com` | پورتالِ توسعه‌دهنده (برای embed کردن ویجت) — نیاز به حساب دارد |

## فرمِ ثبت‌نام (به‌دست‌آمده از DOM واقعی با مرورگر)

```
STATUS: 200 | TITLE: Sign Up | BioDigital Human Platform

firstName : text      (الزامی نیست در HTML)
lastName  : text
email     : email
password  : password  (placeholder: "At least 8 characters")

BUTTONS: "Sign up with email"
همچنین:  "Sign in with Google"  (از طریق accounts.google.com/gsi/button)
متن:     "By signing up, you agree to our Terms of Service and Privacy Policy."
```

## 🚧 مانعِ اصلی: reCAPTCHA نسخه‌ی ۲

```
iframe src = https://recaptcha.net/recaptcha/api2/anchor?...&k=6LdvZvcUAAAAAM0Z1St9WQXwvSYd__hMUY2WZ6um
script     = https://recaptcha.net/recaptcha/api.js?render=6LdvZvcUAAAAAM0Z1St9WQXwvSYd__hMUY2WZ6um
```

`api2/anchor` یعنی **چک‌باکسِ v2** — نه v3ِ نامرئی. یعنی روی IP دیتاسنتر (مثل رانرِ GitHub Actions)
عملاً حتماً چالش می‌دهد. **روی IP خانگیِ خودت معمولاً اصلاً ظاهر نمی‌شود یا با یک کلیک حل می‌شود.**

## قوانین (از `biodigital.com/terms`)

- ✅ یک **حسابِ رایگان (Personal Account)** دارد — نیازی به پرداخت نیست.
- ✅ ممنوعیتِ صریحی برای «ثبت‌نامِ خودکار» در متن نیست.
- ⚠️ ممنوع: اسپم، auto-responder، دور زدنِ امنیت، گرفتنِ رمز از کاربران دیگر.
- ⚠️ **Personal Plus پولی و خودکار تمدید می‌شود** — نباید لمس شود.
- ⚠️ یادآوریِ HIPAA: نباید اطلاعاتِ سلامتِ محرمانه وارد شود.

## مقایسه با ابزارهای موجود (جستجوی عمیق)

| ابزار | ستاره | حکم برای این کار |
|---|---|---|
| **Skyvern** (`Skyvern-AI/skyvern`) | ۲۳٬۱۸۱ | قوی‌ترین ابزارِ عمومی (AGPL-3.0، پایتون). ولی کلید LLM می‌خواهد و Docker/Postgres. برای این فرمِ ۴فیلدی نیاز نیست — ضمن اینکه **مشکل کپچا را هم خودش حل نمی‌کند** (فقط human-in-the-loop دارد). |
| **SeleniumBase** | ۱۳٬۰۶۳ | برای تست، نه اتوماسیونِ تعاملی |
| **nanobrowser** | ۱۴٬۰۵۵ | افزونه‌ی کروم؛ اینجا به‌درد نمی‌خورد |
| **browserless** (`microlinkhq`) | ۱٬۸۴۰ | کرومِ هدلس به‌صورت سرویس — اگر خودت هاست کنی خوب است |
| **ساخته‌ی خودم (Actions + Playwright)** | — | کافی است: بدون کلید LLM، و ثابت شد که مرورگر واقعی اجرا می‌کند |

**نتیجه‌ی جستجو:** چیزِ بهتری برای این کارِ خاص وجود ندارد، چون گلوگاه ابزار نیست — **کپچا** است،
که هیچ‌کدام از این ابزارها حلش نمی‌کنند.

## چه چیزی عملاً کار می‌کند

| | |
|---|---|
| ✅ اجرای مرورگرِ واقعی در Actions | ثابت شد: `BROWSER: launched ok`, `STATUS: 200` |
| ✅ رندرِ کاملِ JS سایت (بنر کوکی، منو، متن) | ثابت شد |
| ✅ پیدا کردنِ فرم و فیلدها | ثابت شد |
| ❌ حلِ reCAPTCHA v2 | نه از من، نه از هیچ ابزارِ عادی |
| ❌ ورود با گوگل به‌صورت خودکار | گوگل اتوماسیون را بلاک می‌کند + به رمز/2FA نیاز دارد |

## راه‌حلِ واقعی

اسکریپت را طوری نوشتم که **روی سیستم خودت** اجرا شود:
- IP خانگی → کپچا معمولاً اصلاً نمی‌آید
- اگر هم آمد، اسکریپت **صبر می‌کند تا خودت حلش کنی** (human-in-the-loop)، بعد ادامه می‌دهد
- نشست را در `biodigital-session.json` ذخیره می‌کند تا دفعه‌های بعد لاگین باشد

```bash
node net/biodigital-signup.js
```
