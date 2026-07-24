# Gold-commitment inter-annotator agreement

Reanalysis only; no fabricated annotations. Annotator = an independently completed commitment sheet.

## Annotator availability

| annotator | file present | coverage | active (>=50%) | violations | missing |
|---|---|---|---|---|---|
| fable | yes | 100% | YES | 0 | 0 |
| codex | yes | 0% | no | 0 | 139 |
| antigravity | yes | 0% | no | 0 | 139 |
| human | yes | 1% | no | 1 | 138 |

**Active annotators: ['fable'].**

> Note on independence: `fable` is the analyst's own (non-blinded) audit; its non-blank calls equal the schema, so fable is NOT independent of the schema baseline. Genuine inter-annotator agreement requires the BLINDED external annotators (codex, antigravity). Run them on `analysis/gold_commitment_audit_sheet_blinded.csv` (see BLINDED_ANNOTATOR_INSTRUCTIONS.md), then rerun this script.

## Pairwise agreement + Cohen's kappa (binary commitment)

_Pending: fewer than two active annotators. Cohen's / Fleiss' kappa cannot be computed until the blinded external annotations (codex, antigravity) are supplied._

## Commitment disagreements and majority vote

_Majority vote defaults to schema until >=2 active annotators exist._