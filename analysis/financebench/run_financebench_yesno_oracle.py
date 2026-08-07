"""FinanceBench yes/no ORACLE-EVIDENCE debate run (Phase 1).

Mirrors the FinTradeBench self-consistency + 1-round debate design, adapted
to FinanceBench: two agents reason ONLY over the human-annotated
`evidence_text` supplied with each question. No RAG, no PDF retrieval, no
outside knowledge.

Agents:
  evidence_accountant  - does the evidence directly support yes or no?
  skeptical_auditor    - is the evidence actually sufficient / is the claim
                         overstated?

Backends (--model prefix):
  vllm:<hf_id>    OpenAI-compatible server ($VLLM_BASE_URL, default
                  http://localhost:8000/v1)
  ollama:<name>   local Ollama (default if no prefix)
  vertex:<model>  Vertex AI

Use --dry-run to print the first N prompts WITHOUT calling any model.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

REPO = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(REPO))

from src.eu_au import counts_to_dist, decompose, gold_metrics  # noqa: E402

SCHEMAS = HERE / "financebench_yesno_schemas.jsonl"
ANSWER_SPACE = ["yes", "no", "insufficient_data"]
NONCOMMIT_SET = {"insufficient_data"}
TAU = 0.7

AGENTS = {
    "evidence_accountant": (
        "You are the Evidence Accountant. Your job is to determine whether "
        "the PROVIDED EVIDENCE directly supports a 'yes' or a 'no' answer to "
        "the question. You read the evidence literally and quantitatively: "
        "locate the specific figures, line items or statements that bear on "
        "the question and follow them to a conclusion."
    ),
    "skeptical_auditor": (
        "You are the Skeptical Auditor. Your job is to test whether the "
        "PROVIDED EVIDENCE is actually sufficient to answer the question, and "
        "whether any yes/no conclusion would be overstated. You look for "
        "missing periods, missing line items, definitional mismatches between "
        "the question and the evidence, and unsupported inferential leaps."
    ),
}

RULES = (
    "\n\nSTRICT RULES:\n"
    "1. Use ONLY the evidence provided below. Do not use outside knowledge, "
    "memorised figures, or anything not present in the evidence.\n"
    "2. If the evidence does not answer the question, choose "
    "\"insufficient_data\".\n"
    "3. Respond with a JSON object ONLY. No prose before or after.\n"
    "4. The \"label\" field MUST be exactly one of: \"yes\", \"no\", "
    "\"insufficient_data\"."
)

USER_TEMPLATE = """QUESTION:
{question}

ORACLE EVIDENCE (the only permitted source):
\"\"\"
{evidence}
\"\"\"

{debate_block}Respond with JSON only, exactly in this form:
{{"label": "<yes|no|insufficient_data>", "rationale": "<2-3 sentences citing the evidence>"}}"""

DEBATE_TEMPLATE = """--- DEBATE: the other analyst (the {opp}) answered "{opp_label}" with this rationale:
"{opp_rationale}"
Weigh their argument against your own reading of the evidence. You may keep or revise your answer.

"""


# ── backends ────────────────────────────────────────────────────────────
def chat(system: str, user: str, model: str, temperature: float = TAU,
         timeout: int = 300) -> str:
    if model.startswith("vertex:"):
        from src.vertex import chat_vertex
        return chat_vertex(system, user, model.split(":", 1)[1],
                           temperature=temperature)
    if model.startswith("vllm:"):
        base = os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1").rstrip("/")
        payload = {
            "model": model.split(":", 1)[1],
            "messages": [{"role": "system", "content": system},
                         {"role": "user", "content": user}],
            "temperature": float(temperature),
            "max_tokens": 512,
        }
        if not os.environ.get("VLLM_NO_JSON_MODE"):
            # some vLLM builds reject response_format -> set VLLM_NO_JSON_MODE=1
            payload["response_format"] = {"type": "json_object"}
        req = urllib.request.Request(
            f"{base}/chat/completions", data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {os.environ.get('VLLM_API_KEY', 'EMPTY')}"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                obj = json.loads(r.read().decode())
        except urllib.error.HTTPError as e:  # surface the server's message
            body = e.read().decode(errors="replace")[:500]
            raise RuntimeError(f"vLLM HTTP {e.code} from {base}: {body}") from None
        except Exception as e:
            raise RuntimeError(f"vLLM request to {base} failed: {e}") from None
        return obj["choices"][0]["message"]["content"]
    # ollama (default)
    name = model.split(":", 1)[1] if model.startswith("ollama:") else model
    payload = {"model": name,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}],
               "stream": False, "format": "json", "think": False,
               "options": {"temperature": float(temperature)}}
    req = urllib.request.Request(
        os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat"),
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("message", {}).get("content", "")


def parse_label(raw: str) -> tuple[str | None, str]:
    """Return (label, method). Strict JSON first, then a bounded fallback."""
    import re
    obj, src = None, "strict_json"
    try:
        obj = json.loads(raw)
    except Exception:
        m = re.search(r"\{.*\}", raw or "", re.DOTALL)
        if m:
            try:
                obj = json.loads(m.group(0))
                src = "embedded_json"  # JSON found inside surrounding prose
            except Exception:
                obj = None
    if isinstance(obj, dict) and "label" in obj:
        lab = str(obj["label"]).strip().lower().replace(" ", "_")
        if lab in ANSWER_SPACE:
            return lab, src
        if lab in {"insufficient", "unknown", "cannot_determine", "n/a"}:
            return "insufficient_data", src + "_alias"
    t = (raw or "").lower()
    if "insufficient_data" in t or "insufficient data" in t:
        return "insufficient_data", "regex"
    m = re.search(r'"label"\s*:\s*"(yes|no)"', t)
    if m:
        return m.group(1), "regex"
    return None, "none"


def build_prompts(sch: dict, evidence_field: str, debate_block: str = "") -> dict:
    ev = sch.get(evidence_field) or sch.get("evidence_text") or ""
    out = {}
    for agent, role in AGENTS.items():
        out[agent] = {
            "system": role + RULES,
            "user": USER_TEMPLATE.format(question=sch["question"], evidence=ev,
                                         debate_block=debate_block),
        }
    return out


def elicit(agent: str, sch: dict, k: int, model: str, evidence_field: str,
           debate_block: str, workers: int, round_id: int, sink: list) -> list[dict]:
    p = build_prompts(sch, evidence_field, debate_block)[agent]

    def one(i):
        t0 = time.time()
        try:
            raw = chat(p["system"], p["user"], model=model)
        except Exception as exc:
            raw = f"__ERROR__ {exc}"
        lab, method = parse_label(raw)
        rec = {"financebench_id": sch["financebench_id"], "agent": agent,
               "round": round_id, "decode": i, "raw_text": raw,
               "parsed_label": lab, "parser_method": method,
               "seconds": round(time.time() - t0, 2)}
        return rec

    with ThreadPoolExecutor(max_workers=workers) as exr:
        recs = list(exr.map(one, range(k)))
    sink.extend(recs)
    return recs


def modal(recs: list[dict]) -> tuple[str, str]:
    labs = [r["parsed_label"] for r in recs if r["parsed_label"]]
    if not labs:
        return "unparseable", ""
    m = Counter(labs).most_common(1)[0][0]
    for r in recs:
        if r["parsed_label"] == m:
            try:
                return m, str(json.loads(r["raw_text"]).get("rationale", ""))[:400]
            except Exception:
                continue
    return m, ""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="vllm:Qwen/Qwen3.6-27B-FP8")
    ap.add_argument("--run-id", default="financebench_yesno_oracle_qwen36")
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--rounds", type=int, default=1)
    ap.add_argument("--evidence-field", default="evidence_text",
                    choices=["evidence_text", "evidence_full_page"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true",
                    help="print prompts for the first N examples; no model calls")
    ap.add_argument("--dry-run-n", type=int, default=3)
    a = ap.parse_args()

    schs = [json.loads(l) for l in SCHEMAS.read_text(encoding="utf-8").splitlines() if l.strip()]

    if a.dry_run:
        print("=" * 78)
        print(f"DRY RUN — no model calls. model would be: {a.model}")
        print(f"K={a.k} rounds={a.rounds} evidence_field={a.evidence_field} "
              f"examples={len(schs)}")
        print("=" * 78)
        for sch in schs[:a.dry_run_n]:
            pr = build_prompts(sch, a.evidence_field)
            print(f"\n{'#'*78}\n# {sch['financebench_id']} | {sch['company']} | "
                  f"{sch['doc_name']} | GOLD={sch['gold_label']}\n{'#'*78}")
            for agent in AGENTS:
                print(f"\n----- [{agent}] SYSTEM -----\n{pr[agent]['system']}")
                print(f"\n----- [{agent}] USER -----\n{pr[agent]['user']}")
                print(f"----- [end {agent}] evidence chars="
                      f"{len(sch.get(a.evidence_field) or sch['evidence_text'])} -----")
            # round-1 preview for the first example only
            if sch is schs[0] and a.rounds >= 1:
                db = DEBATE_TEMPLATE.format(
                    opp="evidence_accountant", opp_label="yes",
                    opp_rationale="<example: modal rationale from round 0>")
                pr1 = build_prompts(sch, a.evidence_field, db)
                print(f"\n----- [skeptical_auditor] ROUND-1 USER (debate block "
                      f"illustrated) -----\n{pr1['skeptical_auditor']['user']}")
        print("\n" + "=" * 78)
        print("Parser self-test on synthetic outputs:")
        for s in ['{"label": "yes", "rationale": "x"}',
                  '{"label":"insufficient_data","rationale":"y"}',
                  'noise {"label": "no", "rationale": "z"} noise',
                  '{"label": "maybe"}', 'garbage']:
            print(f"  {s[:46]:48s} -> {parse_label(s)}")
        print("=" * 78)
        print("DRY RUN COMPLETE — no model was called.")
        return

    # ── preflight: one live call, fail LOUDLY before spending the run ───
    print(f"[preflight] testing backend with 1 call to {a.model} ...", flush=True)
    probe = build_prompts(schs[0], a.evidence_field)["evidence_accountant"]
    try:
        raw = chat(probe["system"], probe["user"], model=a.model, timeout=180)
    except Exception as exc:
        raise SystemExit(
            f"\n[PREFLIGHT FAILED] backend call raised:\n  {exc}\n\n"
            "Common fixes:\n"
            "  * vLLM not reachable  -> check VLLM_BASE_URL (currently "
            f"{os.environ.get('VLLM_BASE_URL', 'http://localhost:8000/v1')})\n"
            "  * model id mismatch   -> must match what the server reports at "
            "GET /v1/models\n"
            "  * 400 on response_format -> export VLLM_NO_JSON_MODE=1\n"
            "No output was written.")
    lab, method = parse_label(raw)
    print(f"[preflight] raw (first 200 chars): {str(raw)[:200]!r}")
    print(f"[preflight] parsed -> label={lab!r} method={method}")
    if lab is None:
        raise SystemExit(
            "\n[PREFLIGHT FAILED] the backend responded but the output could "
            "not be parsed into a label. Inspect the raw text above. "
            "No output was written.")
    print("[preflight] OK\n", flush=True)

    # ── real run ────────────────────────────────────────────────────────
    import pandas as pd
    out_dir = REPO / "results" / a.run_id
    raw_dir = REPO / "results" / "raw" / a.run_id
    man_dir = REPO / "results" / "manifests"
    for d in (out_dir, raw_dir, man_dir):
        d.mkdir(parents=True, exist_ok=True)
    rows_path = out_dir / "rows.csv"

    done = set()
    if rows_path.exists():
        done = set(pd.read_csv(rows_path)["financebench_id"].unique())
        print(f"resuming: {len(done)} already done")

    t0 = time.time()
    for i, sch in enumerate(schs, 1):
        if sch["financebench_id"] in done:
            continue
        print(f"[{i}/{len(schs)}] {sch['financebench_id']} ...", flush=True)
        sink: list = []
        per_round = {}
        r0 = {ag: elicit(ag, sch, a.k, a.model, a.evidence_field, "",
                         a.workers, 0, sink) for ag in AGENTS}
        per_round[0] = r0
        if a.rounds >= 1:
            blocks = {}
            for ag in AGENTS:
                opp = [x for x in AGENTS if x != ag][0]
                lab, rat = modal(r0[opp])
                blocks[ag] = DEBATE_TEMPLATE.format(opp=opp, opp_label=lab,
                                                    opp_rationale=rat)
            per_round[1] = {ag: elicit(ag, sch, a.k, a.model, a.evidence_field,
                                       blocks[ag], a.workers, 1, sink)
                            for ag in AGENTS}

        out_rows = []
        for rnd, agents in per_round.items():
            dists, keff, ok, tot = {}, {}, 0, 0
            for ag, recs in agents.items():
                labs = [r["parsed_label"] for r in recs if r["parsed_label"]]
                ok += len(labs)
                tot += len(recs)
                if labs:
                    dists[ag] = counts_to_dist(labs, ANSWER_SPACE)
                    keff[ag] = len(labs)
            parse_rate = ok / tot if tot else 0.0
            base = {"financebench_id": sch["financebench_id"], "round": rnd,
                    "K": a.k, "gold_label": sch["gold_label"],
                    "parse_rate": round(parse_rate, 4), "model": a.model,
                    "run_id": a.run_id, "evidence_field": a.evidence_field}
            # per-agent rows
            for ag, recs in agents.items():
                labs = [r["parsed_label"] for r in recs if r["parsed_label"]]
                if not labs:
                    continue
                d = counts_to_dist(labs, ANSWER_SPACE)
                pnc = float(sum(d[j] for j, y in enumerate(ANSWER_SPACE)
                                if y in NONCOMMIT_SET))
                pred = ANSWER_SPACE[int(np.argmax(d))]
                out_rows.append({**base, "agent": ag, "predicted": pred,
                                 "correct": pred == sch["gold_label"],
                                 "p_noncommit": round(pnc, 4),
                                 "tu": None, "au": None, "eu": None,
                                 "p_sys": json.dumps(dict(zip(ANSWER_SPACE,
                                                              np.round(d, 4).tolist())))})
            # system row
            if len(dists) == 2:
                dec = decompose(dists, k_effective=keff)
                gm = gold_metrics(dec.p_sys, ANSWER_SPACE, sch["gold_label"])
                pnc = float(sum(dec.p_sys[j] for j, y in enumerate(ANSWER_SPACE)
                                if y in NONCOMMIT_SET))
                out_rows.append({**base, "agent": "system",
                                 "predicted": gm.predicted, "correct": gm.correct,
                                 "p_noncommit": round(pnc, 4),
                                 "tu": dec.tu_norm, "au": dec.au_norm,
                                 "eu": dec.eu_norm,
                                 "p_sys": json.dumps(dict(zip(ANSWER_SPACE,
                                                              np.round(dec.p_sys, 4).tolist())))})
        # never write silence: if nothing parsed, say why and stop
        n_err = sum(1 for r in sink if str(r["raw_text"]).startswith("__ERROR__"))
        if not out_rows:
            first_err = next((r["raw_text"] for r in sink
                              if str(r["raw_text"]).startswith("__ERROR__")), None)
            with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
                for r in sink:
                    f.write(json.dumps(r) + "\n")
            raise SystemExit(
                f"\n[ABORT] {sch['financebench_id']} produced no parseable "
                f"labels ({n_err}/{len(sink)} decodes errored).\n"
                f"first error: {first_err}\n"
                f"raw decodes saved to {raw_dir/'decodes.jsonl'} for inspection.\n"
                "Nothing further was written.")
        if n_err:
            print(f"  [warn] {n_err}/{len(sink)} decodes errored this question",
                  flush=True)
        df = pd.DataFrame(out_rows)
        df.to_csv(rows_path, mode="a", header=not rows_path.exists(), index=False)
        with (raw_dir / "decodes.jsonl").open("a", encoding="utf-8") as f:
            for r in sink:
                f.write(json.dumps(r) + "\n")

    (man_dir / f"{a.run_id}.json").write_text(json.dumps({
        "run_id": a.run_id, "model": a.model, "k": a.k, "tau": TAU,
        "rounds": a.rounds, "evidence_field": a.evidence_field,
        "n_examples": len(schs), "answer_space": ANSWER_SPACE,
        "noncommit_set": sorted(NONCOMMIT_SET),
        "agents": list(AGENTS), "workers": a.workers,
        "seconds": round(time.time() - t0, 1),
    }, indent=1), encoding="utf-8")
    print(f"DONE in {(time.time()-t0)/60:.1f} min -> {rows_path}")


if __name__ == "__main__":
    main()
