# -*- coding: utf-8 -*-
"""اتصالِ واقعی: تشخیص → کارت.

موتورِ تشخیص می‌گوید کدام مفهوم ضعیف است؛ اینجا همان‌ها را به دک تبدیل می‌کنیم.
این همان حلقه‌ای است که می‌خواهیم: اندازه‌گیری → یافتنِ نقطه‌ضعف → تمرینِ همان.
"""
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EDU = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(EDU, 'diagnose'))
sys.path.insert(0, HERE)

import engine as E           # موتورِ تشخیص (diagnose/engine.py)
import build_deck


def diagnose_and_build(theta_true=0.5, weak='chain_rule', seed=7, min_evidence=2):
    """یک دانش‌آموزِ شبیه‌سازی‌شده را تشخیص می‌دهد و برای نقاط‌ضعفش دک می‌سازد."""
    bank = E.load_bank(os.path.join(EDU, 'diagnose', 'bank-calculus.json'))
    rng = random.Random(seed)

    def answer(q):
        drop = 1.8 if weak in q.concepts else 0.0
        return rng.random() < E.p_correct(theta_true - drop, q.b)

    sess = E.Session(bank)
    while not sess.done:
        q = sess.pick()
        if q is None:
            break
        sess.record(q.id, answer(q))
    for q in sess.sweep_targets(top_n=5):
        sess.record(q.id, answer(q))

    rep = sess.report()
    print("تشخیص:")
    print("  توانایی برآوردشده: %s  |  %d سؤال  |  %d پاسخِ درست"
          % (rep['theta'], rep['questions_asked'], rep['correct']))
    print("  مفهومِ ضعیفِ واقعی (در شبیه‌سازی): %s" % weak)
    print("  رتبه‌بندیِ موتور:")
    for i, d in enumerate(rep['weak_first'][:5], 1):
        print("    %d. %-18s شکاف=%+.2f  (%d/%d)  %s"
              % (i, d['concept'], d['gap'], d['correct'], d['asked'], d['status']))

    # مفاهیمی که موتور ضعیف دانسته
    targets = [d['concept'] for d in rep['weak_first'][:3]]
    if weak not in targets:
        targets.append(weak)          # برای مقایسه: مفهومِ واقعاً ضعیف را هم می‌سازیم
        note = "  ⚠ موتور مفهومِ واقعاً ضعیف را در رتبه‌های اول نیاورد"
    else:
        note = "  ✓ موتور مفهومِ واقعاً ضعیف را درست تشخیص داد"
    print(note)

    # موتور اشیاءِ Question برمی‌گرداند؛ کارت‌ساز دیکشنری می‌خواهد
    items = list(bank.values()) if isinstance(bank, dict) else bank
    bank_list = []
    for q in items:
        if isinstance(q, dict):
            bank_list.append(q)
        else:
            bank_list.append({
                'id': q.id,
                'text': q.text,
                'b': q.b,
                'concepts': list(q.concepts),
                'options': list(q.options),
                'answer': q.answer,
                'explanation': getattr(q, 'explanation', '') or '',
            })
    path, n = build_deck.build(targets, bank_list,
                               title='مرورِ هدفمند — ' + weak,
                               out_path=os.path.join(HERE, 'out', 'از-تشخیص.apkg'))
    print()
    print("دک ساخته شد: %s (%d کارت)" % (os.path.basename(path), n))
    print("مفاهیمِ هدف:", '، '.join(targets))
    return path, targets


if __name__ == '__main__':
    diagnose_and_build()
