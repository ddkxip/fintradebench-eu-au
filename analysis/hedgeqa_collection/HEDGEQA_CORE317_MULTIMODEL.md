# HedgeQA-Core 317 — multi-model results (INTERIM: 4 of 7 models)

> **Interim.** Updated as each model in the workstation queue `core317`
> finishes. Every cross-model claim rests on **four** models. Two earlier
> versions of this document made claims that the next model broke (§1, §2);
> treat directions as leads, not findings.

| model | where | digest | items | status |
|---|---|---|---|---|
| gemma3:4b | laptop | a2af6cc3eb7f | 316/317 | done (1 item lost to label surface form) |
| qwen3:8b | workstation | 500a1f067a9f | **317/317** | done, 1.4 h, 0 parse failures — **same weights as the paper's qwen3:8b** |
| gemma4:latest | workstation | c6eb396dbd59 | **317/317** | done, 1.7 h, 0 parse failures — **same weights as the paper's gemma4** |
| qwen3.6:35b-a3b-q8_0 | workstation | 0218f872e86b | **317/317** | done, 2.1 h, 0 parse failures |
| qwen3.6:27b-q8_0 | workstation | cd0210c667bf | — | running — probe 90.6 s/item, **~8 h** |
| gemma4:31b-it-q8_0 | workstation | 53dd8459790f | — | queued |
| llama3.3:70b | workstation | a6eb4748fd29 | — | queued (~10 h) |
| ~~gpt-oss:120b~~ | — | a951a23b46a1 | — | **excluded**: empty content on 73/80 probe calls under format=json + think=false; cannot disable reasoning, so including it would change the condition |

All runs: strict 317, K=10, rounds 0+1, τ=0.7. Every workstation model passed
`probe_models.py` before its full run. Comparisons are **paired** over the 316
items all runs scored.

```bash
python analysis/hedgeqa_collection/compare_core_runs.py --runs \
  hedgeqa_core317_gemma3_4b,hedgeqa_core317_qwen3_8b,hedgeqa_core317_gemma4_latest,hedgeqa_core317_qwen3_6_35b-a3b-q8_0
```

---

## 0. Headline table

| | gemma3:4b | qwen3:8b | gemma4:latest | qwen3.6:35b |
|---|---|---|---|---|
| natural accuracy | 55.8% | 66.9% | 62.8% | **74.3%** |
| **masked decline rate** | 17.0% | 63.8% | **78.7%** | **78.7%** |
| natural items declined | 19.0% | 16.4% | **28.3%** | 17.5% |
| zero-entropy cells | 81.0% | **84.8%** | 81.3% | 69.0% |
| committed, zero-entropy, WRONG | 83 | 49 | 26 | 19 |
| debate rescued / lost | 24 / 6 | 25 / 9 | 32 / 9 | 22 / 8 |
| accuracy r0 → r1 | 44.3→50.0% | 61.4→66.5% | 57.9→65.2% | 70.6→75.0% |

## 1. The uncertainty signal is weak everywhere, and does not track accuracy

AUC(TU) for predicting an error, **committed predictions only** (commitment
held fixed, so `p_noncommit` cannot leak the answer):

| model | AUC | 95% CI | committed | wrong |
|---|---|---|---|---|
| gemma3:4b | 0.598 | [0.546, 0.648] | 257 | 119 |
| qwen3:8b | 0.601 | [0.545, 0.661] | 242 | 72 |
| gemma4:latest | 0.666 | [0.586, 0.747] | 203 | 47 |
| qwen3.6:35b-a3b | 0.705 | [0.620, 0.789] | 232 | 42 |

Paired bootstrap differences against gemma3:4b:

| | difference | 95% CI | |
|---|---|---|---|
| qwen3:8b − gemma3:4b | +0.004 | [−0.068, +0.078] | **not distinguishable** |
| gemma4:latest − gemma3:4b | +0.069 | [−0.026, +0.165] | **not distinguishable** |
| qwen3.6:35b − gemma3:4b | +0.108 | [+0.013, +0.196] | distinguishable |

**Two of three larger models are statistically indistinguishable from the 4B
model.** The 2-model version of this document read qwen3.6's gain as "the
signal improves with capability"; with four points that reading does not
survive.

And the ordering is not an accuracy ordering. qwen3:8b is **more accurate**
than gemma4 on natural items (66.9% vs 62.8%) yet has a **lower** AUC (0.601
vs 0.666). Whatever separates the two AUC groups, it is not simply "being
right more often".

The claim this supports: **entropy is a weak error detector on every model
tested (AUC 0.60–0.71), and three of four models leave it statistically at
the 4B baseline.**

## 2. Declining: two routes to the masked score, and qwen3:8b in between

| | masked declined (right) | natural declined | FinTradeBench declined |
|---|---|---|---|
| gemma3:4b | 17.0% | 19.0% | 52.1% |
| qwen3:8b | 63.8% | 16.4% | 41.7% |
| gemma4:latest | **78.7%** | **28.3%** | **72.9%** |
| qwen3.6:35b | **78.7%** | 17.5% | 46.9% |

**CORRECTION carried from the 3-model version:** the 2-model document said
capability "relocates declining rather than increasing it". gemma4 reaches
qwen3.6's masked decline rate **exactly** while declining more on natural
items, almost all on FinTradeBench — a cautious route to the same score,
against qwen3.6's targeted one. This is consistent with gemma4 being the
FinTradeBench paper's hedge-certainty-regime model.

qwen3:8b adds a third profile: the **least** natural-item declining of the
four (16.4%) with substantial masked declining (63.8%) — targeted like its
qwen3.6 sibling, at lower strength.

**Masked-decline nesting, restated precisely.** Every masked item gemma3:4b
declined, **all three** larger models also declined (0 gemma3-only in every
pair). That is a floor, not a hierarchy: among the larger models the sets
nearly nest but not quite (qwen3:8b declines 2–3 items that gemma4 or qwen3.6
do not).

## 3. The FinTradeBench concentration holds on 4 of 4

| source | gemma3:4b | qwen3:8b | gemma4:latest | qwen3.6:35b |
|---|---|---|---|---|
| convfinqa | 0.0% | 0.0% | 0.0% | 0.0% |
| financebench | 0.0% | 5.6% | 2.8% | 0.0% |
| finqa | 2.1% | 2.1% | 2.1% | 2.1% |
| tatqa | 0.0% | 2.0% | 8.0% | 2.0% |
| **fintradebench** | **52.1%** | **41.7%** | **72.9%** | **46.9%** |

Four models, two families, two architectures, same shape: FinTradeBench
draws 42–73% declining and no other source exceeds 8%. The strongest
cross-model regularity in the data so far. It is a property of the
**source**, not of particular items — on the 2-model comparison the hedge
collisions overlapped on only 21 of 38/32 items.

## 4. Debate — and a result that does NOT replicate the paper

Net positive on all four (+5.7, +5.1, +7.3, +4.4 points), with 2.8–4
rescues per loss, and mean `p_noncommit` unmoved on all four.

**This conflicts with the FinTradeBench paper on qwen3:8b.** There, the same
weights (digest `500a1f067a9f`) had debate **net-harmful**: 4 rescued against
8 lost on the 139-question E-A′ run. Here qwen3:8b is net **positive**, 25
rescued against 9 lost.

Not yet explained, and it should not be smoothed over. Candidate causes, none
tested:

- **Different collection.** HedgeQA is dominated by directional and yes/no
  filing questions with oracle evidence and known derivations; FinTradeBench's
  E-A′ set is judgment-heavy, with an FT lane built to contain conflicting
  signals. Debate may help on computable questions and hurt on judgment ones.
- **Different agent framing.** HedgeQA items ship one combined document, so
  the trading agent receives a single-document note instead of a trading
  context. The two agents are less differentiated than on FinTradeBench.
- Scale: n=139 there vs 317 here, and 12 moved items there.

### Tested: debate split by source

Restricting to HedgeQA's 96 FinTradeBench-sourced items versus everything else
(reanalysis of the same rows, no new calls):

| model | FinTradeBench (96): rescued / lost | net | other sources (~221): rescued / lost | net |
|---|---|---|---|---|
| gemma3:4b | 7 / 1 | +6 | 17 / 5 | +12 |
| **qwen3:8b** | **8 / 7** | **+1** | 17 / 2 | +15 |
| **gemma4:latest** | **2 / 2** | **0** | 30 / 7 | +23 |
| qwen3.6:35b | 10 / 4 | +6 | 12 / 4 | +8 |

**The collection explanation is partly supported.** For **both of the
paper's models**, debate's benefit vanishes on FinTradeBench items (net +1
and 0) and comes almost entirely from the other four sources. qwen3:8b loses
7 of 96 FinTradeBench items to debate against 2 of 221 elsewhere — a loss rate
roughly **8× higher** on FinTradeBench.

It does **not** fully reproduce the paper: net +1 is not net −4. So the
honest statement is that the HedgeQA result and the paper result are
reconciled in *direction* — debate is harmless-to-useless on FinTradeBench
questions and useful on computable filing questions — but not in magnitude.
The residual gap is plausibly the single-document adapter (the two agents are
less differentiated here), untested.

The two non-paper models do not show the pattern as strongly (+6 on
FinTradeBench for both), so this is not a clean universal either. Counts per
cell are small (4–15 moved items); read it as a direction.

## 5. Caveats specific to this interim

- **Four models.** §1 and §2 each contain a claim an earlier version made
  and a later model broke.
- The models differ in **family, size, architecture (dense vs MoE),
  quantization and machine** at once. The paired comparison controls the
  items, not the model. Note qwen3.6:35b-a3b activates ~3B parameters per
  token and still beats dense qwen3:8b on natural accuracy, masked declining,
  AUC and confidently-wrong count — generation, not active parameter count,
  is doing that work.
- gemma3:4b is missing one item (`hqa_FQ_ccc2f20b`) whose discarded answer was
  correct, so its error count is pessimistic by one.
- Masked golds are constructed; the masked stratum has not been re-read end
  to end since two defects were found in four items.
- Run manifests record `ollama_url: localhost`, true on both machines; the
  queue ledger establishes provenance until the hostname is added after the
  queue finishes.
