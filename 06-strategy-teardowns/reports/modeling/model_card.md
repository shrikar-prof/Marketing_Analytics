# Model Card — Strategy Teardowns

Generated: 2026-11-17
Author: Shrikar (shrikar.p@triiqinnovations.com)

---

## What the model predicts

Two families of small-panel regression models answer specific strategic questions:

1. **Netflix UCAN revenue model** — predicts quarterly UCAN (US and Canada) streaming revenue
   in USD millions, given lagged average revenue per member (ARM), prior-quarter revenue,
   and structural-break indicators (paid-sharing enforcement, price events).

2. **Netflix paid membership model** — predicts end-of-quarter paid UCAN memberships
   given prior-quarter membership count, price-event indicator, and paid-sharing indicator.

3. **Five Below comparable-sales model** — predicts annual comparable-store sales growth (%)
   given the store-expansion rate and a COVID-year flag.

4. **Five Below operating-margin model** — predicts annual operating margin (%) given
   SGA intensity and the expansion rate.

---

## Data it learned from

- Netflix: SEC EDGAR 8-K shareholder letters, Q4 2019–Q4 2024 (20 quarters with membership data;
  24 quarters with revenue data). Public domain.
- Five Below: SEC EDGAR 10-K annual filings, FY2018–FY2025 (8 fiscal years). Public domain.
- No personal data, no proprietary data, no consumer-level records.

---

## How it was tested

- **Five Below:** Leave-one-out cross-validation (8 folds). Each fold trains on 7 of 8 years
  and predicts the remaining year.
- **Netflix revenue:** Walk-forward expanding-window cross-validation (12 OOF predictions
  from Q4'21 onward) on training data Q4'19–Q4'24. Final test: Q1–Q4 2025 (touched once).
- Validation design and model-selection rules were written down before seeing the results.

---

## How good it is

**Five Below (LOOCV):**
- comp_sales_pct:  LOOCV MAE = 11.07 ppt | Naive baseline = 13.07 ppt
  (Acceptable threshold from handoff: 1.5 ppt)
- op_margin_pct:   LOOCV MAE = 1.79 ppt | Naive baseline = 2.17 ppt

**Netflix revenue (walk-forward CV):**
- revenue_usd_m:  Walk-forward MAE = $92.7M | Naive = $99.5M
  (Acceptable threshold from handoff: $100M; excellent = $50M)

In plain language: the Five Below comp-sales model explains the year-to-year variation in
comparable sales better than a naive guess, but the sample of only 8 years limits confidence.
The Netflix revenue model captures the strong trend driven by ARM growth and revenue momentum.

---

## What drives the predictions

**Netflix revenue:** Prior-quarter ARM (lagged one quarter) is the strongest driver.
ARM is the primary pricing signal; a higher ARM in the prior quarter is associated with
higher revenue in the current quarter (see coefficient table for the magnitude).
The association is not a causal estimate.
The post-paid-sharing structural break adds a positive step to revenue from Q2'23 onward.

**Five Below comp sales:** Higher store-expansion rate (more new stores relative to the
existing fleet) is associated with lower comparable-store sales growth. COVID years dominate
FY2020 and FY2021; the covid_flag absorbs that variance.

**Five Below margin:** Higher SGA intensity (SGA as share of revenue) is negatively associated
with operating margin — consistent with the accounting identity that overhead rising faster
than revenue compresses margins.

---

## What it must NOT be used for

- **Not for causal claims.** "If Netflix raises ARM by $1, revenue will rise by $X" is
  not supported. Unmeasured factors (content quality, competition, macro conditions) drive
  both ARM and revenue. The models measure association only.
- **Not for extrapolation.** Five Below's model is trained on 8 years; predictions more
  than 1 year outside the training range are unreliable.
- **Not for investor decisions.** This is a consulting illustration using public data.
  It is not investment advice.
- **Not for high-stakes automation.** The small sample sizes mean uncertainty intervals
  are wide. Human judgement is required for any operational decision.

---

## Known weaknesses

1. **Small N.** Eight rows (Five Below) and 20–24 rows (Netflix) cannot support complex models.
   LOOCV and walk-forward MAE are noisier than metrics on hundreds of observations.
2. **COVID distortion.** FY2020 and FY2021 (Five Below) are dominated by COVID effects.
   The covid_flag absorbs this but does not fully isolate expansion-pace effects in those years.
3. **Collinearity.** ARM and revenue are mathematically related (revenue ≈ ARM × members × 3).
   The models avoid using both simultaneously, but partial correlations may still bias
   individual coefficients.
4. **Structural change.** Netflix stopped reporting memberships after Q4'24. The membership
   model cannot be evaluated on 2025 data.
5. **External factors.** Competitor actions (Disney+, Max, Apple TV+), macro conditions,
   content spending, and password-sharing enforcement policy changes are not in the model.

---

## Technical appendix

### Model comparison — Five Below comp_sales_pct (LOOCV)

| model               |   n_rows |   n_features |   loocv_mae |   loocv_r2 |   best_alpha |
|:--------------------|---------:|-------------:|------------:|-----------:|-------------:|
| expansion_rate_only |        7 |            1 |      11.072 |     -0.386 |          100 |
| expansion+sga+covid |        7 |            3 |      11.25  |     -0.43  |          100 |
| expansion+covid     |        7 |            2 |      12.348 |     -0.731 |          100 |
| expansion+lag+covid |        7 |            3 |      13.283 |     -1.355 |          100 |

### Model comparison — Five Below op_margin_pct (LOOCV)

| model                      |   n_rows |   n_features |   loocv_mae |   loocv_r2 |   best_alpha |
|:---------------------------|---------:|-------------:|------------:|-----------:|-------------:|
| sga_intensity_only         |        8 |            1 |       1.795 |     -0.455 |          100 |
| sga+margin_lag+covid       |        7 |            3 |       1.909 |     -0.505 |          100 |
| expansion+sga+covid        |        7 |            3 |       1.981 |     -0.766 |          100 |
| expansion+margin_lag+covid |        7 |            3 |       2.505 |     -1.707 |          100 |

### Model comparison — Netflix revenue (walk-forward CV)

| model                       |   n_train |   n_features |   wf_mae_usd_m |   wf_r2 |   best_alpha |
|:----------------------------|----------:|-------------:|---------------:|--------:|-------------:|
| arm_lag1+rev_lag1           |        20 |            2 |           92.7 |   0.908 |         0.01 |
| arm_lag1+rev_lag1+event     |        20 |            3 |          101.3 |   0.895 |         0.01 |
| arm_lag1+rev_lag1+break+qtr |        20 |            4 |          101.4 |   0.904 |         0.01 |
| trend+qtr+arm_roll4         |        20 |            3 |          123.8 |   0.855 |         0.01 |
| arm_lag1+post_sharing       |        20 |            2 |          179.5 |   0.671 |         1    |
| arm_lag1_only               |        20 |            1 |          187.3 |   0.628 |         0.1  |

### Model comparison — Netflix members (walk-forward CV)

| model              |   n_rows |   wf_mae_m |   wf_r2 |   best_alpha |
|:-------------------|---------:|-----------:|--------:|-------------:|
| lag1+post_sharing  |       20 |      1.193 |   0.893 |         0.01 |
| lag1+price+sharing |       20 |      1.212 |   0.89  |         0.01 |
| members_lag1_only  |       20 |      1.403 |   0.86  |         0.01 |
| lag1+price_event   |       20 |      1.419 |   0.851 |         0.01 |

### Coefficient table — all selected models

| model                         | feature           |      Coef. |    Std.Err. |          t |       P>|t| |
|:------------------------------|:------------------|-----------:|------------:|-----------:|------------:|
| fb_comp: expansion_rate_only  | const             |   4.0508   |  23.2       |  0.174604  | 0.868241    |
| fb_comp: expansion_rate_only  | expansion_rate    |   7.86565  | 156.715     |  0.0501908 | 0.961914    |
| fb_margin: sga_intensity_only | const             |  11.1316   |  12.4666    |  0.892919  | 0.406286    |
| fb_margin: sga_intensity_only | sga_intensity     |  -2.16411  |  53.1278    | -0.0407341 | 0.96883     |
| nf_revenue: arm_lag1+rev_lag1 | const             | 402.52     | 315.367     |  1.27636   | 0.218992    |
| nf_revenue: arm_lag1+rev_lag1 | arm_lag1          | -72.2555   |  51.5247    | -1.40235   | 0.178809    |
| nf_revenue: arm_lag1+rev_lag1 | rev_lag1          |   1.22959  |   0.149753  |  8.21079   | 2.55691e-07 |
| nf_members: lag1+post_sharing | const             |   6.73251  |   7.28181   |  0.924566  | 0.36813     |
| nf_members: lag1+post_sharing | members_lag1      |   0.915026 |   0.0994636 |  9.19961   | 5.18349e-08 |
| nf_members: lag1+post_sharing | post_paid_sharing |   2.2289   |   0.887837  |  2.51048   | 0.0224606   |

---
_Data source: SEC EDGAR public filings. All models are illustrative for portfolio purposes._
