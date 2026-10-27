# Data dictionary

Table `clean.parquet`: **7,043 rows (one per customer), 30 columns.** Raw file columns are listed second.

## Cleaned table (use this)

| column | meaning | type | unit | allowed_values_or_range | share_missing_pct | distinct_values | example | model_input_note |
|---|---|---|---|---|---|---|---|---|
| customerID | Unique account code | object | text id | 7,043 distinct values | 0.00 | 7,043 | 7590-VHVEG | identifier: unique per row, carries no pattern; keep for joining scores back, never as a model input |
| gender | Customer gender as recorded | object | category | Female / Male | 0.00 | 2 | Female | fine as an input, but see hypotheses: no churn difference found; consider fairness review before use |
| SeniorCitizen | 1 if the customer is a senior citizen, else 0 | int64 | 0/1 flag | 0.00 to 1.00 | 0.00 | 2 | 0 | fine |
| Partner | Customer has a partner | object | Yes/No | No / Yes | 0.00 | 2 | Yes | fine |
| Dependents | Customer has dependents (children etc.) | object | Yes/No | No / Yes | 0.00 | 2 | No | fine |
| tenure | Months the customer has been with the company | int64 | months | 0.00 to 72.00 | 0.00 | 73 | 1 | fine, but for churners it is measured up to exit, for stayers up to the snapshot: possible leakage, unclear from this data |
| PhoneService | Customer has home phone service | object | Yes/No | No / Yes | 0.00 | 2 | No | fine; partly overlaps with MultipleLines |
| MultipleLines | Has more than one phone line (No also covers 'no phone service') | object | Yes/No | No / Yes | 0.00 | 2 | No | fine; use with PhoneService |
| InternetService | Type of internet service | object | category | DSL / Fiber optic / No | 0.00 | 3 | DSL | fine |
| OnlineSecurity | Has online security add-on | object | category | No / Yes | 0.00 | 2 | No | fine after cleaning: 'No internet service' repeats InternetService=No |
| OnlineBackup | Has online backup add-on | object | category | No / Yes | 0.00 | 2 | Yes | fine after cleaning (same quirk as OnlineSecurity) |
| DeviceProtection | Has device protection add-on | object | category | No / Yes | 0.00 | 2 | No | fine after cleaning (same quirk) |
| TechSupport | Has tech support add-on | object | category | No / Yes | 0.00 | 2 | No | fine after cleaning (same quirk) |
| StreamingTV | Streams TV through the service | object | category | No / Yes | 0.00 | 2 | No | fine after cleaning (same quirk) |
| StreamingMovies | Streams movies through the service | object | category | No / Yes | 0.00 | 2 | No | fine after cleaning (same quirk) |
| Contract | Contract length | object | category | Month-to-month / One year / Two year | 0.00 | 3 | Month-to-month | fine |
| PaperlessBilling | Bills sent by e-mail, not paper | object | Yes/No | No / Yes | 0.00 | 2 | Yes | fine |
| PaymentMethod | How the customer pays | object | category | Bank transfer (automatic) / Credit card (automatic) / Electronic check / Mailed check | 0.00 | 4 | Electronic check | fine |
| MonthlyCharges | Amount billed per month now | float64 | US dollars per month | 18.25 to 118.75 | 0.00 | 1,585 | 29.85 | fine; also the revenue measure used in this project |
| TotalCharges | Total billed over the customer's life; 11 missing for tenure-0 accounts | float64 | US dollars | 18.80 to 8,684.80 | 0.16 | 6,530 | 29.85 | derived (about tenure x price) and collinear with tenure and MonthlyCharges; handle missing; use with care |
| Churn | Customer left in the observation window | object | Yes/No | No / Yes | 0.00 | 2 | No | TARGET. Never use as input |
| churn_flag | 1 if the customer left, 0 if stayed | int64 | 0/1 flag | 0.00 to 1.00 | 0.00 | 2 | 0 | TARGET (numeric copy of Churn). Never use as input |
| has_internet | 1 if the customer has internet service | int64 | 0/1 flag | 0.00 to 1.00 | 0.00 | 2 | 1 | derived from InternetService: duplicates it; use one or the other |
| n_addons | Count of the six add-ons the customer has | int64 | count 0-6 | 0.00 to 6.00 | 0.00 | 7 | 1 | derived from six columns; do not use together with all six |
| n_protection_addons | Count of security, backup, device protection, tech support the customer has | int64 | count 0-4 | 0.00 to 4.00 | 0.00 | 5 | 1 | derived from four columns; do not use together with them |
| tenure_band | Tenure grouped into bands | object | category (ordered) | 0-6 months / 13-24 months / 25-48 months / 49-72 months / 7-12 months | 0.00 | 5 | 0-6 months | derived from tenure; for reporting; redundant for models that take tenure |
| monthly_charge_band | Monthly price grouped into bands | object | category (ordered) | $30-50 / $50-70 / $70-90 / $90+ / under $30 | 0.00 | 5 | under $30 | derived from MonthlyCharges; for reporting |
| autopay | 1 if paying by bank transfer or credit card automatically | int64 | 0/1 flag | 0.00 to 1.00 | 0.00 | 2 | 0 | derived from PaymentMethod; overlaps with it |
| avg_monthly_spend | Average dollars billed per month of tenure | float64 | US dollars per month | 13.78 to 121.40 | 0.16 | 4,577 | 29.85 | derived from TotalCharges / tenure; missing when tenure is 0; collinear with MonthlyCharges |
| price_vs_history_pct | Current monthly price vs the customer's lifetime average | float64 | percent | -36.44 to 45.11 | 0.16 | 1,923 | 0.0 | derived; missing when tenure is 0; for churners built from totals up to exit: leakage risk, unclear from this data |

## Raw file `data/raw/telco_customer_churn.csv` (for reference)

| column | meaning | type | unit | allowed_values_or_range | share_missing_pct | distinct_values | example | model_input_note |
|---|---|---|---|---|---|---|---|---|
| customerID | Unique account code | object | text id | 7,043 distinct values | 0.00 | 7,043 | 7590-VHVEG | identifier: unique per row, carries no pattern; keep for joining scores back, never as a model input |
| gender | Customer gender as recorded | object | category | Female / Male | 0.00 | 2 | Female | fine as an input, but see hypotheses: no churn difference found; consider fairness review before use |
| SeniorCitizen | 1 if the customer is a senior citizen, else 0 | object | 0/1 flag | 0 / 1 | 0.00 | 2 | 0 | fine |
| Partner | Customer has a partner | object | Yes/No | No / Yes | 0.00 | 2 | Yes | fine |
| Dependents | Customer has dependents (children etc.) | object | Yes/No | No / Yes | 0.00 | 2 | No | fine |
| tenure | Months the customer has been with the company | object | months | 73 distinct values | 0.00 | 73 | 1 | fine, but for churners it is measured up to exit, for stayers up to the snapshot: possible leakage, unclear from this data |
| PhoneService | Customer has home phone service | object | Yes/No | No / Yes | 0.00 | 2 | No | fine; partly overlaps with MultipleLines |
| MultipleLines | Has more than one phone line | object | category | No / No phone service / Yes | 0.00 | 3 | No phone service | fine after cleaning: 'No phone service' repeats PhoneService=No |
| InternetService | Type of internet service | object | category | DSL / Fiber optic / No | 0.00 | 3 | DSL | fine |
| OnlineSecurity | Has online security add-on | object | category | No / No internet service / Yes | 0.00 | 3 | No | fine after cleaning: 'No internet service' repeats InternetService=No |
| OnlineBackup | Has online backup add-on | object | category | No / No internet service / Yes | 0.00 | 3 | Yes | fine after cleaning (same quirk as OnlineSecurity) |
| DeviceProtection | Has device protection add-on | object | category | No / No internet service / Yes | 0.00 | 3 | No | fine after cleaning (same quirk) |
| TechSupport | Has tech support add-on | object | category | No / No internet service / Yes | 0.00 | 3 | No | fine after cleaning (same quirk) |
| StreamingTV | Streams TV through the service | object | category | No / No internet service / Yes | 0.00 | 3 | No | fine after cleaning (same quirk) |
| StreamingMovies | Streams movies through the service | object | category | No / No internet service / Yes | 0.00 | 3 | No | fine after cleaning (same quirk) |
| Contract | Contract length | object | category | Month-to-month / One year / Two year | 0.00 | 3 | Month-to-month | fine |
| PaperlessBilling | Bills sent by e-mail, not paper | object | Yes/No | No / Yes | 0.00 | 2 | Yes | fine |
| PaymentMethod | How the customer pays | object | category | Bank transfer (automatic) / Credit card (automatic) / Electronic check / Mailed check | 0.00 | 4 | Electronic check | fine |
| MonthlyCharges | Amount billed per month now | object | US dollars per month | 1,585 distinct values | 0.00 | 1,585 | 29.85 | fine; also the revenue measure used in this project |
| TotalCharges | Total billed over the customer's life | object | US dollars | 6,530 distinct values | 0.16 | 6,531 | 29.85 | derived: roughly tenure x monthly price; strongly collinear with tenure; stored as text with 11 blanks in the raw file |
| Churn | Customer left in the observation window | object | Yes/No | No / Yes | 0.00 | 2 | No | TARGET. Never use as input |

## Derived columns

Example row is customer 7590-VHVEG. `segment` exists only in the notebook (not in clean.parquet).

| column | formula | built_from | why | expected_direction | motivating_hypothesis | example_7590-VHVEG |
|---|---|---|---|---|---|---|
| churn_flag | 1 if Churn = Yes, else 0 | Churn | Numeric target so averages are churn rates | (target) | All hypotheses | 0 |
| has_internet | 1 if InternetService is not No | InternetService | Keeps internet status after the redundant levels are folded | lower churn (no-internet customers expected to leave less) | H2, H9 (internet type) | 1 |
| n_addons | count of Yes among the six add-ons | six add-on columns | Simple measure of how many extras a customer has | lower churn with more add-ons | H5 (tech support) | 1 |
| n_protection_addons | count of Yes among OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport | four columns | Separates protective extras from streaming extras | lower churn with more protection | H5 (tech support) | 1 |
| tenure_band | 0-6, 7-12, 13-24, 25-48, 49-72 months | tenure | Readable bands for tables and charts | lower churn at longer tenure | H3 (first 12 months) | 0-6 months |
| monthly_charge_band | under $30, $30-50, $50-70, $70-90, $90+ | MonthlyCharges | Same, for price | higher churn at higher bills | H6 (leavers pay more) | under $30 |
| autopay | 1 if PaymentMethod contains 'automatic' | PaymentMethod | Separates automatic from manual payment | lower churn when automatic | H4 (electronic check) | 0 (pays by electronic check) |
| avg_monthly_spend | TotalCharges / tenure (missing when tenure = 0) | TotalCharges, tenure | Average price paid over life; compare to current price | higher churn at higher spend | H6 | 29.85 |
| price_vs_history_pct | 100 x (MonthlyCharges - avg_monthly_spend) / avg_monthly_spend | the two above | How far today's price sits above or below what the customer paid on average | unclear; no prediction made | H6 (price) | 0.0 |
| segment (notebook-only) | Contract + ' / ' + InternetService + ' / ' + (tenure 0-12 or 13+) | Contract, InternetService, tenure | Reporting column for the concentration analysis in 6.6. Built after clean.parquet is saved, so it is NOT in the file | higher churn for month-to-month, fiber, first year | H1, H2, H3 (section 6.6) | Month-to-month / DSL / tenure 0-12 |
