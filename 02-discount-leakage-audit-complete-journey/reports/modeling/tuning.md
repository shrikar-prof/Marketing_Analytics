# Hyperparameter Tuning Summary

Optuna TPE sampler, median pruner, seed=42.
Inner CV: TimeSeriesSplit(n_splits=3) on 200K-row sub-sample.

## LightGBM

- Trials completed: 60
- Best CV RMSE: 0.1511
- Best parameters:
  - `n_estimators`: 387
  - `learning_rate`: 0.01076519836695944
  - `num_leaves`: 132
  - `max_depth`: 9
  - `min_child_samples`: 90
  - `subsample`: 0.8852134760234265
  - `colsample_bytree`: 0.7207769283375451
  - `reg_alpha`: 0.0035345971021763806
  - `reg_lambda`: 0.0002498203242153574

- Parameter importance:
  - `subsample`: 0.2835
  - `colsample_bytree`: 0.1619
  - `max_depth`: 0.1184
  - `learning_rate`: 0.1169
  - `num_leaves`: 0.1076
  - `reg_lambda`: 0.0651
  - `n_estimators`: 0.0514
  - `min_child_samples`: 0.0488
  - `reg_alpha`: 0.0464

## XGBoost

- Trials completed: 60
- Best CV RMSE: 0.1514
- Best parameters:
  - `n_estimators`: 225
  - `learning_rate`: 0.027880315772005337
  - `max_depth`: 7
  - `min_child_weight`: 9.410769153953291
  - `subsample`: 0.675015956501266
  - `colsample_bytree`: 0.66197992498439
  - `reg_alpha`: 0.6762399980717687
  - `reg_lambda`: 0.0015719855193949553

- Parameter importance:
  - `reg_alpha`: 0.4304
  - `learning_rate`: 0.1907
  - `max_depth`: 0.1622
  - `n_estimators`: 0.0924
  - `min_child_weight`: 0.0523
  - `colsample_bytree`: 0.0367
  - `subsample`: 0.0231
  - `reg_lambda`: 0.0122

## CatBoost

- Trials completed: 60
- Best CV RMSE: 0.1513
- Best parameters:
  - `iterations`: 786
  - `learning_rate`: 0.012487685950366444
  - `depth`: 9
  - `l2_leaf_reg`: 0.015185747074546159
  - `bagging_temperature`: 0.7641667217893455
  - `random_strength`: 0.5964423246121136

- Parameter importance:
  - `random_strength`: 0.4097
  - `iterations`: 0.2728
  - `learning_rate`: 0.1396
  - `l2_leaf_reg`: 0.0646
  - `depth`: 0.0632
  - `bagging_temperature`: 0.0502

