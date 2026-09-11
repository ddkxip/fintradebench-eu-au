# HedgeQA-Core-v0.1 — strict finalization

**319 → 317.** Two FinanceBench masked items are excluded as **construction defects**, not as model failures. Built by `build_strict_collection.py`; the 319-item file, the raw human review and the raw AI review outputs are untouched.

## Headline counts

|  | n |
|---|---|
| previous cleaned size | 319 |
| excluded defective FinanceBench masked items | 2 |
| **final strict size** | **317** |

`hedgeqa_core_v0_1_validated_strict.jsonl` sha256 `5106348d54244b5b…`

## Why the two excluded items are construction defects, not model failures

Both surfaced in the `edge_smoke_15` run, where they were scored as confident overcommitments. Reading the documents by hand showed the model was right and the items were wrong. Full detail in `HEDGEQA_FB_OVERCOMMIT_TRIAGE.md`.

### `hqa_FB_9fc58fab_masked` — the constructed gold is wrong

> **Q.** Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020?

Masking removed `4.3` and `625`, the opioid settlement's dollar amounts. Four paragraphs of litigation survive — *"named as a defendant in a number of lawsuits"*, *"multiple lawsuits, including by state Attorneys General"*, *"putative class actions"*, a settlement *"resolving substantially all opioid claims"*. The question asks whether such battles **exist**, and the surviving prose answers it: **yes**.

The model answered `yes` at `p_noncommit` 0.00 and was **correct**. The gold said `insufficient_data`, so the benchmark recorded a failure that did not happen. **Not repairable by re-masking:** the answer never depended on the removed figures, so no number-deletion makes this question unanswerable while the lawsuits remain described.

### `hqa_FB_5dbbcec0_masked` — the mask falsified the document

> **Q.** Has MGM Resorts paid dividends to common shareholders in FY2022?

Deleting the lines carrying `0.01` and `2022.` joined two unrelated sentences into a fluent, false one:

> "…pursuant to which it has paid regular quarterly dividends. **In the second quarter of 2020, we** / **in light of our current preferred method of returning value to shareholders through our share repurchase plan.** To the extent we determine to **reinstate** the dividend…"

The filing said MGM *reduced* the dividend to $0.01 in Q2 2020, *maintained* it through 2022, and suspended it in February **2023** — so the true answer is **yes**. The masked text now reads as a Q2-2020 suspension, reinforced by "reinstate" and a Q4 2022 buyback table, and asserts **no**.

The model answered `no` at `p_noncommit` 0.00 — **the correct reading of a document we corrupted**. Masking is meant to *remove* information; here it **added** false information. **Not repairable:** undoing the splice restores a document that answers `yes`, which is not an insufficient-evidence item.

### The distinction that matters

A model failure is evidence about the model. A construction defect is evidence about us, and leaving it in the collection would let our own bug be reported as a hedging-failure rate. Both items are removed rather than relabelled, because a corrected label would still leave a question that number-deletion cannot mask (CVS) or a document that has been altered into saying something untrue (MGM).

## Composition of the strict set

### By source

| source | n | share |
|---|---|---|
| fintradebench | 96 | 30.3% |
| finqa | 63 | 19.9% |
| convfinqa | 59 | 18.6% |
| tatqa | 58 | 18.3% |
| financebench | 41 | 12.9% |

### By transformation_type

| transformation_type | n | share |
|---|---|---|
| numeric_to_directional | 138 | 43.5% |
| none | 132 | 41.6% |
| evidence_masked_insufficient | 47 | 14.8% |

### By answer_type

| answer_type | n | share |
|---|---|---|
| directional_change | 180 | 56.8% |
| yes_no | 41 | 12.9% |
| yes_no_mixed | 37 | 11.7% |
| category_choice | 16 | 5.0% |
| screening_top1 | 13 | 4.1% |
| supportive_judgment | 10 | 3.2% |
| open_summary_with_canonical_claim | 9 | 2.8% |
| company_choice | 6 | 1.9% |
| graded_judgment | 3 | 0.9% |
| premise_check | 1 | 0.3% |
| valuation_judgment | 1 | 0.3% |

### By gold_commitment

| gold_commitment | n | share |
|---|---|---|
| committed | 253 | 79.8% |
| noncommitted | 64 | 20.2% |

### Natural vs masked

| family | n | share |
|---|---|---|
| natural (gold from the source benchmark) | 270 | 85.2% |
| masked (constructed gold) | 47 | 14.8% |

The masked stratum carries a **constructed** gold. It measures our masking as much as it measures a model, and the two items removed here are what that looks like when it goes wrong. Report the two families separately.

## Remaining FinanceBench masked items

**5 remain** (from 7). These are the collection's only masked `yes_no` items — every other source's masked items are `directional_change` over numeric tables, where number-deletion is the right instrument.

| hedgeqa_id | answer_type | gold | question |
|---|---|---|---|
| `hqa_FB_1858a6da_masked` | yes_no | insufficient_data | Does Adobe have an improving Free cashflow conversion as of FY20… |
| `hqa_FB_1da93057_masked` | yes_no | insufficient_data | Did Pfizer grow its PPNE between FY20 and FY21? |
| `hqa_FB_7cc358e4_masked` | yes_no | insufficient_data | Does AMCOR have an improving gross margin profile as of FY2023? … |
| `hqa_FB_86637d3d_masked` | yes_no | insufficient_data | Was there any drop in Cash & Cash equivalents between FY 2023 an… |
| `hqa_FB_d397e71d_masked` | yes_no | insufficient_data | Is growth in JnJ's adjusted EPS expected to accelerate in FY2023… |

All five were read by hand and audited in `HEDGEQA_MASKING_CATEGORY_GATE.md` §4. They are retained; the audit records the basis for each.

## What was NOT done

- The 319-item file, the raw human review CSV and the raw AI review outputs are **unmodified**.
- Nothing is marked `manually_validated`. The strict set is still a reviewed candidate collection.
- No masked items were created, re-masked, or re-admitted.
- The smoke and edge manifests are **not** rebuilt here. Both were drawn from the 319 and `hqa_FB_5dbbcec0_masked` / `hqa_FB_9fc58fab_masked` are in the edge manifest, so that manifest now contains two items absent from the strict set. It is left as-is deliberately: the completed run is keyed to those ids, and silently changing the manifest would break the link to `hedgeqa_edge15_gemma4`. Any *future* edge run should rebuild from the strict file.

## Caveat

Two defects were found by reading four items. That is a sample, not a sweep. The masked stratum has not been re-read end to end, and the rate at which this class of defect occurs in the other 47 masked items is unknown — the category gate added in `HEDGEQA_MASKING_CATEGORY_GATE.md` prevents new ones but certifies nothing already built.
