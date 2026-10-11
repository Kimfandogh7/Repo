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
    console.log(`beat ${n} @${t}s -> ${path.basename(f)} ${sz}b`);
  }

  if (errors.length) console.log('ERRORS:\n' + errors.slice(0, 20).join('\n'));
  else console.log('no page errors');
  await browser.close();
  console.log(`RUN_ID=${RUN_ID} DONE`);
})();
