# AI-assisted review protocol — HedgeQA-Core-v0.1

## What this is

You have one human reviewer and 368 items. Two AI adjudicators — Gemini via
Antigravity and ChatGPT/Codex — review the same items blind, and their labels
are used to **find where an independent reader disagrees with you**, so your
limited human attention goes to the items that need it.

**AI labels are audit signal, not ground truth.** They never promote an item
by themselves. Everything they produce is stored in columns prefixed by the
reviewer name, kept separate from your `human_*` columns, and no script in
this directory writes `manually_validated`.

### Why AI reviewers are not a second human

They are not independent of each other. Gemini and ChatGPT share training
data, architecture family, and failure modes — the same evidence that fools
one plausibly fools the other. So:

- **AI-AI agreement is weak evidence.** Two models agreeing is consistent
  with two models making the same mistake. The agreement report puts
  human-vs-AI comparisons first for this reason.
- **AI-human disagreement is strong signal.** It means at least one reader
  saw something the other did not, which is exactly what you want surfaced.
- **They cannot substitute for the second human on `gold_commitment`.** If
  you need an inter-annotator κ to report, that still requires a second
  person. What these give you is triage.

## Files

| file | role |
|---|---|
| `export_blind_ai_review_batches.py` | writes blind batches from the core |
| `batches/*.jsonl`, `batches/*.md` | what you paste to a reviewer |
| `reveal/*_reveal.jsonl` | masked-item answer keys — **open only after a decision is recorded** |
| `AI_REVIEW_PROMPT.md` | the prompt to paste ahead of each batch |
| `ai_review_schema.json` | the output contract |
| `responses/` | where reviewer output goes |
| `merge_ai_reviews.py` | joins core + human + both AI |
| `analyze_ai_review_agreement.py` | writes the agreement report |
| `test_ai_review_pipeline.py` | smoke test for the merge/agreement logic |

## Running it

### 1. Export

```bash
python analysis/hedgeqa_collection/ai_review/export_blind_ai_review_batches.py
```

16 batches of ≤25: 6 natural, 6 directional, 4 masked. Families are never
mixed — a reviewer that calibrates on easy natural items would carry that
prior into the masked ones, and mixed batches make per-family agreement
impossible to read.

### 2. What blinding actually hides

Removed from every batch: `gold_label`, `gold_commitment`,
`validation_status`, `schema_confidence`, `exclusion_reason`,
`masked_content`.

Two subtler leaks were found and closed while building this, both of which
would have turned a blind review into a grading exercise:

- **Masked items.** The stored derivation says *"the evidence rows carrying
  its operands (`['16284', '6509']`) were removed"* — it names what is
  missing. A reviewer asked "can this still be answered?" would say no
  because we told them, not because they looked. Batches now carry a neutral
  note that some rows were removed, without saying which.
- **Directional items.** The stored derivation says *"the source answer −7.6
  is a change, mapped to `'decreased'`"* — that is the gold label in plain
  text. Batches now expose only the source arithmetic
  (`subtract(501.4, 509.0)`), so the reviewer derives the direction and can
  check the operand order, which is the actual review task.

The exporter asserts no blinded field appears in any batch and fails loudly
if one does.

### 3. Run the reviewers

For each batch, paste `AI_REVIEW_PROMPT.md`, then the batch `.md` (or
`.jsonl`). Save output as:

```
responses/gemini_antigravity__masked_batch01.jsonl
responses/chatgpt_codex__masked_batch01.jsonl
```

The filename prefix must be `gemini_antigravity` or `chatgpt_codex`; the
merger checks it against the `reviewer_name` field and reports a mismatch
rather than silently attributing a review to the wrong reviewer.

**Run the two reviewers in separate sessions.** Showing one model the
other's output destroys what little independence they have.

### 4. Your own review

Work `hedgeqa_core_v0_1_manual_review.csv` per
`HEDGEQA_CORE_REVIEW_PROTOCOL.md`. It is risk-ordered — masked items first.

**Do your review before reading the AI output.** If you read theirs first
you are no longer an independent third rater, and the disagreement counts
become meaningless. If you want AI help on a specific hard item, record your
own answer first, then look.

### 5. Merge and analyse

```bash
python analysis/hedgeqa_collection/ai_review/merge_ai_reviews.py
python analysis/hedgeqa_collection/ai_review/analyze_ai_review_agreement.py
```

Both degrade gracefully: a missing reviewer leaves blank columns and pushes
items to `review_needed` rather than counting silence as agreement. Run them
at any point to see partial progress.

## Promotion classes

Assigned by `merge_ai_reviews.py`. **These are routing labels, not
promotions.**

| class | condition |
|---|---|
| `strong_keep` | human keep + both AI keep + all three agree on `gold_commitment` **and** on `gold_label` |
| `review_needed` | any disagreement, a missing reviewer, a low-confidence keep, or any `unclear` flag |
| `exclude` | human excluded, **or** both AI reviewers excluded |

### One deliberate deviation from the specified rule

The specification defined `strong_keep` as agreement on `gold_commitment`
alone. Implemented that way, two reviewers can choose **contradictory
labels** — `yes` and `no` are both `committed` — and the item still
promotes. That defeats the purpose of collecting independent labels, so
label agreement is also required. The smoke test seeds exactly this case
(`plain[1]`) and asserts it routes to `review_needed`.

If you want the original behaviour, delete the label-agreement block in
`classify()`; the reason it is there is recorded in that function.

### What `strong_keep` does and does not mean

It means **nobody objected**. It does not mean verified. Three readers can
share a blind spot, and two of the three are language models whose errors
correlate. Treat it as "no evidence of a problem", which is the weakest form
of good news.

**A human decides every promotion.** No script promotes anything, and
nothing in this repository is `manually_validated`.

## How to act on the results

1. **Work `review_needed` first**, and inside it the high-risk list from the
   agreement report, in its printed order:
   - a masked item any reviewer could answer — a single credible
     reconstruction route falsifies the constructed gold, so exclude or
     re-mask;
   - a directional item whose transformation was challenged — check the
     operand order yourself;
   - three-way label splits;
   - commitment splits.
2. **Read the `flags` column.** `rollforward_reconstruction`,
   `total_minus_components`, `figure_repeated_elsewhere`,
   `direction_stated_in_prose` and `adjacent_period_proxy` are the five
   leak routes the masking guards target. A flag naming a *sixth* route is
   the most valuable output this whole exercise can produce — it means the
   guard set is incomplete, and `masking.py` should be extended rather than
   the item merely dropped.
3. **Check `exclude` before accepting it.** Both AI reviewers excluding is
   suggestive, not decisive; their errors correlate. Spot-check a sample.
4. **Watch the exclusion rate per stratum.** A high rate among masked items
   means the construction is unsound and needs revisiting, not patching item
   by item.

## Interpreting the agreement numbers

- **`gold_label`: raw agreement only.** 46 distinct labels appear across the
  core and the answer space is per-item, so there is no shared category set
  to compute chance agreement over. Raw agreement also *overstates* skill,
  because most items admit only 2–4 plausible labels.
- **`gold_commitment`: κ is meaningful** (three shared categories). Expect
  moderate values — two blinded *human* annotators reached only κ = 0.53–0.59
  on this exact judgement in the parent project. Moderate agreement is the
  expected result, not a failure of the workflow.
- **`keep_or_exclude`: κ is unstable when one class dominates.** If almost
  everything is kept, near-perfect raw agreement can still yield a low κ.
  The report says so where it happens; read the raw figure alongside.

## Honesty requirements for any write-up

If results from this collection are reported anywhere:

1. Say that AI-assisted labels were used, name the models, and state that
   they are audit labels rather than annotations.
2. Report human-vs-AI agreement and AI-vs-AI agreement **separately** — do
   not average them into one "inter-annotator agreement" figure, which would
   imply three independent raters.
3. Do not describe items as validated on the strength of AI agreement.
4. Report the exclusion rate and what was excluded.
