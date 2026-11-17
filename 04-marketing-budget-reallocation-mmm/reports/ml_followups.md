# ML Follow-up Q&A — Marketing Budget Reallocation (MMM)

This file is a placeholder. The growth-strategy-partner may send follow-up questions via SendMessage.
Each question and its answer will be appended here with the question, method, and source file.

---

## Round 1 (growth-strategy-partner, 8 questions)
Method for all items: read-only computation on the saved fitted model (`models/mmm_model.joblib`), `reports/modeling/features.parquet`, `reports/exploration/clean.parquet`. No refitting except item 3 folds (Ridge, alpha 2.16, refit on each CV window, same split rule as `src/model_utils.py`). Basis labels: measured / modeled (association, not cause).

### Corrections to `ml_handoff_report.md` found while answering (read these first)
1. **Event weeks (item 6): the report's F3 is wrong.** The raw data has 2 event weeks (event1 on 2018-05-21, event2 on 2019-04-22), not 15. The "15 vs 193 weeks", p < 0.001 and 18% in `findings.md` and chart 08 cannot be reproduced from `clean.parquet` or the raw file. Reliability of F3 should read "not established". I had rated it High; that was an error.
2. **Gap G1 (item 4): my cause was not supported.** Correlations are moderate (below), not severe. OOH and Search are negative because their fitted coefficients are negative, not because of a measured collinearity artifact.
3. **"Market demand is the largest driver" (item 5):** competitor_sales_log has r = 0.96 with cos_1 (seasonality). The two cannot be separated, so that SHAP share is "competitor index plus seasonality", not demand alone.
4. **Final model (item 1) uses no adstock or Hill saturation.** It uses only the log features. G2 and G3 in my report describe the _sat feature set, which is not in the fitted model. Curve shape is log(1+spend) only.
5. Table 04 and the "positive direction" for TV-to-Facebook: see item 3. On the final model the net is negative at the basis I used.
6. CV folds: the split rule gives 11 folds (training windows of 60 to 160 weeks), not 10 as the model card states.

### 1. Features and channel coefficients (modeled)
Fitted features (15, all in the `_log` set; no `_sat` features): tv_S_log, ooh_S_log, print_S_log, facebook_S_log, search_S_log, newsletter_log, competitor_sales_log, event_flag, total_spend_log, print_low_flag, trend, sin_1, cos_1, sin_2, cos_2. Ridge alpha 2.16, fit on 188 training weeks.

| Feature | Coefficient, USD of weekly revenue per +1 unit of log(1+spend) | Per +1 SD (standardized) |
|---|---|---|
| tv_S_log | +19,505 | +97,292 |
| ooh_S_log | -8,685 | -47,917 |
| print_S_log | +19,867 | +85,805 |
| facebook_S_log | +2,407 | +9,762 |
| search_S_log | -474 | -1,495 |
| total_spend_log (media total) | +22,301 | +39,777 |
| print_low_flag | +106,510 | +52,661 |

Note: print_low_flag equals "print spend is zero" (the 5th percentile is 0; flag = 1 in 57.4% of training weeks). It moves one-for-one with print_S_log (VIF 43.5 and 43.6). The print coefficients are not separately identified.

### 2. Marginal return of +$1K weekly spend (modeled; curve method, all other features at training mean)

| Channel | Mean active-week spend (all 208 wks) | Revenue change per +$1K there | All-week average spend (188 train wks, chart marker) | Revenue change per +$1K there |
|---|---|---|---|---|
| TV | $33,560 | +$573 | $15,606 | +$1,211 |
| OOH | $105,757 | -$82 | $46,410 | -$185 |
| Print | $8,914 | +$2,112 | $3,715 | +$4,735 |
| Facebook | $4,419 | +$491 | $2,034 | +$962 |
| Search | $6,991 | -$63 | $5,416 | -$80 |

Per week, USD of revenue, not margin. A value below $1,000 per $1K spent is a revenue return under 1.0x.

### 3. Table 04 scenario (TV -$6,712/wk, Facebook +$6,712/wk, at mean active-week levels; modeled)
Net change: **-$2,129 per week** (TV leg -$4,352, Facebook leg +$2,224). Your read of chart 01 is correct: on this basis the TV loss exceeds the Facebook gain. My report called the direction positive; that was wrong for this basis.

The sign depends on the basis:

| Basis | Net change, USD per week |
|---|---|
| Curve, mean active-week levels (the table 04 numbers) | -2,129 |
| Curve, all-week averages (TV -$3,121, FB +$3,121) | -2,114 |
| Actual weeks, 82 TV-active training weeks, 20% of each week's TV moved to Facebook | +5,880 |
| Same, all 188 training weeks | +2,565 |

Across 11 CV-window refits (curve basis, table 04 amounts): net ranges -$1,090 to +$15,470 per week, mean +$3,660; 6 folds positive, 5 negative. TV leg is stable (-$2,783 to -$5,355). Facebook leg is not (+$3,484 to +$18,252); Facebook coefficient ranged 3,772 to 19,760 per log unit. Folds with 130 or more training weeks all give -$1,090 to -$273. Conclusion: the sign is not established by this model. A geo test is needed.

### 4. Collinearity (measured, all 208 weeks)
| Pair or feature | Result |
|---|---|
| ooh_S_log vs total_spend_log | Pearson r = 0.63 (training only 0.64); VIF 2.1 and 2.9 |
| search_S_log vs trend | r = 0.13; VIF 1.1 and 1.3 |
| Actual high-VIF features | print_S_log 43.6, print_low_flag 43.5, competitor_sales_log 18.6, cos_1 17.8 |

### 5. competitor_sales_log correlations (measured, 208 weeks)
cos_1 0.961; sin_1 0.005; tv_S_log 0.227; ooh_S_log 0.108; print_S_log 0.224; facebook_S_log 0.372; search_S_log 0.103. The index is effectively a seasonal curve. It may absorb some seasonal effect (strong evidence) and some Facebook effect (weak to moderate, r = 0.37).

### 6. Event weeks (measured)
| Group | Weeks | Mean revenue | Median revenue |
|---|---|---|---|
| Event | 2 | $2,452,598 | $2,452,598 |
| Non-event | 206 | $1,816,022 | $1,852,788 |

Lift: +35.1% on means, +32.4% on medians. The report's 18% and its 15-week group are not reproducible. With 2 event weeks (0 in the test set), the event_flag coefficient (+$1.28M per week) rests on two observations. Chart 08 should not be used.

### 7. Media vs baseline (modeled; zero-spend counterfactual on the 208 weeks; predicted total $379.0M)
| Definition | 4-year signed contribution | Share of predicted revenue |
|---|---|---|
| Five channel log terms set to zero | +$25.7M ($123K/wk) | 6.8% |
| Also total_spend_log to 0 and print_low_flag to 1 (all spend zero) | +$64.0M ($308K/wk) | 16.9% |

Channel by channel (first definition): TV +$17.6M, Print +$14.9M, Facebook +$1.9M, Search -$0.7M, OOH -$8.1M. The all-spend-zero total is driven mostly by the total_spend_log term (+$47.6M). Only 2 weeks have zero total spend, so this is an extrapolation. Treat as an association.

### 8. Spend by calendar year (measured; `reports/tables/q8_spend_by_year.csv`)
| Year (weeks) | Total spend | Per week | OOH spend | OOH share |
|---|---|---|---|---|
| 2015 (6) | $681K | $113.6K | $410K | 60% |
| 2016 (52) | $4.24M | $81.6K | $3.00M | 71% |
| 2017 (52) | $5.27M | $101.4K | $3.70M | 70% |
| 2018 (53) | $3.06M | $57.8K | $1.54M | 50% |
| 2019 (45, to 11 Nov) | $1.27M | $28.2K | $0.34M | 27% |

Your read of chart 07 is right: spend fell about 72% per week from 2017 to 2019, mostly OOH. This conflicts with finding F4 (flat budget); the "$34K/week" fits only 2019. Search rose from $264K (2017) to about $400K per year.

## Round 2 (growth-strategy-partner, 4 questions)
Method: descriptive reads of `reports/modeling/scores.csv` (residual = actual minus predicted), `reports/exploration/clean.parquet` and `data/raw/meridian_geo_media.csv`. No new modeling. All figures measured. Years follow the DATE (week start) column; 2018 has 53 weeks, 2019 has 45 (to 2019-11-11).

### 1. Revenue by calendar year
| Year (weeks) | Total revenue | Mean weekly revenue | Mean residual, USD per week | Mean absolute residual |
|---|---|---|---|---|
| 2016 (52) | $93.43M | $1.797M | -1,863 | 138,168 |
| 2017 (52) | $97.49M | $1.875M | +39,551 | 156,945 |
| 2018 (53) | $97.94M | $1.848M | +7,092 | 119,002 |
| 2019 (45) | $74.61M | $1.658M | -32,620 | 105,956 |

Same weeks-of-year, weeks 1-45: 2018 (2018-01-01 to 2018-11-05) mean $1.712M, total $77.04M; 2019 (2019-01-07 to 2019-11-11) mean $1.658M, total $74.61M. Difference -$54K per week, -3.1%.
Other year comparisons on mean weekly revenue: 2017 to 2018 -1.4%; 2018 (all 53 weeks) to 2019 -10.3% (not like for like, 2019 is Jan-Nov only).
Residual caveat: 2019 mixes 25 in-sample weeks (mean residual about -59,000) and the 20 held-out test weeks (mean +384). Residuals do not test the OOH lever: the fitted OOH coefficient is negative, so the model already expects revenue not to fall as OOH falls. This table shows revenue held roughly flat (-1% to -3%) while OOH spend fell; it does not show OOH had no effect (other drivers moved too).

### 2. 2019 spend split (45 weeks, measured)
| Channel | Mean per week | Total 2019 | Share of 2019 spend | Weeks active of 45 |
|---|---|---|---|---|
| TV | $7,298 | $328,428 | 25.8% | 21 |
| OOH | $7,556 | $340,023 | 26.8% | 16 |
| Print | $2,470 | $111,136 | 8.7% | 19 |
| Facebook | $2,009 | $90,386 | 7.1% | 17 |
| Search | $8,909 | $400,907 | 31.5% | 38 |
| Total | $28,242 | $1,270,880 | 100% | |

Median weekly spend in 2019 is $0 for TV, OOH, Print and Facebook; Search median is $7,973. Spend is lumpy: a channel is on in fewer than half the weeks.

### 3. Residual noise (model fit on 188 training weeks)
| Set | SD of weekly residual | Lag-1 autocorrelation | n |
|---|---|---|---|
| Training (in-sample) | $231,326 | +0.077 | 188 |
| Training, 2018-2019 only | $202,532 | not computed | |
| Held-out test | $145,802 | +0.221 | 20 |

Training residuals have mean 0 by construction. The in-sample SD is the figure to use for noise in test sizing; the test SD rests on 20 weeks. Autocorrelation is low, so weekly residuals are close to independent in training, but the test-set value is higher and has wide uncertainty at n = 20. These are residuals of the full model, not the week-to-week SD of revenue.

### 4. Meridian geo file (`data/raw/meridian_geo_media.csv`)
- Geos: 20. Rows 3,120 (156 weeks each, 2021-01-25 to 2024-01-15).
- Weekly revenue = conversions x revenue_per_conversion.
- Median weekly revenue per geo-week (all 3,120 rows): $320,657. Median across geos of each geo's median weekly revenue: $329,283.
- Median across geos of the CV of weekly revenue (SD / mean per geo): 0.276 (range 0.225 to 0.319).
- Size spread: mean weekly revenue by geo runs $98K to $698K (median $328K), a 7x range.
