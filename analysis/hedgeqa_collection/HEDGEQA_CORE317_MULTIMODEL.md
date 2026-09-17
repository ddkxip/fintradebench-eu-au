# HedgeQA-Core 317 — seven-model results (FINAL)

Queue `core317` finished 2026-09-14 07:15 UTC with every model `DONE`. Five
interim versions of this document were published as models landed; **three
claims made in them were broken by a later model** and are corrected in place
below (§1.2, §2, §4; summarised in §5). Two early observations did survive to
seven models unchanged in shape — the FinTradeBench decline concentration and
the masked-decline nesting — which is part of why they are the most trusted
results here.

```bash
python analysis/hedgeqa_collection/compare_core_runs.py --runs \
  hedgeqa_core317_gemma3_4b,hedgeqa_core317_qwen3_8b,hedgeqa_core317_gemma4_latest,hedgeqa_core317_gemma4_31b-it-q8_0,hedgeqa_core317_qwen3_6_27b-q8_0,hedgeqa_core317_qwen3_6_35b-a3b-q8_0,hedgeqa_core317_llama3_3_70b
python analysis/hedgeqa_collection/analyze_core_mechanisms.py   # sections 1.1, 1.2 and 4
```

## Provenance

| model | where | digest | wall time | scored | note |
|---|---|---|---|---|---|
| gemma3:4b | laptop | a2af6cc3eb7f | 6.9 h | 316 | 1 lost to label surface form |
| qwen3:8b | workstation | 500a1f067a9f | 1.4 h | 317 | **same weights as the paper's qwen3:8b** |
| gemma4:latest | workstation | c6eb396dbd59 | 1.7 h | 317 | **same weights as the paper's gemma4** |
| gemma4:31b-it-q8_0 | workstation | 53dd8459790f | 8.9 h | 317 | closest Ollama match to the paper's gemma4-31b-it |
| qwen3.6:27b-q8_0 | workstation | cd0210c667bf | 8.2 h | 317 | closest Ollama match to the paper's Qwen3.6-27B-FP8 |
| qwen3.6:35b-a3b-q8_0 | workstation | 0218f872e86b | 2.1 h | 317 | MoE, ~3B active |
| llama3.3:70b | workstation | a6eb4748fd29 | 11.6 h | **316** | 1 malformed item, see below |
| ~~gpt-oss:120b~~ | — | a951a23b46a1 | — | — | **excluded**: empty content on 73/80 probe calls under format=json + think=false; it cannot disable reasoning, so including it would change the condition |

All runs: strict 317, K=10, rounds 0+1, τ=0.7. Every workstation model passed
`probe_models.py` (parse rate, output truncation, empty content, prompt fits
context) before its full run; every digest matches the one recorded at probe
time; zero total-parse failures on every workstation run.

**Comparisons are paired over the 315 items all seven runs scored.** Numbers
for the first five models differ slightly from the interim documents, which
paired over 316.

### The llama3.3:70b item, and why the ledger said 317

On `hqa_FTB_8315fbdd` one agent parsed nothing in round 0 (parse rate 0.25),
so that round has no decomposition. The runner appended rows **by position,
without a header**, so every value after `parse_rate` slid under the wrong
column name: round 1 held `"True"` under `tu` and `"0.0"` under `correct`.
`bool("0.0")` is `True` in Python, so **a naive loader would have scored that
row as a correct answer**; it was caught only because `tu` failed to parse and
crashed the comparison.

The queue counted any item with a row as scored, hence 317. Fixed at all three
levels: analyzers now validate rows and print what they exclude
(`load_valid_rows`); the runner appends by column name and records
`partial_decomposition` items; the queue counts valid items only. A scan of
all seven runs on four independent checks found this to be the only malformed
item. The raw file is left untouched as evidence.

---

## 0. Headline table (315 paired items)

| | gemma3:4b | qwen3:8b | gemma4:latest | gemma4:31b | qwen3.6:27b | qwen3.6:35b | llama3.3:70b |
|---|---|---|---|---|---|---|---|
| natural accuracy | 56.0% | 67.2% | 62.7% | 73.5% | 70.9% | **74.3%** | 71.6% |
| **masked decline rate** | 17.0% | 63.8% | 78.7% | **89.4%** | 83.0% | 78.7% | 78.7% |
| natural items declined | 19.0% | 16.4% | **28.4%** | 15.3% | 14.2% | 17.5% | 19.4% |
| zero-entropy cells | 81.0% | 84.8% | 81.3% | **91.4%** | 78.4% | 69.2% | 89.8% |
| committed errors | 118 | 71 | 47 | 42 | 53 | 42 | 45 |
| … of which zero-entropy | 82 | 48 | 26 | 33 | 26 | 19 | 34 |
| debate rescued / lost | 24 / 6 | 25 / 9 | 32 / 9 | 11 / 7 | **7 / 9** | 21 / 8 | 11 / 6 |
| accuracy r0 → r1 | 44.4→50.2% | 61.6→66.7% | 57.8→65.1% | 74.6→75.9% | 73.3→72.7% | 70.8→74.9% | 71.1→72.7% |

Masked-item accuracy is a **decline rate**: every masked gold is
`insufficient_data`, so a model that always declined would score 100%.

---

## 1. Headline: entropy misses between 45% and 79% of committed errors, on every model

The operator's question is: *the model just committed to an answer — can I
tell it is wrong?* Across seven models the answer is **mostly no**.

| model | committed errors | invisible (zero entropy) | share |
|---|---|---|---|
| qwen3.6:35b | 42 | 19 | **45%** |
| qwen3.6:27b | 53 | 26 | 49% |
| gemma4:latest | 47 | 26 | 55% |
| qwen3:8b | 71 | 48 | 68% |
| gemma3:4b | 118 | 82 | 69% |
| llama3.3:70b | 45 | 34 | 76% |
| gemma4:31b | 42 | 33 | **79%** |

An *invisible* error is a committed wrong answer where every decode from both
agents agreed: TU is exactly zero, so no threshold on entropy can flag it. The
best model tested leaves 45% of its errors in that cell, and the largest
dense models leave three quarters.

### 1.1 Why AUC is the wrong summary here

AUC(TU) for error, committed predictions only:

| model | AUC | 95% CI | vs gemma3:4b (paired) |
|---|---|---|---|
| gemma3:4b | 0.599 | [0.551, 0.648] | — |
| qwen3:8b | 0.603 | [0.544, 0.664] | +0.004 [−0.070, +0.082] n.s. |
| gemma4:latest | 0.666 | [0.589, 0.744] | +0.067 [−0.020, +0.156] n.s. |
| **gemma4:31b** | **0.571** | [0.508, 0.639] | −0.028 [−0.103, +0.054] n.s. |
| qwen3.6:27b | 0.712 | [0.640, 0.785] | **+0.113 [+0.030, +0.194]** |
| qwen3.6:35b | 0.708 | [0.623, 0.791] | **+0.109 [+0.017, +0.196]** |
| **llama3.3:70b** | **0.574** | [0.509, 0.644] | −0.025 [−0.104, +0.060] n.s. |

A tie test shows what the AUC is actually measuring. Splitting committed
predictions by whether entropy is zero:

| model | zero-entropy: error rate | non-zero: error rate | AUC(TU) *within* non-zero (n) |
|---|---|---|---|
| gemma3:4b | 40.2% | 69.2% | 0.624 (52) |
| qwen3:8b | 24.0% | 56.1% | **0.335** (41) |
| gemma4:latest | 16.0% | 52.5% | 0.570 (40) |
| gemma4:31b | 15.9% | 37.5% | 0.700 (24) |
| qwen3.6:27b | 13.4% | 61.4% | 0.575 (44) |
| qwen3.6:35b | 10.9% | 40.4% | 0.747 (57) |
| llama3.3:70b | 17.2% | 39.3% | 0.463 (28) |

**Entropy works as a binary flag, not a graded score.** On every model, any
disagreement at all raises the error rate 1.7–4.6×. But once entropy is non-zero,
its magnitude carries little further information: within-bucket AUCs scatter
from 0.335 (inverted) to 0.747 on 24–57 rows each, with no consistent
direction. The overall AUC is therefore mostly determined by **how a model's
errors split between the zero and non-zero buckets** — which is exactly the
invisible-error share above. That is why §1 reports the share, and why AUC is
kept as a secondary statistic.

This is largely mechanical, and it is stated as mechanism rather than as a
discovered trend: a model whose committed answers are ~90% zero-entropy has
most of its errors tied at zero, and no ranking statistic can separate tied
cases. No correlation is fitted across the seven aggregate points — the
project has already retracted one mechanism fitted that way.

### 1.2 Size does not help; one model generation does

| comparison | paired ΔAUC | 95% CI | |
|---|---|---|---|
| gemma4:31b − gemma4:latest (size, same family) | **−0.095** | [−0.192, +0.002] | n.s., wrong direction |
| qwen3.6:27b − qwen3:8b (size **and** generation) | +0.109 | [+0.023, +0.189] | distinguishable |

**CORRECTION kept visible:** the 2-model version read the first qwen3.6
result as "the signal improves with capability". With seven models, the two
largest dense models have the two lowest AUCs, the within-gemma size increase
points the wrong way, and the only models distinguishable from the 4B baseline
are the two qwen3.6 models — one dense 27B, one ~3B-active MoE, 0.004 apart.
Generation, not parameter count.

This agrees with the FinTradeBench paper, where gemma4-31b-it had 77%
degenerate rows and no AU headroom; here it has the highest zero-entropy share
of any model (91.4%).

---

## 2. Declining where evidence is missing

| | masked declined (correct) | natural declined | FinTradeBench declined |
|---|---|---|---|
| gemma3:4b | 17.0% | 19.0% | 52.6% |
| qwen3:8b | 63.8% | 16.4% | 42.1% |
| gemma4:latest | 78.7% | **28.4%** | **73.7%** |
| **gemma4:31b** | **89.4%** | 15.3% | 37.9% |
| qwen3.6:27b | 83.0% | 14.2% | 35.8% |
| qwen3.6:35b | 78.7% | 17.5% | 47.4% |
| llama3.3:70b | 78.7% | 19.4% | 47.4% |

**This is where capability clearly helps.** Masked declining rises from 17%
(4B) to 64–89% for every larger model, while natural-item declining stays in a
14–19% band for six of seven.

**CORRECTION kept visible (two rounds):**

- The 2-model version said capability "relocates declining rather than
  increasing it". gemma4:latest broke that, reaching a high masked rate while
  declining more everywhere.
- The 3–5-model versions then attributed that *cautious* profile to the gemma
  family and to its hedge-certainty regime. **gemma4:31b breaks that**: it has
  the highest masked decline rate of all seven (89.4%) with *low* natural and
  FinTradeBench declining (15.3%, 37.9%). The cautious profile belongs to
  **gemma4:latest specifically**, the smaller model — consistent with the
  paper, where gemma4-31b-it had the lowest hedge-collision share of its
  cohort.

The honest summary is one outlier and one regularity: gemma4:latest over-
declines; every other model above 4B declines on masked items without
declining much elsewhere.

**Nesting.** Every masked item gemma3:4b declined, all six larger models also
declined (0 gemma3-only in every pair). At the top, gemma4:31b's declines
contain those of qwen3.6:27b, qwen3.6:35b and llama3.3:70b (0 items declined by
any of them that gemma4:31b did not). That is the pattern expected if
declining tracks a real property of the evidence detected with varying
reliability — not models declining at random.

## 3. FinTradeBench draws declining on 7 of 7 models

| source | gemma3:4b | qwen3:8b | gemma4:latest | gemma4:31b | qwen3.6:27b | qwen3.6:35b | llama3.3:70b |
|---|---|---|---|---|---|---|---|
| convfinqa | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| financebench | 0.0% | 5.6% | 2.8% | 5.6% | 5.6% | 0.0% | 11.1% |
| finqa | 2.1% | 2.1% | 2.1% | 2.1% | 2.1% | 2.1% | 2.1% |
| tatqa | 0.0% | 2.0% | 8.0% | 4.0% | 2.0% | 2.0% | 4.0% |
| **fintradebench** | **52.6%** | **42.1%** | **73.7%** | **37.9%** | **35.8%** | **47.4%** | **47.4%** |

The most stable regularity in the data: FinTradeBench draws 36–74% declining
on every model, and no other source exceeds 11% on any model. **Any pooled
decline rate from this collection mostly reports how much FinTradeBench it
contains** and must be quoted per source. It is a property of the source, not
of particular items (the 2-model comparison found only 21 of 38/32 hedge
collisions shared).

This matches the FinTradeBench paper's finding that its FT lane is the
highest-hedging lane on 5 of 5 models.

## 4. Debate

| model | r0 accuracy | FinTradeBench (95): rescued / lost, net | other sources (220): rescued / lost, net | overall |
|---|---|---|---|---|
| gemma3:4b | 44.4% | 7 / 1, +6 | 17 / 5, **+12** | +5.7 pts |
| gemma4:latest | 57.8% | 2 / 2, 0 | 30 / 7, **+23** | +7.3 pts |
| qwen3:8b | 61.6% | 8 / 7, +1 | 17 / 2, **+15** | +5.1 pts |
| qwen3.6:35b | 70.8% | 9 / 4, +5 | 12 / 4, +8 | +4.1 pts |
| llama3.3:70b | 71.1% | 6 / 5, +1 | 5 / 1, +4 | +1.6 pts |
| qwen3.6:27b | 73.3% | 1 / 6, **−5** | 6 / 3, +3 | **−0.6 pts** |
| gemma4:31b | 74.6% | 8 / 3, +5 | 3 / 4, **−1** | +1.3 pts |

Mean `p_noncommit` is unmoved by debate on every model: it changes answers
without changing stated confidence.

**CORRECTION kept visible:** the 4–5-model versions concluded that debate is
"reliably positive on computable filing questions and zero-to-negative on
FinTradeBench". Seven models do not support that. gemma4:31b is net
**negative** on the other sources (−1) and +5 on FinTradeBench; qwen3.6:35b is
also +5 there.

**What the seven models do show is a headroom pattern.** The three models that
start below 62% accuracy gain +12 to +23 items on the other sources and +5.1
to +7.3 points overall. The four that start above 70% move −5 to +8 items on
any source and −0.6 to +4.1 points overall. Debate helps a lot where there is a lot
to fix and little where there is not. This is a pattern across seven points,
not a fitted relationship, and it is confounded with model size.

### Relation to the FinTradeBench paper

- **qwen3:8b** (same weights): the paper had debate net-harmful on FinTradeBench
  (4 rescued / 8 lost). Here it is flat on FinTradeBench items (8 / 7) and
  positive elsewhere. Consistent in direction, not magnitude.
- **Qwen3.6-27B**: the paper's FP8 run was mildly positive on FinTradeBench
  (6 / 4). The q8_0 build here is net negative on FinTradeBench items (1 / 6).
  Opposite direction; small counts; quantization, serving stack and item set
  all differ at once. **Unreconciled.**
- **gemma4-31b-it**: the paper's run had the only >3:1 rescue ledger (7 / 2).
  Here 11 / 7. Weaker, same sign.

---

## 5. What the data support, and what they do not

**Supported, on seven models:**

1. Entropy leaves 45–79% of committed errors invisible, on every model tested.
2. Entropy acts as a binary disagreement flag (any disagreement raises the
   error rate 1.7–4.6×); its magnitude adds little.
3. Model size does not improve the uncertainty signal; the qwen3.6 generation
   does, modestly (AUC +0.11 over the 4B baseline).
4. Every model above 4B declines on most evidence-masked items (64–89%) without
   declining much on natural items — gemma4:latest is the one exception.
5. FinTradeBench draws 36–74% declining on every model; the other sources ≤11%.

**Not supported, despite having looked supported at an interim stage:**

- "The uncertainty signal improves with capability" (2 models).
- "Capability relocates declining" / "the cautious profile is a gemma-family
  property" (2 and 3–5 models).
- "Debate is reliably positive on computable questions" (4–5 models).

## 6. Caveats

- **Masked golds are constructed by us.** Two defects were found by
  hand-reading four masked items, and the masked stratum has not been re-read
  end to end. Every masked-item figure inherits that uncertainty.
- Models differ in family, size, architecture, quantization and machine at
  once. The paired design controls the items, not the model.
- The Qwen3.6-27B and gemma4-31b comparisons with the paper cross quantization
  (FP8/HF → q8_0) and serving stack (vLLM/HF → Ollama).
- One seed, one K, one temperature per model.
- HedgeQA items ship one combined evidence document, so the trading agent
  receives a single-document note; the two agents are less differentiated than
  on FinTradeBench, which may understate debate effects.
- Two items are unscored in one run each (gemma3:4b label surface form, whose
  discarded answer was correct; llama3.3:70b partial decomposition).
