# Executive Growth Strategy: Two Public-Data Teardowns
**Netflix US and Canada pricing (Q4 2019 to Q4 2025) and Five Below store expansion (FY2018 to FY2025)**
Author: growth-strategy-partner, for Shrikar (shrikar.p@triiqinnovations.com). Date: 17 November 2026.

## How to read this memo

Every number carries one of four labels:
- **measured**: read directly from the filings, via `reports/ml_handoff_report.md` (handoff) or `reports/ml_followups.md` (followups).
- **modeled**: an association from a fitted model. It is not proof of cause.
- **external**: from a cited web source or SEC filing. URLs are in Section 8.
- **assumed**: my own estimate, stated so you can change it.

All effect sizes are associations, not causal estimates. Netflix has 24 quarters of revenue and 20 quarters of membership data. Five Below has 8 fiscal years. Treat every magnitude as a range, not a point.

**Corrections to the handoff.** The statistician confirmed several handoff errors in follow-up rounds (followups, rounds 1 and 2). This memo uses the corrected values:

| Handoff claim | Corrected value | Effect on this memo |
|---|---|---|
| UCAN members at Q4'24 = 83M; "$360M per $1 of ARM" | 89.63M members; $1/month = about $1.08B a year (measured; arithmetic) | Netflix lever 1 resized |
| Paid sharing added +$1,218M per quarter | Pre/post median gap is real, but after removing the trend the lift is +$92M per quarter, 95% CI −$46M to +$231M, p = 0.17 (modeled) | Netflix thesis rewritten |
| ARM growth did not predict subscriber losses (rho = +0.19) | rho = −0.474, p = 0.064, N = 16 (measured): higher ARM growth goes with weaker next-quarter net adds, though only at borderline significance | Price risk is real |
| FY2023 comps = −2.0%; expansion was "20%+ of fleet" | FY2023 comps = +2.8%; FY2023–24 expansion rate was 15.2% and 14.7% (measured) | Five Below thesis rewritten |
| Expansion vs margin rho = −0.82 | Holds for the **absolute store count** (6 years, p = 0.033). For **rate of fleet growth**, rho = +0.50, p = 0.83 (measured) | Lever is "openings per year", not "% growth" |
| "1.6 ppt margin per 100 stores" | Not supported; withdrawn by the statistician | Not used |

---

# PART I: NETFLIX US AND CANADA

## N1. Thesis and three headline levers

**Thesis: Netflix's US and Canada growth since 2023 came mostly from adding paying households, not from raising prices, so the next price step should be protected by member-conversion levers.**

In 2022, price did all the work. Revenue grew 8.6%, ARM [average revenue per member per month] grew 9.3%, and members fell 0.7% (measured, followups round 2). In 2024, revenue grew 16.7%. Member growth supplied about 68% of it and ARM about 33% (measured, followups round 2). The handoff described 2023–24 as ARM-led. The decomposition shows it was member-led.

| # | Lever | Size of the prize | Label |
|---|---|---|---|
| 1 | **Price (ARM).** Each +$1/month of ARM on 89.63M members | about +$1.08B a year in UCAN revenue, if members hold. Break-even loss is about 4.9M members (5.5% of base). | measured arithmetic; members holding is assumed |
| 2 | **Paid member conversion.** Paid sharing, extra-member slots, cheaper entry tier | Members rose 74.40M to 89.63M (+15.23M) from Q1'23 to Q4'24. Each 1M members at $17.26 ARM = about $207M a year. | measured; per-member value is arithmetic |
| 3 | **Ads monetization.** Close the gap between the $8.99 ads plan and the $19.99 Standard plan | Each 1M members who move from Standard to ads gives up about $132M a year in fees unless ad revenue fills the $11/month gap. | external prices; arithmetic |

## N2. Evidence: what the data shows

**Conclusion: revenue doubled and price increases stuck, but the data cannot show that price increases are free.**

| Fact | Value | Label | Source |
|---|---|---|---|
| UCAN quarterly revenue, Q4'19 to Q4'25 | $2,672M to $5,339M (+100%) | measured | handoff §1; chart 01 |
| Calendar 2025 vs 2024 UCAN revenue | $19,957M vs $17,359M (+15.0%) | measured | followups round 1, Q2 |
| ARM, Q4'19 to Q4'24 | $13.22 to $17.26 per month (+31%); Spearman rho = 0.971, 95% CI 0.861–0.996 | measured | handoff Finding 1 |
| UCAN members, Q1'23 to Q4'24 | 74.40M to 89.63M (+15.23M) | measured | followups round 2, Q3 |
| Paid-sharing association with members | +2.23M members per quarter, 95% CI +0.36M to +4.10M, p = 0.022 | modeled | followups round 2, Q3 |
| Paid-sharing association with revenue, trend removed | +$92M per quarter, 95% CI −$46M to +$231M, p = 0.17 | modeled | followups round 1, Q3 |
| ARM growth vs next-quarter net adds | rho = −0.474, p = 0.064, 95% CI −0.81 to 0.03, N = 16 | measured | followups round 1, Q4 |
| Worst quarter for net adds | −1.3M (Q2'22), reversed within two quarters | measured | handoff §6; chart 04 |
| Revenue model accuracy | Walk-forward MAE $92.7M per quarter vs $99.5M naive; held-out Q1'25 error −$88M | modeled | handoff §4 |

What this means:
- **Price increases stuck.** ARM rose in a near-straight line across six price events (chart 03). No price event was followed by a revenue decline (chart 01).
- **Price has a cost.** Higher ARM growth went with weaker next-quarter net adds (rho −0.47). The p-value is 0.064, so this is a warning, not a finding.
- **Paid sharing worked through members, not a revenue jump.** The +$1.2B "lift" in the handoff is mostly the time trend. Once the trend is removed, the revenue association is small and not significant. The member association is significant.
- **The revenue model is a momentum model.** Prior-quarter revenue carries the prediction (coefficient 1.23, p < 0.001). The ARM coefficient is −72, p = 0.18, because ARM is collinear with revenue (modeled; handoff §4). The model cannot price a price change.

### Internal vs external benchmarks

**Conclusion: Netflix monetizes better than the category, and ads are now a real but small second revenue stream.**

| Metric | Netflix | Benchmark | Read-across | Label |
|---|---|---|---|---|
| Revenue growth, 2025 | UCAN +15.0% (measured) | Netflix global 2025 guidance +16% to $45.1B | UCAN keeps pace with the global business | external |
| Monthly churn [share of subscribers cancelling each month] | ~2.1% (third-party estimate) | Disney+ ~5.5%, Max ~6–6.9%, Hulu ~5.3% | Netflix churns at under half the rate of rivals | external, secondary source; primary not verified |
| Ad revenue | >$1.5B in 2025, ~2.5x 2024; 2026 forecast ~double | Netflix target ~$9B ad sales by 2030 | Ads are ~3% of 2025 revenue | external |
| Ads-plan share of new sign-ups | >60% in the 12 ad markets (Q1 2026) | 2024: >40% | New members are entering at the cheapest price | external |
| US prices after March 2026 | Ads $8.99; Standard $19.99; Premium $26.99 | Up $1, $2, $2 | Standard rose 11.1%; ads rose 12.5% | external |
| 2026 company guidance | Revenue $50.7–51.7B (+12–14%); operating margin 31.5% | n/a | Growth slows from 2025's pace | external |

Netflix stopped reporting members after Q4 2024. I could not verify any 2025 UCAN member or ARM figure. Third-party churn tables cite one another; I could not reach a primary source. Treat the churn row as directional.

## N3. Strategic recommendations

**Conclusion: keep pricing up, but fund each price step with a member-conversion move, and measure price response in-house.**

### Decision rule (the "threshold")

A price rise of x% breaks even if members fall by less than x/(1+x). For the March 2026 Standard step (+11.1%), the break-even loss is about 10% of Standard members (arithmetic). For a +$1 ARM blend on 89.63M members, it is about 4.9M members (measured arithmetic). The worst observed single-quarter loss was 1.3M (measured). So past price steps had a wide safety margin. That margin shrinks if ads-plan sign-ups dilute ARM.

### Track A: capability

1. **Build a household-level price-response model.** Use the staggered roll-out of existing-member price increases as a natural experiment (see pilot NF-1). Public data cannot estimate elasticity [how much demand changes when price changes]; internal data can.
2. **Score cancellation risk and persuadability separately.** Prediction finds who will cancel. An uplift model [one that estimates how much an offer changes a person's behavior] finds who a save offer actually changes. Target only the persuadable group.
3. **Track blended revenue per member, fees plus ads.** Report ad revenue per ads-plan member monthly. This tells you whether moving members down to the ads tier adds or loses revenue.
4. **Restore an internal member series.** Public membership reporting ended in Q4 2024. Without it, the ARM-times-members identity cannot be checked (handoff §7, item 4).

### Track B: quick wins (no model needed)

1. **Offer the ads plan as a save at cancellation.** Keeping a member at $8.99 beats losing $19.99 (external prices).
2. **Push extra-member slots to detected borrowers.** Paid sharing is the lever with the firmest member association (+2.23M per quarter, modeled).
3. **Space price steps at least 12 months apart.** The two most recent US steps were 14 months apart (Jan 2025, Mar 2026; external). Keep that rhythm; the negative rho argues against tighter spacing.
4. **Pair every price step with a visible content or live-event moment.** One analyst model credits WWE content with retaining ~1.25M subscribers globally per quarter (external, Parrot Analytics via TheWrap; model-based, not verified).

## N4. Pilot experiments (Netflix)

### NF-1: Billing-cycle price-response test
- **Playbook:** natural-experiment holdout.
- **Trigger:** internal, ARM growth vs next-quarter net adds, rho −0.474 (followups round 1). External, existing members get the new price on their own billing date, after one month's notice.
- **Hypothesis:** if we delay the March 2026 increase by 60 days for a random 5% holdout, 90-day cancellation will be 0.1–0.4 ppt lower in the holdout. This would show price-driven churn is small next to the ~$2/month gain (assumed range).
- **Design:** randomize existing Standard members into a 95% treated group and a 5% delayed group. Base monthly churn of ~2% (external, unverified) needs about 77,000 members per arm to detect a 0.2 ppt change (80% power, 5% significance; assumed calculation). The 5% holdout from 89.63M is far above that.
- **Runtime:** 90 days after notice.
- **Who does what:** Data and Engineering assign groups and log notice dates. Finance books the delayed revenue as the test's cost. Product writes the notice copy. Member Services tracks complaints.
- **North Star:** net revenue per assigned member over 90 days.
- **Guardrails:** cancellation rate; downgrades to the ads plan; support contacts per 1,000 members.
- **Day 30:** if holdout cancellations are more than 0.5 ppt lower, pause the next roll-out wave. **Day 60:** compute elasticity by plan and tenure. **Day 90:** scale if net revenue per member is at least 8% higher in the treated group. Kill the holdout if treated churn is no higher.

### NF-2: Ads-plan save offer with an uplift holdout
- **Playbook:** uplift holdout test.
- **Trigger:** internal, revenue holds only if members hold (break-even 4.9M; measured arithmetic). External, ads plan is >60% of new sign-ups and ad revenue is doubling.
- **Hypothesis:** if we offer a move to the $8.99 ads plan at the cancel screen, the save rate rises by 3–8 ppt from an assumed 10% base. Many cancellers are price-driven, not content-driven (assumed).
- **Design:** randomize cancel-flow visitors 50/50 to offer vs no offer. About 1,600 per arm detects a 3 ppt lift from 10% (assumed calculation). Run 8 weeks, then follow saved members for 6 months.
- **Who does what:** Product builds the cancel-flow variant. Data scores persuadability for the next wave. Ad Sales confirms ad revenue per ads member. Finance sets the revenue floor.
- **North Star:** 6-month revenue per cancel-flow visitor, fees plus ads.
- **Guardrails:** share of saved members who cancel within 60 days; voluntary downgrades by non-cancellers (cannibalization).
- **Day 30:** save rate must be at least +2 ppt. **Day 60:** 60-day re-cancel rate below 50%. **Day 90:** scale if 6-month revenue per visitor is positive after counting voluntary downgrades. Kill if downgrades cost more than saves.

### NF-3: Extra-member slot price test
- **Playbook:** pricing split test.
- **Trigger:** internal, paid sharing has the firmest member association (+2.23M per quarter, CI +0.36M to +4.10M). External, extra-member fees rose $1 in March 2026.
- **Hypothesis:** if detected borrowers see a first-month discount on an extra-member slot, paid conversion rises 10–25% relative (assumed). Borrowers already value the service.
- **Design:** randomize detected borrowing households to three arms: list price, first month at 50% off, first month free. Run 60 days; measure 120-day paid retention.
- **North Star:** 120-day revenue per borrowing household.
- **Guardrails:** primary-account cancellations; complaint rate.
- **Kill** any arm whose 120-day revenue per household is below list price.

---

# PART II: FIVE BELOW

## F1. Thesis and three headline levers

**Thesis: Five Below's constraint is how many stores its teams can open well each year, not how fast the fleet grows in percent, and about 150 a year looks sustainable today.**

The two worst margin years followed the two biggest opening years in absolute count (204 and 227 stores). The same link does not appear when growth is measured as a percent of the fleet. FY2019 grew the fleet 20% with an 11.8% margin (measured, followups round 1, Q5). The likely bottleneck is real estate, construction and store-opening teams, which do not scale with fleet size.

| # | Lever | Size of the prize | Label |
|---|---|---|---|
| 1 | **Cap openings near ~150 a year; raise only when new stores hit the model.** | FY2024 margin of 8.35% vs FY2023's 10.83% cost about $96M of operating income on $3,877M revenue. | measured arithmetic; link to pace is an association |
| 2 | **Keep the merchandise and price reset.** Whole-number prices, trend items, selective above-$5 items | FY2025 comps +12.8%; Q2 transactions +8.7%. Each 1 ppt of comps is worth about $44M of sales. | external; per-ppt value assumed (~$4.4B comp base) |
| 3 | **Bank the capital efficiency.** | Capex fell from $324.0M to $174.7M (−$149M) while revenue rose 22.9%. Revenue per store is $2.48M vs the $2.0M new-store model. | measured; external (10-K) |

**Cost of going slower (assumed).** 50 fewer openings a year defers about $100M of sales. At a ~10% operating margin, that is about $10M of operating income deferred per year. One bad execution year like FY2024 cost about $96M. On these numbers, waiting is about ten times cheaper than a stumble. The FY2024 dip is an association, not proven to be caused by pace.

## F2. Evidence: what the data shows

**Conclusion: the pace signal is real for store count, weak for comps, and absent for percent growth; N is too small for more.**

| FY | Year-end stores | Net new | Expansion rate | Revenue ($M) | Comps | Op margin | SG&A % | Capex ($M) | Rev/store ($M) |
|---|---|---|---|---|---|---|---|---|---|
| 2018 | 750 | 125 | n/a | 1,559.6 | +3.9% | 12.0% | 24.2% | 113.7 | 2.08 |
| 2019 | 900 | 150 | 20.0% | 1,846.7 | +0.6% | 11.8% | 24.7% | 212.3 | 2.05 |
| 2020 (COVID) | 1,020 | 120 | 13.3% | 1,962.1 | −5.5% | 7.9% | 25.4% | 200.2 | 1.92 |
| 2021 (COVID) | 1,190 | 170 | 16.7% | 2,848.4 | +30.3% | 13.3% | 22.8% | 288.2 | 2.39 |
| 2022 | 1,340 | 150 | 12.6% | 3,076.3 | −2.0% | 11.2% | 24.4% | 252.0 | 2.30 |
| 2023 | 1,544 | 204 | 15.2% | 3,559.4 | +2.8% | 10.8% | 21.3% | 335.1 | 2.31 |
| 2024 | 1,771 | 227 | 14.7% | 3,876.5 | −2.7% | 8.4% | 22.2% | 324.0 | 2.19 |
| 2025 | 1,921 | 150 | 8.5% | 4,764.1 | +12.8% | 9.6% | 22.4% | 174.7 | 2.48 |

All measured (followups round 1, Q6–Q7; charts 02–04). Expansion rate = net new ÷ prior year-end stores. Revenue per store uses year-end stores.

| Test (non-COVID years) | Result | Label |
|---|---|---|
| Op margin vs net new stores (count), 6 years | rho = −0.820, exact p = 0.033 | measured |
| Comps vs net new stores (count), 6 years | rho = −0.577, p = 0.142 | measured |
| Op margin vs expansion rate, 5 years | rho = +0.50, p = 0.83 | measured |
| Comps vs expansion rate, 5 years | rho = −0.20, p = 0.39 | measured |
| Revenue per store, FY2022 vs FY2023–24 average | $2.30M vs $2.25M (−2%) | measured |
| Comp-sales model, leave-one-out | MAE 11.07 ppt vs 13.07 naive; R² −0.39 | modeled; not usable for forecasts |
| Margin model, leave-one-out | MAE 1.79 ppt vs 2.17 naive | modeled; weak |

What this means:
- **Store count, not rate, tracks margin.** Only one test passes p < 0.05, and on 6 points. Treat it as a flag.
- **Store dilution was small.** Revenue per store fell only 2% in the peak years and never neared the $2.0M model. Site quality did not visibly fail.
- **Margin bridge is open.** A provisional split of the FY2023 to FY2024 drop (−2.48 ppt) gives gross margin −0.89, SG&A −0.94 and an unexplained −0.65 ppt. The cost-of-sales field changes definition in FY2023, so this is not reliable (followups round 2, Q1).
- **FY2025 has rival explanations.** Comps rose in the same year that management changed pricing to whole numbers and refreshed trend merchandise (external). Openings fell in that year too. The data cannot separate these causes.

### Internal vs external benchmarks

**Conclusion: Five Below now out-comps its closest discount peer by a wide margin, but grows its fleet at half the peer's rate.**

| Metric | Five Below | Benchmark | Read-across | Label |
|---|---|---|---|---|
| Comps | FY2025 +12.8% (measured) | Ollie's Q3 FY2025 +3.3%; FY guide +3.2–3.5% | Five Below is ~9 ppt ahead | external |
| Fleet growth | 8.5% (measured) | Ollie's 645 stores, +18.1% YoY, 86 openings | Ollie's grows faster in percent, from a far smaller absolute count | external |
| Op margin | FY2025 9.6% (measured) | Ollie's Q3 FY2025 9.0% (one quarter only) | Not like-for-like; directional | external |
| New-store model | $2.48M revenue per store (measured) | Company model: $2M first-year sales, $0.4M investment, ~1-year payback | Average store runs 24% above the new-store model | external (10-K) |
| FY2026 outlook | n/a | Sales $5.20–5.30B; comps +3–5%; ~150 net new; capex $230–250M | Management has chosen ~150 again | external |
| Tariffs | n/a | ~150 bps annual margin pressure flagged in 2025 | FY2025's 9.6% was earned despite tariffs | external, secondary summary |
| Store runway | 1,921 stores (measured) | Company target "more than 3,500" | At 150/year, ~10.5 years to 3,500; at 200/year, ~7.9 years | external; arithmetic |

Ollie's shows that 18% fleet growth can coexist with positive comps. That supports the "absolute count" reading: Ollie's opened 86 stores, well under Five Below's 204–227. I could not verify a full-year Ollie's operating margin.

## F3. Strategic recommendations

**Conclusion: make the opening count earn its way up, using new-store results as the gate.**

### Decision rule (the "threshold")

Raise the opening count by ~25 stores a year only if two conditions hold for the prior class. First, the prior class is tracking at or above $2.0M first-year sales. Second, comps in stores near the new ones stay within 1 ppt of the chain (assumed thresholds). Otherwise, hold at 150. This turns a fixed growth target into an earned one.

### Track A: capability

1. **New-store vintage dashboard.** Track each opening class by month 1–24 against the $2.0M and one-year-payback model. Public data cannot tell bad sites from normal ramp-up (handoff §7, item 6). Internal data can.
2. **Cannibalization model.** Measure sales shift from existing stores within 5–10 miles of each new store. Store density rises as the fleet passes 2,000.
3. **Trade-area site scoring.** Add points-of-interest and census demographics to site selection (problem description lists Foursquare Open Source Places, Overture Maps and US Census ACS).
4. **Opening-capacity planning.** Count real-estate, construction and district-manager capacity per quarter. Set the opening plan from capacity, not from a percent target.

### Track B: quick wins

1. **Hold FY2026 at ~150 net new, as guided.** Front-load openings (Q1 guide is ~45, external) so stores reach holiday trading.
2. **Pay real-estate and operations teams on year-2 store sales, not openings count.** This aligns incentives with the gate above.
3. **Protect the price reset.** Keep whole-number price points and the trend-item cadence that coincided with +8.7% transactions (external).
4. **Route the freed capex.** About $149M less capex in FY2025 (measured). Use part for remodels and in-stock systems in older stores rather than more openings.

## F4. Pilot experiments (Five Below)

### FB-1: Opening-cadence pilot by region
- **Playbook:** matched-region operations test.
- **Trigger:** internal, margin vs store count rho −0.82 (p 0.033) but no link with rate (followups round 1, Q5). External, Ollie's sustains +18% unit growth on 86 openings.
- **Hypothesis:** if openings per district manager are capped at two per quarter and spread evenly, first-year new-store sales will be 3–8% higher than in uncapped regions. Openings will get more management attention (assumed range).
- **Design:** pair regions by store density and income; randomize half to the capped cadence. With ~75 new stores per arm from the FY2026 class, and an assumed 8 ppt SD in store sales vs plan, the minimum detectable effect is ~3.7 ppt (assumed calculation). Runtime: 12 months of openings, with a 6-month read.
- **Who does what:** Real Estate re-sequences the calendar. Operations staffs the openings. Data builds the vintage dashboard. Finance tracks pre-opening cost per store.
- **North Star:** first-12-month sales per new store vs the $2.0M model.
- **Guardrails:** total openings for the year (must stay ~150); pre-opening cost per store; comps of existing stores in the region.
- **Day 30:** calendar is live, with no slippage over 10%. **Day 60:** first 30 stores show treated stores at least even with control on weekly sales. **Day 90:** scale the cadence rule nationally if treated stores lead by ≥3% at month 3. Kill if they trail.

### FB-2: Infill timing holdout (cannibalization)
- **Playbook:** randomized deferral.
- **Trigger:** internal, revenue per store dipped 2% in peak years (measured). External, the company targets 3,500+ stores, so infill will grow.
- **Hypothesis:** if half of eligible infill sites are deferred two quarters, sister stores within 5 miles will show 1–4 ppt higher comps over that window (assumed). That gap is the cannibalization cost to price into site economics.
- **Design:** about 40 approved infill sites; randomize 20 open on schedule, 20 deferred. Runtime: 6 months.
- **North Star:** combined sales of new store plus sisters vs sisters-only.
- **Guardrails:** lease penalty costs; total opening count.
- **Decision:** if net incremental sales per infill store are under $1.5M a year, raise the infill hurdle (assumed threshold).

### FB-3: Above-$5 assortment bay test
- **Playbook:** price-architecture split test.
- **Trigger:** internal, comps swung from −2.7% to +12.8% while openings fell. Merchandising is a rival cause. External, management added selective above-$5 items and moved to whole-number prices.
- **Hypothesis:** if 100 stores double the above-$5 bay, average ticket will rise 2–5% with no drop in transactions. The extra choice raises spend per trip (assumed range).
- **Design:** 100 treated and 100 matched control stores, matched on 52-week sales. Use pre-period sales as a covariate. Runtime: 12 weeks, avoiding the holiday peak.
- **North Star:** gross margin dollars per store per week.
- **Guardrails:** transactions per store; shrink [inventory lost to theft or damage]; clearance markdowns.
- **Day 30:** ticket up at least 1%. **Day 60:** transactions within 1% of control. **Day 90:** scale if gross margin dollars rise at least 2%. Kill if transactions fall more than 2%.

---

# PART III: CROSS-COMPANY

## 5. Pattern recognition

**Conclusion: in both cases the obvious lever (price, pace) mattered less than the mechanism behind it.**

1. **The headline lever was not the main driver.** Netflix's 2023–24 growth was 68–72% member-led, not price-led (measured). Five Below's margin tracked opening count, not percent growth (measured).
2. **Before-and-after comparisons overstate effects.** Removing the trend cut the paid-sharing revenue estimate from +$1,218M to +$92M per quarter (modeled). Always compare against the trend, not just the prior period.
3. **Pick the right unit for the constraint.** Teams constrain openings in counts. Households constrain pricing in dollars per month. Measuring in the wrong unit (percent of fleet) hid the Five Below signal.
4. **Monetize what you have before you scale.** Netflix raised price after member growth was secure. Five Below's best recent year came from selling more in existing stores, not from opening more.
5. **Public data generates hypotheses; experiments decide.** With N = 8 and N = 24, every finding here is a candidate. The pilots above are how a client turns them into decisions.

## 6. Risk table

| # | Risk | Company | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| 1 | Effects are associations; confounders (content, macro, merchandising, leadership) drive outcomes | Both | High | High | Run the pilots before committing capital or price |
| 2 | Small samples: 6 non-COVID years; 16–20 quarters | Both | Certain | High | Read results as direction only; refresh each year |
| 3 | Ads plan dilutes ARM faster than ad revenue grows | Netflix | Medium | High | Track fees plus ads per member monthly; NF-2 guardrails |
| 4 | No public member data after Q4'24 | Netflix | Certain | Medium | Use internal series; rely on revenue only for public work |
| 5 | Price fatigue after back-to-back steps (rho −0.47) | Netflix | Medium | Medium | NF-1 holdout; space steps ≥12 months |
| 6 | FY2025 comp surge reverses; guide is +3–5% for FY2026 | Five Below | High | Medium | Judge pace against new-store results, not chain comps |
| 7 | Tariffs (~150 bps) compress margin regardless of pace | Five Below | Medium | Medium | Separate tariff effect in the margin bridge |
| 8 | Margin bridge unreliable: cost-of-sales field changes in FY2023 | Five Below | Certain | Low | Rebuild from 10-K cost lines (open question) |
| 9 | Slower pace cedes sites to rivals | Five Below | Low | Medium | Hold site pipeline at 200+ approved; open at 150 |
| 10 | Pilot cost: delayed price revenue (NF-1), deferred leases (FB-2) | Both | Certain | Low | Cap holdouts at 5% of members and 20 sites |

## 7. Prioritization matrix

| Initiative | Company | Financial impact (driver) | Confidence | Ease / time to value | Wave |
|---|---|---|---|---|---|
| Hold ~150 openings; pay teams on year-2 sales | Five Below | High (operating margin) | Medium: p = 0.033 on N = 6, plus a peer example | 2–4 weeks; low complexity | 1 |
| Ads-plan save offer (NF-2) | Netflix | Medium (retention, revenue) | Medium: price risk signal plus ads uptake | 4–6 weeks | 1 |
| Space price steps ≥12 months | Netflix | Medium (retention) | Low–medium: rho −0.47, p 0.064 | Immediate | 1 |
| Protect whole-number price reset | Five Below | High (comps) | Medium: external evidence only | Immediate | 1 |
| Billing-cycle price-response test (NF-1) | Netflix | High (revenue, pricing power) | High as a design | 6–8 weeks | 2 |
| Opening-cadence pilot (FB-1) | Five Below | High (margin, capital) | Medium | 8–12 weeks; cross-functional | 2 |
| Extra-member slot price test (NF-3) | Netflix | Medium (members) | Medium: CI +0.36M to +4.10M | 6 weeks | 2 |
| Above-$5 bay test (FB-3) | Five Below | Medium (gross margin) | Medium | 6 weeks | 2 |
| Infill holdout (FB-2) | Five Below | Medium (capital efficiency) | Low–medium | 2 quarters | 3 |
| Vintage dashboard and site scoring | Five Below | High over time (capital) | Medium | 3–6 months | 3 |
| Household price-response and uplift models | Netflix | High over time (revenue) | Medium | 6 months | 3 |

## 8. Sources

### Internal
- `reports/ml_handoff_report.md` §1–§8 (handoff). Several values corrected; see top table.
- `reports/ml_followups.md`, rounds 1 and 2: corrected members, H2 trend-adjusted lift, H6 sign, rate vs count tests, Five Below table, growth decomposition, margin bridge.
- `reports/exploration/findings.md`, `reports/exploration/hypotheses.md`, `reports/modeling/model_card.md`, `reports/tables/*.csv`, `reports/modeling/tables/*.csv`.
- Charts reviewed: `reports/charts/01`–`07`; `reports/exploration/charts/02`, `03`, `04`; `reports/modeling/charts/fb_expansion_scatter.png`.
- Five Below FY2025 10-K (`data/raw/five_below_10k/2026-03-19.txt`): new-store model ($2M first-year sales, $0.4M investment, ~1-year payback); 3,500+ store target.
- Netflix Q4 2025 shareholder letter (`data/raw/netflix_letters/2026-01-20_ex991_q425.htm`): 2025 ad revenue >$1.5B; 2026 guidance $50.7–51.7B, 31.5% margin.

### Web (fetched)
- [Five Below Q4 FY2025 release, SEC 8-K](https://www.sec.gov/Archives/edgar/data/1177609/000117760926000006/q42025fivebelowexhibit991.htm): FY2025 sales $4.76B, comps +12.8%, 150 net new, FY2026 guide.
- [Motley Fool, Five Below Q2 FY2025](https://www.fool.com/data-news/2025/08/27/five-below-q2-sales-top-1-billion): comps +12.4%, transactions +8.7%, whole-number pricing, above-$5 items.
- [Ollie's Q3 FY2025 release, SEC 8-K](https://www.sec.gov/Archives/edgar/data/1639300/000114036125044934/ef20060895_ex99-1.htm): comps +3.3%, 645 stores (+18.1%), 9.0% operating margin.
- [TheWrap, Netflix Q3 2025 earnings](https://www.thewrap.com/netflix-earnings-q3-2025/): UCAN Q3 revenue $5.07B (+17%); 2025 guide +16%.
- [TheWrap, Netflix 2026 price increase](https://www.thewrap.com/industry-news/business/netflix-price-increase-2026): ads $8.99, Standard $19.99, Premium $26.99; ad revenue ~$3B in 2026.
- [TheWrap, Netflix 2026 upfront](https://www.thewrap.com/media-platforms/streaming/netflix-ad-tier-monthly-active-viewers-update-upfronts-2026/): >250M ad-tier viewers; >60% of sign-ups on ads plan; ~$9B ad target by 2030.
- [Marketing Brew, Netflix 2025 upfront](https://www.marketingbrew.com/stories/2025/05/15/netflix-94-million-monthly-active-users-ads-tier-upfronts): 94M ad-tier monthly users; in-house ad tech.
- [Churnkey, streaming churn rates](https://churnkey.co/blog/churn-rates-for-streaming-services/): Netflix ~2.1% monthly vs rivals 5–7%; secondary source.
- [TheWrap / Parrot Analytics, churn economics](https://www.thewrap.com/?p=8011678): $6.3B churn loss in 2025; WWE retains ~1.25M subs per quarter (model estimate).

### Web (search results only, not fetched)
- A search summary put tariff pressure at ~150 bps a year for Five Below (StockStory/Finviz). I did not fetch the page; treat as directional.
- A Subscription Insider page returned a 404 error and was not used.

## 9. Open questions

1. **Five Below margin bridge.** Gross margin vs SG&A split for FY2023–25 needs the 10-K cost lines. The cost-of-sales field is not comparable before and after FY2023 (followups round 2).
2. **Netflix 2025 UCAN members and ARM.** Not publicly reported. No value is assumed in this memo.
3. **Ad revenue per ads-plan member, US.** Not disclosed. NF-2 sizing depends on it.
4. **Handoff chart note.** Handoff §4 links the Q1'24 residual to the January 2025 price step. That cannot be right in time order; the October 2023 step is the likelier match.

## 10. Glossary

| Term | Meaning |
|---|---|
| ARM | Average revenue per member per month: revenue ÷ average members ÷ months. |
| UCAN | Netflix's US and Canada reporting region. |
| Paid sharing | Netflix's 2023 policy charging for accounts used outside the household. |
| Extra-member slot | A paid add-on that lets an outside user join an account. |
| Churn | Share of subscribers who cancel in a period. |
| Break-even member loss | Member loss at which a price rise leaves revenue unchanged: x/(1+x). |
| Elasticity | How much demand changes when price changes. |
| Uplift model | A model of how much an action changes a person's behavior, not just their risk. |
| Persuadable | A customer whose behavior an offer actually changes. |
| Holdout | A randomly chosen group that does not receive a treatment, used for comparison. |
| Comparable sales (comps) | Sales growth in stores open at least 15 months. |
| Expansion rate | Net new stores ÷ prior year-end stores. |
| Operating margin | Operating income ÷ revenue. |
| Gross margin | (Revenue − cost of goods) ÷ revenue. |
| SG&A | Selling, general and administrative expenses. |
| Capex | Capital expenditure: cash spent on stores, distribution centers and systems. |
| Payback period | Time for a store's profits to repay its upfront investment. |
| Cannibalization | Sales a new store takes from nearby existing stores. |
| Infill | A new store opened inside an existing market. |
| Shrink | Inventory lost to theft, damage or error. |
| Ticket | Average spend per transaction. |
| bps | Basis points; 100 bps = 1 percentage point. |
| ppt | Percentage point. |
| Spearman rho | Rank correlation, from −1 to +1. |
| p-value | Chance of a result this extreme if there were no real link. |
| 95% CI | Confidence interval; range likely to contain the true value. |
| MAE | Mean absolute error of a model's predictions. |
| R² | Share of variation a model explains; negative means worse than the average. |
| Walk-forward validation | Train on past periods, predict the next, repeat. |
| Leave-one-out validation | Hold out one year at a time, train on the rest, predict it. |
| Hodges-Lehmann | A robust estimate of the median gap between two groups. |
| Collinearity | Two inputs moving together so a model cannot separate their effects. |
| Natural experiment | A real-world split that acts like random assignment. |
| Minimum detectable effect | Smallest true effect a test can reliably detect. |
| North Star metric | The one outcome a pilot is judged on. |
| Guardrail metric | A metric that must not get worse during a pilot. |
| Measured / modeled / external / assumed | Evidence labels; see "How to read this memo". |
