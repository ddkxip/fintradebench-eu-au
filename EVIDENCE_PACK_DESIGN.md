# EVIDENCE_PACK_DESIGN

## Primary mode: oracle_evidence (headline)

Replicates the benchmark's own generation contexts so debate uncertainty
is measured *conditional on the same evidence the golds were built from*.
Source of truth: `generate_benchmark_responses.py` in
`fintradebench-anonymous/PaperSubmission` (inspected 2026-07-09). The
adapter (src/evidence.py) ports its logic:

1. **Ticker detection**: explicit tickers + company-alias index built from
   the 100 per-company CSVs in
   `NASDAQ processed data/output/combined/<TICKER>-daily_with_fundamentals.csv`.
2. **Date window**: `parse_date_range` port — "Q3 2025" → quarter window;
   "August 2025" → month window; "last N months"; bare year; fallback
   lookback. Every golden question mentions a date (150/150, Phase-1
   audit).
3. **Trading context** per ticker: AdjClose first/last/%change over the
   window + last in-window values of MA_20, MACD, MACD_Signal, RSI,
   EMA_20, OBV, One_Day_Reversal, Max_Return_20D, Momentum_5D,
   Momentum_20D, Mean_Reversal_60D, Short_Term_Reversal_1month,
   Medium_Term_Momentum_2month_to_12month, Long_Term_Reversal_13month_to_60month.
4. **Fundamental context** per ticker: window **median** of the F_ columns
   (Cash Flow/Assets, Book/Price, Earnings/Price, Forecast E/P,
   Sales/Assets, Debt/Assets, Debt/Equity, Dividend Yield, ROA, ROE).
5. **Screening questions** (multi-ticker): context includes the shortlist
   tickers from the AnswerSchema (gold top-1 + runners-up + distractors),
   NOT all 100 — bounded context, symmetric evidence across candidate
   labels.

EvidencePack fields: question_id · lane · question · golden_indicators ·
indicator_values (structured dict) · trading_context (str) ·
fundamental_context (str) · date_start/date_end/date_label · tickers ·
evidence_mode.

Golden-indicator alias normalization (audit: "ROE" vs "Return on Equity",
"MA" vs MA_20, "Volatility" → Max_Return_20D / realized proxy, "Short Term
Momentum" vs "Short-term momentum") lives in one mapping table in
src/evidence.py with a unit test that every distinct golden_indicators
token (25 in the golden set) maps to ≥1 CSV column.

## Secondary mode: rag_evidence (ablation only)

Reuses the existing RAG pipeline (`evaluate_rag_pipeline.py` /
`run_snowflake_rag_pipeline.py` line) to retrieve SEC-filing context for
the same questions. Purpose: E-D′ only — does retrieval noise raise AU, or
raise EU via asymmetric readings of incomplete context. Never mixed into
headline rows.

## Intervention mode (E-C′)

`evidence_mode = intervention`, with an `intervention` field naming the
dial: remove_top_indicator / inject_ft_conflict / horizon_dial. Built by
editing an oracle pack, never by re-retrieving.

## Integrity rules

- Agents never see the gold response, golden_indicators labels, or the
  schema (they see evidence + question + the answer_space labels they must
  choose from).
- Every output row stores evidence_mode; headline analyses filter
  evidence_mode == "oracle_evidence".
- If a needed raw value is missing from the combined CSVs, the pack marks
  it NA — never fabricated. Packs failing to cover the question's golden
  indicators are flagged `coverage_incomplete` and reported.
