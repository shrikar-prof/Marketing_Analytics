# Handoff to Model Builder

## Clean file
/Users/shrikar/Documents/Marketing Analytics/02-discount-leakage-audit-complete-journey/reports/exploration/clean.parquet  (1,458,032 rows, 23 columns)

## Target column
`disc_rate` (total_disc / list_revenue) for rate prediction. `total_disc` in dollars for absolute-value tasks.

## Columns to EXCLUDE and why
| Column | Reason |
|---|---|
| basket_id | Identifier; no predictive signal |
| transaction_timestamp | Use `week` instead; exact timestamps risk data leakage |
| sales_value | Derived from list_revenue and total_disc -- leaks the target |
| list_revenue | Partially defines the target denominator; use as offset/weight only |
| is_fuel | Filter rows only; all fuel rows should be excluded before modelling |
| product_id | High-cardinality ID; use product_category + brand unless using embeddings |

## Columns that need encoding
| Column | Type | Suggestion |
|---|---|---|
| department | Nominal ~20 levels | One-hot or target-encode |
| brand | Binary | Binary flag (0/1) |
| product_category | Nominal many levels | Target-encode; group rare categories |
| product_type | Nominal many levels | Target-encode |
| income | Ordinal band | Ordinal integer |
| age | Ordinal band | Ordinal integer |
| display_location | Nominal few levels | One-hot |
| mailer_location | Nominal few levels | One-hot |
| week | Numeric 1-52 | As-is or sine/cosine for seasonality |

## Suggested validation design
Temporal split: train weeks 1-39 (75%), validate weeks 40-52 (25%). Reason: business question is forward-looking. Random splits would leak future-week patterns into training.

## Known pitfalls
1. Collinearity: retail_disc + coupon_disc + coupon_match_disc = total_disc. Do not include all three alongside the derived columns.
2. FUEL lines: exclude is_fuel==True before modelling.
3. Sparse promotions join: on_promo flag may under-count actual promotional activity.
4. Demographics coverage: only 801 of 2467 households have matched demographics.
5. Concentration: top 7% of products drive 80% of discount dollars; models may underfit the high-leakage tail if not weighted.

## Business metric for model evaluation
Primary: total recoverable margin = sum(predicted excess discount x volume) across flagged products.
Secondary: precision of flagged promotions (share that are truly unprofitable).
Do not optimise for RMSE alone -- disc_rate is right-skewed; most error mass is on low-value lines.
