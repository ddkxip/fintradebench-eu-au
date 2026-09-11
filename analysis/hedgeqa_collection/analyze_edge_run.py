"""Analyse an edge-manifest run: does the model decline for the RIGHT reason?

    python analysis/hedgeqa_collection/analyze_edge_run.py \
        --run hedgeqa_edge15_gemma4 --compare hedgeqa_smoke15_gemma4

## Why accuracy is not reported as a headline

Every item in the edge manifest is a masked variant whose gold is
`insufficient_data`. On a single-label set, accuracy IS the decline rate and
a model that always declines scores 100%. Quoting it as accuracy would be
meaningless-to-flattering, so the decline rate is reported under its own
name and the analysis moves to the question the set was actually built for:
**when the model declines, what does it say it is declining about?**

An `evidence_gutted` item is one where a reviewer judged the masked document
visibly damaged. The worry is that a model declines because the input looks
broken rather than because the evidence is absent -- an answer that is right
for the wrong reason, and that would silently inflate any overcommitment
metric computed on masked items.

The two are separable in the rationale text:

  ABSENCE  "the statement does not report X", "no figure for 2019 is given"
  DAMAGE   "the text appears truncated", "the table is incomplete/corrupted"

Both patterns are counted, with the caveat that keyword matching over a
2-3 sentence rationale is a coarse instrument and the counts are a pointer
for reading, not a measurement.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from hedgeqa_schema import read_jsonl  # noqa: E402

MASKED = "evidence_masked_insufficient"

ABSENCE = re.compile(
    r"\b(does not (?:report|provide|include|contain|specify|disclose)|"
    r"not (?:reported|provided|given|disclosed|stated|available)|"
    r"no (?:figure|value|data|amount|information|breakdown)|"
    r"absent|missing|lacks?|without the)\b", re.I)
# NOTE: deliberately no trailing \b. Stem prefixes like "truncat" must match
# "truncated" / "truncation"; the original anchored group never fired on the
# commonest damage word in the vocabulary, which would have made a 0/300
# result look like evidence when it was partly a broken pattern.
DAMAGE = re.compile(
    r"\b(truncat|corrupt|garbl|malform|incomplete|cut off|"
    r"appears? (?:broken|damaged)|fragment|unreadable|"
    r"formatting|not legible|illegible)", re.I)


def rationales(run):
    """question_id -> list of round-1 rationale strings."""
    p = REPO / "results" / "raw" / run / "decodes.jsonl"
    out = collections.defaultdict(list)
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        if d.get("round") != 1:
            continue
        try:
            obj = json.loads(d.get("raw_text") or "{}")
        except Exception:
            continue
        r = obj.get("rationale")
        if r:
            out[d["question_id"]].append(r)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--compare", default=None)
    ap.add_argument("--manifest",
                    default="data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15.jsonl")
    ap.add_argument("--merged",
                    default="analysis/hedgeqa_collection/ai_review/"
                            "hedgeqa_core_review_merged.csv")
    args = ap.parse_args()

    items = {i.hedgeqa_id: i for i in read_jsonl(REPO / args.manifest)}
    rows = pd.read_csv(REPO / "results" / args.run / "rows.csv")
    r1 = rows[(rows["round"] == 1) & rows["correct"].notna()].copy()
    r0 = rows[(rows["round"] == 0) & rows["correct"].notna()].copy()

    merged = pd.read_csv(REPO / args.merged)
    fl = {r["hedgeqa_id"]: " ".join(
        str(r.get(f"{w}__flags") or "")
        for w in ("gemini_antigravity", "chatgpt_codex"))
        for _, r in merged.iterrows()}
    gutted = {h for h, s in fl.items() if "evidence_gutted" in s}

    nc_of = {h: {x.lower() for x in i.noncommit_labels}
             for h, i in items.items()}
    r1["declined"] = r1.apply(
        lambda x: str(x["predicted"]).lower() in nc_of.get(x["question_id"],
                                                           set()), axis=1)
    r1["gutted"] = r1["question_id"].isin(gutted)

    print(f"=== {args.run} ===")
    print(f"items {len(r1)}   parse_rate mean {rows['parse_rate'].mean():.4f}")
    print("\nEvery item is a masked variant with gold `insufficient_data`, so")
    print("accuracy on this set IS the decline rate. Reported as such.\n")

    print(f"  declined            {r1['declined'].mean():.1%} "
          f"({int(r1['declined'].sum())}/{len(r1)})")
    print(f"  mean p_noncommit    {r1['p_noncommit'].mean():.3f}")
    print(f"  zero-entropy cells  {(r1['tu'].abs() < 1e-9).mean():.0%}")

    print("\nGUTTED vs NON-GUTTED (the comparison the set exists for)")
    print(f"  {'group':22s} {'n':>2s} {'declined':>9s} {'p_nc':>6s}")
    for lab, sub in (("evidence_gutted", r1[r1["gutted"]]),
                     ("other masked", r1[~r1["gutted"]])):
        if len(sub):
            print(f"  {lab:22s} {len(sub):2d} {sub['declined'].mean():9.0%} "
                  f"{sub['p_noncommit'].mean():6.2f}")

    if args.compare:
        try:
            c = pd.read_csv(REPO / "results" / args.compare / "rows.csv")
            c1 = c[(c["round"] == 1) & c["correct"].notna()]
            cm = c1[c1["hedgeqa_transformation"] == MASKED]
            print(f"\n  for reference, clean masked items in {args.compare}: "
                  f"n={len(cm)} declined "
                  f"{cm['correct'].astype(bool).mean():.0%} "
                  f"p_nc {cm['p_noncommit'].mean():.2f}")
        except Exception as exc:
            print(f"  (comparison unavailable: {exc})")

    print("\nWHY DOES IT DECLINE? rationale keyword scan (round 1)")
    rat = rationales(args.run)
    tot = collections.Counter()
    per = {}
    for h in items:
        texts = rat.get(h, [])
        a = sum(1 for t in texts if ABSENCE.search(t))
        d = sum(1 for t in texts if DAMAGE.search(t))
        per[h] = (len(texts), a, d)
        tot["decodes"] += len(texts)
        tot["absence"] += a
        tot["damage"] += d
    print(f"  decodes scanned              {tot['decodes']}")
    print(f"  cite EVIDENCE ABSENCE        {tot['absence']} "
          f"({tot['absence']/max(1,tot['decodes']):.0%})")
    print(f"  cite DOCUMENT DAMAGE         {tot['damage']} "
          f"({tot['damage']/max(1,tot['decodes']):.0%})")
    print("  (coarse keyword match over 2-3 sentence rationales; a pointer")
    print("   for reading, not a measurement)")

    print("\nPER ITEM")
    print(f"  {'id':28s} {'gut':3s} {'pred':18s} {'p_nc':>5s} "
          f"{'dec':>4s} {'absence':>8s} {'damage':>7s}")
    for _, x in r1.sort_values("question_id").iterrows():
        h = x["question_id"]
        n, a, d = per.get(h, (0, 0, 0))
        print(f"  {h:28s} {'Y' if x['gutted'] else '-':3s} "
              f"{str(x['predicted'])[:18]:18s} {x['p_noncommit']:5.2f} "
              f"{'Y' if x['declined'] else 'n':>4s} {a:>4d}/{n:<3d} "
              f"{d:>3d}/{n:<3d}")

    a0 = r0.set_index("question_id")["correct"].astype(bool)
    a1 = r1.set_index("question_id")["correct"].astype(bool)
    common = a0.index.intersection(a1.index)
    # Report movement in BOTH directions, never the net rate alone: a
    # 73% -> 73% here concealed a 1-for-1 swap in which debate argued one
    # correctly-declining item INTO an overcommitment.
    resc = int((~a0[common] & a1[common]).sum())
    lost = int((a0[common] & ~a1[common]).sum())
    print(f"\nDEBATE EFFECT: decline rate {a0[common].mean():.0%} -> "
          f"{a1[common].mean():.0%}  rescued {resc}, lost {lost}  "
          f"(n={len(common)})")
    p0 = r0.set_index("question_id")["predicted"].astype(str)
    p1 = r1.set_index("question_id")["predicted"].astype(str)
    for h in common:
        if p0[h] != p1[h]:
            print(f"    {h:28s} {p0[h]:18s} -> {p1[h]}")

    print("\nSAMPLE RATIONALES (first decode of 3 items)")
    for h in list(items)[:3]:
        t = rat.get(h, [])
        if t:
            print(f"  {h}:\n    {t[0][:220]}")


if __name__ == "__main__":
    main()
