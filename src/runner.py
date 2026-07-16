"""Self-consistency debate runner (Round 0 / Round 1), resumable, parallel.

Round 0: each agent answers independently (K decodes, tau=0.7).
Round 1: each agent sees the opponent's Round-0 modal label + one short
rationale (the modal decode's), then re-answers (K fresh decodes).

Raw decodes go to results/raw/<run_id>/decodes.jsonl; aggregated rows to
results/<run_id>_rows.csv. Manifest to results/manifests/<run_id>.json.
"""

from __future__ import annotations

import json
import subprocess
import time
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from pathlib import Path

import numpy as np

from .eu_au import counts_to_dist, decompose, gold_metrics
from .evidence import EvidencePack, build_pack
from .parsing import parse_label
from .schema import AnswerSchema

REPO = Path(__file__).resolve().parents[1]
OLLAMA = "http://localhost:11434/api/chat"
MODEL = "gemma4:latest"
TAU = 0.7
WORKERS = 4

ROLE_PROMPTS = {
    "fundamental": (
        "You are the Fundamental Analysis Agent. You reason from company "
        "fundamentals (profitability, leverage, cash flow, valuation ratios). "
        "{lane_note} Reason ONLY from the provided evidence; do not invent "
        "outside facts. Never give direct investment advice; assess what the "
        "evidence supports."
    ),
    "trading": (
        "You are the Trading-Signal Analysis Agent. You reason from price "
        "action and technical indicators (momentum, RSI, MACD, moving "
        "averages, volume). {lane_note} Reason ONLY from the provided "
        "evidence; do not invent outside facts. Never give direct investment "
        "advice; assess what the evidence supports."
    ),
}

LANE_NOTES = {
    ("fundamental", "F"): "Fundamentals are primary for this question.",
    ("fundamental", "T"): ("This is a trading-signal question; still give your "
                           "best label, acknowledging fundamentals may have "
                           "limited relevance here."),
    ("fundamental", "FT"): "Weigh fundamentals fully; trading signals also matter.",
    ("trading", "F"): ("This is a fundamentals question; still give your best "
                       "label, acknowledging trading signals may have limited "
                       "relevance here."),
    ("trading", "T"): "Trading signals are primary for this question.",
    ("trading", "FT"): "Weigh trading signals fully; fundamentals also matter.",
}

USER_TEMPLATE = """Trading Signals Context:
{trading}

Fundamental Data Context:
{fundamental}

Question: {question}

{debate_block}You must answer with ONLY a JSON object:
{{"label": "<one of: {space}>", "rationale": "<2-3 sentences from the evidence>", "used_indicators": ["<indicator names>"]}}

"label" MUST be exactly one of: {space}.{label_semantics}"""

DEBATE_TEMPLATE = """--- DEBATE: the other analyst (the {opp_role} agent) answered "{opp_label}" with this rationale:
"{opp_rationale}"
Consider their argument against your own reading of the evidence. You may keep or revise your answer.

"""


def ollama_digest() -> str:
    try:
        out = subprocess.run(["ollama", "list"], capture_output=True, text=True,
                             timeout=30).stdout
        for line in out.splitlines():
            if line.startswith(MODEL.split(":")[0]):
                return line.split()[1]
    except Exception:
        pass
    return "unknown"


def chat(system: str, user: str, temperature: float = TAU,
         timeout: int = 300, model: str = MODEL) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}],
        "stream": False,
        "format": "json",
        "think": False,  # disable reasoning-mode preambles (qwen3 etc.)
        "options": {"temperature": float(temperature)},
    }
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode()).get("message", {}).get("content", "")


def _label_semantics(schema: AnswerSchema) -> str:
    if schema.question_id == "FT31":
        return (' Here "supportive" means rotate out of the position; '
                '"unsupportive" means maintain it; "conditional" means it '
                "depends on strategy.")
    return ""


def elicit_agent(agent: str, schema: AnswerSchema, pack: EvidencePack, k: int,
                 debate_block: str = "", raw_sink: list | None = None,
                 round_id: int = 0, model: str = MODEL,
                 extra_instruction: str = "") -> list:
    system = ROLE_PROMPTS[agent].format(
        lane_note=LANE_NOTES[(agent, schema.lane)])
    user = USER_TEMPLATE.format(
        trading=pack.trading_context, fundamental=pack.fundamental_context,
        question=schema.question, debate_block=debate_block,
        space=", ".join(schema.answer_space),
        label_semantics=_label_semantics(schema) + extra_instruction)

    def one(i: int):
        t0 = time.time()
        try:
            raw = chat(system, user, model=model)
        except Exception as exc:
            raw = f"__ERROR__ {exc}"
        pr = parse_label(raw, schema)
        rec = {"question_id": schema.question_id, "agent": agent,
               "round": round_id, "decode": i, "raw_text": raw,
               "parsed_label": pr.parsed_label,
               "parser_confidence": pr.parser_confidence,
               "parser_method": pr.parser_method,
               "parse_failure_reason": pr.parse_failure_reason,
               "seconds": round(time.time() - t0, 2)}
        return rec

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        recs = list(ex.map(one, range(k)))
    if raw_sink is not None:
        raw_sink.extend(recs)
    return recs


def modal_label_and_rationale(recs: list, schema: AnswerSchema) -> tuple[str, str]:
    labels = [r["parsed_label"] for r in recs if r["parsed_label"]]
    if not labels:
        return "unparseable", ""
    modal = Counter(labels).most_common(1)[0][0]
    for r in recs:
        if r["parsed_label"] == modal:
            try:
                rat = json.loads(r["raw_text"]).get("rationale", "")
            except Exception:
                rat = ""
            if rat:
                return modal, rat[:500]
    return modal, ""


def run_question(schema: AnswerSchema, k: int, rounds: int = 1,
                 raw_sink: list | None = None, model: str = MODEL,
                 extra_instruction: str = "") -> list[dict]:
    """Run one question; returns one row per round with EU/AU + gold metrics.

    If schema.gold_label is not in schema.answer_space (e.g. hedge-gold
    questions under a directional-only probe menu), gold metrics are
    skipped and the row carries gold_scoreable = False.
    """
    candidates = [y for y in schema.answer_space
                  if y.isupper() and 2 <= len(y) <= 5]  # ticker labels
    pack = build_pack(schema.question_id, schema.lane, schema.question,
                      schema.golden_indicators, candidate_tickers=candidates)

    kw = {"model": model, "extra_instruction": extra_instruction}
    rows = []
    r0 = {a: elicit_agent(a, schema, pack, k, raw_sink=raw_sink, round_id=0, **kw)
          for a in ("fundamental", "trading")}
    per_round = {0: r0}
    if rounds >= 1:
        blocks = {}
        for a, opp in (("fundamental", "trading"), ("trading", "fundamental")):
            lab, rat = modal_label_and_rationale(r0[opp], schema)
            blocks[a] = DEBATE_TEMPLATE.format(opp_role=opp, opp_label=lab,
                                               opp_rationale=rat)
        per_round[1] = {a: elicit_agent(a, schema, pack, k, debate_block=blocks[a],
                                        raw_sink=raw_sink, round_id=1, **kw)
                        for a in ("fundamental", "trading")}

    for t, agents in per_round.items():
        dists, k_eff, labels_by_agent = {}, {}, {}
        parse_ok = parse_tot = 0
        for a, recs in agents.items():
            labs = [r["parsed_label"] for r in recs if r["parsed_label"]]
            parse_ok += len(labs)
            parse_tot += len(recs)
            labels_by_agent[a] = labs
            if labs:
                dists[a] = counts_to_dist(labs, schema.answer_space)
                k_eff[a] = len(labs)
        row = {"question_id": schema.question_id, "lane": schema.lane,
               "answer_type": schema.answer_type, "round": t, "K": k,
               "evidence_mode": pack.evidence_mode,
               "coverage_incomplete": pack.coverage_incomplete,
               "tickers": "|".join(pack.tickers),
               "parse_rate": parse_ok / parse_tot if parse_tot else 0.0}
        if len(dists) == 2:
            d = decompose(dists, k_effective=k_eff)
            scoreable = schema.gold_label in schema.answer_space
            row["gold_scoreable"] = scoreable
            if scoreable:
                gm = gold_metrics(d.p_sys, schema.answer_space, schema.gold_label)
                gi = schema.answer_space.index(schema.gold_label)
            row.update({
                "tu": d.tu, "au": d.au, "eu": d.eu,
                "tu_mm": d.tu_mm, "au_mm": d.au_mm, "eu_mm": d.eu_mm,
                "tu_norm": d.tu_norm, "au_norm": d.au_norm, "eu_norm": d.eu_norm,
                "eu_tu_ratio": d.eu / d.tu if d.tu > 0 else 0.0,
                "predicted": schema.answer_space[int(np.argmax(d.p_sys))],
                "p_sys": json.dumps(dict(zip(schema.answer_space,
                                             np.round(d.p_sys, 4).tolist()))),
                "agent_entropy_fundamental": d.agent_entropies.get("fundamental"),
                "agent_entropy_trading": d.agent_entropies.get("trading"),
                "k_eff_fundamental": k_eff.get("fundamental"),
                "k_eff_trading": k_eff.get("trading"),
            })
            if scoreable:
                row.update({
                    "gold_prob": gm.gold_prob, "correct": gm.correct,
                    "brier": gm.brier, "nll": gm.nll,
                    "agent_gold_prob_fundamental":
                        float(dists["fundamental"][gi]),
                    "agent_gold_prob_trading": float(dists["trading"][gi]),
                })
        else:
            row["error"] = "agent distribution unavailable (parse failure)"
        rows.append(row)
    return rows
