# -*- coding: utf-8 -*-
"""آزمونِ حساسیت: آیا برتریِ سیاستِ «پایداری» واقعی است یا مصنوعِ فرض‌های من؟

تنها چیزی که می‌دانم با اطمینان نمی‌دانم این است که «یک بازیابیِ موفق چقدر
حافظه را قوی‌تر می‌کند». پس آن را از خوش‌بینانه تا بدبینانه جارو می‌کنم و
می‌بینم نتیجه کجا عوض می‌شود.
"""
import math
import random
import schedule as S


def simulate_g(n_cards=200, days=180, policy='sm2', seed=1, g_max=3.0,
               review_cost=0.15):
    """مانند schedule.simulate ولی با نرخِ رشدِ قابل‌تنظیم (g_max)."""
    rng = random.Random(seed)
    cards = [{'id': i, 'S': rng.uniform(0.6, 1.4),
              'difficulty': rng.uniform(0.75, 1.0),
              'due': 0, 'ef': 2.5, 'interval': 0, 'reps': 0} for i in range(n_cards)]

    reviews = 0
    for day in range(days):
        for c in cards:
            if c['due'] > day:
                continue
            reviews += 1
            elapsed = max(day - c.get('last', 0), 0)
            R = 1.0 if c['reps'] == 0 else math.exp(-elapsed / c['S'])
            grade = 4 if rng.random() < R * c['difficulty'] else 1

            upd = (S.sm2(c, grade) if policy == 'sm2'
                   else S.stability_policy(c, grade))
            c.update(upd)
            growth = 1.0 + (g_max - 2.0) * (1.0 - R) + (g_max - 2.0) * 0.0
            # ساده‌تر و شفاف‌تر: رشد بین ۱ و g_max، هرچه یادآوری سخت‌تر بود رشد بیشتر
            growth = 1.0 + (g_max - 1.0) * (1.0 - R)
            c['S'] = c['S'] * growth if grade >= 3 else max(0.4, c['S'] * 0.55)
            c['last'] = day
            c['due'] = day + max(1, c.get('interval', 1))

    retained = sum(1 for c in cards
                   if c['reps'] and math.exp(-(days - c.get('last', 0)) / c['S']) >= 0.9)
    return 100.0 * retained / n_cards, reviews


if __name__ == '__main__':
    print("=" * 74)
    print("حساسیت به «هر بازیابیِ موفق چقدر حافظه را قوی‌تر می‌کند» (g_max)")
    print("۲۰۰ کارت، ۱۸۰ روز، میانگینِ ۳ seed")
    print("=" * 74)
    print("%-8s | %-16s | %-16s | %s" % ('g_max', 'SM-2 ماندگاری', 'پایداری', 'برنده'))
    print("-" * 74)
    for g in (1.3, 1.6, 2.0, 2.5, 3.0, 4.0):
        a = [simulate_g(policy='sm2', seed=s, g_max=g) for s in (1, 2, 3)]
        b = [simulate_g(policy='stability', seed=s, g_max=g) for s in (1, 2, 3)]
        ra = sum(x[0] for x in a) / 3
        rb = sum(x[0] for x in b) / 3
        ra_rev = sum(x[1] for x in a) / 3
        rb_rev = sum(x[1] for x in b) / 3
        # بازده: ماندگاری به‌ازای هر ۱۰۰ مرور
        ea, eb = ra / max(ra_rev, 1) * 100, rb / max(rb_rev, 1) * 100
        win = 'پایداری' if eb > ea else 'SM-2'
        print("%-8s | %6.1f%% (%5.0f) | %6.1f%% (%5.0f) | %s  (%.2f در برابر %.2f)"
              % (g, ra, ra_rev, rb, rb_rev, win, ea, eb))
    print("-" * 74)
    print("عددِ داخلِ پرانتز = تعدادِ مرور در ۱۸۰ روز (کمتر بهتر)")
