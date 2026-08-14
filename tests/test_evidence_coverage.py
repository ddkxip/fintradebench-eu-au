"""Regression test for the 2026-08 evidence-coverage bug.

An audit found 21/139 headline questions built EMPTY evidence packs because
the company name was missing from src.evidence.NAME_TO_TICKER. Models then
correctly answered "insufficient_data", which the error taxonomy mis-scored
as a hedge collision -- inflating the paper's headline number.

This test pins the invariant so it cannot recur silently.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.evidence import COMBINED_DIR, SUFFIX, NAME_TO_TICKER, build_pack
from src.schema import load_schemas

# Questions with no named entity (sector/category-level) plus FT19, whose
# reference answer IS "insufficient_data" because MRNA has no data file.
# These are legitimately empty and are the ONLY permitted exceptions.
ALLOWED_EMPTY = {"F23", "F45", "F49", "FT19"}
MIN_CHARS = 200


def _packs():
    out = {}
    for s in load_schemas().values():
        if not s.headline_eligible:
            continue
        cands = [y for y in s.answer_space if y.isupper() and 2 <= len(y) <= 5]
        p = build_pack(s.question_id, s.lane, s.question,
                       s.golden_indicators, candidate_tickers=cands)
        out[s.question_id] = p
    return out


def test_no_unexpected_empty_evidence_packs():
    empty = {q for q, p in _packs().items()
             if len(p.trading_context) + len(p.fundamental_context) < MIN_CHARS}
    unexpected = empty - ALLOWED_EMPTY
    assert not unexpected, (
        f"{len(unexpected)} question(s) built empty evidence packs: "
        f"{sorted(unexpected)}. Add the company to NAME_TO_TICKER, or add the "
        f"id to ALLOWED_EMPTY with a justification.")


# Aliases deliberately kept despite having NO data file: the reference
# answers for F31 (Walmart) and F25 (Disney) are correct *because* the data
# is absent, so the entity must still be recognised in the question in order
# for the absence to be visible to the agents.
ALLOWED_MISSING_DATA = {"walmart", "disney"}


def test_every_alias_resolves_to_a_real_data_file():
    bad = {name: tkr for name, tkr in NAME_TO_TICKER.items()
           if name not in ALLOWED_MISSING_DATA
           and not (COMBINED_DIR / f"{tkr}{SUFFIX}").exists()}
    assert not bad, (
        f"aliases point at missing data files: {bad}. Either the ticker is "
        f"wrong or the entity belongs in ALLOWED_MISSING_DATA with a reason.")


def test_empty_pack_rate_is_small():
    packs = _packs()
    empty = sum(1 for p in packs.values()
                if len(p.trading_context) + len(p.fundamental_context) < MIN_CHARS)
    rate = empty / len(packs)
    assert rate <= 0.05, f"empty-pack rate {rate:.1%} exceeds 5% ({empty}/{len(packs)})"


if __name__ == "__main__":
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            fn()
            print(f"PASS {name}")
    print("evidence coverage tests passed")
