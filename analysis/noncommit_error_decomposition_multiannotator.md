# Non-commitment error decomposition — multi-annotator

Primary set = gemma4 + qwen3:8b final rows (n=278). Reanalysis only. One column per available commitment version.

| version | hedge_collision | overcommit | wrong_direction | wrong_nc_type | committed-cell AUROC | survives? |
|---|---|---|---|---|---|---|
| A_schema | 0.617 | 0.055 | 0.29 | 0.038 | 0.421 | YES |
| fable | 0.617 | 0.055 | 0.29 | 0.038 | 0.421 | YES |
| codex | 0.618 | 0.105 | 0.262 | 0.016 | 0.457 | YES |
| antigravity | 0.55 | 0.144 | 0.256 | 0.05 | 0.424 | YES |
| E_majority | 0.574 | 0.093 | 0.251 | 0.082 | 0.429 | YES |
| F_blinded_consensus | 0.574 | 0.093 | 0.251 | 0.082 | 0.429 | YES |

**Survival criterion:** hedge_collision remains the leading error mode (>=30% and modal) AND p_noncommit shows no wrong-direction signal (committed-cell AUROC < 0.55, i.e. ~chance).

## Verdict

Across the **6** currently-available commitment version(s) (A_schema, fable, codex, antigravity, E_majority, F_blinded_consensus), the hedge-collision conclusion **survives in all**: hedge_collision stays the leading error mode and p_noncommit remains a hedge-collision detector with ~chance signal in the non-mechanical cell. This holds under every annotator version and the majority vote.