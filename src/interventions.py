"""Controlled evidence interventions (E-C' do-operators).

Each takes the oracle EvidencePack and returns an edited copy plus a
description of what changed. Edits are transparent string/value surgery on
the built contexts so they are reproducible and auditable. The control arm
for every intervention is the stored oracle Round-0 baseline
(results/ea_full_gemma4), so only the intervened arm is run.

Arms:
  remove_top_indicator  - strip the top golden indicator's values
                          (evidence-sufficiency do-operator; predict U1-source
                          rises: p_noncommit/AU up, gold-prob down if it matters)
  remove_placebo        - strip a matched NON-golden indicator (specificity
                          control; predict NO movement -> the off-diagonal)
  inject_ft_conflict    - append a strong synthetic trading signal opposing the
                          fundamental lean (predict EU up if hedge breaks, else
                          p_noncommit up)
  horizon_short/long    - rewrite the question horizon, evidence fixed
                          (predict verdict/confidence shift; flat = horizon
                          insensitivity)
"""

from __future__ import annotations

import copy
import re

from .evidence import EvidencePack, FUND_COLS, TRADING_COLS, golden_to_columns

# label a column as fundamental (F_ prefix) or trading
_FUND_SET = set(FUND_COLS)


def _strip_columns(pack: EvidencePack, cols: list[str]) -> EvidencePack:
    """Remove any evidence lines / tokens mentioning the given CSV columns."""
    p = copy.deepcopy(pack)
    p.evidence_mode = "intervention"
    fund_cols = [c for c in cols if c in _FUND_SET]
    trade_cols = [c for c in cols if c not in _FUND_SET]

    # fundamental context: drop "  * COL: val" lines
    if fund_cols:
        kept = [ln for ln in p.fundamental_context.splitlines()
                if not any(f"* {c}:" in ln for c in fund_cols)]
        p.fundamental_context = "\n".join(kept)
    # trading context: drop "COL=val" tokens from the Indicators line
    if trade_cols:
        out = []
        for ln in p.trading_context.splitlines():
            if ln.strip().startswith("- Indicators:"):
                toks = [t.strip() for t in ln.split(":", 1)[1].split(",")]
                toks = [t for t in toks
                        if not any(t.startswith(f"{c}=") for c in trade_cols)]
                ln = "- Indicators: " + ", ".join(toks)
            out.append(ln)
        p.trading_context = "\n".join(out)
    return p


def _present(pack: EvidencePack, col: str) -> bool:
    """True if the column has a non-NA value shown in either context."""
    for ctx in (pack.fundamental_context, pack.trading_context):
        for ln in ctx.splitlines():
            if f"* {col}:" in ln:
                return "NA" not in ln.split(":", 1)[1]
            if ln.strip().startswith("- Indicators:"):
                for tok in ln.split(":", 1)[1].split(","):
                    tok = tok.strip()
                    if tok.startswith(f"{col}="):
                        return "NA" not in tok
    return False


def remove_top_indicator(pack: EvidencePack, golden_indicators: str
                         ) -> tuple[EvidencePack, str]:
    """Strip the highest-priority golden indicator that is actually PRESENT
    (non-NA) in the evidence, so the manipulation is meaningful."""
    toks = [t.strip() for t in str(golden_indicators).split("|") if t.strip()]
    for tok in toks:  # golden set is roughly priority-ordered
        cols = [c for c in golden_to_columns(tok) if _present(pack, c)]
        if cols:
            return _strip_columns(pack, cols), f"removed_golden:{tok}->{cols}"
    return pack, "noop_all_golden_absent"


def remove_placebo(pack: EvidencePack, golden_indicators: str
                   ) -> tuple[EvidencePack, str]:
    """Remove a NON-golden indicator of the SAME channel + matched count as the
    top golden indicator, so the only difference vs remove_top is relevance."""
    toks = [t.strip() for t in str(golden_indicators).split("|") if t.strip()]
    golden_cols = set()
    for t in toks:
        golden_cols.update(golden_to_columns(t))
    if not toks:
        return pack, "noop"
    top_cols = golden_to_columns(toks[0])
    n = len(top_cols)
    top_is_fund = bool(top_cols) and top_cols[0] in _FUND_SET
    pool = ([c for c in FUND_COLS if c not in golden_cols] if top_is_fund
            else [c for c in TRADING_COLS
                  if c not in golden_cols and c != "Adj. Close"])
    # keep only columns actually present in this pack's contexts
    present = pack.fundamental_context + pack.trading_context
    pool = [c for c in pool if (f"* {c}:" in present) or (f"{c}=" in present)]
    if not pool:
        return pack, "noop_no_placebo_available"
    victims = pool[:max(1, n)]
    return _strip_columns(pack, victims), f"removed_placebo:{victims}"


# fundamental lean from profitability sign; trading lean from momentum sign
def _fund_lean(values: dict) -> int:
    roe = _first(values, "F_Return on Equity")
    roa = _first(values, "F_Return on Assets")
    s = 0
    for v in (roe, roa):
        if v is not None:
            s += 1 if v > 0 else -1
    return 1 if s > 0 else (-1 if s < 0 else 1)


def _first(values: dict, col: str):
    for _, vd in values.items():
        if isinstance(vd, dict) and col in vd:
            try:
                x = float(vd[col])
                if x == x:  # not NaN
                    return x
            except (TypeError, ValueError):
                continue
    return None


_CONFLICT_VALUES = {
    "bearish": {"RSI": "24.0000", "MACD": "-8.5000", "MACD_Signal": "-5.0000",
                "Momentum_20D": "-0.1800", "Momentum_5D": "-0.0600"},
    "bullish": {"RSI": "76.0000", "MACD": "8.5000", "MACD_Signal": "5.0000",
                "Momentum_20D": "0.1800", "Momentum_5D": "0.0600"},
}


def inject_ft_conflict(pack: EvidencePack) -> tuple[EvidencePack, str]:
    """Coherently overwrite the momentum/RSI/MACD tokens so the trading
    picture opposes the fundamental lean (edited-values do(conflict)).

    Replacement (not appending) keeps the trading channel internally
    coherent while making it point opposite to fundamentals, so both agents
    read one clean cross-signal contradiction rather than a self-contradiction.
    """
    p = copy.deepcopy(pack)
    p.evidence_mode = "intervention"
    direction = "bearish" if _fund_lean(pack.indicator_values) > 0 else "bullish"
    repl = _CONFLICT_VALUES[direction]

    out = []
    edited = False
    for ln in p.trading_context.splitlines():
        if ln.strip().startswith("- Indicators:"):
            toks = [t.strip() for t in ln.split(":", 1)[1].split(",")]
            new = []
            for t in toks:
                key = t.split("=", 1)[0]
                new.append(f"{key}={repl[key]}" if key in repl else t)
            ln = "- Indicators: " + ", ".join(new)
            edited = True
        out.append(ln)
    if edited:
        # also restate the AdjClose direction line so price trend agrees
        note = ("- Note: price trend now points opposite to the fundamental "
                f"picture ({direction} technicals vs opposing fundamentals).")
        out.append(note)
    p.trading_context = "\n".join(out) + "\n"
    d = ("bearish_tech_vs_bullish_fund" if direction == "bearish"
         else "bullish_tech_vs_bearish_fund")
    return p, f"inject_conflict:{d}" + ("" if edited else "_noop")


HORIZON_SHORT = " Consider only the next 3 months (short-term horizon)."
HORIZON_LONG = " Consider the next 5 years (long-term horizon)."


def horizon_rewrite(question: str, direction: str) -> str:
    suffix = HORIZON_SHORT if direction == "short" else HORIZON_LONG
    return question.rstrip() + suffix
