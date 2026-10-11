# -*- coding: utf-8 -*-
"""ساختِ دکِ Anki از خروجیِ موتورِ تشخیص.

ایده: تشخیص می‌گوید کدام مفهوم ضعیف است؛ اینجا برای همان مفهوم کارت می‌سازیم،
نه برای همه‌چیز. خروجی یک فایلِ .apkg است که مستقیماً در Anki باز می‌شود.

دو نکته‌یِ طراحی که در کارت‌سازی مهم‌اند و رعایتشان کرده‌ام:
  ۱. کمینه‌سازیِ اطلاعات: هر کارت یک واقعیت را می‌پرسد، نه چند تا را با هم.
  ۲. راست‌به‌چپِ واقعی: قالبِ کارت dir="rtl" دارد، وگرنه فارسی در Anki
     با نشانه‌گذاریِ غلط (نقطه و پرانتز در جایِ اشتباه) دیده می‌شود.
"""
import json
import os
import random
import sys

import genanki

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)   # edu-agent/

# ── قالبِ کارتِ فارسی (RTL) ──────────────────────────────────────────────
CSS = """
.card {
  font-family: "Vazirmatn", "Noto Naskh Arabic", "Tahoma", sans-serif;
  font-size: 30px; line-height: 1.75;
  color: #eceff1; background: #1b2421;
  direction: rtl; text-align: right;
  padding: 26px 30px;
}
.math { font-family: "STIX Two Text", "Cambria Math", Georgia, serif;
        direction: ltr; unicode-bidi: isolate; display: inline-block; }
.tag  { font-size: 17px; color: #8ba39b; margin-bottom: 14px; }
.hr   { border: 0; border-top: 2px solid #37473f; margin: 22px 0; }
.ans  { color: #f0b45a; font-weight: 600; }
.why  { font-size: 21px; color: #9fb3aa; margin-top: 16px; line-height: 1.6; }
.card:has(.why) .why:empty { display: none; }
"""

PERSIAN_MODEL = genanki.Model(
    1731000001,
    'فارسی — پرسش/پاسخ',
    fields=[{'name': 'پرسش'}, {'name': 'پاسخ'}, {'name': 'مفهوم'}, {'name': 'توضیح'}],
    templates=[{
        'name': 'رو به رو',
        'qfmt': '<div class="card"><div class="tag">{{مفهوم}}</div>{{پرسش}}</div>',
        'afmt': ('<div class="card"><div class="tag">{{مفهوم}}</div>{{پرسش}}'
                 '<hr class="hr"><span class="ans">{{پاسخ}}</span>'
                 '<div class="why">{{توضیح}}</div></div>'),
    }],
    css=CSS,
)


# ── کارت‌سازی ────────────────────────────────────────────────────────────
def cards_for_concept(concept, bank, limit=6):
    """برای یک مفهوم، کارت‌های «کمینه‌اطلاعات» می‌سازد."""
    qs = [q for q in bank if concept in q.get('concepts', [])]
    out = []
    for q in qs[:limit]:
        # هر کارت فقط یک چیز می‌پرسد: خودِ سؤال، بدونِ گزینه‌های انحرافی
        out.append({
            'q': q['text'],
            'a': q['options'][q['answer']],
            'concept': concept,
            'why': q.get('explanation', ''),
        })
    return out


def build(concepts, bank, title='مرورِ هدفمند', out_path=None):
    deck = genanki.Deck(1731000002 + abs(hash(title)) % 1000000, title)
    n = 0
    for c in concepts:
        for card in cards_for_concept(c, bank):
            deck.add_note(genanki.Note(
                model=PERSIAN_MODEL,
                fields=[card['q'], card['a'], card['concept'], card.get('why', '')],
                tags=[c],
            ))
            n += 1
    out_path = out_path or os.path.join(HERE, 'out', 'مرور-هدفمند.apkg')
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    genanki.Package(deck).write_to_file(out_path)
    return out_path, n


def main():
    bank_path = os.path.join(ROOT, 'diagnose', 'bank-calculus.json')
    bank = json.load(open(bank_path, encoding='utf-8'))
    if isinstance(bank, dict):
        bank = list(bank.values())

    # مفاهیم یا از آرگومان می‌آیند یا همان‌هایی که تشخیص ضعیف دانسته
    concepts = sys.argv[1:] or ['chain_rule', 'product_rule', 'quotient_rule']
    path, n = build(concepts, bank)
    print("دک ساخته شد: %s" % path)
    print("تعداد کارت‌ها: %d  |  مفاهیم: %s" % (n, '، '.join(concepts)))
    print("حجم: %d بایت" % os.path.getsize(path))


if __name__ == '__main__':
    main()
