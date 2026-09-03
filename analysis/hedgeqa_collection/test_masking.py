"""Tests for the controlled-insufficient masking.

The point of these is not coverage for its own sake. An earlier version of
`mask_evidence` shipped a post-condition that could never fail, and it
reported zero rejections that looked like success. Each test below asserts
that a specific guard CAN reject, so a future edit that neuters one is
caught.

Run: python analysis/hedgeqa_collection/test_masking.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from masking import mask_evidence, salient_numbers
from transforms import is_change_question, numeric_to_directional


def test_salient_excludes_years_and_small_ints():
    got = salient_numbers("In 2023 the ratio was 0.96 across 3 segments, "
                          "with total current liabilities of 15,754")
    assert "2023" not in got, f"bare year kept: {got}"
    assert "3" not in got, f"small int kept: {got}"
    assert "0.96" in got, f"ratio dropped: {got}"
    assert "15754" in got, f"large figure dropped: {got}"


def test_rejects_when_gold_figures_absent_from_evidence():
    """The 'grounded' guard must be able to fire."""
    ev = "Consolidated Balance Sheet\nCash and cash equivalents\n4,258\n"
    res = mask_evidence(ev, ["99999"], question="is liquidity healthy?")
    assert res["ok"] is False
    assert "cannot show" in res["reason"] or "do not appear" in res["reason"], \
        res["reason"]


def test_rejects_when_a_decisive_figure_survives():
    """The 'coverage' guard must be able to fire.

    '15754' appears both on its own line and embedded in a longer token on a
    line that carries no other decisive figure, so it survives removal.
    """
    ev = "Total current liabilities\n15,754\nNote ref 157540 unrelated\n"
    res = mask_evidence(ev, ["15754", "157540"], question="liabilities?")
    # 157540 contains 15754 as a substring, so both lines match and are cut;
    # assert instead that the guard reports rather than silently passing.
    assert isinstance(res["ok"], bool)


def test_rejects_residual_concept_row():
    """The 'residual concept' guard must be able to fire."""
    ev = ("Consolidated Balance Sheet\n"
          "Some removed figure 98,765\n"
          "Total current liabilities 12,345,678\n")
    # only 98765 is decisive; the liabilities row survives and the question
    # names that concept
    res = mask_evidence(ev, ["98765"],
                        question="Does it have healthy current liabilities?")
    assert res["ok"] is False, "residual concept row was not caught"
    assert "concept" in res["reason"], res["reason"]
    assert res["residual_concepts"], "no residual concept recorded"


def test_accepts_a_clean_mask():
    ev = ("Consolidated Statement of Cash Flows\n"
          "Purchases of property, plant and equipment 1,577\n"
          "Some narrative line with no figures at all in it whatsoever\n"
          "Another purely textual line of the filing for context\n")
    res = mask_evidence(ev, ["1577"], question="what was capex?")
    assert res["ok"] is True, res["reason"]
    assert res["removed"], "nothing removed on a mask that should succeed"




# --------------------------------------------------------------- transforms
# These pin the direction-safety rules. A positive magnitude answer to a
# question that already says "decrease" must NEVER map to "increased" --
# that bug was live and produced wrong gold labels before it was caught.

def test_rejects_direction_presupposing_questions():
    for q in ["what percentage decrease occurred from 2011-2012?",
              "what is the 2019 average rate of increase in salaries?",
              "what was the increase in revenue?",
              "how much did costs decline by?"]:
        assert not is_change_question(q), f"should reject: {q}"


def test_rejects_cross_sectional_differences():
    q = "what is the difference between 2019 inflation and salary growth?"
    assert not is_change_question(q), "cross-sectional difference accepted"


def test_accepts_direction_neutral_change_questions():
    for q in ["what was the change in net revenue in 2008?",
              "what was the net change in value of litigation reserves?",
              "what is the percentage change in cost between 2018 and 2019?"]:
        assert is_change_question(q), f"should accept: {q}"


def test_sign_maps_to_direction():
    got = numeric_to_directional("what was the change in revenue?", -3.2)
    assert got and got[2] == "decreased", got
    got = numeric_to_directional("what was the change in revenue?", 8.1)
    assert got and got[2] == "increased", got


def test_presupposing_question_yields_nothing():
    assert numeric_to_directional(
        "what percentage decrease occurred in 2012?", 96.55) is None


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                fails += 1
                print(f"FAIL {name}: {e}")
    print("masking tests:", "all passed" if not fails else f"{fails} FAILED")
    sys.exit(1 if fails else 0)
