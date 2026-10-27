# Project 03: Demand Forecast for Inventory Planning

## Problem
A general-merchandise retailer replenishes stores on a rule of thumb: order what sold the same weekday over the last four weeks, plus a buffer. About half of all item-days sell zero units, so demand is lumpy and the buffer is set generously. Operations suspects the store carries too much of the slow items and runs out of the fast ones.

## Question to answer
Can a statistical forecast beat the current rule at the item-day level, and what is the improvement worth in inventory dollars and lost sales at a fixed service target?

## Deliverable expected
Forecast accuracy by category against the current rule and a naive baseline, an item-level 28-day forecast, a replenishment simulation that converts forecast error into stock dollars and lost sales at a stated service level, policy recommendations, and an offer sheet.

## Data

### M5 Forecasting competition (Walmart), Nixtla public mirror
Daily unit sales for 3,049 items in 10 stores across California, Texas and Wisconsin, 2011-01-29 to 2016-06-19 (1,941 days), with prices and a calendar.

| File | Content |
|---|---|
| sales_train_evaluation.csv | 30,490 rows (item × store), columns item_id, dept_id, cat_id, store_id, state_id, d_1 … d_1941 (units per day) |
| sales_train_validation.csv | Same, through d_1913 |
| sell_prices.csv | store_id, item_id, wm_yr_wk, sell_price (weekly price; absent before an item is on sale) |
| calendar.csv | date, wm_yr_wk, weekday, wday, month, year, event_name_1/2, event_type_1/2, snap_CA, snap_TX, snap_WI. This mirror lacks the `d` column: day index = row number + 1, d_1 = 2011-01-29 |
| weights_validation.csv, weights_evaluation.csv | Dollar-sales weights per series and aggregation level (Level12 = item × store) for the WRMSSE metric |
| sales_test_validation.csv, sales_test_evaluation.csv | Actuals for d_1914 to d_1941 and d_1942 to d_1969 |

Hierarchy: 3 categories (FOODS, HOBBIES, HOUSEHOLD), 7 departments, 3 states, 10 stores. Competition metric: RMSSE per series, weighted by dollar sales. Known limitation: zero sales are indistinguishable from stockouts; there are no stockout flags.

Files: `data/raw/m5.zip`, unzipped to `data/raw/m5/`

```
curl -L --retry 3 -o data/raw/m5.zip https://github.com/Nixtla/m5-forecasts/raw/main/datasets/m5.zip
unzip -o -q data/raw/m5.zip -d data/raw/m5
```
Original: Kaggle `m5-forecasting-accuracy` (competition rules apply; analysis fine, do not re-host the data).

### Alternative for a second industry (not downloaded)
Corporación Favorita (Kaggle `favorita-grocery-sales-forecasting`): 54 Ecuadorian grocery stores, ~4,100 items, 2013 to 2017, with promotions, holidays, oil price. Needs Kaggle credentials.
