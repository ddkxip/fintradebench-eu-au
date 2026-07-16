"""AnswerSchema loading and validation (ANSWER_SCHEMA_DESIGN.md)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "answer_schemas.jsonl"

HEADLINE_CONFIDENCE = {"high", "medium"}


@dataclass
class AnswerSchema:
    question_id: str
    lane: str
    question: str
    golden_indicators: str
    answer_type: str
    answer_space: list[str]
    gold_label: str | None
    gold_label_evidence: str
    canonical_claim: str
    aliases: dict[str, list[str]] = field(default_factory=dict)
    label_parse_rules: str = ""
    ambiguity_notes: str = ""
    schema_confidence: str = "low"

    @property
    def headline_eligible(self) -> bool:
        return (self.answer_type != "schema_uncertain"
                and self.schema_confidence in HEADLINE_CONFIDENCE
                and bool(self.answer_space)
                and self.gold_label in self.answer_space)


def load_schemas(path: Path = SCHEMA_PATH) -> dict[str, AnswerSchema]:
    out: dict[str, AnswerSchema] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        s = AnswerSchema(**obj)
        if s.question_id in out:
            raise ValueError(f"duplicate question_id {s.question_id}")
        out[s.question_id] = s
    return out


def validate(schemas: dict[str, AnswerSchema],
             expected_total: int | None = None,
             expected_per_lane: dict[str, int] | None = None) -> list[str]:
    """Return a list of human-readable violations (empty = valid)."""
    errs: list[str] = []
    if expected_total is not None and len(schemas) != expected_total:
        errs.append(f"expected {expected_total} schemas, found {len(schemas)}")
    lanes: dict[str, int] = {}
    for s in schemas.values():
        lanes[s.lane] = lanes.get(s.lane, 0) + 1
        uncertain = s.answer_type == "schema_uncertain"
        if not uncertain:
            if not s.answer_space:
                errs.append(f"{s.question_id}: empty answer_space")
            if len(set(s.answer_space)) != len(s.answer_space):
                errs.append(f"{s.question_id}: duplicate labels in answer_space")
            if s.gold_label not in s.answer_space:
                errs.append(f"{s.question_id}: gold_label {s.gold_label!r} not in answer_space")
            if not s.gold_label_evidence.strip():
                errs.append(f"{s.question_id}: missing gold_label_evidence")
            extra = set(s.aliases) - set(s.answer_space)
            if extra:
                errs.append(f"{s.question_id}: aliases for unknown labels {sorted(extra)}")
        else:
            if s.schema_confidence != "low":
                errs.append(f"{s.question_id}: schema_uncertain must be low confidence")
        if s.schema_confidence not in {"high", "medium", "low"}:
            errs.append(f"{s.question_id}: bad schema_confidence")
        if s.lane not in {"F", "T", "FT"}:
            errs.append(f"{s.question_id}: bad lane {s.lane}")
    if expected_per_lane:
        for lane, n in expected_per_lane.items():
            if lanes.get(lane, 0) != n:
                errs.append(f"lane {lane}: expected {n}, found {lanes.get(lane, 0)}")
    return errs
