"""Apply the human review's verdict on controlled-insufficient variants.

Reads:
  data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl
  analysis/hedgeqa_collection/hedgeqa_core_v0_1_manual_review_completed.csv

Writes:
  data/hedgeqa/hedgeqa_core_v0_1_validated_candidates.jsonl
  analysis/hedgeqa_collection/HEDGEQA_MASKED_CLEANUP.md

Neither input is modified.

## The KEEP rule for a masked item

An `evidence_masked_insufficient` item survives only if ALL of these hold in
the human review:

  1. `masked_variant_valid == "yes"`   the reviewer tried and could not answer
  2. `reviewer_gold_label` is one of that item's `noncommit_labels`
  3. `evidence_sufficient_for_gold == "no"`   the intended state for a mask
  4. `keep_or_exclude == "keep"`
  5. the `notes` carry no indication the answer is still reconstructible

Anything else is excluded, including `unclear` on rule 1 -- an unconfirmed
suspicion of a leak is treated as a leak, because a masked item whose gold is
wrong inverts the overcommitment metric and nothing downstream catches it.

Rules 2 and 3 are not redundant with rule 1. A reviewer who answered the
question (`increased`, `yes`, ...) has demonstrated the mask failed whatever
they put in `masked_variant_valid`, so the label and the sufficiency flag are
independent evidence of the same fact. In this data all three agree on every
one of the 93 items, which is a consistency check passing rather than a
reason to drop two of the rules.

## Promotion

**Nothing is marked `manually_validated` by default.** Pass `--promote` to
set it on items that satisfy the documented rule below, and the reason is
written into each item's `notes`:

  PROMOTION RULE (only applied with --promote)
    masked items   : the five KEEP conditions above, i.e. a human confirmed
                     the constructed insufficiency holds. That is exactly the
                     claim the item makes, so confirming it validates it.
    natural items  : NOT promoted. A human agreeing with a reference label is
                     weaker than a human constructing one, and the label came
                     from the source benchmark rather than from this review.

## One decision beyond the masked scope, made explicit

The 5 natural items the human marked `keep_or_exclude == "exclude"` are also
dropped, because shipping a file called "validated" while retaining items the
reviewer explicitly rejected would misrepresent it. They are listed by id in
the report so the call is visible and reversible.

Usage:
    python analysis/hedgeqa_collection/apply_masked_cleanup.py [--promote]
"""

from __future__ import annotations

import argparse
import collections
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

CORE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
HUMAN = HERE / "hedgeqa_core_v0_1_manual_review_completed.csv"
MERGED = HERE / "ai_review" / "hedgeqa_core_review_merged.csv"
OUT = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_candidates.jsonl"
REPORT = HERE / "HEDGEQA_MASKED_CLEANUP.md"

MASKED = "evidence_masked_insufficient"

# Free-text in `notes` that indicates the reviewer thought the answer was
# still reachable. The boilerplate prompt shipped in the sheet
# ("CONSTRUCTED GOLD - verify ...") must NOT match, or every masked item
# would be excluded on its own instructions.
RECON_PATTERNS = [
    r"\breconstruct", r"\brecoverab", r"\bderivab", r"\bstill (?:be )?answer",
    r"\bcan be answered\b", r"\bsums? to\b", r"\btotal minus\b",
    r"\bback out\b", r"\binfer(?:red|able)?\b", r"\bstated in (?:the )?prose\b",
    r"\bleak", r"\bnot (?:really |truly )?insufficient\b",
]
BOILERPLATE = "constructed gold - verify the masked evidence"


def notes_indicate_reconstructible(notes: str):
    t = (notes or "").lower()
    if not t:
        return None
    t = t.replace(BOILERPLATE, " ")           # drop our own prompt text
    for pat in RECON_PATTERNS:
        m = re.search(pat, t)
        if m:
            return m.group(0)
    return None


def norm(v):
    return (v or "").strip().lower()


def masked_verdict(item, row):
    """-> (keep: bool, reason: str)."""
    if row is None:
        return False, "no human review row"
    mv = norm(row.get("masked_variant_valid"))
    lab = norm(row.get("reviewer_gold_label"))
    ev = norm(row.get("evidence_sufficient_for_gold"))
    ke = norm(row.get("keep_or_exclude"))
    ncs = {x.lower() for x in item.noncommit_labels}

    if mv == "no":
        return False, "human found a reconstruction route (masked_variant_valid=no)"
    if mv == "unclear":
        return False, "human unsure the mask holds (masked_variant_valid=unclear)"
    if mv != "yes":
        return False, f"masked_variant_valid not recorded ({mv!r})"
    if lab not in ncs:
        return False, (f"human answered the question ({lab!r}), so the mask "
                       f"did not hold")
    if ev != "no":
        return False, (f"evidence_sufficient_for_gold={ev!r}; a valid mask "
                       f"requires 'no'")
    if ke != "keep":
        return False, f"human keep_or_exclude={ke!r}"
    hit = notes_indicate_reconstructible(row.get("notes"))
    if hit:
        return False, f"notes indicate reconstructibility ({hit!r})"
    return True, "human confirmed the mask holds"


def main(promote=False):
    items = {i.hedgeqa_id: i for i in read_jsonl(CORE)}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        human = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}
    merged = {}
    if MERGED.exists():
        with MERGED.open(encoding="utf-8", newline="") as f:
            merged = {r["hedgeqa_id"]: r for r in csv.DictReader(f)}

    kept, dropped = [], []
    drop_reason, drop_src = collections.Counter(), collections.Counter()
    promoted = 0

    for hid, it in sorted(items.items()):
        row = human.get(hid)
        if it.transformation_type == MASKED:
            ok, why = masked_verdict(it, row)
            if not ok:
                dropped.append((hid, it, why, "masked"))
                drop_reason[why.split("(")[0].strip()] += 1
                drop_src[it.source_benchmark] += 1
                continue
            if promote:
                it.validation_status = "manually_validated"
                it.notes = ((it.notes + " | ") if it.notes else "") + (
                    "PROMOTED: human review confirmed the constructed "
                    "insufficiency (masked_variant_valid=yes, "
                    "gold in noncommit_labels, evidence_sufficient=no, keep)")
                promoted += 1
            kept.append(it)
        else:
            if row is not None and norm(row.get("keep_or_exclude")) == "exclude":
                dropped.append((hid, it, "human excluded this natural item",
                                "natural"))
                drop_reason["human excluded (natural item)"] += 1
                drop_src[it.source_benchmark] += 1
                continue
            kept.append(it)

    n = write_jsonl(kept, OUT)

    # ------------------------------------------------------------- report
    mk_before = [i for i in items.values() if i.transformation_type == MASKED]
    mk_after = [i for i in kept if i.transformation_type == MASKED]
    mk_dropped = [d for d in dropped if d[3] == "masked"]
    nat_dropped = [d for d in dropped if d[3] == "natural"]

    # leak routes: the human recorded no flags, so the routes come from the
    # AI reviewers' flags on the items the human failed
    routes = collections.Counter()
    gutted_kept = []
    both_ai_disagree_kept = []
    for hid, it, why, fam in mk_dropped:
        r = merged.get(hid, {})
        for who in ("gemini_antigravity", "chatgpt_codex"):
            for f in (r.get(f"{who}__flags") or "").split("|"):
                if f.strip():
                    routes[f.strip()] += 1
    for it in mk_after:
        r = merged.get(it.hedgeqa_id, {})
        fl = " ".join((r.get(f"{w}__flags") or "")
                      for w in ("gemini_antigravity", "chatgpt_codex"))
        if "evidence_gutted" in fl:
            gutted_kept.append(it.hedgeqa_id)
        if (norm(r.get("gemini_antigravity__masked_variant_valid")) == "no"
                and norm(r.get("chatgpt_codex__masked_variant_valid")) == "no"):
            both_ai_disagree_kept.append(it.hedgeqa_id)

    L = []
    A = L.append
    A("# HedgeQA-Core — masked-variant cleanup")
    A("")
    A("Generated by `apply_masked_cleanup.py` from the completed human "
      "review. Inputs are not modified.")
    A("")
    A(f"**Output:** `data/hedgeqa/hedgeqa_core_v0_1_validated_candidates.jsonl` "
      f"— {n} items.")
    A("")
    A("**Nothing is `manually_validated`**" if not promote else
      f"**{promoted} masked items promoted to `manually_validated`** under "
      f"the rule documented in this script and below.")
    A("")

    A("## The keep rule")
    A("")
    A("A masked item survives only if the human review recorded **all** of:")
    A("")
    A("1. `masked_variant_valid = yes` — tried, could not answer")
    A("2. `reviewer_gold_label` ∈ that item's `noncommit_labels`")
    A("3. `evidence_sufficient_for_gold = no`")
    A("4. `keep_or_exclude = keep`")
    A("5. no reconstructibility indication in `notes`")
    A("")
    A("`unclear` on rule 1 excludes: an unconfirmed suspicion of a leak is "
      "treated as a leak, because a masked item with a wrong gold inverts the "
      "overcommitment metric and nothing downstream catches it.")
    A("")

    A("## Counts")
    A("")
    A("| | items |")
    A("|---|---|")
    A(f"| masked items before cleanup | **{len(mk_before)}** |")
    A(f"| masked excluded (human-failed) | **{len(mk_dropped)}** |")
    A(f"| masked kept (human-valid) | **{len(mk_after)}** |")
    A(f"| natural items excluded (human `exclude`) | {len(nat_dropped)} |")
    A(f"| **final collection** | **{n}** |")
    A("")
    A(f"The human failure rate on masked variants is "
      f"**{len(mk_dropped)}/{len(mk_before)} = "
      f"{len(mk_dropped)/len(mk_before):.0%}**.")
    A("")

    A("### Masked exclusions by source")
    A("")
    A("| source | excluded | kept | before |")
    A("|---|---|---|---|")
    src_before = collections.Counter(i.source_benchmark for i in mk_before)
    src_after = collections.Counter(i.source_benchmark for i in mk_after)
    for s in sorted(src_before):
        A(f"| {s} | {src_before[s] - src_after[s]} | {src_after[s]} | "
          f"{src_before[s]} |")
    A("")

    A("### Exclusion reasons")
    A("")
    A("| reason | items |")
    A("|---|---|")
    for k, v in drop_reason.most_common():
        A(f"| {k} | {v} |")
    A("")

    A("## Leak routes in the excluded items")
    A("")
    A("The human review recorded **no flags** — the review app offered them "
      "but the reviewer used the structured fields instead. The routes below "
      "come from the two AI reviewers' flags on the same items, and are "
      "corroborating rather than primary evidence.")
    A("")
    if routes:
        A("| flag | occurrences |")
        A("|---|---|")
        for k, v in routes.most_common():
            A(f"| `{k}` | {v} |")
    else:
        A("_none recorded_")
    A("")
    A("`total_minus_components` is a route `masking.py` already guards, and "
      "the automated check passed every one of these items. Its appearance "
      "here means the guard's coverage is narrower than the route: it tests "
      "pipe-delimited table columns, and misses the same arithmetic when the "
      "figures sit in prose, across two tables, or behind one more step. "
      "**That is the concrete guard gap to fix before constructing more "
      "masks.**")
    A("")

    A("## Two things worth a second look in the KEPT set")
    A("")
    A(f"- **{len(gutted_kept)} kept item(s) were flagged `evidence_gutted`** "
      f"by an AI reviewer. A gutted document is a different defect from a "
      f"leak: a model may decline because the input looks damaged rather than "
      f"because the evidence is absent, which confounds the very measurement "
      f"these items exist for. They pass the human rule and are kept, but "
      f"they should be read.")
    if gutted_kept:
        A("")
        A("  " + ", ".join(f"`{x}`" for x in gutted_kept[:20]))
    A("")
    A(f"- **{len(both_ai_disagree_kept)} kept item(s) had BOTH AI reviewers "
      f"report the answer reachable** while the human did not. The human's "
      f"judgement governs, but a unanimous AI dissent is the cheapest place "
      f"to look for a route the human missed.")
    if both_ai_disagree_kept:
        A("")
        A("  " + ", ".join(f"`{x}`" for x in both_ai_disagree_kept))
    A("")

    A("## Corroboration of the human verdict")
    A("")
    both = sum(1 for hid, _, _, fam in mk_dropped
               if fam == "masked"
               and norm(merged.get(hid, {}).get(
                   "gemini_antigravity__masked_variant_valid")) == "no"
               and norm(merged.get(hid, {}).get(
                   "chatgpt_codex__masked_variant_valid")) == "no")
    one = sum(1 for hid, _, _, fam in mk_dropped
              if fam == "masked"
              and (norm(merged.get(hid, {}).get(
                  "gemini_antigravity__masked_variant_valid")) == "no"
                   or norm(merged.get(hid, {}).get(
                       "chatgpt_codex__masked_variant_valid")) == "no"))
    A(f"Of the {len(mk_dropped)} masked items the human failed, **at least "
      f"one AI reviewer independently agreed on {one}** and **both agreed on "
      f"{both}**. The exclusions are not one reader's idiosyncrasy.")
    A("")

    A("## Final collection composition")
    A("")
    for title, key in (("By source", lambda i: i.source_benchmark),
                       ("By answer_type", lambda i: i.answer_type),
                       ("By transformation_type",
                        lambda i: i.transformation_type),
                       ("By gold_commitment", lambda i: i.gold_commitment),
                       ("By validation_status",
                        lambda i: i.validation_status)):
        A(f"### {title}")
        A("")
        A("| value | items |")
        A("|---|---|")
        for k, v in collections.Counter(key(i) for i in kept).most_common():
            A(f"| `{k}` | {v} |")
        A("")

    nc = sum(1 for i in kept if i.gold_commitment == "noncommitted")
    nat = [i for i in kept if i.transformation_type != MASKED]
    ncn = sum(1 for i in nat if i.gold_commitment == "noncommitted")
    A("## What the cleanup costs")
    A("")
    A(f"Non-committal gold: **{nc}/{n} = {nc/n:.1%}** "
      f"(was 112/368 = 30.4%).")
    A(f"Of these, **{nc - ncn} are constructed** masked items and "
      f"**{ncn} are natural**, all in FinTradeBench.")
    A("")
    A("Removing half the masked variants removes half the constructed "
      "non-committal stratum. Overcommitment and wrong-non-committal-type "
      "are now measurable on a smaller base, and outside FinTradeBench they "
      "still rest entirely on constructed items — just fewer, better ones. "
      "That is the honest trade: the metric is narrower and the items behind "
      "it are trustworthy.")
    A("")
    A("## Natural items excluded")
    A("")
    if nat_dropped:
        A("| id | source | reason recorded by the reviewer |")
        A("|---|---|---|")
        for hid, it, why, _ in nat_dropped:
            r = human.get(hid, {})
            A(f"| `{hid}` | {it.source_benchmark} | "
              f"{(r.get('exclusion_reason') or '')[:80]} |")
        A("")
        A("These were dropped because shipping a file called *validated* "
          "while retaining items the reviewer explicitly rejected would "
          "misrepresent it. This is a decision beyond the masked-cleanup "
          "scope, listed here so it is visible and reversible.")
    else:
        A("_none_")
    A("")

    REPORT.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"masked before={len(mk_before)} excluded={len(mk_dropped)} "
          f"kept={len(mk_after)}")
    print(f"natural excluded={len(nat_dropped)}")
    print(f"final collection={n} -> {OUT.relative_to(REPO)}")
    print(f"promoted to manually_validated: {promoted}"
          + ("" if promote else "  (use --promote to apply)"))
    print(f"report -> {REPORT.relative_to(REPO)}")
    return kept


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--promote", action="store_true",
                    help="set manually_validated on masked items meeting the "
                         "documented rule")
    main(promote=ap.parse_args().promote)
