"""Summarise a HedgeQA debate run.

    python analysis/hedgeqa_collection/analyze_hedgeqa_run.py \
        --run hedgeqa_smoke15_gemma4

Reports accuracy, p_noncommit, the error decomposition and the round-0 to
round-1 movement, split by source and by transformation type.

## What 15 items can and cannot support

A smoke run answers "does the pipeline work end to end and are the outputs
shaped correctly". It cannot support a rate: with n=15 the 95% CI on any
proportion is roughly +/-25 points, so every number below is an observation,
not an estimate. Per-source cells hold 3 items each and are printed only to
show the pipeline exercised every source.

The natural / masked split is kept throughout, because a masked item's gold
is constructed and pooling the two reports a property of our masking as a
property of the model.
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from hedgeqa_schema import read_jsonl  # noqa: E402

MASKED = "evidence_masked_insufficient"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--manifest",
                    default="data/hedgeqa/hedgeqa_core_v0_1_smoke_15.jsonl")
    args = ap.parse_args()

    rows = pd.read_csv(REPO / "results" / args.run / "rows.csv")
    items = {i.hedgeqa_id: i for i in read_jsonl(REPO / args.manifest)}
    nc_of = {h: {x.lower() for x in i.noncommit_labels}
             for h, i in items.items()}

    r1 = rows[(rows["round"] == 1) & rows["correct"].notna()].copy()
    r0 = rows[(rows["round"] == 0) & rows["correct"].notna()].copy()
    for d in (r0, r1):
        d["is_masked"] = d["hedgeqa_transformation"] == MASKED
        d["pred_nc"] = d.apply(
            lambda x: str(x["predicted"]).lower()
            in nc_of.get(x["question_id"], set()), axis=1)
        d["gold_nc"] = d["gold_commitment"] == "noncommitted"
        d["err"] = ~d["correct"].astype(bool)

    print(f"=== {args.run} ===")
    print(f"items scored: {len(r1)} / {len(items)}    "
          f"parse_rate mean {rows['parse_rate'].mean():.4f} "
          f"min {rows['parse_rate'].min():.3f}\n")

    print("OVERALL (round 1)")
    print(f"  accuracy      {r1['correct'].mean():.1%}  "
          f"({int(r1['correct'].sum())}/{len(r1)})")
    print(f"  mean p_nc     {r1['p_noncommit'].mean():.3f}")
    print(f"  mean TU/AU/EU {r1['tu'].mean():.3f} / {r1['au'].mean():.3f} "
          f"/ {r1['eu'].mean():.3f}")
    zero = (r1['tu'].abs() < 1e-9).mean()
    print(f"  zero-entropy cells {zero:.0%}  "
          f"(every sample from every agent identical)")

    for lab, sub in (("NATURAL", r1[~r1["is_masked"]]),
                     ("MASKED (constructed gold)", r1[r1["is_masked"]])):
        if not len(sub):
            continue
        print(f"\n{lab}  n={len(sub)}")
        print(f"  accuracy   {sub['correct'].mean():.1%}")
        print(f"  mean p_nc  {sub['p_noncommit'].mean():.3f}")
        print(f"  declined   {sub['pred_nc'].mean():.1%} of items")

    print("\nERROR DECOMPOSITION (round 1)")
    e = r1[r1["err"]]
    if len(e):
        hc = int((~e["gold_nc"] & e["pred_nc"]).sum())
        wd = int((~e["gold_nc"] & ~e["pred_nc"]).sum())
        oc = int((e["gold_nc"] & ~e["pred_nc"]).sum())
        wn = int((e["gold_nc"] & e["pred_nc"]).sum())
        for name, v in (("hedge_collision", hc), ("wrong_direction", wd),
                        ("overcommitment", oc), ("wrong_noncommit_type", wn)):
            print(f"  {name:22s} {v:2d}/{len(e)}  {v/len(e):.0%}")
    else:
        print("  no errors")

    print("\nBY SOURCE (3 items each — shape check only, not a rate)")
    print(f"  {'source':15s} {'n':>2s} {'acc':>6s} {'p_nc':>6s}")
    for s, g in r1.groupby("source_benchmark"):
        print(f"  {s:15s} {len(g):2d} {g['correct'].mean():6.0%} "
              f"{g['p_noncommit'].mean():6.2f}")

    print("\nBY TRANSFORMATION")
    print(f"  {'transformation':30s} {'n':>2s} {'acc':>6s} {'p_nc':>6s}")
    for s, g in r1.groupby("hedgeqa_transformation"):
        print(f"  {s:30s} {len(g):2d} {g['correct'].mean():6.0%} "
              f"{g['p_noncommit'].mean():6.2f}")

    print("\nDEBATE EFFECT (round 0 -> round 1)")
    a0 = r0.set_index("question_id")["correct"].astype(bool)
    a1 = r1.set_index("question_id")["correct"].astype(bool)
    common = a0.index.intersection(a1.index)
    resc = int((~a0[common] & a1[common]).sum())
    lost = int((a0[common] & ~a1[common]).sum())
    print(f"  accuracy {a0[common].mean():.1%} -> {a1[common].mean():.1%}   "
          f"rescued {resc}, lost {lost}  (n={len(common)})")
    p0 = r0.set_index("question_id")["p_noncommit"]
    p1 = r1.set_index("question_id")["p_noncommit"]
    print(f"  mean p_nc {p0[common].mean():.3f} -> {p1[common].mean():.3f} "
          f"({p1[common].mean() - p0[common].mean():+.3f})")

    print("\nPER ITEM")
    print(f"  {'id':26s} {'source':14s} {'transf':6s} {'gold':18s} "
          f"{'pred':18s} {'p_nc':>5s} ok")
    for _, x in r1.sort_values(["source_benchmark", "question_id"]).iterrows():
        it = items[x["question_id"]]
        tr = ("mask" if x["is_masked"]
              else "dir" if x["hedgeqa_transformation"] != "none" else "nat")
        print(f"  {x['question_id']:26s} {x['source_benchmark']:14s} "
              f"{tr:6s} {str(it.gold_label)[:18]:18s} "
              f"{str(x['predicted'])[:18]:18s} {x['p_noncommit']:5.2f} "
              f"{'Y' if x['correct'] else 'n'}")


if __name__ == "__main__":
    main()
