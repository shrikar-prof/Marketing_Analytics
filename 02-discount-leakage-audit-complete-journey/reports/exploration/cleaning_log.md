# Cleaning Log

| Step | Rows before | Rows after | Rule |
|---|---|---|---|
| Raw transactions | 1,469,307 | 1,469,307 | Baseline |
| Drop exact duplicates | 1,469,307 | 1,469,307 | Exact-duplicate rows removed |
| Exclude zero/negative sales_value | 1,469,307 | 1,458,081 | sales_value > 0 |
| Exclude zero-quantity lines | 1,458,081 | 1,458,032 | quantity > 0 |
| Join product attributes (left join) | 1,458,032 | 1,458,032 | Left join on product_id; 32 rows have no department |
| Flag FUEL lines | 1,458,032 | 1,458,032 | 12,997 FUEL lines flagged; retained but excluded from unit analyses |

## Derived Columns Added

total_disc, list_revenue, disc_rate, retailer_disc, mfr_disc, is_fuel
