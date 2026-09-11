# HedgeQA-Core-v0.1 — human review complete: findings

The human review of all 368 core items is recorded, merged with both AI
adjudicators, and analysed. Two findings dominate, and one of them changes
what the AI review can be used for at all.

**Still true: nothing is `manually_validated`.** Promotion classes below are
routing labels only.

---

## Finding 1 — the AI adjudicators exhibit the pathology they were auditing

On **natural items only** (masked variants excluded, since their correct
answer *is* non-committal), the share of items each reader declined to
settle:

| benchmark | n | human | **Gemini** | **ChatGPT** | pipeline |
|---|---|---|---|---|---|
| fintradebench | 99 | 16.2% | **96.0%** | **70.7%** | 19.2% |
| financebench | 36 | 2.8% | 33.3% | 5.6% | 0.0% |
| tatqa | 50 | 12.0% | 22.0% | 16.0% | 32.0% |
| finqa | 50 | 20.0% | 20.0% | 20.0% | 18.0% |
| convfinqa | 40 | 5.0% | 10.0% | 5.0% | 5.0% |
| **all natural** | **275** | **12.7%** | **48.0%** | **33.5%** | 16.7% |

Gemini answered `insufficient_data` on **71 of 99** FinTradeBench items,
`none_clear` on 14 and `mixed` on 10 — **95 of 99 (96%)** of the lane
declined, across the three non-committal labels. Agreement with the
pipeline's own gold on FinTradeBench: human **92.9%**, Gemini **8.1%**,
ChatGPT **19.2%**.

This is not a labelling disagreement. It is **hedge collision**, the exact
failure mode this whole project measures, occurring in the adjudicators
while they read oracle evidence. It is concentrated in precisely the
judgement-style lane the parent paper identifies as highest-hedging, and it
is near-absent on the directional benchmarks (10–22%, close to human), which
is what makes it diagnostic rather than noise.

### Consequences

1. **Gemini and ChatGPT are not usable as adjudicators on FinTradeBench, and
   Gemini is marginal on FinanceBench.** Their labels there are dominated by
   their own refusal to commit, not by the evidence. Any agreement statistic
   computed on that lane measures their hedging rate.
2. **It is usable as a finding.** An independent, accidental replication of
   the paper's central claim — on a different item set, with the models cast
   as readers rather than subjects — is worth more than another debate run.
   It should be reported as what it is: an unplanned observation, not a
   designed experiment.
3. **The directional lanes remain usable.** TAT-QA, FinQA and ConvFinQA show
   5–22% non-commitment across all three readers, so agreement there is
   meaningful.

---

## Finding 2 — roughly half the masked variants are answerable

`masked_variant_valid = no` means the reviewer found a route to the answer,
which falsifies the constructed `insufficient_data` gold.

| reviewer | mask holds (`yes`) | **mask fails (`no`)** |
|---|---|---|
| human | 49 | **44 / 93 (47%)** |
| Gemini | 50 | 43 |
| ChatGPT | 39 | 54 |

- **at least one reviewer found a route: 59 / 93 (63%)**
- **both AI reviewers found a route: 38 / 93**
- **the human found a route: 44 / 93**

The human's 47% is the number that matters. The automated guards caught two
leak patterns — roll-forward, and total-minus-components — and the
independent re-check showed 0 of 323 reconstructible by those two routes.
Human reading finds roughly half still answerable by routes the guards do
not model.

Human-judged failures by source: TAT-QA 17, FinanceBench 16, FinQA 10,
ConvFinQA 1.

### Consequences

**The controlled-insufficient construction is not sound enough to ship as
is.** This was the collection's mechanism for making overcommitment
measurable, and the mechanism is roughly half broken. Options, in the order I
would take them:

1. **Exclude the 44 human-failed variants** and keep 49. The non-committal
   share drops and the remaining set is trustworthy.
2. **Read the human's flags** on the failed ones to learn which routes the
   guards missed, and extend `masking.py`. A newly identified route is worth
   more than the individual items, because it improves every future mask.
3. Do **not** re-mask and re-ship without a fresh human pass. The failure
   rate is too high to trust a repaired batch unread.

---

## Agreement (with Finding 1 in mind)

### `gold_label` — raw agreement only

| comparison | n | raw agreement |
|---|---|---|
| human vs Gemini | 368 | 67.1% |
| human vs ChatGPT | 368 | 73.4% |
| **Gemini vs ChatGPT** | 368 | **79.1%** |

### `gold_commitment` — Cohen's kappa

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 368 | 69.3% | **0.398** |
| human vs ChatGPT | 368 | 77.4% | **0.476** |
| **Gemini vs ChatGPT** | 368 | 82.3% | **0.657** |

**The two AI reviewers agree with each other markedly more than either
agrees with the human** — κ 0.657 against 0.398 / 0.476. This is the
correlated-failure-mode prediction confirmed: they are not independent
raters, and their mutual agreement is partly agreement on a shared bias
(the hedging above). Human–AI κ also sits *below* the 0.53–0.59 that two
blinded humans reached on this same judgement in the parent project.

### `keep_or_exclude` — kappa near zero

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 359 | 66.9% | **0.037** |
| human vs ChatGPT | 359 | 66.0% | **−0.011** |
| Gemini vs ChatGPT | 368 | 75.3% | 0.443 |

Raw agreement of ~66% looks acceptable and is meaningless here. The
marginals explain it:

| reviewer | keep | exclude | exclude rate |
|---|---|---|---|
| human | 354 | 5 | **1.4%** |
| Gemini | 244 | 124 | **33.7%** |
| ChatGPT | 247 | 121 | **32.9%** |

The human kept almost everything; the AI reviewers excluded a third. κ ≈ 0
means that **on which specific items to exclude, the human and the AI
reviewers agree at chance** — and ChatGPT slightly worse than chance. Their
exclusions are largely downstream of their own inability to answer, not of a
defect in the item.

**Do not use AI `keep_or_exclude` as an exclusion signal.** It carries no
information about the human's exclusion criterion.

---

## Promotion classes (routing only)

| class | items |
|---|---|
| `strong_keep` | 171 |
| `review_needed` | 115 |
| `exclude` | 82 |

By transformation:

| transformation | strong_keep | review_needed | exclude |
|---|---|---|---|
| numeric_to_directional (140) | 119 | 16 | 5 |
| evidence_masked_insufficient (93) | 31 | 18 | 44 |
| none (135) | 21 | 81 | 33 |

By benchmark:

| benchmark | strong_keep | review_needed | exclude |
|---|---|---|---|
| convfinqa (60) | 49 | 7 | 4 |
| finqa (75) | 54 | 10 | 11 |
| tatqa (75) | 44 | 15 | 16 |
| financebench (59) | 22 | 17 | 20 |
| **fintradebench (99)** | **2** | 66 | 31 |

**Read these two rows with Finding 1 in hand.** FinTradeBench shows 2
`strong_keep` out of 99 — but that is not evidence those items are bad. It
is the arithmetic consequence of Gemini declining 96% of the lane: an item
cannot reach `strong_keep` when a reviewer who refused to answer is counted
as disagreeing. The same applies to the 82 `exclude`, of which 33 come from
the `none` family where both AI reviewers excluded.

The directional lanes are the ones where the promotion classes mean what
they appear to mean: 119 of 140 `strong_keep`.

---

## Data-quality notes on the human sheet

Two things the review app should have caught and did not:

1. **9 items have no `keep_or_exclude` decision** despite
   `review_status = reviewed`. The app's validation required the label,
   commitment and evidence-sufficiency fields but never `keep_or_exclude`
   itself — a gap in the validation spec I implemented as written. They
   route to `review_needed`, so nothing is silently wrong, but they need a
   decision. Ids: `hqa_FB_04a83e7c`, `hqa_FB_4fcce970`, `hqa_FB_5aee2b1c`,
   `hqa_FB_9954aa1f`, `hqa_FB_cfe29aff_masked`, `hqa_FQ_16a8661c`,
   `hqa_FTB_54bc7248`, `hqa_FTB_7c1b95b5`, `hqa_FTB_b1c0ad1d`.

2. **8 items record a `gold_commitment` that disagrees with their label's
   non-committal status.** Five are `roughly_unchanged` marked `committed`,
   two are `mixed` marked `committed`, one is `unsupportive` marked
   `noncommitted`.

   The `roughly_unchanged` cases look like a **deliberate and defensible
   disagreement with the schema's convention** — the protocol anticipated it
   and asked for it to be noted rather than silently re-classified. It is a
   real methodological question: `roughly_unchanged` reports a finding ("no
   material change") as much as it declines one.

   This is not a clerical matter. If `roughly_unchanged` is committed, the
   non-committal share of the collection and every overcommitment /
   hedge-collision count computed on it move. **Decide the convention
   explicitly, apply it everywhere, and state it in any write-up.**

The 5 human exclusions were: 2 FinQA directional items (derivation unclear /
metric ambiguous) and 3 FinTradeBench items (multiple defensible answers,
missing peer data).

---

## Recommended next steps

1. **Settle the `roughly_unchanged` convention.** It is upstream of every
   hedging statistic; nothing else should be recomputed until it is fixed.
2. **Resolve the 9 items with no keep/exclude decision.**
3. **Act on the masked variants.** Exclude the 44 the human judged
   answerable; mine their flags for leak routes the guards miss; extend
   `masking.py` before constructing any more.
4. **Re-scope the AI review.** Keep it for TAT-QA / FinQA / ConvFinQA, where
   all three readers behave comparably. Drop it as an adjudication signal for
   FinTradeBench and treat Gemini's FinanceBench numbers with caution.
5. **Write up Finding 1 for the paper.** An independent replication of the
   hedging result, obtained accidentally with the models as readers rather
   than subjects, is a genuine contribution — reported honestly as an
   unplanned observation on a small, non-preregistered sample.
6. **Only then** decide promotions, item by item, by hand.
