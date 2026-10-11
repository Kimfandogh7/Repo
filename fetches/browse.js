const { chromium } = require('playwright');
const RUN_ID = '1791686671';
(async () => {
  const out = ['RUN_ID: ' + RUN_ID];
  const browser = await chromium.launch({ args:['--no-sandbox','--disable-dev-shm-usage'] });
  const ctx = await browser.newContext({ userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' });
  const page = await ctx.newPage();
  // ۱) همه‌ی لینک‌های صفحه اصلی
  await page.goto('https://www.biodigital.com', {waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForTimeout(3000);
  const all = await page.evaluate(() => Array.from(document.querySelectorAll('a')).map(a => a.getAttribute('href')).filter(Boolean));
  out.push('--- ALL LINKS (unique) ---');
  out.push([...new Set(all)].slice(0,40).join('\n'));
  // ۲) تلاش برای یافتن صفحه ثبت‌نام
  for (const cand of ['https://www.biodigital.com/human/signup','https://human.biodigital.com/signup','https://www.biodigital.com/sign-up']) {
    try {
      const r = await page.goto(cand, {waitUntil:'domcontentloaded',timeout:30000});
      out.push('--- TRY ' + cand + ' -> ' + (r && r.status()) + ' | final: ' + page.url());
      await page.waitForTimeout(2500);
      const inputs = await page.evaluate(() => Array.from(document.querySelectorAll('input')).map(i =>
        [i.type, i.name, i.id, i.placeholder].filter(Boolean).join('|')));
      const btns = await page.evaluate(() => Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean));
      out.push('  INPUTS: ' + JSON.stringify(inputs.slice(0,12)));
      out.push('  BUTTONS: ' + JSON.stringify(btns.slice(0,10)));
      if (inputs.length) break;
    } catch(e){ out.push('--- TRY ' + cand + ' -> ERR ' + e.message.slice(0,120)); }
  }
  await browser.close();
  console.log(out.join('\n'));
})().catch(e => console.log('RUN_ID: '+RUN_ID+'\nFATAL: ' + e.message.slice(0,400)));
