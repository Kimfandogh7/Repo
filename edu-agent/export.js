// export.js — حالتِ شناسایی: ساختار صفحه را می‌گردد تا بومِ واقعی را پیدا کند
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE || 'http://127.0.0.1:4173';
const SLIDE = process.env.SLIDE || 'forgetting-curve';
const OUT = path.join(__dirname, 'out');
const RUN_ID = process.env.RUN_ID || '1791690065';
fs.mkdirSync(OUT, { recursive: true });
const log = (...a) => console.log(...a);
log('RUN_ID: ' + RUN_ID);

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  page.on('console', (m) => { if (m.type() === 'error') log('[console] ' + m.text().slice(0, 160)); });
  page.on('pageerror', (e) => log('[pageerror] ' + e.message.slice(0, 200)));

  // ۱) صفحه اصلی: چه دک‌هایی هست و مسیرها چیست؟
  await page.goto(BASE + '/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000);
  log('HOME url: ' + page.url());
  log('HOME title: ' + (await page.title()));
  log('--- HOME links ---');
  log((await page.evaluate(() => Array.from(document.querySelectorAll('a')).map((a) => a.getAttribute('href')).filter(Boolean))).slice(0, 25).join('\n'));
  log('--- HOME text (800) ---');
  log(((await page.evaluate(() => document.body.innerText)) || '').slice(0, 800));

  // ۲) صفحه‌ی اسلاید
  const url = `${BASE}/slides/${SLIDE}`;
  log('--- goto: ' + url);
  const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  log('status: ' + (resp && resp.status()) + ' | url: ' + page.url());
  await page.waitForTimeout(6000);
  log('--- SLIDE text (1200) ---');
  log(((await page.evaluate(() => document.body.innerText)) || '').slice(0, 1200));

  // ۳) همه عناصرِ بزرگ — بوم کدام است؟
  log('--- BIG ELEMENTS ---');
  log(await page.evaluate(() => {
    const out = [];
    document.querySelectorAll('*').forEach((el) => {
      const r = el.getBoundingClientRect();
      if (r.width > 700 && r.height > 400) {
        out.push(
          `${el.tagName}.${(el.className && el.className.toString ? el.className.toString() : '').slice(0, 40)} ` +
          `[${Math.round(r.width)}x${Math.round(r.height)}]` +
          (el.getAttribute('data-testid') ? ' testid=' + el.getAttribute('data-testid') : '') +
          (el.getAttribute('data-slide') ? ' data-slide=' + el.getAttribute('data-slide') : '')
        );
      }
    });
    return out.slice(0, 25).join('\n') || 'none';
  }));

  await page.screenshot({ path: path.join(OUT, 'debug-slide.png') });
  log('debug screenshot written');
  await browser.close();
  log('DONE');
})().catch((e) => { console.log('FATAL: ' + e.message); process.exit(1); });
