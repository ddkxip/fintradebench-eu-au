# FinanceBench agent-set control — did the skeptic cause the collapse?

Reanalysis only. All arms: qwen3:8b, oracle `evidence_text`, K=10, 1 debate round, same 37 yes/no schemas — **only the agent pair differs**.

| arm | agents |
|---|---|
| skeptic (original) | evidence_accountant + skeptical_auditor (insufficiency-hunting) |
| neutral (control 1) | evidence_accountant + financial_analyst (both substantive) |
| homogeneous (control 2) | two identical evidence_accountants |

> **Pending arms (not yet run): neutral (control 1), homogeneous (control 2).** Rerun this script once their rows.csv exist.

## 1. Headline comparison

```
               arm  n  R0_acc  R1_acc  dCorrect  p_dCorrect  rescues  losses
skeptic (original) 37   0.595   0.351    -0.243      0.0117        1      10
```

## 2. Non-commitment dynamics

```
               arm  R0_pNC  R1_pNC   dNC  p_dNC
skeptic (original)   0.454   0.582 0.128   0.02
```

## 3. Error composition and the committed cell

```
               arm  errors  hedge_coll  hedge_share  wrong_dir  commit_cell_n  commit_cell_AUROC  cc_CI_lo  cc_CI_hi
skeptic (original)      24          19        0.792          5             18              0.815     0.631     0.958
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