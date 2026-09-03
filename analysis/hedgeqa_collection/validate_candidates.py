"""Run every schema validator over the candidate files.

Items that pass all checks are promoted candidate -> auto_validated.
Items that fail are marked excluded with the FIRST failing check as the
reason -- never silently repaired, because a repaired item is one whose
defect nobody sees.

`auto_validated` means "structurally sound", NOT "correct". In particular
controlled-insufficient variants can be structurally perfect and still have
a wrong gold label; they are held at `candidate` and routed to human review
regardless of how many checks they pass.

Usage: python analysis/hedgeqa_collection/validate_candidates.py [--write]
       (without --write it reports only and changes nothing)
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import (read_jsonl, validate,  # noqa: E402
                            write_jsonl)

CAND = REPO / "data" / "hedgeqa" / "candidates"
FILES = ["fintradebench_candidates.jsonl", "financebench_candidates.jsonl",
         "tatqa_candidates.jsonl", "finqa_candidates.jsonl",
         "convfinqa_candidates.jsonl"]

# Never auto-promote these: structural validity does not establish that the
# constructed gold label is right.
NEVER_AUTO = {"evidence_masked_insufficient"}


def run(write: bool = False):
    grand = collections.Counter()
    for name in FILES:
        path = CAND / name
        items = read_jsonl(path)
        if not items:
            print(f"{name:36s} (empty — source not present)")
            continue
        fail_reasons = collections.Counter()
        promoted = held = excluded = 0
        for it in items:
            if it.validation_status == "excluded":
                excluded += 1
                continue
            results = validate(it)
            bad = [(n, m) for n, ok, m in results if not ok]
            if bad:
                n, m = bad[0]
                it.validation_status = "excluded"
                it.exclusion_reason = f"{n}: {m}"
                fail_reasons[n] += 1
                excluded += 1
            elif it.transformation_type in NEVER_AUTO:
                it.validation_status = "candidate"
                it.notes = ((it.notes or "") +
                            " | structurally valid; held for human review "
                            "because the gold label is constructed")
                held += 1
            else:
                it.validation_status = "auto_validated"
                promoted += 1
        print(f"{name:36s} n={len(items):4d}  auto_validated={promoted:4d}  "
              f"held_for_review={held:3d}  excluded={excluded:3d}")
        for r, c in fail_reasons.most_common():
            print(f"      failed {r}: {c}")
        grand["auto_validated"] += promoted
        grand["held"] += held
        grand["excluded"] += excluded
        if write:
            write_jsonl(items, path)

    print("\nTOTAL  auto_validated=%d  held_for_review=%d  excluded=%d"
          % (grand["auto_validated"], grand["held"], grand["excluded"]))
    if write:
        print("(candidate files updated in place)")
    else:
        print("(dry run — pass --write to persist)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    run(**vars(ap.parse_args()))
