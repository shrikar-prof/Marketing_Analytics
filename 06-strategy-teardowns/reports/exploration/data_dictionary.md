# Data Dictionary — Strategy Teardowns

## Netflix UCAN quarterly data

| column         | meaning                                               | type     | unit         | missing_pct    | usability                                           |
|:---------------|:------------------------------------------------------|:---------|:-------------|:---------------|:----------------------------------------------------|
| quarter        | Quarter label (e.g. Q4'19)                            | string   | —            | 0%             | Date key — not a model input                        |
| end_date       | Last calendar day of the quarter                      | datetime | date         | 0%             | Date key                                            |
| paid_members_m | Paid UCAN memberships at end of quarter               | float    | millions     | 17% (Q1–Q4'25) | Target/feature — core business metric               |
| net_adds_m     | Net new paid memberships added during the quarter     | float    | millions     | 17%            | Feature — derived from successive membership counts |
| arm_usd        | Average monthly revenue per membership (ARM)          | float    | USD/month    | 17%            | Feature — key pricing metric                        |
| revenue_usd_m  | Total UCAN quarterly streaming revenue                | float    | USD millions | 0%             | Target — core business metric                       |
| has_members    | Whether membership data is available for this quarter | bool     | —            | 0%             | Filter flag                                         |


## Five Below annual data

| column               | meaning                                           | type     | unit   | missing_pct                          | usability                                |
|:---------------------|:--------------------------------------------------|:---------|:-------|:-------------------------------------|:-----------------------------------------|
| fiscal_year          | Fiscal year (e.g. 2018 = Feb 2018–Feb 2019)       | int      | —      | 0%                                   | Date key                                 |
| stores_eop           | Total stores open at end of fiscal year           | int      | count  | 0%                                   | Feature — core expansion metric          |
| net_new_stores       | Net new stores opened during the fiscal year      | int      | count  | 0%                                   | Feature — expansion pace                 |
| comp_sales_pct       | Comparable sales growth (stores open ≥15 months)  | float    | % YoY  | 0%                                   | Target — same-store productivity         |
| note                 | Context note (e.g. COVID, 53-week year)           | string   | —      | varies                               | Annotation only — do not encode          |
| fiscal_year_end      | Exact date the fiscal year ended                  | datetime | date   | 0%                                   | Date key                                 |
| revenue_usd          | Annual net sales                                  | float    | USD    | 0%                                   | Feature                                  |
| operating_income_usd | Operating income (revenue minus COGS and SGA)     | float    | USD    | 0%                                   | Feature — profitability measure          |
| net_income_usd       | Net income after tax                              | float    | USD    | 0%                                   | Feature                                  |
| cogs_usd             | Cost of goods sold                                | float    | USD    | 12% (older years tagged differently) | Feature                                  |
| sga_usd              | Selling, general and administrative expenses      | float    | USD    | 0%                                   | Feature                                  |
| capex_usd            | Capital expenditures (property, plant, equipment) | float    | USD    | 0%                                   | Feature — proxy for new store investment |


## Derived columns

| column         | inputs                                           | formula                                  | why                                                             | example                                        |
|:---------------|:-------------------------------------------------|:-----------------------------------------|:----------------------------------------------------------------|:-----------------------------------------------|
| op_margin_pct  | operating_income_usd / revenue_usd               | operating_income_usd / revenue_usd × 100 | Percent of each sales dollar kept as operating profit           | FY2018: 187.2M / 1559.6M × 100 = 12.0%         |
| rev_per_store  | revenue_usd / stores_eop                         | revenue_usd / stores_eop                 | Average annual sales per store; measures new-store productivity | FY2018: $1,559.6M / 750 = $2.08M per store     |
| yoy_rev_growth | revenue_usd (current, prior)                     | (rev_t − rev_{t-1}) / rev_{t-1} × 100    | Year-over-year revenue growth rate                              | FY2019 vs FY2018: (1,962−1,559)/1,559 = +25.9% |
| nf_rev_yoy_pct | revenue_usd_m (current, prior quarter same year) | (rev_q − rev_{q-4}) / rev_{q-4} × 100    | Year-over-year quarterly revenue growth for Netflix UCAN        | Q4'20 vs Q4'19: (2,980−2,672)/2,672 = +11.5%   |


_Source: SEC EDGAR filings. All numbers read from raw files; see notebook Section 2._
