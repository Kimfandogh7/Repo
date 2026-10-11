# -*- coding: utf-8 -*-
"""کدام روش واقعاً الگو را پیدا می‌کند؟

سه روش را روی یک مسئله‌یِ واحد مقایسه می‌کنیم:
  الف) ساده‌شماری: پرتکرارترین نوع خطا را گزارش کن
  ب) نسبت به نرخِ پایه (بدون آزمونِ معناداری)
  ج) آزمونِ دوجمله‌ای + تصحیحِ بونفرونی

اگر روشِ آماری عملاً بدتر از ساده‌شماری باشد، باید صادقانه همان ساده را
انتخاب کنیم — پیچیدگی‌ای که چیزی اضافه نمی‌کند فقط خطرِ خطا بیشتر می‌کند.
"""
import random
import sys
from collections import Counter

sys.path.insert(0, __import__('os').path.dirname(__file__))
import patterns as P

BANK = P.load_bank()
RATES, _ = P.base_rates(BANK)
TYPES = sorted(RATES)


def simulate(bug, bug_rate, n_errors, seed):
    rng = random.Random(seed)
    ids = sorted(BANK)
    wrong = []
    while len(wrong) < n_errors:
        q = BANK[rng.choice(ids)]
        tags = q.get('distractor_tags') or {}
        if not tags:
            continue
        opts = [int(i) for i in tags]
        chosen = None
        if bug:
            cand = [int(i) for i, t in tags.items() if t == bug]
            if cand and rng.random() < bug_rate:
                chosen = rng.choice(cand)
        if chosen is None:
            chosen = rng.choice(opts)
        if chosen == q['answer']:
            continue
        wrong.append((q['id'], chosen))
    return wrong


def top_types(wrong, bank=BANK):
    obs = Counter()
    for qid, ch in wrong:
        t = (bank[qid].get('distractor_tags') or {}).get(str(ch))
        if t:
            obs[t] += 1
    return obs


def detect_naive(wrong, **_):
    """الف) فقط پرتکرارترین."""
    obs = top_types(wrong)
    return [obs.most_common(1)[0][0]] if obs else []


def detect_ratio(wrong, min_ratio=2.0, min_seen=2, **_):
    """ب) هر نوعی که دست‌کم ۲ برابرِ انتظار و دست‌کم ۲ بار دیده شده."""
    obs = top_types(wrong)
    n = sum(obs.values())
    out = []
    for t, k in obs.items():
        exp = n * RATES.get(t, 0)
        if k >= min_seen and exp > 0 and k / exp >= min_ratio:
            out.append(t)
    return out


def detect_binom(wrong, alpha=0.05, **_):
    """ج) آزمونِ دوجمله‌ای با تصحیحِ بونفرونی."""
    return [x['type'] for x in P.analyse(wrong, BANK, alpha=alpha)['flagged']]


METHODS = {'ساده‌شماری': detect_naive, 'نسبت به پایه': detect_ratio, 'دوجمله‌ای+بونفرونی': detect_binom}


def run(bug, bug_rate, n_errors, seeds=80):
    out = {}
    for name, fn in METHODS.items():
        hits = 0
        for s in range(seeds):
            w = simulate(bug, bug_rate, n_errors, s)
            if bug in fn(w):
                hits += 1
        out[name] = 100.0 * hits / seeds
    return out


def false_positive(n_errors, seeds=80):
    """بدونِ هیچ باگی: هر روش چند بار بی‌خود چیزی اعلام می‌کند؟"""
    out = {}
    for name, fn in METHODS.items():
        c = 0
        for s in range(seeds):
            w = simulate(None, 0.0, n_errors, s + 5000)
            if fn(w):
                c += 1
        out[name] = 100.0 * c / seeds
    return out


if __name__ == '__main__':
    for rate in (0.6, 0.85):
        print('=' * 76)
        print('اگر دانش‌آموز در %.0f%%ِ مواقع همان خطای پایدار را مرتکب شود:' % (rate * 100))
        print('=' * 76)
        print('%-8s | %-24s | %-24s | %-24s' % ('تعداد', *METHODS))
        print('-' * 76)
        for n in (8, 12, 20):
            res = {}
            for t in TYPES:
                r = run(t, rate, n)
                for k, v in r.items():
                    res.setdefault(k, []).append(v)
            fp = false_positive(n)
            print('%-8d |' % n, end='')
            for k in METHODS:
                print(' %14.0f%% تشخیص      |' % (sum(res[k]) / len(res[k])), end='')
            print()
            print('%-8s |' % '', end='')
            for k in METHODS:
                print(' %14.0f%% کاذب       |' % fp[k], end='')
            print()
            print('-' * 76)
        print()
