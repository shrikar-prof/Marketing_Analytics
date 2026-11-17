# Model Card — 05 Pricing Simulator

## What the model predicts
The model predicts **weekly unit sales** for a given product at a given store and price.
Given any price input for a product, it returns a predicted unit count with an uncertainty band.
The model is used in a pricing simulator: enter a price, see predicted units, revenue, and gross profit.

## Data it learned from
- Source: Dunnhumby 'Breakfast at the Frat' — 77 grocery stores, 55 products, 156 weeks (Jan 2009 – Dec 2011).
- Four categories: Bag Snacks (pretzels), Cold Cereal, Frozen Pizza, Oral Hygiene (mouthwash).
- Training period: first 130 weeks (Jan 2009 – Jun 2011). Test period: last 26 weeks (Jul–Dec 2011).

## How it was tested
- Held-out test: last 26 weeks of data, never used during training or tuning.
- Cross-validation: 5-fold expanding-window time-series CV on training data.
- Optuna: 60+ trials of Bayesian optimisation per model family.

## How good it is (plain language)
- **RMSE on log(units): 0.111** — typical prediction error is about 0.11 log-units,
  which corresponds to roughly ±12% in actual units.
- **R² on test set: 0.989** — the model explains 99% of the variation in weekly unit sales.
- **MAPE on units: 8.5%** — on average, unit predictions are off by 8.5% of actual units.
- Both baselines are significantly worse: category-mean RMSE was 0.848; simple Ridge RMSE was 0.749.

## What drives predictions
Top controllable drivers (from SHAP analysis):
- **VISITS**: 0.849 mean |SHAP|
- **CATEGORY**: 0.026 mean |SHAP|
- **LOG_PRICE**: 0.020 mean |SHAP|
- **SUB_CATEGORY**: 0.017 mean |SHAP|
- **LOG_BASE_PRICE**: 0.010 mean |SHAP|

Demand momentum (lag-1 and rolling-4) are also strong predictors, reflecting habit buying.

## Price elasticity (econometric estimate)
From the Ridge log-log model with store and product fixed effects:
- ORAL HYGIENE PRODUCTS: elasticity = 0.09 (1% price increase → 0.1% units change)
- COLD CEREAL: elasticity = 0.26 (1% price increase → 0.3% units change)
- FROZEN PIZZA: elasticity = 0.27 (1% price increase → 0.3% units change)
- BAG SNACKS: elasticity = 0.48 (1% price increase → 0.5% units change)
These are associations, not proven causal effects. See limitations below.

## What the model must NOT be used for
- Predicting demand for products outside the four categories in the data.
- Extrapolating to price ranges far outside the training data ($0 or >$12).
- Claiming causal proof that a price change will cause a specific unit change.
- Markets, geographies, or time periods not in the data.

## Known weaknesses
- Feature + Display events are only 4.5% of observations; lift coefficients have wide uncertainty.
- ~2% of rows have PRICE > BASE_PRICE (price increases). The model handles these but they are rare.
- Serial correlation in demand is captured by lag features, but long-run dynamics (new competition,
  changing shopper preferences) are not in the model.
- The elasticity estimates assume price variation is exogenous (not driven by unobserved demand shocks).
  Vendor deals and regional events could violate this.

---

## Technical appendix

### Model family benchmark (CV RMSE, 5-fold time-series CV)
| Model | CV RMSE mean | CV RMSE std | CV R² | CV MAPE |
|---|---|---|---|---|
| LightGBM (tuned) | 0.1043 | 0.0040 | — | — |
| XGBoost (tuned) | 0.1046 | 0.0041 | — | — |
| CatBoost (default) | 0.1053 | 0.0044 | — | — |
| LightGBM (default) | 0.1063 | 0.0038 | — | — |
| Random Forest | 0.1069 | 0.0042 | — | — |
| XGBoost (default) | 0.1070 | 0.0041 | — | — |
| Ridge FE | 0.4132 | 0.0033 | — | — |
| OLS FE | 0.4320 | 0.0343 | — | — |

### Selected model
**Primary (prediction):** LightGBM (tuned) with Optuna-tuned hyperparameters.
**Elasticity model:** Ridge log-log with store and UPC fixed effects.

### Test set performance
| Metric | LightGBM (prediction) | Ridge FE (elasticity) |
|---|---|---|
| RMSE_log | 0.1106 | 0.4188 |
| R² | 0.9886 | 0.8362 |
| MAPE_units | 8.5% | 53.5% |