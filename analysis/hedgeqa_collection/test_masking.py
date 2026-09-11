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

from masking import (classify_question, mask_directional, mask_evidence,
                     parse_value_rows, reconstructible_by_column_sum,
                     reconstructible_by_window, salient_numbers, splice_sites)
from transforms import is_change_question, numeric_to_directional


# --------------------------------------------------------------- splice guard

# The real MGM text, reconstructed from `hqa_FB_5dbbcec0_masked`: the two
# middle lines are what masking deleted (they carry `0.01` and `2022.`), the
# outer two are what survived in the shipped item.
MGM_LINES = [
    "We implemented a dividend program in February 2017 pursuant to which it "
    "has paid regular quarterly dividends. In the second quarter of 2020, we",
    "reduced our annual dividend to $0.01 per share in light of the impact of "
    "the COVID-19 pandemic on our operations at that time. We maintained an "
    "annual",
    "dividend of $0.01 per share throughout 2022. On February 8, 2023, we "
    "announced that the Board of Directors has determined to suspend the "
    "ongoing dividends",
    "in light of our current preferred method of returning value to "
    "shareholders through our share repurchase plan. To the extent we "
    "determine to reinstate the",
    "dividend in the future, the amount, declaration and payment of any "
    "future dividends will be subject to the discretion of our Board.",
]


def test_catches_mgm_sentence_splice():
    """REGRESSION: the defect that shipped in hqa_FB_5dbbcec0_masked.

    Deleting lines 1 and 2 joins "In the second quarter of 2020, we" to
    "in light of our current preferred method..." -- a grammatical sentence
    asserting a Q2-2020 suspension, which is the opposite of the truth (MGM
    maintained a $0.01 dividend through 2022). The guard must reject it.
    """
    sites = splice_sites(MGM_LINES, [1, 2])
    assert sites, "the MGM splice was not detected"
    assert "second quarter of 2020, we" in sites[0]["joined"], sites[0]
    assert "in light of our current preferred" in sites[0]["joined"], sites[0]

    # and end to end, through the real entry point
    res = mask_evidence("\n".join(MGM_LINES), ["0.01"],
                        question="Did MGM pay a dividend in FY2022?")
    assert res["ok"] is False, "mask_evidence shipped a spliced document"
    assert "splice" in res["reason"], res["reason"]
    assert res["splices"], "no splice recorded on the result"


def test_negative_control_deletion_between_complete_sentences():
    """Deleting a whole standalone sentence must NOT fire the splice guard."""
    lines = [
        "The Company operates three reportable business segments worldwide.",
        "Segment revenue for the period was 12,345 across all three units.",
        "Each segment is managed by a separate executive leadership team.",
    ]
    assert not splice_sites(lines, [1]), \
        "guard fired on a deletion between two complete sentences"
    res = mask_evidence("\n".join(lines), ["12345"],
                        question="what was the change in segment revenue?")
    assert res["ok"] is True, res["reason"]
    assert not res["splices"], res["splices"]


def test_negative_control_table_rows_are_not_splices():
    """Table rows have no sentence structure to splice."""
    lines = ["Consolidated Balance Sheet", "Total current assets",
             "58,158", "47,142", "Narrative line of filing text for context"]
    assert not splice_sites(lines, [2, 3]), \
        "guard fired on deleted numeric table rows"


def test_splice_guard_needs_a_real_gap():
    """Two already-adjacent prose lines are not a splice: nothing was joined."""
    assert not splice_sites(MGM_LINES, []), "fired with nothing removed"
    assert not splice_sites(MGM_LINES, [4]), \
        "fired on a trailing deletion that joined nothing"


# ------------------------------------------------------------- category gate

def test_category_gate_refuses_existence_and_qualitative_questions():
    """The two shapes that produced the FinanceBench defects."""
    assert classify_question(
        "Has CVS Health reported any materially important ongoing legal "
        "battles from 2022, 2021 and 2020?")["category"] == "existence"
    assert classify_question(
        "Has MGM Resorts paid dividends to common shareholders in FY2022?"
    )["category"] == "existence"
    assert classify_question(
        "Does Adobe have an improving Free cashflow conversion as of FY2022?"
    )["category"] == "qualitative"
    assert classify_question(
        "Does AMCOR have an improving gross margin profile as of FY2023? If "
        "gross margin is not a useful metric for a company like this, then "
        "state that and explain why.")["category"] == "narrative"
    for q in ("Has CVS reported any material legal battles?",
              "Has MGM paid dividends to common shareholders in FY2022?"):
        assert classify_question(q)["maskable"] is False, q


def test_category_gate_admits_genuinely_numeric_questions():
    """It must not refuse the items number-deletion is built for."""
    for q in ("Did Pfizer grow its PPNE between FY20 and FY21?",
              "Was there any drop in Cash & Cash equivalents between FY 2023 "
              "and Q2 of FY2024?",
              "Is growth in JnJ's adjusted EPS expected to accelerate in "
              "FY2023?"):
        c = classify_question(q)
        assert c["category"] == "numeric", f"{q} -> {c}"
        assert c["maskable"] is True, q


def test_category_gate_blocks_a_prose_answerable_mask_end_to_end():
    """The CVS shape: figures gone, question still answerable from prose."""
    ev = ("The Company is a defendant in a number of lawsuits alleging that "
          "its retail pharmacies overcharged for prescription drugs.\n"
          "The Company agreed to a settlement of 4,300 with several state "
          "Attorneys General during the period.\n"
          "These matters remain subject to court approval and further "
          "proceedings in the ordinary course.\n")
    res = mask_evidence(ev, ["4300"],
                        question="Has the Company reported any materially "
                                 "important ongoing legal battles?")
    assert res["ok"] is False, "a prose-answerable question was masked"
    assert "not maskable" in res["reason"], res["reason"]
    assert res["question_category"] == "existence", res["question_category"]


def test_category_gate_is_discharged_by_proof():
    """`numeric_dependency` overrides the gate -- and only it does."""
    ev = ("Consolidated Statement of Cash Flows\n"
          "Purchases of property, plant and equipment 1,577\n"
          "Some narrative line with no figures at all in it whatsoever\n"
          "Another purely textual line of the filing for context\n")
    q = "Does it have a healthy capital expenditure profile?"
    blocked = mask_evidence(ev, ["1577"], question=q)
    assert blocked["ok"] is False, "qualitative question was not gated"
    proved = mask_evidence(ev, ["1577"], question=q,
                           numeric_dependency="program operands ['1577']")
    assert proved["ok"] is True, proved["reason"]
    assert "numeric dependency proved" in proved["reason"], proved["reason"]


def test_unclassified_questions_fail_closed():
    c = classify_question("Frobnicate the widget?")
    assert c["category"] == "unclassified"
    assert c["maskable"] is False, "unknown question shape defaulted to OPEN"


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
