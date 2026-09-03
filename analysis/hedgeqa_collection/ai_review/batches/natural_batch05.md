# Blind review batch `natural_batch05`

25 items. Family: `none`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FTB_b6b11beb`

- **source**: fintradebench / FT30
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Why is Meta outperforming other tech giants in 2025, and is it sustainable?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=597.8650, last=710.5600, pct_change=18.85%
- Indicators: MA_20=752.7938, MACD=-7.5348, MACD_Signal=-1.4335, RSI=27.8812, EMA_20=745.0124, OBV=5272133438.0000, One_Day_Reversal=-0.0227, Max_Return_20D=0.0187, Momentum_5D=-0.0446, Momentum_20D=-0.0550, Mean_Reversal_60D=-0.0465, Short_Term_Reversal_1month=-0.0129, Medium_Term_Momentum_2month_to_12month=0.3276, Long_Term_Reversal_13month_to_60month=1.0340

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1231
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1767
  * F_Debt/Equity: 0.2676
  * F_Dividend Yield: 0.0009
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---

## Item 2/25 — `hqa_FTB_bcda6815`

- **source**: fintradebench / F1
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of September 2025, is Apple really as profitable as everyone says it is?

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

## Item 3/25 — `hqa_FTB_bd71b8fa`

- **source**: fintradebench / F30
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Meta's valuation make sense after its 2025 recovery?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=597.8650, last=710.5600, pct_change=18.85%
- Indicators: MA_20=752.7938, MACD=-7.5348, MACD_Signal=-1.4335, RSI=27.8812, EMA_20=745.0124, OBV=5272133438.0000, One_Day_Reversal=-0.0227, Max_Return_20D=0.0187, Momentum_5D=-0.0446, Momentum_20D=-0.0550, Mean_Reversal_60D=-0.0465, Short_Term_Reversal_1month=-0.0129, Medium_Term_Momentum_2month_to_12month=0.3276, Long_Term_Reversal_13month_to_60month=1.0340

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1231
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1767
  * F_Debt/Equity: 0.2676
  * F_Dividend Yield: 0.0009
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---

## Item 4/25 — `hqa_FTB_be3741f7`

- **source**: fintradebench / FT8
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: Should I buy Netflix after its Q2 2025 earnings beat?

**Oracle evidence**:

```
[NFLX] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=928.3800, last=1339.1300, pct_change=44.24%
- Indicators: MA_20=1246.0128, MACD=38.1530, MACD_Signal=31.0583, RSI=80.3536, EMA_20=1250.3667, OBV=2065289735.0000, One_Day_Reversal=0.0121, Max_Return_20D=0.0246, Momentum_5D=0.0683, Momentum_20D=0.1093, Mean_Reversal_60D=0.1775, Short_Term_Reversal_1month=0.0948, Medium_Term_Momentum_2month_to_12month=0.6610, Long_Term_Reversal_13month_to_60month=0.3871

[NFLX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0535
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

## Item 5/25 — `hqa_FTB_be575006`

- **source**: fintradebench / FT17
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of Q3 2025, is Intel finally turning around?

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

## Item 6/25 — `hqa_FTB_bfc189ce`

- **source**: fintradebench / F19
- **transformation_type**: `none`
- **answer_type**: `company_choice`
- **answer_space**: ['AMD', 'INTC', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Based on data for the first half of 2025, which is more financially stable: AMD or Intel?

**Oracle evidence**:

```
[AMD] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=120.6300, last=164.6700, pct_change=36.51%
- Indicators: MA_20=160.0480, MACD=0.6474, MACD_Signal=-0.3632, RSI=57.0681, EMA_20=162.1142, OBV=6598997671.0000, One_Day_Reversal=-0.0298, Max_Return_20D=0.0349, Momentum_5D=0.0327, Momentum_20D=0.0895, Mean_Reversal_60D=0.0022, Short_Term_Reversal_1month=0.0469, Medium_Term_Momentum_2month_to_12month=0.0911, Long_Term_Reversal_13month_to_60month=0.8691

[INTC] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=20.2200, last=36.8300, pct_change=82.15%
- Indicators: MA_20=29.7190, MACD=3.2805, MACD_Signal=2.5576, RSI=78.3631, EMA_20=31.0653, OBV=12318654235.0000, One_Day_Reversal=-0.0126, Max_Return_20D=0.2277, Momentum_5D=0.0375, Momentum_20D=0.5039, Mean_Reversal_60D=0.4727, Short_Term_Reversal_1month=0.5542, Medium_Term_Momentum_2month_to_12month=-0.1102, Long_Term_Reversal_13month_to_60month=-0.5225

[AMD] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0188
  * F_Book/Price: 0.2835
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1040
  * F_Debt/Assets: 0.0519
  * F_Debt/Equity: 0.0651
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0098
  * F_Return on Equity: 0.0123

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0106
  * F_Book/Price: 1.0070
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0668
  * F_Debt/Assets: 0.2609
  * F_Debt/Equity: 0.4762
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0024
  * F_Return on Equity: -0.0082
```

---

## Item 7/25 — `hqa_FTB_c14e66f4`

- **source**: fintradebench / T8
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['APP', 'TSLA', 'COST', 'TTD', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: What NASDAQ 100 names are experiencing momentum divergence in Q2 2025?

**Oracle evidence**:

```
[APP] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=282.7000, last=350.0800, pct_change=23.83%
- Indicators: MA_20=369.9935, MACD=-4.4432, MACD_Signal=0.9631, RSI=38.4716, EMA_20=356.1022, OBV=339490594.0000, One_Day_Reversal=0.0488, Max_Return_20D=0.0488, Momentum_5D=0.0438, Momentum_20D=-0.1092, Mean_Reversal_60D=0.0756, Short_Term_Reversal_1month=-0.1447, Medium_Term_Momentum_2month_to_12month=2.5895, Long_Term_Reversal_13month_to_60month=NA

[TSLA] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=268.4600, last=317.6600, pct_change=18.33%
- Indicators: MA_20=323.8915, MACD=2.0777, MACD_Signal=3.6928, RSI=54.0783, EMA_20=325.5706, OBV=21709977362.0000, One_Day_Reversal=-0.0184, Max_Return_20D=0.0823, Momentum_5D=-0.0890, Momentum_20D=-0.0831, Mean_Reversal_60D=0.0514, Short_Term_Reversal_1month=-0.0932, Medium_Term_Momentum_2month_to_12month=0.4871, Long_Term_Reversal_13month_to_60month=1.6838

[COST] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=951.8720, last=988.5910, pct_change=3.86%
- Indicators: MA_20=1001.6943, MACD=-6.1147, MACD_Signal=-4.4984, RSI=42.1546, EMA_20=995.3925, OBV=484512014.0000, One_Day_Reversal=0.0049, Max_Return_20D=0.0247, Momentum_5D=-0.0145, Momentum_20D=-0.0483, Mean_Reversal_60D=-0.0048, Short_Term_Reversal_1month=-0.0276, Medium_Term_Momentum_2month_to_12month=0.1619, Long_Term_Reversal_13month_to_60month=1.9013

[TTD] Trading/Price Data 2025-04-01 -> 2025-06-30
- AdjClose: first=57.1000, last=71.9900, pct_change=26.08%
- Indicators: MA_20=70.8590, MACD=0.0813, MACD_Signal=0.3805, RSI=51.0851, EMA_20=70.3102, OBV=1765454098.0000, One_Day_Reversal=0.0384, Max_Return_20D=0.0431, Momentum_5D=0.0453, Momentum_20D=-0.0429, Mean_Reversal_60D=0.1232, Short_Term_Reversal_1month=-0.0989, Medium_Term_Momentum_2month_to_12month=-0.4405, Long_Term_Reversal_13month_to_60month=1.3108

[APP] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1457
  * F_Book/Price: 0.0064
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2600
  * F_Debt/Assets: 0.6501
  * F_Debt/Equity: 6.4474
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.1128
  * F_Return on Equity: 0.8631

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

[TTD] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0511
  * F_Book/Price: 0.1010
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1080
  * F_Debt/Assets: 0.0587
  * F_Debt/Equity: 0.1233
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0070
  * F_Return on Equity: 0.0208
```

---

## Item 8/25 — `hqa_FTB_c63078f2`

- **source**: fintradebench / FT21
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['buy_now', 'wait', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Should I buy Texas Instruments in August 2025 or wait?

**Oracle evidence**:

```
[TXN] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=180.8600, last=202.4800, pct_change=11.95%
- Indicators: MA_20=195.3610, MACD=2.5792, MACD_Signal=1.1239, RSI=85.3484, EMA_20=198.9782, OBV=2984454189.0000, One_Day_Reversal=-0.0079, Max_Return_20D=0.0504, Momentum_5D=-0.0174, Momentum_20D=0.1195, Mean_Reversal_60D=0.0131, Short_Term_Reversal_1month=0.0850, Medium_Term_Momentum_2month_to_12month=0.0216, Long_Term_Reversal_13month_to_60month=0.5876

[TXN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0532
  * F_Book/Price: 0.0869
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1273
  * F_Debt/Assets: 0.4020
  * F_Debt/Equity: 0.8561
  * F_Dividend Yield: 0.0066
  * F_Return on Assets: 0.0391
  * F_Return on Equity: 0.0770
```

---

## Item 9/25 — `hqa_FTB_c71bc114`

- **source**: fintradebench / F37
- **transformation_type**: `none`
- **answer_type**: `company_choice`
- **answer_space**: ['NFLX', 'AAPL', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: As of Q3 2025, which generates more cash per dollar of assets: Netflix or Apple?

**Oracle evidence**:

```
[NFLX] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=1293.6000, last=1198.9200, pct_change=-7.32%
- Indicators: MA_20=1220.7565, MACD=-3.7012, MACD_Signal=-1.3637, RSI=36.8071, EMA_20=1214.4898, OBV=2034961664.0000, One_Day_Reversal=-0.0062, Max_Return_20D=0.0255, Momentum_5D=-0.0160, Momentum_20D=-0.0125, Mean_Reversal_60D=-0.0139, Short_Term_Reversal_1month=-0.0203, Medium_Term_Momentum_2month_to_12month=0.6297, Long_Term_Reversal_13month_to_60month=0.4783

[AAPL] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=207.5820, last=254.6300, pct_change=22.66%
- Indicators: MA_20=243.1245, MACD=7.4966, MACD_Signal=6.5587, RSI=82.7684, EMA_20=244.6472, OBV=159375777216.0000, One_Day_Reversal=0.0008, Max_Return_20D=0.0431, Momentum_5D=0.0008, Momentum_20D=0.1084, Mean_Reversal_60D=0.1227, Short_Term_Reversal_1month=0.0940, Medium_Term_Momentum_2month_to_12month=-0.0845, Long_Term_Reversal_13month_to_60month=1.1782

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

## Item 10/25 — `hqa_FTB_c99d1421`

- **source**: fintradebench / F36
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does AMD use its assets more efficiently after its recent investments, as of August 2025?

**Oracle evidence**:

```
[AMD] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=171.7000, last=162.6300, pct_change=-5.28%
- Indicators: MA_20=170.8580, MACD=1.3069, MACD_Signal=3.3803, RSI=40.8043, EMA_20=167.7138, OBV=6644358999.0000, One_Day_Reversal=-0.0353, Max_Return_20D=0.0569, Momentum_5D=-0.0306, Momentum_20D=-0.0528, Mean_Reversal_60D=0.0641, Short_Term_Reversal_1month=-0.0609, Medium_Term_Momentum_2month_to_12month=-0.0956, Long_Term_Reversal_13month_to_60month=0.6821

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

## Item 11/25 — `hqa_FTB_ce7df44f`

- **source**: fintradebench / F41
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['KHC', 'CCEP', 'CSCO', 'TXN', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: As of September 2025, which NASDAQ stocks are best for dividend income investors?

**Oracle evidence**:

```
[KHC] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=26.0200, last=26.0400, pct_change=0.08%
- Indicators: MA_20=26.3560, MACD=-0.2596, MACD_Signal=-0.2419, RSI=43.1767, EMA_20=26.3436, OBV=-276117404.0000, One_Day_Reversal=0.0132, Max_Return_20D=0.0350, Momentum_5D=-0.0196, Momentum_20D=0.0008, Mean_Reversal_60D=-0.0341, Short_Term_Reversal_1month=-0.0569, Medium_Term_Momentum_2month_to_12month=-0.1790, Long_Term_Reversal_13month_to_60month=0.4627

[CCEP] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=87.4300, last=90.4100, pct_change=3.41%
- Indicators: MA_20=89.3395, MACD=-0.3508, MACD_Signal=-0.6125, RSI=57.5213, EMA_20=89.7342, OBV=835671052.0000, One_Day_Reversal=0.0092, Max_Return_20D=0.0198, Momentum_5D=0.0115, Momentum_20D=0.0341, Mean_Reversal_60D=-0.0240, Short_Term_Reversal_1month=0.0086, Medium_Term_Momentum_2month_to_12month=0.2605, Long_Term_Reversal_13month_to_60month=1.3441

[CSCO] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=67.3930, last=68.0090, pct_change=0.91%
- Indicators: MA_20=67.1701, MACD=-0.0265, MACD_Signal=-0.0984, RSI=51.8937, EMA_20=67.3454, OBV=21144503056.0000, One_Day_Reversal=0.0103, Max_Return_20D=0.0142, Momentum_5D=0.0130, Momentum_20D=0.0091, Mean_Reversal_60D=0.0046, Short_Term_Reversal_1month=-0.0246, Medium_Term_Momentum_2month_to_12month=0.3239, Long_Term_Reversal_13month_to_60month=0.4992

[TXN] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=199.8100, last=183.7300, pct_change=-8.05%
- Indicators: MA_20=183.4768, MACD=-2.8452, MACD_Signal=-3.4579, RSI=49.4420, EMA_20=184.9752, OBV=2947237743.0000, One_Day_Reversal=0.0027, Max_Return_20D=0.0150, Momentum_5D=0.0093, Momentum_20D=-0.0805, Mean_Reversal_60D=-0.0522, Short_Term_Reversal_1month=-0.1022, Medium_Term_Momentum_2month_to_12month=-0.1084, Long_Term_Reversal_13month_to_60month=0.7398

[KHC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0148
  * F_Book/Price: 1.3639
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0779
  * F_Debt/Assets: 0.2600
  * F_Debt/Equity: 0.5112
  * F_Dividend Yield: 0.0156
  * F_Return on Assets: -0.0897
  * F_Return on Equity: -0.1728

[CCEP] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.2223
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: NA
  * F_Debt/Assets: NA
  * F_Debt/Equity: NA
  * F_Dividend Yield: 0.0102
  * F_Return on Assets: 0.0990
  * F_Return on Equity: 0.3919

[CSCO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0346
  * F_Book/Price: 0.1722
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1200
  * F_Debt/Assets: 0.2297
  * F_Debt/Equity: 0.5997
  * F_Dividend Yield: 0.0060
  * F_Return on Assets: 0.0213
  * F_Return on Equity: 0.0553

[TXN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0532
  * F_Book/Price: 0.0869
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1273
  * F_Debt/Assets: 0.4020
  * F_Debt/Equity: 0.8561
  * F_Dividend Yield: 0.0066
  * F_Return on Assets: 0.0391
  * F_Return on Equity: 0.0770
```

---

## Item 12/25 — `hqa_FTB_cf81aaf3`

- **source**: fintradebench / FT4
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is NVIDIA's pullback in July 2025 a buying opportunity?

**Oracle evidence**:

```
[NVDA] Trading/Price Data 2025-07-01 -> 2025-07-31
- AdjClose: first=153.2910, last=177.8600, pct_change=16.03%
- Indicators: MA_20=169.3334, MACD=7.0918, MACD_Signal=7.1708, RSI=70.0158, EMA_20=169.0433, OBV=166262412151.0000, One_Day_Reversal=-0.0078, Max_Return_20D=0.0404, Momentum_5D=0.0238, Momentum_20D=0.1311, Mean_Reversal_60D=0.1931, Short_Term_Reversal_1month=0.1347, Medium_Term_Momentum_2month_to_12month=0.2112, Long_Term_Reversal_13month_to_60month=11.1981

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
```

---

## Item 13/25 — `hqa_FTB_d1f8a434`

- **source**: fintradebench / FT7
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Has Meta bottomed out after its decline in August 2025?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=749.4960, last=738.1940, pct_change=-1.51%
- Indicators: MA_20=762.0427, MACD=3.7517, MACD_Signal=8.5422, RSI=39.2329, EMA_20=750.9329, OBV=5351470452.0000, One_Day_Reversal=-0.0165, Max_Return_20D=0.0351, Momentum_5D=-0.0213, Momentum_20D=-0.0151, Mean_Reversal_60D=0.0144, Short_Term_Reversal_1month=0.0804, Medium_Term_Momentum_2month_to_12month=0.3902, Long_Term_Reversal_13month_to_60month=0.7196

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1050
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1681
  * F_Debt/Equity: 0.2541
  * F_Dividend Yield: 0.0007
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---

## Item 14/25 — `hqa_FTB_d23c5d4b`

- **source**: fintradebench / F9
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Meta's profitability justify its stock price as of September 2025?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=734.6060, last=734.3800, pct_change=-0.03%
- Indicators: MA_20=756.8771, MACD=-1.1662, MACD_Signal=2.7573, RSI=40.7982, EMA_20=754.4453, OBV=5297292105.0000, One_Day_Reversal=-0.0121, Max_Return_20D=0.0187, Momentum_5D=-0.0278, Momentum_20D=-0.0003, Mean_Reversal_60D=-0.0151, Short_Term_Reversal_1month=-0.0096, Medium_Term_Momentum_2month_to_12month=0.3654, Long_Term_Reversal_13month_to_60month=1.0889

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1050
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1681
  * F_Debt/Equity: 0.2541
  * F_Dividend Yield: 0.0007
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---

## Item 15/25 — `hqa_FTB_d25b3c9a`

- **source**: fintradebench / T50
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['LRCX', 'AMAT', 'MU', 'WBD', 'APP', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: What companies offer the best combination of momentum and stability as of Q3 2025?

**Oracle evidence**:

```
[LRCX] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=96.6140, last=133.9000, pct_change=38.59%
- Indicators: MA_20=118.8435, MACD=7.7814, MACD_Signal=6.9254, RSI=88.9329, EMA_20=121.2499, OBV=8871501719.0000, One_Day_Reversal=0.0214, Max_Return_20D=0.0766, Momentum_5D=0.0170, Momentum_20D=0.3828, Mean_Reversal_60D=0.2608, Short_Term_Reversal_1month=0.2619, Medium_Term_Momentum_2month_to_12month=0.1284, Long_Term_Reversal_13month_to_60month=1.7085

[AMAT] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=183.2330, last=204.7400, pct_change=11.74%
- Indicators: MA_20=181.1330, MACD=9.3339, MACD_Signal=6.1013, RSI=91.2211, EMA_20=187.5483, OBV=3346167758.0000, One_Day_Reversal=-0.0010, Max_Return_20D=0.0653, Momentum_5D=0.0193, Momentum_20D=0.2994, Mean_Reversal_60D=0.1333, Short_Term_Reversal_1month=0.2401, Medium_Term_Momentum_2month_to_12month=-0.1346, Long_Term_Reversal_13month_to_60month=2.5373

[MU] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=120.7000, last=167.2180, pct_change=38.54%
- Indicators: MA_20=151.6601, MACD=10.4632, MACD_Signal=10.5797, RSI=73.2311, EMA_20=152.4584, OBV=3878675015.0000, One_Day_Reversal=0.0209, Max_Return_20D=0.0755, Momentum_5D=0.0055, Momentum_20D=0.4122, Mean_Reversal_60D=0.3031, Short_Term_Reversal_1month=0.3434, Medium_Term_Momentum_2month_to_12month=-0.0020, Long_Term_Reversal_13month_to_60month=1.0007

[WBD] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=10.9400, last=19.5300, pct_change=78.52%
- Indicators: MA_20=16.9198, MACD=1.8634, MACD_Signal=1.7952, RSI=79.2714, EMA_20=17.4104, OBV=1490185159.0000, One_Day_Reversal=0.0353, Max_Return_20D=0.2895, Momentum_5D=-0.0015, Momentum_20D=0.6807, Mean_Reversal_60D=0.4159, Short_Term_Reversal_1month=0.5649, Medium_Term_Momentum_2month_to_12month=0.5867, Long_Term_Reversal_13month_to_60month=-0.6383

[APP] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=336.6900, last=718.5400, pct_change=113.41%
- Indicators: MA_20=602.7590, MACD=59.7779, MACD_Signal=53.4882, RSI=90.6737, EMA_20=610.1187, OBV=570095031.0000, One_Day_Reversal=0.0087, Max_Return_20D=0.1159, Momentum_5D=0.1034, Momentum_20D=0.4916, Mean_Reversal_60D=0.5313, Short_Term_Reversal_1month=0.4726, Medium_Term_Momentum_2month_to_12month=2.0492, Long_Term_Reversal_13month_to_60month=NA

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

[AMAT] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0770
  * F_Book/Price: 0.1287
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2134
  * F_Debt/Assets: 0.1830
  * F_Debt/Equity: 0.3211
  * F_Dividend Yield: 0.0024
  * F_Return on Assets: 0.0457
  * F_Return on Equity: 0.0928

[MU] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0588
  * F_Book/Price: 0.4691
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1186
  * F_Debt/Assets: 0.2059
  * F_Debt/Equity: 0.3181
  * F_Dividend Yield: 0.0012
  * F_Return on Assets: 0.0267
  * F_Return on Equity: 0.0397

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
```

---

## Item 16/25 — `hqa_FTB_d2ece491`

- **source**: fintradebench / T1
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['APP', 'INTC', 'IDXX', 'SHOP', 'AAPL', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: As of August 2025, which NASDAQ 100 stocks are in strong uptrends?

**Oracle evidence**:

```
[APP] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=379.1700, last=478.5900, pct_change=26.22%
- Indicators: MA_20=438.8540, MACD=23.1724, MACD_Signal=20.3591, RSI=54.1691, EMA_20=437.0793, OBV=400182328.0000, One_Day_Reversal=-0.0107, Max_Return_20D=0.1197, Momentum_5D=0.0836, Momentum_20D=0.2622, Mean_Reversal_60D=0.2399, Short_Term_Reversal_1month=0.3315, Medium_Term_Momentum_2month_to_12month=2.7286, Long_Term_Reversal_13month_to_60month=NA

[INTC] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=19.3100, last=24.3500, pct_change=26.10%
- Indicators: MA_20=22.8380, MACD=0.8447, MACD_Signal=0.6705, RSI=66.5474, EMA_20=23.4277, OBV=11546836250.0000, One_Day_Reversal=-0.0233, Max_Return_20D=0.0738, Momentum_5D=-0.0181, Momentum_20D=0.2610, Mean_Reversal_60D=0.0979, Short_Term_Reversal_1month=0.2257, Medium_Term_Momentum_2month_to_12month=0.1385, Long_Term_Reversal_13month_to_60month=-0.3055

[IDXX] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=535.5400, last=647.0900, pct_change=20.83%
- Indicators: MA_20=647.0595, MACD=18.2344, MACD_Signal=22.1065, RSI=46.5673, EMA_20=631.1284, OBV=340329402.0000, One_Day_Reversal=0.0001, Max_Return_20D=0.2749, Momentum_5D=0.0024, Momentum_20D=0.2083, Mean_Reversal_60D=0.1314, Short_Term_Reversal_1month=0.1310, Medium_Term_Momentum_2month_to_12month=0.1245, Long_Term_Reversal_13month_to_60month=0.2417

[SHOP] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=118.6000, last=141.2800, pct_change=19.12%
- Indicators: MA_20=142.1475, MACD=3.6480, MACD_Signal=4.7856, RSI=39.4505, EMA_20=138.7732, OBV=1703226522.0000, One_Day_Reversal=-0.0018, Max_Return_20D=0.2197, Momentum_5D=-0.0058, Momentum_20D=0.1912, Mean_Reversal_60D=0.1347, Short_Term_Reversal_1month=0.1506, Medium_Term_Momentum_2month_to_12month=0.5117, Long_Term_Reversal_13month_to_60month=-0.4009

[AAPL] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=202.1490, last=232.1400, pct_change=14.84%
- Indicators: MA_20=225.6994, MACD=4.8495, MACD_Signal=4.9517, RSI=60.3940, EMA_20=225.7436, OBV=159172072249.0000, One_Day_Reversal=-0.0018, Max_Return_20D=0.0509, Momentum_5D=0.0192, Momentum_20D=0.1484, Mean_Reversal_60D=0.0915, Short_Term_Reversal_1month=0.1137, Medium_Term_Momentum_2month_to_12month=-0.0855, Long_Term_Reversal_13month_to_60month=0.7723

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

## Item 17/25 — `hqa_FTB_d3935030`

- **source**: fintradebench / F31
- **transformation_type**: `none`
- **answer_type**: `company_choice`
- **answer_space**: ['AMZN', 'WMT', 'COST', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: As of mid-2025, which company uses its assets most efficiently: Amazon, Walmart, or Costco?

**Oracle evidence**:

```
[AMZN] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=220.2200, last=219.5100, pct_change=-0.32%
- Indicators: MA_20=226.6545, MACD=-2.2740, MACD_Signal=-1.4041, RSI=31.0070, EMA_20=224.4044, OBV=48983516465.0000, One_Day_Reversal=-0.0130, Max_Return_20D=0.0151, Momentum_5D=-0.0012, Momentum_20D=-0.0552, Mean_Reversal_60D=-0.0314, Short_Term_Reversal_1month=-0.0158, Medium_Term_Momentum_2month_to_12month=0.1546, Long_Term_Reversal_13month_to_60month=0.1247

[WMT] No data file available.

[COST] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=906.3930, last=915.3800, pct_change=0.99%
- Indicators: MA_20=945.0855, MACD=-11.6167, MACD_Signal=-8.2359, RSI=25.1611, EMA_20=937.7305, OBV=462953619.0000, One_Day_Reversal=-0.0015, Max_Return_20D=0.0115, Momentum_5D=-0.0006, Momentum_20D=-0.0499, Mean_Reversal_60D=-0.0396, Short_Term_Reversal_1month=-0.0348, Medium_Term_Momentum_2month_to_12month=0.0810, Long_Term_Reversal_13month_to_60month=1.7534

[AMZN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0477
  * F_Book/Price: 0.1427
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2458
  * F_Debt/Assets: 0.2071
  * F_Debt/Equity: 0.4356
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0270
  * F_Return on Equity: 0.0656

[WMT] No data file available.

[COST] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0458
  * F_Book/Price: 0.0602
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.8469
  * F_Debt/Assets: 0.1084
  * F_Debt/Equity: 0.3016
  * F_Dividend Yield: 0.0011
  * F_Return on Assets: 0.0260
  * F_Return on Equity: 0.0778
```

---

## Item 18/25 — `hqa_FTB_d78b28a8`

- **source**: fintradebench / F33
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Tesla's manufacturing as efficient as its September 2025 valuation suggests?

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

## Item 19/25 — `hqa_FTB_d83f425e`

- **source**: fintradebench / F16
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Does Amazon's massive infrastructure create financial risk in the current 2025 economy?

**Oracle evidence**:

```
[AMZN] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=220.2200, last=219.5100, pct_change=-0.32%
- Indicators: MA_20=226.6545, MACD=-2.2740, MACD_Signal=-1.4041, RSI=31.0070, EMA_20=224.4044, OBV=48983516465.0000, One_Day_Reversal=-0.0130, Max_Return_20D=0.0151, Momentum_5D=-0.0012, Momentum_20D=-0.0552, Mean_Reversal_60D=-0.0314, Short_Term_Reversal_1month=-0.0158, Medium_Term_Momentum_2month_to_12month=0.1546, Long_Term_Reversal_13month_to_60month=0.1247

[AMZN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0477
  * F_Book/Price: 0.1427
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2458
  * F_Debt/Assets: 0.2071
  * F_Debt/Equity: 0.4356
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0270
  * F_Return on Equity: 0.0656
```

---

## Item 20/25 — `hqa_FTB_db4e96c8`

- **source**: fintradebench / FT6
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of 2025, is Google a safe investment for my retirement portfolio?

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

## Item 21/25 — `hqa_FTB_dbf9cd4e`

- **source**: fintradebench / T21
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['INTC', 'MU', 'LRCX', 'AMAT', 'MRVL', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: Which stocks are furthest from their moving averages as of September 15, 2025?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=20.2200, last=36.8300, pct_change=82.15%
- Indicators: MA_20=29.7190, MACD=3.2805, MACD_Signal=2.5576, RSI=78.3631, EMA_20=31.0653, OBV=12318654235.0000, One_Day_Reversal=-0.0126, Max_Return_20D=0.2277, Momentum_5D=0.0375, Momentum_20D=0.5039, Mean_Reversal_60D=0.4727, Short_Term_Reversal_1month=0.5542, Medium_Term_Momentum_2month_to_12month=-0.1102, Long_Term_Reversal_13month_to_60month=-0.5225

[MU] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=87.0780, last=187.8300, pct_change=115.70%
- Indicators: MA_20=160.6320, MACD=13.2406, MACD_Signal=11.5245, RSI=74.4705, EMA_20=160.8200, OBV=3974871225.0000, One_Day_Reversal=0.0228, Max_Return_20D=0.0886, Momentum_5D=0.1950, Momentum_20D=0.4306, Mean_Reversal_60D=0.4296, Short_Term_Reversal_1month=0.5478, Medium_Term_Momentum_2month_to_12month=0.0924, Long_Term_Reversal_13month_to_60month=0.9727

[LRCX] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=71.9040, last=145.8100, pct_change=102.78%
- Indicators: MA_20=125.5980, MACD=9.8058, MACD_Signal=8.0966, RSI=86.4618, EMA_20=127.4862, OBV=8894497635.0000, One_Day_Reversal=-0.0080, Max_Return_20D=0.0766, Momentum_5D=0.1362, Momentum_20D=0.4192, Mean_Reversal_60D=0.3443, Short_Term_Reversal_1month=0.5069, Medium_Term_Momentum_2month_to_12month=0.2226, Long_Term_Reversal_13month_to_60month=1.5526

[AMAT] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=162.5630, last=217.5300, pct_change=33.81%
- Indicators: MA_20=190.2140, MACD=12.2001, MACD_Signal=8.8017, RSI=87.0901, EMA_20=195.8631, OBV=3360763179.0000, One_Day_Reversal=-0.0271, Max_Return_20D=0.0653, Momentum_5D=0.0667, Momentum_20D=0.3366, Mean_Reversal_60D=0.1962, Short_Term_Reversal_1month=0.4310, Medium_Term_Momentum_2month_to_12month=-0.0848, Long_Term_Reversal_13month_to_60month=2.4375

[MRVL] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=113.2800, last=86.2200, pct_change=-23.89%
- Indicators: MA_20=75.4815, MACD=3.9430, MACD_Signal=2.5188, RSI=89.4582, EMA_20=78.1765, OBV=1285251688.0000, One_Day_Reversal=0.0002, Max_Return_20D=0.0733, Momentum_5D=0.0367, Momentum_20D=0.3614, Mean_Reversal_60D=0.1620, Short_Term_Reversal_1month=0.3834, Medium_Term_Momentum_2month_to_12month=0.0935, Long_Term_Reversal_13month_to_60month=0.9461

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0106
  * F_Book/Price: 1.0070
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0668
  * F_Debt/Assets: 0.2609
  * F_Debt/Equity: 0.4762
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0024
  * F_Return on Equity: -0.0082

[MU] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0540
  * F_Book/Price: 0.4691
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1186
  * F_Debt/Assets: 0.2047
  * F_Debt/Equity: 0.3075
  * F_Dividend Yield: 0.0012
  * F_Return on Assets: 0.0267
  * F_Return on Equity: 0.0397

[LRCX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0655
  * F_Book/Price: 0.0950
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2364
  * F_Debt/Assets: 0.2246
  * F_Debt/Equity: 0.4715
  * F_Dividend Yield: 0.0032
  * F_Return on Assets: 0.0707
  * F_Return on Equity: 0.1518

[AMAT] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0467
  * F_Book/Price: 0.1313
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2134
  * F_Debt/Assets: 0.1862
  * F_Debt/Equity: 0.3302
  * F_Dividend Yield: 0.0024
  * F_Return on Assets: 0.0457
  * F_Return on Equity: 0.0928

[MRVL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0224
  * F_Book/Price: 0.2091
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0947
  * F_Debt/Assets: 0.2114
  * F_Debt/Equity: 0.3179
  * F_Dividend Yield: 0.0008
  * F_Return on Assets: 0.0114
  * F_Return on Equity: 0.0135
```

---

## Item 22/25 — `hqa_FTB_e105af3a`

- **source**: fintradebench / T19
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['INTC', 'MRVL', 'TRI', 'COST', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: As of September 1, 2025, which NASDAQ stocks are prime candidates for mean reversion trades?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=20.2200, last=36.8300, pct_change=82.15%
- Indicators: MA_20=29.7190, MACD=3.2805, MACD_Signal=2.5576, RSI=78.3631, EMA_20=31.0653, OBV=12318654235.0000, One_Day_Reversal=-0.0126, Max_Return_20D=0.2277, Momentum_5D=0.0375, Momentum_20D=0.5039, Mean_Reversal_60D=0.4727, Short_Term_Reversal_1month=0.5542, Medium_Term_Momentum_2month_to_12month=-0.1102, Long_Term_Reversal_13month_to_60month=-0.5225

[MRVL] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=113.2800, last=86.2200, pct_change=-23.89%
- Indicators: MA_20=75.4815, MACD=3.9430, MACD_Signal=2.5188, RSI=89.4582, EMA_20=78.1765, OBV=1285251688.0000, One_Day_Reversal=0.0002, Max_Return_20D=0.0733, Momentum_5D=0.0367, Momentum_20D=0.3614, Mean_Reversal_60D=0.1620, Short_Term_Reversal_1month=0.3834, Medium_Term_Momentum_2month_to_12month=0.0935, Long_Term_Reversal_13month_to_60month=0.9461

[TRI] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=159.7230, last=152.9800, pct_change=-4.22%
- Indicators: MA_20=163.2300, MACD=-6.6021, MACD_Signal=-5.9912, RSI=15.7143, EMA_20=161.8057, OBV=64318493.0000, One_Day_Reversal=0.0096, Max_Return_20D=0.0177, Momentum_5D=-0.0257, Momentum_20D=-0.1240, Mean_Reversal_60D=-0.1493, Short_Term_Reversal_1month=-0.1464, Medium_Term_Momentum_2month_to_12month=0.1877, Long_Term_Reversal_13month_to_60month=1.2837

[COST] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=906.3930, last=915.3800, pct_change=0.99%
- Indicators: MA_20=945.0855, MACD=-11.6167, MACD_Signal=-8.2359, RSI=25.1611, EMA_20=937.7305, OBV=462953619.0000, One_Day_Reversal=-0.0015, Max_Return_20D=0.0115, Momentum_5D=-0.0006, Momentum_20D=-0.0499, Mean_Reversal_60D=-0.0396, Short_Term_Reversal_1month=-0.0348, Medium_Term_Momentum_2month_to_12month=0.0810, Long_Term_Reversal_13month_to_60month=1.7534

[INTC] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0106
  * F_Book/Price: 1.0070
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0668
  * F_Debt/Assets: 0.2609
  * F_Debt/Equity: 0.4762
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0024
  * F_Return on Equity: -0.0082

[MRVL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0224
  * F_Book/Price: 0.2091
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0947
  * F_Debt/Assets: 0.2114
  * F_Debt/Equity: 0.3179
  * F_Dividend Yield: 0.0008
  * F_Return on Assets: 0.0114
  * F_Return on Equity: 0.0135

[TRI] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.1580
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: NA
  * F_Debt/Assets: NA
  * F_Debt/Equity: NA
  * F_Dividend Yield: 0.0032
  * F_Return on Assets: 0.1162
  * F_Return on Equity: 0.1746

[COST] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0458
  * F_Book/Price: 0.0602
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.8469
  * F_Debt/Assets: 0.1084
  * F_Debt/Equity: 0.3016
  * F_Dividend Yield: 0.0011
  * F_Return on Assets: 0.0260
  * F_Return on Equity: 0.0778
```

---

## Item 23/25 — `hqa_FTB_e67cda66`

- **source**: fintradebench / F18
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of September 2025, is Meta's debt from acquisitions manageable?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=734.6060, last=734.3800, pct_change=-0.03%
- Indicators: MA_20=756.8771, MACD=-1.1662, MACD_Signal=2.7573, RSI=40.7982, EMA_20=754.4453, OBV=5297292105.0000, One_Day_Reversal=-0.0121, Max_Return_20D=0.0187, Momentum_5D=-0.0278, Momentum_20D=-0.0003, Mean_Reversal_60D=-0.0151, Short_Term_Reversal_1month=-0.0096, Medium_Term_Momentum_2month_to_12month=0.3654, Long_Term_Reversal_13month_to_60month=1.0889

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1050
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1681
  * F_Debt/Equity: 0.2541
  * F_Dividend Yield: 0.0007
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---

## Item 24/25 — `hqa_FTB_e86f8f22`

- **source**: fintradebench / F25
- **transformation_type**: `none`
- **answer_type**: `company_choice`
- **answer_space**: ['NFLX', 'DIS', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: As of September 2025, which offers better value: Netflix or Disney?

**Oracle evidence**:

```
[NFLX] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=1214.1100, last=1198.9200, pct_change=-1.25%
- Indicators: MA_20=1220.7565, MACD=-3.7012, MACD_Signal=-1.3637, RSI=36.8071, EMA_20=1214.4898, OBV=2034961664.0000, One_Day_Reversal=-0.0062, Max_Return_20D=0.0255, Momentum_5D=-0.0160, Momentum_20D=-0.0125, Mean_Reversal_60D=-0.0139, Short_Term_Reversal_1month=-0.0203, Medium_Term_Momentum_2month_to_12month=0.6297, Long_Term_Reversal_13month_to_60month=0.4783

[DIS] No data file available.

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

[DIS] No data file available.
```

---

## Item 25/25 — `hqa_FTB_e8cac668`

- **source**: fintradebench / F20
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of August 2025, should I be concerned about Meta's acquisition debt?

**Oracle evidence**:

```
[META] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=749.4960, last=738.1940, pct_change=-1.51%
- Indicators: MA_20=762.0427, MACD=3.7517, MACD_Signal=8.5422, RSI=39.2329, EMA_20=750.9329, OBV=5351470452.0000, One_Day_Reversal=-0.0165, Max_Return_20D=0.0351, Momentum_5D=-0.0213, Momentum_20D=-0.0151, Mean_Reversal_60D=0.0144, Short_Term_Reversal_1month=0.0804, Medium_Term_Momentum_2month_to_12month=0.3902, Long_Term_Reversal_13month_to_60month=0.7196

[META] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0867
  * F_Book/Price: 0.1050
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1612
  * F_Debt/Assets: 0.1681
  * F_Debt/Equity: 0.2541
  * F_Dividend Yield: 0.0007
  * F_Return on Assets: 0.0695
  * F_Return on Equity: 0.1042
```

---
