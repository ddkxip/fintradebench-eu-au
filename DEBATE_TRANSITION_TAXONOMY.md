# DEBATE_TRANSITION_TAXONOMY

Classification of each question's Round-0 → final-round trajectory.
Implemented in src/transitions.py; thresholds are explicit constants with
a sensitivity sweep in the stats plan. ε_EU, ε_AU, ε_G are minimum
material changes (default: 0.05 nats for EU/AU on normalized scale; 0.05
for G), below which a quantity counts as "unchanged" — this prevents
classifying bootstrap noise as transitions.

Ordered rules (first match wins within each family):

**Outcome family (exclusive):**
- DEBATE_RESCUE: Correct_0 = 0 and Correct_final = 1.
- CORRECTNESS_LOST: Correct_0 = 1 and Correct_final = 0.
- STABLE_SUCCESS: correct at both.
- STABLE_FAILURE: wrong at both.

**Uncertainty-flow family (exclusive, requires material change):**
- PRODUCTIVE_CONVERGENCE: ΔEU ≤ −ε_EU and ΔG ≥ +ε_G.
- FALSE_CONSENSUS: ΔEU ≤ −ε_EU and (ΔG ≤ −ε_G or Correct_final = 0 with
  Correct_0 = 1).
- ALEATORIC_DESTABILIZATION: ΔAU ≥ +ε_AU and ΔG ≤ −ε_G.
- NOISE_REDUCTION: ΔAU ≤ −ε_AU and ΔG ≥ +ε_G.
- NO_MATERIAL_CHANGE: all deltas inside ε.
- MIXED_FLOW: anything else (recorded with its delta signs).

**Standing-pattern flags (non-exclusive booleans):**
- PERSISTENT_RATIONAL_DISAGREEMENT: EU_final ≥ high-EU threshold (top
  tercile) AND max_i p_{i,final}(y*) ≥ 0.5 — someone is right and dissent
  survives.
- CORRECT_MINORITY_SUPPRESSION: max_i p_{i,0}(y*) ≥ 0.5 while
  p_sys,0(y*) < 0.5, and ΔG ≤ −ε_G — an initially-right agent loses the
  system.

Every row stores: outcome class, flow class, both flags, all deltas, and
the ε values used. Rates by lane are headline numbers of E-A′.

Notes: with N=2 and one revision round, "minority" = one agent;
suppression is agent-level, not population-level. The taxonomy
deliberately mirrors the generic phenomena documented in
arXiv:2606.00820/CAGE-CAL so our rates are comparable to theirs — the
contribution is the *finance- and source-conditional structure* of the
rates, not the taxonomy's existence.
