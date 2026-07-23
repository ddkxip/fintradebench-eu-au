# NONCOMMIT_ERROR_DECOMPOSITION_FINDINGS

Reanalysis only (no new model calls). Tables:
analysis/noncommit_error_decomposition.md; per-row data:
analysis/noncommit_decomposition_rows.csv. Primary set = gemma4 + qwen3
final-round rows over the 139 headline-eligible questions (n=278);
gemini's 16-question subset reported separately, never pooled.

**This document materially refines the headline UQ claim in
EA_FULL_FINDINGS §3 and EB_CONTROLLED_FINDINGS §1.** `p_noncommit` does
predict error — but not for the reason the earlier framing implied.

---

## 1. Is p_noncommit mainly detecting hedge collisions? — **Yes, decisively.**

Three independent lines converge:

- **Error composition.** 61.7% of all errors are *hedge collisions*
  (gold is a committed label; the system predicted a non-committal one).
  gemma4 67%, qwen3 55%. By lane: F 73%, FT 80%, T 17%.
- **AUROC splits by gold type.** On committed-gold questions
  p_noncommit is a strong error predictor (**0.853 gemma / 0.769 qwen**);
  on non-committal-gold questions it *inverts* (**0.359 / 0.062** — high
  hedging there predicts being **right**). The pooled 0.694/0.636 is a
  blend of these two opposite regimes, not one coherent effect.
- **The interaction is enormous.** In M3 the slope of p_noncommit is
  **+4.33** on committed-gold questions and **−13.17** on
  non-committal-gold questions (interaction −17.50, p=4e-11); pseudo-R²
  rises from 0.103 (M1) to 0.397 (M3). A single-slope model of
  "uncertainty → error" is badly misspecified.

**Crucial honesty check.** Much of this is *definitional*: when the gold
is committed, a non-committal prediction is wrong **by construction**,
and p_noncommit is essentially the continuous version of "the argmax is
non-committal." So the 0.85 AUROC is substantially mechanical. The test
that removes the mechanism is the cell where gold **and** prediction are
both committed — and there p_noncommit carries **no usable signal**
(AUROC **0.446 gemma / 0.403 qwen**, n=50/71, both indistinguishable
from chance). p_noncommit does not rank *wrong-direction* errors at all.

## 2. How often is non-commitment actually correct? — **Often; it is not a failure mode per se.**

The gold itself is non-committal on **15.8% of questions (22 of 139)** —
F 14%, FT 26%, T 5%. When the gold is non-committal *and* the system
hedges, the error rate is only **0.32 (gemma) / 0.07 (qwen)** — i.e.
hedging is correct roughly **68–93%** of the time in that cell (≈79%
pooled over 34 rows). Non-commitment is a legitimate answer that the
benchmark rewards; the pathology is emitting it on the 84% of questions
whose gold is directional.

## 3. How often do models commit but in the wrong direction? — **29% of errors; and it is the *dominant* mode on T-lane.**

*Wrong-direction commitment* is 29.0% of pooled errors (gemma 24 cases /
24%, qwen 29 / 35%). Within the committed-gold∧committed-prediction cell
the error rate is **0.48 (gemma) / 0.41 (qwen)** — near a coin flip on
questions where the model does take a position. By lane it is 74% of all
T-lane errors (screening top-1 picks), versus 24% on F and just 5% on FT.
The two remaining modes are small: overcommitment (committed prediction
on non-committal gold) 5.5%, wrong-non-committal-type (e.g. `mixed` when
gold is `insufficient_data`) 3.8%.

So the benchmark has **two structurally different failure regimes**:
F/FT fails by hedging, T fails by picking the wrong ticker — and
p_noncommit only sees the first (lane-T AUROC 0.53/0.51, i.e. useless).

## 4. Does p_noncommit still predict error within committed-gold questions? — **Only through the mechanical channel; no residual signal.**

Yes on committed-gold questions taken as a whole (0.853/0.769), but that
is the hedge-collision mechanism doing the work. Restricting to
committed-gold **and** committed-prediction rows — where the outcome is
no longer definitionally tied to the predictor — AUROC falls to
0.446/0.403, at or below chance. **Conditional on the model taking a
position, the amount of probability mass it left on hedge labels tells
you nothing about whether the position is right.**

## 5. How should the paper describe p_noncommit? — **As a hedge-collision detector, not a general error predictor.**

Recommended wording:

> On this benchmark, the mass a multi-agent system places on
> non-committal labels (`p_noncommit`) is a strong predictor of
> benchmark error (AUROC 0.64–0.69), but decomposition shows this is
> specifically a **hedge-collision detector**: it identifies items where
> the system declines to commit while the reference answer is
> directional. It carries no signal for wrong-direction errors
> (AUROC ≈ 0.40–0.45 among committed predictions) and *inverts* on
> items whose reference answer is itself non-committal (AUROC 0.06–0.36),
> where hedging is usually correct.

What must **not** be claimed: that p_noncommit is a general-purpose
uncertainty→error signal, or that it beats TU/AU/EU as a *calibration*
quantity. What survives, and is genuinely informative: (i) the
error-composition result (62% of errors are hedge collisions; 29% are
wrong-direction; the split is lane-structured), (ii) the sign-flipping
interaction as evidence that the benchmark contains two distinct failure
regimes, and (iii) the deployment reading — in a setting where most
reference answers are directional, monitoring non-commitment mass is a
cheap and effective triage signal, *because* of the hedge regime, not
independently of it.

## Consequences for the earlier documents

- **EA_FULL_FINDINGS §3** ("categorical beats distributional") stands as
  a comparison of predictors, but its interpretation must be narrowed:
  p_noncommit wins because errors are mostly hedge collisions, not
  because it measures uncertainty better. TU's null/inverted behaviour is
  unchanged.
- **EB_CONTROLLED_FINDINGS §1** (p_noncommit survives FDR net of TU and
  lane) is unaffected as an estimate but should be reported *with* the
  M3 interaction, since the single-slope specification is misspecified.
- **EC_INTERVENTION_FINDINGS** is reinforced: interventions failed to move
  the signals because the hedge attractor dominates, and this
  decomposition shows that same attractor is what p_noncommit is
  measuring.

## Supplementary — gemini-3.1-pro (16 q, not pooled)

The commitment regime shows a visibly flatter profile: errors split
3 wrong-direction / 3 hedge-collision / 2 overcommitment, and
AUROC(p_noncommit → error) is only 0.594 — consistent with hedge
collisions ceasing to dominate once the model commits. n=16; indicative
only, and the natural thing the costed gemini ≥50q run would settle.
