"""Merge the core sheet, the human review, and both AI reviews.

Reads:
  data/hedgeqa/hedgeqa_core_v0_1_candidates.jsonl        (pipeline labels)
  analysis/hedgeqa_collection/hedgeqa_core_v0_1_manual_review.csv  (human)
  analysis/hedgeqa_collection/ai_review/responses/*.jsonl (AI reviewers)

Writes:
  analysis/hedgeqa_collection/ai_review/hedgeqa_core_review_merged.csv

Nothing is overwritten: the core JSONL and the human sheet are read-only
here, and no `validation_status` is changed anywhere.

## Promotion classes

Assigned per item, and they are ROUTING LABELS, not promotions:

  strong_keep    human keep AND both AI keep AND all three agree on
                 gold_commitment AND all three agree on gold_label.
                 Eligible for a human to promote later.

                 NOTE -- the label-agreement clause is a DELIBERATE
                 STRENGTHENING of the specified rule, which required only
                 commitment agreement. Without it, two reviewers can choose
                 contradictory labels ("yes" vs "no", both of them
                 "committed") and the item is still promoted, which defeats
                 the point of collecting independent labels. A smoke test
                 caught this; see test_ai_review_pipeline.py.
  review_needed  any disagreement, any missing reviewer, any low-confidence
                 keep, or any unclear flag.
  exclude        human excluded, OR both AI reviewers excluded.

A human decides promotion. `strong_keep` means "nobody objected", which is
weaker than "verified" -- three readers can share a blind spot, and two of
the three are language models with correlated failure modes. Nothing here
sets `manually_validated`.

Missing inputs degrade gracefully: absent AI files leave blank columns and
push items to `review_needed` rather than silently counting as agreement.

Usage: python analysis/hedgeqa_collection/ai_review/merge_ai_reviews.py
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE.parent))

from hedgeqa_schema import read_jsonl  # noqa: E402

CORE = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_candidates.jsonl"
# Prefer the reviewer's exported completed sheet; fall back to the blank
# template only when no review has been exported yet. Resolving this here
# rather than requiring a manual edit avoids the failure mode where the
# merge silently runs against the empty template and reports every item as
# "human review not recorded".
_COMPLETED = HERE.parent / "hedgeqa_core_v0_1_manual_review_completed.csv"
_TEMPLATE = HERE.parent / "hedgeqa_core_v0_1_manual_review.csv"
HUMAN = _COMPLETED if _COMPLETED.exists() else _TEMPLATE
RESPONSES = HERE / "responses"
OUT = HERE / "hedgeqa_core_review_merged.csv"

REVIEWERS = ["gemini_antigravity", "chatgpt_codex"]
AI_FIELDS = ["reviewer_gold_label", "reviewer_gold_commitment",
             "evidence_sufficient_for_gold", "transformation_valid",
             "masked_variant_valid", "keep_or_exclude", "exclusion_reason",
             "confidence", "rationale_short", "flags"]


def load_ai():
    """reviewer -> {hedgeqa_id: record}. Reports malformed lines loudly."""
    out = {r: {} for r in REVIEWERS}
    problems = []
    if not RESPONSES.exists():
        return out, ["responses/ directory does not exist"]
    for p in sorted(RESPONSES.glob("*.jsonl")):
        who = p.name.split("__")[0]
        if who not in REVIEWERS:
            problems.append(f"{p.name}: unknown reviewer prefix {who!r}")
            continue
        for n, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            line = line.strip()
            if not line:
                continue
            try:
                d = json.loads(line)
            except json.JSONDecodeError as e:
                problems.append(f"{p.name}:{n}: not JSON ({e})")
                continue
            hid = d.get("hedgeqa_id")
            if not hid:
                problems.append(f"{p.name}:{n}: missing hedgeqa_id")
                continue
            if d.get("reviewer_name") and d["reviewer_name"] != who:
                problems.append(
                    f"{p.name}:{n}: reviewer_name {d['reviewer_name']!r} "
                    f"does not match filename prefix {who!r}")
            if hid in out[who]:
                problems.append(f"{p.name}:{n}: duplicate record for {hid}")
            out[who][hid] = d
    return out, problems


def load_human():
    if not HUMAN.exists():
        return {}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        return {r["hedgeqa_id"]: r for r in csv.DictReader(f)}


def _norm(v):
    return (str(v).strip().lower() if v is not None else "")


def classify(human, ai_recs):
    """-> (promotion_class, reason)."""
    h_keep = _norm(human.get("keep_or_exclude"))
    h_commit = _norm(human.get("reviewer_gold_commitment"))
    present = [r for r in REVIEWERS if ai_recs.get(r)]

    if h_keep == "exclude":
        return "exclude", "human excluded"
    if len(present) == 2 and all(
            _norm(ai_recs[r].get("keep_or_exclude")) == "exclude"
            for r in present):
        return "exclude", "both AI reviewers excluded"

    if not h_keep:
        return "review_needed", "human review not recorded"
    if len(present) < 2:
        missing = [r for r in REVIEWERS if r not in present]
        return "review_needed", f"missing AI review: {', '.join(missing)}"

    if any(_norm(ai_recs[r].get("keep_or_exclude")) != "keep"
           for r in present):
        return "review_needed", "an AI reviewer excluded"
    if h_keep != "keep":
        return "review_needed", f"human keep_or_exclude = {h_keep!r}"

    commits = {h_commit} | {_norm(ai_recs[r].get("reviewer_gold_commitment"))
                            for r in present}
    commits.discard("")
    if len(commits) > 1:
        return "review_needed", f"gold_commitment disagreement: {sorted(commits)}"
    if not h_commit:
        return "review_needed", "human gold_commitment blank"

    # Label agreement. Not in the original rule, added because commitment
    # agreement alone lets contradictory labels through: "yes" and "no" are
    # both committed, so an item nobody actually agreed on would promote.
    labels = {_norm(human.get("reviewer_gold_label"))} | {
        _norm(ai_recs[r].get("reviewer_gold_label")) for r in present}
    labels.discard("")
    if len(labels) > 1:
        return "review_needed", f"gold_label disagreement: {sorted(labels)}"
    if not _norm(human.get("reviewer_gold_label")):
        return "review_needed", "human gold_label blank"

    if any(_norm(ai_recs[r].get("confidence")) == "low" for r in present):
        return "review_needed", "an AI reviewer kept with low confidence"
    if any(_norm(ai_recs[r].get(f)) == "unclear"
           for r in present
           for f in ("evidence_sufficient_for_gold", "transformation_valid",
                     "masked_variant_valid")):
        return "review_needed", "an AI reviewer flagged 'unclear'"

    return "strong_keep", ("human and both AI reviewers keep; label and "
                           "commitment agree")


def main():
    core = {i.hedgeqa_id: i for i in read_jsonl(CORE)}
    human = load_human()
    ai, problems = load_ai()

    cols = (["hedgeqa_id", "source_benchmark", "source_id",
             "transformation_type", "answer_type", "question",
             "pipeline_gold_label", "pipeline_gold_commitment",
             "pipeline_validation_status",
             "human_gold_label", "human_gold_commitment",
             "human_evidence_sufficient", "human_transformation_valid",
             "human_masked_variant_valid", "human_keep_or_exclude",
             "human_exclusion_reason", "human_notes"]
            + [f"{r}__{f}" for r in REVIEWERS for f in AI_FIELDS]
            + ["promotion_class", "promotion_reason"])

    counts = {"strong_keep": 0, "review_needed": 0, "exclude": 0}
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for hid, it in sorted(core.items()):
            h = human.get(hid, {})
            recs = {r: ai[r].get(hid) for r in REVIEWERS}
            cls, why = classify(h, recs)
            counts[cls] += 1
            row = [hid, it.source_benchmark, it.source_id,
                   it.transformation_type, it.answer_type, it.question,
                   it.gold_label, it.gold_commitment, it.validation_status,
                   h.get("reviewer_gold_label", ""),
                   h.get("reviewer_gold_commitment", ""),
                   h.get("evidence_sufficient_for_gold", ""),
                   h.get("transformation_valid", ""),
                   h.get("masked_variant_valid", ""),
                   h.get("keep_or_exclude", ""),
                   h.get("exclusion_reason", ""), h.get("notes", "")]
            for r in REVIEWERS:
                d = recs.get(r) or {}
                for fld in AI_FIELDS:
                    v = d.get(fld, "")
                    row.append("|".join(v) if isinstance(v, list) else v)
            row += [cls, why]
            w.writerow(row)

    print(f"merged {len(core)} items -> {OUT.relative_to(REPO)}")
    print(f"  human sheet           : {HUMAN.name}")
    n_dec = sum(1 for r in human.values()
                if (r.get("keep_or_exclude") or "").strip())
    print(f"  human rows found      : {len(human)} "
          f"({n_dec} with a keep/exclude decision)")
    for r in REVIEWERS:
        print(f"  {r:22s}: {len(ai[r])} records")
    print("\npromotion classes (routing only — no item is promoted here):")
    for k in ("strong_keep", "review_needed", "exclude"):
        print(f"  {k:14s} {counts[k]:4d}")
    if problems:
        print(f"\n{len(problems)} INPUT PROBLEM(S):")
        for p in problems[:15]:
            print(f"  - {p}")
    print("\nNothing was marked manually_validated. Promotion is a separate, "
          "human-controlled step.")
    return counts


if __name__ == "__main__":
    main()
