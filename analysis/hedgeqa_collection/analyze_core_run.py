"""Analyse a full-core HedgeQA run.

    python analysis/hedgeqa_collection/analyze_core_run.py \
        --run hedgeqa_core317_gemma3_4b

Unlike the 15-item smoke analyses, n here is large enough to ask the question
the project exists for: **does the uncertainty signal separate the answers the
model gets right from the ones it gets wrong?** That needs sample size, not
anecdote, so it is reported with an AUC and a confidently-wrong count rather
than as a table of individual cells.

## Two rules carried over from the smoke analyses

1. **Natural and masked are never pooled.** A masked item's gold is
   CONSTRUCTED by us, and every masked gold is `insufficient_data`. Pooling
   reports a property of our masking as a property of the model, and on the
   masked stratum "accuracy" IS the decline rate -- a model that always
   declines scores 100% there. Masked results are labelled as decline rates.

2. **Debate is reported in both directions.** A net rate hides swaps: an
   earlier run moved 73% -> 73% while argging one correct item into an
   overcommitment and rescuing another.

## The failure taxonomy

    hedge_collision       gold committed,    model declined
    wrong_direction       gold committed,    model committed to the wrong label
    overcommitment        gold noncommittal, model committed
    wrong_noncommit_type  gold noncommittal, model chose another noncommittal
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from hedgeqa_schema import read_jsonl  # noqa: E402

MASKED = "evidence_masked_insufficient"


NUMERIC = ("tu", "au", "eu", "p_noncommit")


def load_valid_rows(path):
    """Read a run's rows.csv, keeping only rows with a real decomposition.

    Returns (rows, excluded) where `excluded` lists (question_id, round,
    reason) for every row dropped. Never drops silently.

    Why this exists: the runner appends each item's rows to the CSV by
    POSITION, without a header. When one agent parses nothing, that round has
    no decomposition, the item's rows carry a different column set, and every
    value after `parse_rate` lands under the wrong header. Found on
    llama3.3:70b `hqa_FTB_8315fbdd`: `tu` held "True" and `correct` held
    "0.0" -- and bool("0.0") is True, so a naive loader would have scored that
    garbage row as a CORRECT answer. It was caught only because `tu` failed to
    parse as a number and crashed the comparison.

    An item is kept only if EVERY one of its rounds is valid, because the
    paired round-0 -> round-1 analyses need both.
    """
    d = pd.read_csv(path, dtype=str, keep_default_na=False)
    reasons = {}
    for i, r in d.iterrows():
        why = []
        if r.get("gold_scoreable") not in ("True", "False"):
            why.append(f"gold_scoreable={r.get('gold_scoreable')!r:.40}")
        if r.get("correct") not in ("True", "False", ""):
            why.append(f"correct={r.get('correct')!r}")
        for c in NUMERIC:
            try:
                float(r.get(c, ""))
            except ValueError:
                why.append(f"{c} non-numeric")
                break
        if why:
            reasons.setdefault(r["question_id"], []).append(
                (r["round"], "; ".join(why)))
    bad_items = set(reasons)
    excluded = [(q, rnd, why) for q in sorted(bad_items)
                for rnd, why in reasons[q]]
    keep = d[~d["question_id"].isin(bad_items)].copy()
    for c in NUMERIC + ("round", "parse_rate"):
        keep[c] = pd.to_numeric(keep[c])
    keep["correct"] = keep["correct"].map(
        {"True": True, "False": False, "": None})
    return keep, excluded


def auc(pos, neg):
    """Mann-Whitney AUC: P(score(pos) > score(neg)), ties at 0.5.

    Rolled by hand to avoid a sklearn dependency. 0.5 is no discrimination.
    """
    pos, neg = list(pos), list(neg)
    if not pos or not neg:
        return float("nan")
    allv = sorted(pos + neg)
    rank = {}
    i = 0
    while i < len(allv):
        j = i
        while j + 1 < len(allv) and allv[j + 1] == allv[i]:
            j += 1
        r = (i + j) / 2.0 + 1.0
        rank[allv[i]] = r
        i = j + 1
    rp = sum(rank[v] for v in pos)
    return (rp - len(pos) * (len(pos) + 1) / 2.0) / (len(pos) * len(neg))


def pct(x):
    return "n/a" if x != x else f"{x:.1%}"


def block(title):
    print("\n" + "=" * 74)
    print(title)
    print("=" * 74)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--manifest",
                    default="data/hedgeqa/"
                            "hedgeqa_core_v0_1_validated_strict.jsonl")
    args = ap.parse_args()

    items = {i.hedgeqa_id: i for i in read_jsonl(REPO / args.manifest)}
    rows, excluded = load_valid_rows(REPO / "results" / args.run / "rows.csv")
    if excluded:
        print(f"EXCLUDED {len({q for q, _, _ in excluded})} item(s) with "
              f"malformed rows (not scored, not hidden):")
        for q, rnd, why in excluded:
            print(f"    {q} round {rnd}: {why}")
    r1 = rows[(rows["round"] == 1) & rows["correct"].notna()].copy()
    r0 = rows[(rows["round"] == 0) & rows["correct"].notna()].copy()

    nc_of = {h: {x.lower() for x in i.noncommit_labels}
             for h, i in items.items()}
    for d in (r0, r1):
        d["is_masked"] = d["hedgeqa_transformation"] == MASKED
        d["pred_nc"] = d.apply(
            lambda x: str(x["predicted"]).lower()
            in nc_of.get(x["question_id"], set()), axis=1)
        d["gold_nc"] = d["gold_commitment"] == "noncommitted"
        d["ok"] = d["correct"].astype(bool)
        d["zero_ent"] = d["tu"].abs() < 1e-9

    block(f"{args.run}")
    print(f"manifest      {args.manifest}")
    print(f"items scored  {len(r1)} / {len(items)}  "
          f"({len(r1) / len(items):.1%} complete)")
    print(f"parse_rate    mean {rows['parse_rate'].mean():.4f}  "
          f"min {rows['parse_rate'].min():.4f}")
    if len(r1) < len(items):
        print(f"\n  PARTIAL RUN -- {len(items) - len(r1)} items not yet "
              f"scored. Every figure below is over what has completed, and\n"
              f"  the manifest is processed in sorted-id order, so the "
              f"completed subset is NOT a random sample of sources.")

    nat, msk = r1[~r1["is_masked"]], r1[r1["is_masked"]]

    block("NATURAL ITEMS (gold from the source benchmark)")
    if len(nat):
        print(f"  n                {len(nat)}")
        print(f"  accuracy         {pct(nat['ok'].mean())}")
        print(f"  declined         {pct(nat['pred_nc'].mean())}   "
              f"(gold is non-committal on {pct(nat['gold_nc'].mean())})")
        print(f"  mean p_noncommit {nat['p_noncommit'].mean():.3f}")
        print(f"  zero-entropy     {pct(nat['zero_ent'].mean())}")

    block("MASKED ITEMS (constructed gold -- accuracy IS the decline rate)")
    if len(msk):
        print(f"  n                {len(msk)}")
        print(f"  DECLINED         {pct(msk['ok'].mean())}  "
              f"<- reported as a decline rate, not accuracy")
        print(f"  mean p_noncommit {msk['p_noncommit'].mean():.3f}")
        print(f"  zero-entropy     {pct(msk['zero_ent'].mean())}")

    block("FAILURE TAXONOMY (round 1, natural and masked separated)")
    print(f"  {'mode':24s} {'natural':>12s} {'masked':>12s}")
    modes = (
        ("hedge_collision", lambda d: ~d["gold_nc"] & d["pred_nc"]),
        ("wrong_direction", lambda d: ~d["gold_nc"] & ~d["pred_nc"] & ~d["ok"]),
        ("overcommitment", lambda d: d["gold_nc"] & ~d["pred_nc"]),
        ("wrong_noncommit_type", lambda d: d["gold_nc"] & d["pred_nc"]
         & ~d["ok"]),
    )
    for name, fn in modes:
        a = int(fn(nat).sum()) if len(nat) else 0
        b = int(fn(msk).sum()) if len(msk) else 0
        print(f"  {name:24s} {a:5d} ({pct(a / max(1, len(nat))):>5s}) "
              f"{b:5d} ({pct(b / max(1, len(msk))):>5s})")

    block("DOES UNCERTAINTY SEPARATE RIGHT FROM WRONG?")
    print("  The claim under test: a monitor watching entropy / p_noncommit")
    print("  can flag the answers the model gets wrong. AUC 0.50 = useless.\n")
    print("  WARNING -- the p_noncommit split below is CIRCULAR and is printed")
    print("  only to show how large the circularity is. On masked items every")
    print("  gold is `insufficient_data`, so being right just IS declining,")
    print("  and 'p_nc 0.05 when wrong vs 0.95 when right' restates the")
    print("  definition rather than measuring anything. The same holds in")
    print("  reverse for committed golds. Use AUC(TU), and above all the")
    print("  committed-only test in the next block, which holds the")
    print("  prediction's commitment fixed and so cannot be circular.\n")
    for lab, d in (("natural", nat), ("masked", msk), ("all", r1)):
        if not len(d) or d["ok"].nunique() < 2:
            print(f"  {lab:9s} -- not enough of both classes yet")
            continue
        wrong, right = d[~d["ok"]], d[d["ok"]]
        a_tu = auc(wrong["tu"], right["tu"])
        print(f"  {lab:9s} n={len(d):4d}  errors={len(wrong):4d}")
        print(f"      mean TU     wrong {wrong['tu'].mean():.3f} | "
              f"right {right['tu'].mean():.3f}   AUC(TU) {a_tu:.3f}")
        print(f"      mean p_nc   wrong {wrong['p_noncommit'].mean():.3f} | "
              f"right {right['p_noncommit'].mean():.3f}")
        ze = d[d["zero_ent"]]
        if len(ze):
            print(f"      zero-entropy cells {len(ze):4d}, of which WRONG "
                  f"{int((~ze['ok']).sum()):4d} "
                  f"({pct((~ze['ok']).mean())}) -- confidently wrong, "
                  f"invisible to an entropy monitor")

    block("NON-CIRCULAR TEST: among predictions the model COMMITTED to,\n"
          "can entropy tell right from wrong?")
    print("  Commitment is held fixed, so p_noncommit is near-constant and")
    print("  cannot leak the answer. This is the question an operator has:")
    print("  the model just gave me an answer -- can I tell if it is wrong?\n")
    for lab, d in (("all committed", r1[~r1["pred_nc"]]),
                   ("natural, committed gold",
                    r1[~r1["is_masked"] & ~r1["gold_nc"] & ~r1["pred_nc"]])):
        if not len(d) or d["ok"].nunique() < 2:
            continue
        w, g = d[~d["ok"]], d[d["ok"]]
        print(f"  {lab}")
        print(f"      n={len(d):4d}  wrong={len(w):4d} ({pct(len(w) / len(d))})"
              f"   AUC(TU) {auc(w['tu'], g['tu']):.3f}")
        print(f"      mean TU  wrong {w['tu'].mean():.3f} | "
              f"right {g['tu'].mean():.3f}")
        ze = d[d["zero_ent"]]
        if len(ze):
            print(f"      zero-entropy {len(ze):4d} of {len(d)}, of which "
                  f"WRONG {int((~ze['ok']).sum()):4d} "
                  f"({pct((~ze['ok']).mean())})")

    block("FAILURE MODES BY SOURCE (natural items)")
    print(f"  {'source':15s} {'n':>4s} {'hedge_coll':>11s} {'wrong_dir':>10s} "
          f"{'overcommit':>11s} {'declined':>9s}")
    for s, g in nat.groupby("source_benchmark"):
        hc = int((~g["gold_nc"] & g["pred_nc"]).sum())
        wd = int((~g["gold_nc"] & ~g["pred_nc"] & ~g["ok"]).sum())
        oc = int((g["gold_nc"] & ~g["pred_nc"]).sum())
        print(f"  {s:15s} {len(g):4d} {hc:11d} {wd:10d} {oc:11d} "
              f"{g['pred_nc'].mean():9.1%}")
    print("\n  Read this before quoting any pooled decline rate: if declining")
    print("  is concentrated in one source, the pooled figure describes the")
    print("  collection's composition more than the model's behaviour.")

    block("BY SOURCE (natural items only)")
    if len(nat):
        print(f"  {'source':15s} {'n':>4s} {'acc':>7s} {'declined':>9s} "
              f"{'p_nc':>6s}")
        for s, g in nat.groupby("source_benchmark"):
            print(f"  {s:15s} {len(g):4d} {g['ok'].mean():7.1%} "
                  f"{g['pred_nc'].mean():9.1%} {g['p_noncommit'].mean():6.2f}")

    block("BY TRANSFORMATION")
    print(f"  {'transformation':30s} {'n':>4s} {'acc/decline':>12s} "
          f"{'p_nc':>6s}")
    for s, g in r1.groupby("hedgeqa_transformation"):
        print(f"  {s:30s} {len(g):4d} {g['ok'].mean():12.1%} "
              f"{g['p_noncommit'].mean():6.2f}")

    block("BY GOLD COMMITMENT (natural items only)")
    if len(nat):
        print(f"  {'gold_commitment':20s} {'n':>4s} {'acc':>7s} "
              f"{'declined':>9s}")
        for s, g in nat.groupby("gold_commitment"):
            print(f"  {s:20s} {len(g):4d} {g['ok'].mean():7.1%} "
                  f"{g['pred_nc'].mean():9.1%}")

    block("DEBATE EFFECT (round 0 -> round 1), both directions")
    a0 = r0.set_index("question_id")["ok"]
    a1 = r1.set_index("question_id")["ok"]
    common = a0.index.intersection(a1.index)
    if len(common):
        resc = int((~a0[common] & a1[common]).sum())
        lost = int((a0[common] & ~a1[common]).sum())
        print(f"  overall   {a0[common].mean():.1%} -> {a1[common].mean():.1%}"
              f"   rescued {resc}, lost {lost}  (n={len(common)})")
        m = r1.set_index("question_id")["is_masked"]
        for lab, sel in (("natural", ~m[common]), ("masked", m[common])):
            idx = common[sel.values]
            if len(idx):
                rr = int((~a0[idx] & a1[idx]).sum())
                ll = int((a0[idx] & ~a1[idx]).sum())
                print(f"  {lab:9s} {a0[idx].mean():.1%} -> "
                      f"{a1[idx].mean():.1%}   rescued {rr}, lost {ll}  "
                      f"(n={len(idx)})")
        p0 = r0.set_index("question_id")["p_noncommit"]
        p1 = r1.set_index("question_id")["p_noncommit"]
        print(f"  mean p_noncommit {p0[common].mean():.3f} -> "
              f"{p1[common].mean():.3f} "
              f"({p1[common].mean() - p0[common].mean():+.3f})")

    block("CAVEATS")
    print("  - Masked golds are CONSTRUCTED. Two defective masked items were")
    print("    found and removed by hand-reading (see the triage doc); the")
    print("    masked stratum has not been re-read end to end.")
    print("  - One model, one K, one temperature, one seed.")
    print("  - Per-source cells are unequal; read them as descriptions of")
    print("    this collection, not as benchmark-level comparisons.")


if __name__ == "__main__":
    main()
