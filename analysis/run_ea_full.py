"""E-A' full run over all headline-eligible schemas (139).

Usage: python analysis/run_ea_full.py --model gemma4:latest --run-id ea_full_gemma4
       python analysis/run_ea_full.py --model qwen3:8b --run-id ea_full_qwen3

K=10 F/FT, K=20 T (G0 rule). Rounds 0+1. Resumable per question.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.runner import TAU, WORKERS, ollama_digest, run_question
from src.schema import load_schemas

ap = argparse.ArgumentParser()
ap.add_argument("--model", required=True)
ap.add_argument("--run-id", required=True)
ap.add_argument("--k-t", type=int, default=20)
ap.add_argument("--k-f", type=int, default=10)
ap.add_argument("--only", default="",
                help="comma-separated question_ids to run (e.g. the 17 whose "
                     "evidence packs were empty before the 2026-08 alias fix)")
args = ap.parse_args()
ONLY = {q.strip() for q in args.only.split(",") if q.strip()}

K_BY_LANE = {"F": args.k_f, "FT": args.k_f, "T": args.k_t}

out_dir = REPO / "results" / args.run_id
raw_dir = REPO / "results" / "raw" / args.run_id
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)
rows_path = out_dir / "rows.csv"

schemas = load_schemas()
eligible = sorted((s for s in schemas.values() if s.headline_eligible),
                  key=lambda x: x.question_id)
if ONLY:
    eligible = [s for s in eligible if s.question_id in ONLY]
    print(f"[--only] restricted to {len(eligible)} questions: "
          f"{[s.question_id for s in eligible]}")
done: set[str] = set()
if rows_path.exists():
    # Read the done-set with the csv module, not pandas: a run that already
    # contains a ragged block (pre-fix failure-branch rows) makes
    # pd.read_csv raise ParserError, which would make the run unresumable
    # precisely when resuming matters most.
    import csv as _csv
    with rows_path.open(newline="", encoding="utf-8") as _f:
        _rd = _csv.reader(_f)
        _hdr = next(_rd, None)
        if _hdr:
            _i = _hdr.index("question_id")
            done = {r[_i] for r in _rd if len(r) > _i and r[_i]}
    print(f"[{args.run_id}] resuming: {len(done)}/{len(eligible)} done")

t0 = time.time()
failed: list[str] = []
for i, s in enumerate(eligible, 1):
    if s.question_id in done:
        continue
    k = K_BY_LANE[s.lane]
    print(f"[{args.run_id} {i}/{len(eligible)}] {s.question_id} "
          f"({s.lane}, K={k}) ...", flush=True)
    raw_sink: list = []
    try:
        rows = run_question(s, k=k, rounds=1, raw_sink=raw_sink,
                            model=args.model)
    except Exception as exc:
        print(f"  ERROR {s.question_id}: {exc} — continuing", flush=True)
        continue
    # Never write silence: a run whose decodes all failed (e.g. an
    # unsupported --model prefix returning HTTP 400) previously still wrote
    # result-shaped rows with parse_rate 0. Abort loudly instead.
    if all(float(r.get("parse_rate", 0)) == 0.0 for r in rows):
        first_err = next((x["raw_text"] for x in raw_sink
                          if str(x.get("raw_text", "")).startswith("__ERROR__")),
                         "(no __ERROR__ text captured)")
        # Nothing is written, so a later resume retries this question. A
        # systematic cause (bad --model, expired credentials) shows up as
        # every question failing in a row; a transient one self-heals.
        failed.append(s.question_id)
        print(f"  [SKIP-NO-PARSE] {s.question_id}: every decode failed to "
              f"parse. Nothing written; resume will retry.\n"
              f"    first error: {first_err[:200]}", flush=True)
        if len(failed) >= 5:
            raise SystemExit(
                f"\n[ABORT] {len(failed)} questions failed to parse "
                f"({failed[:8]}...). This looks systematic, not transient.\n"
                f"Check --model: this runner supports 'vertex:<model>' or an "
                f"Ollama model name; other prefixes go to Ollama verbatim.")
        continue
    for r in rows:
        r["model"] = args.model
    pd.DataFrame(rows).to_csv(rows_path, mode="a",
                              header=not rows_path.exists(), index=False)
    with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
        for r in raw_sink:
            f.write(json.dumps(r) + "\n")
    print(f"  done at {time.time()-t0:.0f}s", flush=True)

(man_dir / f"{args.run_id}.json").write_text(json.dumps({
    "run_id": args.run_id, "model": args.model,
    "digest": ollama_digest() if not args.model.startswith("vertex:") else "api",
    "k_by_lane": K_BY_LANE, "tau": TAU, "workers": WORKERS, "rounds": 1,
    "n_questions": len(eligible), "seconds": round(time.time() - t0, 1),
    "failed_no_parse": failed,
}, indent=1), encoding="utf-8")
print(f"[{args.run_id}] ALL DONE in {(time.time()-t0)/3600:.1f}h")
