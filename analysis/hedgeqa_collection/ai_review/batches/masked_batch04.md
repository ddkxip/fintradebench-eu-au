# Blind review batch `masked_batch04`

18 items. Family: `evidence_masked_insufficient`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/18 — `hqa_TAT_4e15b114_masked`

- **source**: tatqa / 3fcf5adf-273a-4265-a488-c524c0881937
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the change in the amount of Net debt and IFRS 16 lease liabilities from 2018 to 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| 2019 | 2018
 | £m | £m
Net debt | 295.2 | 235.8
IFRS 16 lease liabilities | 38.9 | –

Net debt including IFRS 16 lease liabilities
A reconciliation between net debt and net debt including IFRS 16 lease liabilities is given below. A breakdown of the balances that are included within net debt is given within Note 24. Net debt excludes IFRS 16 lease liabilities to enable comparability with prior years.
```

---

## Item 2/18 — `hqa_TAT_55755d65_masked`

- **source**: tatqa / 7b7108df-3586-4bb4-9d65-67a3a408d543
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the percentage change in the Total non-current trade and other payables in 2019 from 2018?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| 31 March 2019 | 31 March 2018
 | $M | $M
Current |  | 
Trade payables | 35.8 | 39.6
Accruals | 46.6 | 68.4
Social security and other taxes | 12.7 | 14.9
Other payables | 7.1 | 11.2
Total current trade and other payables | 102.2 | 134.1
Non-Current |  | 

22 Trade and Other Payables
Trade payables are non interest-bearing and are normally settled on 30-day terms or as otherwise agreed with suppliers.
```

---

## Item 3/18 — `hqa_TAT_5ce27434_masked`

- **source**: tatqa / 6280d80a-8042-4404-93f4-67a8e26082f9
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in the total unamortized compensation cost related to employee purchases under the ESPP the company expects to recognise between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
|  | Year ended December 31 | 
 | 2019 | 2018 | 2017
Expected life (in years) | 0.5 | 0.5 | 0.5
Volatility | 36% - 37% | 33% - 40% | 29% - 37%
Risk-free interest rate | 1.58 - 2.43% | 1.76% - 2.50% | 0.76% - 1.16%
Dividend yield | - % | - % | - %

The fair value of the option component of the ESPP shares was estimated at the grant date using the Black-Scholes option pricing model with the following weighted
average assumptions:
The Company issued 266 shares, 231 shares and 183 shares under the ESPP in the years ended December 31, 2019, 2018 and 2017, respectively, at a weighted average
related to employee purchases under the ESPP over a weighted average period of 0.37 years.
```

---

## Item 4/18 — `hqa_TAT_6ada4621_masked`

- **source**: tatqa / 33e1f138-3e4e-4ec6-a92a-9853bcec45b7
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the change between Foreign exchange forward contracts purchased for March 29, 2019 and March 30, 2018?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
(In millions) | March 29, 2019 | March 30, 2018
Net investment hedges |  | 
Foreign exchange forward contracts sold | $116 | $—
Balance sheet contracts |  | 
Foreign exchange forward contracts sold | $122 | $151

The fair value of our foreign exchange forward contracts is presented on a gross basis in our Condensed Consolidated Balance Sheets. To mitigate losses in the event of nonperformance by counterparties, we have entered into master netting arrangements with our counterparties that allow us to settle payments on a net basis. The effect of netting on our derivative assets and liabilities was not material as of March 29, 2019 and March 30, 2018.
The notional amount of our outstanding foreign exchange forward contracts in U.S. dollar equivalent was as follows:
```

---

## Item 5/18 — `hqa_TAT_7cc28393_masked`

- **source**: tatqa / 33e2cec1-a31d-4782-90ae-0995e9d16547
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in the current accrued benefit liability between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| September 30, | 
 | 2019 | 2018
 | (Amounts in thousands) | 
Non-current accrued benefit liability | 6,904 | 6,168
Total accrued benefit liability | $7,239 | $6,508

Plans with projected benefit obligations in excess of plan assets are attributable to unfunded domestic supplemental retirement plans, and our U.K. retirement plan.
Accrued benefit liability reported as:
As of September 30, 2019 and 2018, the amounts included in accumulated other comprehensive income, consisted of
deferred net losses totaling approximately $6.3 million and $5.3 million, respectively.
The amount of net deferred loss expected to be recognized as a component of net periodic benefit cost for the year ending September 30, 2019, is approximately $229 thousand.
```

---

## Item 6/18 — `hqa_TAT_819756ff_masked`

- **source**: tatqa / cbde27b6-5c33-4d93-a59b-b0881a27da1f
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the percentage change in Interest expense in 2019 from 2018?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| 2019 | 2018 | 2018-2019 Change
 |  | (in millions) | 
Interest income | $(24.8) | $(26.7) | $1.9
Other (income) expense, net | 29.5 | 1.4 | 28.1

Interest and Other
Interest income decreased by $1.9 million from 2018 to 2019 due primarily to lower cash and marketable securities balances in 2019. Interest expense decreased by $8.2 million from 2018 to 2019 due primarily to unrealized losses on equity marketable securities recognized in 2018. Other (income) expense, net increased by $28.1 million from 2018 to 2019 due primarily to a $15.0 million charge for the impairment of the investment in RealWear and an $11.5 million change in pension actuarial (gains) losses from a $3.3 million gain in 2018 to an $8.2 million loss in 2019.
```

---

## Item 7/18 — `hqa_TAT_83225fed_masked`

- **source**: tatqa / 42b056e9-665f-4d90-8876-826757889087
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the change in the Property and equipment, net from 2018 to 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
December 31, |  | 
 | 2019 | 2018
Computer equipment and purchased software | $3,011 | $3,167
Machinery and equipment | 699 | 821
Furniture and fixtures | 1,115 | 1,113
Leasehold improvements (1) | 3,897 | 3,897
Total | 8,722 | 8,998
Less accumulated depreciation and amortization (1) | (7,496) | (6,655)

Property and Equipment
Property and equipment are as follows (in thousands):
(1) In the fourth quarter 2019, the Company announced its decision to exit the San Jose California facility (“SJ Facility”) by March 31, 2020. The Company accelerated the amortization of its SJ Facility leasehold improvements over the remaining estimated life which is estimated to be through March 31, 2020. As of December 31, 2019, the net book value of the SJ Facility leasehold improvements was $0.9 million and will be fully amortized by March 31, 2020.
```

---

## Item 8/18 — `hqa_TAT_863ac028_masked`

- **source**: tatqa / 08885f18-ca2c-4e92-8c32-70916adef5fe
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in the net value of property and equipment between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
As of December 31, |  | 
 | 2019 | 2018
Computers, software, furniture and fixtures | $1,406 | $1,407
Equipment under capital lease  3,348 | 3,348 | 3,525
Less accumulated depreciation and amortization | (3,171) | (2,448)

4. Property and Equipment
Property and equipment consist of the following (in thousands):
Depreciation and amortization expense was $0.9 million and $1.0 million for the years ended December 31, 2019 and 2018, respectively.
```

---

## Item 9/18 — `hqa_TAT_924db34b_masked`

- **source**: tatqa / cca74d6f-5b53-4928-8534-4ddc1453522c
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in the fair market value between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
|  |  | April 30, 2019 | 
 | Cost | Gross Unrealized Gains | Gross Unrealized Losses | Fair Market Value
 |  |  | April 30, 2018 | 
 | Cost | Gross Unrealized Gains | Gross Unrealized Losses | Fair Market Value

8. Marketable Securities
The cost, gross unrealized gains, gross unrealized losses and fair market value of available-for-sale securities at April 30, 2019 and 2018, respectively, were as follows (in thousands):
```

---

## Item 10/18 — `hqa_TAT_9410c4da_masked`

- **source**: tatqa / dc7bfc5a-cd41-4f16-be0d-7ca2d2b89eac
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in the pension discount rate for actuarial benefit obligations between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
As at December 31, | Pension 2019 | Other 2019 | Pension 2018 | Other 2018
Actuarial benefit obligation |  |  |  | 
Benefit costs for the year ended |  |  |  | 
Discount rate | 3.90% | 3.90% to 4.00% | 3.60% | 3.25% to 3.60%
Future salary growth | 2.50% | N/A | 2.50% | N/A
Health care cost trend rate | N/A | 3.49% to 5.49% | N/A | 4.50%
Other medical trend rates | N/A | 4.00% to 4.56% | N/A | 4.50%

The following are the significant assumptions adopted in measuring the Company’s pension and other benefit obligations:
For certain Canadian post-retirement plans the above trend rates are applicable for 2019 to 2024 which will increase linearly to 4.75% in 2029 and grading down to an ultimate rate of 3.57% per annum in 2040 and thereafter.
```

---

## Item 11/18 — `hqa_TAT_a757ebed_masked`

- **source**: tatqa / 77191f82-0a18-4050-8911-bff9f1a401d9
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the percentage change in total inventories between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| March 31, | 
 | 2019 | 2018
Raw materials | $74.5 | $26.0
Work in process | 413.0 | 311.8
Finished goods | 224.2 | 138.4

Inventories
The components of inventories consist of the following (in millions):
Inventories are valued at the lower of cost and net realizable value using the first-in, first-out method. Inventory impairment charges establish a new cost basis for inventory and charges are not subsequently reversed to income even if circumstances later suggest that increased carrying amounts are recoverable.
```

---

## Item 12/18 — `hqa_TAT_a8d33126_masked`

- **source**: tatqa / d09332c7-20e6-426a-ba9b-1bdd2baa8702
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in balance at end of year from 2018 to 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| December 31, | 
 | 2018 | 2019
Charged to cost of sales | 18,408 | 26,301
Deductions | (8,985) | (12,232)
Releases of expired warranty | (8,214) | (5,684)
Foreign currency translation effect | 184 | 84

NOTE 14. PROVISION FOR WARRANTY
The changes in the amount of provision for warranty are as follows:
Costs of warranty include the cost of labor and materials to repair a product during the warranty period. The main term of the warranty period is one year. The Company accrues for the estimated cost of the warranty on its products shipped in the provision for warranty, upon recognition of the sale of the product. The costs are estimated based on actual historical expenses incurred and on estimated future expenses related to current sales, and are updated periodically. Actual warranty costs are charged against the provision for warranty.
```

---

## Item 13/18 — `hqa_TAT_b1f0677c_masked`

- **source**: tatqa / 2f6f4311-f09e-435c-9e06-fc475a876901
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in total remuneration from 2018 to 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| Year ended  December 31 | 
 | 2018 | 2019
Supervisory Board: |  | 
J.C. Lobbezoo | 78.6 | 83.5
H.W. Kreutzer 1) | 21.4 | 0.0
M.C.J. van Pernis | 56.0 | 58.5
U.H.R. Schumacher | 53.5 | 56.0
S. Kahle-Galonske | 55.9 | 60.0
M.J.C. de Jong 2) | 34.0 | 57.5

SUPERVISORY BOARD
The following table sets forth information concerning all remuneration (base compensation, no bonuses or pensions were paid) from the Company (including its subsidiaries) for services in all capacities to all current and former members of the Supervisory Board of the Company:
1 Period January 1 to May 28, 2018
2 Period as of May 28, 2018
The remuneration of members of the Supervisory Board has been determined by the 2018 Annual General Meeting of Shareholders.
No stock options or performance shares have been granted to members of the Supervisory Board.
```

---

## Item 14/18 — `hqa_TAT_b5e1cbd8_masked`

- **source**: tatqa / b55a0581-b496-4d82-8b51-2a041d6e7729
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the percentage change in total other current assets in 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| As of December 31, | 
 | 2019 | 2018
 | (Dollars in millions) | 
Prepaid expenses | $274 | 307
Income tax receivable | 35 | 82
Materials, supplies and inventory | 105 | 120
Contract assets | 42 | 52
Contract acquisition costs | 178 | 167
Contract fulfillment costs | 115 | 82
Other | 59 | 108

Other Current Assets
The following table presents details of other current assets in our consolidated balance sheets:
```

---

## Item 15/18 — `hqa_TAT_bf17a5c6_masked`

- **source**: tatqa / 41f11c5b-c73d-4ec1-88f7-4216ae207eb4
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the percentage change in Other (income) expense, net in 2019 from 2018?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| 2019 | 2018 | 2018-2019 Change
 |  | (in millions) | 
Interest income | $(24.8) | $(26.7) | $1.9
Interest expense | 23.1 | 31.3 | (8.2)

Interest and Other
Interest income decreased by $1.9 million from 2018 to 2019 due primarily to lower cash and marketable securities balances in 2019. Interest expense decreased by $8.2 million from 2018 to 2019 due primarily to unrealized losses on equity marketable securities recognized in 2018. Other (income) expense, net increased by $28.1 million from 2018 to 2019 due primarily to a $15.0 million charge for the impairment of the investment in RealWear and an $11.5 million change in pension actuarial (gains) losses from a $3.3 million gain in 2018 to an $8.2 million loss in 2019.
```

---

## Item 16/18 — `hqa_TAT_d24aae82_masked`

- **source**: tatqa / 058d94f1-d1c9-4bc6-b570-22db3be6fe71
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the change in total revenue from 2018 to 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| Year ended December 31, | 
(EUR thousand) | 2018 | 2019
Equipment revenue | 631,504 | 1,068,645
Spares & service revenue | 186,577 | 215,215

Revenue stream
The Company generates revenue primarily from the sales of equipment and sales of spares & service. The products and services described by nature in Note 1, can be part of all revenue streams.
The proceeds resulting from the patent litigation & arbitration settlements (€159 million) are included in the equipment revenue stream.
```

---

## Item 17/18 — `hqa_TAT_f0b19718_masked`

- **source**: tatqa / 03ffdb11-7405-45dc-85e1-2ce82bad663b
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What is the change in loss per share between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| Year Ended December 31 | 
 | 2019 | 2018
Revenues (in thousands) | $ 224,913 | $ 17,542
Loss from continuing operations (in thousands) | $ (13,432) | $ ( 7,792)
Weighted average number of common shares outstanding - basic and diluted | 32,359,316 | 22,099,149

Our revenues for 2019 include $1.9 million related to the acquired MGI business. Our net loss for 2019 includes $0.3 million of net loss from the acquired MGI business. The following table provides unaudited pro forma information for the periods presented as if the MGI acquisition had occurred January 1, 2018.
No adjustments have been made in the pro forma information for synergies that are resulting or planned from the MGI acquisition. The unaudited proforma information is not indicative of the results that may have been achieved had the companies been combined as of January 1, 2018, or of our future operating results.
```

---

## Item 18/18 — `hqa_TAT_f4ec2a00_masked`

- **source**: tatqa / 8b08afaf-e692-4891-9595-386a78e4de56
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: What was the change in the Basic weighted average common shares outstanding between 2018 and 2019?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
| 2019 | 2018 | 2017
Net income | 108,616 | 13,040 | 112,062
Dilutive effect of share-based awards and options outstanding | 803 | 916 | 941
Diluted weighted average shares outstanding | 31,074 | 33,919 | 34,553
Earnings per share: |  |  | 
Basic | 3.59 | 0.40 | 3.33
Diluted | 3.50 | 0.38 | 3.24

7. Earnings Per Share
The following is a reconciliation of the amounts utilized in the computation of basic and diluted earnings per share for fiscal2 019, 2018 and 2017 (in thousands, except per share amounts):
In each of the fiscal years 2019, 2018 and 2017, share-based awards for approximately 0.1 million shares were not included in the computation of diluted earnings per share as they were antidilutive.
```

---
