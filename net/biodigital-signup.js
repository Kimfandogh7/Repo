#!/usr/bin/env node
/**
 * biodigital-signup.js — ساخت حساب در BioDigital Human و ذخیره‌ی نشست.
 *
 * روی سیستم خودت اجرا کن (نه در سندباکس):
 *   npm i playwright && npx playwright install chromium
 *   node biodigital-signup.js
 *
 * چرا روی سیستم خودت: IP دیتاسنتر کپچا را قطعی می‌کند؛ IP خانگی معمولاً نه.
 * اگر کپچا بیاید، اسکریپت صبر می‌کند تا خودت حلش کنی و بعد ادامه می‌دهد.
 *
 * تنظیمات از محیط (یا اینجا):
 *   BD_FIRST_NAME, BD_LAST_NAME, BD_EMAIL, BD_PASSWORD
 */
const { chromium } = require('playwright');
const path = require('path');

const SESSION = path.join(__dirname, 'biodigital-session.json');
const SHOT    = path.join(__dirname, 'biodigital-state.png');
const SIGNUP  = 'https://human.biodigital.com/login/create';
const APP     = 'https://human.biodigital.com/';

const cfg = {
  firstName: process.env.BD_FIRST_NAME || '',
  lastName:  process.env.BD_LAST_NAME  || '',
  email:     process.env.BD_EMAIL      || '',
  password:  process.env.BD_PASSWORD   || '',
};

const log = (...a) => console.log(...a);

async function hasCaptcha(page) {
  return page.evaluate(() =>
    !!document.querySelector('iframe[src*="recaptcha/api2/anchor"]') ||
    !!document.querySelector('.g-recaptcha'));
}

(async () => {
  const missing = Object.entries(cfg).filter(([, v]) => !v).map(([k]) => k);
  if (missing.length) {
    log('!! این‌ها را ست کن: ' + missing.map(k => 'BD_' + k.replace(/([A-Z])/g, '_$1').toUpperCase()).join(', '));
    process.exit(1);
  }
  if (cfg.password.length < 8) { log('!! رمز باید حداقل ۸ کاراکتر باشد'); process.exit(1); }

  const browser = await chromium.launch({ headless: false, args: ['--no-sandbox'] });
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 900 },
  });
  const page = await ctx.newPage();
  page.on('console', m => { if (m.type() === 'error') log('[page error]', m.text().slice(0, 160)); });

  log('>> باز کردن صفحه‌ی ثبت‌نام…');
  await page.goto(SIGNUP, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(2500);

  // کوکی‌بنر را اگر هست ببند
  const ok = page.locator('button', { hasText: /^(OK|Accept|Got it|I agree)$/i }).first();
  if (await ok.count()) { await ok.click().catch(() => {}); await page.waitForTimeout(600); }

  log('>> پر کردن فرم…');
  await page.fill('input[name="firstName"]', cfg.firstName);
  await page.fill('input[name="lastName"]',  cfg.lastName);
  await page.fill('input[name="email"]',     cfg.email);
  await page.fill('input[name="password"]',  cfg.password);
  log('   فرم پر شد:', cfg.firstName, cfg.lastName, cfg.email, '•'.repeat(cfg.password.length));

  if (await hasCaptcha(page)) {
    log('');
    log('⚠️  کپچا روی صفحه هست. لطفاً در مرورگری که باز شده خودت حلش کن.');
    log('    (روی IP خانگی معمولاً اصلاً ظاهر نمی‌شود)');
    log('    بعد از حل، اینجا Enter بزن…');
    await page.screenshot({ path: SHOT });
    log('    عکسِ صفحه ذخیره شد: ' + SHOT);
    await new Promise(r => process.stdin.once('data', r));
  }

  log('>> ارسال فرم…');
  await page.click('button:has-text("Sign up with email")');
  await page.waitForTimeout(6000);

  log('   URL الان: ' + page.url());
  const body = (await page.evaluate(() => document.body.innerText).catch(() => '')) || '';
  log('   پیام صفحه: ' + body.replace(/\n{2,}/g, ' | ').slice(0, 400));

  // ذخیره‌ی نشست در هر صورت
  await ctx.storageState({ path: SESSION });
  log('>> نشست ذخیره شد: ' + SESSION);

  if (/verify|confirm|check your email|sent you/i.test(body)) {
    log('');
    log('📧 ایمیل تأیید فرستاده شد.');
    log('   بعد از کلیک روی لینک تأیید، این را اجرا کن تا نشستِ لاگین‌شده ذخیره شود:');
    log('     node biodigital-signup.js --after-verify');
  }

  await page.screenshot({ path: SHOT });
  log('   عکس: ' + SHOT);
  await browser.close();
})().catch(e => { console.error('!! خطا:', e.message); process.exit(1); });
