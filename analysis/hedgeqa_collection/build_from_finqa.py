"""HedgeQA candidates from FinQA.

Reads the official FinQA release, vendored at `FinQA-main/dataset/` (with
`data/finqa/` as a fallback). If neither is present the builder emits nothing
rather than inventing items.

Official structure (czyssrs/FinQA): a JSON list whose entries carry

    {"id": "...",
     "pre_text":  [str, ...],     # narrative before the table
     "post_text": [str, ...],     # narrative after the table
     "table":     [[cell, ...], ...],
     "qa": {"question": ..., "answer": ..., "exe_ans": <number>,
            "program": "subtract(a, b)", "gold_inds": {...}}}

Oracle evidence is pre_text + table + post_text, all shipped with the item,
so nothing is retrieved. `gold_inds` (the annotated supporting rows) is
recorded in the provenance string when present.

Only change-shaped questions with a numeric `exe_ans` are kept, mapped to a
direction. FinQA's `program` is carried into the derivation so the rewrite
stays auditable: a reviewer can see that e.g. subtract(2019, 2018) is what
licenses "increased".

Usage: python analysis/hedgeqa_collection/build_from_finqa.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import HedgeQAItem, make_id, write_jsonl  # noqa: E402
from transforms import (clean_ws, numeric_to_directional,  # noqa: E402
                        table_to_text)

SEARCH_DIRS = [REPO / "FinQA-main" / "dataset", REPO / "data" / "finqa"]
CANDIDATE_FILES = ["train.json", "dev.json", "test.json"]
OUT = REPO / "data" / "hedgeqa" / "candidates" / "finqa_candidates.jsonl"

MAX_ITEMS = 60


def _find_source():
    for d in SEARCH_DIRS:
        for name in CANDIDATE_FILES:
            p = d / name
            if p.exists():
                return p
    return None


def build():
    src = _find_source()
    if src is None:
        print("[finqa] SOURCE NOT PRESENT — no candidates emitted.")
        print(f"        expected one of {CANDIDATE_FILES}")
        print(f"        under any of {[str(d) for d in SEARCH_DIRS]}")
        print("        Builder is ready; drop the official release in place "
              "and re-run.")
        write_jsonl([], OUT)
        return []

    data = json.loads(src.read_text(encoding="utf-8"))
    items = []
    stats = {"loaded": 0, "kept": 0, "skip_no_exe_ans": 0,
             "skip_not_change": 0, "skip_no_evidence": 0}

    for entry in data:
        stats["loaded"] += 1
        qa = entry.get("qa") or {}
        pre = "\n".join(clean_ws(x) for x in (entry.get("pre_text") or []))
        post = "\n".join(clean_ws(x) for x in (entry.get("post_text") or []))
        evidence = "\n\n".join(
            x for x in (pre, table_to_text(entry.get("table")), post) if x
        ).strip()
        if len(evidence) < 120:
            stats["skip_no_evidence"] += 1
            continue

        exe = qa.get("exe_ans")
        if exe is None:
            stats["skip_no_exe_ans"] += 1
            continue

        got = numeric_to_directional(
            qa.get("question", ""), exe,
            derivation=f"program={qa.get('program', '')!r}")
        if got is None:
            stats["skip_not_change"] += 1
            continue
        space, nc, gold, deriv = got

        gi = qa.get("gold_inds") or {}
        prov = ("FinQA item-local pre_text + table + post_text shipped with "
                "the question")
        if gi:
            prov += f"; annotated supporting rows: {list(gi)[:6]}"

        sid = entry.get("id") or qa.get("id") or f"finqa_{stats['loaded']}"
        items.append(HedgeQAItem(
            hedgeqa_id=make_id("finqa", sid),
            source_benchmark="finqa", source_id=sid,
            question=qa.get("question", ""),
            oracle_evidence=evidence, evidence_provenance=prov,
            answer_type="directional_change",
            answer_space=space, gold_label=gold, noncommit_labels=nc,
            gold_commitment=("noncommitted" if gold in nc
                             else "committed"),
            transformation_type="numeric_to_directional",
            requires_rag=False, validation_status="candidate",
            schema_confidence=0.6,
            original_question=qa.get("question", ""),
            derivation=deriv,
            notes=f"exe_ans={exe!r}; answer={qa.get('answer')!r}"))
        stats["kept"] += 1
        if stats["kept"] >= MAX_ITEMS:
            break

    n = write_jsonl(items, OUT)
    print(f"[finqa] wrote {n} rows -> {OUT.relative_to(REPO)}")
    for k, v in stats.items():
        print(f"    {k:22s} {v}")
    return items


if __name__ == "__main__":
    build()
