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

---

## 3. FULL 139-REFERENCE AUDIT (completed 2026-08-14)

`analysis/reference_answer_audit.py` checks every headline-eligible
reference against the evidence pack the agents actually saw:

| check | result |
|---|---|
| **B.** superlative claim contradicted by the pack | **2 / 139 (1.4%)** |
| **C.** reference entity absent from the pack | 0 |
| **D.** set-collapse (reference names >1 answer-space entity) | 27 / 139 (19%) |
| **A.** numeric provenance flags | 6 (5 benign, see below) |

### The 2 confirmed contradictions

Both are the same class: an **explicit "highest X" claim falsified by the
released table**. In both, the models' "wrong" answer is the one that
satisfies the reference's own stated criterion.

**F50** — "AppLovin ... ROA at 14.89% (highest)". NVDA is at $0.2131$ vs
APP's $0.1489$. All four models answered NVDA.

**T9** — "Tesla ... an OBV of 22.96 Billion, the highest among all ranked
tickers". NVDA's OBV is $166.28$ B, over 7x TSLA's. Three of four models
answered NVDA.

**Precise reading.** In both cases the *stated justification* is falsified.
Whether the *label* is wrong is a separate question: APP genuinely does have
the highest ROE ($0.827$), and T9's question asks about volume confirmation
"for their price moves", which a normalised reading of OBV might support —
but the reference states no normalisation. So: justification falsified, label
contestable. Do not describe these as "wrong gold labels" in the paper.

### Numeric provenance (check A) — 5 of 6 are benign

F31, F5, F8, T19 cite figures that differ from the pack in the 2nd–3rd
decimal (window-definition differences: the references quote a specific
as-of date, the pack takes a median over the parsed window). T21's "23.93%
above its 20-day moving average" is a *derived* quantity the checker cannot
see, and it is exactly right: $(36.83 - 29.719)/29.719 = 23.93\%$.

The one substantive case is **F14** (PayPal): the reference cites
debt/assets $4.05\%$ and debt/equity $15.99\%$; the pack shows $11.70\%$ and
$47.17\%$. The gap is far beyond rounding. The label (`no`, not
overleveraged) survives either set of figures, so this is a provenance
mismatch rather than a labelling error — but it should be disclosed.

### Checker validation

The first version of check B produced 5 flags, **3 of them false
positives**, because a superlative attached to a composite concept inverts
the indicator direction ("strongest balance sheet" = *lowest* debt/equity;
"most oversold" = *lowest* RSI). Hand-verified against the packs: F12 (GOOGL
*is* argmin debt/equity) and T35 (TRI *is* argmin RSI) are correct
references, and T19 never claims highest RSI at all. The check now fires
only when a superlative directly qualifies a named indicator. All four
hand-checked cases now classify correctly.

### Bottom line

At $1.4\%$, the F50 error was **not the tip of an iceberg** — the reference
set is broadly sound on the claims that can be checked mechanically. The
material issue for the paper is not reference errors but **set-collapse in
the T lane** (§1), which is a schema-construction choice of ours, not a
defect in the expert answers.

### Scope and limits

These checks cover claims that are mechanically verifiable against the pack:
explicit superlatives, cited figures, entity presence, and multi-entity
naming. They do **not** cover judgement claims ("best risk-reward setup"),
direction-ambiguous questions (T19), or reasoning that is valid but
unstated. A reference can pass all four checks and still be contestable.
