# ML follow-ups (descriptive only; no re-modeling)

## Round 1 (from growth-strategy session)
Method for all: pandas on `reports/exploration/clean.parquet` (538,435 rows), script in session scratchpad. Rows are as-is; NOTE clean.parquet has 13,693 duplicate store-UPC-week keys (524,742 unique), contradicting "key confirmed unique" in handoff_to_modeling.md. Sums below include the duplicates.

### CORRECTIONS to ml_handoff_report.md (I did not edit it, per follow-up rules)
- Revenue: the report's "$1.49B total / $801M Cereal annualised" is WRONG. I multiplied the 3-year total by 52 in error. Correct figures below (Q1). Every "Annual revenue ($M)" cell in 6b and the $-figures in section 2 and the revenue-concentration claim inherit the error. Segment RANKINGS (shares) are unaffected.
- VISITS: described as "store traffic" in section 5. Data dictionary is right: shopping trips including this product (an outcome). SHAP 0.849 for VISITS therefore reflects near-duplication of the target (r = 0.987 with UNITS), not a traffic effect.
- Report text said LightGBM ran "holding traffic constant" as the reason counterfactuals are small. Reason is different; see Q2.
- Section 8 said exploration slopes came from "median-of-medians". Unverified; see Q3.
- Section 8 reconciliation said test set was "touched once". I did not verify that; the notebook evaluates on test in section 8 and the counterfactual (10.2) re-scores test rows (no refit).

### Q1 Total SPEND (measured, SPEND column)
Total $28.69M over 156 weeks = $9.56M/year. (Your $30.2M is PRICE x UNITS in my tables; SPEND differs slightly, ~5%.)
| Category | Total SPEND $ | Per year $ (total/3) |
|---|---|---|
| Cold Cereal | 15,408,035 | 5,136,011 |
| Frozen Pizza | 6,644,685 | 2,214,895 |
| Bag Snacks | 4,862,405 | 1,620,802 |
| Oral Hygiene | 1,772,283 | 590,761 |
(156 weeks = 3.0 years.) Your figures are right; the report is wrong.

### Q2 VISITS
Confirmed: VISITS = trips including the product (outcome). corr(UNITS, VISITS) = 0.987. Median UNITS/VISITS = 1.038 (0 rows with VISITS = 0).
Counterfactual (notebooks/03_modeling.ipynb, section 10.2): only LOG_PRICE, DISCOUNT_PCT, PRICE_TO_BASE_RATIO were changed. VISITS, lags, rolling mean, FEATURE/DISPLAY/TPR flags were held at observed values. So the answer to your question is yes. Because VISITS carries almost all the signal and was frozen, the +0.8% to +3.2% figures are a lower bound on a real price response, not a measure of it. The notebook's own narrative says "10-15% increase", which does NOT match the CSV (0.8-3.2%); the CSV is the computed result.

### Q3 Exploration slopes
I could not reproduce chart 01's slopes (-1.44, -1.16, -0.34, -0.38) and the exploration code was not in the artifacts I checked. My reproductions (LOG(units+1) on LOG price, UPC-level medians, one point per UPC):
| Category | n UPC points | slope (SE) | 95% CI |
|---|---|---|---|
| Bag Snacks | 15 | -1.48 (0.34) | -2.2 to -0.7 |
| Cold Cereal | 15 | +0.18 (0.44) | -0.8 to +1.1 |
| Frozen Pizza | 12 | -0.77 (0.41) | -1.7 to +0.1 |
| Oral Hygiene | 13 | -0.50 (0.14) | -0.8 to -0.2 |
So between-product slopes are not individually reliable (Cereal is not distinguishable from zero) and say nothing about what happens when one product's price changes. Chart 01 shows ~9-10 points per panel, so it is also between-point, not within-product.
Row-level pooled slopes (n = 130k/174k/114k/120k rows): Bag -1.35, Cereal -0.50, Pizza -1.18, Oral -0.45 (SE 0.004-0.008). Cereal -0.497 and Mouthwash -0.448 match hypotheses.md H3 exactly, so H3 used row-level; chart 01 and findings F1 ("-0.8 Mouthwash to -1.5 Cereal", which is also reversed: Cereal is the shallower one at row level) use something else. The exploration outputs are mutually inconsistent.
Within-UPC (demeaned by UPC only; no store, week or promo controls, so promo-confounded): Bag -0.21, Cereal -2.35, Pizza -2.73, Oral -1.12. Ordering is very different from chart 01. Treat the category ranking "Bag Snacks and Pizza most price-sensitive" as NOT established.

### Q4 Discounting by category (store-week-UPC rows, measured)
| Category | % rows PRICE<BASE | % FEATURE | % DISPLAY | mean depth when discounted | % of SPEND in discounted rows |
|---|---|---|---|---|---|
| Bag Snacks | 24.5 | 2.5 | 13.0 | 18.7% | 26.9 |
| Cold Cereal | 22.6 | 9.6 | 8.8 | 21.9% | 35.3 |
| Frozen Pizza | 28.3 | 16.7 | 14.7 | 23.1% | 48.4 |
| Oral Hygiene | 28.6 | 5.4 | 8.6 | 26.1% | 34.3 |
Note: all four categories are discounted in 23-29% of rows. Chart 02/finding F2 ("Bag Snacks and Cereal rarely discounted", median 0%) is a median artifact; Bag Snacks is not rarer than Cereal.

### Q5 Promo type by category (median per store-week-UPC row)
| Category | Type | rows | median units | median UPV |
|---|---|---|---|---|
| Bag Snacks | None | 90,516 | 10 | 1.048 |
| | TPR only | 20,985 | 12 | 1.200 |
| | Display only | 15,344 | 31 | 1.094 |
| | Feature only | 1,705 | 18 | 1.091 |
| | Feature+Display | 1,556 | 34 | 1.070 |
| Cold Cereal | None | 133,047 | 21 | 1.053 |
| | TPR only | 18,978 | 29 | 1.105 |
| | Display only | 5,453 | 43 | 1.104 |
| | Feature only | 6,822 | 45 | 1.179 |
| | Feature+Display | 9,828 | 86 | 1.167 |
| Frozen Pizza | None | 79,469 | 6 | 1.000 |
| | TPR only | 9,781 | 9 | 1.111 |
| | Display only | 6,028 | 18 | 1.143 |
| | Feature only | 8,289 | 15 | 1.133 |
| | Feature+Display | 10,754 | 25 | 1.139 |
| Oral Hygiene | None | 82,659 | 3 | 1.000 |
| | TPR only | 22,349 | 4 | 1.000 |
| | Display only | 8,403 | 5 | 1.000 |
| | Feature only | 4,529 | 7 | 1.067 |
| | Feature+Display | 1,940 | 10 | 1.095 |
Flags are taken as exclusive (F+D, F, D, TPR, none in that order). Units lift (2-4x) is far larger than UPV lift (0-15%), meaning promos mostly raise trips including the product, not units per trip. My report's "10-15% lift" is UPV only; do not read it as a unit lift. Oral Hygiene UPV is 1.000 for most types (median is flat; low resolution).

### Q6 Promo lift ratio (promoted / non-promoted median units) by segment within category
| Category | Mainstream | Upscale | Value |
|---|---|---|---|
| Bag Snacks | 1.80 | 1.56 | 1.75 |
| Cold Cereal | 2.05 | 2.00 | 1.78 |
| Frozen Pizza | 2.83 | 2.43 | 2.50 |
| Oral Hygiene | 1.67 | 2.00 | 1.50 |
Value stores are NOT consistently the highest. The Value-store advantage (F5 and my report) does not hold within category: Value is highest in none of the four, and lowest in Cereal and Oral. It was a product-mix artifact. Medians are integers on small counts (Oral: 2 vs 3), so differences are coarse. UPV-based ratios are 1.00-1.14 with no clear segment pattern.

### Q7 Price-increase weeks (PRICE > BASE_PRICE)
Rows: Bag 3,847; Pizza 1,129; Cereal 687; Oral 601; total 6,264 = 1.2% of rows (not ~2%).
Median units, same store-UPC pairs with both kinds of week:
| Category | pairs | median units, price > base | median units, price = base |
|---|---|---|---|
| Bag Snacks | 348 | 26 | 18 |
| Cold Cereal | 363 | 31.5 | 22 |
| Frozen Pizza | 300 | 14 | 9 |
| Oral Hygiene | 212 | 4 | 3 |
Units are HIGHER in price-increase weeks in all four categories. This is the same positive-association pattern as the Ridge results (price raised when demand is high, or deal timing). It is not evidence that raising prices increases demand, and it is a warning that observed price changes are not exogenous. Overall median 30 vs 9 (not pair-matched). Pairs = median of each pair's weeks; no test of significance run.

### Q8 Private label (DESCRIPTION starts "PL"; 3 PL UPCs per category)
| Category | PL share of SPEND | PL mean shelf price $ | National brand mean shelf price $ |
|---|---|---|---|
| Bag Snacks | 41.6% | 1.30 | 2.55 |
| Cold Cereal | 13.9% | 1.88 | 2.97 |
| Frozen Pizza | 24.9% | 3.58 | 6.11 |
| Oral Hygiene | 17.2% | 1.97 | 4.43 |
Prices are row means over all weeks (not size-adjusted; pack sizes differ).

### Optional: week-to-week variability, non-promoted weeks, within store-UPC
Coefficient of variation of weekly UNITS (std/mean, store-UPC pairs with >3 weeks; units > 0): median Bag 0.46, Cereal 0.36, Pizza 0.55, Oral 0.55 (means 0.47/0.38/0.55/0.54). Excludes TPR/Feature/Display weeks only; rows with PRICE < BASE but no flag are included, so this slightly overstates pure noise.

## Round 2 (from growth-strategy session)
Method: pandas on `reports/exploration/clean.parquet`. For Q1-Q5, the 13,693 duplicate store-UPC-week rows were dropped (first kept; 524,742 rows) because run and lag logic needs one row per week. Q6 uses all 538,435 rows (as in round 1 SPEND). "Discounted" = PRICE < BASE_PRICE (23-29% of rows, so includes small, unflagged markdowns). Medians; "pairs" = store-UPC pairs with both kinds of week. Descriptive only, not causal.

### Q1 Stores (measured)
77 stores: Mainstream 43, Upscale 15, Value 19. Every store carries all four categories (77 stores in each). Same split in each category (43/15/19). No store has more than one segment label. Products: Bag Snacks 15 UPCs, Cold Cereal 15, Frozen Pizza 12, Oral Hygiene 13 (55 total).

### Q2 Revenue lift ratio (SPEND per store-UPC-week, discounted vs undiscounted, same pairs)
| Category | pairs | median SPEND $, discounted | median SPEND $, undiscounted | ratio of medians | median of per-pair ratios |
|---|---|---|---|---|---|
| Bag Snacks | 890 | 27.39 | 23.92 | 1.15 | 1.17 |
| Cold Cereal | 1,155 | 92.40 | 59.50 | 1.55 | 1.60 |
| Frozen Pizza | 846 | 75.44 | 33.00 | 2.29 | 1.95 |
| Oral Hygiene | 974 | 12.00 | 9.76 | 1.23 | 1.20 |
(Ratio of medians uses pooled rows from those pairs; the per-pair column takes each pair's own median ratio.) Revenue is gross sales at the lower price; no margin data, so this is not profit. Discounted weeks are also chosen by retailers (often with Feature/Display), so this is not a price effect.

### Q3 Post-promotion dip (units)
"After" = first undiscounted week directly following a discounted week (consecutive weeks). "Far" = undiscounted weeks at least 3 weeks from any discounted week in that pair.
| Category | pairs | median units, after | median units, far | median of per-pair ratios |
|---|---|---|---|---|
| Bag Snacks | 874 | 9.5 | 10.0 | 1.00 |
| Cold Cereal | 1,155 | 21.0 | 21.0 | 1.03 |
| Frozen Pizza | 836 | 6.0 | 6.0 | 1.00 |
| Oral Hygiene | 877 | 2.5 | 3.0 | 1.00 |
Pooled rows from the same pairs: Bag 13 vs 10, Cereal 21 vs 21, Pizza 6 vs 7, Oral 3 vs 3 (after vs far). No post-promotion dip is visible in medians; Bag Snacks is higher after. Weeks "far" from discounts are quieter, low-velocity weeks, so this is not a clean baseline. No stockpiling evidence at median level; I did not test means, run-ends of long promotions, or significance.

### Q4 Discount cadence
| Category | median discounted weeks per store-UPC per year | median run length (weeks) | share of runs lasting 1 week |
|---|---|---|---|
| Bag Snacks | 11.0 | 3 | 26% |
| Cold Cereal | 11.6 | 2 | 33% |
| Frozen Pizza | 16.2 | 2 | 26% |
| Oral Hygiene | 13.8 | 4 | 22% |
Weeks-per-year = discounted weeks / (weeks observed / 52). Runs: 10,058 / 14,902 / 11,674 / 10,149 (Bag / Cereal / Pizza / Oral). A run is consecutive 7-day weeks with PRICE < BASE_PRICE.

### Q5 BASE_PRICE changes
A change = BASE_PRICE differs from the previous week's value for the same store-UPC (any difference; a threshold of 0.01 dollar gave identical results).
| Category | median changes per store-UPC (156 wks) | median per-UPC (of its store medians) | median weeks per UPC with at least 1 store changing | chain-wide share of those weeks (at least 90% of stores) | share of store-level change events that fall in chain-wide weeks |
|---|---|---|---|---|---|
| Bag Snacks | 17 | 18.0 | 111 | 1.4% | 2.7% |
| Cold Cereal | 34 | 30.0 | 135 | 3.6% | 8.6% |
| Frozen Pizza | 18 | 15.3 | 93 | 3.9% | 9.0% |
| Oral Hygiene | 9 | 8.0 | 92 | 1.1% | 2.6% |
Base price is changing often and mostly store by store, not chain-wide; stores already differ on everyday price. Caveat: base price is a derived series in this dataset (regular price flagged by the retailer); frequent changes may include data-definition noise, not real list-price moves. I did not check how changes are staggered across weeks.

### Q6 Concentration
25 of 55 UPCs (45%) account for 80% of total SPEND. Chart 05 (45%) is right; findings F4 ("~20 of 55", "one-third") is wrong, and my report repeated it. By category, UPCs to reach 80% of that category's SPEND: Bag 9 of 15, Cereal 10 of 15, Pizza 7 of 12, Oral 8 of 13. Top 5 UPCs hold 27.9% of SPEND. So revenue is only mildly concentrated; there is no small core of products to focus on.
