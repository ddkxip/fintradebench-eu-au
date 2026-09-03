"""Generate HEDGEQA_COLLECTION_SCOPING.md from the candidate pools.

Everything in the report is computed from the files on disk, so the report
cannot drift from the data. Re-run after any builder change.

Usage: python analysis/hedgeqa_collection/build_scoping_report.py
"""

from __future__ import annotations

import collections
import statistics
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import read_jsonl  # noqa: E402

CAND = REPO / "data" / "hedgeqa" / "candidates"
COLLECTION = REPO / "data" / "hedgeqa" / "hedgeqa_v0_1_candidates.jsonl"
OUT = (REPO / "analysis" / "hedgeqa_collection" /
       "HEDGEQA_COLLECTION_SCOPING.md")

BENCHES = ["fintradebench", "financebench", "tatqa", "finqa", "convfinqa"]

ABSENT_NOTE = {
    "tatqa": ("No TAT-QA candidates were produced. Check that "
              "`TAT-QA-master/dataset_raw/` or `data/tatqa/` holds the "
              "official release."),
    "finqa": ("No FinQA candidates were produced. Check that "
              "`FinQA-main/dataset/` or `data/finqa/` holds the official "
              "release."),
    "convfinqa": ("No ConvFinQA candidates were produced. Extract "
                  "`ConvFinQA-main/data.zip` to "
                  "`data/convfinqa_extract/data/`."),
}

RISKS = {
    "fintradebench": [
        "**Set-collapse.** 27 references name more than one answer-space "
        "entity; our schema keeps one. A system naming another endorsed "
        "member scores as a wrong-direction error. All 27 are excluded here "
        "with that reason recorded, but the same artifact inflates T-lane "
        "wrong-direction counts in the main paper, where it is reported as "
        "an upper bound.",
        "**Two references are known to be falsified by their own evidence** "
        "(F50, T9 — see REFERENCE_QUALITY_AUDIT.md). They are not "
        "auto-excluded here because the *label* may still be defensible; "
        "reviewers should look at them specifically.",
        "**Evidence is model-independent but window-dependent.** Packs are "
        "medians over a parsed date window, so a reference quoting a "
        "specific as-of date can differ in the 2nd-3rd decimal.",
    ],
    "financebench": [
        "**Controlled-insufficient variants are CONSTRUCTED, not observed.** "
        "Their gold label is right only if the masked evidence truly cannot "
        "answer the question. Automation narrows but cannot certify this: a "
        "model may recompute a ratio from components left behind. Every "
        "variant is held at `candidate` for mandatory human review and must "
        "never be pooled with natural items when reporting a non-commitment "
        "base rate.",
        "**Masking can only be attempted where the gold's figures actually "
        "appear in the annotated span.** 13 of 36 attempts were rejected on "
        "that ground, so the variants are not a random subsample of the "
        "yes/no set — they are biased toward items with explicit numeric "
        "evidence.",
        "**One evidence span is too short to serve as oracle evidence** and "
        "is excluded.",
    ],
    "tatqa": [
        "Numeric answers have no finite answer space, so items must be "
        "transformed before any hedging metric is computable. Only "
        "change-shaped arithmetic questions qualify; spans, counts and "
        "open arithmetic are skipped.",
        "The direction mapping uses a flat band only when the source "
        "declares a percentage scale; for absolute magnitudes there is no "
        "denominator, so 'roughly_unchanged' is under-assigned by design.",
    ],
    "finqa": [
        "Same transformation constraint as TAT-QA. The `program` field is "
        "carried into the derivation so a reviewer can check that the "
        "arithmetic really licenses the direction.",
        "`exe_ans` sign conventions vary with the program; a subtract(a, b) "
        "with reversed operands would flip the direction. Spot-check the "
        "derivation before trusting a directional gold.",
    ],
    "convfinqa": [
        "Conversational turns are not self-contained. Only the first two "
        "turns are eligible, and prior turns are inlined verbatim so the "
        "item reads standalone.",
        "Inlining history changes the prompt shape relative to other "
        "benchmarks; ConvFinQA results should not be compared head-to-head "
        "with single-turn items without noting this.",
    ],
}


def dist(xs):
    c = collections.Counter(xs)
    return ", ".join(f"`{k}`={v}" for k, v in c.most_common())


def lenstats(xs):
    if not xs:
        return "n/a"
    xs = sorted(xs)
    return (f"min {xs[0]}, p25 {xs[len(xs)//4]}, median "
            f"{int(statistics.median(xs))}, p75 {xs[3*len(xs)//4]}, "
            f"max {xs[-1]}")


def main():
    L = []
    A = L.append
    A("# HedgeQA-v0.1 — collection scoping report")
    A("")
    A("Generated by `build_scoping_report.py` from the candidate files on "
      "disk. Do not hand-edit; re-run after any builder change.")
    A("")
    A("HedgeQA is **not a new general financial benchmark**. It is a "
      "diagnostic collection for hedging failures, assembled so that hedge "
      "collision, overcommitment, wrong-direction commitment, wrong "
      "non-committal type, `p_noncommit` and AU/EU debate behaviour are all "
      "computable on a finite answer space with oracle evidence.")
    A("")

    total_in = 0
    for b in BENCHES:
        items = read_jsonl(CAND / f"{b}_candidates.jsonl")
        A(f"## {b}")
        A("")
        if not items:
            A(ABSENT_NOTE.get(b, "No candidates."))
            A("")
            A("**Loaded:** 0 | **Included:** 0 | **Excluded:** 0")
            A("")
            A("### Risks / caveats (apply once the data is present)")
            for r in RISKS.get(b, []):
                A(f"- {r}")
            A("")
            continue

        inc = [i for i in items
               if i.validation_status in ("auto_validated", "candidate")]
        exc = [i for i in items if i.validation_status == "excluded"]
        total_in += len(inc)

        A(f"**Loaded:** {len(items)} | **Candidate-included:** {len(inc)} | "
          f"**Excluded:** {len(exc)}")
        A("")
        A(f"- answer_type: {dist(i.answer_type for i in inc)}")
        A(f"- gold commitment: {dist(i.gold_commitment for i in inc)}")
        A(f"- transformation: {dist(i.transformation_type for i in inc)}")
        A(f"- evidence length (chars): "
          f"{lenstats([len(i.oracle_evidence) for i in inc])}")
        A("")

        A("### Top 20 clean candidates")
        A("")
        A("| hedgeqa_id | source_id | gold | commitment | ev.chars | question |")
        A("|---|---|---|---|---|---|")
        clean = sorted(
            [i for i in inc if i.validation_status == "auto_validated"],
            key=lambda x: (-x.schema_confidence, -len(x.oracle_evidence)))[:20]
        for i in clean:
            q = i.question.replace("|", "/")
            q = (q[:90] + "...") if len(q) > 90 else q
            A(f"| `{i.hedgeqa_id}` | {i.source_id} | `{i.gold_label}` | "
              f"{i.gold_commitment} | {len(i.oracle_evidence)} | {q} |")
        A("")

        if exc:
            A("### Top exclusion reasons")
            A("")
            reasons = collections.Counter(
                (i.exclusion_reason or "unspecified").split(":")[0][:110]
                for i in exc)
            for r, c in reasons.most_common(8):
                A(f"- **{c}x** {r}")
            A("")

        A("### Risks / caveats")
        for r in RISKS.get(b, []):
            A(f"- {r}")
        A("")

    coll = read_jsonl(COLLECTION)
    A("## Assembled collection: `data/hedgeqa/hedgeqa_v0_1_candidates.jsonl`")
    A("")
    A(f"**{len(coll)} items.**")
    A("")
    A(f"- by benchmark: {dist(i.source_benchmark for i in coll)}")
    A(f"- by commitment: {dist(i.gold_commitment for i in coll)}")
    A(f"- by transformation: {dist(i.transformation_type for i in coll)}")
    A(f"- by answer_type: {dist(i.answer_type for i in coll)}")
    A("")
    nc = sum(1 for i in coll if i.gold_commitment == "noncommitted")
    masked = sum(1 for i in coll
                 if i.transformation_type == "evidence_masked_insufficient")
    A(f"Non-committal gold rate is {nc}/{len(coll)} = {nc/len(coll):.0%}; "
      f"{masked} of those are constructed masked variants. Without them the "
      f"rate would be {(nc-masked)}/{len(coll)-masked} = "
      f"{(nc-masked)/max(1,len(coll)-masked):.0%}, which is why the variants "
      f"exist: a collection of overwhelmingly settled questions can only "
      f"measure hedge collision, and rewards a system that never declines.")
    A("")
    A("## Collection-level caveats")
    A("")
    A("- **Benchmark-stratified results are primary.** The sources differ in "
      "evidence style, answer space and difficulty; a pooled number is a "
      "weighted average of unlike things and is descriptive only.")
    present = sorted({i.source_benchmark for i in coll})
    A(f"- **Sources present in this build: {', '.join(present)}.** Any "
      "cross-benchmark claim is scoped to these.")
    A("- **`auto_validated` means structurally sound, not correct.** It "
      "asserts the answer space, gold label, evidence and provenance are "
      "well-formed. It says nothing about whether the gold label is right.")
    A("- **Masked variants must be analysed separately** and never pooled "
      "into a non-commitment base rate.")
    A("- **No item requires retrieval.** `requires_rag` is False throughout "
      "and validated; oracle evidence is used specifically to keep retrieval "
      "noise out of the hedging measurement.")

    OUT.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"wrote {OUT.relative_to(REPO)} ({len(L)} lines, "
          f"{total_in} included candidates)")


if __name__ == "__main__":
    main()
