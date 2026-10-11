# -*- coding: utf-8 -*-
"""گرافِ پیش‌نیازهای مفاهیمِ حساب دیفرانسیل.

جهتِ یال: پیش‌نیاز  →  مفهومِ وابسته
مثلاً power_rule → chain_rule یعنی «برای زنجیره‌ای باید قانونِ توان را بلد باشی».

چرا این گراف لازم است: موتورِ تشخیص می‌گوید کدام مفهوم ضعیف است، اما ضعفِ یک
مفهومِ پیشرفته معمولاً **علامت** است نه علت. کسی که در زنجیره‌ای ضعیف است
اغلب در واقع قانونِ توان را بلد نیست. درمانِ علامت وقت تلف کردن است.

احتیاط: این گراف بر اساسِ دانشِ استانداردِ ریاضیِ دوره‌یِ اولِ دانشگاهی نوشته
شده، نه استخراج از داده. اگر روزی داده‌یِ واقعی داشتیم باید با آن سنجیده شود.
"""

PREREQS = {
    # پایه‌ها — پیش‌نیاز ندارند
    'concept_meaning':    [],
    'concept_constant':   [],
    'power_rule':         [],
    'trig_derivative':    [],

    # یک لایه بالاتر
    'negative_exponent':  ['power_rule'],
    'exp_derivative':     ['power_rule'],
    'log_derivative':     ['power_rule'],
    'product_rule':       ['power_rule'],
    'radical':            ['power_rule', 'negative_exponent'],

    # دو لایه
    'quotient_rule':      ['product_rule', 'negative_exponent'],
    'chain_rule':         ['power_rule'],
    'expansion':          ['power_rule'],

    # سه لایه و بالاتر
    'second_derivative':  ['power_rule', 'product_rule'],
    'implicit_diff':      ['chain_rule', 'product_rule'],
    'concept_notation':   ['chain_rule'],
    'applications':       ['concept_meaning', 'second_derivative'],
    'physics_link':       ['applications', 'second_derivative'],
}

NAMES_FA = {
    'concept_meaning':    'معنایِ مشتق',
    'concept_constant':   'مشتقِ ثابت',
    'power_rule':         'قانونِ توان',
    'trig_derivative':    'مشتقِ مثلثاتی',
    'negative_exponent':  'توانِ منفی',
    'exp_derivative':     'مشتقِ نمایی',
    'log_derivative':     'مشتقِ لگاریتمی',
    'product_rule':       'قانونِ ضرب',
    'radical':            'ریشه‌ها',
    'quotient_rule':      'قانونِ خارج‌قسمت',
    'chain_rule':         'قاعده‌ی زنجیره‌ای',
    'expansion':          'بسط دادن',
    'second_derivative':  'مشتقِ دوم',
    'implicit_diff':      'مشتقِ ضمنی',
    'concept_notation':   'نمادگذاری',
    'applications':       'کاربردها',
    'physics_link':       'پیوند با فیزیک',
}


def prereqs(c):
    return PREREQS.get(c, [])


def ancestors(c, _seen=None):
    """همه‌ی اجدادِ یک مفهوم (پیش‌نیازهایِ مستقیم و غیرمستقیم)."""
    _seen = _seen if _seen is not None else set()
    for p in prereqs(c):
        if p not in _seen:
            _seen.add(p)
            ancestors(p, _seen)
    return _seen


def depth(c):
    """دورترین فاصله تا یک پایه — یک معیارِ «چقدر پیشرفته»."""
    ps = prereqs(c)
    return 0 if not ps else 1 + max(depth(p) for p in ps)


def all_concepts():
    return sorted(PREREQS)


if __name__ == '__main__':
    print('%-20s %-8s %s' % ('مفهوم', 'عمق', 'پیش‌نیازها'))
    print('-' * 76)
    for c in sorted(all_concepts(), key=lambda x: (depth(x), x)):
        print('%-20s %-8d %s' % (c, depth(c), '، '.join(prereqs(c)) or '— (پایه)'))
    print('-' * 76)
    print('پایه‌ها (بدون پیش‌نیاز):',
          '، '.join(c for c in all_concepts() if not prereqs(c)))
