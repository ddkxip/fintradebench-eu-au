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

**988 items across all five sources.**

| source | selected | eligible pool | transformation | where the data lives |
|---|---|---|---|---|
| FinTradeBench | 99 | 108 | none | `schemas/answer_schemas.jsonl` |
| FinanceBench | 59 | 59 | 36 none + 23 masked | `data/financebench_open_source.jsonl` |
| TAT-QA | 400 | 2,697 | numeric→directional | `TAT-QA-master/dataset_raw/` |
| FinQA | 400 | 1,385 | numeric→directional | `FinQA-main/dataset/` |
| ConvFinQA | 30 | 930 | numeric→directional | `ConvFinQA-main/data.zip` |

### Guarding against a degenerate baseline

The direction labels in these corpora are skewed (TAT-QA ~62% `increased`,
FinQA ~64%, ConvFinQA ~71%). Sampled proportionally, a system that always
answers `increased` would score around 63% **without reasoning at all**, and
the diagnostic would be passable for the wrong reason.

The TAT-QA and FinQA builders therefore draw a **seeded, label-stratified**
sample (`transforms.stratified_sample`): take every item from scarce classes,
then fill equally from abundant ones. Realised majority-class baselines:

| source | majority-class baseline |
|---|---|
| TAT-QA | 40.5% |
| FinQA | 49.0% |
| **ConvFinQA** | **76.7% — not yet stratified** |

**ConvFinQA is a known weak point.** Its 30 items are a head slice, not a
balanced draw, so its majority-class baseline is worse than the corpus prior.
Its eligible pool is 930 turns and a balanced draw could yield ~534 items at
roughly 50/50. Fixing it is one line — pass its items through
`stratified_sample` as the other two builders do, and raise `MAX_ITEMS`.
Until then, **do not read ConvFinQA accuracy as evidence of anything**;
report it with its baseline alongside.

Caps are CLI-adjustable:

```bash
python analysis/hedgeqa_collection/build_from_tatqa.py --max-items 800
python analysis/hedgeqa_collection/build_from_finqa.py  --max-items 600
```

ConvFinQA ships zipped; extract before building:

```bash
python -c "import zipfile; z=zipfile.ZipFile('ConvFinQA-main/data.zip');   z.extract('data/train.json','data/convfinqa_extract');   z.extract('data/dev.json','data/convfinqa_extract')"
```

Each builder also accepts a manually placed copy under `data/<name>/`.

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
| `hedgeqa_v0_1_manual_review.csv` | two-reviewer adjudication sheet |

## Before using this for a result

1. Work the manual-review sheet. `auto_validated` means well-formed, not
   correct.
2. Adjudicate `gold_commitment` with two reviewers and report agreement —
   the commitment call is the collection's load-bearing judgement, and in
   the parent project inter-annotator κ on exactly this call was 0.53–0.59.
3. Check the masked variants by hand, every one.
4. Report per benchmark.
