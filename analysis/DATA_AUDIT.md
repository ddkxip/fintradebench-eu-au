# Phase 1 data audit — Golden Seed 150

- rows: **150**, duplicate question_id: 0
- lanes: {'F': 50, 'FT': 50, 'T': 50}
- missing values: question=0, golden_indicators=0, response=0
- golden indicators per question: min=1, median=4, max=9
- indicators per lane (mean): {'F': 4.6, 'FT': 6.54, 'T': 1.8}
- response length (words): min=129, median=768, max=1821; by lane median: {'F': 787.0, 'FT': 747.0, 'T': 788.0}
- question length (words): median=12
- questions with explicit date mention: 150/150

## Indicator vocabulary (top 25)

- Cash Flow/Assets: 60
- Earnings/Price: 53
- Debt/Equity: 43
- ROE: 41
- Sales/Assets: 40
- ROA: 37
- RSI: 36
- Volatility: 32
- Debt/Assets: 28
- Dividend Yield: 25
- Book/Price: 24
- OBV: 24
- Return on Equity: 24
- Return on Assets: 24
- MA: 23
- Medium Term Momentum: 23
- MACD: 21
- EMA: 19
- Short Term Momentum: 14
- Long Term Mean Reversal: 13
- Max Return: 12
- One Day Reversal: 10
- Medium-term momentum: 9
- Short-term momentum: 7
- Long-term Mean Reversal: 5

(total distinct indicators: 25)

## Heuristic answer-type candidates (to be refined manually)

- **F**: {'yes_no_mixed': 39, 'choice_superlative': 5, 'unclassified': 4, 'company_choice': 1, 'open_summary_with_canonical_claim': 1}
- **FT**: {'yes_no_mixed': 50}
- **T**: {'yes_no_mixed': 32, 'choice_superlative': 15, 'unclassified': 3}

## Sample questions per lane (first 4 each)

### F
- `F1` [yes_no_mixed] (3 ind): As of September 2025, is Apple really as profitable as everyone says it is?
- `F10` [yes_no_mixed] (4 ind): Why is Broadcom’s stock price so high in 2025 despite being in semiconductors?
- `F11` [yes_no_mixed] (4 ind): As of August 2025, is Tesla financially stable enough to weather an economic downturn?
- `F12` [choice_superlative] (3 ind): As of September 2025, which tech giant has the strongest balance sheet: Apple, Microsoft, or Google?
### FT
- `FT1` [yes_no_mixed] (4 ind): As of August 2025, is Apple a good buy given its valuation and price trend?
- `FT10` [yes_no_mixed] (4 ind): Should I average down on my Qualcomm position that’s losing money in Q3 2025?
- `FT11` [yes_no_mixed] (6 ind): As of August 2025, is Costco worth buying for dividend income?
- `FT12` [yes_no_mixed] (5 ind): Has AMD’s momentum turned positive after the July 2025 selloff?
### T
- `T1` [yes_no_mixed] (3 ind): As of August 2025, which NASDAQ 100 stocks are in strong uptrends?
- `T10` [unclassified] (1 ind): What companies show unusual volume accumulation for the month of August 2025?
- `T11` [yes_no_mixed] (2 ind): Which NASDAQ stocks are seeing volume-confirmed breakdowns as of July 2025?
- `T12` [yes_no_mixed] (1 ind): Based on Q3 2025 data, what stocks have volume patterns suggesting institutional accumulation?