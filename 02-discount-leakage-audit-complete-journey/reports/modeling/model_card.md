# Model Card — Discount Leakage Audit

## What the model predicts

For every transaction line in the loyalty database the model produces a number
between 0 and 1: the fraction of list revenue expected to be given away as
discounts (disc_rate). A score of 0.30 means 30 cents of every dollar on the
shelf goes to promotions on this line. Lines with a high score are candidates for
promotion review.

## Data the model learned from

One year of loyalty-card grocery transactions (Dunnhumby The Complete Journey,
CC0 licence). Training used weeks 1–39 of 2017 (~1.06 million transaction lines
across ~2,400 households, 68,500 products, 457 stores). The model was tested on
weeks 40–52 (held out, never seen during training) — approximately 388,000 lines.

## How it was tested

The held-out test set (weeks 40–52) was evaluated exactly once after all tuning
was complete. No adjustment was made after seeing the test numbers.

Cross-validation inside the training set used TimeSeriesSplit (5 folds), which
keeps later weeks in validation and earlier weeks in training — matching real
deployment conditions.

## How good is it — in plain terms

- **RMSE of 0.147:** On average the model's predicted discount rate
  is off by about 14.7 percentage points. For a product with a
  true discount rate of 30%, the model's answer is typically between
  0% and 45%.
- **R² of 0.173:** The model explains about 17% of
  the variance in discount rates across lines, compared with 0% for a naive
  "predict the average" rule.
- **Capture at top 10%: 28.74%:** When the model flags the 10% of
  lines with the highest predicted discount rate, those lines contain
  29% of all actual discount dollars. A random flag would
  capture only 10%, so the model is roughly 2.9x better than
  random at finding where the discount money goes.
- **Estimated recoverable margin:** Capping promotions at a 25% discount rate for
  lines where the model predicts above 25% is associated with approximately
  $20,585 in potential margin recovery in the test
  period alone (weeks 40–52). This is a modelled association, not a guarantee.

## What drives its predictions

The model ranks drivers as follows (most to least influential):

1. **Product category and product type** (structural) — the promotional norms of
   a product's category explain most of the variance. Frozen foods, snacks, and
   beverages carry structurally higher promotions.
2. **Department** (structural) — TOYS, MEAT, and SEAFOOD departments have the
   highest historical leakage rates.
3. **Store** (semi-controllable) — some stores run promotions more aggressively
   than others.
4. **Brand type** (structural) — national brands attract more manufacturer-funded
   coupons; private brands are funded primarily by the retailer.
5. **Seasonality (week position)** (controllable) — promotional intensity peaks
   in Q1 and Q3.
6. **Quantity (pack size)** (controllable) — bulk promotions correlate with higher
   discount rates.

## What the model cannot do

- It **cannot prove cause and effect.** A high predicted discount rate does not
  mean trimming the promotion will save that money — the product's sales volume
  may depend on the promotion. Associations are not causes.
- It **cannot predict individual households.** Demographic data covers only
  one-third of households; the model focuses on product-level patterns.
- It **cannot detect fraud** or intentional misuse; it only models historical
  patterns.
- It **should not be applied to fuel lines**, which are excluded from training
  (different quantity units).
- It **should not be used past 2017** without retraining on more recent data;
  seasonal patterns and category norms shift over time.

## Known weaknesses

1. The top-7% of products drive 80% of discount dollars; the model may underfit
   the high-leakage tail for niche products with sparse history.
2. Demographic features (income, age, household size) were excluded because they
   cover only 33% of households; they may improve future versions if coverage grows.
3. The training sample covers one year; multi-year seasonality is not captured.

---

## Technical appendix

### Model family

CatBoost with Optuna-tuned hyperparameters.

### Parameters

{
  "iterations": 786,
  "learning_rate": 0.012487685950366444,
  "depth": 9,
  "l2_leaf_reg": 0.015185747074546159,
  "bagging_temperature": 0.7641667217893455,
  "random_strength": 0.5964423246121136,
  "random_seed": 42,
  "verbose": 0
}

### Benchmark table (CV RMSE, 200K-row sub-sample, 3-fold inner CV)

See `reports/modeling/tables/` for full CSVs.

### Tuning details

See `reports/modeling/tuning.md` for the Optuna search space, best parameters,
parameter importance, and optimisation history.

### Validation design

Temporal split: train weeks 1–39, test weeks 40–52.
Inner CV: TimeSeriesSplit(n_splits=5) for model comparison, n_splits=3 for Optuna.
All preprocessing (TargetEncoder) fit inside each CV fold to prevent leakage.

### Metrics

| Metric | Value |
|---|---|
| Test RMSE | 0.1470 |
| Test R² | 0.1734 |
| Test ECE (calibration) | 0.0108 |
| Capture @ top-10% | 0.2874 |
| Recoverable margin (25% cap) | $20,585 |
