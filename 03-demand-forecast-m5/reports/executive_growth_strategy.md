# Executive Growth Strategy: Forecast-Driven Replenishment

**Project:** 03 Demand Forecast for Inventory Planning (M5 / Walmart data, 10 stores, 3,049 items)
**Prepared by:** Growth Strategy Partner
**Date:** 2026-11-04
**Inputs:** `reports/ml_handoff_report.md` (cited as "handoff §n"), `reports/ml_followups.md` (cited as "followups Qn"), 21 charts in `reports/charts/` and `reports/modeling/charts/`, and live web research (section 6).

**Evidence labels used throughout:**
- **measured**: computed from the data in the handoff or followups.
- **modeled**: a model output or association.
- **external**: a cited web source that I fetched.
- **assumed**: my estimate, or a figure I saw but could not fetch.

---

## 1. Executive thesis and diagnosis

**Bottom line: replace the four-week rule with the model's forecast, and size safety stock from the model's smaller error.**

The current rule orders too little of the fast items and too much of the slow ones. The model fixes both at once. It cuts the average daily error per item by 20% (MAE 0.862 vs 1.074 units per item-day, measured, handoff §4).

The cut is broad. It holds in every category: FOODS 21%, HOUSEHOLD 19%, HOBBIES 16% (MAE, measured, followups Q2).

**Three value levers, in order of size:**

| # | Lever | What changes | Directional impact (10 stores, per year) | Label |
|---|---|---|---|---|
| 1 | Fewer empty shelves on fast items | Model under-orders 108,337 fewer units than the rule over 28 days | $0.16M to $0.41M extra revenue | assumed (built on measured gap) |
| 2 | Leaner safety stock at the same service level | Dollar-weighted per-series error falls 20.7% | $0.10M to $0.13M one-time cash release at cost | modeled (followups R2 Q1) + assumed |
| 3 | Stop stocking the slow tail "just in case" | Round tiny forecasts to zero in HOBBIES and HOUSEHOLD | MAE falls 7% in both categories; inventory falls further | modeled (followups Q5) |

The scale matters more than the per-store number. Ten stores sell about $50.9M a year of these items (assumed: $3.90M in 28 days, measured, annualised). The levers are worth about 0.1% to 0.3% of sales in profit, plus a one-off cash release. A chain of hundreds of stores multiplies that linearly (assumed).

**The bigger prize may be hidden.** 1,267 fast series average 5+ units a day, yet logged 4,086 zero-sale days in 28 days (measured, followups R2 Q2). 213 of them had three or more zero days in a row. If those zeros are empty shelves, they cost up to about $0.72M a year (assumed: 5 units x $2.69 per zero day, annualised). Pilot 4 tests this cheaply.

**Where value leaks today (measured, followups Q3 and Q4):**
- On the busiest 10% of item-days, the rule under-forecasts 195,875 units. The model under-forecasts 129,244. That gap is 66,631 units in 28 days. These are the "fast items that run out".
- On the other 90% of item-days, the rule over-forecasts 309,403 units. The model over-forecasts 237,475. That gap is 71,928 units in 28 days. These are the "slow items we carry too much of".
- Operations' suspicion in the problem statement is therefore confirmed by the data.

**How this compares to the market:**
- Retail loses about 6.5% of sales to inventory distortion [the combined cost of empty shelves and excess stock] (external, Board/IHL).
- Fewer than 25% of retailers have deployed AI or machine learning where distortion hits (external, Board/IHL). A rule-of-thumb buyer is in the majority, but a lagging one.
- The model's 20% to 24% error cut sits at the low end of the 20% to 50% range consultancies quote (assumed; McKinsey page could not be fetched).

**Strategic lenses applied:**
- **Asymmetric error economics.** An empty shelf costs lost margin and goodwill. An extra unit costs only holding cost. So the order point should lean toward over-cover on fast items and under-cover on the slow tail.
- **Concentration (Pareto) targeting.** The top 9.3% of series carry 50% of units (measured, handoff §6). Effort should follow volume.
- **Prediction versus changing outcomes.** The model predicts demand. It does not show that a price change causes demand (handoff §5). Value only appears where the model's order differs from the rule's order.
- **Flywheel [a loop where each turn makes the next easier].** Better in-stock lifts sales. Cleaner sales data (with stockout flags) improves the next forecast. A better forecast lowers buffers and frees cash for range and price investment.

---

## 2. Internal versus external benchmarks

**The model is credible against outside evidence, but the business cannot yet measure its own in-stock rate or inventory turns.**

| Metric | This business | External benchmark | Read-across | Source |
|---|---|---|---|---|
| Forecast error cut vs incumbent method | RMSE -24.4%, MAE -19.7% (measured, handoff §4) | 20% to 50% error cut from AI forecasting (assumed: McKinsey claim seen in search results; page timed out) | Low end of range; plausible, not exceptional | [McKinsey, not fetched](https://www.mckinsey.com/capabilities/operations/our-insights/ai-driven-operations-forecasting-in-data-light-environments) |
| Inventory distortion as share of sales | Not measurable: no on-hand or stockout data (handoff §7) | 6.5% of retail sales in 2025; 9.3% in general merchandise and softgoods (external) | Open gap. Instrumentation needed | [Board / IHL](https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos) |
| Empty-shelf losses | Rule under-forecasts 9% more than it over-forecasts (measured, followups Q3) | $690.1B of global losses from empty shelves (external) | Empty shelves are the bigger leak, internally and externally | [Board / IHL](https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos) |
| AI adoption in planning | Rule-of-thumb only | Under 25% of retailers deployed; 76% of adopters report positive forecasting results (external) | Early-mover advantage still available | [Board / IHL](https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos) |
| Inventory turns | Not measurable (no on-hand data) | Walmart: 9.10 turns a year, 40 days on hand, FY ending Jan 2026 (external) | Target to track once on-hand data exists | [stock-analysis-on.net](https://www.stock-analysis-on.net/NASDAQ/Company/Walmart-Inc/Ratios/Short-term-Operating-Activity) |
| SNAP [federal food-benefit] day lift, FOODS | +14.8% units per item-day on SNAP days, test window (measured, followups Q6); 10% to 20% by state (measured, handoff §3) | Food sales +5.6% in full-issuance weeks for the average grocer; +19.2% in high-SNAP ZIP codes (assumed: paper PDF blocked; abstract confirms "large" cycles) | Internal lift sits within the external range | [Goldin, Homonoff, Meckel, AEJ: Policy 2022](https://econpapers.repec.org/RePEc:aea:aejpol:v:14:y:2022:i:1:p:152-78) |
| Retail out-of-stock rate | Unknown | 8.3% average; 72% of stockouts caused in-store (assumed: Gruen and Corsten, seen in search, not fetched) | Used only as a scenario input below | none fetched |
| Safety stock service factor | No service target set (handoff §7) | z = 1.65 at 95%, 2.05 at 98%, 2.33 at 99% (external) | Used to size buffers in section 3 | [Cleverence](https://www.cleverence.com/articles/business-blogs/safety-stock-retail-inventory-4827/) |

**Competitor and market moves (external unless stated):**
- Walmart runs real-time AI for demand forecasting, moves stock to high-need areas, and targets lower overstock. It has rolled this out beyond the US ([Fortune, July 2025](https://fortune.com/2025/07/23/walmart-amazon-ai-supply-chain-retail/)).
- Amazon credits an AI demand-forecasting model as the core of its supply chain (same Fortune source).
- IHL reports that firms which systematically fix workflows cut inventory errors by over 25% ([Board / IHL](https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos)).
- Retailers do not change prices around SNAP surges, per the Goldin et al. abstract. The winning move is stock, not price ([econpapers](https://econpapers.repec.org/RePEc:aea:aejpol:v:14:y:2022:i:1:p:152-78)).

**What I could not verify:** the official M5 [the forecasting competition behind this data] winning score; McKinsey's primary figures; a grocery-specific carrying-cost rate; the Gruen and Corsten stockout figures. All are labelled assumed where used.

---

## 3. Data to dollars

### 3.1 Segment economics

**FOODS carries the money; HOBBIES carries the waste risk.**

| Category | Units, 28 days | Sales, 28 days | $ per unit | Zero-sale days | Model MAE gain vs rule | Role |
|---|---|---|---|---|---|---|
| FOODS | 832,488 | $2,235,403 | $2.69 | 44.8% | 21% | Compounding engine: high volume, SNAP and weekend peaks |
| HOUSEHOLD | 283,420 | $1,162,334 | $4.10 | 60.2% | 19% | Steady middle; HOUSEHOLD_2 is a long tail (~80% zero days) |
| HOBBIES | 115,856 | $503,239 | $4.34 | 68.2% | 16% | Cash trap risk: HOBBIES_2 ~88% zero days |
| **Total** | **1,231,764** | **$3,900,976** | **$3.17** | **~50%** | **20%** | |

Labels: units, sales and $ per unit measured (followups Q1); zero rates measured (handoff §4); department zero rates read from `charts/01_zero_rate_by_category.png` (measured); MAE gains measured against the reconstructed rule (followups Q2).

**Where effort is misallocated:**
- The busiest 10% of item-days hold 53.3% of units (measured, handoff §6). The rule's misses there are mostly shortfalls.
- The bottom 70% of series hold about 20% of units (measured, handoff §6). The rule over-orders there.
- Store WI_2 has the worst error, RMSE 2.354 units per item-day (measured, handoff §4). CA_3 is next at 2.080 (measured, `test_by_store.csv`). Both deserve an operations review.
- FOODS demand peaks Saturday and Sunday at about 1.96 to 1.98 units per item-day, versus about 1.45 midweek (measured, read from `charts/03_demand_category_weekday.png`). The rule already keys on weekday, so this is not the main leak.
- Both forecasters miss more on SNAP days (model MAE 1.158 vs 1.070; rule 1.468 vs 1.353, measured, followups Q6). SNAP is under-served by both.

### 3.2 Traits versus levers

**Almost everything the model uses is a trait to target on, not a lever to pull.**

| Driver | Mean SHAP [average contribution to a forecast], units | Type | How to use it |
|---|---|---|---|
| 7-day average sales (`roll_mean_7`) | 1.30 (modeled) | Trait | Rank items for attention; drives order size |
| Recent volatility, yesterday's sales, weekday | 0.06 to 0.10 each (modeled) | Trait | Size safety stock; schedule deliveries |
| Item's long-run average (`series_mean`) | ~0.04 (modeled) | Trait | Velocity tiering (fast / mid / slow) |
| SNAP day flag | 0.026 (modeled) | Semi-lever: date is fixed, stock response is controllable | Pre-position FOODS before SNAP days |
| Shelf price | 0.007 (modeled) | Lever, but not causal here | Do not use for pricing (see below) |
| Price vs 4-week average | 0.001 (modeled) | Lever, but not causal here | Do not use for pricing |

Source: handoff §5 and `charts/06_shap_importance.png`.

The controllable levers are operational, not in the model. They are: order quantity, safety stock, delivery cadence, range breadth, and shelf allocation. The model informs all five.

**Warning on price.** A 10% price cut and a 10% price rise both associate with about +0.02 units per item-day (modeled, `charts/08_counterfactuals.png`). That is a timing artefact: promotions land in busy weeks. No pricing decision should rest on it.

### 3.3 Turning error into dollars

**At a 95% to 98% service level, the model frees about $102K to $127K of stock at cost across 10 stores.**

Safety stock [spare units held to cover forecast misses] equals a service factor times forecast error over the lead time. So a 24% smaller error means a 24% smaller buffer at the same service level.

| Item | Rule | Model | Difference | Label |
|---|---|---|---|---|
| Forecast error, RMSE, units per item-day | 2.259 | 1.707 | -24.4% | measured (handoff §4) |
| Pooled: buffer per series at 95% (z 1.65, 7-day lead time) | 9.86 units | 7.45 units | -2.41 units | modeled; lead time assumed |
| Pooled: buffer released, 30,490 series, 95% | | | 73,450 units = $175K at cost | assumed 75% cost ratio on $3.17 |
| Pooled: buffer released, 30,490 series, 98% (z 2.05) | | | 91,290 units = $217K at cost | same assumptions |
| Per-series error x price, summed over 30,490 series | $150,842 | $119,635 | -20.7% | measured (followups R2 Q1; rule reconstructed) |
| Buffer at 95%, per-series (z 1.65 x sqrt 7 = 4.37) | $658K at retail | $522K at retail | $136K retail = $102K at cost | modeled; assumed 75% cost ratio |
| Buffer at 98%, per-series (z 2.05 x sqrt 7 = 5.42) | $818K at retail | $649K at retail | $169K retail = $127K at cost | same assumptions |
| Annual holding cost saved at 25% a year (per-series basis) | | | $26K to $32K | assumed rate |

Use the per-series rows. The pooled rows over-state the release because big errors on fast, cheap FOODS dominate the pooled figure. The per-series sum treats errors as independent, so it is a dispersion measure, not a stock count (followups R2 Q1 caveat). Both rows assume a 7-day lead time.

The current rule also adds a "generous" buffer (problem statement). Its size is unknown. If it exceeds the statistical buffer, the real release is larger.

**Lost sales: a scenario, not a measurement.** No stockout data exists (handoff §7, issue 1).
- Assume 8% of demand meets an empty shelf (assumed, Gruen and Corsten, unfetched).
- Assume 40% of that demand is lost to the store (assumed; switch-store plus no-purchase shares).
- Lost sales today would then be about $1.63M a year on $50.9M (assumed).
- If better forecasts cut stockouts 10% to 25%, revenue rises $0.16M to $0.41M a year (assumed). That is well below the "up to 65%" consultancy claim.
- At an assumed 25% gross margin, that is $41K to $102K of gross profit a year.

The upper bound on exposure is clear. The model under-forecasts 108,337 fewer units than the rule over 28 days (measured, followups Q3). At $3.17 per unit, that is $343K of demand at risk per 28 days (measured units x measured price). Most of it is covered by buffers today, which is why the inventory lever and the lost-sales lever trade off.

### 3.4 Profit-maximising order thresholds

**Set the service level by tier, using the cost of a miss versus the cost of a spare unit.**

The newsvendor rule [the textbook stocking rule] says: stock up to the demand level you will meet with probability Cu / (Cu + Co).
- Cu is the cost of a unit short: lost margin, plus lost basket and goodwill.
- Co is the cost of a unit over: holding cost, plus spoilage or markdown.

| Tier | Example | Cu per unit (assumed) | Co per unit per week (assumed) | Implied service target | Recommended target |
|---|---|---|---|---|---|
| Fast movers, shelf-stable | Top-decile FOODS_3 | $0.67 (25% margin on $2.69) | ~$0.01 holding | >98% | 98% |
| Fast movers, perishable | Fresh FOODS | $0.67 | $0.30+ with spoilage | ~70% to 90% | 90%, review weekly |
| Mid velocity | Most HOUSEHOLD | $1.03 (25% on $4.10) | ~$0.02 plus slow markdown | ~95% | 95% |
| Slow tail | HOBBIES_2, HOUSEHOLD_2 | $1.09 (25% on $4.34) | High: obsolescence, shelf space | 85% to 90% | 90%, minimum display only |

The second threshold is the order cutoff. Rounding forecasts under 0.5 units to zero cuts MAE 7% in HOBBIES and HOUSEHOLD (modeled, followups Q5). It raises RMSE slightly (1.707 to 1.715, modeled). Use rounding for order quantities only, never for volume planning.

**Velocity tiers for policy (measured, followups R2 Q3; tier = training-period mean units per day):**

| Tier | Series | Share of series | Share of test units | FOODS / HOUSEHOLD / HOBBIES series |
|---|---|---|---|---|
| Fast (5+ a day) | 1,267 | 4.2% | 30.5% | 932 / 249 / 86 |
| Mid (1 to under 5) | 7,984 | 26.2% | 43.5% | 5,153 / 2,087 / 744 |
| Slow (under 1) | 21,239 | 69.7% | 26.0% | 8,285 / 8,134 / 4,820 |

The slow tier is 70% of series but 26% of units. That is where buffers should shrink. The fast tier is 4% of series but 31% of units. That is where shelves must never run dry.

---

## 4. Recommendations by track

### Track A: technical, product and AI

**Put the model into the nightly order run, with a permanent holdout to prove its worth.**

1. **Nightly batch integration.** Write the 28-day item-store-day forecast and each series' recent error into the replenishment system. Orders = forecast over the lead time plus a tiered buffer.
2. **Human review only by exception.** Store managers see only orders where model and rule differ by more than an agreed amount. This keeps workload low and builds trust.
3. **Measure the change, not the forecast.** Value only arises where the model's order differs from the rule's. Keep 10% of series on the rule as a permanent holdout [a group deliberately left untreated to measure impact]. This is the replenishment version of uplift targeting [acting only where action changes the outcome].
4. **Round the slow tail.** Apply the under-0.5 rounding to order quantities. Plan a two-part model [first predicts "any sale or not", then "how many"] at the next refresh (handoff §7).
5. **Feed SNAP intensity per store.** Today SNAP is one flag for a whole state. Weight it by store-area participation from public USDA data (handoff §7, issue 8).
6. **Instrumentation to capture next**, in priority order:
   - Daily on-hand stock per item-store, and a stockout flag (handoff §7, issue 1).
   - Receipts, lead times, waste and markdown per item.
   - Shelf capacity and minimum display quantities.
   - Store-level SNAP participation.
7. **Drift guardrails [automatic checks that the model is still working].**
   - Retrain monthly on a rolling two-year window (handoff §7, issue 4).
   - Alert if the MAE gain over the holdout falls below 10% for two weeks running.
   - Alert if total forecast bias drifts beyond plus or minus 5%. Today it is within 0.5% (measured, handoff §6).
   - New items use the category median for 28 days (handoff §7, issue 5).

### Track B: commercial, operations and finance

**Five changes can start this month, before the model is live.**

1. **Set an explicit service target by velocity tier.** None exists today (handoff §7). Use the table in section 3.4. Finance owns the carrying-cost rate; merchandising owns the targets.
2. **Add a SNAP uplift to the current rule for FOODS.** Raise FOODS orders for SNAP days by about 15% (measured lift 14.8%, followups Q6). Land stock one day before. This is a spreadsheet change.
3. **Cut buffers on the slow tail now.** Lower the buffer on HOBBIES_2 and HOUSEHOLD_2. Move them to weekly review and minimum display stock. Start a range review of series with more than 85% zero-sale days.
4. **Run an operations review in WI_2 and CA_3.** These stores have the largest errors (measured, section 3.1). Check receiving, shelf capacity and data quality before blaming demand.
5. **Change the scorecard.** Add GMROI [gross margin return on inventory: gross profit per dollar of stock] and in-stock rate to buyer and store goals. Today's rule rewards "never run out", which hides overstock cost.
6. **Freeze price-based promo cases.** Until a price test runs, do not justify promotions with the model's price association (handoff §5).

---

## 5. The 90-day growth lab: five pilots

Design note: there are only 10 stores, so store-level tests lack power. Randomise at the item-store series level within stores, stratified by category and velocity. This gives thousands of units per arm. Shared backroom and truck capacity create small spillover; accept and monitor it.

### Pilot 1: Model-driven replenishment on the top third

- **Playbook:** forecast-led ordering with a holdout.
- **Trigger:** top 32.9% of series hold 80% of units (measured, handoff §6). Rule under-forecasts 52% more than the model in the top decile (measured, followups Q4). External: AI forecasting adopters report positive results 76% of the time (external, Board/IHL).
- **Hypothesis:** If we order the top-third series from the model with tiered buffers, inventory dollars per dollar of sales fall 8% to 15% at equal in-stock, because buffers shrink with a 24% smaller error (assumed range; modeled mechanism).
- **Design:** the fast and mid tiers: 9,251 series holding 74% of units (measured, followups R2 Q3). Random 50/50 split: about 4,625 per arm. Stratify by store, category and tier. Assuming a coefficient of variation of 1 in per-series inventory, the minimum detectable change is about 6% (assumed). Run 8 weeks minimum.
- **Who does what:** Data builds the nightly feed, buffer logic and dashboard. Operations runs ordering. Finance sets carrying cost. Store managers handle exceptions.
- **North Star [the one metric that decides success]:** average on-hand inventory dollars per dollar of sales.
- **Guardrails:** in-stock rate on treated series, units sold per series, waste on perishables, manager override rate.
- **Decision rules:**
  - Day 30: kill if in-stock falls more than 1 point below control. Pivot buffers if inventory is not down at least 3%.
  - Day 60: scale to all top-third series if inventory is down at least 8% and in-stock is flat or better.
  - Day 90: scale chain-wide if the day-60 result holds and override rate is under 10%.

### Pilot 2: SNAP pre-positioning for FOODS

- **Playbook:** calendar-triggered stock build.
- **Trigger:** FOODS sells 14.8% more per item-day on SNAP days, and both forecasters miss more then (measured, followups Q6). External: SNAP weeks lift food sales 5.6% on average and 19.2% in high-SNAP areas (assumed, paper not fetched).
- **Hypothesis:** If we raise FOODS orders before SNAP days on fast and mid series, SNAP-day units sold rise 1% to 3% with no rise in post-SNAP excess, because shelves stop running dry at the peak (assumed range).
- **Design:** FOODS series in the fast and mid tiers. Random 50/50 split by series within store. Cover at least three monthly SNAP cycles (about 90 days). Analyse by state, since SNAP calendars differ.
- **Who does what:** Data adds store-level SNAP intensity. Operations schedules deliveries. Merchandising checks perishables.
- **North Star:** FOODS units sold per series on SNAP days.
- **Guardrails:** on-hand stock three days after SNAP, spoilage and markdowns, zero-sale days on fast series.
- **Decision rules:**
  - Day 30: kill if post-SNAP stock rises more than 10% with no sales gain.
  - Day 60: iterate the uplift factor by state if gains differ.
  - Day 90: scale if SNAP-day sales are up at least 1% with guardrails flat.

### Pilot 3: Slow-tail order rounding and minimum display

- **Playbook:** cost-to-serve cut on the long tail.
- **Trigger:** HOBBIES_2 has about 88% zero-sale days, HOUSEHOLD_2 about 80% (measured, `charts/01`). Rounding cuts MAE 7% in both (modeled, followups Q5). External: general merchandise has the highest distortion rate at 9.3% of sales (external, Board/IHL).
- **Hypothesis:** If we round tiny forecasts to zero and hold minimum display stock on slow series, inventory dollars fall 5% to 15% with sales down less than 2%, because we stop topping up items that rarely sell (assumed).
- **Design:** slow-tier HOBBIES and HOUSEHOLD series: 12,954 (4,820 + 8,134, measured, followups R2 Q3). Random 50/50 split by series within store. Run 12 weeks; slow items need longer to show.
- **Who does what:** Data applies rounding. Merchandising sets display minimums. Category managers own range calls.
- **North Star:** inventory dollars per series.
- **Guardrails:** units sold per series, share of series with zero stock, customer complaints.
- **Decision rules:**
  - Day 30: kill if sales fall more than 5%.
  - Day 60: iterate the cutoff (0.3 or 0.7) if sales fall 2% to 5%.
  - Day 90: scale if inventory is down at least 5% and sales fall under 2%.

### Pilot 4: Hidden-stockout audit

- **Playbook:** measurement sprint that unlocks the flywheel.
- **Trigger:** zero sales cannot be told apart from empty shelves (handoff §7, issue 1). Fast series (5+ units a day) still logged zero on 11.5% of test days; 213 series had runs of 3+ zero days, 152 of them FOODS (measured, followups R2 Q2). External: empty shelves are the largest single distortion loss, $690.1B (external, Board/IHL).
- **Hypothesis:** If we check the shelf on zero-sale days for fast series, we will find that at least 20% of those zeros are stockouts, so true demand is under-stated (assumed).
- **Design:** all 10 stores, the 1,267 fast series, with the 213 run-of-zeros series checked first. Four weeks. Daily shelf check of any fast series that sold zero the day before. Expect about 150 checks a day chain-wide (measured: 4,086 zero days / 28).
- **Who does what:** Store teams do checks. Data supplies the daily list and logs results.
- **North Star:** share of fast-series zero-sale days that were stockouts.
- **Guardrails:** staff hours per store per day.
- **Decision rules:**
  - If over 20%: fund stockout flags chain-wide and retrain on corrected demand.
  - If 5% to 20%: flag only the top decile.
  - If under 5%: close; zeros are true demand.

### Pilot 5: Randomised price test (Wave 3)

- **Playbook:** causal price measurement.
- **Trigger:** the model's price signal is an association only (handoff §5, `charts/08`).
- **Hypothesis:** If we randomly move prices by plus or minus 5% on selected FOODS items, we can estimate elasticity [how much demand moves per 1% price change] within plus or minus 0.3 (assumed precision).
- **Design:** 100 to 200 FOODS items. Random price arm by item-week across stores. 12 weeks. Needs pricing sign-off.
- **Who does what:** Pricing sets arms. Data analyses. Finance reviews margin.
- **North Star:** elasticity estimate with its confidence interval.
- **Guardrails:** category gross margin, price-perception complaints.
- **Decision rules:** stop early if category margin falls more than 1 point. At day 90, use the estimate in promotion planning only if the interval excludes zero.

---

## 6. Prioritisation and sources

### 6.1 Prioritisation matrix

**Start with the free commercial fixes and the stockout audit; run Pilot 1 as the core bet.**

| Initiative | Financial impact (driver) | Confidence | Ease / time to value | Wave |
|---|---|---|---|---|
| Tiered service targets (B1) | Med (working capital, gross margin) | High: textbook rule, measured error | 2 weeks; finance plus merchandising | 1 |
| SNAP uplift on current rule (B2) | Med (revenue, FOODS) | Med-High: measured lift, external support | 1 to 2 weeks; spreadsheet | 1 |
| Slow-tail buffer cut and range review (B3) | Med (working capital) | Med: measured zero rates | 4 weeks; category teams | 1 |
| WI_2 / CA_3 operations review (B4) | Low-Med (revenue) | Med: measured error, cause unknown | 2 weeks | 1 |
| GMROI scorecard (B5) | Med (gross margin, long run) | Med | 1 quarter; HR and finance | 1 |
| Pilot 4: hidden-stockout audit | High indirectly (unlocks true demand) | High as a measurement | 1 week to launch; 4 weeks run | 1 |
| Pilot 1: model replenishment, top third | High (revenue and working capital) | High: 20-24% error cut on held-out test | 6 to 8 weeks to launch | 2 |
| Pilot 3: slow-tail rounding | Med (working capital) | Med: modeled MAE gain | 3 to 4 weeks | 2 |
| Pilot 2: SNAP pre-positioning | Med (revenue) | Med: 28-day descriptive evidence | 4 weeks; 90-day run | 2 |
| Stockout flags and on-hand feed (A6) | High (enables all later gains) | High | 1 to 2 quarters; IT build | 3 |
| Pilot 5: price test | Med-High (gross margin) | Low today; that is the point | 1 quarter; sign-off needed | 3 |
| Two-part model, store SNAP intensity (A4, A5) | Med (accuracy) | Med | Next model refresh | 3 |

### 6.2 Verified web sources (fetched)

| Source | What I took from it |
|---|---|
| [Board blog on IHL distortion study](https://www.board.com/blog/the-1-7-trillion-wake-up-call-why-retail-planning-must-move-beyond-silos) | $1.7T distortion; 6.5% of sales; $690.1B from empty shelves; 9.3% in general merchandise; under 25% AI adoption; 76% positive results |
| [Fortune, July 2025](https://fortune.com/2025/07/23/walmart-amazon-ai-supply-chain-retail/) | Walmart real-time AI forecasting and overstock reduction; Amazon AI forecasting model |
| [stock-analysis-on.net, Walmart ratios](https://www.stock-analysis-on.net/NASDAQ/Company/Walmart-Inc/Ratios/Short-term-Operating-Activity) | Walmart 9.10 inventory turns and 40 days on hand, FY ending Jan 2026 |
| [econpapers: Goldin, Homonoff, Meckel (2022)](https://econpapers.repec.org/RePEc:aea:aejpol:v:14:y:2022:i:1:p:152-78) | Large SNAP-driven monthly food-spend cycles; retailers do not adjust price |
| [Cleverence safety stock guide](https://www.cleverence.com/articles/business-blogs/safety-stock-retail-inventory-4827/) | Safety stock = z x lead-time demand error; z values by service level |
| [IDEAS/RePEc: M5 results paper](https://ideas.repec.org/a/eee/intfor/v38y2022i4p1346-1364.html) | M5 scope: 42,840 series, 30,490 bottom-level forecasts; no scores in abstract |

**Seen but not fetched (all labelled assumed):** McKinsey forecasting article (timed out twice); NYU Wagner SNAP paper PDF (blocked, 403); IHL product page (blocked, 403); Gruen and Corsten stockout study (search only); carrying-cost rates of 20% to 30% (vendor pages, search only).

---

## 7. Open questions

**Two rounds of questions went to the statistician; all nine were answered in `reports/ml_followups.md`.** What remains open:

| # | Open item | Why it matters | Who closes it |
|---|---|---|---|
| 1 | The exact current rule, including its buffer, is not stored. Rule figures use a reconstruction (RMSE 2.219 vs 2.259 in the handoff) | The true inventory release could be larger | Operations: share the live formula |
| 2 | No on-hand stock, receipts or stockout flags | Inventory turns, distortion and lost sales cannot be measured | IT build (Track A6); Pilot 4 |
| 3 | Lead time, cost ratio, gross margin and carrying-cost rate are assumed (7 days, 75%, 25%, 25%) | Every dollar figure in section 3 scales with them | Finance |
| 4 | SNAP evidence is a single 28-day window | SNAP lift could vary by month | Pilot 2 |
| 5 | Handoff §6 "series count" column counts items, not series. True series: FOODS 14,370, HOUSEHOLD 10,470, HOBBIES 5,650 (followups R2 correction) | Units and errors unaffected; this memo uses the corrected counts | Statistician (noted) |

---

## 8. Glossary

| Term | Meaning |
|---|---|
| Buffer / safety stock | Spare units held to cover forecast misses |
| Carrying (holding) cost | Annual cost of holding stock: capital, space, shrink; % of stock value |
| Coefficient of variation | Standard deviation divided by the mean |
| Critical ratio / newsvendor rule | Stock to the demand level met with probability Cu / (Cu + Co) |
| Cu / Co | Cost of being one unit short / one unit over |
| Decile | One tenth of a ranked list |
| Elasticity | Percentage change in demand for a 1% change in price |
| Flywheel | A loop where each turn makes the next easier |
| GMROI | Gross margin return on inventory: gross profit per dollar of average stock |
| Gross margin | Sales minus cost of goods, as a share of sales |
| Guardrail metric | A metric that must not get worse during a test |
| Holdout | A group kept on the old method to measure impact |
| In-stock rate | Share of item-store-days with stock on the shelf |
| Inventory distortion | Combined cost of out-of-stocks and overstocks |
| Inventory turns | Cost of goods sold divided by average inventory |
| Lead time | Days from placing an order to stock on the shelf |
| MAE | Mean absolute error: average size of a miss, units per item-day |
| Minimum detectable change | Smallest effect a test can reliably detect |
| North Star metric | The one metric that decides a pilot's success |
| RMSE | Root mean squared error: average miss that weights big misses more |
| RMSSE / WRMSSE | Error relative to a naive forecast; W = weighted by dollar sales |
| Rule of thumb | Current method: same-weekday average of the last four weeks, plus buffer |
| Service level | Probability that stock covers demand in a cycle |
| SHAP | A method that splits each forecast into feature contributions |
| SNAP | US federal food benefit; paid on set calendar days by state |
| Stockout | Item has no stock on the shelf |
| Stratified randomisation | Random split done within groups so arms stay balanced |
| Uplift targeting | Acting only where the action changes the outcome |
| Working capital | Cash tied up in operations, here mainly inventory |
| z (service factor) | Multiplier on error that sets the service level, e.g. 1.65 for 95% |
