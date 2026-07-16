"""Label parsing hierarchy: strict JSON -> alias/regex -> failure record.

(The schema-aware LLM fallback parser is deliberately deferred until the
pilot shows it is needed — strict-JSON prompting with Ollama format=json
should carry most of the load.)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

from .schema import AnswerSchema


@dataclass
class ParseResult:
    raw_text: str
    parsed_label: str | None
    parser_confidence: float
    parser_method: str
    parse_failure_reason: str | None = None


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 /_-]", "", s.lower()).strip()


def parse_label(raw: str, schema: AnswerSchema) -> ParseResult:
    space = schema.answer_space
    norm_space = {_norm(y): y for y in space}

    # 1. strict JSON with a "label" field
    try:
        obj = json.loads(raw)
    except Exception:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        obj = None
        if m:
            try:
                obj = json.loads(m.group(0))
            except Exception:
                obj = None
    if isinstance(obj, dict) and "label" in obj:
        lab = _norm(str(obj["label"]))
        if lab in norm_space:
            return ParseResult(raw, norm_space[lab], 1.0, "strict_json")
        # label field present but off-space: try alias match on it
        for y, al in schema.aliases.items():
            if any(_norm(a) == lab or _norm(a) in lab for a in al):
                return ParseResult(raw, y, 0.8, "json_alias")
        return ParseResult(raw, None, 0.0, "strict_json",
                           f"label {obj['label']!r} not in answer space")

    # 2. alias/regex over the whole text (last resort, ordered by
    #    specificity: exact-token labels first, then aliases)
    text = _norm(raw)
    for y in space:
        if re.search(rf"\b{re.escape(_norm(y))}\b", text):
            return ParseResult(raw, y, 0.5, "regex_label")
    for y, al in schema.aliases.items():
        for a in sorted(al, key=len, reverse=True):
            if _norm(a) and _norm(a) in text:
                return ParseResult(raw, y, 0.4, "regex_alias")

    return ParseResult(raw, None, 0.0, "none", "no JSON label, no alias hit")
