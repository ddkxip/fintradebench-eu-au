# HedgeQA-Core-v0.1 — selection report

**Status: CANDIDATE-ONLY. Nothing here is `manually_validated`.**
This document describes the *review set*. The human review is now complete —
see `ai_review/HUMAN_REVIEW_FINDINGS.md` for its results. Figures below were
revised in 2026-09 when `roughly_unchanged` was reclassified as committed.

368 items drawn from the 1,658-item v0.1 candidate collection, small enough
to review completely by hand while still supporting every hedging metric
per benchmark.

Built by `build_core_collection.py`; two consecutive builds are
byte-identical.

---

## 1. Counts by source

| source | core | full pool | core share | drawn from |
|---|---|---|---|---|
| fintradebench | 99 | 99 | 26.9% | all of it |
| financebench | 59 | 59 | 16.0% | all of it |
| tatqa | 75 | 500 | 20.4% | 15% sample |
| finqa | 75 | 500 | 20.4% | 15% sample |
| convfinqa | 60 | 500 | 16.3% | 12% sample |
| **total** | **368** | 1,658 | 100% | |

No benchmark exceeds 27%, against 30% in the full collection where the three
directional sources held 90% between them.

## 2. Counts by answer_type

| answer_type | items |
|---|---|
| directional_change | 210 |
| yes_no | 59 |
| yes_no_mixed | 37 |
| category_choice | 16 |
| screening_top1 | 15 |
| supportive_judgment | 10 |
| open_summary_with_canonical_claim | 9 |
| company_choice | 6 |
| graded_judgment | 4 |
| valuation_judgment | 1 |
| premise_check | 1 |

`directional_change` falls from **90.5% of the full collection to 57.1%**
here. The judgement types that were under 6% of v0.1 are 27% of the core, so
a pooled statistic is no longer a near-pure measurement of one answer type.

## 3. Counts by transformation_type

| transformation_type | items |
|---|---|
| numeric_to_directional | 140 |
| none | 135 |
| evidence_masked_insufficient | 93 |

## 4. Counts by gold_commitment

| gold_commitment | items | share |
|---|---|---|
| committed | 256 | 69.6% |
| noncommitted | 112 | 30.4% |

## 5. Natural vs masked

| source | natural | masked | total |
|---|---|---|---|
| fintradebench | 99 | 0 | 99 |
| financebench | 36 | 23 | 59 |
| tatqa | 50 | 25 | 75 |
| finqa | 50 | 25 | 75 |
| convfinqa | 40 | 20 | 60 |
| **total** | **275** | **93** | **368** |

The two are separable by `transformation_type` and must stay separated in
analysis: a masked item's gold is constructed, so pooling it into a
non-commitment rate reports a property of our masking rather than of a model.

Natural directional label balance:

| source | increased | decreased | roughly_unchanged |
|---|---|---|---|
| tatqa | 17 | 17 | 16 |
| finqa | 21 | 20 | 9 |
| convfinqa | 19 | 19 | 2 |

`roughly_unchanged` is scarce upstream (only 9 and 2 exist in the whole FinQA
and ConvFinQA eligible pools); every available one was taken.

## 6. Majority-class baseline by source

| source | items | majority label | baseline | distinct labels |
|---|---|---|---|---|
| fintradebench | 99 | `no` | **14.1%** | 43 |
| financebench | 59 | `yes` | **42.4%** | 3 |
| tatqa | 75 | `insufficient_data` | **33.3%** | 4 |
| finqa | 75 | `insufficient_data` | **33.3%** | 4 |
| convfinqa | 60 | `insufficient_data` | **33.3%** | 4 |
| pooled | 368 | `insufficient_data` | 25.8% | 46 |

No component is passable by guessing one label. The directional benchmarks
sit at exactly 1/3 because the masked variants make `insufficient_data` a
third of each — which also means **a system that always says
`insufficient_data` scores 33% there**, so a hedging model will look
deceptively good on those three unless the natural/masked split is reported
separately. It must be.

## 7. Non-committal share by source

| source | items | non-committal | share | masked | natural n-c | natural share |
|---|---|---|---|---|---|---|
| fintradebench | 99 | 19 | 19.2% | 0 | 19 | 19.2% |
| financebench | 59 | 23 | 39.0% | 23 | 0 | **0.0%** |
| tatqa | 75 | 25 | 33.3% | 25 | 0 | **0.0%** |
| finqa | 75 | 25 | 33.3% | 25 | 0 | **0.0%** |
| convfinqa | 60 | 20 | 33.3% | 20 | 0 | **0.0%** |
| pooled | 368 | 112 | 30.4% | 93 | 19 | **6.9%** |

*(Revised 2026-09: `roughly_unchanged` is committed, so the directional
lanes have no natural non-committal items at all.)*

The headline 30.4% is **83% constructed**. On natural items alone it is
**6.9%**, and **only FinTradeBench has any natural non-committal items
(19)**. So:

- **overcommitment** and **wrong non-committal type** are measurable on
  natural items **only for FinTradeBench**;
- for every other source they are measurable *only* through constructed
  items, i.e. only as strongly as the masking is trusted — and the human
  review found roughly half the masks answerable.

## 8. Evidence-sharing clusters

| source | items | distinct documents | items sharing | max per document |
|---|---|---|---|---|
| fintradebench | 99 | 78 | 38 | 3 |
| financebench | 59 | 59 | 0 | 1 |
| tatqa | 75 | 75 | 0 | 1 |
| finqa | 75 | 75 | 0 | 1 |
| convfinqa | 60 | 60 | 0 | 1 |
| **total** | **368** | **346** | **40** | **3** |

**Evidence sharing drops from 36.7% in the full collection to 10.9% here**,
and all of it is inside FinTradeBench, where several questions legitimately
target the same ticker and window. The four other sources have one document
per item.

`evidence_hash` (sha256[:12] of `oracle_evidence`) is recorded in the review
sheet so later analysis can cluster on it. For the core, clustering matters
only for FinTradeBench; elsewhere items are independent by construction.

## 9. Manual-review burden

| | items | evidence to read |
|---|---|---|
| natural | 275 | 363,718 chars |
| masked | 93 | 132,590 chars |
| **total** | **368** | **496,308 chars** (~124k words) |

Median evidence per item is 862 characters.

A rough single-reviewer estimate, to be treated as an order of magnitude
rather than a schedule:

| pass | scope | estimate |
|---|---|---|
| 1. gold + evidence sufficiency | all 368 | ~16 h |
| 2. masked-variant adjudication | 93 | ~15 h |
| 3. second opinion on `gold_commitment` | 150-item sample | ~6 h |
| | | **~37 h ≈ 5 working days** |

Masked items dominate per-item cost: judging whether evidence *cannot*
answer a question is strictly harder than checking a stated answer, because
the reviewer has to search for reconstruction routes rather than verify one
claim.

The review sheet is **ordered by review priority** — masked items first,
then natural non-committal golds, then transformed items, then the rest — so
a reviewer working top-down covers the highest-risk material first and a
partial review is still useful.

## 10. Why this core is suitable for first model runs

1. **Reviewable.** 368 items is a week of work, not a quarter. The full
   1,658 is not realistically reviewable, and running an unreviewed
   collection would produce numbers nobody can defend.
2. **No benchmark dominates.** 27% maximum, against 90% held by the
   directional sources in v0.1, so a pooled figure is no longer one
   benchmark wearing five names.
3. **Answer-type spread.** `directional_change` drops 90.5% → 57.1%, so the
   judgement-style questions the parent paper is actually about are properly
   represented.
4. **Hedge collision and wrong-direction commitment are computable in every
   source.** Overcommitment is not: after the 2026-09 convention revision
   only FinTradeBench has natural non-committal golds (19), so elsewhere that
   mode rests entirely on the constructed masked variants — roughly half of
   which the human review found answerable. See §7.
5. **Near-independent items.** 10.9% evidence sharing against 36.7%, and
   zero outside FinTradeBench, so confidence intervals need clustering only
   in one source.
6. **No degenerate baseline.** 14–42% majority-class across sources.
7. **Cheap to run.** ~496k characters of evidence total; at K=10/20 with two
   agents over two rounds this is roughly 15k model calls per system, versus
   ~66k for the full collection.

### What this core does NOT establish

- **It is not validated.** 275 items are `auto_validated` (structurally
  well-formed) and 93 are `candidate`. Zero are `manually_validated`. No
  result from these items should be reported before the review.

- **It is a biased subsample, deliberately.** Selection rule 4 prefers
  shorter evidence, and the effect is large:

  | source | core median | pool median | ratio |
  |---|---|---|---|
  | tatqa | 492 | 1,437 | **0.34x** |
  | convfinqa | 1,513 | 3,802 | **0.40x** |
  | finqa | 2,240 | 4,076 | **0.55x** |
  | pooled | 862 | 3,120 | 0.28x |

  FinTradeBench and FinanceBench are unaffected (taken whole). If hedging
  responds to context length — which is plausible and untested — **core
  results will not transfer to the full collection**, and a model may hedge
  measurably less here than on v0.1. Treat the core as a review and
  pilot instrument, and re-measure on the full collection before claiming
  anything about the larger set.

- **The 33.3% `insufficient_data` baseline on the directional sources is an
  artifact of the 2:1 natural:masked ratio**, not a property of the data.
  Always report natural and masked separately.
