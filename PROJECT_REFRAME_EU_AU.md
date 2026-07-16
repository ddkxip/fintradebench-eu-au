# PROJECT_REFRAME_EU_AU — from seven signals to a two-component decomposition

## What changes and why

The previous program computed seven uncertainty quantities U1–U7 and asked
how they relate. The 2026-07 audit (repo `fintradebench-uq-audit`) showed
that framing is not defensible: the seven occupy different ontological
positions (exposure, perception, state, dynamic, metric), several
correlations among them are guaranteed by shared inputs, and two live gates
produced hard negative results — G0 (verbalized probabilities are heaped and
barely carry question-level signal) and G1 (the macro agent's elicited
regime ambiguity is decoupled from real macro uncertainty, ρ=0.16 vs JLN
over 40 quarters).

The pivot: **the central objects are now TU/AU/EU** — the exact entropy
decomposition of the multi-agent system's predictive distribution over a
question-specific finite answer space, estimated by self-consistency
frequencies (not verbalized probabilities), tracked across debate rounds,
and evaluated against FinTradeBench gold labels.

For question q, agent i, round t, label y:

    p_sys(y) = (1/N) Σ_i p_i(y)          system mixture
    TU  = H(p_sys)                        total uncertainty
    AU  = (1/N) Σ_i H(p_i)                within-agent ambiguity/instability
    EU  = TU − AU  (= generalized JSD)    between-agent disagreement

This is the multi-agent analogue of the mutual-information decomposition
(EU = I(Y; agent)); it is exact, non-negative in both parts, and — unlike
U1–U7 — every quantity is defined on the same object (a labeled predictive
distribution) and is directly scoreable against the gold label.

## What each old U becomes

| Old | New status |
|---|---|
| U1 evidence gaps | **source condition / intervention dial** (evidence-pack manipulation), not a signal |
| U2 macro | **external moderator**, data-driven JLN/EPU only (G1: elicited regime entropy is dead as a world measure; retained only as a negative-result diagnostic) |
| U3 disagreement | **replaced by EU** (JSD was two-agent EU already; now generalized, schema-labeled, gold-scored) |
| U4 horizon | **exposure / experimental dial** |
| U5 calibration | **evaluation metric only** (Brier, NLL, ECE, reliability curves); never a feature |
| U6 verdict stability | secondary robustness outcome |
| U7 confidence shift | secondary debate-transition outcome (subsumed by the transition taxonomy) |

No "correlations among seven uncertainties" analysis will be run or
reported.

## What carries over from the audit (binding)

- **G0 protocol**: self-consistency frequencies are the primary
  distribution estimator; K=10 minimum headline, **K=20 for T-lane** and
  for any quantity feeding headline EU/AU; K=5 only for debugging pilots;
  lane-stratified measurement noise must be reported and corrected before
  any cross-lane comparison (T-lane single-elicitation noise was 3–4×
  F/FT on gemma4).
- **G1 decision**: macro enters analyses only as the data-driven JLN/EPU
  covariate/moderator.
- Model: `gemma4:latest` via local Ollama (digest recorded per run);
  parallel request workers to saturate the GPU.
- Oracle evidence (precomputed indicator packs replicating the benchmark's
  own generation contexts) is the headline condition; RAG is a stressor
  ablation only.
- Gold responses are visible only to the evaluator/parser, never to agents.

## The paper this aims at

*Source-conditioned epistemic/aleatoric uncertainty flow in multi-agent
financial reasoning*, evaluated against FinTradeBench gold answers under
controlled financial evidence: does debate reduce EU in a truth-aligned
way (gold-probability up) or produce false consensus (EU down, gold-
probability down), and which finance-native sources (missing indicators,
F/T conflict, horizon, macro state, staleness, retrieval noise) feed EU
versus AU. See NOVELTY_POSITIONING.md for what may and may not be claimed.
