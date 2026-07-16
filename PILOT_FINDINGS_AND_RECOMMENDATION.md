# PILOT_FINDINGS_AND_RECOMMENDATION (Phase 0–4 complete; Phase 5 running)

State at writing: docs + engine (9/9 tests) + 20 validated schemas +
evidence adapter (100% golden-token coverage over all 150 questions) +
parser + runner built; Phase-4 pilot (6 q, K=5, R0, gemma4) complete;
Phase-5 main pilot (16 headline-eligible schemas, K=10 F/FT / 20 T,
Rounds 0+1, ~760 decodes) running in background
(results/main_pilot20/rows.csv, resumable).

## 1. Recommendation: **CONTINUE** (pivot is executing, not just planned)

The EU/AU reframe survives contact with the data and the machinery. No
kill triggers fired. Two genuine risks surfaced (T-lane schema coverage;
hedge-label attractor) — both are manageable and both are *findings*, not
blockers.

## 2. Does the 150-question golden subset support the EU/AU paper?

**Yes, with a quantified carve-out.** F and FT reduce completely to
finite label spaces (13/13 in the pilot sample). T-lane is structurally
split: judgment/ranked-screening T questions reduce (3/7), but
unordered-set and degenerate golds do not (4/7). Projected headline set:
~115–130 of 150. The excluded T items get a set-valued scoring extension
later (documented, not smuggled in). Evidence packs replicate the
benchmark's own generation contexts exactly (same date parser, same
context builder) with complete indicator coverage — the "conditional on
the same evidence" claim is real.

## 3. Are finite answer schemas viable?

**Yes.** 16/20 pilot schemas headline-eligible; every gold_label backed
by a verbatim gold quote; validator + tests enforce the invariants;
`insufficient_data` as a first-class (sometimes correct!) label works —
F25's gold is exactly that. Parse compliance is a solved problem:
**100% (60/60)** strict-JSON parses in the pilot.

## 4. Does T-lane have higher AU? (provisional)

Directionally consistent at pilot scale (T rows AU_norm 0.43/0.19 vs
FT 0.00/0.00; F 0.24/0.36) AND consistent with the prior G0 finding
(T-lane elicitation noise 3–4× F/FT at the single-decode level) — but
n=6 at K=5 is debugging data. The main pilot (K=10/20, both rounds)
gives the first citable estimate; the full-150 run decides.

## 5. Does FT have higher EU? (provisional — early evidence AGAINST)

The pilot's most interesting result cuts the other way: on both FT
questions, **both agents collapsed to the same hedged label on all
decodes** (TU=AU=EU=0 exactly) — and were wrong per gold. A
**hedge-label attractor**: gemma4 gravitates to `conditional`/`mixed`
with false certainty, erasing the cross-signal disagreement FT was
hypothesized to produce. If this replicates, the finding is *"middle
labels absorb RLHF hedging and destroy the EU signal on hybrid
questions"* — a better paper claim than the original hypothesis, with a
clean fix to test (hedge-label justification requirements; or scoring
judgment questions on the directional sublabels). Watch: FT2's gold is
`unsupportive` while `conditional` was flagged defensible in its
ambiguity notes — part of this cell is schema-grading strictness, and the
manual-review pass exists for exactly these items.

## 6. Truth-aligned convergence vs false consensus?

Unanswerable at Round-0-only pilot scale. The main pilot's Round-0→1
transitions produce the first taxonomy rates tonight. Machinery is
tested (false-consensus and productive-convergence classifiers have
green unit tests).

## 7. Should RAG be in the first paper?

**No — E-D′ ablation only, and only after the oracle-evidence core
result exists.** Rationale unchanged (retrieval confound); pilot adds a
practical reason: at 21 s/decode, oracle-mode compute is already the
binding constraint; RAG doubles context length and cost.

## 8. Exact next experiments (order)

1. Finish main_pilot20 (running): first EU/AU-by-round, transition
   rates, hedge-attractor check at K=10/20.
2. Scale schemas 20→150 (F → FT → T), second human pass on flagged
   medium schemas (F1, FT2, FT10 pattern), then full E-A′ (~115–130
   eligible questions, ~6–8k decodes, overnight × 2).
3. E-B′ controlled analysis per STATISTICAL_ANALYSIS_PLAN_EU_AU.md.
4. Hedge-attractor probe (cheap, high value): rerun the FT judgment
   questions with directional-forced labels (supportive/unsupportive
   only, conditional disallowed) to test whether the attractor is
   label-menu-induced — this doubles as the first controlled
   intervention on the label space.
5. E-C′ interventions (remove top indicator / F-T conflict / horizon)
   on 50 q each.
6. Second-model replication subset (qwen3:8b) of the headline table.

## 9. Engineering facts for planning

21.1 s/decode wall-clock on gemma4 (Ollama serializes; client
parallelism doesn't help — consider OLLAMA_NUM_PARALLEL for the full
run). Full E-A′ ≈ 6–8k decodes ≈ 35–45 GPU-hours at current settings →
either 2 overnights, shorter rationales (test impact first), or
OLLAMA_NUM_PARALLEL=2 with the 4096-token context budget checked.
