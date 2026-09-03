"""Assemble HedgeQA-v0.1 from the validated candidate pools.

Also emits the manual-review sheet, because nothing in this collection should
be treated as final on automation alone.

Target composition:
    fintradebench   up to 100, balanced over (lane x gold_commitment)
    financebench    37 yes/no + controlled-insufficient variants
    tatqa           whole validated pool (builder caps + balances the draw)
    finqa           whole validated pool (builder caps + balances the draw)
    convfinqa       whole validated pool

Balancing for FinTradeBench is over (lane x gold_commitment). The pool is
skewed -- most references are committed, and the lanes are 49/50/40 -- so
strict equal-size cells would throw away most of the data. We instead take
proportionally from each cell with a floor, and record the realised
composition rather than claiming a balance we did not achieve.

Selection is deterministic (sorted ids, fixed seed) so the collection can be
rebuilt byte-identically.

Usage: python analysis/hedgeqa_collection/build_collection.py
"""

from __future__ import annotations

import collections
import csv
import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

CAND = REPO / "data" / "hedgeqa" / "candidates"
OUT = REPO / "data" / "hedgeqa" / "hedgeqa_v0_1_candidates.jsonl"
REVIEW = (REPO / "analysis" / "hedgeqa_collection" /
          "hedgeqa_v0_1_manual_review.csv")

SEED = 20260820
# None = take the whole validated pool. The TAT-QA and FinQA builders
# already stratify by gold label when they subsample the corpus, so the
# pool handed here is balanced and can be taken whole.
TARGETS = {"fintradebench": 100, "financebench": None,
           "tatqa": None, "finqa": None, "convfinqa": None}

USABLE = {"auto_validated", "candidate", "manually_validated"}


def _pool(name):
    return [it for it in read_jsonl(CAND / f"{name}_candidates.jsonl")
            if it.validation_status in USABLE]


def _lane_of(it):
    notes = it.notes or ""
    if notes.startswith("lane="):
        return notes.split("=", 1)[1].split(" ")[0]
    return "?"


def select_fintradebench(pool, target, rng):
    """Proportional draw across (lane x gold_commitment) cells."""
    cells = collections.defaultdict(list)
    for it in pool:
        cells[(_lane_of(it), it.gold_commitment)].append(it)
    for v in cells.values():
        v.sort(key=lambda x: x.hedgeqa_id)

    total = sum(len(v) for v in cells.values())
    if total <= target:
        return sorted(pool, key=lambda x: x.hedgeqa_id), dict(
            (f"{k[0]}/{k[1]}", len(v)) for k, v in sorted(cells.items()))

    chosen, realised = [], {}
    for key in sorted(cells):
        v = cells[key]
        take = max(1, round(target * len(v) / total))
        take = min(take, len(v))
        picked = rng.sample(v, take) if take < len(v) else list(v)
        picked.sort(key=lambda x: x.hedgeqa_id)
        chosen.extend(picked)
        realised[f"{key[0]}/{key[1]}"] = take
    # trim/extend to hit the target exactly, deterministically
    chosen.sort(key=lambda x: x.hedgeqa_id)
    if len(chosen) > target:
        chosen = chosen[:target]
    return chosen, realised


def main():
    rng = random.Random(SEED)
    selected, report = [], {}

    for name, target in TARGETS.items():
        pool = _pool(name)
        if not pool:
            report[name] = {"pool": 0, "selected": 0,
                            "note": "source not present"}
            continue
        if name == "fintradebench":
            picked, realised = select_fintradebench(pool, target, rng)
            report[name] = {"pool": len(pool), "selected": len(picked),
                            "cells": realised}
        elif target is None or len(pool) <= target:
            picked = sorted(pool, key=lambda x: x.hedgeqa_id)
            report[name] = {"pool": len(pool), "selected": len(picked)}
        else:
            picked = sorted(rng.sample(pool, target),
                            key=lambda x: x.hedgeqa_id)
            report[name] = {"pool": len(pool), "selected": len(picked)}
        selected.extend(picked)

    selected.sort(key=lambda x: (x.source_benchmark, x.hedgeqa_id))
    n = write_jsonl(selected, OUT)

    # ---------------------------------------------------------- review sheet
    REVIEW.parent.mkdir(parents=True, exist_ok=True)
    with REVIEW.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["hedgeqa_id", "source_benchmark", "source_id", "question",
                    "oracle_evidence_preview", "answer_type", "answer_space",
                    "gold_label", "gold_commitment_auto",
                    "gold_commitment_reviewer1", "gold_commitment_reviewer2",
                    "keep_or_exclude", "exclusion_reason", "notes"])
        for it in selected:
            prev = " ".join((it.oracle_evidence or "").split())[:300]
            w.writerow([it.hedgeqa_id, it.source_benchmark, it.source_id,
                        it.question, prev, it.answer_type,
                        "|".join(it.answer_space), it.gold_label,
                        it.gold_commitment, "", "", "", "",
                        ("CONSTRUCTED - verify the masked evidence really "
                         "cannot answer the question"
                         if it.transformation_type ==
                         "evidence_masked_insufficient" else "")])

    print(f"HedgeQA-v0.1: {n} items -> {OUT.relative_to(REPO)}")
    for k, v in report.items():
        print(f"    {k:16s} {v}")
    print(f"review sheet -> {REVIEW.relative_to(REPO)}")

    by = collections.Counter(it.source_benchmark for it in selected)
    com = collections.Counter(it.gold_commitment for it in selected)
    tr = collections.Counter(it.transformation_type for it in selected)
    print(f"\n  by benchmark : {dict(by)}")
    print(f"  by commitment: {dict(com)}")
    print(f"  by transform : {dict(tr)}")
    return selected


if __name__ == "__main__":
    main()
