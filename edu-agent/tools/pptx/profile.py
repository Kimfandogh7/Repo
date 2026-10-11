#!/usr/bin/env python3
"""مقایسه‌ی پروفایلِ روشناییِ یک اسلاید با ویدیوی مرجع.

چرا: مرجع‌های حرفه‌ای محتوا را در یک نوارِ درخشانِ میانی (۳۰-۶۰٪ ارتفاع)
نگه می‌دارند و بالا/پایین را سیاه می‌گذارند. این ابزار همان پروفایل را
از یک تصویر استخراج می‌کند تا بتوانی خروجی‌ات را با مرجع بسنجی.

استفاده:
    python3 profile.py <تصویر>
"""
import sys, statistics
from PIL import Image


def rows(path, bands=20):
    im = Image.open(path).convert("L")
    w, h = im.size
    out = []
    for i in range(bands):
        y0, y1 = i * h // bands, (i + 1) * h // bands
        px = list(im.crop((0, y0, w, y1)).resize((60, 6)).getdata())
        out.append(sum(px) / len(px))
    return out


REFERENCE = [2.7, 2.7, 3.6, 19.8, 24.8, 6.7, 115.2, 177.4, 181.0, 177.9,
             163.5, 158.0, 82.0, 3.1, 17.2, 15.3, 11.8, 9.8, 4.3, 3.1]


def main(path):
    r = rows(path)
    print(f"{'ناحیه':>9} {'مرجع':>6} {'شما':>6}")
    for i in range(20):
        bar_r = "█" * int(REFERENCE[i] / 8)
        bar_m = "█" * int(r[i] / 8)
        print(f"{i*5:3d}-{(i+1)*5:3d}% {REFERENCE[i]:6.1f} {r[i]:6.1f}  {bar_r:28s}|{bar_m}")
    cr = statistics.mean(REFERENCE[6:12])
    cm = statistics.mean(r[6:12])
    print(f"\nهسته میانی (۳۰-۶۰٪): مرجع {cr:.0f} | شما {cm:.0f} | نسبت {cm/cr:.2f}")
    checks = [
        ("بالا سیاه است (۰-۱۵٪)", statistics.mean(r[0:3]) < 25),
        ("پایین سیاه است (۸۵-۱۰۰٪)", statistics.mean(r[17:20]) < 25),
        ("هسته درخشان است", cm > 80),
    ]
    print()
    for name, ok in checks:
        print(f"  {'✓' if ok else '✗'} {name}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "out.png")
