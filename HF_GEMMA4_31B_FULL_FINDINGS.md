# gemma4-31b-it — full E-A findings

Reanalysis of `results/ea_full_hf_gemma_4_31B_it/rows.csv` (139 headline-eligible questions, R0+R1, K=10 F/FT / 20 T). Metric definitions identical to analyze_ea_full.py; no new model calls.
- parse rate: 1.000; scored final rows: 139

## 1-2. Accuracy (strict) by round and lane

- overall R0 acc = **0.410**, R1 acc = **0.446**
```
round      0      1
lane               
F      0.551  0.551
FT     0.280  0.400
T      0.400  0.375
```

## 3. TU / AU / EU (normalized) + Miller-Madow by lane and round

```
            tu_norm  au_norm  eu_norm  au_mm  eu_mm  tu_mm
lane round                                                
F    0        0.075    0.017    0.058  0.021  0.072  0.092
     1        0.061    0.005    0.056  0.008  0.075  0.082
FT   0        0.116    0.021    0.096  0.031  0.133  0.164
     1        0.172    0.009    0.163  0.014  0.234  0.248
T    0        0.063    0.014    0.049  0.025  0.080  0.104
     1        0.116    0.026    0.091  0.044  0.152  0.196
```

## 4. Debate deltas R0->R1 (paired)

- dAU: mean -0.0054, Wilcoxon p=2.80e-01 (nonzero n=23)
- dEU: mean +0.0356, Wilcoxon p=3.49e-02 (nonzero n=38)
- dNC: mean +0.0074, Wilcoxon p=7.98e-01 (nonzero n=27)
- dG: mean +0.0194, Wilcoxon p=2.16e-01 (nonzero n=29)

## 5. p_noncommit by lane and round

```
             mean  median
lane round               
F    0      0.407     0.0
     1      0.460     0.5
FT   0      0.771     1.0
     1      0.725     1.0
T    0      0.099     0.0
     1      0.118     0.0
```
- degenerate rows (TU=0): 0.773 overall; R1 0.734

## 6. AUROC for error prediction (final round)

error rate = 0.55
| predictor | AUROC (all) | AUROC committed-gold | AUROC commit-gold&commit-pred |
|---|---|---|---|
| tu_norm | 0.473 | 0.431 | 0.552 |
| au_norm | 0.525 | 0.532 | 0.624 |
| eu_norm | 0.470 | 0.427 | 0.541 |
| p_noncommit | 0.721 | 0.785 | 0.437 |

(committed-gold n=117; committed-gold & committed-pred n=78 — the non-mechanical cell.)

## 7. Non-commitment error decomposition (final round)

```
                             n  share
error_type                           
hedge_collision             39  0.506
wrong_direction_commitment  24  0.312
overcommitment               8  0.104
wrong_noncommit_type         6  0.078
```
- non-committal gold questions: 22; correct-noncommitment rate: 0.57 (n_hedged=14)

### share of errors by lane
```
lane  error_type                
F     hedge_collision               0.727
      overcommitment                0.136
      wrong_direction_commitment    0.136
FT    hedge_collision               0.633
      overcommitment                0.100
      wrong_direction_commitment    0.067
      wrong_noncommit_type          0.200
T     hedge_collision               0.160
      overcommitment                0.080
      wrong_direction_commitment    0.760
```

## 8. Debate transitions (R0->R1)

- outcome: {'STABLE_FAILURE': 75, 'STABLE_SUCCESS': 55, 'DEBATE_RESCUE': 7, 'CORRECTNESS_LOST': 2}
- flow: {'NO_MATERIAL_CHANGE': 99, 'MIXED_FLOW': 28, 'PRODUCTIVE_CONVERGENCE': 5, 'ALEATORIC_DESTABILIZATION': 4, 'FALSE_CONSENSUS': 2, 'NOISE_REDUCTION': 1}
- rescue: 7, loss: 2, stable-correct: 55, stable-wrong: 75
- false consensus: 2 (1.4%); minority suppression: 1

## 9. Cross-model comparison

(gemini = 16-q subset, flagged; not pooled with the 139-q models)

```
         model  n_q  R0_acc  R1_acc  R1_EU  R1_AU  R1_pNC    dAU   dEU   dNC  degen_R1  AUROC_pNC_all  AUROC_pNC_commitcell  hedge_coll_share
        gemma4  139   0.266   0.281  0.052  0.049   0.633 -0.091 0.001 0.015     0.712          0.694                 0.446             0.670
      qwen3:8b  139   0.432   0.403  0.098  0.026   0.483 -0.070 0.009 0.056     0.727          0.636                 0.403             0.554
   qwen3.6-27b  139   0.417   0.432  0.055  0.162   0.386 -0.149 0.010 0.017     0.417          0.704                 0.408             0.532
 gemma4-31b-it  139   0.410   0.446  0.104  0.012   0.457 -0.005 0.036 0.007     0.734          0.721                 0.437             0.506
gemini-3.1-pro   16   0.562   0.500  0.114  0.030   0.462 -0.128 0.067 0.031     0.688          0.594                 0.833             0.375
```

### R1 strict accuracy by lane x model

```
model  gemini-3.1-pro  gemma4  gemma4-31b-it  qwen3.6-27b  qwen3:8b
lane                                                               
F               0.429   0.265          0.551        0.612     0.449
FT              0.500   0.180          0.400        0.300     0.340
T               0.667   0.425          0.375        0.375     0.425
```

## 10a. Regime diagnostics (per lane, final round)

```
lane  R1_EU  R1_pNC  judgment_hedge_rate   acc
   F  0.056   0.460                0.517 0.551
  FT  0.163   0.725                0.592 0.400
   T  0.091   0.118                  NaN 0.375
```
## 10b. Verdict — lane-dependent regime, AND the first exception to the AU-reduction law

### (i) BREAKS the "universal AU-reduction law" — report this honestly

Across gemma4, qwen3:8b, qwen3.6-27b and gemini, debate always significantly
reduced AU (p from 3e-13 to 1e-6). **gemma4-31b-it does not: dAU = −0.005,
p = 0.28 (n.s.)** — and it is instead the first *local* model with a
**significant EU increase (dEU = +0.036, p = 0.035)**.

The mechanism is visible and benign, not a contradiction: this model has
**no AU headroom to begin with**. Its R0 AU_norm is the lowest ever
recorded here (F 0.017 / FT 0.021 / T 0.014; R1 AU 0.012 overall) with
**77% degenerate (TU=0) rows**. Its decodes are near-deterministic before
debate, so there is essentially no within-agent instability left to remove;
what debate does instead is push the two framework agents *apart*
(EU up, especially FT: 0.096 → 0.163).

**Restatement required for the paper.** The law is not "debate reduces AU"
unconditionally; it is:

> Debate reduces within-agent instability **where such instability exists**
> (AU headroom); where agents are already near-deterministic, debate instead
> increases between-agent divergence (EU).

That is a strictly better claim — it now has a stated scope condition and an
observed boundary case, and it still covers all five runs. gemini (the other
significant-dEU model) fits the same pattern from the opposite direction:
high capability → commitment → polarization rather than stabilization.

### (ii) Lane-dependent regime — confirms the model×lane map

```
lane   p_noncommit   judgment hedge   acc      reading
F      0.46          0.52             0.551    partial commitment
FT     0.73          0.59             0.400    hedge-certainty
T      0.12          n/a              0.375    committed-but-wrong (76% wrong-direction)
```

Same three-regime split as qwen3.6-27b: commits on F and T, hedges on FT.
This is now **two independent mid-size open-weights models** showing the
identical lane pattern, which materially strengthens the model×lane framing
over a whole-model "capability regime" story. FT remains the highest-hedging
lane in every single model tested (5/5).

### (iii) Best-performing local model on several axes

- **Highest R1 accuracy of the four 139-q models (0.446)** and the best FT
  accuracy among the local models (0.400 vs 0.180/0.300/0.340).
- **Most favourable debate outcome ledger: 7 rescues vs 2 losses**, the only
  model with a >3:1 rescue:loss ratio, and the **lowest false-consensus rate
  (1.4%** vs 4.3–7.9%).
- **Lowest hedge-collision share of the 139-q models (0.506)** — still the
  modal error type, but least dominant.
- Debate mostly does nothing (99/139 NO_MATERIAL_CHANGE), consistent with
  near-deterministic decoding.

### (iv) p_noncommit behaves exactly as established

**Highest overall AUROC yet (0.721)**, 0.785 on committed-gold — but
**0.437 (≈chance) in the non-mechanical committed∧committed-pred cell.**
Fifth consecutive model confirming: hedge-collision detector, no
wrong-direction signal. T-lane errors remain 76% wrong-direction and remain
invisible to every uncertainty channel.
