# HedgeQA-v0.1 item schema

Normative reference for `hedgeqa_schema.py`. Every item in
`data/hedgeqa/**` conforms to this.

## Fields

| # | field | type | meaning |
|---|---|---|---|
| 1 | `source_benchmark` | enum | `fintradebench` / `financebench` / `tatqa` / `finqa` / `convfinqa` |
| 2 | `source_id` | str | the id in the source corpus; must round-trip |
| 3 | `question` | str | the question as presented to the system |
| 4 | `oracle_evidence` | str | the evidence given at inference time |
| 5 | `evidence_provenance` | str | where that text came from, specifically enough to re-derive |
| 6 | `answer_type` | str | e.g. `yes_no`, `company_choice`, `directional_change` |
| 7 | `answer_space` | list[str] | exhaustive, mutually exclusive labels |
| 8 | `gold_label` | str | reference label; must be in `answer_space` |
| 9 | `noncommit_labels` | list[str] | subset of `answer_space` that declines to settle |
| 10 | `gold_commitment` | enum | `committed` / `noncommitted` / `ambiguous_exclude` |
| 11 | `transformation_type` | enum | `none` / `numeric_to_directional` / `comparison_to_choice` / `evidence_masked_insufficient` |
| 12 | `requires_rag` | bool | always `False`; validated |
| 13 | `validation_status` | enum | `candidate` / `auto_validated` / `manually_validated` / `excluded` |
| 14 | `exclusion_reason` | str? | required when `validation_status == "excluded"` |
| 15 | `schema_confidence` | float | 0–1; how much to trust the schema, not the model |

Plus an audit trail: `original_question`, `derivation`, `masked_content`,
`notes`, and the generated `hedgeqa_id`.

### `hedgeqa_id`

`hqa_<TAG>_<sha1(source_benchmark|source_id|suffix)[:8]>[_<suffix>]`, with
TAG in {FTB, FB, TAT, FQ, CFQ}. Deterministic, so rebuilding the collection
yields identical ids.

## What the status values mean

- `candidate` — built, not yet certified.
- `auto_validated` — passes every structural check. **This means well-formed,
  NOT correct.** It asserts nothing about whether the gold label is right.
- `manually_validated` — a human has confirmed the gold label against the
  evidence. Only this status licenses treating an item as ground truth.
- `excluded` — failed a check or a source-specific audit; `exclusion_reason`
  says which. Excluded items are **kept in the candidate files** rather than
  deleted, so the decision stays visible and reversible.

## Validators

Enforced by `validate()`; the first failure becomes the exclusion reason.

1. **`enums`** — all enum fields hold legal values.
2. **`answer_space_size`** — at least 2 committed labels, or 1 committed plus
   at least 1 non-committal. *An answer space that cannot express a hedge
   cannot exercise the phenomenon under study.*
3. **`noncommit_subset`** — `noncommit_labels ⊆ answer_space`.
4. **`gold_in_space`** — `gold_label ∈ answer_space`.
5. **`no_duplicate_labels`** — no repeated labels.
6. **`evidence_present`** — `oracle_evidence` ≥ 120 chars.
7. **`no_rag`** — `requires_rag is False`.
8. **`transformation_audit`** — any item with `transformation_type != "none"`
   carries both `original_question` and `derivation`. *A rewrite without its
   licence is unreviewable.*
9. **`masked_variant_marked`** — a controlled-insufficient item must have a
   non-committal `gold_label`, `gold_commitment == "noncommitted"`, non-empty
   `masked_content`, and `_masked` in its id.
10. **`gold_commitment_consistent`** — `gold_commitment` agrees with whether
    `gold_label` is in `noncommit_labels` (unless flagged
    `ambiguous_exclude`).

## Transformation types

**`none`** — used as written. The only type that needs no derivation.

**`numeric_to_directional`** — a free-form numeric answer has no finite
answer space and therefore no non-committal label, so no hedging metric is
computable on it. Change-shaped questions map onto
`{increased, decreased, roughly_unchanged, insufficient_data}`. Applied only
when the source question already asks about a change, so the task is not
silently replaced.

**`comparison_to_choice`** — an entity comparison becomes pick-one over the
named entities plus `none_clear` / `insufficient_data`.

**`evidence_masked_insufficient`** — the question is unchanged and the
evidence lines carrying the decisive figures are removed, making
`insufficient_data` correct **by construction**. See the README for why these
exist and `masking.py` for the guards. These are constructed items: they are
never auto-promoted, must be reviewed by a human, and must be analysed
separately from natural items.
