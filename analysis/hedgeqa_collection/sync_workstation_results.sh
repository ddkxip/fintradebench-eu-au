#!/usr/bin/env bash
# Pull HedgeQA full-core results from the GPU workstation to this checkout.
#
#   bash analysis/hedgeqa_collection/sync_workstation_results.sh
#
# Copies ONLY runs the workstation queue produced -- the run_ids listed in its
# ledger(s) under results/queue/. An earlier version globbed every
# hedgeqa_core317_* directory on the box, which includes runs that reached the
# box via `git pull` (e.g. the laptop's gemma3:4b run) and overwrote the local
# copy with the remote one. The bytes happened to be identical, but a sync that
# can overwrite runs it did not produce is one divergent file away from
# silently destroying data.
#
# For each queued run:
#   results/<run>/rows.csv            (committed once complete)
#   results/manifests/<run>.json      (committed once complete)
#   results/raw/<run>/decodes.jsonl   (git-ignored; needed for rationale scans)
# plus results/probes/*.json and results/queue/*.json -- the evidence that
# each model passed the gate before it ran.
#
# A run still in progress is copied as-is. rows.csv is append-only and the
# analyzers flag partial runs, so an in-flight copy is safe to read but must
# not be reported as final.
set -euo pipefail
repo="$(cd "$(dirname "$0")/../.." && pwd)"

ssh -o BatchMode=yes workstation 'cd ~/fintradebench-eu-au && python3 - <<"PY"
import glob, json, os, subprocess, sys
runs = set()
for q in glob.glob("results/queue/*.json"):
    for m in json.load(open(q)).get("models", []):
        if m.get("run_id"):
            runs.add(m["run_id"])
paths = ["results/probes", "results/queue"]
for r in sorted(runs):
    for p in (f"results/{r}", f"results/raw/{r}", f"results/manifests/{r}.json"):
        if os.path.exists(p):
            paths.append(p)
sys.stdout.flush()
subprocess.run(["tar", "cf", "-", *paths], check=True)
PY' 2>/dev/null | tar xf - -C "$repo"

echo "synced queue-produced runs into $repo/results:"
python - "$repo" <<'PY'
import csv, glob, json, os, sys
repo = sys.argv[1]
for q in sorted(glob.glob(os.path.join(repo, "results", "queue", "*.json"))):
    for m in json.load(open(q, encoding="utf-8")).get("models", []):
        p = os.path.join(repo, "results", m["run_id"], "rows.csv")
        n = 0
        if os.path.exists(p):
            with open(p, encoding="utf-8", newline="") as f:
                n = len({r["question_id"] for r in csv.DictReader(f)})
        print(f"  {m['model']:24s} {m['status']:28s} {n:4d} items")
PY
