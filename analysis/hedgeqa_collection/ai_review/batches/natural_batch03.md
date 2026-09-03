# Blind review batch `natural_batch03`

25 items. Family: `none`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FTB_30cfebd4`

- **source**: fintradebench / FT43
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['wait_for_confirmation', 'buy_on_fundamentals', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: In Q3 2025, should I wait for technical confirmation before buying Adobe, or are fundamentals sufficient?

**Oracle evidence**:

```
[ADBE] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=392.1000, last=352.7500, pct_change=-10.04%
- Indicators: MA_20=355.2830, MACD=0.6681, MACD_Signal=0.6693, RSI=52.4383, EMA_20=356.5277, OBV=494552281.0000, One_Day_Reversal=-0.0186, Max_Return_20D=0.0278, Momentum_5D=-0.0250, Momentum_20D=0.0206, Mean_Reversal_60D=-0.0125, Short_Term_Reversal_1month=0.0154, Medium_Term_Momentum_2month_to_12month=-0.3060, Long_Term_Reversal_13month_to_60month=0.2071

[ADBE] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0780
  * F_Book/Price: 0.0646
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2090
  * F_Debt/Assets: 0.2335
  * F_Debt/Equity: 0.5733
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0584
  * F_Return on Equity: 0.1286
```

---

## Item 2/25 — `hqa_FTB_38645c6c`

- **source**: fintradebench / F11
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of August 2025, is Tesla financially stable enough to weather an economic downturn?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=302.6300, last=333.8700, pct_change=10.32%
- Indicators: MA_20=332.5705, MACD=5.9422, MACD_Signal=5.1811, RSI=46.8187, EMA_20=334.0421, OBV=21793428285.0000, One_Day_Reversal=-0.0350, Max_Return_20D=0.0622, Momentum_5D=-0.0181, Momentum_20D=0.1032, Mean_Reversal_60D=0.0357, Short_Term_Reversal_1month=0.0844, Medium_Term_Momentum_2month_to_12month=0.4374, Long_Term_Reversal_13month_to_60month=0.7285

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0198
  * F_Book/Price: 0.0756
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1750
  * F_Debt/Assets: 0.0562
  * F_Debt/Equity: 0.0925
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0059
  * F_Return on Equity: 0.0164
```

---

## Item 3/25 — `hqa_FTB_3a7f797e`

- **source**: fintradebench / F13
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Should I worry about Netflix's debt levels in mid-2025?

**Oracle evidence**:

```
[NFLX] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=886.7300, last=1153.3200, pct_change=30.06%
- Indicators: MA_20=1208.7200, MACD=-12.5304, MACD_Signal=-5.5975, RSI=34.4556, EMA_20=1200.7885, OBV=2023028611.0000, One_Day_Reversal=-0.0079, Max_Return_20D=0.0233, Momentum_5D=-0.0473, Momentum_20D=-0.0728, Mean_Reversal_60D=-0.0471, Short_Term_Reversal_1month=-0.0519, Medium_Term_Momentum_2month_to_12month=0.6256, Long_Term_Reversal_13month_to_60month=0.4294

[NFLX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0456
  * F_Book/Price: 0.0605
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2024
  * F_Debt/Assets: 0.2883
  * F_Debt/Equity: 0.6250
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0597
  * F_Return on Equity: 0.1273
```

---

## Item 4/25 — `hqa_FTB_3ba66418`

- **source**: fintradebench / F15
- **transformation_type**: `none`
- **answer_type**: `graded_judgment`
- **answer_space**: ['sound', 'mixed', 'weak', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of Q3 2025, how financially sound is Qualcomm compared to other chip companies?

**Oracle evidence**:

```
[QCOM] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=158.5170, last=166.3600, pct_change=4.95%
- Indicators: MA_20=164.3044, MACD=3.0596, MACD_Signal=3.1730, RSI=63.1991, EMA_20=164.8822, OBV=2548869655.0000, One_Day_Reversal=0.0064, Max_Return_20D=0.0237, Momentum_5D=-0.0187, Momentum_20D=0.0536, Mean_Reversal_60D=0.0535, Short_Term_Reversal_1month=0.0337, Medium_Term_Momentum_2month_to_12month=-0.1357, Long_Term_Reversal_13month_to_60month=0.7029

[QCOM] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0524
  * F_Book/Price: 0.3114
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1889
  * F_Debt/Assets: 0.2695
  * F_Debt/Equity: 0.5435
  * F_Dividend Yield: 0.0056
  * F_Return on Assets: 0.0464
  * F_Return on Equity: 0.1028
```

---

## Item 5/25 — `hqa_FTB_46b2b9ab`

- **source**: fintradebench / FT40
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of September 2025, is Netflix's streaming dominance translating into sustainable financial metrics?

**Oracle evidence**:

```
[NFLX] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=1214.1100, last=1198.9200, pct_change=-1.25%
- Indicators: MA_20=1220.7565, MACD=-3.7012, MACD_Signal=-1.3637, RSI=36.8071, EMA_20=1214.4898, OBV=2034961664.0000, One_Day_Reversal=-0.0062, Max_Return_20D=0.0255, Momentum_5D=-0.0160, Momentum_20D=-0.0125, Mean_Reversal_60D=-0.0139, Short_Term_Reversal_1month=-0.0203, Medium_Term_Momentum_2month_to_12month=0.6297, Long_Term_Reversal_13month_to_60month=0.4783

[NFLX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0456
  * F_Book/Price: 0.0438
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2086
  * F_Debt/Assets: 0.2722
  * F_Debt/Equity: 0.5792
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0636
  * F_Return on Equity: 0.1328
```

---

## Item 6/25 — `hqa_FTB_47429988`

- **source**: fintradebench / FT32
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['attractive_stability', 'underperformance_ahead', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Apple's stability attractive in the volatile 2025 market, or does it signal underperformance ahead?

**Oracle evidence**:

```
[AAPL] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=243.0040, last=258.0200, pct_change=6.18%
- Indicators: MA_20=245.7575, MACD=7.4241, MACD_Signal=6.9845, RSI=79.6440, EMA_20=247.8386, OBV=159516277009.0000, One_Day_Reversal=0.0035, Max_Return_20D=0.0431, Momentum_5D=0.0100, Momentum_20D=0.0765, Mean_Reversal_60D=0.1262, Short_Term_Reversal_1month=0.0782, Medium_Term_Momentum_2month_to_12month=-0.0999, Long_Term_Reversal_13month_to_60month=1.0383

[AAPL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0841
  * F_Book/Price: 0.0205
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2879
  * F_Debt/Assets: 0.2964
  * F_Debt/Equity: 1.4699
  * F_Dividend Yield: 0.0012
  * F_Return on Assets: 0.0748
  * F_Return on Equity: 0.3536
```

---

## Item 7/25 — `hqa_FTB_48b061cd`

- **source**: fintradebench / FT28
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Tesla's robotaxi opportunity justify its September 2025 valuation metrics?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=329.3600, last=444.7200, pct_change=35.03%
- Indicators: MA_20=399.2190, MACD=26.9521, MACD_Signal=24.5006, RSI=78.4302, EMA_20=406.7866, OBV=22958088131.0000, One_Day_Reversal=0.0034, Max_Return_20D=0.0736, Momentum_5D=0.0443, Momentum_20D=0.3503, Mean_Reversal_60D=0.2723, Short_Term_Reversal_1month=0.2810, Medium_Term_Momentum_2month_to_12month=0.2126, Long_Term_Reversal_13month_to_60month=0.6501

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0198
  * F_Book/Price: 0.0756
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1750
  * F_Debt/Assets: 0.0562
  * F_Debt/Equity: 0.0925
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0059
  * F_Return on Equity: 0.0164
```

---

## Item 8/25 — `hqa_FTB_495324ab`

- **source**: fintradebench / FT12
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Has AMD's momentum turned positive after the July 2025 selloff?

**Oracle evidence**:

```
[AMD] Trading/Price Data 2025-07-01 -> 2025-07-31
- AdjClose: first=136.1100, last=176.3100, pct_change=29.53%
- Indicators: MA_20=156.2365, MACD=11.5268, MACD_Signal=10.0163, RSI=81.1030, EMA_20=158.8977, OBV=6855505879.0000, One_Day_Reversal=-0.0178, Max_Return_20D=0.0641, Momentum_5D=0.0875, Momentum_20D=0.2728, Mean_Reversal_60D=0.3360, Short_Term_Reversal_1month=0.2650, Medium_Term_Momentum_2month_to_12month=-0.2077, Long_Term_Reversal_13month_to_60month=1.2978

[AMD] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0195
  * F_Book/Price: 0.2558
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1027
  * F_Debt/Assets: 0.0519
  * F_Debt/Equity: 0.0651
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0193
  * F_Return on Equity: 0.0132
```

---

## Item 9/25 — `hqa_FTB_4fb8ad99`

- **source**: fintradebench / FT39
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Should I be concerned about Alphabet's multiple compression in 2025 despite strong earnings?

**Oracle evidence**:

```
[GOOGL] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=188.8070, last=245.3500, pct_change=29.95%
- Indicators: MA_20=245.9905, MACD=7.0959, MACD_Signal=9.3381, RSI=36.5780, EMA_20=241.5893, OBV=29434712013.0000, One_Day_Reversal=-0.0014, Max_Return_20D=0.0449, Momentum_5D=-0.0048, Momentum_20D=0.0450, Mean_Reversal_60D=0.1416, Short_Term_Reversal_1month=0.0661, Medium_Term_Momentum_2month_to_12month=0.1699, Long_Term_Reversal_13month_to_60month=1.2427

[GOOGL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0760
  * F_Book/Price: 0.1690
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1921
  * F_Debt/Assets: 0.0501
  * F_Debt/Equity: 0.0694
  * F_Dividend Yield: 0.0012
  * F_Return on Assets: 0.0573
  * F_Return on Equity: 0.0872
```

---

## Item 10/25 — `hqa_FTB_54b6da2c`

- **source**: fintradebench / FT33
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['buying_opportunity', 'structural_challenges', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Apple's lack of AI momentum in 2025 indicate a buying opportunity or structural challenges?

**Oracle evidence**:

```
[AAPL] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=243.0040, last=258.0200, pct_change=6.18%
- Indicators: MA_20=245.7575, MACD=7.4241, MACD_Signal=6.9845, RSI=79.6440, EMA_20=247.8386, OBV=159516277009.0000, One_Day_Reversal=0.0035, Max_Return_20D=0.0431, Momentum_5D=0.0100, Momentum_20D=0.0765, Mean_Reversal_60D=0.1262, Short_Term_Reversal_1month=0.0782, Medium_Term_Momentum_2month_to_12month=-0.0999, Long_Term_Reversal_13month_to_60month=1.0383

[AAPL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0841
  * F_Book/Price: 0.0205
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2879
  * F_Debt/Assets: 0.2964
  * F_Debt/Equity: 1.4699
  * F_Dividend Yield: 0.0012
  * F_Return on Assets: 0.0748
  * F_Return on Equity: 0.3536
```

---

## Item 11/25 — `hqa_FTB_54bc7248`

- **source**: fintradebench / FT34
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: As of September 2025, how does Microsoft balance enterprise stability with AI growth exposure?

**Oracle evidence**:

```
[MSFT] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=505.1200, last=517.9500, pct_change=2.54%
- Indicators: MA_20=508.0940, MACD=1.5800, MACD_Signal=0.6328, RSI=65.4211, EMA_20=510.4329, OBV=14636827777.0000, One_Day_Reversal=0.0065, Max_Return_20D=0.0186, Momentum_5D=0.0171, Momentum_20D=0.0254, Mean_Reversal_60D=0.0142, Short_Term_Reversal_1month=0.0097, Medium_Term_Momentum_2month_to_12month=0.2442, Long_Term_Reversal_13month_to_60month=1.1358

[MSFT] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0689
  * F_Book/Price: 0.0929
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1235
  * F_Debt/Assets: 0.0979
  * F_Debt/Equity: 0.1764
  * F_Dividend Yield: 0.0017
  * F_Return on Assets: 0.0507
  * F_Return on Equity: 0.0890
```

---

## Item 12/25 — `hqa_FTB_5895e72d`

- **source**: fintradebench / T14
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['IDXX', 'SHOP', 'MRVL', 'AXON', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: What companies had the biggest single-day moves during August 2025?

**Oracle evidence**:

```
[IDXX] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=535.5400, last=647.0900, pct_change=20.83%
- Indicators: MA_20=647.0595, MACD=18.2344, MACD_Signal=22.1065, RSI=46.5673, EMA_20=631.1284, OBV=340329402.0000, One_Day_Reversal=0.0001, Max_Return_20D=0.2749, Momentum_5D=0.0024, Momentum_20D=0.2083, Mean_Reversal_60D=0.1314, Short_Term_Reversal_1month=0.1310, Medium_Term_Momentum_2month_to_12month=0.1245, Long_Term_Reversal_13month_to_60month=0.2417

[SHOP] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=118.6000, last=141.2800, pct_change=19.12%
- Indicators: MA_20=142.1475, MACD=3.6480, MACD_Signal=4.7856, RSI=39.4505, EMA_20=138.7732, OBV=1703226522.0000, One_Day_Reversal=-0.0018, Max_Return_20D=0.2197, Momentum_5D=-0.0058, Momentum_20D=0.1912, Mean_Reversal_60D=0.1347, Short_Term_Reversal_1month=0.1506, Medium_Term_Momentum_2month_to_12month=0.5117, Long_Term_Reversal_13month_to_60month=-0.4009

[MRVL] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=74.4500, last=62.8650, pct_change=-15.56%
- Indicators: MA_20=74.8822, MACD=-0.9831, MACD_Signal=-0.1111, RSI=27.2885, EMA_20=73.7962, OBV=1009242573.0000, One_Day_Reversal=-0.1860, Max_Return_20D=0.0326, Momentum_5D=-0.1388, Momentum_20D=-0.1556, Mean_Reversal_60D=-0.1473, Short_Term_Reversal_1month=-0.0552, Medium_Term_Momentum_2month_to_12month=0.0964, Long_Term_Reversal_13month_to_60month=0.8913

[AXON] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=742.4700, last=747.2900, pct_change=0.65%
- Indicators: MA_20=785.8965, MACD=-1.7805, MACD_Signal=1.0549, RSI=32.8068, EMA_20=770.5796, OBV=1264002540.0000, One_Day_Reversal=-0.0443, Max_Return_20D=0.1641, Momentum_5D=-0.0247, Momentum_20D=0.0065, Mean_Reversal_60D=-0.0332, Short_Term_Reversal_1month=0.0445, Medium_Term_Momentum_2month_to_12month=1.1335, Long_Term_Reversal_13month_to_60month=2.7117

[IDXX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0558
  * F_Book/Price: 0.0339
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.3331
  * F_Debt/Assets: 0.3637
  * F_Debt/Equity: 0.8304
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0897
  * F_Return on Equity: 0.1935

[SHOP] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.0812
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: NA
  * F_Debt/Assets: NA
  * F_Debt/Equity: NA
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.1607
  * F_Return on Equity: 0.1930

[MRVL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0224
  * F_Book/Price: 0.2091
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0974
  * F_Debt/Assets: 0.2170
  * F_Debt/Equity: 0.3328
  * F_Dividend Yield: 0.0008
  * F_Return on Assets: 0.0119
  * F_Return on Equity: 0.0144

[AXON] Fundamentals (median in window):
  * F_Cash Flow/Assets: -0.0148
  * F_Book/Price: 0.0420
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1076
  * F_Debt/Assets: 0.3301
  * F_Debt/Equity: 0.7508
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0002
  * F_Return on Equity: 0.0155
```

---

## Item 13/25 — `hqa_FTB_599b11e3`

- **source**: fintradebench / T9
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['TSLA', 'INTC', 'LRCX', 'NVDA', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: As of September 2025, which stocks have the strongest volume confirmation for their price moves?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=329.3600, last=444.7200, pct_change=35.03%
- Indicators: MA_20=399.2190, MACD=26.9521, MACD_Signal=24.5006, RSI=78.4302, EMA_20=406.7866, OBV=22958088131.0000, One_Day_Reversal=0.0034, Max_Return_20D=0.0736, Momentum_5D=0.0443, Momentum_20D=0.3503, Mean_Reversal_60D=0.2723, Short_Term_Reversal_1month=0.2810, Medium_Term_Momentum_2month_to_12month=0.2126, Long_Term_Reversal_13month_to_60month=0.6501

[INTC] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=24.2100, last=33.5500, pct_change=38.58%
- Indicators: MA_20=27.8705, MACD=2.7412, MACD_Signal=1.9872, RSI=73.8328, EMA_20=29.0855, OBV=12132002275.0000, One_Day_Reversal=-0.0270, Max_Return_20D=0.2277, Momentum_5D=0.1435, Momentum_20D=0.3858, Mean_Reversal_60D=0.3775, Short_Term_Reversal_1month=0.3831, Medium_Term_Momentum_2month_to_12month=-0.1722, Long_Term_Reversal_13month_to_60month=-0.5419

[LRCX] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=96.8340, last=133.9000, pct_change=38.28%
- Indicators: MA_20=118.8435, MACD=7.7814, MACD_Signal=6.9254, RSI=88.9329, EMA_20=121.2499, OBV=8871501719.0000, One_Day_Reversal=0.0214, Max_Return_20D=0.0766, Momentum_5D=0.0170, Momentum_20D=0.3828, Mean_Reversal_60D=0.2608, Short_Term_Reversal_1month=0.2619, Medium_Term_Momentum_2month_to_12month=0.1284, Long_Term_Reversal_13month_to_60month=1.7085

[NVDA] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=170.7700, last=186.5800, pct_change=9.26%
- Indicators: MA_20=175.9891, MACD=1.8439, MACD_Signal=0.9646, RSI=62.2164, EMA_20=177.9510, OBV=166277664172.0000, One_Day_Reversal=0.0260, Max_Return_20D=0.0393, Momentum_5D=0.0457, Momentum_20D=0.0926, Mean_Reversal_60D=0.0634, Short_Term_Reversal_1month=0.0094, Medium_Term_Momentum_2month_to_12month=0.4343, Long_Term_Reversal_13month_to_60month=9.6108

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0198
  * F_Book/Price: 0.0756
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1750
  * F_Debt/Assets: 0.0562
  * F_Debt/Equity: 0.0925
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0059
  * F_Return on Equity: 0.0164

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0106
  * F_Book/Price: 0.9856
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0668
  * F_Debt/Assets: 0.2636
  * F_Debt/Equity: 0.4800
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0174
  * F_Return on Equity: -0.0267

[LRCX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1197
  * F_Book/Price: 0.0799
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2423
  * F_Debt/Assets: 0.2101
  * F_Debt/Equity: 0.4547
  * F_Dividend Yield: 0.0024
  * F_Return on Assets: 0.0840
  * F_Return on Equity: 0.1870

[NVDA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1092
  * F_Book/Price: 0.0237
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.3321
  * F_Debt/Assets: 0.0732
  * F_Debt/Equity: 0.1028
  * F_Dividend Yield: 0.0001
  * F_Return on Assets: 0.2131
  * F_Return on Equity: 0.3338
```

---

## Item 14/25 — `hqa_FTB_5a0e1efb`

- **source**: fintradebench / F34
- **transformation_type**: `none`
- **answer_type**: `graded_judgment`
- **answer_space**: ['more_efficient', 'similar', 'less_efficient', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Based on Q2 2025 data, how efficiently does Google use its assets compared to other tech giants?

**Oracle evidence**:

```
[GOOGL] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=156.7420, last=176.0720, pct_change=12.33%
- Indicators: MA_20=172.3539, MACD=1.8757, MACD_Signal=1.9537, RSI=50.1959, EMA_20=171.7834, OBV=28798280724.0000, One_Day_Reversal=-0.0129, Max_Return_20D=0.0325, Momentum_5D=0.0668, Momentum_20D=0.0274, Mean_Reversal_60D=0.0761, Short_Term_Reversal_1month=0.0370, Medium_Term_Momentum_2month_to_12month=-0.1258, Long_Term_Reversal_13month_to_60month=1.3906

[GOOGL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0760
  * F_Book/Price: 0.1818
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1898
  * F_Debt/Assets: 0.0475
  * F_Debt/Equity: 0.0654
  * F_Dividend Yield: 0.0013
  * F_Return on Assets: 0.0573
  * F_Return on Equity: 0.1083
```

---

## Item 15/25 — `hqa_FTB_5d6ed0fa`

- **source**: fintradebench / FT48
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Costco's defensive retail model justify its premium Q3 2025 valuation metrics?

**Oracle evidence**:

```
[COST] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=984.6160, last=925.6300, pct_change=-5.99%
- Indicators: MA_20=951.0690, MACD=-9.2855, MACD_Signal=-5.5140, RSI=34.5433, EMA_20=945.1895, OBV=469978714.0000, One_Day_Reversal=0.0096, Max_Return_20D=0.0117, Momentum_5D=-0.0190, Momentum_20D=-0.0140, Mean_Reversal_60D=-0.0320, Short_Term_Reversal_1month=-0.0297, Medium_Term_Momentum_2month_to_12month=0.0463, Long_Term_Reversal_13month_to_60month=1.8450

[COST] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0458
  * F_Book/Price: 0.0602
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.8374
  * F_Debt/Assets: 0.1084
  * F_Debt/Equity: 0.3016
  * F_Dividend Yield: 0.0011
  * F_Return on Assets: 0.0260
  * F_Return on Equity: 0.0778
```

---

## Item 16/25 — `hqa_FTB_5db8c06c`

- **source**: fintradebench / T27
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['MU', 'WBD', 'APP', 'LRCX', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: Which NASDAQ 100 stock has the best risk-reward setup for September 2025?

**Oracle evidence**:

```
[MU] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=118.4080, last=167.2180, pct_change=41.22%
- Indicators: MA_20=151.6601, MACD=10.4632, MACD_Signal=10.5797, RSI=73.2311, EMA_20=152.4584, OBV=3878675015.0000, One_Day_Reversal=0.0209, Max_Return_20D=0.0755, Momentum_5D=0.0055, Momentum_20D=0.4122, Mean_Reversal_60D=0.3031, Short_Term_Reversal_1month=0.3434, Medium_Term_Momentum_2month_to_12month=-0.0020, Long_Term_Reversal_13month_to_60month=1.0007

[WBD] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=11.6200, last=19.5300, pct_change=68.07%
- Indicators: MA_20=16.9198, MACD=1.8634, MACD_Signal=1.7952, RSI=79.2714, EMA_20=17.4104, OBV=1490185159.0000, One_Day_Reversal=0.0353, Max_Return_20D=0.2895, Momentum_5D=-0.0015, Momentum_20D=0.6807, Mean_Reversal_60D=0.4159, Short_Term_Reversal_1month=0.5649, Medium_Term_Momentum_2month_to_12month=0.5867, Long_Term_Reversal_13month_to_60month=-0.6383

[APP] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=481.7300, last=718.5400, pct_change=49.16%
- Indicators: MA_20=602.7590, MACD=59.7779, MACD_Signal=53.4882, RSI=90.6737, EMA_20=610.1187, OBV=570095031.0000, One_Day_Reversal=0.0087, Max_Return_20D=0.1159, Momentum_5D=0.1034, Momentum_20D=0.4916, Mean_Reversal_60D=0.5313, Short_Term_Reversal_1month=0.4726, Medium_Term_Momentum_2month_to_12month=2.0492, Long_Term_Reversal_13month_to_60month=NA

[LRCX] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=96.8340, last=133.9000, pct_change=38.28%
- Indicators: MA_20=118.8435, MACD=7.7814, MACD_Signal=6.9254, RSI=88.9329, EMA_20=121.2499, OBV=8871501719.0000, One_Day_Reversal=0.0214, Max_Return_20D=0.0766, Momentum_5D=0.0170, Momentum_20D=0.3828, Mean_Reversal_60D=0.2608, Short_Term_Reversal_1month=0.2619, Medium_Term_Momentum_2month_to_12month=0.1284, Long_Term_Reversal_13month_to_60month=1.7085

[MU] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0692
  * F_Book/Price: 0.3973
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1367
  * F_Debt/Assets: 0.1845
  * F_Debt/Equity: 0.2821
  * F_Dividend Yield: 0.0010
  * F_Return on Assets: 0.0423
  * F_Return on Equity: 0.0645

[WBD] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0097
  * F_Book/Price: 1.2710
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0965
  * F_Debt/Assets: 0.3404
  * F_Debt/Equity: 0.9273
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0011
  * F_Return on Equity: 0.0436

[APP] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1296
  * F_Book/Price: 0.0098
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2112
  * F_Debt/Assets: 0.5891
  * F_Debt/Equity: 3.0082
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.1489
  * F_Return on Equity: 0.8270

[LRCX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1197
  * F_Book/Price: 0.0799
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2423
  * F_Debt/Assets: 0.2101
  * F_Debt/Equity: 0.4547
  * F_Dividend Yield: 0.0024
  * F_Return on Assets: 0.0840
  * F_Return on Equity: 0.1870
```

---

## Item 17/25 — `hqa_FTB_624fddfe`

- **source**: fintradebench / F17
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: Why do dividend investors like Cisco as of July 2025, despite its slow growth?

**Oracle evidence**:

```
[CSCO] Trading/Price Data 2025-07-01 -> 2025-07-31
- AdjClose: first=68.2820, last=67.6720, pct_change=-0.89%
- Indicators: MA_20=67.8863, MACD=0.4761, MACD_Signal=0.6687, RSI=51.2775, EMA_20=67.5540, OBV=21252243518.0000, One_Day_Reversal=-0.0028, Max_Return_20D=0.0174, Momentum_5D=-0.0031, Momentum_20D=-0.0016, Mean_Reversal_60D=0.0392, Short_Term_Reversal_1month=-0.0101, Medium_Term_Momentum_2month_to_12month=0.3421, Long_Term_Reversal_13month_to_60month=0.1475

[CSCO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0339
  * F_Book/Price: 0.2045
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1181
  * F_Debt/Assets: 0.2444
  * F_Debt/Equity: 0.6374
  * F_Dividend Yield: 0.0072
  * F_Return on Assets: 0.0223
  * F_Return on Equity: 0.0543
```

---

## Item 18/25 — `hqa_FTB_664ec26b`

- **source**: fintradebench / F39
- **transformation_type**: `none`
- **answer_type**: `graded_judgment`
- **answer_space**: ['efficient', 'moderate', 'inefficient', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: How efficiently does Broadcom generate in 2025?

**Oracle evidence**:

```
[AVGO] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=230.3180, last=338.3700, pct_change=46.91%
- Indicators: MA_20=344.0610, MACD=4.8461, MACD_Signal=7.5509, RSI=23.3497, EMA_20=334.7088, OBV=6585520063.0000, One_Day_Reversal=0.0006, Max_Return_20D=0.0977, Momentum_5D=0.0115, Momentum_20D=0.0122, Mean_Reversal_60D=0.0852, Short_Term_Reversal_1month=0.1203, Medium_Term_Momentum_2month_to_12month=0.7632, Long_Term_Reversal_13month_to_60month=3.8942

[AVGO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0398
  * F_Book/Price: 0.0682
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0911
  * F_Debt/Assets: 0.4026
  * F_Debt/Equity: 0.9540
  * F_Dividend Yield: 0.0027
  * F_Return on Assets: 0.0335
  * F_Return on Equity: 0.0712
```

---

## Item 19/25 — `hqa_FTB_6b974835`

- **source**: fintradebench / F7
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of Q3 2025, is Intel still a profitable investment despite losing market share?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=22.8500, last=33.5500, pct_change=46.83%
- Indicators: MA_20=27.8705, MACD=2.7412, MACD_Signal=1.9872, RSI=73.8328, EMA_20=29.0855, OBV=12132002275.0000, One_Day_Reversal=-0.0270, Max_Return_20D=0.2277, Momentum_5D=0.1435, Momentum_20D=0.3858, Mean_Reversal_60D=0.3775, Short_Term_Reversal_1month=0.3831, Medium_Term_Momentum_2month_to_12month=-0.1722, Long_Term_Reversal_13month_to_60month=-0.5419

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0106
  * F_Book/Price: 0.9856
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0668
  * F_Debt/Assets: 0.2636
  * F_Debt/Equity: 0.4800
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0174
  * F_Return on Equity: -0.0267
```

---

## Item 20/25 — `hqa_FTB_6f71b24d`

- **source**: fintradebench / FT2
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: In September 2025, should I invest in Tesla given its volatility and financial health?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=329.3600, last=444.7200, pct_change=35.03%
- Indicators: MA_20=399.2190, MACD=26.9521, MACD_Signal=24.5006, RSI=78.4302, EMA_20=406.7866, OBV=22958088131.0000, One_Day_Reversal=0.0034, Max_Return_20D=0.0736, Momentum_5D=0.0443, Momentum_20D=0.3503, Mean_Reversal_60D=0.2723, Short_Term_Reversal_1month=0.2810, Medium_Term_Momentum_2month_to_12month=0.2126, Long_Term_Reversal_13month_to_60month=0.6501

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0198
  * F_Book/Price: 0.0756
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1750
  * F_Debt/Assets: 0.0562
  * F_Debt/Equity: 0.0925
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0059
  * F_Return on Equity: 0.0164
```

---

## Item 21/25 — `hqa_FTB_6fa9f26d`

- **source**: fintradebench / FT5
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['hold', 'sell', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: Should I hold or sell my Amazon shares after the Q2 2025 rally?

**Oracle evidence**:

```
[AMZN] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=192.1700, last=219.3900, pct_change=14.16%
- Indicators: MA_20=213.0185, MACD=3.9935, MACD_Signal=3.7965, RSI=53.1586, EMA_20=212.5956, OBV=48749660098.0000, One_Day_Reversal=-0.0175, Max_Return_20D=0.0285, Momentum_5D=0.0524, Momentum_20D=0.0701, Mean_Reversal_60D=0.1079, Short_Term_Reversal_1month=0.0908, Medium_Term_Momentum_2month_to_12month=-0.0321, Long_Term_Reversal_13month_to_60month=0.3077

[AMZN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0265
  * F_Book/Price: 0.1515
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2420
  * F_Debt/Assets: 0.2071
  * F_Debt/Equity: 0.4356
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0248
  * F_Return on Equity: 0.0656
```

---

## Item 22/25 — `hqa_FTB_7199c7e7`

- **source**: fintradebench / FT20
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Apple a good defensive stock for September 2025?

**Oracle evidence**:

```
[AAPL] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=229.7200, last=254.6300, pct_change=10.84%
- Indicators: MA_20=243.1245, MACD=7.4966, MACD_Signal=6.5587, RSI=82.7684, EMA_20=244.6472, OBV=159375777216.0000, One_Day_Reversal=0.0008, Max_Return_20D=0.0431, Momentum_5D=0.0008, Momentum_20D=0.1084, Mean_Reversal_60D=0.1227, Short_Term_Reversal_1month=0.0940, Medium_Term_Momentum_2month_to_12month=-0.0845, Long_Term_Reversal_13month_to_60month=1.1782

[AAPL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0841
  * F_Book/Price: 0.0220
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2837
  * F_Debt/Assets: 0.3068
  * F_Debt/Equity: 1.5449
  * F_Dividend Yield: 0.0013
  * F_Return on Assets: 0.0711
  * F_Return on Equity: 0.3536
```

---

## Item 23/25 — `hqa_FTB_74433c22`

- **source**: fintradebench / FT29
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of mid-2025, is Tesla showing signs of fundamental deterioration beneath its technical strength?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=379.2800, last=429.8300, pct_change=13.33%
- Indicators: MA_20=414.3105, MACD=24.3235, MACD_Signal=25.1774, RSI=56.4847, EMA_20=415.6050, OBV=22786013286.0000, One_Day_Reversal=-0.0142, Max_Return_20D=0.0736, Momentum_5D=-0.0240, Momentum_20D=0.2251, Mean_Reversal_60D=0.2055, Short_Term_Reversal_1month=0.3050, Medium_Term_Momentum_2month_to_12month=0.1965, Long_Term_Reversal_13month_to_60month=0.5250

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0198
  * F_Book/Price: 0.0756
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1750
  * F_Debt/Assets: 0.0602
  * F_Debt/Equity: 0.0998
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0059
  * F_Return on Equity: 0.0164
```

---

## Item 24/25 — `hqa_FTB_77a9fd58`

- **source**: fintradebench / FT1
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: As of August 2025, is Apple a good buy given its valuation and price trend?

**Oracle evidence**:

```
[AAPL] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=202.1490, last=232.1400, pct_change=14.84%
- Indicators: MA_20=225.6994, MACD=4.8495, MACD_Signal=4.9517, RSI=60.3940, EMA_20=225.7436, OBV=159172072249.0000, One_Day_Reversal=-0.0018, Max_Return_20D=0.0509, Momentum_5D=0.0192, Momentum_20D=0.1484, Mean_Reversal_60D=0.0915, Short_Term_Reversal_1month=0.1137, Medium_Term_Momentum_2month_to_12month=-0.0855, Long_Term_Reversal_13month_to_60month=0.7723

[AAPL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0841
  * F_Book/Price: 0.0220
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2837
  * F_Debt/Assets: 0.3068
  * F_Debt/Equity: 1.5449
  * F_Dividend Yield: 0.0013
  * F_Return on Assets: 0.0711
  * F_Return on Equity: 0.3536
```

---

## Item 25/25 — `hqa_FTB_7b872c89`

- **source**: fintradebench / T17
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['NVDA', 'TSLA', 'MRVL', 'INTC', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: Which companies show the most extreme daily reversals, based on June 2025 trading?

**Oracle evidence**:

```
[NVDA] Trading/Price Data 2025-06-01 -> 2025-06-30
- AdjClose: first=137.3630, last=157.9810, pct_change=15.01%
- Indicators: MA_20=145.6833, MACD=6.5487, MACD_Signal=5.8152, RSI=77.3772, EMA_20=145.9598, OBV=165567677626.0000, One_Day_Reversal=0.0015, Max_Return_20D=0.0433, Momentum_5D=0.0959, Momentum_20D=0.1693, Mean_Reversal_60D=0.2503, Short_Term_Reversal_1month=0.1702, Medium_Term_Momentum_2month_to_12month=-0.1373, Long_Term_Reversal_13month_to_60month=10.2985

[TSLA] Trading/Price Data 2025-06-01 -> 2025-06-30
- AdjClose: first=342.6900, last=317.6600, pct_change=-7.30%
- Indicators: MA_20=323.8915, MACD=2.0777, MACD_Signal=3.6928, RSI=54.0783, EMA_20=325.5706, OBV=21709977362.0000, One_Day_Reversal=-0.0184, Max_Return_20D=0.0823, Momentum_5D=-0.0890, Momentum_20D=-0.0831, Mean_Reversal_60D=0.0514, Short_Term_Reversal_1month=-0.0932, Medium_Term_Momentum_2month_to_12month=0.4871, Long_Term_Reversal_13month_to_60month=1.6838

[MRVL] Trading/Price Data 2025-06-01 -> 2025-06-30
- AdjClose: first=61.4190, last=77.3360, pct_change=25.92%
- Indicators: MA_20=70.5422, MACD=3.7327, MACD_Signal=3.0685, RSI=63.8683, EMA_20=71.5106, OBV=1083422038.0000, One_Day_Reversal=0.0031, Max_Return_20D=0.0709, Momentum_5D=0.0935, Momentum_20D=0.2859, Mean_Reversal_60D=0.2404, Short_Term_Reversal_1month=0.1946, Medium_Term_Momentum_2month_to_12month=-0.1377, Long_Term_Reversal_13month_to_60month=1.2740

[INTC] Trading/Price Data 2025-06-01 -> 2025-06-30
- AdjClose: first=19.7400, last=22.4000, pct_change=13.48%
- Indicators: MA_20=21.1060, MACD=0.4666, MACD_Signal=0.2586, RSI=61.8812, EMA_20=21.4422, OBV=11416612567.0000, One_Day_Reversal=-0.0128, Max_Return_20D=0.0781, Momentum_5D=0.0571, Momentum_20D=0.1458, Mean_Reversal_60D=0.0833, Short_Term_Reversal_1month=0.1139, Medium_Term_Momentum_2month_to_12month=-0.3296, Long_Term_Reversal_13month_to_60month=-0.4286

[NVDA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.2189
  * F_Book/Price: 0.0310
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.3518
  * F_Debt/Assets: 0.0797
  * F_Debt/Equity: 0.1191
  * F_Dividend Yield: 0.0001
  * F_Return on Assets: 0.1833
  * F_Return on Equity: 0.2824

[TSLA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0172
  * F_Book/Price: 0.0895
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1545
  * F_Debt/Assets: 0.0602
  * F_Debt/Equity: 0.0998
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0024
  * F_Return on Equity: 0.0060

[MRVL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0166
  * F_Book/Price: 0.2477
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0947
  * F_Debt/Assets: 0.2114
  * F_Debt/Equity: 0.3179
  * F_Dividend Yield: 0.0010
  * F_Return on Assets: 0.0111
  * F_Return on Equity: 0.0132

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0042
  * F_Book/Price: 1.0070
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0659
  * F_Debt/Assets: 0.2609
  * F_Debt/Equity: 0.4713
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0024
  * F_Return on Equity: -0.0082
```

---
