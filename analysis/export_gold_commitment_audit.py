"""Export a manual gold-commitment audit sheet for the headline-eligible
schemas. Reanalysis only; writes a review template with blank manual columns.

The paper's central UQ conclusion (p_noncommit is a hedge-collision
detector) depends on which gold answers count as committed vs
non-committed. This sheet lets a human re-adjudicate that binary, with the
riskiest cases sorted to the top.

Output: analysis/gold_commitment_audit_sheet.csv (blank manual_* columns).
Does NOT modify schemas or any findings.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas  # noqa: E402

OUT = REPO / "analysis" / "gold_commitment_audit_sheet.csv"
schemas = load_schemas()

rows = []
for s in schemas.values():
    if not s.headline_eligible:
        continue
    ncset = s.noncommit_set
    commitment = "noncommitted" if s.gold_label in ncset else "committed"
    rows.append({
        "question_id": s.question_id,
        "lane": s.lane,
        "answer_type": s.answer_type,
        "question": s.question,
        "answer_space": "|".join(s.answer_space),
        "gold_label": s.gold_label,
        "schema_noncommit_set": "|".join(sorted(ncset)),
        "schema_gold_commitment": commitment,
        "gold_label_evidence": s.gold_label_evidence,
        "canonical_claim": s.canonical_claim,
        "ambiguity_notes": s.ambiguity_notes or "",
        "schema_confidence": s.schema_confidence,
        # blank manual columns for human completion
        "manual_gold_label": "",
        "manual_gold_commitment": "",
        "manual_confidence": "",
        "manual_notes": "",
        "needs_schema_revision": "",
    })

df = pd.DataFrame(rows)

# priority sort: A noncommitted, B ambiguity nonempty, C medium conf,
# D FT lane, E remaining. Lower key sorts first.
df["_A"] = (df["schema_gold_commitment"] != "noncommitted").astype(int)
df["_B"] = (df["ambiguity_notes"].str.len() == 0).astype(int)
df["_C"] = (df["schema_confidence"] != "medium").astype(int)
df["_D"] = (df["lane"] != "FT").astype(int)
df = df.sort_values(["_A", "_B", "_C", "_D", "question_id"]).drop(
    columns=["_A", "_B", "_C", "_D"])

df.to_csv(OUT, index=False, encoding="utf-8")
print(f"wrote {OUT} ({len(df)} rows)")
print("priority head (first 20):")
print(df[["question_id", "lane", "schema_gold_commitment",
          "schema_confidence", "gold_label"]].head(20).to_string(index=False))
print("\ncommitment counts:",
      df["schema_gold_commitment"].value_counts().to_dict())
