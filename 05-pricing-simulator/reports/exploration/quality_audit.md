# Quality Audit — 05 Pricing Simulator

Transaction table: 524,950 rows × 12 columns

| Issue                |   Count | Description                                   | Action                                                            |
|:---------------------|--------:|:----------------------------------------------|:------------------------------------------------------------------|
| Missing PRICE        |      23 | 23 rows (0.004%)                              | Drop rows — too few to impute                                     |
| Missing BASE_PRICE   |     185 | 185 rows (0.035%)                             | Drop rows — too few to impute                                     |
| PRICE = 0            |       1 | Implausible free product                      | Drop rows                                                         |
| PRICE > BASE_PRICE   |    4906 | 4,906 rows (0.93%)                            | Flag as DISCOUNT_PCT < 0; keep for analysis                       |
| Multiple promo flags |   23414 | Some rows have Feature+Display simultaneously | Assign priority: Feature+Display > Feature > Display > TPR > None |
| UNITS = 0            |       5 | 5 rows (0.00%)                                | Keep; log(UNITS+1) handles zeros                                  |
| SPEND inconsistency  |       0 | 0 rows; likely rounding                       | Exclude SPEND from modelling; use PRICE×UNITS                     |
| Full-row duplicates  |       0 | None found                                    | No action needed                                                  |

## Notes
- PRICE > BASE_PRICE rows kept; interpreted as short price-increase weeks.
- SPEND column excluded from all modelling to prevent outcome leakage.
- Zero-unit rows kept; log(UNITS+1) handles them.
