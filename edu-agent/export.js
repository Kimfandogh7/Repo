// export.js — دک را با مرورگر واقعی رندر می‌کند و از هر صفحه PNG می‌گیرد.
// در GitHub Actions اجرا می‌شود (جایی که مرورگر واقعاً کار می‌کند).
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.env.BASE || 'http://127.0.0.1:4173';
const SLIDE = process.env.SLIDE || 'forgetting-curve';
const OUT = path.join(__dirname, 'out');
const PAGES = Number(process.env.PAGES || 6);
const RUN_ID = process.env.RUN_ID || '1791689749';

fs.mkdirSync(OUT, { recursive: true });
const log = (...a) => console.log(...a);
log('RUN_ID: ' + RUN_ID);

// نامزدهای احتمالی برای خودِ بومِ اسلاید (۱۹۲۰×۱۰۸۰)
const CANDIDATES = [
  '[data-slide-canvas]',
  '[data-canvas]',
  '.osd-canvas',
  '[class*="canvas" i]',
  '[class*="stage" i]',
  '[class*="slide-frame" i]',
  'main',
];

(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });

  const url = `${BASE}/slides/${SLIDE}`;
  log('goto: ' + url);
  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(4000);

  // کدام انتخابگر بومِ واقعی است؟
  let sel = null;
  for (const c of CANDIDATES) {
    try {
      const box = await page.locator(c).first().boundingBox().catch(() => null);
      if (box && box.width > 900 && box.height > 500) {
        log(`canvas candidate ${c} -> ${Math.round(box.width)}x${Math.round(box.height)}`);
        if (!sel) sel = c;
      }
    } catch { /* ignore */ }
  }
  if (!sel) {
    // آخرین راه: کل صفحه
    log('no canvas found; falling back to full page');
    sel = 'body';
  }
  log('USING: ' + sel);

  const target = page.locator(sel).first();

  for (let i = 0; i < PAGES; i++) {
    await page.waitForTimeout(i === 0 ? 2500 : 1400);
    const f = path.join(OUT, `page-${String(i + 1).padStart(2, '0')}.png`);
    await target.screenshot({ path: f }).catch(async (e) => {
      log(`  page ${i + 1} canvas shot failed: ${e.message.slice(0, 80)}`);
      await page.screenshot({ path: f });
    });
    const sz = fs.statSync(f).size;
    log(`  page-${i + 1}.png  ${sz} bytes`);
    if (i < PAGES - 1) {
      await page.keyboard.press('ArrowRight');
    }
  }

  await browser.close();
  log('DONE');
})().catch((e) => {
  console.log('FATAL: ' + e.message);
  process.exit(1);
});
