// رندرِ کتابِ فارسی: از هر بیت یک عکس می‌گیرد (برای بازبینیِ چیدمان و فونت)
// روی Actions اجرا می‌شود چون به اینترنت (edge-tts) و مرورگر نیاز دارد.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const RUN_ID = process.env.RUN_ID || String(Date.now());
const BASE = process.env.BASE || 'http://127.0.0.1:8765';
const BOOK = process.env.BOOK || 'moshkel';
const CH = process.env.CH || 'ch01';
const URL = `${BASE}/${BOOK}/${CH}/`;
const OUT = path.join(__dirname, 'out', 'book', BOOK, CH);

// [شماره‌ی بیت، زمانِ فریزشده بر حسب ثانیه]
const SHOTS = [
  [0, 3.0],   // intro
  [1, 4.0],   // idea
  [2, 4.0],   // wrong
  [3, 6.0],   // why
  [4, 6.0],   // rule
  [5, 8.0],   // example
  [6, 0.5],   // q1 (تمرین)
  [7, 5.0],   // wrap
];

(async () => {
  console.log(`RUN_ID=${RUN_ID}  ${URL}`);
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });

  const errors = [];
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push('CONSOLE: ' + m.text()); });

  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1500);

  // وضعیتِ موتور را گزارش می‌کنیم تا بدانیم RTL فعال شده یا نه
  const diag = await page.evaluate(() => ({
    dir: document.documentElement.getAttribute('dir'),
    lang: document.documentElement.getAttribute('lang'),
    hasTimings: typeof window.TIMINGS === 'object' && !!window.TIMINGS,
    beats: (typeof window.TIMINGS === 'object' && window.TIMINGS) ? Object.keys(window.TIMINGS).length : 0,
    rtl: typeof RTL !== 'undefined' ? RTL : 'undef',
    svgTexts: document.querySelectorAll('#scene text').length,
    sample: [...document.querySelectorAll('#scene text')].slice(0, 4).map(t => t.textContent),
  }));
  console.log('DIAG ' + JSON.stringify(diag));

  for (const [n, t] of SHOTS) {
    const u = `${URL}?beat=${n}&t=${t}`;
    await page.goto(u, { waitUntil: 'networkidle' });
    await page.waitForTimeout(1200);
    const f = path.join(OUT, `beat-${String(n).padStart(2, '0')}.png`);
    await page.screenshot({ path: f });
    const sz = fs.statSync(f).size;

    // تأییدِ برنامه‌ای: چون عکس‌ها را نمی‌بینم، متن را اندازه می‌گیرم.
    // ۱) آیا فارسی واقعاً شکل‌دهی شده یا شده جعبه (tofu)؟
    //    فارسیِ واقعی پهنایِ متنوع دارد؛ tofu همه هم‌عرض‌اند.
    // ۲) آیا متن از کادرِ ۱۶۰۰×۹۰۰ بیرون زده؟
    const audit = await page.evaluate(() => {
      const els = [...document.querySelectorAll('#scene text')];
      const out = [];
      let offscreen = 0, tofuish = 0;
      // مختصاتِ واقعیِ صفحه، نه دستگاهِ محلیِ g/هایِ تو‌در‌تو
      const stage = document.querySelector('svg') || document.body;
      const R = stage.getBoundingClientRect();
      const sx = 1600 / (R.width || 1600), sy = 900 / (R.height || 900);
      for (const e of els) {
        const txt = (e.textContent || '').trim();
        if (!txt) continue;
        // کدریِ مؤثر: متنی از بیت‌های قبل که panel() محو کرده، نباید شمرده شود
        let op = 1, n = e;
        while (n && n !== document.body) {
          const o = getComputedStyle(n).opacity;
          if (o !== '') op *= parseFloat(o);
          if (n.getAttribute && n.getAttribute('display') === 'none') { op = 0; break; }
          n = n.parentElement;
        }
        if (op < 0.05) continue;                           // عملاً نامرئی
        const r = e.getBoundingClientRect();
        if (!r.width && !r.height) continue;               // پنهان یا سایز صفر
        const fa = /[\u0600-\u06FF]/.test(txt);
        // به مختصاتِ ۱۶۰۰×۹۰۰ برمی‌گردانیم
        const bb = { x: (r.left - R.left) * sx, y: (r.top - R.top) * sy,
                     width: r.width * sx, height: r.height * sy };
        const per = txt.length ? bb.width / txt.length : 0;
        const outside = bb.x < -5 || bb.y < -5 || bb.x + bb.width > 1605 || bb.y + bb.height > 905;
        if (outside) offscreen++;
        if (fa) {
          // فارسیِ واقعی: نسبتِ پهنا به اندازه‌ی قلم باید در بازه‌ی معقول باشد
          const fs = parseFloat(getComputedStyle(e).fontSize) || 30;
          const ratio = per / (fs * 0.55);
          if (ratio < 0.15 || ratio > 1.6) tofuish++;
        }
        out.push({ t: txt.slice(0, 28), fa, x: Math.round(bb.x), y: Math.round(bb.y),
                   w: Math.round(bb.width), outside });
      }
      return { n: els.length, offscreen, tofuish, items: out.slice(0, 12) };
    });
    console.log(`beat ${n} @${t}s -> ${path.basename(f)} ${sz}b  text=${audit.n} بیرون‌زده=${audit.offscreen} مشکوک‌به‌توفو=${audit.tofuish}`);
    for (const it of audit.items) {
      console.log(`   [${it.fa ? 'فا' : 'لا'}] x=${String(it.x).padStart(4)} y=${String(it.y).padStart(3)} w=${String(it.w).padStart(4)}${it.outside ? '  ⚠ بیرون از کادر' : ''}  «${it.t}»`);
    }
  }

  if (errors.length) console.log('ERRORS:\n' + errors.slice(0, 20).join('\n'));
  else console.log('no page errors');
  await browser.close();
  console.log(`RUN_ID=${RUN_ID} DONE`);
})();
