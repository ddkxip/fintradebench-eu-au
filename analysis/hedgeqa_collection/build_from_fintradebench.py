"""HedgeQA candidates from the existing FinTradeBench schemas.

Reads schemas/answer_schemas.jsonl (READ ONLY -- nothing here writes to any
existing FinTradeBench or FinanceBench file) and rebuilds the oracle evidence
pack with src.evidence, the same builder the E-A runs used.

transformation_type is "none" throughout: these questions already have a
finite answer space and a reference label, which is why they are the spine of
the collection.

Two source-specific exclusions are applied, both inherited from audits
already recorded in this repo:
  * questions whose evidence pack is empty (the 2026-08 coverage bug); these
    cannot support an oracle-evidence item at all.
  * T-lane screening questions whose reference names more than one entity
    from the answer space. Our schema collapses the set to one label, so a
    system naming another endorsed member is scored wrong -- 48.6% of T-lane
    wrong-direction errors are this artifact. They are emitted with
    gold_commitment="ambiguous_exclude" rather than dropped silently, so the
    decision stays visible and reversible.

Usage: python analysis/hedgeqa_collection/build_from_fintradebench.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from hedgeqa_schema import HedgeQAItem, make_id, write_jsonl  # noqa: E402

from src.evidence import build_pack  # noqa: E402
from src.schema import load_schemas  # noqa: E402

OUT = REPO / "data" / "hedgeqa" / "candidates" / "fintradebench_candidates.jsonl"

LANE_NAME = {"F": "fundamental", "T": "trading_signal", "FT": "cross_signal"}

# FinTradeBench records schema_confidence categorically; HedgeQA stores a
# float so confidences are comparable across source benchmarks.
CONF_MAP = {"high": 0.9, "medium": 0.6, "low": 0.3}

# References whose stated justification is contradicted by the released
# indicators (REFERENCE_QUALITY_AUDIT.md, 2026-08). The LABEL may still be
# defensible -- APP does hold the highest ROE -- so these are not excluded
# outright, but they must not present as the collection's cleanest items.
KNOWN_FALSIFIED_JUSTIFICATION = {
    "F50": ('reference justifies APP as "ROA at 14.89% (highest)" but the '
            "released table shows NVDA at 0.2131 > APP at 0.1489"),
    "T9": ('reference justifies TSLA as "OBV ... the highest among all '
           'ranked tickers" but NVDA OBV is 166.28B vs TSLA 22.96B'),
}


def _tickers_in(space):
    return [y for y in space if y.isupper() and 2 <= len(y) <= 5]


def build():
    schemas = load_schemas()
    items, stats = [], {"loaded": 0, "not_headline": 0, "empty_evidence": 0,
                        "set_collapse": 0, "included": 0}

    for s in sorted(schemas.values(), key=lambda x: x.question_id):
        stats["loaded"] += 1
        if not s.headline_eligible:
            stats["not_headline"] += 1
            continue

        cands = _tickers_in(s.answer_space)
        pack = build_pack(s.question_id, s.lane, s.question,
                          s.golden_indicators, candidate_tickers=cands)
        evidence = (pack.trading_context or "") + "\n" + \
                   (pack.fundamental_context or "")
        evidence = evidence.strip()

        nc = sorted(s.noncommit_set)
        is_nc = s.gold_label in s.noncommit_set
        commitment = "noncommitted" if is_nc else "committed"
        exclusion = None
        status = "candidate"

        if len(evidence) < 120:
            stats["empty_evidence"] += 1
            commitment = "ambiguous_exclude"
            exclusion = ("empty oracle evidence pack: no entity resolved to a "
                         "data file, so the item cannot test hedging against "
                         "present evidence")
            status = "excluded"
        else:
            # set-collapse check, T lane especially
            ev_text = s.gold_label_evidence or ""
            named = [y for y in cands
                     if re.search(r"\b" + re.escape(y) + r"\b", ev_text)]
            if len(named) > 1:
                stats["set_collapse"] += 1
                commitment = "ambiguous_exclude"
                exclusion = (f"set-valued reference: the expert answer names "
                             f"{len(named)} answer-space entities ({named}); "
                             f"collapsing to one label makes other endorsed "
                             f"members score as wrong-direction errors")
                status = "excluded"

        raw_conf = str(getattr(s, "schema_confidence", "") or "").lower()
        conf = CONF_MAP.get(raw_conf, 0.5)
        if status == "excluded":
            conf = min(conf, 0.3)

        falsified = KNOWN_FALSIFIED_JUSTIFICATION.get(s.question_id)
        if falsified:
            stats["known_falsified"] = stats.get("known_falsified", 0) + 1
            conf = min(conf, 0.35)

        items.append(HedgeQAItem(
            hedgeqa_id=make_id("fintradebench", s.question_id),
            source_benchmark="fintradebench",
            source_id=s.question_id,
            question=s.question,
            oracle_evidence=evidence,
            evidence_provenance=(
                f"src.evidence.build_pack over NASDAQ combined daily+"
                f"fundamentals; window {pack.date_start}..{pack.date_end} "
                f"({pack.date_label}); tickers={pack.tickers}"),
            answer_type=s.answer_type,
            answer_space=list(s.answer_space),
            gold_label=s.gold_label,
            noncommit_labels=nc,
            gold_commitment=commitment,
            transformation_type="none",
            requires_rag=False,
            validation_status=status,
            exclusion_reason=exclusion,
            schema_confidence=conf,
            notes=(f"lane={s.lane} ({LANE_NAME.get(s.lane, s.lane)}); "
                   f"golden_indicators={s.golden_indicators}"
                   + (f" | KNOWN ISSUE: {falsified}" if falsified else "")),
        ))
        if status == "candidate":
            stats["included"] += 1

    n = write_jsonl(items, OUT)
    print(f"[fintradebench] wrote {n} rows -> {OUT.relative_to(REPO)}")
    for k, v in stats.items():
        print(f"    {k:16s} {v}")
    return items


if __name__ == "__main__":
    build()
