# Data Dictionary

Generated automatically from the exploration notebook.


## Table: sales_train_evaluation

| Column       | Plain meaning                                                                         | Type   | Unit               | Allowed / range                                                               | % missing   |   # distinct | Example       | Usable     | Note                                                                           |
|:-------------|:--------------------------------------------------------------------------------------|:-------|:-------------------|:------------------------------------------------------------------------------|:------------|-------------:|:--------------|:-----------|:-------------------------------------------------------------------------------|
| item_id      | ID of the specific item (SKU). Use as a grouping key, not a raw numeric input.        | object | text               | ['HOBBIES_1_001', 'FOODS_2_210', 'FOODS_2_201', 'FOODS_2_202', 'FOODS_2_203'] | 0.0%        |         3049 | HOBBIES_1_001 | identifier | ID of the specific item (SKU). Use as a grouping key, not a raw numeric input. |
| dept_id      | Department: 7 departments. Encode as category for modelling.                          | object | text               | ['FOODS_3', 'HOUSEHOLD_1', 'HOUSEHOLD_2', 'HOBBIES_1', 'FOODS_2']             | 0.0%        |            7 | HOBBIES_1     | encode     | Department: 7 departments. Encode as category for modelling.                   |
| cat_id       | Category: FOODS, HOBBIES, HOUSEHOLD. Encode as category.                              | object | text               | ['FOODS', 'HOUSEHOLD', 'HOBBIES']                                             | 0.0%        |            3 | HOBBIES       | encode     | Category: FOODS, HOBBIES, HOUSEHOLD. Encode as category.                       |
| store_id     | Store ID: 10 stores. Encode as category.                                              | object | text               | ['CA_1', 'CA_2', 'CA_3', 'CA_4', 'TX_1']                                      | 0.0%        |           10 | CA_1          | encode     | Store ID: 10 stores. Encode as category.                                       |
| state_id     | US state: CA, TX, WI. Encode as category.                                             | object | text               | ['CA', 'TX', 'WI']                                                            | 0.0%        |            3 | CA            | encode     | US state: CA, TX, WI. Encode as category.                                      |
| d_1 … d_1941 | Units sold on that calendar day (integer ≥ 0). Zero may mean zero demand OR stockout. | int64  | units sold per day | 0 – 763                                                                       | 0.0%        |          419 | 1             | TARGET     | Zero-inflation: 68.0% of all item-day cells are zero.                          |


## Table: calendar

| Column       | Plain meaning                                                          | Type   | Unit   | Allowed / range                                                           | % missing   |   # distinct | Example    | Usable     | Note   |
|:-------------|:-----------------------------------------------------------------------|:-------|:-------|:--------------------------------------------------------------------------|:------------|-------------:|:-----------|:-----------|:-------|
| date         | Calendar date in YYYY-MM-DD format.                                    | object | varies | ['2011-01-29', '2011-01-30', '2011-01-31', '2011-02-01', '2011-02-02']    | 0.0%        |         1969 | 2011-01-29 | identifier |        |
| wm_yr_wk     | Walmart fiscal year-week code. Links to sell_prices.                   | int64  | varies | [11101, 11102, 11103, 11104, 11105]                                       | 0.0%        |          282 | 11101      | encode     |        |
| weekday      | Day-of-week name (Monday…Sunday).                                      | object | varies | ['Monday', 'Saturday', 'Sunday', 'Tuesday', 'Wednesday']                  | 0.0%        |            7 | Saturday   | encode     |        |
| wday         | Day-of-week number (1=Saturday … 7=Friday, Walmart convention).        | int64  | varies | [1, 2, 3, 4, 5]                                                           | 0.0%        |            7 | 1          | encode     |        |
| month        | Calendar month number 1–12.                                            | int64  | varies | [1, 2, 3, 4, 5]                                                           | 0.0%        |           12 | 1          | encode     |        |
| year         | Calendar year.                                                         | int64  | varies | [2011, 2012, 2013, 2014, 2015]                                            | 0.0%        |            6 | 2011       | encode     |        |
| event_name_1 | Primary event name on this day (e.g., SuperBowl). Blank when no event. | object | varies | ['LentStart', 'LentWeek2', 'PresidentsDay', 'SuperBowl', 'ValentinesDay'] | 91.8%       |           30 | SuperBowl  | encode     |        |
| event_type_1 | Type of primary event (Sporting, Cultural, National, Religious).       | object | varies | ['Cultural', 'National', 'Religious', 'Sporting']                         | 91.8%       |            4 | Sporting   | encode     |        |
| event_name_2 | Secondary event name (overlapping events are rare).                    | object | varies | ['Cinco De Mayo', 'Easter', "Father's day", 'OrthodoxEaster']             | 99.7%       |            4 | Easter     | encode     |        |
| event_type_2 | Type of secondary event.                                               | object | varies | ['Cultural', 'Religious']                                                 | 99.7%       |            2 | Cultural   | encode     |        |
| snap_CA      | 1 if California SNAP (food-stamp) benefit day, else 0.                 | int64  | varies | [0, 1]                                                                    | 0.0%        |            2 | 0          | encode     |        |
| snap_TX      | 1 if Texas SNAP benefit day, else 0.                                   | int64  | varies | [0, 1]                                                                    | 0.0%        |            2 | 0          | encode     |        |
| snap_WI      | 1 if Wisconsin SNAP benefit day, else 0.                               | int64  | varies | [0, 1]                                                                    | 0.0%        |            2 | 0          | encode     |        |


## Table: sell_prices

| Column     | Plain meaning                                                                      | Type    | Unit   | Allowed / range   | % missing   |   # distinct | Example       | Usable     | Note   |
|:-----------|:-----------------------------------------------------------------------------------|:--------|:-------|:------------------|:------------|-------------:|:--------------|:-----------|:-------|
| store_id   | Store ID; foreign key to sales.                                                    | object  | text   | 10                | 0.0%        |           10 | CA_1          | encode     |        |
| item_id    | Item ID; foreign key to sales.                                                     | object  | text   | 3049              | 0.0%        |         3049 | HOBBIES_1_001 | identifier |        |
| wm_yr_wk   | Walmart fiscal week; foreign key to calendar.                                      | int64   | text   | 282               | 0.0%        |          282 | 11325         | encode     |        |
| sell_price | Unit sell price (USD) for that item in that store-week. Missing before item debut. | float64 | USD    | 0.01 – 107.32     | 0.0%        |         1048 | 9.58          | encode     |        |


## Derived Columns (created during cleaning / exploration)

Columns created by this notebook that do not exist in the raw files.  Every row gives: name, formula, input columns, reason, motivating finding or hypothesis, expected direction of effect, and an example value.

| Name | Formula / Rule | Input columns | Why needed | Motivating finding / hypothesis | Expected direction | Example |
|------|---------------|--------------|-----------|--------------------------------|-------------------|---------|
| date | calendar.csv row index → d_{n} → lookup calendar.date | d_* col name | Converts wide day-index to a real calendar date for time-series plots | All time-based findings (Findings 1–5) | Increases monotonically | d_1 → 2011-01-29 |
| week_of_year | pd.to_datetime(date).dt.isocalendar().week | date | Captures yearly seasonal cycles without requiring full date parsing | Finding 5 (Q4 peaks visible in monthly trend) | Cyclic 1–52 | d_1 → week 4 |
| zero_flag | 1 if units == 0 else 0 | units | Marks zero-demand days for zero-inflation analysis and CV computation | Finding 1 (structural zero inflation differs by category) | Higher for HOBBIES series | 0 units → 1 |
| item_total_units | sum(d_1..d_1941) per series | d_* | Classifies items as fast or slow movers for the Lorenz-curve analysis | Finding 5 (top 20% of series drive ~70% of volume) | Higher for FOODS items | 1,234 units |
| cv | std(units on non-zero days) / mean(units on non-zero days) per series | d_* | Measures demand lumpiness beyond the zero rate; used in H5 | H5 (FOODS vs HOUSEHOLD volatility comparison) | HOBBIES > HOUSEHOLD > FOODS expected | 2.3 |
| zero_rate | (count of d_* == 0) / 1941 per series | d_* | Fraction of item-days with no sales; primary intermittency metric | Finding 1; H1 (FOODS vs HOBBIES zero rate) | HOBBIES > HOUSEHOLD > FOODS | 0.83 for a typical HOBBIES series |
| nonzero_mean | mean(units) restricted to days where units > 0, per series | d_* | Average demand when the item actually sells; excludes structural zeros from mean | Finding 2 (SNAP lift measured on active-sale days) | Higher for FOODS than HOBBIES | 1.4 units |
| cv_nonzero | std(units on non-zero days) / mean(units on non-zero days) per series | d_* | Coefficient of variation on active-sale days; isolates within-active-day volatility from zero-day frequency | H5; chart 11 | Lower for FOODS; higher for HOBBIES | 1.1 |
| total_revenue_approx | total_units * latest_price (most recent sell_price per item × store) | total_units, sell_prices.csv | Order-of-magnitude dollar-value estimate to rank categories by financial importance | Finding 5 (concentration of value in top series) | FOODS dominates dollar share | $3,210 for a typical FOODS series |
| log_price | log(1 + latest_price) | latest_price | Log transformation normalises the right-skewed price distribution for correlation analysis | Finding 7h (price vs demand; Pearson r = −0.375) | Negatively correlated with log_mean_demand | log(1 + 2.98) = 1.37 |
| log_mean_demand | log(1 + mean(units across all days including zeros)) per series | d_* | Log transformation of average demand for correlation with log_price | Finding 7h | Negatively correlated with log_price | log(1 + 0.8) = 0.59 |