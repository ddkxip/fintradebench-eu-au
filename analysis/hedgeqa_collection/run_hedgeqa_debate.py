"""Run a HedgeQA manifest through the two-agent debate pipeline.

    python analysis/hedgeqa_collection/run_hedgeqa_debate.py \
        --manifest data/hedgeqa/hedgeqa_core_v0_1_smoke_15.jsonl \
        --model gemma4:latest --run-id hedgeqa_smoke15_gemma4

Reuses `src.runner.run_question` so the TU/AU/EU decomposition, the
self-consistency sampling and the round-0/round-1 debate are identical to the
FinTradeBench runs. Only the adapter below is new.

## Why an adapter is needed

`run_question` expects an `AnswerSchema` and builds an oracle pack from the
NASDAQ tables. A HedgeQA item already carries its evidence, and its answer
space came from a different source benchmark, so both are supplied directly
and `build_pack` is bypassed.

## The empty-context trap

`USER_TEMPLATE` renders two labelled sections, "Trading Signals Context" and
"Fundamental Data Context". A HedgeQA item ships ONE evidence document. Left
alone, the trading slot would render empty:

    Trading Signals Context:

    Fundamental Data Context:
    ...

A model reading an empty evidence section can reasonably conclude evidence is
missing and answer `insufficient_data` -- which would inflate the hedging rate
this run exists to measure, and the inflation would look exactly like a
finding. The adapter therefore puts an explicit one-line statement in the
trading slot saying the item ships a single combined document, rather than
leaving it blank or duplicating several kilobytes of filing text.

Nothing is written back to the manifest or to any collection file.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import pandas as pd  # noqa: E402

from hedgeqa_schema import read_jsonl  # noqa: E402
from src.evidence import EvidencePack  # noqa: E402
from src.runner import TAU, WORKERS, ollama_digest, run_question  # noqa: E402
from src.schema import AnswerSchema  # noqa: E402

SINGLE_DOC_NOTE = ("This item ships a single combined evidence document, "
                   "reproduced in full below under Fundamental Data Context. "
                   "There is no separate trading-signal extract for it; that "
                   "is a property of this item's source, not a gap in the "
                   "evidence.")


def lane_of(item) -> str:
    """FinTradeBench items record their lane in notes; others default to F."""
    n = item.notes or ""
    if "lane=" in n:
        lane = n.split("lane=")[1].split(" ")[0].strip()
        if lane in ("F", "T", "FT"):
            return lane
    return "F"


def to_schema(item) -> AnswerSchema:
    return AnswerSchema(
        question_id=item.hedgeqa_id,
        lane=lane_of(item),
        question=item.question,
        golden_indicators="",           # unused: build_pack is bypassed
        answer_type=item.answer_type,
        answer_space=list(item.answer_space),
        gold_label=item.gold_label,
        gold_label_evidence="",
        canonical_claim="",
        aliases={},
        label_parse_rules="",
        ambiguity_notes="",
        schema_confidence=str(item.schema_confidence),
        noncommit_labels=list(item.noncommit_labels),
    )


def to_pack(item) -> EvidencePack:
    return EvidencePack(
        question_id=item.hedgeqa_id,
        lane=lane_of(item),
        question=item.question,
        golden_indicators="",
        indicator_values={},
        trading_context=SINGLE_DOC_NOTE,
        fundamental_context=item.oracle_evidence,
        date_start="", date_end="", date_label="hedgeqa",
        tickers=[],
        evidence_mode="hedgeqa_oracle",
        coverage_incomplete=False,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--model", default="gemma4:latest")
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()

    items = read_jsonl(REPO / args.manifest)
    if not items:
        raise SystemExit(f"no items in {args.manifest}")

    out_dir = REPO / "results" / args.run_id
    raw_dir = REPO / "results" / "raw" / args.run_id
    man_dir = REPO / "results" / "manifests"
    for d in (out_dir, raw_dir, man_dir):
        d.mkdir(parents=True, exist_ok=True)
    rows_path = out_dir / "rows.csv"

    done = set()
    if rows_path.exists():
        import csv as _csv
        with rows_path.open(newline="", encoding="utf-8") as f:
            rd = _csv.reader(f)
            hdr = next(rd, None)
            if hdr:
                i = hdr.index("question_id")
                done = {r[i] for r in rd if len(r) > i and r[i]}
        print(f"[{args.run_id}] resuming: {len(done)}/{len(items)} done")

    t0, failed = time.time(), []
    for n, item in enumerate(items, 1):
        if item.hedgeqa_id in done:
            continue
        print(f"[{args.run_id} {n}/{len(items)}] {item.hedgeqa_id} "
              f"({item.source_benchmark}, {item.transformation_type}, "
              f"K={args.k}) ...", flush=True)
        raw_sink: list = []
        try:
            rows = run_question(to_schema(item), k=args.k, rounds=1,
                                raw_sink=raw_sink, model=args.model,
                                pack=to_pack(item))
        except Exception as exc:
            print(f"  ERROR {item.hedgeqa_id}: {exc} — continuing", flush=True)
            failed.append(item.hedgeqa_id)
            continue

        if all(float(r.get("parse_rate", 0)) == 0.0 for r in rows):
            first = next((x["raw_text"] for x in raw_sink
                          if str(x.get("raw_text", "")).startswith("__ERROR__")),
                         "(no __ERROR__ captured)")
            failed.append(item.hedgeqa_id)
            print(f"  [SKIP-NO-PARSE] nothing written; resume will retry.\n"
                  f"    {first[:160]}", flush=True)
            if len(failed) >= 5:
                raise SystemExit(f"[ABORT] {len(failed)} questions failed to "
                                 f"parse — looks systematic, not transient.")
            continue

        for r in rows:
            r["model"] = args.model
            r["source_benchmark"] = item.source_benchmark
            r["hedgeqa_transformation"] = item.transformation_type
            r["gold_commitment"] = item.gold_commitment
        pd.DataFrame(rows).to_csv(rows_path, mode="a",
                                  header=not rows_path.exists(), index=False)
        with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
            for r in raw_sink:
                f.write(json.dumps(r) + "\n")
        print(f"  done at {time.time() - t0:.0f}s", flush=True)

    (man_dir / f"{args.run_id}.json").write_text(json.dumps({
        "run_id": args.run_id, "model": args.model,
        "manifest": args.manifest, "n_items": len(items),
        "k": args.k, "tau": TAU, "workers": WORKERS, "rounds": 1,
        "evidence_mode": "hedgeqa_oracle",
        "digest": ollama_digest(args.model)
        if not args.model.startswith("vertex:") else "api",
        "failed_no_parse": failed,
        "seconds": round(time.time() - t0, 1),
    }, indent=1), encoding="utf-8")
    print(f"[{args.run_id}] DONE in {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
