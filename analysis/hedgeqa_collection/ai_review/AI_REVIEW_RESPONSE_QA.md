# AI review responses — structural QA

**Blind-safe report.** Structure only. No gold labels, no rationales, no per-item reviewer decisions, and no counts that would reveal a reviewer's overall stance. Rule violations are reported as counts so that a defect is visible without disclosing the content behind it.

**No agreement analysis is included.** The human review is not complete, and computing agreement now would put AI verdicts in front of the human reviewer, destroying their independence as a third rater. Run `analyze_ai_review_agreement.py` only after the human sheet is filled in.

## Summary

- response files: **32**
- expected batches: **16** x 2 reviewers = **32** files
- records parsed: **736** (gemini_antigravity: 368 / chatgpt_codex: 368)
- expected records: **736** (368 per reviewer)
- structural ERRORS: **0**
- structural WARNINGS: **0**

## Checks

| # | check | result |
|---|---|---|
| 1 | valid JSONL | PASS |
| 2 | exactly one JSON object per line | PASS |
| 3 | filename prefix matches `reviewer_name` | PASS |
| 4 | required fields present | PASS |
| 5 | no extra fields | PASS |
| 6 | enum values legal | PASS |
| 7 | flags from schema enum | PASS |
| 8 | every batch has both reviewer files | PASS |
| 9 | paired files share ids in the same order | PASS |
| 10 | no duplicate `hedgeqa_id` per reviewer | PASS |
| 11 | family-specific fields consistent | PASS |
| 12 | excluded rows carry a reason | PASS |
| 13 | kept rows have no reason | PASS |
| 14 | low-confidence keeps (counted, not an error) | 0 row(s) |

## Normalisation applied

`masked_answer_recoverable` did not occur. No normalisation was needed.

No other value was rewritten. Repairing a reviewer's output beyond this one documented alias would destroy the signal being collected.

## Batch pairing

| batch | family | expected | gemini | codex | pairing | same order |
|---|---|---|---|---|---|---|
| `directional_batch01` | numeric_to_directional | 25 | 25 | 25 | both | yes |
| `directional_batch02` | numeric_to_directional | 25 | 25 | 25 | both | yes |
| `directional_batch03` | numeric_to_directional | 25 | 25 | 25 | both | yes |
| `directional_batch04` | numeric_to_directional | 25 | 25 | 25 | both | yes |
| `directional_batch05` | numeric_to_directional | 25 | 25 | 25 | both | yes |
| `directional_batch06` | numeric_to_directional | 15 | 15 | 15 | both | yes |
| `masked_batch01` | evidence_masked_insufficient | 25 | 25 | 25 | both | yes |
| `masked_batch02` | evidence_masked_insufficient | 25 | 25 | 25 | both | yes |
| `masked_batch03` | evidence_masked_insufficient | 25 | 25 | 25 | both | yes |
| `masked_batch04` | evidence_masked_insufficient | 18 | 18 | 18 | both | yes |
| `natural_batch01` | none | 25 | 25 | 25 | both | yes |
| `natural_batch02` | none | 25 | 25 | 25 | both | yes |
| `natural_batch03` | none | 25 | 25 | 25 | both | yes |
| `natural_batch04` | none | 25 | 25 | 25 | both | yes |
| `natural_batch05` | none | 25 | 25 | 25 | both | yes |
| `natural_batch06` | none | 10 | 10 | 10 | both | yes |

## Per-file record counts

| file | records | parse errors | schema errors |
|---|---|---|---|
| `chatgpt_codex__directional_batch01.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__directional_batch02.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__directional_batch03.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__directional_batch04.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__directional_batch05.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__directional_batch06.jsonl` | 15 | 0 | 0 |
| `chatgpt_codex__masked_batch01.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__masked_batch02.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__masked_batch03.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__masked_batch04.jsonl` | 18 | 0 | 0 |
| `chatgpt_codex__natural_batch01.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__natural_batch02.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__natural_batch03.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__natural_batch04.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__natural_batch05.jsonl` | 25 | 0 | 0 |
| `chatgpt_codex__natural_batch06.jsonl` | 10 | 0 | 0 |
| `gemini_antigravity__directional_batch01.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__directional_batch02.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__directional_batch03.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__directional_batch04.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__directional_batch05.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__directional_batch06.jsonl` | 15 | 0 | 0 |
| `gemini_antigravity__masked_batch01.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__masked_batch02.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__masked_batch03.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__masked_batch04.jsonl` | 18 | 0 | 0 |
| `gemini_antigravity__natural_batch01.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__natural_batch02.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__natural_batch03.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__natural_batch04.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__natural_batch05.jsonl` | 25 | 0 | 0 |
| `gemini_antigravity__natural_batch06.jsonl` | 10 | 0 | 0 |

## Flag vocabulary

Only whether the flag vocabulary is legal. **Per-flag frequencies are deliberately withheld**: a count like `answer_reconstructible: N` would tell the human reviewer how many masked items an AI judged answerable, which is precisely the substantive finding their own masked-item pass is supposed to reach independently. Those counts belong in the agreement report, after the human review is recorded.

- distinct flag names used: **9** of 17 available in the schema
- flag occurrences in total: **113** (across 736 records, both reviewers pooled)
- names outside the schema enum: none

## File-level problems

None.

## What this report does not tell you

- whether the reviewers agreed with each other or with the pipeline;
- what any reviewer decided about any item;
- how many items either reviewer would exclude.

All of that waits until the human review is recorded. Reading it first would make the human a second reader of the AI output rather than an independent rater, and the agreement numbers would no longer mean what they appear to mean.
