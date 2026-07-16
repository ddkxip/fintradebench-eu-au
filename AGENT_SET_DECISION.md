# AGENT_SET_DECISION

**Headline EU/AU is computed over exactly 2 agents: Fundamental and
Trading-Signal.** The Integrator/Judge synthesizes a final answer but is
NOT in the EU/AU mixture. Reasons:

1. **Comparability.** EU = generalized JSD is only meaningful over agents
   answering the *same question from the same evidence with different
   analytical priors*. The Integrator conditions on the debaters' outputs
   — including it mixes levels (its "disagreement" with debaters is not
   framework disagreement).
2. **Domain semantics.** With N=2 named frameworks, EU has a direct
   reading: what fundamentals and price action irreducibly dispute. This
   is the finance-native wedge over generic-agent decompositions.
3. **G0 economics.** Every added agent multiplies K decodes. Two agents at
   K=10/20 already cost ~8k decodes for P5; a third adds 50%.
4. **Lane-role protocol** (prompted, not enforced): F questions —
   Fundamental primary, Trading opines with a relevance caveat; T —
   reversed; FT — both full-strength. Both agents ALWAYS emit a label over
   the full answer space, so distributions stay comparable.

Integrator (optional in P5, on by default in analysis-only mode): consumes
both agents' round-1 rationales, emits its own label distribution (K
decodes) — reported as a *baseline/diagnostic* (judge-vs-mixture
agreement, judge confidence), never inside headline EU.

Skeptic and Macro agents: deferred (DO-NOT-DO-YET list). Macro enters only
as the data-driven JLN/EPU covariate.

Sensitivity appendix planned: EU recomputed with Integrator included
(N=3) on a subset, to show conclusions don't hinge on N=2.
