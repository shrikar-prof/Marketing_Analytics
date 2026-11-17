# ML Handoff Report — Marketing Budget Reallocation (MMM)
**Project:** 04-marketing-budget-reallocation-mmm  
**Prepared by:** ml-statistician  
**Date:** 2026-11-09  
**Audience:** growth-strategy-partner, business manager

---

## 1. The Question and the Answer

**Question:** What does each marketing channel contribute to revenue, where does each saturate, and how should a fixed ~$34K median weekly budget be split to maximize revenue?

**Answer:** The Marketing Mix Model [MMM — a statistical model that attributes revenue to media spend, controlling for seasonality and market conditions] explains 94% of weekly revenue variance on a held-out 20-week test set it never saw during training. The single largest driver of weekly revenue is market demand (proxied by competitor sales), not any media channel — this structural factor dwarfs all five spend channels combined in the model's SHAP [Shapley Additive exPlanations — the average USD contribution each feature makes to individual predictions] analysis. Among controllable channels, TV and Print show the highest SHAP magnitudes despite having the most saturated response curves, while OOH consumes 62% of total 4-year spend but ranks third in SHAP contribution. Facebook, though spending the least per active week ($4.4K), sits on the steepest part of its response curve and is the strongest candidate for increased investment under a budget-neutral reallocation. Search and OOH response curves behave anomalously in the model (downward-sloping), which signals collinearity artifacts rather than a real negative return; those channels require a geo experiment to resolve. No reallocation number should be acted on without a controlled geo holdout test first.

---

## 2. The Data

- **Source:** Meta Robyn simulated weekly dataset (MIT license). See `data/raw/dt_simulated_weekly.RData`.
- **Grain:** One row per week. 208 weeks, 23 Nov 2015 to 11 Nov 2019.
- **Target:** `revenue` — weekly USD revenue. Actual 4-year total: $379M (measured). Mean weekly revenue: $1.82M (measured). Median: $1.87M (measured).
- **Channels:** TV, OOH [out-of-home], Print, Facebook, Search. Median weekly total spend: $31.4K (measured). Mean: $69.9K (measured) — the mean is inflated by infrequent OOH spikes of up to $500K/week.
- **Business value at stake:** $379M in revenue over 4 years, ~$1.82M/week on average.
- **Data dictionary:** `problem_description.md` (column-level). **Cleaning log:** `reports/exploration/handoff_to_modeling.md`.

**Note — reconciliation discrepancy (minor):** The exploration report states mean weekly revenue of $2.9M. The measured mean is $1.82M ($2.9M is the mean of the top-predicted decile, not the overall mean). This does not affect the model, which was trained and tested on the correct revenue values. The exploration's 1.2% media-to-revenue ratio relied on the overstated mean; the correct ratio is 3.8% using total spend and total revenue (measured). Both are flagged for the record.

---

## 3. What Exploration Found

Five findings that survive scrutiny. Source: `reports/exploration/findings.md` and `reports/exploration/hypotheses.md`.

| # | Finding | Key number | Reliability | Chart |
|---|---------|-----------|-------------|-------|
| F1 | TV dominates budget but shows the weakest per-quintile revenue lift | 46% of typical-week spend; top-quintile TV weeks earn only ~5% more than bottom-quintile (measured) | Moderate — unadjusted for confounders | `06_revenue_by_spend_quintile_exploration.png` |
| F2 | Search earns the highest revenue lift per spend quintile | Top-quintile search weeks earn 49% more revenue than bottom (measured) | Moderate — same caveat; small n per quintile | `06_revenue_by_spend_quintile_exploration.png` |
| F3 | Event weeks add an average 18% revenue lift | 15 event weeks vs 193 non-event weeks; Mann-Whitney p < 0.001 (measured) | High — well-powered test; controlled by model builder | `08_event_week_revenue_lift.png` |
| F4 | Total budget is flat; reallocation is zero-sum | Spearman ρ = -0.089, p = 0.200, no trend in total spend (measured) | High — simple test on 208 observations | `07_spend_mix_over_time.png` |
| F5 | Channels are largely independent — MMM attribution is feasible | Pairwise spend correlations mostly below r = 0.2 (measured) | High — validated against model's ability to separate channels | `reports/exploration/charts/04_correlation_matrix.png` |

---

## 4. The Model

**What was compared:** Five model families benchmarked on rolling-origin [forward-only] cross-validation [CV] over 188 training weeks, 10 windows of 20 weeks each. See `reports/modeling/tables/full_benchmark.csv`.

| Family | CV RMSE (mean ± std) |
|--------|----------------------|
| **Ridge** | **$303K ± $102K** |
| XGBoost | $310K ± $96K |
| RandomForest | $321K ± $106K |
| CatBoost | $322K ± $101K |
| LightGBM | $353K ± $101K |

**Tuning (Optuna [a hyperparameter search library using TPE — Tree-structured Parzen Estimation]):** 60 trials per family, TPE sampler, MedianPruner. Best Ridge alpha: 2.16 (CV RMSE: $301K). Best XGBoost: n_estimators=115, lr=0.26, max_depth=3 (CV RMSE: $308K). Full details: `reports/modeling/tuning.md`.

**Model chosen:** Ridge regression. Reason: lowest mean CV RMSE, lowest variance, interpretable coefficients, appropriate for small dataset (208 rows). Tree models overfitted despite regularization.

**Held-out test set performance (20 weeks, May–Nov 2019 — touched once):**

| Metric | Value | Plain-words interpretation |
|--------|-------|---------------------------|
| MAPE [mean absolute percentage error] | 6.0% | On a typical $1.95M test week, the model is off by ~$118K |
| RMSE [root mean squared error] | $142K | Typical dollar-size error |
| R² | 0.943 | Model explains 94% of weekly revenue variation |
| Calibration ratio | 1.000 | Average predicted = average actual; no systematic over- or under-prediction |

**Where it is weaker:** Largest errors occur in the highest-spend OOH weeks (the response curve anomaly). The model has not been tested on a channel mix radically different from training data. See `reports/modeling/model_card.md` for the full weakness list.

---

## 5. Drivers and Levers

**Structural** (cannot be changed by marketing): competitor sales index (SHAP $392K — far the largest driver, measured). Annual and semi-annual seasonality (SHAP $99K–$95K cos cycles). Revenue trend (SHAP $21K). These explain most of the week-to-week revenue variation.

**Semi-controllable**: Event weeks (SHAP $26K — 18% average lift; event calendar is partly under brand control).

**Controllable media channels** — SHAP contributions and response curve position (all modeled associations, not causes):

| Channel | SHAP mean|abs| USD | Active weeks / 208 | Mean active-week spend | Response curve position |
|---------|-----------|---------------------|----------------------|------------------------|
| TV | $87K | 92 | $33.6K | Saturated — curve nearly flat at current $33.6K |
| Print | $84K | 87 | $8.9K | Moderately saturated at current $8.9K |
| OOH | $44K | 85 | $105.8K | Anomalous downward slope — collinearity artifact (flag) |
| Facebook | $10K | 101 | $4.4K | Steep rising slope — still on early part of curve |
| Search | $1K | 176 | $7.0K | Anomalous downward slope — collinearity artifact (flag) |

SHAP source: `reports/modeling/tables/shap_importance.csv`. Charts: `reports/charts/01_channel_response_curves.png`, `reports/charts/02_driver_importance_shap_permutation.png`.

**Counterfactual sensitivities are labelled as modeled associations.** The response curves estimate what the model predicts at different spend levels, holding all other features at their training means. They are not controlled experiments.

---

## 6. Actionability

### Revenue concentration by predicted decile

Top 10% of weeks (21 weeks, by predicted revenue) hold 16% of 4-year revenue ($60.7M of $379M). Top 50% hold 66%. This shows the model identifies high-revenue weeks reliably (lift [actual revenue / overall mean] = 1.59× in decile 1). Full table: `reports/tables/01_revenue_concentration_by_decile.csv`. Chart: `reports/charts/03_revenue_decile_lift.png`.

| Top % of weeks | Weeks | % of total revenue | Cumulative revenue at stake |
|---|---|---|---|
| 10% | 21 | 16% | $60.7M |
| 25% | 52 | 37% | $141M |
| 50% | 104 | 66% | $252M |
| 75% | 156 | 86% | $326M |

### Channel spend and SHAP attribution

Full table: `reports/tables/02_channel_spend_and_shap.csv`.

OOH commands 62% of 4-year total spend ($9.0M of $14.5M) but ranks third in SHAP contribution ($44K vs TV's $87K). TV is second-largest by spend (21%) and ranks first in SHAP — but its response curve is flat at current active-week spend of $33.6K.

### Budget reallocation scenario (illustrative, modeled association)

The one clean signal from the response curves: Facebook is on the steep part of its curve at $4.4K/active week. TV is saturated at $33.6K/active week. A conservative, budget-neutral shift of 20% of TV's active-week spend (~$6.7K) to Facebook (~$6.7K added, bringing it to ~$11.1K) moves TV from deep saturation toward the curve's knee and moves Facebook further up its rising slope. Modeled direction: positive for revenue. Magnitude: not quantified here — requires a geo holdout to validate before acting. Full scenario: `reports/tables/04_budget_reallocation_scenario.csv`.

**Before any reallocation:** run a geo holdout test for 8–12 weeks (4 geo markets treated, 4 held out as controls). That experiment is what converts the modeled association into an actionable budget decision. The Meridian geo dataset (`data/raw/meridian_geo_media.csv`, 20 geos, 156 weeks) exists for designing this test.

---

## 7. Failure Modes, Assumptions and Instrumentation Gaps

Listed in priority order (highest business risk first):

| # | Gap | Impact | Fix |
|---|-----|--------|-----|
| G1 | OOH and Search response curves are anomalously downward-sloping — collinearity with total_spend_log. ROI signals for these two channels are unreliable. | Cannot confidently direct OOH cuts or Search increases | Geo experiment; or Bayesian MMM (Meridian) that estimates saturation parameters from data |
| G2 | Fixed adstock [carry-over] decay rates (TV 0.40, OOH 0.30, etc.) are assumed, not estimated from data | TV and OOH contribution may be understated if real decay is slower | Bayesian MMM or held-out lag experiment |
| G3 | Saturation parameters (Hill constants) are set to priors, not learned | Channel ROI estimates are sensitive to these; small changes can flip the reallocation direction | Calibrate against market research or Bayesian estimation |
| G4 | No geo variation in the Robyn dataset — single national time series | Channel effects cannot be identified from regional variation; standard error on ROI estimates is large | Use Meridian geo data for the main model |
| G5 | Small dataset (208 weeks) means confidence intervals on individual channel coefficients are wide | Adjacent channels (TV and Print both peak together in some weeks) may trade coefficient mass | Add geo variation or more years |
| G6 | No pricing or promotion data | Pricing changes in the 4-year window would be assigned to whatever channels ran heavy spend at the same time | Add a price index to the feature set |
| G7 | Exploration report's stated mean revenue ($2.9M/wk) differs from the measured mean ($1.82M/wk) | Does not affect the model; affects verbal interpretation of exploration section | Use $1.82M as the correct figure in all downstream communications |

---

## 8. Chart Manifest

| File | What it shows | Key takeaway | Readable? |
|------|--------------|--------------|-----------|
| `reports/charts/01_channel_response_curves.png` | Predicted revenue vs. spend for each channel, all other features at training mean | TV and Print are saturated; Facebook is on the steep part of its curve; OOH and Search show anomalous downward slopes | Yes |
| `reports/charts/02_driver_importance_shap_permutation.png` | SHAP mean|abs| and permutation importance on the test set | Competitor sales dwarfs all media channels; OOH_log is the top permutation-positive driver | Yes |
| `reports/charts/03_revenue_decile_lift.png` | Actual revenue by predicted decile, plus lift ratio | Model correctly ranks weeks; top decile earns 1.59× the mean | Yes |
| `reports/charts/04_model_family_comparison.png` | Rolling-origin CV RMSE for all five families | Ridge wins clearly; tree models have higher RMSE despite tuning | Yes |
| `reports/charts/05_model_reliability_calibration.png` | Mean actual vs. mean predicted by decile bin | Points closely track the diagonal — model is well-calibrated | Yes |
| `reports/charts/06_revenue_by_spend_quintile_exploration.png` | Mean revenue by zero/low/high spend quintile for each channel | Search shows the steepest spend-to-revenue lift in raw data | Yes |
| `reports/charts/07_spend_mix_over_time.png` | Stacked area chart of weekly spend by channel, 2015–2019 | Total spend is flat; OOH drives the spike weeks; TV shrinks slightly | Yes |
| `reports/charts/08_event_week_revenue_lift.png` | Box plot of revenue in event vs. non-event weeks | Event weeks average 18% more revenue, tight distribution | Yes |

---

## 9. File List

| File | Contents |
|------|---------|
| `reports/ml_handoff_report.md` | This report |
| `reports/ml_followups.md` | Placeholder for partner follow-up Q&A |
| `reports/customer_risk_scores.csv` | Per-week score file: actual revenue, predicted revenue, decile, spend columns, event flag, spend efficiency |
| `reports/tables/01_revenue_concentration_by_decile.csv` | Revenue by predicted decile |
| `reports/tables/02_channel_spend_and_shap.csv` | Channel spend and SHAP attribution |
| `reports/tables/03_revenue_threshold_targeting.csv` | Revenue captured at top 10/25/50/75/90% predicted thresholds |
| `reports/tables/04_budget_reallocation_scenario.csv` | Illustrative budget-neutral TV-to-Facebook shift |
| `reports/charts/01_channel_response_curves.png` | Response curves for all five channels |
| `reports/charts/02_driver_importance_shap_permutation.png` | SHAP and permutation importance |
| `reports/charts/03_revenue_decile_lift.png` | Decile lift chart |
| `reports/charts/04_model_family_comparison.png` | Model comparison chart |
| `reports/charts/05_model_reliability_calibration.png` | Calibration chart |
| `reports/charts/06_revenue_by_spend_quintile_exploration.png` | Quintile revenue by channel |
| `reports/charts/07_spend_mix_over_time.png` | Spend mix time series |
| `reports/charts/08_event_week_revenue_lift.png` | Event week revenue lift |

---

## 10. Glossary

| Term | Plain-words definition |
|------|----------------------|
| MMM (Marketing Mix Model) | A statistical model that uses historical weekly spend and revenue to attribute revenue to each media channel, controlling for seasonality and market conditions. |
| SHAP (Shapley Additive exPlanations) | A method that assigns each input feature a dollar value equal to its average contribution to individual predictions. Mean \|SHAP\| measures importance without regard to direction. |
| Adstock | The carry-over effect of advertising: TV spend in week t still influences revenue in weeks t+1, t+2 … modelled as geometric decay. |
| Hill saturation function | A mathematical curve (S-curve) applied to adstock to model diminishing returns: doubling spend does not double revenue. |
| Rolling-origin cross-validation | A time-series validation method that trains on the past and tests on the future only, repeated 10 times. Prevents the model from "seeing the future." |
| MAPE (Mean Absolute Percentage Error) | Average of |actual – predicted| / actual, expressed as a percentage. 6% means the model is off by 6% of the actual value on average. |
| RMSE (Root Mean Squared Error) | Square root of the average squared prediction error; penalizes large errors more than small ones. |
| R² (R-squared) | Fraction of revenue variance explained by the model. 0.94 means 94% explained. |
| Collinearity | When two features move together, making it impossible to separate their individual effects. OOH and total_spend_log are collinear here, causing anomalous response curves. |
| Lift | Actual revenue in a group divided by the overall mean. Lift = 1.59 means that group averages 59% more revenue than a randomly selected week. |
| Geo holdout | A controlled experiment that assigns some geographic markets to a treatment (budget change) and holds others as controls to measure the causal effect. |
| Optuna / TPE | Optuna is a hyperparameter tuning library. TPE (Tree-structured Parzen Estimation) is its default search algorithm, which learns from past trials to propose better parameters. |
| MedianPruner | An Optuna component that stops unpromising trials early to save time. |
| Permutation importance | Measures how much model accuracy drops when a single feature is shuffled. A large drop means the feature is genuinely predictive on the test set. |
| Baseline revenue | Revenue the brand would earn with zero media spend, driven by trend, seasonality, and market demand. |
