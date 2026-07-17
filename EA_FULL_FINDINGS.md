# EA_FULL_FINDINGS — the powered E-A' results (139 q × 2 models × 2 rounds)

Full tables: results/ea_full_summary.md; transitions_{model}.csv.
Parse 99.8% overall; zero failed questions; gemma4 + qwen3:8b ≈ 14h total.

## 1. The AU-reduction law is now highly significant — the program's anchor result

Debate (one exchange round) reduces within-agent instability in both
models: **dAU gemma4 −0.091 (Wilcoxon p = 8.9e-09), qwen3 −0.070
(p = 3.3e-07)**, while dEU ≈ 0 (p = 0.80/0.86). With the gemini-16 result
this is three-for-three. Decode degeneracy rises correspondingly (up to
90% of gemma4-FT rows TU=0 at R1). Debate in this architecture is a
**self-consistency amplifier, not a disagreement resolver**.

## 2. NEW at scale: debate *increases* categorical hedging

dNC (change in non-commitment mass R0→R1): qwen3 **+0.057
(p = 7.7e-05)**; gemma4 +0.015 (p = 0.098). Seeing the opponent pushes
qwen toward hedge labels. Combined with §1: debate makes agents more
consistent *and* more non-committal — confidence laundering into hedges.

## 3. The central UQ result: categorical beats distributional uncertainty

Error-prediction AUROC (final round):

| predictor | gemma4 | qwen3 |
|---|---|---|
| TU (system entropy) | 0.451 | 0.399 |
| AU | 0.459 | 0.524 |
| EU | 0.446 | 0.384 |
| **p_noncommit** | **0.694** | **0.636** |

Distribution-level uncertainty is uninformative-to-*inverted* (below
0.5: spread decodes weakly signal correctness, concentrated hedges
signal error). **The usable uncertainty signal lives in the label
semantics** — exactly the categorical-vs-distributional thesis, now
quantified on 139 questions × 2 models. This is the paper's headline
table candidate.

## 4. Hedge-collision at scale is worse than the pilot suggested

gemma4-FT: p_noncommit = **0.97** (essentially every FT decode is a
hedge) against ~30% hedge-label golds → strict accuracy **18%**.
Full-set strict accuracy: gemma4 F .27 / FT .18 / T .43; qwen3 F .45 /
FT .34 / T .43. The pilot-16 accuracies (60-69%) were an easy-subset
artifact — the first-authored schemas had cleaner golds. Error rates of
60-72% give the transition taxonomy real mass to classify.

## 5. False consensus EXISTS at scale — the pilot's "pre-emption" needs nuance

gemma4: 6 false-consensus cases (4.3%), 5 rescues vs 3 losses.
qwen3: **11 false consensus (7.9%), 2 correct-minority suppressions,
8 correctness-lost vs 4 rescues** — qwen's debate is net harmful on
outcomes. Revision of the pilot claim: prior hedge-consensus *dampens*
but does not eliminate the CAGE-CAL phenomenon; when commitment exists
(qwen commits more than gemma), debate can and does destroy correct
answers at a measurable rate.

## 6. RQ3 verdicts (confirmatory, MM-corrected, ticker-cluster bootstrap)

- **T-higher-AU: model-dependent.** gemma4 +0.279 [CI +0.128, +0.423]
  SUPPORTED; qwen3 +0.027 [−0.056, +0.115] not supported. The G0
  lane-noise finding generalizes to gemma-family only — report as such,
  never pooled.
- **FT-higher-EU: dead in both models** (gemma −0.047 ns; qwen +0.001
  ns). Consistent with mechanism: hedging suppresses EU precisely on FT.

## 7. Strict vs lenient scoring — screening accuracy is top-1 tie-breaking

T-lane strict 0.425 both models → lenient (predicted named in gold
evidence) **0.775/0.850**. Most T "errors" are within-gold-set picks.
F/FT gaps are small (≤0.06). All screening results must be reported in
both scorings; the strict-lenient gap is itself a benchmark finding.

## 8. Paper skeleton (updated)

1. Setup: schemas, oracle evidence, self-consistency EU/AU with
   p_noncommit as a first-class quantity.
2. **Regimes**: hedge-certainty (open-weights; FT p_noncommit up to
   0.97) vs commitment (gemini-16: EU 3× floor, dEU>0) — capability
   grades the attractor.
3. **Laws**: universal AU-reduction (3 models, p<1e-6); debate increases
   hedging (qwen p<1e-4); EU flat under debate.
4. **UQ claim**: categorical > distributional for error prediction
   (AUROC 0.64-0.69 vs ≤0.52); distributional partly inverted.
5. **Truth alignment**: false consensus 4-8%; qwen debate net harmful;
   rescues rare. Lane hypotheses: T-AU model-dependent, FT-EU dead.
6. Strict/lenient gap + gold-disagreement analysis (benchmark-side
   insight).

Remaining before draft: E-B' mixed-effects with controls (lane,
answer_type, |Y|, ticker RE) formalizing §3-§6; gemini ≥50q run if the
two-regime framing headlines; interventions (E-C') for source
conditioning.
