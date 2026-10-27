# Churn driver diagnostic: final report

Project 01, telecom churn sample (IBM Telco, 7,043 customers). Prepared from the team's files on 27 October 2026.

**How to read this report.** Part A answers the question in plain language. Part B shows how each stage reached its result. Part C lists checks and limits. Part D is the appendix: glossary, charts, web sources and files.

**Evidence labels.** Every number carries one of four labels.

| label | meaning |
|---|---|
| measured | counted directly in the data |
| modeled | produced by the risk model; an association, not a cause |
| external | from a published web source, with its URL in Part D |
| assumed | a number someone chose; not measured |

Money is monthly recurring revenue (the monthly bill, `MonthlyCharges`) in US dollars per month, unless it says per year. Citations name the source file and section.

---

# Part A. The answer in plain language

## The question

Leadership asked three things (`problem_description.md`). Which customer traits most strongly predict churn (a customer leaving in the observation window)? How much revenue sits in the highest-risk groups? What is the smallest intervention that captures most of the upside?

## The answer

Churn here is a contract, first-year and fiber problem. It is not a gender or phone-service problem. Month-to-month customers in their first year on fiber are the core of the loss. A simple risk score ranks customers well, but it is not proven better than a simple segment rule. The strongest lever the business controls is moving customers onto a one-year commitment. No number in this data shows that any offer works, what it costs, or how many customers it keeps. The next step is a set of randomised pilots (tests where a random group gets nothing, for comparison).

## The numbers that matter

| # | number | label | what it means for the decision | source |
|---|---|---|---|---|
| 1 | Leavers paid $139,131 a month, 30.5% of $456,117 monthly revenue; $1,669,570 a year | measured | This is the size of the prize. It is revenue, not profit: margin is not in the data. | `ml_handoff_report.md` s.2 |
| 2 | 916 month-to-month fiber customers in their first 12 months (13.0% of 7,043) leave at 70.2% and hold $53,178 a month, 38.2% of lost revenue | measured | Start here. One-eighth of customers holds over a third of the loss. | `ml_handoff_report.md` s.6.1 |
| 3 | The top 20% of customers by risk score hold 53.8% of lost revenue on 1,409 held-out customers (95% interval 49.8% to 59.0%); random picking gives 20% | measured on held-out rows | The score is a usable call list. Its edge over a simple segment rule (+3.4 points, interval -0.1 to +7.6) is not proven. | `model_card.md` summary; `ml_handoff_report.md` s.4 |
| 4 | Switching month-to-month to a one-year contract lowers predicted churn by 18.0 points (interval -18.6 to -17.4) | modeled | Contract is the strongest lever the business controls. Some of the gap may come from who chooses long contracts. | `model_card.md` s.J |
| 5 | Treating the best 1,060 month-to-month customers (15.1% of the base) gives 50% of the modeled contract saving | modeled | A small, named list can carry half the modeled gain. The save rate is unknown, so the dollar return is unknown. | `ml_handoff_report.md` s.6.3 |

## What should happen next

| # | action | owner track | source |
|---|---|---|---|
| 1 | Make a one-year price lock the default for new fiber sales. | Commercial (Track B) | `executive_growth_strategy.md` s.4 Track B item 1 |
| 2 | Start a randomised fiber first-90-days programme (install check, pre-bill call, free tech-support trial). | Pilot 2 | `executive_growth_strategy.md` s.5 |
| 3 | Test a one-year commitment offer on 2,548 month-to-month customers scored 0.3 or higher, with a holdout. | Pilot 1 | `executive_growth_strategy.md` s.5 |
| 4 | Log every offer, acceptance and outcome, and add event dates, so the save rate can be measured. | Technical (Track A) | `executive_growth_strategy.md` s.4 Track A items 2 and 5 |
| 5 | Keep age and gender out of offer and price decisions; cap the senior share of contacts. | Guardrail | `executive_growth_strategy.md` s.4 Track A item 7 |

## What is uncertain

- No cause is proven: the data is one snapshot, and customers chose their own contract and payment method.
- The save rate, offer cost and margin are not in the data, so every profit figure is assumed.
- The data is IBM's fictional sample of one quarter with no dates; tenure may be recorded at exit.

---

# Part B. How we got there

## B1. The data: 7,043 fictional telecom customers, one snapshot, no rows dropped

**What it is.** The IBM Telco Customer Churn sample: a fictional California telecom over one fiscal quarter (`problem_description.md`). One row per customer, 21 raw columns, no date column. The target is `Churn` (Yes/No).

**Where it came from.** IBM's public GitHub repository, with mirrors on Kaggle and Mendeley Data (`problem_description.md`). A second source, KKBox subscription transactions (1,048,575 rows, 906,706 members), was profiled only. It has no churn label, so nothing from it is used (`reports/exploration/quality_audit.md`).

**How it was checked and cleaned** (`reports/exploration/quality_audit.md`, `reports/exploration/cleaning_log.md`).

| issue | rows affected | action | label |
|---|---|---|---|
| `TotalCharges` stored as text | 7,043 (100%) | converted to a number | measured |
| Blank `TotalCharges` | 11 (0.16%), all tenure-0 accounts | set to missing, not zero | measured |
| Six add-on columns repeat "No internet service" | 1,526 customers x 6 columns = 9,156 cells | folded into "No"; `has_internet` keeps the fact | measured |
| `MultipleLines` repeats "No phone service" | 682 cells | folded into "No" | measured |
| Rows identical apart from the ID | 22 (0.31%) | kept: plausible real customers | measured |
| Lifetime bill far from tenure x price | 2 (0.03%) | kept and flagged | measured |
| Fully duplicated rows | 0 | none to drop | measured |

**What was excluded and why.** No row was dropped (`cleaning_log.md`). The model left out the billing totals (`TotalCharges` and columns built from it). Their timing relative to exit is unknown, so they could leak the answer (`model_card.md` summary). Nine derived columns were added for reporting, such as tenure bands and an autopay flag (`data_dictionary.md`).

**Base numbers** (`reports/exploration/findings.md`, business framing).

| measure | value | label |
|---|---|---|
| Customers | 7,043 | measured |
| Churned | 1,869 (26.5% of 7,043) | measured |
| Monthly revenue, all customers | $456,117 | measured |
| Monthly revenue of churned customers | $139,131 (30.5% of $456,117) | measured |
| Average monthly bill, churned vs stayed | $74.44 vs $61.27 | measured |

## B2. What exploration found: five reliable links, all descriptive

The explorer set a bar before testing (`reports/exploration/hypotheses.md`). A link is "reliable" if p (the chance of a gap this large by luck alone) is below 0.005 and its 95% interval excludes zero. The same data suggested and tested the ideas, so these are not independent proof.

| # | finding | number | label | reliability verdict | chart |
|---|---|---|---|---|---|
| 1 | Contract type is the strongest single link | Month-to-month 42.7% (of 3,875) vs two-year 2.8% (of 1,695); gap 36 points (interval 34 to 38) | measured | Reliable (H1). A link, not proof that a contract changes behaviour. | `reports/charts/01_churn_by_contract.png` |
| 2 | New customers leave at the highest rate | Months 0-6: 52.9% (1,481 customers, 21% of 7,043); after 4 years: 9.5% | measured | Reliable (H3). Tenure of leavers may be recorded at exit. | `reports/charts/02_churn_by_tenure.png` |
| 3 | Fiber customers leave at about twice the DSL rate, inside every contract type | Fiber 41.9% vs DSL 19.0%; month-to-month fiber 55% vs DSL 32% | measured | Reliable (H2, H9; pooled odds ratio 8.2, interval 7.0 to 9.6) | `reports/charts/03_contract_by_internet_heatmap.png` |
| 4 | Electronic-check payers leave at 45.3%, against 15.2% to 19.1% for other methods | 34% of customers, 57% of leavers; gap holds on month-to-month (54% vs about 33%) | measured | Reliable (H4). May stand in for sign-up route. | `reports/exploration/charts/12_heat_payment_by_contract.png` |
| 5 | A small group holds a large share of the loss | Month-to-month fiber, first 12 months: 916 customers (13.0%), 70.2% churn, 38.2% of lost revenue | measured | Reliable on counts (900+ customers). Chosen on the same data, so slightly flattering. | `reports/charts/04_candidate_groups_revenue.png` |

Sources: `reports/exploration/findings.md` summary; `ml_handoff_report.md` s.3.

**Also measured.** Internet customers without tech support leave at 41.6% vs 15.2% with it (H5, reliable). No reliable link for gender (26.9% vs 26.2%) or phone service (26.7% vs 24.9%) (H8, H10) (`findings.md`).

**Single-column link strength** (Cramér's V, a 0-to-1 measure of how strongly two categories are linked; `findings.md`, ranked drivers).

| column | Cramér's V | highest-rate group | lowest-rate group |
|---|---|---|---|
| Contract | 0.41 | Month-to-month 42.7% | Two year 2.8% |
| InternetService | 0.32 | Fiber optic 41.9% | No internet 7.4% |
| PaymentMethod | 0.30 | Electronic check 45.3% | Credit card (automatic) 15.2% |
| PaperlessBilling | 0.19 | Yes 33.6% | No 16.3% |
| TechSupport | 0.17 | No 31.2% | Yes 15.2% |
| gender | 0.01 | Female 26.9% | Male 26.2% |

## B3. The model: a simple logistic regression tied with complex models and was chosen

**What was compared** (`model_card.md` s.B). Five model families were scored on 25 cross-validation folds (fit on part of the training data, score on the rest, repeated) using 5,634 training customers (80%). Three simple baselines were scored the same way. 1,409 customers (20%, 374 leavers) were locked away for one final test.

| model | AUC mean (25 folds) | top-20% revenue capture | Brier | label |
|---|---|---|---|---|
| GLM (logistic regression, engineered features) | 0.8501 | 55.4% | 0.1329 | measured (cross-validation) |
| XGBoost | 0.8481 | 55.2% | 0.1339 | measured (cross-validation) |
| Random forest | 0.8458 | 54.4% | 0.1349 | measured (cross-validation) |
| CatBoost | 0.8447 | 54.3% | 0.1356 | measured (cross-validation) |
| LightGBM | 0.8443 | 54.6% | 0.1356 | measured (cross-validation) |
| Logistic regression, raw columns (baseline) | 0.8444 | 56.6% | 0.1355 | measured (cross-validation) |
| Rule 2: segment churn rate (baseline) | 0.8217 | 52.2% | 0.1425 | measured (cross-validation) |
| Rule 1: month-to-month fiber first-year flag (baseline) | 0.6485 | 43.8% | 0.2103 | measured (cross-validation) |

AUC (area under the curve) is the chance a random leaver is scored above a random stayer; 0.5 is a coin flip. Brier score is the average squared error of the predicted probability; lower is better.

**How tuning worked, in plain words** (`reports/modeling/tuning.md`). Optuna (a tool that tries parameter settings and learns from earlier tries) tuned the top three families. Each family got 60 trials per study. Weak trials were stopped early ("pruned"). Tuning ran inside nested cross-validation (tuning inside each outer fold, so the reported score is not tuned on its own data).

| family | nested AUC (mean +/- SD) | trials completed / pruned | most important parameter (share of score variation) | label |
|---|---|---|---|---|
| GLM | 0.8503 +/- 0.0106 | 39 / 21 | `l1_ratio` 0.654, then `C` 0.346 | measured |
| XGBoost | 0.8503 +/- 0.0088 | 39 / 21 | `learning_rate` 0.264; no single parameter dominates | measured |
| Random forest | 0.8476 +/- 0.0064 | 43 / 17 | `max_depth` 0.632 | measured |

What the parameter importance shows. For the GLM, the penalty mix mattered most, but tuning added almost nothing: 0.8501 untuned vs 0.8503 tuned (measured, `ml_handoff_report.md` s.4). The best XGBoost depth was 2, meaning the signal is nearly additive. That is why the simple model ties the complex one (`ml_handoff_report.md` s.4). Final GLM settings: elastic-net penalty (a penalty that shrinks weights), `C` = 9.51, `l1_ratio` = 0.053 (`model_card.md` s.A).

**Why the GLM won** (`model_card.md` s.D). A selection rule was fixed before the test. Among families within one standard deviation of the best nested AUC, pick the simplest. The GLM tied XGBoost at 0.8503, was simplest, had the lowest nested ECE (0.0235) and scored fastest.

**How good it is on the held-out test** (`model_card.md` s.E; 1,409 customers, 374 leavers).

| measure | estimate | 95% interval | label | what it means |
|---|---|---|---|---|
| AUC | 0.847 | 0.827 to 0.868 | measured | Ranks leavers above stayers 85% of the time |
| Top-20% share of lost revenue | 53.8% ($14,638 of $27,215) | 49.8% to 59.0% | measured | Calling the top fifth reaches just over half the lost revenue |
| Top-20% precision | 67.7% | 62.1% to 72.7% | measured | About two in three flagged customers really leave |
| Top-20% recall | 51.1% | 47.2% to 55.3% | measured | The top fifth contains half of all leavers |
| Brier score | 0.135 | 0.124 to 0.146 | measured | Better than 0.195 for always guessing the base rate |
| ECE (average calibration gap) | 0.021 | 0.018 to 0.045 | measured | Predicted rates match actual rates; target was 0.05 or less |

**Against simple alternatives** (`model_card.md` s.E, paired differences). On top-20% revenue capture, the model beats the segment rule by +3.4 points (interval -0.1 to +7.6). It trails the raw logistic model by -1.1 points (interval -3.6 to +1.3). Both intervals include zero, so no edge is proven on the business metric. On AUC the model leads both, with intervals that exclude zero (+0.031 and +0.008).

**Where it is weaker** (`model_card.md` s.H).

| segment (test) | customers | AUC within segment | top-20% capture within segment | label |
|---|---|---|---|---|
| Month-to-month | 773 | 0.76 | 0.39 | measured |
| Fiber optic | 613 | 0.79 | 0.36 | measured |
| Electronic check | 474 | 0.79 | 0.38 | measured |
| Senior citizens | 222 | 0.78 | 0.35 | measured |
| No internet | 312 | 0.89 | 0.76 | measured |

The model is better at separating segments than at choosing who to call inside the target segment. With 374 test leavers, every rate carries about +/-5 points of noise (`model_card.md` known weaknesses).

Chart: `reports/charts/05_model_evaluation_panel.png`.

## B4. What drives the predictions: contract is the strongest lever the business controls

The model's drivers come from two methods (`model_card.md` s.I). SHAP splits each prediction into per-column contributions. Permutation importance is the AUC lost when one column is shuffled. Both show what the model uses, not what causes churn. All rows are modeled.

| column | type | permutation AUC drop (rank) | mean SHAP (rank) | label |
|---|---|---|---|---|
| InternetService | semi-controllable | 0.230 (1) | 1.21 (2) | modeled |
| MonthlyCharges | semi-controllable | 0.105 (2) | 1.51 (1) | modeled |
| tenure | structural | 0.085 (3) | 0.49 (5) | modeled |
| Contract | controllable | 0.070 (4) | 0.77 (3) | modeled |
| StreamingMovies | controllable | 0.016 (5) | 0.42 (6) | modeled |
| TechSupport | controllable | 0.005 (8) | 0.55 (4) | modeled |
| PaymentMethod | controllable | 0.003 (10) | 0.16 (11) | modeled |
| gender | structural | -0.0001 (17) | 0.01 (18) | modeled |

Structural means the business cannot change it. Semi-controllable means it can change slowly (price, product). Controllable means it can change quickly (offer, process). These types are a judgement, not a result (`ml_handoff_report.md` s.9).

Bill and service mix measure nearly the same thing, so their high ranks do not show that price alone drives churn (`model_card.md` summary). Chart: `reports/charts/06_driver_importance.png`.

**What-if sensitivities** (counterfactual: re-score each eligible test customer with one column changed). All modeled; source `model_card.md` s.J.

| lever | eligible test customers | change in predicted churn (points) | 95% interval | label |
|---|---|---|---|---|
| Month-to-month to one year, bill unchanged | 773 | -18.0 | -18.6 to -17.4 | modeled |
| Electronic check to automatic bank transfer, bill unchanged | 474 | -6.1 | -6.3 to -5.9 | modeled |
| Paperless billing yes to no, bill unchanged | 840 | -5.8 | -6.0 to -5.6 | modeled |
| Tech support added, bill unchanged | 702 | -0.4 | -0.6 to -0.3 | modeled |
| Tech support added, bill up $5.05 | 702 | -5.7 | -5.9 to -5.5 | modeled |
| Online security added, bill unchanged | 701 | -1.4 | -1.6 to -1.3 | modeled |
| Online security added, bill up $5.04 | 701 | -6.7 | -7.0 to -6.5 | modeled |

The two add-on levers swing 5 to 13 times with the bill assumption. Do not size anything from them. The paperless row has no business story (`ml_handoff_report.md` s.5). The intervals cover luck in which customers were drawn; they do not cover selection (customers who chose long contracts may differ in unrecorded ways). Chart: `reports/charts/08_counterfactual_levers.png`.

## B5. Value at risk: the top 30% of customers by score hold 70% of lost revenue

**By segment** (`reports/tables/value_at_risk_by_segment.csv`; `ml_handoff_report.md` s.6.1). Actual lost revenue is measured. Modeled value at risk is predicted probability times bill, summed.

| segment | customers (% of 7,043) | actual churn | actual lost, $/month (% of $139,131) | modeled value at risk, $/month |
|---|---|---|---|---|
| All customers | 7,043 (100%) | 26.5% | 139,131 (100%) | 139,783 |
| Month-to-month | 3,875 (55.0%) | 42.7% | 120,847 (86.9%) | 122,212 |
| Fiber optic | 3,096 (44.0%) | 41.9% | 114,300 (82.2%) | 114,861 |
| Internet, no tech support | 3,473 (49.3%) | 41.6% | 110,710 (79.6%) | 111,388 |
| Month-to-month, fiber | 2,128 (30.2%) | 54.6% | 100,482 (72.2%) | 101,599 |
| Electronic check | 2,365 (33.6%) | 45.3% | 84,289 (60.6%) | 85,240 |
| Month-to-month, first 12 months | 1,994 (28.3%) | 51.4% | 68,301 (49.1%) | 68,541 |
| Month-to-month, fiber, first 12 months | 916 (13.0%) | 70.2% | 53,178 (38.2%) | 53,345 |
| Two-year contract | 1,695 (24.1%) | 2.8% | 4,165 (3.0%) | 4,069 |

The modeled total is $139,783 against $139,131 actual, a gap of +$652 (+0.5%). The score is well calibrated on average (`ml_handoff_report.md` s.6.1).

**By decile** (one tenth of customers ranked by risk; held-out test, `model_card.md` s.F).

| decile | customers | actual churn | lift vs base | cumulative share of leavers | cumulative share of lost revenue | label |
|---|---|---|---|---|---|---|
| 1 | 141 | 76.6% | 2.89 | 28.9% | 31.2% | measured |
| 2 | 141 | 58.9% | 2.22 | 51.1% | 53.8% | measured |
| 3 | 141 | 39.7% | 1.50 | 66.0% | 70.0% | measured |
| 4 | 141 | 31.2% | 1.18 | 77.8% | 80.7% | measured |
| 5 | 141 | 25.5% | 0.96 | 87.4% | 89.0% | measured |
| 10 | 140 | 0.7% | 0.03 | 100% | 100% | measured |

**By score cut-off** (threshold; held-out test, `model_card.md` s.G).

| cut-off | flagged (% of 1,409) | precision | recall | share of lost revenue | label |
|---|---|---|---|---|---|
| 0.10 | 860 (61.0%) | 40.9% | 94.1% | 94.0% | measured |
| 0.25 | 609 (43.2%) | 49.1% | 79.9% | 82.3% | measured |
| 0.50 | 298 (21.1%) | 66.8% | 53.2% | 56.1% | measured |
| 0.75 | 88 (6.2%) | 84.1% | 19.8% | 21.8% | measured |

**Smallest intervention** (`reports/tables/smallest_intervention.csv`; `ml_handoff_report.md` s.6.3). Each eligible customer is re-scored with the lever switched. Saving is the drop in risk times the current bill. No save rate, offer cost or take-up is included. All modeled.

| lever | eligible (% of base) | total modeled saving, $/month | customers for 50% of saving (% of base) | for 80% (% of base) |
|---|---|---|---|---|
| Month-to-month to one year | 3,875 (55.0%) | 48,620 | 1,060 (15.1%) | 2,072 (29.4%) |
| Paperless yes to no | 4,171 (59.2%) | 18,510 | 1,119 (15.9%) | 2,115 (30.0%) |
| Online security (bill up; unstable) | 3,498 (49.7%) | 17,360 | 1,105 (15.7%) | 2,052 (29.1%) |
| Tech support (bill up; unstable) | 3,473 (49.3%) | 14,555 | 1,078 (15.3%) | 2,018 (28.7%) |
| Electronic check to automatic transfer | 2,365 (33.6%) | 11,266 | 771 (10.9%) | 1,430 (20.3%) |

The top 1,060 contract-lever customers are 98% fiber and 84% in their first 12 months, with a mean bill of $85.10. They hold $60,324 a month of actual lost revenue, 43.4% of the total (measured, `smallest_intervention_profile.csv`). If an offer kept 10% of their leavers, about $6,030 a month ($72,400 a year) would be kept before offer cost (assumed: the 10% is chosen). Concentration is mild: each curve is smooth, with no sharp cut-off. Chart: `reports/charts/07_smallest_intervention_curve.png`.

## B6. The strategy: fix the first 90 days and the sales default before buying offers

Source for this section: `reports/executive_growth_strategy.md`.

**Internal metrics against external benchmarks** (memo s.2).

| metric | this business | external benchmark | reading |
|---|---|---|---|
| Customer churn | 26.5% per window (measured); about 9.8% a month if the window is a quarter (assumed conversion) | Frontier consumer fiber 1.41% a month, Q3 2025 (external, Lightwave) | Far worse on any reading of the window |
| Fiber vs other internet | Fiber churn 41.9% vs DSL 19.0% (measured) | Fiber satisfaction score 75 vs non-fiber 70, 2025 (external, ACSI via BGR) | Inverted: fiber should be the stickiest product |
| Fiber monthly bill | $91.50 mean (measured, $283,284 / 3,096) | Frontier fiber revenue per user $68.59 (external); Comcast 1.1 Gbps at $85 (external) | Bill sits above market; data is fictional and of another era |
| Commitment model | 55.0% month-to-month (measured) | Comcast 5-year price guarantee; Verizon 3-year lock (external) | Market sells commitment as a price promise |
| Autopay | 33.6% pay by electronic check (measured) | Comcast charges $10 more a month without autopay and paperless (external) | Market prices the non-autopay path |
| Targeting | Top 10% by risk churn at 76.0% (measured, pooled) | Uplift targeting cut churn 4.1 to 8.7 points (external, Ascarza) | High risk does not mean savable |
| Onboarding | Month-to-month fiber churn 80.5% in months 0-2 (measured) | Frontier credits install and first-bill focus (external) | The first bill is the moment to fix |

**The three value levers** (memo s.1). Ranges are before offer cost.

| lever | who | revenue kept per year | label |
|---|---|---|---|
| Commitment offer (one-year price lock), uplift-tested | 2,548 month-to-month customers scored 0.3 or higher (measured) | $96k to $203k | assumed (built on external 4.1 to 8.7 point range) |
| Fiber first-90-days programme | About 115 new month-to-month fiber customers a month (assumed) | $66k to $132k per yearly cohort | assumed |
| Autopay switch for tenured electronic-check payers | 676 month-to-month fiber customers past month 12 (measured, derived) | About $19k | assumed |
| Total | | $180k to $350k (11% to 21% of the $1.67M annual loss) | assumed |

**Recommendations by track** (memo s.4).

| track | recommendation |
|---|---|
| A. Technical | Score all customers weekly into the customer system (CRM). |
| A. Technical | Show agents the score and a scripted offer; log offer, acceptance and outcome. |
| A. Technical | Use the segment rule as a fallback if engineering is slow. |
| A. Technical | Keep a random 10% to 20% holdout (assumed); move to an uplift model after Pilot 1. |
| A. Technical | Alert if calibration gap passes 0.05 or top-20% capture falls below 45% (assumed thresholds). |
| A. Technical | Senior share of contacts within 5 points of their eligible share (assumed). |
| B. Commercial | Make a one-year price lock the default for new fiber sales. |
| B. Commercial | Run a fiber first-90-days programme. |
| B. Commercial | Offer an autopay credit to electronic-check payers past month 12; autopay as sign-up default. |
| B. Commercial | Review fiber price for value against local offers. |
| B. Commercial | Pay part of sales commission only after month 3 (assumed design). |
| B. Commercial | Review save-offer scripts against California's amended renewal law. |

**The four pilots** (memo s.5). Sizes use a two-sided 5% test with 80% power (the chance a test detects a real effect of the planned size).

| pilot | target group | design | north star | decision rules |
|---|---|---|---|---|
| 1. Commitment offer with uplift holdout | 2,548 month-to-month customers scored 0.3+ (measured) | 50/50 within score bands; about 1,274 per arm detects a 5.5-point drop from 55% (assumed calculation); 90 days, 6-month follow-up | Churn, treatment minus holdout, by band | Day 30 kill if take-up under 5%; day 60 re-target any band with higher churn; day 90 scale if gap is 4+ points and margin exceeds credit |
| 2. Fiber first-90-days concierge | New fiber sign-ups, about 115 a month (assumed) | 50/50; about 345 per arm detects only a 10-point drop from 80% (assumed calculation) | 90-day survival | Day 30 fix delivery if under 70% of calls connect; day 90 scale if churn falls 5+ points, kill if under 2 |
| 3. Autopay switch | 676 tenured electronic-check payers (measured base) | 338 per arm; churn can show only an 11-point effect (assumed calculation) | Autopay enrolment | Day 30 kill if enrolment under 10%; day 90 scale if 25%+ and churn does not rise |
| 4. Tech support trial | 1,796 month-to-month fiber customers without support (measured base) | 898 per arm detects about 7 points from 57% (assumed calculation) | 90-day churn, treatment minus control | Day 30 pause if wait times breach guardrail; day 90 scale if churn falls 4+ points, kill if under 1 |

**Threshold economics** (memo s.3.3; all assumed except counts). The memo assumes $5 contact cost, a $60 credit to 30% of contacts, a 10% save rate, 60% margin and 12 months kept. On those assumptions, net value per held-out campaign peaks near a 0.5 cut-off ($4,189) and is flat from 0.4 to 0.5. At a 5% save rate, every cut-off loses money (assumed).

**Prioritisation** (memo s.6).

| initiative | impact | confidence | time | wave |
|---|---|---|---|---|
| One-year price lock as default for new fiber sales | High | Medium | 4-6 weeks | 1 |
| Retention-desk compliance and offer log | Low direct | High | 2-4 weeks | 1 |
| Fairness and senior-share guardrail | Risk avoidance | High | 2 weeks | 1 |
| Pilot 2: fiber first-90-days | High | Medium | 6-8 weeks | 2 |
| Pilot 1: commitment offer | Med-High | Medium | 4-6 weeks | 2 |
| Pilot 4: tech support trial | Medium | Low-Medium | 4 weeks | 2 |
| Pilot 3: autopay | Low | Medium | 3 weeks | 2 |
| Weekly score in CRM with holdout | Medium | Medium | 6-10 weeks | 2 |
| Event, quality and price telemetry | Enabler | High | 3-6 months | 3 |
| Fiber price-for-value review | Potentially High | Low | 3 months | 3 |
| Home and mobile bundle | High if feasible | Low | 6-12 months | 3 |

## B7. The agent dialogue: nine questions in two rounds shaped all four pilots

The growth strategist sent nine questions to the statistician by direct message (`reports/agent_dialogue.md`). Answers are in `reports/ml_followups.md`. Method: group counts and means, no modeling. Questions are verbatim.

| round | question (verbatim) | answer (from `ml_followups.md`) | memo section | what changed |
|---|---|---|---|---|
| 1 | "(Memo s.5 Pilot 2, autopay) Month-to-month fiber customers split by payment method (electronic check / mailed check / bank transfer auto / credit card auto): count, churn rate, mean monthly bill." | Electronic check 1,307 at 60.4% ($87.18); bank transfer 327 at 45.6% ($88.25); credit card 293 at 41.6% ($87.97); mailed check 201 at 50.7% ($82.59) | s.1 lever 3, s.3.1, Pilot 3 | Confirmed the gap behind the autopay pilot |
| 1 | "(Memo s.3, contract selection check) Churn rate and count for one-year and two-year contract customers with tenure 0-12 months, split fiber vs DSL." | One-year DSL 42 at 16.7%; one-year fiber 7 at 28.6%; two-year DSL 18 at 0.0% | none | Nothing: groups of 7 to 42 are too small; selection caveat stays unquantified |
| 1 | "(Memo s.5 Pilot 3, fiber onboarding/support) Month-to-month fiber customers with vs without TechSupport: count, churn rate, mean monthly bill." | No support 1,796 at 57.5% ($85.49); with support 332 at 38.9% ($95.28) | s.3.1, Pilot 4 | Gave Pilot 4 its trigger and its 1,796-customer group |
| 1 | "(Memo s.3 targeting) Within the top 1,060 contract-lever customers (smallest_intervention_profile): share paying by electronic check, share without TechSupport, share SeniorCitizen." | Electronic check 61.7%; no tech support 87.2%; senior 25.5% (base: 33.6%, 71.0%, 16.2%) | Pilot 4 | Only the 87.2% was used |
| 1 | "(Memo s.3 threshold economics) Held-out test at cutoffs 0.30, 0.40, 0.50, 0.60: customers flagged, true leavers flagged, summed monthly bill of flagged leavers, summed monthly bill of flagged stayers." | 0.3: 531 flagged, 286 leavers; 0.4: 422, 246; 0.5: 299, 200; 0.6: 197, 142 | s.3.3 | Built the threshold table and the 0.4 to 0.5 cut-off |
| 1 | "(Memo s.3 fairness guardrail) SeniorCitizen share in the pooled top-20% risk group vs the whole base." | 30.7% (433 of 1,409) vs 16.2% (1,142 of 7,043) | s.3.2, Track A item 7, Pilot 1 | Added the "senior share within 5 points" guardrail |
| 2 | "(Memo s.5 Pilot 2 sizing) Month-to-month fiber, tenure 0-12 (the 916): split electronic check / mailed check / automatic (bank+card): customers, churn rate, mean bill." | Automatic 162 at 72.2%; electronic check 631 at 71.2%; mailed 123 at 62.6% | s.1 lever 3, s.3.1, Pilot 3 | Autopay lever retargeted to customers past month 12 (676 customers, 50.3% vs 33.6%, derived) |
| 2 | "(Memo s.5 Pilot 3 onboarding) Month-to-month fiber churn by tenure band 0-2, 3-6, 7-12 months: customers, churn rate." | 0-2: 344 at 80.5%; 3-6: 275 at 66.2%; 7-12: 297 at 62.0%; 13+: 1,212 at 42.8% | s.1 thesis, s.1.1, s.3.1, Pilot 2, lever 2 | 80.5% became the core of the thesis; basis of the assumed 115 a month intake |
| 2 | "(Memo s.3/s.5 Pilot 1 targeting) Month-to-month customers by pooled score band <0.3, 0.3-0.5, 0.5-0.7, >=0.7: customers, actual churn rate, mean bill." | Under 0.3: 1,327 at 18.5%; 0.3-0.5: 1,042 at 37.3%; 0.5-0.7: 908 at 60.1%; 0.7+: 598 at 79.3% | s.1 lever 1, s.3.1, Pilot 1 | Pilot 1 target became 2,548 customers scored 0.3+; set the $96k-$203k sizing |

All answer numbers are measured. Four questions named a pilot number that later changed; the dialogue log records the final pilot.

**Notebook review outcome** (`reports/notebook_review.md`).

| notebook | gaps found (round 1) | fixed | found in round 2 | remaining |
|---|---|---|---|---|
| 01 exploration | 10 | 10 | 4 (A to D) | 2 minor: Cramér's V p-values without intervals (disclosed as descriptive); some cells with only an implied "how it works" |
| 02 feature engineering and 03 modeling | 8 | 8 | 8 | 0 reported by the author; no third review run |

Each fix round rebuilt and re-ran the notebooks with 0 errors. Test AUC stayed at 0.84742 and the chosen model stayed GLM. The orchestrator allowed one extra formatting-only fix round per notebook set; this broke the one-round rule and is recorded.

---

# Part C. Checks and limits

## C1. Consistency check

**Numbers in two or more reports.**

| number | where it appears | verdict |
|---|---|---|
| 7,043 customers; 1,869 leavers; 26.5% | findings, model card, handoff, memo | Agree |
| $139,131 lost of $456,117 (30.5%); $1,669,570 a year | findings, handoff, memo | Agree |
| 916 customers, 70.2%, $53,178, 38.2% | findings, handoff, memo | Agree |
| Test AUC 0.847 (0.84742) | model card, handoff, notebook review | Agree |
| Top-20% capture 53.8% held-out | model card, handoff, memo | Agree |
| Top-20% capture, explorer 52% vs model 53.8% | findings chart 14, handoff s.7 | Different bases (in-sample vs held-out); handoff explains; held-out is right |
| Segment count 17 vs 18 | exploration notebook text | Fixed to 17 in the notebook |
| Flagged at 0.5 cut-off: 298 | model card s.G | **Discrepancy**: memo and follow-ups report 299 flagged and 200 leavers at 0.5. Likely "above" vs "at or above"; not verified. |
| Add-on lever swing "5 to 13 times" (4.6 and 12.7) | model card, handoff | **Minor discrepancy**: notebook review says the ratios are "about 5 and 14". |
| 40%-50% band adds 8.2% of lost revenue | handoff s.6.2 | **Minor rounding**: decile table gives 89.0% minus 80.7% = 8.3 points. |
| "Best nested AUC" for GLM | model card summary | **Wording**: GLM and XGBoost tie at 0.8503; GLM won on the simplicity rule. |
| Engineered features: 12 vs 10 | notebook review, model card | Agree once explained: 12 built, 10 kept (`n_streaming`, `price_resid` dropped, `features.md`). |
| Tech support gap 42% vs 15% and 41.6% vs 15.2% | findings, handoff | Agree (rounding) |
| PaymentMethod third by Cramér's V, tenth by permutation | findings, model card | Not a conflict: single-column link vs the model's use alongside overlapping columns |

**Strategy claims with no supporting number in the handoff report.** These come from the follow-ups, from exploration charts, or from the strategist's own derivation.

| claim | source the memo gives | label in memo |
|---|---|---|
| Month-to-month fiber churn 80.5% in months 0-2 | Follow-ups R2-Q2 | measured |
| 676 tenured electronic-check customers, 50.3% vs 33.6% | derived from R1-Q1 and R2-Q1 | measured, derived |
| 2,548 customers scored 0.3+, 55.3% churn, $76.41 bill | derived from R2-Q3 | measured, derived |
| One-year fiber churn 19% vs 55% month-to-month | exploration chart 03 | measured |
| Fiber mean bill $91.50 | derived from handoff s.6.1 ($283,284 / 3,096) | measured |
| Tech support 57.5% vs 38.9% | Follow-ups R1-Q3 | measured |
| About 115 new fiber customers a month | from 344 customers in months 0-2 | assumed |
| All dollar ranges for levers, threshold net values, pilot sizes | memo assumptions | assumed |

**Benchmarks the memo marked unverified** (memo s.2, s.7). None is used for any figure.

| benchmark | why unverified |
|---|---|
| S&P Kagan 1.25% average monthly churn (Q3 2025) | search summary only; page returned 403 |
| AT&T Q1 2025 postpaid phone churn 0.83% | search summary only; pages returned 403 |
| Telenor uplift case (11-fold return gain) | could not be fetched |
| Broadband save-rate and acquisition-cost benchmarks | none found |
| AT&T churn link to reduced autopay discounts | author's commentary, marked "not proven" |

## C2. Limitations and failure modes

Merged from `model_card.md`, `ml_handoff_report.md` s.7, `findings.md` and the memo.

| # | limitation | effect | source |
|---|---|---|---|
| 1 | No causality: snapshot data; customers chose contract and payment | The -18 point contract effect may be mostly selection | handoff s.7 item 1 |
| 2 | No time axis: one quarter, no dates | No trend; cannot show the model holds next quarter; window length unknown changes the benchmark gap sevenfold | handoff s.7 item 2; memo s.6 |
| 3 | Tenure and billing may be recorded at exit | Could inflate the model and the 0-2 month cliff | handoff s.7 item 3; memo s.6 |
| 4 | Weak ranking inside segments | Less useful for choosing who to call within the target group | handoff s.7 item 4 |
| 5 | Price and product cannot be separated | No price effect can be measured; add-on sizing unusable | handoff s.7 item 5 |
| 6 | Small test: 374 leavers, about +/-5 points | Single-segment numbers are fragile | model card |
| 7 | No economics: margin, offer cost, save rate, lifetime | Dollars are revenue, not profit; every return is assumed | handoff s.7 item 7 |
| 8 | Fictional single-company sample | Conclusions describe this data, not a real firm | findings; handoff s.7 item 8 |
| 9 | Fairness: seniors are 30.7% of the top-20% risk group vs 16.2% of the base | Offers by age are not appropriate | handoff s.7 item 9; follow-ups R1-Q6 |
| 10 | Test rows reused for drivers and what-ifs after model choice | Driver and what-if numbers are noisy; no decision depended on them | handoff s.7 |
| 11 | Risk-based targeting can push stayers to leave ("sleeping dogs") | Offers could backfire | memo s.1.2, s.4 |
| 12 | Save offers at the cancel step face California rules | Legal risk | memo s.2 |

## C3. Instrumentation gaps, in priority order

| priority | data to add | what it fixes | source |
|---|---|---|---|
| 1 | Offer log: assignment, take-up, credit paid, outcome; with a random holdout | Measures the save rate and any causal effect | handoff s.7 item 1; memo Track A |
| 2 | Event dates: sign-up, contract change, cancel request, churn | Trend, time-based testing, exit-timing question | handoff s.7 items 2-3 |
| 3 | Fiber quality: install date, missed installs, outages, speed tests, fault tickets | Explains why fiber leaves | memo Track A item 5 |
| 4 | First-bill data: bill vs quoted price, billing calls in month one | Tests the first-bill cliff | memo Track A item 5 |
| 5 | Price history: list price, discounts, promo end dates | Separates price from product | handoff s.7 item 5 |
| 6 | Margin and offer cost from finance | Turns revenue into profit | handoff s.7 item 7 |
| 7 | More customers or periods | Narrows intervals | handoff s.7 item 6 |

---

# Part D. Appendix

## D1. Glossary

| term | plain meaning |
|---|---|
| Annualised churn | A monthly churn rate turned into a yearly one |
| AUC (area under the curve) | Chance a random leaver is scored above a random stayer; 0.5 is a coin flip |
| Autopay | Automatic bank or card payment each month |
| Baseline | A simple method the model must beat |
| Bootstrap interval | Range from re-drawing the same customers many times; shows how much a number could move by luck |
| Break-even save rate | Share of flagged leavers who must be kept for a campaign to cover its cost |
| Brier score | Average squared error of a predicted probability; lower is better |
| Calibration | Whether customers scored 40% leave about 40% of the time |
| Churn | A customer leaving in the observation window |
| Controllable / semi-controllable / structural | The business can change it quickly / slowly / not at all |
| Counterfactual (what-if) | Re-scoring a customer with one column changed; an association, not a cause |
| Cramér's V | Strength of the link between two categories, 0 (none) to 1 (perfect) |
| CRM | The customer system that holds account records |
| Cross-validation | Fit on part of the training data, score on the rest, repeat |
| Cumulative gain | Share of leavers or lost revenue reached as more customers are contacted, riskiest first |
| Decile | One tenth of customers ranked by risk; decile 1 is the riskiest |
| ECE (expected calibration error) | Average gap between predicted and actual churn rates |
| Elastic net | Logistic regression with a penalty that shrinks weights; `C` sets strength, `l1_ratio` the mix |
| Evidence label | measured, modeled, external or assumed |
| False positive / false negative | A stayer flagged / a leaver missed |
| Fiber | Fiber-optic internet service |
| GLM | Generalised linear model; here, logistic regression |
| Gross margin | Revenue minus direct cost of service, as a share of revenue |
| Guardrail metric | A metric that must not get worse during a test |
| Held-out test set | 1,409 customers locked away until the end and scored once |
| Holdout | A random group that gets no offer, used for comparison |
| Leakage | Information in an input that would not be known before the outcome |
| Lift | A group's churn rate divided by the overall rate |
| Logistic regression | A model that turns a weighted sum of inputs into a probability |
| Minimum detectable effect | The smallest change a test of a given size can reliably detect |
| Month-to-month | A plan with no fixed term |
| Nested cross-validation | Tuning inside each outer fold, so the reported score is not tuned on its own data |
| North star metric | The single outcome a pilot is judged on |
| Odds ratio | Odds of leaving in one group divided by odds in another; 1 means no difference |
| Optuna | A tool that searches parameter settings over many trials; pruning stops weak trials early |
| Out-of-fold score | A score from a model that never saw that customer |
| p-value | Chance of a gap this large by luck alone if there were no real link |
| Parameter importance | Share of the tuning score's variation explained by each setting |
| Permutation importance | AUC lost when one column is shuffled |
| Persuadable | A customer who would leave without an offer but stays with one |
| Pilot (randomised) | A test where customers are assigned to offer or no offer by chance |
| Power (80%) | Chance a test detects a real effect of the planned size |
| Precision / recall | Share of flagged who leave / share of all leavers who are flagged |
| Price lock | A promise of a fixed price for a set term |
| Revenue per user (ARPU) | Average monthly revenue per customer |
| Save rate | Share of targeted would-be leavers kept by an offer |
| Selection bias | A gap caused by who chose an option, not by the option itself |
| SHAP | A method that splits each prediction into per-column contributions |
| Sleeping dog | A customer who would have stayed but leaves because of an offer |
| Standard deviation (SD) | Typical spread of a number around its average |
| Threshold (cut-off) | The score above which a customer is contacted |
| Top-20% capture | Share of lost revenue held by the 20% of customers scored riskiest |
| Uplift model | A model that predicts how much an offer changes a customer's chance of leaving |
| Value at risk | Predicted churn probability times monthly bill, summed |
| XGBoost, LightGBM, CatBoost, random forest | Model families built from many decision trees |

## D2. Chart manifest

| file | what it shows | key takeaway |
|---|---|---|
| `reports/charts/01_churn_by_contract.png` | Churn rate by contract type, with group sizes | Month-to-month 43% (n=3,875) vs one year 11% and two year 3% |
| `reports/charts/02_churn_by_tenure.png` | Churn rate by months with the company | 53% in months 0-6 falls to 10% after 4 years |
| `reports/charts/03_contract_by_internet_heatmap.png` | Churn by contract and internet type | Month-to-month is riskiest in every internet type; fiber 55% |
| `reports/charts/04_candidate_groups_revenue.png` | Share of customers vs share of lost revenue for 7 groups | Month-to-month year-one customers: 28% of customers, 49% of lost revenue |
| `reports/charts/05_model_evaluation_panel.png` | ROC, precision-recall, calibration, decile lift, cumulative capture, thresholds | AUC 0.847; well calibrated; top 20% holds 54% of lost revenue |
| `reports/charts/06_driver_importance.png` | Permutation and SHAP importance, coloured by driver type | InternetService and MonthlyCharges lead; Contract is the top controllable |
| `reports/charts/07_smallest_intervention_curve.png` | Share of modeled saving vs share of eligible customers treated, five levers | About a quarter to a third of each group gives half the saving; no sharp cut-off |
| `reports/charts/08_counterfactual_levers.png` | What-if change in predicted churn, with intervals | Contract -18 points; add-on rows depend on the bill assumption |

## D3. Web sources (from `executive_growth_strategy.md` s.7)

| URL | one-line summary |
|---|---|
| https://lightwaveonline.com/home/article/55326989/frontiers-ongoing-fiber-expansion-raises-customer-retention | Frontier Q3 2025 fiber churn 1.41% a month; revenue per user $68.59; install and first-bill focus |
| https://bgr.com/2146659/internet-provider-ranks-highest-customer-satisfaction-at-t/ | 2025 ACSI: fiber 75 vs non-fiber 70; complaints on installs, support, speeds |
| https://lightwaveonline.com/broadband/article/55088085/acsi-data-shows-customers-prefer-fiber | 2024 ACSI: AT&T Fiber 80, Verizon Fios 77 |
| https://www.engadget.com/big-tech/comcast-rolls-out-a-five-year-price-guarantee-for-new-internet-customers-173421830.html | Comcast five-year price guarantee; $10 more without autopay and paperless |
| https://www.lightwaveonline.com/broadband/article/55284110/long-term-price-locks-signal-an-evolving-competitive-landscape | Verizon three-year price lock |
| https://thedesk.net/2026/07/parks-broadband-churn-tracker-q1-2026/ | 280,000 cable broadband disconnects Q1 2026; over a quarter of households bundle |
| https://broadbandbreakfast.com/charter-reports-177-000-broadband-sub-loss-in-q4.md | Charter lost 177,000 subscribers Q4 2024; bundle churn "much lower" |
| https://ama.org/press-releases/eva-ascarza-receives-2023-weitz-winer-odell-award-for-retention-futility | Ascarza: uplift targeting cut churn 4.1 to 8.7 points; risk targeting sometimes raised churn |
| https://www.androidheadlines.com/2025/10/att-faces-customer-retention-problem-despite-strong-subscriber-growth.html | AT&T churn up 14 basis points; author links it to autopay discounts (not proven) |
| https://www.jdsupra.com/legalnews/ftc-click-to-cancel-rule-on-hold-but-2056488 | FTC click-to-cancel on hold; California renewal law from 1 July 2025 |
| https://www.bain.com/insights/telco-fiber-networks-if-you-build-it-will-they-come/ | Fiber returns need about 35% uptake |

## D4. Files produced

**Notebooks (read these first).**

| file | what it shows |
|---|---|
| `notebooks/01_exploration.ipynb` | Data quality audit, cleaning, ten pre-registered hypotheses, churn by every column and pair, concentration and candidate groups |
| `notebooks/02_feature_engineering.ipynb` | Twelve engineered features with formulas, evidence and keep/drop verdicts (10 kept) |
| `notebooks/03_modeling.ipynb` | Baselines, five model families, Optuna nested tuning, model choice, held-out test, drivers and what-if levers |

**Reports.**

| file | what it is |
|---|---|
| `reports/final_report.md`, `reports/final_report.html` | This report |
| `reports/exploration/findings.md`, `hypotheses.md`, `data_dictionary.md` (+ `.csv`), `quality_audit.md`, `cleaning_log.md`, `handoff_to_modeling.md` | Exploration outputs |
| `reports/exploration/clean.parquet` | Cleaned table, 7,043 rows, 30 columns |
| `reports/exploration/charts/` | 16 exploration charts |
| `reports/modeling/model_card.md`, `tuning.md`, `features.md`, `feature_list.json` | Modeling outputs |
| `reports/modeling/features.parquet`, `scores.csv` | Feature table; out-of-fold and held-out scores |
| `reports/modeling/tables/` | 17 tables: baselines, comparison, Optuna trials, test metrics, deciles, thresholds, drivers, levers, segments |
| `reports/modeling/charts/` | 26 modeling charts |
| `reports/ml_handoff_report.md` | Statistician's handoff |
| `reports/customer_risk_scores.csv` | Per-customer risk score, decile, flags, value at risk (7,043 rows) |
| `reports/tables/` | Value at risk, risk-only targeting, smallest intervention and profile, all-customer deciles, chart audit |
| `reports/charts/01` to `08` | Eight selected charts |
| `reports/executive_growth_strategy.md` | Strategy memo |
| `reports/ml_followups.md`, `reports/agent_dialogue.md` | Follow-up answers and dialogue log |
| `reports/notebook_review.md` | Notebook review log |

**Models and code.**

| file | what it is |
|---|---|
| `models/churn_driver_diagnostic_model.joblib`, `models/final_config.json` | Final GLM pipeline and its settings |
| `models/optuna_glm.db`, `optuna_xgb.db`, `optuna_rf.db`, `tuning_*.json` | Saved Optuna studies and tuning results |
| `src/pipeline.py` | Train, evaluate and predict (`--train`, `--evaluate`, `--predict`) |
| `src/build_notebook_01.py`, `02.py`, `03.py`, `nbkit.py` | Notebook builders |
| `src/explore_utils.py`, `features.py`, `model_utils.py`, `model_card_cell.py`, `notes_03.py` | Helper code |
