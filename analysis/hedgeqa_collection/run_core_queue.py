"""Run the full HedgeQA core through several models, one after another.

    python analysis/hedgeqa_collection/run_core_queue.py \
        --models qwen3.6:35b-a3b-q8_0,gemma4:latest,llama3.3:70b

Meant to live in a tmux session on the GPU workstation (`ftb-run`). One model
at a time, because the models do not all fit in 96 GB together and Ollama
would otherwise thrash evicting them.

## Per model

1. **Wait for the model to exist** on the server (pulls may still be running),
   up to --wait-minutes; skip it if it never appears.
2. **Probe it** (`probe_models.py`) and read the verdict. A model that fails
   any check -- parse rate, output truncation, empty content, prompt fits
   context -- is SKIPPED, not run. That is the gate: nothing runs for hours
   on an instrument that has not been shown to measure what it claims.
   An existing passing probe for the same digest is reused.
3. **Full run** of the strict 317 (`run_hedgeqa_debate.py`, K=10, rounds 0+1).
4. **One retry pass.** The runner resumes, so a second invocation retries only
   items that produced no parseable decodes. Items still unscored after that
   are recorded, not hidden.

A ledger is rewritten after every step to results/queue/<queue>.json, so the
state of an overnight queue can be read at any time and survives a crash.

Exit codes are the child process's own. A queue that finishes with any model
skipped or failed exits non-zero.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]

STRICT = "data/hedgeqa/hedgeqa_core_v0_1_validated_strict.jsonl"
OLLAMA = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
BASE = OLLAMA.rsplit("/api/", 1)[0]


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def safe(model):
    return model.replace(":", "_").replace("/", "_").replace(".", "_")


def server_digest(model):
    try:
        with urllib.request.urlopen(BASE + "/api/tags", timeout=30) as r:
            for m in json.loads(r.read().decode()).get("models", []):
                if m.get("name") == model:
                    return m.get("digest", "")[:12]
    except Exception:
        return None
    return None


def run(cmd, log_prefix):
    """Run a child, stream its output, return its OWN exit code."""
    print(f"[{now()}] {log_prefix} $ {' '.join(cmd)}", flush=True)
    p = subprocess.run(cmd, cwd=REPO)
    print(f"[{now()}] {log_prefix} exit={p.returncode}", flush=True)
    return p.returncode


def scored_items(run_id):
    p = REPO / "results" / run_id / "rows.csv"
    if not p.exists():
        return 0
    import csv
    with p.open(newline="", encoding="utf-8") as f:
        rd = csv.DictReader(f)
        return len({r["question_id"] for r in rd if r.get("question_id")})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", required=True)
    ap.add_argument("--queue", default="core317")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--wait-minutes", type=int, default=240)
    args = ap.parse_args()

    models = [m.strip() for m in args.models.split(",") if m.strip()]
    qdir = REPO / "results" / "queue"
    qdir.mkdir(parents=True, exist_ok=True)
    ledger_path = qdir / f"{args.queue}.json"
    ledger = {"queue": args.queue, "started": now(), "ollama_url": OLLAMA,
              "manifest": STRICT, "k": args.k, "models": []}

    def save():
        ledger["updated"] = now()
        ledger_path.write_text(json.dumps(ledger, indent=1), encoding="utf-8")

    save()
    for model in models:
        ent = {"model": model, "run_id": f"hedgeqa_core317_{safe(model)}",
               "status": "pending"}
        ledger["models"].append(ent)
        save()

        # 1. wait for the model to be present on the server
        t0 = time.time()
        dig = server_digest(model)
        while not dig and time.time() - t0 < args.wait_minutes * 60:
            ent["status"] = "waiting_for_model"
            save()
            time.sleep(60)
            dig = server_digest(model)
        if not dig:
            ent["status"] = "SKIPPED_model_absent"
            print(f"[{now()}] SKIP {model}: not on server after "
                  f"{args.wait_minutes} min", flush=True)
            save()
            continue
        ent["digest"] = dig

        # 2. probe gate (reuse a passing probe for the same digest)
        probe_file = REPO / "results" / "probes" / \
            f"{model.replace(':', '_').replace('/', '_')}.json"
        probe = None
        if probe_file.exists():
            try:
                probe = json.loads(probe_file.read_text(encoding="utf-8"))
                if probe.get("digest") != dig:
                    probe = None
            except Exception:
                probe = None
        if probe is None:
            ent["status"] = "probing"
            save()
            rc = run([sys.executable,
                      "analysis/hedgeqa_collection/probe_models.py",
                      "--model", model, "--k", str(args.k)], f"probe {model}")
            if rc != 0 or not probe_file.exists():
                ent["status"] = f"SKIPPED_probe_crashed_rc{rc}"
                save()
                continue
            probe = json.loads(probe_file.read_text(encoding="utf-8"))
        v = probe.get("verdict", {})
        checks = ("parse_ok", "no_output_truncation", "no_empty_content",
                  "prompt_fits_context")
        failed = [c for c in checks if not v.get(c)]
        ent["probe"] = {c: v.get(c) for c in checks}
        ent["probe"]["seconds_per_item"] = probe.get("seconds_per_item")
        ent["probe"]["projected_hours_317"] = probe.get("projected_hours_317")
        if failed:
            ent["status"] = "SKIPPED_probe_failed:" + ",".join(failed)
            print(f"[{now()}] SKIP {model}: probe failed {failed}", flush=True)
            save()
            continue

        # 3. full run, then 4. one retry pass for unscored items
        ent["status"] = "running"
        ent["run_started"] = now()
        save()
        cmd = [sys.executable, "analysis/hedgeqa_collection/run_hedgeqa_debate.py",
               "--manifest", STRICT, "--model", model,
               "--run-id", ent["run_id"], "--k", str(args.k)]
        rc1 = run(cmd, f"run {model}")
        ent["run_exit"] = rc1
        ent["scored_after_run"] = scored_items(ent["run_id"])
        save()
        if ent["scored_after_run"] < 317:
            ent["status"] = "retrying_unscored"
            save()
            ent["retry_exit"] = run(cmd, f"retry {model}")
        ent["scored"] = scored_items(ent["run_id"])
        ent["run_finished"] = now()
        ent["status"] = ("DONE" if ent["scored"] >= 317 else
                         f"DONE_PARTIAL_{ent['scored']}_of_317"
                         if ent["scored"] > 0 else "FAILED_no_rows")
        print(f"[{now()}] {model}: {ent['status']}", flush=True)
        save()

    ledger["finished"] = now()
    save()
    bad = [m["model"] for m in ledger["models"]
           if not m["status"].startswith("DONE")]
    print(f"[{now()}] QUEUE FINISHED. not done: {bad or 'none'}", flush=True)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
