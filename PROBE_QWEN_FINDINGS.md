# PROBE_QWEN_FINDINGS — the hedge attractor is a *non-commitment attractor*, and it is not model-specific

Full tables: results/probe_qwen_summary.md. Probe: 8 judgment questions,
gemma4, K=10, R0, two arms vs main_pilot20 baseline. Replication: all 16
questions, qwen3:8b, K=10/20, R0+R1. Pilot scale throughout (n=8/16) —
directions and mechanisms, not powered claims.

## 1. Probe Arm D (hedge labels removed): the model routes around the menu

Removing `mixed`/`conditional` did **not** release directional
commitment — on 6/8 questions the model migrated to `insufficient_data`,
the remaining non-directional option. Hedge rate went 0.875 → 0 by
construction, but directional-gold accuracy moved only 0/4 → 1/4 (FT12).
**The attractor is not the specific labels; it is non-commitment
itself.** Menu surgery alone cannot break it — the model finds whatever
abstention-shaped cell exists.

## 2. Arm J (justification requirement): dilutes, doesn't break

Hedge rate 0.875 → 0.375, total uncertainty rises (TU 0.16 → 0.24),
directional-gold accuracy 0 → 1/4. Some decodes commit, but F11 still
lands on `mixed` and FT2 on `conditional`. Instruction pressure shifts
mass at the margin.

## 3. Forced choice reveals hedging is *partly* information-bearing

On hedge-gold questions under Arm D (where a genuinely conditional gold
*should* produce split decodes): FT25 shows the largest uncertainty in
the whole program so far (TU_norm 0.51, real disagreement), F1 moderate
(0.30); FT1/FT31 collapse confidently to `insufficient_data`. So the
original hedging carried real two-sidedness on ~half the items and pure
style on the rest. Both probe arms also *raise* EU/AU overall
(TU 0.16 → 0.20/0.24): the attractor labels had been absorbing
probability mass that redistributes once they're constrained.

## 4. qwen3:8b replication: the regime is shared, not a gemma4 quirk

| | EU (R0/R1) | degenerate rows | hedge rate | acc final | dAU | dEU |
|---|---|---|---|---|---|---|
| gemma4 | .032/.034 | 44%/75% | .44 | .625 | −.087 | +.002 |
| qwen3:8b | .028/.031 | 69%/81% | .38 | .688 | −.041 | +.004 |

- EU floor ≈ 0.03 in both models; degeneracy even *higher* in qwen.
- Lane accuracy pattern replicates (F .86/.86, FT .33/.50, T .67/.67).
- **Debate-reduces-AU-not-EU replicates in direction across models.**
- One jewel in the qwen data: T10 final round has **EU 0.387 with
  AU 0.000** — both agents internally certain and disagreeing (a pure
  between-framework dispute), the first clean nonzero-EU observation.
  EU exists in the machinery; the judgment-question attractor just
  usually pre-empts it.

## 5. What this means for the paper

The finding sharpens into something better than the original RQ3
hypothesis: **small open-weights financial reasoners express uncertainty
categorically, not distributionally** — they converge with high
self-consistency on non-committal *labels* instead of spreading
probability across directional ones. Consequences:

1. Label-distribution EU/AU *understates* uncertainty unless
   non-commitment labels are modeled as their own outcome class — the
   analysis must report P(non-committal) alongside TU/AU/EU as a
   first-class quantity ("categorical uncertainty").
2. The FT failure mode is now mechanistic: directional golds + a
   non-commitment attractor ⇒ systematic hedge-collisions.
3. False consensus (CAGE-CAL sense) is doubly pre-empted: consensus
   forms *before* debate, *on abstention-shaped labels*.
4. Cross-model replication (2 families) moves this from anecdote to
   candidate headline; the full-150 run + a larger/API model arm
   (gemini-3.1-pro subset) decide whether capability breaks the
   attractor.

## 6. Next steps (updated)

1. Add `p_noncommit` (mass on mixed/conditional/insufficient_data/
   none_clear) to the aggregator output and analysis plan as a headline
   quantity.
2. Scale schemas to 150 with a per-question `noncommit_labels` field.
3. Full E-A′ on gemma4 + qwen (both now validated end-to-end), with the
   Arm-J instruction as a pre-registered secondary condition.
4. One API-model subset (gemini-3.1-pro, ~16 questions) to test the
   capability hypothesis before committing to the story.
5. Housekeeping done this session: runner emits rectangular rows for
   mixed-scoreability runs; PRD flag has an absolute EU floor.
