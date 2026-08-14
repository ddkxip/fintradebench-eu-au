# FinanceBench yes/no oracle-evidence run — findings

Run `financebench_yesno_oracle_local_qwen3_8b`; model `ollama:qwen3:8b`; evidence field `evidence_text`; K=10. Oracle evidence only (no RAG, no PDF retrieval). Reanalysis script makes no model calls.

Answer space `[yes, no, insufficient_data]`; `noncommit_set = {insufficient_data}`.

## 1. Coverage and parsing

- examples: **37** (schema subset: 37)
- mean parse rate: **1.000** (min 1.000)

## 2. Accuracy and non-commitment by round

- R0: accuracy **0.595**, mean p_noncommit **0.454**
- R1: accuracy **0.351**, mean p_noncommit **0.582**
- gold distribution: {'yes': 26, 'no': 11} (majority-class baseline = 0.703)

## 3. Debate deltas R0->R1 (paired)

- dAU: mean +0.0078, Wilcoxon p=0.591 (nonzero n=14)
- dEU: mean -0.0930, Wilcoxon p=0.129 (nonzero n=20)
- dNC: mean +0.1284, Wilcoxon p=0.02 (nonzero n=20)
- dCorrect: mean -0.2432, Wilcoxon p=0.0117 (nonzero n=11)
- **debate rescues: 1; losses: 10** (stable-correct 12, stable-wrong 14)

## 4. Error decomposition (final round)

- total errors: **24** / 37 (error rate 0.649)
- **hedge_collision** (committed gold, predicted insufficient_data): **19** (79.2% of errors)
- **overcommitment** (insufficient_data gold, committed prediction): **0** (0.0% of errors)
- **wrong_direction** (yes<->no flip): **5** (20.8% of errors)

> **Structural caveat:** this subset contains **no `insufficient_data` golds**, so `overcommitment` is identically 0 by construction and every error is either a hedge collision or a wrong-direction flip. The hedge-vs-wrong-direction *split* is therefore the only informative decomposition here.

## 5. AUROC of p_noncommit for error (final round)

- AUROC(p_noncommit -> error), all: **0.955** (n=37)
- AUROC in committed-gold & committed-pred subset (non-mechanical cell): **0.815** (n=18)

## 6. Qualitative comparison to FinTradeBench

| quantity | FinanceBench yes/no (this run) | FinTradeBench (139q, 4 models) |
|---|---|---|
| non-committal golds | 0/37 (0%) | 22/139 (15.8%) |
| hedge-collision share of errors | 79.2% | 50.6%-67.0% |
| AUROC p_noncommit (all) | 0.955 | 0.636-0.721 |
| AUROC committed-cell | 0.815 | 0.403-0.446 |

Key reading: the **committed-cell AUROC** is the generalization test that matters. In FinTradeBench it sat at 0.40-0.45 (chance) for every model, supporting 'p_noncommit is a hedge-collision detector with no wrong-direction signal'. If this run reproduces a ~chance committed-cell AUROC on an independent benchmark, that claim generalizes; if it is clearly >0.55 here, the claim is benchmark-specific and must be narrowed.
---

## 7. Diagnostics — what actually drove these numbers

### 7.1 The skeptic drags a competent analyst into hedging (agent-design effect)

Per-agent behaviour, by round:

```
agent                round  mean p_noncommit  predicted-insufficient rate  accuracy
evidence_accountant    0          0.232                0.216               0.622
evidence_accountant    1          0.535                0.541               0.324
skeptical_auditor      0          0.676                0.676               0.243
skeptical_auditor      1          0.630                0.649               0.324
```

Read this carefully:

- At **round 0 the Evidence Accountant is the better analyst by far**
  (accuracy 0.622, hedge rate 0.216) while the **Skeptical Auditor hedges on
  two-thirds of items and scores 0.243**.
- After **one debate round the Accountant converges onto the Skeptic**:
  hedge rate 0.216 → 0.541, accuracy 0.622 → 0.324. The Skeptic barely
  moves. Debate transmits hedging *from* the skeptic *to* the accountant.

That is the mechanism behind the headline `1 rescue vs 10 losses`
(dCorrect −0.243, p=0.012) and `dNC +0.128` (p=0.020).

**Honest caveat — this is partly my design, not a law of nature.** I
specified `skeptical_auditor` to hunt for insufficiency, so an
insufficiency-biased debate partner is *built in*. FinTradeBench's two
agents (fundamental vs trading) were both substantive analysts with no
such asymmetry. So this run should be read as evidence about
**asymmetric skeptic-augmented debate**, not as a general claim that
"debate harms accuracy". A neutral-agent control (e.g. two evidence
accountants, or accountant vs a `bull_case` agent) is required before
any generalization. That control is the obvious next run.

### 7.2 The committed-cell AUROC gap is a VARIANCE artifact — and it partly undercuts an earlier claim

`p_noncommit` mass inside the committed-gold ∧ committed-prediction cell:

```
FinanceBench (this run, n=18):     mean 0.247, sd 0.255, range 0.000-0.500
  correct rows: mean pNC 0.154 (n=13)
  wrong   rows: mean pNC 0.490 (n=5)
FinTradeBench qwen3:8b (n=71):     mean 0.079, sd 0.174
```

In FinTradeBench, when models committed they committed **hard** — residual
hedge mass was compressed near zero, so there was almost nothing to rank
and the AUROC sat at chance *mechanically*. Here the system frequently
commits while still holding substantial hedge mass, and that residual mass
**is** informative: wrong answers carry 3× the hedge mass of right ones
(0.490 vs 0.154), giving committed-cell AUROC **0.815**.

**Consequence for the paper (must be stated, not buried):** the earlier
conclusion — *"p_noncommit is a pure hedge-collision detector carrying no
wrong-direction signal"* — was supported by chance-level committed-cell
AUROC across four FinTradeBench models. This run shows that result may be
**a degeneracy artifact rather than a property of the signal**: where
residual hedge mass has variance, it predicts wrong-direction errors well.
The claim should be narrowed to:

> Within the committed cell, `p_noncommit` carries wrong-direction signal
> **only when the system's residual non-commitment mass has meaningful
> variance**. In the near-degenerate regimes typical of small open-weights
> models on FinTradeBench, that variance vanishes and the signal is
> unavailable — which is why it looked like a pure hedge-collision
> detector there.

This is a **partial failure to generalize**, and it is a more interesting
and more accurate statement than the original.

### 7.3 The system is below the majority-class baseline

Gold split is 26 yes / 11 no, so an always-"yes" baseline scores **0.703**.
The system reaches 0.595 (R0) and 0.351 (R1) — i.e. **worse than a constant
answer**, driven by hedging into `insufficient_data` on questions whose
evidence does support a verdict. 79.2% of errors are hedge collisions.

## 8. Status and caveats

- **Model**: `qwen3:8b` (local Ollama), *not* the intended
  Qwen3.6-27B-FP8. Treat as a pipeline validation + small-model data point.
  qwen3:8b is in the FinTradeBench 4-model table, so the cross-benchmark
  comparison for that model is like-for-like.
- **n=37**, and the non-mechanical cell is only **n=18** — the 0.815 AUROC
  is a small-sample estimate and needs the 27B run (and ideally a
  bootstrap CI) before it carries weight.
- No `insufficient_data` golds exist in this subset, so `overcommitment`
  is 0 by construction (already flagged in §4).
- 100% parse rate; no decode errors.

**Required next runs, in priority order:** (1) neutral-agent control to
separate the skeptic artifact from a genuine debate effect; (2) the 27B
run on the cluster for the headline number; (3) bootstrap CI on the
committed-cell AUROC.

---

## 9. Bootstrap CI on the committed-cell AUROC (added 2026-08, reanalysis)

The §7.2 claim needed the CI flagged as missing in §8. Computed from
`results/financebench_yesno_oracle_local_qwen3_8b/rows.csv` (system rows only):

- committed-gold & committed-pred cell: **n=18, 5 errors, AUROC = 0.815**
- **bootstrap 95% CI = [0.631, 0.958]** (5,000 resamples) — **excludes 0.5**
- residual hedge mass: correct rows mean pNC 0.154, wrong rows 0.490

So the divergence from FinTradeBench's chance-level committed cell is
**statistically significant despite the small n**, not a sampling fluke. The
narrowed claim in §7.2 stands and is carried into
`RECOMMENDED_PAPER_DIRECTION_EU_AU.md` §3 as the generalization boundary.

All other numbers in this document were re-verified against the raw rows and
reproduce exactly (R0 acc 0.595, R1 0.351, 24 errors = 19 hedge collision /
5 wrong direction / 0 overcommitment, all-questions AUROC 0.955).

---

## 10. RETRACTION of the §7.2 mechanism (2026-08, reanalysis)

**§7.2 claimed the FinTradeBench-vs-FinanceBench committed-cell gap was a
*variance* artifact — that residual hedge mass predicts wrong-direction
errors when it has variance. That claim is refuted by our own data and is
withdrawn.**

Testing it directly across 14 FinTradeBench cells (4 models x their
lane-level subsets), with committed-cell AUROC against residual hedge-mass
sd:

- within FinTradeBench: Spearman **rho = -0.029, p = 0.92** (no relationship)
- all 15 cells incl. FinanceBench: rho = 0.164, p = 0.56
- aggregate-only (5 points): rho = 0.50, p = 0.39 -- driven entirely by the
  single FinanceBench point, and not significant
- direct counterexamples: qwen3:8b [FT] has sd **0.220** (vs FinanceBench's
  0.255) yet AUROC **0.222**, far *below* chance; gemma4-31b-it overall has
  sd 0.202 with AUROC 0.437
- sd and mean correlate at **0.96**, so "variance, not mean" was never a
  separable claim in the first place

Data: `analysis/fig3_committed_cell_data.csv`.

**What stands instead:** the committed-cell result differs between the two
benchmarks (FinTradeBench 0.40-0.45 across four models; FinanceBench 0.815
[0.631, 0.958]), and the cause is **unidentified** -- confounded with task
format, answer space, agent design, and n. Reported as an open question, not
a mechanism. See `paper/figures/fig3_committed_cell.py` for the figure and
`RECOMMENDED_PAPER_DIRECTION_EU_AU.md` §3.
