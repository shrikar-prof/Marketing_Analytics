# Executive Growth Strategy: Discount Leakage Audit
**Project:** 02 Discount Leakage Audit, Dunnhumby Complete Journey
**Author:** Growth-Strategy Partner
**Date:** 2026-10-28
**Inputs:** `reports/ml_handoff_report.md` (cited as "Handoff s.N"), `reports/ml_followups.md` (cited as "Follow-up Qn" for round 1, "Follow-up R2-Qn" for round 2), charts in `reports/charts/`, live web sources listed in Section 6.

**Evidence labels.** Every number carries one label. *Measured* = computed from the data by the statistician. *Modeled* = a model association, not a proven cause. *External* = a cited web source with URL. *Assumed* = my estimate, stated so you can change it.

**Scope warning.** All dollars cover the loyalty panel only: 2,467 households, 437 stores, one year (Handoff s.2). They are not chain totals. To scale, multiply the per-household figures by the chain's active loyalty households. I do not know that number.

**Corrections to the handoff, used here.** The statistician confirmed four fixes (Follow-up, corrections section). The test window is 14 weeks, so the model saving annualises to $76.5K, not $82.3K. Handoff s.7a shows modeled, not actual, dollars; the actual figures are used here. Decile dollars are taken from `tables/01`. F2's "2.9% vs 16.6%" are medians.

---

## 1. Executive Thesis and Strategic Diagnosis

### Bottom line

**The chain does not have a promotion problem everywhere. It has a depth problem on a short list of products, and it cannot yet prove any promotion pays back.**

- The chain gives away $797K a year, 15.7% of $5.06M list revenue [measured, Handoff s.1]. That is $323 per panel household per year [measured: $797,186 / 2,467].
- Most of it is deep. Lines discounted 25% or more hold 75.8% of discount dollars [measured, Follow-up Q2].
- Discount above a 25% depth ceiling is $227.6K a year, 28.5% of all discount dollars [measured, Follow-up Q2]. That is the gross pool a depth cap can touch.
- Lines 25%+ deep average 40.1% off on $1.51M of list [measured, Follow-up R2-Q1]. At an assumed 33% front margin, they sell about $107K a year below cost [assumed].
- Half the above-ceiling dollars sit in just 383 SKUs [measured, Follow-up R2-Q4].
- For scale: US food retailers keep about 1.7 cents of net profit per sales dollar [external, FMI 2025]. The above-ceiling pool equals 5.3% of pocket revenue [measured: $227.6K / $4.27M]. That is roughly three times a typical grocer's entire net margin.

### Top three value levers

| # | Lever | What changes | Directional annual impact (panel) | Label |
|---|---|---|---|---|
| 1 | **Depth ceiling on deep retailer-funded markdowns** | Cap retailer-paid depth at 25% unless a supplier funds the rest or a test proves payback | $76K (model-targeted) to $228K (gross ceiling, no volume loss); planning case about $100K-$150K net | modeled / measured / assumed |
| 2 | **Supplier funding recovery** | Ask national-brand suppliers to fund depth beyond 20% on the top SKUs | 5-10% of national-brand discount dollars ($618K) = $31K-$62K | measured base, assumed rate |
| 3 | **Mailer promotion payback discipline** | Every mailer event must pass a hold-out payback test within two cycles | Protects $360K of mailer-linked discount; the recoverable share is unknown until tested | measured base, open question |

Lever 1 is gross margin. Lever 2 is gross margin with no price change for shoppers. Lever 3 is capital allocation: it moves promotion money from events that lose to events that earn.

### Internal vs market diagnosis

**Value leaks through depth, not breadth.** Promoted lines carry 31.2% depth versus 10.3% off-promotion [measured, Handoff s.4 F3; chart `04_promoted_vs_not.png`]. Mailer-only lines run 34.4% deep and hold $255.9K [measured, Follow-up Q6].

**The dollar pool is in GROCERY, not TOYS.** TOYS has the highest rate, 43.4%, but under $1K of dollars [measured, Follow-up Q1]. GROCERY holds 58.9% of discount dollars ($469.6K). MEAT and MEAT-PCKGD add 21.3% ($170.2K) [measured, Follow-up Q1]. Chart `02_leakage_by_department.png` ranks by rate, so it overstates TOYS. Read it by dollars.

**The top categories are traffic staples.** Soft drinks ($63K, 25.8% deep), beef ($39K), chicken ($34K, 39.3% deep), milk ($28K) lead the dollar list [measured, exploration chart `05_top_categories_disc_dollars.png`]. These are classic traffic drivers. Cutting them blindly risks trips. That is why the cap needs a test, not a decree.

**Half the leakage has no promotion record.** Lines with no matching promotion event still hold 48.5% of discount dollars at a 10.3% rate [measured, Follow-up Q6]. These are "silent" loyalty-card markdowns. No one plans or reviews them as promotions.

**Payback is unproven, and the market says most promotions fail.** Nielsen found almost three-quarters of US promotions do not break even [external, FoodNavigator 2014]. BCG reports 20-50% of retail promotions give no lift, and another 20-30% do not cover their cost [external, BCG 2015]. This chain has no incremental-sales measure at all [measured gap, Handoff s.8 item 1].

**Supplier funding looks almost absent, which is suspicious.** Only 0.4% of list is supplier-funded in the data [measured, Handoff s.4 F1]. Off-invoice and scan-back money is usually booked outside the till. So "97% retailer-funded" may overstate true cost. It may also mean funds go unclaimed. One study found retailers claim only about half of available trade funds [external, Grocery Dive].

**Households are not the lever.** Income explains 5% of variation (eta-squared 0.052) [measured, Handoff s.4 F5]. The top 10% of households by rate take only 12.9% of discount dollars [measured, Follow-up Q8]. Target products, not people.

**Stores are not the lever either.** Store rates run 13.8% (10th percentile) to 18.5% (90th) across 108 sizeable stores. Only 4 exceed 20% [measured, Follow-up Q5]. A store ceiling would touch little.

### Strategic lenses applied

| Lens | Why it fits this data |
|---|---|
| Pricing waterfall (the walk from list price to cash kept) | The core question is where list dollars leak. Chart `01_price_waterfall.png` is the base. |
| Bain "earned vs bought" growth | Deep markdowns buy volume. The test is whether that volume would have come anyway. |
| BCG portfolio and category roles | Traffic categories (meat, soft drinks) deserve investment. Others are cash traps if promoted deep. |
| Uplift targeting (aim spend only where it changes behaviour) | The model predicts depth, not payback. Hold-out tests must find which promotions change purchases. |
| Asymmetric error costs | A missed deep promotion costs real margin. A wrongly flagged one costs review time or lost trips. |
| Flywheel (a loop where each output feeds the next input) | Margin recovered from bad depth can fund lower everyday prices on traffic items. That builds trips without markdown dependence. |

---

## 2. Internal vs External Benchmark Gap Analysis

**The chain's promotion intensity is normal for US grocery. Its problem is depth and the lack of payback proof.**

| Metric | This chain (panel) | External benchmark | Gap reading |
|---|---|---|---|
| Share of lines or sales on promotion | 22.5% of lines promo-matched [measured, Follow-up Q6] | 24.4% of US food sales sold on deal in 2022, 31% in 2019 [external, [FoodNavigator / Bernstein](https://www.foodnavigator.com/Article/2022/12/21/2022-in-review-Rampant-inflation-the-end-of-the-honeymoon-period-for-plant-based-meat-and-added-sugar-under-attack?page=4)] | In line. Breadth is not the issue. |
| Promotions' share of revenue | Not computed on a revenue basis | 10-45% of revenue at brick-and-mortar retailers [external, [BCG 2015](https://www.bcg.com/en-us/publications/2015/retail-pricing-how-retailers-can-improve-promotion-effectiveness.aspx)] | Not comparable yet. |
| Depth on promoted lines | 31.2% (all promo); 34.4% mailer-only; 36.5% mailer plus display [measured, Handoff s.4 F3; Follow-up Q6] | BCG egg example: a 30% single-unit cut beat a 50% cut on margin [external, BCG 2015] | Mailer depth sits at or above the depth BCG found optimal. Trails. |
| Promotions that fail to break even | Unknown: no incrementality measure [measured gap, Handoff s.8] | Almost three-quarters of US promotions [external, [FoodNavigator / Nielsen 2014](https://www.foodnavigator.com/Article/2014/10/09/Three-quarters-of-CPG-promotions-don-t-break-even-Nielsen)] | Blind spot. Assume the market rate until tested. |
| Supplier-funded share of discount | 2.5% ($20K of $797K) [measured, Handoff s.1] | Retailers claim only about half of available trade funds [external, [Grocery Dive](https://www.grocerydive.com/news/grocery--study-25-of-retailers-increased-ad-budgets-but-left-funds-unclaimed/534857/)] | Likely under-recorded or under-claimed. Must verify off-system. |
| Net profit margin | Not in data | 1.7% for US food retailers [external, [FMI 2025](https://www.fmi.org/newsroom/latest-news/view/2025/07/15/fmi-report--amid-uncertainty--food-industry-succeeds-in-offering-shoppers-value)] | Discount (15.7% of list) is about nine times a typical net margin. |
| Gross margin | Not in data | Kroger 22.3% of sales, FY2024 [external, [Kroger IR](https://ir.kroger.com/news/news-details/2025/Kroger-Reports-Fourth-Quarter-and-Full-Year-2024-Results-Announces-Guidance-for-2025/)] | Used to set my 33% list-price margin assumption (Section 3). |
| Margin gain from better promotion management | Modeled $76.5K = 1.8% of pocket revenue [modeled, Follow-up Q3] | 2-5 points of promotion margin [external, BCG 2015]; 8% margin gain at a regional grocer (vendor claim) [external, [Antuit case](https://www.casestudies.com/company/antuit/case-study/regional-grocery-chain-optimizes-promotion-pricing-to-compete-more-effectively)] | Our estimate sits at the low end. Credible, likely conservative. |
| Where promotion volume comes from | Promo-week units 4.5x non-promo weeks (median, top SKUs; not causal) [measured, Follow-up Q4] | About 75% of a brand's promotional lift is brand switching; 25% is extra category demand [external, [Bell, Chiang, Padmanabhan 1999](https://ideas.repec.org/a/inm/ormksc/v18y1999i4p504-526.html)] | Most of the 4.5x is likely shoppers switching brands inside the same store. |

### Competitor plays and market shifts

- **Fewer, better promotions.** BCG's playbook: set a goal per promotion, set spend by category role, measure true incremental ROI, cut or fix weak events, and get supplier funding for deep ones [external, BCG 2015]. Its case grocer added $166M a year in profit.
- **Private label as the margin engine.** Kroger credits its own brands for its gross margin rise to 22.3% [external, Kroger IR]. It launched over 900 new own-brand items in 2024.
- **Media income.** Kroger's alternative profit businesses, led by media, earned $1.35B of operating profit [external, Kroger IR]. Supplier money is moving from price cuts into paid media on retailer data.
- **Lower promotion share after inflation.** On-deal share fell from 31% (2019) to 24.4% (2022) [external, FoodNavigator / Bernstein]. Shoppers still say they worry about food prices [external, FMI 2025]. Pulling depth must be selective, not across the board.
- **Personalised offers.** Kroger's 84.51 unit reports 10-15% redemption on personalised offers. I could not fetch that page (HTTP 403). Treat it as unverified.

---

## 3. Data-to-Dollars Translation

### 3a. Where value compounds and where it leaks

**A small set of deep, mailer-driven SKUs in meat and grocery staples carries most of the margin risk.**

| Segment | Discount $ / year | Rate | Reading | Label |
|---|---|---|---|---|
| GROCERY department | $469.6K (58.9%) | 16.9% | Biggest pool; rate near average. Win here by trimming depth on the top SKUs. | measured, Follow-up Q1 |
| MEAT + MEAT-PCKGD | $170.2K (21.3%) | 24.9% / 22.6% | Deep and large. Traffic category, so test before cutting. | measured, Follow-up Q1 |
| DRUG GM | $61.7K (7.7%) | 9.4% | Shallow. Low priority. | measured, Follow-up Q1 |
| TOYS | under $1K | 43.4% | Highest rate, no money. Ignore. | measured, Follow-up Q1 |
| Mailer-only promotions | $255.9K (32.1%) | 34.4% | Deepest planned spend. Biggest test target. | measured, Follow-up Q6 |
| Mailer plus display | $104.0K (13.0%) | 36.5% | Deepest of all. | measured, Follow-up Q6 |
| Display only | $50.4K (6.3%) | 17.6% | Shallow. Display may lift volume without deep price. | measured, Follow-up Q6 |
| No promotion record | $386.8K (48.5%) | 10.3% | Silent loyalty markdowns. Unplanned, unreviewed. | measured, Follow-up Q6 |
| National brands | $618.3K (77.6%) | 15.8% | Supplier funding should cover part of this. | measured, Follow-up Q7 |
| Private label | $178.9K (22.4%) | 15.6% | No supplier to share cost. Promoting own brand as deep as national brands is a cash trap. | measured, Follow-up Q7 |

**Concentration makes this manageable.** 5,027 SKUs (7% of active products) drive 80% of discount dollars [measured, Handoff s.4 F4; chart `03_leakage_concentration.png`]. The Lorenz curve is steepest in the first 1-2% of SKUs [measured, read visually from chart 03].

**Seasonal spikes are real but modest.** Week 27 (early July) peaks at 19.9% against a 15.7% average [measured, exploration chart `04_leakage_by_week.png`]. Weeks 21-23 peak near 18%. The chart title says "more than double". That is wrong: 19.9% is 1.27 times the average.

In dollars, week 27 cost $20,710, $5,668 (37.7%) above the mean week of $15,041. Weeks 21-23 cost $5,948 (13.2%) above three mean weeks [measured, Follow-up R2-Q5]. Together the spikes add about $11.6K. Worth managing, but not a main lever.

**Where the above-cap dollars sit.** The $227.6K above a 25% ceiling is even more concentrated than total discount [measured, Follow-up R2-Q2 to Q4]:

| Cut | Dollars above 25% cap | Share |
|---|---|---|
| Mailer-linked (mailer only + both) | $135.6K | 59.6% |
| No promotion record | $78.5K | 34.5% |
| Display only | $13.4K | 5.9% |
| National brands / private label | $183.1K / $44.5K | 80.5% / 19.5% |
| GROCERY / MEAT / MEAT-PCKGD | $122.7K / $38.5K / $21.2K | 53.9% / 16.9% / 9.3% |
| Top categories: soft drinks, chicken, milk, beef, ice cream | $22.4K, $17.2K, $10.3K, $10.0K, $9.3K | 30.4% combined |
| SKUs holding half of it | 383 of 21,926 SKUs with any excess | 50% |
| SKUs holding 80% of it | 2,529 SKUs | 80% |

**So the review list is 383 SKUs, not 5,000.** That is a list one pricing analyst can work through in a quarter.

### 3b. The below-cost test: do deep markdowns lose money on every unit?

**At 25% or deeper, a retailer-funded markdown needs about four times the normal volume just to break even. Most of the observed volume lift is likely brand switching.**

Assumption: front margin on list price is 33% [assumed]. I derive it from Kroger's 22.3% gross margin on sales and this panel's 15.7% average discount. Cost is then about 0.78 x 0.843 = 0.66 of list. Change it if Finance has the real figure.

Break-even unit multiple = margin / (margin - depth). Supplier funding is ignored.

| Depth (retailer-funded) | Margin left per list $ | Units needed vs normal to break even | Label |
|---|---|---|---|
| 10% | 23 cents | 1.4x | assumed |
| 20% | 13 cents | 2.5x | assumed |
| 25% | 8 cents | 4.1x | assumed |
| 30% | 3 cents | 11x | assumed |
| 33% or more | 0 or below | never: every unit sells at or below cost | assumed |

The observed promo-week ratio is 4.5x [measured, Follow-up Q4]. But it is gross, not incremental. Bell et al. found about 75% of brand lift is switching [external, Bell 1999]. Switching inside the same store adds little profit to the retailer. If only a quarter of the extra 3.5x is new to the store, true lift is about 1.9x [assumed]. That clears the 10% hurdle but fails at 20% and deeper.

**Applied to the actual deep lines, the panel sells about $107K a year below cost.** [Product-margin math uses the assumed 33%.]

| Line group | List $ | Discount $ | Average depth | Product margin at 33% front margin | Label |
|---|---|---|---|---|---|
| Depth 25% or more | $1,507K | $604K | 40.1% | -7.1 cents per list $ = **-$107K** | measured list/discount (R2-Q1); margin assumed |
| of which depth 40% or more | $719K | $354K | 49.2% | -16.2 cents per list $ = **-$116K** | same |
| of which depth 25-40% | $789K | $251K | 31.8% | +1.2 cents per list $ = +$9K | derived from the two rows above |

Two things could rescue these lines. Suppliers may pay back part of the depth off-system. Or the deals may bring trips that earn margin on other items. Neither is measured. Both are testable (Pilots 2 and 3).

**Implication.** Mailer lines average 34.4% depth. On my margin assumption, they sell below cost unless suppliers fund the gap or the trip they create earns margin elsewhere. Neither is measured today. That is the case for the payback test in Pilot 2.

### 3c. Recoverable margin: three scenarios

**Plan on about $100K-$150K a year of net margin from the panel, with $228K as the ceiling.**

| Scenario | Annual $ (panel) | How built | Label |
|---|---|---|---|
| Model-targeted cap (the handoff's method) | $76.5K | $20,585 over a 14-week test, x 52/14. Handoff said 13 weeks and $82.3K; corrected. | modeled, Follow-up Q3 |
| Gross ceiling: cap all lines at 25% depth | $227.6K | Sum of discount above 25% on actual rates, all weeks, no volume response | measured, Follow-up Q2 |
| Narrow ceiling: cap at 35% only | $107.1K | Same method, 35% cap | measured, Follow-up Q2 |
| Planning case: 25% cap outside traffic categories, net of volume loss | ~$100K-$150K | See the arithmetic below | assumed |
| Supplier funding recovery | $31K-$62K | 5-10% of national-brand discount dollars | measured base, assumed rate |

**Planning-case arithmetic [assumed inputs, measured bases].** Today the 25%+ lines earn -$107K of product margin (3b). Capped at 25%, they earn 8 cents per list dollar. With no volume loss that is +$121K, a $228K swing. Each 10% of volume lost costs only about $12K, because those units were sold below cost. Then carve out the five traffic categories ($69K, 30.4% of the pool, R2-Q3). With 30% volume loss on the rest, the gain is about $130K. Off-system supplier funding, if it exists, would cut this. Hence a $100K-$150K range.

The real risk of volume loss is lost trips, not lost unit margin. That is why traffic categories are carved out and Pilot 1 guards on store transactions.

Why the model figure is lower: it only touches lines the model predicts above 25%. The model ranks lines well, but its recall at 25% is only 20% (chart `08_threshold_curves.png`) [modeled]. A rule built on each SKU's actual past depth reaches more of the pool.

Per household, the planning case equals $41-$61 a year [assumed: $100K-$150K / 2,467]. Chain impact equals that times active loyalty households.

### 3d. Controllable levers vs structural traits

**Product type explains most of the model. Merchants control depth, mailer selection, multi-buy rules and supplier terms; they do not control product type.**

| Feature (SHAP rank, chart `06_shap_importance.png`) | Type | Use |
|---|---|---|
| Product type (0.055), category (0.013), department (0.004) | Structural | Targeting: which SKUs go on the review list |
| Brand, national vs private (0.005) | Structural, but negotiable | Decides who should fund depth |
| Log quantity, a proxy for multi-buys and bulk (0.012) | Controllable | Multi-buy depth rules. Halving pack size is linked to 2.1 points lower depth, $13.7K [modeled, Handoff s.6] |
| Store (0.007) | Weakly controllable | Narrow spread; monitor the 4 stores over 20% only |
| Week of year (0.005) | Controllable | Calendar: limit stacking of deep events in weeks 21-23 and 27 |
| Promotion depth, mailer slot, supplier funding | Controllable, **not in the model** | The real levers. Must be added as data (Section 4A). |

**A caution on the model's design.** Quantity is only known after the sale. So the model can audit past promotions. It cannot screen a planned promotion before it runs. A planning model needs planned depth, mailer slot and SKU history instead.

### 3e. Profit-maximising model thresholds

**Use a low threshold for a human review queue and a high one for any automatic cap.**

A false positive is a line flagged as leaking that is in fact a sound promotion. A false negative is a deep, loss-making line the model misses.

| Use | Cost of a false positive | Cost of a false negative | Recommended cutoff | Evidence |
|---|---|---|---|---|
| Merchant review queue (human decides) | A few minutes of review per SKU-week [assumed] | The excess discount on a missed line | Predicted 20% or more: 21% of lines, 50.8% of actual discount dollars | measured, Follow-up corrections item 2 |
| Automatic cap at the till | Lost trips and volume on a good traffic promotion | Same as above | Predicted 30% or more: 5% of lines, 22.1% of actual dollars; only after Pilot 1 proves volume holds | measured, Follow-up corrections item 2 |

At a 25% cutoff, precision is 56% and recall 20% [modeled, chart 08]. So 44% of auto-capped lines would be false alarms. That is too many for automation in traffic categories. It is fine for a review list.

Better still: roll scores up to SKU level. Decisions are made per SKU and event, not per till line.

---

## 4. Dual-Track Recommendations

### Track A: Technical, product and AI

**Turn the model into a weekly SKU review list now, and build the data to measure payback next.**

1. **Weekly batch scoring into the promotion planning tool.** Score last week's lines. Roll up to SKU-store-week. Push the top-ranked SKUs to category managers each Monday. No real-time system needed.
2. **A pre-event screen.** Retrain a planning version without quantity. Use planned depth, mailer slot, display, supplier funding and SKU history. Flag any planned event over 25% retailer-funded depth for sign-off.
3. **Move from prediction to uplift.** The current model predicts depth. It does not say whether the promotion changed buying. Every promotion cycle, hold out a random set of stores or SKU-weeks. Estimate incremental units and margin per event. Over time, build an uplift model that ranks events by incremental margin per discount dollar.
4. **Instrumentation to add.**
   - A unified price-event log at the till: every markdown, its type, planned depth and who funds it. This fixes the 48.5% of discount with no promotion record.
   - Supplier funding per event (scan-back, off-invoice, billback), joined to the line.
   - Unit cost per SKU-week, so margin, not just discount, is measured.
   - Basket and trip counts per household, to measure traffic halo from traffic items.
5. **Drift guardrails.** Retrain quarterly. Track error on a rolling 4-week hold-out. Alert if error rises above 0.16 (test error is 0.147) [modeled, Handoff s.5; threshold assumed]. Track the department mix of the review list weekly.
6. **Fix the weak tail.** Error is 0.171 in the top-3 departments vs 0.146 elsewhere [measured, Handoff s.5]. Treat meat scores as directional until a meat sub-model exists.

### Track B: Commercial, pricing and finance (start before the model ships)

**Four policy changes can start this month without any model in production.**

1. **Depth governance rule.** Any retailer-funded depth over 25% needs category director sign-off. Over 35% needs finance sign-off. The 35% tier alone touches $107.1K [measured, Follow-up Q2].
2. **Supplier funding sprint.** Take the top 200 national-brand SKUs by discount dollars to suppliers. Ask them to fund depth beyond 20% or accept a shallower deal. Finance should first audit off-system scan-back and billback receipts. That tells us whether "97% retailer-funded" is real.
3. **Private label depth policy.** Own brand is already cheaper. Do not match national-brand promotional depth on it. Promote it with display, not price. Private label carries $178.9K of fully retailer-paid discount [measured, Follow-up Q7].
4. **Silent markdown review.** Pull the loyalty-card markdowns with no promotion record into the same calendar and approval process. They hold $386.8K [measured, Follow-up Q6].
5. **Calendar discipline.** Do not stack deep mailer and display events in the known spike weeks (21-23, 27) unless suppliers fund them.
6. **Merchant incentives.** Category managers are paid on sales today, I assume. Add a margin-per-promotion-dollar measure to their scorecard [assumed]. Otherwise the policy will be gamed.

---

## 5. The 90-Day Growth Lab: Pilot Portfolio

Stores: 108 stores have $10K or more of panel list revenue [measured, Follow-up Q5]. Pilots use matched store pairs. Pilots 1, 4 and 5 need about 100 pairs in total, so they must draw on the full 437-store estate and use full store sales, not panel only. Keep each store in one pilot only, so effects do not mix. Pilot 2 rotates hold-outs across all stores.

### Pilot 1: Depth Cap Hold-Out Test

| Item | Detail |
|---|---|
| Playbook | Pricing split test with store hold-out |
| Internal trigger | 75.8% of discount dollars sit on lines 25%+ deep; $227.6K above the cap [measured, Follow-up Q2]. Chart `04_promoted_vs_not.png`. |
| External trigger | BCG: a 30% cut beat a 50% cut on margin; 2-5 points of promotion margin available [external, BCG 2015] |
| Hypothesis | If we cap retailer-funded depth at 25% on the 383 SKUs holding half the above-cap dollars (less traffic items), category gross margin dollars will rise 2-5% because those units now sell below cost. |
| Design | 40 matched store pairs (by sales, rate, region). One store per pair gets the cap. Exclude soft drinks, chicken, milk, beef and ice cream (traffic carve-out). 12 weeks. |
| Sample size | Detecting a 3% margin change with week-to-week store noise of about 10% needs about 35-45 pairs over 12 weeks [assumed; confirm with store-level variance]. |
| Who does what | Data: pair matching, SKU list, weekly readout. Pricing: set caps in the price system. Merchandising: approve SKU list. Finance: sign off the margin method. |
| North star | Gross margin $ per store-week in capped categories |
| Guardrails | Store transactions per week (no worse than -1%); category units (no worse than -15%); household visit frequency |
| Day 30 / 60 / 90 | Day 30: kill if traffic falls more than 2% vs control. Day 60: iterate SKU list if margin gain under 1%. Day 90: scale chain-wide if margin gain 2% or more and traffic within 1%. |

### Pilot 2: Mailer Payback Hold-Out

| Item | Detail |
|---|---|
| Playbook | Uplift hold-out test; promotion payback measurement |
| Internal trigger | Mailer lines hold $360K of discount at 34-37% depth [measured, Follow-up Q6]. No incrementality is measured [Handoff s.8 item 1]. |
| External trigger | Almost three-quarters of US promotions do not break even [external, Nielsen via FoodNavigator]; 75% of lift is brand switching [external, Bell 1999] |
| Hypothesis | If we hold out a random 20% of stores from each mailer event, we will find that 40-70% of mailer events do not cover their discount cost, because most lift is switching and stock-up. |
| Design | Random 20% of stores per mailer cycle see shelf price without the mailer deal. Rotate hold-out stores each cycle. 6 mailer cycles (about 12 weeks). Measure incremental units, category margin and basket size. |
| Sample size | Event-level answers need about 20 hold-out stores per event [assumed]. Category-level answers pool across events. |
| Who does what | Data: randomisation, event-level uplift, payback table. Marketing: mailer zoning. Merchandising: event list. Finance: payback rule. |
| North star | Incremental gross margin per $ of discount, per event |
| Guardrails | Store traffic in hold-out stores; complaint rate; supplier contract compliance |
| Day 30 / 60 / 90 | Day 30: confirm randomisation balance. Day 60: drop the bottom third of events by payback from the next mailer. Day 90: make payback the standing rule for mailer slots. Kill if hold-out stores lose over 2% traffic. |

### Pilot 3: Supplier Funding Recovery Sprint

| Item | Detail |
|---|---|
| Playbook | Commercial negotiation, controlled by category |
| Internal trigger | National brands carry $618.3K of discount, only $20K is supplier-coupon funded [measured, Follow-up Q7; Handoff s.1] |
| External trigger | Retailers claim about half of available trade funds [external, Grocery Dive] |
| Hypothesis | If buyers ask suppliers of the top 200 national SKUs to fund depth beyond 20%, retailer-funded discount in those SKUs will fall 5-10% because suppliers already budget trade money for these deals. |
| Design | Randomly assign half of the top national-brand categories to the sprint. The other half are control. 90 days. |
| Who does what | Finance: audit off-system funding first. Buyers: negotiate. Data: weekly net cost per SKU. Legal: contract terms. |
| North star | Net retailer-funded discount $ in sprint categories |
| Guardrails | Shelf price parity with competitors; supplier fill rate; no loss of key deals |
| Day 30 / 60 / 90 | Day 30: audit result; if off-system funding already covers over half of depth, re-base all margin numbers. Day 60: at least 30% of targeted suppliers agreed. Day 90: scale to all national categories if net cost fell 5% or more. |

### Pilot 4: Private Label Display-for-Depth Swap

| Item | Detail |
|---|---|
| Playbook | Packaging and merchandising test |
| Internal trigger | Private label runs 15.6% depth, almost the same as national (15.8%), with no supplier share [measured, Follow-up Q7]. Display-only lines run 17.6% vs 34.4% for mailer-only [measured, Follow-up Q6]. |
| External trigger | Kroger credits own brands for its gross margin rise [external, Kroger IR] |
| Hypothesis | If we replace deep price cuts on own brand with display plus a shallow cut (15% or less), own-brand margin $ will rise 3-6% because own brand is already the low-price option. |
| Design | 30 matched store pairs, top 100 own-brand SKUs, 10 weeks |
| North star | Own-brand gross margin $ per store-week |
| Guardrails | Own-brand unit share of category (no worse than -2 points); category margin |
| Day 30 / 60 / 90 | Day 30: kill if own-brand share drops 3+ points. Day 60: tune depth. Day 90: scale if margin $ up 3% or more. |

### Pilot 5: Multi-Buy Depth Rule

| Item | Detail |
|---|---|
| Playbook | Pricing mechanic test |
| Internal trigger | Quantity is the top controllable driver. Halving pack size links to 2.1 points lower depth, $13.7K [modeled, Handoff s.6] |
| External trigger | BCG egg example: single-unit 30% beat a deeper cut [external, BCG 2015] |
| Hypothesis | If we swap deep "buy 2+" deals for a shallower single-unit price on the top 100 multi-buy SKUs, discount $ per unit will fall 10-20% with units down under 10%, because many multi-buy units are stock-up, not new demand. |
| Design | 30 matched store pairs, 8 weeks |
| North star | Gross margin $ on test SKUs |
| Guardrails | Units, basket size |
| Day 30 / 60 / 90 | Kill at Day 30 if units fall 20% or more. Scale at Day 60-90 if margin up 3% or more. |

---

## 6. Prioritisation Matrix and Sources

**Start with the policy and funding moves; run Pilots 1 and 2 in parallel; save the uplift model for wave 3.**

| Initiative | Financial impact (P&L driver) | Confidence | Ease / time to value | Wave |
|---|---|---|---|---|
| Depth sign-off rule (25% / 35%) | High (gross margin) | Medium-high: measured pool, volume effect unknown | 2-4 weeks, low complexity | 1 |
| Supplier funding audit and sprint (Pilot 3) | Medium-high (gross margin) | Medium: base measured, rate assumed | 4-8 weeks, medium | 1 |
| Silent markdown review | Medium (gross margin) | Medium: measured pool, value of each markdown unknown | 4-6 weeks, medium | 1 |
| Private label depth policy (Pilot 4) | Medium (gross margin) | Medium | 6 weeks, low | 1 |
| Weekly SKU review list from the model | Medium (gross margin) | Medium: model ranks well, 2.0x lift top decile | 4-6 weeks, low-medium | 1 |
| Depth cap hold-out (Pilot 1) | High (gross margin, traffic risk) | Medium; result decides scale | 12 weeks, medium | 2 |
| Mailer payback hold-out (Pilot 2) | High (capital allocation of promotion budget) | High value of information | 12 weeks, medium-high | 2 |
| Multi-buy rule (Pilot 5) | Low-medium (gross margin) | Low-medium: modeled only | 8 weeks, low | 2 |
| Price-event log and unit cost data | Enabler | High: needed for every later step | 3-6 months, high | 2 |
| Uplift model ranking events by incremental margin | High (gross margin, revenue) | Low until Pilot 2 data exists | 6-9 months, high | 3 |
| Flywheel: reinvest saved depth into everyday prices on traffic items | High (revenue, retention) | Low: strategic bet | 6-12 months, high | 3 |

### Verified web sources (fetched)

| URL | What I took from it |
|---|---|
| https://www.foodnavigator.com/Article/2014/10/09/Three-quarters-of-CPG-promotions-don-t-break-even-Nielsen | Nielsen: almost three-quarters of US promotions do not break even; 1M+ UPCs, 39M events (2014). |
| https://www.bcg.com/en-us/publications/2015/retail-pricing-how-retailers-can-improve-promotion-effectiveness.aspx | Promotions 10-45% of revenue; 20-50% give no lift; 20-30% more do not cover cost; 2-5 points margin gain; 30% beat 50% depth; $166M case. |
| https://www.fmi.org/newsroom/latest-news/view/2025/07/15/fmi-report--amid-uncertainty--food-industry-succeeds-in-offering-shoppers-value | US food retailer net margin 1.7%; shoppers still price-worried. |
| https://ir.kroger.com/news/news-details/2025/Kroger-Reports-Fourth-Quarter-and-Full-Year-2024-Results-Announces-Guidance-for-2025/ | Kroger FY2024 gross margin 22.3%; own brands drove margin; media and other income $1.35B operating profit. |
| https://www.grocerydive.com/news/grocery--study-25-of-retailers-increased-ad-budgets-but-left-funds-unclaimed/534857/ | Up to $70B of trade funds offered yearly; retailers claim about half. |
| https://ideas.repec.org/a/inm/ormksc/v18y1999i4p504-526.html | Bell, Chiang, Padmanabhan (1999): about 75% of promotional lift is brand switching, 25% extra demand; 173 brands, 13 categories. |
| https://www.foodnavigator.com/Article/2022/12/21/2022-in-review-Rampant-inflation-the-end-of-the-honeymoon-period-for-plant-based-meat-and-added-sugar-under-attack?page=4 | Bernstein: 24.4% of US food sales on deal in 2022 vs 31% in 2019. |
| https://www.casestudies.com/company/antuit/case-study/regional-grocery-chain-optimizes-promotion-pricing-to-compete-more-effectively | Vendor case: 8% average margin gain at a regional grocer from ad-circular optimisation. |

### What I could not verify

- Progressive Grocer "almost half of purchases on promotion": HTTP 403. Not used.
- 84.51 personalised offer redemption (10-15%): HTTP 403. Mentioned as unverified only.
- Bijmolt et al. (2005) mean price elasticity of -2.62: Tilburg page HTTP 403. Not used.
- No source gave a current US grocery gross margin benchmark. I used Kroger as a single-company proxy.
- The chain's real product cost, supplier funding and active loyalty household count are not in the data. All margin math uses my 33% assumption.

### Open questions (not answerable from this data)

1. Real front margin by category, to replace the 33% assumption.
2. Off-system supplier funding per SKU (scan-backs, billbacks, off-invoice).
3. Number of active loyalty households chain-wide, to scale panel figures.
4. Incremental sales per promotion. Only Pilot 2 can answer this.

---

## Glossary

| Term | Plain meaning |
|---|---|
| List revenue | Sales at shelf price before any discount. |
| Pocket revenue | What the retailer keeps after all discounts. |
| Price waterfall | A chart walking from list price down to pocket revenue, step by step. |
| Leakage | Discount dollars given away between list and pocket revenue. |
| Depth / discount rate | Discount as a share of list price on a line. |
| Retailer-funded discount | A markdown paid from the retailer's own margin. |
| Supplier-funded discount | A markdown paid back by the manufacturer. |
| Trade funds | Money suppliers set aside to pay retailers for promotions. |
| Scan-back | Supplier pays the retailer per unit scanned during a deal. |
| Billback / off-invoice | Supplier pays after the deal (billback) or cuts the invoice price up front (off-invoice). |
| Mailer / display | Promotion in the weekly flyer / on a special in-store display. |
| Silent markdown | A loyalty-card price cut with no promotion record. |
| Private label / own brand | Products sold under the retailer's own brand. |
| National brand | Products made and branded by outside manufacturers. |
| Traffic driver | A product shoppers make trips for, such as milk or meat. |
| Gross margin | Sales minus product cost, as a share of sales. |
| Front margin | Gross margin at list price before discounts. |
| Net profit margin | Profit after all costs, as a share of sales. |
| Break-even unit multiple | How many times normal volume a deal must sell to earn the same margin. |
| Incremental sales / lift | Sales that happened only because of the promotion. |
| Brand switching | Shoppers buying the promoted brand instead of another brand they would have bought. |
| Stockpiling / stock-up | Shoppers buying ahead at the low price, then buying less later. |
| Cannibalisation | Promotion sales taken from other items in the same store. |
| Payback | Whether a promotion's extra margin covers its discount cost. |
| Earned vs bought growth | Growth from loyal demand vs growth paid for with discounts. |
| Flywheel | A loop where each result feeds the next input. |
| Category role | The job a category does, such as traffic, margin or convenience. |
| Uplift / persuadables | Effect of an action on behaviour / shoppers whose behaviour the action changes. |
| Hold-out test | Keep a random group untreated to measure the true effect. |
| Matched store pairs | Similar stores paired so one gets the change and one does not. |
| North star metric | The single main outcome a pilot is judged on. |
| Guardrail metric | A metric that must not get worse while the pilot runs. |
| Model (CatBoost) | A tree-based machine-learning model used to predict line depth. |
| SHAP | A method that measures how much each input moves the model's prediction. |
| Decile / lift (model) | One-tenth of lines ranked by score / concentration vs average. |
| Precision | Share of flagged lines that truly are deep. |
| Recall | Share of truly deep lines that get flagged. |
| False positive / false negative | Flagging a sound line / missing a deep line. |
| Threshold / cutoff | The score above which a line is flagged. |
| RMSE | Typical size of the model's prediction error. |
| Drift | Model accuracy falling as conditions change. |
| Eta-squared | Share of variation explained by a grouping; under 0.06 is small. |
| Lorenz curve | Chart of how concentrated a total is across items. |
| Annualise | Scale a part-year figure to a full year. |
| SKU | A single stock-keeping unit: one product in one size. |
| Panel | The 2,467 loyalty households in the dataset. |
