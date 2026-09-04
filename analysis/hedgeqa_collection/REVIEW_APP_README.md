# HedgeQA-Core-v0.1 review app

A local, single-item-at-a-time Streamlit app for the human review of the
368-item core. It replaces scrolling a 21-column CSV.

## Install

```bash
pip install streamlit
```

Nothing else is needed — the app uses only the standard library beyond
Streamlit, and reads the collection files already in this repo.

## Run

```bash
streamlit run analysis/hedgeqa_collection/review_app.py
```

If `streamlit` is not on your PATH (common on Windows), use:

```bash
python -m streamlit run analysis/hedgeqa_collection/review_app.py
```

It opens at `http://localhost:8501`. Everything is local; the app makes no
network calls and runs no models.

## Files

| file | mode |
|---|---|
| `data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl` | **read only** — never modified |
| `analysis/hedgeqa_collection/hedgeqa_core_v0_1_manual_review.csv` | **read only** — seeds the first run, never modified |
| `analysis/hedgeqa_collection/hedgeqa_core_v0_1_human_review_in_progress.csv` | written — your working file |
| `analysis/hedgeqa_collection/review_backups/in_progress_<timestamp>.csv` | written — a copy before every overwrite (last 40 kept) |
| `analysis/hedgeqa_collection/hedgeqa_core_v0_1_manual_review_completed.csv` | written on **Export completed review** |

Every button press autosaves the working file, and a timestamped backup is
written first, so a crash or a misclick costs at most the current item.

Close and reopen the app freely — it resumes from the in-progress file.

## How blinding is preserved

The point of this review is an independent judgement, so the app must never
show anything that anchors it. Three leaks are closed, and two are not
obvious:

1. **The candidate JSONL contains the pipeline's own answers** —
   `gold_label`, `gold_commitment`, `validation_status`, `schema_confidence`.
   Items are projected through `blind_item()` into a dict holding only the
   permitted keys, so those values never enter app state and no widget can
   render them. A startup assertion fails loudly if one survives.

2. **The manual-review CSV contains `gold_label_auto` and
   `gold_commitment_auto`** (columns 10 and 13). They are dropped when the
   working file is seeded, so the in-progress CSV does not contain them
   either — opening it in Excel mid-review will not spoil you. They are
   re-joined from the original CSV only at final export, because the
   downstream merger expects that schema.

3. **`derivation` restates the answer in prose.** For a directional item the
   stored text reads *"…the source answer −7.6 … mapped to `'decreased'`"*;
   for a masked item it names the removed operands. Both pass through the
   same sanitisers used for the AI blind batches, so you see the source
   arithmetic (which you need, to check operand order) but not our computed
   direction, and you are told rows were removed but not which ones.

The app also never opens `ai_review/responses/`, `ai_review/reveal/`, or
`masked_content`, and computes no agreement.

## What NOT to open until your review is complete

Do not read these until you have exported your completed review:

| do not open | why |
|---|---|
| `ai_review/responses/*.jsonl` | Gemini and ChatGPT labels — reading them makes you a second reader of their output rather than an independent third rater, and the agreement numbers stop meaning what they appear to mean |
| `ai_review/reveal/*_reveal.jsonl` | tells you exactly which rows were removed from every masked item, which decides the hardest judgement for you |
| `ai_review/hedgeqa_core_review_merged.csv` | contains both AI reviewers' columns |
| `data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl` (raw) | contains the pipeline's `gold_label` |
| `hedgeqa_core_v0_1_manual_review.csv` (raw) | contains `gold_label_auto` |

`ai_review/AI_REVIEW_RESPONSE_QA.md` **is** safe — it was written to be
blind-safe and contains only structural counts.

The reveal files exist for a legitimate purpose: after you record a decision
on a masked item, they let you check what was actually removed. Use them
that way round — decision first, reveal second — and note in `notes` if the
reveal changed your mind.

## Using it

**Sidebar filters** — unreviewed only (on by default), family (masked /
directional / natural), items with a non-committal label available, source
benchmark, keep/exclude status, needs-second-look.

**Sidebar progress** — reviewed vs remaining, counts by source and by
family, and how many you have kept, excluded, flagged for a second look or
skipped.

**Per item you fill** — `reviewer_gold_label` (radio over the answer space,
with non-committal options marked ⟨non-committal⟩), `reviewer_gold_commitment`,
`evidence_sufficient_for_gold`, `transformation_valid`,
`masked_variant_valid`, `keep_or_exclude`, `exclusion_reason`, `notes`, plus
family-specific flags.

**Commitment is auto-suggested** from the label you pick — a non-committal
label suggests `noncommitted`, anything else suggests `committed` — and it
follows the label if you change your mind. Override it freely; the app says
when you have.

**Masked items** show a prominent reminder that
`evidence_sufficient_for_gold = no` is the *expected* answer when the mask is
valid, and offer the reconstruction-route flags: `rollforward_reconstruction`,
`total_minus_components`, `figure_repeated_elsewhere`,
`direction_stated_in_prose`, `adjacent_period_proxy`, `evidence_gutted`,
`other`.

**Directional items** show the sanitised source arithmetic and a reminder to
check operand order and direction-neutrality, with flags
`operand_order_suspect`, `question_presupposes_direction`,
`cross_sectional_not_temporal`, `wrong_entity_or_period`, `other`.

**Buttons** — Save, Save and Next, Previous, Next, Skip for later, Needs
second look.

### Validation

A save as *reviewed* is refused, with the reason shown in red at the top,
unless:

- `reviewer_gold_label` is set and is a member of that item's answer space;
- `reviewer_gold_commitment` is set;
- `evidence_sufficient_for_gold` is set;
- `exclusion_reason` is non-empty when `keep_or_exclude` is `exclude`;
- `masked_variant_valid` is set for a masked item;
- `transformation_valid` is set for a directional item.

*Skip for later* and *Needs second look* bypass validation on purpose, so you
can park a hard item without inventing an answer for it.

## When you finish

Click **Export completed review** to write
`hedgeqa_core_v0_1_manual_review_completed.csv`. It carries your columns plus
the original schema, so the downstream merger reads it directly.

The merger currently reads `hedgeqa_core_v0_1_manual_review.csv`. Point it at
the completed file — either edit `HUMAN` in
`ai_review/merge_ai_reviews.py`, or copy the completed file over the original
once you are satisfied with it.

Then, and only then:

```bash
python analysis/hedgeqa_collection/ai_review/merge_ai_reviews.py
python analysis/hedgeqa_collection/ai_review/analyze_ai_review_agreement.py
```

Exporting before you are finished is safe — unreviewed items export blank and
the sidebar warns you how many.

## Reference

Follow `HEDGEQA_CORE_REVIEW_PROTOCOL.md` for the judgement rules themselves:
what `gold_commitment` means, how to test a masked variant, how to check a
directional transformation, and when to exclude. The overriding rule is
there and worth repeating — **when in doubt, exclude**: an excluded item
costs one row, while an item kept with a wrong label produces a number that
looks fine and is false.
