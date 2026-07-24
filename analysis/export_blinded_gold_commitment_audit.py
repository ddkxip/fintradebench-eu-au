"""Export a BLINDED gold-commitment audit sheet for independent annotators.

Blinding: the annotator sees only the question, the answer space, and the
gold's own evidence/final-answer text — NEVER the schema's gold_label, its
commitment classification, the noncommit_set, the canonical_claim, or any
prior manual_* judgement. Each annotator independently derives (a) which
answer-space label the gold asserts and (b) whether that answer is
committed or non-committed.

Output: analysis/gold_commitment_audit_sheet_blinded.csv
Also writes two blank pre-named annotator templates (codex, antigravity)
and a neutral instruction sheet, so the pipeline is turnkey. Does NOT
touch schemas or existing findings. Sorted by question_id (neutral order —
does not signal which cases are 'risky').
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas  # noqa: E402

ANA = REPO / "analysis"
OUT = ANA / "gold_commitment_audit_sheet_blinded.csv"
GOLD_CSV = Path(r"C:\Users\ddkxi\PycharmProjects\Contrastive learning"
                r"\NASDAQ processed data\Final_benchmark\final_dataset_release"
                r"\FinTradeBench_Golden_Seed_150.csv")

schemas = load_schemas()


def final_answer_text(resp: str, limit: int = 1800) -> str:
    """Extract the gold's final-answer section (the classification target)."""
    if not isinstance(resp, str):
        return ""
    parts = re.split(r"(?i)final answer\s*:?", resp)
    tail = parts[-1].strip() if len(parts) > 1 else resp[-limit:]
    tail = re.sub(r"\s+", " ", tail).strip()
    return tail[:limit]


gold_text = {}
if GOLD_CSV.exists():
    src = pd.read_csv(GOLD_CSV)
    for _, r in src.iterrows():
        gold_text[str(r["question_id"])] = final_answer_text(str(r["response"]))
else:
    print(f"[warn] source gold CSV not found at {GOLD_CSV}; "
          "gold_final_answer_text will fall back to evidence only.")

rows = []
for s in schemas.values():
    if not s.headline_eligible:
        continue
    rows.append({
        "question_id": s.question_id,
        "lane": s.lane,
        "answer_type": s.answer_type,
        "question": s.question,
        "answer_space": "|".join(s.answer_space),
        "gold_label_evidence": s.gold_label_evidence,
        "gold_final_answer_text": gold_text.get(s.question_id, s.gold_label_evidence),
        # blank annotator columns
        "annotator_gold_label": "",
        "annotator_gold_commitment": "",
        "annotator_confidence": "",
        "annotator_notes": "",
    })

df = pd.DataFrame(rows).sort_values("question_id")
# hard guarantee: none of the leak columns are present
LEAK = {"gold_label", "schema_gold_commitment", "schema_noncommit_set",
        "canonical_claim", "ambiguity_notes"}
assert not (LEAK & set(df.columns)), "blinding leak!"
assert not any(c.startswith("manual_") for c in df.columns)

df.to_csv(OUT, index=False, encoding="utf-8")
print(f"wrote {OUT} ({len(df)} rows, {sum(bool(gold_text.get(q)) for q in df.question_id)} "
      "with full gold text)")

# turnkey blank templates for the two external annotators (only if absent)
for name in ("gold_commitment_audit_codex.csv",
             "gold_commitment_audit_antigravity.csv"):
    tgt = ANA / name
    if not tgt.exists():
        shutil.copy(OUT, tgt)
        print(f"  created blank template {tgt.name} (fill annotator_* columns)")
    else:
        print(f"  {tgt.name} already exists — left untouched")

# neutral annotator instructions (defines the binary WITHOUT leaking labels)
instr = ANA / "BLINDED_ANNOTATOR_INSTRUCTIONS.md"
instr.write_text(
    "# Blinded gold-commitment annotation — instructions\n\n"
    "You are given, per row: the question, the finite `answer_space` "
    "(pipe-separated candidate labels), and the gold answer's own text "
    "(`gold_label_evidence`, `gold_final_answer_text`). You do NOT see any "
    "prior label or classification. Fill four columns per row:\n\n"
    "- **annotator_gold_label**: the single label from `answer_space` that "
    "the gold answer asserts. Must be copied exactly from answer_space.\n"
    "- **annotator_gold_commitment**: `committed` or `noncommitted`.\n"
    "  - **committed** = the gold's operative conclusion selects one "
    "answer-space direction a reader would act on (caveats on *other* "
    "dimensions are allowed).\n"
    "  - **noncommitted** = the gold (a) declines to determine / says the "
    "data is insufficient, (b) makes the answer conditional on an "
    "unspecified external factor with no default, or (c) weights opposing "
    "conclusions on the *same* dimension equally.\n"
    "- **annotator_confidence**: high / medium / low.\n"
    "- **annotator_notes**: one-line rationale (optional).\n\n"
    "Judge only from the provided gold text. Do not use outside knowledge "
    "about the companies. Save your completed file as "
    "`gold_commitment_audit_codex.csv` or "
    "`gold_commitment_audit_antigravity.csv`.\n",
    encoding="utf-8")
print(f"  wrote {instr.name}")
