"""Figure 2 — what the non-commitment monitor actually separates.

The logistic interaction (slope +5.12 on settled references, -8.90 on
unsettled) is real but is LARGELY MECHANICAL: whenever the answer type
mismatches the reference type the outcome is an error by construction. A
smooth interaction curve would present a definitional step as a discovered
graded relationship. This figure instead plots the empirical error rate by
p_nc stratum for both reference types and *marks which points are
mechanically determined*, so the reader can see that:

  * the dramatic sign flip lives entirely in the mechanical region, and
  * in the non-mechanical region the error rate is essentially FLAT
    (0.30-0.42), i.e. p_nc carries little graded signal once the system
    has chosen an answer type that could match.

Filled marker = empirical (answer type matches reference type; outcome not
forced). Hollow marker with x = mechanically determined.

Output: fig2_interaction.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.stats.proportion import proportion_confint

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from src.schema import load_schemas  # noqa: E402

HERE = Path(__file__).resolve().parent
sch = load_schemas()
C_SET, C_UNS = "#0072B2", "#D55E00"   # Okabe-Ito, CVD- and greyscale-safe
M_SET, M_UNS = "o", "D"


def ncs(q):
    return sch[q].noncommit_set


RUNS = [("ea_full_gemma4", "gemma4"), ("ea_full_qwen3", "qwen3:8b"),
        ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b"),
        ("ea_full_hf_gemma_4_31B_it", "gemma4-31b-it")]
rs = []
for run, m in RUNS:
    d = pd.read_csv(REPO / "results" / run / "rows.csv")
    d = d[(d["round"] == 1) & d.correct.notna()].copy()
    d["model"] = m
    d["gnc"] = d.question_id.map(lambda q: sch[q].gold_label in ncs(q))
    d["pred_nc"] = d.apply(
        lambda r: str(r.predicted) in ncs(r.question_id), axis=1)
    rs.append(d)
df = pd.concat(rs, ignore_index=True)
df["err"] = (~df.correct.astype(bool)).astype(int)
# outcome is forced whenever answer type != reference type
df["mechanical"] = df.gnc != df.pred_nc

BINS = [-.001, .001, .34, .66, .999, 1.001]
LABS = ["0", "(0,.33]", "(.33,.66]", "(.66,1)", "1"]
df["stratum"] = pd.cut(df.p_noncommit, bins=BINS, labels=LABS)

mpl.rcParams.update({"font.family": "serif", "font.size": 9,
                     "axes.linewidth": 0.6, "pdf.fonttype": 42,
                     "ps.fonttype": 42})
fig, ax = plt.subplots(figsize=(5.4, 3.0))

x = np.arange(len(LABS))
for gnc, colour, mk, name, dx in [
        (False, C_SET, M_SET, "settled reference answer", -0.06),
        (True, C_UNS, M_UNS, "non-committal reference answer", +0.06)]:
    sub = df[df.gnc == gnc]
    for k, lab in enumerate(LABS):
        cell = sub[sub.stratum == lab]
        if len(cell) == 0:
            continue
        p = cell.err.mean()
        lo, hi = proportion_confint(int(cell.err.sum()), len(cell),
                                    method="wilson")
        mech = cell.mechanical.mean() > 0.5
        ax.plot([x[k] + dx] * 2, [lo, hi], color=colour, lw=1.3,
                alpha=0.8, zorder=2)
        ax.plot(x[k] + dx, p, mk, ms=7, zorder=3, color=colour,
                markerfacecolor="white" if mech else colour,
                markeredgecolor=colour, markeredgewidth=1.4)
        if mech:  # cross the hollow marker: outcome forced by construction
            ax.plot(x[k] + dx, p, "x", ms=4.5, color=colour, zorder=4,
                    markeredgewidth=1.2)
        ax.text(x[k] + dx, hi + 0.035, f"{len(cell)}", ha="center",
                fontsize=6.5, color="#666666")

ax.set_xticks(x)
ax.set_xticklabels(LABS, fontsize=8.5)
ax.set_xlabel("non-commitment mass $p_{\\mathrm{nc}}$ (stratum)", fontsize=8.5)
ax.set_ylabel("error rate", fontsize=8.5)
ax.set_ylim(-0.08, 1.16)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax.grid(axis="y", color="#DDDDDD", lw=0.5, zorder=0)
ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)

from matplotlib.lines import Line2D  # noqa: E402
ax.legend(handles=[
    Line2D([], [], color=C_SET, marker=M_SET, ls="none", ms=7,
           label="settled reference"),
    Line2D([], [], color=C_UNS, marker=M_UNS, ls="none", ms=7,
           label="non-committal reference"),
    Line2D([], [], color="#666666", marker="o", ls="none", ms=7,
           markerfacecolor="white", markeredgecolor="#666666",
           label="outcome forced by construction")],
    loc="upper center", bbox_to_anchor=(0.5, 1.19), ncol=3, frameon=False,
    fontsize=7.2, handletextpad=0.4, columnspacing=1.2)

fig.tight_layout(pad=0.4)
fig.savefig(HERE / "fig2_interaction.pdf", bbox_inches="tight")
fig.savefig(HERE / "fig2_interaction.png", dpi=200, bbox_inches="tight")

t = df.groupby(["gnc", "stratum"], observed=True).agg(
    n=("err", "size"), err=("err", "mean"), mech=("mechanical", "mean"))
print(t.round(3).to_string())
print("\nwrote fig2_interaction.pdf")
