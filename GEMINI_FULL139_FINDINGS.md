# gemini-3-flash — full E-A findings

Reanalysis of `results/gemini_full139/rows.csv` (139 headline-eligible questions, R0+R1, K=10 F/FT / 20 T). Metric definitions identical to analyze_ea_full.py; no new model calls.
- parse rate: 1.000; scored final rows: 139

## 1-2. Accuracy (strict) by round and lane

- overall R0 acc = **0.504**, R1 acc = **0.590**
```
round      0      1
lane               
F      0.612  0.714
FT     0.460  0.560
T      0.425  0.475
```

## 3. TU / AU / EU (normalized) + Miller-Madow by lane and round

```
            tu_norm  au_norm  eu_norm  au_mm  eu_mm  tu_mm
lane round                                                
F    0        0.181    0.087    0.094  0.122  0.122  0.244
     1        0.158    0.069    0.088  0.101  0.116  0.216
FT   0        0.207    0.097    0.110  0.147  0.152  0.298
     1        0.233    0.075    0.158  0.114  0.224  0.337
T    0        0.129    0.066    0.063  0.114  0.103  0.216
     1        0.124    0.037    0.087  0.066  0.144  0.210
```

## 4. Debate deltas R0->R1 (paired)

- dAU: mean -0.0225, Wilcoxon p=1.30e-01 (nonzero n=64)
- dEU: mean +0.0224, Wilcoxon p=6.55e-02 (nonzero n=69)
- dNC: mean -0.0459, Wilcoxon p=4.26e-03 (nonzero n=48)
- dG: mean +0.0322, Wilcoxon p=4.92e-02 (nonzero n=58)

## 5. p_noncommit by lane and round

```
             mean  median
lane round               
F    0      0.398   0.350
     1      0.315   0.000
FT   0      0.605   0.650
     1      0.567   0.525
T    0      0.049   0.000
     1      0.038   0.000
```
- degenerate rows (TU=0): 0.568 overall; R1 0.568

## 6. AUROC for error prediction (final round)

error rate = 0.41
| predictor | AUROC (all) | AUROC committed-gold | AUROC commit-gold&commit-pred |
|---|---|---|---|
| tu_norm | 0.512 | 0.468 | 0.501 |
| au_norm | 0.532 | 0.544 | 0.553 |
| eu_norm | 0.496 | 0.443 | 0.497 |
| p_noncommit | 0.645 | 0.722 | 0.455 |

(committed-gold n=117; committed-gold & committed-pred n=93 — the non-mechanical cell.)

## 7. Non-commitment error decomposition (final round)

```
                             n  share
error_type                           
wrong_direction_commitment  25  0.439
hedge_collision             24  0.421
overcommitment               7  0.123
wrong_noncommit_type         1  0.018
```
- non-committal gold questions: 22; correct-noncommitment rate: 0.93 (n_hedged=15)

### share of errors by lane
```
lane  error_type                
F     hedge_collision               0.571
      overcommitment                0.143
      wrong_direction_commitment    0.286
FT    hedge_collision               0.682
      overcommitment                0.136
      wrong_direction_commitment    0.136
      wrong_noncommit_type          0.045
T     hedge_collision               0.048
      overcommitment                0.095
      wrong_direction_commitment    0.857
```

## 8. Debate transitions (R0->R1)

- outcome: {'STABLE_SUCCESS': 66, 'STABLE_FAILURE': 53, 'DEBATE_RESCUE': 16, 'CORRECTNESS_LOST': 4}
- flow: {'NO_MATERIAL_CHANGE': 69, 'MIXED_FLOW': 37, 'PRODUCTIVE_CONVERGENCE': 11, 'NOISE_REDUCTION': 10, 'ALEATORIC_DESTABILIZATION': 8, 'FALSE_CONSENSUS': 4}
- rescue: 16, loss: 4, stable-correct: 66, stable-wrong: 53
- false consensus: 4 (2.9%); minority suppression: 1

## 9. Cross-model comparison

(gemini = 16-q subset, flagged; not pooled with the 139-q models)

```
                      model  n_q  R0_acc  R1_acc  R1_EU  R1_AU  R1_pNC    dAU   dEU    dNC  degen_R1  AUROC_pNC_all  AUROC_pNC_commitcell  hedge_coll_share
                     gemma4  139   0.266   0.281  0.052  0.049   0.633 -0.091 0.001  0.015     0.712          0.694                 0.446             0.670
                   qwen3:8b  139   0.432   0.403  0.098  0.026   0.483 -0.070 0.009  0.056     0.727          0.636                 0.403             0.554
                qwen3.6-27b  139   0.417   0.432  0.055  0.162   0.386 -0.149 0.010  0.017     0.417          0.704                 0.408             0.532
              gemma4-31b-it  139   0.410   0.446  0.104  0.012   0.457 -0.005 0.036  0.007     0.734          0.721                 0.437             0.506
gemini-3.1-pro (think, 16q)   16   0.562   0.500  0.114  0.030   0.462 -0.128 0.067  0.031     0.688          0.594                 0.833             0.375
             gemini-3-flash  139   0.504   0.590  0.113  0.062   0.326 -0.022 0.022 -0.046     0.568          0.645                 0.455             0.421
```

### R1 strict accuracy by lane x model

```
model  gemini-3-flash  gemini-3.1-pro (think, 16q)  gemma4  gemma4-31b-it  qwen3.6-27b  qwen3:8b
lane                                                                                            
F               0.714                        0.429   0.265          0.551        0.612     0.449
FT              0.560                        0.500   0.180          0.400        0.300     0.340
T               0.475                        0.667   0.425          0.375        0.375     0.425
```

## 10. Regime diagnostics (per lane, final round)

```
lane  R1_EU  R1_pNC  judgment_hedge_rate   acc
   F  0.088   0.315                0.276 0.714
  FT  0.158   0.567                0.510 0.560
   T  0.087   0.038                  NaN 0.475
```