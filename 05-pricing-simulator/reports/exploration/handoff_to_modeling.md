# Handoff to Modeling — 05 Pricing Simulator

## Clean data
- File: `reports/exploration/clean.parquet`
- Rows: 538,435
- Columns: 30
- One row = one store × one UPC × one week (key confirmed unique).

## Target column
- **UNITS** — weekly unit sales per store-UPC.
- Use **LOG_UNITS** as the model target for log-log demand estimation.
- The elasticity of a product is the coefficient on LOG_PRICE in a
  log-log regression, after controlling for store and time fixed effects.

## Columns to EXCLUDE and why
| Column | Reason to exclude |
|---|---|
| SPEND | PRICE × UNITS — perfect leakage of the target |
| DESCRIPTION, MANUFACTURER | Free-text identifiers; use UPC + category dummies |
| STORE_NAME, ADDRESS_CITY_NAME | Use STORE_NUM or SEG_VALUE_NAME |
| LOG_UNITS, LOG_PRICE | Derived; use as transformed target / input, not alongside raw |
| WEEK_END_DATE | Encode as week fixed effect or seasonal dummies instead |

## Columns that need encoding
- CATEGORY (4 levels) → dummy variables (drop one for intercept)
- SUB_CATEGORY (7 levels) → dummy variables
- SEG_VALUE_NAME (store segment, 5 levels) → dummy variables
- PROMO_TYPE (5 levels) → dummy variables
- PRODUCT_SIZE → extract numeric oz/count, or use as categorical

## Suggested validation design
- **Held-out time split**: hold out the last 26 weeks (Jul–Dec 2011) as the
  test set. The model trains on the first 130 weeks and predicts the last 26.
  This mimics real deployment: you always forecast future prices.
- Do NOT use random-row splits (they leak future information into training).

## Known pitfalls
1. **Store × UPC fixed effects**: each store-product pair has its own baseline
   demand level. Include store and UPC fixed effects to avoid confounding.
2. **VISITS / HHS collinearity**: r ≈ 0.99. Use only VISITS (or neither if
   store fixed effects already absorb traffic variation).
3. **Small cells**: Feature+Display events are only 24,078 rows
   (4.5% of data). Confidence intervals
   on the Feature+Display lift coefficient will be wide.
4. **PRICE > BASE_PRICE rows** (~2% of data): these are price-increase weeks.
   The demand model should handle them naturally, but flag them in residual plots.
5. **Zero-unit rows**: UNITS = 0 on 0 rows. These are
   likely out-of-stock events. Consider excluding them or using a hurdle model.

## Business metric for model evaluation
- **Mean Absolute Percentage Error (MAPE) on held-out UNITS**: the simulator
  user cares about the accuracy of the unit forecast for a given price move.
- Secondary metric: directional accuracy of the profit curve (does the model
  correctly identify the profit-maximising price?).

## Five exploration findings that motivate the model
1. All four categories have negative log-log demand slopes — price responsiveness
   is confirmed in the data.
2. Cold Cereal is more price-elastic than Mouthwash (slopes: Cereal ≈ −1.5,
   Mouthwash ≈ −0.8), suggesting different optimal markdown depths.
3. Feature + Display events lift units-per-visit by ~15% above the no-promo baseline;
   Feature-only weeks also outperform TPR-only weeks on the same traffic-adjusted metric.
4. Only ~28% of store-week-UPC observations have any
   promotion; the model must handle the imbalance between promo and non-promo rows.
5. VISITS and HHS are almost perfectly collinear (r = 0.99) — only one may
   enter the demand model.
