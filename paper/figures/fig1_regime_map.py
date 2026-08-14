"""Figure 1 — the regime map: non-commitment mass by query lane x system.

Form: small matrix (5 systems x 3 lanes) of a single magnitude
(p_noncommit in [0,1]) -> sequential heatmap, ONE hue light->dark, with
every cell direct-labelled (15 cells is small enough to read as a table
with colour). A single-hue sequential ramp is monotone in lightness, so the
figure survives greyscale printing and colour-vision deficiency without
needing a second channel.

Headline the figure must carry: FT (cross-signal) is the highest-hedging
lane in EVERY system, including ones that commit confidently elsewhere.

Output: fig1_regime_map.pdf
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
from src.schema import load_schemas  # noqa: E402

HERE = Path(__file__).resolve().parent
sch = load_schemas()

RUNS = [("ea_full_gemma4", "gemma4"),
        ("ea_full_qwen3", "qwen3:8b"),
        ("ea_full_hf_qwen36_27b_fp8", "qwen3.6-27b"),
        ("ea_full_hf_gemma_4_31B_it", "gemma4-31b-it"),
        ("gemini_subset16", "gemini-3.1-pro*")]
LANES = ["F", "FT", "T"]
LANE_LABEL = {"F": "F\nfund.", "FT": "FT\nhybrid", "T": "T\nscreen"}

rows, counts = {}, {}
for run, m in RUNS:
    d = pd.read_csv(REPO / "results" / run / "rows.csv")
    d = d[(d["round"] == 1) & d.correct.notna()]
    rows[m] = [d[d.lane == ln]["p_noncommit"].mean() for ln in LANES]
    counts[m] = [int((d.lane == ln).sum()) for ln in LANES]

M = np.array([rows[m] for _, m in RUNS])
N = np.array([counts[m] for _, m in RUNS])
models = [m for _, m in RUNS]

mpl.rcParams.update({"font.family": "serif", "font.size": 9,
                     "pdf.fonttype": 42, "ps.fonttype": 42})
fig, ax = plt.subplots(figsize=(3.9, 3.4))

im = ax.imshow(M, cmap="Blues", vmin=0.0, vmax=1.0, aspect="auto")

for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        v = M[i, j]
        # ink colour follows contrast against the cell, not the series
        ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=9,
                color="white" if v > 0.55 else "#1a1a1a")

ax.set_xticks(range(len(LANES)))
ax.set_xticklabels([LANE_LABEL[l] for l in LANES], fontsize=8.5)
ax.set_yticks(range(len(models)))
ax.set_yticklabels(models, fontsize=8.5)
ax.tick_params(length=0)
for sp in ax.spines.values():
    sp.set_visible(False)

# box the FT column — the claim the figure exists to make
ax.add_patch(plt.Rectangle((0.5, -0.5), 1, len(models), fill=False,
                           edgecolor="#D55E00", lw=1.6, zorder=5))

cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cb.set_label("non-commitment mass $p_{\\mathrm{nc}}$", fontsize=8)
cb.ax.tick_params(labelsize=7.5)
cb.outline.set_visible(False)

ax.set_title("FT is the highest-hedging lane in every system",
             fontsize=9, pad=8)
fig.text(0.02, -0.02,
         f"*gemini row from a 16-question subset "
         f"(n={N[-1,0]}/{N[-1,1]}/{N[-1,2]} per lane); all others n=49/50/40.",
         fontsize=6.8, color="#555555")

fig.tight_layout(pad=0.4)
fig.savefig(HERE / "fig1_regime_map.pdf", bbox_inches="tight")
fig.savefig(HERE / "fig1_regime_map.png", dpi=200, bbox_inches="tight")
print(pd.DataFrame(M, index=models, columns=LANES).round(3).to_string())
print("\nwrote fig1_regime_map.pdf")
