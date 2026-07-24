"""Analyze the HF Qwen3.6-27B-FP8 full E-A run and compare to the existing
gemma4 / qwen3:8b / gemini runs. Reanalysis only (no model calls).

Reuses the metric definitions from analyze_ea_full.py and
noncommit_error_decomposition.py so numbers are directly comparable.
Writes HF_QWEN36_FULL_FINDINGS.md at repo root and a comparison CSV.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.schema import load_schemas  # noqa: E402
from src.transitions import RoundState, classify  # noqa: E402

RES = REPO / "results"
OUT = REPO / "HF_QWEN36_FULL_FINDINGS.md"
HEDGE_DEFAULT = {"mixed", "conditional", "insufficient_data", "none_clear"}
schemas = load_schemas()

NEW = ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b")
ALL_RUNS = [
    ("ea_full_gemma4", "gemma4"),
    ("ea_full_qwen3", "qwen3:8b"),
    NEW,
    ("gemini_subset16", "gemini-3.1-pro"),  # 16-q subset; flagged, not pooled
]


def nc_set(q):
    return schemas[q].noncommit_set


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    df["gold_label"] = df["question_id"].map(lambda q: schemas[q].gold_label)
    df["noncommit_is_gold"] = df["question_id"].map(
        lambda q: schemas[q].gold_label in nc_set(q))
    df["predicted_is_noncommit"] = df.apply(
        lambda r: str(r["predicted"]) in nc_set(r["question_id"])
        if pd.notna(r["predicted"]) else False, axis=1)
    df["ticker1"] = df["tickers"].fillna("").map(
        lambda s: str(s).split("|")[0] or "NONE")
    return df


def load_run(run, model):
    d = pd.read_csv(RES / run / "rows.csv")
    d["model"] = model
    return enrich(d)


def auroc(y, s):
    ok = np.isfinite(s)
    y, s = np.asarray(y)[ok], np.asarray(s)[ok]
    n1, n0 = int(y.sum()), len(y) - int(y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


new = load_run(*NEW)
nf = new[(new["round"] == 1) & new["correct"].notna()].copy()
n0 = new[new["round"] == 0].set_index("question_id")
n1 = new[new["round"] == 1].set_index("question_id")

L = ["# HF Qwen3.6-27B-FP8 — full E-A findings\n",
     "Reanalysis of results/ea_full_hf_qwen36_27b_fp8/rows.csv (139 "
     "headline-eligible questions, R0+R1, K=10 F/FT / 20 T). Metric "
     "definitions identical to analyze_ea_full.py; no new model calls.",
     f"- parse rate: {new.parse_rate.mean():.3f}; questions: "
     f"{new.question_id.nunique()}; scored final rows: {len(nf)}\n"]

# ── 1 & 2. accuracy overall + by lane/round ─────────────────────────────
L.append("## 1-2. Accuracy (strict) by round and lane\n")
acc = new[new["correct"].notna()].groupby(["lane", "round"])["correct"].mean().unstack()
overall = new[new["correct"].notna()].groupby("round")["correct"].mean()
L.append(f"- overall R0 acc = **{overall[0]:.3f}**, R1 acc = **{overall[1]:.3f}**")
L.append("```\n" + acc.round(3).to_string() + "\n```")

# ── 3. TU/AU/EU by lane/round ───────────────────────────────────────────
L.append("\n## 3. TU / AU / EU (normalized) + Miller-Madow by lane and round\n")
u = new.groupby(["lane", "round"])[
    ["tu_norm", "au_norm", "eu_norm", "au_mm", "eu_mm", "tu_mm"]].mean()
L.append("```\n" + u.round(3).to_string() + "\n```")

# ── 4. debate deltas ────────────────────────────────────────────────────
L.append("\n## 4. Debate deltas R0->R1 (paired, n=139)\n")
idx = n0.index.intersection(n1.index)
for col, nm in [("au_norm", "dAU"), ("eu_norm", "dEU"), ("p_noncommit", "dNC"),
                ("gold_prob", "dG")]:
    x = (n1.loc[idx, col] - n0.loc[idx, col]).astype(float).values
    nz = x[x != 0]
    p = stats.wilcoxon(nz).pvalue if len(nz) >= 10 else float("nan")
    L.append(f"- {nm}: mean {x.mean():+.4f}, Wilcoxon p={p:.2e} (nonzero n={len(nz)})")

# ── 5. p_noncommit by lane/round ────────────────────────────────────────
L.append("\n## 5. p_noncommit by lane and round\n")
pnc = new.groupby(["lane", "round"])["p_noncommit"].agg(["mean", "median"])
L.append("```\n" + pnc.round(3).to_string() + "\n```")
L.append(f"- degenerate rows (TU=0): "
         f"{float((new['tu_norm'] < 1e-9).mean()):.3f} overall; "
         f"R1 {float((n1['tu_norm'] < 1e-9).mean()):.3f}")

# ── 6. AUROC error prediction (final round) ─────────────────────────────
L.append("\n## 6. AUROC for error prediction (final round)\n")
y = (~nf["correct"].astype(bool)).astype(int).values
L.append(f"error rate = {y.mean():.2f}")
L.append("| predictor | AUROC (all) | AUROC committed-gold | AUROC commit-gold&commit-pred |")
L.append("|---|---|---|---|")
cg = nf[~nf["noncommit_is_gold"]]
cc = nf[(~nf["noncommit_is_gold"]) & (~nf["predicted_is_noncommit"])]
for col in ["tu_norm", "au_norm", "eu_norm", "p_noncommit"]:
    a_all = auroc(y, nf[col].values)
    a_cg = auroc((~cg["correct"].astype(bool)).astype(int).values, cg[col].values)
    a_cc = auroc((~cc["correct"].astype(bool)).astype(int).values, cc[col].values)
    L.append(f"| {col} | {a_all:.3f} | {a_cg:.3f} | {a_cc:.3f} |")
L.append(f"\n(committed-gold n={len(cg)}; committed-gold & committed-pred "
         f"n={len(cc)} — the non-mechanical cell.)")

# ── 7. noncommit error decomposition ────────────────────────────────────
L.append("\n## 7. Non-commitment error decomposition (final round)\n")
nf["strict_error"] = nf["predicted"].astype(str) != nf["gold_label"].astype(str)
def etype(r):
    if not r["strict_error"]:
        return "correct_noncommit" if r["noncommit_is_gold"] and r["predicted_is_noncommit"] else "correct_committed"
    if not r["noncommit_is_gold"] and r["predicted_is_noncommit"]:
        return "hedge_collision"
    if r["noncommit_is_gold"] and not r["predicted_is_noncommit"]:
        return "overcommitment"
    if not r["noncommit_is_gold"] and not r["predicted_is_noncommit"]:
        return "wrong_direction_commitment"
    return "wrong_noncommit_type"
nf["error_type"] = nf.apply(etype, axis=1)
err = nf[nf["strict_error"]]
comp = pd.concat([err["error_type"].value_counts().rename("n"),
                  err["error_type"].value_counts(normalize=True).round(3).rename("share")],
                 axis=1)
L.append("```\n" + comp.to_string() + "\n```")
# correct noncommitment: how often hedging is right when gold is noncommittal
ncg_rows = nf[nf["noncommit_is_gold"]]
if len(ncg_rows):
    hedged = ncg_rows[ncg_rows["predicted_is_noncommit"]]
    L.append(f"- non-committal gold questions: {len(ncg_rows)}; "
             f"correct-noncommitment rate (hedge right when gold hedges): "
             f"{hedged['correct'].mean() if len(hedged) else float('nan'):.2f} "
             f"(n_hedged={len(hedged)})")
L.append("\n### share of errors by lane\n```\n"
         + (err.groupby(["lane", "error_type"]).size()
            / err.groupby("lane").size()).round(3).to_string() + "\n```")

# ── 8. transitions ──────────────────────────────────────────────────────
L.append("\n## 8. Debate transitions (R0->R1)\n")
hi = float(n1["eu_norm"].quantile(2 / 3))
recs = []
for q in idx:
    a, b = n0.loc[q], n1.loc[q]
    if pd.isna(a["correct"]) or pd.isna(b["correct"]):
        continue
    s0 = RoundState(a.eu_norm, a.au_norm, a.gold_prob, bool(a.correct),
                    {"f": a.agent_gold_prob_fundamental, "t": a.agent_gold_prob_trading})
    s1 = RoundState(b.eu_norm, b.au_norm, b.gold_prob, bool(b.correct),
                    {"f": b.agent_gold_prob_fundamental, "t": b.agent_gold_prob_trading})
    tr = classify(s0, s1, high_eu_threshold=hi)
    recs.append({"outcome": tr.outcome, "flow": tr.flow,
                 "cms": tr.correct_minority_suppression})
t = pd.DataFrame(recs)
L.append(f"- outcome: {t.outcome.value_counts().to_dict()}")
L.append(f"- flow: {t.flow.value_counts().to_dict()}")
L.append(f"- rescue: {int((t.outcome=='DEBATE_RESCUE').sum())}, "
         f"loss: {int((t.outcome=='CORRECTNESS_LOST').sum())}, "
         f"stable-correct: {int((t.outcome=='STABLE_SUCCESS').sum())}, "
         f"stable-wrong: {int((t.outcome=='STABLE_FAILURE').sum())}")
L.append(f"- false consensus: {int((t.flow=='FALSE_CONSENSUS').sum())} "
         f"({(t.flow=='FALSE_CONSENSUS').mean():.1%}); "
         f"minority suppression: {int(t.cms.sum())}")

# ── 9. cross-model comparison ───────────────────────────────────────────
L.append("\n## 9. Cross-model comparison\n")
comp_rows = []
for run, model in ALL_RUNS:
    d = load_run(run, model)
    f = d[(d["round"] == 1) & d["correct"].notna()]
    z0 = d[d["round"] == 0].set_index("question_id")
    z1 = d[d["round"] == 1].set_index("question_id")
    ii = z0.index.intersection(z1.index)
    yy = (~f["correct"].astype(bool)).astype(int).values
    cgm = f[~f["noncommit_is_gold"]]
    ccm = f[(~f["noncommit_is_gold"]) & (~f["predicted_is_noncommit"])]
    comp_rows.append({
        "model": model, "n_q": d.question_id.nunique(),
        "R0_acc": round(d[d["round"] == 0]["correct"].mean(), 3),
        "R1_acc": round(f["correct"].mean(), 3),
        "R1_EU": round(f["eu_norm"].mean(), 3),
        "R1_AU": round(f["au_norm"].mean(), 3),
        "R1_pNC": round(f["p_noncommit"].mean(), 3),
        "dAU": round((z1.loc[ii, "au_norm"] - z0.loc[ii, "au_norm"]).mean(), 3),
        "dEU": round((z1.loc[ii, "eu_norm"] - z0.loc[ii, "eu_norm"]).mean(), 3),
        "dNC": round((z1.loc[ii, "p_noncommit"] - z0.loc[ii, "p_noncommit"]).mean(), 3),
        "degen_R1": round(float((z1["tu_norm"] < 1e-9).mean()), 3),
        "AUROC_pNC_all": round(auroc(yy, f["p_noncommit"].values), 3),
        "AUROC_pNC_commitcell": round(
            auroc((~ccm["correct"].astype(bool)).astype(int).values,
                  ccm["p_noncommit"].values), 3) if len(ccm) >= 8 else np.nan,
        "hedge_coll_share": round(
            (f[~f.correct.astype(bool) & ~f.noncommit_is_gold
               & f.predicted_is_noncommit].shape[0]
             / max(1, (~f.correct.astype(bool)).sum())), 3),
    })
cmp = pd.DataFrame(comp_rows)
cmp.to_csv(REPO / "analysis" / "model_comparison_table.csv", index=False)
L.append("(gemini = 16-q subset, flagged; not pooled with the 139-q models)\n")
L.append("```\n" + cmp.to_string(index=False) + "\n```")

# lane accuracy matrix across models
L.append("\n### R1 strict accuracy by lane x model\n")
lane_rows = []
for run, model in ALL_RUNS:
    d = load_run(run, model)
    f = d[(d["round"] == 1) & d["correct"].notna()]
    for lane in ["F", "FT", "T"]:
        lane_rows.append({"model": model, "lane": lane,
                          "acc": round(f[f.lane == lane]["correct"].mean(), 3)
                          if len(f[f.lane == lane]) else np.nan})
lane_piv = pd.DataFrame(lane_rows).pivot(index="lane", columns="model", values="acc")
L.append("```\n" + lane_piv.to_string() + "\n```")

# ── 10. regime verdict ──────────────────────────────────────────────────
L.append("\n## 10. Regime verdict\n")
# compute the diagnostic per lane for qwen3.6
lane_diag = []
for lane in ["F", "FT", "T"]:
    fl = nf[nf.lane == lane]
    jl = fl[fl.answer_type.isin(["yes_no_mixed", "supportive_judgment",
                                 "graded_judgment", "valuation_judgment",
                                 "category_choice"])]
    lane_diag.append({
        "lane": lane, "R1_EU": round(fl.eu_norm.mean(), 3),
        "R1_pNC": round(fl.p_noncommit.mean(), 3),
        "judgment_hedge_rate": round(jl.predicted_is_noncommit.mean(), 3)
        if len(jl) else np.nan,
        "acc": round(fl.correct.mean(), 3)})
ld = pd.DataFrame(lane_diag)
L.append("Per-lane regime diagnostics (qwen3.6-27b, final round):\n")
L.append("```\n" + ld.to_string(index=False) + "\n```")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
