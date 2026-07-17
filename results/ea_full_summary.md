# E-A' full-run summary (139 questions, gemma4 + qwen3:8b, R0+R1)

- rows: 556; parse mean 0.998

## Core table: model x lane x round

```
                        eu     au     tu  au_mm  eu_mm  p_noncommit  gold_prob    acc  acc_lenient  degenerate
model    lane round                                                                                           
gemma4   F    0      0.088  0.132  0.220  0.189  0.114        0.671      0.242  0.245        0.265       0.490
              1      0.062  0.035  0.097  0.050  0.076        0.696      0.257  0.265        0.265       0.796
         FT   0      0.029  0.068  0.097  0.103  0.040        0.972      0.165  0.160        0.160       0.740
              1      0.031  0.010  0.041  0.015  0.045        0.970      0.172  0.180        0.180       0.900
         T    0      0.034  0.239  0.273  0.425  0.052        0.112      0.413  0.425        0.750       0.250
              1      0.067  0.114  0.181  0.205  0.114        0.136      0.401  0.425        0.775       0.375
qwen3:8b F    0      0.090  0.105  0.195  0.149  0.121        0.491      0.442  0.469        0.551       0.510
              1      0.059  0.022  0.081  0.032  0.081        0.571      0.403  0.449        0.510       0.816
         FT   0      0.095  0.089  0.183  0.135  0.128        0.654      0.305  0.360        0.400       0.540
              1      0.133  0.032  0.164  0.049  0.185        0.723      0.307  0.340        0.380       0.680
         T    0      0.081  0.095  0.176  0.169  0.134        0.064      0.361  0.475        0.850       0.525
              1      0.103  0.024  0.128  0.042  0.177        0.075      0.336  0.425        0.850       0.675
```

## Paired R0->R1 (per model, n=139)

- gemma4 dAU: mean -0.0910, Wilcoxon p=8.89e-09 (nonzero n=68)
- gemma4 dEU: mean +0.0008, Wilcoxon p=7.96e-01 (nonzero n=65)
- gemma4 dG: mean +0.0046, Wilcoxon p=9.45e-01 (nonzero n=47)
- gemma4 dNC: mean +0.0150, Wilcoxon p=9.75e-02 (nonzero n=22)
- qwen3:8b dAU: mean -0.0701, Wilcoxon p=3.32e-07 (nonzero n=64)
- qwen3:8b dEU: mean +0.0092, Wilcoxon p=8.55e-01 (nonzero n=65)
- qwen3:8b dG: mean -0.0201, Wilcoxon p=1.03e-01 (nonzero n=48)
- qwen3:8b dNC: mean +0.0565, Wilcoxon p=7.74e-05 (nonzero n=39)

## Transition taxonomy (R0->R1)

### gemma4
- outcome: {'STABLE_FAILURE': 97, 'STABLE_SUCCESS': 34, 'DEBATE_RESCUE': 5, 'CORRECTNESS_LOST': 3}
- flow: {'NO_MATERIAL_CHANGE': 71, 'MIXED_FLOW': 45, 'NOISE_REDUCTION': 12, 'FALSE_CONSENSUS': 6, 'PRODUCTIVE_CONVERGENCE': 3, 'ALEATORIC_DESTABILIZATION': 2}
- false consensus: 6 (4.3%); minority suppression: 0; PRD (floored): 10
- rescue: 5, lost: 3
### qwen3:8b
- outcome: {'STABLE_FAILURE': 75, 'STABLE_SUCCESS': 52, 'CORRECTNESS_LOST': 8, 'DEBATE_RESCUE': 4}
- flow: {'NO_MATERIAL_CHANGE': 74, 'MIXED_FLOW': 39, 'FALSE_CONSENSUS': 11, 'PRODUCTIVE_CONVERGENCE': 9, 'NOISE_REDUCTION': 3, 'ALEATORIC_DESTABILIZATION': 3}
- false consensus: 11 (7.9%); minority suppression: 2; PRD (floored): 26
- rescue: 4, lost: 8

## RQ3 confirmatory tests (round 0, MM-corrected, cluster bootstrap by primary ticker, 4000 resamples)

- gemma4 **T-higher-AU** (AU_mm, T minus F/FT): +0.2793 [95% CI +0.1277, +0.4228] SUPPORTED
- gemma4 **FT-higher-EU** (EU_mm, FT minus F/T): -0.0467 [95% CI -0.1015, +0.0154] not supported
- qwen3:8b **T-higher-AU** (AU_mm, T minus F/FT): +0.0270 [95% CI -0.0557, +0.1154] not supported
- qwen3:8b **FT-higher-EU** (EU_mm, FT minus F/T): +0.0006 [95% CI -0.0889, +0.0747] not supported

## RQ6: error-prediction AUROC (final round, per model)

### gemma4 (error rate 0.72)
- AUROC(tu_norm -> error) = 0.451
- AUROC(au_norm -> error) = 0.459
- AUROC(eu_norm -> error) = 0.446
- AUROC(p_noncommit -> error) = 0.694
### qwen3:8b (error rate 0.60)
- AUROC(tu_norm -> error) = 0.399
- AUROC(au_norm -> error) = 0.524
- AUROC(eu_norm -> error) = 0.384
- AUROC(p_noncommit -> error) = 0.636

## Strict vs lenient accuracy (final round)

```
               correct  correct_lenient
model    lane                          
gemma4   F       0.265            0.265
         FT      0.180            0.180
         T       0.425            0.775
qwen3:8b F       0.449            0.510
         FT      0.340            0.380
         T       0.425            0.850
```