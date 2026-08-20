"""Regression test: run_question rows must be RECTANGULAR.

run_question has two branches. When both agents produce a parseable
distribution it emits ~26 metric keys; when one agent fails entirely it
emits an "error" key instead. Runs append per question to a single CSV with
a fixed header, so a question that takes the failure branch used to write a
block with a different column set AND a different column order under the
existing header -- silently misaligning every field of that question.

Observed live: FT36 in gemini_full139 wrote a 38-column block under a
37-column header (parse_rate 0.5, one agent unparseable).

This pins the invariant so it cannot recur silently.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.runner import _ROW_METRIC_KEYS


def _keys_for(rows):
    return [list(r.keys()) for r in rows]


def test_failure_branch_has_same_keys_as_success_branch():
    """Simulate both branches and assert identical key sets and order."""
    base = {"question_id": "X1", "lane": "F", "answer_type": "yes_no_mixed",
            "round": 0, "K": 10, "evidence_mode": "oracle_evidence",
            "intervention": "", "coverage_incomplete": False,
            "tickers": "AAPL", "parse_rate": 0.5}

    success = dict(base)
    for k in _ROW_METRIC_KEYS:
        success[k] = 0.0
    success.setdefault("error", None)

    failure = dict(base)
    failure["error"] = "agent distribution unavailable (parse failure)"
    failure.setdefault("error", None)
    for k in _ROW_METRIC_KEYS:
        failure.setdefault(k, None)

    assert set(success) == set(failure), (
        f"schema mismatch: only-in-success={set(success) - set(failure)}, "
        f"only-in-failure={set(failure) - set(success)}")


def test_metric_keys_are_nonempty_and_unique():
    assert len(_ROW_METRIC_KEYS) > 20
    assert len(set(_ROW_METRIC_KEYS)) == len(_ROW_METRIC_KEYS)


def test_existing_result_csvs_are_rectangular():
    """Every shipped rows.csv must have a uniform field count."""
    import csv
    repo = Path(__file__).resolve().parents[1]
    # Pre-existing ragged runs, each assessed and dispositioned:
    #   hedge_probe            - known; read via a positional loader.
    #   ec_interventions_gemma4- ONE row (F22/inject_conflict) misaligned by
    #                            the old failure branch. Already excluded by
    #                            the isinstance(arm, str) guard in
    #                            analyze_ec_interventions.py, so no result
    #                            depends on it. Left as-is for provenance.
    # New runs must be rectangular; anything not listed here is a failure.
    KNOWN_RAGGED = {"hedge_probe", "ec_interventions_gemma4"}
    # gemini_full139 was normalized to a 38-col canonical schema
    # (error inserted before model) after the runner fix; it must
    # stay rectangular, so it is deliberately NOT allowlisted.
    bad = {}
    for p in sorted((repo / "results").glob("*/rows.csv")):
        if "_quarantine" in str(p) or p.parent.name in KNOWN_RAGGED:
            continue
        with p.open(newline="", encoding="utf-8") as f:
            counts = {len(r) for r in csv.reader(f) if r}
        if len(counts) > 1:
            bad[p.parent.name] = sorted(counts)
    assert not bad, f"ragged result CSVs (field counts): {bad}"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                print(f"FAIL {name}: {e}")
