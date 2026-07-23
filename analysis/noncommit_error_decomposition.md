# Committed vs non-committed error decomposition

Reanalysis of stored final-round rows; no new model calls.
Primary set: gemma4 + qwen3, 139 headline-eligible questions each (n=278 scored rows). Supplementary gemini section at the end.

`noncommit_set` per question = {mixed, conditional, insufficient_data, none_clear} ∩ answer_space (schema-overridable).

## 0. How often is the GOLD itself non-committal?

```
              mean  sum  count
model  lane                   
gemma4 F     0.143    7     49
       FT    0.260   13     50
       T     0.050    2     40
qwen3  F     0.143    7     49
       FT    0.260   13     50
       T     0.050    2     40
```

Overall share of questions with a non-committal gold: 0.158 (22 of 139).

## A. Error rate by commitment cell

```
                                        n  strict_error  lenient_error
model  prediction_commitment_cell                                     
gemma4 committed_gold__committed_pred  50         0.480          0.200
       committed_gold__noncommit_pred  67         1.000          1.000
       noncommit_gold__committed_pred   3         1.000          1.000
       noncommit_gold__noncommit_pred  19         0.316          0.316
qwen3  committed_gold__committed_pred  71         0.408          0.141
       committed_gold__noncommit_pred  46         1.000          1.000
       noncommit_gold__committed_pred   7         1.000          0.571
       noncommit_gold__noncommit_pred  15         0.067          0.067
```

Note: two cells are **deterministic** — a non-committal prediction can never match a committed gold (error=1 by construction), and a committed prediction can never match a non-committal gold (error=1). Only the two same-type cells admit both outcomes.

### By lane
```
                                      mean  size
lane prediction_commitment_cell                 
F    committed_gold__committed_pred  0.395    38
     committed_gold__noncommit_pred  1.000    46
     noncommit_gold__committed_pred  1.000     2
     noncommit_gold__noncommit_pred  0.000    12
FT   committed_gold__committed_pred  0.267    15
     committed_gold__noncommit_pred  1.000    59
     noncommit_gold__committed_pred  1.000     4
     noncommit_gold__noncommit_pred  0.318    22
T    committed_gold__committed_pred  0.500    68
     committed_gold__noncommit_pred  1.000     8
     noncommit_gold__committed_pred  1.000     4
```

### By answer_type
```
                                                                   mean  size
answer_type                       prediction_commitment_cell                 
category_choice                   committed_gold__committed_pred  0.308    13
                                  committed_gold__noncommit_pred  1.000    21
                                  noncommit_gold__committed_pred  1.000     1
                                  noncommit_gold__noncommit_pred  1.000     1
company_choice                    committed_gold__committed_pred  0.286    14
                                  noncommit_gold__committed_pred  1.000     1
                                  noncommit_gold__noncommit_pred  0.000     3
graded_judgment                   committed_gold__committed_pred  0.667     3
                                  committed_gold__noncommit_pred  1.000     5
                                  noncommit_gold__noncommit_pred  0.000     2
open_summary_with_canonical_claim committed_gold__committed_pred  0.625     8
                                  committed_gold__noncommit_pred  1.000     8
                                  noncommit_gold__committed_pred  1.000     1
                                  noncommit_gold__noncommit_pred  0.000     1
premise_check                     committed_gold__noncommit_pred  1.000     2
screening_top1                    committed_gold__committed_pred  0.514    72
                                  committed_gold__noncommit_pred  1.000     8
                                  noncommit_gold__committed_pred  1.000     4
supportive_judgment               committed_gold__committed_pred  0.000     1
                                  committed_gold__noncommit_pred  1.000    13
                                  noncommit_gold__committed_pred  1.000     1
                                  noncommit_gold__noncommit_pred  0.286     7
valuation_judgment                committed_gold__noncommit_pred  1.000     6
yes_no_mixed                      committed_gold__committed_pred  0.100    10
                                  committed_gold__noncommit_pred  1.000    50
                                  noncommit_gold__committed_pred  1.000     2
                                  noncommit_gold__noncommit_pred  0.200    20
```

## B. Mean p_noncommit by commitment cell

```
                                        mean  median  size
model  prediction_commitment_cell                         
gemma4 committed_gold__committed_pred  0.054     0.0    50
       committed_gold__noncommit_pred  0.993     1.0    67
       noncommit_gold__committed_pred  0.000     0.0     3
       noncommit_gold__noncommit_pred  0.992     1.0    19
qwen3  committed_gold__committed_pred  0.079     0.0    71
       committed_gold__noncommit_pred  0.968     1.0    46
       noncommit_gold__committed_pred  0.286     0.5     7
       noncommit_gold__noncommit_pred  1.000     1.0    15
```

### By lane
```
                                      mean  size
lane prediction_commitment_cell                 
F    committed_gold__committed_pred  0.116    38
     committed_gold__noncommit_pred  0.997    46
     noncommit_gold__committed_pred  0.000     2
     noncommit_gold__noncommit_pred  0.987    12
FT   committed_gold__committed_pred  0.157    15
     committed_gold__noncommit_pred  0.988    59
     noncommit_gold__committed_pred  0.500     4
     noncommit_gold__noncommit_pred  1.000    22
T    committed_gold__committed_pred  0.022    68
     committed_gold__noncommit_pred  0.862     8
     noncommit_gold__committed_pred  0.000     4
```

## C. Share of total errors by type

```
                                    n  share_of_errors
model  error_type                                     
gemma4 hedge_collision             67            0.670
       overcommitment               3            0.030
       wrong_direction_commitment  24            0.240
       wrong_noncommit_type         6            0.060
qwen3  hedge_collision             46            0.554
       overcommitment               7            0.084
       wrong_direction_commitment  29            0.349
       wrong_noncommit_type         1            0.012
```

### Pooled (both models)
```
                              n  share
error_type                            
hedge_collision             113  0.617
wrong_direction_commitment   53  0.290
overcommitment               10  0.055
wrong_noncommit_type          7  0.038
```

### By lane (share of that lane's errors)
```
lane  error_type                
F     hedge_collision               0.730
      overcommitment                0.032
      wrong_direction_commitment    0.238
FT    hedge_collision               0.797
      overcommitment                0.054
      wrong_direction_commitment    0.054
      wrong_noncommit_type          0.095
T     hedge_collision               0.174
      overcommitment                0.087
      wrong_direction_commitment    0.739
```

## D. AUROC of p_noncommit for strict_error

| subset | model | AUROC | n | error rate |
|---|---|---|---|---|
| all questions | gemma4 | 0.694 | 139 | 0.72 |
| all questions | qwen3 | 0.636 | 139 | 0.60 |
| committed-gold only | gemma4 | 0.853 | 117 | 0.78 |
| committed-gold only | qwen3 | 0.769 | 117 | 0.64 |
| noncommitted-gold only | gemma4 | 0.359 | 22 | 0.41 |
| noncommitted-gold only | qwen3 | 0.062 | 22 | 0.36 |
| lane F | gemma4 | 0.677 | 49 | 0.73 |
| lane F | qwen3 | 0.710 | 49 | 0.55 |
| lane FT | gemma4 | 0.611 | 50 | 0.82 |
| lane FT | qwen3 | 0.633 | 50 | 0.66 |
| lane T | gemma4 | 0.532 | 40 | 0.57 |
| lane T | qwen3 | 0.514 | 40 | 0.57 |

**Non-mechanical subset** (committed gold AND committed prediction — the cell where p_noncommit is not definitionally tied to the outcome):

| subset | model | AUROC | n | error rate |
|---|---|---|---|---|
| committed gold & committed pred | gemma4 | 0.446 | 50 | 0.48 |
| committed gold & committed pred | qwen3 | 0.403 | 71 | 0.41 |
| noncommit gold & noncommit pred | gemma4 | 0.538 | 19 | 0.32 |
| noncommit gold & noncommit pred | qwen3 | 0.500 | 15 | 0.07 |

## E. Logistic regressions (cluster-robust SEs by primary ticker)


### M1  y ~ p_noncommit + TU + lane
```
Intercept                                coef=  -0.088  p=0.853
C(lane, Treatment('F'))[T.FT]            coef=  +0.144  p=0.629
C(lane, Treatment('F'))[T.T]             coef=  +0.629  p=0.317
C(model)[T.qwen3]                        coef=  -0.323  p=0.171
p_noncommit                              coef=  +1.662  p=0.000468
tu_norm                                  coef=  -1.384  p=0.0576
pseudo-R2 = 0.103; n = 278
```

### M2  + noncommit_is_gold
```
Intercept                                coef=  -0.033  p=0.949
C(lane, Treatment('F'))[T.FT]            coef=  +0.430  p=0.146
C(lane, Treatment('F'))[T.T]             coef=  +0.665  p=0.353
C(model)[T.qwen3]                        coef=  -0.330  p=0.227
p_noncommit                              coef=  +2.366  p=7.28e-06
tu_norm                                  coef=  -1.531  p=0.044
ncg                                      coef=  -2.471  p=0.000407
pseudo-R2 = 0.204; n = 278
```

### M3  p_noncommit * noncommit_is_gold
```
Intercept                                coef=  -0.192  p=0.72
C(lane, Treatment('F'))[T.FT]            coef=  +0.609  p=0.0591
C(lane, Treatment('F'))[T.T]             coef=  +0.904  p=0.267
C(model)[T.qwen3]                        coef=  -0.578  p=0.0981
p_noncommit                              coef=  +4.333  p=3.04e-08
ncg                                      coef= +11.934  p=7.97e-08
p_noncommit:ncg                          coef= -17.499  p=4.06e-11
tu_norm                                  coef=  -3.116  p=0.00251
pseudo-R2 = 0.397; n = 278
```

Slope of p_noncommit on committed-gold questions: **+4.333**; on non-committal-gold questions: **-13.166** (sum of main + interaction).

## Supplementary — gemini-3.1-pro (16-question subset, NOT pooled with primary)

```
                                n  strict_error  p_noncommit
prediction_commitment_cell                                  
committed_gold__committed_pred  8         0.375        0.125
committed_gold__noncommit_pred  3         1.000        0.967
noncommit_gold__committed_pred  2         1.000        0.250
noncommit_gold__noncommit_pred  3         0.000        1.000
```

Error composition: {'wrong_direction_commitment': np.int64(3), 'hedge_collision': np.int64(3), 'overcommitment': np.int64(2)}
AUROC(p_noncommit -> error), all 16: 0.594