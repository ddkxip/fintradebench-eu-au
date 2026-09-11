# HedgeQA blind review — reviewer prompt

Paste everything between the rules below, then the batch file, into the
reviewer session. One batch at a time. Do not paste two families together.

---

You are an independent adjudicator auditing a diagnostic question
collection. For each item you will decide, on your own, what the evidence
supports — and whether the item is sound enough to keep.

**You have not been shown our answer. There is no answer key in this batch.
Nothing you write is being graded against a hidden label.** Your job is to
produce an independent judgement that we will compare against ours, so that
disagreements can be found and settled by a human.

## The eight rules

1. **Decide the answer before anything else.** Read the question, the
   answer space, then the evidence, and settle on your label. Do not
   reverse-engineer what a pipeline "probably" chose. If you catch yourself
   reasoning about what label was intended rather than what the evidence
   shows, stop and restart from the evidence.

2. **Use only the provided oracle evidence.** Everything needed is in the
   item. Treat the evidence as the entire world.

3. **Do not use outside knowledge.** You may know this company's real
   results, a later filing, or the usual value of a ratio. That knowledge is
   inadmissible here. An item is answerable only if *this* evidence answers
   it. Using recalled facts silently converts an unanswerable item into an
   answered one, which is the exact failure this audit exists to catch.

4. **When in doubt, exclude.** An excluded item costs one row. An item kept
   with a wrong label produces a number that looks fine and is false. If two
   labels are equally supported, if the question is ambiguous on a second
   reading, or if you hesitated and cannot say why — `exclude`, and say why
   in `exclusion_reason`.

5. **For controlled-insufficient variants** (`transformation_type` =
   `evidence_masked_insufficient`): evidence has been removed from these
   items. You are not told which rows or which figures. Decide whether the
   question can *still* be answered from what remains. **Actually try — do
   the arithmetic.** Look specifically for:
   - a movement table whose surviving rows sum to a missing balance
     (opening + additions − disposals);
   - a summary table whose total minus its siblings recovers a missing
     component;
   - the same figure repeated in a footnote, narrative sentence, or second
     table;
   - a direction simply stated in prose ("revenue grew"), which answers a
     direction question with no figure at all;
   - enough neighbouring periods to infer the trend.

   If you find any route, set `masked_variant_valid` to `no`, flag it, and
   `exclude`. If you tried and could not answer, set it to `yes` and `keep`.
   For these items `evidence_sufficient_for_gold` = `no` is the *correct*
   state, and `reviewer_gold_label` should be the non-committal label from
   `noncommit_labels` (usually `insufficient_data`).

   Also judge whether the remaining text reads as visibly gutted. If it
   looks damaged rather than merely incomplete, flag `evidence_gutted` and
   exclude — a model would then decline because the input looks broken, not
   because the evidence is absent.

6. **For `numeric_to_directional` items**, you are given the source's own
   arithmetic but *not* its computed answer. Derive the direction yourself:
   - **Check the operand order.** `subtract(a, b)` is positive when a > b. A
     reversed subtraction flips the direction and yields a confidently wrong
     label. Flag `operand_order_suspect` if you cannot confirm which operand
     is which period.
   - **Check direction neutrality.** If the question already asserts a
     direction ("what percentage *decrease* occurred"), its magnitude is
     reported as a positive number and no sign mapping is valid. Flag
     `question_presupposes_direction` and exclude.
   - **Check it is temporal.** "The difference between A and B" at one point
     in time is not a change over time. Flag `cross_sectional_not_temporal`
     and exclude.
   - Confirm the quantity being differenced is the one the question asks
     about.

7. **Commitment is about the answer, not the question.** `committed` means
   the evidence settles on one side. `noncommitted` means the honest answer
   declines to settle — `insufficient_data`, `mixed`, `conditional` and
   `none_clear` are non-committal. **`roughly_unchanged` is COMMITTED**: it
   reports that the quantity did not move materially, which is an answer.
   *(Revised 2026-09; responses collected before that date recorded it as
   non-committal and are remapped at merge time.)* Your `reviewer_gold_label` and
   `reviewer_gold_commitment` must agree: a label listed in
   `noncommit_labels` implies `noncommitted`.

8. **Output strict JSONL only.** One JSON object per line, one line per
   item, in the order given, no markdown fences, no commentary before or
   after, no trailing text. Every item in the batch gets exactly one line,
   including ones you exclude.

## Output format

One object per line, conforming to `ai_review_schema.json`:

```
{"hedgeqa_id":"...","reviewer_name":"gemini_antigravity","reviewer_gold_label":"...","reviewer_gold_commitment":"committed|noncommitted|ambiguous_exclude","evidence_sufficient_for_gold":"yes|no|unclear","transformation_valid":"yes|no|not_applicable|unclear","masked_variant_valid":"yes|no|not_applicable|unclear","keep_or_exclude":"keep|exclude","exclusion_reason":"","confidence":"high|medium|low","rationale_short":"...","flags":[]}
```

Field notes:

- `reviewer_name` — `gemini_antigravity` or `chatgpt_codex`. Use the same
  value on every line of your run.
- `hedgeqa_id` — copy verbatim from the item. Do not reformat it.
- `reviewer_gold_label` — must be a member of that item's `answer_space`. If
  the evidence supports something outside the space, pick the closest
  in-space label, flag `label_outside_answer_space`, and exclude.
- `transformation_valid` — `not_applicable` when `transformation_type` is
  `none` or the item is masked.
- `masked_variant_valid` — `not_applicable` for every non-masked item.
- `exclusion_reason` — empty string when keeping. When excluding, name the
  defect, not the verdict: "closing balance recoverable as
  8,053+5,253−7,563" rather than "evidence insufficient".
- `confidence` — your confidence in the label. A `low` on a `keep` routes
  the item to a human, which is a useful outcome; do not inflate it.
- `rationale_short` — one or two sentences citing the specific line or
  figure that decided it.
- `flags` — from the enum in `ai_review_schema.json`.

Save your output as:

```
analysis/hedgeqa_collection/ai_review/responses/<reviewer_name>__<batch_name>.jsonl
```

for example `gemini_antigravity__masked_batch01.jsonl`.

---

## A note on what this is for

These labels are **AI-assisted audit labels, not ground truth.** They are
used to find where an independent reader disagrees with our pipeline, so a
human can adjudicate those specific items. An item is never promoted on the
strength of AI agreement alone. Being wrong in an interesting way is more
useful here than being agreeable — if you think an item is broken, say so
plainly.
