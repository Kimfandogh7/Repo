# -*- coding: utf-8 -*-
"""دفترچه‌ی خطاهای تکراری (ایده‌ی ۴۴).

مسئله: گفتنِ «این دانش‌آموز ۵ تا غلط داشت» هیچ کمکی نمی‌کند. چیزی که قابل‌درمان
است **الگو در اشتباه** است: آیا او مدام مشتقِ لایه‌ی درونی را فراموش می‌کند؟
مدام علامت را خراب می‌کند؟

نکته‌یِ آماریِ کلیدی (همان که اگر نادیده گرفته شود کل تحلیل بی‌ارزش می‌شود):
انواعِ خطا نرخِ پایه‌یِ برابر ندارند. در این بانک power_error یک‌چهارمِ
گزینه‌های انحرافی است اما const_error فقط ۳٪. پس دیدنِ «۳ خطای توان» اصلاً
نشانه نیست — همان قدر اتفاق می‌افتد که اگر کسی شانسی می‌زد. اما دیدنِ
«۲ خطای ثابت» بعید است تصادفی باشد.

برای همین اینجا از آزمونِ دوجمله‌ای استفاده می‌کنیم: به‌ازای هر نوع خطا،
«اگر این دانش‌آموز تصادفی غلط می‌زد، چند بار انتظار داشتیم این نوع را ببینیم؟»
و فقط انواعی را گزارش می‌کنیم که به‌طورِ معنادار بیشتر از آن انتظار دیده شده.
"""
import json
import math
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(os.path.dirname(HERE), 'diagnose', 'bank-calculus.json')

try:
    from tag_distractors import LABELS_FA
except ImportError:
    LABELS_FA = {}


# دقتِ رده‌بندی، اندازه‌گیری‌شده با test_patterns.py / compare_methods.py.
# شرط: دانش‌آموز در ۸۵٪ِ مواقع همان خطایِ پایدار را مرتکب می‌شود.
# این جدول برای این است که ابزار ادعایِ قطعیت نکند — می‌گوید با این تعداد
# خطا، انتظارِ واقع‌بینانه چقدر است.
ACCURACY_TOP1 = {12: 26, 20: 34, 30: 40, 50: 46, 100: 56}
ACCURACY_TOP3 = {12: 55, 20: 58, 30: 66, 50: 69, 100: 74}


def accuracy_top3(n):
    """نزدیک‌ترین مقدارِ اندازه‌گیری‌شده برای n خطا."""
    if not ACCURACY_TOP3:
        return 60
    if n <= min(ACCURACY_TOP3):
        return ACCURACY_TOP3[min(ACCURACY_TOP3)]
    if n >= max(ACCURACY_TOP3):
        return ACCURACY_TOP3[max(ACCURACY_TOP3)]
    ks = sorted(ACCURACY_TOP3)
    lo = max(k for k in ks if k <= n)
    hi = min(k for k in ks if k >= n)
    return ACCURACY_TOP3[lo]


def load_bank(path=BANK):
    bank = json.load(open(path, encoding='utf-8'))
    return {q['id']: q for q in bank}


def base_rates(bank):
    """نرخِ پایه: سهمِ هر نوع خطا در میانِ همه‌ی گزینه‌های انحرافیِ بانک."""
    c = Counter()
    for q in bank.values():
        for v in (q.get('distractor_tags') or {}).values():
            c[v] += 1
    tot = sum(c.values())
    return {k: v / tot for k, v in c.items()}, tot


def binom_p_at_least(k, n, p):
    """P(X >= k) برای X ~ Binomial(n, p)."""
    if p <= 0 or n == 0:
        return 1.0
    if k <= 0:
        return 1.0
    if k > n:
        return 0.0
    s = 0.0
    for i in range(k, n + 1):
        s += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return min(1.0, s)


def analyse(answers, bank=None, alpha=0.05):
    """answers: لیستِ (شناسه‌ی سؤال، اندیسِ گزینه‌ی انتخاب‌شده).

    فقط پاسخ‌های غلط بررسی می‌شوند. خروجی: انواعِ خطایی که به‌طورِ معنادار
    بیشتر از نرخِ پایه تکرار شده‌اند.
    """
    bank = bank or load_bank()
    rates, _ = base_rates(bank)

    wrong = []
    for qid, chosen in answers:
        q = bank.get(qid)
        if not q or chosen == q['answer']:
            continue
        tag = (q.get('distractor_tags') or {}).get(str(chosen))
        wrong.append((qid, tag))

    n = len(wrong)
    obs = Counter(t for _, t in wrong if t)
    n_tagged = sum(obs.values())

    rows = []
    for etype, k in obs.items():
        p = rates.get(etype, 0.0)
        exp = n_tagged * p
        pv = binom_p_at_least(k, n_tagged, p)
        rows.append({
            'type': etype,
            'label': LABELS_FA.get(etype, etype),
            'seen': k,
            'expected': round(exp, 2),
            'ratio': round(k / exp, 2) if exp > 0 else None,
            'p_value': pv,
        })

    # تصحیحِ بونفرونی: ده نوع خطا را هم‌زمان آزمایش می‌کنیم، پس ساده‌لوحانه
    # است که هر کدام را با آلفای ۰٫۰۵ بسنجیم — یکی از هر بیست به‌خطا معنادار می‌شود.
    m = max(len(rates), 1)
    for r in rows:
        r['p_corrected'] = min(1.0, r['p_value'] * m)
        r['significant'] = r['p_corrected'] < alpha

    rows.sort(key=lambda r: (r['p_value'], -r['seen']))
    return {
        'errors': n,
        'errors_tagged': n_tagged,
        'patterns': rows,
        'flagged': [r for r in rows if r['significant']],
        'detail': wrong,
    }


def report(answers, bank=None):
    r = analyse(answers, bank)
    n = r['errors_tagged']
    print('تعداد خطا: %d (%d تا قابل‌برچسب)' % (r['errors'], n))
    print()
    print('%-16s %6s %10s %8s %10s' % ('نوع خطا', 'دیده', 'انتظار', 'نسبت', 'p(اصلاح)'))
    print('-' * 60)
    for row in r['patterns']:
        print('%-16s %6d %10.2f %8s %10.3f'
              % (row['type'], row['seen'], row['expected'],
                 ('×%.1f' % row['ratio']) if row['ratio'] else '-',
                 row['p_corrected']))
    print('-' * 60)

    # رده‌بندیِ مظنون‌ها — نه حکم قطعی. دقتِ این رده‌بندی اندازه‌گیری شده است.
    ranked = [x['type'] for x in r['patterns']]
    if ranked:
        print()
        print('مظنون‌های اصلی (به ترتیبِ احتمال):')
        for i, t in enumerate(ranked[:3], 1):
            row = next(x for x in r['patterns'] if x['type'] == t)
            print('  %d. %s  — %d بار، %.1f برابرِ انتظار'
                  % (i, row['label'], row['seen'], row['ratio']))
        print()
        print('  ⚠ این رده‌بندی قطعی نیست. با %d خطا، احتمال اینکه باگِ اصلی' % n)
        print('    در همین سه‌تا باشد حدود %.0f%% است' % accuracy_top3(n))
    else:
        print('هیچ خطایِ قابل‌برچسبی نیست.')
    return r


if __name__ == '__main__':
    # نمونه: دانش‌آموزی که مدام مشتقِ زنجیره‌ای را فراموش می‌کند
    demo = [('c01', 1), ('c02', 1), ('d01', 1), ('c03', 1), ('p01', 1), ('t01', 1)]
    report(demo)
