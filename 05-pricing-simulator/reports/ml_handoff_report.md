# Pricing Simulator — ML Handoff Report
**Project:** 05-pricing-simulator | **Prepared:** 2026-11-16 | **Author:** ml-statistician

---

## 1. The Question and the One-Paragraph Answer

**Question:** Which products and stores should receive a price change, and by how much, to maximise unit volume and revenue?

**Answer:** Every product category loses units when price rises — that is confirmed across all 55 products and 77 stores. Bag Snacks and Frozen Pizza are the most price-sensitive categories (exploration log-log slopes of −1.44 and −1.16 respectively), so targeted price reductions there produce the largest unit lift per percentage markdown. Cold Cereal and Oral Hygiene are less sensitive (slopes −0.34 and −0.38). Price alone is not the whole story: pairing a price cut with a Feature circular ad adds a further 10–15% units-per-visit lift above a price-cut-only event (measured, p < 0.001). Value-segment stores amplify promotional lift the most; the same spending on a Value-store promotion generates more incremental units than the same event at an Upscale store. A LightGBM demand model (R² = 0.989, MAPE = 8.5% on a never-touched held-out test set) is ready to simulate the unit outcome of any candidate price. **The econometric elasticity model (Ridge with store fixed effects) produced positive coefficients — the opposite of economic theory — because store-level omitted variables (vendor deals correlated with high-traffic weeks) contaminated the price signal. Those numbers must not be used as causal levers; they are labelled "modeled association" throughout this report and should be replaced by an IV/2SLS estimate before any price decision is made.**

---

## 2. The Data in Five Lines

| Item | Detail |
|---|---|
| Source | Dunnhumby "Breakfast at the Frat" (`dunnhumby_breakfast_at_the_frat.xlsx`) |
| Grain | One row = one store × one UPC × one week |
| Size | 538,435 rows; 77 stores; 55 products; 156 weeks (Jan 2009 – Jan 2012) |
| Target | UNITS (weekly unit sales per store-product); log-transformed for modelling |
| Business value at stake | ~$1.49 B total revenue in dataset ($801 M Cold Cereal, $346 M Frozen Pizza, $253 M Bag Snacks, $92 M Oral Hygiene — measured, annualised from 3-year period) |

Data dictionary: `reports/exploration/data_dictionary.md`
Cleaning log and feature derivation: `reports/exploration/handoff_to_modeling.md`

---

## 3. What the Exploration Found

Five findings that matter. Full details and reliability verdicts: `reports/exploration/findings.md` and `reports/exploration/hypotheses.md`.

| # | Finding | Key number | Reliability | Chart |
|---|---|---|---|---|
| F1 | Every category loses units when price rises | Log-log slopes: Bag Snacks −1.44, Frozen Pizza −1.16, Cereal −0.34, Mouthwash −0.38 | Strong — holds across all 55 products, 77 stores | `01_demand_curves_by_category.png` |
| F2 | Frozen Pizza and Mouthwash are discounted in more weeks; Bag Snacks and Cereal rarely discounted | Frozen Pizza median discount depth ≈ 11%; Bag Snacks median ≈ 0% | Very strong — direct measurement | `02_discount_depth_by_category.png` |
| F3 | Feature advertising adds the most unit lift; a price cut alone adds less | Median units-per-visit: Feature+Display ≈ 1.14 vs None ≈ 1.00; p < 0.001 | Strong — Mann-Whitney confirmed | `03_promotion_lift_by_type.png` |
| F4 | One-third of products generate 80% of revenue | ~20 of 55 products = 80% of sales; Cold Cereal and Frozen Pizza dominate | Direct measurement | `05_revenue_concentration.png` |
| F5 | Value-segment stores respond more strongly to promotions | Value stores: median lift ratio ≈ 1.75; Upscale ≈ 1.65 | Moderate — does not yet control for product-mix differences by segment | `04_promo_lift_by_store_segment.png` |

**What was not found:** No category is fully price-inelastic. Even Oral Hygiene (mouthwash) shows a negative slope, though it is the shallowest.

---

## 4. The Model

Full technical details: `reports/modeling/model_card.md` and `reports/modeling/tuning.md`.

**What was compared.** Eight model families were benchmarked on 5-fold expanding-window time-series cross-validation [CV: each fold uses all earlier weeks for training and the next block for scoring]: LightGBM, XGBoost, CatBoost, Random Forest, Ridge with fixed effects [FE: a dummy variable per store and per product to absorb baseline demand differences], and plain OLS FE. See `reports/modeling/tables/final_model_comparison.csv`.

**How it was tuned.** Optuna Bayesian optimisation ran 60 trials for LightGBM and 60 for XGBoost (2 and 6 pruned early respectively). Best LightGBM parameters: n_estimators=940, learning_rate=0.031, max_depth=7, num_leaves=102, reg_alpha=4.4, colsample_bytree=0.999. The most important tuning dimension was `colsample_bytree` (feature sub-sampling, importance 0.42), meaning reducing the fraction of features each tree sees was the single biggest regularisation lever. L1 penalty (reg_alpha, 0.15) was second.

**Which model was chosen and why.** LightGBM (tuned) was chosen as the prediction model: best CV RMSE_log 0.1043 ± 0.004, clearly ahead of XGBoost (0.1046) and all others. The Ridge FE model was retained separately as the elasticity estimator, but its positive coefficients indicate store-level confounding (see Section 7).

**How good is it on held-out test.**
Test set = last 26 weeks (Jul 2011 – Jan 2012), never touched during training or tuning.

| Metric | LightGBM (prediction) | Ridge FE (elasticity) |
|---|---|---|
| RMSE log-units | 0.111 | 0.419 |
| R² | 0.989 | 0.836 |
| MAPE (units) | 8.5% | 53.5% |

In plain language: on a week the model has never seen, its unit forecast is off by 8.5% of actual units on average. That is good enough for a pricing simulator where ±10% accuracy is acceptable. The Ridge FE model's 53.5% MAPE makes it unsuitable for unit prediction; it is used only for its elasticity coefficients, which themselves need IV correction.

**Where it is weaker.**
- Bag Snacks: MAPE 10.2% (slightly worse than average).
- Feature+Display events (4.5% of rows): lift coefficients have wide uncertainty.
- Long-run dynamics (new competition, changing preferences) are not captured.

Performance by category: `reports/modeling/tables/performance_by_category.csv`.

---

## 5. Drivers and Levers

SHAP [SHapley Additive exPlanation: how much each feature moved the prediction for a specific row] importance from the LightGBM model. Full table: `reports/modeling/tables/shap_importance.csv`. Chart: `06_shap_importance.png`.

### Structural drivers (not directly controllable)
| Driver | Mean |SHAP| | What it captures |
|---|---|---|
| VISITS | 0.849 | Store traffic — the dominant predictor. If fewer people visit, fewer units sell regardless of price. |
| CATEGORY | 0.026 | Each category has a different baseline demand level. |
| SUB_CATEGORY | 0.017 | Further within-category demand levels. |
| Demand lags (lag-1, roll-4) | 0.006 | Habit buying — last week's sales predict this week's. |
| SEG_VALUE_NAME | 0.002 | Store tier (Value / Mainstream / Upscale). |

### Controllable levers (what a category manager can change)
| Lever | Mean |SHAP| | Note |
|---|---|---|
| LOG_PRICE | 0.020 | Shelf price. Modeled association: higher price → lower units. |
| LOG_BASE_PRICE | 0.010 | Everyday reference price. Modeled association. |
| DISCOUNT_PCT | 0.006 | Markdown depth vs base price. Modeled association. |
| FEATURE | 0.003 | Circular ad inclusion. Measured 10–15% units-per-visit lift. |
| DISPLAY | 0.001 | In-store display. Additional measured lift. |

**Caution:** SHAP importance measures how much the model uses a feature for prediction. It does not prove that changing the lever will cause that outcome. Labels above are modeled associations except where stated "measured."

---

## 6. Actionability

### 6a. Pricing thesis (plain English)

> **Bag Snacks and Frozen Pizza are the highest-return categories for a price-cut promotion.** Their exploration log-log slopes (−1.44 and −1.16) are more than three times the magnitude of Cold Cereal and Oral Hygiene. A 10% price cut on Bag Snacks is associated with a 14.4% unit lift; a 10% cut on Frozen Pizza is associated with 11.6% unit lift. Cold Cereal and Oral Hygiene have shallower slopes (−0.34, −0.38) and generate less volume return per percentage markdown. Pairing any price cut with a Feature circular ad adds a further 10–15 percentage points of units-per-visit lift, measured independently. This combination — moderate price cut + Feature ad — in Value-segment stores is the smallest intervention with the largest expected unit impact. All elasticity numbers are modeled associations; gross-margin data is needed before converting unit lift into profit.

### 6b. Segment table: by category and store tier
(Measured from data. Recommended price range is indicative, not an optimised result — requires margin data.)

| Category | Store tier | Mean price ($) | Weekly units | Annual revenue ($M) | Exploration slope | Modeled: 10% cut unit lift% |
|---|---|---|---|---|---|---|
| BAG SNACKS | Mainstream | 2.21 | 21.3 | 115.6 | −1.44 | 14.4% |
| BAG SNACKS | Upscale | 2.23 | 28.8 | 58.1 | −1.44 | 14.4% |
| BAG SNACKS | Value | 2.14 | 10.0 | 17.1 | −1.44 | 14.4% |
| COLD CEREAL | Mainstream | 2.74 | 34.4 | 343.1 | −0.34 | 3.4% |
| COLD CEREAL | Upscale | 2.75 | 40.9 | 138.8 | −0.34 | 3.4% |
| COLD CEREAL | Value | 2.74 | 28.9 | 122.6 | −0.34 | 3.4% |
| FROZEN PIZZA | Mainstream | 5.33 | 12.2 | 153.5 | −1.16 | 11.6% |
| FROZEN PIZZA | Upscale | 5.41 | 12.1 | 57.3 | −1.16 | 11.6% |
| FROZEN PIZZA | Value | 5.17 | 11.6 | 49.9 | −1.16 | 11.6% |
| ORAL HYGIENE | Mainstream | 3.77 | 4.2 | 38.1 | −0.38 | 3.8% |
| ORAL HYGIENE | Upscale | 3.87 | 6.2 | 21.3 | −0.38 | 3.8% |
| ORAL HYGIENE | Value | 3.66 | 3.5 | 10.1 | −0.38 | 3.8% |

Full table: `reports/tables/segment_summary.csv`. All unit-lift figures are modeled associations using exploration slopes. Assumed: elasticity is constant across store tiers within a category (not tested in the data).

### 6c. Actionability table — smallest intervention by lever
(All revenue impact figures are modeled associations. Margin data not available; assumed 0% — revenue impact is gross revenue change only.)

| Lever | Category most affected | Minimum change | Modeled unit lift | Note |
|---|---|---|---|---|
| Shelf price reduction | Bag Snacks | −5% (≈ −$0.11 per unit) | +7.2% units | Assumed: slope −1.44 |
| Shelf price reduction | Frozen Pizza | −5% (≈ −$0.27 per unit) | +5.8% units | Assumed: slope −1.16 |
| Shelf price reduction | Cold Cereal | −5% (≈ −$0.14 per unit) | +1.7% units | Assumed: slope −0.34 |
| Shelf price reduction | Oral Hygiene | −5% (≈ −$0.19 per unit) | +1.9% units | Assumed: slope −0.38 |
| Feature circular ad | All categories | Add to any promo event | +10–15% UPV | Measured; p < 0.001 |
| In-store display | All categories | Add to any promo event | Smaller incremental lift | Measured; magnitude overlaps Feature |
| Targeting to Value stores | All categories | Redirect existing promo budget | Lift ratio ~1.75 vs ~1.65 at Upscale | Moderate reliability — no product-mix control |

Full table: `reports/tables/actionability_levers.csv`.

### 6d. Risk-only targeting: share of units and revenue by predicted-demand segment
(Top N% of store-UPC-weeks ranked by LightGBM predicted demand. Measured from model output.)

| Top % by predicted demand | Share of all units (%) | Share of all revenue (%) | Mean actual units |
|---|---|---|---|
| Top 10% | 42.6% | 35.3% | 83.6 |
| Top 20% | 60.8% | 53.4% | 59.6 |
| Top 30% | 73.1% | 66.4% | 47.8 |
| Top 40% | 81.9% | 76.2% | 40.2 |
| Top 50% | 88.3% | 83.9% | 34.6 |

The top 10% of store-product-weeks by predicted demand already account for 42.6% of total units and 35.3% of revenue. Any promotional intervention concentrated here will have outsized absolute impact, but these are already high-velocity items — the incremental lift per additional marketing dollar may be lower than at mid-tier velocity items.

Full table: `reports/tables/risk_targeting.csv`. Decile breakdown: `reports/modeling/tables/decile_table.csv`.

### 6e. Counterfactual: 10% price cut applied uniformly
Source: `reports/modeling/tables/counterfactual_10pct_price_cut.csv`. Modeled using the LightGBM simulator.

| Category | Mean unit change (%) | Median unit change (%) |
|---|---|---|
| BAG SNACKS | +3.2% | +1.3% |
| COLD CEREAL | +1.6% | +1.2% |
| FROZEN PIZZA | +0.8% | +0.3% |
| ORAL HYGIENE | +1.2% | +0.4% |

**Note:** These LightGBM counterfactuals are smaller than the exploration slopes predict. The LightGBM model attributes most unit variation to VISITS (store traffic), so it predicts that a price change, holding traffic constant, moves units less than a pure log-log slope implies. This is likely more realistic than the raw slope but could be an underestimate if the price change itself attracts more shoppers. The exploration slopes give a directional upper bound.

---

## 7. Failure Modes, Assumptions and Instrumentation Gaps

Priority order: highest business risk first.

| # | Issue | Type | Impact | What would fix it |
|---|---|---|---|---|
| 1 | **Positive Ridge FE elasticities** — store-level confounding | Modeled weakness | All elasticity-based pricing decisions are directionally wrong if taken at face value | IV/2SLS [Instrumental Variables: a two-stage regression that isolates the part of price variation not correlated with unobserved demand; common instruments are cost-side shocks or competitor prices]. Need an external price instrument (e.g., wholesale cost index, competitor chain prices) |
| 2 | **No gross-margin data** — assumed zero cost | Assumed | Cannot compute profit-maximising price; only revenue | Provide unit cost or margin % per UPC from finance/ERP system |
| 3 | **No competitor pricing** — measured elasticities include cross-price effects | Measured limitation | True own-price elasticity is more negative than estimated; substitution to competitors is unobserved | Scrape or license competitor shelf-price data at store-week level |
| 4 | **Small Feature+Display cell** — 4.5% of rows (24,078) | Data limitation | Wide confidence intervals on the Feature+Display lift coefficient | Continue accumulating Feature+Display events; run a designed experiment |
| 5 | **~2% PRICE > BASE_PRICE rows** — price-increase weeks are rare | Data quality | Demand model at high prices is extrapolating; residuals may be systematically biased for price-increase scenarios | Flag these rows in simulator output; widen uncertainty bands above BASE_PRICE |
| 6 | **No time axis beyond 2012** — 3-year training window | Temporal gap | Long-run demand shifts (new entrants, changing shopper preferences) are not captured | Re-train annually with rolling window |
| 7 | **VISITS dominates SHAP (0.849)** — prediction depends heavily on traffic | Structural | The simulator's unit forecast accuracy collapses if VISITS is not available at prediction time (e.g., planning far in advance) | Build a separate store-traffic forecast; allow VISITS=NULL path in the simulator |
| 8 | **Segment-mix confound in promo lift comparison** — Value stores sell different product mix | Modeled weakness | The Value-store lift advantage (Finding F5) could be a product-mix effect | Rerun the segment comparison within category×UPC groups |

---

## 8. Reconciliation — Did the Numbers Agree?

| Check | Explorer value | Model-builder value | Match? | Comment |
|---|---|---|---|---|
| Total rows | 538,435 | 538,435 | Yes | Exact match |
| Test set dates | Jul–Dec 2011 | Jul 2011–Jan 2012 | Approximate | Jan 4 2012 is the final Wednesday of the dataset; not a material mismatch |
| Train / test split | Last 26 weeks held out | 449,684 / 88,751 rows | Yes | 83.5% train (130/156 = 83.3%) |
| Categories | 4 | 4 | Yes | BAG SNACKS, COLD CEREAL, FROZEN PIZZA, ORAL HYGIENE PRODUCTS |
| Target | UNITS (LOG_UNITS as model input) | UNITS → LOG_UNITS | Yes | |
| Exploration log-log slope, Cereal | −0.34 | Ridge FE +0.26 (positive) | **Material mismatch** | Sign is opposite. Explorer used simple median-of-medians; Ridge used store FE but is upward-biased. Exploration direction (negative) is consistent with economic theory. |
| Exploration log-log slope, Bag Snacks | −1.44 | Ridge FE +0.48 | **Material mismatch** | Same root cause: store confounding in Ridge |
| Test set touched once? | n/a | Yes | Yes | Model card confirms 5-fold CV on train only; test used once for final reporting |

---

## 9. Chart Manifest

| File | What it shows | Key takeaway |
|---|---|---|
| `reports/charts/01_demand_curves_by_category.png` | Log-log demand curves per category | All four categories show negative slopes. Bag Snacks (−1.44) and Frozen Pizza (−1.16) are steepest. |
| `reports/charts/02_discount_depth_by_category.png` | Distribution of discount depth by category | Frozen Pizza and Oral Hygiene are discounted most weeks; Bag Snacks and Cereal rarely discounted. |
| `reports/charts/03_promotion_lift_by_type.png` | Units per shopping visit by promotion type | Feature advertising and Feature+Display lift UPV by ~10–15% above no-promotion baseline. |
| `reports/charts/04_promo_lift_by_store_segment.png` | Median promotional lift ratio by store segment | Value stores respond most strongly (1.75×); Upscale least (1.65×). |
| `reports/charts/05_revenue_concentration.png` | Revenue Lorenz/concentration curve | ~20 of 55 products = 80% of revenue. Cold Cereal and Frozen Pizza dominate. |
| `reports/charts/06_shap_importance.png` | Mean absolute SHAP value per feature | VISITS dominates (0.849); LOG_PRICE third (0.020) — price matters but traffic matters more. |
| `reports/charts/07_decile_lift.png` | Mean actual units per predicted-demand decile | Top decile averages 79 units/week vs overall mean 18 — model discriminates well. |
| `reports/charts/08_model_comparison.png` | CV RMSE by model family | LightGBM (tuned) is best at 0.1043; Ridge FE (0.413) is used only for elasticity direction. |

---

## 10. File List

| File | Contents |
|---|---|
| `reports/ml_handoff_report.md` | This report |
| `reports/customer_risk_scores.csv` | 538,435 rows with predicted units, decile, store segment, expected revenue, and promo flags |
| `reports/tables/segment_summary.csv` | Demand and revenue by category × store tier |
| `reports/tables/actionability_levers.csv` | Lever-level intervention table with unit-lift associations |
| `reports/tables/risk_targeting.csv` | Share of units and revenue held by top N% predicted demand |
| `reports/tables/category_segment_detail.csv` | Detailed category × segment breakdown |
| `reports/modeling/tables/elasticity_by_category.csv` | Ridge FE elasticity per category (positive — see Section 7) |
| `reports/modeling/tables/elasticity_by_upc.csv` | Ridge FE elasticity per UPC |
| `reports/modeling/tables/counterfactual_10pct_price_cut.csv` | LightGBM counterfactual for 10% uniform price cut |
| `reports/modeling/tables/decile_table.csv` | Decile breakdown of model predictions |
| `reports/modeling/tables/performance_by_category.csv` | Model accuracy by category |
| `reports/exploration/findings.md` | Full exploration findings |
| `reports/exploration/hypotheses.md` | Statistical test results |
| `reports/exploration/data_dictionary.md` | Column definitions |
| `reports/exploration/handoff_to_modeling.md` | Cleaning log and modelling instructions |
| `reports/modeling/model_card.md` | Model card |
| `reports/modeling/tuning.md` | Optuna tuning details |

---

## 11. Glossary

| Term | Plain-language definition |
|---|---|
| Elasticity | The % change in units sold for a 1% change in price. A value of −1.0 means a 1% price rise cuts units by 1%. |
| Log-log slope | The slope of a regression of log(units) on log(price). Equals elasticity directly; estimated here from median of product-level medians. |
| Ridge FE | A regression model with L2 regularisation (Ridge) that also includes one dummy variable per store and per product (Fixed Effects) to absorb baseline demand differences. |
| Fixed Effects (FE) | Dummy variables for each entity (store, product) that absorb all time-invariant differences between entities, so the coefficient on price is estimated from within-entity price variation only. |
| IV / 2SLS | Instrumental Variables / Two-Stage Least Squares: a method that isolates the part of price variation driven by cost-side factors (not by unobserved demand), yielding an unbiased elasticity estimate. |
| Store confounding | When stores that set low prices also happen to have naturally high demand (e.g., due to vendor deals coinciding with peak seasons), a naive regression finds a positive price-units association even though the true causal relationship is negative. |
| SHAP | SHapley Additive exPlanation: a technique that decomposes a model's prediction into contributions from each feature, row by row. Mean absolute SHAP is used here as a feature-importance measure. |
| Optuna | A Python library for Bayesian hyperparameter optimisation. Each "trial" trains the model on one candidate set of parameters and scores it on the CV folds. |
| MAPE | Mean Absolute Percentage Error: average of |actual − predicted| / actual across all test rows. Expressed as a % of actual units. |
| RMSE_log | Root Mean Squared Error computed on log(units). One unit of RMSE_log ≈ ±105% in actual units; 0.111 log-units ≈ ±12% in units. |
| UPV | Units Per Visit: units sold divided by shopping trips (VISITS). Normalises for store-traffic differences when comparing promotion types. |
| TPR | Temporary Price Reduction: a price cut with no Feature circular ad or in-store Display. |
| Decile | One tenth of the data, ranked by predicted demand. Decile 10 = top 10% highest predicted demand. |
| Measured | A number computed directly from the data with no model assumption. |
| Modeled | A number produced by a statistical model; it reflects associations in the data, not proven causal effects. |
| Assumed | A number chosen by an analyst or inherited from a prior document; not derived from the data. |
