# HedgeQA-Core 317 — multi-model results (INTERIM: 2 of 7 models)

> **Interim.** Updated as each model in the workstation queue `core317`
> finishes. Nothing here is final until the queue completes, and every
> cross-model claim below rests on **two** models. Treat directions as
> leads, not findings.

| model | where | digest | items | status |
|---|---|---|---|---|
| gemma3:4b | laptop | a2af6cc3eb7f | 316/317 | done (1 item lost to label surface form) |
| qwen3.6:35b-a3b-q8_0 | workstation | 0218f872e86b | **317/317** | done, 2.1 h, 0 parse failures |
| gemma4:latest | workstation | c6eb396dbd59 | — | running |
| qwen3:8b | workstation | 500a1f067a9f | — | queued |
| qwen3.6:27b-q8_0 | workstation | cd0210c667bf | — | queued |
| gemma4:31b-it-q8_0 | workstation | 53dd8459790f | — | queued |
| llama3.3:70b | workstation | a6eb4748fd29 | — | queued (~10 h) |
| ~~gpt-oss:120b~~ | — | a951a23b46a1 | — | **excluded**: empty content on 73/80 probe calls under format=json + think=false; cannot disable reasoning, so including it would change the condition |

All runs: strict 317, K=10, rounds 0+1, τ=0.7. Every model passed
`probe_models.py` (parse rate, no output truncation, no empty content, prompt
fits context) before its full run. Comparisons are **paired** over the 316
items both runs scored.

```bash
python analysis/hedgeqa_collection/compare_core_runs.py \
    --runs hedgeqa_core317_gemma3_4b,hedgeqa_core317_qwen3_6_35b-a3b-q8_0
```

---

## 1. The uncertainty signal gets better with capability — distinguishably, but not by much

AUC(TU) for predicting an error, **committed predictions only** (commitment
held fixed, so `p_noncommit` cannot leak the answer):

| model | AUC | 95% CI | committed | wrong |
|---|---|---|---|---|
| gemma3:4b | 0.598 | [0.546, 0.648] | 257 | 119 |
| qwen3.6:35b-a3b | **0.705** | [0.620, 0.789] | 232 | 42 |

**Paired difference +0.108, 95% CI [+0.013, +0.196] — distinguishable.** The
lower bound sits close to zero, so the honest reading is a real but modest
improvement, not a transformation.

The confidently-wrong count moves more: committed zero-entropy wrong answers
fall from **83 to 19**. Some of that is simply fewer errors (119 → 42); the
share of committed errors that are invisible to entropy falls from 70% to 45%.

## 2. Capability relocates declining rather than increasing it

| | gemma3:4b | qwen3.6:35b |
|---|---|---|
| **masked** decline rate (should decline) | 17.0% | **78.7%** |
| **natural** items declined | 19.0% | 17.5% |

The stronger model declines four times as often where the evidence is
actually missing, and **no more often** on natural items. It is not a more
cautious model; it is a better-targeted one.

The masked declines are **nested**: of 47 masked items, every one gemma3:4b
declined, qwen also declined (8 both, 0 gemma-only, 29 qwen-only, 10
neither). That is the pattern expected if declining tracks a real property of
the evidence that the larger model detects more reliably — not two models
declining at random.

## 3. The FinTradeBench concentration replicates at the source level — not item by item

| source | gemma3:4b declined | qwen3.6:35b declined |
|---|---|---|
| convfinqa | 0.0% | 0.0% |
| financebench | 0.0% | 0.0% |
| finqa | 2.1% | 2.1% |
| tatqa | 0.0% | 2.0% |
| **fintradebench** | **52.1%** | **46.9%** |

On gemma3:4b this looked like it might be a small-model artifact. It is not:
a model with 18 points more natural accuracy shows the same shape. But the
item-level overlap is only partial:

- FinTradeBench hedge collisions: gemma3:4b **38**, qwen **32**, shared **21**
  (17 gemma-only, 11 qwen-only).

So the stable property is that *FinTradeBench questions invite declining*,
not that particular questions do. This matches the FinTradeBench paper's own
finding that the FT lane is the highest-hedging lane in 5 of 5 models, and
that capability buys commitment on F and T but not FT.

Capability also does **not** help on FinTradeBench's genuinely non-committal
golds: 12/17 correct for gemma3:4b, 10/17 for qwen.

## 4. Debate

| | round 0 → round 1 | rescued | lost |
|---|---|---|---|
| gemma3:4b | 44.3% → 50.0% | 24 | 6 |
| qwen3.6:35b | 70.6% → 75.0% | 22 | 8 |

Net positive on both, with a similar absolute gain (~+5 points) despite very
different starting accuracy. Mean `p_noncommit` is unmoved on both (+0.001):
debate changes answers without changing stated confidence.

On qwen's masked items debate is net **negative** (1 rescued, 2 lost) — it
argued two correctly-declining items into commitments. Three items, so a
direction only.

## 5. Caveats specific to this interim

- **Two models, one from each size extreme** of the queue. Anything that
  looks like a trend is a line through two points; the five models still
  running will show whether it is monotone.
- The two differ in **family, size, architecture (dense vs MoE), quantization
  and machine** at once. The paired comparison controls the items, not the
  model.
- gemma3:4b is missing one item (`hqa_FQ_ccc2f20b`) whose discarded answer was
  correct, so its error count is pessimistic by one.
- Masked golds are constructed; the masked stratum has not been re-read end
  to end since two defects were found in four items.
- Run manifests record `ollama_url: localhost`, which is true on both
  machines. The queue ledger (`results/queue/core317.json`) is what
  establishes that a run came from the workstation; the manifest will record
  the hostname once the queue is finished and code can safely change.
