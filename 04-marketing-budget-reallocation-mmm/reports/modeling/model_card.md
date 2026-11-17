# Model Card — Marketing Mix Model (MMM)
## Project: 04-marketing-budget-reallocation-mmm

---

## What the model predicts

This model predicts weekly revenue for a consumer brand from its weekly media spend across
five channels: TV, out-of-home (OOH), print, Facebook, and search. It was built to give the
brand a common yardstick for comparing channels that attribution tools cannot cover together.

## Data it learned from

- 208 weeks of data: 23 Nov 2015 to 11 Nov 2019 (the Robyn simulated weekly dataset).
- Inputs: spend per channel per week, newsletter sends, a competitor sales index, and
  whether the week had a special event (e.g., Christmas).
- Target: weekly revenue in USD.
- The model was trained on the first 188 weeks and evaluated on the last 20 weeks
  (May–Nov 2019) — it never saw those 20 weeks during training.

## How it was tested

- Rolling-origin cross-validation on the 188 training weeks: the model was tested on
  10 separate forward-looking windows, each covering 20 future weeks, before the final
  evaluation.
- One final evaluation on the 20-week held-out test set.

## How good it is

- Average weekly revenue prediction error: 6.0% (MAPE).
  On a typical week of $1.95M revenue, the model is off by roughly
  $118K.
- RMSE: $142K — the typical size of a prediction error in dollar terms.
- R²: 0.94 — the model explains 94% of the variation in weekly revenue.
- Calibration: the model predicts an average of $1.953M against an
  actual average of $1.953M (ratio: 1.000; 1.00 = perfect).

## What drives its predictions

The top controllable levers (by SHAP contribution, USD of predicted revenue variance):
See driver_importance.png in charts/.

Drivers fall into three categories:
- **Structural** (cannot be changed): trend (revenue grows slowly over time), seasonal cycles.
- **Semi-controllable**: competitor sales (a market demand proxy), special event weeks.
- **Controllable by the business**: TV, OOH, print, Facebook, and search spend; newsletter volume.

## Associations, not causes

The model identifies correlations between spend and revenue in this 4-year dataset.
Higher TV saturation is associated with higher revenue, but this does not prove that
*increasing* TV spend will *cause* proportional revenue growth. Event weeks and market
conditions are confounders that the model partly but not fully controls for.
Counterfactual spend estimates in the analysis are labelled as associations and require
a geo holdout experiment to validate before informing budget decisions.

## What it must not be used for

- Predicting revenue in a channel mix that is radically different from the training data
  (e.g., eliminating TV entirely for the first time — the model has no data for that regime).
- Claiming causal ROI without an A/B test or geo experiment to confirm direction of effect.
- Weekly operational decisions at the individual-ad level — this model works at weekly
  channel-spend totals only.

## Known weaknesses

1. Small dataset: 208 weeks limits the model's ability to separate channel effects precisely
   when channels run together (e.g., TV and Facebook often peak at the same time).
2. Fixed adstock decay: decay rates are set by industry priors, not estimated from data.
   Bayesian MMM (e.g., Meridian or Robyn) would estimate them simultaneously.
3. Saturation parameters are fixed, not learned. The Hill half-saturation constants are set
   to reasonable priors; they should be calibrated against market research or Bayesian
   estimation on a larger dataset.
4. No geo variation: the Robyn dataset is national. The Meridian geo dataset was not used
   for the main model (it is a separate system). Geo-level models would give tighter ROI
   estimates by exploiting regional variation.

---

## Technical appendix

### Model family benchmark (CV RMSE)

See reports/modeling/tables/full_benchmark.csv

### Tuning details

See reports/modeling/tuning.md

### Final test-set metrics

| Metric | Value |
|--------|-------|
| RMSE | $142,111 |
| MAE  | $109,414 |
| MAPE | 6.0% |
| R²   | 0.943 |

### Model selection rationale

Ridge was selected. See model selection section in notebook 03_modeling.ipynb
for the full decision logic including the one-std rule.

### Files

- Fitted model: models/mmm_model.joblib
- Predictions: reports/modeling/scores.csv
- Charts: reports/modeling/charts/
- Tables: reports/modeling/tables/
