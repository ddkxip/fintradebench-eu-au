"""Build validated yes/no schemas for the FinanceBench Phase-1 subset.

Reads the candidate proposals + oracle examples, keeps only
proposed_answer_type == "yes_no", validates the gold label, and writes a
clean schema file. Rows whose gold label cannot be established are EXCLUDED
and reported separately (never silently coerced).

No model calls. Does not touch FinTradeBench schemas.

Outputs:
  financebench_yesno_schemas.jsonl
  financebench_yesno_excluded.csv
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAND = HERE / "financebench_schema_candidates.jsonl"
EX = HERE / "financebench_oracle_examples.jsonl"
OUT = HERE / "financebench_yesno_schemas.jsonl"
EXCL = HERE / "financebench_yesno_excluded.csv"

ANSWER_SPACE = ["yes", "no", "insufficient_data"]
NONCOMMIT_SET = ["insufficient_data"]

DECLINE = re.compile(
    r"(there are none|not measured|cannot be determined|can'?t be determined|"
    r"insufficient|unable to determine|no information|not provided|not disclosed)",
    re.I)


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def derive_gold(answer: str) -> tuple[str | None, str]:
    """Return (gold_label, reason). None => exclude."""
    a = re.sub(r"\s+", " ", str(answer or "")).strip()
    if not a:
        return None, "empty gold answer"
    m = re.match(r"^\s*[\"'\*]*\s*(yes|no)\b", a, re.I)
    if not m:
        return None, "gold answer does not open with an explicit yes/no"
    lead = m.group(1).lower()
    # a gold that opens yes/no but then disclaims determinability is ambiguous
    if DECLINE.search(a):
        return None, ("gold opens with yes/no but also disclaims "
                      "determinability - ambiguous, needs manual ruling")
    return lead, f"gold answer opens with an explicit '{lead}'"


def main() -> None:
    cands = read_jsonl(CAND)
    ex = {r["financebench_id"]: r for r in read_jsonl(EX)}

    yn = [c for c in cands if c["proposed_answer_type"] == "yes_no"]
    kept, excluded = [], []
    for c in yn:
        fid = c["financebench_id"]
        e = ex.get(fid, {})
        gold, reason = derive_gold(c["gold_answer"])
        evidence = (e.get("evidence_text_joined") or "").strip()
        if gold is None:
            excluded.append({"financebench_id": fid, "question": c["question"],
                             "gold_answer": c["gold_answer"],
                             "exclusion_reason": reason})
            continue
        if not evidence:
            excluded.append({"financebench_id": fid, "question": c["question"],
                             "gold_answer": c["gold_answer"],
                             "exclusion_reason": "no oracle evidence_text"})
            continue
        if gold not in ANSWER_SPACE:
            excluded.append({"financebench_id": fid, "question": c["question"],
                             "gold_answer": c["gold_answer"],
                             "exclusion_reason": f"derived label {gold!r} not in answer space"})
            continue
        kept.append({
            "financebench_id": fid,
            "question": c["question"],
            "answer_type": "yes_no",
            "answer_space": ANSWER_SPACE,
            "noncommit_set": NONCOMMIT_SET,
            "gold_label": gold,
            "gold_label_evidence": c["gold_answer"],
            "justification": c.get("justification", ""),
            "evidence_text": evidence,
            "company": e.get("company"),
            "doc_name": e.get("doc_name"),
            "schema_confidence": c.get("schema_confidence", "medium"),
            "schema_notes": reason,
        })

    with OUT.open("w", encoding="utf-8") as f:
        for k in kept:
            f.write(json.dumps(k, ensure_ascii=False) + "\n")
    with EXCL.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["financebench_id", "question",
                                          "gold_answer", "exclusion_reason"])
        w.writeheader()
        for r in excluded:
            w.writerow(r)

    from collections import Counter
    print(f"yes_no candidates: {len(yn)}")
    print(f"  kept:     {len(kept)} -> {OUT.name}")
    print(f"  excluded: {len(excluded)} -> {EXCL.name}")
    for r in excluded:
        print(f"    [{r['financebench_id'][-8:]}] {r['exclusion_reason']}")
    print(f"gold split: {Counter(k['gold_label'] for k in kept)}")
    print(f"confidence: {Counter(k['schema_confidence'] for k in kept)}")
    ev = [len(k["evidence_text"]) for k in kept]
    if ev:
        ev.sort()
        print(f"evidence chars: median {ev[len(ev)//2]}, max {ev[-1]}")
    # invariants
    assert all(k["gold_label"] in ANSWER_SPACE for k in kept)
    assert all(k["evidence_text"] for k in kept)
    print("validation: OK (all gold labels in answer_space; all have evidence)")


if __name__ == "__main__":
    main()
