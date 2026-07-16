"""Analysis of main_pilot20 (E-A' on the 16 headline-eligible pilot schemas).

Produces results/main_pilot20/summary.md:
- EU/AU/TU by lane x round (normalized + Miller-Madow)
- paired Round-0 -> Round-1 deltas (Wilcoxon where n allows)
- transition taxonomy rates (incl. false consensus, minority suppression)
- hedge-label attractor check (degenerate TU=0 rows; middle-label mass)
- gold-probability trajectories; correctness by round
- parse rates, K_eff, timing
Pilot-scale (n=16): descriptive with per-question detail; no headline claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas
from src.transitions import RoundState, classify

ROWS = REPO / "results" / "main_pilot20" / "rows.csv"
OUT = REPO / "results" / "main_pilot20" / "summary.md"

df = pd.read_csv(ROWS)
schemas = load_schemas()
df["hedge_label"] = df["predicted"].isin(["mixed", "conditional"])

L = ["# main_pilot20 summary (16 questions, K=10 F/FT / 20 T, R0+R1, gemma4)\n"]
L.append(f"- rows: {len(df)} ({df.question_id.nunique()} questions x rounds "
         f"{sorted(df['round'].unique())})")
L.append(f"- parse rate: min={df.parse_rate.min():.3f} "
         f"mean={df.parse_rate.mean():.3f}")

# ── EU/AU by lane x round ────────────────────────────────────────────────
L.append("\n## EU/AU/TU (normalized) by lane x round\n")
g = df.groupby(["lane", "round"])[["eu_norm", "au_norm", "tu_norm",
                                   "gold_prob", "correct", "brier"]].mean()
L.append("```\n" + g.round(3).to_string() + "\n```")
L.append("\nMiller-Madow (bias-corrected, unnormalized nats):\n")
g2 = df.groupby(["lane", "round"])[["eu_mm", "au_mm", "tu_mm"]].mean()
L.append("```\n" + g2.round(3).to_string() + "\n```")

# ── paired deltas ────────────────────────────────────────────────────────
r0 = df[df["round"] == 0].set_index("question_id")
r1 = df[df["round"] == 1].set_index("question_id")
common = r0.index.intersection(r1.index)
d = pd.DataFrame({
    "lane": r0.loc[common, "lane"],
    "d_eu": r1.loc[common, "eu_norm"] - r0.loc[common, "eu_norm"],
    "d_au": r1.loc[common, "au_norm"] - r0.loc[common, "au_norm"],
    "d_g": r1.loc[common, "gold_prob"] - r0.loc[common, "gold_prob"],
    "d_correct": r1.loc[common, "correct"].astype(int)
                 - r0.loc[common, "correct"].astype(int),
})
L.append("\n## Paired R0->R1 deltas\n")
L.append("```\n" + d.groupby("lane")[["d_eu", "d_au", "d_g", "d_correct"]]
        .agg(["mean", "median"]).round(3).to_string() + "\n```")
try:
    from scipy import stats
    for col in ["d_eu", "d_au", "d_g"]:
        x = d[col].values
        if np.any(x != 0):
            w = stats.wilcoxon(x, zero_method="wilcox")
            L.append(f"- Wilcoxon {col}: stat={w.statistic:.1f} p={w.pvalue:.3f} "
                     f"(n={np.sum(x != 0)} nonzero of {len(x)})")
        else:
            L.append(f"- Wilcoxon {col}: all zeros")
except Exception as exc:
    L.append(f"- scipy unavailable: {exc}")

# ── transition taxonomy ─────────────────────────────────────────────────
hi_eu = float(df[df["round"] == 1]["eu_norm"].quantile(2 / 3))
trans = []
for qid in common:
    a, b = r0.loc[qid], r1.loc[qid]
    s0 = RoundState(a.eu_norm, a.au_norm, a.gold_prob, bool(a.correct),
                    {"f": a.agent_gold_prob_fundamental,
                     "t": a.agent_gold_prob_trading})
    s1 = RoundState(b.eu_norm, b.au_norm, b.gold_prob, bool(b.correct),
                    {"f": b.agent_gold_prob_fundamental,
                     "t": b.agent_gold_prob_trading})
    tr = classify(s0, s1, high_eu_threshold=hi_eu)
    trans.append({"question_id": qid, "lane": a.lane, "outcome": tr.outcome,
                  "flow": tr.flow, "prd": tr.persistent_rational_disagreement,
                  "cms": tr.correct_minority_suppression,
                  "d_eu": tr.d_eu, "d_au": tr.d_au, "d_g": tr.d_g})
tdf = pd.DataFrame(trans)
tdf.to_csv(REPO / "results" / "main_pilot20" / "transitions.csv", index=False)
L.append("\n## Transition taxonomy (R0 -> R1)\n")
L.append(f"- outcome: {tdf.outcome.value_counts().to_dict()}")
L.append(f"- flow: {tdf.flow.value_counts().to_dict()}")
L.append(f"- persistent rational disagreement: {int(tdf.prd.sum())}; "
         f"correct-minority suppression: {int(tdf.cms.sum())}")
L.append(f"- false consensus rate: {float((tdf.flow=='FALSE_CONSENSUS').mean()):.2f}; "
         f"productive convergence rate: "
         f"{float((tdf.flow=='PRODUCTIVE_CONVERGENCE').mean()):.2f}")

# ── hedge-label attractor ────────────────────────────────────────────────
L.append("\n## Hedge-label attractor check\n")
deg = df[df["tu_norm"] < 1e-9]
L.append(f"- degenerate rows (TU=0): {len(deg)}/{len(df)} "
         f"({deg.groupby('lane').size().to_dict() if len(deg) else {}})")
L.append(f"- hedge-label predictions (mixed/conditional): "
         f"{int(df.hedge_label.sum())}/{len(df)} rows; by lane "
         f"{df.groupby('lane')['hedge_label'].mean().round(2).to_dict()}")
judg = df[df.answer_type.isin(["yes_no_mixed", "supportive_judgment"])]
if len(judg):
    L.append(f"- judgment questions predicting a hedge label: "
             f"{int(judg.hedge_label.sum())}/{len(judg)} rows; correct rate on "
             f"those rows: {judg[judg.hedge_label]['correct'].mean():.2f}")

# ── per-question table ───────────────────────────────────────────────────
L.append("\n## Per-question detail\n```")
cols = ["question_id", "lane", "round", "eu_norm", "au_norm", "gold_prob",
        "predicted", "correct"]
L.append(df[cols].round(3).to_string(index=False))
L.append("```")

# gold-label distribution of predictions vs golds (grading sanity)
L.append("\n## Predictions vs gold labels (final round)\n```")
fin = df[df["round"] == df["round"].max()]
gold_map = {q: schemas[q].gold_label for q in fin.question_id}
fin2 = fin.assign(gold=fin.question_id.map(gold_map))
L.append(fin2.groupby(["gold", "predicted"]).size().to_string())
L.append("```")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
