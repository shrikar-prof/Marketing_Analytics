# Quality audit

File audited: `data/raw/telco_customer_churn.csv`, 7,043 rows, 21 columns. Rows are customers.

## Issues found and what we did

| issue | rows | pct_of_7043 | what_it_is | action | why |
|---|---|---|---|---|---|
| TotalCharges stored as text | 7,043 | 100.00 | Money column read as text because of blank entries | Convert to number | Needed for any arithmetic |
| Blank TotalCharges | 11 | 0.16 | Cell holds spaces, not a number; hidden because it is not an empty cell | Set to missing (not zero); keep a note | We do not know the bill was zero; see tenure check |
| Duplicate rows apart from the id | 22 | 0.31 | Different customers with identical attributes | Keep: these are plausible with only 21 coarse columns | Dropping them would delete real customers |
| OnlineSecurity = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| OnlineBackup = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| DeviceProtection = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| TechSupport = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| StreamingTV = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| StreamingMovies = 'No internet service' (redundant level) | 1,526 | 21.67 | Repeats InternetService = No; it is not a separate fact | Fold into 'No'; keep has_internet | Avoids a duplicate level; internet status stays in one column |
| tenure = 0 customers | 11 | 0.16 | Accounts with no months of tenure | Keep | They are real customers; all have blank TotalCharges |
| TotalCharges far from tenure x MonthlyCharges (outside 0.5x to 1.5x) | 2 | 0.03 | Lifetime bill differs a lot from months x current price; price changes or discounts could explain it, unclear from this data | Keep; flag collinearity | Not an error, but the columns are tightly linked |

## Checks that passed (zero rows)

| issue | what_it_is |
|---|---|
| Leading/trailing spaces in text | Text values with stray spaces (excluding fully blank cells counted above) |
| Duplicate full rows | Identical rows |
| tenure outside 0-72 | Months outside the stated 0-72 span |
| MonthlyCharges not in 0-200 | Implausible monthly price |
| SeniorCitizen not 0 or 1 | Flag outside 0/1 |
| MultipleLines = 'No phone service' but PhoneService = Yes | Contradiction |
| PhoneService = No but MultipleLines not 'No phone service' | Contradiction |
| Churn labels not Yes/No | Odd outcome label |

## Columns fully decided by other columns

- `MultipleLines` determines `PhoneService`
- In the raw file, the level 'No internet service' of each of the six add-on columns appears exactly when InternetService = No (checked by assertion above), so it repeats InternetService.

## Money check

TotalCharges divided by tenure x MonthlyCharges has a median of 1.00 (5th to 95th percentile 0.92 to 1.07) across the 7,032 customers with tenure above 0. Correlation of tenure with TotalCharges is 0.83. They carry nearly the same information.

## What we could not check

- Whether the 11 blank TotalCharges are truly zero bills: unclear from this data.
- Whether tenure for churners is measured at exit while stayers are measured at the snapshot date: unclear from this data.
- Whether the figures are real: the source is IBM's fictional sample dataset.

## KKBox transactions (profiled only)

1,048,575 rows, 906,706 distinct members, no churn label, 0 fully duplicated rows, 15,723 transactions with amount paid 0 (1.5% of 1,048,575), 3,745 with expiry before the transaction date. Not cleaned and not part of clean.parquet.
