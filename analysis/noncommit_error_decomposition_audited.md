# Non-commitment error decomposition — AUDITED gold commitment

Primary set = gemma4 + qwen3:8b final-round rows (n=278), matching the original decomposition. Reanalysis only.

This reruns NONCOMMIT_ERROR_DECOMPOSITION with audited commitment labels and reports original vs audited side by side.

## Error-type shares: original (schema) vs audited

| error type | schema share | audited share | hostile-bound share |
|---|---|---|---|
| hedge_collision | 0.617 | 0.617 | 0.492 |
| overcommitment | 0.055 | 0.055 | 0.071 |
| wrong_direction_commitment | 0.29 | 0.29 | 0.273 |
| wrong_noncommit_type | 0.038 | 0.038 | 0.164 |

'hostile-bound' = the maximally hedge-deflating scenario: all 15 hedge-adjacent committed golds reclassified non-committed (taxonomy flag only). This bounds how far hedge_collision could fall under an adversarial reviewer.

## AUROC of p_noncommit for strict error: original vs audited

| subset | schema AUROC | audited AUROC |
|---|---|---|
| all questions | 0.671 | 0.671 |
| committed-gold only | 0.815 | 0.815 |
| noncommitted-gold only | 0.214 | 0.214 |
| committed-gold & committed-pred | 0.421 | 0.421 |

(committed-gold n=234; noncommit-gold n=44; committed∧committed-pred cell n=121.)

## Plain-English guidance — does the hedge-collision conclusion survive?

**Yes.** The audit changed **0** commitment assignments, so the audited decomposition is identical to the original: hedge collisions remain 62% of errors and p_noncommit keeps AUROC 0.81 on committed-gold vs 0.42 (≈chance) in the non-mechanical committed∧committed-pred cell — i.e. still a hedge-collision detector with no wrong-direction signal.

Crucially, even the **hostile bound** — reclassifying all 15 hedge-adjacent committed golds as non-committal — only lowers hedge_collision share to **49%** (from 62%), with overcommitment rising to 7%. Hedge collision remains the largest error mode even under maximally adversarial relabeling. The conclusion is robust to plausible gold-commitment disagreement.