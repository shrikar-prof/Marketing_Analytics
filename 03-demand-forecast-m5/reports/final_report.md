# M5 Demand Forecast: Final Report

**Project:** 03 Demand Forecast for Inventory Planning (Walmart M5 data, 10 stores, 3,049 items)
**Date:** 2026-11-04
**Sources:** every number below cites the file and section it came from. Short names used:
`problem` = `problem_description.md`; `findings` = `reports/exploration/findings.md`; `hypotheses` = `reports/exploration/hypotheses.md`; `card` = `reports/modeling/model_card.md`; `tuning` = `reports/modeling/tuning.md`; `handoff` = `reports/ml_handoff_report.md`; `memo` = `reports/executive_growth_strategy.md`; `followups` = `reports/ml_followups.md`; `dialogue` = `reports/agent_dialogue.md`; `review` = `reports/notebook_review.md`.

**Evidence labels:** *measured* (counted from the data), *modeled* (a model output), *external* (a fetched web source, with link), *assumed* (an estimate or an unfetched figure).

---

# Part A. The answer in plain language

## The question

"Can a statistical forecast beat the current rule at the item-day level, and what is the improvement worth in inventory dollars and lost sales at a fixed service target?" (problem, "Question to answer").

The current rule orders what sold on the same weekday over the last four weeks, plus a buffer (problem, "Problem").

## The answer

Yes. The forecast model makes daily errors 24% smaller than the current rule on 28 days it never saw. It fixes both problems operations suspected: it runs short less often on fast items and over-orders less on slow ones. The money is real but modest at 10 stores, and most of the dollar figures rest on assumptions. The largest possible prize, hidden empty shelves, cannot be measured until the stores record stockouts.

## The numbers that matter

| # | Number | What it means for the decision | Label and source |
|---|---|---|---|
| 1 | Error of 1.707 units per item per day for the model vs 2.259 for the rule: 24.4% smaller (28 test days, 853,720 item-store-days) | The model is clearly better. The gap is large enough to act on. | measured; card "How good is it", handoff §4 |
| 2 | On the busiest 10% of item-days the rule falls short by 195,875 units; the model by 129,244 (28 days) | The rule's biggest leak is empty shelves on fast items. The model cuts that shortfall by 66,631 units. | measured, rule reconstructed; followups Q4 |
| 3 | On the other 90% of item-days the rule over-orders 309,403 units; the model 237,475 (28 days) | The rule also carries too much slow stock. Operations' suspicion is confirmed. | measured, rule reconstructed; followups Q4 |
| 4 | 2,829 of 30,490 item-store series (9.3%) hold 50% of forecast volume | Start with a small set of series. Effort should follow volume. | modeled ranking; handoff §6, `tables/smallest_intervention.csv` |
| 5 | About $102K to $127K of stock released at cost, one time, across 10 stores | Inventory saving is modest. It depends on an assumed 7-day lead time and 75% cost ratio. | modeled plus assumed; memo §3.3 |

## What should happen next

1. **Run the model on the fast and mid tiers with a holdout.** 9,251 series hold 74% of units; split them 50/50 for 8 weeks (memo §5 Pilot 1; followups R2 Q3, measured).
2. **Audit hidden stockouts first.** 1,267 fast series logged 4,086 zero-sale days in 28 days (11.5%); check shelves for four weeks (memo §5 Pilot 4; followups R2 Q2, measured).
3. **Set a written service target by velocity tier.** None exists today (handoff §7; memo §3.4).
4. **Add a SNAP-day uplift of about 15% to FOODS orders now.** FOODS sold 14.8% more per item-day on SNAP days in the test window (followups Q6, measured; memo §4 B2).
5. **Cut buffers on the slow tail.** Round forecasts under 0.5 units to zero for orders; this cuts MAE 7% in HOBBIES and HOUSEHOLD (followups Q5, modeled; memo Pilot 3).

## What is uncertain

- Zero sales may be empty shelves. There is no stockout flag, so true demand and lost sales cannot be measured (handoff §7 issue 1).
- The live rule and its buffer were never supplied. Rule figures are rebuilt (RMSE 2.219 or 2.259, depending on who rebuilt it) (followups, method note).
- Every dollar figure scales with assumed lead time, cost ratio, margin and carrying cost (memo §7 item 3).

---

# Part B. How we got there

## B1. The data: five years of daily Walmart sales, clean but with no stockout record

| Item | Value | Label and source |
|---|---|---|
| Source | M5 forecasting competition (Walmart), Nixtla public mirror; analysis only, not re-hosted | external, problem "Data"; https://github.com/Nixtla/m5-forecasts |
| Grain [the level of one row] | One item in one store on one day | measured, handoff §2 |
| Size | 30,490 item-store series; 1,941 days, 2011-01-29 to 2016-06-19 | measured, problem "Data" |
| Hierarchy | 3 categories, 7 departments, 3 states, 10 stores | measured, problem "Data" |
| Training window | d_1211 to d_1885 (2014-05-23 to 2016-03-27); 20,580,750 rows | measured, handoff §2, card appendix |
| Validation | 28 days, d_1886 to d_1913 | measured, handoff §2 |
| Test | 28 days, d_1914 to d_1941 (2016-04-25 to 2016-05-22) | measured, handoff §2 |
| Zero-sale cells, full history | 40,241,819 cells, 68.0% of all item-day cells | measured, `exploration/quality_audit.md` |
| Price range | $0.01 to $107.32 per unit, 0% missing | measured, data_dictionary "sell_prices" |

**How it was checked.** The explorer audited every table (`exploration/quality_audit.md`). There were no negative sales, no duplicate item-store rows, no zero prices and no price weeks missing from the calendar (measured).

**How it was cleaned.** Two changes only (`exploration/cleaning_log.md`):

| Rule | Rows affected | Why |
|---|---|---|
| Fill blank event names and types with "None" | 7,542 values | Blank means no event that day |
| Add a day index (d_1, d_2, ...) to the calendar by row position | 1,969 rows | The mirror lacks it; needed to join calendar to sales |

**What was excluded and why.** No rows were dropped. Modeling used only the last 675 days (d_1211 to d_1885) to keep training recent; the window length was the model builder's choice (handoff §7, labelled assumed).

**What could not be checked.** The audit flagged the calendar date range as "CRITICAL ... investigate". The cleaning log records no follow-up. Zero sales cannot be split into "no demand" and "empty shelf" (findings, "What we did not find").

## B2. What exploration found: demand is lumpy, calendar-driven and concentrated

Five findings, each tested with a Mann-Whitney test [a test that compares two groups without assuming a bell curve]. Effect size is the rank-biserial r [how often one group beats the other, from -1 to 1]. A finding is "reliable" when |r| is 0.1 or more and the 95% confidence interval [the range the true value likely sits in] excludes zero (hypotheses, decision rule).

| # | Finding | Key number | Effect (95% CI) | Reliability | Chart |
|---|---|---|---|---|---|
| F1 | HOBBIES items sell nothing far more often than FOODS | HOBBIES ~77% vs FOODS ~62% zero-sale days (chart); 18 percentage points apart | r = -0.41 (-0.43 to -0.40) | Reliable, large | `charts/01_zero_rate_by_category.png` |
| F2 | SNAP [federal food-benefit] days lift FOODS sales | +10.4% in California; "10-20%" across states | r = 0.27 (0.22 to 0.33) | Reliable, medium | `charts/02_snap_effect.png` |
| F3 | Sporting events barely move demand | +3% to +3.5% on total store demand | r = 0.13 (-0.12 to 0.37) | Not reliable: interval includes zero | `exploration/charts/07_event_type_effect.png` |
| F4 | FOODS sells far more at weekends; HOBBIES much less so | FOODS weekend +30.7% vs weekdays | r = 0.75 (0.71 to 0.79) | Reliable, large | `charts/03_demand_category_weekday.png` |
| F5 | A minority of series sell most units | Gini [concentration score, 0 to 1] = 0.67; "top 20% drive ~60%" | not tested | Descriptive | `charts/04_sales_concentration.png` |

All measured; sources: findings "Summary", hypotheses "Results". F1 to F5 numbers differ slightly between files; see Part C.

**What the charts show.**
- `charts/01`: HOBBIES 77%, HOUSEHOLD 71%, FOODS 62% zero-sale days. By department, HOBBIES_2 (~88%) and HOUSEHOLD_2 (~80%) are the sparsest.
- `charts/02`: SNAP-day bars sit above non-SNAP bars in all three states; the gap is widest in Wisconsin.
- `charts/03`: FOODS rises from about 1.45 units midweek to about 1.96 to 1.98 at the weekend. HOBBIES and HOUSEHOLD rise far less.
- `charts/04`: a strongly bowed Lorenz curve [cumulative share of series vs share of units]. Its annotation reads "Bottom 80% of items = 30% of sales".

**Not found.** The explorer reported no meaningful volatility difference between FOODS and HOUSEHOLD. The hypotheses table reports the opposite (Part C). There is no store demographic or footfall data (findings).

## B3. How the model was built and tuned: LightGBM won, 24% better than the rule

**What was compared.** Five learning methods and two simple baselines, all scored on the same 28 validation days (card appendix; `modeling/tables/model_comparison.csv`; all measured).

| Model | Plain description | Validation RMSE (units/item-day) | Validation MAE |
|---|---|---|---|
| LightGBM | Many small decision trees, each fixing the last one's errors | 1.735 | 0.852 |
| CatBoost | Same family, different tree recipe | 1.745 | 0.856 |
| XGBoost | Same family, different tree recipe | 1.759 | 0.860 |
| Ridge | A straight-line formula with a penalty for big weights | 1.797 | 0.885 |
| Random Forest | Many independent trees, averaged | 1.806 | 0.864 |
| Rule of thumb | Same-weekday average of last 4 weeks | 2.259 | 1.074 |
| Naive-Lag7 | "Sales equal last week's same day" | 2.660 | 1.205 |

RMSE [root mean squared error: the typical miss, weighting big misses more] and MAE [mean absolute error: the average size of a miss] are in units per item per day.

**How tuning worked.** Optuna [a tool that tries many settings and keeps the best] ran 120 trials [one trial = one full model fit with one set of settings] on LightGBM and 109 on XGBoost (tuning; measured). The best LightGBM trial reached a cross-validation RMSE of 1.6723; XGBoost reached 1.6915.

| Lesson from tuning | Evidence |
|---|---|
| Most of the gain came early | LightGBM's best-so-far line falls from about 1.75 to about 1.68 by trial 43, then flattens (`modeling/charts/optuna_lgb_history.png`) |
| The minimum leaf size mattered most | `min_child_samples` [how many rows a tree's final group must contain] took 40% of parameter importance [the share of score variation each setting explains]; next were learning rate (14%) and `reg_lambda` (11%) |
| Tree size mattered least | `num_leaves` 8%, `max_depth` 3% |
| XGBoost showed the same pattern | `min_child_weight` took 59% of importance |

In plain words: stopping the trees from learning from tiny groups of rows matters most. This fits data with many slow, sparse series (handoff §4).

**Why LightGBM won.** It had the lowest validation RMSE (1.735) of any method. Tuned LightGBM (1.743) and tuned XGBoost (1.743) scored about the same as the untuned version on validation (`model_comparison_full.csv`, measured). The final model uses the tuned settings and 35 inputs (card appendix).

**How good it is on the held-out test** [28 days touched once, after all tuning] (card "How good is it"; handoff §4; measured):

| Metric | Model | Rule of thumb | Improvement |
|---|---|---|---|
| RMSE (units/item-day) | 1.707 | 2.259 | 24.4% |
| MAE (units/item-day) | 0.862 | 1.074 | 19.7% |
| Mean RMSSE [error divided by a naive forecast's error; below 1 beats naive] | 0.708 | not computed for the rule (see Part C) | 29.2% better than naive |

The model's total forecast (1,225,289 units) is within 0.5% of actual sales (1,231,764 units) over 28 days. It is not biased up or down overall (handoff §6, measured). The residual chart (`charts/07_decile_lift.png`, right panel) centres on zero, mean -0.001 units.

**Where it is weaker** (`modeling/tables/test_by_category.csv`, `test_by_store.csv`; measured):

| Segment | RMSE | MAE | Zero-sale rate (test) | Note |
|---|---|---|---|---|
| FOODS | 2.093 | 1.102 | 44.8% | Highest absolute error because highest volume |
| HOBBIES | 1.452 | 0.648 | 68.2% | Most intermittent [sells on few days]; small positive forecasts on zero days |
| HOUSEHOLD | 1.157 | 0.649 | 60.2% | |
| Store WI_2 | 2.354 | 0.982 | n/a | Worst store; FOODS in WI_2 has RMSE 3.154 (`tables/segment_store_x_category.csv`) |
| Store CA_3 | 2.080 | 1.108 | n/a | Second worst |

New items with no history cannot be forecast with lag features [inputs built from past sales] (card "What the model cannot do").

## B4. Recent sales drive the forecast; price is not a usable lever

SHAP [a method that splits each forecast into the share each input contributed] ranks inputs by their average contribution, in units (`modeling/tables/shap_importance.csv`; modeled).

| Driver | Mean contribution (units/item-day) | Type | Can the business change it? |
|---|---|---|---|
| `roll_mean_7` (7-day average sales) | 1.305 | Structural | No; it is the demand signal itself |
| `roll_std_7` (recent volatility) | 0.098 | Structural | No |
| `lag_1` (yesterday's sales) | 0.086 | Structural | No |
| `dow_sin` (weekday cycle) | 0.082 | Structural | No |
| `is_weekend` | 0.064 | Structural | No |
| `series_mean` (item's long-run average) | 0.036 | Structural | No |
| `snap` (benefit day) | 0.026 | Semi-controllable | Date is fixed; stock response is controllable |
| `sell_price` | 0.007 | Controllable | Yes, but effect is tiny and not causal |
| `price_ratio` (price vs 4-week average) | 0.001 | Controllable | Yes, but effect is tiny and not causal |

"Structural" means the business cannot change it in the short term (handoff §5).

**Counterfactual sensitivities** [what the model predicts if one input is nudged, all else fixed] (`modeling/tables/counterfactuals.csv`; modeled):

| Change | Rows tested | Mean change (units/item-day) | 95% interval | % change |
|---|---|---|---|---|
| Price 10% lower | 845,806 | +0.0205 | +0.0201 to +0.0210 | +1.43% |
| Price 10% higher | 845,140 | +0.0222 | +0.0220 to +0.0224 | +1.55% |

Both directions raise predicted demand. That cannot be a real price response. The handoff reads it as promotions timed to busy weeks (handoff §5). Do not use it for pricing. Chart: `charts/08_counterfactuals.png`.

The real levers are operational: order quantity, safety stock, delivery cadence, range breadth and shelf space (memo §3.2). The model informs all five but does not measure their effect.

## B5. Where volume sits: one tenth of item-days holds over half the units

**By category, 28 test days** (`tables/segment_volume_at_risk.csv`; handoff §6; measured; series counts corrected per followups R2):

| Category | Item-store series | Units sold | Share of units | MAE | Total absolute forecast error (units) | Sales, $ |
|---|---|---|---|---|---|---|
| FOODS | 14,370 | 832,488 | 67.6% | 1.10 | 443,226 | $2,235,403 |
| HOUSEHOLD | 10,470 | 283,420 | 23.0% | 0.65 | 190,154 | $1,162,334 |
| HOBBIES | 5,650 | 115,856 | 9.4% | 0.65 | 102,431 | $503,239 |
| **Total** | **30,490** | **1,231,764** | **100%** | **0.86** | **735,812** | **$3,900,976** |

Dollar sales: followups Q1, measured.

**By decile** [one tenth of item-days, ranked by predicted volume] (`modeling/tables/decile_table.csv`; measured):

| Decile | Rows | Mean actual units | Mean predicted | MAE | Share of units | Cumulative share from top |
|---|---|---|---|---|---|---|
| 10 (top) | 85,372 | 7.69 | 7.67 | 2.99 | 53.3% | 53.3% |
| 9 | 85,372 | 2.38 | 2.36 | 1.44 | 16.5% | 69.8% |
| 8 | 85,372 | 1.49 | 1.46 | 1.10 | 10.3% | 80.1% |
| 7 | 85,372 | 1.02 | 1.01 | 0.84 | 7.1% | 87.2% |
| 6 | 85,341 | 0.72 | 0.72 | 0.73 | 5.0% | 92.2% |

Cumulative gain [share of all units captured by the top N deciles] comes from `tables/decile_risk_summary.csv`. These deciles rank item-days, not series (followups Q4 caveat).

**Velocity tiers by series** (followups R2 Q3; measured):

| Tier (training mean units/day) | Series | Share of series | Test units | Share of units |
|---|---|---|---|---|
| Fast (5 or more) | 1,267 | 4.2% | 376,025 | 30.5% |
| Mid (1 to under 5) | 7,984 | 26.2% | 535,529 | 43.5% |
| Slow (under 1) | 21,239 | 69.7% | 320,210 | 26.0% |

**Threshold trade-off: rounding small forecasts to zero** (`tables/fu5_rounding_below_0.5.csv`; modeled):

| Category | Zero-sale days with forecast under 0.5 | MAE before | MAE after | RMSE before | RMSE after |
|---|---|---|---|---|---|
| FOODS | 56.1% | 1.102 | 1.076 | 2.093 | 2.098 |
| HOBBIES | 78.5% | 0.647 | 0.599 | 1.452 | 1.464 |
| HOUSEHOLD | 75.2% | 0.649 | 0.606 | 1.156 | 1.170 |
| All | 68.6% | 0.862 | 0.826 | 1.707 | 1.715 |

Rounding lowers the average miss but slightly raises big misses. Use it for whole-unit orders, not for volume plans (followups Q5).

**Smallest intervention** (`tables/smallest_intervention.csv`; modeled ranking):

| Goal | Series to treat | Share of 30,490 |
|---|---|---|
| Capture 50% of forecast volume | 2,829 | 9.3% |
| Capture 80% of forecast volume | 10,034 | 32.9% |

## B6. The strategy: replace the rule on the busy third, fix stockout data, test the rest

### Internal metrics against external benchmarks (memo §2)

| Metric | This business | Benchmark | Benchmark label |
|---|---|---|---|
| Error cut vs current method | RMSE -24.4%, MAE -19.7% (measured) | 20% to 50% from AI forecasting | assumed: McKinsey page not fetched, https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments |
| Inventory distortion [cost of empty shelves plus excess stock] | Not measurable | 6.5% of retail sales; 9.3% in general merchandise | external, https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos |
| Empty-shelf losses | Rule under-forecasts 9% more than it over-forecasts (measured) | $690.1B globally | external, Board/IHL (above) |
| AI adoption in planning | Rule only | Under 25% deployed; 76% of adopters report positive results | external, Board/IHL |
| Inventory turns [cost of goods sold / average stock] | Not measurable | Walmart 9.10 turns, 40 days on hand, FY to Jan 2026 | external, https://www.stock-analysis-on.net/NASDAQ/Company/Walmart-Inc/Ratios/Short-term-Operating-Activity |
| SNAP lift, FOODS | +14.8% (test window, measured) | +5.6% average grocer; +19.2% high-SNAP ZIPs | assumed: PDF blocked; abstract at https://econpapers.repec.org/RePEc:aea:aejpol:v:14:y:2022:i:1:p:152-78 |
| Out-of-stock rate | Unknown | 8.3% average | assumed: Gruen and Corsten, not fetched |
| Safety-stock service factor | No target set | z = 1.65 (95%), 2.05 (98%), 2.33 (99%) | external, https://www.cleverence.com/articles/business-blogs/safety-stock-retail-inventory-4827/ |

### The value levers (memo §1, §3.3)

| Lever | What changes | Size per year, 10 stores | Label |
|---|---|---|---|
| Fewer empty shelves on fast items | Model under-orders 108,337 fewer units than the rule in 28 days | $0.16M to $0.41M extra revenue | assumed (8% stockout rate, 40% lost, 10-25% cut) on a measured gap |
| Leaner safety stock [spare units held to cover misses] | Dollar-weighted per-series error falls 20.7% ($150,842 to $119,635) | $102K to $127K one-time at cost; $26K to $32K a year holding saving | modeled plus assumed (7-day lead time, 75% cost ratio, 25% carrying rate) |
| Stop over-stocking the slow tail | Round tiny forecasts to zero | MAE -7% in HOBBIES and HOUSEHOLD | modeled |
| Hidden stockouts (if real) | 4,086 zero days on fast series | Up to about $0.72M | assumed (5 units x $2.69 per zero day, annualised) |

Annual sales base: about $50.9M, annualised from $3.90M in 28 days (assumed scaling of a measured figure; memo §1).

### Recommendations by track (memo §4)

| Track | Action | Basis |
|---|---|---|
| A1 | Feed the 28-day forecast into the nightly order run | handoff §4 |
| A2 | Managers review only orders where model and rule differ a lot | memo |
| A3 | Keep 10% of series on the rule as a permanent holdout [untreated comparison group] | memo |
| A4 | Round slow-tail orders; build a two-part model [first "any sale?", then "how many?"] next refresh | followups Q5; handoff §7 |
| A5 | Weight SNAP by store-area participation | handoff §7 issue 8 |
| A6 | Capture on-hand stock and stockout flags | handoff §7 issue 1 |
| A7 | Retrain monthly; alert if gain over holdout falls under 10% or bias drifts past ±5% | handoff §7 issue 4 |
| B1 | Set service targets by velocity tier | memo §3.4 |
| B2 | Raise FOODS orders about 15% for SNAP days | followups Q6 |
| B3 | Cut buffers on HOBBIES_2 and HOUSEHOLD_2; review range of series over 85% zero days | chart 01 |
| B4 | Operations review in WI_2 and CA_3 | test_by_store.csv |
| B5 | Add GMROI [gross profit per dollar of stock] and in-stock rate to scorecards | memo |
| B6 | Do not justify promotions with the model's price signal | handoff §5 |

Service targets proposed (memo §3.4; all assumed): fast shelf-stable 98%; fast perishable 90%; mid velocity 95%; slow tail 90% with minimum display.

### The five pilots (memo §5)

Randomisation is by item-store series within store, stratified [split evenly inside each group] by category and velocity. Only 10 stores exist, so store-level tests lack power.

| Pilot | Who is in it | Length | North Star [the deciding metric] | Kill / scale rules |
|---|---|---|---|---|
| 1. Model ordering, fast and mid tiers | 9,251 series, ~4,625 per arm | 8 weeks min | Inventory $ per $ of sales | Day 30 kill if in-stock drops >1 point; day 60 scale if inventory -8% and in-stock flat; day 90 chain-wide if override rate <10% |
| 2. SNAP pre-positioning, FOODS | Fast and mid FOODS series, 50/50 | ~90 days (3 SNAP cycles) | FOODS units per series on SNAP days | Day 30 kill if post-SNAP stock +10% with no sales gain; day 90 scale if SNAP sales +1% |
| 3. Slow-tail rounding | 12,954 slow HOBBIES and HOUSEHOLD series | 12 weeks | Inventory $ per series | Day 30 kill if sales -5%; day 90 scale if inventory -5% and sales fall <2% |
| 4. Hidden-stockout audit | 1,267 fast series, 213 run-of-zeros first; ~150 checks a day | 4 weeks | Share of zero days that were stockouts | >20%: fund flags chain-wide; 5-20%: top decile only; <5%: close |
| 5. Randomised price test | 100-200 FOODS items, ±5% price | 12 weeks | Elasticity [demand change per 1% price change] with interval | Stop if margin falls >1 point; use only if interval excludes zero |

Hypothesised effects (8-15% inventory cut, 1-3% SNAP sales, 5-15% slow-tail inventory, ≥20% stockouts) and the 6% minimum detectable change are all assumed.

### Prioritisation (memo §6.1)

| Wave | Initiatives | Impact | Confidence |
|---|---|---|---|
| 1 (now) | Tiered service targets; SNAP uplift on the rule; slow-tail buffer cut; WI_2/CA_3 review; GMROI scorecard; Pilot 4 audit | Med, High for Pilot 4 | Med to High |
| 2 | Pilot 1 model ordering; Pilot 3 rounding; Pilot 2 SNAP | High, Med, Med | High, Med, Med |
| 3 | Stockout flags and on-hand feed; Pilot 5 price test; two-part model and SNAP intensity | High, Med-High, Med | High, Low, Med |

## B7. The agent dialogue and notebook review

The growth strategist sent nine questions in two rounds to the statistician. All were answered; none were declined (dialogue, closing note). Questions below are verbatim; answers are quoted from followups.

| Round | Q | Memo section | Question (verbatim) | Answer (from followups) | What changed in the memo |
|---|---|---|---|---|---|
| 1 | 1 | §3 dollar translation | "Average sell_price (USD) per unit by category over the test window d_1914–d_1941, and total test-window dollar sales by category (units × weekly sell_price)." | FOODS $2.69, HOBBIES $4.34, HOUSEHOLD $4.10 per unit; total $3,900,976 | Dollar base of $3.90M per 28 days, ~$50.9M a year |
| 1 | 2 | §2 gap table, §3 | "Rule-of-thumb RMSE and MAE by category (FOODS, HOBBIES, HOUSEHOLD) on the same test window, so the partner can state the improvement per category." | "MAE improvement: FOODS 21%, HOBBIES 16%, HOUSEHOLD 19%." Rule "rebuilt"; "the model-builder's exact rule is unknown." | Per-category gains added; open item 1 added |
| 1 | 3 | §3 asymmetric errors | "Error direction, model vs rule, by category: total over-forecast units (sum of max(pred−actual,0)) and total under-forecast units (sum of max(actual−pred,0)) over the 28 test days." | Model over 364,668 / under 371,143; rule over 438,103 / under 479,480. "the rule's under-forecast exceeds its over-forecast by 9%" | Lever 1 rests on 108,337 fewer short units; $343K demand at risk per 28 days |
| 1 | 4 | §3 targeting | "Model vs rule MAE in the top decile of series (is_top_decile == 1) versus deciles 1–9." | Decile 10 MAE 2.973 vs 3.763; deciles 1-9 0.625 vs 0.773. "is_top_decile is a decile of item-DAY predictions ... not of series." | "Where value leaks" bullets; Pilot 1 trigger |
| 1 | 5 | §4 HOBBIES rounding | "Share of HOBBIES test item-days with actual = 0 where model pred is between 0 and 0.5, and the MAE change if preds < 0.5 are set to 0 (one number per category)." | HOBBIES 78.5%; MAE 0.647 → 0.599. "Rounding lowers MAE 4-8% but raises RMSE slightly" | Lever 3, Pilot 3, rounding for orders only |
| 1 | 6 | §5 SNAP pilot | "Model MAE on FOODS for SNAP vs non-SNAP test days, and the same for the rule-of-thumb." | Model 1.158 vs 1.070; rule 1.468 vs 1.353. "Both forecasters err more on SNAP days" | 14.8% lift; Track B2; Pilot 2; open item 4 |
| 2 | 1 | §3 inventory dollars | "Per-series error dispersion, dollar-weighted ... report the SUM across all 30,490 series (USD), by category and total." | Model $119,635 vs rule $150,842; "Model is 20.7% below the rolling rule" | Stock release fell from $175K-$217K to $102K-$127K; holding saving from $44K-$54K to $26K-$32K; profit share from 0.3-0.8% to 0.1-0.3% |
| 2 | 2 | §5 stockout audit | "Possible hidden stockouts: among series with training-period mean ≥ 5 units/day, how many test item-days had zero sales, and how many series had a run of 3+ consecutive zero days? By category if easy." | 4,086 zero days of 35,476 (11.5%); 213 series with 3+ day runs. "suspicious but not proof" | New "hidden prize" paragraph; Pilot 4 widened from 2 stores to all 10 |
| 2 | 3 | §4 tiering | "For the velocity cut (series mean ≥ 5 vs < 1 unit/day vs in between): series count and share of test units in each tier." | 1,267 / 7,984 / 21,239 series; 30.5% / 43.5% / 26.0% of units | Pilot 1 group 10,034 → 9,251; Pilot 3 group 16,120 → 12,954 |

**Unrequested correction (round 2).** The handoff §6 "series count" column counted items (3,049), not item-store series (30,490). Units and errors were unaffected (followups R2; memo §7 item 5).

**Notebook review outcome** (review):

| Notebook stage | Gaps found, first pass | Fixed | Remaining after the one allowed fix round |
|---|---|---|---|
| 01 exploration | 6 | 6 | 5 new or partial: per-test explanations for H2-H5, interpretation after tests, method rationale and reading guide for the baseline, note on a $195M revenue output |
| 02 feature engineering + 03 modeling | 13 | 13 addressed | 5: XGBoost search-space table, XGBoost rationale, price-ratio chart method notes, explanations before RMSSE and decile cells |

All three notebooks re-ran with 0 errors after fixes (review). Remaining gaps are documentation gaps, not calculation errors.

---

# Part C. Checks and limits

## C1. Consistency check: numbers that appear in two or more reports

| Number | Where it appears | Verdict |
|---|---|---|
| Test RMSE 1.707 vs rule 2.259, 24.4% | card, handoff §4, memo §2-§3 | Agree |
| Test MAE 0.862 vs 1.074 | card, handoff §4, memo §1 (rounded to 20%) | Agree |
| Mean RMSSE 0.708 | card, handoff §4 | Agree; mean of `test_rmsse_per_series.csv` is 0.7077 over 30,453 of 30,490 series (37 blank) |
| Rule RMSSE "1.000" | card, handoff §4 | **Discrepancy.** Both files define RMSSE against a naive forecast, so 1.0 is the naive baseline, not the rule |
| Rule RMSE | 2.259 (card) vs 2.219 (followups, rebuilt rule) | **Discrepancy, explained.** Two rebuilds of the rule; memo category gains use 2.219 |
| Training dates for d_1211 to d_1885 | card: "2015-07-18 to 2015-07-02"; handoff: 2014-05-23 to 2016-03-27 | **Discrepancy.** Card dates are impossible (end before start); handoff dates match the day index |
| Training window length | card and handoff: "~2 years"; d_1211 to d_1885 is 675 days | Minor: closer to 1.85 years |
| Best LightGBM score | tuning 1.6723 (CV) vs card 1.7430 (validation) | Different windows; handoff §4 reconciles |
| "Val RMSE" 1.707 for final LightGBM | handoff §4 comparison table | **Mislabel.** 1.707 is the test RMSE |
| Overall zero-sale share | findings and handoff: "roughly half"; data dictionary and audit: 68.0% of all cells | **Discrepancy.** Different bases (full history vs model window); not reconciled in the files |
| HOBBIES / FOODS zero rates | findings text 83% / 65%; chart and handoff ~77% / ~62% | **Discrepancy**, noted by handoff §3 as minor |
| Sparsest department | chart 01 title "HOBBIES_1 sparsest"; chart bars and memo show HOBBIES_2 (~88%) | **Discrepancy** in the chart title |
| Concentration, top 20% | findings and chart 04 title ~60%; chart 04 annotation "bottom 80% = 30%" (so ~70%); data dictionary ~70%; decile summary 69.8% (item-days) | **Discrepancy** |
| Deciles labelled "series" | decile_risk_summary, handoff §6 | **Mislabel.** Rows are item-days (85,372 = 10% of 853,720), per followups Q4 |
| "Bottom 70% of series hold ~20% of units" | memo §3.1 citing handoff §6 | Built on item-day deciles; series tiers show 69.7% of series hold 26.0% |
| Series count by category | handoff §6: 1,437 / 1,047 / 565 | **Error, corrected** in followups R2: 14,370 / 10,470 / 5,650 |
| SNAP lift | hypotheses +10.4% (CA); findings and chart "10-20%"; followups +14.8% (test, pooled) | Consistent range; different windows |
| Sporting-event lift | findings +3%; hypotheses +3.5%; findings heading "largest demand spike" | Heading overstates an unreliable result (CI includes zero) |
| FOODS vs HOUSEHOLD volatility (H5) | findings: "effect size was small"; hypotheses result r = 0.51 (0.49-0.52), "difference exists" | **Contradiction** between the two explorer files |
| Counterfactuals +0.021 / +0.022 | card, handoff §5, csv | Agree |
| Aggregate bias within 0.5% | handoff §6, memo §4 A7 | Agree |
| Velocity tiers 1,267 / 7,984 / 21,239 | followups R2 Q3, memo §3.4 and §5 | Agree |
| SHAP is "dollar-sized" | handoff glossary | **Error.** SHAP values are in units (shap_importance.csv, chart 06 axis) |
| "21 charts" | memo header | `reports/charts/` and `reports/modeling/charts/` hold 18 PNGs |

## C2. Strategy claims with no supporting number in the handoff report

| Memo claim | Where its number comes from | Label |
|---|---|---|
| $50.9M annual sales | followups Q1, annualised | assumed scaling |
| $0.16M-$0.41M revenue from fewer stockouts | Unfetched 8% stockout rate, assumed 40% loss, 10-25% cut | assumed |
| $102K-$127K stock release; $26K-$32K holding saving | followups R2 Q1 plus assumed lead time, cost ratio, carrying rate | modeled plus assumed |
| Up to $0.72M from hidden stockouts | followups R2 Q2 plus assumed 5 units at $2.69 | assumed |
| 0.1% to 0.3% of sales in profit | memo arithmetic on the above | assumed |
| SNAP uplift of 14.8% | followups Q6 only; handoff says 10-20% | measured, one 28-day window |
| Category MAE gains 21% / 19% / 16% | followups Q2, against a rebuilt rule | measured, rule assumed |
| 7% MAE cut from rounding | followups Q5 | modeled |
| Service targets 90-98% and Cu/Co costs | memo §3.4 | assumed |
| Pilot effect sizes and 6% minimum detectable change | memo §5 | assumed |

## C3. Benchmarks the memo marked unverified

| Benchmark | Why unverified |
|---|---|
| McKinsey 20-50% error cut | Page timed out twice |
| Goldin, Homonoff, Meckel: +5.6% / +19.2% SNAP-week food sales | PDF blocked (403); only abstract read |
| Gruen and Corsten: 8.3% out-of-stock rate, 72% caused in-store | Search result only |
| Carrying-cost rate 20-30% | Vendor pages seen in search only |
| Official M5 winning score | Not found in the fetched abstract |
| IHL product page | Blocked (403); the Board blog summary was used instead |

## C4. Limitations and failure modes (merged from all reports)

| # | Limitation | Effect on the decision | Source |
|---|---|---|---|
| 1 | No stockout flag: a zero may be an empty shelf | True demand on fast items is understated; lost sales cannot be measured | handoff §7.1, findings, card |
| 2 | The live rule and its buffer are unknown | Real stock release could be larger than estimated | followups method note; memo §7.1 |
| 3 | No replenishment simulation at a stated service level was run | The brief's "inventory dollars and lost sales at a fixed service target" is answered by formula, not simulation | problem "Deliverable"; handoff §7 assumptions; memo §3.3 |
| 4 | Price signal is association, not cause | No pricing or promotion decisions from the model | card, handoff §5 |
| 5 | Small positive forecasts for slow items | Over-ordering on the slow tail unless rounded | card, handoff §7.3 |
| 6 | Model ages; trained to early 2016 | Must retrain monthly | handoff §7.4 |
| 7 | New items lack history | Need a category-median rule for 28 days | handoff §7.5 |
| 8 | Some department-store cells are small | Noisy store-level error figures | handoff §7.6 |
| 9 | SNAP flag is state-wide | Adds noise where few shoppers use SNAP | handoff §7.8 |
| 10 | SNAP and test findings rest on one 28-day window | Lift may vary by month | memo §7.4 |
| 11 | Only unweighted mean RMSSE reported | The competition's dollar-weighted WRMSSE was not reported | card; problem "Data" |
| 12 | No forward 28-day forecast beyond the test window, and no offer sheet, are described in the reports | Two brief deliverables are not evidenced | problem "Deliverable expected" |
| 13 | Notebook documentation gaps remain (10) | Harder to audit, not wrong | review |
| 14 | Feature check chart shows empty middle price-ratio buckets | Price-ratio feature may be poorly populated; unexplained in the files | `modeling/charts/fe_price_check.png` |

## C5. Instrumentation gaps, in priority order

1. Daily on-hand stock and a stockout flag per item-store (handoff §7.1; memo A6).
2. The live replenishment formula, including its buffer (memo §7.1).
3. Lead times, receipts, waste and markdowns per item (memo A6).
4. Finance inputs: cost ratio, gross margin, carrying-cost rate (memo §7.3).
5. Shelf capacity and minimum display quantities (memo A6).
6. Store-level SNAP participation (handoff §7.8).

---

# Part D. Appendix

## D1. Glossary

| Term | Plain meaning |
|---|---|
| Association | Two things move together; one may not cause the other |
| At cost | Valued at what the retailer paid, not the shelf price |
| Bias (forecast) | Whether forecasts run high or low on average |
| Bootstrap | Re-sampling the data many times to estimate a range |
| CatBoost | A tree-boosting method, cousin of LightGBM |
| Coefficient of variation (CV) | Spread divided by average; higher means lumpier |
| Confidence interval (95%) | The range the true value likely sits in |
| Controllable lever | A factor the business can change, such as price |
| Counterfactual sensitivity | Model's predicted change when one input is nudged |
| Cross-validation (CV RMSE) | Scoring a model on held-back slices of past data |
| Cu / Co | Cost of one unit short / one unit over |
| Cumulative gain | Share of all units captured by the top N deciles |
| Decile | One tenth of a ranked list |
| Effect size | How big a difference is, separate from whether it is real |
| Elasticity | Percent change in demand for a 1% price change |
| Gini coefficient | Concentration score: 0 equal, 1 all in one series |
| GMROI | Gross profit per dollar of average stock |
| Gradient boosting | Building many small trees, each correcting the last |
| Grain | What one row represents |
| Guardrail metric | A metric that must not get worse in a test |
| Held-out test | Data kept back and scored once, after all tuning |
| Holdout group | Series kept on the old rule to measure impact |
| Hyperparameter | A setting chosen before training, such as tree size |
| In-stock rate | Share of item-store-days with stock on the shelf |
| Intermittent demand | Sales that happen on few days |
| Inventory distortion | Combined cost of empty shelves and excess stock |
| Inventory turns | Cost of goods sold divided by average stock |
| Item-day / item-store-day | One item in one store on one day |
| Lag feature | An input built from past sales, such as yesterday's |
| Lead time | Days from order to stock on shelf |
| LightGBM | The chosen model: a fast tree-boosting method |
| Lift | How much a group beats the average |
| Lorenz curve | Cumulative share of series vs cumulative share of units |
| MAE | Mean absolute error: average size of a miss, units per item-day |
| Mann-Whitney test | Compares two groups without assuming a bell curve |
| Minimum detectable change | Smallest effect a test can reliably detect |
| Naive forecast | "Sales equal a past day's sales"; the floor to beat |
| Newsvendor rule | Stock to the level met with probability Cu / (Cu + Co) |
| North Star metric | The one metric that decides a pilot |
| Optuna | A tool that tries many settings and keeps the best |
| Parameter importance | Share of score variation each setting explains |
| Random Forest | Many independent trees, averaged |
| Rank-biserial r | Effect size from -1 to 1 for how often one group beats another |
| Reconstructed rule | The rule rebuilt by the analysts, as the live one was not supplied |
| Residual | Actual minus predicted |
| Ridge | A straight-line formula with a penalty on large weights |
| RMSE | Root mean squared error: typical miss, weighting big misses more |
| RMSSE | RMSE divided by a naive forecast's error; under 1 beats naive |
| Rolling mean | Average over a moving window, such as the last 7 days |
| Safety stock / buffer | Spare units held to cover forecast misses |
| Series | One item in one store over time (30,490 in all) |
| Service level | Chance that stock covers demand in a cycle |
| SHAP | Splits each forecast into each input's contribution, in units |
| SNAP | US federal food benefit, paid on set days by state |
| Stockout | No stock on the shelf |
| Stratified randomisation | Random split done inside groups so arms stay balanced |
| Structural driver | A factor the business cannot change soon, such as weekday |
| Trial (Optuna) | One full model fit with one set of settings |
| Uplift targeting | Acting only where the action changes the outcome |
| Validation set | Data used to choose between models before the test |
| Velocity tier | Fast, mid or slow, by average daily units |
| WRMSSE | RMSSE weighted by each series' dollar sales; the M5 metric |
| XGBoost | A tree-boosting method, cousin of LightGBM |
| z (service factor) | Multiplier on error that sets service level, e.g. 1.65 for 95% |
| Zero-inflation | Many more zero values than usual |

## D2. Chart manifest

| File | What it shows | Key takeaway |
|---|---|---|
| `charts/01_zero_rate_by_category.png` | Zero-sale rate by category and department | HOBBIES sells nothing on ~77% of days; HOBBIES_2 ~88% |
| `charts/02_snap_effect.png` | FOODS units per item-day, SNAP vs non-SNAP, by state | SNAP days sell more in all three states |
| `charts/03_demand_category_weekday.png` | Units per item-day by weekday and category | FOODS jumps at weekends; others rise less |
| `charts/04_sales_concentration.png` | Lorenz curve of units across series | Demand is concentrated (Gini 0.67) |
| `charts/05_model_comparison.png` | Validation RMSE by model | Every learned model beats the rule; LightGBM best |
| `charts/06_shap_importance.png` | Top 20 drivers by mean SHAP | 7-day average dominates; price is minor |
| `charts/07_decile_lift.png` | Units by decile; residual histogram | Top decile holds 53% of units; errors centre on zero |
| `charts/08_counterfactuals.png` | Predicted change for ±10% price | Both directions raise demand: an artefact, not a lever |
| `modeling/charts/optuna_lgb_history.png` | LightGBM trial scores and parameter importance | Gains flatten after ~40 trials; leaf size matters most |
| `modeling/charts/optuna_xgb_history.png` | XGBoost trial scores and parameter importance | Same pattern; min_child_weight dominates |
| `modeling/charts/fe_calendar_check.png` | Weekday and SNAP checks on the training split | Weekend and SNAP lifts survive in the features |
| `modeling/charts/fe_correlations.png` | Each input's correlation with units | Recent-sales inputs correlate most; zero rate most negative |
| `modeling/charts/fe_price_check.png` | Mean units by price-ratio bucket | Middle buckets are empty (unexplained) |
| `modeling/charts/fe_zero_rate_hist.png` | Series zero-rate spread, FOODS vs HOBBIES | HOBBIES series cluster near 80-95% zero days |
| `modeling/charts/model_comparison.png`, `shap_importance.png`, `decile_lift.png`, `counterfactuals.png` | Copies of charts 05-08 | Same as above |
| `exploration/charts/02`, `03`, `05`, `07`, `08`, `10`, `11` | Further exploration views (demand spread, weekday, trend, events, price, stores, CV) | Listed in findings "Charts produced" |

## D3. Web sources (from memo §6.2)

| Source | One-line summary | Status |
|---|---|---|
| https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos | IHL study: $1.7T distortion, 6.5% of sales, $690.1B empty shelves, <25% AI adoption | fetched |
| https://fortune.com/2025/07/23/walmart-amazon-ai-supply-chain-retail/ | Walmart and Amazon use AI demand forecasting to cut overstock | fetched |
| https://www.stock-analysis-on.net/NASDAQ/Company/Walmart-Inc/Ratios/Short-term-Operating-Activity | Walmart 9.10 inventory turns, 40 days on hand | fetched |
| https://econpapers.repec.org/RePEc:aea:aejpol:v:14:y:2022:i:1:p:152-78 | SNAP drives large monthly food-spend cycles; retailers do not change prices | abstract fetched |
| https://www.cleverence.com/articles/business-blogs/safety-stock-retail-inventory-4827/ | Safety stock formula and z values by service level | fetched |
| https://ideas.repec.org/a/eee/intfor/v38y2022i4p1346-1364.html | M5 scope: 42,840 series, 30,490 bottom-level | fetched |
| https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments | AI forecasting cuts errors 20-50% | not fetched |
| https://github.com/Nixtla/m5-forecasts | Public mirror of the M5 data | data source |

## D4. Files produced

Notebooks first:

| File | What it shows |
|---|---|
| `notebooks/01_exploration.ipynb` | Data audit, cleaning, five hypothesis tests and exploration charts (77 cells) |
| `notebooks/02_feature_engineering.ipynb` | Builds the 35 model inputs and checks them (40 cells) |
| `notebooks/03_modeling.ipynb` | Baselines, model comparison, Optuna tuning, test scoring, SHAP, deciles, counterfactuals (49 cells) |

Other files (fresh listing of `reports/`, `models/`, `src/`, `notebooks/`):

| Folder | Files |
|---|---|
| `reports/` | `final_report.md`, `final_report.html`, `ml_handoff_report.md`, `executive_growth_strategy.md`, `ml_followups.md`, `agent_dialogue.md`, `notebook_review.md`, `customer_risk_scores.csv` (853,720 item-day forecasts; name is a template carry-over) |
| `reports/charts/` | 8 PNGs (01 to 08) |
| `reports/tables/` | `segment_volume_at_risk.csv`, `decile_risk_summary.csv`, `smallest_intervention.csv`, `segment_store_x_category.csv`, `fu1` to `fu9` follow-up tables (9 files) |
| `reports/exploration/` | `findings.md`, `hypotheses.md`, `data_dictionary.md` and `.csv`, `cleaning_log.md`, `quality_audit.md`, `handoff_to_modeling.md`, `clean.parquet`, `calendar_clean.parquet`, `sell_prices_clean.parquet`, `charts/` (11 PNGs) |
| `reports/modeling/` | `model_card.md`, `tuning.md`, `features.md`, `features.parquet`, `scores.csv`, `tables/` (8 CSVs), `charts/` (10 PNGs) |
| `models/` | `demand_forecast_model.joblib`; Optuna studies `optuna_lgb.db`, `optuna_lgb_v2.db` (120 trials, used), `optuna_xgb.db`, `optuna_xgb_v2.db` (109 trials, used) |
| `src/` | `explore_utils.py`, `features.py`, `model_utils.py`, `pipeline.py`, `__init__.py` |
| `notebooks/catboost_info/` | CatBoost training logs |
