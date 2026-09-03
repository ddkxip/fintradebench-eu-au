# HedgeQA-v0.1

## What this is not

**HedgeQA is not a new general financial benchmark.** It does not measure
financial reasoning ability, it is not a leaderboard, and a score on it is
not a capability claim. It is deliberately small, deliberately curated, and
draws its items from other people's benchmarks.

## What it is

A **diagnostic question collection for hedging failures**. Every item is
shaped so that these are all computable:

- **hedge collision** — the system declines; the reference settles
- **overcommitment** — the system answers; the reference declines
- **wrong-direction commitment** — the system commits to the wrong option
- **wrong non-committal type** — both decline, but differently
- **`p_noncommit`** — probability mass on non-committal labels
- **AU / EU debate behaviour** — the aleatoric/epistemic decomposition

That requires three things a raw benchmark rarely provides at once: a finite
and exhaustive answer space, an explicit set of non-committal labels, and a
reference label that is itself classified as committed or not.

## Why oracle evidence

Every item ships the evidence it is to be answered from, and
`requires_rag` is `False` on all of them (validated, not assumed).

Retrieval introduces a second failure source that is easily mistaken for the
one under study: a system that declines because retrieval missed the
relevant page looks identical, in the output, to a system that declines
because it will not commit. Fixing the evidence removes that confound. It is
a measurement choice, not a claim that deployments have oracle evidence —
and it means results here are an **upper bound** on the behaviour of a
retrieval-backed deployment.

## Why controlled-insufficient variants

A collection of questions whose references all settle can only ever measure
hedge collision. On such a set, **"never hedge" is a winning strategy**, and
a system that correctly recognises missing evidence is indistinguishable
from one that guesses.

The `evidence_masked_insufficient` variants fix this by removing the decisive
evidence from an item whose answer is otherwise known, making
`insufficient_data` correct *by construction*. In v0.1 they lift the
non-committal share from 14% to 27%.

They are **constructed items and are treated as such**:

- marked `transformation_type = "evidence_masked_insufficient"`, id suffixed
  `_masked`, with the removed text kept in `masked_content`;
- never auto-promoted past `candidate` — structural validity does not
  establish that the masked evidence truly cannot answer the question;
- **analysed separately.** Pooling them into a non-commitment base rate
  would report a property of our masking as a property of the models.

`masking.py` documents two flaws found while building this — a naive salience
heuristic that deleted unrelated rows, and a post-condition that could never
fail — and the guards that replaced them. Those guards narrow the candidate
set; they do not certify it. Human review is mandatory.

## Reporting rules

**Benchmark-stratified results are primary. Pooled results are descriptive
only.** The sources differ in evidence style, answer space, question
difficulty and annotation provenance; a pooled number averages unlike things
and its movement between systems can be driven by composition rather than
behaviour. Report per benchmark, then pool if you must, and say which is
which.

## Current state (v0.1)

**1,658 items across all five sources.**

| source | natural | masked | eligible pool | transformation |
|---|---|---|---|---|
| FinTradeBench | 99 | – | 108 | none |
| FinanceBench | 36 | 23 | 59 | none + masked |
| TAT-QA | 400 | 100 | 2,697 | numeric→directional |
| FinQA | 400 | 100 | 1,385 | numeric→directional |
| ConvFinQA | 400 | 100 | 930 | numeric→directional |

### Guarding against a degenerate baseline

The direction labels in these corpora are skewed (TAT-QA ~62% `increased`,
FinQA ~64%, ConvFinQA ~71%), and head slices are not samples — the corpora
group questions by filing. All three directional builders therefore draw a
**seeded, label-stratified** sample (`transforms.stratified_sample`).

| source | n | majority-class baseline |
|---|---|---|
| FinTradeBench | 99 | 14.1% |
| FinanceBench | 59 | 42.4% |
| TAT-QA | 500 | 32.4% |
| FinQA | 500 | 39.2% |
| ConvFinQA | 500 | 39.8% |

No component is passable by guessing a single label. Caps are CLI-adjustable:

```bash
python analysis/hedgeqa_collection/build_from_tatqa.py --max-items 800 --masked-items 200
```

### Masking beyond FinanceBench

Masking now covers the directional benchmarks too, which are a **better**
target than FinanceBench's yes/no items: TAT-QA ships an explicit
`derivation` and FinQA/ConvFinQA a `program`, so the figures the answer
depends on are stated rather than inferred from prose. Their answer space
already contains `insufficient_data`, so a masked variant needs no new label.

This lifts the non-committal share from **9.5% to 25.9%** (429/1,658), with
323 masked variants.

Directional masked variants are drawn from pool items **not** selected as
natural items, so no masked/natural pair shares an evidence document.
Pairing would correlate their errors and make any CI over pooled items too
narrow.

#### Two reconstruction leaks found by hand, now guarded

Removing the literal figure is not enough — financial tables let it be
recomputed. Both were found by reading actual masked output, and neither is
caught by any other check, because the operand really is absent as a string:

1. **Roll-forward.** A movement table's surviving components still sum to the
   removed closing balance: `8,053 + 5,253 + 1,256 − 7,563 − 490 = 6,509`.
2. **Total minus components.** A summary table keeps its total row, so a
   removed component returns as `23,678 − (13 + 7,381) = 16,284`.

`reconstructible_by_column_sum` now checks both directions per table column,
and `test_masking.py` pins each with the real numbers. Every shipped variant
was independently re-verified against both patterns: **0 of 323 are
reconstructible.**

This does not make the masks certified. A model may still recover an answer
through a route these checks do not model — a ratio rebuilt from unrelated
components, or a direction inferred from surrounding prose. The guards narrow
the candidate set; **human review remains mandatory**, and every masked item
is held at `candidate` and never auto-promoted.

## Pipeline

```bash
python analysis/hedgeqa_collection/build_from_fintradebench.py
python analysis/hedgeqa_collection/build_from_financebench.py
python analysis/hedgeqa_collection/build_from_tatqa.py
python analysis/hedgeqa_collection/build_from_finqa.py
python analysis/hedgeqa_collection/build_from_convfinqa.py
python analysis/hedgeqa_collection/validate_candidates.py --write
python analysis/hedgeqa_collection/build_collection.py
python analysis/hedgeqa_collection/build_scoping_report.py
python analysis/hedgeqa_collection/test_masking.py
```

Nothing in this pipeline calls a model, and nothing writes to an existing
FinTradeBench or FinanceBench file — all output goes to `data/hedgeqa/` and
this directory.

## Files

| path | role |
|---|---|
| `hedgeqa_schema.md` | normative field + validator spec |
| `hedgeqa_schema.py` | dataclass, id scheme, validators, JSONL io |
| `masking.py` | controlled-insufficient masking and its guards |
| `transforms.py` | numeric→directional, comparison→choice |
| `build_from_*.py` | one candidate builder per source |
| `validate_candidates.py` | runs validators, promotes or excludes |
| `build_collection.py` | assembles v0.1 + the review sheet |
| `build_scoping_report.py` | regenerates the scoping report from disk |
| `test_masking.py` | asserts each masking guard can actually fire |
| `HEDGEQA_COLLECTION_SCOPING.md` | generated report — do not hand-edit |
| `HEDGEQA_QA_AUDIT.md` | QA audit: counts, baselines, validator results, review risks |
| `hedgeqa_v0_1_manual_review.csv` | two-reviewer adjudication sheet |

## Status

**CANDIDATE-ONLY — not validated.** See `HEDGEQA_QA_AUDIT.md`. The build is
deterministic and every structural invariant holds, but 323 items carry a
constructed gold label that no automated check can certify, and no item is
`manually_validated` yet.

## Before using this for a result

1. Work the manual-review sheet. `auto_validated` means well-formed, not
   correct.
2. Adjudicate `gold_commitment` with two reviewers and report agreement —
   the commitment call is the collection's load-bearing judgement, and in
   the parent project inter-annotator κ on exactly this call was 0.53–0.59.
3. Check the masked variants by hand, every one.
4. Report per benchmark.
