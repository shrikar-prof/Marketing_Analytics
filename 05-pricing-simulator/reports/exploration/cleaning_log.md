# Cleaning Log — 05 Pricing Simulator

Raw rows: 538,643  |  Clean rows: 538,435

| Rule                                                                        |   Rows Before |   Rows Affected |   Rows After |
|:----------------------------------------------------------------------------|--------------:|----------------:|-------------:|
| Drop missing PRICE or BASE_PRICE                                            |        538643 |             208 |       538435 |
| Add DISCOUNT_PCT; cap negative discounts at 0                               |        538435 |               0 |       538435 |
| Add PROMO_TYPE (priority: Feature+Display > Feature > Display > TPR > None) |        538435 |               0 |       538435 |
| Add LOG_UNITS = log(UNITS + 1)                                              |        538435 |               0 |       538435 |
| Add LOG_PRICE = log(PRICE); 1 rows with PRICE≤0 set to NaN                  |        538435 |               1 |       538435 |

All derived columns are documented in `data_dictionary.md`.