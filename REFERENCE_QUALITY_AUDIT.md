# Reference-answer quality audit (2026-08-14)

Written while building the qualitative failure-mode box (PAPER_TASKS item 6).
I set out to pick one worked example per failure mode. Verifying the
candidates against the released evidence surfaced two problems with the
*reference answers*, not the models. Both are recorded here because they
change how one number in the paper must be reported.

---

## 1. Set-collapse inflates T-lane wrong-direction counts

T-lane (screening) expert answers name a **set** of entities. Our schema
collapses each to a single reference label, so a system naming a different
member of the endorsed set scores as a wrong-direction commitment.

Mechanical test (`analysis/reference_endorsement_audit.py`): for each
wrong-direction error, does the predicted ticker appear as a whole word in
the reference's own `gold_label_evidence`?

| lane | endorsed / errors | share |
|------|------------------|-------|
| T    | 36 / 74          | **48.6%** |
| F    | 1 / 20           | 5.0%  |
| FT   | 0 / 7            | 0.0%  |

Examples: T2 gold `INTC`, reference text reads "top 5 (INTC, MU, LRCX, APP,
MRVL)"; models answered MU and LRCX — both endorsed. T29, T48, T31, T4 are
the same pattern.

**Reporting position.** T-lane wrong-direction is an **upper bound** on
genuine model error. The paper now says so explicitly (§5.2). F/FT lanes are
essentially clean, which is why the paper's worked wrong-direction example
(F21) is drawn from the F lane.

This independently confirms — by a reproducible machine test — what two
blinded annotators concluded by reading. It strengthens rather than weakens
the central claim: shrinking the wrong-direction mode makes hedge collision
*more* dominant.

---

## 2. One reference answer is contradicted by its own evidence

**F50** — "which tech company has the best overall fundamental profile?"
Reference label `APP`, justified as "ROA at 14.89% (highest) and ROE at
82.70% (highest)".

From the released indicator table the agents actually saw:

| | APP | NVDA |
|---|---|---|
| Return on Assets | 0.1489 | **0.2131** |
| Return on Equity | **0.8270** | 0.3338 |
| Sales/Assets | 0.2112 | **0.3321** |
| Debt/Equity | 3.0082 | **0.1028** |
| Cash Flow/Assets | **0.1296** | 0.1092 |

APP's ROE is indeed highest. **Its ROA is not** — NVDA's 21.31% exceeds
APP's 14.89%. The reference's stated justification is factually wrong on one
of its two cited grounds, and on the remaining indicators NVDA leads on three
of four.

All four models answered NVDA unanimously at `p_nc = 0.00`. On this question
the models' answer is defensible and the reference is at best contestable.

**Action taken.** F50 was my original wrong-direction exemplar. It has been
**dropped** from the failure-mode box and replaced with **F21** (MSFT vs AAPL
book-to-price), where the reference is unambiguous, single-name, and directly
verifiable from the pack (MSFT B/P 0.0929 > AAPL 0.0220 → MSFT cheaper).

Do **not** cite F50 as a model-error example.

### Related: direction-ambiguous references

T19 ("prime candidates for mean reversion trades") labels `INTC` (RSI 78.36,
overbought → reverts *down*). All models answered `TRI` (RSI 15.71, oversold
→ reverts *up*). The question does not specify direction, so both readings
are defensible. Not used as an exemplar.

---

## Scope of this audit

This was a **targeted** audit of exemplar candidates plus one mechanical
sweep of wrong-direction errors — not a full re-verification of all 139
reference answers. The set-collapse rate is measured and reproducible; the
F50 arithmetic error is a single confirmed instance found by hand, and I do
**not** claim a rate for reference errors generally. A full reference audit
remains open (see PAPER_TASKS).
