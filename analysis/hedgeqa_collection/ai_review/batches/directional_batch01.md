# Blind review batch `directional_batch01`

25 items. Family: `numeric_to_directional`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_CFQ_05f42dea`

- **source**: convfinqa / Single_ETR/2016/page_396.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in net revenue that was due the net gas revenue adjustment and the volume/weather adjustment, combined, in millions?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='add(-2.5, -5.1)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy new orleans , inc .
and subsidiaries management 2019s financial discussion and analysis results of operations net income 2016 compared to 2015 net income increased $ 3.9 million primarily due to higher net revenue , partially offset by higher depreciation and amortization expenses , higher interest expense , and lower other income .
2015 compared to 2014 net income increased $ 13.9 million primarily due to lower other operation and maintenance expenses and higher net revenue , partially offset by a higher effective income tax rate .
net revenue 2016 compared to 2015 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges .
following is an analysis of the change in net revenue comparing 2016 to 2015 .
amount ( in millions ) .

 | amount ( in millions )
2015 net revenue | $ 293.9
retail electric price | 39.0
net gas revenue | -2.5 ( 2.5 )
volume/weather | -5.1 ( 5.1 )
other | -8.1 ( 8.1 )
2016 net revenue | $ 317.2

the retail electric price variance is primarily due to an increase in the purchased power and capacity acquisition cost recovery rider , as approved by the city council , effective with the first billing cycle of march 2016 , primarily related to the purchase of power block 1 of the union power station .
see note 14 to the financial statements for discussion of the union power station purchase .
the net gas revenue variance is primarily due to the effect of less favorable weather on residential and commercial sales .
the volume/weather variance is primarily due to a decrease of 112 gwh , or 2% ( 2 % ) , in billed electricity usage , partially offset by the effect of favorable weather on commercial sales and a 2% ( 2 % ) increase in the average number of electric customers. .
```

---

## Item 2/25 — `hqa_CFQ_07480310`

- **source**: convfinqa / Single_UPS/2009/page_33.pdf-2#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the performance of the united parcel service inc . from 2004 to 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(75.95, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
( 1 ) includes shares repurchased through our publicly announced share repurchase program and shares tendered to pay the exercise price and tax withholding on employee stock options .
shareowner return performance graph the following performance graph and related information shall not be deemed 201csoliciting material 201d or to be 201cfiled 201d with the securities and exchange commission , nor shall such information be incorporated by reference into any future filing under the securities act of 1933 or securities exchange act of 1934 , each as amended , except to the extent that the company specifically incorporates such information by reference into such filing .
the following graph shows a five-year comparison of cumulative total shareowners 2019 returns for our class b common stock , the s&p 500 index , and the dow jones transportation average .
the comparison of the total cumulative return on investment , which is the change in the quarterly stock price plus reinvested dividends for each of the quarterly periods , assumes that $ 100 was invested on december 31 , 2004 in the s&p 500 index , the dow jones transportation average , and our class b common stock .
comparison of five year cumulative total return $ 40.00 $ 60.00 $ 80.00 $ 100.00 $ 120.00 $ 140.00 $ 160.00 2004 20092008200720062005 s&p 500 ups dj transport .

 | 12/31/04 | 12/31/05 | 12/31/06 | 12/31/07 | 12/31/08 | 12/31/09
united parcel service inc . | $ 100.00 | $ 89.49 | $ 91.06 | $ 87.88 | $ 70.48 | $ 75.95
s&p 500 index | $ 100.00 | $ 104.91 | $ 121.48 | $ 128.15 | $ 80.74 | $ 102.11
dow jones transportation average | $ 100.00 | $ 111.65 | $ 122.61 | $ 124.35 | $ 97.72 | $ 115.88

.
```

---

## Item 3/25 — `hqa_CFQ_08d45061`

- **source**: convfinqa / Single_EXR/2005/page_46.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the net change in value of the high bid price for the quarter ended december 31, 2004 and the quarter ended march 31, 2005?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(14.30, 14.55)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
part ii item 5 .
market for registrant 2019s common equity and related stockholder matters market information our common stock has been traded on the new york stock exchange ( 2018 2018nyse 2019 2019 ) under the symbol 2018 2018exr 2019 2019 since our ipo on august 17 , 2004 .
prior to that time there was no public market for our common stock .
the following table sets forth , for the periods indicated , the high and low bid price for our common stock as reported by the nyse and the per share dividends declared : dividends high low declared .

 | high | low | dividends declared
period from august 17 2004 to september 30 2004 | $ 14.38 | $ 12.50 | $ 0.1113
quarter ended december 31 2004 | 14.55 | 12.60 | 0.2275
quarter ended march 31 2005 | 14.30 | 12.55 | 0.2275
quarter ended june 30 2005 | 14.75 | 12.19 | 0.2275
quarter ended september 30 2005 | 16.71 | 14.32 | 0.2275
quarter ended december 31 2005 | 15.90 | 13.00 | 0.2275

on february 28 , 2006 , the closing price of our common stock as reported by the nyse was $ 15.00 .
at february 28 , 2006 , we had 166 holders of record of our common stock .
holders of shares of common stock are entitled to receive distributions when declared by our board of directors out of any assets legally available for that purpose .
as a reit , we are required to distribute at least 90% ( 90 % ) of our 2018 2018reit taxable income 2019 2019 is generally equivalent to our net taxable ordinary income , determined without regard to the deduction for dividends paid , to our stockholders annually in order to maintain our reit qualifications for u.s .
federal income tax purposes .
unregistered sales of equity securities and use of proceeds on june 20 , 2005 , we completed the sale of 6200000 shares of our common stock , $ .01 par value , for $ 83514 , which we reported in a current report on form 8-k filed with the securities and exchange commission on june 24 , 2005 .
we used the proceeds for general corporate purposes , including debt repayment .
the shares were issued pursuant to an exemption from registration under the securities act of 1933 , as amended. .
```

---

## Item 4/25 — `hqa_CFQ_3cabceab`

- **source**: convfinqa / Single_CMCSA/2015/page_150.pdf-1#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the difference in comprehensive income attributable to nbc universal between 2013 and 2014?

Question: and the percentage change?

**Original source question**: and the percentage change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(2972, 2017), divide(#0, 2017)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
nbcuniversal media , llc consolidated statement of comprehensive income .

year ended december 31 ( in millions ) | 2015 | 2014 | 2013
net income | $ 3624 | $ 3297 | $ 2122
deferred gains ( losses ) on cash flow hedges net | -21 ( 21 ) | 25 | -5 ( 5 )
employee benefit obligations net | 60 | -106 ( 106 ) | 95
currency translation adjustments net | -121 ( 121 ) | -62 ( 62 ) | -41 ( 41 )
comprehensive income | 3542 | 3154 | 2171
net ( income ) loss attributable to noncontrolling interests | -210 ( 210 ) | -182 ( 182 ) | -154 ( 154 )
other comprehensive ( income ) loss attributable to noncontrolling interests | 29 | 2014 | 2014
comprehensive income attributable to nbcuniversal | $ 3361 | $ 2972 | $ 2017

see accompanying notes to consolidated financial statements .
147 comcast 2015 annual report on form 10-k .
```

---

## Item 5/25 — `hqa_CFQ_421f4e3d`

- **source**: convfinqa / Single_BKNG/2018/page_34.pdf-3#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in value for booking holding inc. in 2018, assuming a $100 initial investment?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(148.18, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
measurement point december 31 booking holdings nasdaq composite index s&p 500 rdg internet composite .

measurement pointdecember 31 | booking holdings inc . | nasdaqcomposite index | s&p 500index | rdg internetcomposite
2013 | 100.00 | 100.00 | 100.00 | 100.00
2014 | 98.09 | 114.62 | 113.69 | 96.39
2015 | 109.68 | 122.81 | 115.26 | 133.20
2016 | 126.12 | 133.19 | 129.05 | 140.23
2017 | 149.50 | 172.11 | 157.22 | 202.15
2018 | 148.18 | 165.84 | 150.33 | 201.16

.
```

---

## Item 6/25 — `hqa_CFQ_4613f27f`

- **source**: convfinqa / Single_UPS/2017/page_31.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the value of the class b common stock, considering its value in 2017 and the original amount invested in it in 2012?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(195.75, 100.00)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
shareowner return performance graph the following performance graph and related information shall not be deemed 201csoliciting material 201d or to be 201cfiled 201d with the sec , nor shall such information be incorporated by reference into any future filing under the securities act of 1933 or securities exchange act of 1934 , each as amended , except to the extent that the company specifically incorporates such information by reference into such filing .
the following graph shows a five-year comparison of cumulative total shareowners 2019 returns for our class b common stock , the standard & poor 2019s 500 index and the dow jones transportation average .
the comparison of the total cumulative return on investment , which is the change in the quarterly stock price plus reinvested dividends for each of the quarterly periods , assumes that $ 100 was invested on december 31 , 2012 in the standard & poor 2019s 500 index , the dow jones transportation average and our class b common stock. .

 | 12/31/2012 | 12/31/2013 | 12/31/2014 | 12/31/2015 | 12/31/2016 | 12/31/2017
united parcel service inc . | $ 100.00 | $ 146.54 | $ 159.23 | $ 148.89 | $ 182.70 | $ 195.75
standard & poor 2019s 500 index | $ 100.00 | $ 132.38 | $ 150.49 | $ 152.55 | $ 170.79 | $ 208.06
dow jones transportation average | $ 100.00 | $ 141.38 | $ 176.83 | $ 147.19 | $ 179.37 | $ 213.49

.
```

---

## Item 7/25 — `hqa_CFQ_4846cde1`

- **source**: convfinqa / Single_AAPL/2007/page_70.pdf-3#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the change in the allowance for doubtful accounts from 2006 to 2007?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(47, 52), divide(#0, 52)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
notes to consolidated financial statements ( continued ) note 2 2014financial instruments ( continued ) covered by collateral , third-party flooring arrangements , or credit insurance are outstanding with the company 2019s distribution and retail channel partners .
one customer accounted for approximately 11% ( 11 % ) of trade receivables as of september 29 , 2007 , while no customers accounted for more than 10% ( 10 % ) of trade receivables as of september 30 , 2006 .
the following table summarizes the activity in the allowance for doubtful accounts ( in millions ) : september 29 , september 30 , september 24 , 2007 2006 2005 .

 | september 29 2007 | september 30 2006 | september 24 2005
beginning allowance balance | $ 52 | $ 46 | $ 47
charged to costs and expenses | 12 | 17 | 8
deductions | -17 ( 17 ) | -11 ( 11 ) | -9 ( 9 )
ending allowance balance | $ 47 | $ 52 | $ 46

vendor non-trade receivables the company has non-trade receivables from certain of its manufacturing vendors resulting from the sale of raw material components to these manufacturing vendors who manufacture sub-assemblies or assemble final products for the company .
the company purchases these raw material components directly from suppliers .
these non-trade receivables , which are included in the consolidated balance sheets in other current assets , totaled $ 2.4 billion and $ 1.6 billion as of september 29 , 2007 and september 30 , 2006 , respectively .
the company does not reflect the sale of these components in net sales and does not recognize any profits on these sales until the products are sold through to the end customer at which time the profit is recognized as a reduction of cost of sales .
derivative financial instruments the company uses derivatives to partially offset its business exposure to foreign exchange risk .
foreign currency forward and option contracts are used to offset the foreign exchange risk on certain existing assets and liabilities and to hedge the foreign exchange risk on expected future cash flows on certain forecasted revenue and cost of sales .
the company 2019s accounting policies for these instruments are based on whether the instruments are designated as hedge or non-hedge instruments .
the company records all derivatives on the balance sheet at fair value. .
```

---

## Item 8/25 — `hqa_CFQ_525e330f`

- **source**: convfinqa / Single_AAP/2016/page_26.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the change in value of an investment in advance auto parts from 2015 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(217.49, 228.88)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock price performance the following graph shows a comparison of the cumulative total return on our common stock , the standard & poor 2019s 500 index and the standard & poor 2019s retail index .
the graph assumes that the value of an investment in our common stock and in each such index was $ 100 on december 31 , 2011 , and that any dividends have been reinvested .
the comparison in the graph below is based solely on historical data and is not intended to forecast the possible future performance of our common stock .
comparison of cumulative total return among advance auto parts , inc. , s&p 500 index and s&p retail index company/index december 31 , december 29 , december 28 , january 3 , january 2 , december 31 .

company/index | december 31 2011 | december 29 2012 | december 28 2013 | january 3 2015 | january 2 2016 | december 31 2016
advance auto parts | $ 100.00 | $ 102.87 | $ 158.46 | $ 228.88 | $ 217.49 | $ 244.64
s&p 500 index | 100.00 | 114.07 | 152.98 | 174.56 | 177.01 | 198.18
s&p retail index | 100.00 | 122.23 | 178.55 | 196.06 | 245.31 | 256.69

.
```

---

## Item 9/25 — `hqa_CFQ_52cedb59`

- **source**: convfinqa / Single_BLL/2011/page_29.pdf-1#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the value of ball corporation in 2008?

Question: what is the change in value from the initial $100 investment?

**Original source question**: what is the change in value from the initial $100 investment?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(97.04, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
shareholder return performance the line graph below compares the annual percentage change in ball corporation fffds cumulative total shareholder return on its common stock with the cumulative total return of the dow jones containers & packaging index and the s&p composite 500 stock index for the five-year period ended december 31 , 2011 .
it assumes $ 100 was invested on december 31 , 2006 , and that all dividends were reinvested .
the dow jones containers & packaging index total return has been weighted by market capitalization .
total return to stockholders ( assumes $ 100 investment on 12/31/06 ) total return analysis .

 | 12/31/2006 | 12/31/2007 | 12/31/2008 | 12/31/2009 | 12/31/2010 | 12/31/2011
ball corporation | $ 100.00 | $ 104.05 | $ 97.04 | $ 121.73 | $ 161.39 | $ 170.70
dj us containers & packaging | $ 100.00 | $ 106.73 | $ 66.91 | $ 93.98 | $ 110.23 | $ 110.39
s&p 500 | $ 100.00 | $ 105.49 | $ 66.46 | $ 84.05 | $ 96.71 | $ 98.75

copyright a9 2012 standard & poor fffds , a division of the mcgraw-hill companies inc .
all rights reserved .
( www.researchdatagroup.com/s&p.htm ) copyright a9 2012 dow jones & company .
all rights reserved. .
```

---

## Item 10/25 — `hqa_CFQ_5310207f`

- **source**: convfinqa / Single_LLY/2018/page_99.pdf-2#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the price of lilly in 2018?

Question: what was the net change assuming a $100 initial investment?

**Original source question**: what was the net change assuming a $100 initial investment?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(259.88, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph this graph compares the return on lilly stock with that of the standard & poor 2019s 500 stock index and our peer group for the years 2014 through 2018 .
the graph assumes that , on december 31 , 2013 , a person invested $ 100 each in lilly stock , the s&p 500 stock index , and the peer groups' common stock .
the graph measures total shareholder return , which takes into account both stock price and dividends .
it assumes that dividends paid by a company are reinvested in that company 2019s stock .
value of $ 100 invested on last business day of 2013 comparison of five-year cumulative total return among lilly , s&p 500 stock index , peer group ( 1 ) .

 | lilly | peer group | s&p 500
dec-13 | $ 100.00 | $ 100.00 | $ 100.00
dec-14 | $ 139.75 | $ 114.39 | $ 113.69
dec-15 | $ 175.21 | $ 116.56 | $ 115.26
dec-16 | $ 157.03 | $ 112.80 | $ 129.05
dec-17 | $ 185.04 | $ 128.90 | $ 157.22
dec-18 | $ 259.88 | $ 136.56 | $ 150.33

( 1 ) we constructed the peer group as the industry index for this graph .
it comprises the companies in the pharmaceutical and biotech industries that we used to benchmark the compensation of our executive officers for 2018 : abbvie inc. ; amgen inc. ; astrazeneca plc ; baxter international inc. ; biogen idec inc. ; bristol-myers squibb company ; celgene corporation ; gilead sciences inc. ; glaxosmithkline plc ; johnson & johnson ; medtronic plc ; merck & co. , inc. ; novartis ag. ; pfizer inc. ; roche holdings ag ; sanofi ; and shire plc. .
```

---

## Item 11/25 — `hqa_CFQ_5572c7eb`

- **source**: convfinqa / Single_APD/2014/page_71.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the net change in sales from 2013 to 2014?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(8.5, 52.3)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
3 .
discontinued operations during the second quarter of 2012 , the board of directors authorized the sale of our homecare business , which had previously been reported as part of the merchant gases operating segment .
this business has been accounted for as a discontinued operation .
in the third quarter of 2012 , we sold the majority of our homecare business to the linde group for sale proceeds of 20ac590 million ( $ 777 ) and recognized a gain of $ 207.4 ( $ 150.3 after-tax , or $ .70 per share ) .
the sale proceeds included 20ac110 million ( $ 144 ) that was contingent on the outcome of certain retender arrangements .
these proceeds were reflected in payables and accrued liabilities on our consolidated balance sheet as of 30 september 2013 .
based on the outcome of the retenders , we were contractually required to return proceeds to the linde group .
in the fourth quarter of 2014 , we made a payment to settle this liability and recognized a gain of $ 1.5 .
during the third quarter of 2012 , an impairment charge of $ 33.5 ( $ 29.5 after-tax , or $ .14 per share ) was recorded to write down the remaining business , which was primarily in the united kingdom and ireland , to its estimated net realizable value .
in the fourth quarter of 2013 , an additional charge of $ 18.7 ( $ 13.6 after-tax , or $ .06 per share ) was recorded to update our estimate of the net realizable value .
in the first quarter of 2014 , we sold the remaining portion of the homecare business for a36.1 million ( $ 9.8 ) and recorded a gain on sale of $ 2.4 .
we entered into an operations guarantee related to the obligations under certain homecare contracts assigned in connection with the transaction .
refer to note 16 , commitments and contingencies , for additional information .
the results of discontinued operations are summarized below: .

 | 2014 | 2013 | 2012
sales | $ 8.5 | $ 52.3 | $ 258.0
income before taxes | $ .7 | $ 3.8 | $ 68.1
income tax provision | 2014 | .2 | 20.8
income from operations of discontinued operations | .7 | 3.6 | 47.3
gain ( loss ) on sale of business and impairment/write-down net of tax | 3.9 | -13.6 ( 13.6 ) | 120.8
income ( loss ) from discontinued operations net of tax | $ 4.6 | $ -10.0 ( 10.0 ) | $ 168.1

the assets and liabilities classified as discontinued operations for the homecare business at 30 september 2013 consisted of $ 2.5 in trade receivables , net , and $ 2.4 in payables and accrued liabilities .
as of 30 september 2014 , no assets or liabilities were classified as discontinued operations. .
```

---

## Item 12/25 — `hqa_CFQ_57d9a4fe`

- **source**: convfinqa / Single_ABMD/2011/page_33.pdf-4#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what is the net change in value of abiomed inc from 2006 to 2009?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(37.98, 100), divide(#0, 100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the following graph compares the yearly change in the cumulative total stockholder return for our last five full fiscal years , based upon the market price of our common stock , with the cumulative total return on a nasdaq composite index ( u.s .
companies ) and a peer group , the nasdaq medical equipment-sic code 3840-3849 index , which is comprised of medical equipment companies , for that period .
the performance graph assumes the investment of $ 100 on march 31 , 2006 in our common stock , the nasdaq composite index ( u.s .
companies ) and the peer group index , and the reinvestment of any and all dividends. .

 | 3/31/2006 | 3/31/2007 | 3/31/2008 | 3/31/2009 | 3/31/2010 | 3/31/2011
abiomed inc | 100 | 105.89 | 101.86 | 37.98 | 80.00 | 112.64
nasdaq composite index | 100 | 103.50 | 97.41 | 65.33 | 102.49 | 118.86
nasdaq medical equipment sic code 3840-3849 | 100 | 88.78 | 84.26 | 46.12 | 83.47 | 91.35

this graph is not 201csoliciting material 201d under regulation 14a or 14c of the rules promulgated under the securities exchange act of 1934 , is not deemed filed with the securities and exchange commission and is not to be incorporated by reference in any of our filings under the securities act of 1933 , as amended , or the exchange act whether made before or after the date hereof and irrespective of any general incorporation language in any such filing .
transfer agent american stock transfer & trust company , 59 maiden lane , new york , ny 10038 , is our stock transfer agent. .
```

---

## Item 13/25 — `hqa_CFQ_5c6f8a33`

- **source**: convfinqa / Double_ETFC/2007/page_22.pdf#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the price of e*trade financial corporation between 12/02 and 12/07?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(73.05, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
december 18 , 2007 , we issued an additional 23182197 shares of common stock to citadel .
the issuances were exempt from registration pursuant to section 4 ( 2 ) of the securities act of 1933 , and each purchaser has represented to us that it is an 201caccredited investor 201d as defined in regulation d promulgated under the securities act of 1933 , and that the common stock was being acquired for investment .
we did not engage in a general solicitation or advertising with regard to the issuances of the common stock and have not offered securities to the public in connection with the issuances .
see item 1 .
business 2014citadel investment .
performance graph the following performance graph shows the cumulative total return to a holder of the company 2019s common stock , assuming dividend reinvestment , compared with the cumulative total return , assuming dividend reinvestment , of the standard & poor 2019s ( 201cs&p 201d ) 500 and the s&p super cap diversified financials during the period from december 31 , 2002 through december 31 , 2007. .

 | 12/02 | 12/03 | 12/04 | 12/05 | 12/06 | 12/07
e*trade financial corporation | 100.00 | 260.29 | 307.61 | 429.22 | 461.32 | 73.05
s&p 500 | 100.00 | 128.68 | 142.69 | 149.70 | 173.34 | 182.87
s&p super cap diversified financials | 100.00 | 139.29 | 156.28 | 170.89 | 211.13 | 176.62

2022 $ 100 invested on 12/31/02 in stock or index-including reinvestment of dividends .
fiscal year ending december 31 .
2022 copyright a9 2008 , standard & poor 2019s , a division of the mcgraw-hill companies , inc .
all rights reserved .
www.researchdatagroup.com/s&p.htm .
```

---

## Item 14/25 — `hqa_CFQ_61e3612e`

- **source**: convfinqa / Single_AWK/2018/page_150.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the change in value of intrinsic value from 2016 to 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(9, 18)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the following table provides the weighted average assumptions used in the black-scholes option-pricing model for grants and the resulting weighted average grant date fair value per share of stock options granted for the years ended december 31: .

 | 2018 | 2017 | 2016
intrinsic value | $ 9 | $ 10 | $ 18
exercise proceeds | 7 | 11 | 15
income tax benefit realized | 2 | 3 | 6

stock units during 2018 , 2017 and 2016 , the company granted rsus to certain employees under the 2007 plan and 2017 omnibus plan , as applicable .
rsus generally vest based on continued employment with the company over periods ranging from one to three years. .
```

---

## Item 15/25 — `hqa_CFQ_62332dc6`

- **source**: convfinqa / Single_C/2009/page_279.pdf-3#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the net change in citigroup from 2007 to 2008?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(18.71, 70.36), divide(#0, 70.36)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
comparison of five-year cumulative total return the following graph compares the cumulative total return on citigroup 2019s common stock with the s&p 500 index and the s&p financial index over the five-year period extending through december 31 , 2009 .
the graph assumes that $ 100 was invested on december 31 , 2004 in citigroup 2019s common stock , the s&p 500 index and the s&p financial index and that all dividends were reinvested .
citigroup s&p 500 index s&p financial index 2005 2006 2007 2008 2009 comparison of five-year cumulative total return for the years ended .

december 31 | citigroup | s&p 500 index | s&p financial index
2005 | 104.38 | 104.83 | 106.30
2006 | 124.02 | 121.20 | 126.41
2007 | 70.36 | 127.85 | 103.47
2008 | 18.71 | 81.12 | 47.36
2009 | 9.26 | 102.15 | 55.27

.
```

---

## Item 16/25 — `hqa_CFQ_642330e7`

- **source**: convfinqa / Single_CDNS/2007/page_30.pdf-3#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the net change in value of cadence design from 2002 to 2007?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(139.82, const_100), divide(#0, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the graph below matches cadence design systems , inc . 2019s cumulative 5-year total shareholder return on common stock with the cumulative total returns of the s&p 500 index , the s&p information technology index , and the nasdaq composite index .
the graph assumes that the value of the investment in our common stock , and in each index ( including reinvestment of dividends ) was $ 100 on december 28 , 2002 and tracks it through december 29 , 2007 .
comparison of 5 year cumulative total return* among cadence design systems , inc. , the s&p 500 index , the nasdaq composite index and the s&p information technology index 12/29/0712/30/0612/31/051/1/051/3/0412/28/02 cadence design systems , inc .
nasdaq composite s & p information technology s & p 500 * $ 100 invested on 12/28/02 in stock or on 12/31/02 in index-including reinvestment of dividends .
indexes calculated on month-end basis .
copyright b7 2007 , standard & poor 2019s , a division of the mcgraw-hill companies , inc .
all rights reserved .
www.researchdatagroup.com/s&p.htm .

 | 12/28/02 | 1/3/04 | 1/1/05 | 12/31/05 | 12/30/06 | 12/29/07
cadence design systems inc . | 100.00 | 149.92 | 113.38 | 138.92 | 147.04 | 139.82
s & p 500 | 100.00 | 128.68 | 142.69 | 149.70 | 173.34 | 182.87
nasdaq composite | 100.00 | 149.75 | 164.64 | 168.60 | 187.83 | 205.22
s & p information technology | 100.00 | 147.23 | 150.99 | 152.49 | 165.32 | 192.28

the stock price performance included in this graph is not necessarily indicative of future stock price performance .
```

---

## Item 17/25 — `hqa_CFQ_654d0297`

- **source**: convfinqa / Single_TFX/2018/page_47.pdf-4#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the change in price of teleflex incorporated from 2014 to 2015?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(143, 124), divide(#0, 124)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
part a0ii item a05 .
market for registrant 2019s common equity , related stockholder matters and issuer purchases of equity securities our common stock is listed on the new york stock exchange under the symbol 201ctfx . 201d as of february 19 , 2019 , we had 473 holders of record of our common stock .
a substantially greater number of holders of our common stock are beneficial owners whose shares are held by brokers and other financial institutions for the accounts of beneficial owners .
stock performance graph the following graph provides a comparison of five year cumulative total stockholder returns of teleflex common stock , the standard a0& poor 2019s ( s&p ) 500 stock index and the s&p 500 healthcare equipment & supply index .
the annual changes for the five-year period shown on the graph are based on the assumption that $ 100 had been invested in teleflex common stock and each index on december a031 , 2013 and that all dividends were reinvested .
market performance .

company / index | 2013 | 2014 | 2015 | 2016 | 2017 | 2018
teleflex incorporated | 100 | 124 | 143 | 177 | 275 | 288
s&p 500 index | 100 | 114 | 115 | 129 | 157 | 150
s&p 500 healthcare equipment & supply index | 100 | 126 | 134 | 142 | 186 | 213

s&p 500 healthcare equipment & supply index 100 126 134 142 186 213 .
```

---

## Item 18/25 — `hqa_CFQ_72ebe479`

- **source**: convfinqa / Double_EW/2016/page_36.pdf#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what is the value of an investment in edwards lifesciences in 2016?

Question: what is the net change from the initial investment?

**Original source question**: what is the net change from the initial investment?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(265.06, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
2mar201707015999 ( c ) in october 2016 , our accelerated share repurchase ( 2018 2018asr 2019 2019 ) agreement concluded and we received an additional 44 thousand shares of our common stock .
shares purchased pursuant to the asr agreement are presented in the table above in the periods in which they were received .
performance graph the following graph compares the performance of our common stock with that of the s&p 500 index and the s&p 500 healthcare equipment index .
the cumulative total return listed below assumes an initial investment of $ 100 at the market close on december 30 , 2011 and reinvestment of dividends .
comparison of 5 year cumulative total return 2011 2012 2016201520142013 edwards lifesciences corporation s&p 500 s&p 500 healthcare equipment index december 31 .

total cumulative return | 2012 | 2013 | 2014 | 2015 | 2016
edwards lifesciences | $ 127.54 | $ 93.01 | $ 180.17 | $ 223.42 | $ 265.06
s&p 500 | 116.00 | 153.58 | 174.60 | 177.01 | 198.18
s&p 500 healthcare equipment index | 117.42 | 150.28 | 181.96 | 194.37 | 207.46

.
```

---

## Item 19/25 — `hqa_CFQ_76164f50`

- **source**: convfinqa / Single_INTC/2018/page_48.pdf-2#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the change in net cash provided by operating activities between 2016 and 2017?

Question: what percentage change does this represent from 2016?

**Original source question**: what percentage change does this represent from 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(22110, 21808), divide(#0, 21808)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
sources and uses of cash ( in millions ) in summary , our cash flows for each period were as follows : years ended ( in millions ) dec 29 , dec 30 , dec 31 .

years ended ( in millions ) | dec 292018 | dec 302017 | dec 312016
net cash provided by operating activities | $ 29432 | $ 22110 | $ 21808
net cash used for investing activities | -11239 ( 11239 ) | -15762 ( 15762 ) | -25817 ( 25817 )
net cash provided by ( used for ) financing activities | -18607 ( 18607 ) | -8475 ( 8475 ) | -5739 ( 5739 )
net increase ( decrease ) in cash and cash equivalents | $ -414 ( 414 ) | $ -2127 ( 2127 ) | $ -9748 ( 9748 )

md&a consolidated results and analysis 40 .
```

---

## Item 20/25 — `hqa_CFQ_847e456a`

- **source**: convfinqa / Double_DISCA/2018/page_39.pdf#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the net change in value of an investment in disca from 2013 to 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(53.56, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph the following graph sets forth the cumulative total shareholder return on our series a common stock , series b common stock and series c common stock as compared with the cumulative total return of the companies listed in the standard and poor 2019s 500 stock index ( 201cs&p 500 index 201d ) and a peer group of companies comprised of cbs corporation class b common stock , scripps network interactive , inc .
( acquired by the company in march 2018 ) , time warner , inc .
( acquired by at&t inc .
in june 2018 ) , twenty-first century fox , inc .
class a common stock ( news corporation class a common stock prior to june 2013 ) , viacom , inc .
class b common stock and the walt disney company .
the graph assumes $ 100 originally invested on december 31 , 2013 in each of our series a common stock , series b common stock and series c common stock , the s&p 500 index , and the stock of our peer group companies , including reinvestment of dividends , for the years ended december 31 , 2014 , 2015 , 2016 , 2017 and 2018 .
two peer companies , scripps networks interactive , inc .
and time warner , inc. , were acquired in 2018 .
the stock performance chart shows the peer group including scripps networks interactive , inc .
and time warner , inc .
and excluding both acquired companies for the entire five year period .
december 31 , december 31 , december 31 , december 31 , december 31 , december 31 .

 | december 312013 | december 312014 | december 312015 | december 312016 | december 312017 | december 312018
disca | $ 100.00 | $ 74.58 | $ 57.76 | $ 59.34 | $ 48.45 | $ 53.56
discb | $ 100.00 | $ 80.56 | $ 58.82 | $ 63.44 | $ 53.97 | $ 72.90
disck | $ 100.00 | $ 80.42 | $ 60.15 | $ 63.87 | $ 50.49 | $ 55.04
s&p 500 | $ 100.00 | $ 111.39 | $ 110.58 | $ 121.13 | $ 144.65 | $ 135.63
peer group incl . acquired companies | $ 100.00 | $ 116.64 | $ 114.02 | $ 127.96 | $ 132.23 | $ 105.80
peer group ex . acquired companies | $ 100.00 | $ 113.23 | $ 117.27 | $ 120.58 | $ 127.90 | $ 141.58

equity compensation plan information information regarding securities authorized for issuance under equity compensation plans will be set forth in our definitive proxy statement for our 2019 annual meeting of stockholders under the caption 201csecurities authorized for issuance under equity compensation plans , 201d which is incorporated herein by reference. .
```

---

## Item 21/25 — `hqa_CFQ_84869786`

- **source**: convfinqa / Double_AON/2007/page_185.pdf#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the future minimum rental payments from 2008 to 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(275, 317)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
notes to consolidated financial statements at december 31 , 2007 , future minimum rental payments required under operating leases for continuing operations that have initial or remaining noncancelable lease terms in excess of one year , net of sublease rental income , most of which pertain to real estate leases , are as follows : ( millions ) .

2008 | $ 317
2009 | 275
2010 | 236
2011 | 214
2012 | 191
later years | 597
total minimum payments required | $ 1830

aon corporation .
```

---

## Item 22/25 — `hqa_CFQ_870de807`

- **source**: convfinqa / Single_JPM/2015/page_77.pdf-5#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the change in value of the s&p from 2010 to 2015?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(180.67, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
jpmorgan chase & co./2015 annual report 67 five-year stock performance the following table and graph compare the five-year cumulative total return for jpmorgan chase & co .
( 201cjpmorgan chase 201d or the 201cfirm 201d ) common stock with the cumulative return of the s&p 500 index , the kbw bank index and the s&p financial index .
the s&p 500 index is a commonly referenced united states of america ( 201cu.s . 201d ) equity benchmark consisting of leading companies from different economic sectors .
the kbw bank index seeks to reflect the performance of banks and thrifts that are publicly traded in the u.s .
and is composed of 24 leading national money center and regional banks and thrifts .
the s&p financial index is an index of 87 financial companies , all of which are components of the s&p 500 .
the firm is a component of all three industry indices .
the following table and graph assume simultaneous investments of $ 100 on december 31 , 2010 , in jpmorgan chase common stock and in each of the above indices .
the comparison assumes that all dividends are reinvested .
december 31 , ( in dollars ) 2010 2011 2012 2013 2014 2015 .

december 31 ( in dollars ) | 2010 | 2011 | 2012 | 2013 | 2014 | 2015
jpmorgan chase | $ 100.00 | $ 80.03 | $ 108.98 | $ 148.98 | $ 163.71 | $ 177.40
kbw bank index | 100.00 | 76.82 | 102.19 | 140.77 | 153.96 | 154.71
s&p financial index | 100.00 | 82.94 | 106.78 | 144.79 | 166.76 | 164.15
s&p 500 index | 100.00 | 102.11 | 118.44 | 156.78 | 178.22 | 180.67

december 31 , ( in dollars ) .
```

---

## Item 23/25 — `hqa_CFQ_8a8b8535`

- **source**: convfinqa / Single_MO/2017/page_65.pdf-4#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the net change in earnings attributable to altria group from 2016 to 2017?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(10222, 14239)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
10-k altria ar release tuesday , february 27 , 2018 10:00pm andra design llc performance stock units : in january 2017 , altria group , inc .
granted an aggregate of 187886 performance stock units to eligible employees .
the payout of the performance stock units requires the achievement of certain performance measures , which were predetermined at the time of grant , over a three-year performance cycle .
these performance measures consist of altria group , inc . 2019s adjusted diluted earnings per share ( 201ceps 201d ) compounded annual growth rate and altria group , inc . 2019s total shareholder return relative to a predetermined peer group .
the performance stock units are also subject to forfeiture if certain employment conditions are not met .
at december 31 , 2017 , altria group , inc .
had 170755 performance stock units remaining , with a weighted-average grant date fair value of $ 70.39 per performance stock unit .
the fair value of the performance stock units at the date of grant , net of estimated forfeitures , is amortized to expense over the performance period .
altria group , inc .
recorded pre-tax compensation expense related to performance stock units for the year ended december 31 , 2017 of $ 6 million .
the unamortized compensation expense related to altria group , inc . 2019s performance stock units was $ 7 million at december 31 , 2017 .
altria group , inc .
did not grant any performance stock units during 2016 and 2015 .
note 12 .
earnings per share basic and diluted eps were calculated using the following: .

( in millions ) | for the years ended december 31 , 2017 | for the years ended december 31 , 2016 | for the years ended december 31 , 2015
net earnings attributable to altria group inc . | $ 10222 | $ 14239 | $ 5241
less : distributed and undistributed earnings attributable to share-based awards | -14 ( 14 ) | -24 ( 24 ) | -10 ( 10 )
earnings for basic and diluted eps | $ 10208 | $ 14215 | $ 5231
weighted-average shares for basic and diluted eps | 1921 | 1952 | 1961

net earnings attributable to altria group , inc .
$ 10222 $ 14239 $ 5241 less : distributed and undistributed earnings attributable to share-based awards ( 14 ) ( 24 ) ( 10 ) earnings for basic and diluted eps $ 10208 $ 14215 $ 5231 weighted-average shares for basic and diluted eps 1921 1952 1961 .
```

---

## Item 24/25 — `hqa_CFQ_8bd6d28a`

- **source**: convfinqa / Single_ABMD/2015/page_53.pdf-4#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the net change in price of the nasdaq composite index from 2010 to 2013?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(136.26, 100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the following graph compares the yearly change in the cumulative total stockholder return for our last five full fiscal years , based upon the market price of our common stock , with the cumulative total return on a nasdaq composite index ( u.s .
companies ) and a peer group , the nasdaq medical equipment-sic code 3840-3849 index , which is comprised of medical equipment companies , for that period .
the performance graph assumes the investment of $ 100 on march 31 , 2010 in our common stock , the nasdaq composite index ( u.s .
companies ) and the peer group index , and the reinvestment of any and all dividends. .

 | 3/31/2010 | 3/31/2011 | 3/31/2012 | 3/31/2013 | 3/31/2014 | 3/31/2015
abiomed inc | 100 | 140.79 | 215.02 | 180.91 | 252.33 | 693.60
nasdaq composite index | 100 | 115.98 | 128.93 | 136.26 | 175.11 | 204.38
nasdaq medical equipment sic code 3840-3849 | 100 | 108.31 | 115.05 | 105.56 | 123.18 | 118.95

this graph is not 201csoliciting material 201d under regulation 14a or 14c of the rules promulgated under the securities exchange act of 1934 , is not deemed filed with the securities and exchange commission and is not to be incorporated by reference in any of our filings under the securities act of 1933 , as amended , or the exchange act whether made before or after the date hereof and irrespective of any general incorporation language in any such filing .
transfer agent american stock transfer & trust company , 59 maiden lane , new york , ny 10038 , is our stock transfer agent. .
```

---

## Item 25/25 — `hqa_CFQ_8f75ba7a`

- **source**: convfinqa / Double_ADBE/2014/page_47.pdf#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the change in percentage points of data center cost between the years of 2014-13 and 2013-12?

Question: for the same years, what was the change in percentage points of depreciation expense?

**Original source question**: for the same years, what was the change in percentage points of depreciation expense?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(3, 3)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
subscription cost of subscription revenue consists of third-party royalties and expenses related to operating our network infrastructure , including depreciation expenses and operating lease payments associated with computer equipment , data center costs , salaries and related expenses of network operations , implementation , account management and technical support personnel , amortization of intangible assets and allocated overhead .
we enter into contracts with third-parties for the use of their data center facilities and our data center costs largely consist of the amounts we pay to these third parties for rack space , power and similar items .
cost of subscription revenue increased due to the following : % ( % ) change 2014-2013 % ( % ) change 2013-2012 .

 | % (  % ) change2014-2013 | % (  % ) change2013-2012
data center cost | 10% ( 10 % ) | 11% ( 11 % )
compensation cost and related benefits associated with headcount | 4 | 5
depreciation expense | 3 | 3
royalty cost | 3 | 4
amortization of purchased intangibles | 2014 | 4
various individually insignificant items | 1 | 2014
total change | 21% ( 21 % ) | 27% ( 27 % )

cost of subscription revenue increased during fiscal 2014 as compared to fiscal 2013 primarily due to data center costs , compensation cost and related benefits , deprecation expense , and royalty cost .
data center costs increased as compared with the year-ago period primarily due to higher transaction volumes in our adobe marketing cloud and creative cloud services .
compensation cost and related benefits increased as compared to the year-ago period primarily due to additional headcount in fiscal 2014 , including from our acquisition of neolane in the third quarter of fiscal 2013 .
depreciation expense increased as compared to the year-ago period primarily due to higher capital expenditures in recent periods as we continue to invest in our network and data center infrastructure to support the growth of our business .
royalty cost increased primarily due to increases in subscriptions and downloads of our saas offerings .
cost of subscription revenue increased during fiscal 2013 as compared to fiscal 2012 primarily due to increased hosted server costs and amortization of purchased intangibles .
hosted server costs increased primarily due to increases in data center costs related to higher transaction volumes in our adobe marketing cloud and creative cloud services , depreciation expense from higher capital expenditures in prior years and compensation and related benefits driven by additional headcount .
amortization of purchased intangibles increased primarily due to increased amortization of intangible assets purchased associated with our acquisitions of behance and neolane in fiscal 2013 .
services and support cost of services and support revenue is primarily comprised of employee-related costs and associated costs incurred to provide consulting services , training and product support .
cost of services and support revenue increased during fiscal 2014 as compared to fiscal 2013 primarily due to increases in compensation and related benefits driven by additional headcount and third-party fees related to training and consulting services provided to our customers .
cost of services and support revenue increased during fiscal 2013 as compared to fiscal 2012 primarily due to increases in third-party fees related to training and consulting services provided to our customers and compensation and related benefits driven by additional headcount , including headcount from our acquisition of neolane in fiscal 2013. .
```

---
