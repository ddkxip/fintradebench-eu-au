"""Audit the built masked items against the two new guards.

    python analysis/hedgeqa_collection/audit_masked_items.py

The guards in `masking.py` gate FUTURE construction. The reviewed collection
is pinned, so this asks the retrospective question instead: how many items
already in the strict set would the guards have refused, and does the MGM
splice defect appear anywhere else?

Two instruments, with different strengths:

* `classify_question` runs on the question text and is exact -- the same code
  that will gate construction.
* `splice_risk_from_removed` is ONE-SIDED. The original document is gone, so
  it can only see that a removed prose line began lower-case (i.e. continued a
  sentence). It flags risk; only reading the item decides.

Nothing is modified. This prints a report.
"""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from hedgeqa_schema import read_jsonl  # noqa: E402
from masking import (classify_question, is_normally_cased,  # noqa: E402
                     splice_risk_from_removed)

STRICT = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_strict.jsonl"
MASKED = "evidence_masked_insufficient"

# The five FinanceBench masked items that remain, with the hand-read verdict
# recorded in HEDGEQA_FB_OVERCOMMIT_TRIAGE.md and extended here.
FB_REVIEW = {
    "hqa_FB_1da93057_masked": dict(
        numeric="yes -- PP&E balances for FY20 and FY21 from a balance sheet",
        prose="no -- the surviving text is a balance-sheet table",
        corrupt="no -- deleted rows are numeric, not sentences",
        keep="KEEP"),
    "hqa_FB_86637d3d_masked": dict(
        numeric="yes -- cash balances at two dates from a table",
        prose="no -- surviving text is a non-GAAP reconciliation table",
        corrupt="no -- deleted rows are numeric, not sentences",
        keep="KEEP"),
    "hqa_FB_7cc358e4_masked": dict(
        numeric="yes -- gross margin from net sales and gross profit",
        prose="PARTLY -- the second clause invites a prose answer",
        corrupt="no -- deleted rows are numeric, not sentences",
        keep="KEEP WITH CAVEAT"),
    "hqa_FB_d397e71d_masked": dict(
        numeric="yes -- 2022 adj-EPS growth vs 2023 guidance",
        prose="no -- both growth figures are gone",
        corrupt="no, but the document is visibly cut mid-clause",
        keep="KEEP"),
    "hqa_FB_1858a6da_masked": dict(
        numeric="yes -- FCF conversion from net income and operating cash flow",
        prose="no -- both years' inputs are gone",
        corrupt="no -- deleted rows are numeric, not sentences",
        keep="KEEP"),
}


def main():
    items = read_jsonl(STRICT)
    masked = [i for i in items if i.transformation_type == MASKED]
    print(f"strict set {len(items)}   masked {len(masked)}\n")

    print("=" * 78)
    print("A. CATEGORY GATE applied retrospectively to every masked item")
    print("=" * 78)
    by_cat, refused = {}, []
    for i in masked:
        c = classify_question(i.question)
        by_cat.setdefault((i.source_benchmark, c["category"]), []).append(i)
        if not c["maskable"]:
            refused.append((i, c))
    print(f"  {'source':14s} {'category':14s} {'n':>3s}")
    for (src, cat), v in sorted(by_cat.items()):
        print(f"  {src:14s} {cat:14s} {len(v):3d}")
    print(f"\n  would be REFUSED by the gate on question category alone: "
          f"{len(refused)}/{len(masked)}")
    for i, c in sorted(refused, key=lambda x: x[0].hedgeqa_id):
        print(f"    {i.hedgeqa_id:26s} {c['category']:12s} "
              f"cue={c['cues'][0] if c['cues'] else '-'}")
    print("\n  NOTE: the directional items carry a program/derivation naming")
    print("  the operands, which discharges the gate, so a refusal here is")
    print("  only decisive for FinanceBench, which has no such artifact.")

    print("\n" + "=" * 78)
    print("B. SPLICE RISK sweep (one-sided; flags risk, does not prove)")
    print("=" * 78)
    flagged = []
    for i in masked:
        rm = [x for x in (i.masked_content or "").split("|||") if x.strip()]
        hits = splice_risk_from_removed(rm, context=i.oracle_evidence)
        if hits:
            flagged.append((i, hits))
    cased = [i for i in masked if is_normally_cased(i.oracle_evidence)]
    print(f"  normally-cased documents (heuristic applies): "
          f"{len(cased)}/{len(masked)}   abstained on the rest")
    print(f"  of those, items with a removed prose line starting lower-case: "
          f"{len(flagged)}/{len(cased)}")
    for i, hits in sorted(flagged, key=lambda x: x[0].hedgeqa_id):
        print(f"\n    {i.hedgeqa_id} ({i.source_benchmark})")
        for h in hits[:2]:
            print(f"      ...{h}")

    print("\n" + "=" * 78)
    print("C. REMAINING FINANCEBENCH MASKED ITEMS -- hand-read audit")
    print("=" * 78)
    fb = [i for i in masked if i.source_benchmark == "financebench"]
    unexpected = {i.hedgeqa_id for i in fb} ^ set(FB_REVIEW)
    if unexpected:
        raise SystemExit(f"[ABORT] audit table and strict set disagree on "
                         f"which FinanceBench masked items exist: "
                         f"{sorted(unexpected)}")
    for i in sorted(fb, key=lambda x: x.hedgeqa_id):
        r = FB_REVIEW[i.hedgeqa_id]
        c = classify_question(i.question)
        print(f"\n  {i.hedgeqa_id}  [gate: {c['category']}]")
        print(f"    Q                : {i.question[:96]}")
        print(f"    numeric/table-dep: {r['numeric']}")
        print(f"    prose answers it : {r['prose']}")
        print(f"    mask corrupts    : {r['corrupt']}")
        print(f"    verdict          : {r['keep']}")
    print(f"\n  all {len(fb)} retained; none re-admitted; none created.")


if __name__ == "__main__":
    main()
