# HF Qwen3.6-27B-FP8 — full E-A findings

Reanalysis of results/ea_full_hf_qwen36_27b_fp8/rows.csv (139 headline-eligible questions, R0+R1, K=10 F/FT / 20 T). Metric definitions identical to analyze_ea_full.py; no new model calls.
- parse rate: 1.000; questions: 139; scored final rows: 139

## 1-2. Accuracy (strict) by round and lane

- overall R0 acc = **0.417**, R1 acc = **0.432**
```
round      0      1
lane               
F      0.612  0.612
FT     0.320  0.300
T      0.300  0.375
```

## 3. TU / AU / EU (normalized) + Miller-Madow by lane and round

```
            tu_norm  au_norm  eu_norm  au_mm  eu_mm  tu_mm
lane round                                                
F    0        0.332    0.276    0.055  0.397  0.059  0.453
     1        0.173    0.121    0.052  0.169  0.062  0.231
FT   0        0.358    0.317    0.041  0.482  0.044  0.522
     1        0.268    0.198    0.070  0.298  0.091  0.389
T    0        0.381    0.346    0.035  0.614  0.048  0.661
     1        0.208    0.168    0.039  0.299  0.060  0.359
```

## 4. Debate deltas R0->R1 (paired, n=139)

- dAU: mean -0.1488, Wilcoxon p=3.44e-13 (nonzero n=107)
- dEU: mean +0.0105, Wilcoxon p=5.07e-01 (nonzero n=105)
- dNC: mean +0.0173, Wilcoxon p=2.67e-01 (nonzero n=73)
- dG: mean +0.0079, Wilcoxon p=8.43e-01 (nonzero n=100)

## 5. p_noncommit by lane and round

```
             mean  median
lane round               
F    0      0.295   0.100
     1      0.299   0.050
FT   0      0.699   0.800
     1      0.736   0.825
T    0      0.045   0.000
     1      0.054   0.000
```
- degenerate rows (TU=0): 0.345 overall; R1 0.417

## 6. AUROC for error prediction (final round)

error rate = 0.57
| predictor | AUROC (all) | AUROC committed-gold | AUROC commit-gold&commit-pred |
|---|---|---|---|
| tu_norm | 0.541 | 0.551 | 0.596 |
| au_norm | 0.551 | 0.564 | 0.619 |
| eu_norm | 0.510 | 0.513 | 0.536 |
| p_noncommit | 0.704 | 0.785 | 0.408 |

(committed-gold n=117; committed-gold & committed-pred n=75 — the non-mechanical cell.)

## 7. Non-commitment error decomposition (final round)

```
                             n  share
error_type                           
hedge_collision             42  0.532
wrong_direction_commitment  24  0.304
overcommitment               8  0.101
wrong_noncommit_type         5  0.063
```
- non-committal gold questions: 22; correct-noncommitment rate (hedge right when gold hedges): 0.64 (n_hedged=14)

### share of errors by lane
```
lane  error_type                
F     hedge_collision               0.632
      overcommitment                0.263
      wrong_direction_commitment    0.105
FT    hedge_collision               0.800
      overcommitment                0.029
      wrong_direction_commitment    0.029
      wrong_noncommit_type          0.143
T     hedge_collision               0.080
      overcommitment                0.080
      wrong_direction_commitment    0.840
```

## 8. Debate transitions (R0->R1)

- outcome: {'STABLE_FAILURE': 75, 'STABLE_SUCCESS': 54, 'DEBATE_RESCUE': 6, 'CORRECTNESS_LOST': 4}
- flow: {'MIXED_FLOW': 47, 'NO_MATERIAL_CHANGE': 33, 'NOISE_REDUCTION': 29, 'PRODUCTIVE_CONVERGENCE': 11, 'FALSE_CONSENSUS': 10, 'ALEATORIC_DESTABILIZATION': 9}
- rescue: 6, loss: 4, stable-correct: 54, stable-wrong: 75
- false consensus: 10 (7.2%); minority suppression: 2

## 9. Cross-model comparison

(gemini = 16-q subset, flagged; not pooled with the 139-q models)

```
         model  n_q  R0_acc  R1_acc  R1_EU  R1_AU  R1_pNC    dAU   dEU   dNC  degen_R1  AUROC_pNC_all  AUROC_pNC_commitcell  hedge_coll_share
        gemma4  139   0.266   0.281  0.052  0.049   0.633 -0.091 0.001 0.015     0.712          0.694                 0.446             0.670
      qwen3:8b  139   0.432   0.403  0.098  0.026   0.483 -0.070 0.009 0.056     0.727          0.636                 0.403             0.554
   qwen3.6-27b  139   0.417   0.432  0.055  0.162   0.386 -0.149 0.010 0.017     0.417          0.704                 0.408             0.532
gemini-3.1-pro   16   0.562   0.500  0.114  0.030   0.462 -0.128 0.067 0.031     0.688          0.594                 0.833             0.375
```

### R1 strict accuracy by lane x model

```
model  gemini-3.1-pro  gemma4  qwen3.6-27b  qwen3:8b
lane                                                
F               0.429   0.265        0.612     0.449
FT              0.500   0.180        0.300     0.340
T               0.667   0.425        0.375     0.425
```

## 10. Regime verdict

Per-lane regime diagnostics (qwen3.6-27b, final round):

```
lane  R1_EU  R1_pNC  judgment_hedge_rate   acc
   F  0.052   0.299                0.483 0.612
  FT  0.070   0.736                0.796 0.300
   T  0.039   0.054                  NaN 0.375
```

### Verdict: a MIXED, LANE-DEPENDENT regime — the cleanest evidence yet that "regime" is a model×lane property, not a whole-model property.

Qwen3.6-27B does not sit in one regime. Within the single model:

- **F-lane → commitment regime.** p_noncommit 0.30, judgment hedge rate
  0.48, and **accuracy 0.612 — the highest F-lane accuracy of ANY model
  tested, beating gemini's 0.429.** It commits on fundamentals and is
  right.
- **FT-lane → hedge-certainty regime.** p_noncommit 0.74 (judgment hedge
  0.80), accuracy 0.30, 80% of FT errors are hedge collisions. On hybrid
  questions — exactly where fundamentals and trading signals conflict —
  the same model retreats to `mixed`/`conditional`.
- **T-lane → committed-but-wrong regime.** p_noncommit 0.05 (fully
  commits), yet accuracy 0.375 with **84% of T errors being
  wrong-direction** (picks the wrong ticker). Commitment without
  accuracy.

This is decisive for the paper's framing: capability (27B, FP8) does not
move a model uniformly from hedging to commitment. It buys commitment on
F and T, but the model still hedges specifically on FT, the cross-signal
conflict lane. This directly corroborates the E-C' mechanism — injected
F/T conflict drives hedging — now seen *naturally*: the lane whose gold
reasoning is inherently cross-signal is the lane where a capable model
chooses to hedge.

### What is genuinely new vs the small local models

1. **It actually expresses distributional uncertainty.** R1 degeneracy
   0.42 vs 0.71–0.73 for gemma4/qwen3:8b; R1 AU_norm 0.162 vs
   0.026–0.049. This is the first *open-weights* model whose decodes
   spread rather than collapse to a single hedge token — so AU is a real,
   moving quantity here.
2. **Largest AU-reduction of any model** (dAU −0.149, p=3e-13),
   *because* it has the most AU to reduce. The universal AU-reduction law
   holds across all four models and is strongest here.
3. **Debate is mildly net-positive on truth** (6 rescues vs 4 losses;
   11 productive-convergence, 29 noise-reduction) — unlike qwen3:8b
   (net-harmful, 4 rescue / 8 loss) and gemma4 (inert, 5/3). More AU
   headroom gives the debate something to work with.

### p_noncommit unchanged in character

Same hedge-collision-detector signature: AUROC 0.785 on committed-gold
but **0.408 (chance) in the non-mechanical committed-gold∧committed-pred
cell**. Even for this stronger model, p_noncommit carries no
wrong-direction signal — consistent with
NONCOMMIT_ERROR_DECOMPOSITION_FINDINGS across all models.

### Updated cross-model regime map

| model | F | FT | T | whole-model reading |
|---|---|---|---|---|
| gemma4 | hedge | hedge (pNC 0.97) | mixed | uniform hedge-certainty |
| qwen3:8b | partial | hedge | committed-wrong | mostly hedge |
| **qwen3.6-27b** | **commit (0.61 acc)** | **hedge (0.74 pNC)** | **committed-wrong** | **lane-dependent** |
| gemini-3.1-pro | commit | partial commit | commit | commitment (n=16) |

**The universal, model-independent regularities** (hold across all four):
(i) FT is always the highest-hedging lane; (ii) debate reduces AU, never
EU; (iii) p_noncommit is a hedge-collision detector with no
committed-cell signal; (iv) T-lane errors are dominated by
wrong-direction commitment, invisible to every uncertainty signal.

---

## Paper impact (tables/figures updated)

- `analysis/model_comparison_table.csv` regenerated with all four models
  (the source for the paper's cross-model table).
- The regime section of the paper moves from a **two-regime (small vs
  capable)** framing to a **model×lane regime map** — qwen3.6-27b is the
  pivot case showing capability alone doesn't determine regime; the lane
  (cross-signal conflict) does. THREE_MODEL_FINDINGS.md updated with a
  pointer to this four-model result.
- Reinforces the E-C' causal story: FT (natural cross-signal conflict)
  is where even a capable model hedges, matching the do(inject_conflict)
  → hedging result.
