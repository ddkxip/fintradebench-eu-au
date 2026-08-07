"""Propose (do NOT finalize) finite answer schemas for FinanceBench-150.

Every proposal is a *candidate* requiring manual review: the script emits
`needs_manual_review` and never writes a production schema file. No model
calls; pure rule-based reduction from the gold answer + justification.

Answer types (per extension spec):
  yes_no                    yes | no | insufficient_data
  numeric                   correct_numeric | wrong_numeric | noncommit
  numeric_freeform          (finite reduction inappropriate -> special scoring)
  company_or_entity_choice  <entities from question/gold> + insufficient_data
  comparison_direction      increase | decrease | flat_or_mixed | insufficient_data
  claim_verification        claim_true | claim_false | mixed | insufficient_data
  open_explanation          -> schema_uncertain unless a canonical claim exists

Outputs:
  financebench_schema_candidates.jsonl   (machine-readable)
  financebench_schema_audit_sheet.csv    (blank manual_* columns)
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "financebench_oracle_examples.jsonl"
OUT_JSONL = HERE / "financebench_schema_candidates.jsonl"
OUT_CSV = HERE / "financebench_schema_audit_sheet.csv"

NONCOMMIT = {"insufficient_data", "noncommit", "mixed", "flat_or_mixed",
             "schema_uncertain"}

INC = r"(increase|increased|grew|grow|growth|rose|rise|higher|improv|expand)"
DEC = r"(decrease|decreased|declin|fell|fall|drop|lower|reduc|contract|worsen)"


def norm(s) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip()


def leading_yes_no(a: str) -> str | None:
    m = re.match(r"^\s*[\"'\*]*\s*(yes|no)\b", a, re.I)
    return m.group(1).lower() if m else None


def is_numeric_answer(a: str) -> bool:
    """Answer's operative content is a number/currency/percentage."""
    a = a.strip()
    return bool(re.match(r"^[\$\(\-]?\s*[\d,]+(\.\d+)?\s*(%|x|bn|mn|million|billion)?\s*\.?$",
                         a, re.I)) or bool(re.match(r"^[\$\(\-]?\s*[\d,]+(\.\d+)?", a))


def extract_entities(question: str, company: str) -> list[str]:
    """Candidate entities for a choice question (company names in the text)."""
    ents = []
    if company:
        ents.append(company)
    # capitalized multiword spans, crude but transparent
    for m in re.findall(r"\b([A-Z][A-Za-z&\.\-]+(?:\s+[A-Z][A-Za-z&\.\-]+){0,2})\b", question):
        t = m.strip()
        if t.lower() in {"fy", "the", "what", "which", "does", "is", "did", "in"}:
            continue
        if len(t) > 2 and t not in ents:
            ents.append(t)
    return ents[:5]


def direction_of(text: str) -> str | None:
    t = text.lower()
    inc, dec = bool(re.search(INC, t)), bool(re.search(DEC, t))
    if inc and not dec:
        return "increase"
    if dec and not inc:
        return "decrease"
    if inc and dec:
        return "flat_or_mixed"
    if re.search(r"(unchanged|flat|stable|no (material )?change|roughly the same)", t):
        return "flat_or_mixed"
    return None


def propose(r: dict) -> dict:
    q, a = norm(r["question"]), norm(r["gold_answer"])
    just = norm(r["justification"])
    notes, conf = [], "medium"
    review = "yes"

    yn = leading_yes_no(a)
    asks_change = bool(re.search(
        r"(change|increase|decrease|grow|declin|improv|trend|yoy|year[- ]over[- ]year|"
        r"compared to (the )?(previous|prior)|from fy\d+ to fy\d+)", q, re.I))
    asks_which = bool(re.search(r"\bwhich\b.*\b(company|segment|business|entity|division)\b", q, re.I))

    # 1. yes/no golds dominate when the answer literally opens with yes/no
    if yn:
        atype = "yes_no"
        space = ["yes", "no", "insufficient_data"]
        gold = yn
        conf = "high" if len(a) < 400 else "medium"
        if re.search(r"(cannot|can't|not enough|insufficient|unable to determine)", a, re.I):
            gold, conf = "insufficient_data", "medium"
            notes.append("answer opens yes/no but disclaims determinability")
        notes.append("gold answer opens with an explicit yes/no")

    # 2. pure numeric golds
    elif is_numeric_answer(a):
        # a metric extraction/computation with a checkable number
        atype = "numeric"
        space = ["correct_numeric", "wrong_numeric", "noncommit"]
        gold = "correct_numeric"
        conf = "high"
        notes.append("gold is a computable/extractable number; scoring must "
                     "compare model's numeric value to gold with a tolerance, "
                     "NOT string-match the label")
        review = "yes"

    # 3. directional comparison questions
    elif asks_change:
        d = direction_of(a) or direction_of(just)
        atype = "comparison_direction"
        space = ["increase", "decrease", "flat_or_mixed", "insufficient_data"]
        gold = d or "flat_or_mixed"
        conf = "medium" if d else "low"
        notes.append("question asks about change/direction; "
                     + ("direction inferred from gold answer text"
                        if d else "NO clear direction found - needs review"))

    # 4. entity-choice questions
    elif asks_which:
        atype = "company_or_entity_choice"
        ents = extract_entities(q, r.get("company") or "")
        space = ents + ["insufficient_data"]
        gold = next((e for e in ents if e.lower() in a.lower()), "insufficient_data")
        conf = "low"
        notes.append("entity list auto-extracted from question text - verify")

    # 5. prose claim answers -> claim_verification or open_explanation
    else:
        if re.search(r"(cannot|can't|not enough|insufficient|unable to determine|"
                     r"no information|not provided|not disclosed)", a, re.I):
            atype = "claim_verification"
            space = ["claim_true", "claim_false", "mixed", "insufficient_data"]
            gold = "insufficient_data"
            conf = "medium"
            notes.append("gold explicitly declines / cites missing information")
        elif len(a) > 220:
            atype = "open_explanation"
            space = []
            gold = "schema_uncertain"
            conf = "low"
            notes.append("long prose gold; needs a canonical claim before it "
                         "can be scored with a finite label")
        else:
            atype = "claim_verification"
            space = ["claim_true", "claim_false", "mixed", "insufficient_data"]
            gold = "claim_true"
            conf = "low"
            notes.append("short prose gold provisionally read as asserting its "
                         "claim; canonical claim must be written manually")

    commitment = "noncommitted" if gold in NONCOMMIT else "committed"
    return {
        "financebench_id": r["financebench_id"],
        "question": q,
        "gold_answer": a,
        "justification": just,
        "question_type": r.get("question_type"),
        "question_reasoning": r.get("question_reasoning"),
        "proposed_answer_type": atype,
        "proposed_answer_space": "|".join(space),
        "proposed_gold_label": gold,
        "gold_commitment": commitment,
        "schema_confidence": conf,
        "schema_notes": "; ".join(notes),
        "needs_manual_review": review,
    }


def main() -> None:
    rows = [json.loads(l) for l in SRC.read_text(encoding="utf-8").splitlines() if l.strip()]
    props = [propose(r) for r in rows]
    ev = {r["financebench_id"]: r.get("evidence_text_joined", "") for r in rows}

    with OUT_JSONL.open("w", encoding="utf-8") as f:
        for p in props:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    cols = ["financebench_id", "question", "gold_answer", "justification",
            "evidence_text_joined", "proposed_answer_type",
            "proposed_answer_space", "proposed_gold_label",
            "proposed_gold_commitment", "schema_confidence", "schema_notes",
            "manual_answer_type", "manual_answer_space", "manual_gold_label",
            "manual_gold_commitment", "manual_confidence", "manual_notes",
            "include_in_phase1"]
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for p in props:
            w.writerow({
                "financebench_id": p["financebench_id"],
                "question": p["question"], "gold_answer": p["gold_answer"],
                "justification": p["justification"],
                "evidence_text_joined": ev.get(p["financebench_id"], "")[:4000],
                "proposed_answer_type": p["proposed_answer_type"],
                "proposed_answer_space": p["proposed_answer_space"],
                "proposed_gold_label": p["proposed_gold_label"],
                "proposed_gold_commitment": p["gold_commitment"],
                "schema_confidence": p["schema_confidence"],
                "schema_notes": p["schema_notes"],
                "manual_answer_type": "", "manual_answer_space": "",
                "manual_gold_label": "", "manual_gold_commitment": "",
                "manual_confidence": "", "manual_notes": "",
                "include_in_phase1": "",
            })

    from collections import Counter
    print(f"wrote {OUT_JSONL.name} and {OUT_CSV.name} ({len(props)} rows)")
    print("proposed_answer_type:", Counter(p["proposed_answer_type"] for p in props))
    print("gold_commitment:", Counter(p["gold_commitment"] for p in props))
    print("schema_confidence:", Counter(p["schema_confidence"] for p in props))


if __name__ == "__main__":
    main()
