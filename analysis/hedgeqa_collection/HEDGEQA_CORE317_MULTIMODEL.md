# HedgeQA-Core 317 — multi-model results (INTERIM: 3 of 7 models)

> **Interim.** Updated as each model in the workstation queue `core317`
> finishes. Every cross-model claim rests on **three** models, and the
> 2-model version of this document made a claim the third model broke (§2).
> Treat directions as leads, not findings.

| model | where | digest | items | status |
|---|---|---|---|---|
| gemma3:4b | laptop | a2af6cc3eb7f | 316/317 | done (1 item lost to label surface form) |
| gemma4:latest | workstation | c6eb396dbd59 | **317/317** | done, 1.7 h, 0 parse failures — **same weights as the paper's gemma4** |
| qwen3.6:35b-a3b-q8_0 | workstation | 0218f872e86b | **317/317** | done, 2.1 h, 0 parse failures |
| qwen3:8b | workstation | 500a1f067a9f | — | running — same weights as the paper's qwen3:8b |
| qwen3.6:27b-q8_0 | workstation | cd0210c667bf | — | queued |
| gemma4:31b-it-q8_0 | workstation | 53dd8459790f | — | queued |
| llama3.3:70b | workstation | a6eb4748fd29 | — | queued (~10 h) |
| ~~gpt-oss:120b~~ | — | a951a23b46a1 | — | **excluded**: empty content on 73/80 probe calls under format=json + think=false; cannot disable reasoning, so including it would change the condition |

All runs: strict 317, K=10, rounds 0+1, τ=0.7. Every workstation model passed
`probe_models.py` before its full run. Comparisons are **paired** over the 316
items all runs scored.

```bash
python analysis/hedgeqa_collection/compare_core_runs.py \
    --runs hedgeqa_core317_gemma3_4b,hedgeqa_core317_gemma4_latest,hedgeqa_core317_qwen3_6_35b-a3b-q8_0
```

---

## 0. Headline table

| | gemma3:4b | gemma4:latest | qwen3.6:35b |
|---|---|---|---|
| natural accuracy | 55.8% | 62.8% | **74.3%** |
| **masked decline rate** | 17.0% | **78.7%** | **78.7%** |
| natural items declined | 19.0% | **28.3%** | 17.5% |
| zero-entropy cells | 81.0% | 81.3% | 69.0% |
| committed, zero-entropy, WRONG | 83 | 26 | 19 |
| debate rescued / lost | 24 / 6 | 32 / 9 | 22 / 8 |
| accuracy r0 → r1 | 44.3→50.0% | 57.9→65.2% | 70.6→75.0% |

## 1. The uncertainty signal: better on both larger models, distinguishably on only one

AUC(TU) for predicting an error, **committed predictions only** (commitment
held fixed, so `p_noncommit` cannot leak the answer):

| model | AUC | 95% CI | committed | wrong |
|---|---|---|---|---|
| gemma3:4b | 0.598 | [0.546, 0.648] | 257 | 119 |
| gemma4:latest | 0.666 | [0.586, 0.747] | 203 | 47 |
| qwen3.6:35b-a3b | 0.705 | [0.620, 0.789] | 232 | 42 |

Paired bootstrap differences against gemma3:4b:

| | difference | 95% CI | |
|---|---|---|---|
| gemma4:latest − gemma3:4b | +0.069 | [−0.026, +0.165] | **not distinguishable** |
| qwen3.6:35b − gemma3:4b | +0.108 | [+0.013, +0.196] | distinguishable |

Both point estimates sit above the 4B model, but only one difference clears
zero. The defensible claim is therefore narrow: **the discrimination signal
is weak on all three models (AUC 0.60–0.71) and no model makes entropy a
reliable error detector.** "It improves with capability" is a direction two
of three points are consistent with, not a result.

## 2. CORRECTION: capability does not simply relocate declining

The 2-model version of this document said the stronger model "declines four
times as often where the evidence is missing, and no more often on natural
items — a better-targeted model, not a more cautious one." **gemma4 breaks
that.**

| | masked declined (right) | natural declined | FinTradeBench declined |
|---|---|---|---|
| gemma3:4b | 17.0% | 19.0% | 52.1% |
| gemma4:latest | **78.7%** | **28.3%** | **72.9%** |
| qwen3.6:35b | **78.7%** | 17.5% | 46.9% |

gemma4 and qwen decline on masked items at **exactly** the same rate, but
gemma4 gets there while declining *more* on natural items, almost entirely on
FinTradeBench. So two different routes reach the same masked score:

- **qwen: targeted.** Declines where evidence is missing, not elsewhere.
- **gemma4: cautious.** Declines more everywhere, which catches the masked
  items and also produces more hedge collisions on FinTradeBench.

This is consistent with the FinTradeBench paper, where gemma4 is the
canonical *hedge-certainty regime* model (judgment-question hedging 100%).
The regime is a property of the model family, and it shows up on a
different collection built by different means.

The nesting pattern survives: every masked item gemma3:4b declined, **both**
larger models also declined (0 gemma3-only in either pair). gemma4 and qwen
agree on 39 of 47 masked items (33 both declined, 6 neither) and swap 4 each
way — the same rate on different items.

## 3. The FinTradeBench concentration replicates at source level, on all three

| source | gemma3:4b | gemma4:latest | qwen3.6:35b |
|---|---|---|---|
| convfinqa | 0.0% | 0.0% | 0.0% |
| financebench | 0.0% | 2.8% | 0.0% |
| finqa | 2.1% | 2.1% | 2.1% |
| tatqa | 0.0% | 8.0% | 2.0% |
| **fintradebench** | **52.1%** | **72.9%** | **46.9%** |

Three models, three families of behaviour, same shape: FinTradeBench draws
declines and the other four sources do not. It is a property of the
**source**, not of particular items — on the 2-model comparison the hedge
collisions overlapped on only 21 of 38/32 items.

## 4. Debate

Net positive on all three (+5.7, +7.3, +4.4 points), 2.8–4 rescues per loss,
and mean `p_noncommit` unmoved on all three. gemma4 has the largest ledger
(32 rescued / 9 lost), which fits a cautious model with more hedge
collisions for a second round to resolve.

## 5. Caveats specific to this interim

- **Three models.** §2 is a worked example of a 2-model trend failing on the
  third; the same can happen to anything here.
- The models differ in **family, size, architecture (dense vs MoE),
  quantization and machine** at once. The paired comparison controls the
  items, not the model.
- gemma3:4b is missing one item (`hqa_FQ_ccc2f20b`) whose discarded answer was
  correct, so its error count is pessimistic by one.
- Masked golds are constructed; the masked stratum has not been re-read end
  to end since two defects were found in four items.
- Run manifests record `ollama_url: localhost`, true on both machines; the
  queue ledger establishes provenance until the hostname is added after the
  queue finishes.
