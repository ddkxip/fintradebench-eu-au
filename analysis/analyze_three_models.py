"""Three-model attractor comparison on the shared 16 questions:
gemma4 (main_pilot20) vs qwen3:8b (qwen_repl16) vs gemini-3.1-pro
(gemini_subset16). Writes results/three_model_comparison.md."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

RES = REPO / "results"
OUT = RES / "three_model_comparison.md"
HEDGE = {"mixed", "conditional", "insufficient_data", "none_clear"}

frames = []
for run, model in [("main_pilot20", "gemma4"), ("qwen_repl16", "qwen3:8b"),
                   ("gemini_subset16", "gemini-3.1-pro")]:
    df = pd.read_csv(RES / run / "rows.csv")
    df["model"] = model
    frames.append(df)
both = pd.concat(frames, ignore_index=True)
both["noncommit_pred"] = both["predicted"].isin(HEDGE)

L = ["# Three-model comparison (shared 16 questions, R0+R1)\n"]
agg = both.groupby(["model", "round"]).agg(
    eu=("eu_norm", "mean"), au=("au_norm", "mean"), tu=("tu_norm", "mean"),
    gold_prob=("gold_prob", "mean"), acc=("correct", "mean"),
    noncommit_pred=("noncommit_pred", "mean"),
    degenerate=("tu_norm", lambda s: float((s < 1e-9).mean())),
    parse=("parse_rate", "mean"))
if "p_noncommit" in both.columns:
    pn = both.groupby(["model", "round"])["p_noncommit"].mean()
    agg["p_noncommit"] = pn
L.append("```\n" + agg.round(3).to_string() + "\n```")

L.append("\n## Lane accuracy (final round)\n")
fin = both[both["round"] == 1]
L.append("```\n" + fin.pivot_table(index="lane", columns="model",
                                   values="correct", aggfunc="mean")
        .round(2).to_string() + "\n```")

L.append("\n## Judgment questions only (the attractor's home turf)\n")
judg = both[both.answer_type.isin(["yes_no_mixed", "supportive_judgment"])]
jagg = judg.groupby(["model", "round"]).agg(
    acc=("correct", "mean"), noncommit_pred=("noncommit_pred", "mean"),
    eu=("eu_norm", "mean"), au=("au_norm", "mean"))
L.append("```\n" + jagg.round(3).to_string() + "\n```")

L.append("\n## Per-question final-round predictions (gold in brackets)\n```")
import json as _json
gold_map = {}
sys.path.insert(0, str(REPO))
from src.schema import load_schemas
for q, s in load_schemas().items():
    gold_map[q] = s.gold_label
piv = fin.pivot_table(index="question_id", columns="model",
                      values="predicted", aggfunc="first")
piv["gold"] = [gold_map.get(q) for q in piv.index]
L.append(piv.to_string())
L.append("```")

L.append("\n## Paired deltas R0->R1 per model\n")
for model, g in both.groupby("model"):
    r0 = g[g["round"] == 0].set_index("question_id")
    r1 = g[g["round"] == 1].set_index("question_id")
    idx = r0.index.intersection(r1.index)
    L.append(f"- {model}: dAU={float((r1.loc[idx,'au_norm']-r0.loc[idx,'au_norm']).mean()):+.3f}, "
             f"dEU={float((r1.loc[idx,'eu_norm']-r0.loc[idx,'eu_norm']).mean()):+.3f}, "
             f"dG={float((r1.loc[idx,'gold_prob']-r0.loc[idx,'gold_prob']).mean()):+.3f} (n={len(idx)})")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
