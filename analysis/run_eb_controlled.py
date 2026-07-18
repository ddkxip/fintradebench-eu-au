"""E-B' controlled analysis over the full E-A' outputs.

Questions (EXPERIMENT_PLAN_EU_AU / STATISTICAL_ANALYSIS_PLAN_EU_AU):
  Q1 Does lane explain AU/EU after controls (model, |Y|, K, answer_type)?
  Q2 Matched-K robustness: does T-higher-AU survive when T-lane AU is
     recomputed from K=10 subsamples of its 20 decodes?
  Q3 Does AU / p_noncommit predict error net of controls (cluster-robust)?
  Q4 Does initial EU predict debate improvement (dG)? Does dEU predict dG?
  Q5 Does debate's hedging push (dNC) survive controls?

Units: question x model (round-0 state, round-1 outcomes, paired deltas).
Clustering: primary ticker (cluster-robust SEs / random intercepts).
Writes analysis/eu_au_controlled_analysis.md.
"""

from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from src.eu_au import counts_to_dist, decompose  # noqa: E402
from src.schema import load_schemas  # noqa: E402

RES = REPO / "results"
OUT = REPO / "analysis" / "eu_au_controlled_analysis.md"
HEDGE = {"mixed", "conditional", "insufficient_data", "none_clear"}
schemas = load_schemas()

frames = []
for run, model in [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3")]:
    d = pd.read_csv(RES / run / "rows.csv")
    d["model"] = model
    d["run"] = run
    frames.append(d)
rows = pd.concat(frames, ignore_index=True)
rows["ticker1"] = rows["tickers"].fillna("").map(
    lambda s: str(s).split("|")[0] or "NONE")
rows["space_n"] = rows["question_id"].map(
    lambda q: len(schemas[q].answer_space))
rows["answer_type"] = rows["question_id"].map(
    lambda q: schemas[q].answer_type)

r0 = rows[rows["round"] == 0].set_index(["question_id", "model"])
r1 = rows[rows["round"] == 1].set_index(["question_id", "model"])
idx = r0.index.intersection(r1.index)
q = r0.loc[idx].copy()
q["au0"], q["eu0"], q["tu0"] = q["au_mm"], q["eu_mm"], q["tu_norm"]
q["nc0"] = q["p_noncommit"]
q["au1"] = r1.loc[idx, "au_mm"]
q["eu1"] = r1.loc[idx, "eu_mm"]
q["nc1"] = r1.loc[idx, "p_noncommit"]
q["g0"] = q["gold_prob"]
q["g1"] = r1.loc[idx, "gold_prob"]
q["err1"] = (~r1.loc[idx, "correct"].astype(bool)).astype(int)
q["nc_fin"] = r1.loc[idx, "p_noncommit"]
q["tu_fin"] = r1.loc[idx, "tu_norm"]
q["d_g"] = q["g1"] - q["g0"]
q["d_eu"] = q["eu1"] - q["eu0"]
q["d_au"] = q["au1"] - q["au0"]
q["d_nc"] = q["nc1"] - q["nc0"]
q = q.reset_index()

L = ["# E-B' controlled analysis (139 q x 2 models; unit = question x model)\n",
     f"- n rows: {len(q)}; clusters (primary ticker): {q.ticker1.nunique()}"]

import statsmodels.formula.api as smf

pvals: list[tuple[str, float]] = []


def report_model(title: str, fit, keep_prefixes=("C(lane", "au0", "eu0",
                 "nc_fin", "tu_fin", "d_eu", "d_au", "np.log", "k_eff",
                 "C(model", "nc0")):
    L.append(f"\n### {title}\n```")
    tab = fit.summary2().tables[1]
    for name, row in tab.iterrows():
        if name == "Intercept" or any(str(name).startswith(p) for p in keep_prefixes):
            p = row.get("P>|z|", row.get("P>|t|", np.nan))
            L.append(f"{name:42s} coef={row['Coef.']:+.4f}  p={p:.3g}")
            if name != "Intercept" and np.isfinite(p):
                pvals.append((f"{title} :: {name}", float(p)))
    L.append("```")


# ── Q1: lane effects on AU/EU net of controls ───────────────────────────
q["k_eff"] = (q["k_eff_fundamental"].fillna(0) + q["k_eff_trading"].fillna(0)) / 2
L.append("\n## Q1 — lane effects on round-0 AU/EU (OLS, cluster-robust by ticker)\n")
L.append("Spec A controls model + log|Y| (+K collinear with lane by design; "
         "see Q2 for the matched-K answer). Spec B adds answer_type — the "
         "mechanism carrier that is partially confounded with lane "
         "(screenings are mostly T); both reported.")
for dv in ["au0", "eu0"]:
    fit = smf.ols(f"{dv} ~ C(lane, Treatment('F')) + C(model) + np.log(space_n)",
                  data=q).fit(cov_type="cluster",
                              cov_kwds={"groups": q["ticker1"]})
    report_model(f"Q1A {dv} ~ lane + model + log|Y|", fit)
    fit_b = smf.ols(f"{dv} ~ C(lane, Treatment('F')) + C(model) + "
                    f"np.log(space_n) + C(answer_type)", data=q
                    ).fit(cov_type="cluster", cov_kwds={"groups": q["ticker1"]})
    report_model(f"Q1B {dv} + answer_type control", fit_b)

# ── Q2: matched-K robustness for T-higher-AU ────────────────────────────
L.append("\n## Q2 — matched-K robustness (T-lane AU recomputed from K=10 "
         "subsamples of its 20 decodes; 50 resamples/question)\n")
rng = np.random.default_rng(7)
for run, model in [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3")]:
    raw_p = RES / "raw" / run / "decodes.jsonl"
    labs: dict = {}
    with raw_p.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r.get("round") != 0 or not r.get("parsed_label"):
                continue
            labs.setdefault((r["question_id"], r["agent"]), []).append(
                r["parsed_label"])
    t_qids = [s.question_id for s in schemas.values()
              if s.headline_eligible and s.lane == "T"]
    sub_au = []
    for qid in t_qids:
        space = schemas[qid].answer_space
        fl = labs.get((qid, "fundamental"), [])
        tl = labs.get((qid, "trading"), [])
        if len(fl) < 10 or len(tl) < 10:
            continue
        vals = []
        for _ in range(50):
            try:
                d = decompose({
                    "f": counts_to_dist(list(rng.choice(fl, 10, replace=False)), space),
                    "t": counts_to_dist(list(rng.choice(tl, 10, replace=False)), space),
                }, k_effective={"f": 10, "t": 10})
                vals.append(d.au_mm)
            except ValueError:
                continue
        if vals:
            sub_au.append(float(np.mean(vals)))
    ft_au = q[(q.model == model) & (q.lane != "T")]["au0"].astype(float)
    t_matched = np.array(sub_au)
    diff = t_matched.mean() - ft_au.mean()
    # simple bootstrap over questions
    diffs = [rng.choice(t_matched, len(t_matched)).mean()
             - rng.choice(ft_au.values, len(ft_au)).mean() for _ in range(4000)]
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    L.append(f"- {model}: T-lane AU_mm at matched K=10 = {t_matched.mean():.3f} "
             f"vs F/FT {ft_au.mean():.3f}; diff {diff:+.3f} "
             f"[{lo:+.3f}, {hi:+.3f}] -> "
             f"{'SUPPORTED' if lo > 0 else 'not supported'} at matched K")

# ── Q3: error prediction net of controls ────────────────────────────────
L.append("\n## Q3 — final-round error ~ uncertainty (logit, cluster-robust)\n")
for model, g in q.groupby("model"):
    try:
        fit = smf.logit("err1 ~ nc_fin + tu_fin + C(lane, Treatment('F'))",
                        data=g).fit(disp=0, cov_type="cluster",
                                    cov_kwds={"groups": g["ticker1"]})
        report_model(f"Q3 {model}: err ~ p_noncommit + TU + lane", fit)
    except Exception as exc:
        L.append(f"- {model}: logit failed ({exc}) — separation likely; "
                 f"see AUROC table in ea_full_summary.md")

# ── Q4: debate improvement models ───────────────────────────────────────
L.append("\n## Q4 — does initial EU predict improvement; does dEU predict dG?\n")
fit = smf.ols("d_g ~ eu0 + au0 + nc0 + C(lane, Treatment('F')) + C(model)",
              data=q).fit(cov_type="cluster", cov_kwds={"groups": q["ticker1"]})
report_model("Q4a dG ~ EU0 + AU0 + NC0 + lane + model", fit)
fit = smf.ols("d_g ~ d_eu + d_au + C(lane, Treatment('F')) + C(model)",
              data=q).fit(cov_type="cluster", cov_kwds={"groups": q["ticker1"]})
report_model("Q4b dG ~ dEU + dAU + lane + model", fit)

# ── Q5: hedging push net of controls ────────────────────────────────────
fit = smf.ols("d_nc ~ C(model) + C(lane, Treatment('F')) + nc0",
              data=q).fit(cov_type="cluster", cov_kwds={"groups": q["ticker1"]})
report_model("Q5 dNC ~ model + lane + NC0", fit)

# ── BH-FDR across the family ────────────────────────────────────────────
from statsmodels.stats.multitest import multipletests
names, ps = zip(*pvals)
rej, p_adj, *_ = multipletests(ps, alpha=0.05, method="fdr_bh")
L.append("\n## BH-FDR across all reported coefficients\n")
survivors = [(n, p, pa) for (n, p, pa, r) in zip(names, ps, p_adj, rej) if r]
L.append(f"- coefficients tested: {len(ps)}; surviving FDR(0.05): {len(survivors)}")
for n, p, pa in sorted(survivors, key=lambda x: x[2]):
    L.append(f"  - {n}  (p={p:.2g}, q={pa:.2g})")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
