"""Set-collapse audit of wrong-direction commitment errors.

The T-lane (screening) questions have expert answers that name a *set* of
entities ("the top 5 are INTC, MU, LRCX, APP, MRVL"). Our schema collapses
each to a single reference label, so a system naming a different member of
the endorsed set is scored as a wrong-direction commitment even though the
expert answer explicitly endorses it.

This script quantifies the contamination with a mechanical, reproducible
test: for each wrong-direction error, does the model's predicted entity
appear as a whole word in the reference's OWN written justification
(`gold_label_evidence`)?

Result (2026-08-14, four models, final round):
    T lane   36/74 = 48.6%  of wrong-direction errors name an endorsed entity
    F lane    1/20 =  5.0%
    FT lane   0/7  =  0.0%

Conclusion: T-lane wrong-direction counts are an UPPER BOUND on genuine model
error and must be reported as such. F/FT lanes are essentially clean. This
independently confirms, by machine, what two blinded annotators concluded by
reading (see GOLD_COMMITMENT_AUDIT findings, T-lane screening cluster).

Run: python analysis/reference_endorsement_audit.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.schema import load_schemas

RUNS = {
    "gemma4": "ea_full_gemma4",
    "qwen3:8b": "ea_full_qwen3",
    "qwen3.6-27b": "ea_full_hf_qwen36_27b_fp8",
    "gemma4-31b-it": "ea_full_hf_gemma_4_31B_it",
}


def collect() -> pd.DataFrame:
    sch = load_schemas()
    rows = []
    for model, run in RUNS.items():
        d = pd.read_csv(REPO / "results" / run / "rows.csv")
        d = d[(d["round"] == 1) & d["correct"].notna()]
        for _, x in d.iterrows():
            s = sch[x.question_id]
            pred = str(x.predicted)
            # wrong-direction = settled reference, committed answer, wrong
            if s.gold_label in s.noncommit_set:
                continue
            if pred in s.noncommit_set:
                continue
            if bool(x.correct):
                continue
            ev = s.gold_label_evidence or ""
            rows.append({
                "model": model,
                "question_id": x.question_id,
                "lane": s.lane,
                "gold": s.gold_label,
                "predicted": pred,
                "endorsed_by_reference": bool(
                    re.search(r"\b" + re.escape(pred) + r"\b", ev)),
            })
    return pd.DataFrame(rows)


def main() -> None:
    d = collect()
    out = REPO / "analysis" / "reference_endorsement_audit.csv"
    d.to_csv(out, index=False, encoding="utf-8")

    print("Wrong-direction errors: is the prediction named in the "
          "reference's own justification?\n")
    t = d.groupby("lane")["endorsed_by_reference"].agg(["sum", "count"])
    t["share"] = (t["sum"] / t["count"]).round(3)
    print(t.to_string())
    print(f"\nOVERALL {d['endorsed_by_reference'].sum()}/{len(d)} = "
          f"{d['endorsed_by_reference'].mean():.1%}")
    print("\nBy model:")
    print(d.groupby("model")["endorsed_by_reference"]
          .agg(["sum", "count", "mean"]).round(3).to_string())
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
