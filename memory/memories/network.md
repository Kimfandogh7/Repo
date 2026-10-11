# network


## 2026-10-11T03:02:44Z

* شبکه سندباکس در لایه ۷/SNI فیلتر می‌شود: TCP برای هاست‌های مسدود هم باز است (bash /dev/tcp) اما دست‌تکانی TLS می‌میرد

## 2026-10-11T03:02:44Z

* هاست‌های مجاز: github.com, api.github.com, codeload.github.com, registry.npmjs.org, pypi.org, files.pythonhosted.org

## 2026-10-11T03:02:44Z

* مسدود: raw.githubusercontent.com, example.com, google.com, huggingface.co, cdn.playwright.dev, objects.githubusercontent.com

## 2026-10-11T11:59:34Z

* کشفِ مهم: سندباکس دسترسیِ مستقیم به github.com، registry.npmjs.org و pypi.org دارد — git clone و npm install و pip install مستقیم کار می‌کنند، نیازی به relay نیست

## 2026-10-11T11:59:34Z

* pip محلی به --break-system-packages نیاز دارد (PEP 668)؛ python3 -m venv --without-pip کار می‌کند ولی venv معمولی نه
