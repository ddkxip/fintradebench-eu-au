# Blind review batch `directional_batch03`

25 items. Family: `numeric_to_directional`.

Follow `AI_REVIEW_PROMPT.md`. Output one JSON object per item, JSONL only, no prose outside the JSON.

---

## Item 1/25 — `hqa_FQ_38d63fd6`

- **source**: finqa / GIS/2019/page_53.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the change in fair value of foreign currency instruments from 2018 to 2019?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(16.8, 21.3)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the table below presents the estimated maximum potential var arising from a one-day loss in fair value for our interest rate , foreign currency , commodity , and equity market-risk-sensitive instruments outstanding as of may 26 , 2019 and may 27 , 2018 , and the average fair value impact during the year ended may 26 , 2019. .

in millions | fair value impact may 26 2019 | fair value impact averageduringfiscal 2019 | fair value impact may 27 2018
interest rate instruments | $ 74.4 | $ 46.1 | $ 33.2
foreign currency instruments | 16.8 | 19.0 | 21.3
commodity instruments | 4.1 | 2.5 | 1.9
equity instruments | 2.3 | 2.2 | 2.0

.
```

---

## Item 2/25 — `hqa_FQ_3bd14ae7`

- **source**: finqa / ETR/2008/page_313.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percent change in net revenue between 2007 and 2008?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(959.2, 991.1), divide(#0, 991.1)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy louisiana , llc management's financial discussion and analysis net revenue 2008 compared to 2007 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges .
following is an analysis of the change in net revenue comparing 2008 to 2007 .
amount ( in millions ) .

 | amount ( in millions )
2007 net revenue | $ 991.1
retail electric price | -17.1 ( 17.1 )
purchased power capacity | -12.0 ( 12.0 )
net wholesale revenue | -7.4 ( 7.4 )
other | 4.6
2008 net revenue | $ 959.2

the retail electric price variance is primarily due to the cessation of the interim storm recovery through the formula rate plan upon the act 55 financing of storm costs and a credit passed on to customers as a result of the act 55 storm cost financing , partially offset by increases in the formula rate plan effective october 2007 .
refer to "hurricane rita and hurricane katrina" and "state and local rate regulation" below for a discussion of the interim recovery of storm costs , the act 55 storm cost financing , and the formula rate plan filing .
the purchased power capacity variance is due to the amortization of deferred capacity costs effective september 2007 as a result of the formula rate plan filing in may 2007 .
purchased power capacity costs are offset in base revenues due to a base rate increase implemented to recover incremental deferred and ongoing purchased power capacity charges .
see "state and local rate regulation" below for a discussion of the formula rate plan filing .
the net wholesale revenue variance is primarily due to provisions recorded for potential rate refunds related to the treatment of interruptible load in pricing entergy system affiliate sales .
gross operating revenue and , fuel and purchased power expenses gross operating revenues increased primarily due to an increase of $ 364.7 million in fuel cost recovery revenues due to higher fuel rates offset by decreased usage .
the increase was partially offset by a decrease of $ 56.8 million in gross wholesale revenue due to a decrease in system agreement rough production cost equalization credits .
fuel and purchased power expenses increased primarily due to increases in the average market prices of natural gas and purchased power , partially offset by a decrease in the recovery from customers of deferred fuel costs. .
```

---

## Item 3/25 — `hqa_FQ_3e5f5d64`

- **source**: finqa / ADBE/2014/page_47.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: from the years 2014-2013 to 2013-2012 , what was the change in percentage points of depreciation expense?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(3, 3)' Derive the direction yourself; check the operand order before trusting it.

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

## Item 4/25 — `hqa_FQ_46ab258b`

- **source**: finqa / SYY/2006/page_26.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in percentage sales to restaurants from 2004 to 2005?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(64%, 64%)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
customers and products the foodservice industry consists of two major customer types 2014 2018 2018traditional 2019 2019 and 2018 2018chain restaurant . 2019 2019 traditional foodservice customers include restaurants , hospitals , schools , hotels and industrial caterers .
sysco 2019s chain restaurant customers include regional and national hamburger , sandwich , pizza , chicken , steak and other chain operations .
services to the company 2019s traditional foodservice and chain restaurant customers are supported by similar physical facilities , vehicles , material handling equipment and techniques , and administrative and operating staffs .
products distributed by the company include a full line of frozen foods , such as meats , fully prepared entrees , fruits , vegetables and desserts ; a full line of canned and dry foods ; fresh meats ; imported specialties ; and fresh produce .
the company also supplies a wide variety of non-food items , including : paper products such as disposable napkins , plates and cups ; tableware such as china and silverware ; cookware such as pots , pans and utensils ; restaurant and kitchen equipment and supplies ; and cleaning supplies .
sysco 2019s operating companies distribute nationally-branded merchandise , as well as products packaged under sysco 2019s private brands .
the company believes that prompt and accurate delivery of orders , close contact with customers and the ability to provide a full array of products and services to assist customers in their foodservice operations are of primary importance in the marketing and distribution of products to traditional customers .
sysco 2019s operating companies offer daily delivery to certain customer locations and have the capability of delivering special orders on short notice .
through the more than 13900 sales and marketing representatives and support staff of sysco and its operating companies , sysco stays informed of the needs of its customers and acquaints them with new products and services .
sysco 2019s operating companies also provide ancillary services relating to foodservice distribution , such as providing customers with product usage reports and other data , menu-planning advice , food safety training and assistance in inventory control , as well as access to various third party services designed to add value to our customers 2019 businesses .
no single customer accounted for 10% ( 10 % ) or more of sysco 2019s total sales for its fiscal year ended july 1 , 2006 .
sysco 2019s sales to chain restaurant customers consist of a variety of food products .
the company believes that consistent product quality and timely and accurate service are important factors in the selection of a chain restaurant supplier .
one chain restaurant customer ( wendy 2019s international , inc. ) accounted for 5% ( 5 % ) of sysco 2019s sales for its fiscal year ended july 1 , 2006 .
although this customer represents approximately 37% ( 37 % ) of the sygma segment sales , the company does not believe that the loss of this customer would have a material adverse effect on sysco as a whole .
based upon available information , the company estimates that sales by type of customer during the past three fiscal years were as follows: .

type of customer | 2006 | 2005 | 2004
restaurants | 63% ( 63 % ) | 64% ( 64 % ) | 64% ( 64 % )
hospitals and nursing homes | 10 | 10 | 10
schools and colleges | 5 | 5 | 5
hotels and motels | 6 | 6 | 6
other | 16 | 15 | 15
totals | 100% ( 100 % ) | 100% ( 100 % ) | 100% ( 100 % )

restaurants **************************************************************** 63% ( 63 % ) 64% ( 64 % ) 64% ( 64 % ) hospitals and nursing homes *************************************************** 10 10 10 schools and colleges ********************************************************* 5 5 5 hotels and motels *********************************************************** 6 6 6 other********************************************************************* 16 15 15 totals ****************************************************************** 100% ( 100 % ) 100% ( 100 % ) 100% ( 100 % ) sources of supply sysco purchases from thousands of suppliers , none of which individually accounts for more than 10% ( 10 % ) of the company 2019s purchases .
these suppliers consist generally of large corporations selling brand name and private label merchandise and independent regional brand and private label processors and packers .
generally , purchasing is carried out through centrally developed purchasing programs and direct purchasing programs established by the company 2019s various operating companies .
the company continually develops relationships with suppliers but has no material long-term purchase commitments with any supplier .
in the second quarter of fiscal 2002 , sysco began a project to restructure its supply chain ( national supply chain project ) .
this project is intended to increase profitability by lowering aggregate inventory levels , operating costs , and future facility expansion needs at sysco 2019s broadline operating companies while providing greater value to our suppliers and customers .
%%transmsg*** transmitting job : h39408 pcn : 004000000 *** %%pcmsg|2 |00010|yes|no|09/06/2006 17:07|0|1|page is valid , no graphics -- color : n| .
```

---

## Item 5/25 — `hqa_FQ_4b4abc53`

- **source**: finqa / PKG/2005/page_73.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in total lease expense , including base rent on all leases and executory costs , such as insurance , taxes , and maintenance from 2004 to 2005?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(35.8, 33.0), divide(#0, 33.0)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
packaging corporation of america notes to consolidated financial statements ( continued ) december 31 , 2005 9 .
shareholders 2019 equity ( continued ) stockholder received proceeds , net of the underwriting discount , of $ 20.69 per share .
the company did not sell any shares in , or receive any proceeds from , the secondary offering .
concurrent with the closing of the secondary offering on december 21 , 2005 , the company entered into a common stock repurchase agreement with pca holdings llc .
pursuant to the repurchase agreement , the company purchased 4500000 shares of common stock directly from pca holdings llc at the initial price to the public net of the underwriting discount or $ 20.69 per share , the same net price per share received by pca holdings llc in the secondary offering .
these shares were retired on december 21 , 2005 .
10 .
commitments and contingencies capital commitments the company had authorized capital expenditures of approximately $ 33.1 million and $ 55.2 million as of december 31 , 2005 and 2004 , respectively , in connection with the expansion and replacement of existing facilities and equipment .
operating leases pca leases space for certain of its facilities and cutting rights to approximately 108000 acres of timberland under long-term leases .
the company also leases equipment , primarily vehicles and rolling stock , and other assets under long-term leases of a duration generally of three years .
the minimum lease payments under non-cancelable operating leases with lease terms in excess of one year are as follows : ( in thousands ) .

2006 | $ 24569
2007 | 21086
2008 | 14716
2009 | 9801
2010 | 6670
thereafter | 37130
total | $ 113972

capital lease obligations were not significant to the accompanying financial statements .
total lease expense , including base rent on all leases and executory costs , such as insurance , taxes , and maintenance , for the years ended december 31 , 2005 , 2004 and 2003 was $ 35.8 million , $ 33.0 million and $ 31.6 million , respectively .
these costs are included in cost of goods sold and selling and administrative expenses. .
```

---

## Item 6/25 — `hqa_FQ_4f19e5e1`

- **source**: finqa / ADI/2010/page_82.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percentage change in the total expense related to the defined contribution plan for u.s employees in 2010?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(20.5, 21.5), divide(#0, 21.5)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the following is a schedule of future minimum rental payments required under long-term operating leases at october 30 , 2010 : fiscal years operating leases .

fiscal years | operating leases
2011 | $ 21871
2012 | 12322
2013 | 9078
2014 | 6381
2015 | 5422
later years | 30655
total | $ 85729

12 .
commitments and contingencies from time to time in the ordinary course of the company 2019s business , various claims , charges and litigation are asserted or commenced against the company arising from , or related to , contractual matters , patents , trademarks , personal injury , environmental matters , product liability , insurance coverage and personnel and employment disputes .
as to such claims and litigation , the company can give no assurance that it will prevail .
the company does not believe that any current legal matters will have a material adverse effect on the company 2019s financial position , results of operations or cash flows .
13 .
retirement plans the company and its subsidiaries have various savings and retirement plans covering substantially all employees .
the company maintains a defined contribution plan for the benefit of its eligible u.s .
employees .
this plan provides for company contributions of up to 5% ( 5 % ) of each participant 2019s total eligible compensation .
in addition , the company contributes an amount equal to each participant 2019s pre-tax contribution , if any , up to a maximum of 3% ( 3 % ) of each participant 2019s total eligible compensation .
the total expense related to the defined contribution plan for u.s .
employees was $ 20.5 million in fiscal 2010 , $ 21.5 million in fiscal 2009 and $ 22.6 million in fiscal 2008 .
the company also has various defined benefit pension and other retirement plans for certain non-u.s .
employees that are consistent with local statutory requirements and practices .
the total expense related to the various defined benefit pension and other retirement plans for certain non-u.s .
employees was $ 11.7 million in fiscal 2010 , $ 10.9 million in fiscal 2009 and $ 13.9 million in fiscal 2008 .
during fiscal 2009 , the measurement date of the plan 2019s funded status was changed from september 30 to the company 2019s fiscal year end .
non-u.s .
plan disclosures the company 2019s funding policy for its foreign defined benefit pension plans is consistent with the local requirements of each country .
the plans 2019 assets consist primarily of u.s .
and non-u.s .
equity securities , bonds , property and cash .
the benefit obligations and related assets under these plans have been measured at october 30 , 2010 and october 31 , 2009 .
analog devices , inc .
notes to consolidated financial statements 2014 ( continued ) .
```

---

## Item 7/25 — `hqa_FQ_5708c95c`

- **source**: finqa / FIS/2006/page_88.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percentage change in estimated fair value of the cash flow hedges from 2005 to 2006?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(4.9, 5.2), divide(#0, 5.2)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
through the certegy merger , the company has an obligation to service $ 200 million ( aggregate principal amount ) of unsecured 4.75% ( 4.75 % ) fixed-rate notes due in 2008 .
the notes were recorded in purchase accounting at a discount of $ 5.7 million , which is being amortized over the term of the notes .
the notes accrue interest at a rate of 4.75% ( 4.75 % ) per year , payable semi-annually in arrears on each march 15 and september 15 .
on april 11 , 2005 , fis entered into interest rate swap agreements which have effectively fixed the interest rate at approximately 5.4% ( 5.4 % ) through april 2008 on $ 350 million of the term loan facilities ( or its replacement debt ) and at approximately 5.2% ( 5.2 % ) through april 2007 on an additional $ 350 million of the term loan .
the company has designated these interest rate swaps as cash flow hedges in accordance with sfas no .
133 .
the estimated fair value of the cash flow hedges results in an asset to the company of $ 4.9 million and $ 5.2 million , as of december 31 , 2006 and december 31 , 2005 , respectively , which is included in the accompanying consolidated balance sheets in other noncurrent assets and as a component of accumulated other comprehensive earnings , net of deferred taxes .
a portion of the amount included in accumulated other comprehensive earnings is reclassified into interest expense as a yield adjustment as interest payments are made on the term loan facilities .
the company 2019s existing cash flow hedges are highly effective and there is no current impact on earnings due to hedge ineffectiveness .
it is the policy of the company to execute such instruments with credit-worthy banks and not to enter into derivative financial instruments for speculative purposes .
principal maturities at december 31 , 2006 ( and at december 31 , 2006 after giving effect to the debt refinancing completed on january 18 , 2007 ) for the next five years and thereafter are as follows ( in thousands ) : december 31 , january 18 , 2007 refinancing .

 | december 31 2006 | january 18 2007 refinancing
2007 | $ 61661 | $ 96161
2008 | 257541 | 282041
2009 | 68129 | 145129
2010 | 33586 | 215586
2011 | 941875 | 165455
thereafter | 1646709 | 2105129
total | $ 3009501 | $ 3009501

fidelity national information services , inc .
and subsidiaries and affiliates consolidated and combined financial statements notes to consolidated and combined financial statements 2014 ( continued ) .
```

---

## Item 8/25 — `hqa_FQ_582b6cb3`

- **source**: finqa / AWK/2018/page_162.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in value for level 3 inputs during 2018?\\n

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(230, 278)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
asset category target allocation total quoted prices in active markets for identical assets ( level 1 ) significant observable inputs ( level 2 ) significant unobservable inputs .

 | level 3
balance as of january 1 2018 | $ 278
actual return on assets | -23 ( 23 )
purchases issuances and settlements net | -25 ( 25 )
balance as of december 31 2018 | $ 230

balance as of january 1 , 2017 .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
$ 140 actual return on assets .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
2 purchases , issuances and settlements , net .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
136 balance as of december 31 , 2017 .
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
.
$ 278 the company 2019s postretirement benefit plans have different levels of funded status and the assets are held under various trusts .
the investments and risk mitigation strategies for the plans are tailored specifically for each trust .
in setting new strategic asset mixes , consideration is given to the likelihood that the selected asset allocation will effectively fund the projected plan liabilities and meet the risk tolerance criteria of the company .
the company periodically updates the long-term , strategic asset allocations for these plans through asset liability studies and uses various analytics to determine the optimal asset allocation .
considerations include plan liability characteristics , liquidity needs , funding requirements , expected rates of return and the distribution of returns .
in 2012 , the company implemented a de-risking strategy for the american water pension plan after conducting an asset-liability study to reduce the volatility of the funded status of the plan .
as part of the de-risking strategy , the company revised the asset allocations to increase the matching characteristics of fixed- income assets relative to liabilities .
the fixed income portion of the portfolio was designed to match the bond- .
```

---

## Item 9/25 — `hqa_FQ_583bec62`

- **source**: finqa / C/2009/page_48.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in total operating expenses between 2007 and 2008?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(510, 1813), divide(#0, 1813)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
corporate/other corporate/other includes global staff functions ( includes finance , risk , human resources , legal and compliance ) and other corporate expense , global operations and technology ( o&t ) , residual corporate treasury and corporate items .
at december 31 , 2009 , this segment had approximately $ 230 billion of assets , consisting primarily of the company 2019s liquidity portfolio , including $ 110 billion of cash and cash equivalents. .

in millions of dollars | 2009 | 2008 | 2007
net interest revenue | $ -1663 ( 1663 ) | $ -2680 ( 2680 ) | $ -2008 ( 2008 )
non-interest revenue | -8893 ( 8893 ) | 422 | -302 ( 302 )
total revenues net of interest expense | $ -10556 ( 10556 ) | $ -2258 ( 2258 ) | $ -2310 ( 2310 )
total operating expenses | $ 1420 | $ 510 | $ 1813
provisions for loan losses and for benefits and claims | -1 ( 1 ) | 1 | -3 ( 3 )
( loss ) from continuing operations before taxes | $ -11975 ( 11975 ) | $ -2769 ( 2769 ) | $ -4120 ( 4120 )
income taxes ( benefits ) | -4369 ( 4369 ) | -587 ( 587 ) | -1446 ( 1446 )
( loss ) from continuing operations | $ -7606 ( 7606 ) | $ -2182 ( 2182 ) | $ -2674 ( 2674 )
income ( loss ) from discontinued operations net of taxes | -445 ( 445 ) | 4002 | 708
net income ( loss ) before attribution of noncontrolling interests | $ -8051 ( 8051 ) | $ 1820 | $ -1966 ( 1966 )
net income attributable to noncontrolling interests | 2014 | 2014 | 2
net income ( loss ) | $ -8051 ( 8051 ) | $ 1820 | $ -1968 ( 1968 )

2009 vs .
2008 revenues , net of interest expense declined , primarily due to the pretax loss on debt extinguishment related to the repayment of the $ 20 billion of tarp trust preferred securities and the pretax loss in connection with the exit from the loss-sharing agreement with the u.s .
government .
revenues also declined , due to the absence of the 2008 sale of citigroup global services limited recorded in o&t .
this was partially offset by a pretax gain related to the exchange offers , revenues and higher intersegment eliminations .
operating expenses increased , primarily due to intersegment eliminations and increases in compensation , partially offset by lower repositioning reserves .
2008 vs .
2007 revenues , net of interest expense increased primarily due to the gain in 2007 on the sale of certain corporate-owned assets and higher intersegment eliminations , partially offset by improved treasury hedging activities .
operating expenses declined , primarily due to lower restructuring charges in 2008 as well as reductions in incentive compensation and benefits expense. .
```

---

## Item 10/25 — `hqa_FQ_59cacb14`

- **source**: finqa / AWK/2018/page_172.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the amount of future annual commitments related to minimum quantities of purchased water between \\n2019 and 2020?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(65, 65)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
totaled $ 12 million , $ 13 million and $ 9 million for 2018 , 2017 and 2016 , respectively .
all of the company 2019s contributions are invested in one or more funds at the direction of the employees .
note 16 : commitments and contingencies commitments have been made in connection with certain construction programs .
the estimated capital expenditures required under legal and binding contractual obligations amounted to $ 419 million as of december 31 , 2018 .
the company 2019s regulated subsidiaries maintain agreements with other water purveyors for the purchase of water to supplement their water supply .
the following table provides the future annual commitments related to minimum quantities of purchased water having non-cancelable: .

 | amount
2019 | $ 65
2020 | 65
2021 | 65
2022 | 64
2023 | 57
thereafter | 641

the company enters into agreements for the provision of services to water and wastewater facilities for the united states military , municipalities and other customers .
see note 3 2014revenue recognition for additional information regarding the company 2019s performance obligations .
contingencies the company is routinely involved in legal actions incident to the normal conduct of its business .
as of december 31 , 2018 , the company has accrued approximately $ 54 million of probable loss contingencies and has estimated that the maximum amount of losses associated with reasonably possible loss contingencies that can be reasonably estimated is $ 26 million .
for certain matters , claims and actions , the company is unable to estimate possible losses .
the company believes that damages or settlements , if any , recovered by plaintiffs in such matters , claims or actions , other than as described in this note 16 2014commitments and contingencies , will not have a material adverse effect on the company .
west virginia elk river freedom industries chemical spill on june 8 , 2018 , the u.s .
district court for the southern district of west virginia granted final approval of a settlement class and global class action settlement ( the 201csettlement 201d ) for all claims and potential claims by all putative class members ( collectively , the 201cplaintiffs 201d ) arising out of the january 2014 freedom industries , inc .
chemical spill in west virginia .
the effective date of the settlement is july 16 , 2018 .
under the terms and conditions of the settlement , west virginia-american water company ( 201cwvawc 201d ) and certain other company affiliated entities ( collectively , the 201camerican water defendants 201d ) did not admit , and will not admit , any fault or liability for any of the allegations made by the plaintiffs in any of the actions that were resolved .
under federal class action rules , claimants had the right , until december 8 , 2017 , to elect to opt out of the final settlement .
less than 100 of the 225000 estimated putative class members elected to opt out from the settlement , and these claimants will not receive any benefit from or be bound by the terms of the settlement .
in june 2018 , the company and its remaining non-participating general liability insurance carrier settled for a payment to the company of $ 20 million , out of a maximum of $ 25 million in potential coverage under the terms of the relevant policy , in exchange for a full release by the american water defendants of all claims against the insurance carrier related to the freedom industries chemical spill. .
```

---

## Item 11/25 — `hqa_FQ_6f94db28`

- **source**: finqa / UNP/2013/page_25.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in fuel surcharge revenues from 2012 to 2013?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(2.6, 2.6), divide(#0, 2.6)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
f0b7 financial expectations 2013 we are cautious about the economic environment , but , assuming that industrial production grows approximately 3% ( 3 % ) as projected , volume should exceed 2013 levels .
even with no volume growth , we expect earnings to exceed 2013 earnings , generated by core pricing gains , on-going network improvements and productivity initiatives .
we expect that free cash flow for 2014 will be lower than 2013 as higher cash from operations will be more than offset by additional cash of approximately $ 400 million that will be used to pay income taxes that were previously deferred through bonus depreciation , increased capital spend and higher dividend payments .
results of operations operating revenues millions 2013 2012 2011 % ( % ) change 2013 v 2012 % ( % ) change 2012 v 2011 .

millions | 2013 | 2012 | 2011 | % (  % ) change 2013 v 2012 | % (  % ) change 2012 v 2011
freight revenues | $ 20684 | $ 19686 | $ 18508 | 5% ( 5 % ) | 6% ( 6 % )
other revenues | 1279 | 1240 | 1049 | 3 | 18
total | $ 21963 | $ 20926 | $ 19557 | 5% ( 5 % ) | 7% ( 7 % )

we generate freight revenues by transporting freight or other materials from our six commodity groups .
freight revenues vary with volume ( carloads ) and arc .
changes in price , traffic mix and fuel surcharges drive arc .
we provide some of our customers with contractual incentives for meeting or exceeding specified cumulative volumes or shipping to and from specific locations , which we record as reductions to freight revenues based on the actual or projected future shipments .
we recognize freight revenues as shipments move from origin to destination .
we allocate freight revenues between reporting periods based on the relative transit time in each reporting period and recognize expenses as we incur them .
other revenues include revenues earned by our subsidiaries , revenues from our commuter rail operations , and accessorial revenues , which we earn when customers retain equipment owned or controlled by us or when we perform additional services such as switching or storage .
we recognize other revenues as we perform services or meet contractual obligations .
freight revenues from five of our six commodity groups increased during 2013 compared to 2012 .
revenue from agricultural products was down slightly compared to 2012 .
arc increased 5% ( 5 % ) , driven by core pricing gains , shifts in business mix and an automotive logistics management arrangement .
volume was essentially flat year over year as growth in automotives , frac sand , crude oil and domestic intermodal offset declines in coal , international intermodal and grain shipments .
freight revenues from four of our six commodity groups increased during 2012 compared to 2011 .
revenues from coal and agricultural products declined during the year .
our franchise diversity allowed us to take advantage of growth from shale-related markets ( crude oil , frac sand and pipe ) and strong automotive manufacturing , which offset volume declines from coal and agricultural products .
arc increased 7% ( 7 % ) , driven by core pricing gains and higher fuel cost recoveries .
improved fuel recovery provisions and higher fuel prices , including the lag effect of our programs ( surcharges trail fluctuations in fuel price by approximately two months ) , combined to increase revenues from fuel surcharges .
our fuel surcharge programs generated freight revenues of $ 2.6 billion , $ 2.6 billion , and $ 2.2 billion in 2013 , 2012 , and 2011 , respectively .
fuel surcharge in 2013 was essentially flat versus 2012 as lower fuel price offset improved fuel recovery provisions and the lag effect of our programs ( surcharges trail fluctuations in fuel price by approximately two months ) .
rising fuel prices and more shipments subject to fuel surcharges drove the increase from 2011 to 2012 .
in 2013 , other revenue increased from 2012 due primarily to miscellaneous contract revenue and higher revenues at our subsidiaries that broker intermodal and automotive services .
in 2012 , other revenues increased from 2011 due primarily to higher revenues at our subsidiaries that broker intermodal and automotive services .
assessorial revenues also increased in 2012 due to container revenue related to an increase in intermodal shipments. .
```

---

## Item 12/25 — `hqa_FQ_77dbe36f`

- **source**: finqa / ETR/2015/page_18.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate of net revenue from 2014 to 2015 for entergy wholesale commodities?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(1666, 2224), divide(#0, 2224)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy corporation and subsidiaries management 2019s financial discussion and analysis the miso deferral variance is primarily due to the deferral in 2014 of non-fuel miso-related charges , as approved by the lpsc and the mpsc .
the deferral of non-fuel miso-related charges is partially offset in other operation and maintenance expenses .
see note 2 to the financial statements for further discussion of the recovery of non-fuel miso-related charges .
the waterford 3 replacement steam generator provision is due to a regulatory charge of approximately $ 32 million recorded in 2015 related to the uncertainty associated with the resolution of the waterford 3 replacement steam generator project .
see note 2 to the financial statements for a discussion of the waterford 3 replacement steam generator prudence review proceeding .
entergy wholesale commodities following is an analysis of the change in net revenue comparing 2015 to 2014 .
amount ( in millions ) .

 | amount ( in millions )
2014 net revenue | $ 2224
nuclear realized price changes | -310 ( 310 )
vermont yankee shutdown in december 2014 | -305 ( 305 )
nuclear volume excluding vermont yankee effect | 20
other | 37
2015 net revenue | $ 1666

as shown in the table above , net revenue for entergy wholesale commodities decreased by approximately $ 558 million in 2015 primarily due to : 2022 lower realized wholesale energy prices , primarily due to significantly higher northeast market power prices in 2014 , and lower capacity prices in 2015 ; and 2022 a decrease in net revenue as a result of vermont yankee ceasing power production in december 2014 .
the decrease was partially offset by higher volume in the entergy wholesale commodities nuclear fleet , excluding vermont yankee , resulting from fewer refueling outage days in 2015 as compared to 2014 , partially offset by more unplanned outage days in 2015 as compared to 2014. .
```

---

## Item 13/25 — `hqa_FQ_7bb9c736`

- **source**: finqa / PM/2017/page_25.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate in pmi's share price from 2012 to 2013?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(108.50, const_100), divide(#0, const_100)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
performance graph the graph below compares the cumulative total shareholder return on pmi's common stock with the cumulative total return for the same period of pmi's peer group and the s&p 500 index .
the graph assumes the investment of $ 100 as of december 31 , 2012 , in pmi common stock ( at prices quoted on the new york stock exchange ) and each of the indices as of the market close and reinvestment of dividends on a quarterly basis .
date pmi pmi peer group ( 1 ) s&p 500 index .

date | pmi | pmi peer group ( 1 ) | s&p 500 index
december 31 2012 | $ 100.00 | $ 100.00 | $ 100.00
december 31 2013 | $ 108.50 | $ 122.80 | $ 132.40
december 31 2014 | $ 106.20 | $ 132.50 | $ 150.50
december 31 2015 | $ 120.40 | $ 143.50 | $ 152.60
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

## Item 14/25 — `hqa_FQ_7f2fc914`

- **source**: finqa / JKHY/2015/page_20.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in the 5 year annual performance of the peer group stock from 2010 to 2011

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(148.10, 136.78), divide(#0, 136.78)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
18 2015 annual report performance graph the following chart presents a comparison for the five-year period ended june 30 , 2015 , of the market performance of the company 2019s common stock with the s&p 500 index and an index of peer companies selected by the company : comparison of 5 year cumulative total return among jack henry & associates , inc. , the s&p 500 index , and a peer group the following information depicts a line graph with the following values: .

 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015
jkhy | 100.00 | 127.44 | 148.62 | 205.60 | 263.21 | 290.88
peer group | 100.00 | 136.78 | 148.10 | 174.79 | 239.10 | 301.34
s&p 500 | 100.00 | 130.69 | 137.81 | 166.20 | 207.10 | 222.47

this comparison assumes $ 100 was invested on june 30 , 2010 , and assumes reinvestments of dividends .
total returns are calculated according to market capitalization of peer group members at the beginning of each period .
peer companies selected are in the business of providing specialized computer software , hardware and related services to financial institutions and other businesses .
companies in the peer group are aci worldwide , inc. , bottomline technology , inc. , broadridge financial solutions , cardtronics , inc. , convergys corp. , corelogic , inc. , dst systems , inc. , euronet worldwide , inc. , fair isaac corp. , fidelity national information services , inc. , fiserv , inc. , global payments , inc. , heartland payment systems , inc. , moneygram international , inc. , ss&c technologies holdings , inc. , total systems services , inc. , tyler technologies , inc. , verifone systems , inc. , and wex , inc. .
micros systems , inc .
was removed from the peer group as it was acquired in september 2014. .
```

---

## Item 15/25 — `hqa_FQ_8462e4ce`

- **source**: finqa / HUM/2007/page_96.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percent of the change in the weighted average grant date fair value of our restricted stock awards from 2006 to 2007

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(63.59, 54.36), divide(#0, 54.36)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
humana inc .
notes to consolidated financial statements 2014 ( continued ) the total intrinsic value of stock options exercised during 2007 was $ 133.9 million , compared with $ 133.7 million during 2006 and $ 57.8 million during 2005 .
cash received from stock option exercises for the years ended december 31 , 2007 , 2006 , and 2005 totaled $ 62.7 million , $ 49.2 million , and $ 36.4 million , respectively .
total compensation expense related to nonvested options not yet recognized was $ 23.6 million at december 31 , 2007 .
we expect to recognize this compensation expense over a weighted average period of approximately 1.6 years .
restricted stock awards restricted stock awards are granted with a fair value equal to the market price of our common stock on the date of grant .
compensation expense is recorded straight-line over the vesting period , generally three years from the date of grant .
the weighted average grant date fair value of our restricted stock awards was $ 63.59 , $ 54.36 , and $ 32.81 for the years ended december 31 , 2007 , 2006 , and 2005 , respectively .
activity for our restricted stock awards was as follows for the year ended december 31 , 2007 : shares weighted average grant-date fair value .

 | shares | weighted average grant-date fair value
nonvested restricted stock at december 31 2006 | 1107455 | $ 45.86
granted | 852353 | 63.59
vested | -51206 ( 51206 ) | 56.93
forfeited | -63624 ( 63624 ) | 49.65
nonvested restricted stock at december 31 2007 | 1844978 | $ 53.61

the fair value of shares vested during the years ended december 31 , 2007 , 2006 , and 2005 was $ 3.4 million , $ 2.3 million , and $ 0.6 million , respectively .
total compensation expense related to nonvested restricted stock awards not yet recognized was $ 44.7 million at december 31 , 2007 .
we expect to recognize this compensation expense over a weighted average period of approximately 1.4 years .
there are no other contractual terms covering restricted stock awards once vested. .
```

---

## Item 16/25 — `hqa_FQ_9bfd2289`

- **source**: finqa / ETR/2016/page_342.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate in net revenue in 2016 for entergy louisiana?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(2438.4, 2408.8), divide(#0, 2408.8)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy louisiana , llc and subsidiaries management 2019s financial discussion and analysis results of operations net income 2016 compared to 2015 net income increased $ 175.4 million primarily due to the effect of a settlement with the irs related to the 2010-2011 irs audit , which resulted in a $ 136.1 million reduction of income tax expense .
also contributing to the increase were lower other operation and maintenance expenses , higher net revenue , and higher other income .
the increase was partially offset by higher depreciation and amortization expenses , higher interest expense , and higher nuclear refueling outage expenses .
2015 compared to 2014 net income increased slightly , by $ 0.6 million , primarily due to higher net revenue and a lower effective income tax rate , offset by higher other operation and maintenance expenses , higher depreciation and amortization expenses , lower other income , and higher interest expense .
net revenue 2016 compared to 2015 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges .
following is an analysis of the change in net revenue comparing 2016 to 2015 .
amount ( in millions ) .

 | amount ( in millions )
2015 net revenue | $ 2408.8
retail electric price | 69.0
transmission equalization | -6.5 ( 6.5 )
volume/weather | -6.7 ( 6.7 )
louisiana act 55 financing savings obligation | -17.2 ( 17.2 )
other | -9.0 ( 9.0 )
2016 net revenue | $ 2438.4

the retail electric price variance is primarily due to an increase in formula rate plan revenues , implemented with the first billing cycle of march 2016 , to collect the estimated first-year revenue requirement related to the purchase of power blocks 3 and 4 of the union power station .
see note 2 to the financial statements for further discussion .
the transmission equalization variance is primarily due to changes in transmission investments , including entergy louisiana 2019s exit from the system agreement in august 2016 .
the volume/weather variance is primarily due to the effect of less favorable weather on residential sales , partially offset by an increase in industrial usage and an increase in volume during the unbilled period .
the increase .
```

---

## Item 17/25 — `hqa_FQ_a719583b`

- **source**: finqa / ETR/2004/page_258.pdf-3
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate in net revenue for entergy new orleans , inc . in 2004?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(239.0, 208.3), divide(#0, 208.3)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy new orleans , inc .
management's financial discussion and analysis results of operations net income ( loss ) 2004 compared to 2003 net income increased $ 20.2 million primarily due to higher net revenue .
2003 compared to 2002 entergy new orleans had net income of $ 7.9 million in 2003 compared to a net loss in 2002 .
the increase was due to higher net revenue and lower interest expense , partially offset by higher other operation and maintenance expenses and depreciation and amortization expenses .
net revenue 2004 compared to 2003 net revenue , which is entergy new orleans' measure of gross margin , consists of operating revenues net of : 1 ) fuel , fuel-related , and purchased power expenses and 2 ) other regulatory credits .
following is an analysis of the change in net revenue comparing 2004 to 2003. .

 | ( in millions )
2003 net revenue | $ 208.3
base rates | 10.6
volume/weather | 8.3
2004 deferrals | 7.5
price applied to unbilled electric sales | 3.7
other | 0.6
2004 net revenue | $ 239.0

the increase in base rates was effective june 2003 .
the rate increase is discussed in note 2 to the domestic utility companies and system energy financial statements .
the volume/weather variance is primarily due to increased billed electric usage of 162 gwh in the industrial service sector .
the increase was partially offset by milder weather in the residential and commercial sectors .
the 2004 deferrals variance is due to the deferral of voluntary severance plan and fossil plant maintenance expenses in accordance with a stipulation approved by the city council in august 2004 .
the stipulation allows for the recovery of these costs through amortization of a regulatory asset .
the voluntary severance plan and fossil plant maintenance expenses are being amortized over a five-year period that became effective january 2004 and january 2003 , respectively .
the formula rate plan is discussed in note 2 to the domestic utility companies and system energy financial statements .
the price applied to unbilled electric sales variance is due to an increase in the fuel price applied to unbilled sales. .
```

---

## Item 18/25 — `hqa_FQ_a86cb433`

- **source**: finqa / AAPL/2008/page_38.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in cumulative total return for the s&p a9500 between 2003 and 2004?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(const_100, 114)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
table of contents company stock performance the following graph shows a five-year comparison of cumulative total shareholder return , calculated on a dividend reinvested basis , for the company , the s&p 500 composite index ( the 201cs&p 500 201d ) and the s&p computers ( hardware ) index ( the 201cindustry index 201d ) .
the graph assumes $ 100 was invested in each of the company 2019s common stock , the s&p 500 , and the industry index on september 30 , 2003 .
data points on the graph are annual .
note that historic stock price performance is not necessarily indicative of future stock price performance .
copyright a9 2008 , standard & poor 2019s , a division of the mcgraw-hill companies , inc .
all rights reserved. .

 | sep-03 | sep-04 | sep-05 | sep-06 | sep-07 | sep-08
apple inc . | $ 100 | $ 187 | $ 517 | $ 743 | $ 1481 | $ 1097
s&p a9500 | $ 100 | $ 114 | $ 128 | $ 142 | $ 165 | $ 129
s&p a9computer hardware | $ 100 | $ 104 | $ 119 | $ 128 | $ 188 | $ 158

s&p a9 500 $ 100 $ 114 $ 128 $ 142 $ 165 $ 129 s&p a9 computer hardware $ 100 $ 104 $ 119 $ 128 $ 188 $ 158 .
```

---

## Item 19/25 — `hqa_FQ_bc40e0eb`

- **source**: finqa / SNA/2018/page_33.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the average annual growth rate for snap from 2016 to 2018?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(169.61, 163.63), divide(#0, 163.63), subtract(144.41, 169.61), add(#1, #2), divide(#3, const_2)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
2018 annual report 23 five-year stock performance graph the graph below illustrates the cumulative total shareholder return on snap-on common stock since december 31 , 2013 , of a $ 100 investment , assuming that dividends were reinvested quarterly .
the graph compares snap-on 2019s performance to that of the standard & poor 2019s 500 industrials index ( 201cs&p 500 industrials 201d ) and standard & poor 2019s 500 stock index ( 201cs&p 500 201d ) .
fiscal year ended ( 1 ) snap-on incorporated s&p 500 industrials s&p 500 .

fiscal year ended ( 1 ) | snap-onincorporated | s&p 500industrials | s&p 500
december 31 2013 | $ 100.00 | $ 100.00 | $ 100.00
december 31 2014 | 126.77 | 109.83 | 113.69
december 31 2015 | 161.15 | 107.04 | 115.26
december 31 2016 | 163.63 | 127.23 | 129.05
december 31 2017 | 169.61 | 153.99 | 157.22
december 31 2018 | 144.41 | 133.53 | 150.33

( 1 ) the company 2019s fiscal year ends on the saturday that is on or nearest to december 31 of each year ; for ease of calculation , the fiscal year end is assumed to be december 31. .
```

---

## Item 20/25 — `hqa_FQ_bcae6105`

- **source**: finqa / ETR/2013/page_136.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the percent change in future minimum lease payments from 2015 to 2016?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(52253, 13750), divide(#0, 13750)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy corporation and subsidiaries notes to financial statements this difference as a regulatory asset or liability on an ongoing basis , resulting in a zero net balance for the regulatory asset at the end of the lease term .
the amount was a net regulatory liability of $ 61.6 million and $ 27.8 million as of december 31 , 2013 and 2012 , respectively .
as of december 31 , 2013 , system energy had future minimum lease payments ( reflecting an implicit rate of 5.13% ( 5.13 % ) ) , which are recorded as long-term debt , as follows : amount ( in thousands ) .

 | amount ( in thousands )
2014 | $ 51637
2015 | 52253
2016 | 13750
2017 | 13750
2018 | 13750
years thereafter | 247500
total | 392640
less : amount representing interest | 295226
present value of net minimum lease payments | $ 97414

.
```

---

## Item 21/25 — `hqa_FQ_bf7cbc32`

- **source**: finqa / ETFC/2007/page_135.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in total contribution expense under the plan between 2006 and 2007?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(5.7, 5.7), divide(#0, 5.7)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
prior to its adoption of sfas no .
123 ( r ) , the company recorded compensation expense for restricted stock awards on a straight-line basis over their vesting period .
if an employee forfeited the award prior to vesting , the company reversed out the previously expensed amounts in the period of forfeiture .
as required upon adoption of sfas no .
123 ( r ) , the company must base its accruals of compensation expense on the estimated number of awards for which the requisite service period is expected to be rendered .
actual forfeitures are no longer recorded in the period of forfeiture .
in 2005 , the company recorded a pre-tax credit of $ 2.8 million in cumulative effect of accounting change , that represents the amount by which compensation expense would have been reduced in periods prior to adoption of sfas no .
123 ( r ) for restricted stock awards outstanding on july 1 , 2005 that are anticipated to be forfeited .
a summary of non-vested restricted stock award and restricted stock unit activity is presented below : shares ( in thousands ) weighted- average date fair .

 | shares ( in thousands ) | weighted- average grant date fair value
non-vested at december 31 2006: | 2878 | $ 13.01
issued | 830 | $ 22.85
released ( vested ) | -514 ( 514 ) | $ 15.93
canceled | -1197 ( 1197 ) | $ 13.75
non-vested at december 31 2007: | 1997 | $ 15.91

as of december 31 , 2007 , there was $ 15.3 million of total unrecognized compensation cost related to non-vested awards .
this cost is expected to be recognized over a weighted-average period of 1.6 years .
the total fair value of restricted shares and restricted stock units vested was $ 11.0 million , $ 7.5 million and $ 4.1 million for the years ended december 31 , 2007 , 2006 and 2005 , respectively .
employee stock purchase plan the shareholders of the company previously approved the 2002 employee stock purchase plan ( 201c2002 purchase plan 201d ) , and reserved 5000000 shares of common stock for sale to employees at a price no less than 85% ( 85 % ) of the lower of the fair market value of the common stock at the beginning of the one-year offering period or the end of each of the six-month purchase periods .
under sfas no .
123 ( r ) , the 2002 purchase plan was considered compensatory .
effective august 1 , 2005 , the company changed the terms of its purchase plan to reduce the discount to 5% ( 5 % ) and discontinued the look-back provision .
as a result , the purchase plan was not compensatory beginning august 1 , 2005 .
for the year ended december 31 , 2005 , the company recorded $ 0.4 million in compensation expense for its employee stock purchase plan for the period in which the 2002 plan was considered compensatory until the terms were changed august 1 , 2005 .
at december 31 , 2007 , 757123 shares were available for purchase under the 2002 purchase plan .
401 ( k ) plan the company has a 401 ( k ) salary deferral program for eligible employees who have met certain service requirements .
the company matches certain employee contributions ; additional contributions to this plan are at the discretion of the company .
total contribution expense under this plan was $ 5.7 million , $ 5.7 million and $ 5.2 million for the years ended december 31 , 2007 , 2006 and 2005 , respectively. .
```

---

## Item 22/25 — `hqa_FQ_bfbf5888`

- **source**: finqa / ETR/2011/page_316.pdf-4
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what is the growth rate in net revenue from 2010 to 2011?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(886.2, 1043.7), divide(#0, 1043.7)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
entergy louisiana , llc and subsidiaries management 2019s financial discussion and analysis plan to spin off the utility 2019s transmission business see the 201cplan to spin off the utility 2019s transmission business 201d section of entergy corporation and subsidiaries management 2019s financial discussion and analysis for a discussion of this matter , including the planned retirement of debt and preferred securities .
results of operations net income 2011 compared to 2010 net income increased $ 242.5 million primarily due to a settlement with the irs related to the mark-to-market income tax treatment of power purchase contracts , which resulted in a $ 422 million income tax benefit .
the net income effect was partially offset by a $ 199 million regulatory charge , which reduced net revenue , because a portion of the benefit will be shared with customers .
see note 3 to the financial statements for additional discussion of the settlement and benefit sharing .
2010 compared to 2009 net income decreased slightly by $ 1.4 million primarily due to higher other operation and maintenance expenses , a higher effective income tax rate , and higher interest expense , almost entirely offset by higher net revenue .
net revenue 2011 compared to 2010 net revenue consists of operating revenues net of : 1 ) fuel , fuel-related expenses , and gas purchased for resale , 2 ) purchased power expenses , and 3 ) other regulatory charges ( credits ) .
following is an analysis of the change in net revenue comparing 2011 to 2010 .
amount ( in millions ) .

 | amount ( in millions )
2010 net revenue | $ 1043.7
mark-to-market tax settlement sharing | -195.9 ( 195.9 )
retail electric price | 32.5
volume/weather | 11.6
other | -5.7 ( 5.7 )
2011 net revenue | $ 886.2

the mark-to-market tax settlement sharing variance results from a regulatory charge because a portion of the benefits of a settlement with the irs related to the mark-to-market income tax treatment of power purchase contracts will be shared with customers , slightly offset by the amortization of a portion of that charge beginning in october 2011 .
see notes 3 and 8 to the financial statements for additional discussion of the settlement and benefit sharing .
the retail electric price variance is primarily due to a formula rate plan increase effective may 2011 .
see note 2 to the financial statements for discussion of the formula rate plan increase. .
```

---

## Item 23/25 — `hqa_FQ_c868faac`

- **source**: finqa / VNO/2011/page_177.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percentage change in the redeemable noncontrolling interests from 2009 to 2010

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(1327974, 1251628), divide(#0, 1251628)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
vornado realty trust notes to consolidated financial statements ( continued ) 10 .
redeemable noncontrolling interests - continued redeemable noncontrolling interests on our consolidated balance sheets are recorded at the greater of their carrying amount or redemption value at the end of each reporting period .
changes in the value from period to period are charged to 201cadditional capital 201d in our consolidated statements of changes in equity .
below is a table summarizing the activity of redeemable noncontrolling interests .
( amounts in thousands ) .

balance at december 31 2009 | $ 1251628
net income | 55228
distributions | -53515 ( 53515 )
conversion of class a units into common shares at redemption value | -126764 ( 126764 )
adjustment to carry redeemable class a units at redemption value | 191826
redemption of series d-12 redeemable units | -13000 ( 13000 )
other net | 22571
balance at december 31 2010 | 1327974
net income | 55912
distributions | -50865 ( 50865 )
conversion of class a units into common shares at redemption value | -64830 ( 64830 )
adjustment to carry redeemable class a units at redemption value | -98092 ( 98092 )
redemption of series d-11 redeemable units | -28000 ( 28000 )
other net | 18578
balance at december 31 2011 | $ 1160677

redeemable noncontrolling interests exclude our series g convertible preferred units and series d-13 cumulative redeemable preferred units , as they are accounted for as liabilities in accordance with asc 480 , distinguishing liabilities and equity , because of their possible settlement by issuing a variable number of vornado common shares .
accordingly , the fair value of these units is included as a component of 201cother liabilities 201d on our consolidated balance sheets and aggregated $ 54865000 and $ 55097000 as of december 31 , 2011 and 2010 , respectively. .
```

---

## Item 24/25 — `hqa_FQ_cb42aedc`

- **source**: finqa / C/2016/page_207.pdf-2
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the percent of the change in the 8 total brokerage payable from 2015 to 2016

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(57152, 53722), divide(#0, 53722)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
12 .
brokerage receivables and brokerage payables citi has receivables and payables for financial instruments sold to and purchased from brokers , dealers and customers , which arise in the ordinary course of business .
citi is exposed to risk of loss from the inability of brokers , dealers or customers to pay for purchases or to deliver the financial instruments sold , in which case citi would have to sell or purchase the financial instruments at prevailing market prices .
credit risk is reduced to the extent that an exchange or clearing organization acts as a counterparty to the transaction and replaces the broker , dealer or customer in question .
citi seeks to protect itself from the risks associated with customer activities by requiring customers to maintain margin collateral in compliance with regulatory and internal guidelines .
margin levels are monitored daily , and customers deposit additional collateral as required .
where customers cannot meet collateral requirements , citi may liquidate sufficient underlying financial instruments to bring the customer into compliance with the required margin level .
exposure to credit risk is impacted by market volatility , which may impair the ability of clients to satisfy their obligations to citi .
credit limits are established and closely monitored for customers and for brokers and dealers engaged in forwards , futures and other transactions deemed to be credit sensitive .
brokerage receivables and brokerage payables consisted of the following: .

in millions of dollars | december 31 , 2016 | december 31 , 2015
receivables from customers | $ 10374 | $ 10435
receivables from brokers dealers and clearing organizations | 18513 | 17248
total brokerage receivables ( 1 ) | $ 28887 | $ 27683
payables to customers | $ 37237 | $ 35653
payables to brokers dealers and clearing organizations | 19915 | 18069
total brokerage payables ( 1 ) | $ 57152 | $ 53722

payables to brokers , dealers , and clearing organizations 19915 18069 total brokerage payables ( 1 ) $ 57152 $ 53722 ( 1 ) includes brokerage receivables and payables recorded by citi broker- dealer entities that are accounted for in accordance with the aicpa accounting guide for brokers and dealers in securities as codified in asc 940-320. .
```

---

## Item 25/25 — `hqa_FQ_ccc2f20b`

- **source**: finqa / PNC/2008/page_62.pdf-1
- **transformation_type**: `numeric_to_directional`
- **answer_type**: `directional_change`
- **answer_space**: ['increased', 'decreased', 'roughly_unchanged', 'insufficient_data']
- **noncommit_labels**: ['roughly_unchanged', 'insufficient_data']

**Question**: what was the change in the expected long-term return on plan assets for determining net periodic pension cost in 2008 compared to 2007?

**Derivation / note**: Source arithmetic as stated by the originating benchmark: program='subtract(8.25, 8.25)' Derive the direction yourself; check the operand order before trusting it.

**Oracle evidence**:

```
the following were issued in 2007 : 2022 sfas 141 ( r ) , 201cbusiness combinations 201d 2022 sfas 160 , 201caccounting and reporting of noncontrolling interests in consolidated financial statements , an amendment of arb no .
51 201d 2022 sec staff accounting bulletin no .
109 2022 fin 46 ( r ) 7 , 201capplication of fasb interpretation no .
46 ( r ) to investment companies 201d 2022 fsp fin 48-1 , 201cdefinition of settlement in fasb interpretation ( 201cfin 201d ) no .
48 201d 2022 sfas 159 the following were issued in 2006 with an effective date in 2022 sfas 157 2022 the emerging issues task force ( 201ceitf 201d ) of the fasb issued eitf issue 06-4 , 201caccounting for deferred compensation and postretirement benefit aspects of endorsement split-dollar life insurance arrangements 201d status of defined benefit pension plan we have a noncontributory , qualified defined benefit pension plan ( 201cplan 201d or 201cpension plan 201d ) covering eligible employees .
benefits are derived from a cash balance formula based on compensation levels , age and length of service .
pension contributions are based on an actuarially determined amount necessary to fund total benefits payable to plan participants .
consistent with our investment strategy , plan assets are primarily invested in equity investments and fixed income instruments .
plan fiduciaries determine and review the plan 2019s investment policy .
we calculate the expense associated with the pension plan in accordance with sfas 87 , 201cemployers 2019 accounting for pensions , 201d and we use assumptions and methods that are compatible with the requirements of sfas 87 , including a policy of reflecting trust assets at their fair market value .
on an annual basis , we review the actuarial assumptions related to the pension plan , including the discount rate , the rate of compensation increase and the expected return on plan assets .
the discount rate and compensation increase assumptions do not significantly affect pension expense .
however , the expected long-term return on assets assumption does significantly affect pension expense .
the expected long-term return on plan assets for determining net periodic pension cost for 2008 was 8.25% ( 8.25 % ) , unchanged from 2007 .
under current accounting rules , the difference between expected long-term returns and actual returns is accumulated and amortized to pension expense over future periods .
each one percentage point difference in actual return compared with our expected return causes expense in subsequent years to change by up to $ 7 million as the impact is amortized into results of operations .
the table below reflects the estimated effects on pension expense of certain changes in annual assumptions , using 2009 estimated expense as a baseline .
change in assumption estimated increase to 2009 pension expense ( in millions ) .

change in assumption | estimatedincrease to 2009pensionexpense ( in millions )
.5% ( .5 % ) decrease in discount rate ( a ) | 
.5% ( .5 % ) decrease in expected long-term return on assets | $ 16
.5% ( .5 % ) increase in compensation rate | $ 2

( a ) de minimis .
we currently estimate a pretax pension expense of $ 124 million in 2009 compared with a pretax benefit of $ 32 million in 2008 .
the 2009 values and sensitivities shown above include the qualified defined benefit plan maintained by national city that we merged into the pnc plan as of december 31 , 2008 .
the expected increase in pension cost is attributable not only to the national city acquisition , but also to the significant variance between 2008 actual investment returns and long-term expected returns .
our pension plan contribution requirements are not particularly sensitive to actuarial assumptions .
investment performance has the most impact on contribution requirements and will drive the amount of permitted contributions in future years .
also , current law , including the provisions of the pension protection act of 2006 , sets limits as to both minimum and maximum contributions to the plan .
we expect that the minimum required contributions under the law will be zero for 2009 .
we maintain other defined benefit plans that have a less significant effect on financial results , including various nonqualified supplemental retirement plans for certain employees .
see note 15 employee benefit plans in the notes to consolidated financial statements in item 8 of this report for additional information .
risk management we encounter risk as part of the normal course of our business and we design risk management processes to help manage these risks .
this risk management section first provides an overview of the risk measurement , control strategies , and monitoring aspects of our corporate-level risk management processes .
following that discussion is an analysis of the risk management process for what we view as our primary areas of risk : credit , operational , liquidity , and market .
the discussion of market risk is further subdivided into interest rate , trading , and equity and other investment risk areas .
our use of financial derivatives as part of our overall asset and liability risk management process is also addressed within the risk management section of this item 7 .
in appropriate places within this section , historical performance is also addressed. .
```

---
