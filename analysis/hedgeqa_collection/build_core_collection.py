"""Assemble HedgeQA-Core-v0.1 -- a manually reviewable subset.

The full v0.1 collection (1,658 items) is internally consistent but not
validated, and reviewing all of it by hand is not realistic. This picks a
300-400 item core that is small enough to review completely and still
supports every hedging metric per benchmark.

Selection preference, applied within each stratum:

  1. an evidence document not already used by a selected item (items sharing
     a document are correlated, and the full collection has 36.7% sharing);
  2. higher schema_confidence;
  3. shorter oracle_evidence -- cheaper to read, and it keeps context length
     from drifting apart across benchmarks, which would otherwise confound
     source with prompt size;
  4. hedgeqa_id, purely to make ties deterministic.

Natural and masked items are selected separately and stay separable by
`transformation_type`, because a masked item's gold is CONSTRUCTED and must
never be pooled into a natural non-commitment rate.

Nothing here marks anything `manually_validated`. This prepares a review
set; the review has not happened.

Usage: python analysis/hedgeqa_collection/build_core_collection.py
"""

from __future__ import annotations

import collections
import csv
import hashlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

SRC = REPO / "data" / "hedgeqa" / "hedgeqa_v0_1_candidates.jsonl"
OUT = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
REVIEW = (REPO / "analysis" / "hedgeqa_collection" /
          "hedgeqa_core_v0_1_manual_review.csv")

MASKED = "evidence_masked_insufficient"

# (natural target, masked target). None = take every natural item available.
TARGETS = {
    "fintradebench": (None, 0),
    "financebench": (36, 23),
    "tatqa": (50, 25),
    "finqa": (50, 25),
    "convfinqa": (40, 20),
}


def evidence_hash(text: str) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:12]


def _pick(pool, target, used_hashes):
    """Greedy draw honouring the preference order above."""
    if target is None or target >= len(pool):
        chosen = sorted(pool, key=lambda x: x.hedgeqa_id)
        for i in chosen:
            used_hashes.add(evidence_hash(i.oracle_evidence))
        return chosen

    remaining = list(pool)
    chosen = []
    while remaining and len(chosen) < target:
        remaining.sort(key=lambda x: (
            evidence_hash(x.oracle_evidence) in used_hashes,   # False first
            -float(x.schema_confidence or 0.0),
            len(x.oracle_evidence),
            x.hedgeqa_id))
        pick = remaining.pop(0)
        chosen.append(pick)
        used_hashes.add(evidence_hash(pick.oracle_evidence))
    return sorted(chosen, key=lambda x: x.hedgeqa_id)


def _stratified(pool, target, used_hashes, key=lambda i: i.gold_label):
    """Equal-as-possible draw across label strata, scarce classes first."""
    if target is None or target >= len(pool):
        return _pick(pool, None, used_hashes)
    buckets = collections.defaultdict(list)
    for i in pool:
        buckets[key(i)].append(i)
    order = sorted(buckets, key=lambda k: len(buckets[k]))
    chosen, remaining_target = [], target
    for n, k in enumerate(order):
        share = remaining_target // (len(order) - n)
        take = min(share, len(buckets[k]))
        got = _pick(buckets[k], take, used_hashes)
        chosen.extend(got)
        remaining_target -= len(got)
    return sorted(chosen, key=lambda x: x.hedgeqa_id)


def _lane(it):
    n = it.notes or ""
    return n.split("lane=")[1].split(" ")[0] if "lane=" in n else "?"


def main():
    items = read_jsonl(SRC)
    used_hashes = set()
    selected, report = [], {}

    for bench, (tnat, tmask) in TARGETS.items():
        sub = [i for i in items if i.source_benchmark == bench]
        nat = [i for i in sub if i.transformation_type != MASKED]
        msk = [i for i in sub if i.transformation_type == MASKED]

        if bench == "fintradebench":
            # Priority: every natural non-committal gold first (there are only
            # 19, and they are the only natural items that can exercise
            # overcommitment here), then a lane-balanced draw over the rest.
            nc = [i for i in nat if i.gold_commitment == "noncommitted"]
            rest = [i for i in nat if i.gold_commitment != "noncommitted"]
            pick_nc = _pick(nc, None, used_hashes)
            budget = None if tnat is None else max(0, tnat - len(pick_nc))
            pick_rest = _stratified(rest, budget, used_hashes, key=_lane)
            got_nat = sorted(pick_nc + pick_rest, key=lambda x: x.hedgeqa_id)
        else:
            got_nat = _stratified(nat, tnat, used_hashes)

        got_msk = _pick(msk, tmask if tmask else 0, used_hashes) if tmask else []
        selected.extend(got_nat + got_msk)
        report[bench] = {
            "natural": len(got_nat), "masked": len(got_msk),
            "natural_labels": dict(collections.Counter(
                i.gold_label for i in got_nat)),
        }

    selected.sort(key=lambda x: (x.source_benchmark, x.transformation_type,
                                 x.hedgeqa_id))
    n = write_jsonl(selected, OUT)

    # ------------------------------------------------------- review sheet
    # Ordered by review priority so a reviewer working top-down meets the
    # highest-risk items first: constructed golds, then non-committal golds,
    # then transformed items, then the rest.
    def prio(i):
        return (0 if i.transformation_type == MASKED else
                1 if i.gold_commitment == "noncommitted" else
                2 if i.transformation_type != "none" else 3,
                i.source_benchmark, i.hedgeqa_id)

    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    with REVIEW.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "hedgeqa_id", "source_benchmark", "source_id", "evidence_hash",
            "transformation_type", "answer_type", "question",
            "original_question", "oracle_evidence_preview", "gold_label_auto",
            "answer_space", "noncommit_labels", "gold_commitment_auto",
            "reviewer_gold_label", "reviewer_gold_commitment",
            "evidence_sufficient_for_gold", "transformation_valid",
            "masked_variant_valid", "keep_or_exclude", "exclusion_reason",
            "notes"])
        for i in sorted(selected, key=prio):
            prev = " ".join((i.oracle_evidence or "").split())[:400]
            w.writerow([
                i.hedgeqa_id, i.source_benchmark, i.source_id,
                evidence_hash(i.oracle_evidence), i.transformation_type,
                i.answer_type, i.question, i.original_question or "", prev,
                i.gold_label, "|".join(i.answer_space),
                "|".join(i.noncommit_labels), i.gold_commitment,
                "", "", "", "",
                "not_applicable" if i.transformation_type != MASKED else "",
                "", "",
                ("CONSTRUCTED GOLD - verify the masked evidence truly cannot "
                 "answer the question" if i.transformation_type == MASKED
                 else "")])

    print(f"HedgeQA-Core-v0.1: {n} items -> {OUT.relative_to(REPO)}")
    for b, r in report.items():
        print(f"    {b:14s} natural={r['natural']:3d} masked={r['masked']:3d}")
    print(f"review sheet -> {REVIEW.relative_to(REPO)}")

    hashes = [evidence_hash(i.oracle_evidence) for i in selected]
    c = collections.Counter(hashes)
    print(f"\n  distinct evidence documents: {len(c)} / {len(selected)} items")
    print(f"  items sharing a document:     {sum(v for v in c.values() if v > 1)}")
    print(f"  by commitment: {dict(collections.Counter(i.gold_commitment for i in selected))}")
    print(f"  by transform : {dict(collections.Counter(i.transformation_type for i in selected))}")
    return selected


if __name__ == "__main__":
    main()
