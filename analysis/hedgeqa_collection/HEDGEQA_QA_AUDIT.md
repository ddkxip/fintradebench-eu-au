# HedgeQA-v0.1 — QA audit

**Status: CANDIDATE-ONLY. This collection is NOT validated.**

Everything below reports *internal consistency* — that the build is
deterministic, that items are well-formed, and that the structural invariants
hold. None of it establishes that a gold label is correct. 323 items (19.5%)
have a **constructed** gold label that no automated check can certify, and the
remaining 1,335 carry reference labels inherited from their source benchmarks
that this audit did not re-adjudicate. Do not report a result from this
collection until the manual review in
`hedgeqa_v0_1_manual_review.csv` is complete.

Pipeline run: all nine steps, clean, on the current working tree.
Figures below are computed from the artifacts that run produced.

---

## 0. Build determinism (not requested, but it failed first time)

Two consecutive full rebuilds now produce **byte-identical** candidate files,
collection and review sheet.

They did not at the start of this audit. `validate_candidates.py --write`
appended its "held for human review" note **unconditionally**, so every
re-run duplicated the phrase and changed the file hash. Running the pipeline
twice produced different bytes from identical inputs. Fixed to append once;
re-verified by running the whole pipeline twice and diffing md5s.

This mattered enough to fix before reporting anything else: a non-idempotent
build makes every other number in this document unreproducible.

---

## 1. Final item counts by source

| source | items |
|---|---|
| fintradebench | 99 |
| financebench | 59 |
| tatqa | 500 |
| finqa | 500 |
| convfinqa | 500 |
| **total** | **1,658** |

## 2. Final item counts by answer_type

| answer_type | items |
|---|---|
| directional_change | 1,500 |
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

**90.5% of the collection is a single answer type.** Any pooled statistic is
dominated by `directional_change`; the nine judgement types together are
under 6% of items.

## 3. Final item counts by gold_commitment

| gold_commitment | items | share |
|---|---|---|
| committed | 1,229 | 74.1% |
| noncommitted | 429 | 25.9% |
| ambiguous_exclude | 0 | — |

Items flagged `ambiguous_exclude` are excluded at the candidate stage and so
never reach the collection (32 of them; §5).

## 4. Final item counts by transformation_type

| transformation_type | items |
|---|---|
| numeric_to_directional | 1,200 |
| evidence_masked_insufficient | 323 |
| none | 135 |
| comparison_to_choice | 0 |

`comparison_to_choice` is implemented and tested but currently yields
nothing — no source path invokes it. It is dead code in this build.

## 5. auto_validated vs candidate vs excluded

Candidate pools (everything the builders emitted, including excluded rows
retained for provenance):

| source | auto_validated | candidate | excluded | total |
|---|---|---|---|---|
| fintradebench | 108 | 0 | 31 | 139 |
| financebench | 36 | 23 | 1 | 60 |
| tatqa | 400 | 100 | 0 | 500 |
| finqa | 400 | 100 | 0 | 500 |
| convfinqa | 400 | 100 | 0 | 500 |
| **total** | **1,344** | **323** | **32** | **1,699** |

In the assembled collection: **1,335 auto_validated, 323 candidate, 0
excluded.**

`auto_validated` means *structurally well-formed*. It is not a correctness
claim, and nothing in this collection is `manually_validated` yet — that
status is currently unused.

Every `candidate` item is a controlled-insufficient variant, deliberately
held back: structural validity cannot establish that masked evidence really
fails to answer the question.

## 6. Majority-class baseline by source

The score a system gets by always emitting the most common label, with no
reasoning.

| source | items | majority label | baseline |
|---|---|---|---|
| fintradebench | 99 | `no` | **14.1%** |
| financebench | 59 | `yes` | **42.4%** |
| tatqa | 500 | `decreased` | **32.4%** |
| finqa | 500 | `increased` | **39.2%** |
| convfinqa | 500 | `increased` | **39.8%** |
| pooled | 1,658 | `increased` | 33.6% |

No component is passable by guessing one label. This is the result of the
seeded label-stratified sampling in the three directional builders; drawn
proportionally, those baselines would sit near 62–71%.

## 7. Non-committal gold share by source

| source | items | non-committal | share | of which masked | natural non-committal | natural share |
|---|---|---|---|---|---|---|
| fintradebench | 99 | 19 | 19.2% | 0 | 19 | 19.2% |
| financebench | 59 | 23 | 39.0% | 23 | 0 | **0.0%** |
| tatqa | 500 | 176 | 35.2% | 100 | 76 | 19.0% |
| finqa | 500 | 109 | 21.8% | 100 | 9 | 2.3% |
| convfinqa | 500 | 102 | 20.4% | 100 | 2 | **0.5%** |
| pooled | 1,658 | 429 | 25.9% | 323 | 106 | 7.9% |

**Read the last two columns before using this collection.** The healthy
25.9% headline is 75% constructed. Strip the masked variants and the natural
non-committal rate is 7.9%, and for FinanceBench and ConvFinQA it is
essentially zero. Overcommitment and wrong-non-committal-type are therefore
**not measurable on natural items** outside FinTradeBench and TAT-QA.

## 8. Evidence length distribution by source (characters)

| source | n | min | p25 | median | p75 | max |
|---|---|---|---|---|---|---|
| fintradebench | 99 | 790 | 795 | 798 | 1,591 | 3,975 |
| financebench | 59 | 172 | 512 | 1,168 | 1,639 | 4,468 |
| tatqa | 500 | 216 | 841 | 1,437 | 2,233 | 6,813 |
| finqa | 500 | 632 | 3,299 | 4,076 | 4,799 | 14,591 |
| convfinqa | 500 | 467 | 2,811 | 3,802 | 4,615 | 11,446 |
| pooled | 1,658 | 172 | 1,435 | 3,120 | 4,219 | 14,591 |

Evidence length varies by **85x** across the collection. FinQA and ConvFinQA
items carry ~5x the context of FinTradeBench items. Since hedging plausibly
responds to context length, **cross-benchmark comparisons confound source
with evidence length**, which is a further reason to report stratified.

## 9. Failed or suspicious validator checks

### Validators: 16,580 checks over 1,658 items — **zero failures**

| check | failures |
|---|---|
| enums | 0 |
| answer_space_size | 0 |
| noncommit_subset | 0 |
| gold_in_space | 0 |
| no_duplicate_labels | 0 |
| evidence_present | 0 |
| no_rag | 0 |
| transformation_audit | 0 |
| masked_variant_marked | 0 |
| gold_commitment_consistent | 0 |

Zero failures is expected, not reassuring: failing items are excluded at the
candidate stage, so the collection is the set that already passed. The
informative number is what got excluded (below).

### Exclusions in the candidate pools (32)

| source | n | reason |
|---|---|---|
| fintradebench | 27 | set-valued reference (expert answer names >1 answer-space entity) |
| fintradebench | 4 | empty oracle evidence pack |
| financebench | 1 | annotated evidence span too short to serve as oracle evidence |

### Independent re-checks

| check | result |
|---|---|
| duplicate `hedgeqa_id` | 0 |
| `requires_rag` true anywhere | 0 |
| masked items auto-promoted | 0 |
| transformed items missing `original_question`/`derivation` | 0 |
| masked/natural sharing a source item (directional) | 0 |
| directional masked variants re-checked for reconstruction | 300 |
| …of which reconstructible by column sum or total-minus-components | **0** |

### Suspicious — two things that are not defects but change interpretation

**(a) 609 of 1,658 items (36.7%) share an evidence document with another
item.** Only 1,316 distinct evidence strings exist; one document is reused by
up to 5 items.

| source | items | distinct evidence | max reuse | items sharing |
|---|---|---|---|---|
| fintradebench | 99 | 78 | 3 | 38 |
| financebench | 59 | 59 | 1 | 0 |
| tatqa | 500 | 450 | 2 | 100 |
| finqa | 500 | 436 | 3 | 125 |
| convfinqa | 500 | 414 | 4 | 157 |

This is inherent to the sources — TAT-QA asks several questions per table,
ConvFinQA turns 0 and 1 share a filing — but it means **items are not
independent**. Any confidence interval computed over pooled items will be too
narrow. Cluster by `oracle_evidence` (or by source document) when computing
uncertainty, exactly as the parent project clusters by ticker.

**(b) 23 `source_id`s appear twice**, all FinanceBench. These are the
natural/masked pairs, which the FinanceBench builder deliberately pairs
(37 items is too few to spend on independence). Their evidence differs
(masked ≠ natural), so they are not duplicate items — but the pair is
correlated and should not be treated as two independent observations. The
three directional benchmarks avoid this by construction: 0 shared source
items.

### Schema confidence by source

| source | min | median | max |
|---|---|---|---|
| fintradebench | 0.35 | 0.90 | 0.90 |
| financebench | 0.60 | 0.70 | 0.70 |
| tatqa | 0.60 | 0.60 | 0.60 |
| finqa | 0.60 | 0.60 | 0.60 |
| convfinqa | 0.55 | 0.55 | 0.60 |

The two FinTradeBench items at 0.35 are F50 and T9, whose references are
contradicted by their own evidence (`REFERENCE_QUALITY_AUDIT.md`);
they are demoted so they cannot head a clean-candidate list.

## 10. Masking tests

**All 14 pass** (`test_masking.py`, exit 0).

| test | guards |
|---|---|
| `test_salient_excludes_years_and_small_ints` | salience filter |
| `test_rejects_when_gold_figures_absent_from_evidence` | grounded |
| `test_rejects_when_a_decisive_figure_survives` | coverage |
| `test_rejects_residual_concept_row` | residual concept row |
| `test_accepts_a_clean_mask` | positive control |
| `test_catches_rollforward_reconstruction` | roll-forward leak |
| `test_catches_total_minus_components_reconstruction` | total-minus-components leak |
| `test_rollforward_guard_does_not_overfire` | false-positive control |
| `test_mask_directional_rejects_reconstructible` | end-to-end rejection |
| `test_rejects_direction_presupposing_questions` | direction safety |
| `test_rejects_cross_sectional_differences` | direction safety |
| `test_accepts_direction_neutral_change_questions` | positive control |
| `test_sign_maps_to_direction` | sign mapping |
| `test_presupposing_question_yields_nothing` | end-to-end rejection |

Each asserts a guard **can reject**. That design exists because an earlier
post-condition could never fail and reported zero rejections that looked like
success.

Passing tests do not mean the masks are correct. They mean the four known
failure modes are caught. A fifth is not excluded.

---

## 11. Highest-risk categories requiring manual review

Ordered by (items at risk) x (probability the gold is wrong) x (how invisible
the error would be downstream).

### RISK 1 — the 323 controlled-insufficient variants (19.5% of the collection)

Their gold is `insufficient_data` **by construction**, correct only if the
masked evidence truly cannot answer the question. Two reconstruction routes
were found by hand-reading output and are now guarded — a movement table
whose components still sum to the removed balance, and a summary table whose
total minus siblings recovers it. **Both were live in the first batch.** A
third route is not excluded: a ratio rebuilt from unrelated components, a
direction stated in surrounding prose, or a figure repeated in a footnote the
line-based mask left intact.

*Review*: for each, read the masked evidence and ask whether a competent
analyst could still answer. Reject on any doubt. This is the single highest
priority; a wrong gold here inverts the overcommitment metric.

### RISK 2 — the 1,200 numeric→directional items (72.4%)

The gold is derived from the sign of a source answer. Direction-presupposing
and cross-sectional questions are now rejected (that bug produced flatly
wrong labels: `"what percentage decrease occurred"` → `+96.55` → `increased`),
but two residual hazards remain:

- **Operand-order dependence.** FinQA `subtract(a, b)` with reversed operands
  flips the direction. The `program` is recorded in `derivation` precisely so
  this is checkable — check it.
- **`exe_ans` disagreeing with the stated answer.** At least one FinQA item
  has `exe_ans` 0.97656 against a stated answer of `56.25%`. The direction
  survives there, but the disagreement means `exe_ans` is not always the
  quantity the question asks about.

*Review*: sample ~50 per benchmark, recompute the direction from the
derivation, and measure the disagreement rate before trusting the other 1,150.

### RISK 3 — ConvFinQA history inlining (400 items)

Turn-1 items inline prior turns verbatim into the question text. This changes
prompt shape relative to every other benchmark and can make a turn's subject
ambiguous. *Review*: confirm each turn-1 item is answerable as written.

### RISK 4 — FinTradeBench references (99 items)

Two (F50, T9) have justifications contradicted by their own evidence and are
confidence-demoted but **not excluded**, because the label may still be
defensible. 27 further items were excluded for set-valued references — that
exclusion rule is a judgement call worth a second opinion.

### RISK 5 — the `gold_commitment` call itself (all 1,658)

Whether a reference "settles" a question is the collection's load-bearing
judgement. In the parent project, two blinded annotators reached only
κ = 0.53–0.59 on exactly this call. The review sheet has two reviewer columns
for this reason. *Report inter-annotator agreement; do not treat the auto
value as ground truth.*

### RISK 6 — evidence-sharing clusters (609 items)

Not a labelling risk but an inference one: items sharing a document are
correlated. Cluster by evidence when computing any interval.

---

## What would move this from candidate to validated

1. Two reviewers adjudicate `gold_commitment` on a sample; report κ.
2. Every one of the 323 masked variants read by a human.
3. A ~50-item-per-benchmark recomputation of the directional golds from their
   derivations, with a disagreement rate reported.
4. F50, T9 and the 27 set-collapse exclusions given a second opinion.
5. Only then may items move to `manually_validated`, and only those items may
   support a reported result.
