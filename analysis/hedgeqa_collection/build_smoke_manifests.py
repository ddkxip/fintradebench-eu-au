"""Build the 15-item smoke manifest and its risky edge-case counterpart.

Input   data/hedgeqa/hedgeqa_core_v0_1_validated_candidates.jsonl (319 items)
Output  data/hedgeqa/hedgeqa_core_v0_1_smoke_15.jsonl
        data/hedgeqa/hedgeqa_core_v0_1_smoke_15_manifest.md
        data/hedgeqa/hedgeqa_core_v0_1_edge_smoke_15.jsonl

3 items per source, 15 total, deterministic.

## What the main manifest excludes, and why

* the 10 kept masked items an AI reviewer flagged `evidence_gutted` -- a
  model may decline on those because the input looks damaged rather than
  because the evidence is absent, which confounds the one thing a smoke run
  is meant to check;
* `hqa_TAT_924db34b_masked` specifically (it is also in that set);
* anything not in the validated 319;
* anything whose human-review notes read as unresolved.

## Composition target per source

Where the pool allows: a natural committed item, a natural non-committal
item, and a valid masked item. Only FinTradeBench has natural non-committal
golds after the convention revision, and only FinTradeBench has no masked
items, so the realised mix differs by source and is reported rather than
asserted.

Usage: python analysis/hedgeqa_collection/build_smoke_manifests.py
"""

from __future__ import annotations

import collections
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

VALID = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_candidates.jsonl"
MERGED = HERE / "ai_review" / "hedgeqa_core_review_merged.csv"
HUMAN = HERE / "hedgeqa_core_v0_1_manual_review_completed.csv"
SMOKE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_smoke_15.jsonl"
EDGE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_edge_smoke_15.jsonl"
MANIFEST = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_smoke_15_manifest.md"

MASKED = "evidence_masked_insufficient"
SOURCES = ["fintradebench", "financebench", "tatqa", "finqa", "convfinqa"]
PER_SOURCE = 3
ALWAYS_EXCLUDE = {"hqa_TAT_924db34b_masked"}
UNRESOLVED = re.compile(r"\b(unsure|unclear|revisit|check again|not sure|"
                        r"todo|\?\?)\b", re.I)


def load_side_tables():
    merged, human = {}, {}
    if MERGED.exists():
        with MERGED.open(encoding="utf-8", newline="") as f:
            merged = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}
    if HUMAN.exists():
        with HUMAN.open(encoding="utf-8", newline="") as f:
            human = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}
    return merged, human


def flags_for(hid, merged):
    return " ".join((merged.get(hid, {}).get(f"{w}__flags") or "")
                    for w in ("gemini_antigravity", "chatgpt_codex"))


def pick(pool, want, taken):
    """First `want` items not already taken, deterministic by id."""
    out = []
    for it in sorted(pool, key=lambda x: x.hedgeqa_id):
        if len(out) >= want:
            break
        if it.hedgeqa_id in taken:
            continue
        out.append(it)
        taken.add(it.hedgeqa_id)
    return out


def main():
    items = read_jsonl(VALID)
    merged, human = load_side_tables()

    gutted = {i.hedgeqa_id for i in items
              if "evidence_gutted" in flags_for(i.hedgeqa_id, merged)}
    unresolved = {i.hedgeqa_id for i in items
                  if UNRESOLVED.search(human.get(i.hedgeqa_id, {})
                                       .get("notes") or "")}
    barred = gutted | unresolved | ALWAYS_EXCLUDE

    clean = [i for i in items if i.hedgeqa_id not in barred]
    risky = [i for i in items if i.hedgeqa_id in barred]

    # ------------------------------------------------------------ main smoke
    chosen, taken, realised = [], set(), {}
    for src in SOURCES:
        pool = [i for i in clean if i.source_benchmark == src]
        nat_nc = [i for i in pool if i.transformation_type != MASKED
                  and i.gold_commitment == "noncommitted"]
        msk = [i for i in pool if i.transformation_type == MASKED]
        nat_c = [i for i in pool if i.transformation_type != MASKED
                 and i.gold_commitment == "committed"]
        got = []
        got += pick(nat_nc, 1, taken)          # scarce: prefer first
        got += pick(msk, 1, taken)
        got += pick(nat_c, PER_SOURCE - len(got), taken)
        # top up from anything left in this source if a family was empty
        if len(got) < PER_SOURCE:
            got += pick(pool, PER_SOURCE - len(got), taken)
        chosen.extend(got)
        realised[src] = got

    n = write_jsonl(chosen, SMOKE)

    # ------------------------------------------------------------ edge smoke
    # Seed `etaken` with the main manifest so the two sets are DISJOINT.
    # An item in both would let a failure be reported against whichever set
    # made it look better, and makes "clean on smoke, dirty on edge"
    # impossible to interpret.
    edge, etaken = [], {i.hedgeqa_id for i in chosen}
    edge += pick([i for i in risky if i.hedgeqa_id in gutted], 10, etaken)
    remaining = PER_SOURCE * len(SOURCES) - len(edge)
    if remaining > 0:
        # fill with the kept masked items both AI reviewers called reachable,
        # then any other masked item, so the edge set stays stress-shaped
        both_no = [i for i in items
                   if i.transformation_type == MASKED
                   and (merged.get(i.hedgeqa_id, {})
                        .get("gemini_antigravity__masked_variant_valid",
                             "").strip().lower() == "no")
                   and (merged.get(i.hedgeqa_id, {})
                        .get("chatgpt_codex__masked_variant_valid",
                             "").strip().lower() == "no")]
        edge += pick(both_no, remaining, etaken)
        remaining = PER_SOURCE * len(SOURCES) - len(edge)
        if remaining > 0:
            edge += pick([i for i in items
                          if i.transformation_type == MASKED], remaining,
                         etaken)
    ne = write_jsonl(edge, EDGE)

    # -------------------------------------------------------------- manifest
    L, A = [], None
    A = L.append
    A("# HedgeQA-Core smoke manifests")
    A("")
    A("Generated by `build_smoke_manifests.py` from the 319-item validated "
      "collection. Deterministic: selection is by sorted id within each "
      "stratum.")
    A("")
    A("**Nothing here is `manually_validated`.** These are smoke-test "
      "manifests, not a certified subset.")
    A("")
    A("## Main manifest — `hedgeqa_core_v0_1_smoke_15.jsonl`")
    A("")
    A(f"**{n} items, 3 per source.** Intended as the first end-to-end run: "
      f"big enough to exercise every code path, small enough that a failure "
      f"is cheap to diagnose.")
    A("")
    A("| # | hedgeqa_id | source | transformation | answer_type | commitment |")
    A("|---|---|---|---|---|---|")
    for k, i in enumerate(chosen, 1):
        A(f"| {k} | `{i.hedgeqa_id}` | {i.source_benchmark} | "
          f"{i.transformation_type} | {i.answer_type} | {i.gold_commitment} |")
    A("")
    A("### Realised composition")
    A("")
    A("| source | items | natural committed | natural non-committal | masked |")
    A("|---|---|---|---|---|")
    for src in SOURCES:
        got = realised[src]
        nc = sum(1 for i in got if i.transformation_type != MASKED
                 and i.gold_commitment == "noncommitted")
        mk = sum(1 for i in got if i.transformation_type == MASKED)
        A(f"| {src} | {len(got)} | {len(got) - nc - mk} | {nc} | {mk} |")
    A("")
    for title, fn in (("By transformation_type",
                       lambda i: i.transformation_type),
                      ("By answer_type", lambda i: i.answer_type),
                      ("By gold_commitment", lambda i: i.gold_commitment)):
        A(f"**{title}:** " + ", ".join(
            f"`{k}`={v}" for k, v in
            collections.Counter(fn(i) for i in chosen).most_common()))
        A("")
    A("The mix is reported rather than asserted. After the convention "
      "revision only FinTradeBench has natural non-committal golds, and "
      "FinTradeBench has no masked items at all, so no single source can "
      "supply all five requested families.")
    A("")
    A("### Exclusions applied")
    A("")
    A(f"- **{len(gutted)} kept masked items flagged `evidence_gutted`** by an "
      f"AI reviewer. A gutted document is a confound, not a leak: a model may "
      f"decline because the input looks damaged rather than because the "
      f"evidence is absent, which is the one thing a smoke run must not be "
      f"ambiguous about.")
    A(f"- `hqa_TAT_924db34b_masked`, named explicitly (also in that set).")
    A(f"- Everything outside the validated 319.")
    A(f"- Items with unresolved-looking human notes: **{len(unresolved)}** "
      f"found.")
    A("")
    A("## Edge manifest — `hedgeqa_core_v0_1_edge_smoke_15.jsonl`")
    A("")
    A(f"**{ne} items. STRESS TEST ONLY — do not pool these with the main "
      f"manifest and do not report a metric over them without saying which "
      f"set it came from.**")
    A("")
    A("These are kept, human-validated items that are nonetheless the "
      "hardest cases in the collection: the `evidence_gutted` ones, and "
      "masked items where both AI reviewers believed the answer was still "
      "reachable while the human did not. They exist to find out whether a "
      "system declines for the right reason.")
    A("")
    A("| # | hedgeqa_id | source | transformation | why it is here |")
    A("|---|---|---|---|---|")
    for k, i in enumerate(edge, 1):
        why = ("flagged evidence_gutted" if i.hedgeqa_id in gutted
               else "both AI reviewers called the answer reachable"
               if (merged.get(i.hedgeqa_id, {})
                   .get("gemini_antigravity__masked_variant_valid",
                        "").strip().lower() == "no")
               else "masked variant, stress case")
        A(f"| {k} | `{i.hedgeqa_id}` | {i.source_benchmark} | "
          f"{i.transformation_type} | {why} |")
    A("")
    A("## Caveats")
    A("")
    A("- 15 items cannot support a rate. Use these to check the pipeline "
      "runs, parses, and scores — not to measure hedging.")
    A("- The main manifest deliberately avoids the hardest items, so a "
      "clean pass on it says nothing about the edge set.")
    A("- Both manifests are subsets of the validated collection, whose "
      "masked items are constructed and whose non-committal stratum outside "
      "FinTradeBench is entirely constructed.")

    MANIFEST.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"smoke  : {n} items -> {SMOKE.name}")
    print(f"edge   : {ne} items -> {EDGE.name}")
    print(f"barred from main: {len(barred)} "
          f"(gutted {len(gutted)}, unresolved {len(unresolved)})")
    for src in SOURCES:
        got = realised[src]
        print(f"   {src:14s} {[i.transformation_type[:4] for i in got]} "
              f"{[i.gold_commitment[:6] for i in got]}")
    print(f"manifest -> {MANIFEST.name}")


if __name__ == "__main__":
    main()
