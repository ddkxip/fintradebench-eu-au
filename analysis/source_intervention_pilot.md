# E-C' source-intervention results (gemma4, R0, F+FT, K=10)

Control = ea_full_gemma4 round-0 oracle baseline; paired within-question.

- questions run: 30; arms: ['horizon_long', 'horizon_short', 'inject_conflict', 'remove_placebo', 'remove_top']

## Paired do-effects vs oracle baseline (mean delta [95% CI], Wilcoxon p)

| arm | metric | delta | 95% CI | p | n |
|---|---|---|---|---|---|
| remove_top | p_noncommit | +0.0035 | [-0.0481, +0.0633] | 0.938 | 30 |
| remove_top | au_mm | +0.0197 | [-0.0626, +0.0940] | 0.384 | 30 |
| remove_top | eu_mm | -0.0204 | [-0.0805, +0.0316] | 0.72 | 30 |
| remove_top | gold_prob | -0.0088 | [-0.0354, +0.0150] | 0.469 | 30 |
| remove_placebo | p_noncommit | -0.0226 | [-0.0594, +0.0067] | 0.312 | 30 |
| remove_placebo | au_mm | +0.0379 | [-0.0388, +0.1034] | 0.102 | 30 |
| remove_placebo | eu_mm | -0.0154 | [-0.0515, +0.0202] | 0.38 | 30 |
| remove_placebo | gold_prob | -0.0221 | [-0.0650, +0.0150] | 0.219 | 30 |
| inject_conflict | p_noncommit | +0.0277 | [+0.0000, +0.0677] | 0.125 | 29 |
| inject_conflict | au_mm | -0.0184 | [-0.0961, +0.0551] | 0.684 | 29 |
| inject_conflict | eu_mm | -0.0407 | [-0.0870, -0.0011] | 0.102 | 29 |
| inject_conflict | gold_prob | -0.0159 | [-0.0345, -0.0022] | nan | 29 |
| horizon_short | p_noncommit | +0.0368 | [-0.0000, +0.0888] | 0.156 | 30 |
| horizon_short | au_mm | +0.0066 | [-0.0702, +0.0752] | 0.534 | 30 |
| horizon_short | eu_mm | -0.0729 ** | [-0.1454, -0.0128] | 0.0398 | 30 |
| horizon_short | gold_prob | -0.0387 | [-0.0967, +0.0067] | 0.25 | 30 |
| horizon_long | p_noncommit | +0.0223 | [-0.0015, +0.0486] | 0.219 | 30 |
| horizon_long | au_mm | +0.0778 | [-0.0298, +0.1887] | 0.12 | 30 |
| horizon_long | eu_mm | -0.0365 | [-0.0993, +0.0265] | 0.243 | 30 |
| horizon_long | gold_prob | -0.0371 ** | [-0.0771, -0.0042] | 0.043 | 30 |

## Construct validity: evidence-removal selectivity

Diagonal (remove_top) should move uncertainty; off-diagonal (remove_placebo, matched non-golden removal) should NOT. A large top-minus-placebo gap = the uncertainty responds to *relevant* evidence loss, not to any evidence loss.

- **p_noncommit**: remove_top +0.0035 vs placebo -0.0226; top-minus-placebo +0.0261 (paired p=0.438, n=30)
- **au_mm**: remove_top +0.0197 vs placebo +0.0379; top-minus-placebo -0.0182 (paired p=0.948, n=30)
- **gold_prob**: remove_top -0.0088 vs placebo -0.0221; top-minus-placebo +0.0133 (paired p=0.812, n=30)

## Horizon sensitivity (short vs long, same evidence)

- gold_prob long-minus-short: +0.0017 (p=0.773, n=30)
- p_noncommit long-minus-short: -0.0145 (p=0.719, n=30)
- verdict flips short vs long: 3/30

(Flat horizon response = horizon-insensitivity finding: the system's verdict does not condition on the stated horizon.)

## inject_conflict by lane (does explicit F/T conflict break the hedge?)

- F eu_mm: -0.0698 [-0.1551,+0.0091] p=0.203 (n=14)
- F p_noncommit: +0.0467 [-0.0036,+0.1259] p=nan (n=14)
- FT eu_mm: -0.0135 [-0.0341,+0.0000] p=nan (n=15)
- FT p_noncommit: +0.0100 [+0.0000,+0.0300] p=nan (n=15)