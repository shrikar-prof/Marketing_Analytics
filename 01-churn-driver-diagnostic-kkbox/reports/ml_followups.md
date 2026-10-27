# Follow-up answers

Source: `reports/exploration/clean.parquet` joined to `reports/customer_risk_scores.csv` by customerID (pooled scores: out-of-fold for training rows, held-out for test rows). Method: group counts and means, no modeling. Churn rate = share of customers in the cell who left. Money is monthly bill, $ per month. Asked by the growth strategist.

**Q1. Month-to-month fiber by payment method (2,128 customers)**

| PaymentMethod | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|
| Bank transfer (automatic) | 327 | 45.6 | 88.25 |
| Credit card (automatic) | 293 | 41.6 | 87.97 |
| Electronic check | 1307 | 60.4 | 87.18 |
| Mailed check | 201 | 50.7 | 82.59 |

**Q2. One/two-year contract, tenure 0-12 months (tenure <= 12), fiber vs DSL**

| Contract | InternetService | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|---|
| One year | DSL | 42 | 16.7 | 53.41 |
| One year | Fiber optic | 7 | 28.6 | 95.04 |
| Two year | DSL | 18 | 0.0 | 58.17 |

**Q3. Month-to-month fiber by TechSupport**

| TechSupport | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|
| No | 1796 | 57.5 | 85.49 |
| Yes | 332 | 38.9 | 95.28 |

**Q4. Top 1,060 contract-lever customers (ranked by modeled_saving_if_one_year_contract_usd_per_month in customer_risk_scores.csv)**

n=1060; electronic check 61.7%; no TechSupport 87.2% (0 of them have no internet); SeniorCitizen 25.5%. Whole base for comparison: e-check 33.6%, no TechSupport 71.0%, senior 16.2%.

**Q5. Held-out test (1,409 customers, 374 leavers), flagged = score >= cutoff**

| cutoff | flagged | true_leavers_flagged | bill_of_flagged_leavers_usd_per_month | bill_of_flagged_stayers_usd_per_month |
|---|---|---|---|---|
| 0.3 | 531.0 | 286.0 | 21655.6 | 18867.9 |
| 0.4 | 422.0 | 246.0 | 19002.7 | 13719.5 |
| 0.5 | 299.0 | 200.0 | 15370.0 | 7773.75 |
| 0.6 | 197.0 | 142.0 | 10999.95 | 4500.1 |

**Q6. SeniorCitizen share.** Pooled top-20% risk group (n=1409): 30.7% senior (433 customers). Whole base (n=7,043): 16.2% (1142).


---

# Follow-up answers, round 2

Same source and method as round 1: group counts and means, no modeling. Tenure 0-2 means tenure <= 2 months. Churn rate = share of the cell who left. Bill is $ per month.

**R2-Q1. Month-to-month fiber, tenure 0-12 months (n=916)**

| pay | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|
| Automatic (bank + card) | 162 | 72.2 | 83.03 |
| Electronic check | 631 | 71.2 | 82.31 |
| Mailed check | 123 | 62.6 | 79.65 |

**R2-Q2. Month-to-month fiber by tenure band (months; 13+ shown for reference)**

| band | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|
| 0-2 | 344 | 80.5 | 78.46 |
| 3-6 | 275 | 66.2 | 83.34 |
| 7-12 | 297 | 62.0 | 85.1 |
| 13+ | 1212 | 42.8 | 90.76 |

**R2-Q3. Month-to-month customers by pooled score band (n=3875; out-of-fold for training rows, held-out for test rows)**

| score_band | customers | churn_rate_pct | mean_bill_usd |
|---|---|---|---|
| <0.3 | 1327 | 18.5 | 47.18 |
| 0.3-0.5 | 1042 | 37.3 | 72.6 |
| 0.5-0.7 | 908 | 60.1 | 78.19 |
| >=0.7 | 598 | 79.3 | 80.33 |
