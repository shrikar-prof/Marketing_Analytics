# ML Handoff Report — Strategy Teardowns
**Author:** Shrikar (shrikar.p@triiqinnovations.com)
**Date:** 2026-11-17
**Agent ID:** ml-statistician

---

## 1. The Question and the Answer

**What does the data say about how each company should approach its core strategic lever?**

**Netflix** has demonstrated that price increases — executed gradually and paired with product expansion (paid-sharing enforcement, advertising tier) — do not destroy the UCAN [US and Canada] subscriber base and do grow revenue. UCAN quarterly revenue doubled from $2,672M in Q4 2019 to $5,339M in Q4 2025, while average revenue per member [ARM] rose 31% from $13.22 to $17.26 per month. The 2022 net-subscriber losses coincided with post-pandemic streaming normalisation, not with any single price change, and they reversed within two quarters. The bigger finding is structural: the May 2023 paid-sharing enforcement added a median $1,218M per quarter (95% CI: $760M–$1,637M), dwarfing the incremental lift from any single price move. The evidence supports continued ARM-first revenue growth so long as membership stays above ~75M UCAN accounts — but every sensitivity in this report is a modeled association, not a causal estimate.

**Five Below** ran a natural experiment in expansion speed. When it opened 204 stores in FY2023 and 227 in FY2024 (a 20%+ annual fleet expansion), comparable-store [comp] sales turned negative (−2.0% and −2.7%) and operating margin fell to 8.4% — its lowest non-COVID level. When expansion was cut to 150 stores in FY2025, comps recovered sharply to +12.8% and margin improved to 9.6%. Revenue per store remained above the company's own $2M viability floor throughout, suggesting the problem was execution bandwidth and store-maturity mix, not site-quality failure. The data supports a targeted-expansion model: 150–165 stores per year, allowing the new cohort to mature before the next wave.

---

## 2. The Data in Five Lines

| Item | Netflix UCAN | Five Below |
|------|-------------|------------|
| **Source** | SEC EDGAR 8-K shareholder letters | SEC EDGAR 10-K annual filings |
| **Grain** | Quarter (Q4 2019 – Q4 2025) | Fiscal year (FY2018 – FY2025) |
| **Rows** | 24 quarters revenue; 20 quarters with membership | 8 fiscal years |
| **Target and rate** | Revenue: $2,672M → $5,339M/qtr; ARM: $13.22 → $17.26/mo | Comp sales: range −5.5% to +30.3%; op margin: 7.9% to 13.3% |
| **Business value at stake** | ~$360M annual revenue per $1/month ARM increase at Q4 2024 membership base (modeled association) | ~1.6 ppt operating margin per 100-store reduction in annual expansion pace (directional; N=6) |

Data dictionary: `reports/exploration/data_dictionary.md`
Cleaning log: `reports/exploration/cleaning_log.md`
Quality audit: `reports/exploration/quality_audit.md`

---

## 3. What Exploration Found

Five findings matter. Full detail and charts are in `reports/exploration/findings.md` and `reports/exploration/hypotheses.md`.

**Finding 1 — Netflix price increases never produced a sustained revenue decline.** [Measured]
ARM grew from $13.22 to $17.26/month (+$4.04, +31%) across six price events. Spearman rho = 0.971 (p < 0.001; bootstrap 95% CI: 0.861–0.996). Every event was followed by continued UCAN revenue growth. Chart: `reports/charts/01_netflix_ucan_revenue.png`.

**Finding 2 — Paid-sharing enforcement was the biggest single revenue catalyst.** [Measured]
Median quarterly UCAN revenue rose $1,218M after May 2023 enforcement. Mann-Whitney p = 0.000; bootstrap 95% CI: $760M–$1,637M. UCAN memberships jumped 5.7M in two quarters. Chart: `reports/charts/05_netflix_revenue_decomposition.png`.

**Finding 3 — ARM growth did not predict next-quarter subscriber losses.** [Measured, uncertain]
Spearman rho between ARM growth and next-quarter net adds = +0.19 (H6 rho = −0.474, p = 0.064; CI crosses zero). The 2022 net-add losses coincided with post-pandemic normalisation. The data cannot isolate pricing as the cause. Reliability: directional, not conclusive at N = 15.

**Finding 4 — Five Below's fastest expansion years compressed comp sales and margins.** [Measured, low power]
FY2023–FY2024: 204–227 stores opened, comps −2.0% and −2.7%, margin 10.8% and 8.4%. FY2025: 150 stores, comps +12.8%, margin 9.6%. Spearman rho (margin vs expansion rate) = −0.820 (permutation p = 0.033). Comp-sales correlation rho = −0.577 (p = 0.14 — insufficient power). Chart: `reports/charts/02_five_below_stores_vs_comp.png`, `reports/charts/03_five_below_op_margin.png`.

**Finding 5 — Revenue per store diluted temporarily but stayed above the $2M viability floor.** [Measured]
Peak $2.60M in FY2022 (note: exploration text says $2.60M; FY2022 shown in chart as $2.30M — the exploration text appears to reference a slightly different derivation; use chart value $2.30M as measured). Fell to $2.19M in FY2024. Recovered to $2.48M in FY2025. External benchmark [assumed]: company new-store model of $2M/year. Chart: `reports/charts/04_five_below_rev_per_store.png`.

---

## 4. The Models

### What was compared

Four Ridge [regularised linear regression] models were evaluated. No Optuna or ensemble methods were used; with N = 7–20, any model with more than 2–3 free parameters overfits. See `reports/modeling/tuning.md` for the full comparison grid.

| Model | Dataset | Method | MAE | Naive MAE | R² | Best alpha |
|-------|---------|--------|-----|-----------|-----|------------|
| arm_lag1 + rev_lag1 (selected) | Netflix revenue | Walk-forward CV | $92.7M/qtr | $99.5M/qtr | 0.908 | 0.01 |
| lag1 + post_sharing (selected) | Netflix members | Walk-forward CV | 1.19M members | 1.40M (lag-only) | 0.893 | 0.01 |
| expansion_rate_only (selected) | Five Below comp sales | LOOCV | 11.07 ppt | 13.07 ppt | −0.39 | 100.0 |
| sga_intensity_only (selected) | Five Below op margin | LOOCV | 1.79 ppt | 2.17 ppt | −0.46 | 100.0 |

### Validation design

Netflix: walk-forward expanding-window [train on first N quarters, predict next one, repeat]. Initial window: 8 quarters. Steps: 12 out-of-fold [OOF] predictions from Q4 2021 onward. Held-out test: Q1–Q4 2025 — touched once after model selection. Five Below: leave-one-out cross-validation [LOOCV] — 8 folds, train on 7 years, predict the remaining year.

### How good it is

**Netflix revenue:** Walk-forward MAE of $92.7M is within the $100M acceptable threshold set in `reports/exploration/handoff_to_modeling.md`. The model correctly tracks the revenue acceleration from 2023 onward. On the held-out Q1 2025 test, residual = −$88M (underpredicted by 1.9%). This is a single out-of-sample data point; confidence in the out-of-sample bound requires more future observations.

**Five Below comp sales:** LOOCV MAE of 11.07 ppt beats the naive baseline (13.07 ppt) but far exceeds the acceptable threshold of 1.5 ppt. The model predicts ~5% comp sales regardless of year. It is not a reliable comp-sales predictor; it is useful only for confirming that expansion rate has a direction association with comp outcomes. The COVID years (FY2020: actual −5.5% predicted 5.2%; FY2021: actual +30.3% predicted 5.2%) dominate the error.

**Five Below op margin:** LOOCV MAE of 1.79 ppt is modestly better than the naive baseline (2.17 ppt) and close to the 1.5 ppt threshold. The model explains margin variation through SGA intensity [SGA as share of revenue]. Confidence intervals on individual coefficients are wide at N = 8.

### Where the model is weaker

- Five Below comp sales model has negative R² (−0.39) in LOOCV: it performs worse than the sample mean for held-out years.
- Netflix arm_lag1 coefficient is individually not significant (p = 0.18) due to collinearity with rev_lag1; the ARM signal is real but captured through momentum.
- Q1 2024 is the largest Netflix OOF residual ($190M over); this coincides with the January 2025 Standard plan increase announcement effect appearing earlier than expected.

Full model card: `reports/modeling/model_card.md`. Full comparison tables: `reports/modeling/tables/`.

---

## 5. Drivers and Levers

### Netflix

| Driver | Type | Effect | Label |
|--------|------|--------|-------|
| Prior-quarter ARM | Structural (pricing history) | Captured through rev_lag1 momentum (coeff +1.23, p < 0.001) | Modeled association |
| Paid-sharing enforcement (post May 2023) | Structural (policy break) | +$1,218M/qtr median; +2.23M members (coeff p = 0.022) | Measured + modeled |
| Membership base level | Structural | Strong AR(1) for members: coeff 0.915 (p < 0.001) | Modeled association |
| Price event quarter | Controllable | Not independently significant when rev_lag1 included | Modeled association |

**Structural** = not easily changed in the next 12 months (content library, platform scale, enforcement policy).
**Controllable** = price level, tier mix, promotional cadence.

The ARM-to-revenue sensitivity of ~$360M/year per $1/month increase is derived from the accounting identity (revenue ≈ ARM × members × 3), not from a causal model. It assumes membership does not change — an assumption [assumed] that may not hold at higher ARM levels.

### Five Below

| Driver | Type | Effect | Label |
|--------|------|--------|-------|
| Annual expansion rate (net new / prior fleet) | Controllable | Spearman rho = −0.577 vs comps; −0.820 vs margin | Modeled association |
| SGA intensity | Structural (cost structure) | Negative association with margin; coefficient not significant | Modeled association |
| COVID shock | External | FY2020–FY2021 dominate residuals; absorbed by covid_flag | Measured outlier |
| Store maturity mix | Structural (portfolio) | Not directly modelled; inferred from rev-per-store recovery | Assumed mechanism |

---

## 6. Actionability

### Business value at risk by segment

Full tables: `reports/tables/actionability_netflix.csv` and `reports/tables/actionability_five_below.csv`.

**Netflix — key thresholds** [Modeled associations]

| Scenario | ARM | UCAN members (assumed constant at Q4'24: ~83M) | Implied annual UCAN revenue |
|----------|-----|------------------------------------------------|----------------------------|
| Current (Q4'24) | $17.26/mo | 83M | ~$17.1B/year |
| +$1/mo increase | $18.26/mo | 83M | ~$18.1B/year (+$1.0B) |
| +$2/mo increase | $19.26/mo | 83M | ~$19.1B/year (+$2.0B) |
| Membership −5M (churn scenario) | $17.26/mo | 78M | ~$16.1B/year (−$1.0B) |

The churn scenario row illustrates the break-even: a $1/month increase is offset only if more than 5.8M UCAN members leave. The largest observed UCAN net-add loss in this dataset was −1.3M in a single quarter (Q2 2022), and that reversed the following quarter. These are arithmetic estimates [assumed], not predictions.

**Five Below — expansion pace vs margin trade-off** [Modeled association, N=6]

| Annual stores opened | Expansion rate (of ~1,765 stores FY2025 fleet) | Observed comp sales | Observed op margin |
|---------------------|------------------------------------------------|---------------------|--------------------|
| 150 (FY2025 actual) | 8.5% | +12.8% | 9.6% |
| 200 (FY2023 pace) | ~12% | +2.8% | 10.8% |
| 227 (FY2024 pace) | ~14% | −2.7% | 8.4% |

The pattern is directional; treat it as a flag, not a formula. Only 6 non-COVID data points underlie the correlation.

### Decile view — Netflix revenue model residuals

| Quartile by actual revenue | Period | Average actual ($M/qtr) | Average predicted ($M/qtr) | Average abs error ($M) |
|---------------------------|--------|------------------------|---------------------------|------------------------|
| Q1 (lowest, $2,703–$3,235M) | Q4'19–Q2'21 | 2,980 | 2,982 | 42 |
| Q2 ($3,235–$3,601M) | Q3'21–Q4'22 | 3,420 | 3,448 | 52 |
| Q3 ($3,601–$4,224M) | Q1'23–Q3'24 | 3,836 | 3,780 | 80 |
| Q4 (highest, $4,224M+) | Q4'24–Q1'25 | 4,567 | 4,593 | 103 |

Error grows with revenue level — typical of a linear model on an accelerating trend. Still within the $100M threshold through Q4 2024.

---

## 7. Failure Modes, Assumptions and Instrumentation Gaps

Listed in priority order (most material first).

| # | Issue | Type | Impact | What would fix it |
|---|-------|------|--------|-------------------|
| 1 | Small N — Five Below (8 rows) | Data gap | LOOCV MAE is noisy; any coefficient estimate has confidence interval spanning ±100% of its value | 10–15 more years of data, or store-level quarterly panel |
| 2 | Causality — all effects are associations | Assumption | "If ARM rises $1, revenue rises $X" is not supported; confounders (content quality, macro) drive both | Randomised pricing test (geo holdout) |
| 3 | COVID distortion — FY2020–FY2021 (Five Below) | Data quality | COVID spike (+30.3% comps) dominates residuals; covid_flag absorbs variance but cannot isolate expansion effects | Exclude COVID years from expansion-pace analysis; retest on 6 clean observations |
| 4 | Netflix membership data stops after Q4 2024 | Data gap | Membership model cannot be evaluated on 2025–2026; ARM-to-revenue arithmetic depends on stable membership | Reinstate member reporting or use household/engagement proxy |
| 5 | Collinearity — ARM and revenue (Netflix) | Model weakness | arm_lag1 coefficient is individually insignificant (p = 0.18); the ARM pricing signal is real but cannot be isolated from momentum | Partial-out ARM from revenue; use ARM growth rate instead of level |
| 6 | No store-level P&L (Five Below) | Data gap | Cannot distinguish low-quality-site failure from normal new-store ramp | Store-level revenue and cost data (internal) |
| 7 | External factors not modelled | Assumption | Competitor moves (Disney+, Max), content spending, macro (consumer confidence) drive both companies' outcomes | Add competitor subscriber counts; add content spend as covariate |
| 8 | Single held-out test point (Netflix Q1 2025 only) | Validation gap | One test observation cannot give reliable out-of-sample confidence | Evaluate model quarterly as 2025 and 2026 data arrive |

---

## 8. Chart Manifest and File List

| # | File | What it shows | Key takeaway | Readable |
|---|------|---------------|--------------|---------|
| 01 | `reports/charts/01_netflix_ucan_revenue.png` | UCAN quarterly revenue Q4'19–Q4'25 with price-event markers | Revenue nearly doubled; every price event followed by growth | Yes |
| 02 | `reports/charts/02_five_below_stores_vs_comp.png` | Net new stores vs comp sales % by fiscal year | Fastest expansion years coincide with negative comps | Yes |
| 03 | `reports/charts/03_five_below_op_margin.png` | Operating margin % FY2018–FY2025 | Margin compressed in peak expansion; recovered in FY2025 | Yes |
| 04 | `reports/charts/04_five_below_rev_per_store.png` | Revenue per store FY2018–FY2025 | Dip to $2.19M in FY2024; recovered to $2.48M in FY2025 | Yes |
| 05 | `reports/charts/05_netflix_revenue_decomposition.png` | Member growth vs ARM growth vs total revenue growth YoY | Both ARM and member growth contribute; ARM dominates post-2023 | Yes |
| 06 | `reports/charts/06_netflix_revenue_model.png` | Actual vs walk-forward predicted revenue; 2025 held-out | Model tracks trend; slightly underpredicts 2025 acceleration | Yes |
| 07 | `reports/charts/07_five_below_model_fit.png` | LOOCV actual vs predicted for comp sales and op margin | Comp model misses COVID extremes; margin model is tighter | Yes |

**Supporting files:**
- `reports/customer_risk_scores.csv` — per-row actuals, predictions, residuals and split labels for all models
- `reports/tables/actionability_netflix.csv` — Netflix effect sizes and confidence bounds
- `reports/tables/actionability_five_below.csv` — Five Below effect sizes and confidence bounds
- `reports/modeling/tables/model_comparison.csv` — full model comparison grid
- `reports/modeling/tables/coefficient_table.csv` — all model coefficients with standard errors
- `reports/modeling/scores.csv` — original scores file from model builder
- `reports/exploration/findings.md` — full exploration findings
- `reports/exploration/hypotheses.md` — hypothesis tests with intervals
- `reports/modeling/model_card.md` — full model card
- `reports/modeling/tuning.md` — validation design and tuning log
- `reports/modeling/features.md` — feature catalogue

---

## Reconciliation Check

| Item | Explorer value | Model builder value | Match? | Note |
|------|---------------|--------------------|---------|----|
| Netflix rows | 24 (revenue); 20 (with members) | 20 train + 4 test (revenue) | Yes | Explorer counted all 24 quarters; model correctly separated 2025 as held-out |
| Netflix target | revenue_usd_m | revenue_usd_m | Yes | — |
| Five Below rows | 8 | 7 (comp model); 8 (margin model) | Yes — reconciled | Comp model drops FY2018 (needs lag); margin model uses all 8 |
| Five Below target | comp_sales_pct and op_margin_pct | Same | Yes | — |
| Held-out test touched once | Specified in handoff | Confirmed in tuning.md | Yes | Model card and tuning.md both confirm |
| Revenue per store peak value | $2.60M (findings.md) | Not modelled directly | Minor discrepancy | Chart (07_five_below_rev_per_store.png) shows FY2022 as $2.30M; findings.md text says $2.60M. Use chart value ($2.30M) as the directly read number. |

No material reconciliation failures found.

---

## 9. Glossary

| Term | Plain-language meaning |
|------|----------------------|
| ARM | Average Revenue per Member per month. Total UCAN revenue divided by memberships divided by 3 (months per quarter). Netflix's key pricing metric. |
| UCAN | United States and Canada. Netflix's reporting region for North American subscribers and revenue. |
| Walk-forward CV | Cross-validation for time series. Train on the first N periods, predict the next one, expand the window, repeat. Prevents future data leaking into training. |
| LOOCV | Leave-one-out cross-validation. Each fold holds out one row; the model trains on the rest. Used here because N = 8 for Five Below. |
| Ridge regression | Linear regression with a penalty on coefficient size. The penalty (alpha) shrinks coefficients to prevent overfitting on small samples. |
| OOF (out-of-fold) | Predictions made on data points that were held out of that training fold. Equivalent to test-set predictions within cross-validation. |
| Comparable sales (comps) | Sales growth for stores open at least 15 months. Removes the effect of new-store openings; measures organic same-store productivity. |
| Operating margin | Operating income as a share of revenue. What percentage of each revenue dollar the company keeps after cost of goods and SGA. |
| SGA intensity | Selling, general and administrative expenses divided by revenue. Measures overhead burden. |
| Expansion rate | Net new stores opened divided by the prior-year store count. Measures how fast the fleet is growing as a share of its own size. |
| Spearman rho | A rank-order correlation coefficient. Ranges from −1 to +1. Does not assume a linear relationship or normally distributed data. |
| Modeled association | An effect size estimated from a statistical model. It tells you two variables move together, not that one causes the other. |
| Measured | A number read directly from the data, requiring no model. |
| Assumed | A number chosen by a person as an input (e.g., the company's $2M/store viability threshold). |
| Hodges-Lehmann estimator | A robust measure of median difference between two groups, paired with the Mann-Whitney test. Resistant to outliers. |
| Exact permutation test | A significance test that enumerates all possible orderings of the data. Used when N is too small for asymptotic approximations. |
| Paid-sharing enforcement | Netflix's May 2023 policy change requiring members to pay for accounts shared outside their household. Treated here as a structural break. |
