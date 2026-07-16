"""Joint analysis: hedge-attractor probe arms vs baseline, and qwen3:8b
replication vs gemma4. Writes results/probe_qwen_summary.md."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas

RES = REPO / "results"
OUT = RES / "probe_qwen_summary.md"

schemas = load_schemas()
base = pd.read_csv(RES / "main_pilot20" / "rows.csv")
qwen = pd.read_csv(RES / "qwen_repl16" / "rows.csv")

# hedge_probe/rows.csv is ragged: unscoreable rows (28 cols) and scoreable
# rows (34 cols) were appended headerless. Column orders are deterministic
# from run_question's dict-insertion order.
BASE_COLS = ["question_id", "lane", "answer_type", "round", "K",
             "evidence_mode", "coverage_incomplete", "tickers", "parse_rate",
             "gold_scoreable",
             "tu", "au", "eu", "tu_mm", "au_mm", "eu_mm",
             "tu_norm", "au_norm", "eu_norm", "eu_tu_ratio",
             "predicted", "p_sys",
             "agent_entropy_fundamental", "agent_entropy_trading",
             "k_eff_fundamental", "k_eff_trading"]
GOLD_COLS = ["gold_prob", "correct", "brier", "nll",
             "agent_gold_prob_fundamental", "agent_gold_prob_trading"]
TAIL_COLS = ["arm", "gold_label"]


def load_probe(path: Path) -> pd.DataFrame:
    import csv as _csv
    recs = []
    with path.open(encoding="utf-8") as f:
        rows = list(_csv.reader(f))
    for r in rows:
        if not r or r[0] == "question_id":  # header line(s)
            continue
        if len(r) == len(BASE_COLS) + len(TAIL_COLS):
            cols = BASE_COLS + TAIL_COLS
        elif len(r) == len(BASE_COLS) + len(GOLD_COLS) + len(TAIL_COLS):
            cols = BASE_COLS + GOLD_COLS + TAIL_COLS
        else:
            raise ValueError(f"unexpected field count {len(r)}")
        recs.append(dict(zip(cols, r)))
    df = pd.DataFrame(recs)
    for c in ["round", "K", "parse_rate", "tu_norm", "au_norm", "eu_norm",
              "gold_prob", "brier", "nll"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    if "correct" in df.columns:
        df["correct"] = df["correct"].map({"True": True, "False": False})
    return df


probe = load_probe(RES / "hedge_probe" / "rows.csv")

HEDGE = {"mixed", "conditional"}
JQ = ["F1", "F11", "FT1", "FT2", "FT10", "FT12", "FT25", "FT31"]
DIRECTIONAL_GOLD = ["F11", "FT2", "FT10", "FT12"]   # gold not a hedge label
HEDGE_GOLD = ["F1", "FT1", "FT25", "FT31"]

L = ["# Hedge probe + qwen replication summary\n"]

# ── probe ────────────────────────────────────────────────────────────────
b0 = base[(base["round"] == 0) & base.question_id.isin(JQ)].copy()
b0["arm"] = "baseline_menu"
for df in (b0, probe):
    df["hedge_pred"] = df["predicted"].isin(HEDGE)

L.append("## Probe: 8 judgment questions, Round 0, K=10, gemma4\n")
comb = pd.concat([b0, probe], ignore_index=True)
agg = comb.groupby("arm").agg(
    eu=("eu_norm", "mean"), au=("au_norm", "mean"), tu=("tu_norm", "mean"),
    hedge_rate=("hedge_pred", "mean"),
    degenerate=("tu_norm", lambda s: float((s < 1e-9).mean())),
    parse=("parse_rate", "mean"))
L.append("```\n" + agg.round(3).to_string() + "\n```")

L.append("\n### Directional-gold questions (F11, FT2, FT10, FT12) — accuracy by arm\n")
dsub = comb[comb.question_id.isin(DIRECTIONAL_GOLD)]
acc = dsub.groupby("arm").agg(acc=("correct", "mean"),
                              gold_prob=("gold_prob", "mean"))
L.append("```\n" + acc.round(3).to_string() + "\n```")

L.append("\n### Hedge-gold questions (F1, FT1, FT25, FT31) — forced-choice uncertainty (Arm D)\n")
hsub = probe[(probe.arm == "directional_menu") & probe.question_id.isin(HEDGE_GOLD)]
L.append("```\n" + hsub[["question_id", "eu_norm", "au_norm", "tu_norm",
                         "predicted"]].round(3).to_string(index=False) + "\n```")
L.append("(High AU/EU here = hedging was information-bearing; confident "
         "directional picks = hedging was surface style.)")

L.append("\n### Per-question arm detail\n```")
cols = ["question_id", "arm", "eu_norm", "au_norm", "predicted",
        "gold_label", "correct"]
pcols = [c for c in cols if c in probe.columns]
L.append(probe[pcols].round(3).to_string(index=False))
L.append("```")

# ── qwen replication ─────────────────────────────────────────────────────
L.append("\n## qwen3:8b replication (16 questions, R0+R1) vs gemma4\n")
gm = base.assign(model="gemma4")
qm = qwen.assign(model="qwen3:8b")
both = pd.concat([gm, qm], ignore_index=True)
both["hedge_pred"] = both["predicted"].isin(HEDGE)
rep = both.groupby(["model", "round"]).agg(
    eu=("eu_norm", "mean"), au=("au_norm", "mean"), tu=("tu_norm", "mean"),
    gold_prob=("gold_prob", "mean"), acc=("correct", "mean"),
    hedge_rate=("hedge_pred", "mean"),
    degenerate=("tu_norm", lambda s: float((s < 1e-9).mean())),
    parse=("parse_rate", "mean"))
L.append("```\n" + rep.round(3).to_string() + "\n```")

L.append("\n### Lane accuracy by model (final round)\n")
fin = both[both["round"] == 1]
la = fin.pivot_table(index="lane", columns="model", values="correct",
                     aggfunc="mean")
L.append("```\n" + la.round(2).to_string() + "\n```")

L.append("\n### AU drop R0->R1 by model (paired mean)\n")
for model, g in both.groupby("model"):
    r0 = g[g["round"] == 0].set_index("question_id")
    r1 = g[g["round"] == 1].set_index("question_id")
    idx = r0.index.intersection(r1.index)
    dau = (r1.loc[idx, "au_norm"] - r0.loc[idx, "au_norm"]).mean()
    deu = (r1.loc[idx, "eu_norm"] - r0.loc[idx, "eu_norm"]).mean()
    L.append(f"- {model}: mean dAU = {dau:+.3f}, mean dEU = {deu:+.3f} (n={len(idx)})")

L.append("\n### qwen per-question detail (final round)\n```")
qf = qwen[qwen["round"] == 1]
qcols = [c for c in ["question_id", "lane", "eu_norm", "au_norm",
                     "gold_prob", "predicted", "correct", "parse_rate"]
         if c in qf.columns]
L.append(qf[qcols].round(3).to_string(index=False))
L.append("```")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
