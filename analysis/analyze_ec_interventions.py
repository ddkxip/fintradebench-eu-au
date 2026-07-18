"""E-C' analysis: paired do-effects vs the oracle Round-0 baseline.

Control = ea_full_gemma4 round 0 (same questions, same K=10, oracle
evidence). For each arm, paired within-question deltas on p_noncommit, AU,
EU, gold_prob; paired Wilcoxon + bootstrap CIs; the construct-validity
diagonal/off-diagonal contrast (remove_top vs remove_placebo).

Writes analysis/source_intervention_pilot.md.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

RES = REPO / "results"
OUT = REPO / "analysis" / "source_intervention_pilot.md"

ec = pd.read_csv(RES / "ec_interventions_gemma4" / "rows.csv")
ec = ec[ec["round"] == 0].copy()
ec = ec[ec["arm"].apply(lambda x: isinstance(x, str))].copy()  # drop parse-fail rows
base = pd.read_csv(RES / "ea_full_gemma4" / "rows.csv")
base = base[base["round"] == 0].set_index("question_id")

METRICS = ["p_noncommit", "au_mm", "eu_mm", "gold_prob", "au_norm", "eu_norm"]
qids = ec["question_id"].unique()


def paired(arm_df: pd.DataFrame, metric: str):
    """Return (mean delta, wilcoxon p, ci_lo, ci_hi, n) vs baseline."""
    d = []
    for _, r in arm_df.iterrows():
        q = r["question_id"]
        if q in base.index and pd.notna(r[metric]) and pd.notna(base.loc[q, metric]):
            d.append(float(r[metric]) - float(base.loc[q, metric]))
    d = np.array(d)
    if len(d) < 3:
        return np.nan, np.nan, np.nan, np.nan, len(d)
    rng = np.random.default_rng(0)
    boot = [rng.choice(d, len(d)).mean() for _ in range(5000)]
    lo, hi = np.percentile(boot, [2.5, 97.5])
    nz = d[d != 0]
    p = stats.wilcoxon(nz).pvalue if len(nz) >= 5 else np.nan
    return d.mean(), p, lo, hi, len(d)


L = ["# E-C' source-intervention results (gemma4, R0, F+FT, K=10)\n",
     "Control = ea_full_gemma4 round-0 oracle baseline; paired within-question.\n",
     f"- questions run: {len(qids)}; arms: {sorted(ec['arm'].unique())}"]

L.append("\n## Paired do-effects vs oracle baseline (mean delta [95% CI], Wilcoxon p)\n")
L.append("| arm | metric | delta | 95% CI | p | n |")
L.append("|---|---|---|---|---|---|")
summary = {}
for arm in ["remove_top", "remove_placebo", "inject_conflict",
            "horizon_short", "horizon_long"]:
    a = ec[ec["arm"] == arm]
    if a.empty:
        continue
    for m in ["p_noncommit", "au_mm", "eu_mm", "gold_prob"]:
        dm, p, lo, hi, n = paired(a, m)
        summary[(arm, m)] = (dm, lo, hi, p)
        star = "" if not np.isfinite(p) else (" **" if p < 0.05 else "")
        L.append(f"| {arm} | {m} | {dm:+.4f}{star} | [{lo:+.4f}, {hi:+.4f}] | "
                 f"{p:.3g} | {n} |")

# ── construct-validity: remove_top vs remove_placebo (diagonal/off-diag) ──
L.append("\n## Construct validity: evidence-removal selectivity\n")
L.append("Diagonal (remove_top) should move uncertainty; off-diagonal "
         "(remove_placebo, matched non-golden removal) should NOT. A large "
         "top-minus-placebo gap = the uncertainty responds to *relevant* "
         "evidence loss, not to any evidence loss.\n")
for m in ["p_noncommit", "au_mm", "gold_prob"]:
    top = summary.get(("remove_top", m))
    pla = summary.get(("remove_placebo", m))
    if top and pla:
        # paired top-vs-placebo per question
        d = []
        rt = ec[ec.arm == "remove_top"].set_index("question_id")
        rp = ec[ec.arm == "remove_placebo"].set_index("question_id")
        for q in rt.index.intersection(rp.index):
            if pd.notna(rt.loc[q, m]) and pd.notna(rp.loc[q, m]):
                d.append(float(rt.loc[q, m]) - float(rp.loc[q, m]))
        d = np.array(d)
        p = stats.wilcoxon(d[d != 0]).pvalue if (d != 0).sum() >= 5 else np.nan
        L.append(f"- **{m}**: remove_top {top[0]:+.4f} vs placebo {pla[0]:+.4f}; "
                 f"top-minus-placebo {d.mean():+.4f} (paired p={p:.3g}, n={len(d)})")

# ── horizon sensitivity: short vs long ──────────────────────────────────
L.append("\n## Horizon sensitivity (short vs long, same evidence)\n")
hs = ec[ec.arm == "horizon_short"].set_index("question_id")
hl = ec[ec.arm == "horizon_long"].set_index("question_id")
common = hs.index.intersection(hl.index)
for m in ["gold_prob", "p_noncommit", "predicted"]:
    if m == "predicted":
        flips = sum(hs.loc[q, "predicted"] != hl.loc[q, "predicted"]
                    for q in common)
        L.append(f"- verdict flips short vs long: {flips}/{len(common)}")
    else:
        d = np.array([float(hl.loc[q, m]) - float(hs.loc[q, m])
                      for q in common if pd.notna(hs.loc[q, m])])
        p = stats.wilcoxon(d[d != 0]).pvalue if (d != 0).sum() >= 5 else np.nan
        L.append(f"- {m} long-minus-short: {d.mean():+.4f} (p={p:.3g}, n={len(d)})")
L.append("\n(Flat horizon response = horizon-insensitivity finding: the "
         "system's verdict does not condition on the stated horizon.)")

# ── by-lane conflict effect (FT is the hedge hot-spot) ──────────────────
L.append("\n## inject_conflict by lane (does explicit F/T conflict break the hedge?)\n")
ic = ec[ec.arm == "inject_conflict"]
for lane in ["F", "FT"]:
    a = ic[ic.lane == lane]
    if a.empty:
        continue
    for m in ["eu_mm", "p_noncommit"]:
        dm, p, lo, hi, n = paired(a, m)
        L.append(f"- {lane} {m}: {dm:+.4f} [{lo:+.4f},{hi:+.4f}] p={p:.3g} (n={n})")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
