# -*- coding: utf-8 -*-
"""برنامه‌ریزیِ مرور (فاصله‌دار) — پیاده‌سازی و سنجش.

به‌جای تکرارِ ادعاهای دیگران، اینجا سه سیاست را روی یک مدلِ فراموشی
شبیه‌سازی می‌کنیم و بازدهِ هر کدام را به‌ازای «هر دقیقه مطالعه» می‌سنجیم.

مدل: احتمالِ یادآوری بعد از t روز با پایداریِ S برابر است با
        R(t) = exp(-t / S)
(همان نماییِ کلاسیکِ ابینگهاوس). پایداری بعد از هر بازیابیِ موفق رشد می‌کند
و بعد از شکست می‌ریزد — این هسته‌یِ مشترکِ SM-2 و FSRS است.
"""
import math
import random

# ── SM-2 (الگوریتمِ کلاسیکِ Anki) ────────────────────────────────────────
def sm2(card, grade):
    """grade: ۰=فراموش … ۵=عالی. خروجی: (فاصله‌ی بعدی به روز، ضریبِ آسانی)."""
    ef, interval, reps = card.get('ef', 2.5), card.get('interval', 0), card.get('reps', 0)

    if grade >= 3:                               # یادآوریِ موفق
        if reps == 0:
            interval = 1
        elif reps == 1:
            interval = 6
        else:
            interval = round(interval * ef)
        reps += 1
        ef = ef + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    else:                                        # فراموشی: از نو
        reps = 0
        interval = 1
    ef = max(1.3, ef)
    return {'ef': ef, 'interval': interval, 'reps': reps}


# ── یک سیاستِ ساده‌تر بر پایه‌یِ «پایداری» (نزدیک به FSRS) ────────────────
def stability_policy(card, grade):
    """فاصله را مستقیماً از پایداریِ برآوردشده می‌گیرد، نه از یک ضریبِ ثابت.

    ایده: هدف این است که در مرورِ بعدی احتمالِ یادآوری نزدیکِ ۰.۹ باشد،
    یعنی t = -S · ln(0.9). پایداری بعد از بازیابیِ موفق رشد می‌کند.
    """
    S = card.get('S', 1.0)
    target = 0.9                                  # احتمالِ یادآوریِ هدف
    if grade >= 3:
        # بازیابیِ موفق پایداری را می‌کشد؛ هرچه دیرتر یادآوری شود، اثرش بیشتر
        elapsed = max(card.get('interval', 1), 1)
        retrievability = math.exp(-elapsed / S)
        growth = 1.0 + (3.0 - 2.0 * retrievability)   # سخت‌تر یادآوری → رشدِ بیشتر
        S = S * growth
    else:
        S = max(0.4, S * 0.55)                    # فراموشی پایداری را می‌شکند
    interval = max(1, round(-S * math.log(target)))
    return {'S': S, 'interval': interval, 'reps': card.get('reps', 0) + 1}


# ── شبیه‌ساز ─────────────────────────────────────────────────────────────
# ── مدل‌های فراموشی ──────────────────────────────────────────────────────
# نکته‌یِ روش‌شناختی: سیاستِ «پایداری» بالا با فرضِ فراموشیِ نمایی نوشته شده.
# اگر همان مدل را در شبیه‌ساز هم به کار ببریم، مقایسه دورِ باطل می‌شود و
# سیاستِ خودمان همیشه می‌برد. پس شبیه‌ساز را با قانون‌های مختلف اجرا می‌کنیم
# تا ببینیم کدام سیاست در برابر «اشتباه فرض‌کردنِ مدل» مقاوم است.
def recall_prob(elapsed, S, model='exp'):
    if model == 'exp':
        return math.exp(-elapsed / S)
    if model == 'power':                     # فراموشیِ توانی: دُم‌سنگین‌تر
        return (1.0 + elapsed / S) ** -0.45
    raise ValueError(model)


def simulate(n_cards=200, days=180, policy='sm2', seed=1, review_cost=0.15,
             real_model='exp'):
    """هر کارت را در طول `days` روز مرور می‌کند.

    خروجی: چند کارت در پایان هنوز در حافظه است (R >= ۰.۹) و هزینه چقدر بوده.
    review_cost: زمانِ هر مرور بر حسب دقیقه.
    """
    rng = random.Random(seed)
    cards = []
    for i in range(n_cards):
        cards.append({
            'id': i,
            'S': rng.uniform(0.6, 1.4),           # پایداریِ اولیه: کارت‌ها با هم فرق دارند
            'difficulty': rng.uniform(0.75, 1.0),  # بعضی کارت‌ها ذاتاً سخت‌ترند
            'due': 0, 'ef': 2.5, 'interval': 0, 'reps': 0,
        })

    reviews = 0
    for day in range(days):
        for c in cards:
            if c['due'] > day:
                continue
            reviews += 1
            elapsed = max(day - c.get('last', -c['interval'] if c['interval'] else 0), 0)
            if c['reps'] == 0:
                R = 1.0                            # کارتِ نو: هنوز همان روز یاد گرفته شده
            else:
                R = recall_prob(elapsed, c['S'], real_model)
            p = R * c['difficulty']
            grade = 4 if rng.random() < p else 1   # موفق/ناموفق

            upd = sm2(c, grade) if policy == 'sm2' else stability_policy(c, grade)
            c.update(upd)
            if grade >= 3:
                # بازیابیِ موفق پایداری را می‌کشد (برای SM-2 هم لازم است،
                # وگرنه مدل پایداری ثابت می‌ماند و شبیه‌سازی بی‌معنا می‌شود)
                growth = 1.0 + (3.0 - 2.0 * R)
                c['S'] = c['S'] * growth
            else:
                c['S'] = max(0.4, c['S'] * 0.55)
            c['last'] = day
            c['due'] = day + max(1, c.get('interval', 1))

    # در پایان: چند کارت هنوز یادآوری می‌شوند؟
    retained = 0
    for c in cards:
        if c['reps'] == 0:
            continue
        elapsed = days - c.get('last', 0)
        if recall_prob(elapsed, c['S'], real_model) >= 0.9:
            retained += 1
    return {
        'policy': policy,
        'retained': retained,
        'pct': 100.0 * retained / n_cards,
        'reviews': reviews,
        'minutes': round(reviews * review_cost, 1),
        'per_100': round(100.0 * retained / max(reviews, 1) * 100, 1),
    }


def compare(n_cards=200, days=180, seeds=(1, 2, 3, 4, 5), real_model='exp'):
    out = {}
    for pol in ('sm2', 'stability'):
        rs = [simulate(n_cards, days, pol, s, real_model=real_model) for s in seeds]
        out[pol] = {
            'retained_pct': round(sum(r['pct'] for r in rs) / len(rs), 1),
            'reviews': round(sum(r['reviews'] for r in rs) / len(rs)),
            'minutes': round(sum(r['minutes'] for r in rs) / len(rs), 1),
        }
    return out


if __name__ == '__main__':
    print("مقایسه با مدل‌های مختلفِ فراموشی (۲۰۰ کارت، ۱۸۰ روز، میانگینِ ۵ seed)")
    print("هر دو سیاست فرض می‌کنند فراموشی نمایی است؛ واقعیت ممکن است چیزِ دیگری باشد.")
    print()
    for model in ('exp', 'power'):
        print("=" * 66)
        print("اگر قانونِ واقعیِ فراموشی = %s باشد:" % ('نمایی' if model == 'exp' else 'توانی'))
        print("=" * 66)
        r = compare(real_model=model)
        print("%-12s %12s %14s %10s" % ('سیاست', 'ماندگاری', 'تعداد مرور', 'دقیقه'))
        print("-" * 66)
        for pol, v in r.items():
            print("%-12s %11s%% %14d %10s" % (pol, v['retained_pct'], v['reviews'], v['minutes']))
        a, b = r['sm2'], r['stability']
        print("-" * 66)
        print("  بازده: SM-2 = %.3f کارت/دقیقه | پایداری = %.3f کارت/دقیقه"
              % (a['retained_pct'] / a['minutes'], b['retained_pct'] / b['minutes']))
        print()
