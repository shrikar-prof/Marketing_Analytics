# Model card: customer churn risk score

## Plain-language summary

- **What it predicts.** For each customer, the chance of leaving (churning) in the observation window, as a probability from 0 to 1. The use is to rank customers so a retention team can start with the riskiest. It does not say why anyone leaves.
- **Data it learned from.** The IBM Telco sample: 7,043 customers, one row each, one fiscal quarter; 26.5% left. 5,634 customers (80%) were used to build and tune the model; 1,409 (20%, with 374 leavers) were locked away and scored once at the end. Billing-total columns were left out because their timing relative to exit is unknown.
- **How it was tested.** Five model types were compared on 25 cross-validation folds. The top three were tuned with Optuna (60 trials per study, nested cross-validation so the tuning score is honest). The chosen model is **glm** (it had the best nested AUC, 0.8503, and is the simplest family; xgb, rf were also within one standard deviation but are more complex, so the rule preferred glm (section 6 of notebook 03)).
- **How good it is (held-out test, 1,409 customers).** AUC (chance that a random leaver is scored above a random stayer; 0.5 is a coin flip) is 0.847 (95% interval 0.827 to 0.868). The 20% of customers with the highest scores contain **53.8% (95% interval 49.8% to 59.0%)** of the monthly revenue of customers who left ($14,638 of $27,215); picking at random would capture 20%. In that group 67.7% (95% interval 62.1% to 72.7%) really leave (base rate 26.5%) and it holds 51.1% (95% interval 47.2% to 55.3%) of all leavers.
- **Against simple alternatives (same test rows).** The explorer-style segment rule captures 50.3% of lost revenue in its top 20%; the plain logistic model on raw columns 54.8%. The paired difference of the final model over the segment rule is +3.4 points (95% interval -0.1 to +7.6); over the raw logistic -1.1 points (-3.6 to +1.3). Where the interval includes zero, the model is not shown to beat that alternative on this test set.
- **Calibration (do customers scored 40% leave about 40% of the time?).** ECE (average gap between predicted and actual rate) is 0.021 (95% interval 0.018 to 0.045); Brier score (mean squared error of the probability; 0 is perfect, about 0.195 for always guessing the base rate) is 0.135 (95% interval 0.124 to 0.146). Our target was ECE of 0.05 or lower.
- **What drives the score** (top five original columns by SHAP): MonthlyCharges, InternetService, Contract, TechSupport, tenure. Contract, tenure, internet type and payment method overlap, so their individual shares are partly shared. MonthlyCharges and InternetService rank high partly because the bill and the service mix measure nearly the same thing and the model uses them together; this does not show that price alone drives churn. Types: structural (cannot be changed) tenure, Dependents; controllable by the business, most used: Contract, TechSupport, StreamingMovies.
- **What-if sensitivity (association, not cause).** Changing a lever in the model for eligible test customers moves their predicted churn probability by: Contract: month-to-month -> one year (bill unchanged) (-18.0 points, interval -18.6 to -17.4); PaymentMethod: electronic check -> bank transfer (automatic) (bill unchanged) (-6.1 points, interval -6.3 to -5.9); TechSupport: no -> yes, internet customers (bill unchanged) (-0.4 points, interval -0.6 to -0.3); TechSupport: no -> yes, internet customers (bill rises by add-on price) (-5.7 points, interval -5.9 to -5.5); OnlineSecurity: no -> yes, internet customers (bill unchanged) (-1.4 points, interval -1.6 to -1.3); OnlineSecurity: no -> yes, internet customers (bill rises by add-on price) (-6.7 points, interval -7.0 to -6.5); PaperlessBilling: yes -> no (bill unchanged) (-5.8 points, interval -6.0 to -5.6). These are model associations. The two add-on levers change by about 5 to 13 times (security 4.6 times, tech support 12.7 times) with the assumption about the bill, so they are not stable and must not be used to size anything. Customers who choose long contracts or automatic payment may differ in ways the data does not record. A randomised pilot is needed to measure what an offer really saves.
- **Must not be used for.** Deciding prices, service or credit for an individual on the basis of age (SeniorCitizen) or gender; treating a score as the reason a customer left; estimating the revenue an offer will save (no save rate or offer cost is in the data); using it on a different business or a different period without re-testing.
- **Known weaknesses.** One quarter of data and one company: no sign of how it behaves over time. About 374 leavers in the test set, so every estimate carries a wide interval (about +/-5 points). Tenure and billing may be measured at exit for leavers (unclear from this data), which could flatter the model. Segments with fewer than 100 test customers are not interpreted. Scores in `scores.csv` for training customers are out-of-fold; the model is not recalibrated.

# Technical appendix

## A. Validation design

Stratified random 80/20 split (seed 42): 5,634 train, 1,409 test. Model choice and tuning used repeated stratified 5-fold cross-validation (5 repeats, 25 fold-scores) on the training rows; the test set was scored once. Preprocessing is inside a scikit-learn Pipeline. Primary metric AUC; business metric top-20% revenue capture.

Final model: **glm**, parameters: `{"penalty": "elasticnet", "C": 9.512835184510749, "l1_ratio": 0.05281079501960359}`. Inputs: 15 categorical and 3 numeric raw columns plus engineered features ['contract_ord', 'm2m_fiber', 'm2m_echeck', 'm2m_first_year', 'first_year', 'log_tenure', 'internet_no_techsupport', 'internet_no_protection', 'n_protection', 'household_size'] (see features.md).

## B. Baselines and model families (25-fold cross-validation, training rows; mean and SD)

| model | auc mean | auc sd | pr_auc mean | pr_auc sd | top20_rev mean | top20_rev sd | top20_precision mean | top20_precision sd | brier mean | brier sd | ece mean | ece sd | fit s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GLM (logistic, engineered) | 0.8501 | 0.0092 | 0.6731 | 0.0219 | 0.5543 | 0.0202 | 0.6827 | 0.0248 | 0.1329 | 0.0039 | 0.0243 | 0.0049 | 0.0184 |
| Random forest | 0.8458 | 0.0103 | 0.6612 | 0.0237 | 0.5440 | 0.0204 | 0.6671 | 0.0226 | 0.1349 | 0.0042 | 0.0270 | 0.0071 | 0.9331 |
| LightGBM | 0.8443 | 0.0098 | 0.6644 | 0.0220 | 0.5456 | 0.0180 | 0.6687 | 0.0216 | 0.1356 | 0.0043 | 0.0313 | 0.0068 | 0.1059 |
| XGBoost | 0.8481 | 0.0094 | 0.6692 | 0.0220 | 0.5523 | 0.0183 | 0.6779 | 0.0230 | 0.1339 | 0.0039 | 0.0277 | 0.0061 | 0.1053 |
| CatBoost | 0.8447 | 0.0098 | 0.6628 | 0.0204 | 0.5425 | 0.0212 | 0.6660 | 0.0236 | 0.1356 | 0.0042 | 0.0304 | 0.0080 | 0.5129 |
| Logistic regression, raw columns | 0.8444 | 0.0101 | 0.6599 | 0.0172 | 0.5659 | 0.0210 | 0.6766 | 0.0226 | 0.1355 | 0.0039 | 0.0264 | 0.0082 | 0.0170 |
| Rule 2: segment churn rate | 0.8217 | 0.0115 | 0.5702 | 0.0182 | 0.5220 | 0.0363 | 0.6131 | 0.0221 | 0.1425 | 0.0038 | 0.0225 | 0.0089 | 0.0022 |

| model | auc mean | auc sd | pr_auc mean | pr_auc sd | top20_rev mean | top20_rev sd | top20_precision mean | top20_precision sd | brier mean | brier sd | ece mean | ece sd | fit s |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Rule 1: m2m fiber first-year flag | 0.6485 | 0.0116 | 0.4212 | 0.0160 | 0.4384 | 0.0259 | 0.5333 | 0.0267 | 0.2103 | 0.0069 | 0.2103 | 0.0069 | 0.0006 |
| Rule 2: segment churn rate | 0.8217 | 0.0115 | 0.5702 | 0.0182 | 0.5220 | 0.0363 | 0.6131 | 0.0221 | 0.1425 | 0.0038 | 0.0225 | 0.0089 | 0.0022 |
| Logistic regression, raw columns | 0.8444 | 0.0101 | 0.6599 | 0.0172 | 0.5659 | 0.0210 | 0.6766 | 0.0226 | 0.1355 | 0.0039 | 0.0264 | 0.0082 | 0.0170 |

## C. Tuning summary (nested cross-validation)

| family | nested_auc_mean | nested_auc_sd | nested_top20_mean | nested_top20_sd | nested_prauc_mean | nested_brier_mean | nested_ece_mean | final_best_auc | final_best_auc_sd | trials | pruned |
|---|---|---|---|---|---|---|---|---|---|---|---|
| glm | 0.8503 | 0.0106 | 0.5526 | 0.0174 | 0.6731 | 0.1328 | 0.0235 | 0.8510 | 0.0064 | 60 | 21 |
| xgb | 0.8503 | 0.0088 | 0.5559 | 0.0167 | 0.6710 | 0.1332 | 0.0252 | 0.8510 | 0.0061 | 60 | 21 |
| rf | 0.8476 | 0.0064 | 0.5446 | 0.0163 | 0.6625 | 0.1343 | 0.0273 | 0.8484 | 0.0073 | 60 | 17 |

Full search spaces, best parameters, importance tables and plots: tuning.md.

## D. Model selection

| family | nested_auc | auc_sd | top20_capture | pr_auc | brier | ece | simplicity_rank | seconds_to_score_1000 | within_1sd_of_best | chosen |
|---|---|---|---|---|---|---|---|---|---|---|
| glm | 0.8503 | 0.0106 | 0.5526 | 0.6731 | 0.1328 | 0.0235 | 1 | 0.0031 | True | True |
| xgb | 0.8503 | 0.0088 | 0.5559 | 0.6710 | 0.1332 | 0.0252 | 2 | 0.0043 | True | False |
| rf | 0.8476 | 0.0064 | 0.5446 | 0.6625 | 0.1343 | 0.0273 | 3 | 0.0307 | True | False |

## E. Held-out test metrics with 95% bootstrap intervals

| model | metric | estimate | ci_low | ci_high |
|---|---|---|---|---|
| FINAL: glm | auc | 0.8474 | 0.8269 | 0.8679 |
| FINAL: glm | pr_auc | 0.6638 | 0.6137 | 0.7146 |
| FINAL: glm | top20_rev | 0.5379 | 0.4977 | 0.5896 |
| FINAL: glm | top20_precision | 0.6773 | 0.6206 | 0.7270 |
| FINAL: glm | top20_recall | 0.5107 | 0.4722 | 0.5534 |
| FINAL: glm | brier | 0.1348 | 0.1236 | 0.1456 |
| FINAL: glm | ece | 0.0206 | 0.0184 | 0.0448 |
| Rule 1: m2m fiber first-year flag | auc | 0.6340 | 0.6090 | 0.6588 |
| Rule 1: m2m fiber first-year flag | pr_auc | 0.3956 | 0.3551 | 0.4363 |
| Rule 1: m2m fiber first-year flag | top20_rev | 0.4173 | 0.3724 | 0.4600 |
| Rule 1: m2m fiber first-year flag | top20_precision | 0.5106 | 0.4362 | 0.5709 |
| Rule 1: m2m fiber first-year flag | top20_recall | 0.3850 | 0.3399 | 0.4232 |
| Rule 1: m2m fiber first-year flag | brier | 0.2229 | 0.1994 | 0.2456 |
| Rule 1: m2m fiber first-year flag | ece | 0.2229 | 0.1994 | 0.2456 |
| Rule 2: segment churn rate | auc | 0.8162 | 0.7940 | 0.8379 |
| Rule 2: segment churn rate | pr_auc | 0.5447 | 0.4956 | 0.5921 |
| Rule 2: segment churn rate | top20_rev | 0.5034 | 0.4579 | 0.5482 |
| Rule 2: segment churn rate | top20_precision | 0.5816 | 0.5142 | 0.6418 |
| Rule 2: segment churn rate | top20_recall | 0.4385 | 0.3979 | 0.4798 |
| Rule 2: segment churn rate | brier | 0.1458 | 0.1349 | 0.1558 |
| Rule 2: segment churn rate | ece | 0.0224 | 0.0122 | 0.0439 |
| Logistic regression, raw columns | auc | 0.8392 | 0.8175 | 0.8604 |
| Logistic regression, raw columns | pr_auc | 0.6297 | 0.5755 | 0.6828 |
| Logistic regression, raw columns | top20_rev | 0.5485 | 0.5104 | 0.5970 |
| Logistic regression, raw columns | top20_precision | 0.6596 | 0.6028 | 0.7199 |
| Logistic regression, raw columns | top20_recall | 0.4973 | 0.4607 | 0.5387 |
| Logistic regression, raw columns | brier | 0.1391 | 0.1280 | 0.1497 |
| Logistic regression, raw columns | ece | 0.0259 | 0.0181 | 0.0492 |

Paired differences (final minus baseline) on the same bootstrap resamples:

| final_minus | metric | difference | ci_low | ci_high | excludes_zero |
|---|---|---|---|---|---|
| Rule 1: m2m fiber first-year flag | top20_rev | 0.1205 | 0.0790 | 0.1691 | True |
| Rule 1: m2m fiber first-year flag | auc | 0.2134 | 0.1928 | 0.2371 | True |
| Rule 2: segment churn rate | top20_rev | 0.0345 | -0.0012 | 0.0760 | False |
| Rule 2: segment churn rate | auc | 0.0312 | 0.0199 | 0.0433 | True |
| Logistic regression, raw columns | top20_rev | -0.0106 | -0.0365 | 0.0127 | False |
| Logistic regression, raw columns | auc | 0.0082 | 0.0026 | 0.0137 | True |

## F. Decile table (test set, 1 = highest predicted risk)

| decile | customers | mean_predicted_risk | actual_churn_rate | lift_vs_base | leavers | monthly_revenue_lost_usd | cum_share_customers | cum_share_leavers_captured | cum_share_lost_revenue_captured |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 141 | 0.778 | 0.766 | 2.886 | 108 | 8494.900 | 0.100 | 0.289 | 0.312 |
| 2 | 141 | 0.589 | 0.589 | 2.218 | 83 | 6143.000 | 0.200 | 0.511 | 0.538 |
| 3 | 141 | 0.453 | 0.397 | 1.496 | 56 | 4414.700 | 0.300 | 0.660 | 0.700 |
| 4 | 141 | 0.333 | 0.312 | 1.176 | 44 | 2908.100 | 0.400 | 0.778 | 0.807 |
| 5 | 141 | 0.230 | 0.255 | 0.962 | 36 | 2256.250 | 0.500 | 0.874 | 0.890 |
| 6 | 141 | 0.139 | 0.163 | 0.615 | 23 | 1200.500 | 0.600 | 0.936 | 0.934 |
| 7 | 141 | 0.078 | 0.113 | 0.428 | 16 | 1227.950 | 0.700 | 0.979 | 0.979 |
| 8 | 141 | 0.043 | 0.043 | 0.160 | 6 | 419.500 | 0.801 | 0.995 | 0.994 |
| 9 | 141 | 0.021 | 0.007 | 0.027 | 1 | 92.450 | 0.901 | 0.997 | 0.998 |
| 10 | 140 | 0.008 | 0.007 | 0.027 | 1 | 57.550 | 1.000 | 1.000 | 1.000 |

## G. Threshold table (test set)

| cutoff | customers_flagged | share_flagged | precision | recall | false_positive_rate | share_lost_revenue_captured |
|---|---|---|---|---|---|---|
| 0.100 | 860 | 0.610 | 0.409 | 0.941 | 0.491 | 0.940 |
| 0.250 | 609 | 0.432 | 0.491 | 0.799 | 0.300 | 0.823 |
| 0.500 | 298 | 0.211 | 0.668 | 0.532 | 0.096 | 0.561 |
| 0.750 | 88 | 0.062 | 0.841 | 0.198 | 0.014 | 0.218 |
| 0.900 | 4 | 0.003 | 1.000 | 0.011 | 0.000 | 0.013 |

## H. Segment performance (test set; small = fewer than 100 customers)

| segment | value | customers | leavers | actual_churn_pct | mean_predicted_pct | gap_pts | auc_within_segment | top20_capture | small |
|---|---|---|---|---|---|---|---|---|---|
| Contract | Month-to-month | 773 | 329 | 42.56 | 43.14 | 0.58 | 0.76 | 0.39 | False |
| Contract | One year | 300 | 36 | 12.00 | 11.15 | -0.85 | 0.75 | 0.51 | False |
| Contract | Two year | 336 | 9 | 2.68 | 2.95 | 0.28 | 0.74 | 0.71 | False |
| InternetService | DSL | 484 | 97 | 20.04 | 18.86 | -1.18 | 0.83 | 0.48 | False |
| InternetService | Fiber optic | 613 | 252 | 41.11 | 42.91 | 1.80 | 0.79 | 0.36 | False |
| InternetService | No | 312 | 25 | 8.01 | 7.22 | -0.79 | 0.89 | 0.76 | False |
| Tenure | 13+ months | 960 | 159 | 16.56 | 17.17 | 0.61 | 0.84 | 0.61 | False |
| Tenure | first 12 months | 449 | 215 | 47.88 | 47.21 | -0.67 | 0.77 | 0.45 | False |
| PaymentMethod | Bank transfer (automatic) | 300 | 57 | 19.00 | 15.94 | -3.06 | 0.87 | 0.65 | False |
| PaymentMethod | Credit card (automatic) | 309 | 51 | 16.50 | 16.67 | 0.17 | 0.85 | 0.64 | False |
| PaymentMethod | Electronic check | 474 | 206 | 43.46 | 45.07 | 1.61 | 0.79 | 0.38 | False |
| PaymentMethod | Mailed check | 326 | 60 | 18.40 | 19.59 | 1.19 | 0.82 | 0.61 | False |
| SeniorCitizen | not senior | 1187 | 276 | 23.25 | 23.88 | 0.63 | 0.85 | 0.58 | False |
| SeniorCitizen | senior | 222 | 98 | 44.14 | 42.06 | -2.09 | 0.78 | 0.35 | False |
| gender | Female | 687 | 193 | 28.09 | 26.71 | -1.38 | 0.84 | 0.51 | False |
| gender | Male | 722 | 181 | 25.07 | 26.78 | 1.71 | 0.85 | 0.57 | False |

## I. Driver importance

| column | auc_drop_mean | auc_drop_sd | top20_drop_mean | top20_drop_sd | mean_abs_shap | rank_perm | rank_shap | driver_type |
|---|---|---|---|---|---|---|---|---|
| MonthlyCharges | 0.1051 | 0.0086 | 0.0919 | 0.0134 | 1.5085 | 2.0000 | 1.0000 | semi-controllable |
| InternetService | 0.2301 | 0.0179 | 0.2932 | 0.0210 | 1.2086 | 1.0000 | 2.0000 | semi-controllable |
| Contract | 0.0701 | 0.0119 | 0.0668 | 0.0172 | 0.7663 | 4.0000 | 3.0000 | controllable |
| TechSupport | 0.0045 | 0.0022 | 0.0181 | 0.0067 | 0.5464 | 8.0000 | 4.0000 | controllable |
| tenure | 0.0849 | 0.0061 | 0.0921 | 0.0148 | 0.4919 | 3.0000 | 5.0000 | structural |
| StreamingMovies | 0.0161 | 0.0029 | 0.0410 | 0.0133 | 0.4220 | 5.0000 | 6.0000 | controllable |
| StreamingTV | 0.0142 | 0.0036 | 0.0373 | 0.0076 | 0.4172 | 6.0000 | 7.0000 | controllable |
| MultipleLines | 0.0093 | 0.0022 | 0.0394 | 0.0095 | 0.3351 | 7.0000 | 8.0000 | semi-controllable |
| OnlineSecurity | 0.0001 | 0.0003 | -0.0008 | 0.0030 | 0.1885 | 15.0000 | 9.0000 | controllable |
| PaperlessBilling | 0.0017 | 0.0015 | 0.0154 | 0.0068 | 0.1844 | 11.0000 | 10.0000 | controllable |
| PaymentMethod | 0.0026 | 0.0013 | 0.0098 | 0.0098 | 0.1566 | 10.0000 | 11.0000 | controllable |
| PhoneService | 0.0027 | 0.0016 | 0.0117 | 0.0041 | 0.0999 | 9.0000 | 12.0000 | semi-controllable |
| Dependents | -0.0002 | 0.0006 | 0.0035 | 0.0056 | 0.0590 | 18.0000 | 13.0000 | structural |
| DeviceProtection | 0.0012 | 0.0018 | 0.0028 | 0.0064 | 0.0535 | 13.0000 | 14.0000 | controllable |
| SeniorCitizen | 0.0014 | 0.0004 | 0.0004 | 0.0038 | 0.0406 | 12.0000 | 15.0000 | structural |
| OnlineBackup | 0.0006 | 0.0006 | 0.0035 | 0.0049 | 0.0224 | 14.0000 | 16.0000 | controllable |
| Partner | -0.0001 | 0.0002 | -0.0015 | 0.0017 | 0.0209 | 16.0000 | 17.0000 | structural |
| gender | -0.0001 | 0.0001 | 0.0006 | 0.0019 | 0.0115 | 17.0000 | 18.0000 | structural |

## J. What-if sensitivity (association, not causal)

| lever | bill_change_usd | eligible | mean_risk_before | mean_risk_after | mean_change_pts | ci_low_pts | ci_high_pts | change_in_expected_monthly_revenue_lost_usd | rev_ci_low | rev_ci_high |
|---|---|---|---|---|---|---|---|---|---|---|
| Contract: month-to-month -> one year (bill unchanged) | 0.000 | 773 | 0.431 | 0.251 | -18.026 | -18.632 | -17.426 | -9680.656 | -10114.606 | -9266.575 |
| PaymentMethod: electronic check -> bank transfer (automatic) (bill unchanged) | 0.000 | 474 | 0.451 | 0.390 | -6.090 | -6.268 | -5.898 | -2247.982 | -2341.311 | -2149.826 |
| TechSupport: no -> yes, internet customers (bill unchanged) | 0.000 | 702 | 0.419 | 0.415 | -0.446 | -0.562 | -0.328 | -173.422 | -235.184 | -115.804 |
| TechSupport: no -> yes, internet customers (bill rises by add-on price) | 5.049 | 702 | 0.419 | 0.362 | -5.731 | -5.936 | -5.533 | -2968.696 | -3081.312 | -2851.534 |
| OnlineSecurity: no -> yes, internet customers (bill unchanged) | 0.000 | 701 | 0.424 | 0.409 | -1.446 | -1.576 | -1.322 | -700.588 | -762.114 | -639.742 |
| OnlineSecurity: no -> yes, internet customers (bill rises by add-on price) | 5.038 | 701 | 0.424 | 0.356 | -6.730 | -6.963 | -6.495 | -3490.486 | -3623.623 | -3354.775 |
| PaperlessBilling: yes -> no (bill unchanged) | 0.000 | 840 | 0.339 | 0.281 | -5.775 | -5.993 | -5.576 | -3711.879 | -3880.937 | -3550.995 |

## K. Files

Model: models/churn_driver_diagnostic_model.joblib; config: models/final_config.json; scores: reports/modeling/scores.csv; tables: reports/modeling/tables/; charts: reports/modeling/charts/; pipeline: src/pipeline.py (`--train`, `--evaluate`, `--predict`).
