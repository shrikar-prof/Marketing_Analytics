# Cleaning Log

One row per rule applied. 'Rows before/after' counts the number of affected values.

| Rule                                                                    | Table                  |   Rows before |   Rows after | Reason                                                                                                       |
|:------------------------------------------------------------------------|:-----------------------|--------------:|-------------:|:-------------------------------------------------------------------------------------------------------------|
| Fill event name/type nulls with 'None'                                  | calendar               |          7542 |            0 | Null means no event; a string 'None' is safer for categorical encoding.                                      |
| Add d_col column to calendar (d_1, d_2, …) using row position           | calendar               |             0 |         1969 | Problem description states this column is missing from the Nixtla mirror; needed to merge calendar to sales. |
| Sales data: no negatives, no duplicates — no changes applied            | sales_train_evaluation |         30490 |        30490 | Quality audit found no actionable issues.                                                                    |
| sell_prices: no zero prices, no missing sell_price — no changes applied | sell_prices            |       6841121 |      6841121 | Quality audit found no actionable issues.                                                                    |