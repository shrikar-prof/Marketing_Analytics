# Tuning Report — MMM Budget Reallocation

## Selected model: Ridge

## Ridge search space
| Parameter | Range | Reason |
|-----------|-------|--------|
| alpha | 0.01 – 1000 (log-uniform) | Controls L2 penalty; wide range to let Optuna find the right scale |

**Best alpha:** 2.1603
**Best CV RMSE:** $301,426

## LightGBM search space
| Parameter | Range | Reason |
|-----------|-------|--------|
| n_estimators | 100–1000 | Number of boosting rounds |
| learning_rate | 0.005–0.3 (log) | Step size; small values need more rounds |
| max_depth | 2–8 | Tree depth; cap at 8 to avoid overfitting on 188 rows |
| num_leaves | 7–63 | Leaf count; correlated with depth |
| min_child_samples | 5–50 | Minimum samples per leaf; prevents overfitting |
| reg_alpha / reg_lambda | 1e-4 – 10 (log) | L1/L2 regularisation |
| subsample / colsample_bytree | 0.5–1.0 | Stochastic sampling for variance reduction |

**Best LightGBM CV RMSE:** $325,588
**Best params:** {'n_estimators': 540, 'learning_rate': 0.005213834914078768, 'max_depth': 8, 'num_leaves': 38, 'min_child_samples': 5, 'reg_alpha': 0.006245516335565081, 'reg_lambda': 0.004256187975475099, 'subsample': 0.669189556825644, 'colsample_bytree': 0.6804476282768768}

## XGBoost search space
| Parameter | Range | Reason |
|-----------|-------|--------|
| n_estimators | 100–1000 | Boosting rounds |
| learning_rate | 0.005–0.3 (log) | Same motivation as LightGBM |
| max_depth | 2–8 | Tree depth |
| min_child_weight | 1–20 | Minimum sum of instance weights per leaf |
| reg_alpha / reg_lambda | 1e-4 – 10 (log) | Regularisation |
| subsample / colsample_bytree | 0.5–1.0 | Stochastic sampling |

**Best XGBoost CV RMSE:** $308,028
**Best params:** {'n_estimators': 115, 'learning_rate': 0.2646843140122581, 'max_depth': 3, 'subsample': 0.9320098382967369, 'colsample_bytree': 0.7027659390792522, 'reg_alpha': 0.00872308367704873, 'reg_lambda': 2.86781086910453, 'min_child_weight': 1}

## Optuna settings
- Sampler: TPE (seed=42)
- Pruner: MedianPruner (n_warmup_steps=5)
- N trials: 60 per family
- Objective: mean rolling-origin CV RMSE (training set only)

## Parameter importance
(See charts/optuna_importance_{family}.png for plots)