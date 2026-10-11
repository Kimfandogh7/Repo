// browse.js — اجرا در GitHub Actions با مرورگر واقعی
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });
  const page = await ctx.newPage();
  const out = [];
  page.on('console', m => out.push('[console] ' + m.text().slice(0,200)));
  const url = process.env.TARGET || 'https://www.biodigital.com';
  const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  out.push('STATUS: ' + (resp && resp.status()));
  out.push('URL: ' + page.url());
  out.push('TITLE: ' + await page.title());
  await page.waitForTimeout(4000);
  // محتوای واقعی بعد از اجرای JS
  const txt = (await page.evaluate(() => document.body.innerText)) || '';
  out.push('--- TEXT (first 2500) ---');
  out.push(txt.replace(/\n{2,}/g, '\n').slice(0, 2500));
  // لینک‌ها و فرم‌ها: نشانه‌های ثبت‌نام/ورود
  const links = await page.evaluate(() =>
    Array.from(document.querySelectorAll('a')).map(a => a.href)
      .filter(h => /sign|login|regist|account|join|pricing/i.test(h)).slice(0, 15));
  out.push('--- AUTH LINKS ---');
  out.push([...new Set(links)].join('\n'));
  const forms = await page.evaluate(() =>
    Array.from(document.querySelectorAll('form')).map(f => ({
      action: f.action, method: f.method,
      inputs: Array.from(f.querySelectorAll('input')).map(i => i.type + ':' + (i.name||''))
    })));
  out.push('--- FORMS ---');
  out.push(JSON.stringify(forms, null, 1).slice(0, 1200));
  await browser.close();
  console.log(out.join('\n'));
})().catch(e => { console.log('ERROR: ' + e.message); process.exit(1); });
// run 1791686526
