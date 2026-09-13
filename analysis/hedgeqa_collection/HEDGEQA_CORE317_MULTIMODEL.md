# HedgeQA-Core 317 — multi-model results (INTERIM: 5 of 7 models)

> **Interim.** Updated as each model in the workstation queue `core317`
> finishes. Every cross-model claim rests on **five** models. Earlier
> versions of this document made claims that a later model broke (§1, §2);
> those corrections are kept visible. Treat directions as leads.

| model | where | digest | items | status |
|---|---|---|---|---|
| gemma3:4b | laptop | a2af6cc3eb7f | 316/317 | done (1 item lost to label surface form) |
| qwen3:8b | workstation | 500a1f067a9f | **317/317** | done, 1.4 h — **same weights as the paper's qwen3:8b** |
| gemma4:latest | workstation | c6eb396dbd59 | **317/317** | done, 1.7 h — **same weights as the paper's gemma4** |
| qwen3.6:27b-q8_0 | workstation | cd0210c667bf | **317/317** | done, 8.2 h — closest Ollama match to the paper's Qwen3.6-27B-FP8 |
| qwen3.6:35b-a3b-q8_0 | workstation | 0218f872e86b | **317/317** | done, 2.1 h |
| gemma4:31b-it-q8_0 | workstation | 53dd8459790f | — | probing |
| llama3.3:70b | workstation | a6eb4748fd29 | — | queued (~10 h) |
| ~~gpt-oss:120b~~ | — | a951a23b46a1 | — | **excluded**: empty content on 73/80 probe calls under format=json + think=false; cannot disable reasoning, so including it would change the condition |

All runs: strict 317, K=10, rounds 0+1, τ=0.7, **0 parse failures on every
workstation run**. Every workstation model passed `probe_models.py` before its
full run. Comparisons are **paired** over the 316 items all runs scored.

```bash
python analysis/hedgeqa_collection/compare_core_runs.py --runs \
  hedgeqa_core317_gemma3_4b,hedgeqa_core317_qwen3_8b,hedgeqa_core317_gemma4_latest,hedgeqa_core317_qwen3_6_27b-q8_0,hedgeqa_core317_qwen3_6_35b-a3b-q8_0
```

---

## 0. Headline table

| | gemma3:4b | qwen3:8b | gemma4:latest | qwen3.6:27b | qwen3.6:35b |
|---|---|---|---|---|---|
| natural accuracy | 55.8% | 66.9% | 62.8% | 70.6% | **74.3%** |
| **masked decline rate** | 17.0% | 63.8% | 78.7% | **83.0%** | 78.7% |
| natural items declined | 19.0% | 16.4% | **28.3%** | 14.1% | 17.5% |
| zero-entropy cells | 81.0% | **84.8%** | 81.3% | 78.2% | 69.0% |
| committed, zero-entropy, WRONG | 83 | 49 | 26 | 26 | 19 |
| debate rescued / lost | 24 / 6 | 25 / 9 | 32 / 9 | **7 / 9** | 22 / 8 |
| accuracy r0 → r1 | 44.3→50.0% | 61.4→66.5% | 57.9→65.2% | **73.1→72.5%** | 70.6→75.0% |

## 1. The uncertainty signal: weak everywhere; better for one model generation, not for size

AUC(TU) for predicting an error, **committed predictions only** (commitment
held fixed, so `p_noncommit` cannot leak the answer):

| model | AUC | 95% CI | vs gemma3:4b (paired) | |
|---|---|---|---|---|
| gemma3:4b | 0.598 | [0.546, 0.648] | — | |
| qwen3:8b | 0.601 | [0.545, 0.661] | +0.004 [−0.068, +0.078] | not distinguishable |
| gemma4:latest | 0.666 | [0.586, 0.747] | +0.069 [−0.026, +0.165] | not distinguishable |
| **qwen3.6:27b** | **0.718** | [0.647, 0.790] | +0.120 [+0.035, +0.208] | **distinguishable** |
| **qwen3.6:35b-a3b** | **0.705** | [0.620, 0.789] | +0.108 [+0.013, +0.196] | **distinguishable** |

The split is by **model generation**. Both qwen3.6 models are distinguishable
from the 4B baseline; qwen3:8b and gemma4 are not. The two qwen3.6 models are
a dense 27B and a mixture-of-experts with ~3B active parameters, and they land
within 0.013 of each other — so within this set neither total nor active
parameter count predicts the signal, and generation does.

The ordering is also not an accuracy ordering: qwen3:8b is more accurate than
gemma4 on natural items (66.9% vs 62.8%) with lower AUC (0.601 vs 0.666).

**CORRECTION kept visible:** the 2-model version read the first qwen3.6
result as "the signal improves with capability". Two later models of greater
size than the 4B baseline did not improve it.

Defensible claim: **entropy is a weak error detector on every model tested
(AUC 0.60–0.72); only the qwen3.6 generation moves it measurably off the 4B
baseline, and even there roughly one committed error in two is invisible to
it** (qwen3.6:27b: 26 of 54 committed errors are zero-entropy).

## 2. Declining: targeted vs cautious routes to the masked score

| | masked declined (right) | natural declined | FinTradeBench declined |
|---|---|---|---|
| gemma3:4b | 17.0% | 19.0% | 52.1% |
| qwen3:8b | 63.8% | 16.4% | 41.7% |
| gemma4:latest | 78.7% | **28.3%** | **72.9%** |
| qwen3.6:27b | **83.0%** | **14.1%** | **35.4%** |
| qwen3.6:35b | 78.7% | 17.5% | 46.9% |

**CORRECTION kept visible:** the 2-model version said capability "relocates
declining rather than increasing it". gemma4 broke that — it matches qwen3.6's
masked rate while declining more on natural items. With five models the
picture is two distinct profiles:

- **Targeted (qwen family):** natural-item declining stays low on all three
  (14.1–17.5%, not monotone in capability) while masked declining rises from
  63.8% (qwen3:8b) to 78.7–83.0% (qwen3.6). qwen3.6:27b is the extreme on
  both axes: highest masked decline (83.0%) and lowest natural and
  FinTradeBench declining (14.1%, 35.4%).
- **Cautious (gemma4):** reaches a high masked rate by declining more
  everywhere, most of all on FinTradeBench — consistent with gemma4 being the
  FinTradeBench paper's hedge-certainty-regime model.

**Nesting.** Every masked item gemma3:4b declined, all four larger models also
declined (0 gemma3-only in every pair). The two qwen3.6 models nearly nest in
each other: 37 both, 2 only-27b, **0** only-35b, 8 neither.

## 3. The FinTradeBench concentration holds on 5 of 5

| source | gemma3:4b | qwen3:8b | gemma4:latest | qwen3.6:27b | qwen3.6:35b |
|---|---|---|---|---|---|
| convfinqa | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| financebench | 0.0% | 5.6% | 2.8% | 5.6% | 0.0% |
| finqa | 2.1% | 2.1% | 2.1% | 2.1% | 2.1% |
| tatqa | 0.0% | 2.0% | 8.0% | 2.0% | 2.0% |
| **fintradebench** | **52.1%** | **41.7%** | **72.9%** | **35.4%** | **46.9%** |

FinTradeBench draws 35–73% declining on every model; no other source exceeds
8% on any model. The strongest cross-model regularity in the data. It is a
property of the **source**, not of particular items (the 2-model comparison
found only 21 of 38/32 hedge collisions shared).

## 4. Debate: helps on filing questions, flat-to-harmful on FinTradeBench

Debate split by source (same rows, no new calls):

| model | FinTradeBench (96): rescued / lost | net | other sources (~221): rescued / lost | net |
|---|---|---|---|---|
| gemma3:4b | 7 / 1 | +6 | 17 / 5 | +12 |
| qwen3:8b | 8 / 7 | **+1** | 17 / 2 | +15 |
| gemma4:latest | 2 / 2 | **0** | 30 / 7 | +23 |
| **qwen3.6:27b** | **1 / 6** | **−5** | 6 / 3 | +3 |
| qwen3.6:35b | 10 / 4 | +6 | 12 / 4 | +8 |

**On other sources debate is net positive for all five models.** On
FinTradeBench it is net +1, 0 and **−5** for three of five — including both of
the paper's local models and the closest match to its Qwen3.6-27B.

qwen3.6:27b is the first model whose debate is net-negative **overall** (7
rescued, 9 lost), and the losses localise: 6 of 9 are FinTradeBench items. It
is also the model with the highest round-0 accuracy (73.1%), so there is least
to rescue. Three of its nine losses are debate-induced **direction flips** on
computable filing questions (`decreased` → `increased` twice,
`roughly_unchanged` → `decreased` once) — debate manufacturing wrong-direction
commitments, not only hedges.

### Relation to the FinTradeBench paper

- **qwen3:8b** (same weights): the paper found debate net-harmful on
  FinTradeBench (4 rescued / 8 lost). HedgeQA overall is net positive (25 / 9),
  but on its FinTradeBench items it is flat (8 / 7). **Consistent in direction,
  not magnitude.**
- **Qwen3.6-27B**: the paper's FP8 run was mildly net-positive on FinTradeBench
  (6 rescued / 4 lost). Here the q8_0 build is net-**negative** on
  FinTradeBench items (1 / 6). **Opposite direction.** Small counts on both
  sides (10 and 7 moved items), and three things differ at once: quantization
  (FP8 vs q8_0), serving stack (vLLM vs Ollama) and the item set (139 E-A′
  questions vs 96 HedgeQA items). Not reconcilable from this data.

The HedgeQA evidence therefore supports a narrower claim than either result
alone: **debate's value depends on the question source — reliably positive on
computable filing questions, and zero-to-negative on FinTradeBench's
judgment-heavy questions.** Whether a given model is net positive overall is
largely a matter of how many FinTradeBench items the evaluation contains.

## 5. Caveats specific to this interim

- **Five models, two families** (gemma, qwen) plus one more to come
  (llama3.3). "Generation, not size" in §1 rests on a single generation (two
  qwen3.6 models); gemma4:31b is the direct test of whether size helps within
  the gemma family.
- The models differ in family, size, architecture, quantization and machine
  at once. The paired comparison controls the items, not the model.
- gemma3:4b is missing one item (`hqa_FQ_ccc2f20b`) whose discarded answer was
  correct, so its error count is pessimistic by one.
- Masked golds are constructed; the masked stratum has not been re-read end
  to end since two defects were found in four items.
- Run manifests record `ollama_url: localhost`, true on both machines; the
  queue ledger establishes provenance until the hostname is added after the
  queue finishes.
