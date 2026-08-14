# RECOMMENDED_PAPER_DIRECTION_EU_AU

Consolidated paper direction as of 2026-08. Supersedes the pre-data direction
in `PROJECT_REFRAME_EU_AU.md` / `NOVELTY_POSITIONING.md` (both still valid on
scope and threats; this doc replaces their *claim set* with what the data
actually supports). Every number below traces to a findings doc in this repo.

---

## 1. The paper in one paragraph

Multi-agent financial debate systems do not express uncertainty
*distributionally* (spread probability over answers) so much as
*categorically* (converge, with high self-consistency, on non-committal
labels like `mixed` / `conditional` / `insufficient_data`). We measure this
with an exact TU = AU + EU decomposition over schema-constrained answer
spaces plus a first-class `p_noncommit` quantity, on 139 gold-labelled
FinTradeBench questions × 4 open-weights models (+ a Gemini subset and an
independent-benchmark FinanceBench probe). The consequences: the dominant
error mode is a **hedge collision** (system hedges, reference answer is
directional; 51–67% of all errors); debate reduces within-agent instability
only where such instability exists, and otherwise polarizes; whether a model
hedges is a **model × lane** property, not a capability level; and controlled
evidence interventions fail to move the uncertainty signals at all, which
bounds how much construct validity the decomposition has in the hedging
regime.

---

## 2. Result inventory — what is established, and how strongly

Grades: **A** = multi-model + controlled/blinded + survives FDR;
**B** = multi-model descriptive; **C** = single-run / small-n, directional.

| # | Result | Evidence | Grade |
|---|---|---|---|
| R1 | **Hedge collision is the modal error mode**: 50.6–67.0% of errors across 4 models (pooled 57.2%); lane-structured (F 71%, FT 76% hedge-collision vs T 77% wrong-direction) | `noncommit_error_decomposition_allmodels.md` | **A** |
| R2 | **`p_noncommit` predicts error net of TU and lane** in both original models (q=.012/.016 under BH-FDR, ticker-clustered); AUROC 0.64–0.72 across 4 models | `EB_CONTROLLED_FINDINGS.md`, allmodels | **A** |
| R3 | **The effect is a sign-flipping interaction, not a single slope**: slope +5.12 on committed-gold vs −8.90 on non-committal-gold (interaction p=1.7e-10), pseudo-R² 0.152→0.388 (n=556) | allmodels §E | **A** |
| R4 | **Gold-commitment labels are robust to independent blinded re-annotation**: Codex vs Antigravity agreement 86.3%, Cohen κ 0.590, Fleiss κ 0.531; conclusion survives all 6 commitment versions (hedge-collision modal in 4/4 under majority vote) | `INTERANNOTATOR_FINDINGS.md` | **A** |
| R5 | **Regime is model × lane, not whole-model**: FT is the highest-hedging lane in **5/5** models; qwen3.6-27b and gemma4-31b-it independently commit on F (acc .61/.55) while hedging on FT (pNC .74/.73) | `HF_QWEN36_*`, `HF_GEMMA4_31B_*` | **B** |
| R6 | **Debate reduces AU where AU headroom exists** (p<1e-6 in 3 models; up to −0.149), **but not universally** — gemma4-31b-it (R1 AU 0.012, 77% degenerate) shows dAU n.s. and a *significant* dEU increase | `EA_FULL_*`, `HF_GEMMA4_31B_*` | **B** |
| R7 | **Debate improvement is unpredictable**: no round-0 uncertainty quantity (EU₀/AU₀/NC₀) nor any delta predicts ΔG (all p>0.34) → you cannot route debate on these signals | `EB_CONTROLLED_FINDINGS.md` Q4 | **A (null)** |
| R8 | **Controlled evidence interventions do not move the signals**: removing the top golden indicator has no selective effect vs a matched placebo; injected F/T conflict *lowers* EU (−0.041, CI excl. 0) as both agents retreat to a shared hedge; horizon dial flips 3/30 verdicts | `EC_INTERVENTION_FINDINGS.md` | **A (causal null)** |
| R9 | **Non-commitment is often correct**: gold is non-committal on 15.8% of questions, and hedging there is right 57–93% of the time — hedging is not intrinsically a failure | allmodels §D | **B** |
| R10 | ⚠ **"No wrong-direction signal" is a degeneracy artifact, not a property of `p_noncommit`** — see §3 | FinanceBench probe | **C (but decisive for framing)** |

---

## 3. The FinanceBench probe — a partial failure to generalize (must be reported)

An independent-benchmark probe (FinanceBench, oracle `evidence_text`, 37
yes/no items, qwen3:8b — the *same* model as in the FinTradeBench table, so
like-for-like; `analysis/financebench/FINANCEBENCH_YESNO_ORACLE_FINDINGS.md`)
was run as a future-work scoping exercise. It **replicates R1 and undercuts
part of R2**, and the honest version of both belongs in the paper.

**Replicates (strongly):** hedge collision = **79.2%** of errors, the highest
observed anywhere; overall AUROC(`p_noncommit`→error) = **0.955**. The
categorical-uncertainty story transfers to a different benchmark, different
question type, and different agent roles.

**Undercuts:** in FinTradeBench the *non-mechanical* committed-gold ∧
committed-prediction cell sat at chance for all four models (AUROC
0.403–0.446), which is what licensed the claim "`p_noncommit` is a pure
hedge-collision detector carrying no wrong-direction signal". On FinanceBench
that same cell gives AUROC **0.815**, and the bootstrap CI I computed for
this doc is **[0.631, 0.958] — excluding 0.5** (n=18, 5 errors; small but
significant).

The mechanism is visible in the variance, not the mean: in FinTradeBench,
committed predictions carried almost no residual hedge mass (qwen3:8b: mean
pNC 0.079, sd 0.174), so there was nothing to rank and chance-level AUROC was
**mechanically forced**. On FinanceBench the system often commits while
retaining real hedge mass (mean 0.247, sd 0.255), and that residual is
informative — wrong answers carry ~3× the hedge mass of right ones (0.490 vs
0.154).

**Required claim narrowing (adopt this wording):**

> Within the committed cell, `p_noncommit` carries wrong-direction signal
> **only when residual non-commitment mass has meaningful variance**. In the
> near-degenerate regimes typical of small open-weights models on
> FinTradeBench that variance vanishes and the signal is unavailable — which
> is why it there appeared to be a pure hedge-collision detector.

This is a better result than the original: it converts an absolute claim into
a scoped one with a stated mechanism and a boundary case on an independent
benchmark. **Do not report the original unqualified version.**

**Second FinanceBench caveat (agent design, not a law):** that run paired an
`evidence_accountant` with a deliberately insufficiency-hunting
`skeptical_auditor`. At R0 the accountant was much the better analyst
(acc 0.622, hedge 0.216) and the skeptic hedged on two-thirds of items
(acc 0.243); after one round the accountant converged *onto the skeptic*
(hedge 0.216→0.541, acc 0.622→0.324), producing 1 rescue vs 10 losses. That
is evidence about **asymmetric skeptic-augmented debate**, not a general
"debate harms accuracy" claim — FinTradeBench's two agents were symmetric
substantive analysts. A neutral-agent control is required before any
generalization, and the paper must say so.

---

## 4. Recommended framing

**Title direction:** *Categorical, not distributional: how multi-agent
financial reasoners express — and mis-express — uncertainty.*

**Contribution claim (narrowest defensible):**

> We show that multi-agent financial debate systems express uncertainty
> categorically rather than distributionally, quantify this with a
> first-class non-commitment mass alongside an exact epistemic/aleatoric
> decomposition over gold-anchored answer schemas, and demonstrate across
> four open-weights models, an independent blinded gold-commitment audit, a
> controlled intervention suite, and a second benchmark that (i) the dominant
> failure mode is hedge collision, (ii) whether a system hedges is a
> model × lane property, and (iii) the diagnostic value of non-commitment
> mass is bounded by a degeneracy condition we characterize.

**What NOT to claim** (each was tested and failed or narrowed):
- *not* "debate reduces aleatoric uncertainty" unconditionally (R6)
- *not* "`p_noncommit` is a general error predictor" (R3) nor "a pure
  hedge-collision detector with no wrong-direction signal" (R10)
- *not* "uncertainty can route debate" (R7)
- *not* that the uncertainty channels are construct-valid in the hedging
  regime (R8)
- *not* "FT questions have higher EU" (rejected in both models)

**Positioning vs. the literature** is unchanged from `NOVELTY_POSITIONING.md`
(EGAC, *Why Don't You Know?*, CAGE-CAL, FinDebate). The wedge is now sharper:
the closest work decomposes uncertainty on math reasoning; we show that in a
finance setting with *labelled* answer spaces the interesting variance is not
in the entropy decomposition at all but in **which label the system retreats
to**, and we bound when the entropy view is even measurable.

---

## 5. Table/figure plan

| slot | content | source |
|---|---|---|
| Table 1 | Controlled error-prediction (M1/M2/M3 with interaction), n=556, ticker-clustered | allmodels §E |
| Table 2 | Cross-model summary: acc, TU/AU/EU, pNC, deltas, degeneracy, AUROC splits (5 models) | `analysis/model_comparison_table.csv` |
| Table 3 | Error decomposition by model × lane (hedge collision / wrong direction / overcommitment) | allmodels §C |
| Table 4 | Inter-annotator agreement + 6-version survival | `INTERANNOTATOR_FINDINGS.md` |
| Table 5 | Intervention response matrix (do-operators × channels, incl. placebo) | `EC_INTERVENTION_FINDINGS.md` |
| Fig 1 | Model × lane regime map (pNC heatmap, 5 models × 3 lanes) | comparison table |
| Fig 2 | The interaction: error rate vs `p_noncommit`, split by gold commitment | allmodels |
| Fig 3 | Committed-cell AUROC vs residual-hedge-mass variance — **the generalization boundary**, FinTradeBench (4 pts) + FinanceBench | this doc §3 |
| Appendix | Matched-K T-lane robustness; lane OLS collinearity caveat; strict-vs-lenient scoring | `EB_CONTROLLED`, `EA_FULL` |

Fig 3 is the one to build next — it turns R10 from a caveat into a *result*
by making the degeneracy condition visible as a scatter.

---

## 6. Gaps before submission (ranked)

1. **Neutral-agent control on FinanceBench** — separates the skeptic artifact
   from a genuine debate effect. Cheapest high-value run; blocks any
   cross-benchmark debate claim.
2. **Qwen3.6-27B on FinanceBench** — the intended headline model; also gives
   a second committed-cell variance point for Fig 3.
3. **More committed-cell variance points** — the Fig-3 claim currently rests
   on 4 degenerate + 1 non-degenerate observation. Any model/benchmark combo
   with intermediate degeneracy strengthens it materially.
4. **Gemini ≥50q** — the 16-q subset is indicative only (its committed-cell
   AUROC 0.833 sits on 8 errors and should not be quoted as a result).
5. **T-lane schema revision** — both blinded annotators independently read
   multi-name screening golds as non-committal (10 questions). A set-valued
   or `none_clear` treatment would tighten the benchmark; the decomposition
   already survives either way, so this is quality, not rescue.
6. Optional: RAG arm (E-D′), still deliberately out of the headline.

---

## 7. Honest limitations to state in the paper

- Gold labels are **ex-post benchmark labels**, not market truth; correctness
  means agreement with an expert-audited conclusion given the same evidence.
- Commitment labelling is **moderately** reliable (κ≈0.53–0.59), not
  objective; we report κ and show conclusion-invariance rather than claiming
  the labels are self-evident.
- Pooled rows are **not independent** (each question appears once per model);
  per-model results are primary, pooled is descriptive, regressions cluster
  by ticker.
- EU is computed over **N=2** framework agents — a single edge, not a graph.
- The intervention suite ran on **one model** (gemma4) at n=30; its causal
  nulls are scoped to the hedging regime.
- FinanceBench probe: **n=37, one model, asymmetric agents, no
  non-committal golds** (so overcommitment is 0 by construction).
