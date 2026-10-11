import {
  type DesignSystem,
  type Page,
  type SlideMeta,
  type SlideTransition,
  Step,
  Steps,
  useIsActivePage,
} from '@open-slide/core';
import type { CSSProperties, ReactNode } from 'react';

export const design: DesignSystem = {
  palette: { bg: '#0f1115', text: '#e8e6e1', accent: '#f0a04b' },
  fonts: {
    display: '"Vazirmatn", "IRANSans", "Tahoma", "Segoe UI", system-ui, sans-serif',
    body: '"Vazirmatn", "IRANSans", "Tahoma", "Segoe UI", system-ui, sans-serif',
  },
  typeScale: { hero: 132, body: 34 },
  radius: 14,
};

const ink = {
  soft: '#b9b6b0',
  muted: '#8b8880',
  dim: '#5c5a55',
  rule: '#2a2d33',
  good: '#5fbf8f',
  bad: '#e0645f',
};

/* ── قلمروِ نمودار ───────────────────────────────────────────── */
const CH = { x0: 300, y0: 300, w: 1320, h: 520 };

function path(fn: (t: number) => number, n = 160): string {
  const pts: string[] = [];
  for (let i = 0; i <= n; i++) {
    const t = i / n;
    const x = CH.x0 + t * CH.w;
    const y = CH.y0 + (1 - fn(t)) * CH.h;
    pts.push(`${x.toFixed(1)},${y.toFixed(1)}`);
  }
  return 'M' + pts.join(' L');
}

/** فراموشیِ ساده: افتِ نمایی */
const decay = (t: number) => Math.exp(-2.9 * t);

/** مرورِ فاصله‌دار: افت می‌کند، با هر مرور بالاتر برمی‌گردد */
const REVIEWS = [0, 0.22, 0.45, 0.68, 0.86];
const spaced = (t: number) => {
  let base = REVIEWS[0];
  let idx = 0;
  for (let i = 0; i < REVIEWS.length; i++) {
    if (REVIEWS[i] <= t) { base = REVIEWS[i]; idx = i; }
  }
  const floor = Math.min(0.72, 0.17 * idx);
  return floor + (1 - floor) * Math.exp(-2.9 * (t - base));
};

/* ── اجزای کمکی ──────────────────────────────────────────────── */
const RTL: CSSProperties = {
  direction: 'rtl',
  fontFamily: 'var(--osd-font-body)',
  height: '100%',
  padding: '86px 130px',
  display: 'flex',
  flexDirection: 'column',
  background: 'var(--osd-bg)',
  color: 'var(--osd-text)',
  boxSizing: 'border-box',
};

const h1: CSSProperties = {
  fontFamily: 'var(--osd-font-display)',
  fontSize: 'var(--osd-size-hero)',
  fontWeight: 800,
  lineHeight: 1.05,
  margin: 0,
  letterSpacing: '-0.02em',
};

const h2: CSSProperties = {
  fontFamily: 'var(--osd-font-display)',
  fontSize: 64,
  fontWeight: 800,
  lineHeight: 1.1,
  margin: '0 0 12px',
};

const lede: CSSProperties = {
  fontSize: 'var(--osd-size-body)',
  color: ink.soft,
  lineHeight: 1.6,
  margin: 0,
};

const bullet: CSSProperties = {
  fontSize: 42,
  lineHeight: 1.45,
  color: 'var(--osd-text)',
  padding: '20px 28px',
  borderRadius: 'var(--osd-radius)',
  background: '#171a1f',
  borderRight: `5px solid var(--osd-accent)`,
  marginBottom: 18,
};

const axis: CSSProperties = { stroke: ink.rule, strokeWidth: 2, fill: 'none' };
const axisLabel: CSSProperties = {
  fill: ink.dim,
  fontSize: 22,
  fontFamily: 'var(--osd-font-body)',
};

function Frame({ children, title, sub }: { children: ReactNode; title: string; sub?: string }) {
  return (
    <div style={RTL}>
      <div style={{ marginBottom: 18 }}>
        <h2 style={h2}>{title}</h2>
        {sub && <p style={lede}>{sub}</p>}
      </div>
      <div style={{ flex: 1, minHeight: 0 }}>{children}</div>
    </div>
  );
}

function Curve({
  d,
  color,
  active,
  delay = 0,
}: {
  d: string;
  color: string;
  active: boolean;
  delay?: number;
}) {
  const len = 4000; // طولِ تقریبی برای انیمیشنِ رسم
  return (
    <path
      d={d}
      fill="none"
      stroke={color}
      strokeWidth={7}
      strokeLinecap="round"
      style={{
        strokeDasharray: len,
        strokeDashoffset: active ? 0 : len,
        transition: `stroke-dashoffset 1500ms cubic-bezier(.22,.61,.36,1) ${delay}ms`,
      }}
    />
  );
}

function Axes() {
  return (
    <g>
      <path style={axis} d={`M${CH.x0} ${CH.y0} L${CH.x0} ${CH.y0 + CH.h} L${CH.x0 + CH.w} ${CH.y0 + CH.h}`} />
      <text style={axisLabel} x={CH.x0 + CH.w} y={CH.y0 + CH.h + 44} textAnchor="end">
        زمان
      </text>
      <text style={axisLabel} x={CH.x0 - 22} y={CH.y0 + 14} textAnchor="end">
        بخاطرسپاری
      </text>
    </g>
  );
}

/* ── صفحه ۱: جلد ─────────────────────────────────────────────── */
const Cover: Page = () => (
  <div style={{ ...RTL, justifyContent: 'center' }}>
    <div
      style={{
        fontSize: 26,
        color: 'var(--osd-accent)',
        letterSpacing: '0.22em',
        marginBottom: 26,
      }}
    >
      منحنیِ فراموشی · ابینگهاوس ۱۸۸۵
    </div>
    <h1 style={{ ...h1, maxWidth: 1500 }}>چرا هرچه می‌خوانی فراموش می‌کنی؟</h1>
    <div
      style={{
        width: 190,
        height: 7,
        background: 'var(--osd-accent)',
        borderRadius: 4,
        margin: '46px 0 34px',
      }}
    />
    <p style={{ ...lede, maxWidth: 1150, fontSize: 38 }}>
      و سه کاری که از امروز می‌توانی درباره‌اش انجام بدهی
    </p>
  </div>
);

/* ── صفحه ۲: خودِ منحنی ──────────────────────────────────────── */
const TheCurve: Page = () => {
  const active = useIsActivePage();
  return (
    <Frame title="فراموشی از همان روزِ اول شروع می‌شود" sub="بدون مرور، بیشترِ آنچه خوانده‌ای در یک هفته می‌رود.">
      <svg viewBox="0 0 1920 1080" style={{ width: '100%', height: '100%' }}>
        <Axes />
        <Curve d={path(decay)} color={ink.bad} active={active} />
        <g style={axisLabel}>
          <text x={CH.x0 + 8} y={CH.y0 + CH.h + 90}>روز ۱</text>
          <text x={CH.x0 + CH.w * 0.33} y={CH.y0 + CH.h + 90}>روز ۷</text>
          <text x={CH.x0 + CH.w * 0.98} y={CH.y0 + CH.h + 90} textAnchor="end">روز ۳۰</text>
        </g>
      </svg>
    </Frame>
  );
};

/* ── صفحه ۳: چرا ─────────────────────────────────────────────── */
const Why: Page = () => (
  <Frame title="چرا؟">
    <Steps>
      <div style={bullet}>مغز چیزی را که از آن استفاده نمی‌شود هرس می‌کند — این نقص نیست، بهینه‌سازی است.</div>
      <Step>
        <div style={bullet}>هر بار که چیزی را «به خاطر می‌آوری»، آن مسیرِ عصبی ضخیم‌تر می‌شود.</div>
      </Step>
      <Step>
        <div style={bullet}>پس مشکل «نخواندن» نیست؛ مشکل «دوباره نخواندن» است.</div>
      </Step>
      <Step>
        <div style={{ ...bullet, borderRightColor: ink.good }}>
          نتیجه: یادگیری یک رویداد نیست — یک زمان‌بندی است.
        </div>
      </Step>
    </Steps>
  </Frame>
);

/* ── صفحه ۴: راه حل ──────────────────────────────────────────── */
const TheFix: Page = () => {
  const active = useIsActivePage();
  return (
    <Frame title="مرورِ فاصله‌دار" sub="هر مرور، خطِ فراموشی را یک پله بالاتر می‌برد.">
      <svg viewBox="0 0 1920 1080" style={{ width: '100%', height: '100%' }}>
        <Axes />
        <path d={path(decay)} fill="none" stroke={ink.bad} strokeWidth={4} strokeDasharray="9 11" opacity={0.45} />
        <Curve d={path(spaced)} color={ink.good} active={active} delay={220} />
        {REVIEWS.slice(1).map((r, i) => (
          <circle
            key={i}
            cx={CH.x0 + r * CH.w}
            cy={CH.y0 + (1 - spaced(r)) * CH.h}
            r={13}
            fill="var(--osd-accent)"
            style={{
              opacity: active ? 1 : 0,
              transition: `opacity 500ms ease ${900 + i * 260}ms`,
            }}
          />
        ))}
      </svg>
    </Frame>
  );
};

/* ── صفحه ۵: مقایسه ──────────────────────────────────────────── */
const colTitle: CSSProperties = { fontSize: 44, fontWeight: 800, marginBottom: 22 };
const col: CSSProperties = { flex: 1, padding: '0 26px' };

const Compare: Page = () => (
  <Frame title="دو روش، دو نتیجه">
    <div style={{ display: 'flex', height: '100%', gap: 26 }}>
      <div style={col}>
        <div style={{ ...colTitle, color: ink.bad }}>فشرده‌خوانیِ شبِ امتحان</div>
        <Steps>
          <div style={{ ...bullet, borderRightColor: ink.bad, fontSize: 34 }}>یک‌باره حجمِ زیاد</div>
          <Step><div style={{ ...bullet, borderRightColor: ink.bad, fontSize: 34 }}>احساسِ تسلطِ کاذب</div></Step>
          <Step><div style={{ ...bullet, borderRightColor: ink.bad, fontSize: 34 }}>تا دو هفته: تقریباً هیچ</div></Step>
        </Steps>
      </div>
      <div style={{ width: 2, background: ink.rule }} />
      <div style={col}>
        <div style={{ ...colTitle, color: ink.good }}>مطالعه‌ی توزیع‌شده</div>
        <Steps>
          <div style={{ ...bullet, borderRightColor: ink.good, fontSize: 34 }}>حجمِ کم، دفعاتِ بیشتر</div>
          <Step><div style={{ ...bullet, borderRightColor: ink.good, fontSize: 34 }}>سخت‌تر به‌نظر می‌رسد — چون واقعاً یاد می‌گیری</div></Step>
          <Step><div style={{ ...bullet, borderRightColor: ink.good, fontSize: 34 }}>ماندگاریِ ماه‌ها</div></Step>
        </Steps>
      </div>
    </div>
  </Frame>
);

/* ── صفحه ۶: عمل ─────────────────────────────────────────────── */
const Action: Page = () => (
  <Frame title="از امروز، سه قانون">
    <Steps>
      <div style={bullet}>
        <span style={{ color: 'var(--osd-accent)', fontWeight: 800 }}>۱. </span>
        قبل از اینکه فراموش کنی مرور کن — نه بعدش.
      </div>
      <Step>
        <div style={bullet}>
          <span style={{ color: 'var(--osd-accent)', fontWeight: 800 }}>۲. </span>
          خودت را امتحان کن، دوباره نخوان. بازیابی، تمرین است؛ مرور، فقط آشناست.
        </div>
      </Step>
      <Step>
        <div style={bullet}>
          <span style={{ color: 'var(--osd-accent)', fontWeight: 800 }}>۳. </span>
          فاصله را زیاد کن: فردا · ۳ روز · ۷ روز · ۲۱ روز
        </div>
      </Step>
    </Steps>
  </Frame>
);

/* ── قراردادهای چارچوب ───────────────────────────────────────── */
export const meta: SlideMeta = {
  title: 'منحنی فراموشی',
  createdAt: '2026-10-11T03:26:53.676Z',
};

export const transition: SlideTransition = {
  duration: 520,
  easing: 'cubic-bezier(.22,.61,.36,1)',
  enter: { keyframes: [{ opacity: 0, transform: 'translateY(22px)' }, { opacity: 1, transform: 'none' }] },
  exit: { keyframes: [{ opacity: 1 }, { opacity: 0 }], duration: 220 },
};

export const notes: (string | undefined)[] = [
  // ۱ — جلد
  'با یک سؤال شروع کن، نه با تعریف. از کلاس بپرس: «آخرین چیزی که خواندی و یادت مانده چی بود؟» '
    + 'بعد بگو بیشترِ آنچه این هفته خوانده‌ای تا هفته‌ی دیگر رفته است — و این تقصیرِ تو نیست.',

  // ۲ — منحنی
  'بگذار منحنی رسم شود و ساکت بمان؛ عدد را نگو تا خودشان بپرسند. '
    + 'نکته‌ی کلیدی: افت در ۲۴ ساعتِ اول تندترین بخش است، نه در ماهِ بعد.',

  // ۳ — چرا
  'اینجا مفهومِ هرس کردن (pruning) را با یک مثال بزن: مسیرهایی که رفت‌وآمد ندارند، '
    + 'مثل جاده‌های متروکه در جنگل، کم‌کم پوشیده می‌شوند. '
    + 'جمله‌ی آخر را با مکث بگو: «یادگیری یک رویداد نیست، یک زمان‌بندی است.»',

  // ۴ — راه حل
  'روی هر نقطه‌ی نارنجی مکث کن: این یک مرور است. نشان بده که خطِ پایه با هر مرور بالاتر می‌آید. '
    + 'همین‌جا برنامه‌ی مرور را با آن‌ها بچین: فردا، ۳ روز، ۷ روز، ۲۱ روز.',

  // ۵ — مقایسه
  'روی «احساسِ تسلطِ کاذب» تأکید کن — این همان دامی است که دانش‌آموزانِ باهوش در آن می‌افتند. '
    + 'اگر مطالعه آسان به‌نظر می‌رسد، احتمالاً چیزی یاد نگرفته‌ای.',

  // ۶ — عمل
  'سه قانون را روی تخته بنویس. از آن‌ها بخواه همین امشب یک مرورِ ۱۰ دقیقه‌ای برای درسِ دیروز بگذارند. '
    + 'تعهدِ کوچکِ امروز از برنامه‌ی بزرگِ فردا بیشتر ارزش دارد.',
];

export default [Cover, TheCurve, Why, TheFix, Compare, Action] satisfies Page[];
