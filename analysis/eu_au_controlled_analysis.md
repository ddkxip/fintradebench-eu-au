# E-B' controlled analysis (139 q x 2 models; unit = question x model)

- n rows: 278; clusters (primary ticker): 30

## Q1 — lane effects on round-0 AU/EU (OLS, cluster-robust by ticker)

Spec A controls model + log|Y| (+K collinear with lane by design; see Q2 for the matched-K answer). Spec B adds answer_type — the mechanism carrier that is partially confounded with lane (screenings are mostly T); both reported.

### Q1A au0 ~ lane + model + log|Y|
```
Intercept                                  coef=+0.0460  p=0.838
C(lane, Treatment('F'))[T.FT]              coef=-0.0572  p=0.183
C(lane, Treatment('F'))[T.T]               coef=+0.0839  p=0.235
C(model)[T.qwen3]                          coef=-0.0764  p=0.0922
np.log(space_n)                            coef=+0.1229  p=0.48
```

### Q1B au0 + answer_type control
```
Intercept                                  coef=-0.3216  p=0.389
C(lane, Treatment('F'))[T.FT]              coef=-0.0771  p=0.0789
C(lane, Treatment('F'))[T.T]               coef=+0.3093  p=3.96e-15
C(model)[T.qwen3]                          coef=-0.0764  p=0.0971
np.log(space_n)                            coef=+0.3924  p=0.167
```

### Q1A eu0 ~ lane + model + log|Y|
```
Intercept                                  coef=-0.0449  p=0.78
C(lane, Treatment('F'))[T.FT]              coef=-0.0402  p=0.194
C(lane, Treatment('F'))[T.T]               coef=-0.0614  p=0.299
C(model)[T.qwen3]                          coef=+0.0578  p=0.0257
np.log(space_n)                            coef=+0.1022  p=0.435
```

### Q1B eu0 + answer_type control
```
Intercept                                  coef=+0.1526  p=0.445
C(lane, Treatment('F'))[T.FT]              coef=-0.0845  p=0.0461
C(lane, Treatment('F'))[T.T]               coef=+0.0927  p=0.000514
C(model)[T.qwen3]                          coef=+0.0578  p=0.028
np.log(space_n)                            coef=-0.0104  p=0.947
```

## Q2 — matched-K robustness (T-lane AU recomputed from K=10 subsamples of its 20 decodes; 50 resamples/question)

- gemma4: T-lane AU_mm at matched K=10 = 0.409 vs F/FT 0.146; diff +0.263 [+0.148, +0.384] -> SUPPORTED at matched K
- qwen3: T-lane AU_mm at matched K=10 = 0.161 vs F/FT 0.142; diff +0.019 [-0.062, +0.104] -> not supported at matched K

## Q3 — final-round error ~ uncertainty (logit, cluster-robust)


### Q3 gemma4: err ~ p_noncommit + TU + lane
```
Intercept                                  coef=-0.1144  p=0.823
C(lane, Treatment('F'))[T.FT]              coef=-0.1165  p=0.758
C(lane, Treatment('F'))[T.T]               coef=+0.2144  p=0.776
nc_fin                                     coef=+1.8243  p=0.000892
tu_fin                                     coef=+0.0020  p=0.999
```

### Q3 qwen3: err ~ p_noncommit + TU + lane
```
Intercept                                  coef=-0.4784  p=0.282
C(lane, Treatment('F'))[T.FT]              coef=+0.4868  p=0.318
C(lane, Treatment('F'))[T.T]               coef=+0.9725  p=0.163
nc_fin                                     coef=+1.5837  p=0.00165
tu_fin                                     coef=-2.2933  p=0.0368
```

## Q4 — does initial EU predict improvement; does dEU predict dG?


### Q4a dG ~ EU0 + AU0 + NC0 + lane + model
```
Intercept                                  coef=+0.0209  p=0.491
C(lane, Treatment('F'))[T.FT]              coef=+0.0160  p=0.407
C(lane, Treatment('F'))[T.T]               coef=-0.0160  p=0.703
C(model)[T.qwen3]                          coef=-0.0226  p=0.097
eu0                                        coef=-0.0960  p=0.342
au0                                        coef=-0.0061  p=0.899
nc0                                        coef=-0.0152  p=0.653
```

### Q4b dG ~ dEU + dAU + lane + model
```
Intercept                                  coef=-0.0023  p=0.881
C(lane, Treatment('F'))[T.FT]              coef=+0.0184  p=0.347
C(lane, Treatment('F'))[T.T]               coef=-0.0052  p=0.83
C(model)[T.qwen3]                          coef=-0.0240  p=0.168
d_eu                                       coef=-0.0250  p=0.843
d_au                                       coef=-0.0137  p=0.79
```

### Q5 dNC ~ model + lane + NC0
```
Intercept                                  coef=+0.0675  p=0.0093
C(model)[T.qwen3]                          coef=+0.0315  p=0.0362
C(lane, Treatment('F'))[T.FT]              coef=-0.0073  p=0.7
C(lane, Treatment('F'))[T.T]               coef=-0.0611  p=0.0467
nc0                                        coef=-0.0522  p=0.0615
```

## BH-FDR across all reported coefficients

- coefficients tested: 39; surviving FDR(0.05): 4
  - Q1B au0 + answer_type control :: C(lane, Treatment('F'))[T.T]  (p=4e-15, q=1.5e-13)
  - Q1B eu0 + answer_type control :: C(lane, Treatment('F'))[T.T]  (p=0.00051, q=0.01)
  - Q3 gemma4: err ~ p_noncommit + TU + lane :: nc_fin  (p=0.00089, q=0.012)
  - Q3 qwen3: err ~ p_noncommit + TU + lane :: nc_fin  (p=0.0016, q=0.016)