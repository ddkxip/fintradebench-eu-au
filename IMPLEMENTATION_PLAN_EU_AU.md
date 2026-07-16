# IMPLEMENTATION_PLAN_EU_AU

## Repo layout

```
src/            eu_au.py (decomposition + metrics), transitions.py,
                schema.py (load/validate), evidence.py (oracle packs),
                runner.py (self-consistency debate runner, resumable),
                parsing.py (label parser hierarchy), ollama.py (client,
                parallel workers, digest pinning)
schemas/        answer_schemas.jsonl (+ validation report)
tests/          test_eu_au.py, test_transitions.py, test_schema.py,
                test_evidence.py, test_parsing.py
results/        run outputs (CSV + manifests)
analysis/       audit + analysis scripts and reports
```

## Build order (matches EXPERIMENT_PLAN phases)

1. ✅ Phase 0/1 docs + data audit.
2. src/eu_au.py + src/transitions.py + tests (no LLM). Gate: all 8
   mandated unit tests green.
3. schemas: 20 pilot (7F/7T/6FT) + src/schema.py validator +
   SCHEMA_VALIDATION.md. Gate: validation tests pass; count checks
   adjusted to pilot (20) with the 150-version parameterized.
4. src/evidence.py: port parse_date_range + build_contexts_for_ticker +
   alias index from the benchmark repo; golden-indicator alias map + test.
5. src/parsing.py: strict-JSON → regex → schema-aware fallback → manual
   flag; parser_confidence recorded; synthetic-example tests.
6. src/runner.py: Round 0 (independent; K decodes per agent, parallel
   Ollama workers with bounded concurrency ~4), Round 1 (each agent sees
   opponent's round-0 modal label + short rationale; K fresh decodes),
   resumable JSONL, manifest (model digest, K, τ, seeds, git commit).
7. Phase-4 tiny pilot: 6 q, K=5, Round 0 only → parse rate, schema
   adequacy, s/decode timing → recalibrate P5 budget.
8. Phase-5 main run (background, overnight): 150 q, K=10/20, R0+R1.
9. analysis scripts: aggregator → eu_au_natural_150.csv; summary md;
   plots (dataviz skill).

## Run hygiene

- Every runner invocation writes results/manifests/<run_id>.json with
  model digest (`ollama show`), K, τ, worker count, git commit, question
  set hash, evidence_mode.
- Raw decode texts stored under results/raw/<run_id>/ (JSONL, one line
  per decode) — parses are re-derivable offline.
- Agents receive: system role prompt + evidence pack + question +
  answer_space + JSON output contract. Never the gold response, never
  golden_indicators labels, never the schema metadata.
- Commit + push after every phase gate (repo: ddkxip/fintradebench-eu-au,
  private).
