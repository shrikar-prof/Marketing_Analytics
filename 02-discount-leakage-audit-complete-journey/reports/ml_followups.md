# ML follow-ups (round 1, 2026-10-28)

Base for all items: clean.parquet, fuel excluded: 1,445,035 lines, list revenue $5,063,618, discount $797,186 (full year, weeks 1-53 as indexed). Method: groupby sums in pandas on reports/exploration/clean.parquet. No modeling.

## Q1 Discount $ by department (measured)
| Dept | Discount $ | Share of total | Rate (% of list) |
|---|---|---|---|
| GROCERY | 469,588 | 58.9% | 16.9% |
| MEAT | 102,393 | 12.8% | 24.9% |
| MEAT-PCKGD | 67,784 | 8.5% | 22.6% |
| DRUG GM | 61,721 | 7.7% | 9.4% |
| PRODUCE | 41,646 | 5.2% | 11.4% |
| SEAFOOD-PCKGD | 11,897 | 1.5% | 24.9% |
| TOYS | ~0 (rounds to $0K) | ~0% | 43.4% |
Full list: all departments from the same groupby; TOYS dollar pool is below $1K per the exploration chart 02.

## Q2 Caps on actual rates, all weeks (measured)
| Cap | Discount $ above cap | Share of total |
|---|---|---|
| 25% | 227,564 | 28.5% |
| 35% | 107,138 | 13.4% |
| 50% | 15,978 | 2.0% |

| Lines with actual rate | Lines | Share of lines | Discount $ | Share of discount $ |
|---|---|---|---|---|
| >= 25% | 359,203 | 24.9% | 604,432 | 75.8% |
| >= 40% | 153,524 | 10.6% | 353,758 | 44.4% |
| >= 50% | 47,819 | 3.3% | 156,063 | 19.6% |
Note: this is a ceiling on what a cap touches, with no volume response. The model card's $20,585 is test-window, predicted>25% lines only, so it is not comparable.

## Q3 Test window vs rest (measured)
Correction: the test split is weeks 40-53 = 14 weeks, not 13 as the report says.
| Window | Lines | Discount $ | List $ | Rate | Discount $ per week |
|---|---|---|---|---|---|
| Weeks 1-39 | 1,057,007 | 587,348 | 3,672,090 | 15.99% | 15,060 |
| Weeks 40-53 | 388,028 | 209,838 | 1,391,529 | 15.08% | 14,988 |
The report's x4 (52/13) is wrong; the right factor is 52/14 = 3.71, giving about $76,500 per year, not $82,340. Weekly discount $ in the test window is within 0.5% of weeks 1-39, so the window is representative on dollars (rate is 0.9 pt lower). Assumes the saving scales with discount $ (assumed).

## Q4 Volume response proxy (measured, NOT a causal lift)
Top 100 SKUs by discount $. Per SKU: median weekly units in weeks with SKU rate >= 20% divided by median in weeks with rate < 5%. Needs >= 3 weeks in each state: 74 of 100 SKUs qualify.
Median ratio 4.5x; IQR 3.3x to 6.7x (with >= 1 week each: 88 SKUs, median 4.5x, IQR 3.3-6.4x).
Caveat: promo weeks are chosen by the retailer (seasonality, mailers, stockpiling, cannibalisation). Gross units only, no baseline or margin. It cannot support a payback verdict. A hold-out test is needed (report s.8 item 1).

## Q5 Store spread (measured)
108 stores with list revenue >= $10K (of 437). Store disc_rate p10 13.8%, median 15.9%, p90 18.5%; min 11.1%, max 23.7%. Stores above 20%: 4. The spread is narrow, so a store ceiling would touch few stores.

## Q6 Promotions join (measured)
Join key: product_id + store_id + week; matched lines 325,050 (22.5%), same as hypotheses.md H1. Display flag = display_location != '0'; mailer flag = mailer_location != '0'.
| Group | Lines | Discount $ | Rate | Share of total discount $ |
|---|---|---|---|---|
| Both | 71,001 | 104,004 | 36.5% | 13.0% |
| Mailer only | 167,657 | 255,927 | 34.4% | 32.1% |
| Display only | 86,392 | 50,435 | 17.6% | 6.3% |
| Matched, neither | 0 | 0 | n/a | 0% |
| Unmatched | 1,119,985 | 386,820 | 10.3% | 48.5% |
Promo-matched lines hold 51.5% of discount $ on 22.5% of lines. Note unmatched lines still carry 48.5% of discount $, so the promotions table does not explain half the leakage.

## Q7 Brand (measured)
National: $618,316 (77.6%), rate 15.8%. Private label: $178,870 (22.4%), rate 15.6%.

## Q8 Households (measured)
2,467 households ranked by household disc_rate, no minimum spend filter.
| Group | Households | Share of discount $ | Share of list $ | Group rate |
|---|---|---|---|---|
| Top 10% | 247 | 12.9% | 7.6% | 26.7% |
| Top 20% | 493 | 26.3% | 17.3% | 23.9% |
Household targeting is weak, consistent with report F5.

## Corrections to ml_handoff_report.md found while answering (not edited, per follow-up rules)
1. Test window is 14 weeks (40-53); "13-week" and x4 annualisation should be 14 weeks and x3.71 (about $76.5K per year).
2. Section 7a column "Actual disc $" holds the modeled expected value, and the shares are wrong. Actual discount $ and share on flagged lines: >=10%: $686,180 (86.1%); >=20%: $404,724 (50.8%); >=25%: $286,425 (35.9%); >=30%: $176,428 (22.1%). Modeled expected $ is in tables/02 column expected_risk_usd. Tables/02 CSV is right.
3. Section 7b decile dollars were typed from rounded shares; the exact figures are in tables/01_decile_targeting.csv (e.g. decile 1 $268,417, decile 2 $121,201). Rows 6-10 total $159,780.
4. F2 "2.9% vs 16.6%" are medians of line-level rates, not department averages.

# Round 2 (2026-10-28)
Same base and method (descriptive groupbys on clean.parquet, fuel excluded; promo join as in round 1). Excess = sum of max(0, total_disc - 0.25 x list_revenue) = $227,564. Measured, no modeling.

## Q1 List $ on high-rate lines
| Lines with actual rate | List $ | Discount $ | Average rate |
|---|---|---|---|
| >= 25% | 1,507,472 | 604,432 | 40.1% |
| >= 40% | 718,828 | 353,758 | 49.2% |

## Q2 Excess above 25% cap by group
| Promo group | Excess $ | Share |
|---|---|---|
| Mailer only | 95,342 | 41.9% |
| Unmatched | 78,536 | 34.5% |
| Both | 40,294 | 17.7% |
| Display only | 13,393 | 5.9% |
| Brand | Excess $ | Share |
| National | 183,077 | 80.5% |
| Private | 44,487 | 19.5% |

## Q3 Excess by department and category
| Department | Excess $ | Share |
|---|---|---|
| GROCERY | 122,742 | 53.9% |
| MEAT | 38,496 | 16.9% |
| MEAT-PCKGD | 21,163 | 9.3% |
| DRUG GM | 17,972 | 7.9% |
| PRODUCE | 14,606 | 6.4% |
| Category | Excess $ | Share |
|---|---|---|
| SOFT DRINKS | 22,387 | 9.8% |
| CHICKEN | 17,196 | 7.6% |
| FLUID MILK PRODUCTS | 10,340 | 4.5% |
| BEEF | 10,022 | 4.4% |
| ICE CREAM/MILK/SHERBTS | 9,342 | 4.1% |
| PORK | 8,947 | 3.9% |
| FRZN MEAT/MEAT DINNERS | 8,020 | 3.5% |
| CHEESE | 6,698 | 2.9% |
| BAKED BREAD/BUNS/ROLLS | 5,144 | 2.3% |
| HOT DOGS | 5,132 | 2.3% |

## Q4 SKUs holding the excess
21,926 SKUs have any excess. 383 SKUs hold 50% of it; 2,529 hold 80%.

## Q5 Seasonality
The data has 53 weeks; mean weekly discount $ = $15,041.
| Week | Discount $ | Excess over mean |
|---|---|---|
| 27 | 20,710 | +5,668 (+37.7%) |
| 21 | 16,663 | +1,622 |
| 22 | 17,798 | +2,757 |
| 23 | 16,611 | +1,570 |
| 21-23 total | 51,072 | +5,948 (+13.2% over 3 x mean) |
Week 27 is the highest week of the year; next are week 28 ($18,426), 45 ($18,046), 52 ($18,031).
