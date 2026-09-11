# HedgeQA smoke_15 — first debate run

`gemma4:latest` via Ollama, K=10, rounds 0+1, tau=0.7, 22.3 min.
Manifest: `data/hedgeqa/hedgeqa_core_v0_1_smoke_15.jsonl` (15 items).

**This is a smoke test, not a measurement.** With n=15 the 95% CI on any
proportion is roughly +/-25 points, per-source cells hold 3 items, and the
error decomposition rests on 5 errors. Every figure below is an observation.

## Did the pipeline work

Yes. **15/15 items scored, parse_rate exactly 1.0000**, every predicted label
inside its answer space, gold scoring and the TU/AU/EU decomposition
computing on every row. No retries, no aborts.

## What was observed

| | value |
|---|---|
| accuracy (round 1) | 66.7% (10/15) |
| mean `p_noncommit` | 0.377 |
| **zero-entropy cells** | **80%** |
| debate effect | 60.0% -> 66.7% (2 rescued, 1 lost) |

**80% of question-model cells had exactly zero total entropy** -- every
sample from every agent produced the identical answer. That reproduces the
parent paper's near-determinism finding on a different item set, and it is
the cleanest signal in a run this size because it does not depend on the
gold labels at all.

### Natural vs masked, kept separate

| | n | accuracy | mean p_nc | declined |
|---|---|---|---|---|
| natural | 11 | 63.6% | 0.227 | 18.2% |
| masked (constructed gold) | 4 | 75.0% | 0.787 | 75.0% |

The masked items behaved as designed: the model declined on 3 of 4 and was
scored correct for doing so. The fourth, `hqa_FB_1858a6da_masked`, was
answered `yes` at `p_nc = 0.00` -- a confident commitment on evidence a human
reviewer verified cannot support an answer. **That is an overcommitment, and
it is the single most useful event in this run**: the masked items exist to
make that failure visible, and on their first outing they did.

### Error decomposition (5 errors)

| mode | n |
|---|---|
| wrong_direction | 3 |
| hedge_collision | 1 |
| overcommitment | 1 |
| wrong_noncommit_type | 0 |

Note `numeric_to_directional` items drew **mean p_nc = 0.00** -- the model
never once declined on a directional question, committing on all 6 and
getting 4 right. Both directional errors are TAT-QA items answered
`increased` against golds of `decreased` and `roughly_unchanged`. The second
of those is a wrong_direction error rather than a hedge collision precisely
because of the convention revision.

## Caveats

- 15 items. No rate here is estimable; do not quote these percentages.
- 3 items per source. The by-source table shows the pipeline exercised every
  source, nothing more.
- One model, one K, one temperature.
- The manifest deliberately excludes the 10 `evidence_gutted` items, so a
  clean pass here says nothing about the edge set
  (`hedgeqa_core_v0_1_edge_smoke_15.jsonl`), which is where declining for
  the wrong reason would show up.

## Full output

```
=== hedgeqa_smoke15_gemma4 ===
items scored: 15 / 15    parse_rate mean 1.0000 min 1.000

OVERALL (round 1)
  accuracy      66.7%  (10/15)
  mean p_nc     0.377
  mean TU/AU/EU 0.160 / 0.031 / 0.129
  zero-entropy cells 80%  (every sample from every agent identical)

NATURAL  n=11
  accuracy   63.6%
  mean p_nc  0.227
  declined   18.2% of items

MASKED (constructed gold)  n=4
  accuracy   75.0%
  mean p_nc  0.787
  declined   75.0% of items

ERROR DECOMPOSITION (round 1)
  hedge_collision         1/5  20%
  wrong_direction         3/5  60%
  overcommitment          1/5  20%
  wrong_noncommit_type    0/5  0%

BY SOURCE (3 items each — shape check only, not a rate)
  source           n    acc   p_nc
  convfinqa        3   100%   0.33
  financebench     3    33%   0.05
  finqa            3   100%   0.33
  fintradebench    3    67%   0.83
  tatqa            3    33%   0.33

BY TRANSFORMATION
  transformation                  n    acc   p_nc
  evidence_masked_insufficient    4    75%   0.79
  none                            5    60%   0.50
  numeric_to_directional          6    67%   0.00

DEBATE EFFECT (round 0 -> round 1)
  accuracy 60.0% -> 66.7%   rescued 2, lost 1  (n=15)
  mean p_nc 0.343 -> 0.377 (+0.033)

PER ITEM
  id                         source         transf gold               pred                p_nc ok
  hqa_CFQ_05f42dea           convfinqa      dir    decreased          decreased           0.00 Y
  hqa_CFQ_07480310           convfinqa      dir    decreased          decreased           0.00 Y
  hqa_CFQ_13c20530_masked    convfinqa      mask   insufficient_data  insufficient_data   1.00 Y
  hqa_FB_04a83e7c            financebench   nat    yes                no                  0.00 n
  hqa_FB_11e71606            financebench   nat    no                 no                  0.00 Y
  hqa_FB_1858a6da_masked     financebench   mask   insufficient_data  yes                 0.15 n
  hqa_FQ_0921febd            finqa          dir    decreased          decreased           0.00 Y
  hqa_FQ_0bb282d6            finqa          dir    decreased          decreased           0.00 Y
  hqa_FQ_23b54354_masked     finqa          mask   insufficient_data  insufficient_data   1.00 Y
  hqa_FTB_008bd6df           fintradebench  nat    conditional        conditional         1.00 Y
  hqa_FTB_01c97f78           fintradebench  nat    value_trap         mixed               1.00 n
  hqa_FTB_06c86cd6           fintradebench  nat    reinvestment_oppor reinvestment_oppor  0.50 Y
  hqa_TAT_0a4b6243           tatqa          dir    decreased          increased           0.00 n
  hqa_TAT_10183a57           tatqa          dir    roughly_unchanged  increased           0.00 n
  hqa_TAT_55755d65_masked    tatqa          mask   insufficient_data  insufficient_data   1.00 Y
```
