# STATISTICAL_ANALYSIS_PLAN_EU_AU

Carries over the discipline of the audit's plan (clustering, FDR,
measurement-noise honesty) applied to EU/AU objects.

## Units and dependence

- Row = question × round × evidence_mode. Rounds within a question are
  **paired**, never pooled as independent.
- Clusters: company/ticker (repeated across questions), date window
  (150/150 questions are dated; many share months), template family,
  lane. Cluster bootstrap resamples **questions grouped by primary
  ticker**; date-level claims use date clusters.
- Never IID-pool: report design effects as in the audit (sector ICC 0.72
  there; expect ticker clustering here).

## Measurement noise (binding, from G0)

- T-lane single-decode noise is 3–4× F/FT. Lane comparisons of AU/EU use:
  (a) equal-K subsampling (compare at matched K), (b) Miller–Madow
  correction, and (c) a noise-corrected contrast: subtract the
  within-question bootstrap variance component from the lane mean
  difference. All three reported; disagreement between them = flagged.
- Every headline aggregate carries the median within-question bootstrap
  CI width next to the between-question spread (if within ≥ between, the
  quantity is uninformative at current K — the audit's P2-A rule).

## Analyses

1. **Descriptives**: EU/AU/TU distributions by lane × round (violin/CDF),
   EU/TU ratio, G by round, transition-class rates with multinomial CIs.
2. **Paired round-0 vs round-1**: Wilcoxon signed-rank + paired bootstrap
   on ΔEU, ΔAU, ΔG; effect sizes (matched-pairs rank-biserial).
3. **Lane-stratified models**: mixed-effects (statsmodels MixedLM;
   random intercept = ticker) of AU and EU on lane + answer_type + |Y| +
   K_eff + date fixed effects. The RQ3 hypotheses (T→AU↑, FT→EU↑) are
   confirmatory — pre-registered here; everything else exploratory.
4. **ΔEU vs ΔG**: within-lane Spearman + quadrant analysis (the
   false-consensus quadrant rate is the headline); logistic model of
   FALSE_CONSENSUS on round-0 features (EU_0, AU_0, G_0, lane, |Y|).
5. **RQ6 incremental value**: AUROC of error prediction from {EU, AU,
   EU/TU} vs baselines {system entropy TU, single-agent self-consistency
   entropy, verbalized confidence}; ΔAUROC with cluster bootstrap CI.
   (KILL-6 analogue: if ΔAUROC ≈ 0, say so — decomposition still has
   descriptive value via transitions, but the predictive claim dies.)
6. **Sensitivity**: ε-threshold sweep for the taxonomy; K-sensitivity
   (K=5/10/20 subsample curves); parse-failure exclusion vs imputation;
   model sensitivity (second-model subset); Miller–Madow on/off.
7. **Multiplicity**: BH-FDR within families (lane grid; transition rates;
   intervention cells).

## Calibration (evaluation only — U5 rule)

Brier, NLL, ECE (equal-mass bins, only if n per bin ≥ 30), reliability
curves per lane. Never as features.

## Power sanity

~144 headline questions (150 minus schema_uncertain): paired round
contrast detects d_z ≈ 0.24 at 80%/α=.05; lane contrasts (~48/lane)
detect d ≈ 0.58 between lanes — moderate: report CIs, avoid
overclaiming null lane differences.
