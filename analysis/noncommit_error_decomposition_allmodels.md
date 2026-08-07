# Non-commitment error decomposition — ALL full-run models

Reanalysis only. Supersedes the 2-model version (`noncommit_error_decomposition.md`, gemma4 + qwen3:8b) by adding **qwen3.6-27b** and **gemma4-31b-it**. The original file is left intact.

- models: gemma4, qwen3:8b, qwen3.6-27b, gemma4-31b-it (139 headline-eligible questions each; pooled rows n=556)
- pooled rows are **not independent** (each question appears once per model); per-model columns are the primary read, pooled is descriptive, and regressions use ticker-clustered SEs.

Gold is non-committal on **15.8%** of questions (22/139) — identical across models by construction.

## A. Error rate by commitment cell (per model)

```
model                           gemma4  gemma4-31b-it  qwen3.6-27b  qwen3:8b
cell                                                                        
committed_gold__committed_pred   0.480          0.308        0.320     0.408
committed_gold__noncommit_pred   1.000          1.000        1.000     1.000
noncommit_gold__committed_pred   1.000          1.000        1.000     1.000
noncommit_gold__noncommit_pred   0.316          0.429        0.357     0.067
```

cell sizes:
```
model                           gemma4  gemma4-31b-it  qwen3.6-27b  qwen3:8b
cell                                                                        
committed_gold__committed_pred      50             78           75        71
committed_gold__noncommit_pred      67             39           42        46
noncommit_gold__committed_pred       3              8            8         7
noncommit_gold__noncommit_pred      19             14           14        15
```

Two cells are **deterministic**: a non-committal prediction can never match a committed gold (error=1) and vice versa. Only the two same-type cells admit both outcomes.

## B. Mean p_noncommit by commitment cell (per model)

```
model                           gemma4  gemma4-31b-it  qwen3.6-27b  qwen3:8b
cell                                                                        
committed_gold__committed_pred   0.054          0.110        0.041     0.079
committed_gold__noncommit_pred   0.993          0.999        0.889     0.968
noncommit_gold__committed_pred   0.000          0.250        0.044     0.286
noncommit_gold__noncommit_pred   0.992          1.000        0.918     1.000
```

## C. Share of total errors by type

shares:
```
error_type     hedge_collision  wrong_direction_commitment  overcommitment  wrong_noncommit_type
model                                                                                           
gemma4                   0.670                       0.240           0.030                 0.060
gemma4-31b-it            0.506                       0.312           0.104                 0.078
qwen3.6-27b              0.532                       0.304           0.101                 0.063
qwen3:8b                 0.554                       0.349           0.084                 0.012
```

counts:
```
error_type     hedge_collision  wrong_direction_commitment  overcommitment  wrong_noncommit_type
model                                                                                           
gemma4                      67                          24               3                     6
gemma4-31b-it               39                          24               8                     6
qwen3.6-27b                 42                          24               8                     5
qwen3:8b                    46                          29               7                     1
```

**Pooled across the four models:** hedge_collision 57.2%, wrong_direction_commitment 29.8%, overcommitment 7.7%, wrong_noncommit_type 5.3%

**hedge_collision is the modal error type in 4/4 models** (range 0.506–0.670).

### by lane (pooled across the four models)
```
error_type  hedge_collision  wrong_direction_commitment  overcommitment  wrong_noncommit_type
lane                                                                                         
F                     0.712                       0.192           0.096                   NaN
FT                    0.763                       0.050           0.058                 0.129
T                     0.146                       0.771           0.083                   NaN
```

## D. AUROC of p_noncommit for strict error

| subset | gemma4 | qwen3:8b | qwen3.6-27b | gemma4-31b-it |
|---|---|---|---|---|
| all questions | 0.694 | 0.636 | 0.704 | 0.721 |
| committed-gold only | 0.853 | 0.769 | 0.785 | 0.785 |
| noncommitted-gold only | 0.359 | 0.062 | 0.239 | 0.214 |
| **committed-gold & committed-pred** (non-mechanical) | 0.446 | 0.403 | 0.408 | 0.437 |
| lane F | 0.677 | 0.710 | 0.823 | 0.830 |
| lane FT | 0.611 | 0.633 | 0.701 | 0.828 |
| lane T | 0.532 | 0.514 | 0.520 | 0.573 |

The pattern established on 2 models now holds on **4/4**: strong on committed-gold (mechanical — a hedge cannot match a committed gold), **at/below chance in the non-mechanical committed∧committed cell**, and inverted on non-committal-gold questions.

### Correct-noncommitment rate (hedging when the gold hedges)

```
        model  n_hedged_on_nc_gold  correct_rate
       gemma4                   19         0.684
     qwen3:8b                   15         0.933
  qwen3.6-27b                   14         0.643
gemma4-31b-it                   14         0.571
```

## E. Logistic regressions (pooled, cluster-robust by primary ticker)


### M1  y ~ p_noncommit + TU + lane
```
Intercept                                coef=  -0.874  p=0.0329
C(lane, Treatment('F'))[T.FT]            coef=  +0.075  p=0.816
C(lane, Treatment('F'))[T.T]             coef=  +1.346  p=0.0143
C(model)[T.gemma4-31b-it]                coef=  -0.371  p=0.287
C(model)[T.qwen3.6-27b]                  coef=  -0.088  p=0.782
C(model)[T.qwen3:8b]                     coef=  -0.237  p=0.358
p_noncommit                              coef=  +2.484  p=3.9e-07
tu_norm                                  coef=  -0.339  p=0.559
pseudo-R2 = 0.152; n = 556
```

### M2  + noncommit_is_gold
```
Intercept                                coef=  -0.823  p=0.0571
C(lane, Treatment('F'))[T.FT]            coef=  +0.187  p=0.529
C(lane, Treatment('F'))[T.T]             coef=  +1.354  p=0.0212
C(model)[T.gemma4-31b-it]                coef=  -0.360  p=0.324
C(model)[T.qwen3.6-27b]                  coef=  -0.056  p=0.866
C(model)[T.qwen3:8b]                     coef=  -0.219  p=0.42
p_noncommit                              coef=  +2.808  p=4.33e-08
tu_norm                                  coef=  -0.430  p=0.489
ncg                                      coef=  -1.347  p=0.0129
pseudo-R2 = 0.182; n = 556
```

### M3  p_noncommit * noncommit_is_gold
```
Intercept                                coef=  -1.253  p=0.0111
C(lane, Treatment('F'))[T.FT]            coef=  +0.468  p=0.131
C(lane, Treatment('F'))[T.T]             coef=  +1.971  p=0.00934
C(model)[T.gemma4-31b-it]                coef=  -0.614  p=0.164
C(model)[T.qwen3.6-27b]                  coef=  -0.210  p=0.6
C(model)[T.qwen3:8b]                     coef=  -0.365  p=0.281
p_noncommit                              coef=  +5.124  p=8.28e-13
ncg                                      coef=  +9.183  p=9.29e-09
p_noncommit:ncg                          coef= -14.019  p=1.69e-10
tu_norm                                  coef=  -2.044  p=0.0182
pseudo-R2 = 0.388; n = 556
```

Slope of p_noncommit: **+5.124** on committed-gold questions vs **-8.895** on non-committal-gold questions (interaction -14.019, p=1.69e-10). pseudo-R2 rises 0.152 -> 0.388.

## F. Robustness — majority-vote commitment (schema + codex + antigravity)

```
error_type     hedge_collision  wrong_direction_commitment  overcommitment  wrong_noncommit_type
model                                                                                           
gemma4                   0.610                       0.210           0.060                 0.120
gemma4-31b-it            0.468                       0.260           0.156                 0.117
qwen3.6-27b              0.494                       0.228           0.177                 0.101
qwen3:8b                 0.530                       0.301           0.133                 0.036
```

Non-mechanical-cell AUROC under majority commitment: {'gemma4': 0.468, 'qwen3:8b': 0.403, 'qwen3.6-27b': 0.396, 'gemma4-31b-it': 0.44}

hedge_collision remains modal in 4/4 models (range 0.468–0.610).

## Supplementary — gemini-3.1-pro (16-q subset, not pooled)

- error composition: {'wrong_direction_commitment': np.int64(3), 'hedge_collision': np.int64(3), 'overcommitment': np.int64(2)}
- AUROC(p_noncommit -> error), all: 0.594