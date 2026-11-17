# Pricing and Promotion: Final Report
**Project:** 05-pricing-simulator | **Date:** 16 Nov 2026 | **Author:** report-writer
**Sources:** every number cites its file and section. Short forms: EXP = `reports/exploration/findings.md`; DD = `reports/exploration/data_dictionary.md`; HTM = `reports/exploration/handoff_to_modeling.md`; MC = `reports/modeling/model_card.md`; TUN = `reports/modeling/tuning.md`; HR = `reports/ml_handoff_report.md`; FU = `reports/ml_followups.md` (R1/R2 = round, Q = question); MEMO = `reports/executive_growth_strategy.md`; DIA = `reports/agent_dialogue.md`; NBR = `reports/notebook_review.md`.

**Evidence labels.** *measured* = counted directly from the data. *modeled* = output of a statistical model; an association, not proof of cause. *external* = from a cited web source. *assumed* = an analyst's estimate or arithmetic on other figures.

**Corrections applied throughout.** The statistician corrected several handoff numbers after the fact (FU R1, "CORRECTIONS"). This report uses the corrected values only:
- Revenue is $9.56M a year, not $1.49B. The $1.49B was an arithmetic error.
- VISITS counts shopping trips that included the product. It is an outcome, not store traffic.
- The exploration price slopes (−1.44, −1.16, −0.34, −0.38) could not be reproduced.
- The cleaned file holds 13,693 duplicate rows.
- Exploration finding F2 ("Bag Snacks and Cereal rarely discounted") is wrong.
- Exploration finding F4 ("~20 of 55 products make 80% of revenue") is corrected to 25 of 55.

---

# Part A. The answer in plain language

## The question the client asked
A grocery chain sets one price and promotion rule per aisle. Its category managers asked three things (`problem_description.md`):
1. How price-sensitive is each product?
2. How much do weekly-ad features and in-store displays add beyond the price cut?
3. Which products can take a price increase without losing profit?

## The answer
The data cannot yet answer the first and third questions reliably. Every method gives a different price sensitivity, and the econometric model gives the wrong sign. The demand forecast is accurate, but only because one input (VISITS) nearly duplicates the sales it predicts. No cost data exists, so profit cannot be calculated. What the data does show is that discounting is heavy and probably loses money. About 37% of revenue sells on discount, and no category's average discount week recovers its markdown at an assumed 30% margin. The recommendation is promotion discipline now and store-level price tests next, not price cuts.

## The numbers that matter

| # | Number | Label | Source | What it means for the decision |
|---|---|---|---|---|
| 1 | **$9.56M revenue a year** across 4 categories, 55 products, 77 stores ($28.69M over 156 weeks) | measured | FU R1 Q1 | The real money at stake is small. The value is the method, if it scales chain-wide. |
| 2 | **36.8% of revenue sold at a discount**, about **$1.0M a year in markdown** (10.5% of category revenue) | assumed (arithmetic on measured inputs) | MEMO §3.1, §3.2 | Discounting is the biggest controllable cost in these categories. |
| 3 | **0 of 4 categories break even** on an average discount week at an assumed 30% margin; 1 of 4 at 40% | assumed | MEMO §3.2 | Cutting or re-funding weak promotions is the first lever. |
| 4 | **Price sensitivity ranges from −0.2 to −2.7** depending on method; the econometric model gives **+0.09 to +0.48** (wrong sign) | measured (association; not verified) and modeled | FU R1 Q3; MC "Price elasticity" | No product-level price move can be justified from history alone. Tests are needed. |
| 5 | Forecast error **8.5% of units** on 26 unseen weeks, but driven by VISITS, an outcome; simulated 10% price cut adds only **+0.8% to +3.2% units**, a lower bound | modeled | MC "How good it is"; FU R1 Q2 | The simulator must not be used for price decisions until it is rebuilt without VISITS. |

## What should happen next

| # | Action | Owner | When | Source |
|---|---|---|---|---|
| 1 | Freeze the simulator and the "cut Bag Snacks and Pizza prices" and "target Value stores" advice. | Chief merchant | Week 0 | MEMO §4 B1 |
| 2 | Put a break-even check on every discount event and cap retailer-funded depth at 20%. | Category managers, finance | Weeks 1–12 | MEMO §4 B2, B4 |
| 3 | Load unit cost and vendor funding per product, and remove the 13,693 duplicate rows. | Finance, IT, data science | Weeks 0–6 | MEMO §4 A1, A3 |
| 4 | Run a store-randomised promotion holdout in Frozen Pizza and Cereal (38 test vs 39 control stores, 12 weeks). | Data science, category managers | Weeks 4–20 | MEMO §5 Pilot 1 |
| 5 | Run an everyday-price ladder (+3% and +5%) on the top 10 Cereal products to measure true price sensitivity. | Pricing team | Weeks 4–20 | MEMO §5 Pilot 2 |

## What is uncertain
- All margin and break-even figures rest on assumed 30% and 40% margins; no cost or vendor-funding data exists.
- True price sensitivity per product is unknown; only randomised store tests can measure it.
- The data is from 2009–2011 and the external benchmarks are from 2016–2026, so gaps are directional only.

---
# Part B. How we got there

## B1. The data: 538,435 store-product-weeks, with 13,693 duplicates found late

**What it is.** Dunnhumby "Breakfast at the Frat": weekly sales and promotion records (`problem_description.md`). One row is one store, one product and one week (HTM "Clean data").

| Item | Value | Label | Source |
|---|---|---|---|
| Stores | 77 (43 Mainstream, 15 Upscale, 19 Value) | measured | FU R2 Q1 |
| Products [UPC: one product at one pack size] | 55 (Bag Snacks 15, Cold Cereal 15, Frozen Pizza 12, Oral Hygiene 13) | measured | FU R2 Q1 |
| Weeks | 156 (week ending 14 Jan 2009 to 4 Jan 2012) | measured | DD |
| Raw rows | 538,643 | measured | `cleaning_log.md` |
| Clean rows | 538,435 (208 dropped for missing price or base price) | measured | `cleaning_log.md` |
| Unique store-product-weeks | 524,742; **13,693 duplicate rows** remain in the clean file | measured | FU R1 header |
| Source | GitHub mirror of the dunnhumby workbook, same file size as the original (34,051,636 bytes) | measured | `problem_description.md` |

**How it was checked and cleaned** (`quality_audit.md`, `cleaning_log.md`).

| Check | Count | Action |
|---|---|---|
| Missing PRICE | 23 rows | Dropped |
| Missing BASE_PRICE [regular everyday price] | 185 rows | Dropped |
| PRICE = 0 | 1 row | LOG_PRICE set to blank |
| PRICE above BASE_PRICE | 4,906 rows (0.93%) in the audit; 6,264 rows (1.2%) per FU R1 Q7 | Kept as price-increase weeks |
| Several promotion flags on one row | 23,414 rows | One label by priority: Feature+Display, Feature, Display, TPR, None |
| UNITS = 0 | 5 rows | Kept |
| Full-row duplicates | Audit reported 0; FU R1 later found 13,693 duplicate keys | Not removed; MEMO §4 A1 asks for removal |

**What was excluded from modeling and why** (HTM "Columns to EXCLUDE").

| Column | Reason |
|---|---|
| SPEND | Price times units; it would leak [give away] the answer |
| DESCRIPTION, MANUFACTURER, STORE_NAME, city | Text labels; product and store codes used instead |
| HHS [unique households] | Correlation [how closely two numbers move together, −1 to 1] of 0.99 with VISITS |
| WEEK_END_DATE | Replaced by week-of-year and year |

**Columns added.** Discount % (`(BASE_PRICE − PRICE) / BASE_PRICE × 100`), promotion type, log of units, log of price, and units per visit [UPV: units ÷ trips that included the product] (DD "Derived Columns").

**Data limits.** No cost, margin, vendor-funding, competitor-price or store-traffic data (EXP "What could not be checked"; HR §7).

## B2. What exploration found: five findings, three of which were later corrected

Each finding below shows the original claim, the corrected position and its reliability. The exploration charts are in `reports/charts/`.

| # | Original finding (EXP) | Corrected position | Label | Reliability now | Chart |
|---|---|---|---|---|---|
| F1 | Every category loses units when price rises. Slopes −1.44 Bag Snacks, −1.16 Frozen Pizza, −0.34 Cereal, −0.38 Oral Hygiene (chart 01). | Direction holds in pooled data. The sizes could not be reproduced; three other methods rank the categories differently (FU R1 Q3). | measured (association; not verified) | Weak for size, moderate for direction | `01_demand_curves_by_category.png` |
| F2 | Bag Snacks and Cereal are rarely discounted; Pizza and Mouthwash in over half of weeks. | **Wrong.** All four categories are discounted in 23–29% of rows. The 0% median was a median artifact (FU R1 Q4). | measured | Original: not reliable | `02_discount_depth_by_category.png` |
| F3 | Feature ads add the most lift; median units per visit about 1.14 with Feature+Display vs 1.00 with no promotion (HR §3), p < 0.001. | Per-trip lift is only 0–15%. Total units are 2–4 times higher in promoted weeks, mainly from more trips (FU R1 Q5). Retailer chose the weeks, so lift is inflated. | measured | Moderate; selection-biased | `03_promotion_lift_by_type.png` |
| F4 | ~20 of 55 products make 80% of revenue. | **Corrected to 25 of 55 (45%).** Top 5 products hold 27.9% (FU R2 Q6). | measured | Strong | `05_revenue_concentration.png` |
| F5 | Value stores respond more to promotions (lift 1.75 vs 1.65 Upscale, HR §3). | **Does not hold within any category.** Value is highest in none of four (FU R1 Q6). It was a product-mix effect. | measured | Original: not reliable | `04_promo_lift_by_store_segment.png` |

**Within-category promotion lift by store tier** (median promoted ÷ non-promoted units; measured; FU R1 Q6).

| Category | Mainstream | Upscale | Value |
|---|---|---|---|
| Bag Snacks | 1.80 | 1.56 | 1.75 |
| Cold Cereal | 2.05 | 2.00 | 1.78 |
| Frozen Pizza | 2.83 | 2.43 | 2.50 |
| Oral Hygiene | 1.67 | 2.00 | 1.50 |

**Statistical tests** (`hypotheses.md`; Mann-Whitney U [a test comparing two groups by rank]; rank-biserial r [effect size, 0 = no effect, 1 = full separation]).

| Test | Result | Label |
|---|---|---|
| H1 promoted vs not | median 16 vs 9 units; r = −0.254 (95% CI −0.325 to −0.176) | measured |
| H2 Feature+Display vs Feature only | median 38 vs 17 units; r = −0.391 | measured |
| H3 Cereal vs Mouthwash slope | −0.497 vs −0.448; no p-value reported | measured (association; not verified) |
| H4 Upscale vs Value baseline | median 11 vs 7 units; r = −0.212 | measured |
| H6 Mouthwash promoted vs not | median 5 vs 3 units; r = −0.348 | measured |

**Collinearity [two inputs carrying the same information].** VISITS and HHS correlate at 1.00 on the heat map; VISITS and UNITS at 0.99 (chart `exploration/charts/7E_correlation_matrix.png`; FU R1 Q2 gives r = 0.987).

## B3. How the model was built: accurate on unseen weeks, but for the wrong reason

**What it predicts.** Weekly units for one product in one store (MC "What the model predicts").

**How it was tested.** The last 26 weeks (88,751 rows) were held out [kept unseen until the end]. The first 130 weeks (449,684 rows) trained the model (HR §8). Models were compared with 5-fold expanding-window cross-validation [CV: train on earlier weeks, score on the next block, repeat five times] (MC "How it was tested").

**What was compared** (`modeling/tables/final_model_comparison.csv`; RMSE_log [typical error on the log scale; 0.10 is roughly ±10% in units]; modeled).

| Model | CV RMSE_log (mean) | Std. dev. |
|---|---|---|
| LightGBM, tuned | 0.1043 | 0.0040 |
| XGBoost, tuned | 0.1046 | 0.0041 |
| CatBoost, default | 0.1053 | 0.0044 |
| LightGBM, default | 0.1063 | 0.0038 |
| Random Forest | 0.1069 | 0.0042 |
| XGBoost, default | 0.1070 | 0.0041 |
| Ridge with fixed effects | 0.4132 | 0.0033 |
| OLS with fixed effects | 0.4320 | 0.0343 |

LightGBM, XGBoost, CatBoost and Random Forest are tree models [many small decision rules added together]. Ridge and OLS are regressions [straight-line formulas]; fixed effects [a separate baseline for each store and product] absorb level differences. Chart: `08_model_comparison.png`.

**How it was tuned.** Optuna [software that tries many settings and learns which work] ran trials [one full test of one set of settings] for the two best families (TUN).

| | LightGBM | XGBoost |
|---|---|---|
| Trials completed | 60 (2 more stopped early) | 60 (6 more stopped early) |
| Best CV RMSE_log | 0.1043 | 0.1046 |
| Most important setting | colsample_bytree [share of inputs each tree may see], 0.42 | reg_alpha [penalty that pushes weak inputs to zero], 0.34 |
| Second | reg_alpha, 0.15 | n_estimators [number of trees], 0.22 |

The history charts show most gains came in the first 10–15 trials; later trials moved the error by about 0.001 (`modeling/charts/optuna_lgb_history.png`, `optuna_xgb_history.png`). Tuning improved LightGBM from 0.1063 to 0.1043 (modeled; table above).

**Why LightGBM won.** It had the lowest CV error, narrowly ahead of tuned XGBoost (MC "Selected model"). Ridge was kept separately only to estimate price sensitivity.

**How good it is on the held-out 26 weeks** (MC "Test set performance"; modeled).

| Metric | LightGBM | Ridge FE | Plain meaning |
|---|---|---|---|
| RMSE_log | 0.111 | 0.419 | LightGBM: about ±12% in units (MC) |
| R² [share of variation explained] | 0.989 | 0.836 | |
| MAPE [average miss as % of actual units] | 8.5% | 53.5% | |

Baselines: category average RMSE_log 0.848; simple Ridge 0.749 (MC).

**What that means.** The accuracy is real but not useful for pricing. VISITS counts trips that bought the product, so it nearly equals the target (FU R1 Q2). The model is reading sales to predict sales.

**Where it is weaker** (`modeling/tables/performance_by_category.csv`; modeled).

| Category | Test rows | MAPE | R² |
|---|---|---|---|
| Frozen Pizza | 20,532 | 10.5% | 0.978 |
| Bag Snacks | 22,088 | 10.2% | 0.983 |
| Oral Hygiene | 20,179 | 7.1% | 0.972 |
| Cold Cereal | 25,952 | 6.5% | 0.990 |

Feature+Display weeks are only 4.5% of rows (24,078), so their effect is uncertain (MC "Known weaknesses").

## B4. What drives the predictions: one outcome variable dominates; price barely registers

**SHAP importance** [SHAP: how much each input moved each prediction, averaged] (`modeling/tables/shap_importance.csv`, `driver_importance.csv`; modeled).

| Driver | Mean SHAP | Can the business change it? |
|---|---|---|
| VISITS (trips that included the product) | 0.849 | No. It is an outcome, not a lever (FU R1 Q2). Model card lists it as a driver; `driver_importance.csv` calls it "semi-controllable". |
| Category | 0.026 | No (structural) |
| Shelf price (log) | 0.020 | Yes |
| Sub-category | 0.017 | No |
| Base price (log) | 0.010 | Yes |
| Discount % | 0.006 | Yes |
| 4-week rolling demand | 0.004 | No (habit) |
| Feature ad | 0.003 | Yes |
| Display | 0.001 | Yes |

Charts: `06_shap_importance.png`, `modeling/charts/driver_importance.png`. Permutation importance [error change when one input is shuffled] confirms VISITS dominates; every other input changes error by under 0.01 (`modeling/tables/permutation_importance.csv`).

**What changing the levers does: modeled sensitivities.** The model was re-scored with every price cut 10%, holding VISITS, ads and displays at observed values (`modeling/tables/counterfactual_10pct_price_cut.csv`; FU R1 Q2).

| Category | Mean unit change | Median unit change | Label |
|---|---|---|---|
| Bag Snacks | +3.2% | +1.3% | modeled (lower bound) |
| Cold Cereal | +1.6% | +1.2% | modeled (lower bound) |
| Oral Hygiene | +1.2% | +0.4% | modeled (lower bound) |
| Frozen Pizza | +0.8% | +0.3% | modeled (lower bound) |

These are a **lower bound only**. VISITS carries nearly all the signal and was frozen, so a real price response cannot show (FU R1 Q2).

**Price sensitivity by method** [elasticity: % change in units for a 1% price change] (FU R1 Q3; MC; MEMO §3.3).

| Category | Chart 01 slope | Between-product slope (95% CI) | Pooled row slope | Within-product slope | Ridge FE elasticity |
|---|---|---|---|---|---|
| Label | measured (association; not verified) | measured | measured | measured | modeled; wrong sign |
| Bag Snacks | −1.44 | −1.48 (−2.2 to −0.7) | −1.35 | −0.21 | +0.48 |
| Frozen Pizza | −1.16 | −0.77 (−1.7 to +0.1) | −1.18 | −2.73 | +0.27 |
| Cold Cereal | −0.34 | +0.18 (−0.8 to +1.1) | −0.50 | −2.35 | +0.26 |
| Oral Hygiene | −0.38 | −0.50 (−0.8 to −0.2) | −0.45 | −1.12 | +0.09 |

Units were *higher* in price-increase weeks in all four categories (e.g., Bag Snacks median 26 vs 18 units, 348 store-product pairs; measured; FU R1 Q7). Prices moved with demand, so history alone cannot show cause.

## B5. Where the volume sits: the top 10% of store-product-weeks hold 43% of units

**By category and store tier** (`reports/tables/category_segment_detail.csv`; measured; revenue = price × units over 156 weeks).

| Category | Tier | Rows | Mean price | Mean weekly units | 3-year revenue |
|---|---|---|---|---|---|
| Cold Cereal | Mainstream | 99,664 | $2.74 | 34.4 | $8.75M |
| Cold Cereal | Upscale | 41,795 | $2.75 | 39.5 | $4.34M |
| Frozen Pizza | Mainstream | 67,173 | $5.33 | 12.2 | $3.91M |
| Cold Cereal | Value | 41,571 | $2.74 | 28.9 | $3.12M |
| Bag Snacks | Mainstream | 77,307 | $2.21 | 21.3 | $2.95M |
| Frozen Pizza | Upscale | 29,812 | $5.38 | 12.2 | $1.84M |
| Bag Snacks | Upscale | 31,923 | $2.23 | 28.3 | $1.74M |
| Frozen Pizza | Value | 23,626 | $5.17 | 11.6 | $1.27M |
| Oral Hygiene | Mainstream | 71,245 | $3.77 | 4.2 | $0.97M |
| Oral Hygiene | Upscale | 31,971 | $3.87 | 5.7 | $0.63M |
| Bag Snacks | Value | 26,318 | $2.14 | 10.0 | $0.44M |
| Oral Hygiene | Value | 23,416 | $3.66 | 3.5 | $0.26M |

The handoff's "Annual revenue ($M)" column (HR §6b) is overstated about 50-fold and is not used (FU R1 corrections). `segment_summary.csv` shows fewer Upscale rows than this table (e.g., Bag Snacks 26,481 vs 31,923); the cause is not documented.

**Decile table** [decile: one tenth of rows, ranked by predicted units] (`modeling/tables/decile_table.csv`, test set 88,751 rows; modeled).

| Decile | Rows | Mean actual units | Lift vs average |
|---|---|---|---|
| 10 (highest) | 8,875 | 78.7 | 4.34× |
| 9 | 8,875 | 32.3 | 1.79× |
| 8 | 8,875 | 21.6 | 1.19× |
| 7 | 8,875 | 15.5 | 0.86× |
| 1 (lowest) | 8,876 | 1.2 | 0.07× |

**Share captured by top-ranked rows** (`reports/tables/risk_targeting.csv`; modeled ranking, measured shares).

| Top % by predicted demand | Share of units | Share of revenue |
|---|---|---|
| 10% | 42.6% | 35.3% |
| 20% | 60.8% | 53.4% |
| 30% | 73.1% | 66.4% |
| 50% | 88.3% | 83.9% |

**Threshold table** (`modeling/tables/threshold_table.csv`; modeled).

| Cut-off (predicted units) | Share of rows flagged | Share of units captured |
|---|---|---|
| 41.17 | 10% | 43.4% |
| 21.43 | 25% | 67.7% |
| 9.67 | 50% | 88.1% |
| 4.08 | 75% | 97.1% |

Because VISITS drives the ranking, these tables describe where volume already is, not where a lever would add volume.

**Smallest intervention.** The handoff named "moderate price cut plus Feature ad in Value stores" (HR §6a). That advice is **withdrawn**: the slopes behind it could not be reproduced and the Value-store effect failed within categories (FU R1 Q3, Q6; MEMO §4 B1). The memo's smallest step is a policy one: a break-even check on each discount event (MEMO §4 B2).

## B6. The strategy: promotion discipline first, then store-randomised price tests

**Thesis** (MEMO §1): the profit opportunity is promotion discipline, not price cuts. Proof should come from store-level tests.

**Internal metrics against external benchmarks** (MEMO §2). Internal data is 2009–2011; benchmarks are 2016–2026.

| Metric | This chain | Market | Gap | Labels |
|---|---|---|---|---|
| Share of revenue sold on discount | 36.8% (26.9% Bag Snacks to 48.4% Frozen Pizza) | 34% of branded units on promotion, Europe 2026 ([FoodNavigator/Circana](https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/)) | In line; Pizza far above | assumed; external |
| Promotions that break even | 0 of 4 category averages at 30% margin | About 1 in 4 ([FoodNavigator/Nielsen](https://www.foodnavigator.com/Article/2016/04/04/Four-strategies-for-overcoming-diminishing-returns-on-trade-promotions/)) | Consistent with market waste | assumed; external |
| Store-brand dollar share | Bag Snacks 41.6%, Pizza 24.9%, Oral 17.2%, Cereal 13.9% | 21.3% US 2025 ([PLMA](https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025)) | Cereal −7.4 pts, Oral −4.1 pts | measured; external |
| Net margin, food retail | Not in data | 2.1% of sales ([FMI](https://www.fmi.org/our-research/supermarket-facts)) | Thin margins make markdown waste matter | external |
| Own-price elasticity | −0.2 to −2.7 by method | −2.62 literature average (Bijmolt et al. 2005; page not fetched) | Not comparable | measured; assumed |
| AI promotion optimisation result | Not deployed | +2.5% ([DemandTec](https://www.demandtec.com/case-studies/smarter-pricing-stronger-outcomes-how-ngi-is-driving-growth-through-data-driven-strategy/)); +7% margin ([Hexaware](https://hexaware.com/case-study/ai-pricing-optimization-and-promotions-drive-retail-margin-improvements-for-a-leading-latin-american-convenience-retailer/)) | Vendor claims, unaudited | external |
| Display lift | Display-only median units 1.6× to 3.1× no-promo weeks | +14% across 16 digital-screen studies ([Grocery TV](https://grocerytv.com/meta-study/cpg/)) | Internal figure inflated by week choice | measured; external |

**Break-even test** (MEMO §3.2). A discount of depth d breaks even only if units rise by m ÷ (m − d), where m is gross margin [revenue minus cost of goods, as a share].

| Category | Mean depth | Revenue lift, discount vs regular week | Implied unit lift | Break-even at 30% margin | At 40% | Verdict |
|---|---|---|---|---|---|---|
| Label | measured (FU R1 Q4) | measured (FU R2 Q2) | assumed | assumed | assumed | |
| Bag Snacks | 18.7% | 1.15× | 1.41× | 2.65× | 1.88× | Loses at both |
| Cold Cereal | 21.9% | 1.55× | 1.98× | 3.70× | 2.21× | Loses; near break-even at 40% |
| Frozen Pizza | 23.1% | 2.29× | 2.98× | 4.35× | 2.37× | Breaks even only at 40%+ |
| Oral Hygiene | 26.1% | 1.23× | 1.66× | 7.69× | 2.88× | Loses at both |

No post-promotion dip [sales falling after a deal] shows in medians (FU R2 Q3; measured).

**Three levers** (MEMO §1; all assumed).

| Lever | What changes | Annual impact on these 4 categories |
|---|---|---|
| 1. Promotion pruning and re-funding | Cut or vendor-fund the worst 25% of discount events | +$0.10M to +$0.25M gross margin |
| 2. Everyday-price test and learn | +2% to +5% base-price tests on the 25 products making 80% of revenue | +$0.08M to +$0.15M |
| 3. Store-brand price-gap architecture | Close store-brand share gaps in Cereal and Oral Hygiene | +$0.03M to +$0.06M |

If the playbook added 1% of revenue chain-wide, the memo sizes it at about $27M a year, assuming a $2.7B chain (77 stores × $668,377 a week × 52; assumed; MEMO §1).

**Recommendations by track** (MEMO §4).

| Track | # | Action | Timeline | Gate to proceed |
|---|---|---|---|---|
| B (quick wins) | B1 | Freeze simulator for price decisions | Week 0 | No price change cites HR §6a |
| B | B2 | Break-even gate: lift ≥ 1.2 × m ÷ (m − d) or vendor funding | Weeks 1–4 | ≥ 90% of events carry a break-even sheet |
| B | B3 | Re-negotiate below-break-even events with vendors | Weeks 2–10 | Vendor-funded share +10 pts |
| B | B4 | 20% cap on retailer-funded depth | Weeks 2–12 | Depth ≤ 20%, units down < 5% |
| B | B5 | Store-brand price-gap rules | Weeks 4–16 | Cereal store-brand share +2 pts by week 26 |
| B | B6 | Brief finance and vendors on corrected baseline | Weeks 0–2 | Leadership sign-off |
| A (capability) | A1 | Remove duplicates; correct revenue; re-issue reports | Weeks 0–2 | Revenue reconciles to $28.69M within 0.5% |
| A | A2 | Rebuild simulator without VISITS | Weeks 2–8 | Test error ≤ 20%; negative price response in all 4 |
| A | A3 | Load unit cost and vendor funding | Weeks 0–6 | Margin coverage ≥ 90% of revenue |
| A | A4 | Store randomisation engine | Weeks 2–8 | Pre-period difference < 3% |
| A | A5 | Causal elasticity from pilots plus a cost instrument | Weeks 8–20 | Negative elasticity, CI width < 1.0 |
| A | A6 | Uplift scoring [predicting the extra margin an event adds] | Weeks 12–26 | Beats business-as-usual in Pilot 1 holdout |
| A | A7 | Capture basket, competitor price, store traffic, deal terms | Weeks 4–26 | 3 of 4 feeds live |
| A | A8 | Drift guardrails: quarterly retrain, alerts | From week 8 | No silent failure in 90 days |

**Five pilots** (MEMO §5). All randomise by store, stratify by tier and size, and read results by difference-in-differences [change in test stores minus change in control stores]. Effect ranges and MDEs [minimum detectable effect: the smallest change the test can see] are assumed.

| Pilot | Categories | Design | Hypothesis | North-star metric | Day-90 decision rule |
|---|---|---|---|---|---|
| 1. Promotion holdout | Frozen Pizza, Cereal | 38 vs 39 stores, 12 weeks; MDE ≈ 10% | Skipping the lowest-lift 25% of events lifts margin 3–8% | Category gross margin $ per store-week | ≥ +3% with CI above 0: scale; ≤ 0: kill |
| 2. Everyday-price ladder | Top 10 Cereal | Control / +3% / +5%; 25/26/26 stores, 12 weeks; MDE ≈ 12% | +3% lifts margin 1–3% with < 3% unit loss | Cereal gross margin $ | ≥ +1%: roll +3%; elasticity < −1.5: reverse |
| 3. Depth test 15% vs 25% | Frozen Pizza, Oral Hygiene | 38 vs 39 stores, 8 event weeks; MDE ≈ 15% | Margin per event +10–30%, units fall < 25% | Gross margin $ per event | ≥ +10%: new depth standard; else revert |
| 4. Display without discount | Bag Snacks | 38 vs 39 stores, 8 weeks, 4 products; MDE ≈ 12% | Margin per display week +15–40% | Gross margin $ per display week | ≥ +15%: standard; < 0: kill |
| 5. Store-brand price gap | Cereal, Oral Hygiene | 38 vs 39 stores, 12 weeks; MDE ≈ 1.5 pts | Store-brand share +2–4 pts | Margin $ and store-brand share | ≥ +2 pts and margin up: scale; else revert |

Pilots 1, 3 and 4 share no category and can run together. Pilots 2 and 5 both touch Cereal, so Pilot 5 waits or uses a separate split (MEMO §5).

**Prioritisation** (MEMO §6.2).

| Initiative | Impact | Confidence | Time to value | Wave |
|---|---|---|---|---|
| B2 gate + B4 depth cap | High | Medium | 2–4 weeks | 1 |
| B3 vendor re-negotiation | High | Medium | 4–10 weeks | 1 |
| A1 data fix + B1 freeze | Risk avoidance | High | 1–2 weeks | 1 |
| A3 cost and funding data | Enabler | High | 4–6 weeks | 1 |
| Pilot 1 promotion holdout | High | Medium-high | 4 weeks to launch | 2 |
| Pilot 3 depth test | Medium-high | Medium | 4 weeks | 2 |
| Pilot 2 price ladder | Medium | Low-medium | 6 weeks | 2 |
| Pilot 4 display | Medium | Low-medium | 4 weeks | 2 |
| A2 leak-free simulator | Enabler | Medium | 6–8 weeks | 2 |
| Pilot 5 + B5 store brand | Low-medium | Medium | 8 weeks | 3 |
| A5/A6 causal elasticity, uplift | High at scale | Medium | 20–26 weeks | 3 |

## B7. The agent dialogue: 14 questions in two rounds reshaped the strategy

The growth-strategy partner sent questions to the statistician by direct message. Questions are verbatim from DIA. Answers are quoted from FU (key lines; full tables in FU). No question was declined and none remains open (DIA).

### Round 1 (8 questions plus 1 optional)

| # | Memo section | Question (verbatim) | Answer (quoted from FU R1) | What changed |
|---|---|---|---|---|
| 1 | §1, §2, §3 | "Total revenue. decile_revenue.csv and category_segment_detail.csv sum SPEND to about $30.2M over 156 weeks. Handoff §2 and §6b state $1.49B total / $801M Cereal "annualised". Which is correct? Please give total SPEND and annual SPEND (total/3) by category." | "Total $28.69M over 156 weeks = $9.56M/year." "Your figures are right; the report is wrong." | Revenue corrected; levers re-sized; corrections box added |
| 2 | §3.3, §3.4, A2, B1 | "VISITS definition. data_dictionary.md defines VISITS as "shopping trips including this product" (an outcome, r=0.99 with UNITS), not store traffic as handoff §5 states. Please confirm, and confirm the §6e counterfactual held VISITS fixed at observed values when price was cut 10%. Also give median UNITS/VISITS overall." | "Confirmed: VISITS = trips including the product (outcome). corr(UNITS, VISITS) = 0.987. Median UNITS/VISITS = 1.038." "the +0.8% to +3.2% figures are a lower bound on a real price response, not a measure of it." | Simulator frozen for price decisions; counterfactual relabelled a lower bound |
| 3 | §3.3, §1 | "Exploration slopes (−1.44, −1.16, −0.34, −0.38): are they each fit across one point per UPC (~10–15 points per chart 01)? Give n and SE for each slope; reconcile with hypotheses.md H3 and findings.md F1." | "I could not reproduce chart 01's slopes" "The exploration outputs are mutually inconsistent." "Treat the category ranking "Bag Snacks and Pizza most price-sensitive" as NOT established." | Slopes labelled not reproducible; thesis withdrawn; Pilot 2 moved to Cereal |
| 4 | §1, §2, §3.2 | "By category: % of store-weeks with PRICE < BASE_PRICE; % with FEATURE=1; % with DISPLAY=1; mean discount depth; % of SPEND sold in discounted weeks." | "all four categories are discounted in 23-29% of rows. Chart 02/finding F2 ... is a median artifact" | ~37% discount share and ~$1.0M markdown derived; F2 exposed |
| 5 | §3.2, Pilot 4 | "By category × promo type (None, TPR only, Display only, Feature only, Feature+Display): row count, median UNITS per store-week, median UPV." | "Units lift (2-4x) is far larger than UPV lift (0-15%), meaning promos mostly raise trips including the product, not units per trip." | Pilot 4 (display without discount) added |
| 6 | §3.4, B1, risks | "Promo lift ratio (promoted / non-promoted median units) by store segment within each category." | "Value stores are NOT consistently the highest." "It was a product-mix artifact." | Value-store targeting withdrawn |
| 7 | §3.3 | "For rows with PRICE > BASE_PRICE (~2%): count by category, and median units in those weeks vs median units at PRICE = BASE_PRICE for the same UPC-store pairs." | "total 6,264 = 1.2% of rows (not ~2%)." "Units are HIGHER in price-increase weeks in all four categories." | Confirms prices follow demand; test before rollout |
| 8 | §2, Lever 3, Pilot 5, B5 | "Revenue share of private-label UPCs by category; mean shelf price of PL vs national-brand UPCs within each category." | PL share: Bag Snacks 41.6%, Cereal 13.9%, Pizza 24.9%, Oral 17.2% | Lever 3, Pilot 5 and B5 added |
| opt | §5 | "week-to-week CV for pilot sizing" | "median Bag 0.46, Cereal 0.36, Pizza 0.55, Oral 0.55" | Pilot MDE calculations |

### Round 2 (6 questions)

| # | Memo section | Question (verbatim) | Answer (quoted from FU R2) | What changed |
|---|---|---|---|---|
| 1 | §5 | "Number of stores by segment (Mainstream / Upscale / Value), and number of distinct stores selling each category." | "77 stores: Mainstream 43, Upscale 15, Value 19. Every store carries all four categories" | 38 vs 39 store arms; tier stratification |
| 2 | §3.2, Lever 1, Pilots 1, 3 | "By category: median SPEND per store-UPC-week in discounted vs undiscounted rows (same store-UPC pairs). Revenue lift ratio." | Ratio of medians: Bag 1.15, Cereal 1.55, Pizza 2.29, Oral 1.23. "this is not a price effect." | Break-even table added |
| 3 | §3.2 | "Post-promotion dip. By category: median units in the first undiscounted week after a discounted week vs undiscounted weeks ≥3 weeks away from any discount." | "No post-promotion dip is visible in medians" | Main risk is markdown waste, not pull-forward |
| 4 | §3.1, B4 | "By category: median discounted weeks per store-UPC per year; median length of consecutive discount runs." | Weeks a year: Bag 11.0, Cereal 11.6, Pizza 16.2, Oral 13.8; run length 2–4 weeks | Informs holdout design |
| 5 | §3.3, Pilot 2 | "By category: median BASE_PRICE changes per UPC over 156 weeks; share that are chain-wide (same week, ≥90% of stores)." | "Base price is changing often and mostly store by store, not chain-wide" (2.6%–9.0% of change events chain-wide) | Store-level price tests judged operationally normal |
| 6 | §3.1 | "Number of UPCs making up 80% of SPEND, out of 55 total." | "25 of 55 UPCs (45%) account for 80% of total SPEND." | F4 corrected; Pilot 2 targets top 25 |

### Notebook review: 10 gaps still open after one fix round

| Notebook | Gaps found, pass 1 | Fix round | Gaps open after pass 2 | Source |
|---|---|---|---|---|
| 01_exploration | 11 | All 11 sent to the explorer; H4 string bug fixed; re-run with 0 errors | 3 | NBR |
| 02_feature_engineering + 03_modeling | 10 | All 10 sent to the model builder; re-run with 0 errors | 7 (some new, some carried over) | NBR |

Remaining gaps:
- Exploration: no alternatives named for the lift-ratio chart; no formal null hypothesis [the "no effect" statement a test tries to reject] for H1, H2, H4–H6; discount direction missing in the data dictionary.
- Modeling: three diagnostic cells have no captured output (decile lift, permutation, SHAP plots); diagnostics and Ridge fit lack explanatory notes; no "Finding" notes after residual, decile, threshold, permutation and SHAP results; XGBoost `min_child_weight` missing from the tuning search-space table; `features.md` lacks formula, expected direction and example row.

The review stopped at its one-fix-round limit (NBR).

---

# Part C. Checks and limits

## C1. Consistency check: numbers that appear in two or more reports

| Item | Values found | Status |
|---|---|---|
| Total revenue | HR §2: ~$1.49B; FU R1 Q1 and MEMO: $28.69M over 3 years, $9.56M a year | **Discrepancy.** HR is an arithmetic error (FU). Use $9.56M. |
| Category revenue | HR §6b and `actionability_levers.csv`: Cereal $801M a year; FU R1 Q1: $5.14M | **Discrepancy.** Same error; CSV still carries it. |
| What VISITS measures | HR §5, `features.md`: store traffic; DD, FU R1 Q2: trips including the product | **Discrepancy.** DD and FU are right. |
| Price slopes | Chart 01: Bag −1.44 ... Cereal −0.34; EXP F1: "−0.8 Mouthwash to −1.5 Cereal"; HTM: Cereal ≈ −1.5; H3: Cereal −0.497, Mouthwash −0.448 | **Discrepancy.** Mutually inconsistent and not reproducible (FU R1 Q3). |
| Ridge FE elasticity | MC, `elasticity_by_category.csv`: +0.09 to +0.48 | Agree with each other; **wrong sign** (HR §7). `elasticity_by_upc.csv` lists 20 products, 7 negative. |
| Discount frequency | EXP F2: Pizza and Mouthwash in over half of weeks; HTM: ~28% of rows promoted; FU R1 Q4: 23–29% of rows | **Discrepancy.** F2 wrong. |
| Products making 80% of revenue | EXP F4, HR §3: ~20 of 55; chart 05: 45%; FU R2 Q6: 25 of 55 | **Discrepancy.** 25 of 55 is right. |
| Value-store lift | EXP F5, HR §3, chart 04: Value highest; FU R1 Q6: highest in no category | **Discrepancy.** Claim withdrawn. |
| Price-increase rows | Audit: 4,906 (0.93%); HTM, MC, HR: ~2%; FU R1 Q7: 6,264 (1.2%) | **Discrepancy.** Different row bases; 1.2% is the latest count. |
| Duplicates | Audit: 0; HTM: "key confirmed unique"; FU R1: 13,693 duplicate keys | **Discrepancy.** Duplicates exist. |
| Zero-unit rows | Audit: 5; HTM: 0 | Minor discrepancy. |
| Store segments | DD, HTM: 5 values; DD distinct count and FU R2 Q1: 3 | **Discrepancy.** 3 segments. |
| Test period | HTM: Jul–Dec 2011; HR §8: Jul 2011–Jan 2012 | Agree in substance (final week ends 4 Jan 2012). |
| Test-set rows | HR §8: 88,751; `decile_table.csv`: 10 × ~8,875 | Agree. |
| Test set used once | HR §8: yes; FU R1: not verified, counterfactual re-scored test rows | **Unverified.** |
| Counterfactual size | Notebook narrative: "10–15%"; CSV and HR §6e: +0.8% to +3.2% | **Discrepancy.** CSV is the computed result (FU R1 Q2). |
| Optuna trials | TUN: 60 completed each, 2 and 6 pruned; history charts show 62 and 66 points; MC: "60+" | Agree. |
| Best CV error | TUN, MC, `final_model_comparison.csv`: 0.1043 LightGBM | Agree. |
| Test metrics | MC and HR §4: RMSE 0.111, R² 0.989, MAPE 8.5% | Agree. |
| Weakest category | HR §4: Bag Snacks MAPE 10.2%; `performance_by_category.csv`: Frozen Pizza 10.5% is higher | **Discrepancy.** Pizza is weakest. |
| Model families compared | HR §4: "eight model families", names six | Minor: eight rows are six families with tuned and default variants. |
| Top-decile units | HR §9: 79 vs mean 18; chart 07 and `decile_table.csv`: 78.7 vs 18.1 | Agree. |
| Upscale row counts | `segment_summary.csv` vs `category_segment_detail.csv`: e.g., 26,481 vs 31,923 Bag Snacks Upscale rows | **Unexplained discrepancy.** |
| Feature+Display rows | HTM, MC, HR: 24,078 (4.5%); audit: 23,414 rows with several flags | Different definitions; not a conflict. |

**Strategy claims with no supporting number in the handoff report.** Each rests on FU answers or memo arithmetic instead.

| Memo claim | Where its number comes from | Label |
|---|---|---|
| 36.8% of revenue on discount; ~$1.0M markdown a year | MEMO arithmetic on FU R1 Q1, Q4 | assumed |
| 0 of 4 categories break even | FU R2 Q2 lifts plus assumed 30%/40% margin | assumed |
| Lever dollar ranges ($0.10–0.25M, $0.08–0.15M, $0.03–0.06M) | Memo estimate | assumed |
| $2.7B chain revenue; $27M chain-wide value | FMI average × 77 stores | assumed |
| Store-brand gaps | FU R1 Q8 plus PLMA | measured; external |
| Pilot effect ranges, MDEs, 1.2× safety bar, 20% depth cap | Memo estimate | assumed |
| No pull-forward | FU R2 Q3 medians, untested | measured |

**Benchmarks the memo marked unverified** (MEMO §6.5).

| Source | Figure | Problem |
|---|---|---|
| McKinsey pricing articles | ~8% profit per 1% price | Fetch timed out; seen in search summaries only |
| Bijmolt et al. 2005 | −2.62 average elasticity | Repository returned 403; abstract only |
| Marketing Week UK | (not used) | Returned 403 |
| Columbia/Kellogg elasticity PDF | (not used) | Not machine-readable |
| DemandTec, Hexaware, Grocery TV | +2.5%, +7%, +14% | Vendor-published and unaudited |

## C2. Limitations and failure modes (merged, highest business risk first)

| # | Issue | Effect | Fix | Sources |
|---|---|---|---|---|
| 1 | Ridge FE elasticities have the wrong sign | Price decisions taken from them would be directionally wrong | IV/2SLS [a two-step method using a cost-driven price signal] or pilot data | HR §7; MEMO A5 |
| 2 | VISITS is an outcome inside the demand model | Accuracy is inflated; price response is hidden | Rebuild without VISITS | FU R1 Q2; MEMO A2 |
| 3 | No cost, margin or vendor-funding data | Profit and break-even cannot be measured | Load from ERP and trade-funds ledger | EXP; HR §7; MEMO A3 |
| 4 | Prices move with demand | History cannot show cause | Randomised store tests | FU R1 Q7 |
| 5 | Exploration outputs inconsistent; code missing | Category ranking not established | Re-run exploration with code retained | FU R1 Q3 |
| 6 | 13,693 duplicate rows | Totals and lags slightly distorted | De-duplicate | FU R1; MEMO A1 |
| 7 | No competitor prices | Substitution unobserved | License competitor price data | EXP; HR §7 |
| 8 | Feature+Display only 4.5% of rows | Wide uncertainty on that effect | Designed tests | HTM; MC |
| 9 | Promotion comparisons are selection-biased | Lifts overstated | Holdout pilots | FU R1 Q5; MEMO §3.2 |
| 10 | Price-increase weeks are rare (1.2%) | Forecasts above base price extrapolate | Flag and widen bands | FU R1 Q7; HR §7 |
| 11 | Data is 2009–2011 | Behaviour may have changed | Pilots produce current data | MEMO §6.3 |
| 12 | Base price is a derived series | Some changes may be data noise | Validate against price files | FU R2 Q5 |
| 13 | No basket data | Halo [extra items bought on the same trip] unseen | Basket feed | MEMO §3.2 |
| 14 | Notebook documentation gaps (10 open) | Harder to audit | Another review round | NBR |

## C3. Instrumentation gaps, in priority order

1. Unit cost, gross margin and vendor funding per product (MEMO §6.4; HR §7 row 2).
2. Randomised store-level price and promotion change log (MEMO A4).
3. Store traffic counting all trips, not product trips (MEMO A7; HR §7 row 7).
4. Competitor shelf prices at store-week level (HR §7 row 3).
5. Basket-level data for halo effects (MEMO A7).
6. Retained exploration code so slopes can be reproduced (MEMO §6.4 item 4).

---

# Part D. Appendix

## D1. Glossary

| Term | Plain meaning |
|---|---|
| Base price | The regular everyday shelf price before any temporary discount. |
| Basket halo | Extra items a shopper buys on a trip because a promoted item drew them in. |
| Bayesian optimisation | A search that uses past trial results to choose the next settings to try. |
| Break-even lift | The unit increase a discount needs to earn the same margin dollars: m ÷ (m − d). |
| CatBoost, XGBoost, LightGBM | Three tree-based forecasting programs that add many small decision rules together. |
| CI (confidence interval) | The range likely to contain the true value; here 95% likely. |
| colsample_bytree | The share of inputs each tree is allowed to see; lower values reduce over-fitting. |
| Collinearity | Two inputs carrying almost the same information. |
| Correlation (r) | How closely two numbers move together, from −1 to 1. |
| Counterfactual | A "what if" run: change one input and re-score the model. |
| Cross-validation (CV) | Testing a model several times on blocks of data it did not train on. |
| Cumulative gain | The share of all units captured by the top-ranked rows. |
| Decile | One tenth of the rows, ranked by predicted units. |
| Difference-in-differences | Change in test stores minus change in control stores over the same period. |
| Display | An in-store secondary placement such as an end-cap. |
| Drift | A model's accuracy slipping as conditions change. |
| Elasticity | The % change in units for a 1% change in price. −1.5 means a 1% price rise cuts units 1.5%. |
| Expanding window | Each test fold trains on all weeks before it. |
| Feature | Inclusion in the retailer's weekly circular ad. |
| Fixed effects (FE) | A separate baseline for each store and product. |
| Gross margin | Revenue minus cost of goods. |
| Held-out test set | Data kept unseen until the end to judge the final model. |
| Holdout / control stores | Stores that do not get the change, used for comparison. |
| Hyperparameter | A setting chosen before training, such as number of trees. |
| IV / 2SLS / instrument | A two-step method using a price driver unrelated to demand, such as a cost change, to isolate cause. |
| Leakage | When an input contains the answer the model predicts, as VISITS does here. |
| Learning rate | How large a step each new tree takes. |
| Lift | How much higher a group's result is than the average or baseline. |
| Log / log-log slope | Logarithm turns % changes into straight-line distances; the slope of log units on log price. |
| MAPE | Mean absolute percentage error: the average miss as a % of actual units. |
| Mann-Whitney U | A test comparing two groups by rank rather than average. |
| Markdown | Dollars given away by selling below the base price. |
| max_depth, num_leaves, min_child_samples, min_child_weight | Limits on how detailed each tree may become. |
| MDE (minimum detectable effect) | The smallest change a test can reliably see. |
| Median | The middle value when sorted. |
| n_estimators | Number of trees in the model. |
| Net margin | Profit after all costs as a share of sales. |
| Null hypothesis | The "no effect" statement a test tries to reject. |
| OLS | Ordinary least squares: a straight-line regression. |
| Optuna | Software that tries many hyperparameter settings and learns which work. |
| Outcome variable | A number produced by the thing being predicted, not a cause of it. |
| p-value | The chance of seeing a result this large if there were no real effect. |
| Permutation importance | How much error rises when one input is shuffled. |
| Pruned trial | An Optuna trial stopped early because it was not promising. |
| Pull-forward | Shoppers buying ahead during a deal, lowering later sales. |
| R² | Share of variation in the outcome a model explains. |
| Random Forest | Many decision trees averaged together. |
| Rank-biserial r | Effect size for Mann-Whitney: 0 no effect, 1 full separation. |
| reg_alpha, reg_lambda | Penalties that shrink weak inputs to reduce over-fitting. |
| Regression | A formula linking an outcome to inputs. |
| Ridge | A regression with a penalty that keeps coefficients small. |
| RMSE / RMSE_log | Root mean squared error; on the log scale, 0.11 is roughly ±12% in units. |
| SE (standard error) | The typical uncertainty of an estimate. |
| SHAP | Shapley additive explanations: each input's average contribution to a prediction. |
| Spearman ρ | A rank-based correlation. |
| Store brand (private label, PL) | The retailer's own-label products. |
| Store tier | The chain's store segment: Mainstream, Upscale or Value. |
| Stratify | Balance test and control groups on key traits such as tier and size. |
| subsample | Share of rows each tree trains on. |
| Threshold | A cut-off on predicted units used to flag rows. |
| TPR | Temporary price reduction without a feature ad or display. |
| Trade spend / vendor funding | Money manufacturers pay retailers to fund promotions. |
| Trial | One test of one set of model settings. |
| UPC | Universal product code: one product at one pack size. |
| Uplift | The extra effect of an action compared with no action. |
| UPV | Units per visit: units ÷ trips that included the product. |
| VISITS | Shopping trips that included the product that week. |

## D2. Chart manifest

| File | What it shows | Key takeaway |
|---|---|---|
| `charts/01_demand_curves_by_category.png` (= `exploration/charts/7B`) | Log units vs log price, ~9–10 product points per category | Negative slopes everywhere; sizes not reproducible |
| `charts/02_discount_depth_by_category.png` (= `7A`) | Box plot of discount depth | Median 0% for Bag Snacks and Cereal is a median artifact; all discount 23–29% of rows |
| `charts/03_promotion_lift_by_type.png` (= `7C`) | Units per visit by promotion type | Feature and Feature+Display medians about 1.14 vs 1.00; per-trip lift is small |
| `charts/04_promo_lift_by_store_segment.png` (= `7F`) | Median lift ratio by tier | Value looks highest pooled; fails within category |
| `charts/05_revenue_concentration.png` (= `7D`) | Revenue by product with cumulative share | 45% of products (25 of 55) make 80% of revenue |
| `charts/06_shap_importance.png` | Mean SHAP by input | VISITS dwarfs every other input |
| `charts/07_decile_lift.png` | Mean actual units by predicted decile | Top decile 78.7 units vs 18.1 average |
| `charts/08_model_comparison.png` | CV error by model | Tree models ~0.105; regressions ~0.41–0.43; baseline 0.749 |
| `exploration/charts/7E_correlation_matrix.png` | Correlation heat map | VISITS and HHS 1.00; VISITS and UNITS 0.99 |
| `modeling/charts/optuna_lgb_history.png`, `optuna_xgb_history.png` | Error per Optuna trial | Gains flatten after ~10–15 trials |
| `modeling/charts/optuna_lgb_importance.png`, `optuna_xgb_importance.png` | Which settings mattered | colsample_bytree (0.42) for LightGBM; reg_alpha (0.34) for XGBoost |
| `modeling/charts/driver_importance.png` | SHAP coloured by controllability | Controllable levers are tiny next to VISITS |
| `modeling/charts/permutation_importance.png` | Error change when shuffled (VISITS off-scale) | No non-VISITS input matters much |
| `modeling/charts/reliability_curve.png` | Predicted vs actual log units; residuals | Tight fit; residuals centred on zero |
| `modeling/charts/feat_*.png` (7 files) | Distribution and relation to units for each engineered input | VISITS is a near-straight line with units; price inputs show weak spread |

## D3. Web sources (from MEMO §6.5)

| URL | Summary |
|---|---|
| https://www.fmi.org/our-research/supermarket-facts | 2025 food-retail net margin 2.1%; average store sells $668,377 a week |
| https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025 | US store brands $282.8B in 2025; 21.3% dollar share |
| https://www.foodnavigator.com/Article/2016/04/04/Four-strategies-for-overcoming-diminishing-returns-on-trade-promotions/ | About three-quarters of promotions do not break even; trade spend 15–20% of sales |
| https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/ | Europe: 34% of branded vs 14% of store-brand units sold on promotion |
| https://www.demandtec.com/case-studies/smarter-pricing-stronger-outcomes-how-ngi-is-driving-growth-through-data-driven-strategy/ | Vendor case: +2.5% sales, units and margin dollars |
| https://hexaware.com/case-study/ai-pricing-optimization-and-promotions-drive-retail-margin-improvements-for-a-leading-latin-american-convenience-retailer/ | Vendor case: +7% margin, test vs control stores |
| https://grocerytv.com/meta-study/cpg/ | Vendor: +14% average lift from in-store digital screens |

## D4. Files produced

**Notebooks (listed first).**

| File | What it shows |
|---|---|
| `notebooks/01_exploration.ipynb` | Quality audit, cleaning, charts 7A–7F and tests H1–H6 (72 cells) |
| `notebooks/02_feature_engineering.ipynb` | Construction of the 20 model inputs, lags and seasonal terms (49 cells) |
| `notebooks/03_modeling.ipynb` | Model benchmark, Optuna tuning, Ridge FE elasticities, diagnostics, SHAP and the 10% price-cut counterfactual (67 cells) |

**Reports and tables.**

| Folder | Files |
|---|---|
| `reports/` | `final_report.md`, `final_report.html`, `ml_handoff_report.md`, `ml_followups.md`, `executive_growth_strategy.md`, `agent_dialogue.md`, `notebook_review.md`, `customer_risk_scores.csv` (538,435 scored rows) |
| `reports/exploration/` | `findings.md`, `data_dictionary.md`/`.csv`, `handoff_to_modeling.md`, `hypotheses.md`, `quality_audit.md`, `cleaning_log.md`, `clean.parquet`, 6 charts |
| `reports/modeling/` | `model_card.md`, `tuning.md`, `features.md`, `features.parquet`, `scores.csv`, 17 charts |
| `reports/modeling/tables/` | `counterfactual_10pct_price_cut`, `decile_table`, `driver_importance`, `elasticity_by_category`, `elasticity_by_upc`, `final_model_comparison`, `model_comparison`, `performance_by_category`, `permutation_importance`, `shap_importance`, `threshold_table` (all `.csv`) |
| `reports/tables/` | `actionability_levers`, `category_segment_detail`, `decile_revenue`, `risk_targeting`, `segment_summary` (all `.csv`) |
| `reports/charts/` | 8 charts, `01` to `08` |
| `models/` | `pricing_model.joblib` (tuned LightGBM), `optuna_lgb.db`, `optuna_xgb.db` (trial histories) |
| `src/` | `explore_utils.py`, `features.py`, `model_utils.py`, `pipeline.py` |

**Not found among the files:** the pricing simulator HTML, the per-product elasticity table with confidence intervals, profit curves, a repricing shortlist and the offer sheet that `problem_description.md` asked for.
