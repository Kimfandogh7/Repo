const { chromium } = require('playwright');
const RUN_ID = '1791686567';
(async () => {
  const out = ['RUN_ID: ' + RUN_ID];
  out.push('NODE: ' + process.version);
  let browser;
  try {
    browser = await chromium.launch({ args: ['--no-sandbox','--disable-dev-shm-usage'] });
    out.push('BROWSER: launched ok');
  } catch (e) { out.push('LAUNCH_FAILED: ' + e.message.slice(0,300)); console.log(out.join('\n')); return; }
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36'
  });
  const page = await ctx.newPage();
  try {
    const r = await page.goto('https://www.biodigital.com', { waitUntil:'domcontentloaded', timeout:60000 });
    out.push('STATUS: ' + (r && r.status()));
    out.push('TITLE: ' + await page.title());
    await page.waitForTimeout(5000);
    const txt = await page.evaluate(() => document.body.innerText) || '';
    out.push('--- TEXT (2000) ---');
    out.push(txt.replace(/\n{2,}/g,'\n').slice(0,2000));
    const links = await page.evaluate(() => Array.from(document.querySelectorAll('a'))
      .map(a=>a.href).filter(h=>/sign|login|regist|account|join|pricing|human/i.test(h)));
    out.push('--- AUTH LINKS ---');
    out.push([...new Set(links)].slice(0,20).join('\n'));
  } catch (e) { out.push('NAV_ERROR: ' + e.message.slice(0,300)); }
  await browser.close();
  console.log(out.join('\n'));
})().catch(e => console.log('RUN_ID: '+RUN_ID+'\nFATAL: ' + e.message.slice(0,400)));
