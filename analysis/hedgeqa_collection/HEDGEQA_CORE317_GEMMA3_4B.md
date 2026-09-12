# Full-core run — gemma3:4b on HedgeQA-Core 317

First run over the whole strict collection. `gemma3:4b` (3.3 GB, the smallest
non-embedding model available), K=10, rounds 0+1, τ=0.7, **413.7 min**.
**316/317 scored**, parse_rate mean 0.9996.

```bash
python analysis/hedgeqa_collection/run_hedgeqa_debate.py \
    --manifest data/hedgeqa/hedgeqa_core_v0_1_validated_strict.jsonl \
    --model gemma3:4b --run-id hedgeqa_core317_gemma3_4b --k 10
python analysis/hedgeqa_collection/analyze_core_run.py \
    --run hedgeqa_core317_gemma3_4b
```

This is the first run with enough n to ask the question the project exists
for, rather than to check that the pipeline works.

---

## 1. The headline: the uncertainty signal barely works

**AUC(TU) for predicting an error, among answers the model committed to:
0.598.** Chance is 0.500.

That is the non-circular form of the question, and the only one worth
quoting. An operator's question is *the model just gave me an answer — can I
tell whether it is wrong?* Holding the prediction's commitment fixed, entropy
answers that barely better than a coin.

| population | n | wrong | AUC(TU) |
|---|---|---|---|
| all committed predictions | 257 | 119 (46.3%) | **0.598** |
| natural items, committed gold | 213 | 75 (35.2%) | **0.593** |

And the failure is concentrated exactly where a monitor is blind:

> **205 of 257 committed predictions (80%) are zero-entropy cells — every
> decode from every agent identical — and 83 of those are WRONG (40.5%).**

So on this model, 83 confidently wrong answers arrive with *no* measurable
uncertainty at all. That is the overcommitment failure mode at scale, and it
is the strongest version of the claim the project has produced, because it
rests on 257 observations rather than three.

### A circularity this analysis had to route around

The obvious statistic — mean `p_noncommit` when wrong (0.280) versus when
right (0.150) — looks like strong discrimination and is **largely an
artefact**. On masked items every gold is `insufficient_data`, so *being
right just is declining*, and "p_nc 0.05 when wrong vs 0.95 when right"
restates the definition. The same holds in reverse for committed golds.

The analyzer now prints that split with an explicit warning and reports the
committed-only AUC above as the honest number. Anyone quoting the p_nc split
as evidence would be quoting the scoring rule back at themselves.

## 2. A 4B model overcommits catastrophically on insufficient evidence

| stratum | n | declined |
|---|---|---|
| masked (gold `insufficient_data`) | 47 | **17.0%** |

**39 of 47 masked items are overcommitments (83%).**

30 items have now been run by **both** models, which allows a head-to-head on
identical inputs rather than a comparison of two different sets:

| | n | gemma4 declined | gemma3:4b declined | gemma4 acc | gemma3:4b acc |
|---|---|---|---|---|---|
| masked | 19 | **79%** | **16%** | 79% | 16% |
| natural | 11 | 0% | 0% | 64% | **73%** |

The gap is **entirely in abstention, not in competence**. On the same 19
masked documents the larger model declines 79% of the time and the 4B model
16%. On natural items the 4B model is not worse at all — it is slightly
better (73% vs 64%, though n=11 supports no ranking).

That is a sharper claim than "small models are worse": *what the drop to 4B
costs is not the ability to answer, it is the ability to notice that the
evidence is not there.* The probe that preceded this run showed the
mechanism — asked about Pfizer's PP&E with the PP&E rows masked, the model
quoted `$5,054m` and `$3,406m`, which are the **Long-term investments** rows
immediately adjacent, and committed at p_nc 0.00. It does not decline because
it does not notice anything is missing; it reads the neighbouring row.

## 3. Declining is concentrated in ONE source

This is the finding that most changes how the other numbers should be read.

| source | n | hedge_collision | wrong_direction | overcommitment | declined |
|---|---|---|---|---|---|
| convfinqa | 40 | 0 | 12 | 0 | 0.0% |
| financebench | 36 | 0 | 12 | 0 | 0.0% |
| finqa | 47 | 1 | 11 | 0 | 2.1% |
| tatqa | 50 | 0 | 13 | 0 | 0.0% |
| **fintradebench** | **96** | **38** | **27** | **5** | **52.1%** |

**All 38 hedge collisions and all 5 natural overcommitments are
FinTradeBench.** The other four sources produce essentially zero declining —
combined, 1 decline in 173 items.

So the pooled "declined 19.0%" is not a property of the model in any portable
sense. It is 52% on one source and ~0.6% on the rest, and the pooled figure
mostly reports how much FinTradeBench is in the collection. Any decline rate
quoted from this collection must be quoted per-source.

Two things plausibly drive it, and this run cannot separate them:
FinTradeBench is the only source contributing natural non-committal golds (17
of 96), and it is the only source whose evidence is market data assembled by
our own pipeline rather than a filing excerpt with a known derivation. Its
accuracy is also the outlier — 27.1% against 66.7–74.5% everywhere else.

## 4. Overall performance

| stratum | n | accuracy | mean p_nc | zero-entropy |
|---|---|---|---|---|
| natural | 269 | 55.8% | 0.217 | 82.9% |
| masked | 47 | 17.0% *(decline rate)* | 0.204 | 70.2% |

Masked accuracy is reported as a **decline rate**: single-label gold means a
model that always declines scores 100%, so "accuracy" there would be
meaningless-to-flattering.

Failure taxonomy on natural items: **wrong_direction 75 (27.9%)** is the
largest mode, ahead of hedge_collision 39 (14.5%) and overcommitment 5
(1.9%). By transformation, `numeric_to_directional` scores 73.0% against
37.9% for untransformed items — but that comparison is confounded, since the
untransformed stratum is where FinTradeBench sits.

## 5. Debate helps, consistently

| | round 0 | round 1 | rescued | lost |
|---|---|---|---|---|
| overall | 44.3% | **50.0%** | 24 | 6 |
| natural | 49.8% | 55.8% | 22 | 6 |
| masked | 12.8% | 17.0% | 2 | 0 |

A net **+5.7 points**, 4 rescued for every 1 lost. This is a cleaner result
than the gemma4 runs, where debate was net-zero on the edge set and
manufactured an overcommitment. Reported in both directions as always: it
still loses 6 items that were right at round 0.

Mean `p_noncommit` is unmoved (0.214 → 0.215). Debate changes *answers*
without changing *stated confidence* — which is consistent with §1: whatever
the second round fixes, it is not visible in the uncertainty signal.

## 6. Two instrument bugs found and fixed

**The run manifest recorded the wrong model.** `ollama_digest()` read the
module-level `MODEL` constant instead of the `--model` actually passed, so
this gemma3:4b run was stamped with **gemma4's** digest (`c6eb396dbd59`). It
also matched by prefix, which cannot distinguish `gemma3:4b` from
`gemma3:12b`. Now takes the model explicitly and matches the name exactly;
this run's manifest reads `a2af6cc3eb7f`. Earlier runs were recorded
correctly only by accident, because they happened to use the default model.

**The one unscored item is not a parse failure.** `hqa_FQ_ccc2f20b` returned
valid JSON with the semantically *correct* answer — `"label": "unchanged"`
where the answer space says `roughly_unchanged` — and every decode was
discarded as out-of-space. It failed again on retry, so it is systematic for
this item. It is left unscored rather than patched with a one-off alias,
which would change the instrument for a single item.

Scope checked rather than assumed: parse_rate is 1.0 on every other row
(mean 0.9996, 2 rows below 1.0 out of 632), and the model emits
`roughly_unchanged` correctly 357 times elsewhere in the run. So this is an
isolated surface-form loss, not a systematic scoring leak. Its direction is
worth noting — the discarded answer was **right**, so the error count here is
pessimistic by one item.

## 7. Caveats

- **One model, one K, one temperature, one seed.** Nothing here separates
  "4B models overcommit" from "this 4B model overcommits".
- **Masked golds are constructed by us.** Two defective masked items were
  found by hand-reading four; the masked stratum has not been re-read end to
  end, so the base rate of construction defects in the remaining 47 is
  unknown. The 83% overcommitment figure inherits that uncertainty.
- **Per-source cells are unequal** (36–96 natural items) and the collection
  was not designed as a balanced factorial. Read §3 as a description of this
  collection, not a benchmark ranking.
- **AUC(TU) 0.598 is one model's number.** A weak signal here does not
  establish that entropy monitoring fails in general — it establishes that it
  fails to separate this model's errors on this collection. The gemma4 runs
  were too small to compare against; a gemma4 full-core run is the obvious
  next step, and the analyzer is ready for it.
- 316 scored items is a real n, but the subgroup that carries §1 (83
  confidently-wrong committed answers) is still a single slice of a single
  run.

## 8. Full output

```
==========================================================================
hedgeqa_core317_gemma3_4b
==========================================================================
manifest      data/hedgeqa/hedgeqa_core_v0_1_validated_strict.jsonl
items scored  316 / 317  (99.7% complete)
parse_rate    mean 0.9996  min 0.8000

  PARTIAL RUN -- 1 items not yet scored. Every figure below is over what has completed, and
  the manifest is processed in sorted-id order, so the completed subset is NOT a random sample of sources.

==========================================================================
NATURAL ITEMS (gold from the source benchmark)
==========================================================================
  n                269
  accuracy         55.8%
  declined         19.0%   (gold is non-committal on 6.3%)
  mean p_noncommit 0.217
  zero-entropy     82.9%

==========================================================================
MASKED ITEMS (constructed gold -- accuracy IS the decline rate)
==========================================================================
  n                47
  DECLINED         17.0%  <- reported as a decline rate, not accuracy
  mean p_noncommit 0.204
  zero-entropy     70.2%

==========================================================================
FAILURE TAXONOMY (round 1, natural and masked separated)
==========================================================================
  mode                          natural       masked
  hedge_collision             39 (14.5%)     0 ( 0.0%)
  wrong_direction             75 (27.9%)     0 ( 0.0%)
  overcommitment               5 ( 1.9%)    39 (83.0%)
  wrong_noncommit_type         0 ( 0.0%)     0 ( 0.0%)

==========================================================================
DOES UNCERTAINTY SEPARATE RIGHT FROM WRONG?
==========================================================================
  The claim under test: a monitor watching entropy / p_noncommit
  can flag the answers the model gets wrong. AUC 0.50 = useless.

  WARNING -- the p_noncommit split below is CIRCULAR and is printed
  only to show how large the circularity is. On masked items every
  gold is `insufficient_data`, so being right just IS declining,
  and 'p_nc 0.05 when wrong vs 0.95 when right' restates the
  definition rather than measuring anything. The same holds in
  reverse for committed golds. Use AUC(TU), and above all the
  committed-only test in the next block, which holds the
  prediction's commitment fixed and so cannot be circular.

  natural   n= 269  errors= 119
      mean TU     wrong 0.156 | right 0.066   AUC(TU) 0.566
      mean p_nc   wrong 0.355 | right 0.107
      zero-entropy cells  223, of which WRONG   90 (40.4%) -- confidently wrong, invisible to an entropy monitor
  masked    n=  47  errors=  39
      mean TU     wrong 0.225 | right 0.084   AUC(TU) 0.619
      mean p_nc   wrong 0.051 | right 0.950
      zero-entropy cells   33, of which WRONG   26 (78.8%) -- confidently wrong, invisible to an entropy monitor
  all       n= 316  errors= 158
      mean TU     wrong 0.173 | right 0.067   AUC(TU) 0.578
      mean p_nc   wrong 0.280 | right 0.150
      zero-entropy cells  256, of which WRONG  116 (45.3%) -- confidently wrong, invisible to an entropy monitor

==========================================================================
NON-CIRCULAR TEST: among predictions the model COMMITTED to,
can entropy tell right from wrong?
==========================================================================
  Commitment is held fixed, so p_noncommit is near-constant and
  cannot leak the answer. This is the question an operator has:
  the model just gave me an answer -- can I tell if it is wrong?

  all committed
      n= 257  wrong= 119 (46.3%)   AUC(TU) 0.598
      mean TU  wrong 0.208 | right 0.066
      zero-entropy  205 of 257, of which WRONG   83 (40.5%)
  natural, committed gold
      n= 213  wrong=  75 (35.2%)   AUC(TU) 0.593
      mean TU  wrong 0.203 | right 0.066
      zero-entropy  175 of 213, of which WRONG   53 (30.3%)

==========================================================================
FAILURE MODES BY SOURCE (natural items)
==========================================================================
  source             n  hedge_coll  wrong_dir  overcommit  declined
  convfinqa         40           0         12           0      0.0%
  financebench      36           0         12           0      0.0%
  finqa             47           1         11           0      2.1%
  fintradebench     96          38         27           5     52.1%
  tatqa             50           0         13           0      0.0%

  Read this before quoting any pooled decline rate: if declining
  is concentrated in one source, the pooled figure describes the
  collection's composition more than the model's behaviour.

==========================================================================
BY SOURCE (natural items only)
==========================================================================
  source             n     acc  declined   p_nc
  convfinqa         40   70.0%      0.0%   0.00
  financebench      36   66.7%      0.0%   0.03
  finqa             47   74.5%      2.1%   0.02
  fintradebench     96   27.1%     52.1%   0.58
  tatqa             50   74.0%      0.0%   0.02

==========================================================================
BY TRANSFORMATION
==========================================================================
  transformation                    n  acc/decline   p_nc
  evidence_masked_insufficient     47        17.0%   0.20
  none                            132        37.9%   0.43
  numeric_to_directional          137        73.0%   0.01

==========================================================================
BY GOLD COMMITMENT (natural items only)
==========================================================================
  gold_commitment         n     acc  declined
  committed             252   54.8%     15.5%
  noncommitted           17   70.6%     70.6%

==========================================================================
DEBATE EFFECT (round 0 -> round 1), both directions
==========================================================================
  overall   44.3% -> 50.0%   rescued 24, lost 6  (n=316)
  natural   49.8% -> 55.8%   rescued 22, lost 6  (n=269)
  masked    12.8% -> 17.0%   rescued 2, lost 0  (n=47)
  mean p_noncommit 0.214 -> 0.215 (+0.001)

==========================================================================
CAVEATS
==========================================================================
  - Masked golds are CONSTRUCTED. Two defective masked items were
    found and removed by hand-reading (see the triage doc); the
    masked stratum has not been re-read end to end.
  - One model, one K, one temperature, one seed.
  - Per-source cells are unequal; read them as descriptions of
    this collection, not as benchmark-level comparisons.
```
