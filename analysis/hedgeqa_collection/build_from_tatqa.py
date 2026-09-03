"""HedgeQA candidates from TAT-QA.

Reads the official TAT-QA release, vendored at `TAT-QA-master/dataset_raw/`
(with `data/tatqa/` as a fallback for a manually placed copy). If neither is
present the builder emits nothing rather than inventing items.

Expected structure: a JSON list whose entries each carry

    {"table": {"uid": ..., "table": [[cell, ...], ...]},
     "paragraphs": [{"uid":..., "order":..., "text": ...}, ...],
     "questions": [{"uid":..., "question":..., "answer": ...,
                    "answer_type": "span|multi-span|count|arithmetic",
                    "answer_from": "table|text|table-text",
                    "scale": "", "derivation": "..."}]}

Oracle evidence is the item's own table plus its paragraphs -- TAT-QA ships
the context with the question, so nothing is retrieved.

Only two families are kept, because only these have a defensible finite
answer space:
  * arithmetic answers to change questions -> numeric_to_directional
  * comparison questions naming >=2 entities -> comparison_to_choice
Everything else (spans, counts, open arithmetic) is counted and skipped.

Usage: python analysis/hedgeqa_collection/build_from_tatqa.py
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

# The official release is vendored in the repo root; data/tatqa/ is a
# fallback for a manually placed copy.
SEARCH_DIRS = [REPO / "TAT-QA-master" / "dataset_raw", REPO / "data" / "tatqa"]
CANDIDATE_FILES = ["tatqa_dataset_train.json", "tatqa_dataset_dev.json",
                   "tatqa_dataset_test.json"]
OUT = REPO / "data" / "hedgeqa" / "candidates" / "tatqa_candidates.jsonl"

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
        print("[tatqa] SOURCE NOT PRESENT — no candidates emitted.")
        print(f"        expected one of {CANDIDATE_FILES}")
        print(f"        under any of {[str(d) for d in SEARCH_DIRS]}")
        print("        Builder is ready; drop the official release in place "
              "and re-run.")
        write_jsonl([], OUT)
        return []

    data = json.loads(src.read_text(encoding="utf-8"))
    items = []
    stats = {"loaded": 0, "kept": 0, "skip_not_arithmetic": 0,
             "skip_not_change": 0, "skip_no_evidence": 0}

    for entry in data:
        table = (entry.get("table") or {}).get("table") or []
        paras = entry.get("paragraphs") or []
        evidence = (table_to_text(table) + "\n\n" +
                    "\n".join(clean_ws(p.get("text", "")) for p in paras)).strip()

        for q in entry.get("questions") or []:
            stats["loaded"] += 1
            if len(evidence) < 120:
                stats["skip_no_evidence"] += 1
                continue
            atype = (q.get("answer_type") or "").lower()
            if atype != "arithmetic":
                stats["skip_not_arithmetic"] += 1
                continue
            got = numeric_to_directional(
                q.get("question", ""), q.get("answer"),
                derivation=q.get("derivation", ""), scale=q.get("scale", ""))
            if got is None:
                stats["skip_not_change"] += 1
                continue
            space, nc, gold, deriv = got
            uid = q.get("uid") or f"{entry.get('table',{}).get('uid','?')}"
            items.append(HedgeQAItem(
                hedgeqa_id=make_id("tatqa", uid),
                source_benchmark="tatqa", source_id=uid,
                question=q.get("question", ""),
                oracle_evidence=evidence,
                evidence_provenance=("TAT-QA item-local table + paragraphs "
                                     "shipped with the question"),
                answer_type="directional_change",
                answer_space=space, gold_label=gold, noncommit_labels=nc,
                gold_commitment=("noncommitted" if gold in nc
                                 else "committed"),
                transformation_type="numeric_to_directional",
                requires_rag=False, validation_status="candidate",
                schema_confidence=0.6,
                original_question=q.get("question", ""),
                derivation=deriv,
                notes=f"source answer={q.get('answer')!r} "
                      f"scale={q.get('scale')!r} "
                      f"answer_from={q.get('answer_from')!r}"))
            stats["kept"] += 1
            if stats["kept"] >= MAX_ITEMS:
                break
        if stats["kept"] >= MAX_ITEMS:
            break

    n = write_jsonl(items, OUT)
    print(f"[tatqa] wrote {n} rows -> {OUT.relative_to(REPO)}")
    for k, v in stats.items():
        print(f"    {k:24s} {v}")
    return items


if __name__ == "__main__":
    build()
