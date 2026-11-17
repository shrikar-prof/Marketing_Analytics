# Hyperparameter Tuning Summary

## LightGBM

- Trials completed: 120
- Best CV RMSE: 1.6723
- Best parameters:
  - learning_rate: 0.2542059946009627
  - num_leaves: 369
  - max_depth: 7
  - min_child_samples: 50
  - subsample: 0.9481886927786826
  - colsample_bytree: 0.6046430733644007
  - reg_alpha: 0.019377650302198447
  - reg_lambda: 0.013439491857475434

Parameter importance:

| Parameter | Importance |
|---|---|
| min_child_samples | 0.4008 |
| learning_rate | 0.1383 |
| reg_lambda | 0.1142 |
| subsample | 0.1049 |
| reg_alpha | 0.0915 |
| num_leaves | 0.0768 |
| colsample_bytree | 0.0441 |
| max_depth | 0.0295 |

## XGBoost

- Trials completed: 109
- Best CV RMSE: 1.6915
- Best parameters:
  - learning_rate: 0.046724517095949776
  - max_depth: 10
  - min_child_weight: 28
  - subsample: 0.9053801720872909
  - colsample_bytree: 0.7027807162053101
  - reg_alpha: 0.011348012239614014
  - reg_lambda: 2.374856927636318

Parameter importance:

| Parameter | Importance |
|---|---|
| min_child_weight | 0.5916 |
| subsample | 0.1470 |
| reg_alpha | 0.0747 |
| learning_rate | 0.0588 |
| colsample_bytree | 0.0506 |
| reg_lambda | 0.0491 |
| max_depth | 0.0282 |