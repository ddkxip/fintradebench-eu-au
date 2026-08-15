"""Full audit of all 139 reference answers against the evidence packs.

Motivated by F50, whose reference justifies label APP as having "ROA at
14.89% (highest)" while the released table shows NVDA at 0.2131 > APP at
0.1489. That error was found by hand. This script looks for the same class of
problem systematically.

Four mechanical checks per question, run against the evidence pack the agents
actually saw:

  A. NUMERIC PROVENANCE  every number cited in `gold_label_evidence` should
     appear somewhere in the pack (raw or percent-scaled). A number that
     appears nowhere means the reference cites data the agents never saw.
  B. SUPERLATIVE         a claim "<TICKER> ... highest/lowest <indicator>"
     should hold: TICKER must be the argmax/argmin of that indicator among
     the pack's tickers.
  C. GOLD ENTITY DATA    if the reference label is a ticker, it must be
     present in the pack with non-NA values.
  D. SET-COLLAPSE        the reference names more than one entity from the
     answer space (the T-lane screening problem).

These are TRIAGE SIGNALS, not verdicts. Check A in particular fires on
legitimate cases (a reference may quote a figure computed over a different
window than the pack's). Every flag needs a human read; the point is to
reduce 139 references to a short list worth reading.

Run: python analysis/reference_answer_audit.py
Writes: analysis/reference_answer_audit.csv
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

import numpy as np
import pandas as pd

from src.evidence import GOLDEN_ALIAS, build_pack
from src.schema import load_schemas

# indicator words that may appear in prose -> pack value keys
PROSE_TO_KEY: dict[str, str] = {
    "roa": "F_Return on Assets",
    "return on assets": "F_Return on Assets",
    "roe": "F_Return on Equity",
    "return on equity": "F_Return on Equity",
    "cash flow/assets": "F_Cash Flow/Assets",
    "cash flow to assets": "F_Cash Flow/Assets",
    "book/price": "F_Book/Price",
    "book-to-price": "F_Book/Price",
    "book to price": "F_Book/Price",
    "sales/assets": "F_Sales/Assets",
    "debt/assets": "F_Debt/Assets",
    "debt-to-assets": "F_Debt/Assets",
    "debt/equity": "F_Debt/Equity",
    "debt-to-equity": "F_Debt/Equity",
    "dividend yield": "F_Dividend Yield",
    "earnings/price": "F_Earnings/Price",
    "rsi": "RSI",
    "macd": "MACD",
    "obv": "OBV",
    "momentum_20d": "Momentum_20D",
    "momentum_5d": "Momentum_5D",
    "short_term_reversal_1month": "Short_Term_Reversal_1month",
    "mean_reversal_60d": "Mean_Reversal_60D",
    "max_return_20d": "Max_Return_20D",
    "ma_20": "MA_20",
    "ema_20": "EMA_20",
}

MAX_SUPER = re.compile(
    r"\b(highest|strongest|best|largest|greatest|top|most)\b", re.I)
MIN_SUPER = re.compile(r"\b(lowest|weakest|smallest|least|cheapest)\b", re.I)
NUM = re.compile(r"(?<![\w.])(-?\d+\.\d+|-?\d+)\s*%?")


def pack_values(pack) -> dict[str, dict[str, float]]:
    """ticker -> {key: value}, NaNs dropped."""
    return {t: {k: v for k, v in vals.items()
                if isinstance(v, (int, float)) and pd.notna(v)}
            for t, vals in pack.indicator_values.items()}


def number_in_pack(x: float, vals: dict[str, dict[str, float]]) -> bool:
    """Does x appear as a pack value, raw or percent-scaled?"""
    for per_t in vals.values():
        for v in per_t.values():
            for cand in (v, v * 100.0):
                if abs(cand - x) <= max(0.005, abs(x) * 0.01):
                    return True
    return False


def check_numbers(ev: str, vals) -> list[str]:
    out = []
    for m in NUM.finditer(ev):
        raw = m.group(1)
        try:
            x = float(raw)
        except ValueError:
            continue
        # ignore bare years and small integers (counts, "top 5")
        if float(x).is_integer() and (abs(x) < 100 or 1900 < abs(x) < 2100):
            continue
        if not number_in_pack(x, vals):
            out.append(raw)
    return out


def check_superlatives(ev: str, gold: str, vals) -> list[str]:
    """Claims where a superlative DIRECTLY qualifies a named indicator.

    Deliberately conservative. A superlative attached to a composite concept
    ("the strongest balance sheet", "the most oversold asset") does not
    constrain any single indicator's argmax -- indeed it often inverts it, so
    a loose proximity match produces false positives. We fire only on:

        "<super> <indicator>"                e.g. "highest ROA"
        "<indicator> ...<=40ch... <super>"   e.g. "ROA at 14.89% (highest)"
                                             e.g. "an OBV of 22.96B, the highest"

    and only when the superlative word is not separated from the indicator by
    a sentence boundary.
    """
    problems = []
    low = ev.lower()
    for prose, key in PROSE_TO_KEY.items():
        for m in re.finditer(re.escape(prose), low):
            pre = low[max(0, m.start() - 22): m.start()]
            post = low[m.end(): m.end() + 40]
            # a sentence/clause break cuts the link
            # split on sentence breaks only -- NOT on the decimal point
            # inside a figure like "14.89%", which would truncate the very
            # "(highest)" we are looking for.
            sent = r"(?<!\d)\.(?!\d)|;"
            post_head = re.split(sent + r"|\band\b(?!\s*\()", post)[0]
            pre_tail = re.split(sent, pre)[-1]
            hit_max = MAX_SUPER.search(pre_tail) or MAX_SUPER.search(post_head)
            hit_min = MIN_SUPER.search(pre_tail) or MIN_SUPER.search(post_head)
            if not (hit_max or hit_min) or (hit_max and hit_min):
                continue
            have = {t: d[key] for t, d in vals.items() if key in d}
            if len(have) < 2 or gold not in have:
                continue
            best = (max(have, key=have.get) if hit_max
                    else min(have, key=have.get))
            if best != gold:
                problems.append(
                    f"{'highest' if hit_max else 'lowest'} {prose}: reference "
                    f"says {gold} ({have[gold]:.4f}) but {best} "
                    f"({have[best]:.4f}) wins")
    return sorted(set(problems))


def main() -> None:
    sch = load_schemas()
    rows = []
    for s in sorted(sch.values(), key=lambda x: x.question_id):
        if not s.headline_eligible:
            continue
        cands = [y for y in s.answer_space if y.isupper() and 2 <= len(y) <= 5]
        pack = build_pack(s.question_id, s.lane, s.question,
                          s.golden_indicators, candidate_tickers=cands)
        vals = pack_values(pack)
        ev = s.gold_label_evidence or ""
        gold = s.gold_label

        # D: set-collapse
        named = [y for y in cands if re.search(r"\b" + re.escape(y) + r"\b", ev)]
        # C: gold entity has data
        gold_missing = bool(gold in cands and not vals.get(gold))
        # B: superlatives
        supers = check_superlatives(ev, gold, vals) if gold in cands else []
        # A: numeric provenance
        orphan = check_numbers(ev, vals)

        rows.append({
            "question_id": s.question_id, "lane": s.lane, "gold": gold,
            "n_entities_named": len(named),
            "set_collapse": len(named) > 1,
            "gold_entity_no_data": gold_missing,
            "superlative_contradicted": bool(supers),
            "superlative_detail": " | ".join(supers),
            "orphan_numbers": " ".join(orphan[:6]),
            "n_orphan_numbers": len(orphan),
            "evidence_chars": len(pack.trading_context)
                              + len(pack.fundamental_context),
        })
    d = pd.DataFrame(rows)
    out = REPO / "analysis" / "reference_answer_audit.csv"
    d.to_csv(out, index=False, encoding="utf-8")

    n = len(d)
    print(f"AUDITED {n} reference answers\n")
    print(f"B. superlative contradicted by pack : "
          f"{d.superlative_contradicted.sum():3d}  <-- READ THESE")
    print(f"C. gold entity absent from pack     : "
          f"{d.gold_entity_no_data.sum():3d}")
    print(f"D. set-collapse (>1 entity named)   : "
          f"{d.set_collapse.sum():3d}  ({d.set_collapse.mean():.0%})")
    print(f"A. has >=1 orphan number            : "
          f"{(d.n_orphan_numbers > 0).sum():3d}  (triage only)")
    print("\nset-collapse by lane:")
    print(d.groupby("lane").set_collapse.agg(["sum", "count", "mean"])
          .round(3).to_string())

    bad = d[d.superlative_contradicted]
    if len(bad):
        print("\n" + "=" * 70)
        print("SUPERLATIVE CONTRADICTIONS (reference vs. released indicators)")
        print("=" * 70)
        for _, r in bad.iterrows():
            print(f"\n{r.question_id} [{r.lane}] gold={r.gold}")
            for part in r.superlative_detail.split(" | "):
                print(f"    {part}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
