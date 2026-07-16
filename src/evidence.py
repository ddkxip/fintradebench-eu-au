"""Oracle evidence packs — port of the benchmark's own context builder.

Replicates generate_benchmark_responses.py (fintradebench-anonymous/
PaperSubmission): date-window parsing from question text, per-ticker
trading context (first/last close + last in-window indicator values) and
fundamental context (window medians of F_ columns).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

COMBINED_DIR = Path(r"C:\Users\ddkxi\PycharmProjects\Contrastive learning"
                    r"\NASDAQ processed data\output\combined")
SUFFIX = "-daily_with_fundamentals.csv"
DEFAULT_LOOKBACK_DAYS = 90

TRADING_COLS = ["Adj. Close", "MA_20", "MACD", "MACD_Signal", "RSI", "EMA_20",
                "OBV", "One_Day_Reversal", "Max_Return_20D", "Momentum_5D",
                "Momentum_20D", "Mean_Reversal_60D", "Short_Term_Reversal_1month",
                "Medium_Term_Momentum_2month_to_12month",
                "Long_Term_Reversal_13month_to_60month"]
FUND_COLS = ["F_Cash Flow/Assets", "F_Book/Price", "F_Earnings/Price",
             "F_Forecast Earnings/Price", "F_Sales/Assets", "F_Debt/Assets",
             "F_Debt/Equity", "F_Dividend Yield", "F_Return on Assets",
             "F_Return on Equity"]

# golden_indicators vocabulary (25 tokens, Phase-1 audit) -> CSV columns
GOLDEN_ALIAS: dict[str, list[str]] = {
    "rsi": ["RSI"], "macd": ["MACD", "MACD_Signal"], "ma": ["MA_20"],
    "ema": ["EMA_20"], "obv": ["OBV"],
    "volatility": ["Max_Return_20D"], "max return": ["Max_Return_20D"],
    "one day reversal": ["One_Day_Reversal"],
    "short term momentum": ["Momentum_5D", "Momentum_20D"],
    "short-term momentum": ["Momentum_5D", "Momentum_20D"],
    "medium term momentum": ["Medium_Term_Momentum_2month_to_12month"],
    "medium-term momentum": ["Medium_Term_Momentum_2month_to_12month"],
    "long term mean reversal": ["Long_Term_Reversal_13month_to_60month"],
    "long-term mean reversal": ["Long_Term_Reversal_13month_to_60month"],
    "cash flow/assets": ["F_Cash Flow/Assets"], "book/price": ["F_Book/Price"],
    "earnings/price": ["F_Earnings/Price"], "sales/assets": ["F_Sales/Assets"],
    "debt/assets": ["F_Debt/Assets"], "debt/equity": ["F_Debt/Equity"],
    "dividend yield": ["F_Dividend Yield"],
    "roa": ["F_Return on Assets"], "return on assets": ["F_Return on Assets"],
    "roe": ["F_Return on Equity"], "return on equity": ["F_Return on Equity"],
}

MONTHS = {m.lower(): i + 1 for i, m in enumerate(
    ["January", "February", "March", "April", "May", "June", "July",
     "August", "September", "October", "November", "December"])}

# company-name aliases for tickers appearing in the golden set
NAME_TO_TICKER = {
    "apple": "AAPL", "microsoft": "MSFT", "google": "GOOGL", "alphabet": "GOOGL",
    "amazon": "AMZN", "meta": "META", "tesla": "TSLA", "nvidia": "NVDA",
    "netflix": "NFLX", "intel": "INTC", "amd": "AMD", "qualcomm": "QCOM",
    "broadcom": "AVGO", "costco": "COST", "walmart": "WMT", "disney": "DIS",
    "applovin": "APP", "shopify": "SHOP", "idexx": "IDXX", "micron": "MU",
    "lam research": "LRCX", "marvell": "MRVL", "cintas": "CTAS",
    "verisk": "VRSK", "fastenal": "FAST", "coca-cola europacific": "CCEP",
    "roper": "ROP",
}


@lru_cache(maxsize=128)
def load_ticker(ticker: str) -> pd.DataFrame | None:
    p = COMBINED_DIR / f"{ticker}{SUFFIX}"
    if not p.exists():
        return None
    df = pd.read_csv(p, parse_dates=["Date"])
    return df.sort_values("Date").drop_duplicates(subset=["Date"])


def parse_date_range(text: str,
                     default_end: datetime = datetime(2025, 12, 31),
                     ) -> tuple[datetime, datetime, str]:
    """Port of the benchmark's parse_date_range (quarter/month/lastN/year)."""
    s = (text or "").lower()
    m = re.search(r"\bq([1-4])\s*(20\d{2})\b", s)
    if m:
        q, year = int(m.group(1)), int(m.group(2))
        sm = {1: 1, 2: 4, 3: 7, 4: 10}[q]
        start = datetime(year, sm, 1)
        end = (datetime(year + (sm + 2) // 12, (sm + 2) % 12 + 1, 1)
               - timedelta(days=1))
        return start, end, f"Q{q}_{year}"
    m = re.search(r"\b([a-z]+)\s+(20\d{2})\b", s)
    if m and m.group(1) in MONTHS:
        year, mon = int(m.group(2)), MONTHS[m.group(1)]
        start = datetime(year, mon, 1)
        end = (datetime(year + mon // 12, mon % 12 + 1, 1) - timedelta(days=1))
        return start, end, f"{year}-{mon:02d}"
    m = re.search(r"\b(last|past)\s+(\d+)\s+(day|days|week|weeks|month|months)\b", s)
    if m:
        n, unit = int(m.group(2)), m.group(3)
        if unit.startswith("day"):
            start = default_end - timedelta(days=n)
        elif unit.startswith("week"):
            start = default_end - timedelta(weeks=n)
        else:
            start = default_end - timedelta(days=30 * n)
        return start, default_end, f"last_{n}_{unit}"
    m = re.search(r"\b(20\d{2})\b", s)
    if m:
        year = int(m.group(1))
        end = min(datetime(year, 12, 31), default_end)
        return datetime(year, 1, 1), end, f"Year_{year}"
    return default_end - timedelta(days=DEFAULT_LOOKBACK_DAYS), default_end, \
        f"default_{DEFAULT_LOOKBACK_DAYS}d"


def detect_tickers(question: str, extra: list[str] = ()) -> list[str]:
    q = question.lower()
    found = list(extra)
    for name, tkr in NAME_TO_TICKER.items():
        if name in q and tkr not in found:
            found.append(tkr)
    for m in re.findall(r"\b([A-Z]{2,5})\b", question):
        if (COMBINED_DIR / f"{m}{SUFFIX}").exists() and m not in found:
            found.append(m)
    return found


def golden_to_columns(golden_indicators: str) -> list[str]:
    cols: list[str] = []
    for tok in str(golden_indicators).split("|"):
        for c in GOLDEN_ALIAS.get(tok.strip().lower(), []):
            if c not in cols:
                cols.append(c)
    return cols


@dataclass
class EvidencePack:
    question_id: str
    lane: str
    question: str
    golden_indicators: str
    indicator_values: dict = field(default_factory=dict)
    trading_context: str = ""
    fundamental_context: str = ""
    date_start: str = ""
    date_end: str = ""
    date_label: str = ""
    tickers: list[str] = field(default_factory=list)
    evidence_mode: str = "oracle_evidence"
    coverage_incomplete: bool = False


def _context_for_ticker(ticker: str, start: datetime, end: datetime
                        ) -> tuple[str, str, dict]:
    df = load_ticker(ticker)
    if df is None:
        msg = f"[{ticker}] No data file available.\n"
        return msg, msg, {}
    win = df[(df["Date"] >= start) & (df["Date"] <= end)]
    if win.empty:
        msg = f"[{ticker}] No data for {start.date()} -> {end.date()}.\n"
        return msg, msg, {}
    win = win.sort_values("Date")
    closes = win["Adj. Close"].dropna()
    first_c = float(closes.iloc[0]) if len(closes) else np.nan
    last_c = float(closes.iloc[-1]) if len(closes) else np.nan
    pct = (last_c - first_c) / first_c * 100.0 if first_c else np.nan

    vals: dict = {"AdjClose_first": first_c, "AdjClose_last": last_c,
                  "pct_change": pct}
    tl = [f"[{ticker}] Trading/Price Data {start.date()} -> {end.date()}",
          f"- AdjClose: first={first_c:.4f}, last={last_c:.4f}, "
          f"pct_change={pct:.2f}%"]
    ind = {}
    for col in TRADING_COLS:
        if col == "Adj. Close" or col not in win.columns:
            continue
        s = win[col].dropna()
        ind[col] = float(s.iloc[-1]) if len(s) else np.nan
    vals.update(ind)
    tl.append("- Indicators: " + ", ".join(
        f"{k}={v:.4f}" if pd.notna(v) else f"{k}=NA" for k, v in ind.items()))

    fl = [f"[{ticker}] Fundamentals (median in window):"]
    for col in FUND_COLS:
        if col not in win.columns:
            continue
        s = win[col].dropna()
        v = float(s.median()) if len(s) else np.nan
        vals[col] = v
        fl.append(f"  * {col}: {v:.4f}" if pd.notna(v) else f"  * {col}: NA")
    return "\n".join(tl) + "\n", "\n".join(fl) + "\n", vals


def build_pack(question_id: str, lane: str, question: str,
               golden_indicators: str, candidate_tickers: list[str] = ()
               ) -> EvidencePack:
    start, end, label = parse_date_range(question)
    tickers = detect_tickers(question, extra=list(candidate_tickers))
    trading, fundamental, values = [], [], {}
    for t in tickers:
        tc, fc, vals = _context_for_ticker(t, start, end)
        trading.append(tc)
        fundamental.append(fc)
        values[t] = vals
    needed = golden_to_columns(golden_indicators)
    covered = {c for v in values.values() for c, x in v.items() if pd.notna(x)}
    incomplete = (not tickers) or any(c not in covered for c in needed)
    return EvidencePack(
        question_id=question_id, lane=lane, question=question,
        golden_indicators=golden_indicators, indicator_values=values,
        trading_context="\n".join(trading),
        fundamental_context="\n".join(fundamental),
        date_start=start.date().isoformat(), date_end=end.date().isoformat(),
        date_label=label, tickers=tickers,
        coverage_incomplete=bool(incomplete),
    )
