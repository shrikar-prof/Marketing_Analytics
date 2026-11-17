# Cleaning Log — Strategy Teardowns

|   step | rule                                       | input_cols                        | formula                                  |   rows_before |   rows_after | notes                                     |
|-------:|:-------------------------------------------|:----------------------------------|:-----------------------------------------|--------------:|-------------:|:------------------------------------------|
|      1 | Add op_margin_pct to Five Below            | operating_income_usd, revenue_usd | operating_income_usd / revenue_usd × 100 |             8 |            8 | No rows changed; new column added.        |
|      2 | Add rev_per_store_m to Five Below          | revenue_usd, stores_eop           | revenue_usd / stores_eop / 1e6           |             8 |            8 | No rows changed.                          |
|      3 | Add rev_yoy_pct to Five Below              | revenue_usd                       | pct_change(1) × 100                      |             8 |            8 | FY2018 is NaN (no prior year).            |
|      4 | Add covid_affected flag to Five Below      | fiscal_year                       | fiscal_year in {2020, 2021}              |             8 |            8 | 2 rows flagged.                           |
|      5 | Add rev_yoy_pct and arm_yoy_pct to Netflix | revenue_usd_m, arm_usd            | pct_change(periods=4) × 100              |            25 |           25 | First 4 rows NaN (no year-prior quarter). |

_No rows were dropped. All transformations are reversible additions of new columns._
