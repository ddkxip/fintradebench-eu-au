# EB_CONTROLLED_FINDINGS — what survives controls

Full tables: analysis/eu_au_controlled_analysis.md. Unit = question ×
model (n=278); clustering = primary ticker (30 clusters); BH-FDR across
all 39 reported coefficients. Reading below is deliberately conservative.

## The four results that survive FDR (q < 0.05)

> **REFINED — see NONCOMMIT_ERROR_DECOMPOSITION_FINDINGS.md.** The
> estimate below is unaffected, but the single-slope specification is
> misspecified: adding a p_noncommit × noncommit_is_gold interaction
> flips the slope from +4.33 (committed gold) to −13.17 (non-committal
> gold) and lifts pseudo-R² from 0.10 to 0.40. Report the interaction.

1. **p_noncommit predicts error, net of TU and lane, in BOTH models**
   (gemma4 β=+1.82, q=0.012; qwen3 β=+1.58, q=0.016). This is the
   headline UQ claim confirmed under controls: the mass an item places on
   non-committal labels is a genuine error signal, and it is not a
   lane artifact. TU is null (gemma) or *negative* (qwen β=−2.29,
   p=0.037, not FDR-surviving) — distribution-level uncertainty does not
   help and may invert. Categorical > distributional, controlled.

2. **T-lane shows higher AU and higher EU once answer_type is in the
   model** (q=1.5e-13 and q=0.01) — but see the caveat below; this
   coefficient is not clean.

## The honest caveat on the lane coefficients (do not overclaim)

- **Without answer_type** (Q1A), no lane effect on AU is significant
  (T: β=+0.084, p=0.24). **With answer_type** (Q1B) the T coefficient
  jumps to +0.31 and becomes hugely significant — accompanied by a
  rank-deficiency warning. Reason: `screening_top1` answer_type is
  ~perfectly collinear with T-lane (nearly all screenings are T). The
  regression cannot separate "T-lane" from "screening-format", so the
  Q1B coefficient is a **suppression artifact of collinear predictors**,
  not independent confirmation. I am NOT reporting it as clean evidence.

- The **defensible** evidence for T-higher-AU is the **matched-K
  bootstrap (Q2)**, which rules out the K=10-vs-20 estimator asymmetry:
  recomputing T-lane AU from K=10 subsamples, **gemma4 T-AU exceeds F/FT
  by +0.263 [95% CI +0.148, +0.384] — SUPPORTED; qwen3 +0.019
  [−0.062, +0.104] — not supported.** So the powered, controlled verdict
  matches E-A': **T-higher-AU is real but gemma-family-specific**, and it
  is a measurement-noise property (survives matched-K), not a
  format/space-size artifact.

## Strong negative result: debate improvement is unpredictable (Q4)

Neither initial EU (β=−0.096, p=0.34), initial AU, nor initial
p_noncommit predicts ΔG; and ΔEU/ΔAU do not predict ΔG (both p>0.79).
**Nothing in the uncertainty profile forecasts whether a debate round
will help.** Combined with the near-zero mean ΔG, this says the single
exchange round is close to inert on truth for these models — you cannot
target debate at the items it will help, because uncertainty doesn't
flag them. A clean, citable null that constrains any "uncertainty-guided
debate" pitch (and matches why we deferred routing).

## Q5 hedging push — directionally consistent, not FDR-robust

dNC is higher for qwen than gemma (β=+0.031, p=0.036) and lower on
T-lane (β=−0.061, p=0.047), but neither survives FDR. The debate-
increases-hedging effect is real in the raw Wilcoxon (qwen dNC p=8e-5,
EA_FULL_FINDINGS §2) but, once decomposed by model/lane with clustering,
individual cells are underpowered. Report the pooled Wilcoxon as the
claim; treat the model×lane breakdown as exploratory.

## Consolidated verdicts (E-A' + E-B' together)

| Claim | Status after controls |
|---|---|
| p_noncommit predicts error (net of TU, lane) | **CONFIRMED, both models, FDR** |
| Categorical > distributional uncertainty | **CONFIRMED** (TU null/inverted) |
| Debate reduces AU | **CONFIRMED** (Wilcoxon p<1e-6 both; 3-model) |
| Debate improvement predictable from uncertainty | **REJECTED** (Q4 all null) |
| T-higher-AU | **gemma-only**, survives matched-K; qwen null |
| FT-higher-EU | **REJECTED** both models |
| Debate increases hedging | supported pooled (qwen); cell-level exploratory |
| False consensus at scale | 4% gemma / 8% qwen (E-A'); qwen net-harmful |

## For the paper

Q3 is Table 1 (controlled error-prediction). Q2 is the T-AU robustness
box. Q4 is the "you can't route on it" null that motivates the
descriptive rather than prescriptive framing. The lane regression (Q1)
goes in the appendix WITH the collinearity caveat — the matched-K
bootstrap is the result, not the OLS coefficient.

Remaining program items: E-C' source interventions (the one thing that
can turn these associations causal); optional gemini ≥50q run if the
two-regime story headlines. E-B' closes the observational analysis.
