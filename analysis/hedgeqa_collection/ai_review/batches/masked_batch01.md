# Blind review batch `masked_batch01`

25 items. Family: `evidence_masked_insufficient`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_CFQ_1279a468_masked`

- **source**: convfinqa / Single_AOS/2016/page_19.pdf-2#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the a. o. smith corporation share price as of 12/31/16?

Question: and the change in price between 12/31/11 and this date?

**Original source question**: and the change in price between 12/31/11 and this date?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
the graph below shows a five-year comparison of the cumulative shareholder return on our common stock with the cumulative total return of the standard & poor 2019s ( s&p ) mid cap 400 index and the russell 1000 index , both of which are published indices .
comparison of five-year cumulative total return from december 31 , 2011 to december 31 , 2016 assumes $ 100 invested with reinvestment of dividends period indexed returns .

company/index | baseperiod 12/31/11 | baseperiod 12/31/12 | baseperiod 12/31/13 | baseperiod 12/31/14 | baseperiod 12/31/15 | 12/31/16
s&p mid cap 400 index | 100.0 | 117.9 | 157.4 | 172.8 | 169.0 | 204.1
russell 1000 index | 100.0 | 116.4 | 155.0 | 175.4 | 177.0 | 198.4

2011 2012 2013 2014 2015 2016 smith ( a o ) corp s&p midcap 400 index russell 1000 index .
```

---

## Item 2/25 — `hqa_CFQ_13c20530_masked`

- **source**: convfinqa / Double_UPS/2015/page_35.pdf#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the performance value of the ups class b common stock from 2010 to 2015?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
shareowner return performance graph the following performance graph and related information shall not be deemed 201csoliciting material 201d or to be 201cfiled 201d with the sec , nor shall such information be incorporated by reference into any future filing under the securities act of 1933 or securities exchange act of 1934 , each as amended , except to the extent that the company specifically incorporates such information by reference into such filing .
the following graph shows a five year comparison of cumulative total shareowners 2019 returns for our class b common stock , the standard & poor 2019s 500 index , and the dow jones transportation average .
the comparison of the total cumulative return on investment , which is the change in the quarterly stock price plus reinvested dividends for each of the quarterly periods , assumes that $ 100 was invested on december 31 , 2010 in the standard & poor 2019s 500 index , the dow jones transportation average , and our class b common stock. .

 | 12/31/2010 | 12/31/2011 | 12/31/2012 | 12/31/2013 | 12/31/2014 | 12/31/2015
standard & poor 2019s 500 index | $ 100.00 | $ 102.11 | $ 118.43 | $ 156.77 | $ 178.22 | $ 180.67
dow jones transportation average | $ 100.00 | $ 100.01 | $ 107.49 | $ 151.97 | $ 190.08 | $ 158.23

.
```

---

## Item 3/25 — `hqa_CFQ_1d1128f4_masked`

- **source**: convfinqa / Single_ETFC/2007/page_22.pdf-2#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the value of the common stock for e*trade financial corporation from 2004 to 2005?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
december 18 , 2007 , we issued an additional 23182197 shares of common stock to citadel .
the issuances were exempt from registration pursuant to section 4 ( 2 ) of the securities act of 1933 , and each purchaser has represented to us that it is an 201caccredited investor 201d as defined in regulation d promulgated under the securities act of 1933 , and that the common stock was being acquired for investment .
we did not engage in a general solicitation or advertising with regard to the issuances of the common stock and have not offered securities to the public in connection with the issuances .
see item 1 .
business 2014citadel investment .
performance graph the following performance graph shows the cumulative total return to a holder of the company 2019s common stock , assuming dividend reinvestment , compared with the cumulative total return , assuming dividend reinvestment , of the standard & poor 2019s ( 201cs&p 201d ) 500 and the s&p super cap diversified financials during the period from december 31 , 2002 through december 31 , 2007. .

 | 12/02 | 12/03 | 12/04 | 12/05 | 12/06 | 12/07
s&p 500 | 100.00 | 128.68 | 142.69 | 149.70 | 173.34 | 182.87
s&p super cap diversified financials | 100.00 | 139.29 | 156.28 | 170.89 | 211.13 | 176.62

2022 $ 100 invested on 12/31/02 in stock or index-including reinvestment of dividends .
fiscal year ending december 31 .
2022 copyright a9 2008 , standard & poor 2019s , a division of the mcgraw-hill companies , inc .
all rights reserved .
www.researchdatagroup.com/s&p.htm .
```

---

## Item 4/25 — `hqa_CFQ_3240be6a_masked`

- **source**: convfinqa / Single_JPM/2016/page_73.pdf-4#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the value of the kbw bank index in 2016?

Question: and what was the change in value of the stock from 2011 to 2016?

**Original source question**: and what was the change in value of the stock from 2011 to 2016?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

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
s&p financial index | 100.00 | 128.75 | 174.57 | 201.06 | 197.92 | 242.94
s&p 500 index | 100.00 | 115.99 | 153.55 | 174.55 | 176.95 | 198.10

december 31 , ( in dollars ) .
```

---

## Item 5/25 — `hqa_CFQ_378d381c_masked`

- **source**: convfinqa / Single_DISCA/2012/page_54.pdf-4#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in value of disca common stock from 2018, less a $100 initial investment?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
stock performance graph the following graph sets forth the cumulative total shareholder return on our series a common stock , series b common stock and series c common stock as compared with the cumulative total return of the companies listed in the standard and poor 2019s 500 stock index ( 201cs&p 500 index 201d ) and a peer group of companies comprised of cbs corporation class b common stock , news corporation class a common stock , scripps network interactive , inc. , time warner , inc. , viacom , inc .
class b common stock and the walt disney company .
the graph assumes $ 100 originally invested on september 18 , 2008 , the date upon which our common stock began trading , in each of our series a common stock , series b common stock and series c common stock , the s&p 500 index , and the stock of our peer group companies , including reinvestment of dividends , for the period september 18 , 2008 through december 31 , 2008 and the years ended december 31 , 2009 , 2010 , 2011 , and 2012 .
december 31 , december 31 , december 31 , december 31 , december 31 .

 | december 312008 | december 312009 | december 312010 | december 312011 | december 312012
discb | $ 78.53 | $ 162.82 | $ 225.95 | $ 217.56 | $ 327.11
disck | $ 83.69 | $ 165.75 | $ 229.31 | $ 235.63 | $ 365.63
s&p 500 | $ 74.86 | $ 92.42 | $ 104.24 | $ 104.23 | $ 118.21
peer group | $ 68.79 | $ 100.70 | $ 121.35 | $ 138.19 | $ 190.58

equity compensation plan information information regarding securities authorized for issuance under equity compensation plans will be set forth in our definitive proxy statement for our 2013 annual meeting of stockholders under the caption 201csecurities authorized for issuance under equity compensation plans , 201d which is incorporated herein by reference. .
```

---

## Item 6/25 — `hqa_CFQ_446ed3a5_masked`

- **source**: convfinqa / Single_AOS/2007/page_17.pdf-2#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the value of a o smith corp from 2002 to 2007?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
the graph below shows a five-year comparison of the cumulative shareholder return on the company's common stock with the cumulative total return of the s&p smallcap 600 index and the s&p 600 electrical equipment index , all of which are published indices .
comparison of five-year cumulative total return from december 31 , 2002 to december 31 , 2007 assumes $ 100 invested with reinvestment of dividends period indexed returns .

company/index | baseperiod 12/31/02 | baseperiod 12/31/03 | baseperiod 12/31/04 | baseperiod 12/31/05 | baseperiod 12/31/06 | 12/31/07
s&p smallcap 600 index | 100.00 | 138.79 | 170.22 | 183.30 | 211.01 | 210.39
s&p 600 electrical equipment | 100.00 | 126.12 | 152.18 | 169.07 | 228.83 | 253.33

12/31/02 12/31/03 12/31/04 12/31/05 12/31/06 12/31/07 smith ( a o ) corp s&p smallcap 600 index s&p 600 electrical equipment .
```

---

## Item 7/25 — `hqa_CFQ_4b27112b_masked`

- **source**: convfinqa / Double_JKHY/2016/page_25.pdf#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the performance value of the peer group stock from 2014 to 2016?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
22 2016 annual report performance graph the following chart presents a comparison for the five-year period ended june 30 , 2016 , of the market performance of the company 2019s common stock with the s&p 500 index and an index of peer companies selected by the company : comparison of 5 year cumulative total return among jack henry & associates , inc. , the s&p 500 index , and a peer group the following information depicts a line graph with the following values: .

 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016
jkhy | 100.00 | 116.62 | 161.33 | 206.53 | 228.24 | 312.11
s&p 500 | 100.00 | 105.45 | 127.17 | 158.46 | 170.22 | 177.02

this comparison assumes $ 100 was invested on june 30 , 2011 , and assumes reinvestments of dividends .
total returns are calculated according to market capitalization of peer group members at the beginning of each period .
peer companies selected are in the business of providing specialized computer software , hardware and related services to financial institutions and other businesses .
companies in the peer group are aci worldwide , inc. , bottomline technology , inc. , broadridge financial solutions , cardtronics , inc. , convergys corp. , corelogic , inc. , dst systems , inc. , euronet worldwide , inc. , fair isaac corp. , fidelity national information services , inc. , fiserv , inc. , global payments , inc. , moneygram international , inc. , ss&c technologies holdings , inc. , total systems services , inc. , tyler technologies , inc. , verifone systems , inc. , and wex , inc. .
heartland payment systems , inc .
was removed from the peer group as it merged with global payments , inc .
in april 2016. .
```

---

## Item 8/25 — `hqa_CFQ_64646a26_masked`

- **source**: convfinqa / Single_UPS/2010/page_33.pdf-4#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the performance value of the united parcel service inc . in 2010?

Question: and what was the change in this performance from 2005 to 2010?

**Original source question**: and what was the change in this performance from 2005 to 2010?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
shareowner return performance graph the following performance graph and related information shall not be deemed 201csoliciting material 201d or to be 201cfiled 201d with the securities and exchange commission , nor shall such information be incorporated by reference into any future filing under the securities act of 1933 or securities exchange act of 1934 , each as amended , except to the extent that the company specifically incorporates such information by reference into such filing .
the following graph shows a five year comparison of cumulative total shareowners 2019 returns for our class b common stock , the standard & poor 2019s 500 index , and the dow jones transportation average .
the comparison of the total cumulative return on investment , which is the change in the quarterly stock price plus reinvested dividends for each of the quarterly periods , assumes that $ 100 was invested on december 31 , 2005 in the standard & poor 2019s 500 index , the dow jones transportation average , and our class b common stock .
comparison of five year cumulative total return $ 40.00 $ 60.00 $ 80.00 $ 100.00 $ 120.00 $ 140.00 $ 160.00 201020092008200720062005 s&p 500 ups dj transport .

 | 12/31/05 | 12/31/06 | 12/31/07 | 12/31/08 | 12/31/09 | 12/31/10
standard & poor 2019s 500 index | $ 100.00 | $ 115.79 | $ 122.16 | $ 76.96 | $ 97.33 | $ 111.99
dow jones transportation average | $ 100.00 | $ 109.82 | $ 111.38 | $ 87.52 | $ 103.79 | $ 131.59

.
```

---

## Item 9/25 — `hqa_CFQ_66b29a53_masked`

- **source**: convfinqa / Single_PM/2017/page_25.pdf-2#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the pmi's share price from 2014 to 2015?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
performance graph the graph below compares the cumulative total shareholder return on pmi's common stock with the cumulative total return for the same period of pmi's peer group and the s&p 500 index .
the graph assumes the investment of $ 100 as of december 31 , 2012 , in pmi common stock ( at prices quoted on the new york stock exchange ) and each of the indices as of the market close and reinvestment of dividends on a quarterly basis .
date pmi pmi peer group ( 1 ) s&p 500 index .

date | pmi | pmi peer group ( 1 ) | s&p 500 index
december 31 2012 | $ 100.00 | $ 100.00 | $ 100.00
december 31 2013 | $ 108.50 | $ 122.80 | $ 132.40
december 31 2016 | $ 130.80 | $ 145.60 | $ 170.80
december 31 2017 | $ 156.80 | $ 172.70 | $ 208.10

( 1 ) the pmi peer group presented in this graph is the same as that used in the prior year , except reynolds american inc .
was removed following the completion of its acquisition by british american tobacco p.l.c .
on july 25 , 2017 .
the pmi peer group was established based on a review of four characteristics : global presence ; a focus on consumer products ; and net revenues and a market capitalization of a similar size to those of pmi .
the review also considered the primary international tobacco companies .
as a result of this review , the following companies constitute the pmi peer group : altria group , inc. , anheuser-busch inbev sa/nv , british american tobacco p.l.c. , the coca-cola company , colgate-palmolive co. , diageo plc , heineken n.v. , imperial brands plc , japan tobacco inc. , johnson & johnson , kimberly-clark corporation , the kraft-heinz company , mcdonald's corp. , mondel z international , inc. , nestl e9 s.a. , pepsico , inc. , the procter & gamble company , roche holding ag , and unilever nv and plc .
note : figures are rounded to the nearest $ 0.10. .
```

---

## Item 10/25 — `hqa_CFQ_6aedbd76_masked`

- **source**: convfinqa / Single_RE/2016/page_40.pdf-4#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in pre-tax catastrophe losses from 2015 to 2016?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

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
2014 | 56.3
2013 | 194.0
2012 | 410.0

our losses from future catastrophic events could exceed our projections .
we use projections of possible losses from future catastrophic events of varying types and magnitudes as a strategic underwriting tool .
we use these loss projections to estimate our potential catastrophe losses in certain geographic areas and decide on the placement of retrocessional coverage or other actions to limit the extent of potential losses in a given geographic area .
these loss projections are approximations , reliant on a mix of quantitative and qualitative processes , and actual losses may exceed the projections by a material amount , resulting in a material adverse effect on our financial condition and results of operations. .
```

---

## Item 11/25 — `hqa_CFQ_6e99706b_masked`

- **source**: convfinqa / Single_L/2016/page_62.pdf-1#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the change in the value of the s&p index from 2011 to 2016?

Question: what is the percent change?

**Original source question**: what is the percent change?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
item 5 .
market for the registrant 2019s common equity , related stockholder matters and issuer purchases of equity securities the following graph compares annual total return of our common stock , the standard & poor 2019s 500 composite stock index ( 201cs&p 500 index 201d ) and our peer group ( 201cloews peer group 201d ) for the five years ended december 31 , 2016 .
the graph assumes that the value of the investment in our common stock , the s&p 500 index and the loews peer group was $ 100 on december 31 , 2011 and that all dividends were reinvested. .

 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016

( a ) the loews peer group consists of the following companies that are industry competitors of our principal operating subsidiaries : chubb limited ( name change from ace limited after it acquired the chubb corporation on january 15 , 2016 ) , w.r .
berkley corporation , the chubb corporation ( included through january 15 , 2016 when it was acquired by ace limited ) , energy transfer partners l.p. , ensco plc , the hartford financial services group , inc. , kinder morgan energy partners , l.p .
( included through november 26 , 2014 when it was acquired by kinder morgan inc. ) , noble corporation , spectra energy corp , transocean ltd .
and the travelers companies , inc .
dividend information we have paid quarterly cash dividends in each year since 1967 .
regular dividends of $ 0.0625 per share of loews common stock were paid in each calendar quarter of 2016 and 2015. .
```

---

## Item 12/25 — `hqa_CFQ_782828a3_masked`

- **source**: convfinqa / Single_DISCA/2008/page_141.pdf-4#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the change in value of an investment in disca from sep 18 to dec 31, 2008?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
2 0 0 8 a n n u a l r e p o r t stock performance graph the following graph sets forth the performance of our series a common , series b common stock , and series c common stock for the period september 18 , 2008 through december 31 , 2008 as compared with the performance of the standard and poor 2019s 500 index and a peer group index which consists of the walt disney company , time warner inc. , cbs corporation class b common stock , viacom , inc .
class b common stock , news corporation class a common stock , and scripps network interactive , inc .
the graph assumes $ 100 originally invested on september 18 , 2006 and that all subsequent dividends were reinvested in additional shares .
september 18 , september 30 , december 31 , 2008 2008 2008 .

 | september 18 2008 | september 30 2008 | december 31 2008
discb | $ 100.00 | $ 105.54 | $ 78.53
disck | $ 100.00 | $ 88.50 | $ 83.69
s&p 500 | $ 100.00 | $ 96.54 | $ 74.86
peer group | $ 100.00 | $ 92.67 | $ 68.79

s&p 500 peer group .
```

---

## Item 13/25 — `hqa_CFQ_7897a7cc_masked`

- **source**: convfinqa / Double_AAPL/2011/page_24.pdf#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in price for apple inc. between 9/30/11 and 9/30/06?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
company stock performance the following graph shows a five-year comparison of cumulative total shareholder return , calculated on a dividend reinvested basis , for the company , the s&p 500 composite index , the s&p computer hardware index , and the dow jones u.s .
technology index .
technology index on september 30 , 2006 .
data points on the graph are annual .
note that historic stock price performance is not necessarily indicative of future stock price performance .
comparison of 5 year cumulative total return* among apple inc. , the s&p 500 index , the s&p computer hardware index and the dow jones us technology index sep-10sep-09sep-08sep-07sep-06 sep-11 apple inc .
fiscal year ending september 30 .
copyright a9 2011 s&p , a division of the mcgraw-hill companies inc .
all rights reserved .
copyright a9 2011 dow jones & co .
all rights reserved .
september 30 , september 30 , september 30 , september 30 , september 30 , september 30 .

 | september 30 2006 | september 30 2007 | september 30 2008 | september 30 2009 | september 30 2010 | september 30 2011

.
```

---

## Item 14/25 — `hqa_CFQ_7f731a74_masked`

- **source**: convfinqa / Single_AAL/2015/page_51.pdf-3#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in value of american airlines stock over the 4 year period?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
table of contents capital deployment program will be subject to market and economic conditions , applicable legal requirements and other relevant factors .
our capital deployment program does not obligate us to continue a dividend for any fixed period , and payment of dividends may be suspended at any time at our discretion .
stock performance graph the following stock performance graph and related information shall not be deemed 201csoliciting material 201d or 201cfiled 201d with the securities and exchange commission , nor shall such information be incorporated by reference into any future filings under the securities act of 1933 or the exchange act , each as amended , except to the extent that we specifically incorporate it by reference into such filing .
the following stock performance graph compares our cumulative total stockholder return on an annual basis on our common stock with the cumulative total return on the standard and poor 2019s 500 stock index and the amex airline index from december 9 , 2013 ( the first trading day of aag common stock ) through december 31 , 2015 .
the stock performance shown on the graph below represents historical stock performance and is not necessarily indicative of future stock price performance. .

 | 12/9/2013 | 12/31/2013 | 12/31/2014 | 12/31/2015

purchases of equity securities by the issuer and affiliated purchasers since july 2014 , our board of directors has approved several share repurchase programs aggregating $ 7.0 billion of authority of which , as of december 31 , 2015 , $ 2.4 billion remained unused under repurchase programs .
```

---

## Item 15/25 — `hqa_CFQ_893fb41a_masked`

- **source**: convfinqa / Single_VLO/2016/page_23.pdf-3#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the net change in shares purchased as part of publicly announced plans from nov 2016 to dec 2016?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
table of contents the following table discloses purchases of shares of our common stock made by us or on our behalf during the fourth quarter of 2016 .
period total number of shares purchased average price paid per share total number of shares not purchased as part of publicly announced plans or programs ( a ) total number of shares purchased as part of publicly announced plans or programs approximate dollar value of shares that may yet be purchased under the plans or programs ( b ) .

period | total numberof sharespurchased | averageprice paidper share | total number ofshares notpurchased as part ofpublicly announcedplans or programs ( a ) | total number ofshares purchased aspart of publiclyannounced plans orprograms | approximate dollarvalue of shares thatmay yet be purchasedunder the plans orprograms ( b )
october 2016 | 433272 | $ 52.69 | 50337 | 382935 | $ 2.7 billion
total | 2660485 | $ 62.95 | 299374 | 2361111 | $ 2.5 billion

( a ) the shares reported in this column represent purchases settled in the fourth quarter of 2016 relating to ( i ) our purchases of shares in open-market transactions to meet our obligations under stock-based compensation plans , and ( ii ) our purchases of shares from our employees and non-employee directors in connection with the exercise of stock options , the vesting of restricted stock , and other stock compensation transactions in accordance with the terms of our stock-based compensation plans .
( b ) on july 13 , 2015 , we announced that our board of directors authorized our purchase of up to $ 2.5 billion of our outstanding common stock .
this authorization has no expiration date .
as of december 31 , 2016 , the approximate dollar value of shares that may yet be purchased under the 2015 authorization is $ 40 million .
on september 21 , 2016 , we announced that our board of directors authorized our purchase of up to an additional $ 2.5 billion of our outstanding common stock with no expiration date .
as of december 31 , 2016 , no purchases have been made under the 2016 authorization. .
```

---

## Item 16/25 — `hqa_CFQ_ad675ca7_masked`

- **source**: convfinqa / Single_VTR/2007/page_48.pdf-1#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the difference between the share price of ventas between 12/31/02 and 12/31/03?

Question: and the growth rate during this time?

**Original source question**: and the growth rate during this time?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
stock performance graph the following performance graph compares the cumulative total return ( including dividends ) to the holders of our common stock from december 31 , 2002 through december 31 , 2007 , with the cumulative total returns of the nyse composite index , the ftse nareit composite reit index ( the 201call reit index 201d ) , the ftse nareit healthcare equity reit index ( the 201chealthcare reit index 201d ) and the russell 1000 index over the same period .
the comparison assumes $ 100 was invested on december 31 , 2002 in our common stock and in each of the foregoing indices and assumes reinvestment of dividends , as applicable .
we have included the nyse composite index in the performance graph because our common stock is listed on the nyse .
we have included the other indices because we believe that they are either most representative of the industry in which we compete , or otherwise provide a fair basis for comparison with ventas , and are therefore particularly relevant to an assessment of our performance .
the figures in the table below are rounded to the nearest dollar. .

 | 12/31/2002 | 12/31/2003 | 12/31/2004 | 12/31/2005 | 12/31/2006 | 12/31/2007
nyse composite index | $ 100 | $ 132 | $ 151 | $ 166 | $ 200 | $ 217
all reit index | $ 100 | $ 138 | $ 181 | $ 196 | $ 262 | $ 215
healthcare reit index | $ 100 | $ 154 | $ 186 | $ 189 | $ 273 | $ 279
russell 1000 index | $ 100 | $ 130 | $ 145 | $ 154 | $ 178 | $ 188

ventas nyse composite index all reit index healthcare reit index russell 1000 index .
```

---

## Item 17/25 — `hqa_CFQ_b7e2687e_masked`

- **source**: convfinqa / Single_UNP/2009/page_38.pdf-4#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what is the net change in value of cash provided by operating activities from 2007 to 2008?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
have access to liquidity by issuing bonds to public or private investors based on our assessment of the current condition of the credit markets .
at december 31 , 2009 , we had a working capital surplus of approximately $ 1.0 billion , which reflects our decision to maintain additional cash reserves to enhance liquidity in response to difficult economic conditions .
at december 31 , 2008 , we had a working capital deficit of approximately $ 100 million .
historically , we have had a working capital deficit , which is common in our industry and does not indicate a lack of liquidity .
we maintain adequate resources and , when necessary , have access to capital to meet any daily and short-term cash requirements , and we have sufficient financial capacity to satisfy our current liabilities .
cash flows millions of dollars 2009 2008 2007 .

millions of dollars | 2009 | 2008 | 2007
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

## Item 18/25 — `hqa_CFQ_dea5f1e8_masked`

- **source**: convfinqa / Single_JPM/2015/page_77.pdf-5#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what is the change in value of the s&p from 2010 to 2015?

Question: assuming an initial investment of $100, what was the percent change?

**Original source question**: assuming an initial investment of $100, what was the percent change?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

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

december 31 , ( in dollars ) .
```

---

## Item 19/25 — `hqa_CFQ_eaadc3af_masked`

- **source**: convfinqa / Single_RSG/2010/page_135.pdf-2#turn0
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: what was the change in the weighted-average estimated fair values of stock options granted from 2009 to 2010?

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

 | 2010 | 2009 | 2008
expected volatility | 28.6% ( 28.6 % ) | 28.7% ( 28.7 % ) | 27.3% ( 27.3 % )
risk-free interest rate | 2.4% ( 2.4 % ) | 1.4% ( 1.4 % ) | 1.7% ( 1.7 % )
dividend yield | 2.9% ( 2.9 % ) | 3.1% ( 3.1 % ) | 2.9% ( 2.9 % )
expected life ( in years ) | 4.3 | 4.2 | 4.2
contractual life ( in years ) | 7 | 7 | 7
expected forfeiture rate | 3.0% ( 3.0 % ) | 3.0% ( 3.0 % ) | 3.0% ( 3.0 % )

republic services , inc .
notes to consolidated financial statements , continued .
```

---

## Item 20/25 — `hqa_CFQ_f9c627e5_masked`

- **source**: convfinqa / Single_BKNG/2017/page_35.pdf-1#turn1
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Conversation so far:
Q1: what was the price of booking holdings inc. in 2017?

Question: and the change in price between this time and the original investment?

**Original source question**: and the change in price between this time and the original investment?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
measurement point december 31 booking holdings nasdaq composite index s&p 500 rdg internet composite .

measurement pointdecember 31 | booking holdings inc . | nasdaqcomposite index | s&p 500index | rdg internetcomposite
2012 | 100.00 | 100.00 | 100.00 | 100.00
2013 | 187.37 | 141.63 | 132.39 | 163.02
2014 | 183.79 | 162.09 | 150.51 | 158.81
2015 | 205.51 | 173.33 | 152.59 | 224.05
2016 | 236.31 | 187.19 | 170.84 | 235.33

sales of unregistered securities between october 1 , 2017 and december 31 , 2017 , we issued 103343 shares of our common stock in connection with the conversion of $ 196.1 million principal amount of our 1.0% ( 1.0 % ) convertible senior notes due 2018 .
the conversions were effected in accordance with the indenture , which provides that the principal amount of converted notes be paid in cash and the conversion premium be paid in cash and/or shares of common stock at our election .
in each case , we chose to pay the conversion premium in shares of common stock ( fractional shares are paid in cash ) .
the issuances of the shares were not registered under the securities act of 1933 , as amended ( the "act" ) pursuant to section 3 ( a ) ( 9 ) of the act. .
```

---

## Item 21/25 — `hqa_FB_1858a6da_masked`

- **source**: financebench / financebench_id_00591
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Adobe have an improving Free cashflow conversion as of FY2022?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
ADOBE INC.
 CONSOLIDATED STATEMENTS OF CASH FLOWS
(In millions)
 
Years Ended
 
December 2,
2022
December 3,
2021
November 27,
2020
Cash flows from operating activities:
 
 
Net income
$ 
$ 
$ 
5,260 
Adjustments to reconcile net income to net cash provided by operating activities:
Depreciation, amortization and accretion
 
856 
 
788 
 
757 
Stock-based compensation
 
1,440 
 
1,069 
 
909 
Reduction of operating lease right-of-use assets
 
83 
 
73 
 
87 
Deferred income taxes
 
328 
 
183 
 
(1,501) 
Unrealized losses (gains) on investments, net
 
29 
 
(4) 
(11) 
Other non-cash items
 
10 
 
7 
 
40 
Changes in operating assets and liabilities, net of acquired assets and 
 assumed liabilities:
Trade receivables, net
 
(198) 
(430) 
106 
Prepaid expenses and other assets
 
(94) 
(475) 
(288) 
Trade payables
 
66 
 
(20) 
96 
Accrued expenses and other liabilities
 
7 
 
162 
 
86 
Income taxes payable
 
19 
 
2 
 
(72) 
Deferred revenue
 
536 
 
1,053 
 
258 
Net cash provided by operating activities
 
 
 
5,727 
Cash flows from investing activities:
 
 
Purchases of short-term investments
 
(909) 
(1,533) 
(1,071) 
Maturities of short-term investments
 
683 
 
877 
 
915 
Proceeds from sales of short-term investments
 
270 
 
191 
 
167 
Acquisitions, net of cash acquired
 
(126) 
(2,682) 
 
Purchases of property and equipment
 
(442) 
(348) 
(419) 
Purchases of long-term investments, intangibles and other assets
 
(46) 
(42) 
(15) 
Proceeds from sales of long-term investments and other assets
 
 
 
 
 
9 
Net cash used for investing activities
 
(570) 
(3,537) 
(414)
```

---

## Item 22/25 — `hqa_FB_1da93057_masked`

- **source**: financebench / financebench_id_00302
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Did Pfizer grow its PPNE between FY20 and FY21?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
As of December 31,
(MILLIONS, EXCEPT PER COMMON SHARE DATA)
2021
2020
Assets
Cash and cash equivalents
$
1,944 
$
1,786 
Short-term investments
29,125 
10,437 
Trade accounts receivable, less allowance for doubtful accounts: 2021$492; 2020$508
11,479 
7,913 
Inventories
9,059 
8,020 
Current tax assets
4,266 
3,264 
Other current assets
3,820 
3,646 
Total current assets
59,693 
35,067 
Equity-method investments
16,472 
16,856 
Long-term investments
5,054 
3,406 
Property, plant and equipment
```

---

## Item 23/25 — `hqa_FB_27095e41_masked`

- **source**: financebench / financebench_id_00080
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does Paypal have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
PayPal Holdings, Inc.
CONSOLIDATED BALANCE SHEETS
 
As of December 31,
2022
2021
 
(In millions, except par value)
ASSETS
Current assets:
Cash and cash equivalents
$
7,776 
$
5,197 
Short-term investments
3,092 
4,303 
Accounts receivable, net
800 
Loans and interest receivable, net of allowances of $598 and $491 as of December 31, 2022 and 2021,
respectively
4,846 
Funds receivable and customer accounts
36,141 
Prepaid expenses and other current assets
1,287 
Total current assets
57,517 
52,574 
Long-term investments
5,018 
6,797 
Property and equipment, net
1,730 
1,909 
Goodwill
11,209 
11,454 
Intangible assets, net
788 
1,332 
Other assets
2,455 
1,737 
Total assets
$
78,717 
$
75,803 
LIABILITIES AND EQUITY
Current liabilities:
Accounts payable
$
126 
$
197 
Funds payable and amounts due to customers
40,107 
38,841 
Accrued expenses and other current liabilities
4,055 
3,755 
Income taxes payable
813 
236 
Total current liabilities
45,101 
43,029 
Deferred tax liability and other long-term liabilities
2,925 
2,998 
Long-term debt
10,417 
8,049 
Total liabilities
58,443 
54,076 
Commitments and contingencies (Note 13)
Equity:
Common stock, $0.0001 par value; 4,000 shares authorized; 1,136 and 1,168 shares outstanding as of
December 31, 2022 and 2021, respectively
 
 
Preferred stock, $0.0001 par value; 100 shares authorized, unissued
 
 
Treasury stock at cost, 173 and 132 shares as of December 31, 2022 and 2021, respectively
(16,079)
(11,880)
Additional paid-in-capital
18,327 
17,208 
Retained earnings
18,954 
16,535 
Accumulated other comprehensive income (loss)
(928)
(136)
Total equity
20,274 
21,727 
Total liabilities and equity
$
78,717 
$
75,803 
The accompanying notes are an integral part of these consolidated financial statements.
6
```

---

## Item 24/25 — `hqa_FB_2efc769e_masked`

- **source**: financebench / financebench_id_00070
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Does American Water Works have positive working capital based on FY2022 data? If working capital is not a useful or relevant metric for this company, then please state that and explain why.

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
American Water Works Company, Inc. and Subsidiary Companies
Consolidated Balance Sheets
(In millions, except share and per share data)
December 31, 2022
December 31, 2021
ASSETS
Property, plant and equipment
$
29,736 
$
27,413 
Accumulated depreciation
(6,513)
(6,329)
Property, plant and equipment, net
23,223 
21,084 
Current assets:
 
 
Cash and cash equivalents
85 
116 
Restricted funds
32 
20 
Accounts receivable, net of allowance for uncollectible accounts of $60 and $75, respectively
271 
Income tax receivable
4 
Unbilled revenues
248 
Materials and supplies
98 
57 
Assets held for sale
 
683 
Other
155 
Total current assets
1,250 
1,554

American Water Works Company, Inc. and Subsidiary Companies
Consolidated Balance Sheets
(In millions, except share and per share data)
December 31, 2022
December 31, 2021
CAPITALIZATION AND LIABILITIES
Capitalization:
 
 
Common stock ($0.01 par value; 500,000,000 shares authorized; 187,200,539 and 186,880,413 shares
issued, respectively)
$
2 
$
2 
Paid-in-capital
6,824 
6,781 
Retained earnings
1,267 
925 
Accumulated other comprehensive loss
(23)
(45)
Treasury stock, at cost (5,342,477 and 5,269,324 shares, respectively)
(377)
(365)
Total common shareholders' equity
7,693 
7,298 
Long-term debt
10,926 
10,341 
Redeemable preferred stock at redemption value
3 
3 
Total long-term debt
10,929 
10,344 
Total capitalization
18,622 
17,642 
Current liabilities:
 
 
Short-term debt
1,175 
584 
Current portion of long-term debt
281 
57 
Accounts payable
254 
235 
Accrued liabilities
706 
701 
Accrued taxes
49 
176 
Accrued interest
91 
88 
Liabilities related to assets held for sale
 
83 
Other
255 
217 
Total current liabilities
2,811 
2,141
```

---

## Item 25/25 — `hqa_FB_435b88c4_masked`

- **source**: financebench / financebench_id_00566
- **transformation_type**: `evidence_masked_insufficient`
- **answer_type**: `yes_no`
- **answer_space**: ['yes', 'no', 'insufficient_data']
- **noncommit_labels**: ['insufficient_data']

**Question**: Has Verizon increased its debt on balance sheet between 2022 and the 2021 fiscal period?

**Derivation / note**: This item is a controlled-insufficient variant: some evidence rows were removed from the source document. You are NOT told which rows or which figures. Decide from the evidence below whether the question can still be answered.

**Oracle evidence**:

```
At December 31,
Maturities 
Interest 
Rates %
2022
2021 
Verizon Communications
< 5 Years
0.75 - 5.82
$ 
23,929 
$ 
18,406 
5-10 Years
1.50 - 7.88
42,637 
43,225 
> 10 Years
1.13 - 8.95
60,134 
73,520 
< 5 Years
Floating
(1) 
2,992 
4,086 
5-10 Years
Floating
(1) 
3,029 
824 
Alltel Corporation
5-10 Years
6.80 - 7.88
94 
38 
> 10 Years
N/A
N/A 
58 
Operating telephone company subsidiariesdebentures
< 5 Years
N/A
N/A 
141 
5-10 Years
6.00 - 8.75
475 
375 
> 10 Years
5.13 - 7.38
139 
250 
Other subsidiariesasset-backed debt
< 5 Years
0.41 - 5.72
9,767 
9,620 
< 5 Years
Floating
(2) 
10,271 
4,610 
Finance lease obligations (average rate of 2.5% and 2.2% in 
2022 and 2021, respectively)
1,732 
1,325 
Unamortized discount, net of premium
(4,039) 
(4,922) 
Unamortized debt issuance costs
(671) 
(688) 
Total long-term debt, including current maturities
150,489 
Less long-term debt maturing within one year
9,813 
7,443 
Total long-term debt
$ 
140,676 
$ 
143,425 
Long-term debt maturing within one year
$ 
9,813 
$ 
7,443 
Add commercial paper
150 
 
Debt maturing within one year
9,963 
7,443 
Add long-term debt
140,676 
143,425 
Total debt
$ 
$
```

---
