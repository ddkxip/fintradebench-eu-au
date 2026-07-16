# Three-model comparison (shared 16 questions, R0+R1)

```
                         eu     au     tu  gold_prob    acc  noncommit_pred  degenerate  parse  p_noncommit
model          round                                                                                       
gemini-3.1-pro 0      0.047  0.159  0.206      0.516  0.562           0.438       0.375  1.000        0.431
               1      0.114  0.030  0.144      0.550  0.500           0.375       0.688  1.000        0.462
gemma4         0      0.032  0.147  0.179      0.600  0.625           0.562       0.438  0.992          NaN
               1      0.034  0.060  0.093      0.612  0.625           0.562       0.750  0.994          NaN
qwen3:8b       0      0.028  0.083  0.111      0.591  0.625           0.375       0.688  1.000          NaN
               1      0.031  0.042  0.074      0.662  0.688           0.438       0.812  1.000          NaN
```

## Lane accuracy (final round)

```
model  gemini-3.1-pro  gemma4  qwen3:8b
lane                                   
F                0.43    0.86      0.86
FT               0.50    0.33      0.50
T                0.67    0.67      0.67
```

## Judgment questions only (the attractor's home turf)

```
                        acc  noncommit_pred     eu     au
model          round                                     
gemini-3.1-pro 0      0.625           0.625  0.049  0.133
               1      0.500           0.500  0.062  0.000
gemma4         0      0.375           1.000  0.028  0.134
               1      0.375           1.000  0.025  0.030
qwen3:8b       0      0.500           0.750  0.004  0.052
               1      0.500           0.750  0.001  0.050
```

## Per-question final-round predictions (gold in brackets)
```
model           gemini-3.1-pro             gemma4           qwen3:8b               gold
question_id                                                                            
F1                         yes              mixed              mixed              mixed
F11                        yes              mixed              mixed                yes
F12                      GOOGL              GOOGL              GOOGL              GOOGL
F2                        MSFT              GOOGL              GOOGL              GOOGL
F25          insufficient_data  insufficient_data  insufficient_data  insufficient_data
F31          insufficient_data               COST               COST               COST
F44                claim_false         claim_true         claim_true         claim_true
FT1                conditional        conditional         supportive        conditional
FT10               conditional        conditional        conditional         supportive
FT12                       yes              mixed                yes                yes
FT2                conditional        conditional        conditional       unsupportive
FT25              unsupportive        conditional        conditional        conditional
FT31               conditional  insufficient_data        conditional        conditional
T1                         APP                APP                APP                APP
T10                       NVDA               AAPL               AAPL               AAPL
T2                        INTC               LRCX                 MU               INTC
```

## Paired deltas R0->R1 per model

- gemini-3.1-pro: dAU=-0.128, dEU=+0.067, dG=+0.034 (n=16)
- gemma4: dAU=-0.087, dEU=+0.002, dG=+0.012 (n=16)
- qwen3:8b: dAU=-0.041, dEU=+0.004, dG=+0.072 (n=16)