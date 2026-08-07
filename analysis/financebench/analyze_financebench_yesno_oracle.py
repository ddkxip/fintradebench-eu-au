"""Analyze a FinanceBench yes/no oracle run and compare to FinTradeBench.

Reanalysis only (no model calls). Reads results/<run_id>/rows.csv produced
by run_financebench_yesno_oracle.py and writes
analysis/financebench/FINANCEBENCH_YESNO_ORACLE_FINDINGS.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
RES = REPO / "results"
OUT = HERE / "FINANCEBENCH_YESNO_ORACLE_FINDINGS.md"
SCHEMAS = HERE / "financebench_yesno_schemas.jsonl"
NONCOMMIT = {"insufficient_data"}
COMMITTED = {"yes", "no"}
OPPOSITE = {"yes": "no", "no": "yes"}

# FinTradeBench reference values (139q, final round) for qualitative contrast
FTB = {"hedge_coll_share": {"gemma4": 0.670, "qwen3:8b": 0.554,
                            "qwen3.6-27b": 0.532, "gemma4-31b-it": 0.506},
       "auroc_all": {"gemma4": 0.694, "qwen3:8b": 0.636,
                     "qwen3.6-27b": 0.704, "gemma4-31b-it": 0.721},
       "auroc_commitcell": {"gemma4": 0.446, "qwen3:8b": 0.403,
                            "qwen3.6-27b": 0.408, "gemma4-31b-it": 0.437},
       "noncommit_gold_share": 22 / 139}


def auroc(y, s):
    ok = np.isfinite(s)
    y, s = np.asarray(y)[ok], np.asarray(s)[ok]
    n1, n0 = int(y.sum()), len(y) - int(y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = stats.rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-id", default="financebench_yesno_oracle_qwen36")
    a = ap.parse_args()

    p = RES / a.run_id / "rows.csv"
    if not p.exists():
        raise SystemExit(f"[error] {p} not found — run the experiment first "
                         "(this script does not call any model).")
    df = pd.read_csv(p)
    sysrows = df[df["agent"] == "system"].copy()
    r0 = sysrows[sysrows["round"] == 0].set_index("financebench_id")
    r1 = sysrows[sysrows["round"] == 1].set_index("financebench_id")
    idx = r0.index.intersection(r1.index)
    fin = r1 if len(r1) else r0

    schs = {json.loads(l)["financebench_id"]: json.loads(l)
            for l in SCHEMAS.read_text(encoding="utf-8").splitlines() if l.strip()}

    L = ["# FinanceBench yes/no oracle-evidence run — findings\n",
         f"Run `{a.run_id}`; model `{fin['model'].iloc[0]}`; "
         f"evidence field `{fin['evidence_field'].iloc[0]}`; "
         f"K={int(fin['K'].iloc[0])}. Oracle evidence only (no RAG, no PDF "
         "retrieval). Reanalysis script makes no model calls.\n",
         "Answer space `[yes, no, insufficient_data]`; "
         "`noncommit_set = {insufficient_data}`.\n"]

    L.append("## 1. Coverage and parsing\n")
    L.append(f"- examples: **{sysrows['financebench_id'].nunique()}** "
             f"(schema subset: {len(schs)})")
    L.append(f"- mean parse rate: **{df['parse_rate'].mean():.3f}** "
             f"(min {df['parse_rate'].min():.3f})")

    L.append("\n## 2. Accuracy and non-commitment by round\n")
    acc = sysrows.groupby("round")["correct"].mean()
    pnc = sysrows.groupby("round")["p_noncommit"].mean()
    for rnd in sorted(sysrows["round"].unique()):
        L.append(f"- R{rnd}: accuracy **{acc[rnd]:.3f}**, "
                 f"mean p_noncommit **{pnc[rnd]:.3f}**")
    gold_counts = pd.Series({k: v["gold_label"] for k, v in schs.items()}).value_counts()
    L.append(f"- gold distribution: {gold_counts.to_dict()} "
             f"(majority-class baseline = {gold_counts.max()/gold_counts.sum():.3f})")

    if len(idx):
        L.append("\n## 3. Debate deltas R0->R1 (paired)\n")
        for col, nm in [("au", "dAU"), ("eu", "dEU"),
                        ("p_noncommit", "dNC"), ("correct", "dCorrect")]:
            x = (r1.loc[idx, col].astype(float) - r0.loc[idx, col].astype(float)).values
            nz = x[x != 0]
            pv = stats.wilcoxon(nz).pvalue if len(nz) >= 10 else float("nan")
            L.append(f"- {nm}: mean {x.mean():+.4f}, Wilcoxon p={pv:.3g} "
                     f"(nonzero n={len(nz)})")
        resc = int(((~r0.loc[idx, "correct"].astype(bool)) & r1.loc[idx, "correct"].astype(bool)).sum())
        loss = int((r0.loc[idx, "correct"].astype(bool) & (~r1.loc[idx, "correct"].astype(bool))).sum())
        L.append(f"- **debate rescues: {resc}; losses: {loss}** "
                 f"(stable-correct {int((r0.loc[idx,'correct'].astype(bool) & r1.loc[idx,'correct'].astype(bool)).sum())}, "
                 f"stable-wrong {int(((~r0.loc[idx,'correct'].astype(bool)) & (~r1.loc[idx,'correct'].astype(bool))).sum())})")

    # error decomposition
    fin = fin.copy()
    fin["gold"] = fin.index.map(lambda q: schs[q]["gold_label"])
    fin["pred"] = fin["predicted"].astype(str)
    hedge = fin[(fin["gold"].isin(COMMITTED)) & (fin["pred"].isin(NONCOMMIT))]
    over = fin[(fin["gold"].isin(NONCOMMIT)) & (fin["pred"].isin(COMMITTED))]
    wrong = fin[(fin["gold"].isin(COMMITTED)) & (fin["pred"].isin(COMMITTED))
                & (fin["pred"] != fin["gold"])]
    errs = fin[~fin["correct"].astype(bool)]
    L.append("\n## 4. Error decomposition (final round)\n")
    L.append(f"- total errors: **{len(errs)}** / {len(fin)} "
             f"(error rate {len(errs)/max(1,len(fin)):.3f})")
    L.append(f"- **hedge_collision** (committed gold, predicted "
             f"insufficient_data): **{len(hedge)}** "
             f"({len(hedge)/max(1,len(errs)):.1%} of errors)")
    L.append(f"- **overcommitment** (insufficient_data gold, committed "
             f"prediction): **{len(over)}** "
             f"({len(over)/max(1,len(errs)):.1%} of errors)")
    L.append(f"- **wrong_direction** (yes<->no flip): **{len(wrong)}** "
             f"({len(wrong)/max(1,len(errs)):.1%} of errors)")
    n_nc_gold = sum(1 for v in schs.values() if v["gold_label"] in NONCOMMIT)
    if n_nc_gold == 0:
        L.append("\n> **Structural caveat:** this subset contains **no "
                 "`insufficient_data` golds**, so `overcommitment` is "
                 "identically 0 by construction and every error is either a "
                 "hedge collision or a wrong-direction flip. The "
                 "hedge-vs-wrong-direction *split* is therefore the only "
                 "informative decomposition here.")

    L.append("\n## 5. AUROC of p_noncommit for error (final round)\n")
    y = (~fin["correct"].astype(bool)).astype(int).values
    cc = fin[(fin["gold"].isin(COMMITTED)) & (fin["pred"].isin(COMMITTED))]
    a_all = auroc(y, fin["p_noncommit"].values)
    a_cc = auroc((~cc["correct"].astype(bool)).astype(int).values,
                 cc["p_noncommit"].values) if len(cc) >= 8 else float("nan")
    L.append(f"- AUROC(p_noncommit -> error), all: **{a_all:.3f}** (n={len(fin)})")
    L.append(f"- AUROC in committed-gold & committed-pred subset "
             f"(non-mechanical cell): **{a_cc:.3f}** (n={len(cc)})")

    L.append("\n## 6. Qualitative comparison to FinTradeBench\n")
    L.append("| quantity | FinanceBench yes/no (this run) | FinTradeBench (139q, 4 models) |")
    L.append("|---|---|---|")
    L.append(f"| non-committal golds | 0/{len(schs)} (0%) | 22/139 (15.8%) |")
    L.append(f"| hedge-collision share of errors | {len(hedge)/max(1,len(errs)):.1%} | "
             f"{min(FTB['hedge_coll_share'].values()):.1%}-{max(FTB['hedge_coll_share'].values()):.1%} |")
    L.append(f"| AUROC p_noncommit (all) | {a_all:.3f} | "
             f"{min(FTB['auroc_all'].values()):.3f}-{max(FTB['auroc_all'].values()):.3f} |")
    L.append(f"| AUROC committed-cell | {a_cc:.3f} | "
             f"{min(FTB['auroc_commitcell'].values()):.3f}-{max(FTB['auroc_commitcell'].values()):.3f} |")
    L.append("\nKey reading: the **committed-cell AUROC** is the "
             "generalization test that matters. In FinTradeBench it sat at "
             "0.40-0.45 (chance) for every model, supporting "
             "'p_noncommit is a hedge-collision detector with no "
             "wrong-direction signal'. If this run reproduces a ~chance "
             "committed-cell AUROC on an independent benchmark, that claim "
             "generalizes; if it is clearly >0.55 here, the claim is "
             "benchmark-specific and must be narrowed.")

    OUT.write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L))
    print(f"\n[wrote {OUT.name}]")


if __name__ == "__main__":
    main()
