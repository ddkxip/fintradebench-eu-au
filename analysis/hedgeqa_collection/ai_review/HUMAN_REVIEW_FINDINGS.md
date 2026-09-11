# HedgeQA-Core-v0.1 — human review complete: findings

The human review of all 368 core items is recorded, merged with both AI
adjudicators, and analysed.

**Convention revised (2026-09).** `roughly_unchanged` is now **committed**,
not non-committal: it reports that a quantity did not move materially, which
is an answer rather than a declination. Only `insufficient_data` declines on
a directional item. This was the reviewer's call, it is applied throughout
the schema, builders, protocol, prompt and reports, and **every number below
is computed under it.** Figures in earlier versions of this document are
superseded.

**Nothing is `manually_validated`.** Promotion classes are routing labels.

---

## Finding 1 — the AI adjudicators exhibit the pathology they were auditing

Share of **natural items** (masked variants excluded, since their correct
answer *is* non-committal) that each reader declined to settle:

| benchmark | n | human | **Gemini** | **ChatGPT** | pipeline |
|---|---|---|---|---|---|
| fintradebench | 99 | 16.2% | **96.0%** | **70.7%** | 19.2% |
| financebench | 36 | 2.8% | 33.3% | 5.6% | 0.0% |
| tatqa | 50 | 0.0% | 10.0% | 4.0% | 0.0% |
| finqa | 50 | 4.0% | 4.0% | 2.0% | 0.0% |
| convfinqa | 40 | 0.0% | 5.0% | 0.0% | 0.0% |
| **all natural** | **275** | **6.9%** | **42.2%** | **27.3%** | **6.9%** |

The human and the pipeline decline at exactly the same rate (6.9%). Gemini
declines **6.1x** as often, ChatGPT **4.0x**.

On FinTradeBench, Gemini returned a non-committal label on **95 of 99**
items. Agreement with the pipeline's own gold there: human **92.9%**,
Gemini **8.1%**, ChatGPT **19.2%**.

This is **hedge collision** — the exact failure mode this project measures —
occurring in the adjudicators while they read oracle evidence. It is
concentrated in the judgement-style lane the parent paper identifies as
highest-hedging, and near-absent on the directional lanes (0–10%), which is
what makes it diagnostic rather than noise.

### Consequences

1. **Gemini and ChatGPT cannot adjudicate FinTradeBench**, and Gemini is
   unreliable on FinanceBench. Their labels there are produced by their own
   refusal to commit, not by the evidence.
2. **It is a finding worth reporting.** An independent replication of the
   paper's central claim, on a different item set, with the models cast as
   readers rather than subjects — obtained accidentally. Report it as an
   unplanned observation on a small non-preregistered sample, not as a
   designed experiment.
3. **The directional lanes stay usable.** All three readers sit at 0–10%
   there, so agreement on TAT-QA, FinQA and ConvFinQA is meaningful.

---

## Finding 2 — roughly half the masked variants are answerable

`masked_variant_valid = no` means the reviewer found a route to the answer,
which falsifies the constructed `insufficient_data` gold.

| reviewer | mask holds | **mask fails** |
|---|---|---|
| **human** | 49 | **44 / 93 (47%)** |
| Gemini | 50 | 43 |
| ChatGPT | 39 | 54 |

- at least one reviewer found a route: **59 / 93 (63%)**
- both AI reviewers found a route: **38 / 93**
- the human found a route: **44 / 93**

The human's 47% is the number that matters. The automated guards catch two
leak patterns — roll-forward and total-minus-components — and an independent
re-check confirmed 0 of 323 reconstructible by those two. Human reading finds
roughly half still answerable by routes the guards do not model.

Human-judged failures by source: TAT-QA 17, FinanceBench 16, FinQA 10,
ConvFinQA 1.

### Consequences

**The controlled-insufficient construction is not sound enough to ship.** It
was the mechanism that made overcommitment measurable, and it is roughly half
broken. In order:

1. **Exclude the 44 human-failed variants**, keep 49.
2. **Mine the flags on the failures** for leak routes the guards miss and
   extend `masking.py`. A newly identified route is worth more than the
   items, because it improves every future mask.
3. **Do not re-mask and re-ship without a fresh human pass.** The failure
   rate is too high to trust a repaired batch unread.

---

## Agreement

All figures computed under the revised convention. The AI reviewers were
*instructed* under the old one, so their recorded commitment for a
`roughly_unchanged` label is obedience to a superseded instruction rather
than a judgement; it is remapped at merge time. Their raw response files on
disk are unmodified — they are the evidence.

### `gold_label` — raw agreement only

Kappa is undefined here: the answer space is per-item, 46 distinct labels
appear, so there is no shared category set. Raw agreement also **overstates
skill**, because most items admit only 2–4 plausible labels.

| comparison | n | raw agreement |
|---|---|---|
| human vs Gemini | 368 | 67.1% |
| human vs ChatGPT | 368 | 73.4% |
| **Gemini vs ChatGPT** | 368 | **79.1%** |

### `gold_commitment` — Cohen's kappa

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 368 | 70.7% | **0.389** |
| human vs ChatGPT | 368 | 78.8% | **0.461** |
| **Gemini vs ChatGPT** | 368 | 82.6% | **0.651** |

**The two AI reviewers agree with each other markedly more than either agrees
with the human** — κ 0.651 against 0.389 / 0.461. This is the
correlated-failure-mode caveat confirmed: they are not independent raters,
and their mutual agreement is partly agreement on a shared bias. Human–AI κ
also sits *below* the 0.53–0.59 that two blinded humans reached on this same
judgement in the parent project.

### `keep_or_exclude` — kappa at chance

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 368 | 67.1% | **0.037** |
| human vs ChatGPT | 368 | 66.3% | **−0.010** |
| Gemini vs ChatGPT | 368 | 75.3% | 0.443 |

Raw agreement near 66% looks acceptable and means nothing. The marginals:

| reviewer | keep | exclude | exclude rate |
|---|---|---|---|
| human | 363 | 5 | **1.4%** |
| Gemini | 244 | 124 | **33.7%** |
| ChatGPT | 247 | 121 | **32.9%** |

κ ≈ 0 means that **on which specific items to exclude, the human and the AI
reviewers agree at chance** — ChatGPT marginally worse. Their exclusions are
largely downstream of their own inability to answer.

**Do not use AI `keep_or_exclude` as an exclusion signal.** It carries no
information about the human's criterion.

---

## Promotion classes (routing only)

| class | items |
|---|---|
| `strong_keep` | 180 |
| `review_needed` | 106 |
| `exclude` | 82 |

By transformation:

| transformation | strong_keep | review_needed | exclude |
|---|---|---|---|
| numeric_to_directional (140) | **124** | 11 | 5 |
| evidence_masked_insufficient (93) | 31 | 18 | 44 |
| none (135) | 25 | 77 | 33 |

By benchmark:

| benchmark | strong_keep | review_needed | exclude |
|---|---|---|---|
| convfinqa (60) | 50 | 6 | 4 |
| finqa (75) | 56 | 8 | 11 |
| tatqa (75) | 46 | 13 | 16 |
| financebench (59) | 26 | 13 | 20 |
| **fintradebench (99)** | **2** | 66 | 31 |

**Read the FinTradeBench row with Finding 1 in hand.** 2 `strong_keep` of 99
is not evidence those items are bad — it is the arithmetic consequence of
Gemini declining 96% of the lane, since an item cannot reach `strong_keep`
when a reviewer who refused to answer counts as disagreeing.

The directional lanes are where the classes mean what they appear to:
**124 of 140 `strong_keep`**.

---

## Changes applied to the human sheet

Backed up first to
`hedgeqa_core_v0_1_manual_review_completed.pre_convention_backup.csv`.

| change | rows |
|---|---|
| `roughly_unchanged` commitment remapped to `committed` | 11 |
| blank `keep_or_exclude` set to `keep` (reviewer: blank means keep) | 9 |
| `gold_commitment_auto` / `noncommit_labels` refreshed to the new convention | 27 |

The 9 keep-defaults are noted in each row's `notes`. They were blank because
the review app's validation required the label, commitment and
evidence-sufficiency fields but **not `keep_or_exclude` itself** — a gap in
the validation spec as I implemented it.

### Three commitment/label inconsistencies remain, deliberately

These are outside the `roughly_unchanged` convention and are the reviewer's
own calls, so they were left alone:

| item | label | recorded | implied by schema |
|---|---|---|---|
| `hqa_FTB_6f71b24d` | `unsupportive` | noncommitted | committed |
| `hqa_FTB_8c3f38fa` | `mixed` | committed | noncommitted |
| `hqa_FTB_90f40b4c` | `mixed` | committed | noncommitted |

If `mixed` should also be committed — the same argument that carried for
`roughly_unchanged` applies less clearly, since "both effects are present"
genuinely does not settle which dominates — say so and it will be applied
schema-wide. Otherwise these three want a second look.

---

## Recommended next steps

1. **Act on the masked variants.** Exclude the 44 the human judged
   answerable; mine their flags for missed leak routes; extend `masking.py`
   before constructing more.
2. **Decide the three remaining inconsistencies** above.
3. **Re-scope the AI review.** Keep it for TAT-QA / FinQA / ConvFinQA. Drop
   it as adjudication for FinTradeBench; treat Gemini's FinanceBench numbers
   with caution.
4. **Write up Finding 1.** It is a genuine, if accidental, contribution.
5. **Then** decide promotions item by item, by hand. Nothing here promotes
   anything.
