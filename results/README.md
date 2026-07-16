# results/

Run outputs. One subfolder per run_id; manifests in `manifests/`
(model digest, K, τ, seeds, git commit, question-set hash,
evidence_mode). Raw decode JSONL under `raw/<run_id>/`.

Headline files:
- `eu_au_natural_150.csv` — E-A′ per question × round metrics
- `eu_au_natural_150_summary.md`
- `eu_au_intervention_pilot.csv` — E-C′
- `pilot_6q/` — Phase-4 debugging pilot (K=5; never cite in the paper)

Column dictionary lives next to each CSV as `<name>.columns.md`.
Every row has `evidence_mode` ∈ {oracle_evidence, rag_evidence,
intervention}. Headline analyses filter oracle_evidence only.
