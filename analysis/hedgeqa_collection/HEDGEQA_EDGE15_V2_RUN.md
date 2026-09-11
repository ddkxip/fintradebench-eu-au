# Edge set v2 — refilling the two vacated slots

The two defective FinanceBench items were excluded from the strict set, which
left the 15-item edge manifest holding 13. This refills those slots, runs the
replacements, and re-reads the v1 conclusions against the corrected set.

`gemma4:latest`, K=10, rounds 0+1, τ=0.7 — identical to v1. The two new items
took 3.2 min; **2/2 scored, parse_rate 1.0000**. Rows are pooled from
`hedgeqa_edge15_gemma4` (the 13 retained) and `hedgeqa_edge_refill2_gemma4`
(the 2 new); the analyzer refuses to pool runs whose model differs.

```bash
python analysis/hedgeqa_collection/build_edge_refill.py
python analysis/hedgeqa_collection/run_hedgeqa_debate.py \
    --manifest data/hedgeqa/hedgeqa_core_v0_1_edge_refill_2.jsonl \
    --model gemma4:latest --run-id hedgeqa_edge_refill2_gemma4
python analysis/hedgeqa_collection/analyze_edge_run.py \
    --run hedgeqa_edge15_gemma4,hedgeqa_edge_refill2_gemma4 \
    --manifest data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15_v2.jsonl \
    --compare hedgeqa_smoke15_gemma4
```

---

## 1. The gutted pool is exhausted, so the set is diluted

The original selection preferred `evidence_gutted` items, then masked items
both AI reviewers called reachable, then any masked item. Against the strict
file **all three tiers are empty**:

- 8 `evidence_gutted` items survive, and **all 8 are already in the retained
  13** — the excluded pair were the other two;
- exactly **1** masked item has both AI reviewers calling the answer
  reachable, and it is already used.

So the refill had to come from ordinary masked items, and the edge set is now
**8 gutted + 7 filler** rather than 10 + 5. v2 is a weaker stress set than v1,
and the two cannot be compared as though they were the same instrument.

### Which two, and why

Given a free choice among 30 ordinary masked items, the informative pick
answers an open question. v1's headline was that all three FinanceBench edge
items answered confidently; triage showed two were our own defects, leaving
the FinanceBench pattern resting on **one** item. So the rule was mechanical:
*untested, FinanceBench, masked, audit verdict an unqualified KEEP* — which
excludes AMCOR (`KEEP WITH CAVEAT`) and yields exactly two, deterministically.

| item | question |
|---|---|
| `hqa_FB_1da93057_masked` | Did Pfizer grow its PP&E between FY20 and FY21? |
| `hqa_FB_86637d3d_masked` | Was there any drop in Cash & Cash equivalents between FY2023 and Q2 FY2024? |

This preserves the source balance the excluded items had and tests the claim
v1 left standing on a single observation.

## 2. The two new items

| item | round 0 | round 1 | p_nc (r1) | TU | |
|---|---|---|---|---|---|
| `hqa_FB_1da93057_masked` | `no` | `insufficient_data` | 0.50 | 0.856 | **rescued by debate** |
| `hqa_FB_86637d3d_masked` | `no` | `no` | 0.25 | 0.562 | overcommitment |

Both committed to **`no`** at round 0. Neither is a zero-entropy cell.

## 3. Correction: the directional argument against the gutted confound has flipped

v1 offered two arguments that gutted documents do not induce spurious
declining. **One of them no longer holds.**

| group | v1 | **v2** |
|---|---|---|
| `evidence_gutted` | 70% declined (n=10) | **88% declined (n=8)** |
| other masked | 80% declined (n=5) | **71% declined (n=7)** |

v1 reported that gutted items declined *less* — the opposite of the confound's
prediction — and treated that as evidence against it. **That direction was
carried entirely by the two defective items.** With them removed, gutted
items decline *more*, which is weakly consistent with the confound rather
than against it.

The honest reading is that **neither direction means anything at this n**.
88% vs 71% is 7-of-8 against 5-of-7 — one failure versus two. The v1 claim was
over-read in one direction and it would be a repeat of the same error to
over-read the reversal in the other.

What survives is the **rationale evidence**, which was always the stronger
leg: across 300 round-1 decodes, **1 cites document damage**.

## 4. The first genuine damage citation

v1 reported 0/300. v2 reports **1/300**, and it is real, not a regex artifact:

> "…despite the **formatting issue** in the provided context snippet for that
> specific line."

The model is describing a real artifact of our masking: deleting the PP&E
figure left a bare `$` with no number behind it. So the count is no longer
exactly zero, and the honest statement is *1 decode in 300*, not *none*.

Two things worth noting about that decode. First, it is **construction
hygiene**: the mask removed the value and left the currency symbol, which is a
visible tell. Second, the rationale is **confabulated** — it claims "the 2021
value is provided and the 2020 value is also provided" when both were masked,
and then commits. It is not an example of damage *causing* a decline; it is an
example of damage being noticed and then argued past.

## 5. FinanceBench masked items — the full picture

Every FinanceBench masked item ever run, at round 1:

| item | predicted | p_nc | TU | status |
|---|---|---|---|---|
| `hqa_FB_9fc58fab_masked` | `yes` | **0.00** | **−0.000** | **defective, excluded** |
| `hqa_FB_5dbbcec0_masked` | `no` | **0.00** | **−0.000** | **defective, excluded** |
| `hqa_FB_d397e71d_masked` | `no` | 0.05 | 0.199 | clean |
| `hqa_FB_1858a6da_masked` | `yes` | 0.15 | 1.010 | clean |
| `hqa_FB_86637d3d_masked` | `no` | 0.25 | 0.562 | clean |
| `hqa_FB_1da93057_masked` | `insufficient_data` | 0.50 | 0.856 | clean |

**The two defective items are the only zero-entropy FinanceBench cells.**
Every clean item has non-zero entropy.

That materially weakens v1's strongest claim. "Confident overcommitment
invisible to an entropy monitor" was, on FinanceBench, carried by exactly the
two items whose documents genuinely *did* support a confident answer — the
model was confident because the evidence was there. Remove them and no
FinanceBench masked cell is zero-entropy.

Something real remains: **3 of 4 clean items still overcommit** (mean p_nc
0.24), and JnJ at 0.05 is confident by any standard. But the claim is now "an
entropy monitor would catch some of these", not "it sees nothing" — and 4
items support neither as a rate.

A secondary pattern, offered only as a lead: of the 5 clean-item commitments
observed across all runs, **4 were `no`**. Absence of evidence being resolved
as evidence of absence is the obvious hypothesis for a yes/no question, and it
would be worth testing deliberately on a set built for it.

## 6. Combined v2 set

| | v1 (n=15) | **v2 (n=15)** |
|---|---|---|
| declined | 73.3% | **80.0%** (12/15) |
| mean `p_noncommit` | 0.760 | **0.810** |
| zero-entropy cells | 80% | **67%** |
| debate | 73% → 73% (1 rescued, 1 lost) | **73% → 80%** (2 rescued, 1 lost) |

Debate now moves the set, and again in both directions:

| item | round 0 | round 1 | |
|---|---|---|---|
| `hqa_CFQ_4b27112b_masked` | `increased` | `insufficient_data` | rescued |
| `hqa_FB_1da93057_masked` | `no` | `insufficient_data` | rescued |
| `hqa_CFQ_3240be6a_masked` | `insufficient_data` | `increased` | **lost** |

The net gain is real but small, and debate still manufactures an
overcommitment as well as removing two. Report movement in both directions,
never the net.

## 7. Caveats

- **v2 is a weaker set than v1** (8 gutted vs 10) and the two are not
  interchangeable. Any v1→v2 delta mixes a real change in the items with a
  change in what the set is.
- 15 items, subgroups of 8 / 7 / 4. Nothing here is a rate, and §3 is a worked
  example of what happens when a direction at this n is taken seriously.
- Rows are pooled across two runs of identical configuration. The analyzer
  enforces the model match; K, τ and rounds were identical by construction but
  are not machine-checked.
- Single-label gold, one model, one temperature.
- The rationale scan remains coarse, and its absence class is much broader
  than its damage class, so 62% vs 0.3% is not like-for-like.

## 8. Full output

```
=== hedgeqa_edge15_gemma4 + hedgeqa_edge_refill2_gemma4 ===
manifest: data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15_v2.jsonl
items 15   parse_rate mean 1.0000

Every item is a masked variant with gold `insufficient_data`, so
accuracy on this set IS the decline rate. Reported as such.

  declined            80.0% (12/15)
  mean p_noncommit    0.810
  zero-entropy cells  67%

GUTTED vs NON-GUTTED (the comparison the set exists for)
  group                   n  declined   p_nc
  evidence_gutted         8       88%   0.88
  other masked            7       71%   0.73

  for reference, clean masked items in hedgeqa_smoke15_gemma4: n=4 declined 75% p_nc 0.79

WHY DOES IT DECLINE? rationale keyword scan (round 1)
  decodes scanned              300
  cite EVIDENCE ABSENCE        186 (62%)
  cite DOCUMENT DAMAGE         1 (0%)
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
  hqa_FB_1da93057_masked       -   insufficient_data   0.50    Y    6/20    1/20 
  hqa_FB_86637d3d_masked       -   no                  0.25    n   16/20    0/20 
  hqa_FB_d397e71d_masked       Y   no                  0.05    n    9/20    0/20 
  hqa_TAT_5ce27434_masked      Y   insufficient_data   1.00    Y   20/20    0/20 
  hqa_TAT_924db34b_masked      Y   insufficient_data   1.00    Y   15/20    0/20 

DEBATE EFFECT: decline rate 73% -> 80%  rescued 2, lost 1  (n=15)
    hqa_CFQ_3240be6a_masked      insufficient_data  -> increased
    hqa_CFQ_4b27112b_masked      increased          -> insufficient_data
    hqa_FB_1da93057_masked       no                 -> insufficient_data

SAMPLE RATIONALES (first decode of 3 items)
  hqa_CFQ_1279a468_masked:
    The provided data only shows the cumulative shareholder return for Smith (A) Corp, which is a multiplier based on an initial investment of $100. It does not provide the absolute share price at 12/31/16 or the initial sha
  hqa_CFQ_446ed3a5_masked:
    The provided data includes a row for 'smith ( a o ) corp' but only shows a single data point for the base period of 12/31/02. There are no subsequent values for this company through 12/31/2007 to calculate the change in 
  hqa_CFQ_6e99706b_masked:
    The evidence mentions a graph comparing total returns for the S&P 500 index but only provides the starting value of $100 on December 31, 2011. The actual final value for the S&P 500 index on December 31, 2016, is not pro
```
