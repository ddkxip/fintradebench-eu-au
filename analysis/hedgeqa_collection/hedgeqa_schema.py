"""HedgeQA-v0.1 item schema, id scheme, and validators.

HedgeQA is NOT a new general financial benchmark. It is a diagnostic
collection assembled so that hedging-failure metrics (hedge collision,
overcommitment, wrong-direction commitment, wrong non-committal type,
p_noncommit, AU/EU debate behaviour) can be computed on a finite answer
space with oracle evidence, across several source benchmarks.

Every item carries its provenance and, where the source question was
rewritten, the original question and the derivation that licences the
rewrite. Nothing here requires retrieval.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path

# ---------------------------------------------------------------- vocabularies

SOURCE_BENCHMARKS = (
    "fintradebench", "financebench", "tatqa", "finqa", "convfinqa",
)

TRANSFORMATION_TYPES = (
    "none",                          # question used as written
    "numeric_to_directional",        # numeric answer -> up/down/higher/lower
    "comparison_to_choice",          # comparison -> pick-one over entities
    "evidence_masked_insufficient",  # evidence deliberately removed; gold is
                                     # a non-committal label BY CONSTRUCTION
)

GOLD_COMMITMENT = ("committed", "noncommitted", "ambiguous_exclude")

VALIDATION_STATUS = (
    "candidate", "auto_validated", "manually_validated", "excluded",
)

# Labels treated as non-committal wherever they appear in an answer space.
CANONICAL_NONCOMMIT = (
    "insufficient_data", "mixed", "conditional", "none_clear",
    "cannot_determine",
)


# ---------------------------------------------------------------------- item

@dataclass
class HedgeQAItem:
    # provenance
    hedgeqa_id: str
    source_benchmark: str
    source_id: str

    # question + evidence
    question: str
    oracle_evidence: str
    evidence_provenance: str          # where the evidence text came from

    # answer structure
    answer_type: str
    answer_space: list
    gold_label: str
    noncommit_labels: list

    # diagnostic bookkeeping
    gold_commitment: str
    transformation_type: str
    requires_rag: bool = False
    validation_status: str = "candidate"
    exclusion_reason: str = None
    schema_confidence: float = 0.0

    # transformation audit trail (required when transformation_type != none)
    original_question: str = None
    derivation: str = None
    masked_content: str = None        # what was removed, for masked variants

    notes: str = None

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)

    @property
    def committed_labels(self) -> list:
        return [y for y in self.answer_space if y not in self.noncommit_labels]


def make_id(source_benchmark: str, source_id: str, suffix: str = "") -> str:
    """Deterministic, collision-resistant, human-greppable item id."""
    key = f"{source_benchmark}|{source_id}|{suffix}"
    h = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
    tag = {"fintradebench": "FTB", "financebench": "FB", "tatqa": "TAT",
           "finqa": "FQ", "convfinqa": "CFQ"}.get(source_benchmark, "UNK")
    return f"hqa_{tag}_{h}" + (f"_{suffix}" if suffix else "")


# ----------------------------------------------------------------- validators
# Each validator returns (ok, message). A failing REQUIRED check means the
# item must be excluded, not silently repaired.

MIN_EVIDENCE_CHARS = 120


def v_answer_space_size(it):
    """>=2 committed labels, OR >=1 committed label plus a non-committal one.

    A space with a single committed label and no escape hatch cannot express
    a hedge, so it cannot exercise the phenomenon under study.
    """
    nc = [y for y in it.answer_space if y in it.noncommit_labels]
    com = it.committed_labels
    ok = len(com) >= 2 or (len(com) >= 1 and len(nc) >= 1)
    return ok, (f"{len(com)} committed / {len(nc)} non-committal labels"
                if ok else
                f"answer space cannot express a hedge: committed={com}, "
                f"noncommit={nc}")


def v_noncommit_subset(it):
    extra = [y for y in it.noncommit_labels if y not in it.answer_space]
    return (not extra), ("ok" if not extra else
                         f"noncommit_labels not in answer_space: {extra}")


def v_gold_in_space(it):
    ok = it.gold_label in it.answer_space
    return ok, ("ok" if ok else
                f"gold_label {it.gold_label!r} not in answer_space")


def v_evidence_present(it):
    n = len(it.oracle_evidence or "")
    ok = n >= MIN_EVIDENCE_CHARS
    return ok, (f"{n} chars" if ok else
                f"oracle_evidence too short ({n} < {MIN_EVIDENCE_CHARS})")


def v_no_rag(it):
    ok = it.requires_rag is False
    return ok, ("ok" if ok else "requires_rag must be False in HedgeQA")


def v_transformation_audit(it):
    """A rewritten question must carry the original and the derivation."""
    if it.transformation_type == "none":
        return True, "not transformed"
    missing = []
    if not it.original_question:
        missing.append("original_question")
    if not it.derivation:
        missing.append("derivation")
    return (not missing), ("ok" if not missing else
                           f"transformed item missing {missing}")


def v_masked_variant_marked(it):
    """Controlled-insufficient variants must be unmistakably marked."""
    masked = it.transformation_type == "evidence_masked_insufficient"
    if not masked:
        return True, "not a masked variant"
    problems = []
    if it.gold_label not in it.noncommit_labels:
        problems.append("masked variant must have a non-committal gold_label")
    if it.gold_commitment != "noncommitted":
        problems.append("masked variant must have gold_commitment=noncommitted")
    if not it.masked_content:
        problems.append("masked variant must record masked_content")
    if "_masked" not in it.hedgeqa_id:
        problems.append("masked variant id must carry the _masked suffix")
    return (not problems), ("ok" if not problems else "; ".join(problems))


def v_gold_commitment_consistent(it):
    if it.gold_commitment == "ambiguous_exclude":
        return True, "flagged ambiguous"
    is_nc = it.gold_label in it.noncommit_labels
    want = "noncommitted" if is_nc else "committed"
    ok = it.gold_commitment == want
    return ok, ("ok" if ok else
                f"gold_commitment={it.gold_commitment} but gold_label "
                f"{it.gold_label!r} is {'non-' if is_nc else ''}committal")


def v_enums(it):
    bad = []
    if it.source_benchmark not in SOURCE_BENCHMARKS:
        bad.append(f"source_benchmark={it.source_benchmark}")
    if it.transformation_type not in TRANSFORMATION_TYPES:
        bad.append(f"transformation_type={it.transformation_type}")
    if it.gold_commitment not in GOLD_COMMITMENT:
        bad.append(f"gold_commitment={it.gold_commitment}")
    if it.validation_status not in VALIDATION_STATUS:
        bad.append(f"validation_status={it.validation_status}")
    return (not bad), ("ok" if not bad else f"bad enum values: {bad}")


def v_no_duplicate_labels(it):
    ok = len(set(it.answer_space)) == len(it.answer_space)
    return ok, ("ok" if ok else f"duplicate labels in {it.answer_space}")


VALIDATORS = [
    ("enums", v_enums),
    ("answer_space_size", v_answer_space_size),
    ("noncommit_subset", v_noncommit_subset),
    ("gold_in_space", v_gold_in_space),
    ("no_duplicate_labels", v_no_duplicate_labels),
    ("evidence_present", v_evidence_present),
    ("no_rag", v_no_rag),
    ("transformation_audit", v_transformation_audit),
    ("masked_variant_marked", v_masked_variant_marked),
    ("gold_commitment_consistent", v_gold_commitment_consistent),
]


def validate(it) -> list:
    return [(name, *fn(it)) for name, fn in VALIDATORS]


def first_failure(it):
    for name, ok, msg in validate(it):
        if not ok:
            return f"{name}: {msg}"
    return None


# --------------------------------------------------------------------- io

def write_jsonl(items, path) -> int:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for it in items:
            f.write(it.to_json() + "\n")
    return len(items)


def read_jsonl(path) -> list:
    path = Path(path)
    out = []
    if not path.exists():
        return out
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(HedgeQAItem(**json.loads(line)))
    return out
