# Masking: splice guard and question-category gate

Two new guards in `masking.py`, both prompted by real defects found by
hand-reading four FinanceBench items (`HEDGEQA_FB_OVERCOMMIT_TRIAGE.md`).
**31/31 tests pass**, including all 22 that existed before.

Both guards govern **future construction**. The reviewed collection stays
pinned, as established in `HEDGEQA_MASKING_GUARD_UPDATE.md`; §4 measures what
they would have done to what is already built.

---

## 1. The splice guard

### The defect

Masking deletes whole **lines**. When a deleted line sat in the middle of a
sentence, the surviving fragments become adjacent — and if the grammar of that
join happens to work, the document acquires a sentence the filing never
contained.

On `hqa_FB_5dbbcec0_masked` the filing said MGM *reduced* its dividend to
$0.01 in Q2 2020, *maintained* it through 2022, and suspended it in February
**2023**. Deleting the two lines carrying `0.01` and `2022.` left:

> In the second quarter of 2020, we
> in light of our current preferred method of returning value to shareholders
> through our share repurchase plan.

A grammatical sentence asserting a **Q2-2020 suspension** — the opposite of
the truth. Every existing check passed, because each only asked whether the
figures were gone. **Masking is supposed to remove information; here it added
false information.**

### The check

`splice_sites(lines, removed_idx)` fires only where all four hold:

1. the deletion actually created a **new adjacency** (`b > a + 1`);
2. **both** sides are running prose (≥4 words, alphabetic mass > 3× digits) —
   table rows and headings have no sentence to splice;
3. the left fragment does **not** end a sentence (no terminal punctuation);
4. the right fragment **continues** one (starts lower-case).

Wired into `mask_evidence` as a final acceptance check, so every pre-existing
rejection reason is preserved and only masks that would otherwise have
shipped are refused.

### Tests

| test | what it pins |
|---|---|
| `test_catches_mgm_sentence_splice` | **regression** — the real MGM text, both via `splice_sites` and end-to-end through `mask_evidence` |
| `test_negative_control_deletion_between_complete_sentences` | **negative control** — deleting a whole standalone sentence must not fire, and the mask must still succeed |
| `test_negative_control_table_rows_are_not_splices` | numeric table rows are not prose |
| `test_splice_guard_needs_a_real_gap` | no deletion, or a trailing deletion joining nothing, must not fire |

The MGM fixture is the **actual filing text**, reconstructed from the shipped
item's surviving evidence plus its `masked_content`, not a paraphrase.

### Known cost

The guard is deliberately conservative and will refuse benign splices. Measured
case: `hqa_TAT_5ce27434_masked` joins *"…at a weighted average"* to *"related
to employee purchases under the ESPP…"*. That is garbled, but it asserts
nothing false, and the guard cannot tell the difference — a fluent join and a
garbled one look identical to it. Consistent with the module's stated position
that skipping an item is free and a bad masked item is not.

---

## 2. The question-category gate

### The defect

`mask_evidence` deletes lines carrying salient **numbers**. That is the right
instrument when the gold answer is a computation over those figures, and
category-inappropriate when the answer is carried by **prose**.

`hqa_FB_9fc58fab_masked` is the worked example. "Has CVS reported any
materially important ongoing legal battles?" Masking removed the opioid
settlement's dollar amounts and left four paragraphs describing the lawsuits.
The constructed gold said `insufficient_data`; the surviving prose says `yes`.

The item's `derivation` asserted:

> "…a post-condition check confirmed none survives in the remaining text, **so
> the question cannot be settled from what is left**."

The first clause is true and **the second does not follow**. The check
verifies that figures are gone and then asserts the question is unanswerable.
For a numeric question those coincide; here they come apart, and the sentence
was generated either way.

### The rule

A mask is refused unless **either**:

- the question is **numeric by category**, **or**
- the caller supplies `numeric_dependency` — positive proof that the gold
  answer is a computation over the removed figures.

`classify_question` assigns one of five categories, in this order:

| order | category | maskable | cues |
|---|---|---|---|
| 1 | `narrative` | no | explain, describe, discuss, why did, what factors, state that |
| 2 | `numeric` | **yes** | how much, what was, grow/growth, increase, decrease, declin-, drop in, change in, accelerat-, percentage, between fy, compared to |
| 3 | `existence` | no | *has … paid*, *reported any*, *is/are there any*, *has/have … any*, *ever* |
| 4 | `qualitative` | no | improving, healthy, strong, weak, attractive, reasonable, useful metric, materially important, profile |
| 5 | `unclassified` | no | — |

Order matters. `narrative` is checked **first**: an instruction to explain
makes an item answerable in prose no matter which figures go, which is why
AMCOR's *"If gross margin is not a useful metric… state that and explain why"*
classifies as narrative rather than qualitative. `numeric` is checked before
`existence` so that *"Was there **any drop in** Cash & Cash equivalents
between FY2023 and Q2 FY2024?"* is read as the quantitative question it is,
rather than caught by the bare word "any".

**Unclassified fails closed.** An unrecognised question shape is not maskable.

### What counts as proof

`numeric_dependency` must be an **artifact naming the operands**, not an
assertion. TAT-QA ships a `derivation` and FinQA/ConvFinQA a `program`, so
`mask_directional` passes `f"program operands {ops}"` and legitimately
discharges the gate for all three corpora.

The FinanceBench builder has **no such artifact** — it infers salient figures
from the gold answer's free text, which is precisely the weak inference that
produced the CVS item. It therefore passes nothing and is gated on question
category alone. This is the intended consequence: **new FinanceBench masked
items are now built only for questions that are numeric by category.**

### Tests

| test | what it pins |
|---|---|
| `test_category_gate_refuses_existence_and_qualitative_questions` | the four real FinanceBench question shapes classify as existence / existence / qualitative / narrative |
| `test_category_gate_admits_genuinely_numeric_questions` | Pfizer, Best Buy and JnJ stay maskable — the gate must not refuse what number-deletion is *for* |
| `test_category_gate_blocks_a_prose_answerable_mask_end_to_end` | the CVS shape is refused through `mask_evidence`, with the category recorded |
| `test_category_gate_is_discharged_by_proof` | `numeric_dependency` overrides, and **only** it does |
| `test_unclassified_questions_fail_closed` | an unknown shape does not default to open |

---

## 3. Retrospective sweep of the built collection

Run `python analysis/hedgeqa_collection/audit_masked_items.py`. Nothing is
modified.

### Category gate over all 47 masked items in the strict set

| source | category | n |
|---|---|---|
| convfinqa | numeric | 19 |
| finqa | numeric | 15 |
| tatqa | numeric | 8 |
| financebench | numeric | 3 |
| financebench | narrative | 1 |
| financebench | qualitative | 1 |

**Refused on category alone: 2/47** — `hqa_FB_1858a6da_masked` (qualitative,
cue *improving*) and `hqa_FB_7cc358e4_masked` (narrative, cue *explain*). The
other 45 are numeric, and the 42 directional ones would discharge the gate
with their program regardless.

The two already-excluded items are exactly the two the gate would have
stopped at construction: CVS as `existence`, MGM as `existence`. The gate
catches both known defects and adds two conservative refusals.

### Splice sweep

`splice_risk_from_removed` is **one-sided**: the original document is gone, so
it can only detect that a removed prose line began lower-case, i.e. continued
a sentence. It flags risk; only reading decides.

It **abstains on lower-cased corpora.** ConvFinQA and FinQA ship filings
entirely in lower case, where "starts lower-case" carries no information
whatever. A first version omitted this check and flagged 8 ConvFinQA/FinQA
items purely because of their corpus convention — a vacuous result that looked
like a finding. `is_normally_cased` now gates it, and abstains on 37 of 47.

> A second bug in the same check: the casing sample originally included the
> removed lines, which are the lower-case continuations under test, dragging
> the ratio from 0.33 to 0.25 and abstaining on a true hit. The convention is
> now established from the surviving text only.

Of the **10 normally-cased** items, **2** are flagged, and both were read:

| item | join | verdict |
|---|---|---|
| `hqa_FB_d397e71d_masked` | deletion is **trailing** — the document ends mid-clause at *"…of 4.0%\* and"*, joining nothing | visible truncation, **not** falsification; gold unaffected |
| `hqa_TAT_5ce27434_masked` | *"…at a weighted average"* + *"related to employee purchases under the ESPP…"* | garbled, asserts nothing false; gold unaffected |

**No second instance of the MGM defect was found.** Two caveats on that: the
sweep abstains on 37 items, and it detects a broken sentence rather than a
false one.

---

## 4. Audit: the five remaining FinanceBench masked items

Part C. All five were read by hand; none is re-admitted and none is created.

| item | numeric / table-dependent? | surviving prose answers it? | mask corrupts meaning? | remain in strict set? |
|---|---|---|---|---|
| `hqa_FB_1da93057_masked` <br>*Did Pfizer grow its PPNE between FY20 and FY21?* | **yes** — PP&E balances for both years from a balance sheet | **no** — surviving text is a balance-sheet table | no — deleted rows are numeric | **KEEP** |
| `hqa_FB_86637d3d_masked` <br>*Was there any drop in Cash & Cash equivalents between FY2023 and Q2 FY2024?* | **yes** — two cash balances from a table | **no** — surviving text is a non-GAAP reconciliation table | no — deleted rows are numeric | **KEEP** |
| `hqa_FB_d397e71d_masked` <br>*Is growth in JnJ's adjusted EPS expected to accelerate in FY2023?* | **yes** — 2022 adj-EPS growth vs 2023 guidance | **no** — both growth figures are gone | no, but the document is **visibly cut mid-clause** | **KEEP** |
| `hqa_FB_1858a6da_masked` <br>*Does Adobe have an improving Free cashflow conversion as of FY2022?* | **yes** — conversion needs net income and operating cash flow | **no** — both years' inputs are gone (only FY2020 net income survives, so no trend) | no — deleted rows are numeric | **KEEP** (gate would refuse: qualitative) |
| `hqa_FB_7cc358e4_masked` <br>*Does AMCOR have an improving gross margin profile as of FY2023? If gross margin is not a useful metric… explain why.* | **yes** — margin needs net sales and gross profit | **PARTLY** — the second clause invites a prose answer regardless | no — deleted rows are numeric | **KEEP WITH CAVEAT** (gate would refuse: narrative) |

### On the two the gate would refuse

Adobe and AMCOR are retained because the **hand read** confirms the decisive
figures are genuinely gone — which is the question that decides retention. The
gate answers a different question: *should we have built this shape at all?*
It governs construction, where it is right to be conservative; it is not a
re-labelling rule for items a human has already verified.

AMCOR carries a caveat because its second clause ("if gross margin is not a
useful metric… explain why") is answerable from general knowledge no matter
what is masked. It is not the CVS defect — the *first* clause genuinely
cannot be answered — but a model can produce a creditable response to the
question as asked without the missing figures. Treat any AMCOR result as
weaker evidence than the other four.

### AMCOR reconstruction check

Because cost of sales survives for all three years, the
`total_minus_components` route was checked explicitly. **Net sales and gross
profit are both masked** for FY2023 and FY2022 — 14,694−11,969 = 2,725 and
14,544−11,724 = 2,820 confirm the pairing — so neither unknown can be
recovered from the other. The route is closed.

---

## 5. Limitations

1. **The splice guard cannot judge truth.** It detects a broken sentence, not
   a false one, so it refuses benign joins (TAT-QA, above) and would not fire
   on a deletion that produces a false statement without breaking a sentence.
2. **The category gate is lexical.** It classifies by cue words and will
   misread a question phrased unusually. It fails closed, so the error mode is
   lost items rather than bad ones.
3. **The retrospective sweep abstains on 37 of 47 items.** No second MGM
   instance was found, which is not the same as none existing.
4. **Nothing here certifies an existing item.** The guards prevent this class
   of defect in future construction. The two defects that were found were
   found by a human reading four items, and that remains the only instrument
   that has actually caught this class.
5. **Two defects in four items read.** The masked stratum has not been
   re-read end to end, so the base rate of this defect class is unknown.

## 6. Full output

### Tests

```
PASS test_accepts_a_clean_mask
PASS test_accepts_direction_neutral_change_questions
PASS test_catches_mgm_sentence_splice
PASS test_catches_one_step_deeper_total_minus_several_components
PASS test_catches_reconstruction_spanning_two_blocks
PASS test_catches_rollforward_reconstruction
PASS test_catches_total_minus_components_in_prose_layout
PASS test_catches_total_minus_components_reconstruction
PASS test_category_gate_admits_genuinely_numeric_questions
PASS test_category_gate_blocks_a_prose_answerable_mask_end_to_end
PASS test_category_gate_is_discharged_by_proof
PASS test_category_gate_refuses_existence_and_qualitative_questions
PASS test_mask_directional_rejects_reconstructible
PASS test_negative_control_deletion_between_complete_sentences
PASS test_negative_control_ordinary_totals_do_not_fire
PASS test_negative_control_table_rows_are_not_splices
PASS test_parses_vertical_label_then_numbers_layout
PASS test_parses_whitespace_table_layout
PASS test_pipe_header_cells_do_not_leak_numbers
PASS test_presupposing_question_yields_nothing
PASS test_rejects_cross_sectional_differences
PASS test_rejects_direction_presupposing_questions
PASS test_rejects_residual_concept_row
PASS test_rejects_when_a_decisive_figure_survives
PASS test_rejects_when_gold_figures_absent_from_evidence
PASS test_rollforward_guard_does_not_overfire
PASS test_salient_excludes_years_and_small_ints
PASS test_sign_maps_to_direction
PASS test_splice_guard_needs_a_real_gap
PASS test_unclassified_questions_fail_closed
PASS test_window_search_stays_advisory
hedgeqa tests: all passed
```

### Audit

```
strict set 317   masked 47

==============================================================================
A. CATEGORY GATE applied retrospectively to every masked item
==============================================================================
  source         category         n
  convfinqa      numeric         19
  financebench   narrative        1
  financebench   numeric          3
  financebench   qualitative      1
  finqa          numeric         15
  tatqa          numeric          8

  would be REFUSED by the gate on question category alone: 2/47
    hqa_FB_1858a6da_masked     qualitative  cue=improving
    hqa_FB_7cc358e4_masked     narrative    cue=explain

  NOTE: the directional items carry a program/derivation naming
  the operands, which discharges the gate, so a refusal here is
  only decisive for FinanceBench, which has no such artifact.

==============================================================================
B. SPLICE RISK sweep (one-sided; flags risk, does not prove)
==============================================================================
  normally-cased documents (heuristic applies): 10/47   abstained on the rest
  of those, items with a removed prose line starting lower-case: 2/10

    hqa_FB_d397e71d_masked (financebench)
      ...adjusted operational EPS of $10.50, reflecting growth of 3.5%*

    hqa_TAT_5ce27434_masked (tatqa)
      ...exercise price per share of $86.51, $77.02, and $73.02, respectively. As of December 31, 2

==============================================================================
C. REMAINING FINANCEBENCH MASKED ITEMS -- hand-read audit
==============================================================================

  hqa_FB_1858a6da_masked  [gate: qualitative]
    Q                : Does Adobe have an improving Free cashflow conversion as of FY2022?
    numeric/table-dep: yes -- FCF conversion from net income and operating cash flow
    prose answers it : no -- both years' inputs are gone
    mask corrupts    : no -- deleted rows are numeric, not sentences
    verdict          : KEEP

  hqa_FB_1da93057_masked  [gate: numeric]
    Q                : Did Pfizer grow its PPNE between FY20 and FY21?
    numeric/table-dep: yes -- PP&E balances for FY20 and FY21 from a balance sheet
    prose answers it : no -- the surviving text is a balance-sheet table
    mask corrupts    : no -- deleted rows are numeric, not sentences
    verdict          : KEEP

  hqa_FB_7cc358e4_masked  [gate: narrative]
    Q                : Does AMCOR have an improving gross margin profile as of FY2023? If gross margin is not a useful 
    numeric/table-dep: yes -- gross margin from net sales and gross profit
    prose answers it : PARTLY -- the second clause invites a prose answer
    mask corrupts    : no -- deleted rows are numeric, not sentences
    verdict          : KEEP WITH CAVEAT

  hqa_FB_86637d3d_masked  [gate: numeric]
    Q                : Was there any drop in Cash & Cash equivalents between FY 2023 and Q2 of FY2024?
    numeric/table-dep: yes -- cash balances at two dates from a table
    prose answers it : no -- surviving text is a non-GAAP reconciliation table
    mask corrupts    : no -- deleted rows are numeric, not sentences
    verdict          : KEEP

  hqa_FB_d397e71d_masked  [gate: numeric]
    Q                : Is growth in JnJ's adjusted EPS expected to accelerate in FY2023?
    numeric/table-dep: yes -- 2022 adj-EPS growth vs 2023 guidance
    prose answers it : no -- both growth figures are gone
    mask corrupts    : no, but the document is visibly cut mid-clause
    verdict          : KEEP

  all 5 retained; none re-admitted; none created.
```
