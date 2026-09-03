# HedgeQA-Core-v0.1 — AI-assisted review agreement report

**These are AI-assisted audit labels, not human ground truth.** Gemini and ChatGPT are used to locate disagreement for a human to adjudicate. No item is promoted on the strength of AI agreement, and nothing in this pipeline sets `manually_validated`.

## Coverage

| reviewer | items reviewed | of |
|---|---|---|
| human | 0 | 368 |
| gemini_antigravity | 0 | 368 |
| chatgpt_codex | 0 | 368 |

> **Incomplete.** Every figure below is computed only over items where both members of a pair recorded a label. Comparisons with zero overlap are reported as `n/a`, never as agreement.

## 1. Agreement on `gold_label`

Raw agreement only. Kappa is not defined here: the answer space is per-item and 46 distinct labels appear across the core, so there is no shared category set to compute chance agreement over. Raw agreement also **overstates skill**, because most items admit only 2-4 plausible labels.

| comparison | n | raw agreement |
|---|---|---|
| human vs Gemini | 0 | n/a |
| human vs ChatGPT | 0 | n/a |
| Gemini vs ChatGPT | 0 | n/a |

## 2. Agreement on `gold_commitment`

Three shared categories, so kappa is meaningful. This is the collection's load-bearing judgement; in the parent project two blinded human annotators reached only kappa 0.53-0.59 on it, so **moderate agreement here is the expected result, not a failure**.

| comparison | n | raw agreement | Cohen kappa |
|---|---|---|---|
| human vs Gemini | 0 | n/a | n/a |
| human vs ChatGPT | 0 | n/a | n/a |
| Gemini vs ChatGPT | 0 | n/a | n/a |

## 3. Agreement on `keep_or_exclude`

| comparison | n | raw agreement | Cohen kappa |
|---|---|---|---|
| human vs Gemini | 0 | n/a | n/a |
| human vs ChatGPT | 0 | n/a | n/a |
| Gemini vs ChatGPT | 0 | n/a | n/a |

## 4. Disagreement rate by stratum

Disagreement = the two raters recorded different `gold_label`, over items where both recorded one.

### By source benchmark

| stratum | n | human-Gemini | human-ChatGPT | Gemini-ChatGPT |
|---|---|---|---|---|
| convfinqa | 60 | n/a | n/a | n/a |
| financebench | 59 | n/a | n/a | n/a |
| finqa | 75 | n/a | n/a | n/a |
| fintradebench | 99 | n/a | n/a | n/a |
| tatqa | 75 | n/a | n/a | n/a |

### By transformation type

| stratum | n | human-Gemini | human-ChatGPT | Gemini-ChatGPT |
|---|---|---|---|---|
| evidence_masked_insufficient | 93 | n/a | n/a | n/a |
| none | 135 | n/a | n/a | n/a |
| numeric_to_directional | 140 | n/a | n/a | n/a |

### Masked variants specifically

93 masked items. These carry a CONSTRUCTED gold, so the question is not only whether raters agree but whether any of them found a route to the answer.

| comparison | n | disagreement on `masked_variant_valid` |
|---|---|---|
| human vs Gemini | 0 | n/a |
| human vs ChatGPT | 0 | n/a |
| Gemini vs ChatGPT | 0 | n/a |

**0 masked item(s) had at least one reviewer report the answer was still reachable.** Every one of these should be excluded or re-masked; a single credible reconstruction route falsifies the constructed gold.

### numeric_to_directional specifically

140 items. The failure mode here is a direction inverted by operand order, which produces a confidently wrong label.

| comparison | n | disagreement on `transformation_valid` |
|---|---|---|
| human vs Gemini | 0 | n/a |
| human vs ChatGPT | 0 | n/a |
| Gemini vs ChatGPT | 0 | n/a |

## 6. High-risk disagreements

Ranked: a masked item any reviewer could answer, then a directional item whose transformation is challenged, then any three-way `gold_label` split, then commitment splits.

None recorded. With incomplete reviewer coverage this means *not yet computable*, not *no disagreement*.

## 7. Promotion classes

| class | items | meaning |
|---|---|---|
| `strong_keep` | 0 | human + both AI kept, commitment agrees — *eligible* for human promotion |
| `review_needed` | 368 | disagreement, missing reviewer, low confidence, or an `unclear` flag |
| `exclude` | 0 | human excluded, or both AI reviewers excluded |

`strong_keep` means **nobody objected**, which is weaker than verified. Two of the three raters are language models with correlated failure modes, so unanimity among them is not independent confirmation. A human still decides every promotion, and no item in this repository is `manually_validated`.

