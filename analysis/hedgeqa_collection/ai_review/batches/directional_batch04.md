# Blind review batch `directional_batch04`

25 items. Family: `numeric_to_directional`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FQ_cccdd70f`

- **source**: finqa / STT/2012/page_42.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the percent change in state street corporation's cumulative total shareholder return on common stock between 2008 and 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(55, 49), divide(#0, 49)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
shareholder return performance presentation the graph presented below compares the cumulative total shareholder return on state street's common stock to the cumulative total return of the s&p 500 index and the s&p financial index over a five-year period .
the cumulative total shareholder return assumes the investment of $ 100 in state street common stock and in each index on december 31 , 2007 at the closing price on the last trading day of 2007 , and also assumes reinvestment of common stock dividends .
the s&p financial index is a publicly available measure of 80 of the standard & poor's 500 companies , representing 26 diversified financial services companies , 22 insurance companies , 17 real estate companies and 15 banking companies .
comparison of five-year cumulative total shareholder return .

 | 2007 | 2008 | 2009 | 2010 | 2011 | 2012
state street corporation | $ 100 | $ 49 | $ 55 | $ 58 | $ 52 | $ 61
s&p 500 index | 100 | 63 | 80 | 92 | 94 | 109
s&p financial index | 100 | 45 | 52 | 59 | 49 | 63

.
```

---

## Item 2/25 — `hqa_FQ_cdc17c89`

- **source**: finqa / AAL/2016/page_37.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the net change in airliner count during 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(55, 71)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
table of contents item 2 .
properties flight equipment and fleet renewal as of december 31 , 2016 , american operated a mainline fleet of 930 aircraft .
in 2016 , we continued our extensive fleet renewal program , which has provided us with the youngest fleet of the major u.s .
network carriers .
during 2016 , american took delivery of 55 new mainline aircraft and retired 71 aircraft .
we are supported by our wholly-owned and third-party regional carriers that fly under capacity purchase agreements operating as american eagle .
as of december 31 , 2016 , american eagle operated 606 regional aircraft .
during 2016 , we increased our regional fleet by 61 regional aircraft , we removed and placed in temporary storage one embraer erj 140 aircraft and retired 41 other regional aircraft .
mainline as of december 31 , 2016 , american 2019s mainline fleet consisted of the following aircraft : average seating capacity average ( years ) owned leased total .

 | average seating capacity | average age ( years ) | owned | leased | total
airbus a319 | 128 | 12.8 | 19 | 106 | 125
airbus a320 | 150 | 15.5 | 10 | 41 | 51
airbus a321 | 178 | 4.9 | 153 | 46 | 199
airbusa330-200 | 258 | 5.0 | 15 | 2014 | 15
airbusa330-300 | 291 | 16.4 | 4 | 5 | 9
boeing737-800 | 160 | 7.7 | 123 | 161 | 284
boeing757-200 | 179 | 17.9 | 39 | 12 | 51
boeing767-300er | 211 | 19.5 | 28 | 3 | 31
boeing777-200er | 263 | 16.0 | 44 | 3 | 47
boeing777-300er | 310 | 2.8 | 18 | 2 | 20
boeing787-8 | 226 | 1.3 | 17 | 2014 | 17
boeing787-9 | 285 | 0.2 | 4 | 2014 | 4
embraer 190 | 99 | 9.2 | 20 | 2014 | 20
mcdonnell douglasmd-80 | 140 | 22.0 | 25 | 32 | 57
total |  | 10.3 | 519 | 411 | 930

.
```

---

## Item 3/25 — `hqa_FQ_d04445bc`

- **source**: finqa / VNO/2010/page_173.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the percentage change in the redeemable non controlling interests balance at december 31 2009 from 2008

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(1251628, 1177978), divide(#0, 1177978)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
vornado realty trust notes to consolidated financial statements ( continued ) 10 .
redeemable noncontrolling interests - continued redeemable noncontrolling interests on our consolidated balance sheets are recorded at the greater of their carrying amount or redemption value at the end of each reporting period .
changes in the value from period to period are charged to 201cadditional capital 201d in our consolidated statements of changes in equity .
below is a table summarizing the activity of redeemable noncontrolling interests .
( amounts in thousands ) .

balance at december 31 2008 | $ 1177978
net income | 25120
distributions | -42451 ( 42451 )
conversion of class a units into common shares at redemption value | -90955 ( 90955 )
adjustment to carry redeemable class a units at redemption value | 167049
other net | 14887
balance at december 31 2009 | $ 1251628
net income | 55228
distributions | -53515 ( 53515 )
conversion of class a units into common shares at redemption value | -126764 ( 126764 )
adjustment to carry redeemable class a units at redemption value | 191826
redemption of series d-12 redeemable units | -13000 ( 13000 )
other net | 22571
balance at december 31 2010 | $ 1327974

as of december 31 , 2010 and 2009 , the aggregate redemption value of redeemable class a units was $ 1066974000 and $ 971628000 , respectively .
redeemable noncontrolling interests exclude our series g convertible preferred units and series d-13 cumulative redeemable preferred units , as they are accounted for as liabilities in accordance with asc 480 , distinguishing liabilities and equity , because of their possible settlement by issuing a variable number of vornado common shares .
accordingly the fair value of these units is included as a component of 201cother liabilities 201d on our consolidated balance sheets and aggregated $ 55097000 and $ 60271000 as of december 31 , 2010 and 2009 , respectively. .
```

---

## Item 4/25 — `hqa_FQ_d32f7aa4`

- **source**: finqa / JPM/2010/page_236.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the percentage change in the accretable yield activity for the firm 2019s pci consumer loans in 2010

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(19097, 25544), divide(#0, 25544)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
notes to consolidated financial statements 236 jpmorgan chase & co./2010 annual report the table below sets forth the accretable yield activity for the firm 2019s pci consumer loans for the years ended december 31 , 2010 , 2009 and .

year ended december 31 , ( in millions except ratios ) | year ended december 31 , 2010 | year ended december 31 , 2009 | 2008
balance january 1 | $ 25544 | $ 32619 | $ 2014
washington mutual acquisition | 2014 | 2014 | 39454
accretion into interest income | -3232 ( 3232 ) | -4363 ( 4363 ) | -1292 ( 1292 )
changes in interest rates on variable rate loans | -819 ( 819 ) | -4849 ( 4849 ) | -5543 ( 5543 )
other changes in expected cash flows ( a ) | -2396 ( 2396 ) | 2137 | 2014
balance december 31 | $ 19097 | $ 25544 | $ 32619
accretable yield percentage | 4.35% ( 4.35 % ) | 5.14% ( 5.14 % ) | 5.81% ( 5.81 % )

( a ) other changes in expected cash flows may vary from period to period as the firm continues to refine its cash flow model and periodically updates model assumptions .
for the years ended december 31 , 2010 and 2009 , other changes in expected cash flows were principally driven by changes in prepayment assumptions , as well as reclassification to the nonaccretable difference .
such changes are expected to have an insignificant impact on the accretable yield percentage .
the factors that most significantly affect estimates of gross cash flows expected to be collected , and accordingly the accretable yield balance , include : ( i ) changes in the benchmark interest rate indices for variable rate products such as option arm and home equity loans ; and ( ii ) changes in prepayment assump- tions .
to date , the decrease in the accretable yield percentage has been primarily related to a decrease in interest rates on vari- able-rate loans and , to a lesser extent , extended loan liquida- tion periods .
certain events , such as extended loan liquidation periods , affect the timing of expected cash flows but not the amount of cash expected to be received ( i.e. , the accretable yield balance ) .
extended loan liquidation periods reduce the accretable yield percentage because the same accretable yield balance is recognized against a higher-than-expected loan balance over a longer-than-expected period of time. .
```

---

## Item 5/25 — `hqa_FQ_d99d6e5a`

- **source**: finqa / RE/2010/page_138.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the percent change of the beginning and ending amount of unrecognized tax benefits in 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(29010, 34366), divide(#0, 34366)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
a reconciliation of the beginning and ending amount of unrecognized tax benefits , for the periods indicated , is as follows: .

( dollars in thousands ) | 2010 | 2009 | 2008
balance at january 1 | $ 29010 | $ 34366 | $ 29132
additions based on tax positions related to the current year | 7119 | 6997 | 5234
additions for tax positions of prior years | - | - | -
reductions for tax positions of prior years | - | - | -
settlements with taxing authorities | -12356 ( 12356 ) | -12353 ( 12353 ) | -
lapses of applicable statutes of limitations | - | - | -
balance at december 31 | $ 23773 | $ 29010 | $ 34366

the entire amount of the unrecognized tax benefits would affect the effective tax rate if recognized .
in 2010 , the company favorably settled a 2003 and 2004 irs audit .
the company recorded a net overall tax benefit including accrued interest of $ 25920 thousand .
in addition , the company was also able to take down a $ 12356 thousand fin 48 reserve that had been established regarding the 2003 and 2004 irs audit .
the company is no longer subject to u.s .
federal , state and local or foreign income tax examinations by tax authorities for years before 2007 .
the company recognizes accrued interest related to net unrecognized tax benefits and penalties in income taxes .
during the years ended december 31 , 2010 , 2009 and 2008 , the company accrued and recognized a net expense ( benefit ) of approximately $ ( 9938 ) thousand , $ 1563 thousand and $ 2446 thousand , respectively , in interest and penalties .
included within the 2010 net expense ( benefit ) of $ ( 9938 ) thousand is $ ( 10591 ) thousand of accrued interest related to the 2003 and 2004 irs audit .
the company is not aware of any positions for which it is reasonably possible that the total amounts of unrecognized tax benefits will significantly increase or decrease within twelve months of the reporting date .
for u.s .
income tax purposes the company has foreign tax credit carryforwards of $ 55026 thousand that begin to expire in 2014 .
in addition , for u.s .
income tax purposes the company has $ 41693 thousand of alternative minimum tax credits that do not expire .
management believes that it is more likely than not that the company will realize the benefits of its net deferred tax assets and , accordingly , no valuation allowance has been recorded for the periods presented .
tax benefits of $ 629 thousand and $ 1714 thousand related to share-based compensation deductions for stock options exercised in 2010 and 2009 , respectively , are included within additional paid-in capital of the shareholders 2019 equity section of the consolidated balance sheets. .
```

---

## Item 6/25 — `hqa_FQ_dc32fb1c`

- **source**: finqa / ORLY/2018/page_30.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the five year change in value of the o 2019reilly automotive inc . stock?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(268, const_100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph : the graph below shows the cumulative total shareholder return assuming the investment of $ 100 , on december 31 , 2013 , and the reinvestment of dividends thereafter , if any , in the company 2019s common stock versus the standard and poor 2019s s&p 500 retail index ( 201cs&p 500 retail index 201d ) and the standard and poor 2019s s&p 500 index ( 201cs&p 500 201d ) . .

company/index | december 31 , 2013 | december 31 , 2014 | december 31 , 2015 | december 31 , 2016 | december 31 , 2017 | december 31 , 2018
o 2019reilly automotive inc . | $ 100 | $ 150 | $ 197 | $ 216 | $ 187 | $ 268
s&p 500 retail index | 100 | 110 | 137 | 143 | 184 | 208
s&p 500 | $ 100 | $ 111 | $ 111 | $ 121 | $ 145 | $ 136

.
```

---

## Item 7/25 — `hqa_FQ_e6e1f02f`

- **source**: finqa / DG/2008/page_73.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the percentage change in held-to-maturity securities at cost and at fair value as of january 30 , 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(28.9, 31.4), divide(#0, 31.4)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the contractual maturities of held-to-maturity securities as of january 30 , 2009 were in excess of three years and were $ 31.4 million at cost and $ 28.9 million at fair value , respectively .
for the successor year ended january 30 , 2009 and period ended february 1 , 2008 , and the predecessor period ended july 6 , 2007 and year ended february 2 , 2007 , gross realized gains and losses on the sales of available-for-sale securities were not material .
the cost of securities sold is based upon the specific identification method .
merchandise inventories inventories are stated at the lower of cost or market with cost determined using the retail last-in , first-out ( 201clifo 201d ) method .
under the company 2019s retail inventory method ( 201crim 201d ) , the calculation of gross profit and the resulting valuation of inventories at cost are computed by applying a calculated cost-to-retail inventory ratio to the retail value of sales at a department level .
costs directly associated with warehousing and distribution are capitalized into inventory .
the excess of current cost over lifo cost was approximately $ 50.0 million at january 30 , 2009 and $ 6.1 million at february 1 , 2008 .
current cost is determined using the retail first-in , first-out method .
the company 2019s lifo reserves were adjusted to zero at july 6 , 2007 as a result of the merger .
the successor recorded lifo provisions of $ 43.9 million and $ 6.1 million during 2008 and 2007 , respectively .
the predecessor recorded a lifo credit of $ 1.5 million in 2006 .
in 2008 , the increased commodity cost pressures mainly related to food and pet products which have been driven by fruit and vegetable prices and rising freight costs .
increases in petroleum , resin , metals , pulp and other raw material commodity driven costs also resulted in multiple product cost increases .
the company intends to address these commodity cost increases through negotiations with its vendors and by increasing retail prices as necessary .
on a quarterly basis , the company estimates the annual impact of commodity cost fluctuations based upon the best available information at that point in time .
store pre-opening costs pre-opening costs related to new store openings and the construction periods are expensed as incurred .
property and equipment property and equipment are recorded at cost .
the company provides for depreciation and amortization on a straight-line basis over the following estimated useful lives: .

land improvements | 20
buildings | 39-40
furniture fixtures and equipment | 3-10

improvements of leased properties are amortized over the shorter of the life of the applicable lease term or the estimated useful life of the asset. .
```

---

## Item 8/25 — `hqa_FQ_e7c2edef`

- **source**: finqa / HST/2018/page_160.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the net change in millions in the accumulated depreciation and amortization of real estate assets from 2015 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(5949, 5666)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
schedule iii page 6 of 6 host hotels & resorts , inc. , and subsidiaries host hotels & resorts , l.p. , and subsidiaries real estate and accumulated depreciation december 31 , 2018 ( in millions ) ( b ) the change in accumulated depreciation and amortization of real estate assets for the fiscal years ended december 31 , 2018 , 2017 and 2016 is as follows: .

balance at december 31 2015 | $ 5666
depreciation and amortization | 572
dispositions and other | -159 ( 159 )
depreciation on assets held for sale | -130 ( 130 )
balance at december 31 2016 | 5949
depreciation and amortization | 563
dispositions and other | -247 ( 247 )
depreciation on assets held for sale | 7
balance at december 31 2017 | 6272
depreciation and amortization | 546
dispositions and other | -344 ( 344 )
depreciation on assets held for sale | -101 ( 101 )
balance at december 31 2018 | $ 6373

( c ) the aggregate cost of real estate for federal income tax purposes is approximately $ 10458 million at december 31 , 2018 .
( d ) the total cost of properties excludes construction-in-progress properties. .
```

---

## Item 9/25 — `hqa_FQ_e98c5e1e`

- **source**: finqa / ETR/2011/page_358.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the growth rate in net revenue from 2010 to 2011?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(247.0, 272.9), divide(#0, 272.9)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy new orleans , inc .
management 2019s financial discussion and analysis plan to spin off the utility 2019s transmission business see the 201cplan to spin off the utility 2019s transmission business 201d section of entergy corporation and subsidiaries management 2019s financial discussion and analysis for a discussion of this matter , including the planned retirement of debt and preferred securities .
results of operations net income 2011 compared to 2010 net income increased $ 4.9 million primarily due to lower other operation and maintenance expenses , lower taxes other than income taxes , a lower effective income tax rate , and lower interest expense , partially offset by lower net revenue .
2010 compared to 2009 net income remained relatively unchanged , increasing $ 0.6 million , primarily due to higher net revenue and lower interest expense , almost entirely offset by higher other operation and maintenance expenses , higher taxes other than income taxes , lower other income , and higher depreciation and amortization expenses .
net revenue 2011 compared to 2010 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges ( credits ) .
following is an analysis of the change in net revenue comparing 2011 to 2010 .
amount ( in millions ) .

 | amount ( in millions )
2010 net revenue | $ 272.9
retail electric price | -16.9 ( 16.9 )
net gas revenue | -9.1 ( 9.1 )
gas cost recovery asset | -3.0 ( 3.0 )
volume/weather | 5.4
other | -2.3 ( 2.3 )
2011 net revenue | $ 247.0

the retail electric price variance is primarily due to formula rate plan decreases effective october 2010 and october 2011 .
see note 2 to the financial statements for a discussion of the formula rate plan filing .
the net gas revenue variance is primarily due to milder weather in 2011 compared to 2010 .
the gas cost recovery asset variance is primarily due to the recognition in 2010 of a $ 3 million gas operations regulatory asset associated with the settlement of entergy new orleans 2019s electric and gas formula rate plan case and the amortization of that asset .
see note 2 to the financial statements for additional discussion of the formula rate plan settlement. .
```

---

## Item 10/25 — `hqa_FQ_e9d8aa67`

- **source**: finqa / HIG/2014/page_126.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the growth rate in balance of u.s . life insurance subsidiaries from 2013 to 2014?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(7157, 6639)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the agencies consider many factors in determining the final rating of an insurance company .
one consideration is the relative level of statutory surplus necessary to support the business written .
statutory surplus represents the capital of the insurance company reported in accordance with accounting practices prescribed by the applicable state insurance department .
see part i , item 1a .
risk factors 2014 201cdowngrades in our financial strength or credit ratings , which may make our products less attractive , could increase our cost of capital and inhibit our ability to refinance our debt , which would have a material adverse effect on our business , financial condition , results of operations and liquidity . 201d statutory surplus the table below sets forth statutory surplus for the company 2019s insurance companies as of december 31 , 2014 and 2013: .

 | 2014 | 2013
u.s . life insurance subsidiaries includes domestic captive insurance subsidiaries in 2013 | $ 7157 | $ 6639
property and casualty insurance subsidiaries | 8069 | 8022
total | $ 15226 | $ 14661

statutory capital and surplus for the u.s .
life insurance subsidiaries , including domestic captive insurance subsidiaries in 2013 , increased by $ 518 , primarily due to variable annuity surplus impacts of $ 788 , net income from non-variable annuity business of $ 187 , increases in unrealized gains from other invested assets carrying values of $ 138 , partially offset by returns of capital of $ 500 , and changes in reserves on account of change in valuation basis of $ 100 .
effective april 30 , 2014 the last domestic captive ceased operations .
statutory capital and surplus for the property and casualty insurance increased by $ 47 , primarily due to statutory net income of $ 1.1 billion , and unrealized gains on investments of $ 1.4 billion , largely offset by dividends to the hfsg holding company of $ 2.5 billion .
the company also held regulatory capital and surplus for its former operations in japan until the sale of those operations on june 30 , 2014 .
under the accounting practices and procedures governed by japanese regulatory authorities , the company 2019s statutory capital and surplus was $ 1.2 billion as of december 31 , 2013. .
```

---

## Item 11/25 — `hqa_FQ_ee6f94ed`

- **source**: finqa / UNP/2009/page_38.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the percentage change in cash provided by operating activities from 2007 to 2008?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(4070, 3277), divide(#0, 3277)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
have access to liquidity by issuing bonds to public or private investors based on our assessment of the current condition of the credit markets .
at december 31 , 2009 , we had a working capital surplus of approximately $ 1.0 billion , which reflects our decision to maintain additional cash reserves to enhance liquidity in response to difficult economic conditions .
at december 31 , 2008 , we had a working capital deficit of approximately $ 100 million .
historically , we have had a working capital deficit , which is common in our industry and does not indicate a lack of liquidity .
we maintain adequate resources and , when necessary , have access to capital to meet any daily and short-term cash requirements , and we have sufficient financial capacity to satisfy our current liabilities .
cash flows millions of dollars 2009 2008 2007 .

millions of dollars | 2009 | 2008 | 2007
cash provided by operating activities | $ 3234 | $ 4070 | $ 3277
cash used in investing activities | -2175 ( 2175 ) | -2764 ( 2764 ) | -2426 ( 2426 )
cash used in financing activities | -458 ( 458 ) | -935 ( 935 ) | -800 ( 800 )
net change in cash and cash equivalents | $ 601 | $ 371 | $ 51

operating activities lower net income in 2009 , a reduction of $ 184 million in the outstanding balance of our accounts receivable securitization program , higher pension contributions of $ 72 million , and changes to working capital combined to decrease cash provided by operating activities compared to 2008 .
higher net income and changes in working capital combined to increase cash provided by operating activities in 2008 compared to 2007 .
in addition , accelerated tax deductions enacted in 2008 on certain new operating assets resulted in lower income tax payments in 2008 versus 2007 .
voluntary pension contributions in 2008 totaling $ 200 million and other pension contributions of $ 8 million partially offset the year-over-year increase versus 2007 .
investing activities lower capital investments and higher proceeds from asset sales drove the decrease in cash used in investing activities in 2009 versus 2008 .
increased capital investments and lower proceeds from asset sales drove the increase in cash used in investing activities in 2008 compared to 2007. .
```

---

## Item 12/25 — `hqa_FQ_ef8ca35e`

- **source**: finqa / ALXN/2007/page_49.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the percent change in the investment into alexion pharmaceuticals between 7/02 and 7/03?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(108.38, 100), divide(#0, 100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the company 2019s stock performance the following graph compares cumulative total return of the company 2019s common stock with the cumulative total return of ( i ) the nasdaq stock market-united states , and ( ii ) the nasdaq biotechnology index .
the graph assumes ( a ) $ 100 was invested on july 31 , 2001 in each of the company 2019s common stock , the stocks comprising the nasdaq stock market-united states and the stocks comprising the nasdaq biotechnology index , and ( b ) the reinvestment of dividends .
comparison of 65 month cumulative total return* among alexion pharmaceuticals , inc. , the nasdaq composite index and the nasdaq biotechnology index alexion pharmaceuticals , inc .
nasdaq composite nasdaq biotechnology .

 | 7/02 | 7/03 | 7/04 | 7/05 | 12/05 | 12/06 | 12/07
alexion pharmaceuticals inc . | 100.00 | 108.38 | 102.64 | 167.89 | 130.56 | 260.41 | 483.75
nasdaq composite | 100.00 | 128.98 | 142.51 | 164.85 | 168.24 | 187.43 | 204.78
nasdaq biotechnology | 100.00 | 149.29 | 146.51 | 176.75 | 186.10 | 183.89 | 187.04

.
```

---

## Item 13/25 — `hqa_FQ_efa45e04`

- **source**: finqa / HOLX/2004/page_87.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the percentage change in rental expense between 2003 and 2004?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(4660, 4963), divide(#0, 4963)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
hologic , inc .
notes to consolidated financial statements 2014 ( continued ) ( in thousands , except per share data ) future minimum lease payments under all the company 2019s operating leases are approximately as follows: .

fiscal years ending | amount
september 24 2005 | $ 4848
september 30 2006 | 4672
september 29 2007 | 3680
september 27 2008 | 3237
september 26 2009 | 3158
thereafter | 40764
total ( not reduced by minimum sublease rentals of $ 165 ) | $ 60359

the company subleases a portion of its bedford facility and has received rental income of $ 277 , $ 410 and $ 682 for fiscal years 2004 , 2003 and 2002 , respectively , which has been recorded as an offset to rent expense in the accompanying statements of income .
rental expense , net of sublease income , was approximately $ 4660 , $ 4963 , and $ 2462 for fiscal 2004 , 2003 and 2002 , respectively .
9 .
business segments and geographic information the company reports segment information in accordance with sfas no .
131 , disclosures about segments of an enterprise and related information .
operating segments are identified as components of an enterprise about which separate , discrete financial information is available for evaluation by the chief operating decision maker , or decision-making group , in making decisions how to allocate resources and assess performance .
the company 2019s chief decision-maker , as defined under sfas no .
131 , is the chief executive officer .
to date , the company has viewed its operations and manages its business as four principal operating segments : the manufacture and sale of mammography products , osteoporosis assessment products , digital detectors and other products .
as a result of the company 2019s implementation of a company wide integrated software application in fiscal 2003 , identifiable assets for the four principal operating segments only consist of inventories , intangible assets , and property and equipment .
the company has presented all other assets as corporate assets .
prior periods have been restated to conform to this presentation .
intersegment sales and transfers are not significant. .
```

---

## Item 14/25 — `hqa_FQ_f6d8326c`

- **source**: finqa / L/2016/page_62.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the growth rate of the s&p 500 index from 2011 to 2016

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(198.18, 100.0), divide(#0, const_100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
item 5 .
market for the registrant 2019s common equity , related stockholder matters and issuer purchases of equity securities the following graph compares annual total return of our common stock , the standard & poor 2019s 500 composite stock index ( 201cs&p 500 index 201d ) and our peer group ( 201cloews peer group 201d ) for the five years ended december 31 , 2016 .
the graph assumes that the value of the investment in our common stock , the s&p 500 index and the loews peer group was $ 100 on december 31 , 2011 and that all dividends were reinvested. .

 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016
loews common stock | 100.0 | 108.91 | 129.64 | 113.59 | 104.47 | 128.19
s&p 500 index | 100.0 | 116.00 | 153.57 | 174.60 | 177.01 | 198.18
loews peer group ( a ) | 100.0 | 113.39 | 142.85 | 150.44 | 142.44 | 165.34

( a ) the loews peer group consists of the following companies that are industry competitors of our principal operating subsidiaries : chubb limited ( name change from ace limited after it acquired the chubb corporation on january 15 , 2016 ) , w.r .
berkley corporation , the chubb corporation ( included through january 15 , 2016 when it was acquired by ace limited ) , energy transfer partners l.p. , ensco plc , the hartford financial services group , inc. , kinder morgan energy partners , l.p .
( included through november 26 , 2014 when it was acquired by kinder morgan inc. ) , noble corporation , spectra energy corp , transocean ltd .
and the travelers companies , inc .
dividend information we have paid quarterly cash dividends in each year since 1967 .
regular dividends of $ 0.0625 per share of loews common stock were paid in each calendar quarter of 2016 and 2015. .
```

---

## Item 15/25 — `hqa_FQ_fab23070`

- **source**: finqa / UPS/2015/page_108.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in millions of aircraft from 2014 to 2015?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(2289, 2289)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
united parcel service , inc .
and subsidiaries notes to consolidated financial statements capital lease obligations we have certain property , plant and equipment subject to capital leases .
some of the obligations associated with these capital leases have been legally defeased .
the recorded value of our property , plant and equipment subject to capital leases is as follows as of december 31 ( in millions ) : .

 | 2015 | 2014
vehicles | $ 74 | $ 86
aircraft | 2289 | 2289
buildings | 207 | 197
accumulated amortization | -849 ( 849 ) | -781 ( 781 )
property plant and equipment subject to capital leases | $ 1721 | $ 1791

these capital lease obligations have principal payments due at various dates from 2016 through 3005 .
facility notes and bonds we have entered into agreements with certain municipalities to finance the construction of , or improvements to , facilities that support our u.s .
domestic package and supply chain & freight operations in the united states .
these facilities are located around airport properties in louisville , kentucky ; dallas , texas ; and philadelphia , pennsylvania .
under these arrangements , we enter into a lease or loan agreement that covers the debt service obligations on the bonds issued by the municipalities , as follows : 2022 bonds with a principal balance of $ 149 million issued by the louisville regional airport authority associated with our worldport facility in louisville , kentucky .
the bonds , which are due in january 2029 , bear interest at a variable rate , and the average interest rates for 2015 and 2014 were 0.03% ( 0.03 % ) and 0.05% ( 0.05 % ) , respectively .
2022 bonds with a principal balance of $ 42 million and due in november 2036 issued by the louisville regional airport authority associated with our air freight facility in louisville , kentucky .
the bonds bear interest at a variable rate , and the average interest rates for 2015 and 2014 were 0.02% ( 0.02 % ) and 0.05% ( 0.05 % ) , respectively .
2022 bonds with a principal balance of $ 29 million issued by the dallas / fort worth international airport facility improvement corporation associated with our dallas , texas airport facilities .
the bonds are due in may 2032 and bear interest at a variable rate , however the variable cash flows on the obligation have been swapped to a fixed 5.11% ( 5.11 % ) .
2022 bonds with a principal balance of $ 100 million issued by the delaware county , pennsylvania industrial development authority associated with our philadelphia , pennsylvania airport facilities .
the bonds , which were due in december 2015 , had a variable interest rate , and the average interest rates for 2015 and 2014 were 0.02% ( 0.02 % ) and 0.04% ( 0.04 % ) , respectively .
as of december 2015 , these $ 100 million bonds were repaid in full .
2022 in september 2015 , we entered into an agreement with the delaware county , pennsylvania industrial development authority , associated with our philadelphia , pennsylvania airport facilities , for bonds issued with a principal balance of $ 100 million .
these bonds , which are due september 2045 , bear interest at a variable rate .
the average interest rate for 2015 was 0.00% ( 0.00 % ) .
pound sterling notes the pound sterling notes consist of two separate tranches , as follows : 2022 notes with a principal amount of a366 million accrue interest at a 5.50% ( 5.50 % ) fixed rate , and are due in february 2031 .
these notes are not callable .
2022 notes with a principal amount of a3455 million accrue interest at a 5.125% ( 5.125 % ) fixed rate , and are due in february 2050 .
these notes are callable at our option at a redemption price equal to the greater of 100% ( 100 % ) of the principal amount and accrued interest , or the sum of the present values of the remaining scheduled payout of principal and interest thereon discounted to the date of redemption at a benchmark u.k .
government bond yield plus 15 basis points and accrued interest. .
```

---

## Item 16/25 — `hqa_TAT_0a4b6243`

- **source**: tatqa / 0026dd98-75c7-4e4e-b7f2-283c6281180d
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in Current income tax expense (benefit) in 2019 from 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (203-447)/447 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
|  | Fiscal | 
 | 2019 | 2018 | 2017
 |  | (in millions) | 
Current income tax expense (benefit): |  |  | 
U.S.: |  |  | 
Federal | $ (28) | $ 20 | $ (9)
State | 2 | 21 | 9
Non-U.S. | 229 | 406 | 322
 | 203 | 447 | 322
Deferred income tax expense (benefit): |  |  | 
U.S.: |  |  | 
Federal | (25) | 499 | (119)
State | (8) | (30) | (15)
Non-U.S. | (185) | (1,260) | (8)
 | (218) | (791) | (142)
Income tax expense (benefit) | $ (15) | $ (344) | $ 180

Income Tax Expense (Benefit)
Significant components of the income tax expense (benefit) were as follows:
```

---

## Item 17/25 — `hqa_TAT_10183a57`

- **source**: tatqa / 045cf854-cb0b-459a-a1a0-a643e9d545da
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in net computer software between 2018 and 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (406.0-405.6)/405.6 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| December 31, | 
 | 2019 | 2018
Internally developed software | $808.2 | $746.0
Purchased software | 78.9 | 60.7
Computer software | 887.1 | 806.7
Accumulated amortization | (481.1) | (401.1)
Computer software, net | $406.0 | $405.6

(8) Computer Software
Computer software, net consists of the following (in millions):
In the fourth quarter of 2019, we entered into agreements to acquire software in exchange for a combination of cash consideration and certain of our products and services. The software was acquired for $32.0 million, of which software valued at $6.5 million was received as of December 31, 2019 and resulted in non-cash investing activity of $4.8 million.
```

---

## Item 18/25 — `hqa_TAT_12e27eaa`

- **source**: tatqa / 03e1ffb8-f176-456a-b4ea-35a47c240941
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the change in operating profit between 2018 and 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: 120,953-152,790 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| Year Ended December 31, | 
 | 2019 | 2018
Total revenue | $529,646 | $414,673
Total costs and expenses | 408,693 | 261,883
Operating profit | 120,953 | 152,790
Total other income (expense), net | (22,297) | (19,276)
Net income | $98,656 | $133,514

GreenSky, Inc. NOTES TO CONSOLIDATED FINANCIAL STATEMENTS — (Continued) (United States Dollars in thousands, except per share data, unless otherwise stated)
The following table reflects the impact of consolidation of GS Holdings into the Consolidated Statements of Operations for the years indicated.
```

---

## Item 19/25 — `hqa_TAT_261ad3a9`

- **source**: tatqa / e2b0141c-a9f5-412c-a62b-47de0287d740
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in Cash and cash equivalents from 2018 to 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (172,960-172,704)/172,704 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| December 31, | 
 | 2019 | 2018
Cash and cash equivalents | $172,960 | $172,704
Restricted cash included in other long-term assets | 116 | 114
Total cash, cash equivalents and restricted cash reported on the Consolidated Statements of Cash Flows | $173,076 | $172,818

Restricted Cash
The following table provides a reconciliation of cash, cash equivalents and restricted cash reported on the Consolidated Balance Sheets to the amounts reported on the Consolidated Statements of Cash Flows (in thousands):
As of December 31, 2019 and 2018, restricted cash included a security deposit that is set aside in a bank account and cannot be withdrawn by the Company under the terms of a lease agreement. The restriction will end upon the expiration of the lease.
```

---

## Item 20/25 — `hqa_TAT_2728a2bd`

- **source**: tatqa / 2189131d-ea05-40c5-9034-68d130f2c97f
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in the Total shares reserved for issuance between 2018 and 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (29,002-27,382)/27,382 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| June 30,
2019 | June 30,
2018
2013 Equity Incentive Plan shares available for grant | 8,462 | 9,957
Employee stock options and awards outstanding | 10,455 | 12,060
2014 Employee Stock Purchase Plan | 10,085 | 5,365
Total shares reserved for issuance | 29,002 | 27,382

Shares Reserved for Issuance
The following are shares reserved for issuance (in thousands):
```

---

## Item 21/25 — `hqa_TAT_28c0f57b`

- **source**: tatqa / b310f082-f650-4361-bf8b-65e6caae60dd
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in Other receivables in 2019 from 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (0.3-0.1)/0.1 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
|  | 2019 | 2018
 | Note | £m | £m
Net trade receivables | 18 | 24.9 | 25.4
Accrued income | 18 | 28.0 | 26.7
Other receivables | 18 | 0.3 | 0.1
Cash and cash equivalents | 19 | 5.9 | 4.3
Total |  | 59.1 | 56.5

31. Financial instruments
Financial assets
```

---

## Item 22/25 — `hqa_TAT_37191d9a`

- **source**: tatqa / ffd43080-e942-4219-822f-065e6152c233
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in total revenue between 2018 and 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (468,999-470,483)/470,483 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| Twelve Months Ended December 31, | 
 | 2019 | 2018
Transportation | $299,005 | $300,124
Industrial | 78,369 | 86,968
Medical | 41,901 | 40,663
Aerospace & Defense | 32,569 | 23,323
Telecom & IT | 17,155 | 19,405
Total | $468,999 | $470,483

NOTES TO CONSOLIDATED FINANCIAL STATEMENTS (in thousands, except for share and per share data)
Disaggregated Revenue
The following table presents revenues disaggregated by the major markets we serve:
```

---

## Item 23/25 — `hqa_TAT_37cd0c30`

- **source**: tatqa / eb92a24d-a751-48c1-bb6f-6c83030d24bb
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What is the change in the allocation of equities from 2018 to 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: 55%-55% Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
| As of June 30 | 
 | 2019 | 2018
Fixed income | 40% | 40%
Equities | 55% | 55%
Other | 5% | 5%
Total | 100% | 100%

The defined benefit pension plan utilizes various investment securities. Generally, investment securities are exposed to various risks, such as interest rate risks, credit risk, and overall market volatility. Due to the level of risk associated with certain investment securities, it is reasonably possible that changes in the values of investment securities will occur and that such changes could materially affect the amounts reported.
The following table presents the Company’s target for the allocation of invested defined benefit pension plan assets at June 30, 2019 and June 30, 2018:
```

---

## Item 24/25 — `hqa_TAT_37e855b0`

- **source**: tatqa / 69a4977f-afb4-47ba-8d30-e4717132c290
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What was the percentage change in Total operating income in the Communications Solutions segment in 2019 from 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (49-13)/13 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
|  | Fiscal
 | 2019 | 2018
 |  | (in millions)
Restructuring and other charges, net | $  48 | $  13
Other items | 1 | —
Total | $  49 | $  13

In the Communications Solutions segment, operating income decreased $79 million in fiscal 2019 as compared to fiscal 2018. The Communications Solutions segment’s operating income included the following:
Excluding these items, operating income decreased in fiscal 2019 due primarily to lower volume.
```

---

## Item 25/25 — `hqa_TAT_3bfabcc3`

- **source**: tatqa / e07f8967-1b86-4433-ba9c-47b09e89e6b8
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: What is the percentage change in share-based compensation for sales and marketing between 2018 and 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: (31,156 - 20,807)/20,807 Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
|  | Year ended December 31, | 
 | 2019 | 2018 | 2017
Cost of revenues | $8,741 | $4,982 | $3,735
Research and development | 23,132 | 14,975 | 9,550
Sales and marketing | 38,325 | 27,324 | 16,015
General and administrative | 31,156 | 20,807 | 12,760
Total share-based compensation expense | $101,354 | 68,088 | 42,060

Note 11. Share-Based Compensation
A summary of share-based compensation expense recognized in the Company’s Consolidated Statements of Operations is as follows (in thousands):
```

---
