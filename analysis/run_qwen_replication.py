"""qwen3:8b replication of main_pilot20 (same 16 questions, K=10/20, R0+R1).

Question: is the hedge-certainty regime (EU~0, hedge-label collapse)
a gemma4 property or shared across open-weights models?
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.runner import TAU, WORKERS, run_question
from src.schema import load_schemas

MODEL = "qwen3:8b"
RUN_ID = "qwen_repl16"
K_BY_LANE = {"F": 10, "FT": 10, "T": 20}

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
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
    print(f"resuming: {len(done)} questions done")

t0 = time.time()
for s in eligible:
    if s.question_id in done:
        continue
    k = K_BY_LANE[s.lane]
    print(f"[{s.question_id}] ({s.lane}, K={k}) ...", flush=True)
    raw_sink: list = []
    rows = run_question(s, k=k, rounds=1, raw_sink=raw_sink, model=MODEL)
    for r in rows:
        r["model"] = MODEL
    pd.DataFrame(rows).to_csv(rows_path, mode="a",
                              header=not rows_path.exists(), index=False)
    with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
        for r in raw_sink:
            f.write(json.dumps(r) + "\n")
    print(f"  done at {time.time()-t0:.0f}s "
          f"(parse: {[round(r['parse_rate'],2) for r in rows]})", flush=True)

(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "k_by_lane": K_BY_LANE, "tau": TAU,
    "workers": WORKERS, "rounds": 1,
    "questions": [s.question_id for s in eligible],
    "seconds": round(time.time() - t0, 1)}, indent=1), encoding="utf-8")
print(f"QWEN REPLICATION DONE in {time.time()-t0:.0f}s")
