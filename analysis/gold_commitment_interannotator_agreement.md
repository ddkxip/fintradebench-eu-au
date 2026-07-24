# Gold-commitment inter-annotator agreement

Reanalysis only; no fabricated annotations. Annotator = an independently completed commitment sheet.

## Annotator availability

| annotator | file present | coverage | active (>=50%) | violations | missing |
|---|---|---|---|---|---|
| fable | yes | 100% | YES | 0 | 0 |
| codex | yes | 100% | YES | 0 | 0 |
| antigravity | yes | 100% | YES | 0 | 0 |
| human | yes | 27% | no | 0 | 101 |

**Active annotators: ['fable', 'codex', 'antigravity'].**

> Note on independence: `fable` is the analyst's own (non-blinded) audit; its non-blank calls equal the schema, so fable is NOT independent of the schema baseline. Genuine inter-annotator agreement requires the BLINDED external annotators (codex, antigravity). Run them on `analysis/gold_commitment_audit_sheet_blinded.csv` (see BLINDED_ANNOTATOR_INSTRUCTIONS.md), then rerun this script.

## Pairwise agreement + Cohen's kappa (binary commitment)

All present annotator pairs, computed on their complete-case overlap. `fable` is the analyst's own non-blinded audit (≈schema); `codex`/`antigravity` are the independent blinded external raters; `human` is partial (low n).

| pair | n common | exact-label agree | commit agree | Cohen kappa | note |
|---|---|---|---|---|---|
| fable vs codex | 139 | 0.863 | 0.813 | 0.271 | vs non-blinded self-audit |
| fable vs antigravity | 139 | 0.892 | 0.892 | 0.683 | vs non-blinded self-audit |
| fable vs human | 38 | 0.974 | 1.000 | 1.000 | low-n (partial annotator) |
| codex vs antigravity | 139 | 0.914 | 0.863 | 0.590 | **independent blinded pair** |
| codex vs human | 38 | 0.763 | 0.605 | 0.271 | low-n (partial annotator) |
| antigravity vs human | 38 | 0.895 | 0.921 | 0.834 | low-n (partial annotator) |

**Fleiss' kappa across the 3 active annotators (fable, codex, antigravity; n=139 complete items): 0.531.**

**Headline (independent blinded pair, codex vs antigravity, n=139): commitment agreement 0.863, Cohen kappa 0.590.**

## Commitment disagreements and majority vote

- rows with any commitment disagreement among active annotators: **30**
```
question_id       schema        fable        codex  antigravity
         F1 noncommitted noncommitted    committed noncommitted
        FT1 noncommitted noncommitted    committed noncommitted
       FT10    committed    committed noncommitted noncommitted
       FT25 noncommitted noncommitted    committed noncommitted
        F16    committed    committed    committed noncommitted
         F6 noncommitted noncommitted    committed noncommitted
         F7 noncommitted noncommitted    committed noncommitted
       FT17 noncommitted noncommitted    committed noncommitted
       FT22 noncommitted noncommitted    committed noncommitted
        FT3    committed    committed    committed noncommitted
       FT30 noncommitted noncommitted    committed noncommitted
       FT35    committed    committed    committed noncommitted
       FT42 noncommitted noncommitted    committed noncommitted
       FT44 noncommitted noncommitted    committed noncommitted
       FT49 noncommitted noncommitted    committed noncommitted
        FT5    committed    committed    committed noncommitted
       FT50 noncommitted noncommitted    committed noncommitted
        FT9 noncommitted noncommitted    committed noncommitted
        T11    committed    committed noncommitted noncommitted
        T12    committed    committed noncommitted noncommitted
        T20    committed    committed noncommitted noncommitted
        T23    committed    committed noncommitted noncommitted
        T31    committed    committed noncommitted    committed
        T37    committed    committed noncommitted noncommitted
         T4    committed    committed noncommitted noncommitted
        T40    committed    committed noncommitted noncommitted
        T42    committed    committed noncommitted noncommitted
        T48    committed    committed noncommitted noncommitted
         T6    committed    committed noncommitted noncommitted
         T7 noncommitted noncommitted    committed noncommitted
```