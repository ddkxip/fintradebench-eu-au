# main_pilot20 summary (16 questions, K=10 F/FT / 20 T, R0+R1, gemma4)

- rows: 32 (16 questions x rounds [np.int64(0), np.int64(1)])
- parse rate: min=0.875 mean=0.993

## EU/AU/TU (normalized) by lane x round

```
            eu_norm  au_norm  tu_norm  gold_prob  correct  brier
lane round                                                      
F    0        0.029    0.137    0.166      0.793    0.857  0.274
     1        0.010    0.033    0.042      0.843    0.857  0.289
FT   0        0.019    0.123    0.142      0.367    0.333  1.146
     1        0.033    0.040    0.073      0.383    0.333  1.163
T    0        0.063    0.218    0.281      0.617    0.667  0.485
     1        0.091    0.162    0.253      0.531    0.667  0.614
```

Miller-Madow (bias-corrected, unnormalized nats):

```
            eu_mm  au_mm  tu_mm
lane round                     
F    0      0.039  0.208  0.244
     1      0.011  0.039  0.050
FT   0      0.026  0.187  0.210
     1      0.046  0.060  0.106
T    0      0.105  0.416  0.521
     1      0.158  0.303  0.461
```

## Paired R0->R1 deltas

```
       d_eu          d_au           d_g        d_correct       
       mean median   mean median   mean median      mean median
lane                                                           
F    -0.019 -0.005 -0.104 -0.117  0.050    0.0       0.0    0.0
FT    0.014  0.000 -0.083 -0.059  0.017    0.0       0.0    0.0
T     0.028  0.010 -0.056 -0.170 -0.085    0.0       0.0    0.0
```
- Wilcoxon d_eu: stat=29.0 p=0.721 (n=11 nonzero of 16)
- Wilcoxon d_au: stat=18.0 p=0.181 (n=11 nonzero of 16)
- Wilcoxon d_g: stat=12.0 p=0.400 (n=8 nonzero of 16)

## Transition taxonomy (R0 -> R1)

- outcome: {'STABLE_SUCCESS': 10, 'STABLE_FAILURE': 6}
- flow: {'NO_MATERIAL_CHANGE': 5, 'MIXED_FLOW': 4, 'NOISE_REDUCTION': 3, 'ALEATORIC_DESTABILIZATION': 2, 'PRODUCTIVE_CONVERGENCE': 2}
- persistent rational disagreement: 11; correct-minority suppression: 0
- false consensus rate: 0.00; productive convergence rate: 0.12

## Hedge-label attractor check

- degenerate rows (TU=0): 19/32 ({'F': 9, 'FT': 8, 'T': 2})
- hedge-label predictions (mixed/conditional): 14/32 rows; by lane {'F': 0.29, 'FT': 0.83, 'T': 0.0}
- judgment questions predicting a hedge label: 14/16 rows; correct rate on those rows: 0.43

## Per-question detail
```
question_id lane  round  eu_norm  au_norm  gold_prob         predicted  correct
         F1    F      0    0.026    0.117      0.950             mixed     True
         F1    F      1   -0.000    0.000      1.000             mixed     True
        F11    F      0    0.085    0.220      0.000             mixed    False
        F11    F      1   -0.000    0.000      0.000             mixed    False
        F12    F      0    0.005    0.401      0.750             GOOGL     True
        F12    F      1   -0.000    0.000      1.000             GOOGL     True
         F2    F      0   -0.000    0.000      1.000             GOOGL     True
         F2    F      1    0.068    0.228      0.900             GOOGL     True
        F25    F      0   -0.000    0.000      1.000 insufficient_data     True
        F25    F      1   -0.000    0.000      1.000 insufficient_data     True
        F31    F      0    0.085    0.220      0.850              COST     True
        F31    F      1   -0.000    0.000      1.000              COST     True
        F44    F      0   -0.000    0.000      1.000        claim_true     True
        F44    F      1   -0.000    0.000      1.000        claim_true     True
        FT1   FT      0   -0.000    0.000      1.000       conditional     True
        FT1   FT      1   -0.000    0.000      1.000       conditional     True
       FT10   FT      0    0.085    0.220      0.000       conditional    False
       FT10   FT      1   -0.000    0.000      0.000       conditional    False
       FT12   FT      0   -0.000    0.000      0.000             mixed    False
       FT12   FT      1   -0.000    0.000      0.000             mixed    False
        FT2   FT      0   -0.000    0.000      0.000       conditional    False
        FT2   FT      1   -0.000    0.000      0.000       conditional    False
       FT25   FT      0    0.026    0.117      0.950       conditional     True
       FT25   FT      1   -0.000    0.000      1.000       conditional     True
       FT31   FT      0    0.005    0.401      0.250 insufficient_data    False
       FT31   FT      1    0.198    0.243      0.300 insufficient_data    False
         T1    T      0   -0.000    0.000      1.000               APP     True
         T1    T      1    0.010    0.367      0.594               APP     True
        T10    T      0    0.065    0.170      0.850              AAPL     True
        T10    T      1   -0.000    0.000      1.000              AAPL     True
         T2    T      0    0.124    0.484      0.000              LRCX    False
         T2    T      1    0.263    0.118      0.000              LRCX    False
```

## Predictions vs gold labels (final round)
```
gold               predicted        
AAPL               AAPL                 1
APP                APP                  1
COST               COST                 1
GOOGL              GOOGL                2
INTC               LRCX                 1
claim_true         claim_true           1
conditional        conditional          2
                   insufficient_data    1
insufficient_data  insufficient_data    1
mixed              mixed                1
supportive         conditional          1
unsupportive       conditional          1
yes                mixed                2
```