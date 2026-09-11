# HedgeQA-Core — review finalisation

Two reviewer decisions applied after the human review closed. Both inputs
were backed up first; neither the candidate JSONL nor the AI response files
were modified.

**Nothing is `manually_validated`.** The promotion rule is documented and
implemented, but not run — see below.

---

## 1. Masked-variant cleanup

Full detail in `HEDGEQA_MASKED_CLEANUP.md`. Applied by
`apply_masked_cleanup.py`.

| | items |
|---|---|
| masked before cleanup | 93 |
| masked excluded (human-failed) | **44 (47%)** |
| masked kept (human-valid) | **49** |
| natural excluded (human `exclude`) | 5 |
| **validated collection** | **319** |

Output: `data/hedgeqa/hedgeqa_core_v0_1_validated_candidates.jsonl`

The keep rule requires all five of: `masked_variant_valid = yes`,
`reviewer_gold_label ∈ noncommit_labels`, `evidence_sufficient_for_gold =
no`, `keep_or_exclude = keep`, and no reconstructibility language in `notes`.
`unclear` excludes — an unconfirmed suspicion of a leak is treated as a leak.

In this data all three structured signals agreed on every one of the 93
items (49 held / 44 failed), so the redundant rules are a consistency check
passing rather than dead weight.

### One trap worth recording

The review sheet pre-filled every masked item's `notes` with the boilerplate
*"CONSTRUCTED GOLD - verify the masked evidence truly cannot answer the
question."* A naive keyword scan for reconstructibility language matches that
text and would have **excluded all 93 items on the strength of their own
instructions**. The matcher strips the boilerplate before scanning, and that
behaviour is asserted directly.

### Corroboration

Of the 44 exclusions, **at least one AI reviewer independently agreed on all
44**, and both agreed on 37. These are not one reader's idiosyncrasy.

### Leak routes

The human recorded no flags — the app offered them but the structured fields
carried the verdict. The routes below come from the AI reviewers' flags on
the same items:

| flag | occurrences |
|---|---|
| `answer_reconstructible` | 60 |
| `total_minus_components` | 11 |
| `direction_stated_in_prose` | 2 |

**`total_minus_components` is a route `masking.py` already guards, and the
automated check passed every one of these items.** The guard tests
pipe-delimited table columns; it misses the same arithmetic when the figures
sit in prose, span two tables, or need one more step. That is the concrete
gap to close before constructing any more masks.

### Two flags on the KEPT set

- **16 kept items were flagged `evidence_gutted`** by an AI reviewer. A
  gutted document is a different defect from a leak: a model may decline
  because the input looks damaged rather than because the evidence is
  absent, which confounds the exact measurement these items exist for. They
  pass the human rule and are kept, but they should be read.
- **1 kept item had both AI reviewers call the answer reachable** while the
  human did not. The human's judgement governs; a unanimous AI dissent is
  still the cheapest place to look for a missed route.

---

## 2. Commitment inconsistencies resolved

Backed up to
`hedgeqa_core_v0_1_manual_review_completed.pre_finalization_backup.csv`.

Rule applied: `unsupportive → committed`, `mixed → noncommitted`.

| item | label | was | now |
|---|---|---|---|
| `hqa_FTB_6f71b24d` | `unsupportive` | noncommitted | **committed** |
| `hqa_FTB_8c3f38fa` | `mixed` | committed | **noncommitted** |
| `hqa_FTB_90f40b4c` | `mixed` | committed | **noncommitted** |

The rule was applied to **every** row carrying those labels — 5
`unsupportive` and 6 `mixed` — and only these 3 needed changing; the other 8
already complied. So the rule matches what the schema enforces globally
rather than being a per-row patch, which is the condition the instruction
anticipated. Each changed row records the reason in its `notes`.

**Commitment/label inconsistencies remaining: 0.**

---

## 3. Agreement after finalisation

Reran on all 368 reviewed items (the review record, including excluded ones).

### `gold_commitment`

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 368 | 70.9% | 0.395 |
| human vs ChatGPT | 368 | 79.1% | 0.469 |
| **Gemini vs ChatGPT** | 368 | 82.6% | **0.651** |

### `keep_or_exclude` — unchanged, still at chance

| comparison | n | raw | kappa |
|---|---|---|---|
| human vs Gemini | 368 | 67.1% | 0.037 |
| human vs ChatGPT | 368 | 66.3% | −0.010 |
| Gemini vs ChatGPT | 368 | 75.3% | 0.443 |

Promotion classes: `strong_keep` 180, `review_needed` 106, `exclude` 82.

### Secondary view — the 319 validated items only

| field | human–Gemini | human–ChatGPT | Gemini–ChatGPT |
|---|---|---|---|
| `gold_label` (raw) | 64.3% | 71.5% | **80.3%** |
| `gold_commitment` (κ) | 0.373 | 0.475 | **0.679** |

Promotion within the validated set: `strong_keep` 180, `review_needed` 99,
`exclude` 40.

**The pattern is unchanged and slightly stronger after cleanup:** the two AI
reviewers still agree with each other far more than either agrees with the
human (κ 0.679 vs 0.373 / 0.475). Removing the broken masked items did not
bring the AI readers closer to the human, which is what you would expect if
their divergence is a property of the readers rather than of the items.

Finding 1 also survives: on the 270 validated natural items the human
declines 5.9% and the pipeline 6.3%, against Gemini **41.5%** and ChatGPT
**27.8%**.

---

## 4. Promotion rule — documented, not applied

`apply_masked_cleanup.py --promote` will set `manually_validated`, and
writes the reason into each item's `notes`. It was **not** run.

| family | promoted? | why |
|---|---|---|
| masked | yes, under the five KEEP conditions | a human confirmed the constructed insufficiency, which is precisely the claim the item makes |
| natural | **no** | a human agreeing with a reference label is weaker than a human constructing one, and the label came from the source benchmark rather than from this review |

If you want the 49 masked items promoted, run it with `--promote`. The
natural items need a separate decision about what evidence would license
promoting a label this review only concurred with.

---

## 5. Collection after finalisation

**319 items.**

| source | items |
|---|---|
| fintradebench | 96 |
| finqa | 63 |
| convfinqa | 59 |
| tatqa | 58 |
| financebench | 43 |

| transformation | items |
|---|---|
| numeric_to_directional | 138 |
| none | 132 |
| evidence_masked_insufficient | 49 |

| gold_commitment | items |
|---|---|
| committed | 253 |
| noncommitted | 66 |

Non-committal gold is **66/319 = 20.7%** (was 112/368 = 30.4%). **49 of those
66 are constructed** masked items; the other **17 are natural, all in
FinTradeBench**.

### The honest cost

Removing half the masked variants removed half the constructed non-committal
stratum. Overcommitment and wrong-non-committal-type now rest on a smaller
base, and outside FinTradeBench still entirely on constructed items — just
fewer, better-verified ones. The metric is narrower and the items behind it
are trustworthy. That is the correct trade, but it should be stated whenever
those two modes are reported.

---

## Recommended next steps

1. **Close the `total_minus_components` guard gap** in `masking.py` before
   building more masks — 11 flags on items the automated check passed.
2. **Read the 16 `evidence_gutted` kept items.** They may need re-masking
   rather than exclusion.
3. **Decide on promotion.** The masked rule is ready; the natural one needs
   a criterion.
4. **When reporting**, give the per-benchmark split and say that outside
   FinTradeBench the non-committal stratum is wholly constructed.
