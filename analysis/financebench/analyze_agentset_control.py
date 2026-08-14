"""Compare FinanceBench agent-set arms: skeptic (original) vs neutral vs
homogeneous. Reanalysis only — no model calls.

The question: was the original run's accuracy collapse (1 rescue / 10 losses,
dCorrect -0.243) caused by the *insufficiency-biased skeptic*, or by debate
itself? The neutral arm removes the skeptic bias while keeping perspective
diversity; the homogeneous arm removes diversity too.

Writes analysis/financebench/FINANCEBENCH_AGENTSET_CONTROL.md
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RES = REPO / "results"
OUT = HERE / "FINANCEBENCH_AGENTSET_CONTROL.md"

ARMS = [("financebench_yesno_oracle_local_qwen3_8b", "skeptic (original)"),
        ("financebench_yesno_neutral_local_qwen3_8b", "neutral (control 1)"),
        ("financebench_yesno_homog_local_qwen3_8b", "homogeneous (control 2)")]
NC = {"insufficient_data"}


def load(run):
    p = RES / run / "rows.csv"
    if not p.exists():
        return None
    d = pd.read_csv(p)
    d["pred_nc"] = d["predicted"].astype(str).isin(NC)
    d["gold_nc"] = d["gold_label"].astype(str).isin(NC)
    return d


def auroc(y, s):
    y, s = np.asarray(y), np.asarray(s)
    n1, n0 = int(y.sum()), len(y) - int(y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def boot_auroc_ci(sub, n_boot=5000, seed=0):
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        s = sub.iloc[rng.integers(0, len(sub), len(sub))]
        y = (~s.correct.astype(bool)).astype(int).values
        if y.sum() in (0, len(y)):
            continue
        vals.append(auroc(y, s.p_noncommit.values))
    if not vals:
        return (np.nan, np.nan)
    return tuple(np.percentile(vals, [2.5, 97.5]))


L = ["# FinanceBench agent-set control — did the skeptic cause the collapse?\n",
     "Reanalysis only. All arms: qwen3:8b, oracle `evidence_text`, K=10, "
     "1 debate round, same 37 yes/no schemas — **only the agent pair differs**.\n",
     "| arm | agents |", "|---|---|",
     "| skeptic (original) | evidence_accountant + skeptical_auditor (insufficiency-hunting) |",
     "| neutral (control 1) | evidence_accountant + financial_analyst (both substantive) |",
     "| homogeneous (control 2) | two identical evidence_accountants |", ""]

summary, missing = [], []
for run, label in ARMS:
    d = load(run)
    if d is None:
        missing.append(label)
        continue
    s = d[d.agent == "system"]
    r0, r1 = s[s["round"] == 0], s[s["round"] == 1]
    j = r0.set_index("financebench_id").join(
        r1.set_index("financebench_id"), lsuffix="_0", rsuffix="_1")
    dcorr = j["correct_1"].astype(int) - j["correct_0"].astype(int)
    nz = dcorr[dcorr != 0]
    p_dc = stats.wilcoxon(nz).pvalue if len(nz) >= 5 else float("nan")
    dnc = j["p_noncommit_1"] - j["p_noncommit_0"]
    nzn = dnc[dnc != 0]
    p_nc = stats.wilcoxon(nzn).pvalue if len(nzn) >= 5 else float("nan")
    err1 = r1[~r1.correct.astype(bool)]
    hc = int(((~err1.gold_nc) & err1.pred_nc).sum())
    wd = int(((~err1.gold_nc) & (~err1.pred_nc)).sum())
    cc = r1[(~r1.gold_nc) & (~r1.pred_nc)]
    cc_auc = auroc((~cc.correct.astype(bool)).astype(int).values,
                   cc.p_noncommit.values) if len(cc) >= 8 else np.nan
    lo, hi = boot_auroc_ci(cc) if len(cc) >= 8 else (np.nan, np.nan)
    summary.append({
        "arm": label, "n": len(r1),
        "R0_acc": round(r0.correct.mean(), 3), "R1_acc": round(r1.correct.mean(), 3),
        "dCorrect": round(float(dcorr.mean()), 3), "p_dCorrect": round(p_dc, 4),
        "R0_pNC": round(r0.p_noncommit.mean(), 3),
        "R1_pNC": round(r1.p_noncommit.mean(), 3),
        "dNC": round(float(dnc.mean()), 3), "p_dNC": round(p_nc, 4),
        "rescues": int(((j.correct_0 == False) & (j.correct_1 == True)).sum()),
        "losses": int(((j.correct_0 == True) & (j.correct_1 == False)).sum()),
        "errors": len(err1), "hedge_coll": hc,
        "hedge_share": round(hc / len(err1), 3) if len(err1) else np.nan,
        "wrong_dir": wd,
        "commit_cell_n": len(cc), "commit_cell_AUROC": round(cc_auc, 3),
        "cc_CI_lo": round(lo, 3), "cc_CI_hi": round(hi, 3),
    })

if missing:
    L.append(f"> **Pending arms (not yet run): {', '.join(missing)}.** "
             "Rerun this script once their rows.csv exist.\n")

if summary:
    sm = pd.DataFrame(summary)
    L.append("## 1. Headline comparison\n")
    L.append("```\n" + sm[["arm", "n", "R0_acc", "R1_acc", "dCorrect",
                           "p_dCorrect", "rescues", "losses"]].to_string(index=False) + "\n```")
    L.append("\n## 2. Non-commitment dynamics\n")
    L.append("```\n" + sm[["arm", "R0_pNC", "R1_pNC", "dNC", "p_dNC"]].to_string(index=False) + "\n```")
    L.append("\n## 3. Error composition and the committed cell\n")
    L.append("```\n" + sm[["arm", "errors", "hedge_coll", "hedge_share", "wrong_dir",
                           "commit_cell_n", "commit_cell_AUROC", "cc_CI_lo",
                           "cc_CI_hi"]].to_string(index=False) + "\n```")

    # per-agent drift (the mechanism)
    L.append("\n## 4. Per-agent drift — who moves whom\n")
    for run, label in ARMS:
        d = load(run)
        if d is None:
            continue
        g = (d[d.agent != "system"].groupby(["agent", "round"])
             .agg(acc=("correct", "mean"), pNC=("p_noncommit", "mean"),
                  hedge_rate=("pred_nc", "mean")).round(3))
        L.append(f"\n**{label}**\n```\n{g.to_string()}\n```")

    # verdict
    base = sm[sm.arm.str.startswith("skeptic")]
    ctrl = sm[~sm.arm.str.startswith("skeptic")]
    if len(base) and len(ctrl):
        b = base.iloc[0]
        L.append("\n## 5. Verdict\n")
        for _, c in ctrl.iterrows():
            verdict = ("**skeptic-driven**" if c.dCorrect > b.dCorrect + 0.10
                       else "**debate-driven (persists without the skeptic)**"
                       if c.dCorrect <= b.dCorrect + 0.05 else "partial")
            L.append(f"- {c.arm}: dCorrect {c.dCorrect:+.3f} vs skeptic "
                     f"{b.dCorrect:+.3f}; rescues/losses {c.rescues}/{c.losses} "
                     f"vs {b.rescues}/{b.losses} -> {verdict}")
        L.append("\nInterpretation rule fixed in advance: if the neutral arm's "
                 "accuracy drop largely disappears, the original collapse was an "
                 "artifact of the insufficiency-biased skeptic and must not be "
                 "reported as a general debate effect. If it persists, debate "
                 "itself degrades accuracy on this benchmark.")

OUT.write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
