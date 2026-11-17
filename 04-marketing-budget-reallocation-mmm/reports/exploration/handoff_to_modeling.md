# Handoff to Model Builder — MMM Budget Reallocation

## Clean data file
`reports/exploration/clean.parquet`
- Rows: 208 (one per week)
- Target column: `revenue`
- Date column: `DATE` (datetime, weekly frequency, Monday start)

## Target column
`revenue` — weekly USD revenue. It is right-skewed (CV ≈ 20%). Consider log-transforming before fitting a linear model, or use a Gamma GLM which natively handles positive-skewed outcomes.

## Columns to EXCLUDE from the model (and why)

| Column | Reason |
|--------|--------|
| `facebook_I` | Collinear with `facebook_S` (r = 0.97+). Keep spend only. |
| `search_clicks_P` | Collinear with `search_S` (r = 0.95+). Keep spend only. |
| `events` | Raw string column; replaced by `event_flag` (0/1). |
| `DATE` | Identifier — not a predictor. Use as time index for adstock. |

## Columns to ENCODE

| Column | Action |
|--------|--------|
| `event_flag` | Already 0/1 binary. No further encoding needed. |
| `events` | Excluded (see above). |

## Suggested model inputs
`tv_S`, `ooh_S`, `print_S`, `facebook_S`, `search_S`, `newsletter`, `competitor_sales_B`, `event_flag`

## Suggested validation design
- **Rolling-origin cross-validation**: hold out the last 10–20 weeks (Oct–Nov 2019) as an out-of-time test set. Do not use random k-fold — time series data must be validated forward in time only, or the model will "see the future."
- **Geo holdout (Meridian data)**: with 20 geos, hold out 4 geos as a geo test for the Meridian model. Random assignment is acceptable because geos differ in size but not in time structure.

## Known pitfalls

1. **Adstock / carryover.** TV and OOH spend in week t affects revenue in weeks t+1, t+2 … Model this with a geometric decay (adstock) or Weibull decay. Failing to do so will underestimate TV's true contribution.
2. **Saturation curves.** All channels show diminishing returns. Use a Hill or Michaelis-Menten saturation function. A linear model will overestimate the value of high-spend weeks.
3. **Trend confound.** Revenue has a mild upward trend. Include a linear or polynomial trend term, or use the competitor sales index as a control.
4. **Event weeks.** 15 weeks have outsized revenue. Without `event_flag`, the model will assign event-week uplift to whatever channels ran heavy spend in those weeks.
5. **Small cells.** Print spend is near zero in some weeks (minimum ≈ $500). Very low spend weeks give unstable ROI estimates for print. Flag or winsorise the bottom 5% of print weeks.

## Business metric for model evaluation
Primary: out-of-sample MAPE (mean absolute percentage error) on weekly revenue.
Secondary: decomposed channel contribution sums must be non-negative and must sum to total revenue (a sanity check unique to MMMs).

## Meridian secondary dataset
`data/raw/meridian_geo_media.csv` — 3,120 rows (20 geos × 156 weeks).
Use for geo-level MMM validation and geo-test design.
Target: `revenue` (= `conversions` × `revenue_per_conversion`).
Media inputs: `Channel0_spend` through `Channel3_spend`.
Controls: `competitor_activity_score_control`, `sentiment_score_control`, `population`.
