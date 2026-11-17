# Data Dictionary

| Table | Column | Meaning | Type | Unit | % Missing | # Distinct | Example | Usability | Motivating finding or hypothesis | Expected direction |
|---|---|---|---|---|---|---|---|---|---|---|
| transactions | household_id | Unique loyalty-card customer ID | object | ID | 0.0 | 2469 | 900 | identifier | nan | nan |
| transactions | store_id | Store where basket was rung | object | ID | 0.0 | 457 | 330 | grouping variable | nan | nan |
| transactions | basket_id | Unique shopping trip ID | object | ID | 0.0 | 155848 | 31198570044 | identifier | nan | nan |
| transactions | product_id | SKU identifier | object | ID | 0.0 | 68509 | 1095275 | join key | nan | nan |
| transactions | quantity | Units purchased | object | count | 0.0 | 8443 | 1.0 | input | nan | nan |
| transactions | sales_value | Amount retailer receives after all discounts | object | $ | 0.0 | 5003 | 0.5 | TARGET: pocket revenue | nan | nan |
| transactions | retail_disc | Loyalty-card markdown (positive = deduction) | object | $ | 0.0 | 2054 | 0.0 | input – retailer cost | nan | nan |
| transactions | coupon_disc | Manufacturer coupon face value | object | $ | 0.0 | 321 | 0.0 | input – manufacturer cost | nan | nan |
| transactions | coupon_match_disc | Retailer match of manufacturer coupon | object | $ | 0.0 | 66 | 0.0 | input – retailer cost | nan | nan |
| transactions | week | Week number 1-52 | object | week | 0.0 | 53 | 1 | time dimension | nan | nan |
| transactions | transaction_timestamp | Date-time of purchase | object | datetime | 0.0 | 155036 | 2017-01-01 11:53:26 | time dimension | nan | nan |
| transactions | product_id | SKU identifier | object | ID | 0.0 | 92331 | 25671 | join key | nan | nan |
| products | manufacturer_id | Manufacturer numeric ID | object | ID | 0.0 | 6471 | 2 | grouping variable | nan | nan |
| products | department | Broad merchandise department | object | category | 0.0 | 32 | GROCERY | grouping variable | nan | nan |
| products | brand | National vs Private label | object | category | 0.0 | 2 | National | input | nan | nan |
| products | product_category | Mid-level category | object | category | 0.58 | 303 | FRZN ICE | grouping variable | nan | nan |
| products | product_type | Fine-grained product type | object | category | 0.57 | 2378 | ICE - CRUSHED/CUBED | grouping variable | nan | nan |
| products | package_size | Package size as printed on pack | object | text | 33.13 | 3705 | 22 LB | rarely usable | nan | nan |
| transactions | product_id | SKU identifier | object | ID | 0.0 | 59800 | 1000050 | join key | nan | nan |
| transactions | store_id | Store where basket was rung | object | ID | 0.0 | 112 | 316 | grouping variable | nan | nan |
| promotions | display_location | In-store display location code | object | category | 0.0 | 10 | 9 | input | nan | nan |
| promotions | mailer_location | Circular/mailer position code | object | category | 0.0 | 11 | 0 | input | nan | nan |
| transactions | week | Week number 1-52 | object | week | 0.0 | 53 | 1 | time dimension | nan | nan |
| coupons | coupon_upc | UPC barcode of coupon | object | ID | 0.0 | 981 | 10000085207 | join key | nan | nan |
| transactions | product_id | SKU identifier | object | ID | 0.0 | 41857 | 9676830 | join key | nan | nan |
| coupons | campaign_id | Campaign that issued this coupon | object | ID | 0.0 | 27 | 26 | join key | nan | nan |
| transactions | household_id | Unique loyalty-card customer ID | object | ID | 0.0 | 410 | 1029 | identifier | nan | nan |
| coupons | coupon_upc | UPC barcode of coupon | object | ID | 0.0 | 491 | 51380041013 | join key | nan | nan |
| coupons | campaign_id | Campaign that issued this coupon | object | ID | 0.0 | 26 | 26 | join key | nan | nan |
| coupon_redemptions | redemption_date | Date coupon was used | object | date | 0.0 | 263 | 2017-01-01 | time dimension | nan | nan |
| coupons | campaign_id | Campaign that issued this coupon | object | ID | 0.0 | 27 | 1 | join key | nan | nan |
| transactions | household_id | Unique loyalty-card customer ID | object | ID | 0.0 | 1559 | 105 | identifier | nan | nan |
| coupons | campaign_id | Campaign that issued this coupon | object | ID | 0.0 | 27 | 1 | join key | nan | nan |
| campaign_descriptions | campaign_type | Type A/B/C classification | object | category | 0.0 | 3 | Type B | grouping variable | nan | nan |
| campaign_descriptions | start_date | Campaign start date | object | date | 0.0 | 25 | 2017-03-03 | time dimension | nan | nan |
| campaign_descriptions | end_date | Campaign end date | object | date | 0.0 | 25 | 2017-04-09 | time dimension | nan | nan |
| transactions | household_id | Unique loyalty-card customer ID | object | ID | 0.0 | 801 | 1 | identifier | nan | nan |
| demographics | age | Age band of head of household | object | ordinal | 0.0 | 6 | 65+ | input | nan | nan |
| demographics | income | Annual income band | object | ordinal | 0.0 | 12 | 35-49K | input | nan | nan |
| demographics | home_ownership | Own/rent/unknown | object | category | 29.09 | 4 | Homeowner | input | nan | nan |
| demographics | marital_status | Marital status | object | category | 17.1 | 2 | Married | input | nan | nan |
| demographics | household_size | Number of people in household | object | ordinal | 0.0 | 5 | 2 | input | nan | nan |
| demographics | household_comp | Household composition description | object | category | 0.0 | 4 | 2 Adults No Kids | input | nan | nan |
| demographics | kids_count | Number of children | object | ordinal | 0.0 | 4 | 0 | input | nan | nan |
| clean | total_disc | Sum of all three discount fields | object | $ | 0.0 | 999 | 1.29 | input | Finding 1 (price waterfall); H1-H4 (leakage-rate comparisons) | >= 0; higher in promoted lines (H1 predicts this) |
| clean | list_revenue | Pocket revenue + all discounts = full shelf price * qty | object | $ | 0.0 | 999 | 3.49 | input | Finding 1 (denominator of overall leakage rate); disc_rate denominator | > 0 always (sales_value > 0 after cleaning + non-negative discounts) |
| clean | disc_rate | Fraction of list revenue given away as discounts | object | fraction | 0.0 | 999 | 0.37 | input | Primary leakage metric across all hypotheses H1-H5 and all department/brand charts | 0 to 1; higher for promoted lines (H1); higher for top-3 departments (H4) |
| clean | retailer_disc | retail_disc + coupon_match_disc (retailer-funded total) | object | $ | 0.0 | 999 | 1.00 | input | H3 (private label vs national retailer-funded rate); Finding 4 | >= 0; expected higher for Private-brand lines on a per-list-revenue basis (H3) |
| clean | mfr_disc | coupon_disc (manufacturer-reimbursed) | object | $ | 0.0 | 999 | 0.29 | input | H2 (national brands receive more manufacturer-coupon funding); Finding 4 | >= 0; expected higher for National-brand lines (H2); near 0 for Private brands |
| clean | is_fuel | True if line belongs to FUEL department | object | flag | 0.0 | 2 | False | filter | Data quality / known quirk (FUEL quantities are in gallons, not items) | True for ~1.7% of lines; all FUEL lines excluded from leakage analysis |

## Derived Columns
Rows with table='clean' above.
