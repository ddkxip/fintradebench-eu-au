"""HedgeQA candidates from FinanceBench (open-source split).

Two families are produced.

1. NATURAL YES/NO ITEMS (transformation_type="none")
   The 37 yes/no schemas already curated in
   analysis/financebench/financebench_yesno_schemas.jsonl are re-emitted with
   HedgeQA provenance. Evidence is the human-annotated `evidence_text` from
   data/financebench_open_source.jsonl -- never a retrieval result.

2. CONTROLLED-INSUFFICIENT VARIANTS
   (transformation_type="evidence_masked_insufficient")
   The same question is paired with evidence from which the lines carrying
   the decisive figures have been removed. The correct answer becomes
   "insufficient_data" BY CONSTRUCTION, giving ground-truth non-committal
   items whose provenance is explicit.

   These exist because a benchmark of settled questions can only measure
   hedge collision; it cannot measure whether a system correctly declines.
   Without them, "never hedge" is a winning strategy and the diagnostic is
   one-sided.

   Masking is conservative: a variant is emitted ONLY if every number the
   gold justification relies on is actually removed, and enough evidence
   remains that the item still reads as a real question. Items failing
   either test are skipped rather than shipped as weak masks.

   These variants are marked, id-suffixed `_masked`, and MUST be analysed
   separately -- they are constructed, not naturally occurring, so pooling
   them with natural items would inflate the non-committal base rate.

READ ONLY with respect to existing FinanceBench files; all output goes to
data/hedgeqa/candidates/.

Usage: python analysis/hedgeqa_collection/build_from_financebench.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import HedgeQAItem, make_id, write_jsonl  # noqa: E402
from masking import mask_evidence, salient_numbers  # noqa: E402

SRC = REPO / "data" / "financebench_open_source.jsonl"
YESNO = REPO / "analysis" / "financebench" / "financebench_yesno_schemas.jsonl"
OUT = REPO / "data" / "hedgeqa" / "candidates" / "financebench_candidates.jsonl"

MIN_REMAINING_CHARS = 200      # a mask that guts the evidence is not a fair item
NUM_RE = re.compile(r"-?\$?\d[\d,]*\.?\d*%?")


def _load_source():
    rows = {}
    with SRC.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            rows[r["financebench_id"]] = r
    return rows


def _evidence_text(row) -> tuple:
    """Human-annotated evidence, preferring the tight span over full page."""
    ev = row.get("evidence") or []
    if not ev:
        return "", "no annotated evidence"
    parts, prov = [], []
    for e in ev:
        t = (e.get("evidence_text") or "").strip()
        src = "evidence_text"
        if len(t) < 80:
            t = (e.get("evidence_text_full_page") or "").strip()
            src = "evidence_text_full_page"
        if t:
            parts.append(t)
            prov.append(f"{e.get('doc_name')} p.{e.get('evidence_page_num')} "
                        f"({src})")
    return "\n\n".join(parts), "; ".join(prov)


def _decisive_numbers(text: str) -> list:
    """Numbers appearing in the gold justification / answer."""
    return [m.group(0) for m in NUM_RE.finditer(text or "")
            if any(ch.isdigit() for ch in m.group(0))]


def _mask(evidence: str, numbers: list) -> tuple:
    """Drop every evidence line containing a decisive figure.

    Returns (masked_evidence, removed_lines). Line-level rather than
    token-level so the result still reads as coherent text rather than
    redacted gibberish, which would cue the model that something was done
    to the input.
    """
    if not numbers:
        return evidence, []
    norm = {n.replace("$", "").replace(",", "").rstrip("%") for n in numbers}
    norm = {n for n in norm if len(n) >= 2}       # skip trivial 1-digit hits
    if not norm:
        return evidence, []
    kept, removed = [], []
    for line in evidence.splitlines():
        flat = line.replace("$", "").replace(",", "")
        if any(n in flat for n in norm):
            removed.append(line)
        else:
            kept.append(line)
    return "\n".join(kept), removed


def build():
    src = _load_source()
    stats = {"yesno_loaded": 0, "natural_included": 0, "natural_skipped": 0,
             "masked_attempted": 0, "masked_included": 0,
             "masked_skipped_too_thin": 0}
    items = []
    skipped_detail = []

    schemas = [json.loads(l) for l in YESNO.open(encoding="utf-8") if l.strip()]
    for sc in schemas:
        stats["yesno_loaded"] += 1
        fid = sc["financebench_id"]
        row = src.get(fid)
        if row is None:
            stats["natural_skipped"] += 1
            continue
        evidence, prov = _evidence_text(row)
        if len(evidence) < 120:
            stats["natural_skipped"] += 1
            items.append(HedgeQAItem(
                hedgeqa_id=make_id("financebench", fid),
                source_benchmark="financebench", source_id=fid,
                question=sc["question"], oracle_evidence=evidence,
                evidence_provenance=prov or "none",
                answer_type=sc["answer_type"],
                answer_space=list(sc["answer_space"]),
                gold_label=sc["gold_label"],
                noncommit_labels=list(sc["noncommit_set"]),
                gold_commitment="ambiguous_exclude",
                transformation_type="none", requires_rag=False,
                validation_status="excluded",
                exclusion_reason="annotated evidence span too short to serve "
                                 "as oracle evidence",
                schema_confidence=0.3))
            continue

        nc = list(sc["noncommit_set"])
        gold = sc["gold_label"]
        items.append(HedgeQAItem(
            hedgeqa_id=make_id("financebench", fid),
            source_benchmark="financebench", source_id=fid,
            question=sc["question"], oracle_evidence=evidence,
            evidence_provenance=f"FinanceBench human annotation: {prov}",
            answer_type=sc["answer_type"],
            answer_space=list(sc["answer_space"]), gold_label=gold,
            noncommit_labels=nc,
            gold_commitment="noncommitted" if gold in nc else "committed",
            transformation_type="none", requires_rag=False,
            validation_status="candidate", exclusion_reason=None,
            schema_confidence=float(sc.get("schema_confidence", 0.7) or 0.7)
            if isinstance(sc.get("schema_confidence"), (int, float)) else 0.7,
            notes=f"company={sc.get('company')}; doc={sc.get('doc_name')}"))
        stats["natural_included"] += 1

        # ---- controlled-insufficient variant -----------------------------
        stats["masked_attempted"] += 1
        salient = salient_numbers(
            (sc.get("gold_label_evidence") or "") + " " +
            (sc.get("justification") or "") + " " + str(row.get("answer", "")))
        res = mask_evidence(evidence, salient, question=sc["question"])
        if not res["ok"]:
            r = res["reason"]
            # NOTE: every new rejection reason in masking.py needs a branch
            # here. Without one it falls through to the final `else` and is
            # silently counted as a residual-concept skip, which reads like a
            # different guard doing the work.
            key = ("masked_skip:no_salient" if "no salient" in r else
                   "masked_skip:not_grounded" if "do not appear" in r
                   or "cannot show" in r else
                   "masked_skip:nothing_removed" if "nothing was removed" in r
                   else "masked_skip:figures_survive" if "survive" in r else
                   "masked_skip:sentence_splice" if "splice" in r else
                   "masked_skip:question_category" if "not maskable" in r
                   else "masked_skip:residual_concept_rows")
            stats[key] = stats.get(key, 0) + 1
            skipped_detail.append((fid, r))
            continue
        masked_ev = res["masked"]
        removed = res["removed"]
        if len(masked_ev.strip()) < MIN_REMAINING_CHARS:
            stats["masked_skipped_too_thin"] += 1
            continue
        items.append(HedgeQAItem(
            hedgeqa_id=make_id("financebench", fid, "masked"),
            source_benchmark="financebench", source_id=fid,
            question=sc["question"], oracle_evidence=masked_ev.strip(),
            evidence_provenance=(
                f"FinanceBench human annotation with decisive lines REMOVED: "
                f"{prov}"),
            answer_type=sc["answer_type"],
            answer_space=list(sc["answer_space"]),
            gold_label="insufficient_data",
            noncommit_labels=nc,
            gold_commitment="noncommitted",
            transformation_type="evidence_masked_insufficient",
            requires_rag=False, validation_status="candidate",
            exclusion_reason=None, schema_confidence=0.6,
            original_question=sc["question"],
            derivation=(
                "Controlled-insufficient variant. Every salient figure the "
                f"gold answer relies on ({salient[:6]}) was removed by "
                "deleting the evidence lines carrying it, and a post-condition "
                "check confirmed none survives in the remaining text, so the "
                "question cannot be settled from what is left. Question text "
                "is unchanged."),
            masked_content=" ||| ".join(x.strip() for x in removed)[:4000],
            notes="CONSTRUCTED ITEM -- analyse separately from natural items; "
                  "REQUIRES MANUAL REVIEW before use"))
        stats["masked_included"] += 1

    n = write_jsonl(items, OUT)
    print(f"[financebench] wrote {n} rows -> {OUT.relative_to(REPO)}")
    for k, v in sorted(stats.items()):
        print(f"    {k:34s} {v}")
    if skipped_detail:
        print("")
        print("    why masked variants were skipped (first 6):")
        for fid, r in skipped_detail[:6]:
            print(f"      {fid}: {r[:100]}")
    return items


if __name__ == "__main__":
    build()
