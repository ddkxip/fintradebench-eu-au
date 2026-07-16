# Hedge probe + qwen replication summary

## Probe: 8 judgment questions, Round 0, K=10, gemma4

```
                     eu     au     tu  hedge_rate  degenerate  parse
arm                                                                 
baseline_menu     0.028  0.134  0.163       0.875       0.375    1.0
directional_menu  0.052  0.150  0.202       0.000       0.500    1.0
hedge_justified   0.069  0.168  0.237       0.375       0.375    1.0
```

### Directional-gold questions (F11, FT2, FT10, FT12) — accuracy by arm

```
                   acc  gold_prob
arm                              
baseline_menu      0.0      0.000
directional_menu  0.25      0.150
hedge_justified   0.25      0.238
```

### Hedge-gold questions (F1, FT1, FT25, FT31) — forced-choice uncertainty (Arm D)

```
question_id  eu_norm  au_norm  tu_norm         predicted
         F1    0.068    0.228    0.296 insufficient_data
        FT1   -0.000    0.000   -0.000 insufficient_data
       FT25    0.196    0.315    0.512      unsupportive
       FT31   -0.000    0.000   -0.000 insufficient_data
```
(High AU/EU here = hedging was information-bearing; confident directional picks = hedging was surface style.)

### Per-question arm detail
```
question_id              arm  eu_norm  au_norm         predicted   gold_label correct
         F1 directional_menu    0.068    0.228 insufficient_data        mixed     NaN
         F1  hedge_justified    0.085    0.220 insufficient_data        mixed   False
        F11 directional_menu   -0.000    0.000 insufficient_data          yes   False
        F11  hedge_justified    0.247    0.220             mixed          yes   False
        FT1 directional_menu   -0.000    0.000 insufficient_data  conditional     NaN
        FT1  hedge_justified   -0.000    0.000       conditional  conditional    True
        FT2 directional_menu    0.033    0.148 insufficient_data unsupportive   False
        FT2  hedge_justified   -0.000    0.000       conditional unsupportive   False
       FT10 directional_menu   -0.000    0.000 insufficient_data   supportive   False
       FT10  hedge_justified    0.110    0.567 insufficient_data   supportive   False
       FT12 directional_menu    0.121    0.506               yes          yes    True
       FT12  hedge_justified    0.026    0.117               yes          yes    True
       FT25 directional_menu    0.196    0.315      unsupportive  conditional     NaN
       FT25  hedge_justified    0.085    0.220      unsupportive  conditional   False
       FT31 directional_menu   -0.000    0.000 insufficient_data  conditional     NaN
       FT31  hedge_justified   -0.000    0.000 insufficient_data  conditional   False
```

## qwen3:8b replication (16 questions, R0+R1) vs gemma4

```
                   eu     au     tu  gold_prob    acc  hedge_rate  degenerate  parse
model    round                                                                      
gemma4   0      0.032  0.147  0.179      0.600  0.625       0.438       0.438  0.992
         1      0.034  0.060  0.093      0.612  0.625       0.438       0.750  0.994
qwen3:8b 0      0.028  0.083  0.111      0.591  0.625       0.375       0.688  1.000
         1      0.031  0.042  0.074      0.662  0.688       0.375       0.812  1.000
```

### Lane accuracy by model (final round)

```
model  gemma4  qwen3:8b
lane                   
F        0.86      0.86
FT       0.33      0.50
T        0.67      0.67
```

### AU drop R0->R1 by model (paired mean)

- gemma4: mean dAU = -0.087, mean dEU = +0.002 (n=16)
- qwen3:8b: mean dAU = -0.041, mean dEU = +0.004 (n=16)

### qwen per-question detail (final round)
```
question_id lane  eu_norm  au_norm  gold_prob         predicted  correct  parse_rate
         F1    F   -0.000    0.000       1.00             mixed     True         1.0
        F11    F   -0.000    0.000       0.00             mixed    False         1.0
        F12    F   -0.000    0.000       1.00             GOOGL     True         1.0
         F2    F   -0.000    0.000       1.00             GOOGL     True         1.0
        F25    F    0.107    0.278       0.85 insufficient_data     True         1.0
        F31    F   -0.000    0.000       1.00              COST     True         1.0
        F44    F   -0.000    0.000       1.00        claim_true     True         1.0
        FT1   FT    0.005    0.401       0.25        supportive    False         1.0
       FT10   FT   -0.000    0.000       0.00       conditional    False         1.0
       FT12   FT   -0.000    0.000       1.00               yes     True         1.0
        FT2   FT   -0.000    0.000       0.00       conditional    False         1.0
       FT25   FT   -0.000    0.000       1.00       conditional     True         1.0
       FT31   FT   -0.000    0.000       1.00       conditional     True         1.0
         T1    T   -0.000    0.000       1.00               APP     True         1.0
        T10    T    0.387    0.000       0.50              AAPL     True         1.0
         T2    T   -0.000    0.000       0.00                MU    False         1.0
```