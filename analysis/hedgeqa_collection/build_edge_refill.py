"""Refill the two edge slots vacated by the defective FinanceBench items.

    python analysis/hedgeqa_collection/build_edge_refill.py

Outputs
    data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15_v2.jsonl   (15: 13 + 2)
    data/hedgeqa/hedgeqa_core_v0_1_edge_refill_2.jsonl      (the 2 to run)

The v1 edge manifest is NOT overwritten: the completed `hedgeqa_edge15_gemma4`
run is keyed to its ids, and silently changing it would break that link.

## The gutted pool is exhausted

The original selection preferred `evidence_gutted` items, then masked items
both AI reviewers called reachable, then any masked item. Against the strict
file all three tiers are empty:

* 8 `evidence_gutted` items survive, and **all 8 are already** in the retained
  13 (the other 2 were the excluded items);
* exactly 1 masked item has both AI reviewers calling the answer reachable,
  and it is already used.

So the refill can only come from ordinary masked items, and the refilled set
is **8 gutted + 7 filler** rather than 10 + 5. The edge character is diluted,
and no run over it can be compared to v1 as though the sets were equivalent.

## Why FinanceBench, and which two

Given a free choice among 30 ordinary masked items, the informative pick is
the one that answers an open question. The v1 run's headline was that all
three FinanceBench edge items answered confidently; triage showed two of those
were our own defects. That leaves the FinanceBench pattern resting on ONE item
(JnJ), and the obvious test is the FinanceBench masked items that have never
been run.

Three are untested. `HEDGEQA_MASKING_CATEGORY_GATE.md` §4 records a hand-read
verdict for each, and the selection rule here is mechanical: **untested,
FinanceBench, masked, audit verdict KEEP** -- which excludes AMCOR
(`KEEP WITH CAVEAT`, its second clause is answerable from general knowledge
regardless of masking) and yields exactly two items, deterministically.

This keeps the source balance the excluded items had (both FinanceBench) and
tests the one claim the triage left standing on a single observation.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

DATA = REPO / "data" / "hedgeqa"
STRICT = DATA / "hedgeqa_core_v0_1_validated_strict.jsonl"
EDGE_V1 = DATA / "hedgeqa_core_v0_1_edge_smoke_15.jsonl"
SMOKE = DATA / "hedgeqa_core_v0_1_smoke_15.jsonl"
EDGE_V2 = DATA / "hedgeqa_core_v0_1_edge_smoke_15_v2.jsonl"
REFILL = DATA / "hedgeqa_core_v0_1_edge_refill_2.jsonl"

# From HEDGEQA_MASKING_CATEGORY_GATE.md section 4. Only unqualified KEEPs are
# eligible; AMCOR's caveat disqualifies it.
AUDIT_KEEP = {"hqa_FB_1da93057_masked", "hqa_FB_86637d3d_masked"}
MASKED = "evidence_masked_insufficient"


def main():
    strict = {i.hedgeqa_id: i for i in read_jsonl(STRICT)}
    edge_v1 = read_jsonl(EDGE_V1)
    smoke_ids = {i.hedgeqa_id for i in read_jsonl(SMOKE)}

    retained = [i for i in edge_v1 if i.hedgeqa_id in strict]
    vacated = [i.hedgeqa_id for i in edge_v1 if i.hedgeqa_id not in strict]
    if len(vacated) != 2:
        raise SystemExit(f"[ABORT] expected 2 vacated slots, found "
                         f"{len(vacated)}: {vacated}")

    used = {i.hedgeqa_id for i in retained} | smoke_ids | set(vacated)
    pool = sorted(h for h, i in strict.items()
                  if i.source_benchmark == "financebench"
                  and i.transformation_type == MASKED
                  and h not in used
                  and h in AUDIT_KEEP)
    if len(pool) != 2:
        raise SystemExit(
            f"[ABORT] selection rule yielded {len(pool)} items, not 2: {pool}. "
            f"Refusing to guess a refill.")

    refill = [strict[h] for h in pool]
    combined = retained + refill
    if len(combined) != 15:
        raise SystemExit(f"[ABORT] v2 has {len(combined)} items, not 15")
    ids = [i.hedgeqa_id for i in combined]
    if len(set(ids)) != len(ids):
        raise SystemExit("[ABORT] duplicate ids in v2")
    if set(ids) & smoke_ids:
        raise SystemExit(f"[ABORT] v2 overlaps smoke_15: "
                         f"{sorted(set(ids) & smoke_ids)}")

    write_jsonl(combined, EDGE_V2)
    write_jsonl(refill, REFILL)

    print(f"vacated : {vacated}")
    print(f"retained: {len(retained)}")
    print(f"refill  : {[i.hedgeqa_id for i in refill]}")
    for i in refill:
        print(f"    {i.hedgeqa_id} | {i.source_benchmark} | gold={i.gold_label}")
        print(f"      Q: {i.question[:90]}")
    print(f"v2      : {len(combined)} items -> {EDGE_V2.name}")
    print(f"to run  : {len(refill)} items -> {REFILL.name}")


if __name__ == "__main__":
    main()
