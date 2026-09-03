# Blind review batch `natural_batch04`

25 items. Family: `none`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FTB_7c1b95b5`

- **source**: fintradebench / FT45
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['contrarian_value_play', 'value_trap', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: As of September 2025, should I view Intel as a contrarian value play or a value trap?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=24.2100, last=33.5500, pct_change=38.58%
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

## Item 2/25 — `hqa_FTB_7d9b0eea`

- **source**: fintradebench / F4
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Nvidia's profitability sustainable with its valuation in September 2025?

**Oracle evidence**:

```
[NVDA] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=170.7700, last=186.5800, pct_change=9.26%
- Indicators: MA_20=175.9891, MACD=1.8439, MACD_Signal=0.9646, RSI=62.2164, EMA_20=177.9510, OBV=166277664172.0000, One_Day_Reversal=0.0260, Max_Return_20D=0.0393, Momentum_5D=0.0457, Momentum_20D=0.0926, Mean_Reversal_60D=0.0634, Short_Term_Reversal_1month=0.0094, Medium_Term_Momentum_2month_to_12month=0.4343, Long_Term_Reversal_13month_to_60month=9.6108

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

## Item 3/25 — `hqa_FTB_7dbce4b0`

- **source**: fintradebench / F10
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: Why is Broadcom's stock price so high in 2025 despite being in semiconductors?

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

## Item 4/25 — `hqa_FTB_7ffcdb70`

- **source**: fintradebench / FT11
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: As of August 2025, is Costco worth buying for dividend income?

**Oracle evidence**:

```
[COST] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=952.5200, last=943.3200, pct_change=-0.97%
- Indicators: MA_20=966.7985, MACD=-4.8056, MACD_Signal=-1.2076, RSI=29.6978, EMA_20=959.9048, OBV=469874955.0000, One_Day_Reversal=-0.0017, Max_Return_20D=0.0264, Momentum_5D=-0.0159, Momentum_20D=-0.0097, Mean_Reversal_60D=-0.0280, Short_Term_Reversal_1month=0.0202, Medium_Term_Momentum_2month_to_12month=0.0888, Long_Term_Reversal_13month_to_60month=1.5565

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

## Item 5/25 — `hqa_FTB_8315fbdd`

- **source**: fintradebench / T47
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['CMCSA', 'TEAM', 'KDP', 'TRI', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: Which companies are showing decreasing momentum quality in Q3 2025?

**Oracle evidence**:

```
[CMCSA] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=35.6190, last=31.0880, pct_change=-12.72%
- Indicators: MA_20=32.2015, MACD=-0.5498, MACD_Signal=-0.4593, RSI=13.4719, EMA_20=31.9275, OBV=2195417369.0000, One_Day_Reversal=-0.0022, Max_Return_20D=0.0044, Momentum_5D=-0.0063, Momentum_20D=-0.0794, Mean_Reversal_60D=-0.0581, Short_Term_Reversal_1month=-0.0620, Medium_Term_Momentum_2month_to_12month=-0.1620, Long_Term_Reversal_13month_to_60month=-0.0196

[TEAM] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=207.7100, last=159.7000, pct_change=-23.11%
- Indicators: MA_20=170.1605, MACD=-3.3201, MACD_Signal=-2.5875, RSI=26.7494, EMA_20=168.6788, OBV=153997463.0000, One_Day_Reversal=-0.0339, Max_Return_20D=0.0559, Momentum_5D=-0.0361, Momentum_20D=-0.0752, Mean_Reversal_60D=-0.1074, Short_Term_Reversal_1month=-0.0649, Medium_Term_Momentum_2month_to_12month=0.1756, Long_Term_Reversal_13month_to_60month=-0.0710

[KDP] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=33.2700, last=25.5100, pct_change=-23.32%
- Indicators: MA_20=26.8376, MACD=-1.4057, MACD_Signal=-1.4737, RSI=30.9432, EMA_20=27.0857, OBV=244664425.0000, One_Day_Reversal=-0.0062, Max_Return_20D=0.0212, Momentum_5D=-0.0287, Momentum_20D=-0.1097, Mean_Reversal_60D=-0.1748, Short_Term_Reversal_1month=-0.1157, Medium_Term_Momentum_2month_to_12month=-0.1061, Long_Term_Reversal_13month_to_60month=0.4646

[TRI] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=200.9860, last=155.3300, pct_change=-22.72%
- Indicators: MA_20=166.9220, MACD=-6.2029, MACD_Signal=-5.4373, RSI=21.5465, EMA_20=165.1094, OBV=65873982.0000, One_Day_Reversal=-0.0054, Max_Return_20D=0.0177, Momentum_5D=-0.0340, Momentum_20D=-0.1256, Mean_Reversal_60D=-0.1475, Short_Term_Reversal_1month=-0.1239, Medium_Term_Momentum_2month_to_12month=0.1846, Long_Term_Reversal_13month_to_60month=1.3576

[CMCSA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0285
  * F_Book/Price: 0.7338
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1107
  * F_Debt/Assets: 0.3707
  * F_Debt/Equity: 1.0418
  * F_Dividend Yield: 0.0093
  * F_Return on Assets: 0.0168
  * F_Return on Equity: 0.1218

[TEAM] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.0252
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: NA
  * F_Debt/Assets: NA
  * F_Debt/Equity: NA
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: -0.0425
  * F_Return on Equity: -0.1908

[KDP] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.5563
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0766
  * F_Debt/Assets: 0.2924
  * F_Debt/Equity: 0.6362
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0128
  * F_Return on Equity: 0.0220

[TRI] Fundamentals (median in window):
  * F_Cash Flow/Assets: NA
  * F_Book/Price: 0.1395
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: NA
  * F_Debt/Assets: NA
  * F_Debt/Equity: NA
  * F_Dividend Yield: 0.0029
  * F_Return on Assets: 0.0902
  * F_Return on Equity: 0.1285
```

---

## Item 6/25 — `hqa_FTB_8647404c`

- **source**: fintradebench / FT25
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: Should I add more to my Netflix position in September 2025 after buying earlier?

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

## Item 7/25 — `hqa_FTB_869351e8`

- **source**: fintradebench / F44
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: Why don't high-growth tech companies (like Amazon, Meta) pay dividends in 2025?

**Oracle evidence**:

```
[AMZN] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=220.2200, last=219.5100, pct_change=-0.32%
- Indicators: MA_20=226.6545, MACD=-2.2740, MACD_Signal=-1.4041, RSI=31.0070, EMA_20=224.4044, OBV=48983516465.0000, One_Day_Reversal=-0.0130, Max_Return_20D=0.0151, Momentum_5D=-0.0012, Momentum_20D=-0.0552, Mean_Reversal_60D=-0.0314, Short_Term_Reversal_1month=-0.0158, Medium_Term_Momentum_2month_to_12month=0.1546, Long_Term_Reversal_13month_to_60month=0.1247

[META] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=597.8650, last=710.5600, pct_change=18.85%
- Indicators: MA_20=752.7938, MACD=-7.5348, MACD_Signal=-1.4335, RSI=27.8812, EMA_20=745.0124, OBV=5272133438.0000, One_Day_Reversal=-0.0227, Max_Return_20D=0.0187, Momentum_5D=-0.0446, Momentum_20D=-0.0550, Mean_Reversal_60D=-0.0465, Short_Term_Reversal_1month=-0.0129, Medium_Term_Momentum_2month_to_12month=0.3276, Long_Term_Reversal_13month_to_60month=1.0340

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

## Item 8/25 — `hqa_FTB_88541c51`

- **source**: fintradebench / FT16
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: Should I buy Starbucks during this August 2025 dip?

**Oracle evidence**:

```
[SBUX] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=86.2790, last=88.1900, pct_change=2.21%
- Indicators: MA_20=89.7888, MACD=-1.0668, MACD_Signal=-0.7918, RSI=41.0619, EMA_20=89.4645, OBV=1069770402.0000, One_Day_Reversal=0.0019, Max_Return_20D=0.0336, Momentum_5D=-0.0021, Momentum_20D=0.0221, Mean_Reversal_60D=-0.0354, Short_Term_Reversal_1month=-0.0447, Medium_Term_Momentum_2month_to_12month=-0.0192, Long_Term_Reversal_13month_to_60month=0.0343

[SBUX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0298
  * F_Book/Price: -0.0738
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2810
  * F_Debt/Assets: 0.8287
  * F_Debt/Equity: -3.6317
  * F_Dividend Yield: 0.0067
  * F_Return on Assets: 0.0200
  * F_Return on Equity: -0.0715
```

---

## Item 9/25 — `hqa_FTB_8c3f38fa`

- **source**: fintradebench / FT22
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Micron's Q3 2025 rally just getting started?

**Oracle evidence**:

```
[MU] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=120.7000, last=167.2180, pct_change=38.54%
- Indicators: MA_20=151.6601, MACD=10.4632, MACD_Signal=10.5797, RSI=73.2311, EMA_20=152.4584, OBV=3878675015.0000, One_Day_Reversal=0.0209, Max_Return_20D=0.0755, Momentum_5D=0.0055, Momentum_20D=0.4122, Mean_Reversal_60D=0.3031, Short_Term_Reversal_1month=0.3434, Medium_Term_Momentum_2month_to_12month=-0.0020, Long_Term_Reversal_13month_to_60month=1.0007

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
```

---

## Item 10/25 — `hqa_FTB_8ed2e330`

- **source**: fintradebench / F38
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['productive', 'aging', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: In 2025, is Cisco's asset base productive or aging into obsolescence?

**Oracle evidence**:

```
[CSCO] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=57.5940, last=67.9200, pct_change=17.93%
- Indicators: MA_20=67.3107, MACD=0.1063, MACD_Signal=-0.0087, RSI=60.3137, EMA_20=67.5252, OBV=21155438699.0000, One_Day_Reversal=0.0003, Max_Return_20D=0.0142, Momentum_5D=0.0165, Momentum_20D=0.0214, Mean_Reversal_60D=0.0035, Short_Term_Reversal_1month=0.0095, Medium_Term_Momentum_2month_to_12month=0.3158, Long_Term_Reversal_13month_to_60month=0.4618

[CSCO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0339
  * F_Book/Price: 0.1840
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1181
  * F_Debt/Assets: 0.2444
  * F_Debt/Equity: 0.6374
  * F_Dividend Yield: 0.0064
  * F_Return on Assets: 0.0223
  * F_Return on Equity: 0.0543
```

---

## Item 11/25 — `hqa_FTB_90f40b4c`

- **source**: fintradebench / F6
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: In mid-2025, why do investors love companies like Adobe and Nvidia?

**Oracle evidence**:

```
[NVDA] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=138.2810, last=187.6200, pct_change=35.68%
- Indicators: MA_20=178.7130, MACD=3.1174, MACD_Signal=1.8756, RSI=62.1522, EMA_20=180.5387, OBV=166450717998.0000, One_Day_Reversal=-0.0067, Max_Return_20D=0.0393, Momentum_5D=0.0529, Momentum_20D=0.1234, Mean_Reversal_60D=0.0616, Short_Term_Reversal_1month=0.1071, Medium_Term_Momentum_2month_to_12month=0.5239, Long_Term_Reversal_13month_to_60month=8.1817

[ADBE] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=441.0000, last=346.7400, pct_change=-21.37%
- Indicators: MA_20=355.2910, MACD=-1.2704, MACD_Signal=-0.0815, RSI=49.7458, EMA_20=354.1621, OBV=488879895.0000, One_Day_Reversal=-0.0135, Max_Return_20D=0.0278, Momentum_5D=-0.0378, Momentum_20D=-0.0064, Mean_Reversal_60D=-0.0255, Short_Term_Reversal_1month=0.0086, Medium_Term_Momentum_2month_to_12month=-0.3263, Long_Term_Reversal_13month_to_60month=0.1758

[NVDA] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.1490
  * F_Book/Price: 0.0237
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.3518
  * F_Debt/Assets: 0.0797
  * F_Debt/Equity: 0.1191
  * F_Dividend Yield: 0.0001
  * F_Return on Assets: 0.2131
  * F_Return on Equity: 0.3338

[ADBE] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0829
  * F_Book/Price: 0.0646
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1908
  * F_Debt/Assets: 0.2191
  * F_Debt/Equity: 0.5012
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0584
  * F_Return on Equity: 0.1268
```

---

## Item 12/25 — `hqa_FTB_9175a3ca`

- **source**: fintradebench / T44
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['INTC', 'ASML', 'TRI', 'MRVL', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: What stocks have the highest probability reversal setups for the week of September 8, 2025?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=20.2200, last=36.8300, pct_change=82.15%
- Indicators: MA_20=29.7190, MACD=3.2805, MACD_Signal=2.5576, RSI=78.3631, EMA_20=31.0653, OBV=12318654235.0000, One_Day_Reversal=-0.0126, Max_Return_20D=0.2277, Momentum_5D=0.0375, Momentum_20D=0.5039, Mean_Reversal_60D=0.4727, Short_Term_Reversal_1month=0.5542, Medium_Term_Momentum_2month_to_12month=-0.1102, Long_Term_Reversal_13month_to_60month=-0.5225

[ASML] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=692.0780, last=1032.2200, pct_change=49.15%
- Indicators: MA_20=912.8085, MACD=62.1203, MACD_Signal=53.8326, RSI=89.1995, EMA_20=924.1952, OBV=545973354.0000, One_Day_Reversal=0.0020, Max_Return_20D=0.0656, Momentum_5D=0.0848, Momentum_20D=0.3205, Mean_Reversal_60D=0.2961, Short_Term_Reversal_1month=0.3981, Medium_Term_Momentum_2month_to_12month=-0.1493, Long_Term_Reversal_13month_to_60month=1.5277

[TRI] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=159.7230, last=152.9800, pct_change=-4.22%
- Indicators: MA_20=163.2300, MACD=-6.6021, MACD_Signal=-5.9912, RSI=15.7143, EMA_20=161.8057, OBV=64318493.0000, One_Day_Reversal=0.0096, Max_Return_20D=0.0177, Momentum_5D=-0.0257, Momentum_20D=-0.1240, Mean_Reversal_60D=-0.1493, Short_Term_Reversal_1month=-0.1464, Medium_Term_Momentum_2month_to_12month=0.1877, Long_Term_Reversal_13month_to_60month=1.2837

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

[ASML] Fundamentals (median in window):
  * F_Cash Flow/Assets: -0.0013
  * F_Book/Price: 0.0717
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1702
  * F_Debt/Assets: 0.0809
  * F_Debt/Equity: 0.2103
  * F_Dividend Yield: 0.0100

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

## Item 13/25 — `hqa_FTB_9216ec7b`

- **source**: fintradebench / F35
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: Why is Apple's return on equity so extraordinarily high in 2025?

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

## Item 14/25 — `hqa_FTB_921c1811`

- **source**: fintradebench / FT50
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Has Starbucks's 2025 turnaround plan gained traction based on fundamental and momentum signals?

**Oracle evidence**:

```
[SBUX] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=90.4160, last=86.4200, pct_change=-4.42%
- Indicators: MA_20=84.1810, MACD=-0.4628, MACD_Signal=-0.9594, RSI=63.6297, EMA_20=85.2328, OBV=1030662154.0000, One_Day_Reversal=-0.0035, Max_Return_20D=0.0275, Momentum_5D=0.0363, Momentum_20D=0.0116, Mean_Reversal_60D=-0.0232, Short_Term_Reversal_1month=-0.0061, Medium_Term_Momentum_2month_to_12month=-0.0567, Long_Term_Reversal_13month_to_60month=0.1962

[SBUX] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0298
  * F_Book/Price: -0.0726
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2810
  * F_Debt/Assets: 0.8222
  * F_Debt/Equity: -3.4659
  * F_Dividend Yield: 0.0067
  * F_Return on Assets: 0.0200
  * F_Return on Equity: -0.0715
```

---

## Item 15/25 — `hqa_FTB_94705863`

- **source**: fintradebench / F22
- **transformation_type**: `none`
- **answer_type**: `open_summary_with_canonical_claim`
- **answer_space**: ['claim_true', 'claim_false', 'mixed']
- **noncommit_labels**: ['mixed']

**Question**: As of Q3 2025, why is Tesla's stock price so high compared to its earnings?

**Oracle evidence**:

```
[TSLA] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=300.7100, last=444.7200, pct_change=47.89%
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

## Item 16/25 — `hqa_FTB_9a70a1f9`

- **source**: fintradebench / F24
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['growth', 'value', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Amazon a value or growth stock at its August 2025 prices?

**Oracle evidence**:

```
[AMZN] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=214.7500, last=229.0000, pct_change=6.64%
- Indicators: MA_20=225.1670, MACD=1.7111, MACD_Signal=1.4651, RSI=61.3973, EMA_20=226.9174, OBV=49100139636.0000, One_Day_Reversal=-0.0112, Max_Return_20D=0.0400, Momentum_5D=0.0007, Momentum_20D=0.0664, Mean_Reversal_60D=0.0302, Short_Term_Reversal_1month=0.0061, Medium_Term_Momentum_2month_to_12month=0.2735, Long_Term_Reversal_13month_to_60month=0.1078

[AMZN] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0477
  * F_Book/Price: 0.1427
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2458
  * F_Debt/Assets: 0.1963
  * F_Debt/Equity: 0.4013
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0270
  * F_Return on Equity: 0.0638
```

---

## Item 17/25 — `hqa_FTB_a0c0d5cc`

- **source**: fintradebench / FT13
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: In mid-2025, should I switch from bonds to Pepsi stock for income?

**Oracle evidence**:

```
[PEP] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=145.8750, last=141.9800, pct_change=-2.67%
- Indicators: MA_20=141.6560, MACD=-0.5742, MACD_Signal=-0.6861, RSI=55.4120, EMA_20=142.1245, OBV=1411201321.0000, One_Day_Reversal=-0.0023, Max_Return_20D=0.0192, Momentum_5D=0.0110, Momentum_20D=-0.0301, Mean_Reversal_60D=-0.0054, Short_Term_Reversal_1month=-0.0333, Medium_Term_Momentum_2month_to_12month=-0.1631, Long_Term_Reversal_13month_to_60month=0.3925

[PEP] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0187
  * F_Book/Price: 0.0921
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2157
  * F_Debt/Assets: 0.4769
  * F_Debt/Equity: 2.6185
  * F_Dividend Yield: 0.0089
  * F_Return on Assets: 0.0191
  * F_Return on Equity: 0.0834
```

---

## Item 18/25 — `hqa_FTB_a14e5de6`

- **source**: fintradebench / F47
- **transformation_type**: `none`
- **answer_type**: `premise_check`
- **answer_space**: ['premise_false', 'premise_true_explained', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Why does Intel maintain its dividend in 2025 despite its challenges?

**Oracle evidence**:

```
[INTC] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=20.2200, last=36.8300, pct_change=82.15%
- Indicators: MA_20=29.7190, MACD=3.2805, MACD_Signal=2.5576, RSI=78.3631, EMA_20=31.0653, OBV=12318654235.0000, One_Day_Reversal=-0.0126, Max_Return_20D=0.2277, Momentum_5D=0.0375, Momentum_20D=0.5039, Mean_Reversal_60D=0.4727, Short_Term_Reversal_1month=0.5542, Medium_Term_Momentum_2month_to_12month=-0.1102, Long_Term_Reversal_13month_to_60month=-0.5225

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

## Item 19/25 — `hqa_FTB_a32e1559`

- **source**: fintradebench / FT26
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is NVIDIA's August 2025 pullback a buying opportunity given its AI dominance?

**Oracle evidence**:

```
[NVDA] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=173.7100, last=174.1700, pct_change=0.26%
- Indicators: MA_20=179.6890, MACD=2.1064, MACD_Signal=3.2077, RSI=35.7453, EMA_20=177.8547, OBV=165598124469.0000, One_Day_Reversal=-0.0332, Max_Return_20D=0.0362, Momentum_5D=-0.0214, Momentum_20D=0.0026, Mean_Reversal_60D=0.0494, Short_Term_Reversal_1month=0.0050, Medium_Term_Momentum_2month_to_12month=0.1952, Long_Term_Reversal_13month_to_60month=7.7986

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

## Item 20/25 — `hqa_FTB_a5c1c626`

- **source**: fintradebench / T24
- **transformation_type**: `none`
- **answer_type**: `screening_top1`
- **answer_space**: ['APP', 'LRCX', 'MNST', 'INTC', 'none_clear']
- **noncommit_labels**: ['none_clear']

**Question**: What companies are breaking above key moving average resistance during September 2025?

**Oracle evidence**:

```
[APP] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=481.7300, last=718.5400, pct_change=49.16%
- Indicators: MA_20=602.7590, MACD=59.7779, MACD_Signal=53.4882, RSI=90.6737, EMA_20=610.1187, OBV=570095031.0000, One_Day_Reversal=0.0087, Max_Return_20D=0.1159, Momentum_5D=0.1034, Momentum_20D=0.4916, Mean_Reversal_60D=0.5313, Short_Term_Reversal_1month=0.4726, Medium_Term_Momentum_2month_to_12month=2.0492, Long_Term_Reversal_13month_to_60month=NA

[LRCX] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=96.8340, last=133.9000, pct_change=38.28%
- Indicators: MA_20=118.8435, MACD=7.7814, MACD_Signal=6.9254, RSI=88.9329, EMA_20=121.2499, OBV=8871501719.0000, One_Day_Reversal=0.0214, Max_Return_20D=0.0766, Momentum_5D=0.0170, Momentum_20D=0.3828, Mean_Reversal_60D=0.2608, Short_Term_Reversal_1month=0.2619, Medium_Term_Momentum_2month_to_12month=0.1284, Long_Term_Reversal_13month_to_60month=1.7085

[MNST] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=62.6700, last=67.3100, pct_change=7.40%
- Indicators: MA_20=64.5250, MACD=0.8960, MACD_Signal=0.6919, RSI=70.5128, EMA_20=64.7313, OBV=2543820188.0000, One_Day_Reversal=0.0052, Max_Return_20D=0.0281, Momentum_5D=0.0439, Momentum_20D=0.0740, Mean_Reversal_60D=0.0791, Short_Term_Reversal_1month=0.0797, Medium_Term_Momentum_2month_to_12month=0.1296, Long_Term_Reversal_13month_to_60month=0.2236

[INTC] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=24.2100, last=33.5500, pct_change=38.58%
- Indicators: MA_20=27.8705, MACD=2.7412, MACD_Signal=1.9872, RSI=73.8328, EMA_20=29.0855, OBV=12132002275.0000, One_Day_Reversal=-0.0270, Max_Return_20D=0.2277, Momentum_5D=0.1435, Momentum_20D=0.3858, Mean_Reversal_60D=0.3775, Short_Term_Reversal_1month=0.3831, Medium_Term_Momentum_2month_to_12month=-0.1722, Long_Term_Reversal_13month_to_60month=-0.5419

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

[MNST] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0534
  * F_Book/Price: 0.1176
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2419
  * F_Debt/Assets: 0.0000
  * F_Debt/Equity: 0.0000
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0569
  * F_Return on Equity: 0.0749

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

## Item 21/25 — `hqa_FTB_a6d883cc`

- **source**: fintradebench / FT18
- **transformation_type**: `none`
- **answer_type**: `supportive_judgment`
- **answer_space**: ['supportive', 'unsupportive', 'conditional', 'insufficient_data']
- **noncommit_labels**: ['conditional', 'insufficient_data']

**Question**: Should I invest in Cisco for stability in the volatile 2025 market?

**Oracle evidence**:

```
[CSCO] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=57.5940, last=67.9200, pct_change=17.93%
- Indicators: MA_20=67.3107, MACD=0.1063, MACD_Signal=-0.0087, RSI=60.3137, EMA_20=67.5252, OBV=21155438699.0000, One_Day_Reversal=0.0003, Max_Return_20D=0.0142, Momentum_5D=0.0165, Momentum_20D=0.0214, Mean_Reversal_60D=0.0035, Short_Term_Reversal_1month=0.0095, Medium_Term_Momentum_2month_to_12month=0.3158, Long_Term_Reversal_13month_to_60month=0.4618

[CSCO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0339
  * F_Book/Price: 0.1840
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1181
  * F_Debt/Assets: 0.2444
  * F_Debt/Equity: 0.6374
  * F_Dividend Yield: 0.0064
  * F_Return on Assets: 0.0223
  * F_Return on Equity: 0.0543
```

---

## Item 22/25 — `hqa_FTB_a6f3790c`

- **source**: fintradebench / FT14
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['sustainable', 'take_profits', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Broadcom's Q3 2025 rally sustainable or should I take profits?

**Oracle evidence**:

```
[AVGO] Trading/Price Data 2025-07-01 -> 2025-09-30
- AdjClose: first=264.2800, last=329.9100, pct_change=24.83%
- Indicators: MA_20=340.6510, MACD=5.9882, MACD_Signal=9.9495, RSI=13.1781, EMA_20=333.9730, OBV=6529730686.0000, One_Day_Reversal=0.0061, Max_Return_20D=0.0977, Momentum_5D=-0.0266, Momentum_20D=0.1081, Mean_Reversal_60D=0.0687, Short_Term_Reversal_1month=0.0642, Medium_Term_Momentum_2month_to_12month=0.6624, Long_Term_Reversal_13month_to_60month=4.0679

[AVGO] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0433
  * F_Book/Price: 0.0521
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.0963
  * F_Debt/Assets: 0.3878
  * F_Debt/Equity: 0.8765
  * F_Dividend Yield: 0.0020
  * F_Return on Assets: 0.0276
  * F_Return on Equity: 0.0596
```

---

## Item 23/25 — `hqa_FTB_a809667e`

- **source**: fintradebench / FT46
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['exposure_limits', 'diversification_offsets', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: In 2025, does Qualcomm's smartphone exposure limit its appeal, or do diversification efforts offset this?

**Oracle evidence**:

```
[QCOM] Trading/Price Data 2025-01-01 -> 2025-12-31
- AdjClose: first=151.0500, last=169.1800, pct_change=12.00%
- Indicators: MA_20=165.7325, MACD=2.7446, MACD_Signal=2.9782, RSI=64.5255, EMA_20=165.7587, OBV=2565660079.0000, One_Day_Reversal=0.0020, Max_Return_20D=0.0237, Momentum_5D=-0.0001, Momentum_20D=0.0584, Mean_Reversal_60D=0.0681, Short_Term_Reversal_1month=0.0795, Medium_Term_Momentum_2month_to_12month=-0.1001, Long_Term_Reversal_13month_to_60month=0.6019

[QCOM] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0524
  * F_Book/Price: 0.1641
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1983
  * F_Debt/Assets: 0.2641
  * F_Debt/Equity: 0.5423
  * F_Dividend Yield: 0.0055
  * F_Return on Assets: 0.0521
  * F_Return on Equity: 0.1077
```

---

## Item 24/25 — `hqa_FTB_b1c0ad1d`

- **source**: fintradebench / F46
- **transformation_type**: `none`
- **answer_type**: `category_choice`
- **answer_space**: ['red_flag', 'smart_allocation', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is PayPal's lack of dividend (as of August 2025) a red flag or smart capital allocation?

**Oracle evidence**:

```
[PYPL] Trading/Price Data 2025-08-01 -> 2025-08-31
- AdjClose: first=67.1100, last=70.1900, pct_change=4.59%
- Indicators: MA_20=68.9545, MACD=-0.5008, MACD_Signal=-0.8333, RSI=63.2116, EMA_20=69.8192, OBV=43270247.0000, One_Day_Reversal=0.0019, Max_Return_20D=0.0391, Momentum_5D=0.0041, Momentum_20D=0.0459, Mean_Reversal_60D=-0.0257, Short_Term_Reversal_1month=0.0050, Medium_Term_Momentum_2month_to_12month=0.0517, Long_Term_Reversal_13month_to_60month=-0.7036

[PYPL] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0113
  * F_Book/Price: 0.2831
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.1039
  * F_Debt/Assets: 0.0405
  * F_Debt/Equity: 0.1599
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0151
  * F_Return on Equity: 0.0618
```

---

## Item 25/25 — `hqa_FTB_b538ab74`

- **source**: fintradebench / FT9
- **transformation_type**: `none`
- **answer_type**: `yes_no_mixed`
- **answer_space**: ['yes', 'no', 'mixed', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data', 'mixed']

**Question**: Is Adobe too expensive at its September 2025 levels?

**Oracle evidence**:

```
[ADBE] Trading/Price Data 2025-09-01 -> 2025-09-30
- AdjClose: first=345.6300, last=352.7500, pct_change=2.06%
- Indicators: MA_20=355.2830, MACD=0.6681, MACD_Signal=0.6693, RSI=52.4383, EMA_20=356.5277, OBV=494552281.0000, One_Day_Reversal=-0.0186, Max_Return_20D=0.0278, Momentum_5D=-0.0250, Momentum_20D=0.0206, Mean_Reversal_60D=-0.0125, Short_Term_Reversal_1month=0.0154, Medium_Term_Momentum_2month_to_12month=-0.3060, Long_Term_Reversal_13month_to_60month=0.2071

[ADBE] Fundamentals (median in window):
  * F_Cash Flow/Assets: 0.0764
  * F_Book/Price: 0.0786
  * F_Earnings/Price: NA
  * F_Forecast Earnings/Price: NA
  * F_Sales/Assets: 0.2082
  * F_Debt/Assets: 0.2308
  * F_Debt/Equity: 0.5638
  * F_Dividend Yield: 0.0000
  * F_Return on Assets: 0.0601
  * F_Return on Equity: 0.1347
```

---
