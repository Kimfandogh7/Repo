# -*- coding: utf-8 -*-
"""برچسب‌زدنِ گزینه‌های انحرافی با «نوعِ خطا».

چرا لازم است: بدونِ دانستنِ اینکه هر گزینه‌ی غلط چرا غلط است، فقط می‌توانیم
بگوییم دانش‌آموز «غلط زده» — نه اینکه «چه اشتباهی می‌کند». الگو در اشتباه
است که قابل‌درمان است، نه در نمره.

طبقه‌بندی (ده نوع، بر اساسِ خطاهای واقعیِ حسابِ دیفرانسیل):
  forgot_chain    ضرب‌نکردن در مشتقِ لایه‌ی درونی
  forgot_product  فقط یکی از دو عامل را مشتق گرفتن (ضرب را مثل تک‌تابع دیدن)
  power_error     اشتباه در قانونِ توان (ضریب / کاهشِ توان)
  sign_error      افتادن یا اضافه‌شدنِ منفی
  const_error     اشتباه درباره‌یِ ثابت‌ها
  confused_rule   انتخابِ قانونِ اشتباه
  trig_mixup      قاطی‌کردنِ مشتق‌های مثلثاتی
  exp_log_mixup   قاطی‌کردنِ قوانینِ نمایی و لگاریتمی
  partial_work    روش درست بوده ولی نیمه‌کاره رها شده
  concept_error   کج‌فهمیِ معنایِ مشتق
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BANK = os.path.join(os.path.dirname(HERE), 'diagnose', 'bank-calculus.json')

# شناسه‌ی سؤال -> {اندیسِ گزینه: نوعِ خطا}
TAGS = {
    'd01': {1: 'power_error',   2: 'power_error',   3: 'power_error'},
    'd02': {1: 'power_error',   2: 'power_error',   3: 'power_error'},
    'd03': {1: 'const_error',   2: 'const_error',   3: 'const_error'},
    'd04': {1: 'sign_error',    2: 'power_error',   3: 'power_error'},
    'd05': {1: 'power_error',   2: 'power_error',   3: 'power_error'},

    'p01': {1: 'forgot_product', 2: 'forgot_product', 3: 'forgot_product'},
    'p02': {1: 'forgot_product', 2: 'forgot_product', 3: 'forgot_product'},
    'p03': {1: 'partial_work',   2: 'power_error',    3: 'power_error'},

    'q01': {1: 'confused_rule',  2: 'confused_rule',  3: 'confused_rule'},
    'q02': {1: 'sign_error',     2: 'power_error',    3: 'power_error'},
    'q03': {1: 'concept_error',  2: 'concept_error',  3: 'concept_error'},

    'c01': {1: 'forgot_chain',   2: 'sign_error',     3: 'trig_mixup'},
    'c02': {1: 'forgot_chain',   2: 'partial_work',   3: 'power_error'},
    'c03': {1: 'forgot_chain',   2: 'partial_work',   3: 'exp_log_mixup'},
    'c04': {1: 'forgot_chain',   2: 'partial_work',   3: 'exp_log_mixup'},
    'c05': {1: 'forgot_chain',   2: 'power_error',    3: 'partial_work'},
    'c06': {1: 'forgot_chain',   2: 'confused_rule',  3: 'confused_rule'},

    't01': {1: 'sign_error',     2: 'trig_mixup',     3: 'trig_mixup'},
    't02': {1: 'trig_mixup',     2: 'trig_mixup',     3: 'trig_mixup'},

    'e01': {1: 'power_error',    2: 'power_error',    3: 'exp_log_mixup'},
    'l01': {1: 'exp_log_mixup',  2: 'exp_log_mixup',  3: 'exp_log_mixup'},

    'a01': {1: 'concept_error',  2: 'concept_error',  3: 'concept_error'},
    'a02': {1: 'concept_error',  2: 'concept_error',  3: 'concept_error'},
    'a03': {1: 'concept_error',  2: 'concept_error',  3: 'concept_error'},
    'a04': {1: 'concept_error',  2: 'concept_error',  3: 'concept_error'},

    'm01': {1: 'partial_work',   2: 'power_error',    3: 'power_error'},
    'm02': {1: 'sign_error',     2: 'confused_rule',  3: 'partial_work'},
    'm03': {1: 'exp_log_mixup',  2: 'power_error',    3: 'partial_work'},
}

LABELS_FA = {
    'forgot_chain':   'مشتقِ لایه‌ی درونی را فراموش می‌کند',
    'forgot_product': 'در ضرب، فقط یکی از دو عامل را مشتق می‌گیرد',
    'power_error':    'اشتباه در قانونِ توان',
    'sign_error':     'اشتباهِ علامت (منفی)',
    'const_error':    'اشتباه درباره‌یِ ثابت‌ها',
    'confused_rule':  'قانونِ اشتباه را انتخاب می‌کند',
    'trig_mixup':     'قاطی‌کردنِ مشتق‌های مثلثاتی',
    'exp_log_mixup':  'قاطی‌کردنِ قوانینِ نمایی و لگاریتمی',
    'partial_work':   'روش درست است ولی نیمه‌کاره رها می‌شود',
    'concept_error':  'کج‌فهمی در معنایِ مشتق',
}


def main():
    bank = json.load(open(BANK, encoding='utf-8'))
    missing, n_tagged = [], 0
    for q in bank:
        t = TAGS.get(q['id'])
        if not t:
            missing.append(q['id'])
            continue
        # بررسیِ سازگاری: نباید به گزینه‌یِ درست برچسب زده شود
        for i in t:
            if i == q['answer']:
                raise SystemExit('خطا: %s گزینه‌ی %d پاسخِ درست است' % (q['id'], i))
        q['distractor_tags'] = {str(k): v for k, v in t.items()}
        n_tagged += 1

    if missing:
        print('هشدار: این سؤال‌ها برچسب نگرفتند:', missing)
    json.dump(bank, open(BANK, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('برچسب‌گذاری شد: %d سؤال' % n_tagged)

    # پراکندگیِ انواعِ خطا در بانک — برای مقایسه‌یِ پایه لازم است
    from collections import Counter
    c = Counter()
    for q in bank:
        for v in (q.get('distractor_tags') or {}).values():
            c[v] += 1
    tot = sum(c.values())
    print('\nفراوانیِ هر نوع خطا در بانک (این همان «نرخِ پایه» است):')
    for k, v in c.most_common():
        print('  %-16s %3d  (%4.1f%%)' % (k, v, 100.0 * v / tot))


if __name__ == '__main__':
    main()
