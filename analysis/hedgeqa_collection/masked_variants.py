"""Build controlled-insufficient variants for the directional benchmarks.

Shared by build_from_tatqa / build_from_finqa / build_from_convfinqa so the
construction and its guards live in one place.

## Why these are drawn from UNUSED pool items

A masked variant could be paired with its own natural item (same evidence,
opposite gold), which is what the FinanceBench builder does -- there, the
pairing is the point, because 37 items is too few to spend on anything else.

Here the eligible pools are large (2,697 / 1,385 / 930), so variants are
drawn from items NOT selected as natural items. Pairing would put two rows
sharing one evidence document into the collection, and their errors would be
correlated; anything computing a CI over pooled items would then understate
its width. Independent draws avoid that for free.

## What the gold means

The directional answer space already contains `insufficient_data` as a
non-committal label, so a masked variant needs no new label -- only a
different gold. Removing the rows carrying the program's operands means the
direction can no longer be derived, so `insufficient_data` is correct BY
CONSTRUCTION.

As with every masked item: structurally valid is not the same as correct.
These are never auto-promoted and require human review.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import HedgeQAItem, make_id
from masking import mask_directional
from transforms import DIRECTIONAL_NONCOMMIT, DIRECTIONAL_SPACE

MIN_REMAINING_CHARS = 200


def build_masked_variants(pool, benchmark, target, stats=None):
    """Attempt a masked variant for each (source_id, question, evidence,
    program, notes) tuple in `pool`, stopping at `target` successes.

    `pool` entries are dicts with keys: source_id, question, evidence,
    program, provenance, original_question.
    """
    out = []
    reasons = {}
    for rec in pool:
        if len(out) >= target:
            break
        res = mask_directional(rec["evidence"], rec["program"],
                               question=rec["question"])
        if not res["ok"]:
            key = res["reason"].split("(")[0].strip()[:60]
            reasons[key] = reasons.get(key, 0) + 1
            continue
        masked = res["masked"].strip()
        if len(masked) < MIN_REMAINING_CHARS:
            reasons["masked evidence too thin"] = \
                reasons.get("masked evidence too thin", 0) + 1
            continue

        out.append(HedgeQAItem(
            hedgeqa_id=make_id(benchmark, rec["source_id"], "masked"),
            source_benchmark=benchmark,
            source_id=rec["source_id"],
            question=rec["question"],
            oracle_evidence=masked,
            evidence_provenance=(rec["provenance"] +
                                 " | rows carrying the derivation's operands "
                                 "REMOVED"),
            answer_type="directional_change",
            answer_space=list(DIRECTIONAL_SPACE),
            gold_label="insufficient_data",
            noncommit_labels=list(DIRECTIONAL_NONCOMMIT),
            gold_commitment="noncommitted",
            transformation_type="evidence_masked_insufficient",
            requires_rag=False,
            validation_status="candidate",
            schema_confidence=0.6,
            original_question=rec["original_question"],
            derivation=(
                "Controlled-insufficient variant. The source states the "
                f"arithmetic explicitly ({rec['program']!r}); the evidence "
                f"rows carrying its operands ({res['operands'][:6]}) were "
                "removed, and coverage plus proportion checks confirmed none "
                "survives and the document is not gutted. With those rows "
                "gone the direction cannot be derived, so insufficient_data "
                "is correct by construction. Question text is unchanged."),
            masked_content=" ||| ".join(x.strip() for x in res["removed"])[:4000],
            notes="CONSTRUCTED ITEM -- analyse separately from natural items; "
                  "REQUIRES MANUAL REVIEW before use"))

    if stats is not None:
        stats["masked_included"] = len(out)
        for k, v in sorted(reasons.items(), key=lambda x: -x[1])[:5]:
            stats[f"masked_skip:{k}"] = v
    return out
