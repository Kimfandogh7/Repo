#!/usr/bin/env python3
"""
موتورِ آزمونِ تطبیقی برای ایجنتِ مشاور تحصیلی.

ایده: به‌جای ۵۰ سؤالِ ثابت، با ~۱۵ سؤالِ هوشمند سطحِ واقعی را تخمین می‌زند.
هر سؤال بعدی بر اساس پاسخ‌های قبلی انتخاب می‌شود (بیشینه‌سازیِ اطلاعِ فیشر).

مدل: 1PL / Rasch —  P(درست) = 1 / (1 + exp(-(θ - b)))
  θ = تواناییِ دانش‌آموز   b = دشواریِ سؤال

چرا این مدل: ساده، قابل تفسیر، و با ۱۰-۱۵ سؤال هم به‌خوبی همگرا می‌شود.
(مدل‌های 3PL به داده‌ی خیلی بیشتری نیاز دارند و اینجا فایده‌ای ندارند.)

بدون وابستگیِ خارجی — فقط کتابخانه‌ی استاندارد.
"""
from __future__ import annotations
import json
import math
import random
from dataclasses import dataclass, field, asdict
from typing import Callable, Optional


# ── مدل ────────────────────────────────────────────────────────────
def p_correct(theta: float, b: float) -> float:
    """احتمالِ پاسخِ درست با توانایی θ و دشواریِ b"""
    return 1.0 / (1.0 + math.exp(-(theta - b)))


def fisher_information(theta: float, b: float) -> float:
    """اطلاعِ فیشر — هرچه بیشتر، آن سؤال در این سطح دقیق‌تر اندازه می‌گیرد"""
    p = p_correct(theta, b)
    return p * (1.0 - p)


@dataclass
class Question:
    id: str
    text: str
    b: float                      # دشواری (معمولاً -3 تا +3)
    concepts: list[str]           # مفاهیمی که این سؤال می‌سنجد
    options: list[str] = field(default_factory=list)
    answer: int = 0               # اندیسِ گزینه‌ی درست
    explanation: str = ""


@dataclass
class Answer:
    qid: str
    correct: bool


# ── تخمینِ توانایی ─────────────────────────────────────────────────
def estimate_theta(answers: list[Answer], bank: dict[str, Question]) -> tuple[float, float]:
    """
    برآوردِ بیشینه‌درست‌نمایی (MLE) با جست‌وجوی سه‌بخشی،
    به‌همراه خطای استاندارد (از اطلاعِ فیشر).

    بازگشت: (theta, standard_error)
    """
    if not answers:
        return 0.0, float("inf")

    def loglik(theta: float) -> float:
        ll = 0.0
        for a in answers:
            p = p_correct(theta, bank[a.qid].b)
            p = min(max(p, 1e-9), 1 - 1e-9)   # جلوگیری از log(0)
            ll += math.log(p) if a.correct else math.log(1 - p)
        return ll

    # MLE در مسائلِ همه-درست/همه-غلط به بی‌نهایت میل می‌کند؛ مهارش می‌کنیم
    lo, hi = -4.0, 4.0
    for _ in range(60):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if loglik(m1) < loglik(m2):
            lo = m1
        else:
            hi = m2
    theta = (lo + hi) / 2

    info = sum(fisher_information(theta, bank[a.qid].b) for a in answers)
    se = 1.0 / math.sqrt(info) if info > 0 else float("inf")
    return theta, se


# ── انتخابِ سؤالِ بعدی ────────────────────────────────────────────
def next_question(
    theta: float,
    asked: set[str],
    bank: dict[str, Question],
    focus: Optional[list[str]] = None,
) -> Optional[Question]:
    """سؤالی را برمی‌گرداند که بیشترین اطلاع را در سطحِ فعلی دارد."""
    cands = [q for q in bank.values() if q.id not in asked]
    if focus:
        pref = [q for q in cands if set(q.concepts) & set(focus)]
        if pref:
            cands = pref
    if not cands:
        return None
    return max(cands, key=lambda q: fisher_information(theta, q.b))


# ── نقشه‌ی تسلط بر مفاهیم ─────────────────────────────────────────
def concept_mastery(answers: list[Answer], bank: dict[str, Question]) -> dict[str, dict]:
    """
    برای هر مفهوم: عملکردِ واقعی در برابر انتظار.

    نکته‌ی کلیدی (که در اولین نسخه اشتباه بود): انتظار نباید از تواناییِ کل
    حساب شود. اگر دانش‌آموز در یک مفهوم ضعیف باشد، نمره‌ی کلش هم می‌افتد،
    پس انتظار هم می‌افتد و شکاف اصلاً دیده نمی‌شود.
    راه‌حل: توانایی را *بدون* سؤال‌های آن مفهوم تخمین بزن (leave-one-out)،
    بعد عملکرد روی خودِ آن مفهوم را با آن بسنج.
    """
    concepts: set[str] = set()
    for a in answers:
        concepts.update(bank[a.qid].concepts)

    overall, _ = estimate_theta(answers, bank)
    out: dict[str, dict] = {}

    for c in concepts:
        mine = [a for a in answers if c in bank[a.qid].concepts]
        others = [a for a in answers if c not in bank[a.qid].concepts]

        # تواناییِ بدونِ این مفهوم؛ اگر داده کافی نیست، سراغ تواناییِ کل می‌رویم
        if len(others) >= 3:
            theta_c, _ = estimate_theta(others, bank)
            basis = "leave-one-out"
        else:
            theta_c, basis = overall, "overall (داده کم)"

        asked = len(mine)
        correct = sum(1 for a in mine if a.correct)
        expected = sum(p_correct(theta_c, bank[a.qid].b) for a in mine)
        exp_rate = expected / asked if asked else 0
        rate = correct / asked if asked else 0
        gap = exp_rate - rate                    # مثبت = ضعیف‌تر از انتظار

        if asked == 0:
            status = "سنجیده نشد"
        elif asked < 2:
            status = "نامشخص (۱ سؤال)"
        elif gap > 0.25:
            status = "ضعیف"
        elif gap < -0.15:
            status = "قوی"
        else:
            status = "متوسط"

        out[c] = {
            "asked": asked,
            "correct": correct,
            "rate": round(rate, 2),
            "expected": round(exp_rate, 2),
            "gap": round(gap, 2),
            "theta_without": round(theta_c, 2),
            "basis": basis,
            "status": status,
        }
    return out


# ──────────────────────────────────────────────────────────────────
@dataclass
class Session:
    bank: dict[str, Question]
    answers: list[Answer] = field(default_factory=list)
    theta: float = 0.0
    se: float = float("inf")

    def asked_ids(self) -> set[str]:
        return {a.qid for a in self.answers}

    def pick(self, focus: Optional[list[str]] = None) -> Optional[Question]:
        return next_question(self.theta, self.asked_ids(), self.bank, focus)

    def record(self, qid: str, correct: bool) -> None:
        self.answers.append(Answer(qid, correct))
        self.theta, self.se = estimate_theta(self.answers, self.bank)

    # آستانه‌ها بر اساس اندازه‌گیری روی شبیه‌سازی (نه حدس):
    #   خطا: ۵ سؤال ۰.۸۶ | ۱۰ سؤال ۰.۵۶ | ۱۲ سؤال ۰.۵۵ | ۱۵ سؤال ۰.۵۰ | ۲۵ سؤال ۰.۴۲
    #   یعنی بعد از ~۱۲ سؤال بازده به‌شدت کم می‌شود: دو برابر سؤال، فقط ۰.۱۳ بهبود.
    #   سقفِ ۰.۳۵ هم دست‌نیافتنی بود (با ۱PL و این بانک کفِ SE حدود ۰.۴۵ است).
    TARGET_N = 12
    EARLY_SE = 0.50
    EARLY_MIN_N = 8

    @property
    def done(self) -> bool:
        n = len(self.answers)
        if n >= self.TARGET_N:
            return True
        return n >= self.EARLY_MIN_N and self.se < self.EARLY_SE

    # ── مرحله‌ی دوم: پوششِ مفاهیم ─────────────────────────────────
    # مشکلِ مرحله‌ی اول: انتخابِ «بیشینه اطلاع» فقط تواناییِ کل را دقیق می‌کند،
    # و بیشترِ مفاهیم یا صفر سؤال می‌گیرند یا یکی — که برای تشخیصِ مفهومی بی‌فایده است.
    # مرحله‌ی دوم برای مفاهیمی که کم سنجیده شده‌اند سؤالِ هدفمند می‌پرسد.
    SWEEP_MIN_PER_CONCEPT = 3
    SWEEP_EXTRA = 8

    def sweep_targets(self, top_n: int = 5) -> list[Question]:
        """مفاهیمی را که کمتر از حد سنجیده شده‌اند هدف می‌گیرد (مهم‌ترها اول)."""
        counts = self._concept_counts()
        freq = self._concept_frequency()          # مفاهیمِ پرتکرارتر = مهم‌تر
        needy = [c for c in freq if counts.get(c, 0) < self.SWEEP_MIN_PER_CONCEPT]
        needy.sort(key=lambda c: (-freq[c], counts.get(c, 0)))
        picked: list[Question] = []
        seen = self.asked_ids()
        for c in needy[:top_n]:
            cands = [q for q in self.bank.values()
                     if c in q.concepts and q.id not in seen]
            if not cands:
                continue
            # نزدیک‌ترین دشواری به تواناییِ فعلی — نه بیشترین اطلاع
            q = min(cands, key=lambda q: abs(q.b - self.theta))
            picked.append(q); seen.add(q.id)
            if len(picked) >= self.SWEEP_EXTRA:
                break
        return picked

    def _concept_counts(self) -> dict[str, int]:
        d: dict[str, int] = {}
        for a in self.answers:
            for c in self.bank[a.qid].concepts:
                d[c] = d.get(c, 0) + 1
        return d

    def _concept_frequency(self) -> dict[str, int]:
        d: dict[str, int] = {}
        for q in self.bank.values():
            for c in q.concepts:
                d[c] = d.get(c, 0) + 1
        return d

    def report(self, min_evidence: int = 3) -> dict:
        concepts = concept_mastery(self.answers, self.bank)
        ranked = sorted(
            [c for c in concepts.items() if c[1]["asked"] >= min_evidence],
            key=lambda kv: -kv[1]["gap"],
        )
        return {
            "theta": round(self.theta, 2),
            "se": round(self.se, 3) if self.se != float("inf") else None,
            "questions_asked": len(self.answers),
            "correct": sum(1 for a in self.answers if a.correct),
            "concepts": concepts,
            "weak_first": [{"concept": k, **v} for k, v in ranked],
        }


def load_bank(path: str) -> dict[str, Question]:
    with open(path, encoding="utf8") as f:
        raw = json.load(f)
    return {q["id"]: Question(**q) for q in raw}


# ── شبیه‌ساز: برای تستِ خودِ موتور ─────────────────────────────────
def simulate(true_theta: float, bank: dict[str, Question], rng: random.Random) -> Session:
    """یک دانش‌آموزِ فرضی با تواناییِ معلوم — برای اینکه بفهمیم موتور درست تخمین می‌زند یا نه"""
    s = Session(bank)
    while not s.done:
        q = s.pick()
        if q is None:
            break
        correct = rng.random() < p_correct(true_theta, q.b)
        s.record(q.id, correct)
    return s
