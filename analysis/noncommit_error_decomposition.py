"""Committed-vs-noncommitted error decomposition (reanalysis only, no model calls).

Answers the paper question: does p_noncommit predict error mainly because
models emit non-committal labels on questions whose GOLD is committed
(hedge collision), or does it carry error signal more generally?

Primary set: ea_full_gemma4 + ea_full_qwen3 (139 headline-eligible q each,
final round). gemini_subset16 (16 q) reported separately as supplementary —
different, smaller question subset, never pooled with the primary set.

Writes analysis/noncommit_error_decomposition.md.
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
OUT = REPO / "analysis" / "noncommit_error_decomposition.md"
schemas = load_schemas()

PRIMARY = [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3")]
SUPP = [("gemini_subset16", "gemini-3.1-pro")]


def load(runs) -> pd.DataFrame:
    fr = []
    for run, model in runs:
        d = pd.read_csv(RES / run / "rows.csv")
        d = d[(d["round"] == 1) & d["correct"].notna()].copy()
        d["model"] = model
        fr.append(d)
    df = pd.concat(fr, ignore_index=True)

    def nc_set(q):
        return schemas[q].noncommit_set

    df["gold_label"] = df["question_id"].map(lambda q: schemas[q].gold_label)
    df["noncommit_is_gold"] = df["question_id"].map(
        lambda q: schemas[q].gold_label in nc_set(q))
    df["predicted_is_noncommit"] = df.apply(
        lambda r: str(r["predicted"]) in nc_set(r["question_id"]), axis=1)
    df["prediction_commitment_cell"] = np.where(
        ~df["noncommit_is_gold"] & ~df["predicted_is_noncommit"],
        "committed_gold__committed_pred",
        np.where(~df["noncommit_is_gold"] & df["predicted_is_noncommit"],
                 "committed_gold__noncommit_pred",
                 np.where(df["noncommit_is_gold"] & ~df["predicted_is_noncommit"],
                          "noncommit_gold__committed_pred",
                          "noncommit_gold__noncommit_pred")))
    df["strict_correct"] = df["predicted"].astype(str) == df["gold_label"].astype(str)
    df["strict_error"] = ~df["strict_correct"]

    # lenient = strict OR the committed prediction is named in the gold evidence
    # (same rule as analyze_ea_full.py: runner-up credit for screenings)
    def lenient(r):
        if r["strict_correct"]:
            return True
        s = schemas[r["question_id"]]
        txt = (s.gold_label_evidence + " " + s.canonical_claim).lower()
        p = str(r["predicted"]).lower()
        return len(p) >= 2 and not r["predicted_is_noncommit"] and p in txt

    df["lenient_correct"] = df.apply(lenient, axis=1)
    df["error_type"] = np.where(
        df["strict_correct"], "correct",
        np.where(df["prediction_commitment_cell"] == "committed_gold__noncommit_pred",
                 "hedge_collision",
                 np.where(df["prediction_commitment_cell"] == "noncommit_gold__committed_pred",
                          "overcommitment",
                          np.where(df["prediction_commitment_cell"] == "committed_gold__committed_pred",
                                   "wrong_direction_commitment",
                                   "wrong_noncommit_type"))))
    df["ticker1"] = df["tickers"].fillna("").map(
        lambda s: str(s).split("|")[0] or "NONE")
    return df


def auroc(y: np.ndarray, s: np.ndarray) -> tuple[float, int]:
    """AUROC of score s for binary outcome y (1 = error). Returns (auc, n)."""
    ok = np.isfinite(s)
    y, s = np.asarray(y)[ok], np.asarray(s)[ok]
    n1, n0 = int(y.sum()), int(len(y) - y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan"), len(y)
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)), len(y)


df = load(PRIMARY)
L = ["# Committed vs non-committed error decomposition\n",
     "Reanalysis of stored final-round rows; no new model calls.",
     f"Primary set: gemma4 + qwen3, 139 headline-eligible questions each "
     f"(n={len(df)} scored rows). Supplementary gemini section at the end.\n",
     "`noncommit_set` per question = {mixed, conditional, insufficient_data, "
     "none_clear} ∩ answer_space (schema-overridable).\n"]

# ── framing counts ──────────────────────────────────────────────────────
ncg = df.groupby("model")["noncommit_is_gold"].mean()
L.append("## 0. How often is the GOLD itself non-committal?\n")
L.append("```\n" + df.groupby(["model", "lane"])["noncommit_is_gold"]
        .agg(["mean", "sum", "count"]).round(3).to_string() + "\n```")
L.append(f"\nOverall share of questions with a non-committal gold: "
         f"{df['noncommit_is_gold'].mean():.3f} "
         f"({int(df['noncommit_is_gold'].sum()/df['model'].nunique())} of 139).")

# ── A. error rate by commitment cell ────────────────────────────────────
L.append("\n## A. Error rate by commitment cell\n")
a = df.groupby(["model", "prediction_commitment_cell"]).agg(
    n=("strict_error", "size"), strict_error=("strict_error", "mean"),
    lenient_error=("lenient_correct", lambda s: 1 - s.mean()))
L.append("```\n" + a.round(3).to_string() + "\n```")
L.append("\nNote: two cells are **deterministic** — a non-committal prediction "
         "can never match a committed gold (error=1 by construction), and a "
         "committed prediction can never match a non-committal gold (error=1). "
         "Only the two same-type cells admit both outcomes.")
L.append("\n### By lane\n```\n" + df.groupby(
    ["lane", "prediction_commitment_cell"])["strict_error"]
    .agg(["mean", "size"]).round(3).to_string() + "\n```")
L.append("\n### By answer_type\n```\n" + df.groupby(
    ["answer_type", "prediction_commitment_cell"])["strict_error"]
    .agg(["mean", "size"]).round(3).to_string() + "\n```")

# ── B. mean p_noncommit by cell ─────────────────────────────────────────
L.append("\n## B. Mean p_noncommit by commitment cell\n")
b = df.groupby(["model", "prediction_commitment_cell"])["p_noncommit"].agg(
    ["mean", "median", "size"])
L.append("```\n" + b.round(3).to_string() + "\n```")
L.append("\n### By lane\n```\n" + df.groupby(
    ["lane", "prediction_commitment_cell"])["p_noncommit"]
    .agg(["mean", "size"]).round(3).to_string() + "\n```")

# ── C. share of total errors ────────────────────────────────────────────
L.append("\n## C. Share of total errors by type\n")
err = df[df["strict_error"]]
c = (err.groupby(["model", "error_type"]).size()
     / err.groupby("model").size()).rename("share_of_errors")
cn = err.groupby(["model", "error_type"]).size().rename("n")
L.append("```\n" + pd.concat([cn, c.round(3)], axis=1).to_string() + "\n```")
L.append("\n### Pooled (both models)\n```\n"
         + pd.concat([err["error_type"].value_counts().rename("n"),
                      err["error_type"].value_counts(normalize=True)
                      .round(3).rename("share")], axis=1).to_string() + "\n```")
L.append("\n### By lane (share of that lane's errors)\n```\n"
         + (err.groupby(["lane", "error_type"]).size()
            / err.groupby("lane").size()).round(3).to_string() + "\n```")

# ── D. AUROC of p_noncommit ─────────────────────────────────────────────
L.append("\n## D. AUROC of p_noncommit for strict_error\n")
L.append("| subset | model | AUROC | n | error rate |")
L.append("|---|---|---|---|---|")


def add_auroc(label: str, sub: pd.DataFrame):
    for model, g in sub.groupby("model"):
        if len(g) < 8:
            L.append(f"| {label} | {model} | (n too small) | {len(g)} | - |")
            continue
        au, n = auroc(g["strict_error"].astype(int).values,
                      g["p_noncommit"].values)
        L.append(f"| {label} | {model} | {au:.3f} | {n} | "
                 f"{g['strict_error'].mean():.2f} |")


add_auroc("all questions", df)
add_auroc("committed-gold only", df[~df["noncommit_is_gold"]])
add_auroc("noncommitted-gold only", df[df["noncommit_is_gold"]])
for lane in ["F", "FT", "T"]:
    add_auroc(f"lane {lane}", df[df["lane"] == lane])
L.append("\n**Non-mechanical subset** (committed gold AND committed "
         "prediction — the cell where p_noncommit is not definitionally "
         "tied to the outcome):")
L.append("\n| subset | model | AUROC | n | error rate |")
L.append("|---|---|---|---|---|")
add_auroc("committed gold & committed pred", df[
    df["prediction_commitment_cell"] == "committed_gold__committed_pred"])
add_auroc("noncommit gold & noncommit pred", df[
    df["prediction_commitment_cell"] == "noncommit_gold__noncommit_pred"])

# ── E. logistic regressions ─────────────────────────────────────────────
L.append("\n## E. Logistic regressions (cluster-robust SEs by primary ticker)\n")
import statsmodels.formula.api as smf

d = df.copy()
d["y"] = d["strict_error"].astype(int)
d["ncg"] = d["noncommit_is_gold"].astype(int)
specs = [
    ("M1  y ~ p_noncommit + TU + lane",
     "y ~ p_noncommit + tu_norm + C(lane, Treatment('F')) + C(model)"),
    ("M2  + noncommit_is_gold",
     "y ~ p_noncommit + tu_norm + C(lane, Treatment('F')) + C(model) + ncg"),
    ("M3  p_noncommit * noncommit_is_gold",
     "y ~ p_noncommit * ncg + tu_norm + C(lane, Treatment('F')) + C(model)"),
]
for title, formula in specs:
    L.append(f"\n### {title}\n```")
    try:
        fit = smf.logit(formula, data=d).fit(disp=0, cov_type="cluster",
                                             cov_kwds={"groups": d["ticker1"]})
        tab = fit.summary2().tables[1]
        for name, row in tab.iterrows():
            L.append(f"{str(name):40s} coef={row['Coef.']:+8.3f}  "
                     f"p={row['P>|z|']:.3g}")
        L.append(f"pseudo-R2 = {fit.prsquared:.3f}; n = {int(fit.nobs)}")
    except Exception as exc:
        L.append(f"FAILED: {exc}")
    L.append("```")

# marginal reading of the interaction
try:
    fit3 = smf.logit(specs[2][1], data=d).fit(disp=0, cov_type="cluster",
                                              cov_kwds={"groups": d["ticker1"]})
    b_nc = fit3.params.get("p_noncommit", np.nan)
    b_int = fit3.params.get("p_noncommit:ncg", np.nan)
    L.append(f"\nSlope of p_noncommit on committed-gold questions: "
             f"**{b_nc:+.3f}**; on non-committal-gold questions: "
             f"**{b_nc + b_int:+.3f}** (sum of main + interaction).")
except Exception:
    pass

# ── supplementary: gemini ───────────────────────────────────────────────
try:
    gdf = load(SUPP)
    L.append("\n## Supplementary — gemini-3.1-pro (16-question subset, "
             "NOT pooled with primary)\n")
    L.append("```\n" + gdf.groupby("prediction_commitment_cell").agg(
        n=("strict_error", "size"), strict_error=("strict_error", "mean"),
        p_noncommit=("p_noncommit", "mean")).round(3).to_string() + "\n```")
    ge = gdf[gdf["strict_error"]]
    L.append("\nError composition: " + str(dict(ge["error_type"].value_counts())))
    au, n = auroc(gdf["strict_error"].astype(int).values, gdf["p_noncommit"].values)
    L.append(f"AUROC(p_noncommit -> error), all 16: {au:.3f}")
except Exception as exc:
    L.append(f"\n(supplementary gemini section unavailable: {exc})")

df.to_csv(REPO / "analysis" / "noncommit_decomposition_rows.csv", index=False)
OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
