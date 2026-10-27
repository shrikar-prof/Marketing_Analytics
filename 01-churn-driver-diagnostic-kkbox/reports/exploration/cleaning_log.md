# Cleaning log

Input 7,043 rows, 21 columns. Output `clean.parquet`: 7043 rows, 30 columns. No row was dropped.

| rule | rows_with_problem_before | rows_with_problem_after | note |
|---|---|---|---|
| R1 strip stray spaces in all text columns | 11 | 0 | Blank TotalCharges cells become empty text |
| R2 TotalCharges: text to number; blanks to missing | 11 | 11 | Problem moves from 'blank text' to 'missing number': 11 tenure-0 accounts. Not filled. |
| R3 tenure, MonthlyCharges, SeniorCitizen to numeric types | 21,129 | 0 | Values unchanged; 3 columns x 7,043 rows re-typed |
| R4 six add-ons: fold 'No internet service' into 'No' | 9,156 | 0 | 9,156 cells = 1,526 customers x 6 columns; has_internet keeps the information |
| R5 MultipleLines: fold 'No phone service' into 'No' | 682 | 0 | PhoneService column keeps the information |
| R6 drop fully duplicated rows | 0 | 0 | None found |
| R7 add churn_flag (1 = left) | 0 | 0 | No odd labels; Churn text kept for reference |

## Derived columns

| column | meaning | model_input_note |
|---|---|---|
| churn_flag | 1 if the customer left, 0 if stayed | TARGET (numeric copy of Churn). Never use as input |
| has_internet | 1 if the customer has internet service | derived from InternetService: duplicates it; use one or the other |
| n_addons | Count of the six add-ons the customer has | derived from six columns; do not use together with all six |
| n_protection_addons | Count of security, backup, device protection, tech support the customer has | derived from four columns; do not use together with them |
| tenure_band | Tenure grouped into bands | derived from tenure; for reporting; redundant for models that take tenure |
| monthly_charge_band | Monthly price grouped into bands | derived from MonthlyCharges; for reporting |
| autopay | 1 if paying by bank transfer or credit card automatically | derived from PaymentMethod; overlaps with it |
| avg_monthly_spend | Average dollars billed per month of tenure | derived from TotalCharges / tenure; missing when tenure is 0; collinear with MonthlyCharges |
| price_vs_history_pct | Current monthly price vs the customer's lifetime average | derived; missing when tenure is 0; for churners built from totals up to exit: leakage risk, unclear from this data |
