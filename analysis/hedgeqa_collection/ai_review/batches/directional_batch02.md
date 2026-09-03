# Blind review batch `directional_batch02`

25 items. Family: `numeric_to_directional`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_CFQ_9621ac0e`

- **source**: convfinqa / Single_AMAT/2014/page_37.pdf-1#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what was the price of applied materials as of 10/28/12?

Question: and the change in price between then and the original investment?

**Original source question**: and the change in price between then and the original investment?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(88.54, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the performance graph below shows the five-year cumulative total stockholder return on applied common stock during the period from october 25 , 2009 through october 26 , 2014 .
this is compared with the cumulative total return of the standard & poor 2019s 500 stock index and the rdg semiconductor composite index over the same period .
the comparison assumes $ 100 was invested on october 25 , 2009 in applied common stock and in each of the foregoing indices and assumes reinvestment of dividends , if any .
dollar amounts in the graph are rounded to the nearest whole dollar .
the performance shown in the graph represents past performance and should not be considered an indication of future performance .
comparison of 5 year cumulative total return* among applied materials , inc. , the s&p 500 index 201cs&p 201d is a registered trademark of standard & poor 2019s financial services llc , a subsidiary of the mcgraw-hill companies , inc. .

 | 10/25/2009 | 10/31/2010 | 10/30/2011 | 10/28/2012 | 10/27/2013 | 10/26/2014
applied materials | 100.00 | 97.43 | 101.85 | 88.54 | 151.43 | 183.29
s&p 500 index | 100.00 | 116.52 | 125.94 | 145.09 | 184.52 | 216.39
rdg semiconductor composite index | 100.00 | 121.00 | 132.42 | 124.95 | 163.20 | 207.93

dividends during fiscal 2014 , applied 2019s board of directors declared four quarterly cash dividends of $ 0.10 per share each .
during fiscal 2013 , applied 2019s board of directors declared three quarterly cash dividends of $ 0.10 per share each and one quarterly cash dividend of $ 0.09 per share .
during fiscal 2012 , applied 2019s board of directors declared three quarterly cash dividends of $ 0.09 per share each and one quarterly cash dividend of $ 0.08 .
dividends declared during fiscal 2014 , 2013 and 2012 totaled $ 487 million , $ 469 million and $ 438 million , respectively .
applied currently anticipates that it will continue to pay cash dividends on a quarterly basis in the future , although the declaration and amount of any future cash dividends are at the discretion of the board of directors and will depend on applied 2019s financial condition , results of operations , capital requirements , business conditions and other factors , as well as a determination that cash dividends are in the best interests of applied 2019s stockholders .
$ 100 invested on 10/25/09 in stock or 10/31/09 in index , including reinvestment of dividends .
indexes calculated on month-end basis .
and the rdg semiconductor composite index 183145 97 102 121 132 10/25/09 10/31/10 10/30/11 10/28/12 10/27/13 10/26/14 applied materials , inc .
s&p 500 rdg semiconductor composite .
```

---

## Item 2/25 — `hqa_CFQ_9cddac48`

- **source**: convfinqa / Single_EW/2013/page_33.pdf-1#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what is the net change in value of edwards lifesciences in 2013 less 100?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(239.34, const_100), divide(#0, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
25feb201400255845 performance graph the following graph compares the performance of our common stock with that of the s&p 500 index and the s&p 500 healthcare equipment index .
the cumulative total return listed below assumes an initial investment of $ 100 on december 31 , 2008 and reinvestment of dividends .
comparison of five year cumulative total return 2008 2009 2010 2011 20132012 edwards lifesciences s&p 500 s&p 500 healthcare equipment december 31 .

total cumulative return | 2009 | 2010 | 2011 | 2012 | 2013
edwards lifesciences | $ 158.05 | $ 294.23 | $ 257.32 | $ 328.19 | $ 239.34
s&p 500 | 126.46 | 145.51 | 148.59 | 172.37 | 228.19
s&p 500 healthcare equipment index | 120.83 | 117.02 | 123.37 | 145.84 | 186.00

.
```

---

## Item 3/25 — `hqa_CFQ_b6555530`

- **source**: convfinqa / Double_ORLY/2015/page_28.pdf#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: was the five year return of the s&p 500 retail index greater than the s&p 500?

Question: what was the price change of the s&p 500 between 2010 and 2011?

**Original source question**: what was the price change of the s&p 500 between 2010 and 2011?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(100, 100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph : the graph below shows the cumulative total shareholder return assuming the investment of $ 100 , on december 31 , 2010 , and the reinvestment of dividends thereafter , if any , in the company's common stock versus the standard and poor's s&p 500 retail index ( "s&p 500 retail index" ) and the standard and poor's s&p 500 index ( "s&p 500" ) . .

company/index | december 31 , 2010 | december 31 , 2011 | december 31 , 2012 | december 31 , 2013 | december 31 , 2014 | december 31 , 2015
o'reilly automotive inc . | $ 100 | $ 132 | $ 148 | $ 213 | $ 319 | $ 419
s&p 500 retail index | 100 | 103 | 128 | 185 | 203 | 252
s&p 500 | $ 100 | $ 100 | $ 113 | $ 147 | $ 164 | $ 163

.
```

---

## Item 4/25 — `hqa_CFQ_ba327bc7`

- **source**: convfinqa / Single_JPM/2016/page_73.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the value of jpmorgan chase from the original investment in 2011 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(298.31, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
jpmorgan chase & co./2016 annual report 35 five-year stock performance the following table and graph compare the five-year cumulative total return for jpmorgan chase & co .
( 201cjpmorgan chase 201d or the 201cfirm 201d ) common stock with the cumulative return of the s&p 500 index , the kbw bank index and the s&p financial index .
the s&p 500 index is a commonly referenced united states of america ( 201cu.s . 201d ) equity benchmark consisting of leading companies from different economic sectors .
the kbw bank index seeks to reflect the performance of banks and thrifts that are publicly traded in the u.s .
and is composed of leading national money center and regional banks and thrifts .
the s&p financial index is an index of financial companies , all of which are components of the s&p 500 .
the firm is a component of all three industry indices .
the following table and graph assume simultaneous investments of $ 100 on december 31 , 2011 , in jpmorgan chase common stock and in each of the above indices .
the comparison assumes that all dividends are reinvested .
december 31 , ( in dollars ) 2011 2012 2013 2014 2015 2016 .

december 31 ( in dollars ) | 2011 | 2012 | 2013 | 2014 | 2015 | 2016
jpmorgan chase | $ 100.00 | $ 136.18 | $ 186.17 | $ 204.57 | $ 221.68 | $ 298.31
kbw bank index | 100.00 | 133.03 | 183.26 | 200.42 | 201.40 | 258.82
s&p financial index | 100.00 | 128.75 | 174.57 | 201.06 | 197.92 | 242.94
s&p 500 index | 100.00 | 115.99 | 153.55 | 174.55 | 176.95 | 198.10

december 31 , ( in dollars ) .
```

---

## Item 5/25 — `hqa_CFQ_bce1262b`

- **source**: convfinqa / Single_BKNG/2015/page_38.pdf-4#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what is the 2015 value of priceline less 100?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(319.10, const_100), divide(#0, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
measurement point december 31 the priceline group nasdaq composite index s&p 500 rdg internet composite .

measurement pointdecember 31 | the priceline group inc . | nasdaqcomposite index | s&p 500index | rdg internetcomposite
2010 | 100.00 | 100.00 | 100.00 | 100.00
2011 | 117.06 | 100.53 | 102.11 | 102.11
2012 | 155.27 | 116.92 | 118.45 | 122.23
2013 | 290.93 | 166.19 | 156.82 | 199.42
2014 | 285.37 | 188.78 | 178.29 | 195.42
2015 | 319.10 | 199.95 | 180.75 | 267.25

.
```

---

## Item 6/25 — `hqa_CFQ_c80d1d26`

- **source**: convfinqa / Double_MAS/2010/page_29.pdf#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the performance price of the masco common stock in the five year period ended 2010?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(51.51, 100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the table below compares the cumulative total shareholder return on our common stock with the cumulative total return of ( i ) the standard & poor 2019s 500 composite stock index ( 201cs&p 500 index 201d ) , ( ii ) the standard & poor 2019s industrials index ( 201cs&p industrials index 201d ) and ( iii ) the standard & poor 2019s consumer durables & apparel index ( 201cs&p consumer durables & apparel index 201d ) , from december 31 , 2005 through december 31 , 2010 , when the closing price of our common stock was $ 12.66 .
the graph assumes investments of $ 100 on december 31 , 2005 in our common stock and in each of the three indices and the reinvestment of dividends .
performance graph 201020092008200720062005 s&p 500 index s&p industrials index s&p consumer durables & apparel index the table below sets forth the value , as of december 31 for each of the years indicated , of a $ 100 investment made on december 31 , 2005 in each of our common stock , the s&p 500 index , the s&p industrials index and the s&p consumer durables & apparel index and includes the reinvestment of dividends. .

 | 2006 | 2007 | 2008 | 2009 | 2010
masco | $ 101.79 | $ 76.74 | $ 42.81 | $ 54.89 | $ 51.51
s&p 500 index | $ 115.61 | $ 121.95 | $ 77.38 | $ 97.44 | $ 111.89
s&p industrials index | $ 113.16 | $ 126.72 | $ 76.79 | $ 92.30 | $ 116.64
s&p consumer durables & apparel index | $ 106.16 | $ 84.50 | $ 56.13 | $ 76.51 | $ 99.87

in july 2007 , our board of directors authorized the purchase of up to 50 million shares of our common stock in open-market transactions or otherwise .
at december 31 , 2010 , we had remaining authorization to repurchase up to 27 million shares .
during 2010 , we repurchased and retired three million shares of our common stock , for cash aggregating $ 45 million to offset the dilutive impact of the 2010 grant of three million shares of long-term stock awards .
we did not purchase any shares during the three months ended december 31 , 2010. .
```

---

## Item 7/25 — `hqa_CFQ_ca7d7f01`

- **source**: convfinqa / Single_ETFC/2015/page_27.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the change in the value of an investment in e*trade financial corporation from 2010 to 2015?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(185.25, const_100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
table of contents performance graph the following performance graph shows the cumulative total return to a holder of the company 2019s common stock , assuming dividend reinvestment , compared with the cumulative total return , assuming dividend reinvestment , of the standard & poor ( "s&p" ) 500 index and the dow jones us financials index during the period from december 31 , 2010 through december 31 , 2015. .

 | 12/10 | 12/11 | 12/12 | 12/13 | 12/14 | 12/15
e*trade financial corporation | 100.00 | 49.75 | 55.94 | 122.75 | 151.59 | 185.25
s&p 500 index | 100.00 | 102.11 | 118.45 | 156.82 | 178.29 | 180.75
dow jones us financials index | 100.00 | 87.16 | 110.56 | 148.39 | 170.04 | 170.19

.
```

---

## Item 8/25 — `hqa_CFQ_e1fe26ff`

- **source**: convfinqa / Single_GPN/2007/page_39.pdf-2#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what is the net change in value of global payments from 2003 to 2004?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(129.77, 94.20), divide(#0, 94.20)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph the following line-graph presentation compares our cumulative shareholder returns with the standard & poor 2019s information technology index and the standard & poor 2019s 500 stock index for the past five years .
the line graph assumes the investment of $ 100 in our common stock , the standard & poor 2019s information technology index , and the standard & poor 2019s 500 stock index on may 31 , 2002 and assumes reinvestment of all dividends .
comparison of 5 year cumulative total return* among global payments inc. , the s&p 500 index and the s&p information technology index 5/02 5/03 5/04 5/05 5/06 5/07 global payments inc .
s&p 500 s&p information technology * $ 100 invested on 5/31/02 in stock or index-including reinvestment of dividends .
fiscal year ending may 31 .
global payments s&p 500 information technology .

 | global payments | s&p 500 | s&p information technology
may 31 2002 | $ 100.00 | $ 100.00 | $ 100.00
may 31 2003 | 94.20 | 91.94 | 94.48
may 31 2004 | 129.77 | 108.79 | 115.24
may 31 2005 | 193.30 | 117.75 | 116.29
may 31 2006 | 260.35 | 127.92 | 117.14
may 31 2007 | 224.24 | 157.08 | 144.11

issuer purchases of equity securities on april 5 , 2007 , our board of directors authorized repurchases of our common stock in an amount up to $ 100 million .
the board has authorized us to purchase shares from time to time as market conditions permit .
there is no expiration date with respect to this authorization .
no amounts have been repurchased during the fiscal year ended may 31 , 2007. .
```

---

## Item 9/25 — `hqa_CFQ_e2dffb49`

- **source**: convfinqa / Single_TFX/2015/page_42.pdf-3#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what is the change value of the s&p healthcare index from 2010 to 2015?

Question: what is the change in value of the s&p 500 from 2010 to 2015?

**Original source question**: what is the change in value of the s&p 500 from 2010 to 2015?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(199, 100), subtract(181, 100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph the following graph provides a comparison of five year cumulative total stockholder returns of teleflex common stock , the standard & poor 2019s ( s&p ) 500 stock index and the s&p 500 healthcare equipment & supply index .
the annual changes for the five-year period shown on the graph are based on the assumption that $ 100 had been invested in teleflex common stock and each index on december 31 , 2010 and that all dividends were reinvested .
market performance .

company / index | 2010 | 2011 | 2012 | 2013 | 2014 | 2015
teleflex incorporated | 100 | 117 | 138 | 185 | 229 | 266
s&p 500 index | 100 | 102 | 118 | 157 | 178 | 181
s&p 500 healthcare equipment & supply index | 100 | 99 | 116 | 148 | 187 | 199

s&p 500 healthcare equipment & supply index 100 99 116 148 187 199 .
```

---

## Item 10/25 — `hqa_CFQ_e45ced5c`

- **source**: convfinqa / Single_AON/2009/page_90.pdf-4#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in value of unrecognized tax benefits from 2008 to 2009?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(77, 86)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
at december 31 , 2009 , aon had domestic federal operating loss carryforwards of $ 7 million that will expire at various dates from 2010 to 2024 , state operating loss carryforwards of $ 513 million that will expire at various dates from 2010 to 2028 , and foreign operating and capital loss carryforwards of $ 453 million and $ 252 million , respectively , nearly all of which are subject to indefinite carryforward .
unrecognized tax benefits the following is a reconciliation of the company 2019s beginning and ending amount of unrecognized tax benefits ( in millions ) : .

 | 2009 | 2008
balance at january 1 | $ 86 | $ 70
additions based on tax positions related to the current year | 2 | 5
additions for tax positions of prior years | 5 | 12
reductions for tax positions of prior years | -11 ( 11 ) | -11 ( 11 )
settlements | -10 ( 10 ) | -4 ( 4 )
lapse of statute of limitations | -3 ( 3 ) | -1 ( 1 )
acquisitions | 6 | 21
foreign currency translation | 2 | -6 ( 6 )
balance at december 31 | $ 77 | $ 86

as of december 31 , 2009 , $ 61 million of unrecognized tax benefits would impact the effective tax rate if recognized .
aon does not expect the unrecognized tax positions to change significantly over the next twelve months .
the company recognizes penalties and interest related to unrecognized income tax benefits in its provision for income taxes .
aon accrued potential penalties of less than $ 1 million during each of 2009 , 2008 and 2007 .
aon accrued interest of $ 2 million during 2009 and less than $ 1 million during both 2008 and 2007 .
as of december 31 , 2009 and 2008 , aon has recorded a liability for penalties of $ 5 million and $ 4 million , respectively , and for interest of $ 18 million and $ 14 million , respectively .
aon and its subsidiaries file income tax returns in the u.s .
federal jurisdiction as well as various state and international jurisdictions .
aon has substantially concluded all u.s .
federal income tax matters for years through 2006 .
material u.s .
state and local income tax jurisdiction examinations have been concluded for years through 2002 .
aon has concluded income tax examinations in its primary international jurisdictions through 2002. .
```

---

## Item 11/25 — `hqa_CFQ_eaf13931`

- **source**: convfinqa / Single_MMM/2015/page_19.pdf-2#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the amount of shares authorized for repurchase between 2014 and 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(10, 12)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
part ii item 5 .
market for registrant 2019s common equity , related stockholder matters and issuer purchases of equity securities .
equity compensation plans 2019 information is incorporated by reference from part iii , item 12 , 201csecurity ownership of certain beneficial owners and management and related stockholder matters , 201d of this document , and should be considered an integral part of item 5 .
at january 31 , 2016 , there were 84607 shareholders of record .
3m 2019s stock is listed on the new york stock exchange , inc .
( nyse ) , the chicago stock exchange , inc. , and the swx swiss exchange .
cash dividends declared and paid totaled $ 1.025 per share for each of the second , third , and fourth quarters of 2015 .
cash dividends declared in the fourth quarter of 2014 included a dividend paid in november 2014 of $ 0.855 per share and a dividend paid in march 2015 of $ 1.025 per share .
cash dividends declared and paid totaled $ 0.855 per share for each of the second and third quarters of 2014 .
cash dividends declared in the fourth quarter of 2013 include a dividend paid in march 2014 of $ 0.855 per share .
stock price comparisons follow : stock price comparisons ( nyse composite transactions ) .

( per share amounts ) | first quarter | second quarter | third quarter | fourth quarter | total
2015 high | $ 170.50 | $ 167.70 | $ 157.94 | $ 160.09 | $ 170.50
2015 low | 157.74 | 153.92 | 134.00 | 138.57 | 134.00
2014 high | $ 139.29 | $ 145.53 | $ 147.87 | $ 168.16 | $ 168.16
2014 low | 123.61 | 132.02 | 138.43 | 130.60 | 123.61

issuer purchases of equity securities repurchases of 3m common stock are made to support the company 2019s stock-based employee compensation plans and for other corporate purposes .
in february 2014 , 3m 2019s board of directors authorized the repurchase of up to $ 12 billion of 3m 2019s outstanding common stock , with no pre-established end date .
in february 2016 , 3m 2019s board of directors replaced the company 2019s february 2014 repurchase program with a new repurchase program .
this new program authorizes the repurchase of up to $ 10 billion of 3m 2019s outstanding common stock , with no pre-established end date. .
```

---

## Item 12/25 — `hqa_CFQ_eb6cfd8c`

- **source**: convfinqa / Single_RCL/2016/page_37.pdf-2#turn1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: Conversation so far:
Q1: what is the value of an investment in s&p500 in 2016?

Question: what is the change in value of an investment in s&p500 from 2011 to 2016?

**Original source question**: what is the change in value of an investment in s&p500 from 2011 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(198.18, const_100)' History handling: turn 1; 1 prior turn(s) inlined verbatim. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the following graph compares the total return , assuming reinvestment of dividends , on an investment in the company , based on performance of the company's common stock , with the total return of the standard & poor's 500 composite stock index and the dow jones united states travel and leisure index for a five year period by measuring the changes in common stock prices from december 31 , 2011 to december 31 , 2016. .

 | 12/11 | 12/12 | 12/13 | 12/14 | 12/15 | 12/16
royal caribbean cruises ltd . | 100.00 | 139.36 | 198.03 | 350.40 | 437.09 | 362.38
s&p 500 | 100.00 | 116.00 | 153.58 | 174.60 | 177.01 | 198.18
dow jones us travel & leisure | 100.00 | 113.33 | 164.87 | 191.85 | 203.17 | 218.56

the stock performance graph assumes for comparison that the value of the company's common stock and of each index was $ 100 on december 31 , 2011 and that all dividends were reinvested .
past performance is not necessarily an indicator of future results. .
```

---

## Item 13/25 — `hqa_CFQ_f1de8ce5`

- **source**: convfinqa / Single_ORLY/2017/page_30.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the net change in value of an investment in s&p500 from 2014 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(157, 144)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
stock performance graph : the graph below shows the cumulative total shareholder return assuming the investment of $ 100 , on december 31 , 2012 , and the reinvestment of dividends thereafter , if any , in the company 2019s common stock versus the standard and poor 2019s s&p 500 retail index ( 201cs&p 500 retail index 201d ) and the standard and poor 2019s s&p 500 index ( 201cs&p 500 201d ) . .

company/index | december 31 , 2012 | december 31 , 2013 | december 31 , 2014 | december 31 , 2015 | december 31 , 2016 | december 31 , 2017
o 2019reilly automotive inc . | $ 100 | $ 144 | $ 215 | $ 283 | $ 311 | $ 269
s&p 500 retail index | 100 | 144 | 158 | 197 | 206 | 265
s&p 500 | $ 100 | $ 130 | $ 144 | $ 143 | $ 157 | $ 187

.
```

---

## Item 14/25 — `hqa_CFQ_f3666c8b`

- **source**: convfinqa / Single_STT/2013/page_54.pdf-4#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the fraction change of the investment in s&p500 from 2008 to 2013?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='divide(228, 100)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
shareholder return performance presentation the graph presented below compares the cumulative total shareholder return on state street's common stock to the cumulative total return of the s&p 500 index , the s&p financial index and the kbw bank index over a five- year period .
the cumulative total shareholder return assumes the investment of $ 100 in state street common stock and in each index on december 31 , 2008 at the closing price on the last trading day of 2008 , and also assumes reinvestment of common stock dividends .
the s&p financial index is a publicly available measure of 81 of the standard & poor's 500 companies , representing 17 diversified financial services companies , 22 insurance companies , 19 real estate companies and 23 banking companies .
the kbw bank index seeks to reflect the performance of banks and thrifts that are publicly traded in the u.s. , and is composed of 24 leading national money center and regional banks and thrifts. .

 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013
state street corporation | $ 100 | $ 111 | $ 118 | $ 105 | $ 125 | $ 198
s&p 500 index | 100 | 126 | 146 | 149 | 172 | 228
s&p financial index | 100 | 117 | 132 | 109 | 141 | 191
kbw bank index | 100 | 98 | 121 | 93 | 122 | 168

.
```

---

## Item 15/25 — `hqa_CFQ_f82e55fe`

- **source**: convfinqa / Single_ETR/2004/page_159.pdf-1#turn0
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the net change in revenues from 2003 to 2004?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: turn_program='subtract(978.4, 998.7)' History handling: first turn; no history needed. Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy arkansas , inc .
management's financial discussion and analysis results of operations net income 2004 compared to 2003 net income increased $ 16.2 million due to lower other operation and maintenance expenses , a lower effective income tax rate for 2004 compared to 2003 , and lower interest charges .
the increase was partially offset by lower net revenue .
2003 compared to 2002 net income decreased $ 9.6 million due to lower net revenue , higher depreciation and amortization expenses , and a higher effective income tax rate for 2003 compared to 2002 .
the decrease was substantially offset by lower other operation and maintenance expenses , higher other income , and lower interest charges .
net revenue 2004 compared to 2003 net revenue , which is entergy arkansas' measure of gross margin , consists of operating revenues net of : 1 ) fuel , fuel-related , and purchased power expenses and 2 ) other regulatory credits .
following is an analysis of the change in net revenue comparing 2004 to 2003. .

 | ( in millions )
2003 net revenue | $ 998.7
deferred fuel cost revisions | -16.9 ( 16.9 )
other | -3.4 ( 3.4 )
2004 net revenue | $ 978.4

deferred fuel cost revisions includes the difference between the estimated deferred fuel expense and the actual calculation of recoverable fuel expense , which occurs on an annual basis .
deferred fuel cost revisions decreased net revenue due to a revised estimate of fuel costs filed for recovery at entergy arkansas in the march 2004 energy cost recovery rider , which reduced net revenue by $ 11.5 million .
the remainder of the variance is due to the 2002 energy cost recovery true-up , made in the first quarter of 2003 , which increased net revenue in 2003 .
gross operating revenues , fuel and purchased power expenses , and other regulatory credits gross operating revenues increased primarily due to : 2022 an increase of $ 20.7 million in fuel cost recovery revenues due to an increase in the energy cost recovery rider effective april 2004 ( fuel cost recovery revenues are discussed in note 2 to the domestic utility companies and system energy financial statements ) ; 2022 an increase of $ 15.5 million in grand gulf revenues due to an increase in the grand gulf rider effective january 2004 ; 2022 an increase of $ 13.9 million in gross wholesale revenue primarily due to increased sales to affiliated systems ; 2022 an increase of $ 9.5 million due to volume/weather primarily resulting from increased usage during the unbilled sales period , partially offset by the effect of milder weather on billed sales in 2004. .
```

---

## Item 16/25 — `hqa_FQ_0921febd`

- **source**: finqa / STT/2001/page_85.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percentage change in the balance of letters of credit from 2000 to 2001?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(164, 218), divide(#0, 218)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
loan commitments ( unfunded loans and unused lines of credit ) , asset purchase agreements , standby letters of credit and letters of credit are issued to accommodate the financing needs of state street 2019s clients and to provide credit enhancements to special purpose entities .
loan commitments are agreements by state street to lend monies at a future date .
asset purchase agreements are commitments to purchase receivables or securities , subject to conditions established in the agreements , and at december 31 , 2001 , include $ 8.0 billion outstanding to special purpose entities .
standby letters of credit and letters of credit commit state street to make payments on behalf of clients and special purpose entities when certain specified events occur .
standby letters of credit outstanding to special purpose entities were $ 608 million at december 31 , 2001 .
these loan , asset purchase and letter of credit commitments are subject to the same credit policies and reviews as loans .
the amount and nature of collateral are obtained based upon management 2019s assessment of the credit risk .
approximately 89% ( 89 % ) of the loan commitments and asset purchase agreements expire within one year from the date of issue .
sincemany of the commitments are expected to expire or renewwithout being drawn , the total commitment amounts do not necessarily represent future cash requirements .
the following is a summary of the contractual amount of credit-related , off-balance sheet financial instruments at december 31: .

( dollars in millions ) | 2001 | 2000
indemnified securities on loan | $ 113047 | $ 101438
loan commitments | 12962 | 11367
asset purchase agreements | 10366 | 7112
standby letters of credit | 3918 | 4028
letters of credit | 164 | 218

state street corporation 53 .
```

---

## Item 17/25 — `hqa_FQ_0bb282d6`

- **source**: finqa / AON/2018/page_90.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the total benefits from 2017 to 2018 in millions

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(168, 173)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
( 3 ) refer to note 2 201csummary of significant accounting principles and practices 201d for further information .
13 .
employee benefitsp y defined contribution savings plans aon maintains defined contribution savings plans for the benefit of its employees .
the expense recognized for these plans is included in compensation and benefits in the consolidated statements of income .
the expense for the significant plans in the u.s. , u.k. , netherlands and canada is as follows ( in millions ) : .

years ended december 31 | 2018 | 2017 | 2016
u.s . | $ 98 | $ 105 | $ 121
u.k . | 45 | 43 | 43
netherlands and canada | 25 | 25 | 27
total | $ 168 | $ 173 | $ 191

pension and other postretirement benefits the company sponsors defined benefit pension and postretirement health and welfare plans that provide retirement , medical , and life insurance benefits .
the postretirement health care plans are contributory , with retiree contributions adjusted annually , and the aa life insurance and pension plans are generally noncontributory .
the significant u.s. , u.k. , netherlands and canadian pension plans are closed to new entrants. .
```

---

## Item 18/25 — `hqa_FQ_14d227e6`

- **source**: finqa / AAPL/2016/page_23.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the cumulative change in apple inc . stock between 2016 and 2011?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(213, const_100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
apple inc .
| 2016 form 10-k | 20 company stock performance the following graph shows a comparison of cumulative total shareholder return , calculated on a dividend reinvested basis , for the company , the s&p 500 index , the s&p information technology index and the dow jones u.s .
technology supersector index for the five years ended september 24 , 2016 .
the graph assumes $ 100 was invested in each of the company 2019s common stock , the s&p 500 index , the s&p information technology index and the dow jones u.s .
technology supersector index as of the market close on september 23 , 2011 .
note that historic stock price performance is not necessarily indicative of future stock price performance .
* $ 100 invested on 9/23/11 in stock or index , including reinvestment of dividends .
data points are the last day of each fiscal year for the company 2019s common stock and september 30th for indexes .
copyright a9 2016 s&p , a division of mcgraw hill financial .
all rights reserved .
copyright a9 2016 dow jones & co .
all rights reserved .
september september september september september september .

 | september2011 | september2012 | september2013 | september2014 | september2015 | september2016
apple inc . | $ 100 | $ 166 | $ 123 | $ 183 | $ 212 | $ 213
s&p 500 index | $ 100 | $ 130 | $ 155 | $ 186 | $ 185 | $ 213
s&p information technology index | $ 100 | $ 132 | $ 142 | $ 183 | $ 187 | $ 230
dow jones u.s . technology supersector index | $ 100 | $ 130 | $ 137 | $ 178 | $ 177 | $ 217

.
```

---

## Item 19/25 — `hqa_FQ_16a8661c`

- **source**: finqa / SLB/2011/page_56.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the net change in shares outstanding during 2011?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(1434, 1434)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
schlumberger limited and subsidiaries shares of common stock ( stated in millions ) issued in treasury shares outstanding .

 | issued | in treasury | shares outstanding
balance january 1 2009 | 1334 | -140 ( 140 ) | 1194
shares sold to optionees less shares exchanged | 2013 | 4 | 4
vesting of restricted stock | 2013 | 1 | 1
shares issued under employee stock purchase plan | 2013 | 4 | 4
stock repurchase program | 2013 | -8 ( 8 ) | -8 ( 8 )
balance december 31 2009 | 1334 | -139 ( 139 ) | 1195
acquisition of smith international inc . | 100 | 76 | 176
shares sold to optionees less shares exchanged | 2013 | 6 | 6
shares issued under employee stock purchase plan | 2013 | 3 | 3
stock repurchase program | 2013 | -27 ( 27 ) | -27 ( 27 )
issued on conversions of debentures | 2013 | 8 | 8
balance december 31 2010 | 1434 | -73 ( 73 ) | 1361
shares sold to optionees less shares exchanged | 2013 | 6 | 6
vesting of restricted stock | 2013 | 1 | 1
shares issued under employee stock purchase plan | 2013 | 3 | 3
stock repurchase program | 2013 | -37 ( 37 ) | -37 ( 37 )
balance december 31 2011 | 1434 | -100 ( 100 ) | 1334

see the notes to consolidated financial statements .
```

---

## Item 20/25 — `hqa_FQ_19f6d315`

- **source**: finqa / C/2018/page_179.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in the total incentive compensation from 2017 to 2018

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(2021, 2251), divide(#0, 2251)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
incentive compensation cost the following table shows components of compensation expense , relating to certain of the incentive compensation programs described above : in a0millions a0of a0dollars 2018 2017 2016 charges for estimated awards to retirement-eligible employees $ 669 $ 659 $ 555 amortization of deferred cash awards , deferred cash stock units and performance stock units 202 354 336 immediately vested stock award expense ( 1 ) 75 70 73 amortization of restricted and deferred stock awards ( 2 ) 435 474 509 .

in millions of dollars | 2018 | 2017 | 2016
charges for estimated awards to retirement-eligible employees | $ 669 | $ 659 | $ 555
amortization of deferred cash awards deferred cash stock units and performance stock units | 202 | 354 | 336
immediately vested stock award expense ( 1 ) | 75 | 70 | 73
amortization of restricted and deferred stock awards ( 2 ) | 435 | 474 | 509
other variable incentive compensation | 640 | 694 | 710
total | $ 2021 | $ 2251 | $ 2183

( 1 ) represents expense for immediately vested stock awards that generally were stock payments in lieu of cash compensation .
the expense is generally accrued as cash incentive compensation in the year prior to grant .
( 2 ) all periods include amortization expense for all unvested awards to non-retirement-eligible employees. .
```

---

## Item 21/25 — `hqa_FQ_1e05763b`

- **source**: finqa / CB/2008/page_217.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percentage change in the balance of outstanding options from 2005 to 2008?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(9923563, 12643761), divide(#0, 12643761)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
n o t e s t o c o n s o l i d a t e d f i n a n c i a l s t a t e m e n t s ( continued ) ace limited and subsidiaries the following table shows changes in the company 2019s stock options for the years ended december 31 , 2008 , 2007 , and number of options weighted average exercise price .

 | number of options | weightedaverageexercise price
options outstanding december 31 2005 | 12643761 | $ 36.53
granted | 1505215 | $ 56.29
exercised | -1982560 ( 1982560 ) | $ 33.69
forfeited | -413895 ( 413895 ) | $ 39.71
options outstanding december 31 2006 | 11752521 | $ 39.43
granted | 1549091 | $ 56.17
exercised | -1830004 ( 1830004 ) | $ 35.73
forfeited | -200793 ( 200793 ) | $ 51.66
options outstanding december 31 2007 | 11270815 | $ 42.12
granted | 1612507 | $ 60.17
exercised | -2650733 ( 2650733 ) | $ 36.25
forfeited | -309026 ( 309026 ) | $ 54.31
options outstanding december 31 2008 | 9923563 | $ 46.24

the weighted-average remaining contractual term was 5.8 years for the stock options outstanding and 4.6 years for the stock options exercisable at december 31 , 2008 .
the total intrinsic value was approximately $ 66 million for stock options out- standing and $ 81 million for stock options exercisable at december 31 , 2008 .
the weighted-average fair value for the stock options granted for the year ended december 31 , 2008 was $ 17.60 .
the total intrinsic value for stock options exercised dur- ing the years ended december 31 , 2008 , 2007 , and 2006 , was approximately $ 54 million , $ 44 million , and $ 43 million , respectively .
the amount of cash received during the year ended december 31 , 2008 , from the exercise of stock options was $ 97 million .
restricted stock the company 2019s 2004 ltip also provides for grants of restricted stock .
the company generally grants restricted stock with a 4-year vesting period , based on a graded vesting schedule .
the restricted stock is granted at market close price on the date of grant .
included in the company 2019s share-based compensation expense in the year ended december 31 , 2008 , is a portion of the cost related to the unvested restricted stock granted in the years 2004 to 2008. .
```

---

## Item 22/25 — `hqa_FQ_294c3620`

- **source**: finqa / AAPL/2015/page_24.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the s&p 500 index between 2010 and 2015?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(187, const_100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
table of contents company stock performance the following graph shows a comparison of cumulative total shareholder return , calculated on a dividend reinvested basis , for the company , the s&p 500 index , the s&p information technology index and the dow jones u.s .
technology supersector index for the five years ended september 26 , 2015 .
the graph assumes $ 100 was invested in each of the company 2019s common stock , the s&p 500 index , the s&p information technology index and the dow jones u.s .
technology supersector index as of the market close on september 24 , 2010 .
note that historic stock price performance is not necessarily indicative of future stock price performance .
* $ 100 invested on 9/25/10 in stock or index , including reinvestment of dividends .
data points are the last day of each fiscal year for the company 2019scommon stock and september 30th for indexes .
copyright a9 2015 s&p , a division of mcgraw hill financial .
all rights reserved .
copyright a9 2015 dow jones & co .
all rights reserved .
september september september september september september .

 | september 2010 | september 2011 | september 2012 | september 2013 | september 2014 | september 2015
apple inc . | $ 100 | $ 138 | $ 229 | $ 170 | $ 254 | $ 294
s&p 500 index | $ 100 | $ 101 | $ 132 | $ 157 | $ 188 | $ 187
s&p information technology index | $ 100 | $ 104 | $ 137 | $ 147 | $ 190 | $ 194
dow jones u.s . technology supersector index | $ 100 | $ 103 | $ 134 | $ 141 | $ 183 | $ 183

apple inc .
| 2015 form 10-k | 21 .
```

---

## Item 23/25 — `hqa_FQ_32685ea4`

- **source**: finqa / RE/2016/page_40.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the amount of pre-tax catastrophe losses from 2015 to 2016 in millions

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(301.2, 53.8)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
risks relating to our business fluctuations in the financial markets could result in investment losses .
prolonged and severe disruptions in the overall public debt and equity markets , such as occurred during 2008 , could result in significant realized and unrealized losses in our investment portfolio .
although financial markets have significantly improved since 2008 , they could deteriorate in the future .
there could also be disruption in individual market sectors , such as occurred in the energy sector in recent years .
such declines in the financial markets could result in significant realized and unrealized losses on investments and could have a material adverse impact on our results of operations , equity , business and insurer financial strength and debt ratings .
our results could be adversely affected by catastrophic events .
we are exposed to unpredictable catastrophic events , including weather-related and other natural catastrophes , as well as acts of terrorism .
any material reduction in our operating results caused by the occurrence of one or more catastrophes could inhibit our ability to pay dividends or to meet our interest and principal payment obligations .
by way of illustration , during the past five calendar years , pre-tax catastrophe losses , net of contract specific reinsurance but before cessions under corporate reinsurance programs , were as follows: .

calendar year: | pre-tax catastrophe losses
( dollars in millions ) | 
2016 | $ 301.2
2015 | 53.8
2014 | 56.3
2013 | 194.0
2012 | 410.0

our losses from future catastrophic events could exceed our projections .
we use projections of possible losses from future catastrophic events of varying types and magnitudes as a strategic underwriting tool .
we use these loss projections to estimate our potential catastrophe losses in certain geographic areas and decide on the placement of retrocessional coverage or other actions to limit the extent of potential losses in a given geographic area .
these loss projections are approximations , reliant on a mix of quantitative and qualitative processes , and actual losses may exceed the projections by a material amount , resulting in a material adverse effect on our financial condition and results of operations. .
```

---

## Item 24/25 — `hqa_FQ_35480d43`

- **source**: finqa / SLG/2011/page_58.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in ground leases between 2012 and 2013 in millions?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(33429, 33429)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
56 / 57 management 2019s discussion and analysis of financial condition and results of operations junior subordinate deferrable interest debentures in june 2005 , we issued $ 100.0 a0million of trust preferred securities , which are reflected on the balance sheet as junior subordinate deferrable interest debentures .
the proceeds were used to repay our revolving credit facility .
the $ 100.0 a0million of junior subordi- nate deferrable interest debentures have a 30-year term ending july 2035 .
they bear interest at a fixed rate of 5.61% ( 5.61 % ) for the first 10 years ending july 2015 .
thereafter , the rate will float at three month libor plus 1.25% ( 1.25 % ) .
the securities are redeemable at par .
restrictive covenants the terms of the 2011 revolving credit facility and certain of our senior unsecured notes include certain restrictions and covenants which may limit , among other things , our ability to pay dividends ( as discussed below ) , make certain types of investments , incur additional indebtedness , incur liens and enter into negative pledge agreements and the disposition of assets , and which require compliance with financial ratios including our minimum tangible net worth , a maximum ratio of total indebtedness to total asset value , a minimum ratio of ebitda to fixed charges and a maximum ratio of unsecured indebtedness to unencumbered asset value .
the dividend restriction referred to above provides that we will not during any time when we are in default , make distributions with respect to common stock or other equity interests , except to enable us to continue to qualify as a reit for federal income tax purposes .
as of december a031 , 2011 and 2010 , we were in compli- ance with all such covenants .
market rate risk we are exposed to changes in interest rates primarily from our floating rate borrowing arrangements .
we use interest rate deriv- ative instruments to manage exposure to interest rate changes .
a a0hypothetical 100 a0basis point increase in interest rates along the entire interest rate curve for 2011 and 2010 , would increase our annual interest cost by approximately $ 12.3 a0million and $ 11.0 a0mil- lion and would increase our share of joint venture annual interest cost by approximately $ 4.8 a0million and $ 6.7 a0million , respectively .
we recognize all derivatives on the balance sheet at fair value .
derivatives that are not hedges must be adjusted to fair value through income .
if a derivative is a hedge , depending on the nature of the hedge , changes in the fair value of the derivative will either be offset against the change in fair value of the hedged asset , liability , or firm commitment through earnings , or recognized in other comprehensive income until the hedged item is recognized in earnings .
the ineffective portion of a derivative 2019s change in fair value is recognized immediately in earnings .
approximately $ 4.8 a0billion of our long- term debt bore interest a0at fixed rates , and therefore the fair value of these instru- ments is affected by changes in the market interest rates .
the interest rate on our variable rate debt and joint venture debt as of december a031 , 2011 ranged from libor plus 150 a0basis points to libor plus 350 a0basis points .
contractual obligations combined aggregate principal maturities of mortgages and other loans payable , our 2011 revolving credit facility , senior unsecured notes ( net of discount ) , trust preferred securities , our share of joint venture debt , including as- of-right extension options , estimated interest expense ( based on weighted average interest rates for the quarter ) , and our obligations under our capital lease and ground leases , as of december a031 , 2011 are as follows ( in thousands ) : .

 | 2012 | 2013 | 2014 | 2015 | 2016 | thereafter | total
property mortgages | $ 52443 | $ 568649 | $ 647776 | $ 270382 | $ 556400 | $ 2278190 | $ 4373840
revolving credit facility | 2014 | 2014 | 2014 | 2014 | 350000 | 2014 | 350000
trust preferred securities | 2014 | 2014 | 2014 | 2014 | 2014 | 100000 | 100000
senior unsecured notes | 119423 | 2014 | 98578 | 657 | 274804 | 777194 | 1270656
capital lease | 1555 | 1555 | 1555 | 1592 | 1707 | 42351 | 50315
ground leases | 33429 | 33429 | 33429 | 33429 | 33533 | 615450 | 782699
estimated interest expense | 312672 | 309280 | 269286 | 244709 | 212328 | 470359 | 1818634
joint venture debt | 176457 | 93683 | 123983 | 102476 | 527814 | 800102 | 1824515
total | $ 695979 | $ 1006596 | $ 1174607 | $ 653245 | $ 1956586 | $ 5083646 | $ 10570659

.
```

---

## Item 25/25 — `hqa_FQ_37ff807a`

- **source**: finqa / CB/2008/page_243.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate of net amount from 2007 to 2008?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(13203, 12297), divide(#0, 12297)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
s c h e d u l e i v ( continued ) ace limited and subsidiaries s u p p l e m e n t a l i n f o r m a t i o n c o n c e r n i n g r e i n s u r a n c e premiums earned for the years ended december 31 , 2008 , 2007 , and 2006 ( in millions of u.s .
dollars ) direct amount ceded to companies assumed from other companies net amount percentage of amount assumed to .

for the years ended december 31 2008 2007 and 2006 ( in millions of u.s . dollars ) | direct amount | ceded to other companies | assumed from other companies | net amount | percentage of amount assumed to net
2008 | $ 16087 | $ 6144 | $ 3260 | $ 13203 | 25% ( 25 % )
2007 | $ 14673 | $ 5834 | $ 3458 | $ 12297 | 28% ( 28 % )
2006 | $ 13562 | $ 5198 | $ 3461 | $ 11825 | 29% ( 29 % )

.
```

---
