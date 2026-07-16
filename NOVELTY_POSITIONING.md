# NOVELTY_POSITIONING

## Claims we may NOT make

Not the first: uncertainty decomposition in multi-agent debate; epistemic/
aleatoric decomposition for LLMs; source-conditioned UQ evaluation;
financial debate system; financial reasoning benchmark; false-consensus
finding; self-consistency/semantic-entropy UQ.

## The claim we aim for (exact wording)

> "We present the first source-conditioned epistemic/aleatoric
> uncertainty-flow study in multi-agent **financial** reasoning, evaluated
> against FinTradeBench gold answers under controlled financial evidence.
> We adapt debate-level uncertainty decomposition to a domain where
> uncertainty sources are not generic but structured — fundamentals,
> trading signals, cross-signal conflict, horizon, macro state, evidence
> staleness, retrieval noise — and test whether debate reduces epistemic
> uncertainty in a truth-aligned way or manufactures false consensus."

## Threat table

| Threat | What it already does | What it kills | What survives | Allowed wording |
|---|---|---|---|---|
| Epistemic Gain, Aleatoric Cost (arXiv:2603.01221) | EU/AU decomposition of debate on math reasoning; RL to raise epistemic gain | "first EU/AU in debate"; the bare decomposition as contribution | finance domain; named-framework agents (EU = F-vs-T dispute); gold-label alignment (G, Brier, transitions); source conditioning; oracle-evidence control | "following [EGAC], we decompose…; unlike math settings, our agents are analytical frameworks and our sources are domain-structured" |
| Why Don't You Know? (arXiv:2604.10495) | source-labeled dataset; shows UQ methods degrade off their home source (single model) | "first source-aware UQ evaluation" | multi-agent EU/AU response to *financial* sources via controlled evidence edits; expert golden-indicator basis for interventions | "extending source-conditioned evaluation to multi-agent finance" |
| CAGE-CAL (arXiv:2605.30653) + Not-All-Flips (arXiv:2606.00820) | false consensus, communication-induced correlation, conformity typing, interventions | false consensus / minority suppression as findings | the *rates conditional on finance sources and lanes*; EU-flow (distribution-level) rather than flip-level typing; gold-probability trajectory G | "we replicate the false-consensus phenomenon and characterize its finance-conditional structure" |
| FinDebate (arXiv:2509.17395) | role-specialized finance debate + RAG, calibrated-confidence claims (LLM/human eval) | "novel financial debate architecture" | quantitative EU/AU measurement layer; benchmark-gold scoring; controlled evidence | "unlike systems work, we measure" |
| TradingAgents (arXiv:2412.20138) / MarketSenseAI | trading-firm MAS; portfolio-level live validation | any systems/returns claim | question-level uncertainty science | cite as landscape |
| FinTradeBench (arXiv:2603.19225, ours) | the benchmark, golds, indicators, RAG eval | "new benchmark" claims | benchmark *reuse for UQ*: schemas, label spaces, gold-aligned uncertainty — a new capability layer | "we equip FinTradeBench with canonical answer schemas enabling distribution-level scoring" |
| Semantic entropy / self-consistency UQ (Kuhn/Farquhar; Wang) | single-model UQ machinery | novelty of frequency-based distributions | they are our estimators and baselines, not competitors | cite as baselines B1/B6 |
| Sequential Consensus / ARMOR-MAD / DebUnc | uncertainty-gated debate control | any routing claim (deferred anyway) | n/a in this paper | future-work sentence only |

## Vulnerabilities to manage

1. Single benchmark, single domain → framed as depth, plus 2nd-model
   replication of headline cells.
2. Gold labels are ex-post benchmark labels, not market truth → say so
   explicitly; correctness = agreement with expert-audited benchmark
   conclusion given the same evidence.
3. N=2 agents → EU is two-framework JSD; sensitivity appendix with N=3.
4. gemma4-only headline → replicate headline table on qwen3:8b or
   gemini-3.1-pro subset before submission.
5. Re-run this threat search before submission; the subfield moves weekly.
