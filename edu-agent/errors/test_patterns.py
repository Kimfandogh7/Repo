# -*- coding: utf-8 -*-
"""آزمونِ سخت‌گیرانه: آیا این ابزار واقعاً الگو را پیدا می‌کند؟

دو پرسش که باید جواب داده شوند وگرنه ابزار بی‌فایده است:
  ۱. اگر دانش‌آموز واقعاً یک باگِ پایدار داشته باشد، چند خطا طول می‌کشد تا
     آن را تشخیص دهیم؟ (حساسیت)
  ۲. اگر هیچ الگویی نداشته باشد و فقط شانسی غلط بزند، چند بار بی‌خود
     «الگو» اعلام می‌کنیم؟ (خطایِ مثبتِ کاذب)

هر دو را با هم می‌سنجیم، چون ابزاری که همه‌چیز را «الگو» می‌بیند بی‌فایده است،
و ابزاری که هیچ‌وقت چیزی نمی‌بیند هم همین‌طور.
"""
import random
import sys
from collections import Counter

sys.path.insert(0, __import__('os').path.dirname(__file__))
import patterns as P

BANK = P.load_bank()
RATES, _ = P.base_rates(BANK)
TYPES = sorted(RATES)


def distractors_of(q, etype):
    return [int(i) for i, t in (q.get('distractor_tags') or {}).items() if t == etype]


def simulate(bug=None, bug_rate=0.6, n_errors=10, seed=0, alpha=0.05):
    """یک دانش‌آموز شبیه‌سازی می‌کند.

    bug: نوعِ خطایِ پایدار (مثلاً forgot_chain) یا None یعنی خطایِ تصادفی.
    bug_rate: اگر گزینه‌ای با آن نوع خطا در دسترس باشد، با این احتمال آن را برمی‌گزیند.
    """
    rng = random.Random(seed)
    ids = sorted(BANK)
    wrong = []
    while len(wrong) < n_errors:
        qid = rng.choice(ids)
        q = BANK[qid]
        tags = q.get('distractor_tags') or {}
        if not tags:
            continue
        opts = [int(i) for i in tags]
        chosen = None
        if bug:
            cand = distractors_of(q, bug)
            if cand and rng.random() < bug_rate:
                chosen = rng.choice(cand)
        if chosen is None:
            chosen = rng.choice(opts)
        if chosen == q['answer']:
            continue
        wrong.append((qid, chosen))
    return wrong


def trial(bug, n_errors, seed, alpha=0.05, bug_rate=0.6):
    ans = simulate(bug, bug_rate, n_errors, seed)
    r = P.analyse(ans, BANK, alpha=alpha)
    flags = [x['type'] for x in r['flagged']]
    hit = (bug in flags) if bug else False
    return hit, bool(flags), flags


def run(n_errors, seeds=60, bug_rate=0.6, alpha=0.05):
    """برای هر نوع خطا: چند درصدِ مواقع باگ درست تشخیص داده می‌شود."""
    out = {}
    for t in TYPES:
        hits = sum(trial(t, n_errors, s, alpha, bug_rate)[0] for s in range(seeds))
        out[t] = 100.0 * hits / seeds
    # نرخِ هشدارِ کاذب: بدونِ هیچ باگی
    fps = sum(trial(None, n_errors, s, alpha, bug_rate)[1] for s in range(seeds))
    return out, 100.0 * fps / seeds


if __name__ == '__main__':
    print('=' * 78)
    print('چند خطا لازم است تا یک باگِ پایدار شناخته شود؟')
    print('(دانش‌آموز در ۶۰٪ِ مواقع همان خطایِ پایدار را مرتکب می‌شود؛ ۶۰ آزمایش)')
    print('=' * 78)
    print('%-8s | %s | %s' % ('تعداد', 'میانگینِ نرخِ تشخیص', 'هشدارِ کاذب'))
    print('-' * 78)
    for n in (5, 8, 12, 16, 20, 30):
        res, fp = run(n)
        avg = sum(res.values()) / len(res)
        print('%-8d | %18.0f%% | %10.0f%%' % (n, avg, fp))
    print('-' * 78)
    print()
    print('=' * 78)
    print('کدام نوع خطا زودتر شناخته می‌شود؟ (با ۱۲ خطا)')
    print('=' * 78)
    res, fp = run(12)
    for t in sorted(res, key=lambda k: -res[k]):
        print('  %-16s %5.0f%%   (نرخِ پایه %.1f%%)' % (t, res[t], 100 * RATES[t]))
    print('-' * 78)
    print('  هشدارِ کاذب (وقتی هیچ الگویی نیست): %.0f%%' % fp)
