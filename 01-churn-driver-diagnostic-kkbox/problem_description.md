# Project 01: Churn Driver Diagnostic

## Problem
A subscription business (the demo instance is a telecom and internet provider with 7,043 accounts) loses about 27% of its customers per observation window, taking roughly 31% of monthly recurring revenue with them. Leadership does not know whether churn is a pricing problem, a product problem or a customer-mix problem, or where a retention budget should go first.

## Question to answer
Which customer characteristics most strongly predict churn, how much revenue sits in the highest-risk groups, and what is the smallest intervention that captures most of the upside?

## Deliverable expected
A consulting memo (situation, question, approach, recommendation, measurable impact), ranked drivers with effect sizes, a risk score per customer, revenue at risk by segment, and an offer sheet (input, timeline, deliverable, price).

## Data

### IBM Telco Customer Churn (primary)
- Publisher: IBM, sample data for Cognos Analytics and Watson Studio tutorials. Fictional California telecom, one fiscal quarter.
- Grain: one row per customer (snapshot). 7,043 rows, 21 columns. Target column `Churn` (Yes/No), 26.5% Yes.
- Columns: customerID, gender, SeniorCitizen, Partner, Dependents, tenure, PhoneService, MultipleLines, InternetService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies, Contract, PaperlessBilling, PaymentMethod, MonthlyCharges, TotalCharges, Churn.
- Known quirks: `TotalCharges` is stored as text with 11 blank values (all tenure-0 accounts); six add-on columns carry a redundant "No internet service" level.
- File: `data/raw/telco_customer_churn.csv`

```
curl -L -o data/raw/telco_customer_churn.csv \
  https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv
```
Mirrors: Kaggle `blastchar/telco-customer-churn`, Mendeley Data `phsxg9ssrf`.

### KKBox churn challenge transactions (real subscription data, optional upgrade)
- Publisher: KKBox via Kaggle, WSDM Cup 2018. Mirror on Mendeley Data `mv3f8bdrvy`, CC BY 4.0.
- Grain: one row per subscription transaction, March 2017. Columns: msno, payment_method_id, payment_plan_days, plan_list_price, actual_amount_paid, is_auto_renew, transaction_date, membership_expire_date, is_cancel.
- The mirror is truncated at 1,048,575 rows (Excel's limit). The full competition data (members, daily user logs, churn labels) needs Kaggle credentials in `~/.kaggle/kaggle.json`: `kaggle competitions download -c kkbox-churn-prediction-challenge`.
- Churn definition in the competition: no new transaction within 30 days of `membership_expire_date`.
- File: `data/raw/kkbox_transactions_v2.csv`

```
curl -L -C - --retry 5 -o data/raw/kkbox_transactions_v2.csv \
  "https://data.mendeley.com/public-files/datasets/mv3f8bdrvy/files/503be31b-1630-4732-8ad7-f07856aae192/file_downloaded"
```
