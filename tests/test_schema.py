"""Schema validation tests (Phase-2 pilot: 20 schemas, 7F/7T/6FT).

The 150-question expectations are parameterized; when the full set ships,
change PILOT_* to the 150/50/50/50 values.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.schema import load_schemas, validate

PILOT_TOTAL = 150
PILOT_LANES = {"F": 50, "T": 50, "FT": 50}


def test_load_and_validate_pilot():
    schemas = load_schemas()
    errs = validate(schemas, expected_total=PILOT_TOTAL,
                    expected_per_lane=PILOT_LANES)
    assert not errs, "\n".join(errs)


def test_no_duplicate_ids_enforced_by_loader():
    schemas = load_schemas()
    assert len(schemas) == PILOT_TOTAL


def test_headline_exclusion_of_low_confidence():
    schemas = load_schemas()
    for s in schemas.values():
        if s.schema_confidence == "low" or s.answer_type == "schema_uncertain":
            assert not s.headline_eligible, s.question_id
    eligible = [s for s in schemas.values() if s.headline_eligible]
    assert all(s.gold_label in s.answer_space for s in eligible)
    assert len(eligible) >= 100  # 150-scale expectation


def test_gold_labels_nonempty_for_eligible():
    schemas = load_schemas()
    for s in schemas.values():
        if s.headline_eligible:
            assert s.gold_label and s.answer_space


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
    print("schema tests passed")
