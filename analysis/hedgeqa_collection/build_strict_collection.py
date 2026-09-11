"""Exclude the two defective FinanceBench masked items; emit the strict set.

    python analysis/hedgeqa_collection/build_strict_collection.py

Input   data/hedgeqa/hedgeqa_core_v0_1_validated_candidates.jsonl (319)
Output  data/hedgeqa/hedgeqa_core_v0_1_validated_strict.jsonl     (317)
        analysis/hedgeqa_collection/HEDGEQA_STRICT_FINALIZATION.md

## Why these two are removed

Both were found by hand-reading the three FinanceBench items the edge run
scored as overcommitments (`HEDGEQA_FB_OVERCOMMIT_TRIAGE.md`). Neither is a
model failure and neither is repairable by re-masking:

* `hqa_FB_9fc58fab_masked` -- the constructed gold is WRONG. The question asks
  whether CVS has ongoing legal battles; masking removed only the opioid
  settlement's dollar amounts, and four paragraphs of litigation survive. The
  surviving prose supports `yes`. The question is not maskable by
  number-deletion at all, because its answer never depended on the figures.

* `hqa_FB_5dbbcec0_masked` -- line deletion SPLICED two unrelated sentences
  into a fluent false one, so the document asserts the opposite of the truth.
  Repair would require restoring the splice, after which the document answers
  `yes` and is not an insufficient-evidence item.

Nothing else is changed: the same items, in the same order, minus two.
The 319-item file, the raw human review and the raw AI review outputs are all
left untouched.
"""

from __future__ import annotations

import collections
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from hedgeqa_schema import read_jsonl, write_jsonl  # noqa: E402

SRC = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_candidates.jsonl"
DST = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_strict.jsonl"
DOC = HERE / "HEDGEQA_STRICT_FINALIZATION.md"

MASKED = "evidence_masked_insufficient"

EXCLUDE = {
    "hqa_FB_9fc58fab_masked":
        "constructed gold is wrong; surviving prose still supports `yes`",
    "hqa_FB_5dbbcec0_masked":
        "line deletion spliced the document into a fluent false statement",
}


def table(rows, headers):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(x) for x in r) + " |")
    return out


def counts(items, key):
    c = collections.Counter(key(i) for i in items)
    return [(k, v, f"{v / max(1, len(items)):.1%}")
            for k, v in sorted(c.items(), key=lambda x: (-x[1], x[0]))]


def main():
    items = read_jsonl(SRC)
    before = len(items)

    present = [h for h in EXCLUDE if any(i.hedgeqa_id == h for i in items)]
    missing = sorted(set(EXCLUDE) - set(present))
    if missing:
        raise SystemExit(
            f"[ABORT] {len(missing)} item(s) to exclude are not in the input: "
            f"{missing}. Refusing to write a strict file whose size would "
            f"silently differ from the documented 317.")

    strict = [i for i in items if i.hedgeqa_id not in EXCLUDE]
    n = write_jsonl(strict, DST)
    if n != before - len(EXCLUDE):
        raise SystemExit(f"[ABORT] expected {before - len(EXCLUDE)}, wrote {n}")

    fb_masked = [i for i in strict if i.source_benchmark == "financebench"
                 and i.transformation_type == MASKED]
    nat = [i for i in strict if i.transformation_type != MASKED]
    msk = [i for i in strict if i.transformation_type == MASKED]

    L = []
    A = L.append
    A("# HedgeQA-Core-v0.1 — strict finalization")
    A("")
    A(f"**{before} → {len(strict)}.** Two FinanceBench masked items are "
      f"excluded as **construction defects**, not as model failures. Built by "
      f"`build_strict_collection.py`; the 319-item file, the raw human review "
      f"and the raw AI review outputs are untouched.")
    A("")
    A("## Headline counts")
    A("")
    L.extend(table([
        ("previous cleaned size", before),
        ("excluded defective FinanceBench masked items", len(EXCLUDE)),
        ("**final strict size**", f"**{len(strict)}**"),
    ], ["", "n"]))
    A("")
    A(f"`{DST.name}` sha256 "
      f"`{hashlib.sha256(DST.read_bytes()).hexdigest()[:16]}…`")
    A("")

    A("## Why the two excluded items are construction defects, not model "
      "failures")
    A("")
    A("Both surfaced in the `edge_smoke_15` run, where they were scored as "
      "confident overcommitments. Reading the documents by hand showed the "
      "model was right and the items were wrong. Full detail in "
      "`HEDGEQA_FB_OVERCOMMIT_TRIAGE.md`.")
    A("")
    A("### `hqa_FB_9fc58fab_masked` — the constructed gold is wrong")
    A("")
    A("> **Q.** Has CVS Health reported any materially important ongoing legal "
      "battles from 2022, 2021 and 2020?")
    A("")
    A("Masking removed `4.3` and `625`, the opioid settlement's dollar "
      "amounts. Four paragraphs of litigation survive — *\"named as a "
      "defendant in a number of lawsuits\"*, *\"multiple lawsuits, including "
      "by state Attorneys General\"*, *\"putative class actions\"*, a "
      "settlement *\"resolving substantially all opioid claims\"*. The "
      "question asks whether such battles **exist**, and the surviving prose "
      "answers it: **yes**.")
    A("")
    A("The model answered `yes` at `p_noncommit` 0.00 and was **correct**. "
      "The gold said `insufficient_data`, so the benchmark recorded a failure "
      "that did not happen. **Not repairable by re-masking:** the answer "
      "never depended on the removed figures, so no number-deletion makes "
      "this question unanswerable while the lawsuits remain described.")
    A("")
    A("### `hqa_FB_5dbbcec0_masked` — the mask falsified the document")
    A("")
    A("> **Q.** Has MGM Resorts paid dividends to common shareholders in "
      "FY2022?")
    A("")
    A("Deleting the lines carrying `0.01` and `2022.` joined two unrelated "
      "sentences into a fluent, false one:")
    A("")
    A("> \"…pursuant to which it has paid regular quarterly dividends. **In "
      "the second quarter of 2020, we** / **in light of our current preferred "
      "method of returning value to shareholders through our share repurchase "
      "plan.** To the extent we determine to **reinstate** the dividend…\"")
    A("")
    A("The filing said MGM *reduced* the dividend to $0.01 in Q2 2020, "
      "*maintained* it through 2022, and suspended it in February **2023** — "
      "so the true answer is **yes**. The masked text now reads as a Q2-2020 "
      "suspension, reinforced by \"reinstate\" and a Q4 2022 buyback table, "
      "and asserts **no**.")
    A("")
    A("The model answered `no` at `p_noncommit` 0.00 — **the correct reading "
      "of a document we corrupted**. Masking is meant to *remove* "
      "information; here it **added** false information. **Not repairable:** "
      "undoing the splice restores a document that answers `yes`, which is "
      "not an insufficient-evidence item.")
    A("")
    A("### The distinction that matters")
    A("")
    A("A model failure is evidence about the model. A construction defect is "
      "evidence about us, and leaving it in the collection would let our own "
      "bug be reported as a hedging-failure rate. Both items are removed "
      "rather than relabelled, because a corrected label would still leave a "
      "question that number-deletion cannot mask (CVS) or a document that has "
      "been altered into saying something untrue (MGM).")
    A("")

    A("## Composition of the strict set")
    A("")
    A("### By source")
    A("")
    L.extend(table(counts(strict, lambda i: i.source_benchmark),
                   ["source", "n", "share"]))
    A("")
    A("### By transformation_type")
    A("")
    L.extend(table(counts(strict, lambda i: i.transformation_type),
                   ["transformation_type", "n", "share"]))
    A("")
    A("### By answer_type")
    A("")
    L.extend(table(counts(strict, lambda i: i.answer_type),
                   ["answer_type", "n", "share"]))
    A("")
    A("### By gold_commitment")
    A("")
    L.extend(table(counts(strict, lambda i: i.gold_commitment),
                   ["gold_commitment", "n", "share"]))
    A("")
    A("### Natural vs masked")
    A("")
    L.extend(table([
        ("natural (gold from the source benchmark)", len(nat),
         f"{len(nat) / len(strict):.1%}"),
        ("masked (constructed gold)", len(msk),
         f"{len(msk) / len(strict):.1%}"),
    ], ["family", "n", "share"]))
    A("")
    A("The masked stratum carries a **constructed** gold. It measures our "
      "masking as much as it measures a model, and the two items removed here "
      "are what that looks like when it goes wrong. Report the two families "
      "separately.")
    A("")

    A("## Remaining FinanceBench masked items")
    A("")
    A(f"**{len(fb_masked)} remain** (from 7). These are the collection's only "
      f"masked `yes_no` items — every other source's masked items are "
      f"`directional_change` over numeric tables, where number-deletion is "
      f"the right instrument.")
    A("")
    L.extend(table(
        [(f"`{i.hedgeqa_id}`", i.answer_type, i.gold_label,
          i.question[:64] + ("…" if len(i.question) > 64 else ""))
         for i in sorted(fb_masked, key=lambda x: x.hedgeqa_id)],
        ["hedgeqa_id", "answer_type", "gold", "question"]))
    A("")
    A("All five were read by hand and audited in "
      "`HEDGEQA_MASKING_CATEGORY_GATE.md` §4. They are retained; the audit "
      "records the basis for each.")
    A("")

    A("## What was NOT done")
    A("")
    A("- The 319-item file, the raw human review CSV and the raw AI review "
      "outputs are **unmodified**.")
    A("- Nothing is marked `manually_validated`. The strict set is still a "
      "reviewed candidate collection.")
    A("- No masked items were created, re-masked, or re-admitted.")
    A("- The smoke and edge manifests are **not** rebuilt here. Both were "
      "drawn from the 319 and `hqa_FB_5dbbcec0_masked` / "
      "`hqa_FB_9fc58fab_masked` are in the edge manifest, so that manifest "
      "now contains two items absent from the strict set. It is left as-is "
      "deliberately: the completed run is keyed to those ids, and silently "
      "changing the manifest would break the link to `hedgeqa_edge15_gemma4`. "
      "Any *future* edge run should rebuild from the strict file.")
    A("")
    A("## Caveat")
    A("")
    A("Two defects were found by reading four items. That is a sample, not a "
      "sweep. The masked stratum has not been re-read end to end, and the "
      "rate at which this class of defect occurs in the other 47 masked items "
      "is unknown — the category gate added in "
      "`HEDGEQA_MASKING_CATEGORY_GATE.md` prevents new ones but certifies "
      "nothing already built.")

    DOC.write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"{before} -> {n}  (excluded {len(EXCLUDE)})")
    for h, why in sorted(EXCLUDE.items()):
        print(f"  - {h}: {why}")
    print(f"financebench masked remaining: {len(fb_masked)}")
    print(f"natural {len(nat)} / masked {len(msk)}")
    print(f"wrote {DST.name} and {DOC.name}")


if __name__ == "__main__":
    main()
