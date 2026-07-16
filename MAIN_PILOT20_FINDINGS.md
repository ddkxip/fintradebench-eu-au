# MAIN_PILOT20_FINDINGS — first EU/AU debate data (16 q, K=10/20, R0+R1, gemma4)

Full tables: results/main_pilot20/summary.md, transitions.csv, rows.csv.
Pilot-scale (n=16): everything below is provisional; nothing here is a
paper claim yet. But the qualitative structure is strong.

## 1. The dominant phenomenon is a *hedge-certainty regime*, not EU flow

- EU is tiny everywhere (normalized 0.01–0.09 lane means): the two
  framework agents almost never disagree systematically.
- 14/16 judgment-question rows predict a hedge label (`mixed`/
  `conditional`); on those rows accuracy is 43%. FT hedge rate: 83%.
- 19/32 rows are fully degenerate (TU = 0: every decode of both agents
  identical).
- The confusion table is diagnostic: every FT/F error is a
  hedge-collision — gold `yes` → predicted `mixed` (×2), gold
  `supportive`/`unsupportive` → predicted `conditional` (×2). When the
  gold itself is a hedge label the system is "right" (conditional golds
  2/2, mixed gold 1/1); when the gold is directional it hedges and loses.
- Consequence: **lane accuracy F 86% / T 67% / FT 33%** — FT is the
  failure locus not because of cross-signal *disagreement* (the RQ3
  hypothesis) but because directional FT golds meet a hedging model.

## 2. Debate reduces ALEATORIC uncertainty, barely touches epistemic

Paired R0→R1: AU drops in all lanes (F −0.104, FT −0.083, T −0.056
normalized; Wilcoxon p=0.18 at n=16 — direction consistent, power
absent), while EU is flat-to-slightly-up (F −0.019, FT +0.014,
T +0.028). Seeing the opponent's answer makes each agent *internally
more consistent* without moving the between-agent structure. In the
Epistemic-Gain/Aleatoric-Cost vocabulary: this debate produces
**aleatoric gain, no epistemic movement** — the inverse emphasis of the
math-reasoning finding, and a sensible candidate headline once powered.
Note two counterexamples where debate *created* uncertainty (F2, T2:
EU and/or AU rose from 0) — debate is not uniformly stabilizing.

## 3. Classic false consensus cannot occur here — and that is a finding

Transition outcomes: 10 STABLE_SUCCESS, 6 STABLE_FAILURE, **zero**
DEBATE_RESCUE, zero CORRECTNESS_LOST — debate changed no verdicts.
False-consensus rate 0, minority-suppression 0: with EU ≈ 0 at Round 0,
there is no initial diversity to collapse. The CAGE-CAL-style pathology
presupposes disagreement; this system fails *upstream* of it, by prior
consensus on hedged labels. RQ2 reframes: the finance failure mode (for
this model class) is **confident premature hedging**, not induced
convergence.

Caveat on the "persistent rational disagreement: 11" line in summary.md:
with EU mostly zero, the top-tercile threshold degenerates (~0.005), so
the flag fires on trivial EU. Analysis artifact — the flag needs an
absolute floor (e.g. EU_norm ≥ 0.1); fix before the full run.

## 4. RQ3 scorecard (provisional)

- **T-lane higher AU: SUPPORTED.** AU_norm R0: T 0.218 > F 0.137 ≈ FT
  0.123; survives Miller–Madow with T at K=20 (correction *smaller* for
  T, so the gap is not estimator bias). Consistent with G0's
  lane-structured elicitation noise.
- **FT-lane higher EU: NOT SUPPORTED** at pilot scale — FT EU is the
  lowest at R0 (0.019). The cross-signal conflict hypothesis is
  preempted by hedge collapse. Possibla rescue: EU may only appear with
  (a) directional-forced label menus, or (b) stronger models that
  actually take positions. Both are cheap probes.

## 5. What this changes in the plan

1. **Hedge-attractor probe is promoted to the next experiment** (before
   scaling schemas): rerun the 10 judgment questions with directional
   labels only (`conditional`/`mixed` removed; `insufficient_data`
   kept), same K — does EU appear? does FT accuracy move? Also rerun
   with an explicit "hedge labels require decisive-evidence
   justification" instruction as arm 2.
2. Second-model check (qwen3:8b) on the same 16 — is hedge-certainty a
   gemma4 property or an open-weights property? (If a stronger model
   shows real EU, the paper gains a model-capability axis.)
3. Transition classifier: add absolute EU floor to the PRD flag.
4. FT2/FT10-style grading strictness: the manual-review pass on flagged
   medium schemas is now mandatory before the full run (2 of 6 FT
   "errors" are defensible-alternative-label cases).
5. Full-150 scale-up proceeds as planned after the probes; power for the
   AU-drop and lane-AU claims needs the full set (current p≈0.18 at
   n=16 → n≈115–130 gives ~3x the paired power).

## 6. Engineering

~9,300 s for 720 decodes ≈ 13 s/decode (better than the 21 s pilot
estimate; shorter contexts on judgment questions). Full E-A′ at ~6.5k
decodes ≈ 24 GPU-hours → two overnights, or one with
OLLAMA_NUM_PARALLEL=2 (test context-memory fit first). Parse rates:
mean 99.3%, min 87.5% (one T screening agent-round) — the strict-JSON
contract holds at K=20.
