# Churn driver diagnostic: handoff report

Labels used throughout: **measured** (counted in the data), **modeled** (from the model; an association, not a cause), **assumed** (a number someone chose). Money is monthly recurring revenue (the monthly bill, `MonthlyCharges`) per month unless it says per year. Technical terms are defined in brackets at first use and again in the glossary (section 9).

## 1. The question and the answer

**Question.** Which customer traits predict churn (a customer leaving in the observation window), how much revenue sits in the riskiest groups, and what is the smallest intervention that captures most of the upside?

**Answer.** Churn is a contract, tenure and fiber problem, not a gender or phone problem. Month-to-month customers leave at 42.7% (of 3,875 customers) and hold 86.9% of the monthly revenue lost (measured). The sharpest group is month-to-month fiber customers in their first 12 months: 916 customers (13.0% of the base) leave at 70.2% and hold $53,178 per month of lost revenue, 38.2% of the $139,131 total (measured). A logistic-regression risk score ranks customers well on 1,409 held-out customers: the top 20% by score hold 53.8% of lost revenue (95% interval 49.8% to 59.0%) (measured on held-out rows). It does not beat a simple segment rule or a plain logistic model by a margin the test can show. The smallest modeled lever is a switch from month-to-month to a one-year contract: treating the best 27% of month-to-month customers (1,060 customers, 15% of the base) captures 50% of the modeled saving (modeled). Nothing in this data says an offer works, what it costs, or how many customers it would keep. A randomised pilot is the next step.

## 2. The data in five lines

- **Source.** IBM Telco Customer Churn sample (fictional California telecom, one fiscal quarter). Dictionary: `reports/exploration/data_dictionary.md`. Cleaning log: `reports/exploration/cleaning_log.md`.
- **Grain.** One row per customer, one snapshot. No date column.
- **Size.** 7,043 customers, 21 raw columns. No row dropped in cleaning.
- **Target and rate.** `churn_flag` (1 = left): 1,869 of 7,043 customers, 26.5% of customers (measured).
- **Value at stake.** Leavers paid $139,131 per month, 30.5% of the $456,117 monthly revenue; $1,669,570 per year (measured). Margin, acquisition cost and lifetime value are not in the data.

## 3. What the exploration found

Full detail: `reports/exploration/findings.md`, `reports/exploration/hypotheses.md`. Reliability verdict is the explorer's pre-set bar (p below 0.005 and an interval that excludes zero) and my reconciliation check (section 7).

| # | Finding (measured) | Number | Reliability | Chart |
|---|---|---|---|---|
| 1 | Contract is the strongest single link. | Month-to-month 42.7% vs two-year 2.8% of customers who left; gap 36.0 points (95% interval 34.2 to 37.8). | Reliable (H1). A link, not proof that a contract changes behaviour. | `charts/01_churn_by_contract.png` |
| 2 | New customers leave most. | Months 0-6: 52.9% (of 1,481); months 49-72: 9.5%. First 12 months 47.4% vs 17.1%. | Reliable (H3). Tenure of leavers may be measured at exit (unknown). | `charts/02_churn_by_tenure.png` |
| 3 | Fiber leaves at about twice the DSL rate, inside every contract type. | Fiber 41.9% vs DSL 19.0%; month-to-month fiber 55% vs DSL 32%. Pooled odds ratio 8.2 (7.0 to 9.6) for contract within internet type. | Reliable (H2, H9). Why fiber leaves is unknown: no price, fault or quality field. | `charts/03_contract_by_internet_heatmap.png` |
| 4 | Electronic-check payers leave at 45.3% vs 15.2% to 19.1% for other methods; gap holds on month-to-month (54% vs about 33%). | 34% of customers, 57% of leavers. | Reliable (H4). May stand in for sign-up route. | `reports/exploration/charts/12_heat_payment_by_contract.png` |
| 5 | A small group holds a large share of the loss. | Month-to-month fiber, first 12 months: 13.0% of customers, 70.2% churn, 38.2% of lost revenue. All month-to-month in year one: 28.3% of customers, 49.1% of lost revenue. | Reliable on counts (900+ customers each). Group was chosen on the same data, so it is slightly flattering. | `charts/04_candidate_groups_revenue.png` |

Also measured: internet customers without tech support leave at 41.6% vs 15.2% with it (H5, reliable). No reliable link for gender (26.9% vs 26.2%) or phone service (H8, H10).

## 4. The model

Full detail: `reports/modeling/model_card.md` (plain summary and technical appendix), `reports/modeling/tuning.md`.

- **Compared.** Five families on 25 cross-validation folds (5-fold, repeated 5 times) on 5,634 training customers: logistic regression (GLM) with 10 engineered features, random forest, LightGBM, XGBoost, CatBoost. Baselines: a raw-column logistic model and two segment rules.
- **Tuned (Optuna, a search tool that tries parameter sets and learns from earlier tries).** Top three families, 60 trials each, with nested cross-validation (tuning inside each outer fold, so the tuning score is honest). Pruned trials: 21 (GLM), 21 (XGBoost), 17 (random forest).
- **Best parameters.** GLM: elastic-net penalty, `C` = 9.51, `l1_ratio` = 0.053 (almost no shrinkage, mostly ridge-type). Nested AUC 0.8503 for GLM and XGBoost, 0.8476 for random forest.
- **Parameter importance.** GLM: `l1_ratio` 0.65, `C` 0.35. XGBoost: spread out (learning rate 0.26, subsample 0.22, nothing above 0.3). Random forest: `max_depth` 0.63. Tuning added almost nothing for the GLM: 0.8501 untuned vs 0.8503 tuned (measured). The best XGBoost depth is 2, meaning the signal is nearly additive, which is why the simple model ties the complex one.
- **Chosen: GLM.** Tied on AUC with XGBoost within one standard deviation, simplest, best-calibrated, fastest. The rule was fixed before the test was scored.
- **Held-out test, plain words.** Picking the top-scored fifth of customers finds just over half of the revenue that leaves, where picking at random finds a fifth. Of customers flagged in that fifth, 68% really leave.

| held-out test (1,409 customers, 374 leavers) | estimate | 95% interval |
|---|---|---|
| AUC (chance a random leaver outscores a random stayer; 0.5 = coin flip) | 0.847 | 0.827 to 0.868 |
| Top-20% share of lost revenue (of $27,215 per month lost in the test set) | 53.8% | 49.8% to 59.0% |
| Top-20% precision (share of flagged who leave) | 67.7% | 62.1% to 72.7% |
| Top-20% recall (share of all leavers flagged) | 51.1% | 47.2% to 55.3% |
| Brier score (mean squared probability error; 0.195 if always guessing the base rate) | 0.135 | 0.124 to 0.146 |
| ECE (average calibration gap; target 0.05 or less) | 0.021 | 0.018 to 0.045 |

- **Against simple alternatives** (same test rows; top-20% revenue capture): segment rule 50.3%, raw logistic 54.8%. Paired difference final minus segment rule +3.4 points (-0.1 to +7.6); minus raw logistic -1.1 points (-3.6 to +1.3). Both intervals include zero. On AUC the final model is ahead of both (+0.031 and +0.008), intervals exclude zero, but the AUC gain over raw logistic is small. **The business-metric edge over simple rules is not proven on this test.**
- **Where weaker.** Ranking inside segments is weaker (section 7). Small test: about +/-5 points on every rate. One quarter, one company. Tenure and billing may be recorded at exit.
- Chart: `charts/05_model_evaluation_panel.png`. Model comparison: `reports/modeling/charts/model_comparison.png` (its axes are cut, so bars exaggerate gaps; read the error bars).

## 5. Drivers and levers

All rows are **modeled** (SHAP, a method that splits each prediction into per-column contributions, and permutation importance, the AUC lost when one column is shuffled). They show what the model uses, not what causes churn. Source: `reports/modeling/tables/driver_importance.csv`. Chart: `charts/06_driver_importance.png`.

| type | columns | how the model uses them |
|---|---|---|
| Structural (business cannot change) | tenure, Dependents, SeniorCitizen, Partner, gender | Tenure ranks 3rd by permutation, 5th by SHAP. The rest are near zero. Gender must not be used. SeniorCitizen should not drive offers. |
| Semi-controllable (price and product design) | MonthlyCharges, InternetService, MultipleLines, PhoneService | InternetService is 1st by permutation (AUC drop 0.230), MonthlyCharges 1st by SHAP. They overlap (bill is mostly service mix), so this is not proof that price drives churn. |
| Controllable (offer or process) | Contract, TechSupport, StreamingMovies, StreamingTV, PaperlessBilling, PaymentMethod, add-ons | Contract is the strongest controllable column (AUC drop 0.070). TechSupport matters by SHAP (0.55) but little by permutation (0.005), because other columns carry the same signal. |

**What-if sensitivity (modeled association, not cause).** Held-out eligible customers, model score moved with one column changed. Source: `reports/modeling/tables/counterfactual_levers.csv`. Chart: `charts/08_counterfactual_levers.png`.

| lever | eligible (test) | change in predicted churn | 95% interval |
|---|---|---|---|
| Month-to-month to one year, bill unchanged | 773 | -18.0 points | -18.6 to -17.4 |
| Electronic check to automatic bank transfer, bill unchanged | 474 | -6.1 points | -6.3 to -5.9 |
| Paperless billing yes to no, bill unchanged | 840 | -5.8 points | -6.0 to -5.6 |
| Tech support added, bill unchanged / bill up $5.05 | 702 | -0.4 / -5.7 points | -0.6 to -0.3 / -5.9 to -5.5 |
| Online security added, bill unchanged / bill up $5.04 | 701 | -1.4 / -6.7 points | -1.6 to -1.3 / -7.0 to -6.5 |

The add-on rows move 5 to 13 times with the bill assumption (the model gives the bill a negative weight once services are fixed). Do not size anything from them. The intervals are bootstrap intervals over customers; they do not include the risk that customers who pick long contracts differ in unrecorded ways (selection). The paperless row has no business story; its direction was a guess.

## 6. Actionability

Built from the model's score file (`reports/modeling/scores.csv`: 5,634 out-of-fold scores, a score from a model that never saw that customer, plus 1,409 held-out scores) joined to the clean table. Per-customer file: `reports/customer_risk_scores.csv` (7,043 rows). Tables: `reports/tables/`.

### 6.1 Value at risk by segment (`tables/value_at_risk_by_segment.csv`)

Revenue exposed = sum of monthly bills of every customer in the segment (measured). Actual lost = bills of customers who left (measured). Expected value at risk = sum of score times bill (modeled).

| segment | customers (% of base) | actual churn | revenue exposed, $/month (% of total) | actual lost, $/month (% of total lost) | modeled value at risk, $/month |
|---|---|---|---|---|---|
| All customers | 7,043 (100%) | 26.5% | 456,117 (100%) | 139,131 (100%) | 139,783 |
| Month-to-month | 3,875 (55.0%) | 42.7% | 257,294 (56.4%) | 120,847 (86.9%) | 122,212 |
| Fiber optic | 3,096 (44.0%) | 41.9% | 283,284 (62.1%) | 114,300 (82.2%) | 114,861 |
| Electronic check | 2,365 (33.6%) | 45.3% | 180,345 (39.5%) | 84,289 (60.6%) | 85,240 |
| Tenure first 12 months | 2,186 (31.0%) | 47.4% | 122,630 (26.9%) | 68,954 (49.6%) | 69,175 |
| Internet, no tech support | 3,473 (49.3%) | 41.6% | 259,040 (56.8%) | 110,710 (79.6%) | 111,388 |
| Month-to-month, first 12 months | 1,994 (28.3%) | 51.4% | 116,087 (25.5%) | 68,301 (49.1%) | 68,541 |
| Month-to-month, fiber, first 12 months | 916 (13.0%) | 70.2% | 75,183 (16.5%) | 53,178 (38.2%) | 53,345 |
| Two-year contract | 1,695 (24.1%) | 2.8% | 103,006 (22.6%) | 4,165 (3.0%) | 4,069 |

**Reconciliation.** Modeled total $139,783 per month vs actual $139,131: gap +$652 (+0.5%). Segment gaps are within 3% of segment loss, except one-year contracts (-4.4%). Reading: the score is well calibrated on average, so summed risk is a fair total. It says nothing about any single customer. Annual actual loss in the first-year month-to-month fiber group: $638,140 per year (measured).

### 6.2 Risk-only targeting (`tables/risk_only_targeting.csv`)

Contact the top share of customers by predicted risk. Held-out test only (1,409 customers) is the honest column; pooled uses out-of-fold scores for the 5,634 training rows.

| top share by risk | held-out: share of leavers | held-out: share of lost revenue | pooled 7,043: share of leavers | pooled: share of lost revenue | pooled: churn rate in group |
|---|---|---|---|---|---|
| 10% | 28.9% | 31.2% | 28.6% | 31.0% | 76.0% |
| 20% | 51.1% | 53.8% | 51.7% | 55.2% | 68.6% |
| 30% | 66.0% | 70.0% | 67.0% | 71.0% | 59.3% |
| 40% | 77.8% | 80.7% | 78.9% | 81.6% | 52.3% |
| 50% | 87.4% | 89.0% | 88.3% | 89.8% | 46.9% |

Reading: the first 30% of customers reach about 70% of lost revenue (measured on held-out rows); the 40% to 50% band adds only 8.2% of lost revenue for 10% of customers, less than a random draw would. Cut-offs by probability: score above 0.50 flags 21.1% of customers at 66.8% precision and 56.1% of lost revenue; above 0.25 flags 43.2% at 49.1% and 82.3% (`reports/modeling/tables/threshold_table.csv`).

### 6.3 Smallest intervention (`tables/smallest_intervention.csv`)

Method (modeled): for each lever, every eligible customer is re-scored with the lever switched; saving = (risk before minus risk after) times current bill, in $ per month of expected revenue not lost. Customers are ranked by saving. All 7,043 customers are scored with the saved model (the 5,634 training rows are in-sample for the model; a held-out-only check agrees within 1 to 2 points of share). No save rate, offer cost or take-up is included.

| lever | eligible (% of base) | total modeled saving, $/month | customers for 50% of saving (% of eligible / % of base) | for 80% (% of eligible / % of base) |
|---|---|---|---|---|
| Month-to-month to one year | 3,875 (55.0%) | 48,620 | 1,060 (27.4% / 15.1%) | 2,072 (53.5% / 29.4%) |
| Electronic check to automatic transfer | 2,365 (33.6%) | 11,266 | 771 (32.6% / 10.9%) | 1,430 (60.5% / 20.3%) |
| Paperless yes to no | 4,171 (59.2%) | 18,510 | 1,119 (26.8% / 15.9%) | 2,115 (50.7% / 30.0%) |
| Tech support (bill up; unstable) | 3,473 (49.3%) | 14,555 | 1,078 (31.0% / 15.3%) | 2,018 (58.1% / 28.7%) |
| Online security (bill up; unstable) | 3,498 (49.7%) | 17,360 | 1,105 (31.6% / 15.7%) | 2,052 (58.7% / 29.1%) |

Chart: `charts/07_smallest_intervention_curve.png`. Reading:
- **Concentration is mild.** About a quarter to a third of the eligible group gives half of the modeled saving. Because each curve is smooth, there is no sharp "small group" cut-off; the choice depends on offer cost.
- **Who the contract-lever top 1,060 are** (`tables/smallest_intervention_profile.csv`): 98% fiber, 84% in their first 12 months, mean bill $85.10, actual churn 66.9%. They hold $60,324 per month of actual lost revenue, 43.4% of the total (measured). This is the same group the explorer found.
- **Illustration (assumed).** If a contract offer kept 10% of the leavers in those 1,060 customers, revenue kept would be about $6,030 per month ($72,400 per year) before offer cost. The 10% is chosen, not estimated. Break-even needs the client's offer cost and real save rate.
- Pricing, discounts and the bill assumption are open: the contract row assumes the bill does not change.

## 7. Failure modes, assumptions and instrumentation gaps

**Reconciliation of exploration and modeling (done by me).** Match: 7,043 rows, 1,869 leavers, 26.5% target rate; `churn_flag` and `MonthlyCharges` agree for every customer between `clean.parquet` and `scores.csv`; train and test rates are 26.54% each; $456,117 and $139,131 reproduce. Cleaning rules were used as logged and the leakage-prone billing totals were left out as the handoff advised. Differences, none material:
| item | explorer | model-builder | verdict |
|---|---|---|---|
| Top-20% capture of lost revenue | 52% (in-sample, 17 segments) | 53.8% (held-out); explorer-style rule 50.3% held-out | Different bases. Held-out is right; in-sample flatters. |
| Segments | 17 segments (notebook text once said 18) | n/a | 17 is right; fixed in the notebook. |
| Total modeled vs actual lost revenue | n/a | n/a | $139,783 vs $139,131 (+0.5%), see 6.1. |
| Review status | Notebooks 01 to 03 got two review rounds each; minor gaps (explanations) left open, no third review | | Low risk to numbers; results unchanged between rounds. |

**Held-out test touched once?** For selection and the performance numbers: yes. The code (`src/build_notebook_03.py`, section 7) scores the test rows in one cell after model choice; nothing was chosen on them. The same rows were later reused for descriptive work: permutation importance, segment performance, what-if tables, and a re-score by `src/pipeline.py --evaluate` that reproduces AUC 0.84742. No decision depended on those. Verified by reading the code, not by re-running the notebooks. Consequence: driver and what-if numbers are test-based and noisy.

**Failure modes and gaps, in priority order.**

| # | issue | what it does | telemetry that fixes it |
|---|---|---|---|
| 1 | **Causality.** Snapshot, customers chose their contract and payment. The -18 point contract effect is an association. | Could overstate any lever; selection may explain much of it. | Randomised pilot with holdout; offer log with assignment and take-up. |
| 2 | **No time axis.** One quarter, no dates. | No trend, no seasonality, no time-based test; model cannot be shown to hold next quarter. | Monthly snapshots with signup, contract-change and churn dates. |
| 3 | **Tenure and billing may be measured at exit** (unknown). | Could inflate the model, mostly through tenure (3rd most important). | Data owner confirms; add "as of" date per column. |
| 4 | **Weak ranking inside segments.** Test AUC within month-to-month 0.76, fiber 0.79, seniors 0.78; top-20% capture inside month-to-month 0.39, fiber 0.36, electronic check 0.38 (`reports/modeling/tables/segment_performance.csv`). | Best for splitting segments from each other, less for choosing who to call within the target segment. | Usage, call, fault and billing-event data per customer. |
| 5 | **Poorly identified variables.** Bill and service mix nearly equal (r = 1.00 with average spend); tech support and security share signal; add-on levers swing 5 to 13 times with the bill assumption. | Price effect cannot be separated from product; add-on sizing unusable. | Price history, discounts, promo flags, list price by plan. |
| 6 | **Small cells and wide intervals.** 374 test leavers: about +/-5 points. Five tiny segments (under 100 customers); bank-transfer segment is 3.1 points under-predicted on test. | Single-segment numbers are fragile. | More customers or periods; pool across quarters. |
| 7 | **No economics.** No margin, offer cost, save rate, customer lifetime. | Cannot compute return; $ figures are revenue, not profit. | Offer cost and margin from finance; pilot save rate. |
| 8 | **Fictional single-company sample.** | Conclusions describe this data. | Re-test on the client's own data (KKBox is only profiled, no label). |
| 9 | **Fairness.** SeniorCitizen links to churn (41.7% vs 23.6%). | Offers or credit by age is not appropriate. | Policy review before use. |

**Assumptions.** Measured: counts, rates, revenue. Modeled: scores, driver ranks, what-ifs, intervention savings. Assumed: the bill is unchanged in the contract, payment and paperless levers; add-on price from a regression on training bills ($5.05 and $5.04); the 10% save-rate illustration; the 20/80% capture thresholds chosen by me.

**Use limits.** Do not use the score to decide price or credit for an individual, to explain why a customer left, or to forecast saved revenue.

## 8. Chart manifest and file list

Selected charts (`reports/charts/`):

| file | source | shows |
|---|---|---|
| `01_churn_by_contract.png` | exploration chart 03 | churn by contract |
| `02_churn_by_tenure.png` | exploration chart 04 | churn by tenure band |
| `03_contract_by_internet_heatmap.png` | exploration chart 10 | contract x internet churn |
| `04_candidate_groups_revenue.png` | exploration chart 15 | customer share vs lost-revenue share for 7 groups |
| `05_model_evaluation_panel.png` | modeling evaluation panel | ROC, precision-recall, calibration, deciles, capture, thresholds |
| `06_driver_importance.png` | modeling driver chart | permutation and SHAP importance |
| `07_smallest_intervention_curve.png` | new (this report) | modeled saving vs customers treated |
| `08_counterfactual_levers.png` | modeling counterfactual chart | what-if changes with intervals |

I opened all 42 PNGs (16 exploration, 26 modeling). All are readable. Minor issues: exploration 07 has a blank right margin and an overlapping label; exploration 08 average label touches bars; the GLM Optuna history is squashed by two bad trials; `feat_price_resid` labels overlap its legend; `model_comparison.png` axes are cut. Per-chart record: `tables/chart_audit.csv`.

Files written:
- `reports/ml_handoff_report.md` (this file)
- `reports/customer_risk_scores.csv`: per customer score, rank, pooled decile, top-20% flag, segment flags, expected value at risk, modeled contract-lever saving
- `reports/tables/value_at_risk_by_segment.csv`, `risk_only_targeting.csv`, `smallest_intervention.csv`, `smallest_intervention_profile.csv`, `decile_table_all_customers.csv`, `chart_audit.csv`
- `reports/charts/01` to `08` (above)

Note on the score file: `risk_decile_pooled` ranks the 5,634 out-of-fold and 1,409 held-out scores together; the held-out-only decile table is in `reports/modeling/tables/decile_table.csv`.

## 9. Glossary

- **AUC** (area under the ROC curve): chance a random leaver is scored above a random stayer; 0.5 is a coin flip.
- **Bootstrap interval:** range from re-drawing the same customers many times; shows how much a number could move by luck.
- **Brier score:** mean squared error of the predicted probability; lower is better.
- **Calibration / ECE:** whether customers scored 40% leave about 40% of the time; ECE is the average gap.
- **Churn:** a customer leaving in the observation window.
- **Counterfactual (what-if):** re-scoring a customer with one column changed; an association, not a cause.
- **Cramér's V:** link strength between two categories, 0 to 1.
- **Cross-validation:** fit on part of the training data, score on the rest, repeat.
- **Decile:** one tenth of customers ranked by risk; decile 1 is the riskiest.
- **Elastic net:** logistic regression with a penalty that shrinks weights; `C` is the inverse penalty strength, `l1_ratio` the mix of ridge and lasso.
- **Expected value at risk:** predicted churn probability times monthly bill, summed.
- **GLM:** generalised linear model; here, logistic regression.
- **Held-out test set:** 1,409 customers locked away until the end.
- **Lift:** group churn rate divided by the overall rate.
- **Nested cross-validation:** tuning inside each outer fold so the reported score is not tuned on its own data.
- **Odds ratio:** odds of leaving in one group divided by odds in another; 1 means no effect.
- **Optuna:** a tool that searches parameter settings across trials; pruning stops weak trials early.
- **Out-of-fold score:** a score from a model that never saw that customer.
- **Permutation importance:** AUC lost when one column is shuffled.
- **Precision / recall:** share of flagged who leave / share of leavers flagged.
- **SHAP:** a method that splits each prediction into per-column contributions.
- **Structural / semi-controllable / controllable:** the business cannot / can slowly / can quickly change the column (a judgement, not a result).
- **Top-20% capture:** share of lost revenue held by the 20% of customers with the highest scores.
