"""Main pilot over all headline-eligible pilot schemas (16 of 20).

K=10 for F/FT, K=20 for T (G0 rule). Rounds 0+1. Resumable: skips
questions already in the output CSV. This is E-A' on the schema pilot
subset; the full-150 version runs after schemas scale up.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.runner import MODEL, TAU, WORKERS, ollama_digest, run_question
from src.schema import load_schemas

RUN_ID = "main_pilot20"
K_BY_LANE = {"F": 10, "FT": 10, "T": 20}

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)
rows_path = out_dir / "rows.csv"
raw_path = raw_dir / "decodes.jsonl"

schemas = load_schemas()
eligible = [s for s in schemas.values() if s.headline_eligible]
done: set[str] = set()
if rows_path.exists():
    done = set(pd.read_csv(rows_path)["question_id"].unique())
    print(f"resuming: {len(done)} questions already done")

t0 = time.time()
for s in sorted(eligible, key=lambda x: x.question_id):
    if s.question_id in done:
        continue
    k = K_BY_LANE[s.lane]
    print(f"[{s.question_id}] ({s.lane}, {s.answer_type}, K={k}) ...", flush=True)
    raw_sink: list = []
    rows = run_question(s, k=k, rounds=1, raw_sink=raw_sink)
    df = pd.DataFrame(rows)
    header = not rows_path.exists()
    df.to_csv(rows_path, mode="a", header=header, index=False)
    with raw_path.open("a", encoding="utf-8") as f:
        for r in raw_sink:
            f.write(json.dumps(r) + "\n")
    print(f"  done at {time.time()-t0:.0f}s "
          f"(parse rates: {[round(r['parse_rate'],2) for r in rows]})", flush=True)

(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "digest": ollama_digest(),
    "k_by_lane": K_BY_LANE, "tau": TAU, "workers": WORKERS, "rounds": 1,
    "questions": [s.question_id for s in eligible],
    "seconds": round(time.time() - t0, 1),
}, indent=1), encoding="utf-8")
print(f"\nALL DONE in {time.time()-t0:.0f}s -> {rows_path}")
