# Triage: the three FinanceBench "overcommitments"

All three edge-run FinanceBench items answered confidently on evidence whose
gold is `insufficient_data`. Reading the three documents by hand, **only one
is a model failure. Two are defects in our own construction**, and one of
those is worse than a wrong label.

| item | verdict | model | gold | who is wrong |
|---|---|---|---|---|
| `hqa_FB_9fc58fab_masked` | gold is wrong | `yes` @ p_nc 0.00 | `insufficient_data` | **us** |
| `hqa_FB_5dbbcec0_masked` | document is falsified | `no` @ p_nc 0.00 | `insufficient_data` | **us** |
| `hqa_FB_d397e71d_masked` | genuine overcommitment | `no` @ p_nc 0.05 | `insufficient_data` | the model |

---

## 1. CVS — the gold is wrong; the model was right

> **Q.** Has CVS Health reported any materially important ongoing legal
> battles from 2022, 2021 and 2020?

Masking removed `4.3` and `625` — the opioid settlement's dollar amounts.
What survives is four paragraphs of litigation:

> "named as a defendant in a number of lawsuits…"
> "facing multiple lawsuits, including by state Attorneys General,
> governmental subdivisions and several putative class actions…"
> "the Company agreed to a formal settlement agreement… would resolve
> substantially all opioid claims…"

The question asks whether such battles **exist**. The surviving text answers
that overwhelmingly: **yes**. The removed figures quantify a settlement; they
are irrelevant to existence.

The model answered `yes` at p_nc 0.00 and was **correct**. We scored it as an
overcommitment.

### The general defect

`masking.py` selects *salient numbers* and deletes the lines carrying them.
That is sound when the answer is a computation over figures. It is
**category-inappropriate when the answer is carried by prose** — existence,
policy, or narrative questions. No amount of number-deletion makes "are there
lawsuits" unanswerable while leaving the lawsuits described.

The `derivation` field states the post-condition confidently:

> "…a post-condition check confirmed none survives in the remaining text, so
> the question cannot be settled from what is left."

The first clause is true and the second does not follow. The check verifies
*figures* are gone and then asserts *the question* is unanswerable. For a
numeric question those coincide; here they come apart, and the derivation
text asserts the conclusion either way.

## 2. MGM — the mask spliced a false statement into the document

> **Q.** Has MGM Resorts paid dividends to common shareholders in FY2022?

This one is not merely unanswerable-or-not. The line deletion **joined two
unrelated sentences into a fluent, false one.**

The filing said, in substance: in Q2 2020 MGM *reduced* the dividend to $0.01
because of COVID; it *maintained* $0.01 throughout 2022; and on 8 February
**2023** the Board suspended it in favour of buybacks. So the true answer is
**yes — MGM paid a $0.01 dividend through FY2022.**

After deleting the lines carrying `0.01` and `2022.`, the surviving text
reads:

> "We implemented a dividend program in February 2017 pursuant to which it
> has paid regular quarterly dividends. **In the second quarter of 2020, we**
> **in light of our current preferred method of returning value to**
> **shareholders through our share repurchase plan.** To the extent we
> determine to **reinstate** the dividend in the future…"

The fragment "In the second quarter of 2020, we" now runs directly into the
*2023* suspension clause. A reader gets: MGM stopped paying in Q2 2020,
prefers buybacks, and would have to "reinstate" the dividend — reinforced by
a full table of Q4 2022 share repurchases. The document now asserts **no**.

The model answered `no` at p_nc 0.00. **That is the correct reading of the
document we handed it.** Its confidence is appropriate; the text is
unambiguous. It is unambiguous because we made it so, in the wrong direction.

This is the most serious finding here: masking is supposed to *remove*
information, and on this item it **added** information that is false. A
line-oriented deleter cannot see that it has spliced a sentence, because the
grammar of the join happens to work.

## 3. JnJ — a genuine overcommitment, and a good one

> **Q.** Is growth in JnJ's adjusted EPS expected to accelerate in FY2023?

Answering needs 2022 adjusted-EPS growth (`3.6%`, masked) and the 2023
adjusted-EPS guidance (`$10.50` / `3.5%`, masked). Both are gone. The 2023
guidance line is cut mid-clause at "…sales growth excluding COVID-19 Vaccine
of 4.0%* and". **The gold is right: acceleration cannot be determined.**

The model answered `no` at p_nc 0.05. The likely route is visible in what
survives: 2022 full-year *operational sales* growth 6.1% against 2023
*guided sales* growth 4.0% — lower, therefore "decelerating", therefore `no`.
That substitutes sales growth for EPS growth and guidance for outturn. It is
a real reasoning failure, committed at near-zero measured uncertainty.

Worth noting for the separate damage question: this document is **visibly
truncated mid-sentence**, and still none of its 20 decodes mentioned damage.
That strengthens rather than weakens the 0/300 result — the model does not
cite damage even when damage is present.

---

## What this does to the edge-run conclusion

The headline "all 3 FinanceBench edge items overcommitted confidently" stands
as a description of the scores and **fails as a description of the model's
behaviour**. Corrected: **1 of 3 is a model failure; 2 of 3 are our bugs**,
and in one of those the model reasoned correctly from a document we
falsified.

The broader claim survives intact and is now better supported: the JnJ item
is a clean instance of overcommitment at p_nc 0.05 — a wrong answer that an
entropy monitor cannot see. One clean instance, not three.

It also re-reads §4 of `HEDGEQA_EDGE15_RUN.md`. The gutted-vs-source split
there — 7/7 non-FinanceBench declined, 0/3 FinanceBench — is not mainly a
property of FinanceBench's documents or of its `yes`/`no` answer space. **It
is mainly a property of masking prose-answerable questions by deleting
numbers.**

## Scope of the defect

**7 masked `yes_no` items, all FinanceBench** — the entire FinanceBench
masked stratum. (Every other source's masked items are `directional_change`
over numeric tables, where number-deletion is the right instrument.)

Four have now been run:

| item | run | model | assessment |
|---|---|---|---|
| `hqa_FB_9fc58fab_masked` | edge | `yes` 0.00 | **gold wrong** |
| `hqa_FB_5dbbcec0_masked` | edge | `no` 0.00 | **document falsified** |
| `hqa_FB_d397e71d_masked` | edge | `no` 0.05 | gold sound, genuine failure |
| `hqa_FB_1858a6da_masked` | smoke_15 | `yes` 0.00 | gold sound, genuine failure |

The remaining three were read and are **structurally sound** — all are
numeric-table questions where the needed figures really are gone:

- `hqa_FB_1da93057_masked` (Pfizer PP&E) — both years removed.
- `hqa_FB_86637d3d_masked` (Best Buy cash) — both balances removed.
- `hqa_FB_7cc358e4_masked` (AMCOR gross margin) — checked specifically for
  the `total_minus_components` route, since cost of sales survives for all
  three years. **Net sales and gross profit are both masked** for FY2023 and
  FY2022 (14,694−11,969=2,725 and 14,544−11,724=2,820 confirm the pairing),
  so one unknown cannot be recovered from the other. The route is closed.

So the damage is **2 items of 319**, both identified, and the pattern that
produced them is understood.

## Why the human review did not catch these

The reviewer marked all three `masked_variant_valid = yes`. The `notes` field
on each reads "CONSTRUCTED GOLD - verify the masked evidence truly cannot
answer the question" — that is the **auto-generated instruction the builder
wrote**, not a reviewer observation, so it is not evidence the check was run
on these particular items.

This is not a reviewer failure so much as a workflow one. Verifying a mask
means re-reading a full filing excerpt against the question and asking what
*could* still answer it, across 93 items. The two failures here are precisely
the cases that reward slow reading: one needs you to notice that a question
is qualitative, the other needs you to notice that a sentence has been
spliced. Both look fine at speed.

Notably, an AI reviewer flagged **all three** as `evidence_gutted` — which is
how they reached the edge manifest. That flag was treated as a confound to
route around. On two of the three it was **pointing at a real defect**.

## Recommended next steps, in order

1. **Exclude `hqa_FB_9fc58fab_masked` and `hqa_FB_5dbbcec0_masked`** from the
   validated collection (319 → 317), with the reason recorded. Neither is
   repairable by re-masking: the CVS question is not maskable by number
   deletion at all, and the MGM document would need the splice repaired
   *and* would then answer `yes`.
2. **Add a splice guard to `masking.py`**: after deletion, reject when a
   surviving line ends without terminal punctuation and the join to the next
   surviving line forms a new sentence. This is mechanical and testable, and
   it is the check that would have caught MGM.
3. **Gate masking by question category.** Refuse to build a masked variant
   for an existence/policy/narrative question. A cheap conservative rule:
   require that the gold answer be a computation over the removed figures —
   which for FinanceBench `yes_no` items is often not the case.
4. **Re-read the other three FinanceBench yes/no items against rule 3** even
   though their figures are properly gone — "improving gross margin profile"
   invites qualitative answers from surrounding prose in a way that
   "did PP&E grow" does not.
5. Re-run those two items' slots after exclusion before quoting any
   FinanceBench masked number again.

## Caveat

This is four items read by hand. The reading is reported in full above so it
can be checked; the MGM splice and the AMCOR arithmetic are the two claims
that carry weight and both are quoted verbatim from the artifacts.
