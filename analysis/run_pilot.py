"""Phase-4 tiny pilot: 6 questions (2/lane), K=5, Round 0 only.

Purpose: parse rate, schema adequacy, timing. Never cite in the paper.
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

PILOT_QIDS = ["F11", "F12", "T2", "T10", "FT2", "FT12"]
K = 5
RUN_ID = "pilot_6q"

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)

schemas = load_schemas()
raw_sink: list = []
rows: list = []
t0 = time.time()
for qid in PILOT_QIDS:
    s = schemas[qid]
    print(f"[{qid}] ({s.lane}, {s.answer_type}) ...", flush=True)
    rows.extend(run_question(s, k=K, rounds=0, raw_sink=raw_sink))
    print(f"  done at {time.time()-t0:.0f}s", flush=True)

pd.DataFrame(rows).to_csv(out_dir / "rows.csv", index=False)
(raw_dir / "decodes.jsonl").write_text(
    "\n".join(json.dumps(r) for r in raw_sink), encoding="utf-8")
(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "digest": ollama_digest(),
    "k": K, "tau": TAU, "workers": WORKERS, "rounds": 0,
    "questions": PILOT_QIDS, "seconds": round(time.time() - t0, 1),
    "n_decodes": len(raw_sink),
}, indent=1), encoding="utf-8")

df = pd.DataFrame(rows)
cols = ["question_id", "lane", "parse_rate", "eu_norm", "au_norm", "tu_norm",
        "gold_prob", "predicted", "correct"]
print(df[[c for c in cols if c in df.columns]].to_string(index=False))
print(f"\ntotal {time.time()-t0:.0f}s for {len(raw_sink)} decodes "
      f"({(time.time()-t0)/max(len(raw_sink),1):.1f} s/decode)")
