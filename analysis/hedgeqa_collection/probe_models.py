"""Probe a model before committing hours of GPU to a full-core run.

    python analysis/hedgeqa_collection/probe_models.py --model llama3.3:70b

Runs the REAL pipeline (`run_question`, K=10, rounds 0+1) on the two items
with the largest evidence documents, with `src.runner.chat` wrapped so every
call records what the server reports rather than only the content string.

## What a probe must catch, and why each is silent otherwise

* **Prompt truncation.** When a prompt exceeds the server's context window,
  Ollama truncates it from the FRONT -- the system prompt and early evidence
  go first -- and returns a normal-looking answer. Nothing errors. The run
  would score a model on documents it never saw. Detected by comparing the
  server's `prompt_eval_count` with the loaded `context_length`.

* **Output truncation / reasoning leakage.** The runner sends `think: False`,
  which some reasoning models (gpt-oss) do not honour. Reasoning tokens can
  exhaust the output budget and leave empty or cut-off JSON. Detected via
  `done_reason` ("length" means the output was cut) and parse rate.

* **Label surface forms.** gemma3:4b lost an item by answering "unchanged"
  where the space says "roughly_unchanged". The largest-evidence item is that
  exact item, so the probe checks whether a model repeats it.

* **Throughput.** Seconds per item at the real K and round count, so a
  317-item projection is measured rather than guessed.

Writes results/probes/<model>.json. Nothing touches any run directory.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

import src.runner as R  # noqa: E402
from hedgeqa_schema import read_jsonl  # noqa: E402
from run_hedgeqa_debate import to_pack, to_schema  # noqa: E402

STRICT = REPO / "data" / "hedgeqa" / "hedgeqa_core_v0_1_validated_strict.jsonl"

CALLS: list[dict] = []


def _base():
    return R.OLLAMA.rsplit("/api/", 1)[0]


def instrumented_chat(system, user, temperature=R.TAU, timeout=300,
                      model=R.MODEL):
    """Same request as src.runner.chat, but keeps the server's metadata."""
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False, "format": "json", "think": False,
        "options": {"temperature": float(temperature)},
    }
    req = urllib.request.Request(R.OLLAMA, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as r:
        body = json.loads(r.read().decode())
    msg = body.get("message", {}) or {}
    CALLS.append({
        "prompt_eval_count": body.get("prompt_eval_count"),
        "eval_count": body.get("eval_count"),
        "done_reason": body.get("done_reason"),
        "wall_s": round(time.time() - t, 2),
        "content_chars": len(msg.get("content") or ""),
        "control_chars_in_content": sum(
            1 for ch in (msg.get("content") or "")
            if ord(ch) < 32 and ch not in "\n\r\t"),
        "raw_head": (msg.get("content") or "")[:160],
        "thinking_chars": len(msg.get("thinking") or ""),
        "prompt_chars": len(system) + len(user),
    })
    return msg.get("content", "")


def _label_of(raw):
    """Best-effort label, for REPORTING only -- never used for scoring.

    The first gpt-oss:120b probe crashed here: its output carried a literal
    control character inside a JSON string, which strict json.loads rejects.
    A diagnostic must not die on the very quirk it exists to surface, so this
    is lenient and records unparseable output instead of raising. Whether the
    RUNNER accepts such output is a separate question, answered by
    parse_rate_by_round, which comes from the runner's own parser.
    """
    if not raw.lstrip().startswith("{"):
        return "<non-json>"
    try:
        return json.loads(raw, strict=False).get("label")
    except Exception:
        return "<unparseable>"


def loaded_context_length(model):
    try:
        with urllib.request.urlopen(_base() + "/api/ps", timeout=30) as r:
            for m in json.loads(r.read().decode()).get("models", []):
                if m.get("name") == model:
                    return m.get("context_length")
    except Exception:
        pass
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--n", type=int, default=2)
    args = ap.parse_args()

    items = read_jsonl(STRICT)
    items.sort(key=lambda i: -len(i.oracle_evidence))
    probe = items[:args.n]

    R.chat = instrumented_chat                      # capture server metadata
    out = {"model": args.model, "ollama_url": R.OLLAMA, "k": args.k,
           "digest": R.ollama_digest(args.model), "items": []}
    print(f"[probe {args.model}] digest={out['digest']} url={R.OLLAMA}",
          flush=True)

    t_all = time.time()
    for it in probe:
        before = len(CALLS)
        sink: list = []
        t = time.time()
        rows = R.run_question(to_schema(it), k=args.k, rounds=1,
                              raw_sink=sink, model=args.model,
                              pack=to_pack(it))
        calls = CALLS[before:]
        r1 = [r for r in rows if r.get("round") == 1]
        labels = sorted({_label_of(s.get("raw_text") or "")
                         for s in sink} - {None})
        rec = {
            "hedgeqa_id": it.hedgeqa_id,
            "evidence_chars": len(it.oracle_evidence),
            "gold": it.gold_label,
            "seconds": round(time.time() - t, 1),
            "parse_rate_by_round": [r.get("parse_rate") for r in rows],
            "predicted_r1": r1[0].get("predicted") if r1 else None,
            "emitted_labels": labels,
            "out_of_space_labels": [x for x in labels
                                    if x not in it.answer_space],
            "max_prompt_tokens": max((c["prompt_eval_count"] or 0)
                                     for c in calls),
            "done_reasons": sorted({str(c["done_reason"]) for c in calls}),
            "max_thinking_chars": max(c["thinking_chars"] for c in calls),
            "empty_content_calls": sum(1 for c in calls
                                       if c["content_chars"] == 0),
            "calls_with_control_chars": sum(
                1 for c in calls if c["control_chars_in_content"]),
            "raw_head_sample": calls[0]["raw_head"] if calls else "",
            "calls": len(calls),
        }
        out["items"].append(rec)
        print(json.dumps(rec), flush=True)

    out["context_length"] = loaded_context_length(args.model)
    out["seconds_per_item"] = round((time.time() - t_all) / len(probe), 1)
    out["projected_hours_317"] = round(out["seconds_per_item"] * 317 / 3600, 2)
    mx = max(i["max_prompt_tokens"] for i in out["items"])
    ctx = out["context_length"]
    out["verdict"] = {
        "parse_ok": all(min(i["parse_rate_by_round"]) >= 0.9
                        for i in out["items"]),
        "no_output_truncation": all(i["done_reasons"] == ["stop"]
                                    for i in out["items"]),
        "no_empty_content": all(i["empty_content_calls"] == 0
                                for i in out["items"]),
        # Headroom rather than equality: a prompt that fills the window to
        # within 5% is indistinguishable from one that was cut to fit it.
        "prompt_fits_context": (ctx is not None and mx < 0.95 * ctx),
        "max_prompt_tokens": mx,
    }
    dst = REPO / "results" / "probes"
    dst.mkdir(parents=True, exist_ok=True)
    safe = args.model.replace(":", "_").replace("/", "_")
    (dst / f"{safe}.json").write_text(json.dumps(out, indent=1),
                                      encoding="utf-8")
    print("VERDICT " + json.dumps({"model": args.model, **out["verdict"],
                                   "context_length": ctx,
                                   "seconds_per_item": out["seconds_per_item"],
                                   "projected_hours_317":
                                       out["projected_hours_317"]}),
          flush=True)


if __name__ == "__main__":
    main()
