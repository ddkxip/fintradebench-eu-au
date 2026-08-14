"""Figure 3 — committed-cell AUROC across models, lanes, and benchmarks.

ORIGINAL PLAN (abandoned, see below): scatter of committed-cell AUROC vs
residual hedge-mass variance, to show that p_noncommit regains
wrong-direction signal when hedge mass has variance.

WHY IT WAS ABANDONED: the mechanism is refuted by our own data. Within
FinTradeBench, Spearman(sd, AUROC) = -0.029 (p=0.92, n=14); across all 15
points 0.164 (p=0.56). Direct counterexamples exist (qwen3:8b FT-lane: sd
0.220, AUROC 0.222). sd and mean correlate at 0.96, so "variance not mean"
is not even a separable claim. A scatter through the 5 aggregate points
(rho=0.50, p=0.39) would be a trend line fitted to noise and contradicted by
the within-benchmark points.

WHAT THIS PLOTS INSTEAD: a forest plot of the estimates themselves, with
bootstrap CIs — the honest statement of what we know. Every FinTradeBench
estimate straddles chance; the FinanceBench estimate sits above it; the
cause is not identified.

Output: fig3_committed_cell.pdf (vector, for LaTeX).
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from src.schema import load_schemas  # noqa: E402

HERE = Path(__file__).resolve().parent
sch = load_schemas()

# Okabe-Ito: colourblind-safe and distinguishable in greyscale print.
# Identity is carried by marker SHAPE as well as hue, so the figure never
# relies on colour alone (survives B&W printing and CVD).
C_FTB, C_FB = "#0072B2", "#D55E00"
M_FTB, M_FB = "o", "D"


def ncs(q):
    return sch[q].noncommit_set


def auroc(y, s):
    y, s = np.asarray(y), np.asarray(s)
    n1, n0 = int(y.sum()), len(y) - int(y.sum())
    if n1 == 0 or n0 == 0:
        return np.nan
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot(y, s, n_boot=5000, seed=0):
    rng = np.random.default_rng(seed)
    y, s = np.asarray(y), np.asarray(s)
    out = []
    for _ in range(n_boot):
        i = rng.integers(0, len(y), len(y))
        yy, ss = y[i], s[i]
        if yy.sum() in (0, len(yy)):
            continue
        out.append(auroc(yy, ss))
    return (np.nan, np.nan) if not out else tuple(np.percentile(out, [2.5, 97.5]))


rows = []
FULL = [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3:8b"),
        ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b"),
        ("ea_full_hf_gemma_4_31B_it", "gemma4-31b-it")]
for run, m in FULL:
    d = pd.read_csv(REPO / "results" / run / "rows.csv")
    d = d[(d["round"] == 1) & d.correct.notna()].copy()
    d["gnc"] = d.question_id.map(lambda q: sch[q].gold_label in ncs(q))
    d["pnc"] = d.apply(lambda r: str(r.predicted) in ncs(r.question_id), axis=1)
    cc = d[(~d.gnc) & (~d.pnc)]
    y = (~cc.correct.astype(bool)).astype(int).values
    lo, hi = boot(y, cc.p_noncommit.values)
    rows.append(dict(bench="FinTradeBench", label=m, n=len(cc),
                     auc=auroc(y, cc.p_noncommit.values), lo=lo, hi=hi))

NC = {"insufficient_data"}
FB = [("financebench_yesno_oracle_local_qwen3_8b", "qwen3:8b (skeptic pair)"),
      ("financebench_yesno_neutral_local_qwen3_8b", "qwen3:8b (neutral pair)")]
for run, lab in FB:
    p = REPO / "results" / run / "rows.csv"
    if not p.exists():
        continue
    d = pd.read_csv(p)
    s = d[(d.agent == "system") & (d["round"] == 1)].copy()
    cc = s[(~s.gold_label.astype(str).isin(NC))
           & (~s.predicted.astype(str).isin(NC))]
    y = (~cc.correct.astype(bool)).astype(int).values
    lo, hi = boot(y, cc.p_noncommit.values)
    rows.append(dict(bench="FinanceBench", label=lab, n=len(cc),
                     auc=auroc(y, cc.p_noncommit.values), lo=lo, hi=hi))

df = pd.DataFrame(rows).iloc[::-1].reset_index(drop=True)  # FB on top

mpl.rcParams.update({
    "font.family": "serif", "font.size": 9, "axes.linewidth": 0.6,
    "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})
fig, ax = plt.subplots(figsize=(5.4, 2.9))

# chance reference — the only thing the reader must compare against
ax.axvline(0.5, color="#444444", lw=0.9, ls="--", zorder=1)
ax.text(0.5, -0.5, " chance", fontsize=7.5, color="#444444",
        va="bottom", ha="left")

for i, r in df.iterrows():
    is_fb = r.bench == "FinanceBench"
    c, mk = (C_FB, M_FB) if is_fb else (C_FTB, M_FTB)
    ax.plot([r.lo, r.hi], [i, i], color=c, lw=1.6, solid_capstyle="round",
            zorder=2, alpha=0.85)
    ax.plot(r.auc, i, mk, color=c, ms=6.5, zorder=3,
            markeredgecolor="white", markeredgewidth=0.8)
    ax.text(1.005, i, f"$n$={r.n}", fontsize=7.5, va="center",
            color="#555555", transform=ax.get_yaxis_transform(
                which="grid") if False else ax.transData)

ax.set_yticks(range(len(df)))
ax.set_yticklabels([f"{r.label}" for _, r in df.iterrows()], fontsize=8.5)
ax.set_xlabel("AUROC of $p_{\\mathrm{nc}}$ for error\n"
              "(committed-gold $\\wedge$ committed-prediction cell)",
              fontsize=8.5)
ax.set_xlim(0.0, 1.12)
ax.set_ylim(-0.6, len(df) + 0.35)  # blank band at top for the legend
ax.set_xticks([0.0, 0.25, 0.5, 0.75, 1.0])

# legend carries benchmark identity (shape + hue, never hue alone)
from matplotlib.lines import Line2D  # noqa: E402
ax.legend(handles=[
    Line2D([], [], color=C_FTB, marker=M_FTB, ls="-", lw=1.6, ms=6.5,
           markeredgecolor="white", markeredgewidth=0.8,
           label="FinTradeBench (139 q)"),
    Line2D([], [], color=C_FB, marker=M_FB, ls="-", lw=1.6, ms=6.5,
           markeredgecolor="white", markeredgewidth=0.8,
           label="FinanceBench (37 q)")],
    loc="upper left", frameon=False, fontsize=7.5,
    handletextpad=0.5, borderaxespad=0.3)

for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.grid(axis="x", color="#DDDDDD", lw=0.5, zorder=0)
ax.set_axisbelow(True)

fig.tight_layout(pad=0.4)
out = HERE / "fig3_committed_cell.pdf"
fig.savefig(out, bbox_inches="tight")
fig.savefig(HERE / "fig3_committed_cell.png", dpi=200, bbox_inches="tight")
print(df.round(3).to_string(index=False))
print(f"\nwrote {out}")
