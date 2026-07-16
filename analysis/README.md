# analysis/

Audit + analysis scripts and their reports.

- `phase1_data_audit.py` → `DATA_AUDIT.md` — golden-seed CSV audit
- `schema_pilot_excerpts.json` — gold final-answer excerpts used to derive
  the 20 pilot schemas (evaluator-side only; agents never see these)
- `eu_au_controlled_analysis.md` — E-B′ (after the main run)
- `source_intervention_pilot.md` — E-C′
- `rag_vs_oracle_uncertainty.md` — E-D′

Statistical rules: STATISTICAL_ANALYSIS_PLAN_EU_AU.md at repo root.
No analysis treats rows as IID; cluster by ticker/date; lane comparisons
must apply the G0 measurement-noise corrections.
