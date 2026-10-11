const { chromium } = require('playwright');
const RUN_ID = '1791686830';
(async () => {
  const out = ['RUN_ID: ' + RUN_ID];
  const browser = await chromium.launch({ args:['--no-sandbox','--disable-dev-shm-usage'] });
  const ctx = await browser.newContext({ userAgent:'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36' });
  const page = await ctx.newPage();
  await page.goto('https://human.biodigital.com/login/create', {waitUntil:'domcontentloaded',timeout:60000});
  await page.waitForTimeout(8000);
  out.push('--- recaptcha elements in DOM ---');
  out.push(await page.evaluate(() => {
    const els = document.querySelectorAll('.g-recaptcha, [data-sitekey], iframe[src*="recaptcha"]');
    return Array.from(els).map(e => e.tagName + '.' + e.className + ' sitekey=' + (e.getAttribute('data-sitekey')||'') + ' src=' + (e.src||'').slice(0,90)).join('\n') || 'NONE RENDERED';
  }));
  out.push('--- all iframes ---');
  out.push(await page.evaluate(() => Array.from(document.querySelectorAll('iframe')).map(f=>(f.src||'').slice(0,100)).join('\n') || 'none'));
  out.push('--- scripts mentioning recaptcha ---');
  out.push(await page.evaluate(() => Array.from(document.querySelectorAll('script')).map(s=>s.src||'(inline)')
     .filter(s=>/recaptcha|google/i.test(s)).join('\n') || 'none'));
  out.push('--- is a captcha VISIBLE on screen? ---');
  out.push(await page.evaluate(() => {
    const c = document.querySelector('.g-recaptcha');
    if (!c) return 'no .g-recaptcha element';
    const b = c.getBoundingClientRect();
    return 'exists, size=' + Math.round(b.width) + 'x' + Math.round(b.height) + ' visible=' + (b.width>0 && b.height>0);
  }));
  out.push('--- google sign-in button present? ---');
  out.push(await page.evaluate(() => {
    const b = Array.from(document.querySelectorAll('button,div,a')).find(e=>/Sign in with Google/i.test(e.innerText||''));
    return b ? 'YES: ' + b.tagName : 'no';
  }));
  await browser.close();
  console.log(out.join('\n'));
})().catch(e => console.log('RUN_ID: '+RUN_ID+'\nFATAL: ' + e.message.slice(0,400)));
