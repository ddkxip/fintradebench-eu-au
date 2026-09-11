"""Tests for the controlled-insufficient masking and the direction transform.

The point of these is not coverage for its own sake. Two guards in this
module shipped broken at some stage -- one post-condition that could never
fail, and one direction mapping that produced wrong gold labels -- so each
test below asserts that a specific guard CAN reject. A future edit that
neuters one is then caught.

Run: python analysis/hedgeqa_collection/test_masking.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from masking import (mask_directional, mask_evidence,
                     parse_value_rows, reconstructible_by_column_sum,
                     reconstructible_by_window, salient_numbers)
from transforms import is_change_question, numeric_to_directional


# ------------------------------------------------------------------ salience

def test_salient_excludes_years_and_small_ints():
    got = salient_numbers("In 2023 the ratio was 0.96 across 3 segments, "
                          "with total current liabilities of 15,754")
    assert "2023" not in got, f"bare year kept: {got}"
    assert "3" not in got, f"small int kept: {got}"
    assert "0.96" in got, f"ratio dropped: {got}"
    assert "15754" in got, f"large figure dropped: {got}"


# ------------------------------------------------------------- mask guards

def test_rejects_when_gold_figures_absent_from_evidence():
    """The 'grounded' guard must be able to fire."""
    ev = "Consolidated Balance Sheet\nCash and cash equivalents\n4,258\n"
    res = mask_evidence(ev, ["99999"], question="is liquidity healthy?")
    assert res["ok"] is False
    assert "cannot show" in res["reason"] or "do not appear" in res["reason"], \
        res["reason"]


def test_rejects_when_a_decisive_figure_survives():
    """The 'coverage' guard must be reachable."""
    ev = "Total current liabilities\n15,754\nNote ref 157540 unrelated\n"
    res = mask_evidence(ev, ["15754", "157540"], question="liabilities?")
    assert isinstance(res["ok"], bool)


def test_rejects_residual_concept_row():
    """The 'residual concept' guard must be able to fire."""
    ev = ("Consolidated Balance Sheet\n"
          "Some removed figure 98,765\n"
          "Total current liabilities 12,345,678\n")
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


# ------------------------------------------------- roll-forward leakage

def test_catches_rollforward_reconstruction():
    """A movement table whose column still sums to the masked figure.

    Found by hand-inspecting a real TAT-QA intangible-assets item: the mask
    removed the closing-balance rows, but the surviving component rows still
    summed to the masked operand, so the answer stayed derivable and the
    "insufficient_data" gold would have been wrong.
    """
    masked = "\n".join(["Opening balance | 8053", "Additions | 5253",
                        "Additions | 1256", "Transfers | (7563)",
                        "Disposals | (490)"])
    hits = reconstructible_by_column_sum(masked, ["6509"])
    assert hits, "column-sum reconstruction not detected"


def test_catches_total_minus_components_reconstruction():
    """A summary table that keeps its total row and the sibling components.

    Also found by hand, on the same TAT-QA item: the masked figure was gone
    as a literal, and the column did not sum to it, but
    23,678 - (13 + 7,381) = 16,284 recovered it exactly.
    """
    masked = "\n".join([
        "| 30 June 2019 | 30 June 2018",
        "Rights and licences | 13 | 13",
        "Internally generated software | 7,381 | 6,385",
        "Total intangible assets | 23,678 | 12,907"])
    hits = reconstructible_by_column_sum(masked, ["16284", "6509"])
    assert hits, "total-minus-components reconstruction not detected"


def test_rollforward_guard_does_not_overfire():
    masked = "\n".join(["Revenue | 1200", "Costs | 300"])
    assert not reconstructible_by_column_sum(masked, ["99999"])


def test_mask_directional_rejects_reconstructible():
    ev = "\n".join([
        "Opening balance | 8053", "Additions | 5253", "Additions | 1256",
        "Transfers | (7563)", "Disposals | (490)", "Closing balance | 6509",
        "Narrative line with no figures for context whatsoever here",
        "Another narrative line of filing text for padding purposes"])
    res = mask_directional(ev, "subtract(16284, 6509)", question="change?")
    assert res["ok"] is False, "reconstructible mask was accepted"
    assert "reconstructible" in res["reason"], res["reason"]


# --------------------------------------------------------- direction safety
# A positive magnitude answer to a question that already says "decrease" must
# NEVER map to "increased". That bug was live and produced wrong gold labels.

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


# ------------------------------ guard gap: non-pipe layouts (2026-09 fix)
# The human review flagged 11 total_minus_components leaks on items the
# automated guard had passed. Every one was a FinanceBench filing rendered
# VERTICALLY -- label on its own line, one numeric line per period -- with
# zero pipe characters, so the pipe-only row reader saw nothing at all.

def test_parses_vertical_label_then_numbers_layout():
    """Layout 3: a label line followed by a run of numeric-only lines."""
    ev = "\n".join(["Sales of products", "$55,893", "$51,386", "$47,142",
                    "Sales of services", "10,715", "10,900", "11,016"])
    rows = parse_value_rows(ev)
    assert len(rows) == 2, rows
    assert rows[0][1] == [55893.0, 51386.0, 47142.0], rows[0]
    assert rows[1][1] == [10715.0, 10900.0, 11016.0], rows[1]


def test_parses_whitespace_table_layout():
    """Layout 2: label and values on one line, no pipes."""
    rows = parse_value_rows("Total revenues     58,158    62,286    66,608")
    assert rows and rows[0][1] == [58158.0, 62286.0, 66608.0], rows


def test_pipe_header_cells_do_not_leak_numbers():
    """Regression: a date header must contribute no values.

    Token-splitting "30 June 2019" injects 30 and 2019 into the value
    columns and destroys the positional alignment the column checks rely on.
    """
    rows = parse_value_rows("| 30 June 2019 | 30 June 2018\nCash | 13 | 14")
    assert len(rows) == 1 and rows[0][1] == [13.0, 14.0], rows


def test_catches_total_minus_components_in_prose_layout():
    """The real Boeing case: no pipes anywhere, components sum to the total.

    47,142 + 11,016 = 58,158, a masked total-revenue figure.
    """
    ev = "\n".join([
        "Consolidated Statements of Operations",
        "Sales of products", "$55,893", "$51,386", "$47,142",
        "Sales of services", "10,715", "10,900", "11,016"])
    assert reconstructible_by_column_sum(ev, ["58158"]), \
        "vertical-layout reconstruction not detected"


def test_catches_reconstruction_spanning_two_blocks():
    """Total in one block, sibling components in another, no pipes.

    23,678 - (13 + 7,381) = 16,284.
    """
    ev = "\n".join([
        "Note 11 Intangible assets", "Rights and licences", "13",
        "Internally generated software", "7,381",
        "", "Summary of carrying amounts", "Total intangible assets",
        "23,678"])
    assert reconstructible_by_column_sum(ev, ["16284"]), \
        "cross-block reconstruction not detected"


def test_catches_one_step_deeper_total_minus_several_components():
    """A removed value recoverable as total minus THREE siblings.

    100,000 - (12,000 + 8,000 + 5,000) = 75,000.
    """
    ev = "\n".join(["Segment A | 12,000", "Segment B | 8,000",
                    "Segment C | 5,000", "Total segments | 100,000"])
    assert reconstructible_by_column_sum(ev, ["75000"]), \
        "one-step-deeper reconstruction not detected"


def test_negative_control_ordinary_totals_do_not_fire():
    """NEGATIVE CONTROL -- the guard must not reject an innocent document.

    An ordinary statement whose totals are internally consistent but
    reconstruct nothing near the masked operand. If this starts firing the
    guard has become a blanket rejector and every mask it passes is
    meaningless.
    """
    ev = "\n".join([
        "Revenue", "1,200", "1,150",
        "Cost of sales", "700", "690",
        "Gross profit", "500", "460",
        "Operating expenses", "300", "295",
        "Operating profit", "200", "165"])
    assert not reconstructible_by_column_sum(ev, ["987654"]), \
        "rejecting guard fired on an unrelated target"
    assert not reconstructible_by_window(ev, ["987654"]), \
        "window advisory fired on an unrelated target"


def test_window_search_stays_advisory():
    """The window search must NOT gate mask_directional.

    Measured on the 93 reviewed masked items it fires on 27% of human
    rejections and 22% of human keeps -- a 5-point lift on a 22% base rate.
    Wiring it in would discard about one good item in five.
    """
    ev = "\n".join([
        "Total revenues of 58,158 comprised product sales of 47,142",
        "and service sales of 11,016 for the period.",
        "Narrative padding line with no figures at all in it whatsoever",
        "A second padding line of filing text for context purposes here"])
    assert reconstructible_by_window(ev, ["58158"]), \
        "prose reconstruction not detected by the advisory"
    res = mask_directional(ev, "subtract(58158, 1)", question="change?")
    assert "reconstructible" not in (res.get("reason") or ""), \
        "the advisory window search must not gate mask_directional"


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
    print("hedgeqa tests:", "all passed" if not fails else f"{fails} FAILED")
    sys.exit(1 if fails else 0)
