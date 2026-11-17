# Optuna Tuning Report — 05 Pricing Simulator

## LightGBM

### Search space
| Parameter | Range | Reason |
|---|---|---|
| n_estimators | 200–1000 | More trees improve fit; pruner prevents over-tuning |
| learning_rate | 0.005–0.1 (log) | Small LR + more trees generalises better |
| max_depth | 3–8 | Deep trees overfit panel data |
| num_leaves | 15–127 | Leaf-based growth complexity |
| subsample | 0.5–1.0 | Row sampling regularisation |
| colsample_bytree | 0.5–1.0 | Column sampling regularisation |
| reg_alpha | 1e-3–10 (log) | L1 regularisation |
| reg_lambda | 1e-3–10 (log) | L2 regularisation |
| min_child_samples | 10–100 | Min rows per leaf |

### Best parameters
- n_estimators: 940
- learning_rate: 0.03099922646608065
- max_depth: 7
- num_leaves: 102
- subsample: 0.8547882940121044
- colsample_bytree: 0.9989374621316585
- reg_alpha: 4.379535929839597
- reg_lambda: 0.13980360292262448
- min_child_samples: 67

**Best CV RMSE_log:** 0.1043
**Trials completed:** 60 | Pruned: 2

### Parameter importance (LightGBM)
| Parameter | Importance |
|---|---|
| colsample_bytree | 0.4210 |
| reg_alpha | 0.1470 |
| reg_lambda | 0.0841 |
| min_child_samples | 0.0841 |
| n_estimators | 0.0789 |
| max_depth | 0.0563 |
| subsample | 0.0558 |
| learning_rate | 0.0382 |
| num_leaves | 0.0346 |

---

## XGBoost

- n_estimators: 980
- learning_rate: 0.0333210640564721
- max_depth: 7
- subsample: 0.8082151379381173
- colsample_bytree: 0.9915720464599056
- reg_alpha: 2.0110301968896502
- reg_lambda: 3.2761667650278916
- min_child_weight: 16

**Best CV RMSE_log:** 0.1046
**Trials completed:** 60 | Pruned: 6

### Parameter importance (XGBoost)
| Parameter | Importance |
|---|---|
| reg_alpha | 0.3381 |
| n_estimators | 0.2228 |
| max_depth | 0.1020 |
| colsample_bytree | 0.0920 |
| subsample | 0.0818 |
| learning_rate | 0.0700 |
| reg_lambda | 0.0476 |
| min_child_weight | 0.0457 |