# Hand-off to the model builder

## Files
- Cleaned table: `reports/exploration/clean.parquet` (7,043 rows, one per customer, 30 columns).
- Column meanings and notes: `reports/exploration/data_dictionary.md` and `.csv`.
- The KKBox file is not in the table (no churn label).

## Target
- `churn_flag` (1 = customer left, 0 = stayed). Rate 26.5% (1,869 of 7,043). It is the numeric copy of `Churn` (Yes/No).

## Columns to exclude, and why
| Column | Why |
|---|---|
| `customerID` | Identifier. Keep only to join scores back to customers. |
| `Churn` | Text copy of the target. |
| `tenure_band`, `monthly_charge_band` | Reporting bands built from `tenure` and `MonthlyCharges`. Redundant. |
| `TotalCharges`, `avg_monthly_spend`, `price_vs_history_pct` | Built from lifetime billing. For leavers the total stops at exit, so these can carry the outcome. Drop from the first model; add back only after a leakage check. `TotalCharges` has 11 missing values (tenure-0 accounts). |
| `has_internet` or `InternetService` | Same information. Use one. |
| `n_addons`, `n_protection_addons` | Counts of columns already present. Use the counts or the originals, not both. |

## Suggested inputs
- Categorical, need encoding (one-hot; `Contract` can also be coded as ordered 0/1/2): gender, Partner, Dependents, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod.
- Numeric: tenure, MonthlyCharges, SeniorCitizen, has_internet, n_addons, n_protection_addons, autopay. `SeniorCitizen`, `has_internet`, `autopay` are already 0/1.
- Add-on columns now hold only Yes/No. Customers with no internet are "No" on all six; keep `InternetService` so the model can tell "no internet" from "declined the add-on".

## Validation design
1. Hold out a random 1,409-customer test set (20%), stratified on `churn_flag`, seed 42. It will hold about 374 leavers. Touch it once, at the end.
2. On the other 80%, use repeated stratified 5-fold cross-validation (5 repeats) to choose and tune.
3. Why: one row per customer, so rows are independent and no grouping is needed. There is no date, so a time-based split is impossible. Stratifying keeps 26.5% leavers in every fold. With about 374 leavers in the test set, a rate estimated on it is uncertain by about +/- 5 points, so report intervals, not single numbers.
4. Any group ranking or threshold must be set on training folds only. The segment ranking in this exploration used all customers and is optimistic.

## Known pitfalls
- **Collinearity:** tenure and TotalCharges (r = 0.83); MonthlyCharges and avg_monthly_spend (r = 1.00); n_addons and n_protection_addons (r = 0.91); add-ons and InternetService.
- **Leakage (unclear from this data):** tenure and billing totals for leavers may be measured at exit. If so, a model learns "short tenure" partly because the customer already left. Ask the data owner.
- **Small cells:** segments with under 100 customers: One year | Fiber optic | tenure 0-12, One year | DSL | tenure 0-12, One year | No | tenure 0-12, Two year | DSL | tenure 0-12, Two year | No | tenure 0-12. Do not report rates for them. Two-way cells of tenure band by contract also have 5 small cells.
- **No customers with tenure 0 left** (11 accounts, all with blank TotalCharges). Do not over-read them.
- **Fairness:** gender shows no churn link; `SeniorCitizen` does (V = 0.15). Check the policy before using age-related fields to decide who gets offers.
- **Overlap of drivers:** contract, tenure, internet type, payment method and price overlap. Single-column effects in this exploration will shrink when combined in a model.

## Business metric the model should be judged on
- **Primary:** share of lost monthly revenue captured in the top 20% of customers by risk score, on the held-out set. Reference to beat: the simple contract x internet x tenure ranking captures about 52% at 20% of customers (in-sample, so a fair model must be compared on held-out data too). Total lost monthly revenue to capture: $139,131.
- **Secondary:** precision (share of flagged customers who really leave) and recall (share of leavers flagged) at the same cut-off; area under the precision-recall curve; calibration (do customers scored 40% leave about 40% of the time?).
- **Decision value:** `monthly revenue kept = (leavers contacted) x (save rate) x (average bill $74.44)` minus `(customers contacted) x (cost per offer)`. Save rate and offer cost are not in the data; they must come from the client or a test.
