# HedgeQA edge_smoke_15 — stress run

`gemma4:latest`, K=10, rounds 0+1, tau=0.7, 19.5 min. **15/15 items scored,
parse_rate 1.0000.** Nothing was written back to any collection file.

```bash
python analysis/hedgeqa_collection/run_hedgeqa_debate.py \
    --manifest data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15.jsonl \
    --model gemma4:latest --run-id hedgeqa_edge15_gemma4
python analysis/hedgeqa_collection/analyze_edge_run.py \
    --run hedgeqa_edge15_gemma4 --compare hedgeqa_smoke15_gemma4
```

## 1. Why accuracy is not the headline

Every item in this manifest is a masked variant whose gold is
`insufficient_data`. On a single-label set **accuracy IS the decline rate**,
and a model that declines unconditionally scores 100%. Quoting 73.3% as
"accuracy" would be meaningless-to-flattering, so it is reported as a decline
rate throughout.

## 2. What is actually in the set

| | n | note |
|---|---|---|
| flagged `evidence_gutted` | **10** | the genuine stress cases |
| ordinary masked filler | 5 | all ConvFinQA |

The builder intended to fill the remaining 5 slots with masked items *both*
AI reviewers called reachable while the human did not — the sharpest
disagreement in the collection. Only one kept item met that condition and it
was already taken, so the fill fell through to "any other masked item."
Describing those 5 as stress cases in the manifest was generous; the edge
signal is the 10.

Sources: ConvFinQA 10, FinanceBench 3, TAT-QA 2. FinTradeBench and FinQA
contributed no `evidence_gutted` flags, so neither appears.

`hqa_TAT_924db34b_masked` — excluded by name from the main manifest — is
here, which is where it belongs.

## 3. Headline: the `evidence_gutted` confound is not supported

The worry that motivated this manifest: a model may decline on a gutted
document because the input *looks damaged*, not because the evidence is
*absent*. Right answer, wrong reason — and it would silently inflate any
overcommitment metric computed over masked items.

**Across 300 round-1 decodes, zero cited document damage.**

| rationale cites | decodes | share |
|---|---|---|
| evidence ABSENCE | 167 | 56% |
| document DAMAGE | **0** | **0%** |

The rationales name the specific missing quantity rather than complaining
about the document:

> "…only shows the cumulative shareholder return… It does not provide the
> absolute share price at 12/31/16"

> "…only shows a single data point for the base period of 12/31/02. There are
> no subsequent values… to calculate the change"

And the direction of the group difference is the **opposite** of what the
confound predicts:

| group | n | declined | mean p_nc |
|---|---|---|---|
| `evidence_gutted` | 10 | **70%** | 0.70 |
| other masked | 5 | 80% | 0.87 |
| clean masked (smoke_15, reference) | 4 | 75% | 0.79 |

If gutted documents induced spurious declining, gutted would decline *more*.
It declines slightly less, and all three groups sit within a few points of
each other on 4–10 items — which is to say indistinguishable.

The triage in §4 **strengthens** this. Of the 3 gutted items that did not
decline, 2 did not decline because their evidence genuinely still supported
an answer. Correcting for that, gutted items declined whenever declining was
the right response — so the gutted group shows no spurious declining *and* no
unexplained answering.

### The detector was broken, and that was caught before the number was used

The damage pattern shipped as `\b(truncat|corrupt|…)\b`. The trailing `\b`
meant it never matched **"truncated"** — the commonest damage word in the
vocabulary. A 0/300 would have looked like evidence when it was partly a dead
regex. It was fixed to stem prefixes and verified to fire on six damage
phrasings and on neither of two absence phrasings before the result above was
trusted. A first repair attempt silently no-op'd on heredoc escaping and was
caught by re-reading the file rather than by the test output, which had
implied success.

## 4. Where the model actually fails

**4 overcommitments — and 3 of them are all three FinanceBench items.**

| item | gutted | predicted | p_nc |
|---|---|---|---|
| `hqa_FB_5dbbcec0_masked` | Y | `no` | **0.00** |
| `hqa_FB_9fc58fab_masked` | Y | `yes` | **0.00** |
| `hqa_FB_d397e71d_masked` | Y | `no` | 0.05 |
| `hqa_CFQ_3240be6a_masked` | – | `increased` | 0.50 |

> **CORRECTED — read `HEDGEQA_FB_OVERCOMMIT_TRIAGE.md` before citing this
> section.** The three FinanceBench documents were subsequently read by
> hand. **Only one of the three is a model failure.** On `hqa_FB_9fc58fab`
> the gold is wrong — the question asks whether CVS has ongoing legal
> battles, masking removed only the settlement's dollar amounts, and four
> paragraphs of litigation survive, so the model's `yes` was **correct**. On
> `hqa_FB_5dbbcec0` the line deletion **spliced two sentences into a fluent
> false one**, making a document that had said MGM maintained a $0.01
> dividend through 2022 now assert the opposite; the model's `no` is the
> correct reading of a document we falsified. Only `hqa_FB_d397e71d` is a
> genuine overcommitment. The table above is accurate as scores and
> misleading as behaviour.

On evidence a human reviewer verified cannot support an answer, the model
answered with **near-zero measured uncertainty**. That is the overcommitment
failure mode arriving invisible to an entropy monitor — the paper's central
claim. After triage it is reproduced here on **2 items**
(`hqa_FB_d397e71d_masked` at p_nc 0.05, and `hqa_CFQ_3240be6a_masked` at
0.50, which debate itself created — see §5), not 4.

This also re-reads the section-3 result, though not in the way first written.
Within the gutted group the split is not gutted-vs-not, it is **source**: all
5 ConvFinQA and both TAT-QA gutted items declined (7/7); all 3 FinanceBench
gutted items answered (0/3). The original reading — that this is about
FinanceBench's long filings or its `yes`/`no` space inviting a coin-flip — is
**wrong**. Two of the three answered because the evidence still supported an
answer. The real driver is that FinanceBench holds the collection's only
masked `yes_no` items, and **masking a prose-answerable question by deleting
numbers does not make it unanswerable**. That is a defect in our construction,
not a property of the source or of the model.

## 5. Other observations

- **80% zero-entropy cells** — identical to smoke_15. Every decode from every
  agent agreeing is the norm for this model at tau=0.7, including on the two
  items it got confidently wrong.
- **Debate was net-zero but not inert.** The decline rate is 73% → 73%,
  and it would be wrong to read that as nothing happening: **two items
  swapped, one each way** (1 rescued, 1 lost).

  | item | round 0 | round 1 | |
  |---|---|---|---|
  | `hqa_CFQ_4b27112b_masked` | `increased` | `insufficient_data` | rescued |
  | `hqa_CFQ_3240be6a_masked` | `insufficient_data` | `increased` | **lost** |

  So **debate manufactured one of the four overcommitments.** The one
  non-FinanceBench failure in §4 declined correctly on its own and was
  argued out of it, landing at p_nc 0.50 — the only genuinely split cell in
  the run. Debate as a hedging remedy has to be measured on movement in both
  directions, not on a net rate; here the net is zero and the movement is
  1-for-1. In smoke_15 the same mechanism gave 60.0% → 66.7% (2 rescued,
  1 lost).
- Overall: declined 73.3% (11/15), mean `p_noncommit` 0.760.

## 6. Caveats

- **n=15**, and the interesting subgroups are 10 / 5 / 3. No rate here is
  estimable; the 95% CI on any of them spans most of the unit interval.
- Single-label gold, so the scoring is degenerate by construction (§1).
- One model, one K, one temperature, one seed.
- The keyword scan is a coarse instrument over 2–3 sentence rationales: a
  pointer for reading, not a measurement. Its absence class is also much
  broader than its damage class, so 56% vs 0% is not a like-for-like contrast
  — the load-bearing claim is the zero, which was verified against a working
  detector and an independent unanchored scan.
- The edge set is drawn from the validated 319, whose masked items are all
  constructed. Nothing here is `manually_validated`.

## 7. Full analyzer output

```
=== hedgeqa_edge15_gemma4 ===
items 15   parse_rate mean 1.0000

Every item is a masked variant with gold `insufficient_data`, so
accuracy on this set IS the decline rate. Reported as such.

  declined            73.3% (11/15)
  mean p_noncommit    0.760
  zero-entropy cells  80%

GUTTED vs NON-GUTTED (the comparison the set exists for)
  group                   n  declined   p_nc
  evidence_gutted        10       70%   0.70
  other masked            5       80%   0.87

  for reference, clean masked items in hedgeqa_smoke15_gemma4: n=4 declined 75% p_nc 0.79

WHY DOES IT DECLINE? rationale keyword scan (round 1)
  decodes scanned              300
  cite EVIDENCE ABSENCE        167 (56%)
  cite DOCUMENT DAMAGE         0 (0%)
  (coarse keyword match over 2-3 sentence rationales; a pointer
   for reading, not a measurement)

PER ITEM
  id                           gut pred                p_nc  dec  absence  damage
  hqa_CFQ_1279a468_masked      Y   insufficient_data   1.00    Y    9/20    0/20 
  hqa_CFQ_1d1128f4_masked      -   insufficient_data   1.00    Y   12/20    0/20 
  hqa_CFQ_3240be6a_masked      -   increased           0.50    n    3/20    0/20 
  hqa_CFQ_378d381c_masked      -   insufficient_data   1.00    Y   20/20    0/20 
  hqa_CFQ_446ed3a5_masked      Y   insufficient_data   1.00    Y    8/20    0/20 
  hqa_CFQ_4b27112b_masked      -   insufficient_data   0.85    Y    6/20    0/20 
  hqa_CFQ_64646a26_masked      -   insufficient_data   1.00    Y   17/20    0/20 
  hqa_CFQ_6e99706b_masked      Y   insufficient_data   1.00    Y   17/20    0/20 
  hqa_CFQ_7897a7cc_masked      Y   insufficient_data   1.00    Y   12/20    0/20 
  hqa_CFQ_7f731a74_masked      Y   insufficient_data   1.00    Y   16/20    0/20 
  hqa_FB_5dbbcec0_masked       Y   no                  0.00    n    3/20    0/20 
  hqa_FB_9fc58fab_masked       Y   yes                 0.00    n    0/20    0/20 
  hqa_FB_d397e71d_masked       Y   no                  0.05    n    9/20    0/20 
  hqa_TAT_5ce27434_masked      Y   insufficient_data   1.00    Y   20/20    0/20 
  hqa_TAT_924db34b_masked      Y   insufficient_data   1.00    Y   15/20    0/20 

DEBATE EFFECT: decline rate 73% -> 73%  rescued 1, lost 1  (n=15)
    hqa_CFQ_3240be6a_masked      insufficient_data  -> increased
    hqa_CFQ_4b27112b_masked      increased          -> insufficient_data

SAMPLE RATIONALES (first decode of 3 items)
  hqa_CFQ_1279a468_masked:
    The provided data only shows the cumulative shareholder return for Smith (A) Corp, which is a multiplier based on an initial investment of $100. It does not provide the absolute share price at 12/31/16 or the initial sha
  hqa_CFQ_446ed3a5_masked:
    The provided data includes a row for 'smith ( a o ) corp' but only shows a single data point for the base period of 12/31/02. There are no subsequent values for this company through 12/31/2007 to calculate the change in 
  hqa_CFQ_6e99706b_masked:
    The evidence mentions a graph comparing total returns for the S&P 500 index but only provides the starting value of $100 on December 31, 2011. The actual final value for the S&P 500 index on December 31, 2016, is not pro
```
