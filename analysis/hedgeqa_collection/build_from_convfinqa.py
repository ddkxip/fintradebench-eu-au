"""HedgeQA candidates from ConvFinQA.

Reads the official ConvFinQA release. The repo ships it zipped at
`ConvFinQA-main/data.zip`; extract train.json/dev.json to
`data/convfinqa_extract/data/` (see README). If no source is found the
builder emits nothing rather than inventing items.

Official structure (czyssrs/ConvFinQA): entries carry `pre_text`,
`post_text`, `table`, and an `annotation` block with the decomposed
conversation:

    "annotation": {"dialogue_break": [turn_question, ...],
                   "turn_program":   [program_str, ...],
                   "exe_ans_list":   [number, ...]}

ConvFinQA turns are conversational, so a later turn can be unintelligible
without its history ("and what about 2019?"). Two rules keep items
self-contained, which HedgeQA requires:

  * only the FIRST turn, or a turn whose text still names its own subject,
    is eligible (`SHORT_HISTORY_TURNS` bounds how deep we go);
  * for a non-first turn the preceding turns are prepended verbatim as
    conversation history inside the question text, so the item is readable
    standalone and nothing has to be inferred from a missing context.

Oracle evidence is the item's own pre_text + table + post_text.

Usage: python analysis/hedgeqa_collection/build_from_convfinqa.py
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

SEARCH_DIRS = [REPO / "data" / "convfinqa_extract" / "data",
               REPO / "data" / "convfinqa"]
CANDIDATE_FILES = ["train.json", "dev.json"]
OUT = REPO / "data" / "hedgeqa" / "candidates" / "convfinqa_candidates.jsonl"

MAX_ITEMS = 30
SHORT_HISTORY_TURNS = 2      # turn index 0 or 1 only -- "short history"


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
        print("[convfinqa] SOURCE NOT PRESENT — no candidates emitted.")
        print(f"        expected one of {CANDIDATE_FILES}")
        print(f"        under any of {[str(d) for d in SEARCH_DIRS]}")
        print("        Builder is ready; drop the official release in place "
              "and re-run.")
        write_jsonl([], OUT)
        return []

    data = json.loads(src.read_text(encoding="utf-8"))
    items = []
    stats = {"conversations": 0, "turns_seen": 0, "kept": 0,
             "skip_too_deep": 0, "skip_not_change": 0,
             "skip_no_evidence": 0, "skip_no_answer": 0}

    for entry in data:
        stats["conversations"] += 1
        ann = entry.get("annotation") or {}
        turns = ann.get("dialogue_break") or []
        progs = ann.get("turn_program") or []
        answers = ann.get("exe_ans_list") or []

        pre = "\n".join(clean_ws(x) for x in (entry.get("pre_text") or []))
        post = "\n".join(clean_ws(x) for x in (entry.get("post_text") or []))
        evidence = "\n\n".join(
            x for x in (pre, table_to_text(entry.get("table")), post) if x
        ).strip()

        for i, turn in enumerate(turns):
            stats["turns_seen"] += 1
            if i >= SHORT_HISTORY_TURNS:
                stats["skip_too_deep"] += 1
                continue
            if len(evidence) < 120:
                stats["skip_no_evidence"] += 1
                continue
            if i >= len(answers) or answers[i] is None:
                stats["skip_no_answer"] += 1
                continue

            prog = progs[i] if i < len(progs) else ""
            got = numeric_to_directional(turn, answers[i],
                                         derivation=f"turn_program={prog!r}")
            if got is None:
                stats["skip_not_change"] += 1
                continue
            space, nc, gold, deriv = got

            # make the turn self-contained
            if i == 0:
                qtext = turn
                hist_note = "first turn; no history needed"
            else:
                hist = "\n".join(f"Q{j + 1}: {turns[j]}" for j in range(i))
                qtext = (f"Conversation so far:\n{hist}\n\n"
                         f"Question: {turn}")
                hist_note = f"turn {i}; {i} prior turn(s) inlined verbatim"

            sid = f"{entry.get('id', 'conv')}#turn{i}"
            items.append(HedgeQAItem(
                hedgeqa_id=make_id("convfinqa", sid),
                source_benchmark="convfinqa", source_id=sid,
                question=qtext, oracle_evidence=evidence,
                evidence_provenance=("ConvFinQA item-local pre_text + table + "
                                     "post_text shipped with the conversation"),
                answer_type="directional_change",
                answer_space=space, gold_label=gold, noncommit_labels=nc,
                gold_commitment=("noncommitted" if gold in nc
                                 else "committed"),
                transformation_type="numeric_to_directional",
                requires_rag=False, validation_status="candidate",
                schema_confidence=0.55,
                original_question=turn,
                derivation=deriv + f" History handling: {hist_note}.",
                notes=f"exe_ans={answers[i]!r}; {hist_note}"))
            stats["kept"] += 1
            if stats["kept"] >= MAX_ITEMS:
                break
        if stats["kept"] >= MAX_ITEMS:
            break

    n = write_jsonl(items, OUT)
    print(f"[convfinqa] wrote {n} rows -> {OUT.relative_to(REPO)}")
    for k, v in stats.items():
        print(f"    {k:22s} {v}")
    return items


if __name__ == "__main__":
    build()
