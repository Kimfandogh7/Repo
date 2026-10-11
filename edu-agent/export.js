// export.js — دک را با مرورگر واقعی رندر می‌کند و از هر صفحه PNG می‌گیرد.
// مسیر درست: /s/<slide-id>  (نه /slides/... که ۴۰۴ می‌دهد)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE || 'http://127.0.0.1:4173';
const SLIDE = process.env.SLIDE || 'forgetting-curve';
const OUT = path.join(__dirname, 'out');
const PAGES = Number(process.env.PAGES || 6);
const RUN_ID = process.env.RUN_ID || '1791690499';
fs.mkdirSync(OUT, { recursive: true });
const log = (...a) => console.log(...a);
log('RUN_ID: ' + RUN_ID);

const CANDIDATES = [
  '[data-testid="slide-canvas"]',
  '[data-slide-canvas]',
  '[data-canvas]',
  '[class*="canvas" i]',
  '[class*="stage" i]',
  '[class*="slide-frame" i]',
  'section',
];

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', (e) => log('[pageerror] ' + e.message.slice(0, 160)));

  const url = `${BASE}/s/${SLIDE}`;
  log('goto: ' + url);
  const r = await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  log('status: ' + (r && r.status()));
  await page.waitForTimeout(6000);

  let sel = null;
  for (const c of CANDIDATES) {
    const box = await page.locator(c).first().boundingBox().catch(() => null);
    if (box && box.width > 700 && box.height > 400) {
      const ar = box.width / box.height;
      log(`  candidate ${c} -> ${Math.round(box.width)}x${Math.round(box.height)} ar=${ar.toFixed(2)}`);
      if (!sel && ar > 1.3 && ar < 2.1) sel = c;
    }
  }
  log('USING: ' + (sel || 'full page (fallback)'));
  const target = sel ? page.locator(sel).first() : page;

  for (let i = 0; i < PAGES; i++) {
    await page.waitForTimeout(i === 0 ? 3000 : 1600);
    const f = path.join(OUT, `page-${String(i + 1).padStart(2, '0')}.png`);
    await target.screenshot({ path: f }).catch(async (e) => {
      log(`  p${i + 1} canvas failed (${e.message.slice(0, 60)}); full page`);
      await page.screenshot({ path: f });
    });
    log(`  page-${i + 1}.png  ${fs.statSync(f).size} bytes`);
    if (i < PAGES - 1) await page.keyboard.press('ArrowRight');
  }

  await browser.close();
  log('DONE');
})().catch((e) => { console.log('FATAL: ' + e.message); process.exit(1); });
