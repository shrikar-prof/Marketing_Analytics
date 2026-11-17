# ML follow-ups (round 1, from growth-strategy-partner)

Method for all: test window d_1914-d_1941 (28 days, 853,720 item-store-days) from modeling/scores.csv (model pred), joined to calendar_clean (week) and sell_prices_clean (weekly price; 0% missing). Dollars = units x weekly sell_price (measured, USD, 28 days).
Rule-of-thumb is NOT stored in any artifact. I rebuilt it as the mean of actual sales at t-7,-14,-21,-28 (same weekday, last 4 weeks), no buffer ("rule_rolling"). It gives RMSE 2.219 / MAE 1.075 vs the model-builder's 2.259 / 1.074: close, not identical, so the model-builder's exact rule is unknown. A fixed-origin variant (4 weeks before d_1913 only) gives 2.314 / 1.104. Treat rule numbers as reconstructed (assumed definition). Tables: reports/tables/fu*.csv. Script run once; no modeling.

Q1 Dollar sales, test window (measured)
| Cat | Units | USD sales (28d) | USD per unit sold (dollar-weighted) | Mean weekly price over all item-days |
|---|---|---|---|---|
| FOODS | 832,488 | 2,235,403 | 2.69 | 3.34 |
| HOBBIES | 115,856 | 503,239 | 4.34 | 5.54 |
| HOUSEHOLD | 283,420 | 1,162,334 | 4.10 | 5.47 |
| Total | 1,231,764 | 3,900,976 | 3.17 | 4.48 |

Q2 and Q3 Accuracy and error direction by category (units/item-day; over/under = summed units over 28 days)
| Cat | Forecaster | RMSE | MAE | Over-forecast | Under-forecast |
|---|---|---|---|---|---|
| FOODS | model | 2.093 | 1.102 | 219,956 | 223,270 |
| FOODS | rule | 2.756 | 1.394 | 263,848 | 296,955 |
| HOBBIES | model | 1.452 | 0.647 | 50,263 | 52,168 |
| HOBBIES | rule | 1.775 | 0.771 | 59,277 | 62,727 |
| HOUSEHOLD | model | 1.156 | 0.649 | 94,449 | 95,705 |
| HOUSEHOLD | rule | 1.486 | 0.801 | 114,978 | 119,799 |
| All | model | 1.707 | 0.862 | 364,668 | 371,143 |
| All | rule | 2.219 | 1.075 | 438,103 | 479,480 |
MAE improvement: FOODS 21%, HOBBIES 16%, HOUSEHOLD 19%. Neither forecaster is lopsided; the rule's under-forecast exceeds its over-forecast by 9% (all categories). Model is balanced (within 2%). Note these are point forecasts, no safety buffer.

Q4 Top decile vs the rest. Caveat: is_top_decile is a decile of item-DAY predictions (scores.csv pred_decile), not of series.
| Group | Forecaster | MAE | RMSE | Over | Under |
|---|---|---|---|---|---|
| Decile 10 (85,372 rows) | model | 2.973 | 4.522 | 127,193 | 129,244 |
| Decile 10 | rule | 3.763 | 5.901 | 128,700 | 195,875 |
| Deciles 1-9 | model | 0.625 | 0.972 | 237,475 | 241,899 |
| Deciles 1-9 | rule | 0.773 | 1.250 | 309,403 | 283,605 |
MAE gain: decile 10 -0.79 units (21%); deciles 1-9 -0.15 units (19%). In decile 10 the rule's under-forecast is 52% above the model's (195,875 vs 129,244 units).

Q5 Rounding preds < 0.5 to 0 (model, modeled)
| Cat | Zero-sale days with pred in [0,0.5) | Share of all item-days that are zero and pred<0.5 | MAE before -> after | RMSE before -> after |
|---|---|---|---|---|
| FOODS | 56.1% | 25.2% | 1.102 -> 1.076 | 2.093 -> 2.098 |
| HOBBIES | 78.5% | 53.6% | 0.647 -> 0.599 | 1.452 -> 1.464 |
| HOUSEHOLD | 75.2% | 45.2% | 0.649 -> 0.606 | 1.156 -> 1.170 |
| All | 68.6% | 37.3% | 0.862 -> 0.826 | 1.707 -> 1.715 |
Rounding lowers MAE 4-8% but raises RMSE slightly (it adds bigger misses on the few days that sell). It suits order-quantity decisions in whole units, not volume totals.

Q6 FOODS, SNAP vs non-SNAP days (SNAP flag matched to store state; 143,700 SNAP rows vs 258,660 non-SNAP rows)
| Day type | Model MAE | Rule MAE | Model RMSE | Rule RMSE | Mean units/item-day |
|---|---|---|---|---|---|
| Non-SNAP | 1.070 | 1.353 | 2.015 | 2.605 | 1.965 |
| SNAP | 1.158 | 1.468 | 2.227 | 3.010 | 2.256 |
Model MAE gain 21% non-SNAP, 21% SNAP. Both forecasters err more on SNAP days, so the model has not fully absorbed the SNAP lift. Day counts differ by state (counts in SNAP/non-SNAP rows above are pooled across CA/TX/WI), and this is a 28-day window: descriptive, not a pilot result.

# Round 2 (from growth-strategy-partner)

Method: same test window (d_1914-d_1941), scores.csv model pred, reconstructed rule (mean of t-7..t-28 actuals; assumed definition, see round 1), weekly sell_price from sell_prices_clean. "Training mean" = mean daily units over d_1211-d_1885 (the model's training window), from clean.parquet. Tables: tables/fu7_*.csv, fu8_*.csv, fu9_*.csv.

CORRECTION to round 1 and to ml_handoff_report.md section 6: the "Series count" column (1,437 / 1,047 / 565, total 3,049) counts distinct ITEMS, not item-store series. Item-store series are FOODS 14,370, HOUSEHOLD 10,470, HOBBIES 5,650, total 30,490. Units, errors and shares in that table are unaffected. I have not edited the report (follow-up mode).

Q1 Sum over series of (28-day RMSE x mean weekly price), USD per unit of z-score (measured on test window; modeled forecast)
| Cat | Series | Model | Rule (rolling) | Rule (fixed origin) |
|---|---|---|---|---|
| FOODS | 14,370 | 58,472 | 74,753 | 76,629 |
| HOBBIES | 5,650 | 20,528 | 25,214 | 25,480 |
| HOUSEHOLD | 10,470 | 40,635 | 50,875 | 51,853 |
| Total | 30,490 | 119,635 | 150,842 | 153,961 |
Model is 20.7% below the rolling rule (22.3% below fixed-origin). Caveats: this is a one-period sum of per-series daily error sizes in dollars, not an inventory value; it treats errors as independent across series and days, and RMSE here is around the forecast (mean error not removed). Leading zeros and price in weeks with no price are not an issue (0% missing price in test).

Q2 Possible hidden stockouts, series with training mean >= 5 units/day (1,267 series)
| Cat | Series | Test item-days | Zero-sale item-days | Zero share | Series with any zero day | Series with run of 3+ zero days |
|---|---|---|---|---|---|---|
| FOODS | 932 | 26,096 | 3,066 | 11.7% | 403 | 152 |
| HOBBIES | 86 | 2,408 | 347 | 14.4% | 74 | 16 |
| HOUSEHOLD | 249 | 6,972 | 673 | 9.7% | 140 | 45 |
| All | 1,267 | 35,476 | 4,086 | 11.5% | 617 | 213 |
Zero days at this velocity are suspicious but not proof: there are no stockout flags, so a zero cannot be told apart from true no-demand, a delisted item or a data gap. 213 series (16.8% of the tier) is the pilot candidate list. Run length is within the 28-day window only (runs cut at the window edges).

Q3 Velocity tiers (training mean units/day per item-store series; test units are measured)
| Tier | Series | Share of series | Test units (28d) | Share of test units |
|---|---|---|---|---|
| >= 5 | 1,267 | 4.2% | 376,025 | 30.5% |
| 1 to < 5 | 7,984 | 26.2% | 535,529 | 43.5% |
| < 1 | 21,239 | 69.7% | 320,210 | 26.0% |
By category (>=5 / 1-5 / <1): FOODS 932 / 5,153 / 8,285; HOUSEHOLD 249 / 2,087 / 8,134; HOBBIES 86 / 744 / 4,820. Dollar-weighted RMSE sum by tier (model vs rule): >=5 11,139 vs 15,380; 1-5 40,979 vs 51,903; <1 67,517 vs 83,559.
