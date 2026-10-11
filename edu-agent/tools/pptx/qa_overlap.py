#!/usr/bin/env python3
"""بازرسیِ خودکارِ اسلایدها: برخورد متن‌ها، خروج از بوم، حاشیه‌ی ناایمن.

چرا لازم است: دروازه‌ی کیفیتِ ppt-master فقط خطاهای ساختاری را می‌گیرد،
نه اشتباهاتِ چیدمان. دو متن می‌توانند دقیقاً روی هم بیفتند و دروازه
هیچ نگوید. این ابزار همان‌ها را می‌گیرد.

استفاده:
    python3 qa_overlap.py <file.pptx>
"""
import sys
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU = 914400
# تقریبِ پهنای متن برای Arial: هر کاراکتر حدود ۰٫۵۲ برابر اندازه‌ی قلم
CHAR_W = 0.52


def walk(shapes, out=None):
    if out is None:
        out = []
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            walk(sh.shapes, out)
        else:
            out.append(sh)
    return out


def text_boxes(slide):
    """مستطیلِ هر متن را برمی‌گرداند (اینچ)."""
    boxes = []
    for sh in walk(slide.shapes):
        if not (sh.has_text_frame and sh.text_frame.text.strip()):
            continue
        txt = sh.text_frame.text.strip()
        size = 18.0
        for p in sh.text_frame.paragraphs:
            for r in p.runs:
                if r.font.size:
                    size = r.font.size.pt
                    break
            break
        left = (sh.left or 0) / EMU
        top = (sh.top or 0) / EMU
        box_w = (sh.width / EMU) if sh.width else 0
        box_h = (sh.height / EMU) if sh.height else 0
        # پهنای واقعیِ حروف را تخمین بزن؛ جعبه ممکن است عریض‌تر باشد
        est_w = len(txt) * size * CHAR_W / 72
        w = min(est_w, box_w) if box_w else est_w
        # بلندیِ حروف (نه جعبه): جعبه شامل فاصله‌ی خط است
        glyph_h = size * 1.0 / 72
        # حروف درون جعبه عموداً وسط‌چین‌اند
        t = top + max(0.0, (box_h - glyph_h) / 2.0) if box_h else top
        boxes.append({
            "text": txt, "l": left, "t": t,
            "r": left + w, "b": t + glyph_h, "pt": size,
        })
    return boxes


def overlap(a, b):
    ox = min(a["r"], b["r"]) - max(a["l"], b["l"])
    oy = min(a["b"], b["b"]) - max(a["t"], b["t"])
    if ox > 0.02 and oy > 0.02:
        return round(ox, 2), round(oy, 2)
    return None


def main(path):
    prs = Presentation(path)
    W = prs.slide_width / EMU
    H = prs.slide_height / EMU
    problems = []
    print(f"بررسی {path}")
    print(f"بوم: {W:.2f} × {H:.2f} اینچ\n")

    for i, slide in enumerate(prs.slides, 1):
        boxes = text_boxes(slide)
        # ۱. برخوردِ متن‌ها
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                ov = overlap(boxes[a], boxes[b])
                if ov:
                    problems.append(
                        f"اسلاید {i}: برخوردِ متن {ov[0]}×{ov[1]} اینچ — "
                        f"«{boxes[a]['text'][:34]}» با «{boxes[b]['text'][:34]}»"
                    )
        # ۲. خروج از بوم
        for bx in boxes:
            if bx["r"] > W + 0.01:
                problems.append(
                    f"اسلاید {i}: «{bx['text'][:34]}» "
                    f"{bx['r'] - W:.2f} اینچ از سمت راست بیرون زده"
                )
            if bx["b"] > H + 0.01:
                problems.append(
                    f"اسلاید {i}: «{bx['text'][:34]}» "
                    f"{bx['b'] - H:.2f} اینچ از پایین بیرون زده"
                )
            if bx["l"] < -0.01 or bx["t"] < -0.01:
                problems.append(
                    f"اسلاید {i}: «{bx['text'][:34]}» خارج از گوشه‌ی بالا-چپ"
                )
        # ۳. حاشیه‌ی ناایمن (کمتر از ۰٫۴ اینچ تا لبه)
        for bx in boxes:
            for lbl, dist in (("چپ", bx["l"]), ("بالا", bx["t"]),
                              ("راست", W - bx["r"]), ("پایین", H - bx["b"])):
                if 0 <= dist < 0.4:
                    problems.append(
                        f"اسلاید {i}: «{bx['text'][:28]}» تنها {dist:.2f} "
                        f"اینچ تا لبه‌ی {lbl} فاصله دارد"
                    )
        print(f"  اسلاید {i}: {len(boxes)} متن")

    print()
    if problems:
        print(f"⚠  {len(problems)} مشکل یافت شد:")
        for p in problems:
            print("   -", p)
        return 1
    print("✓ هیچ برخورد یا خروجی یافت نشد")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "out.pptx"))
