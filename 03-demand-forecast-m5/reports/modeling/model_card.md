# Model Card — M5 Demand Forecast

## What this model predicts

This model forecasts the number of units each item will sell each day
at each of 10 Walmart stores. It produces one number per item per store per day.

## Who it is for

Inventory planners and store replenishment teams who set daily reorder quantities.
The model's 28-day forecast is designed to replace the current rule of thumb
(average of the same weekday over the last 4 weeks).

## Data it learned from

- **Source**: Walmart retail sales records from 2015-07-18 to 2015-07-02
  (d_1211 to d_1885; last ~2 years before the evaluation period).
- **Series**: 30,490 item-store combinations across California, Texas, Wisconsin.
- **Inputs**: recent sales history (lags and rolling averages), day-of-week,
  annual seasonality, holiday/event flags, government SNAP benefit-day flags,
  and weekly sell prices.
- **Training observations**: 20,580,750 item-store-day rows.

## How good is it

Evaluated on a held-out test set of 28 days (d_1914 to d_1941) never seen
during training or tuning:

| Metric | Model | Rule-of-thumb | Improvement |
|---|---|---|---|
| RMSE (units/day) | 1.707 | 2.259 | 24.4% |
| MAE (units/day)  | 0.862  | 1.074 | — |
| Mean RMSSE       | 0.708 | 1.000 | — |

**RMSE** (Root Mean Squared Error): average prediction error in units per item per day.
**RMSSE** < 1.0 means the model is more accurate than predicting "today equals yesterday".
A mean RMSSE of 0.708 means 29% improvement over naive.

## What drives predictions (top 5 factors)

1. **Recent sales history** (lag_7, roll_mean_28): items that sold well last week
   will be forecast to sell well again.
2. **Day of week**: weekends show 31% higher FOODS demand.
3. **Annual seasonality**: Q4 holiday peaks are captured automatically.
4. **SNAP benefit days**: food-stamp disbursement days lift FOODS demand by 10–20%.
5. **Sell price**: higher-priced items tend to sell fewer units per day.

## Controllable levers

| Action | Estimated demand change | Caveat |
|---|---|---|
| Reduce price by 10% (price_ratio -= 0.1) | +0.021 units/item-day | Association only |
| Increase price by 10% (price_ratio += 0.1) | +0.022 units/item-day | Association only |

**These are associations, not causal effects.** Promotions are often timed to
periods of expected high demand; the model cannot disentangle this confound.

## What the model cannot do

- **Stockouts**: zero sales may be stockout days, not zero demand.
- **New items**: lag features are unavailable for items with no history.
- **Demand shocks**: sudden events not in historical data are not captured.
- **Causal inference**: do not use price-demand associations for pricing decisions
  without additional causal analysis.

## Known weaknesses

- **Zero inflation**: 65–83% of item-days are zero; the model may predict small
  positive values for rarely-sold items. Consider rounding predictions < 0.5 to
  zero for ordering decisions.
- **Model age**: retrain monthly when new sales data accumulates.
- **Category differences**: RMSSE is highest for HOBBIES items (most intermittent).

## Technical appendix

**Selected model**: LightGBM
**Optuna trials**: LGB=120, XGB=109
**Best val RMSE**: 1.7430
**Test RMSE**: 1.7074
**Mean RMSSE**: 0.7077
**Features**: 35
**Training rows**: 20,580,750

**Benchmark table:**
              model  cv_rmse_mean  cv_mae_mean
LightGBM-FINAL-TEST      1.707390     0.861887
           LightGBM      1.735109     0.851986
          LGB-tuned      1.742985     0.856847
          XGB-tuned      1.743142     0.853707
           CatBoost      1.744800     0.856055
            XGBoost      1.759491     0.860196
              Ridge      1.796684     0.885242
      Random Forest      1.806005     0.863502
      Rule-of-thumb      2.258847     1.073838
         Naive-Lag7      2.660112     1.205352

**Best hyperparameters:**
{
  "learning_rate": 0.2542059946009627,
  "num_leaves": 369,
  "max_depth": 7,
  "min_child_samples": 50,
  "subsample": 0.9481886927786826,
  "colsample_bytree": 0.6046430733644007,
  "reg_alpha": 0.019377650302198447,
  "reg_lambda": 0.013439491857475434
}
