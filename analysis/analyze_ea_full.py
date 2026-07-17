"""E-A' full-run analysis (139 questions x 2 models x 2 rounds).

Produces results/ea_full_summary.md:
- lane x round EU/AU/TU (normalized + Miller-Madow) + p_noncommit
- paired R0->R1 Wilcoxon per model
- transition taxonomy rates at scale (PRD absolute floor applied)
- strict vs lenient scoring (lenient credits predictions named in the
  gold evidence/canonical claim - runner-up credit for screenings)
- confirmatory RQ3 tests: T-higher-AU, FT-higher-EU (cluster bootstrap
  by primary ticker; MM-corrected for the K=10-vs-20 asymmetry)
- RQ6: error prediction AUROC for EU/AU/TU/p_noncommit
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas
from src.transitions import RoundState, classify

RES = REPO / "results"
OUT = RES / "ea_full_summary.md"
HEDGE = {"mixed", "conditional", "insufficient_data", "none_clear"}
schemas = load_schemas()

frames = []
for run, model in [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3:8b")]:
    df = pd.read_csv(RES / run / "rows.csv")
    df["model"] = model
    frames.append(df)
df = pd.concat(frames, ignore_index=True)
df["noncommit_pred"] = df["predicted"].isin(HEDGE)
df["ticker1"] = df["tickers"].fillna("").map(lambda s: str(s).split("|")[0] or "NONE")

# lenient scoring: strict-correct OR predicted label named in gold evidence
def lenient(row) -> bool:
    if row.get("correct") is True or row.get("correct") == True:  # noqa: E712
        return True
    s = schemas[row["question_id"]]
    txt = (s.gold_label_evidence + " " + s.canonical_claim).lower()
    p = str(row["predicted"]).lower()
    return len(p) >= 2 and p not in HEDGE and p in txt

df["correct_lenient"] = df.apply(lenient, axis=1)

L = [f"# E-A' full-run summary (139 questions, gemma4 + qwen3:8b, R0+R1)\n",
     f"- rows: {len(df)}; parse mean {df.parse_rate.mean():.3f}"]

# ── lane x round x model core table ─────────────────────────────────────
core = df.groupby(["model", "lane", "round"]).agg(
    eu=("eu_norm", "mean"), au=("au_norm", "mean"), tu=("tu_norm", "mean"),
    au_mm=("au_mm", "mean"), eu_mm=("eu_mm", "mean"),
    p_noncommit=("p_noncommit", "mean"),
    gold_prob=("gold_prob", "mean"),
    acc=("correct", "mean"), acc_lenient=("correct_lenient", "mean"),
    degenerate=("tu_norm", lambda s: float((s < 1e-9).mean())))
L.append("\n## Core table: model x lane x round\n")
L.append("```\n" + core.round(3).to_string() + "\n```")

# ── paired deltas + Wilcoxon per model ──────────────────────────────────
L.append("\n## Paired R0->R1 (per model, n=139)\n")
for model, g in df.groupby("model"):
    r0 = g[g["round"] == 0].set_index("question_id")
    r1 = g[g["round"] == 1].set_index("question_id")
    idx = r0.index.intersection(r1.index)
    for col, name in [("au_norm", "dAU"), ("eu_norm", "dEU"),
                      ("gold_prob", "dG"), ("p_noncommit", "dNC")]:
        x = (r1.loc[idx, col] - r0.loc[idx, col]).astype(float).values
        nz = x[x != 0]
        if len(nz) >= 10:
            w = stats.wilcoxon(nz)
            L.append(f"- {model} {name}: mean {x.mean():+.4f}, "
                     f"Wilcoxon p={w.pvalue:.2e} (nonzero n={len(nz)})")
        else:
            L.append(f"- {model} {name}: mean {x.mean():+.4f} (nonzero n={len(nz)})")

# ── transition taxonomy at scale ────────────────────────────────────────
L.append("\n## Transition taxonomy (R0->R1)\n")
for model, g in df.groupby("model"):
    r0 = g[g["round"] == 0].set_index("question_id")
    r1 = g[g["round"] == 1].set_index("question_id")
    idx = r0.index.intersection(r1.index)
    hi = float(r1["eu_norm"].quantile(2 / 3))
    recs = []
    for q in idx:
        a, b = r0.loc[q], r1.loc[q]
        s0 = RoundState(a.eu_norm, a.au_norm, a.gold_prob, bool(a.correct),
                        {"f": a.agent_gold_prob_fundamental,
                         "t": a.agent_gold_prob_trading})
        s1 = RoundState(b.eu_norm, b.au_norm, b.gold_prob, bool(b.correct),
                        {"f": b.agent_gold_prob_fundamental,
                         "t": b.agent_gold_prob_trading})
        tr = classify(s0, s1, high_eu_threshold=hi)
        recs.append({"q": q, "lane": a.lane, "outcome": tr.outcome,
                     "flow": tr.flow, "cms": tr.correct_minority_suppression,
                     "prd": tr.persistent_rational_disagreement})
    t = pd.DataFrame(recs)
    t.to_csv(RES / f"transitions_{model.replace(':', '_')}.csv", index=False)
    L.append(f"### {model}")
    L.append(f"- outcome: {t.outcome.value_counts().to_dict()}")
    L.append(f"- flow: {t.flow.value_counts().to_dict()}")
    L.append(f"- false consensus: {int((t.flow == 'FALSE_CONSENSUS').sum())}"
             f" ({(t.flow == 'FALSE_CONSENSUS').mean():.1%}); "
             f"minority suppression: {int(t.cms.sum())}; "
             f"PRD (floored): {int(t.prd.sum())}")
    L.append(f"- rescue: {int((t.outcome == 'DEBATE_RESCUE').sum())}, "
             f"lost: {int((t.outcome == 'CORRECTNESS_LOST').sum())}")

# ── RQ3 confirmatory: T-higher-AU, FT-higher-EU (cluster bootstrap) ─────
L.append("\n## RQ3 confirmatory tests (round 0, MM-corrected, "
         "cluster bootstrap by primary ticker, 4000 resamples)\n")
rng = np.random.default_rng(42)

def cluster_boot_diff(g: pd.DataFrame, col: str, lane_a: str, lane_b) -> tuple:
    obs_a = g[g.lane == lane_a][col].mean()
    obs_b = g[g.lane.isin(lane_b)][col].mean()
    tickers = g["ticker1"].unique()
    by_t = {t: g[g.ticker1 == t] for t in tickers}
    diffs = []
    for _ in range(4000):
        pick = rng.choice(tickers, len(tickers), replace=True)
        bs = pd.concat([by_t[t] for t in pick])
        a = bs[bs.lane == lane_a][col]
        b = bs[bs.lane.isin(lane_b)][col]
        if len(a) and len(b):
            diffs.append(a.mean() - b.mean())
    lo, hiq = np.percentile(diffs, [2.5, 97.5])
    return obs_a - obs_b, lo, hiq

for model, g0 in df[df["round"] == 0].groupby("model"):
    d, lo, hi_ = cluster_boot_diff(g0, "au_mm", "T", ["F", "FT"])
    L.append(f"- {model} **T-higher-AU** (AU_mm, T minus F/FT): "
             f"{d:+.4f} [95% CI {lo:+.4f}, {hi_:+.4f}] "
             f"{'SUPPORTED' if lo > 0 else 'not supported'}")
    d, lo, hi_ = cluster_boot_diff(g0, "eu_mm", "FT", ["F", "T"])
    L.append(f"- {model} **FT-higher-EU** (EU_mm, FT minus F/T): "
             f"{d:+.4f} [95% CI {lo:+.4f}, {hi_:+.4f}] "
             f"{'SUPPORTED' if lo > 0 else 'not supported'}")

# ── RQ6: error prediction AUROC (final round) ───────────────────────────
L.append("\n## RQ6: error-prediction AUROC (final round, per model)\n")

def auroc(y: np.ndarray, s: np.ndarray) -> float:
    r = stats.rankdata(s)
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

fin = df[df["round"] == 1].dropna(subset=["correct"])
for model, g in fin.groupby("model"):
    y = (~g["correct"].astype(bool)).astype(int).values  # 1 = error
    L.append(f"### {model} (error rate {y.mean():.2f})")
    for col in ["tu_norm", "au_norm", "eu_norm", "p_noncommit"]:
        L.append(f"- AUROC({col} -> error) = {auroc(y, g[col].values):.3f}")

# ── strict vs lenient overall ───────────────────────────────────────────
L.append("\n## Strict vs lenient accuracy (final round)\n")
lt = fin.groupby(["model", "lane"])[["correct", "correct_lenient"]].mean()
L.append("```\n" + lt.round(3).to_string() + "\n```")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
