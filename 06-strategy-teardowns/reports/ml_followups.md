# ML follow-ups (round 1, growth-strategy-partner)

Method for all items: recomputed from reports/modeling/features_nf.parquet, features_fb.parquet (copies of the clean tables) with scipy/statsmodels; test definitions taken from notebooks/01_exploration.ipynb. No refitting of selected models; one OLS fit of the already-named spec for item 3.

1. Q4'24 UCAN paid members = 89.63M (clean table; chart 02 is right). 83M in the handoff was wrong. ARM is $ per member per month, so $1/month x 89.63M x 12 = $1,076M per year (about $1,050M on the 87.2M average members implied by Q4'24 revenue 4,517/3/17.26). The "$360M/year" was an arithmetic error in the handoff (it is not 83M x $1 x 12 = $996M, nor any other defensible figure). Break-even: a $1 rise at ARM 17.26 is offset by losing about 4.9M members (5.5%). Assumed: flat membership; modeled-free arithmetic, not a causal estimate.
2. Revenue USD M: Q2'25 4,929; Q3'25 5,072; Q4'25 5,339. CY2025 = 19,957; CY2024 = 17,359; growth +14.97% (+2,598M).
3. Pre = Q4'19-Q1'23 (14 quarters, median 3,246.5M); post = Q2'23-Q4'25 (11 quarters, median 4,322M). Median difference = 1,075.5M (findings.md 1,060M does not reproduce). Hodges-Lehmann = 1,218M (reproduces; this is what hypotheses.md reports). Both mix in the time trend and include 2025. Trend-adjusted: OLS (Ridge alpha 0.01 is ~OLS) of revenue on arm_lag1, rev_lag1, post_paid_sharing, quarter dummies, fitted on 20 training quarters Q1'20-Q4'24: post_paid_sharing = +92.4M/qtr, SE 64.1, 95% CI [-46, +231], p = 0.17. Without quarter dummies: +86.9M, SE 59.8. The model does not support a $1.2B/qtr step. (Members model: post_paid_sharing +2.23M members, SE 0.89, p = 0.022, model_card.)
4. rho = -0.474 (p = 0.064, bootstrap CI [-0.810, 0.033]) is correct; reproduced. Pair: ARM YoY growth in quarter t vs net adds in quarter t+1, quarters Q4'20-Q3'24, N = 16 (hypotheses.md says N=15; notebook prints 16). I could not reproduce +0.19 anywhere. Sign meaning: higher ARM growth goes with lower next-quarter net adds (borderline). Variants: QoQ ARM change vs next net adds rho -0.23 (N=19, p 0.35); same-quarter ARM YoY vs net adds rho -0.54 (N=17, p 0.026).
5. Both H3 and H4 use ABSOLUTE net_new_stores, on six non-COVID years FY2018, 2019, 2022, 2023, 2024, 2025. Results: comps vs stores rho -0.577, exact p 0.1417 (102/720); margin vs stores rho -0.820, p 0.0333 (24/720). Rate (net new / prior fleet; FY2018 undefined so 5 years FY2019, 2022-25): comps vs rate rho -0.20, one-sided exact p 0.39 (47/120); margin vs rate rho +0.50, p 0.825. Your hand calculation is right: the negative link holds for store count, not for rate.
6. Table below (revenue, op income, capex USD M; SG&A / revenue).
| FY | Stores EOP | Net new | Revenue | Op income | SG&A % | Capex |
| 2018 | 750 | 125 | 1,559.6 | 187.2 | 24.2 | 113.7 |
| 2019 | 900 | 150 | 1,846.7 | 217.3 | 24.7 | 212.3 |
| 2020 | 1,020 | 120 | 1,962.1 | 154.8 | 25.4 | 200.2 |
| 2021 | 1,190 | 170 | 2,848.4 | 379.9 | 22.8 | 288.2 |
| 2022 | 1,340 | 150 | 3,076.3 | 345.0 | 24.4 | 252.0 |
| 2023 | 1,544 | 204 | 3,559.4 | 385.6 | 21.3 | 335.1 |
| 2024 | 1,771 | 227 | 3,876.5 | 323.8 | 22.2 | 324.0 |
| 2025 | 1,921 | 150 | 4,764.1 | 457.4 | 22.4 | 174.7 |
7. Comps: FY2022 -2.0, FY2023 +2.8, FY2024 -2.7 (clean table). Handoff section 1 and findings.md wrongly put -2.0 on FY2023. Only FY2024 of the two peak-expansion years was negative. FY2023 margin = 10.83% (rounds to 10.8; 10.7 in findings is a slip).
8. Neither file is the full story. scores.csv holds full-sample fitted values (in-sample MAE: comps 9.36, margin 1.51; Netflix 63.6M), flat because alpha = 100 shrinks the slope to ~0. The chart plots true leave-one-out predictions (leave-one-out mean reproduces its FY2021 value ~0.8-1.0; LOO MAE 10.9 and 1.7, matching the model card 11.07 and 1.79). Selected model is the same; the chart is the honest out-of-sample view. My customer_risk_scores.csv inherited the in-sample values but labels them "loocv" and "wf-CV OOF": that labelling is wrong. Only Netflix Q1'25 is a held-out score; Q2-Q4'25 were not scored.
9. Revenue per store = revenue / year-end stores (data dictionary). FY2022 = $2.2958M = $2.30M. $2.60M in findings.md is wrong. On average-fleet basis FY2022 = $2.43M. Note FY2022 to FY2023-24 average is -$0.05M (-2%) per hypotheses H5; "dilution" is small.

# Round 2 (growth-strategy-partner)

Method: recomputed from the clean tables (features_fb.parquet, features_nf.parquet); XBRL companyfacts was not re-queried.

1. Gross margin = 1 - cogs_usd / revenue_usd, from the cleaned cogs_usd column. Identity check: gross margin - SG&A % = operating margin holds exactly for FY2018-FY2022 (residual 0.00 ppt) but NOT for FY2023-FY2025 (residual 3.67, 4.32, 4.03 ppt). So cogs_usd for FY2023+ appears to exclude a cost line that the earlier years include (the data dictionary flags cogs as tagged differently in some years). Gross margin FY2023+ is therefore not comparable with earlier years. Status: OPEN, needs a check of the 10-K cost lines.
GM % / SG&A % / op margin %: 2018 36.23/24.23/12.00; 2019 36.50/24.73/11.77; 2020 33.25/25.36/7.89; 2021 36.18/22.84/13.34; 2022 35.61/24.39/11.22; 2023 35.79/21.28/10.83; 2024 34.89/22.22/8.35; 2025 35.99/22.36/9.60.
Bridge (ppt of revenue), as the data stands: FY23->24 op margin -2.48 = gross margin -0.89, SG&A -0.94 (22.22 vs 21.28), unexplained other cost -0.65. FY24->25 +1.25 = gross margin +1.10, SG&A -0.14, other +0.29. The "other" line is the unreconciled residual; do not read it as a finding.
2. Annual decomposition, log basis, revenue = sum of 4 quarters, members = mean of the 4 quarter-end counts, implied ARM = revenue / avg members / 12 (reported-ARM in brackets).
2022: revenue +8.6%; members -0.7%, ARM +9.3%; share members -8%, ARM 108% [reported ARM +8.9%, 104%].
2023: revenue +5.6%; members +4.0%, ARM +1.5%; share members 72%, ARM 28% [reported ARM +2.6%, 47%].
2024: revenue +16.7%; members +11.0%, ARM +5.2%; share members 68%, ARM 33% [reported ARM +5.7%, 36%].
You are right: 2023 and 2024 were member-led; 2022 was ARM-led. Handoff section 8 / chart-05 wording was wrong. Descriptive arithmetic, not causal.
3. post_paid_sharing in lag1+post_sharing members model: +2.23M, SE 0.89, 95% CI [+0.36M, +4.10M], p 0.022 (coefficient_table.csv; n=20, so fragile). Q1'23 74.40M to Q4'24 89.63M = +15.23M. Association, not a causal effect of enforcement.
