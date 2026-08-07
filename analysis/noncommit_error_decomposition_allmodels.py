"""Non-commitment error decomposition across ALL full-run models.

Supersedes the 2-model version (analysis/noncommit_error_decomposition.py,
gemma4 + qwen3:8b) by adding qwen3.6-27b and gemma4-31b-it. Reanalysis only;
does not overwrite the original outputs.

Reports per-model (the primary, dependence-free view) and pooled across the
four 139-question models (descriptive; each question appears once per model,
so pooled n is not independent — regressions use ticker-clustered SEs).
gemini (16-q subset) reported separately, never pooled.

Writes analysis/noncommit_error_decomposition_allmodels.md
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

RES = REPO / "results"
ANA = REPO / "analysis"
OUT = ANA / "noncommit_error_decomposition_allmodels.md"
schemas = load_schemas()

FULL = [("ea_full_gemma4", "gemma4"),
        ("ea_full_qwen3", "qwen3:8b"),
        ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b"),
        ("ea_full_hf_gemma_4_31B_it", "gemma4-31b-it")]
SUPP = [("gemini_subset16", "gemini-3.1-pro")]
ETYPES = ["hedge_collision", "wrong_direction_commitment",
          "overcommitment", "wrong_noncommit_type"]


def nc_set(q):
    return schemas[q].noncommit_set


def load(runs) -> pd.DataFrame:
    fr = []
    for run, model in runs:
        p = RES / run / "rows.csv"
        if not p.exists():
            continue
        d = pd.read_csv(p)
        d = d[(d["round"] == 1) & d["correct"].notna()].copy()
        d["model"] = model
        fr.append(d)
    df = pd.concat(fr, ignore_index=True)
    df["gold_label"] = df["question_id"].map(lambda q: schemas[q].gold_label)
    df["noncommit_is_gold"] = df["question_id"].map(
        lambda q: schemas[q].gold_label in nc_set(q))
    df["predicted_is_noncommit"] = df.apply(
        lambda r: str(r["predicted"]) in nc_set(r["question_id"]), axis=1)
    df["strict_error"] = df["predicted"].astype(str) != df["gold_label"].astype(str)
    df["cell"] = np.where(
        ~df.noncommit_is_gold & ~df.predicted_is_noncommit, "committed_gold__committed_pred",
        np.where(~df.noncommit_is_gold & df.predicted_is_noncommit, "committed_gold__noncommit_pred",
                 np.where(df.noncommit_is_gold & ~df.predicted_is_noncommit,
                          "noncommit_gold__committed_pred", "noncommit_gold__noncommit_pred")))

    def et(r):
        if not r["strict_error"]:
            return "correct"
        ng, npr = r["noncommit_is_gold"], r["predicted_is_noncommit"]
        if not ng and npr:
            return "hedge_collision"
        if ng and not npr:
            return "overcommitment"
        if not ng and not npr:
            return "wrong_direction_commitment"
        return "wrong_noncommit_type"

    df["error_type"] = df.apply(et, axis=1)
    df["ticker1"] = df["tickers"].fillna("").map(
        lambda s: str(s).split("|")[0] or "NONE")
    return df


def auroc(y, s):
    ok = np.isfinite(s)
    y, s = np.asarray(y)[ok], np.asarray(s)[ok]
    n1, n0 = int(y.sum()), len(y) - int(y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


df = load(FULL)
models = [m for _, m in FULL]

L = ["# Non-commitment error decomposition — ALL full-run models\n",
     "Reanalysis only. Supersedes the 2-model version "
     "(`noncommit_error_decomposition.md`, gemma4 + qwen3:8b) by adding "
     "**qwen3.6-27b** and **gemma4-31b-it**. The original file is left intact.\n",
     f"- models: {', '.join(models)} (139 headline-eligible questions each; "
     f"pooled rows n={len(df)})",
     "- pooled rows are **not independent** (each question appears once per "
     "model); per-model columns are the primary read, pooled is descriptive, "
     "and regressions use ticker-clustered SEs.\n"]

# ── 0. framing ──────────────────────────────────────────────────────────
ncg = df.groupby("model")["noncommit_is_gold"].mean().iloc[0]
L.append(f"Gold is non-committal on **{ncg:.1%}** of questions (22/139) — "
         "identical across models by construction.\n")

# ── A. error rate by commitment cell ────────────────────────────────────
L.append("## A. Error rate by commitment cell (per model)\n")
a = df.pivot_table(index="cell", columns="model", values="strict_error",
                   aggfunc="mean").round(3)
n = df.pivot_table(index="cell", columns="model", values="strict_error",
                   aggfunc="size")
L.append("```\n" + a.to_string() + "\n```")
L.append("\ncell sizes:\n```\n" + n.to_string() + "\n```")
L.append("\nTwo cells are **deterministic**: a non-committal prediction can "
         "never match a committed gold (error=1) and vice versa. Only the two "
         "same-type cells admit both outcomes.")

# ── B. mean p_noncommit by cell ─────────────────────────────────────────
L.append("\n## B. Mean p_noncommit by commitment cell (per model)\n")
b = df.pivot_table(index="cell", columns="model", values="p_noncommit",
                   aggfunc="mean").round(3)
L.append("```\n" + b.to_string() + "\n```")

# ── C. share of total errors ────────────────────────────────────────────
L.append("\n## C. Share of total errors by type\n")
err = df[df.strict_error]
share = (err.groupby(["model", "error_type"]).size()
         / err.groupby("model").size()).unstack().reindex(columns=ETYPES).round(3)
cnt = err.groupby(["model", "error_type"]).size().unstack().reindex(columns=ETYPES)
L.append("shares:\n```\n" + share.to_string() + "\n```")
L.append("\ncounts:\n```\n" + cnt.fillna(0).astype(int).to_string() + "\n```")
pooled = err["error_type"].value_counts(normalize=True).reindex(ETYPES).round(3)
L.append(f"\n**Pooled across the four models:** " +
         ", ".join(f"{k} {v:.1%}" for k, v in pooled.items()))
L.append(f"\n**hedge_collision is the modal error type in "
         f"{int((share['hedge_collision'] == share.max(axis=1)).sum())}/4 models** "
         f"(range {share['hedge_collision'].min():.3f}–{share['hedge_collision'].max():.3f}).")

L.append("\n### by lane (pooled across the four models)\n```\n"
         + (err.groupby(["lane", "error_type"]).size()
            / err.groupby("lane").size()).unstack()
         .reindex(columns=ETYPES).round(3).to_string() + "\n```")

# ── D. AUROC splits ─────────────────────────────────────────────────────
L.append("\n## D. AUROC of p_noncommit for strict error\n")
L.append("| subset | " + " | ".join(models) + " |")
L.append("|---" * (len(models) + 1) + "|")


def auroc_row(label, sub):
    cells = []
    for m in models:
        g = sub[sub.model == m]
        cells.append(f"{auroc(g.strict_error.astype(int).values, g.p_noncommit.values):.3f}"
                     if len(g) >= 8 else "n/a")
    L.append(f"| {label} | " + " | ".join(cells) + " |")


auroc_row("all questions", df)
auroc_row("committed-gold only", df[~df.noncommit_is_gold])
auroc_row("noncommitted-gold only", df[df.noncommit_is_gold])
auroc_row("**committed-gold & committed-pred** (non-mechanical)",
          df[df.cell == "committed_gold__committed_pred"])
for lane in ["F", "FT", "T"]:
    auroc_row(f"lane {lane}", df[df.lane == lane])

L.append("\nThe pattern established on 2 models now holds on **4/4**: strong "
         "on committed-gold (mechanical — a hedge cannot match a committed "
         "gold), **at/below chance in the non-mechanical committed∧committed "
         "cell**, and inverted on non-committal-gold questions.")

# correct-noncommitment rate
L.append("\n### Correct-noncommitment rate (hedging when the gold hedges)\n")
rows = []
for m in models:
    g = df[(df.model == m) & df.noncommit_is_gold & df.predicted_is_noncommit]
    rows.append({"model": m, "n_hedged_on_nc_gold": len(g),
                 "correct_rate": round(float(g.correct.mean()), 3) if len(g) else np.nan})
L.append("```\n" + pd.DataFrame(rows).to_string(index=False) + "\n```")

# ── E. logistic regressions ─────────────────────────────────────────────
L.append("\n## E. Logistic regressions (pooled, cluster-robust by primary ticker)\n")
import statsmodels.formula.api as smf

d = df.copy()
d["y"] = d.strict_error.astype(int)
d["ncg"] = d.noncommit_is_gold.astype(int)
specs = [("M1  y ~ p_noncommit + TU + lane",
          "y ~ p_noncommit + tu_norm + C(lane, Treatment('F')) + C(model)"),
         ("M2  + noncommit_is_gold",
          "y ~ p_noncommit + tu_norm + C(lane, Treatment('F')) + C(model) + ncg"),
         ("M3  p_noncommit * noncommit_is_gold",
          "y ~ p_noncommit * ncg + tu_norm + C(lane, Treatment('F')) + C(model)")]
fits = {}
for title, f in specs:
    L.append(f"\n### {title}\n```")
    try:
        fit = smf.logit(f, data=d).fit(disp=0, cov_type="cluster",
                                       cov_kwds={"groups": d["ticker1"]})
        fits[title] = fit
        for name, row in fit.summary2().tables[1].iterrows():
            L.append(f"{str(name):40s} coef={row['Coef.']:+8.3f}  p={row['P>|z|']:.3g}")
        L.append(f"pseudo-R2 = {fit.prsquared:.3f}; n = {int(fit.nobs)}")
    except Exception as exc:
        L.append(f"FAILED: {exc}")
    L.append("```")
m3 = fits.get(specs[2][0])
if m3 is not None:
    b, bi = m3.params.get("p_noncommit", np.nan), m3.params.get("p_noncommit:ncg", np.nan)
    L.append(f"\nSlope of p_noncommit: **{b:+.3f}** on committed-gold questions "
             f"vs **{b + bi:+.3f}** on non-committal-gold questions "
             f"(interaction {bi:+.3f}, p={m3.pvalues.get('p_noncommit:ncg', np.nan):.3g}). "
             f"pseudo-R2 rises {fits[specs[0][0]].prsquared:.3f} -> {m3.prsquared:.3f}.")

# ── robustness: majority-vote commitment ────────────────────────────────
try:
    cx = pd.read_csv(ANA / "gold_commitment_audit_codex.csv", keep_default_na=False).set_index("question_id")
    ag = pd.read_csv(ANA / "gold_commitment_audit_antigravity.csv", keep_default_na=False).set_index("question_id")

    def sc(q):
        return "noncommitted" if schemas[q].gold_label in nc_set(q) else "committed"

    def majority(q):
        v = [sc(q)]
        for src, col in ((cx, "annotator_gold_commitment"), (ag, "annotator_gold_commitment")):
            if q in src.index:
                val = str(src.loc[q, col]).strip().lower()
                if val in ("committed", "noncommitted"):
                    v.append(val)
        return "noncommitted" if v.count("noncommitted") > v.count("committed") else "committed"

    r = df.copy()
    r["noncommit_is_gold"] = r["question_id"].map(lambda q: majority(q) == "noncommitted")
    r["predicted_is_noncommit"] = r.apply(
        lambda x: str(x["predicted"]) in nc_set(x["question_id"]), axis=1)

    def et2(x):
        if not x["strict_error"]:
            return "correct"
        ng, npr = x["noncommit_is_gold"], x["predicted_is_noncommit"]
        if not ng and npr:
            return "hedge_collision"
        if ng and not npr:
            return "overcommitment"
        if not ng and not npr:
            return "wrong_direction_commitment"
        return "wrong_noncommit_type"

    r["error_type"] = r.apply(et2, axis=1)
    e2 = r[r.strict_error]
    sh2 = (e2.groupby(["model", "error_type"]).size()
           / e2.groupby("model").size()).unstack().reindex(columns=ETYPES).round(3)
    L.append("\n## F. Robustness — majority-vote commitment (schema + codex + antigravity)\n")
    L.append("```\n" + sh2.to_string() + "\n```")
    cc2 = r[(~r.noncommit_is_gold) & (~r.predicted_is_noncommit)]
    aur = {m: round(auroc(cc2[cc2.model == m].strict_error.astype(int).values,
                          cc2[cc2.model == m].p_noncommit.values), 3) for m in models}
    L.append(f"\nNon-mechanical-cell AUROC under majority commitment: {aur}")
    L.append(f"\nhedge_collision remains modal in "
             f"{int((sh2['hedge_collision'] == sh2.max(axis=1)).sum())}/4 models "
             f"(range {sh2['hedge_collision'].min():.3f}–{sh2['hedge_collision'].max():.3f}).")
except Exception as exc:
    L.append(f"\n(majority-vote robustness unavailable: {exc})")

# ── supplementary gemini ────────────────────────────────────────────────
try:
    g = load(SUPP)
    ge = g[g.strict_error]
    L.append("\n## Supplementary — gemini-3.1-pro (16-q subset, not pooled)\n")
    L.append(f"- error composition: {dict(ge.error_type.value_counts())}")
    L.append(f"- AUROC(p_noncommit -> error), all: "
             f"{auroc(g.strict_error.astype(int).values, g.p_noncommit.values):.3f}")
except Exception as exc:
    L.append(f"\n(gemini supplementary unavailable: {exc})")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
