"""Gemini 3.1 Pro subset: the same 16 pilot questions, via Vertex AI.

Tests whether model capability breaks the non-commitment attractor.
K=10 uniform (API cost control), Rounds 0+1. Resumable.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.runner import TAU, run_question
from src.schema import load_schemas

MODEL = "vertex:gemini-3.1-pro-preview"
RUN_ID = "gemini_subset16"
QIDS = ["F1", "F11", "F12", "F2", "F25", "F31", "F44",
        "FT1", "FT10", "FT12", "FT2", "FT25", "FT31",
        "T1", "T10", "T2"]
K = 10

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)
rows_path = out_dir / "rows.csv"

schemas = load_schemas()
done: set[str] = set()
if rows_path.exists():
    done = set(pd.read_csv(rows_path)["question_id"].unique())
    print(f"resuming: {len(done)} done")

t0 = time.time()
for qid in QIDS:
    if qid in done:
        continue
    s = schemas[qid]
    print(f"[gemini {qid}] ({s.lane}) ...", flush=True)
    raw_sink: list = []
    try:
        rows = run_question(s, k=K, rounds=1, raw_sink=raw_sink, model=MODEL)
    except Exception as exc:
        print(f"  ERROR {qid}: {exc} — continuing", flush=True)
        continue
    for r in rows:
        r["model"] = MODEL
    pd.DataFrame(rows).to_csv(rows_path, mode="a",
                              header=not rows_path.exists(), index=False)
    with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
        for r in raw_sink:
            f.write(json.dumps(r) + "\n")
    print(f"  done at {time.time()-t0:.0f}s", flush=True)

(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "k": K, "tau": TAU, "rounds": 1,
    "questions": QIDS, "seconds": round(time.time() - t0, 1),
}, indent=1), encoding="utf-8")
print(f"GEMINI SUBSET DONE in {time.time()-t0:.0f}s")
