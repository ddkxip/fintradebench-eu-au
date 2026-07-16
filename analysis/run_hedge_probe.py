"""Hedge-attractor probe (gemma4, Round 0, K=10).

Two arms over the 8 judgment questions (yes_no_mixed / supportive_judgment
among the headline-eligible pilot schemas):

  ARM D  directional_menu   hedge labels (mixed/conditional) removed from
                            the answer space; insufficient_data kept.
  ARM J  hedge_justified    original menu + instruction that hedge labels
                            require genuinely two-sided evidence.

Predictions:
- If hedging was surface style (menu-induced): Arm D shows confident
  directional answers; accuracy on directional-gold questions rises;
  EU stays ~0.
- If hedging was information-bearing: Arm D shows *split* decodes
  (AU/EU rise), especially on hedge-gold questions (F1, FT1, FT25, FT31),
  which is the correct behavior under a forced choice.

Hedge-gold questions are unscoreable in Arm D (gold not in menu) — their
uncertainty response IS the outcome there. evidence_mode=intervention.
"""

from __future__ import annotations

import dataclasses
import json
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import pandas as pd

from src.runner import MODEL, TAU, WORKERS, ollama_digest, run_question
from src.schema import load_schemas

JUDGMENT_QIDS = ["F1", "F11", "FT1", "FT2", "FT10", "FT12", "FT25", "FT31"]
HEDGE_LABELS = {"mixed", "conditional"}
K = 10
RUN_ID = "hedge_probe"

JUSTIFY_INSTRUCTION = (
    ' IMPORTANT: the labels "mixed" and "conditional" are reserved for '
    "evidence that genuinely cuts both ways with comparable force. If the "
    "evidence on balance leans one way, you MUST choose the directional "
    "label, even if some indicators disagree."
)

out_dir = REPO / "results" / RUN_ID
raw_dir = REPO / "results" / "raw" / RUN_ID
man_dir = REPO / "results" / "manifests"
for d in (out_dir, raw_dir, man_dir):
    d.mkdir(parents=True, exist_ok=True)
rows_path = out_dir / "rows.csv"

schemas = load_schemas()
done: set[tuple[str, str]] = set()
if rows_path.exists():
    prev = pd.read_csv(rows_path)
    done = set(zip(prev.question_id, prev.arm))
    print(f"resuming: {len(done)} (question, arm) pairs done")

t0 = time.time()
for qid in JUDGMENT_QIDS:
    base = schemas[qid]
    arms = {}
    # ARM D: directional menu
    d_space = [y for y in base.answer_space if y not in HEDGE_LABELS]
    d_aliases = {k: v for k, v in base.aliases.items() if k in d_space}
    arms["directional_menu"] = (
        dataclasses.replace(base, answer_space=d_space, aliases=d_aliases), "")
    # ARM J: original menu + justification instruction
    arms["hedge_justified"] = (base, JUSTIFY_INSTRUCTION)

    for arm, (schema, instr) in arms.items():
        if (qid, arm) in done:
            continue
        print(f"[{qid}/{arm}] space={schema.answer_space} ...", flush=True)
        raw_sink: list = []
        rows = run_question(schema, k=K, rounds=0, raw_sink=raw_sink,
                            extra_instruction=instr)
        for r in rows:
            r["arm"] = arm
            r["evidence_mode"] = "intervention"
            r["gold_label"] = base.gold_label
        df = pd.DataFrame(rows)
        df.to_csv(rows_path, mode="a", header=not rows_path.exists(), index=False)
        with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
            for r in raw_sink:
                r["arm"] = arm
                f.write(json.dumps(r) + "\n")
        print(f"  done at {time.time()-t0:.0f}s", flush=True)

(man_dir / f"{RUN_ID}.json").write_text(json.dumps({
    "run_id": RUN_ID, "model": MODEL, "digest": ollama_digest(), "k": K,
    "tau": TAU, "workers": WORKERS, "rounds": 0, "questions": JUDGMENT_QIDS,
    "arms": ["directional_menu", "hedge_justified"],
    "seconds": round(time.time() - t0, 1)}, indent=1), encoding="utf-8")
print(f"PROBE DONE in {time.time()-t0:.0f}s")
