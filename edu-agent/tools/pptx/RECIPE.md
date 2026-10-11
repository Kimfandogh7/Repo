# دستورِ کار — ساخت اسلایدِ بومی با ppt-master

نصب: `bash edu-agent/tools/pptx/setup.sh`
منبع: `github.com/hugohe3/ppt-master` · MIT · حدود ۶۰ هزار ستاره · پروانه‌ی آزاد، داده محلی می‌ماند، به هیچ مدلی قفل نیست.

---

## ۱. ساخت پروژه (حتماً با `project_manager`، دستی نساز)

```bash
cd edu-agent/vendor/ppt-master
P=projects/<نام>
python3 skills/ppt-master/scripts/project_manager.py init <نام> --format ppt169
python3 skills/ppt-master/scripts/project_manager.py scaffold-lock $P
```

> نامِ پوشه خودکار `_ppt169_<تاریخ>` می‌گیرد. بعد از ساخت، جاهای `[fill]` را در
> `spec_lock.md` پر کن (زبان، مخاطب، هدف، رنگ‌ها، تایپوگرافی).

## ۲. نوشتن اسلایدها در `svg_output/*.svg`

بومِ `ppt169` یعنی `viewBox="0 0 1280 720"`.
هر لایه‌ی منطقی را در یک `<g id="..." data-pptx-bounds="x y w h">` ببند —
بدون این گروه‌ها، انیمیشنِ جداگانه روی آن‌ها ممکن نیست.

## ۳. انیمیشن

```bash
python3 skills/ppt-master/scripts/animation_config.py scaffold $P   # ساختِ animations.json
python3 skills/ppt-master/scripts/animation_config.py list-groups $P # دیدنِ گروه‌های واقعی
python3 skills/ppt-master/scripts/animation_config.py validate $P
```

در `animations.json` برای هر گروه اثر بگذار: `entrance_fade`, `entrance_fly`,
`entrance_zoom`, `entrance_wipe`, `emphasis_*`, `path_*`, `exit_*` (بیش از ۲۰۰ اثر)
و انتقالِ بین اسلایدها (بیش از ۶۰ مورد: `morph`, `cube`, `origami`, `vortex`, `ferris_wheel`, …).

## ۴. تصویر و برش (cutout)

تصویر را کنارِ SVG بگذار و با مسیرِ نسبی ارجاع بده، بعد جاسازی‌اش کن:

```xml
<image x="172" y="112" width="496" height="496"
       preserveAspectRatio="xMidYMid slice"
       clip-path="url(#cut-circle)"
       xlink:href="photo.jpg"/>
```

```bash
python3 skills/ppt-master/scripts/finalize_svg.py $P    # تبدیل به base64 و جاسازی
```

`clip-path` **فقط** روی `<image>` مجاز است — همان برش/حذفِ پس‌زمینه.

## ۵. عبور از دروازه‌ی کیفیت (واجب)

```bash
python3 skills/ppt-master/scripts/svg_quality_checker.py $P --canonical-authoring --stage final --json
```

تا خطا صفر نشود، خروجی نمی‌دهد. بعد از **هر** ویرایشِ SVG دوباره اجرا کن.

## ۶. صدور

```bash
python3 skills/ppt-master/scripts/svg_to_pptx.py -o out.pptx -f ppt169 $P
```

---

## خطاهایی که گرفت و راه‌حل‌شان

| پیام | علت | درمان |
|---|---|---|
| `spec_lock.md is required` | پوشه دستی ساخته شده | `project_manager.py init` + `scaffold-lock` |
| `requires a passing final SVG quality report` | گزارشِ کیفیت اجرا نشده | `svg_quality_checker.py ... --stage final --json` |
| `<g> without data-pptx-bounds` | گروه بی‌مرز | `data-pptx-bounds="0 0 1280 720"` اضافه کن |
| `font-size N exceeds sparse-display limit of 2` | اندازه‌ی قلم تکراری | آن اندازه را با نام در `spec_lock.md` تعریف کن (`metric: 34`) |
| `unresolved href` | مسیرِ تصویر اشتباه است | تصویر را کنارِ SVG بگذار و با نامِ فایل ارجاع بده |

---

## رندرِ پیش‌نمایش (دیدنِ خروجی بدون پاورپوینت)

در سندباکس نه LibreOffice هست نه cairo. مسیری که کار می‌کند:

```
SVG → svglib → reportlab (PDF) → PyMuPDF → PNG
```

```python
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
import pymupdf
renderPDF.drawToFile(svg2rlg('s.svg'), 's.pdf')
pymupdf.open('s.pdf')[0].get_pixmap(dpi=100).save('s.png')
```

**محدودیتِ رندرر:** svglib مقدارِ `stop-opacity` را درون گرادینت نادیده می‌گیرد و
آن را رنگِ کامل می‌کشد. برای پیش‌نمایش، عنصرِ درخشان (glow) را موقتاً حذف کن.
این ایرادِ **پیش‌نمایش** است، نه فایل — پاورپوینت آن را درست نشان می‌دهد.

---

## نتیجه‌ی اندازه‌گیری‌شده (تستِ ۴ اسلایدیِ فرمول یک)

- ۴ اسلایدِ ۱۶:۹ (۱۳٫۳۳ × ۷٫۵ اینچ)
- انتقالِ `morph` تأیید شده در XML
- انیمیشن روی اسلایدها، با `timing` و گره‌های `animEffect`
- تصویرِ واقعی به صورت `PICTURE` درون `GROUP` جاسازی شد
- همه‌ی اشیاء از نوع `TEXT_BOX` / `AUTO_SHAPE` / `FREEFORM` / `PICTURE` —
  **هیچ چیز به عکس فلت نشده**؛ متن و شکل‌ها در پاورپوینت قابل ویرایش‌اند

## تولید تصویر

هیچ کلیدِ API لازم نیست: خودِ ایجنت تصویر می‌سازد و خروجی را در `svg_output/` می‌گذارد.
اگر بخواهی مستقیم از خط فرمان بسازی، `image_gen.py` شانزده بک‌اند دارد
(gemini, openai, qwen, seedream, flux, ideogram, replicate, fal, …) که با کلیدِ خودت کار می‌کنند.
