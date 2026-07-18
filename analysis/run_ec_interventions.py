"""E-C' source-intervention run (gemma4, Round 0).

Five elicitation passes over a 30-question F/FT subset (15 F + 15 FT,
K=10 — matched to the ea_full_gemma4 baseline for paired comparison):

  remove_top      strip the top PRESENT golden indicator (evidence-sufficiency)
  remove_placebo  strip a matched non-golden indicator (specificity control)
  inject_conflict coherently oppose trading vs fundamental lean (do-conflict)
  horizon_short   append "next 3 months"; evidence fixed
  horizon_long    append "next 5 years"; evidence fixed

Control arm = stored baseline (results/ea_full_gemma4, round 0). Only the
intervened arms are run here. T-lane excluded by design: single-indicator
screenings are not a substrate for top-indicator removal or F/T conflict.
Resumable per (question, arm).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import dataclasses

import pandas as pd

from src.evidence import build_pack
from src.interventions import (horizon_rewrite, inject_ft_conflict,
                               remove_placebo, remove_top_indicator)
from src.runner import MODEL, TAU, ollama_digest, run_question
from src.schema import load_schemas

RUN_ID = "ec_interventions_gemma4"
K = 10
N_PER_LANE = 15

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)
rows_path = out_dir / "rows.csv"

schemas = load_schemas()
subset = []
for lane in ("F", "FT"):
    picks = [s for s in sorted(schemas.values(), key=lambda x: x.question_id)
             if s.lane == lane and s.headline_eligible][:N_PER_LANE]
    subset += picks

done: set[tuple[str, str]] = set()
if rows_path.exists():
    prev = pd.read_csv(rows_path)
    done = set(zip(prev.question_id, prev.intervention.fillna("")))
    print(f"resuming: {len(done)} (question, arm) pairs done")


def emit(schema, pack, arm, raw_sink):
    rows = run_question(schema, k=K, rounds=0, raw_sink=raw_sink,
                        model=MODEL, pack=pack, intervention=arm)
    for r in rows:
        r["arm"] = arm
    return rows


t0 = time.time()
for s in subset:
    cands = [y for y in s.answer_space if y.isupper() and 2 <= len(y) <= 5]
    base = build_pack(s.question_id, s.lane, s.question,
                      s.golden_indicators, candidate_tickers=cands)

    rt_pack, rt_desc = remove_top_indicator(base, s.golden_indicators)
    rp_pack, rp_desc = remove_placebo(base, s.golden_indicators)
    ic_pack, ic_desc = inject_ft_conflict(base)

    arms = [
        ("remove_top", rt_pack, s, rt_desc),
        ("remove_placebo", rp_pack, s, rp_desc),
        ("inject_conflict", ic_pack, s, ic_desc),
        ("horizon_short", base,
         dataclasses.replace(s, question=horizon_rewrite(s.question, "short")),
         "horizon_short"),
        ("horizon_long", base,
         dataclasses.replace(s, question=horizon_rewrite(s.question, "long")),
         "horizon_long"),
    ]
    for arm, pack, sch, desc in arms:
        if (s.question_id, arm) in done:
            continue
        print(f"[{s.question_id}/{arm}] {desc} ...", flush=True)
        raw_sink: list = []
        rows = emit(sch, pack, arm, raw_sink)
        for r in rows:
            r["intervention_desc"] = desc
        pd.DataFrame(rows).to_csv(rows_path, mode="a",
                                  header=not rows_path.exists(), index=False)
        with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
            for r in raw_sink:
                r["arm"] = arm
                f.write(json.dumps(r) + "\n")
        print(f"  done at {time.time()-t0:.0f}s", flush=True)

(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "digest": ollama_digest(), "k": K,
    "tau": TAU, "rounds": 0, "n_questions": len(subset),
    "arms": ["remove_top", "remove_placebo", "inject_conflict",
             "horizon_short", "horizon_long"],
    "control": "ea_full_gemma4 round 0",
    "seconds": round(time.time() - t0, 1)}, indent=1), encoding="utf-8")
print(f"E-C' DONE in {(time.time()-t0)/3600:.1f}h")
