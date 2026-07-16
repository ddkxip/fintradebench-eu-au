# THREE_MODEL_FINDINGS — capability transforms the attractor; it does not fix accuracy

Shared 16 questions, R0+R1: gemma4 (K=10/20), qwen3:8b (K=10/20),
gemini-3.1-pro-preview (K=10, Vertex). Tables:
results/three_model_comparison.md. n=16 — directions, not powered claims.

## 1. Capability *reduces* categorical hedging but does not eliminate it

Non-committal predictions on judgment questions: gemma4 **100%**,
qwen3:8b 75%, gemini **50–62%**. Gemini actually answers `yes` on F1/F11
and takes directional positions (FT25 `unsupportive`) where local models
hedge. The attractor is capability-graded, not binary.

## 2. EU finally exists — commitment is its precondition

Gemini's round-1 EU_norm = **0.114, ~3× the local floor (0.03)**, with
judgment-question AU collapsing to ~0 while EU rises. Debate deltas:
gemini dEU **+0.067** vs +0.002/+0.004 local. Mechanism: when agents
actually commit to directional labels, the fundamental-vs-trading
frameworks *visibly disagree* — epistemic uncertainty in this system is
gated on the model being willing to take positions. The p_noncommit
column (now first-class) captures the mass that used to hide this.

## 3. But benchmark accuracy does NOT improve: 0.50–0.56 vs 0.625–0.688 local

The per-question table shows the error *transformation*:
- Gemini wins where hedging was the failure: F11 (`yes` vs local hedges),
  T2 (`INTC` — the gold's numeric momentum ranking — where locals picked
  wrong tickers), FT12.
- Gemini loses in three NEW ways local models didn't:
  1. **Inverse hedge-collision**: F1 gold is `mixed` — gemini commits
     `yes` and loses where the locals' hedge was accidentally right.
  2. **Evidence-caution abstention**: F31 — gemini answers
     `insufficient_data` (Walmart data genuinely missing) while the gold
     picks COST from the available pair. Arguably *more* epistemically
     virtuous than the gold; scored wrong.
  3. **Genuine directional disagreement with the gold**: F2 (MSFT vs
     GOOGL), F44 (claim_false — contrarian on the reinvestment claim),
     FT25, T10 (NVDA vs AAPL — both in the gold's top-3; lenient scoring
     would credit it).

## 4. The one universal: debate reduces aleatoric uncertainty in ALL three models

dAU: gemini −0.128, gemma4 −0.087, qwen −0.041 (dG mildly positive in
all three). *Debate as self-consistency amplifier* is now a three-model
regularity — the most replicated effect in the program.

## 5. What this does to the paper story

The clean two-regime narrative:

- **Hedge-certainty regime (small open-weights):** consensus forms
  pre-debate on non-committal labels; EU ≈ 0; errors are
  hedge-collisions with directional golds; classic false consensus is
  structurally pre-empted.
- **Commitment regime (capable model):** hedging halves; EU emerges
  (framework disagreement becomes measurable); debate *polarizes* rather
  than only stabilizes (dEU > 0); errors become directional
  disagreements with the gold and evidence-caution abstentions —
  accuracy does not rise.

Plus the universal AU-reduction law across regimes. This is a richer and
more defensible contribution than either "attractor" or "capability
fixes it" alone — and it surfaces a benchmark-side insight: several
gemini "errors" are epistemically defensible readings (F31 abstention;
T10 within-gold-set pick), so the full analysis must report
**lenient (alias-credited) scoring alongside strict scoring** and the
gold-disagreement cell separately.

## Caveats and follow-ups

n=16, K=10 for gemini; single Vertex run (~24 min, 100% parse). The
running full-150 local runs give the powered versions of regimes 1 and
the AU law; a gemini full-150 (or ≥50-question) run is the costed
follow-up if the two-regime story headlines. Lenient scoring and the
strict/lenient gap are already computable from stored aliases —
scheduled for the E-B′ analysis.
