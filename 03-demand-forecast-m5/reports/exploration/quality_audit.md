# Quality Audit

Every check that found something is listed below.  CRITICAL = must fix before modelling. MINOR = noted, minor impact. INFO = background fact.

| Table                  | Column             | Issue                                                        |    Count | Pct      | Severity   | Action                                                                       |
|:-----------------------|:-------------------|:-------------------------------------------------------------|---------:|:---------|:-----------|:-----------------------------------------------------------------------------|
| calendar               | event_name_1       | Missing values                                               |     1807 | 91.8%    | MINOR      | event_name/type nulls mean no event that day — replace with 'None'.          |
| calendar               | event_type_1       | Missing values                                               |     1807 | 91.8%    | MINOR      | event_name/type nulls mean no event that day — replace with 'None'.          |
| calendar               | event_name_2       | Missing values                                               |     1964 | 99.7%    | MINOR      | event_name/type nulls mean no event that day — replace with 'None'.          |
| calendar               | event_type_2       | Missing values                                               |     1964 | 99.7%    | MINOR      | event_name/type nulls mean no event that day — replace with 'None'.          |
| sales_train_evaluation | d_* (day cols)     | Negative unit sales                                          |        0 | 0.0%     | NONE       | None needed (zero negatives found).                                          |
| sales_train_evaluation | item_id + store_id | Duplicate key rows                                           |        0 | 0.0%     | NONE       | None needed.                                                                 |
| calendar               | date               | Date range check                                             |        1 | MISMATCH | CRITICAL   | Range 2011-01-29 to 2016-06-19 — investigate.                                |
| sell_prices ↔ calendar | wm_yr_wk           | Price weeks not in calendar                                  |        0 | 0.0%     | MINOR      | All price weeks found in calendar.                                           |
| sales_train_evaluation | d_* (day cols)     | Zero-unit-sales rate (structural zeros / possible stockouts) | 40241819 | 68.0%    | INFO       | High zero rate is expected for lumpy retail demand; model must handle zeros. |
| sell_prices            | sell_price         | Price range $0.01–$107.32; zero-price rows                   |        0 | 0.0%     | MINOR      | No zero prices found.                                                        |