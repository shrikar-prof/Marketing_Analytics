# Executive Growth Strategy: Pricing and Promotion, Four Grocery Categories
**Project:** 05-pricing-simulator | **Date:** 2026-11-16 | **Author:** growth-strategy-partner
**Inputs:** `reports/ml_handoff_report.md` (cited as HR §n), `reports/ml_followups.md` (cited as FU R1/R2 Qn), exploration and modeling tables and charts, live web research (§6 sources).

**Evidence labels.** Every number is tagged with one of four labels.
- *measured*: computed from the data.
- *modeled*: a model output; it shows an association, not a cause.
- *external*: from a cited source.
- *assumed*: my estimate or my arithmetic on other figures. The derivation is shown.

**Read this first: four corrections to the handoff report.** These came from two rounds of questions to the statistician (FU R1).
1. Revenue is $28.69M over 156 weeks, or $9.56M a year (measured, FU R1 Q1). It is not $1.49B. Every dollar cell in HR §2 and §6b is overstated about 50-fold.
2. VISITS counts shopping trips that included the product. That is an outcome, not store traffic (measured, FU R1 Q2). The demand model's 8.5% error and 0.989 R² [share of variation explained] depend on it. So the simulator cannot yet show what a price change does.
3. The category price-sensitivity slopes in HR §3 could not be reproduced. Three methods give three different rankings (FU R1 Q3). "Bag Snacks and Frozen Pizza are most price-sensitive" is **not established**.
4. "Value stores respond more to promotions" does not hold within any category (measured, FU R1 Q6). Stop using it to target promotions.

---

## §1 Thesis and three headline levers

**Thesis: this chain's profit opportunity is promotion discipline, not price cuts.** The proof will come from store-level tests, not from the current models.

- About 37% of revenue in these four categories sells at a discount (assumed; arithmetic on FU R1 Q1 and Q4).
- That costs roughly $1.0M a year in markdown [the price reduction given away] on $9.56M of revenue (assumed; derivation in §3.2).
- At an assumed 30% gross margin, no category's average discounted week recovers its markdown (assumed; §3.2).
- This matches the market: roughly three-quarters of grocery promotions lose money (external, Nielsen via FoodNavigator).

The demand model predicts well but cannot price yet. The econometric elasticities have the wrong sign (HR §7 row 1). So every price move below starts as a test, not a rollout.

| # | Lever | What changes | Directional annual impact on these 4 categories | Label |
|---|---|---|---|---|
| 1 | **Promotion pruning and re-funding** | Cut or vendor-fund the worst 25% of discount events. Cap depth until tests show break-even. | +$0.10M to +$0.25M gross margin (1.0% to 2.6% of revenue) | assumed |
| 2 | **Everyday-price test and learn** | Randomised +2% to +5% base-price tests on the 25 products that make 80% of revenue. Keep only the moves that hold volume. | +$0.08M to +$0.15M gross margin if a 1% to 2% net price gain survives | assumed |
| 3 | **Private-label price-gap architecture** | Close the gap to the 21.3% US store-brand share in Cereal (13.9%) and Oral Hygiene (17.2%). Do this through range and gap, not deeper deals. | +$0.03M to +$0.06M gross margin | assumed |

**Why the dollars look small.** These four categories are about $9.56M of a 77-store chain's revenue (measured). A typical US supermarket sells $668,377 a week (external, FMI). At that average, the chain sells about $2.7B a year (assumed: 77 x $668,377 x 52). The value is in the *method*. A promotion-pruning and price-testing playbook that adds 1% of revenue in margin is worth about $27M a year if it scales chain-wide (assumed).

**Compare against net margin.** The average US food retailer nets 2.1% of sales (external, FMI). Lever 1 alone is about half to all of that on these categories (assumed).

---

## §2 Benchmark table: current state vs market

**Conclusion: the chain discounts at market-typical intensity, and its promotions probably lose money as most promotions do.** Its store-brand share is above market in Bag Snacks and below market in Cereal.

Caveat: the internal data covers 2009–2011. The external benchmarks are 2016–2026. Treat the gaps as directional.

| Metric | This chain (internal) | Market benchmark | Gap reading | Labels |
|---|---|---|---|---|
| Net profit margin, food retail | Not in data (no cost data) | 2.1% of sales, 2025 ([FMI](https://www.fmi.org/our-research/supermarket-facts)) | Thin margin, so markdown waste matters | external |
| Share of sales sold on discount | 36.8% of revenue (range 26.9% Bag Snacks to 48.4% Frozen Pizza) | 34% of branded units sold on promotion, Europe 2026 ([FoodNavigator/Circana](https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/)) | In line overall. Frozen Pizza is far above. | assumed (internal arithmetic); external |
| Promotions that break even | 0 of 4 category averages at an assumed 30% margin; 1 of 4 at 40% (§3.2) | About 1 in 4 grocery promotions break even ([FoodNavigator/Nielsen](https://www.foodnavigator.com/Article/2016/04/04/Four-strategies-for-overcoming-diminishing-returns-on-trade-promotions/)) | Consistent with market waste | assumed; external |
| Trade spend as share of manufacturer gross sales | Not in data | 15–20% (same FoodNavigator/Acosta source) | Shows how much vendor money is available to re-negotiate | external |
| Store-brand dollar share | Bag Snacks 41.6%, Pizza 24.9%, Oral 17.2%, Cereal 13.9% (FU R1 Q8) | 21.3% US, 2025 ([PLMA/Circana](https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025)) | Cereal and Oral trail by 7.4 and 4.1 pts | measured; external |
| Store-brand reliance on promotion | Not measured | 14% of store-brand units on promotion vs 34% branded, Europe ([FoodNavigator/Circana](https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/)) | Store brands win on everyday gap, not deals | external |
| Own-price elasticity [% unit change per 1% price change] | Cannot be pinned down: −0.2 to −2.7 depending on method (FU R1 Q3) | Literature average −2.62, Bijmolt et al. 2005 (page returned 403; seen only in a search abstract) | Internal evidence is too weak to compare | measured; assumed |
| Result of AI-driven promotion optimisation | Not yet deployed | +2.5% sales, units and margin dollars, ~300 stores ([DemandTec/NGI](https://www.demandtec.com/case-studies/smarter-pricing-stronger-outcomes-how-ngi-is-driving-growth-through-data-driven-strategy/)); +7% margin, test vs control stores ([Hexaware](https://hexaware.com/case-study/ai-pricing-optimization-and-promotions-drive-retail-margin-improvements-for-a-leading-latin-american-convenience-retailer/)) | Vendor-published and unaudited. Use 2–7% as an upper range. | external |
| In-store display sales lift | Display-only median units are 1.6x to 3.1x no-promo weeks (FU R1 Q5; retailer chose which weeks) | +14% average lift across 16 studies of in-store digital screens ([Grocery TV](https://grocerytv.com/meta-study/cpg/)) | Internal lift is inflated by week selection | measured; external |

**What competitors and the market are doing (external).**
- Store brands keep gaining. US store-brand sales grew 3.3% in 2025 vs 1.2% for national brands ([PLMA](https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025)).
- Promotions are buying less loyalty. Circana says promotion is "becoming less effective at building loyalty" ([FoodNavigator](https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/)).
- Leading grocers automate promotion decisions at scale. NGI optimises over 9,000 promotions a week ([DemandTec](https://www.demandtec.com/case-studies/smarter-pricing-stronger-outcomes-how-ngi-is-driving-growth-through-data-driven-strategy/)).
- The credible results come from test-vs-control store designs. Hexaware's 7% figure is one ([Hexaware](https://hexaware.com/case-study/ai-pricing-optimization-and-promotions-drive-retail-margin-improvements-for-a-leading-latin-american-convenience-retailer/)).

---

## §3 Evidence: segment economics, response curves, driver importance

### 3.1 Where the money is

**Conclusion: Cold Cereal is the profit pool, and Frozen Pizza is the most promotion-dependent.** Revenue spreads across many products, not a few.

| Category | Revenue / year | Products (UPCs) | Products making 80% of category revenue | Store-brand share | Weeks discounted per store-product per year | Share of revenue sold on discount |
|---|---|---|---|---|---|---|
| Cold Cereal | $5.14M | 15 | 10 | 13.9% | 11.6 | 35.3% |
| Frozen Pizza | $2.21M | 12 | 7 | 24.9% | 16.2 | 48.4% |
| Bag Snacks | $1.62M | 15 | 9 | 41.6% | 11.0 | 26.9% |
| Oral Hygiene | $0.59M | 13 | 8 | 17.2% | 13.8 | 34.3% |
| **Total** | **$9.56M** | **55** | **25 (45%)** | | | **36.8%** |

All measured (FU R1 Q1, Q4, Q8; FU R2 Q4, Q6), except the 36.8% total. That total is assumed arithmetic: the sum of each category's revenue times its discount share.

- Chart `05_revenue_concentration.png` shows 45% of products make 80% of revenue. FU R2 Q6 confirms 25 of 55. HR F4 ("~20 of 55") is wrong.
- The top 5 products hold 27.9% of revenue (measured, FU R2 Q6). A focused price test on about 25 products covers 80% of the money.
- Store mix: 43 Mainstream, 15 Upscale and 19 Value stores (measured, FU R2 Q1). Every store carries all four categories.

### 3.2 Promotion economics: the leak

**Conclusion: discounted weeks raise revenue, but not by enough to cover the markdown at plausible margins.** The exception is vendor-funded events.

- Promotions add units mainly by bringing more trips that include the product. Units per trip barely move.
- Median units in promoted weeks are 2x to 4x non-promoted weeks. Units per trip rise only 0% to 15% (measured, FU R1 Q5).
- HR §3's "10–15% lift" is the per-trip figure. Do not read it as a unit lift.

**Break-even test.**
- A discount of depth d breaks even only if units rise by at least m / (m − d). Here m is the gross margin share of regular price.
- Example: at m = 30% and d = 20%, units must triple.
- Unit lift is approximated as revenue lift ÷ (1 − d).

| Category | Mean depth when discounted (measured, FU R1 Q4) | Revenue lift, discounted vs regular weeks, same store-product (measured, FU R2 Q2) | Implied unit lift (assumed) | Break-even unit lift at 30% margin (assumed) | Break-even at 40% margin (assumed) | Verdict |
|---|---|---|---|---|---|---|
| Bag Snacks | 18.7% | 1.15x | 1.41x | 2.65x | 1.88x | Loses at both margins |
| Cold Cereal | 21.9% | 1.55x | 1.98x | 3.70x | 2.21x | Loses; near break-even at 40% |
| Frozen Pizza | 23.1% | 2.29x | 2.98x | 4.35x | 2.37x | Breaks even only at 40%+ |
| Oral Hygiene | 26.1% | 1.23x | 1.66x | 7.69x | 2.88x | Loses at both margins |

**Markdown sizing (assumed arithmetic).**
- Formula: discounted revenue x d ÷ (1 − d), summed by category.
- By category over 3 years: Bag $0.30M, Cereal $1.53M, Pizza $0.97M, Oral $0.22M.
- Total: $3.0M over 3 years, or about **$1.0M a year**. That is about 10.5% of category revenue.

**Three reasons this may overstate the loss. Each must be checked before acting.**
1. Vendors often fund part of the markdown. We have no funding data (HR §7 row 2).
2. Promotions may bring in shoppers who buy other items too. Basket data is absent.
3. The retailer chose when to promote. Promoted weeks may be high-demand weeks anyway. Q7 shows prices are not set independently of demand (FU R1 Q7).

**One reason it may understate the loss.** No post-promotion dip shows in medians. For example, Frozen Pizza is 6 units after a deal vs 6 units in normal weeks (measured, FU R2 Q3; untested). So pull-forward [buying ahead during a deal] is not visible. Pure markdown waste is the larger risk.

**Promotion mechanics differ by category** (measured, FU R1 Q5).
- In Bag Snacks, display-only weeks show median 31 units vs 10 in no-promo weeks. Feature ads are rare: 2.5% of rows (FU R1 Q4).
- In Cereal, Feature+Display weeks show median 86 vs 21.
- These are selection-biased comparisons. They tell us where to test, not what to roll out.

### 3.3 Response curves: what we know about price sensitivity

**Conclusion: every category's units fall as price rises, but the size of the effect is unknown.** It must be measured by experiment.

The brief asks me to use the exploration slopes as directional price-sensitivity measures. I report them below as **measured association**. The statistician could not reproduce them, and other methods reorder the categories. So I use them only to choose test cells, never to set prices.

| Category | Exploration slope, chart 01 (measured association; not reproducible) | Between-product slope, one point per product, with 95% CI (measured, FU R1 Q3) | Row-level pooled slope (measured) | Within-product slope, no promo controls (measured) | Econometric model (Ridge FE) elasticity (modeled; wrong sign; do not use) |
|---|---|---|---|---|---|
| Bag Snacks | −1.44 | −1.48 (−2.2 to −0.7) | −1.35 | −0.21 | +0.48 |
| Frozen Pizza | −1.16 | −0.77 (−1.7 to +0.1) | −1.18 | −2.73 | +0.27 |
| Cold Cereal | −0.34 | +0.18 (−0.8 to +1.1) | −0.50 | −2.35 | +0.26 |
| Oral Hygiene | −0.38 | −0.50 (−0.8 to −0.2) | −0.45 | −1.12 | +0.09 |

**How to read this table.**
- Chart 01 slopes compare cheap products with expensive ones across about 10 points per category. They do not show what happens when one product's price changes.
- The within-product slopes are the closest to a real elasticity. They are still mixed up with feature and display timing.
- On that within-product view, Cereal and Pizza look *more* sensitive than Bag Snacks. That reverses the HR §6a thesis.
- The simulator's 10% price-cut counterfactual gives +0.8% to +3.2% units (modeled, HR §6e). It held VISITS fixed. So it is a lower bound, not a price response (FU R1 Q2).
- Price-increase weeks are 1.2% of rows. Units were *higher* in those weeks for the same store-product pairs (measured, FU R1 Q7). Price moves follow demand, so history alone cannot reveal elasticity.

**Natural variation we can use.**
- Everyday prices already differ by store.
- Base prices change a median 9 to 34 times per store-product over 156 weeks.
- Only 3% to 9% of those change events are chain-wide (measured, FU R2 Q5).
- So store-level price tests would be operationally normal for this chain.

### 3.4 Driver importance: what is controllable

**Conclusion: the model's drivers are dominated by an outcome variable.** Controllable levers explain little of its predictions, and the model was not designed to show cause.

| Driver | Mean SHAP [average contribution to a prediction] (modeled, HR §5) | Type | Use |
|---|---|---|---|
| VISITS (trips that included the product) | 0.849 | Outcome that leaks into the inputs; not a lever | Remove for price simulation (Track A2) |
| Category, sub-category | 0.026, 0.017 | Structural trait | Segmenting tests |
| Shelf price (log) | 0.020 | Controllable | Test (Pilot 2) |
| Base price (log) | 0.010 | Controllable | Test (Pilot 2) |
| Discount depth | 0.006 | Controllable | Test (Pilot 3) |
| Feature ad / Display | 0.003 / 0.001 | Controllable | Test (Pilots 1, 4) |
| Store tier | 0.002 | Structural trait | Stratify only. The Value-store targeting claim failed (FU R1 Q6). |
| Recent-demand lags | 0.006 | Structural (habit) | Baseline forecasting |

**Decision cut-offs.** There is no yes/no classifier here, so false-positive and false-negative thresholds do not apply directly. The equivalent decision rule is the break-even lift m / (m − d) in §3.2.
- Approve an event only if its predicted lift clears break-even with a safety margin.
- A wrongly approved event loses roughly d x revenue per unit.
- A wrongly rejected event loses only the incremental margin forgone, which is usually smaller.
- So set the bar *above* break-even: proposed 1.2x break-even (assumed) until tests calibrate it.

---

## §4 Dual-track recommendations

**Conclusion: Track B captures cash in the next 60 days with policy alone.** Track A builds the evidence and tooling needed to scale beyond these four categories.

### Track A: capability (data, product and AI)

| # | Initiative | Owner | Timeline | Gate metric to proceed |
|---|---|---|---|---|
| A1 | **Fix the data foundation.** Remove 13,693 duplicate store-product-week rows (FU R1 header). Correct the revenue figures. Re-issue HR §2, §3 F2/F4/F5 and §6. | Data science lead | Weeks 0–2 | Re-issued report; revenue reconciles to $28.69M within 0.5% |
| A2 | **Rebuild the simulator without outcome leakage.** Drop VISITS. Use lagged demand and store-week totals as inputs. Show price-response curves with uncertainty bands. | Data science | Weeks 2–8 | Test-set error ≤ 20% (assumed bar) and negative price response in all 4 categories |
| A3 | **Load unit cost and vendor funding per product** from the ERP and trade-funds ledger. | Finance + IT | Weeks 0–6 | Margin coverage ≥ 90% of revenue |
| A4 | **Store-randomisation engine.** Assign stores to test or control, stratified by tier and size. Lock assignments and log every price and promotion change. | Data engineering | Weeks 2–8 | First pilot randomised; balance check passes, pre-period difference < 3% |
| A5 | **Causal elasticity from experiments.** Re-estimate elasticity with pilot data, plus an instrument [a cost-driven price signal] from wholesale-cost changes. Replace the Ridge FE numbers. | Data science | Weeks 8–20 | Negative elasticity per category with CI width < 1.0 |
| A6 | **Uplift scoring for promotion events.** Predict *incremental* margin per event, not units. Use the pilot control stores as the holdout. | Data science + category management | Weeks 12–26 | Ranked events beat business-as-usual on margin in Pilot 1 holdout |
| A7 | **New data to capture:** basket-level halo, competitor shelf prices, store traffic (all trips, not product trips), vendor deal terms. | Data engineering + procurement | Weeks 4–26 | Feeds live for 3 of 4 sources |
| A8 | **Drift guardrails.** Retrain quarterly. Alert if weekly forecast error exceeds 15% for 3 weeks. Flag any request above the observed price range. | ML ops | From week 8 | Alerts wired; no silent failure in 90 days |

### Track B: commercial quick wins (no model needed)

| # | Action | Owner | Timeline | Gate metric |
|---|---|---|---|---|
| B1 | **Freeze simulator use for price decisions** until A2 passes. Withdraw the "Value-store targeting" and "cut Bag Snacks and Pizza prices" recommendations. | Chief merchant | Week 0 | No price change cites HR §6a |
| B2 | **Break-even gate on every discount event.** A planner must show expected lift ≥ 1.2 x m / (m − d) or vendor funding that covers the gap. | Category managers + finance | Weeks 1–4 | ≥ 90% of events carry a break-even sheet |
| B3 | **Vendor re-negotiation for below-break-even events.** Target Oral Hygiene (26.1% depth) and Bag Snacks (1.15x revenue lift) first. Ask for higher funding or fewer, better events. | Category managers + procurement | Weeks 2–10 | Vendor-funded share of markdown +10 pts |
| B4 | **Interim depth cap of 20%** on retailer-funded discounts. This excludes vendor-funded and clearance events. Pizza (23.1%) and Oral (26.1%) currently average above it. | Chief merchant | Weeks 2–12 | Average retailer-funded depth ≤ 20% with category units down < 5% |
| B5 | **Store-brand price-gap rules.** Set target gaps to the national brand per category. Keep store brands out of deep deals. Expand store-brand range in Cereal and Oral toward the 21.3% benchmark. | Store-brand team | Weeks 4–16 | Store-brand share +2 pts in Cereal by week 26 |
| B6 | **Fix the narrative.** Brief finance and vendors with corrected revenue and the "elasticity unknown, testing" stance. | Strategy / PMO | Weeks 0–2 | Leadership sign-off on corrected baseline |

---

## §5 Pilot experiments: the 90-day growth lab

**Conclusion: five store-randomised pilots turn associations into decisions within 90 days.** Pilot 1 alone could pay for the programme.

**Shared design rules.**
- The unit of randomisation is the store.
- Stratify by tier (43/15/19 stores) and size.
- Measure with difference-in-differences [change in test stores minus change in control stores, using an 8-week pre-period].
- Sample sizes use the measured within-store week-to-week variation in units: 0.36 to 0.55 (FU R1 optional).
- Assumption: averaging over products and 8+ weeks cuts store-level noise to about 15% (assumed). The minimum detectable effect (MDE) [smallest effect the test can reliably see] is about 2.8 x 0.15 x √(2/n stores per arm).

| # | Pilot and playbook | Internal + external trigger | Hypothesis | Design and sizing | Execution | North-star metric / guardrails | Day 30 / 60 / 90 gates |
|---|---|---|---|---|---|---|---|
| 1 | **Promotion holdout (uplift test)**, Frozen Pizza and Cereal | Pizza has 48.4% of revenue on discount and misses break-even at 30% margin (§3.2). About 75% of grocery promotions lose money (external, FoodNavigator). | If we skip the 25% lowest-lift retailer-funded events in test stores, category gross margin rises 3% to 8% because markdown falls faster than incremental units (assumed range). | 38 test vs 39 control stores, 12 weeks. MDE ≈ 10% on store-category margin (assumed). | Data: randomise and track. Category managers: choose the events to skip. Finance: margin ledger. | **Category gross margin $ per store-week.** Guardrails: category units ≥ −5%; store-brand share stable; store complaints. | D30: no guardrail breach, else stop. D60: margin up ≥ 2%, else iterate the event list. D90: ≥ 3% with CI above 0 → scale to all stores; ≤ 0 → kill. |
| 2 | **Everyday-price ladder**, top 10 Cereal products (≈ 80% of Cereal revenue) | Within-product slope −2.35 vs between-product +0.18, so sensitivity is unknown (FU R1 Q3). A 1% price rise at flat volume lifts operating profit about 8% (McKinsey; fetch timed out, so treated as assumed). | If we raise base price 3% in test stores, Cereal gross margin rises 1% to 3% with unit loss under 3% (assumed). This holds only if true elasticity is shallower than about −1. | 3 arms: control, +3%, +5%. 25 / 26 / 26 stores, 12 weeks. MDE ≈ 12% per arm (assumed); pool arms for the slope. | Data: price files and monitoring. Pricing team: execution. Store ops: shelf tags. | **Cereal gross margin $ per store-week.** Guardrails: units ≥ −5%; switching to store brand; basket size. | D30: units within −8%. D60: estimated elasticity has its sign and CI. D90: margin gain ≥ 1% → roll +3% to all stores; elasticity < −1.5 → reverse. |
| 3 | **Depth test: 15% vs 25%**, Frozen Pizza and Oral Hygiene feature events | Mean depth 23.1% and 26.1%. Break-even lift is 4.35x and 7.69x at 30% margin (§3.2). | If we cut depth from about 25% to 15% on the same featured events, margin per event rises 10% to 30% while units fall less than 25% (assumed). The feature ad, not the depth, drives most trips. | 38 vs 39 stores, 8 event weeks. Event-level MDE ≈ 15% (assumed). | Category managers: event calendar. Vendors: co-fund. Data: event-level reads. | **Gross margin $ per event.** Guardrails: event units ≥ −25%; vendor funding unchanged. | D30: 2 events read clean. D60: margin per event ≥ +5%. D90: ≥ +10% → set new depth standard; else revert. |
| 4 | **Display without discount**, Bag Snacks | Display-only weeks show median 31 vs 10 units in no-promo weeks (measured, selection-biased). Feature ads cover only 2.5% of rows. Digital-display studies average +14% (external, Grocery TV, vendor). | If we put Bag Snacks on display at full price instead of a ~19% discount, gross margin per display week rises 15% to 40% while units keep at least 60% of the deal lift (assumed). | 38 vs 39 stores, 8 weeks, 4 top Bag Snacks products. MDE ≈ 12% (assumed). | Store ops: display build. Category managers: product choice. Data: read-out. | **Gross margin $ per display week.** Guardrails: category units ≥ −5%; store-brand share. | D30: execution compliance ≥ 85%. D60: margin ≥ +10%. D90: ≥ +15% → standard practice; < 0 → kill. |
| 5 | **Store-brand price-gap test**, Cereal and Oral Hygiene | Store-brand share is 13.9% and 17.2% vs the 21.3% US benchmark (external, PLMA). Store brands sell less on promotion: 14% vs 34% of units (external, FoodNavigator/Circana). | If we hold a fixed store-brand gap (e.g., 30% below the national brand) with secondary placement, store-brand share rises 2 to 4 pts and category margin rises 1% to 3% (assumed; needs store-brand margin data). | 38 vs 39 stores, 12 weeks. MDE ≈ 1.5 share pts (assumed). | Store-brand team: pricing and placement. Finance: store-brand margin. Data: share tracking. | **Category gross margin $ and store-brand share.** Guardrails: category units ≥ −3%; national-brand vendor funding. | D30: share ≥ +0.5 pt. D60: ≥ +1.5 pts with margin ≥ 0. D90: ≥ +2 pts and margin up → scale; else revert. |

**Interference rule.** Pilots 1, 3 and 4 share no category, so they can run on the same store split. Pilots 2 and 5 both touch Cereal. Run Pilot 5 in the second 90 days, or on a separate stratified store split.

---

## §6 Roadmap, prioritisation, risks and sources

### 6.1 Roadmap

| Wave | Weeks | Initiatives | Exit gate |
|---|---|---|---|
| Wave 1: commercial quick wins | 0–8 | A1, A3, B1, B2, B3, B4, B6 | Corrected baseline signed off; break-even gate live |
| Wave 2: core pilots | 4–20 | A2, A4, Pilots 1–4 | At least 2 pilots pass Day-90 scale gates |
| Wave 3: structural flywheel | 16–52 | A5, A6, A7, A8, B5, Pilot 5, extension to other categories | Causal elasticities in the simulator; uplift-ranked promotion calendar in 4+ categories |

**The flywheel.** Every pilot adds clean, randomised price data. That data sharpens the elasticity estimates. Sharper estimates prune more waste, and the savings fund further tests.

### 6.2 Prioritisation matrix

| Initiative | Financial impact (P&L driver) | Confidence | Ease / time to value | Wave |
|---|---|---|---|---|
| B2 break-even gate + B4 depth cap | High (gross margin) | Medium: measured lifts plus assumed margins; external 75% loss rate | 2–4 weeks, low complexity | 1 |
| B3 vendor re-negotiation | High (gross margin) | Medium: depends on funding data | 4–10 weeks, medium | 1 |
| A1 data correction + B1 freeze | Risk avoidance (protects against wrong-sign pricing) | High: errors confirmed | 1–2 weeks, low | 1 |
| A3 cost and funding data | Enabler for all margin math | High | 4–6 weeks, medium | 1 |
| Pilot 1 promotion holdout | High (gross margin) | Medium-high | 4 weeks to launch, medium | 2 |
| Pilot 3 depth test | Medium-high (gross margin) | Medium | 4 weeks, medium | 2 |
| Pilot 2 everyday-price ladder | Medium (revenue, margin) | Low-medium: sign of the effect is uncertain | 6 weeks, medium-high | 2 |
| Pilot 4 display without discount | Medium (gross margin) | Low-medium: selection-biased signal | 4 weeks, medium | 2 |
| A2 leak-free simulator | Enabler (decision speed) | Medium | 6–8 weeks, medium | 2 |
| Pilot 5 + B5 store-brand gap | Low-medium (margin mix) | Medium: external benchmark is strong; no store-brand margin data | 8 weeks, medium | 3 |
| A5/A6 causal elasticity and uplift scoring | High at chain scale (margin, revenue) | Medium: depends on pilots | 20–26 weeks, high | 3 |

### 6.3 Risk table

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Someone uses the Ridge FE elasticities or the HR §6a thesis to cut prices | Medium | High: margin loss on wrong-sign evidence | B1 freeze; A1 re-issue; A5 replacement |
| The markdown is mostly vendor-funded, so Lever 1 is smaller | Medium | Medium | A3 before scaling; re-size Lever 1 from funding data |
| Promotions drive basket halo [extra items bought on the same trip] that is invisible here | Medium | Medium | Add basket margin as a Pilot 1 guardrail; A7 basket feed |
| Competitors respond to price rises | Medium | Medium | Pilot 2 caps at +5%; A7 competitor price feed |
| Store-execution error contaminates tests | Medium | Medium | Compliance audits; D30 gates |
| 2009–2011 behaviour no longer holds | High | Medium | Pilots generate current data; benchmarks are 2025–26 |
| Duplicate rows or derived base price distort baselines | Known | Low-medium | A1 de-duplication; validate base price against price files |
| Vendor pushback on fewer or shallower events | Medium | Medium | Frame as co-investment; share pilot reads |

### 6.4 Open questions (not answerable from current data)
1. Unit cost, gross margin and vendor funding by product. Every margin figure above depends on these. The 30% and 40% margins are assumed.
2. Basket halo of promoted products.
3. The true elasticity per category. Only Pilot 2 and A5 can answer it.
4. Why chart 01 and findings F1 slopes cannot be reproduced. The exploration code was not in the artifacts (FU R1 Q3).

### 6.5 Verified web sources

| URL | What I took from it |
|---|---|
| https://www.fmi.org/our-research/supermarket-facts | 2025 food-retailer net margin 2.1%; average weekly sales per supermarket $668,377; 33,248 items. |
| https://www.plma.com/article/us-private-label-industry-reached-2828-billion-sales-2025 | US store brands $282.8B in 2025; 21.3% dollar share; 23.5% unit share; +3.3% vs +1.2% for national brands. |
| https://www.foodnavigator.com/Article/2016/04/04/Four-strategies-for-overcoming-diminishing-returns-on-trade-promotions/ | About three-quarters of promotions do not break even (Nielsen); trade spend 15–20% of manufacturer gross sales (Acosta). |
| https://www.foodnavigator.com/Article/2026/06/24/private-label-hits-50-share-despite-heavy-brand-ppromotions/ | Circana, Europe: store brands 50% of units; 34% of branded units vs 14% of store-brand units sold on promotion. |
| https://www.demandtec.com/case-studies/smarter-pricing-stronger-outcomes-how-ngi-is-driving-growth-through-data-driven-strategy/ | NGI (~300 stores): +2.5% sales, units and margin dollars; 9,000+ promotions optimised weekly (vendor case study). |
| https://hexaware.com/case-study/ai-pricing-optimization-and-promotions-drive-retail-margin-improvements-for-a-leading-latin-american-convenience-retailer/ | +7% margin in test vs control stores across an 805-store scope (vendor case study, convenience retail). |
| https://grocerytv.com/meta-study/cpg/ | +14% average sales lift across 16 in-store digital display studies (vendor; method not disclosed). |

**Could not be fetched, so figures are labelled assumed.**
- McKinsey, "Using big data to make better pricing decisions" and "The power of pricing": both timed out. The roughly 8% profit-per-1%-price figure was seen only in search summaries.
- Bijmolt et al. 2005 elasticity meta-analysis: Tilburg repository returned 403. The −2.62 figure was seen only in a search abstract.
- Marketing Week UK promotions article: returned 403.
- Columbia/Kellogg elasticity PDF: not machine-readable.

---

## Glossary

| Term | Meaning |
|---|---|
| Base price | The regular, everyday shelf price before any temporary discount. |
| Basket halo | Extra items a shopper buys on a trip because a promoted item drew them in. |
| Break-even lift | The unit increase needed for a discount to earn the same margin dollars as no discount: m / (m − d). |
| CI (confidence interval) | The range that likely contains the true value. Here, 95% likely. |
| Difference-in-differences | Change in test stores minus change in control stores over the same period. It removes shared trends. |
| Display | An in-store secondary placement such as an end-cap or stand. |
| Elasticity | The % change in units for a 1% change in price. −1.5 means a 1% price rise cuts units 1.5%. |
| Feature | Inclusion in the retailer's weekly circular ad. |
| Fixed effects (FE) | Model terms that absorb each store's and product's constant baseline level. |
| Gross margin | Revenue minus cost of goods, in dollars or as a share of revenue. |
| Holdout / control group | Stores that do not get the change, so the change's effect can be measured. |
| Instrument (IV) | A price driver unrelated to demand, such as a cost change. It isolates a causal price effect. |
| Leakage | When a model input contains the answer it is trying to predict, as VISITS does here. |
| LightGBM | A gradient-boosted decision-tree model used here to forecast weekly units. |
| Log-log slope | The slope of log(units) against log(price). It reads as an elasticity only under strict conditions. |
| MAPE | Mean absolute percentage error: the average forecast miss as a % of actual units. |
| Markdown | Dollars given away by selling below the base price. |
| MDE (minimum detectable effect) | The smallest effect a test can reliably detect at its sample size. |
| Net margin | Profit after all costs as a share of sales. |
| Pull-forward | Shoppers buying ahead during a deal, which lowers later weeks' sales. |
| R² | Share of variation in the outcome that a model explains. |
| Ridge FE | A penalised regression with fixed effects. Used here for elasticities, which came out with the wrong sign. |
| SHAP | Shapley additive explanations: each input's average contribution to a model prediction. |
| Store brand (private label) | The retailer's own-label products, marked "PL" in this data. |
| Store tier | The chain's segment label for a store: Mainstream, Upscale or Value. |
| TPR (temporary price reduction) | A discount with no feature ad or display. |
| Trade spend | Money manufacturers pay retailers to fund promotions and placement. |
| Uplift | The *incremental* effect of an action vs no action, as opposed to the raw outcome. |
| UPC | Universal product code: one product at one pack size. |
| UPV (units per visit) | Units sold divided by trips that included the product. |
| Vendor funding | The part of a markdown paid by the manufacturer, not the retailer. |
