# -*- coding: utf-8 -*-
"""اعتبارسنجیِ مدل، پیش از هر نتیجه‌گیری درباره‌یِ سیاست‌ها.

یافته‌ی تثبیت‌شده: با **همان مقدار مطالعه**، مرورِ فاصله‌دار ماندگاریِ بیشتری
از مرورِ انبوه می‌دهد.

نکته‌یِ طراحی (و خطایی که دو بار اول مرتکب شدم):
  - بارِ اول فاصله‌ی ثابتِ ۷ روزه گذاشتم؛ از ظرفیتِ حافظه بیشتر بود، کارت مرد.
  - بارِ دوم افق را ثابت گرفتم و تعدادِ مرور را آزاد؛ انبوه ۶۰۰۰ مرور کرد در
    برابر ۳۱ مرورِ فاصله‌دار و طبیعتاً بیشتر ماند. آن مقایسه بی‌معناست.
درستش این است: تعدادِ مرور را برابر بگیریم (هزینه‌ی مطالعه یکی باشد) و فقط
زمان‌بندی را عوض کنیم — همان کاری که آزمایش‌های واقعی می‌کنند.
"""
import math
import random


def R_(t, S):
    return math.exp(-t / S)


def run_one(policy, g_max, seed, n_reviews=10, spread=90, measure_after=30):
    """دقیقاً `n_reviews` مرور؛ فقط زمان‌بندی فرق می‌کند."""
    rng = random.Random(seed)
    S = 1.0
    last = None

    if policy == 'spaced':
        # مرورها در `spread` روز پخش می‌شوند، با فاصله‌یِ گسترش‌یابنده
        gaps, g = [], 1.0
        while len(gaps) < n_reviews:
            gaps.append(g)
            g *= 1.9
        scale = spread / sum(gaps)
        days = [sum(gaps[:i + 1]) * scale for i in range(n_reviews)]
    else:
        days = [0.0] * n_reviews                 # همه در یک روز

    for day in days:
        R = 1.0 if last is None else R_(day - last, S)
        ok = rng.random() < R
        # «دشواریِ مطلوب»: هرچه یادآوری در آستانه‌یِ فراموشی بوده، دستاورد بیشتر
        S = S * (1.0 + (g_max - 1.0) * (1.0 - R)) if ok else max(0.4, S * 0.7)
        last = day

    return S          # پایداریِ نهایی (معیارِ پیوسته)


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2.0


def run(g_max, n_cards=800, **kw):
    out = {}
    for pol in ('spaced', 'massed'):
        Ss = [run_one(pol, g_max, s, **kw) for s in range(n_cards)]
        out[pol] = median(Ss)          # میانه، چون توزیعِ S چوله است
    return out


if __name__ == '__main__':
    print("=" * 74)
    print("اعتبارسنجی: با تعدادِ مرورِ برابر، آیا فاصله‌دار بهتر از انبوه است؟")
    print("(۱۰ مرور برای هر دو؛ فقط زمان‌بندی فرق دارد. ۸۰۰ کارت در هر حالت)")
    print("=" * 74)
    print("%-8s | %-16s | %-16s | %s" % ('g_max', 'پایداریِ فاصله‌دار', 'پایداریِ انبوه', 'برنده'))
    print("-" * 74)
    bad = 0
    for g in (1.3, 1.6, 2.0, 2.5, 3.0, 4.0):
        r = run(g)
        ok = r['spaced'] > r['massed']
        bad += 0 if ok else 1
        print("%-8s | %13.1f روز | %13.1f روز | %s  (×%.2f)"
              % (g, r['spaced'], r['massed'],
                 'فاصله‌دار ✓' if ok else 'انبوه ✗',
                 r['spaced'] / max(r['massed'], 0.01)))
    print("-" * 74)
    print("حالت‌های خلافِ یافته‌ی تثبیت‌شده: %d از ۶" % bad)
    print("=> " + ("مدل اعتبارسنجی شد: اثرِ فاصله‌گذاری در همه‌ی فرض‌ها دیده می‌شود."
                   if bad == 0 else "مدل غیرقابل‌اعتماد است."))
