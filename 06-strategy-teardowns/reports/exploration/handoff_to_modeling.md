# Handoff to Model Builder — Strategy Teardowns
Date: 2026-11-17

## Cleaned data files

| File | Rows | Columns | Description |
|------|------|---------|-------------|
| reports/exploration/netflix_clean.parquet | 24 | 9 | Netflix UCAN quarterly, Q4'19-Q4'25 |
| reports/exploration/five_below_clean.parquet | 8 | 13 | Five Below annual, FY2018-FY2025 |
| reports/exploration/clean.parquet | 8 | 13 | Same as five_below_clean (default file) |

## Target columns

**Netflix:** revenue_usd_m (UCAN quarterly revenue, USD millions).
Secondary target: paid_members_m (available only through Q4 2024).

**Five Below:** comp_sales_pct (comparable sales pct change) and op_margin_pct (derived).
Revenue growth (rev_yoy_pct) is a secondary target.

## Columns to exclude

| Column | Reason |
|--------|--------|
| quarter | String label; use end_date for time ordering |
| has_members | Filter flag; not a predictor |
| note (Five Below) | Annotation text; encode COVID flag instead |
| fiscal_year_end | Redundant with fiscal_year |

## Columns that need encoding or transformation

- covid_affected (Five Below): boolean -- keep as-is or one-hot encode.
- end_date / fiscal_year: use as time index; extract year and quarter number.
- Dollar amounts (revenue_usd, cogs_usd, etc.): raw USD; consider log-transform.

## Suggested validation design

**Netflix:** Time series with 20-24 observations. Use walk-forward validation
(train on first N quarters, test on next 1). Do not shuffle. Natural hold-out is
Q1-Q4 2025 (revenue only). Report MAE in USD millions.

**Five Below:** Only 8 observations. Leave-one-out cross-validation (LOOCV) is the only
reasonable approach. Any model here is illustrative, not predictive.

## Known pitfalls

1. Leakage risk (Netflix): arm_usd x paid_members_m x 3 ~ revenue_usd_m.
   Do not use both ARM and memberships as features for revenue prediction.
2. COVID distortion (Five Below): FY2020 and FY2021 are outliers.
3. Collinear columns (Five Below): stores_eop and net_new_stores are highly correlated.
4. Small N (Five Below): 8 rows. Any model with more than 2 parameters will overfit.
5. Missing 2025 memberships (Netflix): restrict to Q4'19-Q4'24 or impute.

## Business metric for model evaluation

- Netflix: MAE on UCAN quarterly revenue (USD millions). +/-$100M acceptable; >$300M too large.
- Five Below: MAE on comparable sales pct change. +/-1.5 ppt acceptable.

## Price events reference (Netflix)

| Date | Event |
|------|-------|
| Oct 2020 | Standard plan $12.99 -> $13.99 |
| Jan 2022 | Standard plan $13.99 -> $15.49 |
| Nov 2022 | Ads plan $6.99 launched |
| May 2023 | Paid-sharing enforcement began |
| Oct 2023 | Basic $9.99 -> $11.99; Premium $19.99 -> $22.99 |
| Jan 2025 | Standard $15.49 -> $17.99 |
| Mar 2026 | Standard $17.99 -> $19.99 |