# HedgeQA-Core-v0.1 — AI-assisted review agreement report

**These are AI-assisted audit labels, not human ground truth.** Gemini and ChatGPT are used to locate disagreement for a human to adjudicate. No item is promoted on the strength of AI agreement, and nothing in this pipeline sets `manually_validated`.

## Coverage

| reviewer | items reviewed | of |
|---|---|---|
| human | 368 | 368 |
| gemini_antigravity | 368 | 368 |
| chatgpt_codex | 368 | 368 |

## 1. Agreement on `gold_label`

Raw agreement only. Kappa is not defined here: the answer space is per-item and 46 distinct labels appear across the core, so there is no shared category set to compute chance agreement over. Raw agreement also **overstates skill**, because most items admit only 2-4 plausible labels.

| comparison | n | raw agreement |
|---|---|---|
| human vs Gemini | 368 | 67.1% |
| human vs ChatGPT | 368 | 73.4% |
| Gemini vs ChatGPT | 368 | 79.1% |

## 2. Agreement on `gold_commitment`

Three shared categories, so kappa is meaningful. This is the collection's load-bearing judgement; in the parent project two blinded human annotators reached only kappa 0.53-0.59 on it, so **moderate agreement here is the expected result, not a failure**.

| comparison | n | raw agreement | Cohen kappa |
|---|---|---|---|
| human vs Gemini | 368 | 70.9% | 0.395 |
| human vs ChatGPT | 368 | 79.1% | 0.469 |
| Gemini vs ChatGPT | 368 | 82.6% | 0.651 |

## 3. Agreement on `keep_or_exclude`

| comparison | n | raw agreement | Cohen kappa |
|---|---|---|---|
| human vs Gemini | 368 | 67.1% | 0.037 |
| human vs ChatGPT | 368 | 66.3% | -0.010 |
| Gemini vs ChatGPT | 368 | 75.3% | 0.443 |

## 4. Disagreement rate by stratum

Disagreement = the two raters recorded different `gold_label`, over items where both recorded one.

### By source benchmark

| stratum | n | human-Gemini | human-ChatGPT | Gemini-ChatGPT |
|---|---|---|---|---|
| convfinqa | 60 | 6.7% (n=60) | 0.0% (n=60) | 6.7% (n=60) |
| financebench | 59 | 22.0% (n=59) | 6.8% (n=59) | 25.4% (n=59) |
| finqa | 75 | 8.0% (n=75) | 8.0% (n=75) | 9.3% (n=75) |
| fintradebench | 99 | 90.9% (n=99) | 80.8% (n=99) | 39.4% (n=99) |
| tatqa | 75 | 10.7% (n=75) | 10.7% (n=75) | 16.0% (n=75) |

### By transformation type

| stratum | n | human-Gemini | human-ChatGPT | Gemini-ChatGPT |
|---|---|---|---|---|
| evidence_masked_insufficient | 93 | 8.6% (n=93) | 10.8% (n=93) | 19.4% (n=93) |
| none | 135 | 75.6% (n=135) | 60.0% (n=135) | 37.0% (n=135) |
| numeric_to_directional | 140 | 7.9% (n=140) | 5.0% (n=140) | 6.4% (n=140) |

### Masked variants specifically

93 masked items. These carry a CONSTRUCTED gold, so the question is not only whether raters agree but whether any of them found a route to the answer.

| comparison | n | disagreement on `masked_variant_valid` |
|---|---|---|
| human vs Gemini | 93 | 7.5% |
| human vs ChatGPT | 93 | 17.2% |
| Gemini vs ChatGPT | 93 | 22.6% |

**59 masked item(s) had at least one reviewer report the answer was still reachable.** Every one of these should be excluded or re-masked; a single credible reconstruction route falsifies the constructed gold.

### numeric_to_directional specifically

140 items. The failure mode here is a direction inverted by operand order, which produces a confidently wrong label.

| comparison | n | disagreement on `transformation_valid` |
|---|---|---|
| human vs Gemini | 140 | 7.9% |
| human vs ChatGPT | 140 | 4.3% |
| Gemini vs ChatGPT | 140 | 5.0% |

## 5. Flags raised by AI reviewers

| flag | count |
|---|---|
| `answer_reconstructible` | 68 |
| `evidence_gutted` | 16 |
| `total_minus_components` | 11 |
| `cross_sectional_not_temporal` | 7 |
| `label_outside_answer_space` | 5 |
| `direction_stated_in_prose` | 2 |
| `question_presupposes_direction` | 2 |
| `evidence_truncated` | 1 |
| `operand_order_suspect` | 1 |

## 6. High-risk disagreements

Ranked: a masked item any reviewer could answer, then a directional item whose transformation is challenged, then any three-way `gold_label` split, then commitment splits.

| # | hedgeqa_id | transformation | issue |
|---|---|---|---|
| 1 | `hqa_CFQ_3240be6a_masked` | evidence_masked_insufficient | masked item reported answerable |
| 2 | `hqa_CFQ_6e99706b_masked` | evidence_masked_insufficient | masked item reported answerable |
| 3 | `hqa_CFQ_7897a7cc_masked` | evidence_masked_insufficient | masked item reported answerable |
| 4 | `hqa_CFQ_7f731a74_masked` | evidence_masked_insufficient | masked item reported answerable |
| 5 | `hqa_CFQ_b7e2687e_masked` | evidence_masked_insufficient | masked item reported answerable |
| 6 | `hqa_CFQ_f9c627e5_masked` | evidence_masked_insufficient | masked item reported answerable |
| 7 | `hqa_FB_27095e41_masked` | evidence_masked_insufficient | masked item reported answerable |
| 8 | `hqa_FB_2efc769e_masked` | evidence_masked_insufficient | masked item reported answerable |
| 9 | `hqa_FB_435b88c4_masked` | evidence_masked_insufficient | masked item reported answerable |
| 10 | `hqa_FB_4755512d_masked` | evidence_masked_insufficient | masked item reported answerable |
| 11 | `hqa_FB_49becde3_masked` | evidence_masked_insufficient | masked item reported answerable |
| 12 | `hqa_FB_50664e43_masked` | evidence_masked_insufficient | masked item reported answerable |
| 13 | `hqa_FB_5dbbcec0_masked` | evidence_masked_insufficient | masked item reported answerable |
| 14 | `hqa_FB_6358a99a_masked` | evidence_masked_insufficient | masked item reported answerable |
| 15 | `hqa_FB_84463d0e_masked` | evidence_masked_insufficient | masked item reported answerable |
| 16 | `hqa_FB_93bd00fd_masked` | evidence_masked_insufficient | masked item reported answerable |
| 17 | `hqa_FB_9ef802db_masked` | evidence_masked_insufficient | masked item reported answerable |
| 18 | `hqa_FB_9fc58fab_masked` | evidence_masked_insufficient | masked item reported answerable |
| 19 | `hqa_FB_a7999aa2_masked` | evidence_masked_insufficient | masked item reported answerable |
| 20 | `hqa_FB_cb5deceb_masked` | evidence_masked_insufficient | masked item reported answerable |
| 21 | `hqa_FB_cfe29aff_masked` | evidence_masked_insufficient | masked item reported answerable |
| 22 | `hqa_FB_d397e71d_masked` | evidence_masked_insufficient | masked item reported answerable |
| 23 | `hqa_FB_e3f5b062_masked` | evidence_masked_insufficient | masked item reported answerable |
| 24 | `hqa_FB_e671ffe0_masked` | evidence_masked_insufficient | masked item reported answerable |
| 25 | `hqa_FB_f0c3b380_masked` | evidence_masked_insufficient | masked item reported answerable |
| 26 | `hqa_FQ_1a22ef34_masked` | evidence_masked_insufficient | masked item reported answerable |
| 27 | `hqa_FQ_2eaf4c8c_masked` | evidence_masked_insufficient | masked item reported answerable |
| 28 | `hqa_FQ_34845583_masked` | evidence_masked_insufficient | masked item reported answerable |
| 29 | `hqa_FQ_425a8ac9_masked` | evidence_masked_insufficient | masked item reported answerable |
| 30 | `hqa_FQ_6b2ec826_masked` | evidence_masked_insufficient | masked item reported answerable |
| 31 | `hqa_FQ_aa3e2bfa_masked` | evidence_masked_insufficient | masked item reported answerable |
| 32 | `hqa_FQ_b48cf832_masked` | evidence_masked_insufficient | masked item reported answerable |
| 33 | `hqa_FQ_c3975ba4_masked` | evidence_masked_insufficient | masked item reported answerable |
| 34 | `hqa_FQ_c635a8df_masked` | evidence_masked_insufficient | masked item reported answerable |
| 35 | `hqa_FQ_e59a4f4f_masked` | evidence_masked_insufficient | masked item reported answerable |
| 36 | `hqa_FQ_fa1ef8b2_masked` | evidence_masked_insufficient | masked item reported answerable |
| 37 | `hqa_TAT_05876add_masked` | evidence_masked_insufficient | masked item reported answerable |
| 38 | `hqa_TAT_19b2dd4a_masked` | evidence_masked_insufficient | masked item reported answerable |
| 39 | `hqa_TAT_1e9ec6bd_masked` | evidence_masked_insufficient | masked item reported answerable |
| 40 | `hqa_TAT_1eb0a8a9_masked` | evidence_masked_insufficient | masked item reported answerable |
| 41 | `hqa_TAT_1f0fd903_masked` | evidence_masked_insufficient | masked item reported answerable |
| 42 | `hqa_TAT_30ff91f5_masked` | evidence_masked_insufficient | masked item reported answerable |
| 43 | `hqa_TAT_3f358251_masked` | evidence_masked_insufficient | masked item reported answerable |
| 44 | `hqa_TAT_4e15b114_masked` | evidence_masked_insufficient | masked item reported answerable |
| 45 | `hqa_TAT_5ce27434_masked` | evidence_masked_insufficient | masked item reported answerable |
| 46 | `hqa_TAT_7cc28393_masked` | evidence_masked_insufficient | masked item reported answerable |
| 47 | `hqa_TAT_819756ff_masked` | evidence_masked_insufficient | masked item reported answerable |
| 48 | `hqa_TAT_83225fed_masked` | evidence_masked_insufficient | masked item reported answerable |
| 49 | `hqa_TAT_863ac028_masked` | evidence_masked_insufficient | masked item reported answerable |
| 50 | `hqa_TAT_924db34b_masked` | evidence_masked_insufficient | masked item reported answerable |
| 51 | `hqa_TAT_9410c4da_masked` | evidence_masked_insufficient | masked item reported answerable |
| 52 | `hqa_TAT_a757ebed_masked` | evidence_masked_insufficient | masked item reported answerable |
| 53 | `hqa_TAT_a8d33126_masked` | evidence_masked_insufficient | masked item reported answerable |
| 54 | `hqa_TAT_b1f0677c_masked` | evidence_masked_insufficient | masked item reported answerable |
| 55 | `hqa_TAT_b5e1cbd8_masked` | evidence_masked_insufficient | masked item reported answerable |
| 56 | `hqa_TAT_bf17a5c6_masked` | evidence_masked_insufficient | masked item reported answerable |
| 57 | `hqa_TAT_d24aae82_masked` | evidence_masked_insufficient | masked item reported answerable |
| 58 | `hqa_TAT_f0b19718_masked` | evidence_masked_insufficient | masked item reported answerable |
| 59 | `hqa_TAT_f4ec2a00_masked` | evidence_masked_insufficient | masked item reported answerable |
| 60 | `hqa_CFQ_525e330f` | numeric_to_directional | directional transformation challenged |

…and 120 more; the full list is the `review_needed` rows of the merged CSV.

## 7. Promotion classes

| class | items | meaning |
|---|---|---|
| `strong_keep` | 180 | human + both AI kept, commitment agrees — *eligible* for human promotion |
| `review_needed` | 106 | disagreement, missing reviewer, low confidence, or an `unclear` flag |
| `exclude` | 82 | human excluded, or both AI reviewers excluded |

`strong_keep` means **nobody objected**, which is weaker than verified. Two of the three raters are language models with correlated failure modes, so unanimity among them is not independent confirmation. A human still decides every promotion, and no item in this repository is `manually_validated`.

