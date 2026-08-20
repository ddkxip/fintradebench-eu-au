"""Generic per-model full E-A analyzer (reanalysis only, no model calls).

Generalizes analyze_hf_qwen36.py so any run directory can be analyzed with
identical metric definitions. Also regenerates the cross-model comparison
table over every registered run.

Usage:
    python analysis/analyze_model_run.py --run ea_full_hf_gemma_4_31B_it \
        --model gemma4-31b-it --out HF_GEMMA4_31B_FULL_FINDINGS.md
"""

from __future__ import annotations

import argparse
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
schemas = load_schemas()

# every full-run registered for the cross-model table (subsets flagged)
ALL_RUNS = [
    ("ea_full_gemma4", "gemma4", 139),
    ("ea_full_qwen3", "qwen3:8b", 139),
    ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b", 139),
    ("ea_full_hf_gemma_4_31B_it", "gemma4-31b-it", 139),
    # NOTE ON THE TWO GEMINI ROWS. They are NOT interchangeable.
    #   gemini_subset16   ran with the Vertex default (extended thinking),
    #                     which is UNMATCHED against every other row here --
    #                     the Ollama path uses "think": False. It also covers
    #                     only 16 questions. Keep for provenance; do not quote.
    #   gemini_full139    ran with thinkingBudget=0, matching the local
    #                     models' no-reasoning config. This is the row that
    #                     belongs in the paper's cross-model table.
    ("gemini_subset16", "gemini-3.1-pro (think, 16q)", 16),
    ("gemini_full139", "gemini-3-flash", 139),
]
JUDGMENT_TYPES = ["yes_no_mixed", "supportive_judgment", "graded_judgment",
                  "valuation_judgment", "category_choice"]


def nc_set(q):
    return schemas[q].noncommit_set


def enrich(df):
    df["gold_label"] = df["question_id"].map(lambda q: schemas[q].gold_label)
    df["noncommit_is_gold"] = df["question_id"].map(
        lambda q: schemas[q].gold_label in nc_set(q))
    df["predicted_is_noncommit"] = df.apply(
        lambda r: str(r["predicted"]) in nc_set(r["question_id"])
        if pd.notna(r["predicted"]) else False, axis=1)
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


def analyze(run, model, out_name):
    new = load_run(run, model)
    nf = new[(new["round"] == 1) & new["correct"].notna()].copy()
    r0 = new[new["round"] == 0].set_index("question_id")
    r1 = new[new["round"] == 1].set_index("question_id")
    idx = r0.index.intersection(r1.index)

    L = [f"# {model} — full E-A findings\n",
         f"Reanalysis of `results/{run}/rows.csv` ({new.question_id.nunique()} "
         "headline-eligible questions, R0+R1, K=10 F/FT / 20 T). Metric "
         "definitions identical to analyze_ea_full.py; no new model calls.",
         f"- parse rate: {new.parse_rate.mean():.3f}; scored final rows: {len(nf)}\n"]

    # 1-2 accuracy
    overall = new[new["correct"].notna()].groupby("round")["correct"].mean()
    L.append("## 1-2. Accuracy (strict) by round and lane\n")
    L.append(f"- overall R0 acc = **{overall[0]:.3f}**, R1 acc = **{overall[1]:.3f}**")
    L.append("```\n" + new[new["correct"].notna()].groupby(["lane", "round"])["correct"]
             .mean().unstack().round(3).to_string() + "\n```")

    # 3 TU/AU/EU
    L.append("\n## 3. TU / AU / EU (normalized) + Miller-Madow by lane and round\n")
    L.append("```\n" + new.groupby(["lane", "round"])[
        ["tu_norm", "au_norm", "eu_norm", "au_mm", "eu_mm", "tu_mm"]]
        .mean().round(3).to_string() + "\n```")

    # 4 deltas
    L.append("\n## 4. Debate deltas R0->R1 (paired)\n")
    for col, nm in [("au_norm", "dAU"), ("eu_norm", "dEU"),
                    ("p_noncommit", "dNC"), ("gold_prob", "dG")]:
        x = (r1.loc[idx, col] - r0.loc[idx, col]).astype(float).values
        nz = x[x != 0]
        p = stats.wilcoxon(nz).pvalue if len(nz) >= 10 else float("nan")
        L.append(f"- {nm}: mean {x.mean():+.4f}, Wilcoxon p={p:.2e} "
                 f"(nonzero n={len(nz)})")

    # 5 p_noncommit
    L.append("\n## 5. p_noncommit by lane and round\n")
    L.append("```\n" + new.groupby(["lane", "round"])["p_noncommit"]
             .agg(["mean", "median"]).round(3).to_string() + "\n```")
    L.append(f"- degenerate rows (TU=0): {float((new['tu_norm'] < 1e-9).mean()):.3f} "
             f"overall; R1 {float((r1['tu_norm'] < 1e-9).mean()):.3f}")

    # 6 AUROC
    L.append("\n## 6. AUROC for error prediction (final round)\n")
    y = (~nf["correct"].astype(bool)).astype(int).values
    cg = nf[~nf["noncommit_is_gold"]]
    cc = nf[(~nf["noncommit_is_gold"]) & (~nf["predicted_is_noncommit"])]
    L.append(f"error rate = {y.mean():.2f}")
    L.append("| predictor | AUROC (all) | AUROC committed-gold | AUROC commit-gold&commit-pred |")
    L.append("|---|---|---|---|")
    for col in ["tu_norm", "au_norm", "eu_norm", "p_noncommit"]:
        L.append(f"| {col} | {auroc(y, nf[col].values):.3f} | "
                 f"{auroc((~cg['correct'].astype(bool)).astype(int).values, cg[col].values):.3f} | "
                 f"{auroc((~cc['correct'].astype(bool)).astype(int).values, cc[col].values):.3f} |")
    L.append(f"\n(committed-gold n={len(cg)}; committed-gold & committed-pred "
             f"n={len(cc)} — the non-mechanical cell.)")

    # 7 decomposition
    nf["strict_error"] = nf["predicted"].astype(str) != nf["gold_label"].astype(str)

    def etype(r):
        if not r["strict_error"]:
            return ("correct_noncommit" if r["noncommit_is_gold"]
                    and r["predicted_is_noncommit"] else "correct_committed")
        ng, npr = r["noncommit_is_gold"], r["predicted_is_noncommit"]
        if not ng and npr:
            return "hedge_collision"
        if ng and not npr:
            return "overcommitment"
        if not ng and not npr:
            return "wrong_direction_commitment"
        return "wrong_noncommit_type"

    nf["error_type"] = nf.apply(etype, axis=1)
    err = nf[nf["strict_error"]]
    L.append("\n## 7. Non-commitment error decomposition (final round)\n")
    L.append("```\n" + pd.concat([
        err["error_type"].value_counts().rename("n"),
        err["error_type"].value_counts(normalize=True).round(3).rename("share")],
        axis=1).to_string() + "\n```")
    ncg = nf[nf["noncommit_is_gold"]]
    hedged = ncg[ncg["predicted_is_noncommit"]]
    L.append(f"- non-committal gold questions: {len(ncg)}; correct-noncommitment "
             f"rate: {hedged['correct'].mean() if len(hedged) else float('nan'):.2f} "
             f"(n_hedged={len(hedged)})")
    L.append("\n### share of errors by lane\n```\n"
             + (err.groupby(["lane", "error_type"]).size()
                / err.groupby("lane").size()).round(3).to_string() + "\n```")

    # 8 transitions
    L.append("\n## 8. Debate transitions (R0->R1)\n")
    hi = float(r1["eu_norm"].quantile(2 / 3))
    recs = []
    for q in idx:
        a, b = r0.loc[q], r1.loc[q]
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

    # 9 cross-model comparison (all registered runs)
    L.append("\n## 9. Cross-model comparison\n")
    cmp_rows, lane_rows = [], []
    for run_i, model_i, nq in ALL_RUNS:
        p = RES / run_i / "rows.csv"
        if not p.exists():
            continue
        d = load_run(run_i, model_i)
        f = d[(d["round"] == 1) & d["correct"].notna()]
        z0 = d[d["round"] == 0].set_index("question_id")
        z1 = d[d["round"] == 1].set_index("question_id")
        ii = z0.index.intersection(z1.index)
        yy = (~f["correct"].astype(bool)).astype(int).values
        ccm = f[(~f["noncommit_is_gold"]) & (~f["predicted_is_noncommit"])]
        e = f[~f["correct"].astype(bool)]
        hedge_share = (e[~e.noncommit_is_gold & e.predicted_is_noncommit].shape[0]
                       / max(1, len(e)))
        cmp_rows.append({
            "model": model_i, "n_q": d.question_id.nunique(),
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
            "hedge_coll_share": round(hedge_share, 3),
        })
        for lane in ["F", "FT", "T"]:
            fl = f[f.lane == lane]
            lane_rows.append({"model": model_i, "lane": lane,
                              "acc": round(fl["correct"].mean(), 3) if len(fl) else np.nan})
    cmp = pd.DataFrame(cmp_rows)
    cmp.to_csv(REPO / "analysis" / "model_comparison_table.csv", index=False)
    L.append("(gemini = 16-q subset, flagged; not pooled with the 139-q models)\n")
    L.append("```\n" + cmp.to_string(index=False) + "\n```")
    L.append("\n### R1 strict accuracy by lane x model\n")
    L.append("```\n" + pd.DataFrame(lane_rows).pivot(
        index="lane", columns="model", values="acc").to_string() + "\n```")

    # 10 regime diagnostics
    L.append("\n## 10. Regime diagnostics (per lane, final round)\n")
    diag = []
    for lane in ["F", "FT", "T"]:
        fl = nf[nf.lane == lane]
        jl = fl[fl.answer_type.isin(JUDGMENT_TYPES)]
        diag.append({"lane": lane, "R1_EU": round(fl.eu_norm.mean(), 3),
                     "R1_pNC": round(fl.p_noncommit.mean(), 3),
                     "judgment_hedge_rate": round(jl.predicted_is_noncommit.mean(), 3)
                     if len(jl) else np.nan,
                     "acc": round(fl.correct.mean(), 3)})
    L.append("```\n" + pd.DataFrame(diag).to_string(index=False) + "\n```")

    (REPO / out_name).write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n[wrote {out_name} + analysis/model_comparison_table.csv]")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    analyze(a.run, a.model, a.out)
