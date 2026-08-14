# FinanceBench agent-set control — did the skeptic cause the collapse?

Reanalysis only. All arms: qwen3:8b, oracle `evidence_text`, K=10, 1 debate round, same 37 yes/no schemas — **only the agent pair differs**.

| arm | agents |
|---|---|
| skeptic (original) | evidence_accountant + skeptical_auditor (insufficiency-hunting) |
| neutral (control 1) | evidence_accountant + financial_analyst (both substantive) |
| homogeneous (control 2) | two identical evidence_accountants |

## 1. Headline comparison

```
                    arm  n  R0_acc  R1_acc  dCorrect  p_dCorrect  rescues  losses
     skeptic (original) 37   0.595   0.351    -0.243      0.0117        1      10
    neutral (control 1) 37   0.595   0.649     0.054         NaN        3       1
homogeneous (control 2)  2   0.000   0.000     0.000         NaN        0       0
```

## 2. Non-commitment dynamics

```
                    arm  R0_pNC  R1_pNC    dNC  p_dNC
     skeptic (original)   0.454   0.582  0.128 0.0200
    neutral (control 1)   0.281   0.258 -0.023 0.4893
homogeneous (control 2)   0.500   0.500  0.000    NaN
```

## 3. Error composition and the committed cell

```
                    arm  errors  hedge_coll  hedge_share  wrong_dir  commit_cell_n  commit_cell_AUROC  cc_CI_lo  cc_CI_hi
     skeptic (original)      24          19        0.792          5             18              0.815     0.631     0.958
    neutral (control 1)      13           7        0.538          6             30              0.576     0.360     0.822
homogeneous (control 2)       2           1        0.500          1              1                NaN       NaN       NaN
```

## 4. Per-agent drift — who moves whom


**skeptic (original)**
```
                             acc    pNC  hedge_rate
agent               round                          
evidence_accountant 0      0.622  0.232       0.216
                    1      0.324  0.535       0.541
skeptical_auditor   0      0.243  0.676       0.676
                    1      0.324  0.630       0.649
```

**neutral (control 1)**
```
                             acc    pNC  hedge_rate
agent               round                          
evidence_accountant 0      0.595  0.222       0.216
                    1      0.676  0.222       0.216
financial_analyst   0      0.568  0.341       0.324
                    1      0.568  0.295       0.297
```

**homogeneous (control 2)**
```
                             acc  pNC  hedge_rate
agent                 round                      
evidence_accountant_a 0      0.0  0.5         0.5
                      1      0.0  0.5         0.5
evidence_accountant_b 0      0.0  0.5         0.5
                      1      0.0  0.5         0.5
```

## 5. Verdict

- neutral (control 1): dCorrect +0.054 vs skeptic -0.243; rescues/losses 3/1 vs 1/10 -> **skeptic-driven**
- homogeneous (control 2): dCorrect +0.000 vs skeptic -0.243; rescues/losses 0/0 vs 1/10 -> **skeptic-driven**

Interpretation rule fixed in advance: if the neutral arm's accuracy drop largely disappears, the original collapse was an artifact of the insufficiency-biased skeptic and must not be reported as a general debate effect. If it persists, debate itself degrades accuracy on this benchmark.