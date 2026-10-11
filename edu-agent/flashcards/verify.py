# -*- coding: utf-8 -*-
"""تأییدِ دکِ ساخته‌شده: .apkg را باز می‌کنیم و محتوا را می‌خوانیم.

چرا لازم است: ساخته‌شدنِ فایل به‌معنای درست‌بودنش نیست. اینجا چیزهایی را
چک می‌کنیم که واقعاً ممکن است خراب باشند — مخصوصاً جهتِ راست‌به‌چپ.
"""
import json
import os
import sqlite3
import sys
import zipfile


def verify(path):
    print("بررسی:", os.path.basename(path), "(%d بایت)" % os.path.getsize(path))
    ok = True

    z = zipfile.ZipFile(path)
    names = z.namelist()
    if 'collection.anki2' not in names:
        print("  ✗ collection.anki2 پیدا نشد")
        return False
    print("  ✓ ساختارِ apkg درست است:", names)

    tmp = '/tmp/verify-col.anki2'
    z.extract('collection.anki2', '/tmp/')
    if os.path.exists(tmp):
        os.remove(tmp)
    os.replace('/tmp/collection.anki2', tmp)
    con = sqlite3.connect(tmp)

    notes = con.execute('select flds, tags from notes').fetchall()
    cards = con.execute('select count(*) from cards').fetchone()[0]
    print("  ✓ تعداد note: %d | تعداد کارت: %d" % (len(notes), cards))
    if not notes:
        print("  ✗ هیچ کارتی نیست")
        return False

    # مدل و قالبِ کارت را از پیکربندی می‌خوانیم
    col = con.execute('select models from col').fetchone()[0]
    models = json.loads(col)
    tmpl = ''
    css = ''
    for m in models.values():
        for t in m.get('tmpls', []):
            tmpl += t.get('afmt', '') + t.get('qfmt', '')
        css += m.get('css', '')
    print("  %s قالبِ کارت دارای dir=\"rtl\"" %
          ('✓' if 'direction: rtl' in css or 'dir="rtl"' in css else '✗'))
    if 'direction: rtl' not in css:
        ok = False

    # نمونه‌ی کارت‌ها
    print()
    print("  نمونه‌ی کارت‌ها:")
    shown = 0
    for flds, tags in notes:
        parts = flds.split('\x1f')
        if len(parts) >= 2:
            print("    [%s] %s  →  %s" % (tags or '-', parts[0][:44], parts[1][:26]))
            shown += 1
        if shown >= 6:
            break

    # بررسی: کارتِ خالی یا ناقص؟
    bad = [f for f, _ in notes if len(f.split('\x1f')) < 2 or not f.split('\x1f')[1].strip()]
    print()
    print("  %s کارتِ ناقص (بدون پاسخ): %d" % ('✓' if not bad else '✗', len(bad)))
    if bad:
        ok = False

    # بررسی: متنِ فارسی واقعاً هست؟
    fa = sum(1 for f, _ in notes if any('\u0600' <= ch <= '\u06ff' for ch in f))
    print("  %s کارت‌های فارسی: %d از %d" %
          ('✓' if fa == len(notes) else '✗', fa, len(notes)))
    if fa != len(notes):
        ok = False

    return ok


if __name__ == '__main__':
    p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'out', 'مرور-هدفمند.apkg')
    r = verify(p)
    print()
    print("نتیجه:", "قبول ✓" if r else "مردود ✗")
    sys.exit(0 if r else 1)
