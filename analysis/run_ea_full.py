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
args = ap.parse_args()

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
done: set[str] = set()
if rows_path.exists():
    done = set(pd.read_csv(rows_path)["question_id"].unique())
    print(f"[{args.run_id}] resuming: {len(done)}/{len(eligible)} done")

t0 = time.time()
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
}, indent=1), encoding="utf-8")
print(f"[{args.run_id}] ALL DONE in {(time.time()-t0)/3600:.1f}h")
