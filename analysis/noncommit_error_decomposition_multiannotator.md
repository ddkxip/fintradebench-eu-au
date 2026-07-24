# Non-commitment error decomposition — multi-annotator

Primary set = gemma4 + qwen3:8b final rows (n=278). Reanalysis only. One column per available commitment version.

| version | hedge_collision | overcommit | wrong_direction | wrong_nc_type | committed-cell AUROC | survives? |
|---|---|---|---|---|---|---|
| A_schema | 0.617 | 0.055 | 0.29 | 0.038 | 0.421 | YES |
| fable | 0.617 | 0.055 | 0.29 | 0.038 | 0.421 | YES |

**Survival criterion:** hedge_collision remains the leading error mode (>=30% and modal) AND p_noncommit shows no wrong-direction signal (committed-cell AUROC < 0.55, i.e. ~chance).

**Pending annotators:** ['codex', 'antigravity'] — their templates are blank. Versions C/D and majority vote will populate automatically when `analysis/gold_commitment_audit_{codex,antigravity}.csv` are filled and this script is rerun.

## Verdict

Across the **2** currently-available commitment version(s) (A_schema, fable), the hedge-collision conclusion **survives in all**: hedge_collision stays the leading error mode and p_noncommit remains a hedge-collision detector with ~chance signal in the non-mechanical cell. Full multi-annotator + majority-vote confirmation is pending the blinded external annotations (codex, antigravity).