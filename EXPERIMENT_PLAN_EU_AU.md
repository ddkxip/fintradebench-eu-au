# EXPERIMENT_PLAN_EU_AU

Replaces the old E-A/E-B (U1–U7). All runs: gemma4:latest via local Ollama
(digest in run manifest), τ=0.7 self-consistency, parallel workers, oracle
evidence unless stated. Gold responses never reach agents.

## Phasing (execution order)

- **P0 reframe** — PROJECT_REFRAME_EU_AU.md ✅
- **P1 data audit** — analysis/DATA_AUDIT.md ✅
- **P2 schemas** — 20 pilot schemas + validation; scale to 150 only after
  the design survives.
- **P3 engine** — EU/AU + transition classifier, unit tests green, no LLM
  calls.
- **P4 tiny pilot** — 6 questions (2/lane), K=5, Round 0 only: parse rate,
  schema adequacy, cost calibration.
- **P5 main pilot (= E-A′)** — all 150 (minus schema_uncertain) in
  oracle_evidence; agents: Fundamental + Trading (headline; see
  AGENT_SET_DECISION.md); K=10 F/FT, K=20 T; Rounds 0+1. Outputs:
  results/eu_au_natural_150.csv + results/eu_au_natural_150_summary.md
  with per-round TU/AU/EU (raw, Miller–Madow, normalized), G, ŷ,
  correctness, Brier, NLL, parse rates, transition class, false-consensus
  and productive-convergence rates, lane breakdowns.
- **P6 analysis (= E-B′)** — controlled models on P5 outputs: lane,
  answer_type, |Y|, company, date, K_effective, baseline entropy;
  cluster-robust/bootstrap CIs. Questions: does initial EU predict debate
  improvement; does AU predict error; ΔEU vs ΔG; lane effects on AU/EU
  net of controls (measurement-noise corrected). Output:
  analysis/eu_au_controlled_analysis.md.

## Later (gated on P5 core result existing)

- **E-C′ source-intervention pilot** (50 q per arm): remove top golden
  indicator / inject F–T conflict / horizon dial 3m↔60m. Predictions:
  removal → AU↑ (and G↓ if indicator matters); conflict → EU↑
  selectively; horizon → confidence shift or a horizon-insensitivity
  finding. Output: results/eu_au_intervention_pilot.csv +
  analysis/source_intervention_pilot.md.
- **E-D′ RAG ablation** (subset ~30 q): oracle vs rag_evidence — does
  retrieval noise load on AU or EU. Output:
  analysis/rag_vs_oracle_uncertainty.md.

## Baselines (P5 must include)

single-agent self-consistency (each agent alone), no-debate two-agent
mixture (Round 0 = this by construction), post-debate round 1, majority
vote over decodes, self-consistency entropy as scalar predictor,
verbalized probability diagnostic (secondary), judge confidence if the
integrator is enabled.

## Explicitly deferred

Uncertainty-guided routing, RL, macro agent, any U1–U7 aggregator,
source-aware policies, full intervention matrix, full RAG study.

## Compute budget

P5: 150 q × 2 agents × (K=10 F/FT | 20 T) × 2 rounds ≈ 8,000 decodes;
short label+rationale JSON outputs (~120 tokens) at ~3–5 s/decode with
4 parallel workers ≈ 3–6 h wall-clock on the local GPU. Feasible
overnight; resumable runner mandatory.
