const { chromium } = require('playwright');
const RUN_ID = '1791686754';
(async () => {
  const out = ['RUN_ID: ' + RUN_ID];
  const browser = await chromium.launch({ args:['--no-sandbox','--disable-dev-shm-usage'] });
  const ctx = await browser.newContext({ userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' });
  const page = await ctx.newPage();
  const r = await page.goto('https://human.biodigital.com/login/create', {waitUntil:'domcontentloaded',timeout:60000});
  out.push('STATUS: ' + (r && r.status()) + ' | URL: ' + page.url());
  await page.waitForTimeout(6000);
  out.push('TITLE: ' + await page.title());
  out.push('--- INPUTS ---');
  const inputs = await page.evaluate(() => Array.from(document.querySelectorAll('input')).map(i =>
    JSON.stringify({type:i.type, name:i.name, id:i.id, ph:i.placeholder, req:i.required})));
  out.push(inputs.slice(0,20).join('\n'));
  out.push('--- BUTTONS ---');
  out.push((await page.evaluate(() => Array.from(document.querySelectorAll('button')).map(b=>b.innerText.trim()).filter(Boolean))).slice(0,12).join(' | '));
  out.push('--- CAPTCHA SIGNS ---');
  out.push(await page.evaluate(() => {
    const h = document.documentElement.innerHTML;
    return ['recaptcha','hcaptcha','turnstile','cf-challenge','g-recaptcha'].filter(k => h.toLowerCase().includes(k)).join(', ') || 'none found';
  }));
  out.push('--- VISIBLE TEXT (1200) ---');
  out.push(((await page.evaluate(() => document.body.innerText))||'').replace(/\n{2,}/g,'\n').slice(0,1200));
  await browser.close();
  console.log(out.join('\n'));
})().catch(e => console.log('RUN_ID: '+RUN_ID+'\nFATAL: ' + e.message.slice(0,400)));
