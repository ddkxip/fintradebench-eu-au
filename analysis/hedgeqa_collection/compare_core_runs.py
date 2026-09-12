"""Compare several full-core runs model against model, on identical items.

    python analysis/hedgeqa_collection/compare_core_runs.py \
        --runs hedgeqa_core317_gemma3_4b,hedgeqa_core317_llama3_3_70b

Every run covers the same strict 317-item collection, so comparisons are
PAIRED: each statistic is computed over the items every compared run scored,
and the item set is printed so a reader can see it is the same for all.

## Why confidence intervals, now

The gemma3:4b analysis reported AUC(TU) 0.598 and called it "barely above
chance" without an interval. With ~250 committed predictions the sampling
error on an AUC is several points, so "0.60 vs 0.65" between two models could
easily be noise. Every AUC here carries a 95% item-level bootstrap interval,
and the between-model difference is bootstrapped on the SAME resampled items
(paired), which is far tighter than comparing two independent intervals.

## Rules carried over

* Natural and masked are never pooled; masked accuracy is a decline rate.
* The p_noncommit-vs-correctness split is circular and is not reported. The
  discrimination test holds commitment fixed (committed predictions only).
* Declining is reported per source, because on gemma3:4b one source carried
  all of it.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from analyze_core_run import auc  # noqa: E402
from hedgeqa_schema import read_jsonl  # noqa: E402

MASKED = "evidence_masked_insufficient"
STRICT = "data/hedgeqa/hedgeqa_core_v0_1_validated_strict.jsonl"


def load(run, nc_of):
    d = pd.read_csv(REPO / "results" / run / "rows.csv")
    models = d["model"].dropna().unique()
    out = {}
    for rnd in (0, 1):
        r = d[(d["round"] == rnd) & d["correct"].notna()].copy()
        r["pred_nc"] = r.apply(
            lambda x: str(x["predicted"]).lower()
            in nc_of.get(x["question_id"], set()), axis=1)
        r["ok"] = r["correct"].astype(bool)
        r["masked"] = r["hedgeqa_transformation"] == MASKED
        r["gold_nc"] = r["gold_commitment"] == "noncommitted"
        r["zero"] = r["tu"].abs() < 1e-9
        out[rnd] = r.set_index("question_id")
    return out, (models[0] if len(models) else run)


def boot_auc(frame, ids, n_boot, seed):
    """AUC(TU) for error among committed predictions, bootstrapped by item."""
    rng = random.Random(seed)
    ids = list(ids)
    vals = []
    for _ in range(n_boot):
        s = [ids[rng.randrange(len(ids))] for _ in ids]
        f = frame.loc[s]
        f = f[~f["pred_nc"]]
        w, g = f[~f["ok"]]["tu"], f[f["ok"]]["tu"]
        if len(w) and len(g):
            vals.append(auc(w, g))
    vals.sort()
    if not vals:
        return float("nan"), float("nan")
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals)) - 1]


def point_auc(frame):
    f = frame[~frame["pred_nc"]]
    w, g = f[~f["ok"]]["tu"], f[f["ok"]]["tu"]
    return auc(w, g) if len(w) and len(g) else float("nan")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", required=True)
    ap.add_argument("--boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20260912)
    args = ap.parse_args()

    items = {i.hedgeqa_id: i for i in read_jsonl(REPO / STRICT)}
    nc_of = {h: {x.lower() for x in i.noncommit_labels}
             for h, i in items.items()}
    runs = [r.strip() for r in args.runs.split(",") if r.strip()]
    data, names = {}, {}
    for r in runs:
        data[r], names[r] = load(r, nc_of)

    shared = set(items)
    for r in runs:
        shared &= set(data[r][1].index) & set(data[r][0].index)
    shared = sorted(shared)
    print(f"runs: {len(runs)}   items scored by ALL runs: {len(shared)} / "
          f"{len(items)}")
    for r in runs:
        miss = sorted(set(items) - set(data[r][1].index))
        print(f"  {names[r]:26s} scored {len(data[r][1])}"
              + (f"   unscored: {miss}" if miss else ""))

    W = max(len(names[r]) for r in runs) + 2

    def row(label, fn, fmt="{:.1%}"):
        cells = []
        for r in runs:
            v = fn(data[r][1].loc[shared], data[r][0].loc[shared])
            cells.append(v if isinstance(v, str) else fmt.format(v))
        print(f"  {label:34s}" + "".join(f"{c:>{W}s}" for c in cells))

    print("\n" + "=" * (36 + W * len(runs)))
    print(f"  {'':34s}" + "".join(f"{names[r]:>{W}s}" for r in runs))
    print("=" * (36 + W * len(runs)))

    nat = lambda f: f[~f["masked"]]
    msk = lambda f: f[f["masked"]]
    row("natural accuracy", lambda f, _: nat(f)["ok"].mean())
    row("MASKED decline rate", lambda f, _: msk(f)["ok"].mean())
    row("natural declined", lambda f, _: nat(f)["pred_nc"].mean())
    row("zero-entropy cells", lambda f, _: f["zero"].mean())
    row("committed & zero-entropy & WRONG",
        lambda f, _: str(int((~f["pred_nc"] & f["zero"] & ~f["ok"]).sum())),
        "{}")
    row("debate: rescued / lost",
        lambda f, f0: f"{int((~f0['ok'] & f['ok']).sum())} / "
                      f"{int((f0['ok'] & ~f['ok']).sum())}", "{}")
    row("accuracy r0 -> r1",
        lambda f, f0: f"{f0['ok'].mean():.1%}->{f['ok'].mean():.1%}", "{}")

    print("\n  DISCRIMINATION: AUC(TU) for error, committed predictions only")
    print("  (commitment held fixed, so p_noncommit cannot leak the answer)")
    for r in runs:
        f = data[r][1].loc[shared]
        lo, hi = boot_auc(f, shared, args.boot, args.seed)
        ncom = int((~f["pred_nc"]).sum())
        nerr = int((~f["pred_nc"] & ~f["ok"]).sum())
        print(f"    {names[r]:26s} AUC {point_auc(f):.3f}  "
              f"95% CI [{lo:.3f}, {hi:.3f}]   committed {ncom}, wrong {nerr}")

    if len(runs) >= 2:
        print("\n  PAIRED AUC DIFFERENCES (same bootstrap resamples)")
        base = runs[0]
        rng = random.Random(args.seed)
        draws = [[shared[rng.randrange(len(shared))] for _ in shared]
                 for _ in range(args.boot)]
        for r in runs[1:]:
            diffs = []
            for s in draws:
                a = point_auc(data[r][1].loc[s])
                b = point_auc(data[base][1].loc[s])
                if a == a and b == b:
                    diffs.append(a - b)
            diffs.sort()
            d0 = point_auc(data[r][1].loc[shared]) - \
                point_auc(data[base][1].loc[shared])
            lo = diffs[int(0.025 * len(diffs))]
            hi = diffs[int(0.975 * len(diffs)) - 1]
            verdict = ("distinguishable" if lo > 0 or hi < 0
                       else "NOT distinguishable")
            print(f"    {names[r]} - {names[base]}: {d0:+.3f}  "
                  f"95% CI [{lo:+.3f}, {hi:+.3f}]  -> {verdict}")

    print("\n  DECLINE RATE BY SOURCE (natural items)")
    srcs = sorted(nat(data[runs[0]][1].loc[shared])["source_benchmark"].unique())
    print(f"    {'source':15s}" + "".join(f"{names[r]:>{W}s}" for r in runs))
    for s in srcs:
        cells = []
        for r in runs:
            g = nat(data[r][1].loc[shared])
            g = g[g["source_benchmark"] == s]
            cells.append(f"{g['pred_nc'].mean():.1%} (n={len(g)})")
        print(f"    {s:15s}" + "".join(f"{c:>{W}s}" for c in cells))

    print("\n  MASKED ITEMS: paired agreement on declining")
    ms = [h for h in shared if data[runs[0]][1].loc[h, "masked"]]
    for i, a in enumerate(runs):
        for b in runs[i + 1:]:
            da = data[a][1].loc[ms, "ok"]
            db = data[b][1].loc[ms, "ok"]
            print(f"    {names[a]} vs {names[b]}: both declined "
                  f"{int((da & db).sum())}, only {names[a]} "
                  f"{int((da & ~db).sum())}, only {names[b]} "
                  f"{int((~da & db).sum())}, neither "
                  f"{int((~da & ~db).sum())}  (n={len(ms)})")


if __name__ == "__main__":
    main()
