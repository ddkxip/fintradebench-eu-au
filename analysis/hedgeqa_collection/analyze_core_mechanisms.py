"""Mechanism analyses behind HEDGEQA_CORE317_MULTIMODEL.md sections 1 and 4.

    python analysis/hedgeqa_collection/analyze_core_mechanisms.py

Three analyses over the seven full-core runs, paired over the items every run
scored (315):

A. Within-family size test -- paired bootstrap AUC(TU) differences between
   models of the same family, so size is separated from family.
B. Tie test -- committed predictions split by zero vs non-zero entropy. Shows
   that entropy works as a binary disagreement flag: the error rate jumps
   when there is any disagreement, but TU's magnitude discriminates little
   within the non-zero bucket. This is why the invisible-error SHARE, not
   AUC, is the headline statistic.
C. Debate split by source -- FinTradeBench vs the other four sources.

No correlation is fitted across the aggregate model points: with seven points
it would fit noise, and the project has already retracted one mechanism
fitted that way.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from analyze_core_run import auc, load_valid_rows  # noqa: E402
from hedgeqa_schema import read_jsonl  # noqa: E402

STRICT = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_strict.jsonl"
RUNS = [("gemma3:4b", "hedgeqa_core317_gemma3_4b"),
        ("qwen3:8b", "hedgeqa_core317_qwen3_8b"),
        ("gemma4:latest", "hedgeqa_core317_gemma4_latest"),
        ("gemma4:31b", "hedgeqa_core317_gemma4_31b-it-q8_0"),
        ("qwen3.6:27b", "hedgeqa_core317_qwen3_6_27b-q8_0"),
        ("qwen3.6:35b", "hedgeqa_core317_qwen3_6_35b-a3b-q8_0"),
        ("llama3.3:70b", "hedgeqa_core317_llama3_3_70b")]
PAIRS = [("gemma4:31b", "gemma4:latest"), ("gemma4:31b", "gemma3:4b"),
         ("qwen3.6:27b", "qwen3:8b")]
BOOT, SEED = 2000, 20260912


def main():
    items = {i.hedgeqa_id: i for i in read_jsonl(STRICT)}
    nc = {h: {x.lower() for x in i.noncommit_labels} for h, i in items.items()}
    R0, R1 = {}, {}
    for name, run in RUNS:
        d, _ = load_valid_rows(REPO / "results" / run / "rows.csv")
        d = d[d["correct"].notna()].copy()
        d["pnc"] = d.apply(lambda x: str(x["predicted"]).lower()
                           in nc.get(x["question_id"], set()), axis=1)
        d["ok"] = d["correct"].astype(bool)
        R0[name] = d[d["round"] == 0].set_index("question_id")
        R1[name] = d[d["round"] == 1].set_index("question_id")
    shared = sorted(set.intersection(
        *[set(R0[n].index) & set(R1[n].index) for n, _ in RUNS]))
    print(f"shared items: {len(shared)}")

    def pauc(f):
        f = f[~f["pnc"]]
        w, g = f[~f["ok"]]["tu"], f[f["ok"]]["tu"]
        return auc(w, g) if len(w) and len(g) else float("nan")

    print("\nA) WITHIN-FAMILY SIZE TEST, paired bootstrap "
          f"({BOOT}, same resamples)")
    rng = random.Random(SEED)
    draws = [[shared[rng.randrange(len(shared))] for _ in shared]
             for _ in range(BOOT)]
    for big, small in PAIRS:
        dif = sorted(x for x in (pauc(R1[big].loc[s]) - pauc(R1[small].loc[s])
                                 for s in draws) if x == x)
        d0 = pauc(R1[big].loc[shared]) - pauc(R1[small].loc[shared])
        lo, hi = dif[int(.025 * len(dif))], dif[int(.975 * len(dif)) - 1]
        print(f"   {big} - {small}: {d0:+.3f}  95% CI [{lo:+.3f}, {hi:+.3f}]"
              f"  -> {'distinguishable' if lo > 0 or hi < 0 else 'NOT distinguishable'}")

    print("\nB) TIE TEST: committed predictions, zero vs non-zero entropy")
    print(f"   {'model':14s} {'committed':>9s} {'zero-ent':>8s} "
          f"{'err|zero':>9s} {'err|nonzero':>11s} {'ratio':>6s} "
          f"{'invisible':>10s} {'AUC|nonzero':>11s}")
    for n, _ in RUNS:
        f = R1[n].loc[shared]
        c = f[~f["pnc"]]
        z, nz = c[c["tu"].abs() < 1e-9], c[c["tu"].abs() >= 1e-9]
        w, g = nz[~nz["ok"]]["tu"], nz[nz["ok"]]["tu"]
        a = auc(w, g) if len(w) and len(g) else float("nan")
        ez, enz = (~z["ok"]).mean(), (~nz["ok"]).mean()
        inv = int((~z["ok"]).sum())
        wrong = int((~c["ok"]).sum())
        print(f"   {n:14s} {len(c):9d} {len(z):8d} {ez:9.1%} {enz:11.1%} "
              f"{enz / ez:5.1f}x {inv:3d}/{wrong:<3d}{inv / wrong:4.0%} "
              f"{a:11.3f} (n={len(nz)})")

    print("\nC) DEBATE BY SOURCE (rescued / lost, net)")
    for n, _ in RUNS:
        a0, a1 = R0[n].loc[shared], R1[n].loc[shared]
        cells = []
        for sel in (a1["source_benchmark"] == "fintradebench",
                    a1["source_benchmark"] != "fintradebench"):
            o0, o1 = a0.loc[sel.values, "ok"], a1.loc[sel.values, "ok"]
            r, l = int((~o0 & o1).sum()), int((o0 & ~o1).sum())
            cells.append(f"{r} / {l}, {r - l:+d}")
        print(f"   {n:14s} r0 {a0['ok'].mean():5.1%}  FinTradeBench "
              f"{cells[0]:10s}  other {cells[1]:10s}  overall "
              f"{a1['ok'].mean() - a0['ok'].mean():+.1%}")


if __name__ == "__main__":
    main()
