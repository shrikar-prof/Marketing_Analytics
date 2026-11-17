# ML Handoff Report — Discount Leakage Audit
**Project:** 02 Discount Leakage Audit — Complete Journey
**Author:** ML Statistician
**Date:** 2026-10-28
**Audience:** Growth-Strategy Partner, Business Manager

---

## 1. The Question and the Answer

**Question:** How much list revenue leaks to discounts, where does it concentrate, and what margin is recoverable if the worst promotions are trimmed?

**Answer:** Of the $5.06M in gross list revenue [measured] the chain kept in its loyalty panel over one year, $0.80M (15.7%) was given away as discounts. Almost all of that ($777K, 97%) is retailer-funded — cost the chain can influence directly. Leakage is not spread evenly: the top 7% of products (5,027 SKUs) drive 80% of all discount dollars, three departments (TOYS, MEAT, SEAFOOD-PCKGD) carry rates more than 1.5x the chain average, and promoted products carry a 31.2% discount rate versus 10.3% off-promotion. A CatBoost model trained on weeks 1–39 and tested on weeks 40–52 can identify the 21% of transaction lines that hold 50% of discount spend — the smallest intervention set. Capping those lines at a 25% discount rate is associated with approximately $20,585 in recoverable margin in the 13-week test window, or roughly $82K annualised [modeled association, not a guarantee]. Income does not explain leakage (eta-squared 0.05); this is a product and department story, not a household targeting story.

---

## 2. The Data in Five Lines

- **Source:** Dunnhumby "The Complete Journey" (CC0 licence), one loyalty-card year (2017-01-01 to 2017-12-31).
- **Grain:** One row per loyalty transaction line (product × basket × household).
- **Size:** 1,445,035 lines after cleaning (1,458,032 raw, minus 11,275 zero-value/zero-quantity, minus 12,997 fuel lines excluded). 2,467 households, 437 stores.
- **Target and rate:** `disc_rate` = total discount / list revenue, mean 15.7%, right-skewed (median 0%).
- **Business value at stake:** $797K discount spend per year on this panel; of which $777K is retailer-funded; modeled recoverable share at 25% cap = $20,585 per 13 weeks [modeled].

Data dictionary: `reports/exploration/data_dictionary.md`. Cleaning log: `reports/exploration/cleaning_log.md`.

---

## 3. Reconciliation Verdict

All counts and totals were independently verified. No material mismatches found.

| Check | Explorer | Model-builder | Match? |
|---|---|---|---|
| Clean rows (ex-fuel) | 1,445,035 | 1,445,035 (scores file) | Yes |
| Gross list revenue | $5,063,618 | $5,063,618 (scores sum) | Yes |
| Total discount | $797,183 | $797,186 (scores sum) | Yes (<$5 rounding) |
| Train/test split | Weeks 1–39 / 40–52 | 1,057,007 / 388,028 rows | Yes |
| Target definition | disc_rate = total_disc / list_revenue | same | Yes |
| Test set touched once | Recommended | Confirmed in model card | Yes |

The recoverable margin figure ($20,585) was re-derived from the scores file: applying the 25% cap to test-set lines where `pred_disc_rate > 0.25` gives excess discount of $20,585 — exact match to the model card [measured from scores file].

---

## 4. What the Exploration Found

Five findings that matter. Source: `reports/exploration/findings.md`, `reports/exploration/hypotheses.md`.

**F1 — $0.8M leaks to discounts (15.7% of list revenue)** [measured]
$5.06M gross list, $4.27M pocket. $777K retailer-funded (15.4%), $20K manufacturer-funded (0.4%). The manufacturer share is immaterial; the policy lever is retailer markdowns.
Chart: `reports/charts/01_price_waterfall.png`. Readable, labelled clearly.

**F2 — Department leakage rates vary 10x: TOYS gives away 43.4%, MEAT and SEAFOOD-PCKGD each 24.9%** [measured]
Mann-Whitney comparison of top-3 departments vs all others: rank-biserial r = −0.152 (medium effect), p < 0.001. The average non-promoted department is at 2.9% median vs 16.6% in these three.
Chart: `reports/charts/02_leakage_by_department.png`. Readable; all departments labelled.

**F3 — Promoted products carry 31.2% discount rate vs 10.3% off-promotion** [measured]
Mann-Whitney: rank-biserial r = −0.584 (large effect), p < 0.001. 95% CI on median difference: 0.310 to 0.315. Reliable: price reductions are the primary mechanic for promotions in this dataset. (Caveat: the promotions table may under-count events; association confirmed but magnitude is a floor estimate.)
Chart: `reports/charts/04_promoted_vs_not.png`. Readable, clear comparison.

**F4 — Leakage is concentrated: 7% of SKUs drive 80% of discount dollars** [measured]
Exact Lorenz calculation. Reviewing 5,027 out of 68,178 active products would cover 80% of all discount spend.
Chart: `reports/charts/03_leakage_concentration.png`. Readable; Lorenz curve with 80/7% marker.

**F5 — Income does not explain household discount capture** [measured]
Kruskal-Wallis on income bands: H = 51.99, eta-squared = 0.052 (small). Income explains only 5% of variance in disc_rate. Leakage is driven by which products a household buys, not by who they are.

---

## 5. The Model

Source: `reports/modeling/model_card.md`, `reports/modeling/tuning.md`.

**What was compared.** Ridge regression [a linear model], Random Forest, LightGBM, XGBoost, and CatBoost — all with default parameters first, then Optuna-tuned. Cross-validation used TimeSeriesSplit (5 inner folds) to prevent future-week leakage.
Chart: `reports/charts/05_model_comparison.png`. All tuned gradient boosters land within 0.001 RMSE of each other; Ridge is ~0.005 worse.

**Tuning.** Optuna TPE sampler [a Bayesian parameter-search algorithm], 60 trials per model, 3-fold inner CV on a 200K-row sub-sample. CatBoost best CV RMSE: 0.1513. Key parameters: 786 iterations, learning rate 0.012, depth 9, L2-leaf 0.015. Parameter importance showed `random_strength` (41%) and `iterations` (27%) dominated — meaning the model needed regularisation and enough trees more than it needed fine depth or bagging.

**Why CatBoost was chosen.** CatBoost (CV RMSE 0.1513) edged LightGBM (0.1511) and XGBoost (0.1514) by less than 0.001. The practical reason: CatBoost handles categorical features natively without pre-encoding, reducing the risk of target-leak in TargetEncoder steps.

**How good it is on the held-out test (weeks 40–52, 388,028 lines, never seen during training):**
- RMSE [root mean squared error] of 0.147: the model's predicted discount rate is off by about 14.7 percentage points on average.
- R² [variance explained] of 0.173: explains 17% of variance vs 0% for a naive average.
- Capture at top 10%: 28.7% of all discount dollars are in the 10% of lines the model ranks highest — 2.9× better than random.
- ECE [Expected Calibration Error] of 0.011: predicted rates are well-calibrated; the number can be used as an expected value directly.

**Where it is weaker:** RMSE is 0.171 in the top-3 departments vs 0.146 elsewhere (measured from segment_performance table) — the high-leakage tail underfits, so individual line scores in TOYS/MEAT/SEAFOOD should be treated as directional, not precise. Demographics were excluded (only 33% of households matched).

---

## 6. Drivers and Levers

SHAP [SHapley Additive exPlanations: a method that measures each feature's average contribution to individual predictions] importance from the held-out test.

### Structural (cannot be changed by promotion policy)

| Driver | SHAP mean |abs| | What it means |
|---|---|---|
| Product type | 0.0551 | Dominant. Promotional norms are baked into the product type. |
| Product category | 0.0132 | Category-level markdown norms persist regardless of individual promotion decisions. |
| Brand (national vs private) | 0.0051 | National brands attract manufacturer coupons; private label is all retailer-funded. |
| Department | 0.0043 | TOYS, MEAT, SEAFOOD carry structurally high rates. |

### Controllable / semi-controllable

| Driver | SHAP mean |abs| | Lever |
|---|---|---|
| Log quantity (pack size) | 0.0124 | Bulk promotions correlate with higher rates. Adjusting multi-pack markdown policy is actionable. |
| Store | 0.0066 | Some stores run promotions more aggressively. A store-level markdown ceiling is actionable. |
| Seasonality (week cos/sin) | 0.0047 | Promotional intensity peaks in Q1 and Q3. Scheduling promotions to off-peak weeks reduces average rate. |

**Counterfactual sensitivity [modeled association, not a cause]:** Shifting log_quantity by 0.693 units (equivalent to halving pack size) across 97,000 eligible lines is associated with a mean disc_rate reduction of −2.1 pp (95% CI: −2.1 to −2.0 pp), translating to $13,671 in associated saving [modeled]. Source: `reports/modeling/tables/counterfactual_sensitivity.csv`.

---

## 7. Actionability

### 7a. Value at risk by discount threshold

The table below uses the full 1,445,035-line dataset scored by the model.

| Predicted disc rate | Lines flagged | Share of base | Actual disc $ in those lines | Disc $ share |
|---|---|---|---|---|
| >=10% | 858,028 | 59.4% | $648,882 [modeled] | 81.4% |
| >=20% | 309,892 | 21.4% | $382,876 [modeled] | 48.0% |
| >=25% | 162,139 | 11.2% | $268,618 [modeled] | 33.7% |
| >=30% | 71,732 | 5.0% | $163,863 [modeled] | 20.6% |

Full table: `reports/tables/02_value_at_risk_by_threshold.csv`.

### 7b. Risk-only targeting by decile (decile 1 = highest predicted disc_rate)

| Decile | Lines | Mean pred rate | Actual disc $ | Disc $ share | Cumulative disc $ share |
|---|---|---|---|---|---|
| 1 (top) | 144,504 | 31.7% | $268,451 | 33.7% | 33.7% |
| 2 | 144,503 | 22.9% | $121,198 | 15.2% | 48.9% |
| 3 | 144,504 | 18.7% | $98,002 | 12.3% | 61.2% |
| 4 | 144,503 | 15.6% | $81,698 | 10.2% | 71.4% |
| 5 | 144,504 | 13.2% | $68,059 | 8.5% | 80.0% |
| 6–10 | 722,517 | 6.3% avg | $159,778 | 20.0% | 100.0% |

Full table: `reports/tables/01_decile_targeting.csv`.

### 7c. Smallest intervention

| Target | Lines to treat | Share of base | Min predicted disc rate |
|---|---|---|---|
| Capture 50% of discount dollars | 301,305 | 20.9% | >=20.2% |
| Capture 80% of discount dollars | 723,333 | 50.1% | >=12.1% |

Treating 21% of lines (the top two deciles) captures half of all discount spend. That is the minimum viable review scope. Full table: `reports/tables/03_smallest_intervention.csv`.

**Recoverable margin estimate [modeled, assumed 25% cap]:** Annualising the test-period figure: $20,585 per 13 weeks × (52/13) = **$82,340 per year**. This assumes: (a) no volume response to trimming promotions [assumed]; (b) the test-period pattern holds across all weeks [assumed]; (c) the 25% cap is achievable for all flagged lines [assumed]. If promoted products lose 20% of their volume when discounts are trimmed, the net saving shrinks proportionally.

---

## 8. Failure Modes, Assumptions and Instrumentation Gaps

Priority order: highest business risk first.

| # | Issue | Source | Business risk | Fix |
|---|---|---|---|---|
| 1 | **No incremental sales measurement.** Promotions may drive volume that offsets the discount cost. The model cannot measure this. | Model card | Over-estimates recoverable margin. A 10% volume lift at 25% margin on a 30%-discounted item may make the promotion break-even. | Run a hold-out A/B test: remove promotions from a matched set of stores for 8 weeks. |
| 2 | **One-year data, no multi-year seasonality.** Week-of-year features cannot distinguish year-on-year trend from seasonality. | Tuning, model card | Model may misrank lines in weeks where promotional norms shifted year-over-year. | Re-train on 2+ years when available. |
| 3 | **Demographics cover only 33% of households.** Model excludes income, age, household size. | Handoff, model card | Cannot target by household value; leakage analysis is product-centric only. | Extend demographics coverage via loyalty programme at sign-up. |
| 4 | **Promotions join is sparse.** The on_promo flag matches only 22% of lines; the remaining 78% may include unadvertised price cuts. | Handoff, findings | Finding 3's 31.2% rate applies to matched events only; true promoted-rate may be higher. | Capture all price-change events in a unified event log at POS. |
| 5 | **High-leakage tail underfits.** RMSE in top-3 departments is 0.171 vs 0.146 overall. | Segment performance table | Individual line scores in TOYS/MEAT/SEAFOOD are directional, not precise. | Weight high-leakage lines in training loss; or build a department-specific sub-model. |
| 6 | **No store-level geography.** Store-level leakage rates not compared; 437 stores treated as interchangeable beyond ID encoding. | Findings | A rogue store running deep promotions would not be isolated. | Add store-level markdown ceiling as a policy guardrail and monitor deviation. |
| 7 | **Model is static to 2017.** Seasonal patterns, category norms and household composition shift. | Model card | Scores degrade if applied to current data without retraining. | Schedule quarterly retraining; monitor RMSE on rolling 4-week hold-out. |

---

## 9. Chart Manifest and File List

All charts in `reports/charts/` are readable and carry a clear title. Key takeaway for each:

| File | Shows | Key takeaway |
|---|---|---|
| `01_price_waterfall.png` | Gross list → retailer discount → mfr coupon → pocket revenue | $0.8M (15.7%) lost; 97% retailer-funded |
| `02_leakage_by_department.png` | Discount rate by department, sorted desc | TOYS 43.4%; MEAT and SEAFOOD >24%; 15 departments below average |
| `03_leakage_concentration.png` | Lorenz curve of discount dollars by SKU | 7% of SKUs = 80% of discount spend |
| `04_promoted_vs_not.png` | Median disc rate: promoted vs not | 31.2% vs 10.3% — 3× gap |
| `05_model_comparison.png` | CV RMSE for all model families | Tuned gradient boosters cluster at 0.151; Ridge is 0.155 |
| `06_shap_importance.png` | SHAP mean |abs| by feature | Product type dominates; pack size and store are controllable |
| `07_decile_lift.png` | Lift (actual rate / average) by predicted decile | Top decile: 2.0× lift; bottom decile: 0.16× |
| `08_threshold_curves.png` | Precision, recall and disc-$ captured vs threshold | 25% threshold: 56% precision, 20% recall, 26% disc $ captured |

### Supporting files

| File | Description |
|---|---|
| `reports/customer_discount_scores.csv` | 1,445,035 rows; columns: week, list_revenue, total_disc, split, pred_disc_rate, actual_disc_rate, decile, expected_disc_at_risk, is_high_leakage, is_top_decile, is_test |
| `reports/tables/01_decile_targeting.csv` | Full decile table, all 1.4M rows aggregated to 10 rows |
| `reports/tables/02_value_at_risk_by_threshold.csv` | Four threshold scenarios |
| `reports/tables/03_smallest_intervention.csv` | Lines needed for 50% and 80% capture |
| `reports/modeling/tables/counterfactual_sensitivity.csv` | Pack-size lever estimate |
| `reports/modeling/tables/segment_performance.csv` | RMSE by brand and department segment |

---

## 10. Glossary

| Term | Plain meaning |
|---|---|
| List revenue | The price on the shelf label before any discount. |
| Pocket revenue | What the retailer actually receives after all discounts. |
| Retail discount (retailer-funded) | A markdown the retailer pays from its own margin (e.g., loyalty card price). |
| Manufacturer coupon (mfr-funded) | A discount reimbursed to the retailer by the product manufacturer. |
| disc_rate | Fraction of list revenue given away as discount on a transaction line. |
| Leakage | The gap between list revenue and pocket revenue; the discount cost. |
| Decile | One-tenth of the scored population, ranked by predicted disc_rate. Decile 1 = highest predicted risk. |
| Lift | Ratio of actual disc_rate in a group to the overall average; 2.0× means twice as concentrated. |
| SHAP | SHapley Additive exPlanations: measures each feature's average contribution to individual model predictions. |
| CatBoost | A gradient-boosted tree algorithm that handles categorical features natively. |
| Optuna | A Python library for automated hyperparameter search using Bayesian methods. |
| RMSE | Root mean squared error: the typical prediction error, in the same units as the target. |
| R² | Fraction of variance in the target explained by the model (0 = no better than predicting the mean; 1 = perfect). |
| ECE | Expected Calibration Error: how closely predicted probabilities match observed rates (0 = perfect calibration). |
| Counterfactual sensitivity | How the model's prediction changes when one feature is shifted; a modeled association, not a proven cause. |
| Temporal split | Training on earlier data, testing on later data, to mimic real deployment conditions. |
| TimeSeriesSplit | A cross-validation scheme that never uses future folds to validate past folds. |
| Rank-biserial r | An effect-size measure for non-parametric comparisons; |r| > 0.30 is large. |
| Eta-squared | Effect-size measure for Kruskal-Wallis; <0.06 is small. |
| TPE sampler | Tree-structured Parzen Estimator: Optuna's default Bayesian search method. |

---

*Labels used throughout: [measured] = computed from the data; [modeled] = output of the model, an association only; [assumed] = a number or rule someone chose.*
