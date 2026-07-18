# EC_INTERVENTION_FINDINGS — the causal arm: uncertainty is NOT evidence-responsive in the hedge-certainty regime

gemma4, Round 0, 30 F/FT questions, K=10, paired vs the ea_full_gemma4
oracle baseline. Full table: analysis/source_intervention_pilot.md.
Parse 97.6%. These are do-interventions (randomized edits we applied), so
the language here is licensed to be causal — but the headline result is a
causal *null*, and that null is the point.

## Headline: the do-operators barely move the uncertainty signals

Not one of the pre-registered on-target predictions is confirmed at the
FDR-corrected level; most are null even uncorrected:

| do-operator | predicted | observed | verdict |
|---|---|---|---|
| remove top golden indicator | p_noncommit/AU ↑, G ↓ | +0.004 / +0.020 / −0.009 (all p>0.38) | **no effect** |
| — vs placebo (selectivity) | top ≫ placebo | top−placebo +0.026 p_noncommit (p=0.44); null on AU, G | **no selectivity** |
| inject F/T conflict | EU ↑ | **EU −0.041** [−0.087,−0.001]; p_noncommit +0.028; G −0.016 [−0.035,−0.002] | **opposite: conflict suppresses EU** |
| horizon dial (short vs long) | verdict/confidence shift | 3/30 verdict flips; G long−short +0.002 (p=0.77) | **horizon-insensitive** |

## Result 1 — construct validity FAILS for evidence sufficiency (in this regime)

Removing the single most important golden indicator does not
selectively raise uncertainty or lower gold-probability, and the
diagonal-vs-off-diagonal contrast (remove_top vs matched-placebo removal)
is null on every metric. **gemma4's uncertainty does not track which
evidence is present.** A large fraction of paired deltas are *exactly
zero* — the model was already at a degenerate hedge (TU=0) and stayed
there after the edit. So the EU/AU decomposition, in the hedge-certainty
regime, is not a valid measure of evidence-driven uncertainty: it is a
stable stylistic property, not an evidence-responsive one. This is the
causal confirmation of what E-A'/E-B' showed observationally (p_noncommit
predicts error but TU/EU do not) — now with interventions ruling out
confounds.

## Result 2 — injected conflict SUPPRESSES measurable disagreement (the pathological signature)

The sharpest mechanistic finding. We coherently rewrote the trading
channel to oppose the fundamental lean — a genuine cross-signal
contradiction both agents can see. Prediction was EU ↑. **EU went down
(−0.041, CI excludes 0), p_noncommit went up (+0.028), gold-prob dropped
(−0.016, CI excludes 0).** Mechanism: forced conflict drives *both*
framework agents into the same non-committal labels, so they *agree more*
on "mixed/conditional" — apparent between-agent disagreement falls while
the answer gets slightly worse. Conflict is absorbed into shared hedging,
not expressed as epistemic uncertainty. This is exactly the failure mode
that makes EU untrustworthy here: the debate looks *more* consensual
precisely when the evidence is *most* contradictory. (F-lane shows the
effect more than FT, consistent with FT already being saturated at
p_noncommit≈0.97.)

## Result 3 — horizon insensitivity at the verdict level

Dialing the horizon from 3 months to 5 years (evidence fixed) flips only
3/30 verdicts and moves gold-prob by +0.002 (null). There are minor
distributional perturbations vs the no-suffix baseline (short horizon
lowers EU −0.073 p=0.04; long horizon lowers gold-prob −0.037 p=0.04),
but neither survives BH-FDR across the ~20-cell grid, and the direct
short-vs-long contrast is flat. **The system does not condition its
verdict on the stated horizon** — a clean finding given that horizon is
the canonical finance-native uncertainty dial.

## Why the nulls strengthen the paper

The two-regime story now has a causal boundary condition:

- **Hedge-certainty regime (gemma4, shown here):** uncertainty signals
  are *not* evidence-responsive — remove-evidence, inject-conflict, and
  horizon-dial all fail to move them selectively; injected conflict even
  *suppresses* EU. The decomposition lacks construct validity as an
  evidence-driven uncertainty measure in this regime.
- **Commitment regime (gemini, THREE_MODEL_FINDINGS):** EU emerges and
  tracks real framework disagreement. **Prediction, now decisively
  testable:** the same interventions on gemini *should* produce the
  selective responses that failed here. This is the single most valuable
  follow-up — it would show construct validity is *recovered* with
  capability, turning "the decomposition sometimes fails" into
  "the decomposition is valid iff the model commits."

## Caveats

n=30, one model, Round 0. Several Wilcoxon cells are undefined (too few
nonzero deltas — itself diagnostic of degeneracy); where that happens I
rely on the bootstrap CI (inject_conflict G and EU CIs exclude 0). The
inject_conflict arm uses edited (fabricated-but-flagged) trading values;
its result is about the *system's response to contradiction*, correctly
scoped. FDR across the arm×metric grid leaves nothing significant, which
is the honest headline: **the interventions do not move the signals.**

## Program status

Both arms of the empirical program are now closed:
- Observational: E-A' (139q×2 models) + E-B' (controlled, FDR).
- Causal: E-C' interventions (this doc).
Remaining optional: gemini intervention run (the construct-validity
recovery test) and gemini ≥50q E-A' — both only if the two-regime story
headlines. The paper can be drafted now.
