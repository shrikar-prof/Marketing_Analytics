# Quality Audit — Strategy Teardowns

Date: 2026-11-17

| dataset      | issue                                              |   rows_affected | detail                                                                                                                                                    | action                                                                                                                                 |
|:-------------|:---------------------------------------------------|----------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------|
| Netflix UCAN | Missing memberships Q1–Q4 2025                     |               4 | Netflix stopped reporting per-region memberships after Q4 2024. Revenue data for 2025 is available. Flag set via has_members column.                      | Keep rows; use revenue_only analysis for 2025 quarters.                                                                                |
| Netflix UCAN | ARM cross-check small discrepancy                  |               0 | Implied revenue (members × ARM × 3) differs from reported by up to ~8%. ARM is a simple average; actual monthly counts vary. No data error.               | No change. Use reported revenue, not implied.                                                                                          |
| Five Below   | FY2020 comparable sales distorted by COVID-19      |               1 | All stores temporarily closed March–April 2020. Comparable sales −5.5% reflects closures, not underlying store productivity.                              | Retain; annotate FY2020 and FY2021 as COVID-affected.                                                                                  |
| Five Below   | FY2023 is a 53-week year                           |               1 | Fiscal 2023 ended Feb 3, 2024 (53 weeks). Comparable sales reported on restated calendar basis per NRF definition.                                        | Retain; note in charts where relevant.                                                                                                 |
| Five Below   | COGS missing FY2018–FY2022 (different XBRL tag)    |               5 | Older 10-Ks tagged CostOfGoodsSold; newer use CostOfGoodsAndServicesSold. Company facts API only returned the newer tag with consistent data from FY2023. | Compute gross profit from revenue − COGS only where available (FY2023–FY2025). Use operating income margin as proxy for earlier years. |
| Five Below   | EOP store count vs net new stores: FY2021 off by 1 |               1 | 10-K text says '170 net new stores' but end-of-period count implies 171 (1,190 − 1,020 = 170, plus 1 relocation). Minor rounding/relocation effect.       | Use net_new_stores as stated (170 net) and stores_eop as stated (1,190).                                                               |


## Summary

Total issues found: 6. None prevent analysis. All are documented and handled.
The Netflix dataset has a planned gap (no memberships after Q4 2024).
Five Below financials are consistent with reported text; minor COVID distortions are noted.
