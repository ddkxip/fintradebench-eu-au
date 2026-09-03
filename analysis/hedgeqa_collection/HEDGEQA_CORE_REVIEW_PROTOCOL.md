# HedgeQA-Core-v0.1 — manual review protocol

You are validating 368 items in
`hedgeqa_core_v0_1_manual_review.csv`. Nothing in this collection is
validated yet; your review is what makes any result from it reportable.

**The single rule that overrides everything below: when in doubt, exclude.**
The collection is a diagnostic instrument, not a corpus to maximise. An
excluded item costs one row. An item with a wrong gold label produces a
number that looks fine and is false, and no downstream check will catch it.

---

## Before you start

Work the sheet **top to bottom**. It is ordered by risk: constructed
(masked) golds first, then natural non-committal golds, then transformed
items, then the rest. A partial review done in this order is still useful; a
partial review done in ID order is not.

For every row you touch, fill in **all** of:
`reviewer_gold_label`, `reviewer_gold_commitment`,
`evidence_sufficient_for_gold`, `transformation_valid`,
`masked_variant_valid`, `keep_or_exclude`. Add `exclusion_reason` whenever
you exclude, and `notes` whenever you hesitated.

Do **not** edit `data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl`. The CSV is
the record; the JSONL is regenerated from the pipeline.

Read the `oracle_evidence_preview` column, but for masked items and anything
you are unsure about, open the full `oracle_evidence` from the JSONL. The
preview is truncated at 400 characters and is not sufficient for a decision.

---

## 1. Validating `gold_label`

**Question: does the evidence support this exact label, out of this exact
answer space?**

1. Read `question`, then `answer_space`, then the full `oracle_evidence`.
2. Decide the answer **yourself, before looking at `gold_label_auto`.** The
   auto label anchors you; forming your own answer first is the only
   protection against confirming it.
3. Enter your answer in `reviewer_gold_label`, whether or not it matches.
4. If it differs from `gold_label_auto`, that is a finding, not a mistake —
   record it and set `keep_or_exclude = exclude` unless the disagreement is
   purely a tie you can justify either way (note it if so).

Exclude when:
- the evidence supports a label outside `answer_space`;
- two labels are equally supported and the schema forces a choice;
- the question is ambiguous enough that a competent analyst could answer
  differently on a second reading.

**Known items to look at specifically:** the two FinTradeBench items whose
references are contradicted by their own evidence (`F50`, `T9` — see
`REFERENCE_QUALITY_AUDIT.md`). They were kept because the *label* may still
be defensible even though the stated justification is false. Decide.

## 2. Validating `gold_commitment`

**Question: does the reference answer settle the question, or decline to?**

`committed` = the reference picks a side. `noncommitted` = the reference
says the evidence does not settle it (`insufficient_data`, `mixed`,
`conditional`, `none_clear`, `roughly_unchanged`).

This is the collection's **load-bearing judgement** and the one humans agree
on least: in the parent project two blinded annotators reached only
κ = 0.53–0.59 on exactly this call. Treat disagreement as expected
information, not as one of you being wrong.

Rules:
- Judge the **reference answer**, not the question and not what a model
  would say.
- `roughly_unchanged` is non-committal in this schema. It reports that the
  direction is not resolved, which is a declination even though it sounds
  like a finding. If you disagree with that convention, note it — do not
  silently re-classify.
- `mixed` is non-committal. "Both effects are present" does not settle
  which dominates.
- A reference that commits *and* hedges ("probably yes, though the data is
  thin") is `committed` if it names an answer. Note the hedge.

Two reviewers should independently complete `reviewer_gold_commitment` on at
least a 150-item sample so κ can be reported. **Report the agreement figure
whatever it is** — a low κ is a real property of this task and belongs in
any write-up.

## 3. Validating masked-insufficient variants (93 items — highest risk)

**Question: with the removed rows gone, can the question still be answered?**

These items have `gold_label = insufficient_data` **by construction**. That
gold is correct only if the masked evidence genuinely fails to settle the
question. Automation cannot establish this; you are the check.

For each masked item:

1. Read `question` and the **full** masked `oracle_evidence`.
2. Try to answer the question from what remains. Actually try — do the
   arithmetic.
3. Look specifically for these reconstruction routes. The first two were
   found live in this data and are now guarded, so treat them as proof the
   class exists rather than as the whole class:
   - **Roll-forward.** A movement table's surviving components sum to the
     removed balance: opening + additions − disposals = the masked figure.
   - **Total minus components.** A summary table keeps its total row, so a
     removed component returns as total − siblings.
   - **A repeated figure.** The same number appearing in a footnote, a
     narrative sentence, or a second table that the line-based mask left
     alone.
   - **A stated direction.** Prose that says "revenue grew" answers a
     direction question without any figure at all.
   - **An adjacent-period proxy.** Enough neighbouring periods to infer the
     trend even without the exact values.
4. Record:
   - `masked_variant_valid = yes` — you tried and could not answer;
   - `= no` — you found a route (say which in `notes`), and
     `keep_or_exclude = exclude`;
   - `= unclear` — you suspect a route but cannot confirm it. **Treat
     unclear as exclude for now** and note why.

Also check the mask did not mutilate the document: if what remains reads as
obviously gutted, a model may answer `insufficient_data` because the input
looks damaged rather than because the evidence is absent. That is a
confounded item — exclude it.

`masked_variant_valid = not_applicable` is pre-filled for the 275
non-masked items. Leave it.

## 4. Validating `numeric_to_directional` transformations (140 items)

**Question: does the recorded derivation actually license this direction?**

The `derivation` field carries the source's own arithmetic — TAT-QA's
`derivation` string, FinQA's and ConvFinQA's `program`. Use it.

1. Read `original_question` (the source question, unmodified) and
   `question`. They should be identical for these items; the transformation
   changes the *answer space*, not the question.
2. Read the derivation and confirm the sign:
   - `subtract(a, b)` is positive when a > b. **Check the operand order.** A
     reversed subtract flips the direction and produces a confidently wrong
     gold.
   - Confirm the quantity being differenced is the one the question asks
     about.
3. Confirm the question is **direction-neutral**. A question that already
   asserts a direction ("what percentage *decrease* occurred") reports its
   magnitude as a positive number, and mapping that sign gives the opposite
   of the truth. Such questions are supposed to be rejected upstream; if you
   find one here, that is a filter escape — exclude it and note it.
4. Watch for `exe_ans` disagreeing with the source's stated answer. At least
   one FinQA item has `exe_ans` 0.97656 against a stated `56.25%`. The
   direction may still be right, but the disagreement means `exe_ans` is not
   always the quantity asked about — check which one the question wants.
5. Record `transformation_valid` as yes / no / unclear. `no` or `unclear`
   ⇒ exclude.

For `transformation_type = none` (135 items), set `transformation_valid =
not_applicable` or leave blank; there is nothing to check.

## 5. Validating evidence sufficiency

**Question: is the evidence enough to reach the gold, and is it the right
evidence?**

Set `evidence_sufficient_for_gold`:

- **yes** — a competent analyst could reach `gold_label` from this evidence
  alone. This is the answer you want for every *natural* item.
- **no** — the evidence does not support the gold. For a natural item this
  is a defect: exclude. **For a masked item, `no` is the intended state** —
  that is the whole construction, so `no` here plus `masked_variant_valid =
  yes` is a correct masked item.
- **unclear** — you cannot tell. Exclude and note.

Also check the evidence is not *over*-sufficient in a way that trivialises
the item: if the evidence literally states the answer in prose, the item
tests reading rather than judgement. Note it; it is not automatically an
exclusion, but a collection full of such items measures nothing interesting.

Watch for evidence that is present but about the wrong entity or period —
the FinTradeBench packs are built from a parsed date window, and a window
that does not match the question makes the item unanswerable for a reason
that has nothing to do with hedging.

## 6. When to exclude

Exclude — set `keep_or_exclude = exclude` and give an `exclusion_reason` —
whenever any of these is true:

| condition | why |
|---|---|
| your label differs from `gold_label_auto` and you can defend yours | the gold is wrong or contestable |
| two labels are equally supported | the item cannot discriminate |
| a masked item is answerable (`masked_variant_valid` = no/unclear) | the constructed gold is false |
| a directional gold is not licensed by its derivation | the transformation inverted or misread the answer |
| the question presupposes a direction | filter escape; sign mapping is invalid |
| evidence is about the wrong entity or period | unanswerable for the wrong reason |
| masked evidence reads as visibly gutted | model may hedge on damage, not absence |
| the question is ambiguous on a second reading | you will not reproduce your own judgement |
| you hesitated and cannot say why | record it; treat as exclude pending a second opinion |

Do **not** exclude merely because:

- an item is hard — difficulty is the point;
- a model would probably get it wrong;
- the reference is non-committal — those items are scarce and valuable;
- the evidence is long.

## After the review

1. Count exclusions per source and per `transformation_type`. A high
   exclusion rate in one stratum is itself a finding — especially among the
   masked variants, where it would mean the masking guards are still too
   weak and the construction needs revisiting rather than patching.
2. Report κ on `gold_commitment` between the two reviewers.
3. Only items with `keep_or_exclude = keep`, both reviewers agreeing on
   `gold_commitment`, and no `unclear` flag may be promoted to
   `manually_validated`.
4. Promotion is a deliberate, separate step. It is **not** part of this
   protocol and must not be done by editing `validation_status` by hand in
   the JSONL — the pipeline regenerates that file.
