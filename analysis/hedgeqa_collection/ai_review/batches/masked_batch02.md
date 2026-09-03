# Blind review batch `masked_batch02`

25 items. Family: `evidence_masked_insufficient`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FB_4755512d_masked`

- **source**: financebench / financebench_id_00438
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Adobe have an improving operating margin profile as of FY2022? If operating margin is not a useful metric for a company like this, then state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
ADOBE INC.
CONSOLIDATED STATEMENTS OF INCOME
(In millions, except per share data)
 
Years Ended
 
December 2,
2022
December 3,
2021
November 27,
2020
Revenue:
 
Subscription
$ 
11,626 
Product
 
532 
555 
507 
Services and other
 
686 
657 
735 
Total revenue
 
17,606 
15,785 
12,868 
 
Cost of revenue:
Subscription
 
1,646 
1,374 
1,108 
Product
 
35 
41 
36 
Services and other
 
484 
450 
578 
Total cost of revenue
 
2,165 
1,865 
1,722 
 
Gross profit
 
15,441 
13,920 
11,146 
 
Operating expenses:
Research and development
 
2,987 
2,540 
2,188 
Sales and marketing
 
4,968 
4,321 
3,591 
General and administrative
 
1,219 
1,085 
968 
Amortization of intangibles
 
169 
172 
162 
Total operating expenses
 
9,343 
8,118 
6,909 
 
Operating income
 
4,237
```

---

## Item 2/25 — `hqa_FB_49becde3_masked`

- **source**: financebench / financebench_id_00678
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Boeing have an improving gross margin profile as of FY2022? If gross margin is not a useful metric for a company like this, then state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
The Boeing Company and Subsidiaries
Consolidated Statements of Operations
(Dollars in millions, except per share data)
 
 
 
Years ended December 31,
2022
2021
2020
Sales of products
$55,893 
$51,386 
$47,142 
Sales of services
10,715 
10,900 
11,016 
Total revenues
58,158 
Cost of products
(53,969)
(49,954)
(54,568)
Cost of services
(9,109)
(9,283)
(9,232)
Boeing Capital interest expense
(28)
(32)
(43)
Total costs and expenses
(63,106)
(59,269)
(63,843)
(5,685)
```

---

## Item 3/25 — `hqa_FB_50664e43_masked`

- **source**: financebench / financebench_id_00460
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Was there any change in the number of Best Buy stores between Q2 of FY2024 and FY2023?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
iscal 2024 was primarily driven by comparable sales declines in appliances, home theater, 
computing and mobile phones, partially offset by comparable sales growth in gaming. Online revenue of $2.8 billion and $5.5 billion in the second quarter and 
first six months of fiscal 2024 decreased 7.1% and 9.7% on a comparable basis, respectively. These decreases in revenue were primarily due to the reasons 
described above and within the Consolidated Results section, above.
 
Domestic segment stores open at the beginning and end of the second quarters of fiscal 2024 and fiscal 2023 were as follows:
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Fiscal 2024
 
Fiscal 2023
 
Total Stores at 
Beginning of 
Second Quarter 
Stores 
Opened
 
Stores 
Closed
 
Total Stores at 
End of Second 
Quarter
 
Total Stores at 
Beginning of 
Second Quarter 
Stores 
Opened
 
Stores 
Closed
 
Total Stores at 
End of Second 
Quarter
Best Buy
 
 908 
 - 
 (1) 
 907 
 931 
 1 
 (2) 
 930 
Outlet Centers
 
 20 
 1 
 (1) 
 20 
 16 
 2 
 - 
 18 
Pacific Sales
 
 20 
 - 
 - 
 20 
 21 
 - 
 - 
 21 
Yardbird
 
 18 
 4 
 - 
 22 
 9 
 4 
 - 
 13 
Total
 
 966 
 5 
 (2) 
 977 
 7 
 (2)
```

---

## Item 4/25 — `hqa_FB_5dbbcec0_masked`

- **source**: financebench / financebench_id_01254
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Has MGM Resorts paid dividends to common shareholders in FY2022?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
PART II
ITEM 5. MARKET FOR REGISTRANTS COMMON EQUITY, RELATED STOCKHOLDER MATTERS AND ISSUER PURCHASES OF
EQUITY SECURITIES
Common Stock Information
Our common stock is traded on the New York Stock Exchange (NYSE) under the symbol MGM.
There were approximately 3,143 record holders of our common stock as of February 22, 2023.
Dividend Policy
We implemented a dividend program in February 2017 pursuant to which it has paid regular quarterly dividends. In the second quarter of 2020, we
in light of our current preferred method of returning value to shareholders through our share repurchase plan. To the extent we determine to reinstate the
dividend in the future, the amount, declaration and payment of any future dividends will be subject to the discretion of our Board of Directors who will
evaluate our dividend policy from time to time based on factors it deems relevant, and the contractual limitations described below.
Purchases of Equity Securities by the Issuer
The following table provides information about share repurchases of our common stock during the quarter ended December 31, 2022:
Period
Total Number of
Shares Purchased
Average Price Paid
per Share
Total Number of
Shares Purchased as
Part of a Publicly
Announced Program
Dollar Value of
Shares that May Yet
be Purchased Under
the Program
(In thousands)
October 1, 2022 October 31, 2022
5,727,219 
$
31.74 
5,727,219 
$
645,485 
November 1, 2022 November 30, 2022
1,259,233 
$
33.65 
1,259,233 
$
603,108 
December 1, 2022 December 31, 2022
3,700,000 
$
34.61 
3,700,000 
$
475,049 
In March 2022, we announced that the Board of Directors authorized a $2.0 billion stock repurchase plan and in February 2023, we announced that the
Board of Directors had authorized a $2.0 billion stock repurchase plan. Under the stock repurchase plans, we may repurchase shares from time to time in the
open market or in privately negotiated agreements. Repurchases of common stock may also be made under a Rule 10b5-1 plan, which would permit common
stock to be purchased when we might otherwise be precluded from doing so under insider trading laws. The timing, volume and nature of stock repurchases
will be at the sole discretion of management, dependent on market conditions, applicable securities laws, and other factors, and may be suspended or
discontinued at any time. All shares we repurchased during the quarter ended December 31, 2022 were purchased pursuant to our publicly announced stock
repurchase plans and have been retired.
30
```

---

## Item 5/25 — `hqa_FB_6358a99a_masked`

- **source**: financebench / financebench_id_00005
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Corning have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Consolidated Balance Sheets
Corning Incorporated and Subsidiary Companies
 
 
 
December 31,
 
(in millions, except share and per share amounts)
 
2022
 
2021
 
 
 
 
 
Assets
 
 
 
 
 
 
 
Current assets:
 
 
 
Cash and cash equivalents
 $
1,671 $
2,148 
Trade accounts receivable, net of doubtful accounts - $40 and $42
 
2,004 
Inventories (Note 5)
 
2,481 
Other current assets (Notes 10 and 14)
 
1,026 
Total current assets
 
7,453 
7,659 
 
 
 
 
Property, plant and equipment, net of accumulated depreciation - $14,147 and $13,969 (Note 8)
 
15,371 
15,804 
Goodwill, net (Note 9)
 
2,394 
2,421 
Other intangible assets, net (Note 9)
 
1,029 
1,148 
Deferred income taxes (Note 7)
 
1,073 
1,066 
Other assets (Notes 10 and 14)
 
2,179 
2,056 
 
 
 
 
Total Assets
 $
29,499 $
30,154 
 
 
 
 
Liabilities and Equity
 
 
 
 
 
 
 
Current liabilities:
 
 
 
Current portion of long-term debt and short-term borrowings (Note 11)
 $
224 $
55 
Accounts payable
 
1,804 
1,612 
Other accrued liabilities (Notes 10 and 13)
 
3,147 
3,139 
Total current liabilities
 
5,175 
4,806 
 
 
 
 
Long-term debt (Note 11)
 
6,687 
6,989 
Postretirement benefits other than pensions (Note 12)
 
407 
622 
Other liabilities (Notes 10 and 13)
 
4,955 
5,192 
Total liabilities
 
17,224 
17,609
```

---

## Item 6/25 — `hqa_FB_7cc358e4_masked`

- **source**: financebench / financebench_id_00684
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does AMCOR have an improving gross margin profile as of FY2023? If gross margin is not a useful metric for a company like this, then state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Amcor plc and Subsidiaries
Consolidated Statements of Income
($ in millions, except per share data)
For the years ended June 30,
2023
2022
2021
Net sales
$
$
$
12,861 
Cost of sales
(11,969)
(11,724)
(10,129)
Gross profit
2,732
```

---

## Item 7/25 — `hqa_FB_84463d0e_masked`

- **source**: financebench / financebench_id_00552
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Has Microsoft increased its debt on balance sheet between FY2023 and the FY2022 period?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
BALANCE SHEETS 
 
(In millions)
 
 
 
 
 
 
 
 
 
June 30,
 
2023 
2022 
 
 
 
Assets
 
 
 
Current assets:
 
 
 
Cash and cash equivalents
 $
34,704 $
13,931 
Short-term investments
 
76,558 
90,826 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Total cash, cash equivalents, and short-term investments
 
111,262 
104,757 
Accounts receivable, net of allowance for doubtful accounts of $650 and $633
 
48,688 
44,261 
Inventories
 
2,500 
3,742 
Other current assets
 
21,807 
16,924 
 
 
 
 
 
 
 
 
 
 
 
 
Total current assets
 
184,257 
169,684 
Property and equipment, net of accumulated depreciation of $68,251 and $59,660
 
95,641 
74,398 
Operating lease right-of-use assets
 
14,346 
13,148 
Equity investments
 
9,879 
6,891 
Goodwill
 
67,886 
67,524 
Intangible assets, net
 
9,366 
11,298 
Other long-term assets
 
30,601 
21,897 
 
 
 
 
 
 
 
 
 
 
 
 
Total assets
 $
411,976 $
364,840 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Liabilities and stockholders equity
 
 
 
Current liabilities:
 
 
 
Accounts payable
 $
18,095 $
19,000 
Current portion of long-term debt
 
Accrued compensation
 
11,009 
10,661 
Short-term income taxes
 
4,152 
4,067 
Short-term unearned revenue
 
50,901 
45,538 
Other current liabilities
 
14,745 
13,067 
 
 
 
 
 
 
 
 
 
 
 
 
Total current liabilities
 
104,149 
95,082 
Long-term debt
 
Long-term income taxes
 
25,560 
26,069 
Long-term unearned revenue
 
2,912 
2,870 
Deferred income taxes
 
433 
230 
Operating lease liabilities
 
12,728 
11,489 
Other long-term liabilities
 
17,981 
15,526 
 
 
 
 
 
 
 
 
 
 
 
 
Total liabilities
 
205,753 
198,298 
 
 
 
 
 
 
 
 
 
 
 
 
Commitments and contingencies
 
 
 
Stockholders equity:
 
 
 
Common stock and paid-in capital shares authorized 24,000; outstanding 7,432 and 7,464
 
93,718 
86,939 
Retained earnings
 
118,848 
84,281 
Accumulated other comprehensive loss
 
(6,343) 
(4,678)
 
 
 
 
 
 
 
 
 
 
 
 
Total stockholders equity
 
206,223 
166,542 
 
 
 
 
 
 
 
 
 
 
 
 
Total liabilities and stockholders equity
 $
411,976 $
364,8
```

---

## Item 8/25 — `hqa_FB_86637d3d_masked`

- **source**: financebench / financebench_id_00288
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Was there any drop in Cash & Cash equivalents between FY 2023 and Q2 of FY2024?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
July 29, 2023
 
July 30, 2022
 
July 29, 2023
 
July 30, 2022
Operating income
$
 348 
 $
 371 
 $
 659 
 $
 833 
% of revenue
 
 3.6 % 
 3.6 % 
 3.5 % 
 4.0 %
Intangible asset amortization(1)
 
 21 
 
 22 
 
 41 
 
 44 
Restructuring charges(2)
 
 (7) 
 
 34 
 
 (16) 
 
 35 
Non-GAAP operating income
$
 362 
 $
 427 
 $
 684 
 $
 912 
% of revenue
 
 3.8 % 
 4.1 % 
 3.6 % 
 4.3 %
 
 
 
 
 
 
 
 
 
Effective tax rate
 
 26.1 % 
 15.6 % 
 24.8 % 
 20.5 %
Intangible asset amortization(1)
 
 (0.4)% 
 0.4 % 
 0.4 % 
 0.2 %
Restructuring charges(2)
 
 0.4 % 
 0.7 % 
 (0.1)% 
 0.1 %
Loss on investments
 
 0.5 % 
 -% 
 -% 
 -%
Non-GAAP effective tax rate
 
 26.6 % 
 16.7 % 
 25.1 % 
 20.8 %
 
 
 
 
 
 
 
 
 
Diluted EPS
$
 1.25 
 $
 1.35 
 $
 2.36 
 $
 2.85 
Intangible asset amortization(1)
 
 0.10 
 
 0.10 
 
 0.18 
 
 0.19 
Restructuring charges(2)
 
 (0.03) 
 
 0.15 
 
 (0.07) 
 
 0.15 
Loss on investments
 
 - 
 
 - 
 
 0.02 
 
 - 
Gain on sale of subsidiary, net(3)
 
 (0.10) 
 
 - 
 
 (0.10) 
 
 - 
Income tax impact of non-GAAP adjustments(4)
 
 - 
 
 (0.06) 
 
 (0.02) 
 
 (0.08) 
Non-GAAP diluted EPS
$
 1.22 
 $
 1.54 
 $
 2.37 
 $
 3.11 
For additional information regarding the nature of charges discussed below, refer to Note 1, Basis of Presentation, Note 2, Restructuring, and Note 3, Goodwill and Intangible Assets, of the Notes to 
Condensed Consolidated Financial Statements, included in this Quarterly Report on Form 10-Q.
(1)
Represents the non-cash amortization of definite-lived intangible assets associated with acquisitions, including customer relationships, tradenames and developed technology assets.
(2)
Represents charges related to employee termination benefits and subsequent adjustments from higher-than-expected employee retention related to previously planned organizational changes.
(3)
Represents the gain on sale of a Mexico subsidiary subsequent to our exit from operations in Mexico.
(4)
The non-GAAP adjustments primarily relate to the U.S. and Mexico. As such, the forecasted annual income tax charge on the U.S. non-GAAP adjustments is calculated using the statutory tax rate of 
24.5%. There is no forecasted annual income tax benefit for Mexico non-GAAP items, as there is no forecasted annual tax expense on the income in the calculation of GAAP income tax expense.
 
Our non-GAAP operating income rates decreased in the second quarter and first six months of fiscal 2024, primarily due to unfavorable SG&A rates, partially 
offset by favorable gross profit rates.
 
Our non-GAAP effective tax rate increased in the second quarter of fiscal 2024, primarily due to the prior year resolution of certain discrete tax matters. Our non-
GAAP effective tax rate increased in the first six months of fiscal 2024, primarily due to the prior year resolution of certain discrete tax matters and decreased tax 
benefits from stock-based compensation, partially offset by the impact of lower pre-tax earnings.
 
Our non-GAAP diluted EPS decreased in the second quarter and first six months of fiscal 2024, primarily due to the decreases in non-GAAP operating income.
 
Liquidity and Capital Resources
 
We closely manage our liquidity and capital resources. Our liquidity requirements depend on key variables, including the level of investment required to support 
our business strategies, the performance of our business, capital expenditures, dividends, credit facilities, short-term borrowing arrangements and working capital 
management. We modify our approach to managing these variables as changes in our operating environment arise. For example, capital expenditures and share 
repurchases are a component of our cash flow and capital management strategy, which, to a large extent, we can adjust in response to economic and other 
changes in our business environment. We have a disciplined approach to capital allocation, which focuses on investing in key priorities that support our strategy.
 
Cash and cash equivalents were as follows ($ in millions):
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
July 29, 2023
 
January 28, 2023
 
July 30, 2022
Cash and cash equivalents
 
 $
 840
```

---

## Item 9/25 — `hqa_FB_93bd00fd_masked`

- **source**: financebench / financebench_id_00790
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Is CVS Health a capital-intensive business based on FY2022 data?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Consolidated Statements of Operations
For the Years Ended December 31,
In millions, except per share amounts
2022
2021
2020
Revenues:
 
 
 
Products
$
226,616 $
203,738 $
190,688 
Premiums
85,330 
76,132 
69,364 
Services
9,683 
11,042 
7,856 
Net investment income
838 
1,199 
798 
Total revenues
322,467 
292,111 
268,706 
Operating costs:
Cost of products sold
196,892 
175,803 
163,981 
Benefit costs
71,281 
64,260 
55,679 
Opioid litigation charges
5,803 
 
 
Loss on assets held for sale
2,533 
 
 
Store impairments
 
1,358 
 
Goodwill impairment
 
431 
 
Operating expenses
38,212 
37,066 
35,135 
Total operating costs
314,721 
278,918 
254,795 
Operating income
7,746 
13,193 
13,911 
Interest expense
2,287 
2,503 
2,907 
Loss on early extinguishment of debt
 
452 
1,440 
Other income
(169)
(182)
(206)
Income before income tax provision
5,628 
10,420 
9,770 
Income tax provision
1,463 
2,522 
2,569 
Income from continuing operations
7,201 
Loss from discontinued operations, net of tax
 
 
(9)
Net income
7,192

Consolidated Balance Sheets
At December 31,
In millions, except per share amounts
2022
2021
Assets:
 
Cash and cash equivalents
$
12,945 $
9,408 
Investments
2,778 
3,117 
Accounts receivable, net
27,276 
24,431 
Inventories
19,090 
17,760 
Assets held for sale
908 
 
Other current assets
2,685 
5,292 
Total current assets
65,682 
60,008 
Long-term investments
21,096 
23,025 
Property and equipment, net
12,896 
Operating lease right-of-use assets
17,872 
19,122 
Goodwill
78,150 
79,121 
Intangible assets, net
24,754 
29,026 
Separate accounts assets
3,228 
5,087 
Other assets
4,620 
4,714 
Total assets
$
```

---

## Item 10/25 — `hqa_FB_9ef802db_masked`

- **source**: financebench / financebench_id_00685
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Are Best Buy's gross margins historically consistent (not fluctuating more than roughly 2% each year)? If gross margins are not a relevant metric for a company like this, then please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Consolidated Statements of Earnings
$ and shares in millions, except per share amounts
 
 
 
 
 
 
 
 
 
 
 
 
 
Fiscal Years Ended
January 28, 2023
 
January 29, 2022
 
January 30, 2021
Revenue
$
 
$
 
$
 47,262 
Cost of sales
 
 36,386 
 
 
 40,121 
 
 
 36,689 
Gross profit
 
 
 
 
 
 10,573 
Selling, general and administrative expenses
 
 7,970 
 
 
 8,635 
 
 
 7,928 
Restructuring charges
 
 147 
 
 
 (34) 
 
 
 254 
Operating income
 
 1,795 
 
 
 3,039 
 
 
 2,391 
Other income (expense):
 
 
 
 
 
 
 
 
 
 
 
Investment income and other
 
 28 
 
 
 10 
 
 
 38 
Interest expense
 
 (35) 
 
 
 (25) 
 
 
 (52) 
Earnings before income tax expense and equity in income of affiliates
 
 1,788 
 
 
 3,024 
 
 
 2,377 
Income tax expense
 
 370 
 
 
 574 
 
 
 579 
Equity in income of affiliates
 
 1 
 
 
 4 
 
 
 - 
Net earnings
$
 1,419 
 
$
 2,454 
 
$
 1,798
```

---

## Item 11/25 — `hqa_FB_9fc58fab_masked`

- **source**: financebench / financebench_id_01107
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Has CVS Health reported any materially important ongoing legal battles from 2022, 2021 and 2020?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Usual and Customary Pricing Litigation
The Company and certain current and former directors and officers are named as a defendant in a number of lawsuits that allege that the Companys retail
pharmacies overcharged for prescription drugs by not submitting the correct usual and customary price during the claims adjudication process.

The Company is facing multiple lawsuits, including by state Attorneys General, governmental subdivisions and several putative class actions, regarding drug
pricing and its rebate arrangements with drug manufacturers. These complaints, brought by a number of different types of plaintiffs under a variety of legal
theories, generally allege that rebate agreements between the drug manufacturers and PBMs caused inflated prices for certain drug products.

In December 2022, the Company agreed to a formal settlement agreement, the financial amounts of which were agreed to in principle in October 2022, with a
leadership group of a number of state Attorneys General and the Plaintiffs Executive Committee (PEC). The agreement would resolve substantially all
opioid claims against Company entities by states and political subdivisions, but not private plaintiffs. The maximum amount payable by the Company under the
would be payable over 10 years, beginning in 2023.
```

---

## Item 12/25 — `hqa_FB_a7999aa2_masked`

- **source**: financebench / financebench_id_01487
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Did JnJ's net earnings as a percent of sales increase in Q2 of FY2023 compared to Q2 of FY2022?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Johnson & Johnson and Subsidiaries
 
Condensed Consolidated Statement of Earnings 
 
(Unaudited; in Millions Except Per Share Figures)
Percent
Percent
Percent
Increase
Amount
to Sales
Amount
to Sales
(Decrease)
Sales to customers
25,530
$ 
 100.0
24,020
$ 
 100.0
6.3
Cost of products sold
 8,212
32.2
 
7,919
 
33.0
 
3.7
Gross Profit
17,318
 
67.8
 
16,101
 
67.0
 
7.6
Selling, marketing and administrative expenses
 6,665
26.1
 
6,226
 
25.9
 
7.1
Research and development expense
 3,829
15.0
 
3,703
 
15.4
 
3.4
Interest (income) expense, net
(23)
 
 (0.1)
(26)
 
 (0.1)
 
Other (income) expense, net*
(60)
 
 (0.2)
273
 
1.1
 
 
Restructuring
 145
0.5
 
85
 
0.4
 
 
Earnings before provision for taxes on income
 6,762
26.5
 
5,840
 
24.3
 
15.8
Provision for taxes on income
 1,618
6.4
 
1,026
 
4.3
 
57.7
Net earnings
5,144
$ 
 
4,814
$ 
20.0
 
6.9
```

---

## Item 13/25 — `hqa_FB_cb5deceb_masked`

- **source**: financebench / financebench_id_00215
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Is Verizon a capital intensive business based on FY 2022 data?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Consolidated Balance Sheets 
Verizon Communications Inc. and Subsidiaries 
(dollars in millions, except per share amounts) 
At December 31,
2022
2021 
Assets 
Current assets 
Cash and cash equivalents
$ 
2,605 
$ 
2,921 
Accounts receivable
 
25,332 
 
24,742 
Less Allowance for credit losses
 
826 
 
896 
Accounts receivable, net 
 
24,506 
 
23,846 
Inventories
 
2,388 
 
3,055 
Prepaid expenses and other
 
8,358 
 
6,906 
Total current assets
 
37,857 
 
36,728 
Property, plant and equipment
 
307,689 
 
289,897 
Less Accumulated depreciation
 
200,255 
 
190,201 
Property, plant and equipment, net
 
107,434 
 
99,696 
Investments in unconsolidated businesses
 
1,071 
 
1,061 
Wireless licenses
 
149,796 
 
147,619 
Goodwill
 
28,671 
 
28,603 
Other intangible assets, net
 
11,461 
 
11,677 
Operating lease right-of-use assets
 
26,130 
 
27,883 
Other assets
 
17,260 
 
13,329 
Total assets
$ 
$ 
366,596

Consolidated Operating Revenues 
(dollars in millions) 
Increase/(Decrease) 
Years Ended December 31,
2022
2021 
2022 vs. 2021 
Consumer
$ 103,506 
$ 95,300 $ 
8,206 
 8.6 % 
Business
31,072 
31,042 
30 
 0.1 
Corporate and other
2,510 
7,722 
(5,212) 
 (67.5) 
Eliminations
(253)
(451)
198 
 43.9 
Consolidated Operating Revenues
$ 133,613 $ 
3,222 
 2.4
```

---

## Item 14/25 — `hqa_FB_cfe29aff_masked`

- **source**: financebench / financebench_id_00216
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Verizon have a reasonably healthy liquidity profile based on its quick ratio for FY 2022? If the quick ratio is not relevant to measure liquidity, please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Consolidated Balance Sheets 
Verizon Communications Inc. and Subsidiaries 
(dollars in millions, except per share amounts) 
At December 31,
2022
2021 
Assets 
Current assets 
Cash and cash equivalents
$ 
2,605 
$ 
2,921 
Accounts receivable
 
25,332 
 
24,742 
Less Allowance for credit losses
 
826 
 
896 
Accounts receivable, net 
 
24,506 
 
23,846 
Inventories
 
 
3,055 
Prepaid expenses and other
 
 
6,906 
Total current assets
 
 
36,728 
Property, plant and equipment
 
307,689 
 
289,897 
Less Accumulated depreciation
 
200,255 
 
190,201 
Property, plant and equipment, net
 
107,434 
 
99,696 
Investments in unconsolidated businesses
 
1,071 
 
1,061 
Wireless licenses
 
149,796 
 
147,619 
Goodwill
 
28,671 
 
28,603 
Other intangible assets, net
 
11,461 
 
11,677 
Operating lease right-of-use assets
 
26,130 
 
27,883 
Other assets
 
17,260 
 
13,329 
Total assets
$ 
379,680 
$ 
366,596 
Liabilities and Equity 
Current liabilities 
Debt maturing within one year
$ 
9,963 
$ 
7,443 
Accounts payable and accrued liabilities
 
23,977 
 
24,833 
Current operating lease liabilities
 
4,134 
 
3,859 
Other current liabilities
 
12,097 
 
11,025 
Total current liabilities
 
 
 
 
 
 
 
 
 
 
 
 
 
47,160
```

---

## Item 15/25 — `hqa_FB_d397e71d_masked`

- **source**: financebench / financebench_id_00651
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Is growth in JnJ's adjusted EPS expected to accelerate in FY2023?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
2022 Fourth-Quarter reported sales decline of 4.4% to $23.7 Billion primarily driven by unfavorable 
foreign exchange and reduced COVID-19 Vaccine sales vs. prior year. Operational growth excluding 
COVID-19 Vaccine of 4.6%* 
 2022 Fourth-Quarter earnings per share (EPS) of $1.33 decreasing 24.9% and adjusted EPS of $2.35 
increasing by 10.3%* 
__________________________________________________________________________________________ 
 2022 Full-Year reported sales growth of 1.3% to $94.9 Billion primarily driven by strong commercial 
execution partially offset by unfavorable foreign exchange. Operational growth of 6.1%* 
 2022 Full-Year earnings per share (EPS) of $6.73 decreasing 13.8% and adjusted EPS of $10.15 
__________________________________________________________________________________________ 
 Company guides 2023 adjusted operational sales growth excluding COVID-19 Vaccine of 4.0%* and
```

---

## Item 16/25 — `hqa_FB_e3f5b062_masked`

- **source**: financebench / financebench_id_00807
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does 3M have a reasonably healthy liquidity profile based on its quick ratio for Q2 of FY2023? If the quick ratio is not relevant to measure liquidity, please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
3M Company and Subsidiaries
Consolidated Balance Sheet
(Unaudited)
(Dollars in millions, except per share amount)
June 30, 2023
December 31, 2022
Assets
Current assets
Cash and cash equivalents
$
4,258 
$
3,655 
Marketable securities current
56 
238 
Accounts receivable net of allowances of $160 and $174
4,947 
4,532 
Inventories
Finished goods
2,526 
2,497 
Work in process
1,527 
1,606 
Raw materials and supplies
1,227 
1,269 
Total inventories
5,280 
5,372 
Prepaids
674 
435 
Other current assets
539 
456 
Total current assets
14,688 
Property, plant and equipment
26,459 
25,998 
Less: Accumulated depreciation
(17,248)
(16,820)
Property, plant and equipment net
9,211 
9,178 
Operating lease right of use assets
812 
829 
Goodwill
12,869 
12,790 
Intangible assets net
4,470 
4,699 
Other assets
5,764 
4,271 
Total assets
$
48,880 
$
46,455 
Liabilities
Current liabilities
Short-term borrowings and current portion of long-term debt
$
3,033 
$
1,938 
Accounts payable
3,231 
3,183 
Accrued payroll
785 
692 
Accrued income taxes
172 
259 
Operating lease liabilities current
244 
261 
Other current liabilities
3,471 
3,190 
Total current liabilities
9,523
```

---

## Item 17/25 — `hqa_FB_e671ffe0_masked`

- **source**: financebench / financebench_id_00517
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Are there any product categories / service categories that represent more than 20% of Boeing's revenue for FY2022?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
The Boeing Company and Subsidiaries
Notes to the Consolidated Financial Statements
Summary of Business Segment Data
(Dollars in millions)
 
Years ended December 31,
2022
2021
2020
Revenues:
Commercial Airplanes
$19,493 
$16,162 
Defense, Space & Security
26,540 
26,257 
Global Services
16,328 
15,543 
Boeing Capital
199 
272 
261 
Unallocated items, eliminations and other
(231)
(347)
(65)
Total revenues
$62,286 
$58,158
```

---

## Item 18/25 — `hqa_FB_f0c3b380_masked`

- **source**: financebench / financebench_id_00956
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Are JnJ's FY2022 financials that of a high growth company?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
Results of Operations
Analysis of Consolidated Sales
For discussion on results of operations and financial condition pertaining to the fiscal years 2021 and 2020 see the Companys Annual Report on Form 10-
K for the fiscal year ended January 2, 2022, Item 7. Management's Discussion and Analysis of Results of Operations and Financial Condition.
Sales increase/(decrease) due to:
2022
2021
Volume
6.9 %
12.9 %
Price
(0.8)
(0.7)
Currency
(4.8)
1.4 
Total
13.6 %
```

---

## Item 19/25 — `hqa_FQ_1a22ef34_masked`

- **source**: finqa / ETR/2016/page_396.pdf-4
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate in net revenue in 2016 for entergy new orleans , inc?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
entergy new orleans , inc .
and subsidiaries management 2019s financial discussion and analysis results of operations net income 2016 compared to 2015 net income increased $ 3.9 million primarily due to higher net revenue , partially offset by higher depreciation and amortization expenses , higher interest expense , and lower other income .
2015 compared to 2014 net income increased $ 13.9 million primarily due to lower other operation and maintenance expenses and higher net revenue , partially offset by a higher effective income tax rate .
net revenue 2016 compared to 2015 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges .
following is an analysis of the change in net revenue comparing 2016 to 2015 .
amount ( in millions ) .

 | amount ( in millions )
retail electric price | 39.0
net gas revenue | -2.5 ( 2.5 )
volume/weather | -5.1 ( 5.1 )
other | -8.1 ( 8.1 )

the retail electric price variance is primarily due to an increase in the purchased power and capacity acquisition cost recovery rider , as approved by the city council , effective with the first billing cycle of march 2016 , primarily related to the purchase of power block 1 of the union power station .
see note 14 to the financial statements for discussion of the union power station purchase .
the net gas revenue variance is primarily due to the effect of less favorable weather on residential and commercial sales .
the volume/weather variance is primarily due to a decrease of 112 gwh , or 2% ( 2 % ) , in billed electricity usage , partially offset by the effect of favorable weather on commercial sales and a 2% ( 2 % ) increase in the average number of electric customers. .
```

---

## Item 20/25 — `hqa_FQ_23b54354_masked`

- **source**: finqa / SNA/2018/page_33.pdf-1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percent change in the snap-on performance from 2015 to 2016

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
2018 annual report 23 five-year stock performance graph the graph below illustrates the cumulative total shareholder return on snap-on common stock since december 31 , 2013 , of a $ 100 investment , assuming that dividends were reinvested quarterly .
the graph compares snap-on 2019s performance to that of the standard & poor 2019s 500 industrials index ( 201cs&p 500 industrials 201d ) and standard & poor 2019s 500 stock index ( 201cs&p 500 201d ) .
fiscal year ended ( 1 ) snap-on incorporated s&p 500 industrials s&p 500 .

fiscal year ended ( 1 ) | snap-onincorporated | s&p 500industrials | s&p 500
december 31 2013 | $ 100.00 | $ 100.00 | $ 100.00
december 31 2015 | 161.15 | 107.04 | 115.26
december 31 2017 | 169.61 | 153.99 | 157.22
december 31 2018 | 144.41 | 133.53 | 150.33

( 1 ) the company 2019s fiscal year ends on the saturday that is on or nearest to december 31 of each year ; for ease of calculation , the fiscal year end is assumed to be december 31. .
```

---

## Item 21/25 — `hqa_FQ_23de6e2d_masked`

- **source**: finqa / RSG/2010/page_135.pdf-1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: from 2009 to 2010 what was the percentage change in the expected volatility

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
2006 plan prior to december 5 , 2008 became fully vested and nonforfeitable upon the closing of the acquisition .
awards may be granted under the 2006 plan , as amended and restated , after december 5 , 2008 only to employees and consultants of allied waste industries , inc .
and its subsidiaries who were not employed by republic services , inc .
prior to such date .
at december 31 , 2010 , there were approximately 15.3 million shares of common stock reserved for future grants under the 2006 plan .
stock options we use a binomial option-pricing model to value our stock option grants .
we recognize compensation expense on a straight-line basis over the requisite service period for each separately vesting portion of the award , or to the employee 2019s retirement eligible date , if earlier .
expected volatility is based on the weighted average of the most recent one-year volatility and a historical rolling average volatility of our stock over the expected life of the option .
the risk-free interest rate is based on federal reserve rates in effect for bonds with maturity dates equal to the expected term of the option .
we use historical data to estimate future option exercises , forfeitures and expected life of the options .
when appropriate , separate groups of employees that have similar historical exercise behavior are considered separately for valuation purposes .
the weighted-average estimated fair values of stock options granted during the years ended december 31 , 2010 , 2009 and 2008 were $ 5.28 , $ 3.79 and $ 4.36 per option , respectively , which were calculated using the following weighted-average assumptions: .

 | 2010 | 2009 | 2008
risk-free interest rate | 2.4% ( 2.4 % ) | 1.4% ( 1.4 % ) | 1.7% ( 1.7 % )
dividend yield | 2.9% ( 2.9 % ) | 3.1% ( 3.1 % ) | 2.9% ( 2.9 % )
expected life ( in years ) | 4.3 | 4.2 | 4.2
contractual life ( in years ) | 7 | 7 | 7
expected forfeiture rate | 3.0% ( 3.0 % ) | 3.0% ( 3.0 % ) | 3.0% ( 3.0 % )

republic services , inc .
notes to consolidated financial statements , continued .
```

---

## Item 22/25 — `hqa_FQ_2bcd94c6_masked`

- **source**: finqa / RSG/2016/page_69.pdf-2
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the ratio of the changes in assets and liabilities , net of effects from business acquisitions and divestitures in 2016 to 2015

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
liquidity and capital resources the major components of changes in cash flows for 2016 , 2015 and 2014 are discussed in the following paragraphs .
the following table summarizes our cash flow from operating activities , investing activities and financing activities for the years ended december 31 , 2016 , 2015 and 2014 ( in millions of dollars ) : .

 | 2016 | 2015 | 2014
net cash provided by operating activities | $ 1847.8 | $ 1679.7 | $ 1529.8
net cash used in investing activities | -961.2 ( 961.2 ) | -1482.8 ( 1482.8 ) | -959.8 ( 959.8 )
net cash used in financing activities | -851.2 ( 851.2 ) | -239.7 ( 239.7 ) | -708.1 ( 708.1 )

as of december 31 , 2016 and 2015 , our days sales outstanding were 38.1 and 38.3 days , or 26.1 and 25.8 days net of deferred revenue , respectively .
2022 our accounts payable decreased $ 9.8 million during 2016 compared to an increase of $ 35.6 million during 2015 , due to the timing of payments .
2022 cash paid for capping , closure and post-closure obligations was $ 11.0 million lower during 2016 compared to 2015 .
the decrease in cash paid for capping , closure , and post-closure obligations is primarily due to payments in 2015 related to a required capping event at one of our closed landfills .
2022 cash paid for remediation obligations was $ 13.2 million lower during 2016 compared to 2015 primarily due to the timing of obligations .
in addition , cash paid for income taxes was approximately $ 265 million and $ 321 million for 2016 and 2015 , respectively .
income taxes paid in 2016 and 2015 reflect the favorable tax depreciation provisions of the protecting americans from tax hikes act signed into law in december 2015 as well as the realization of certain tax credits .
cash paid for interest was $ 330.2 million and $ 327.6 million for 2016 and 2015 , respectively .
as of december 31 , 2015 and 2014 , our days sales outstanding were 38 days , or 26 and 25 days net of deferred revenue , respectively .
2022 our accounts payable increased $ 35.6 million and $ 3.3 million during 2015 and 2014 , respectively , due to the timing of payments as of december 31 , 2015. .
```

---

## Item 23/25 — `hqa_FQ_2eaf4c8c_masked`

- **source**: finqa / ETR/2004/page_216.pdf-4
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percent change in receivables from or ( payables to ) the money pool from 2001 to 2002?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
entergy louisiana , inc .
management's financial discussion and analysis setting any of entergy louisiana's rates .
therefore , to the extent entergy louisiana's use of the proceeds would ordinarily have reduced its rate base , no change in rate base shall be reflected for ratemaking purposes .
the sec approval for additional return of equity capital is now expired .
entergy louisiana's receivables from or ( payables to ) the money pool were as follows as of december 31 for each of the following years: .

2004 | 2003 | 2002 | 2001
( in thousands ) | ( in thousands ) | ( in thousands ) | ( in thousands )

money pool activity used $ 81.9 million of entergy louisiana's operating cash flow in 2004 , provided $ 60.2 million in 2003 , and used $ 15.0 million in 2002 .
see note 4 to the domestic utility companies and system energy financial statements for a description of the money pool .
investing activities the decrease of $ 25.1 million in net cash used by investing activities in 2004 was primarily due to decreased spending on customer service projects , partially offset by increases in spending on transmission projects and fossil plant projects .
the increase of $ 56.0 million in net cash used by investing activities in 2003 was primarily due to increased spending on customer service , transmission , and nuclear projects .
financing activities the decrease of $ 404.4 million in net cash used by financing activities in 2004 was primarily due to : 2022 the net issuance of $ 98.0 million of long-term debt in 2004 compared to the retirement of $ 261.0 million in 2022 a principal payment of $ 14.8 million in 2004 for the waterford lease obligation compared to a principal payment of $ 35.4 million in 2003 ; and 2022 a decrease of $ 29.0 million in common stock dividends paid .
the decrease of $ 105.5 million in net cash used by financing activities in 2003 was primarily due to : 2022 a decrease of $ 125.9 million in common stock dividends paid ; and 2022 the repurchase of $ 120 million of common stock from entergy corporation in 2002 .
the decrease in net cash used in 2003 was partially offset by the following : 2022 the retirement in 2003 of $ 150 million of 8.5% ( 8.5 % ) series first mortgage bonds compared to the net retirement of $ 134.6 million of first mortgage bonds in 2002 ; and 2022 principal payments of $ 35.4 million in 2003 for the waterford 3 lease obligation compared to principal payments of $ 15.9 million in 2002 .
see note 5 to the domestic utility companies and system energy financial statements for details of long-term debt .
uses of capital entergy louisiana requires capital resources for : 2022 construction and other capital investments ; 2022 debt and preferred stock maturities ; 2022 working capital purposes , including the financing of fuel and purchased power costs ; and 2022 dividend and interest payments. .
```

---

## Item 24/25 — `hqa_FQ_34845583_masked`

- **source**: finqa / C/2009/page_195.pdf-1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in the allowance for loan losses from 2008 to 2009?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
18 .
allowance for credit losses .

in millions of dollars | 2009 | 2008 ( 1 ) | 2007 ( 1 )
gross credit losses | -32784 ( 32784 ) | -20760 ( 20760 ) | -11864 ( 11864 )
gross recoveries | 2043 | 1749 | 1938
net credit ( losses ) recoveries ( ncls ) | $ -30741 ( 30741 ) | $ -19011 ( 19011 ) | $ -9926 ( 9926 )
ncls | $ 30741 | $ 19011 | $ 9926
net reserve builds ( releases ) | 5741 | 11297 | 6550
net specific reserve builds ( releases ) | 2278 | 3366 | 356
total provision for credit losses | $ 38760 | $ 33674 | $ 16832
other net ( 2 ) | -1602 ( 1602 ) | -1164 ( 1164 ) | 271
allowance for credit losses on unfunded lending commitments at beginning of year ( 3 ) | $ 887 | $ 1250 | $ 1100
provision for unfunded lending commitments | 244 | -363 ( 363 ) | 150
allowance for credit losses on unfunded lending commitments at end of year ( 3 ) | $ 1157 | $ 887 | $ 1250
total allowance for loans leases and unfunded lending commitments | $ 37190 | $ 30503 | $ 17367

( 1 ) reclassified to conform to the current period 2019s presentation .
( 2 ) 2009 primarily includes reductions to the loan loss reserve of approximately $ 543 million related to securitizations , approximately $ 402 million related to the sale or transfers to held-for-sale of u.s .
real estate lending loans , and $ 562 million related to the transfer of the u.k .
cards portfolio to held-for-sale .
2008 primarily includes reductions to the loan loss reserve of approximately $ 800 million related to fx translation , $ 102 million related to securitizations , $ 244 million for the sale of the german retail banking operation , $ 156 million for the sale of citicapital , partially offset by additions of $ 106 million related to the cuscatl e1n and bank of overseas chinese acquisitions .
2007 primarily includes reductions to the loan loss reserve of $ 475 million related to securitizations and transfers to loans held-for-sale , and reductions of $ 83 million related to the transfer of the u.k .
citifinancial portfolio to held-for-sale , offset by additions of $ 610 million related to the acquisitions of egg , nikko cordial , grupo cuscatl e1n and grupo financiero uno .
( 3 ) represents additional credit loss reserves for unfunded corporate lending commitments and letters of credit recorded in other liabilities on the consolidated balance sheet. .
```

---

## Item 25/25 — `hqa_FQ_425a8ac9_masked`

- **source**: finqa / PNC/2007/page_93.pdf-1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in commercial commitments net of participations , assignments and syndications , primarily to financial services companies in 2007 compared to 2006 in billions?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
net unfunded credit commitments .

december 31 - in millions | 2007 | 2006
commercial | $ 39171 | $ 31009
consumer | 10875 | 10495
commercial real estate | 2734 | 2752
other | 567 | 579
total | $ 53347 | $ 44835

commitments to extend credit represent arrangements to lend funds subject to specified contractual conditions .
commitments generally have fixed expiration dates , may require payment of a fee , and contain termination clauses in the event the customer 2019s credit quality deteriorates .
based on our historical experience , most commitments expire unfunded , and therefore cash requirements are substantially less than the total commitment .
consumer home equity lines of credit accounted for 80% ( 80 % ) of consumer unfunded credit commitments .
unfunded credit commitments related to market street totaled $ 8.8 billion at december 31 , 2007 and $ 5.6 billion at december 31 , 2006 and are included in the preceding table primarily within the 201ccommercial 201d and 201cconsumer 201d categories .
note 24 commitments and guarantees includes information regarding standby letters of credit and bankers 2019 acceptances .
at december 31 , 2007 , the largest industry concentration was for general medical and surgical hospitals , which accounted for approximately 5% ( 5 % ) of the total letters of credit and bankers 2019 acceptances .
at december 31 , 2007 , we pledged $ 1.6 billion of loans to the federal reserve bank ( 201cfrb 201d ) and $ 33.5 billion of loans to the federal home loan bank ( 201cfhlb 201d ) as collateral for the contingent ability to borrow , if necessary .
certain directors and executive officers of pnc and its subsidiaries , as well as certain affiliated companies of these directors and officers , were customers of and had loans with subsidiary banks in the ordinary course of business .
all such loans were on substantially the same terms , including interest rates and collateral , as those prevailing at the time for comparable transactions with other customers and did not involve more than a normal risk of collectibility or present other unfavorable features .
the aggregate principal amounts of these loans were $ 13 million at december 31 , 2007 and $ 18 million at december 31 , 2006 .
during 2007 , new loans of $ 48 million were funded and repayments totaled $ 53 million. .
```

---
