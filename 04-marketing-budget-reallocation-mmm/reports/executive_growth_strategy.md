# Executive Growth Strategy: Marketing Budget Reallocation
**Project:** 04-marketing-budget-reallocation-mmm
**Prepared by:** growth-strategy-partner
**Date:** 9 Nov 2026
**Inputs:** `reports/ml_handoff_report.md` (cited as HR §n), `reports/ml_followups.md` (cited as FU R1/R2 item n), 14 charts, live web sources (listed in §7).

**Evidence labels used:** measured (from the data or handoff report), modeled (a model association, not a cause), external (a cited source), assumed (my estimate).

**Read this first.** The follow-up answers corrected four claims in the handoff report. This memo uses the corrected figures. Details are in §1.3.

---

## 1. Executive Thesis and Strategic Diagnosis

### 1.1 Bottom line
Do not move budget between channels yet; the model cannot tell us which way to move it. Instead, freeze the 2019 mix, and spend the gap to the $34K/week plan on three tests.

- The proposed shift of TV money to Facebook has no established sign. On the model's own curves it loses $2,129 of revenue per week (modeled, FU R1 item 3).
- Across 11 re-fits of the model, that same shift ranges from -$1,090 to +$15,470 per week (modeled, FU R1 item 3). Six re-fits say gain, five say loss.
- Media is a small P&L lever here. 2019 spend was $28.2K/week against $1.66M/week revenue, about 1.7% (measured, FU R2 items 1-2).

**Top three value levers:**

| # | Lever | What it is worth | Label |
|---|---|---|---|
| 1 | Keep out-of-home (billboards; OOH) at the 2019 level unless a test earns it back | Avoids re-spending up to $3.3M/year (2017 OOH $3.70M vs 2019 run-rate $0.39M) | measured spend; return assumed |
| 2 | Test brand search before renewing it | Search is now the largest line: $401K in 45 weeks, 31.5% of 2019 spend. Modeled return is about zero | measured; modeled |
| 3 | Fund a standing test budget from the gap between $28.2K and $34K/week | $5.8K/week, about $0.30M/year, buys the evidence for every later reallocation | measured; assumed |

The direct profit upside of reallocation is modest: roughly $0.2M to $0.6M of yearly gross margin (assumed). The bigger value is avoiding a wrong decision on a $1.5M to $1.8M yearly budget.

### 1.2 Where the business stands
The business already ran a large, unplanned cut and revenue barely moved.

- Media spend fell from $101.4K/week in 2017 to $28.2K/week in 2019, a 72% drop (measured, FU R1 item 8).
- Most of the cut was OOH. Its share of spend fell from 70% to 27% (measured, FU R1 item 8).
- Like-for-like revenue (weeks 1-45) fell only 3.1%, from $1.712M to $1.658M per week (measured, FU R2 item 1).
- From 2018 to 2019, spend fell $29.6K/week and revenue fell $54K/week. Even if media caused all of that dip, each cut dollar cost at most $1.82 of revenue (measured inputs; attribution assumed).
- At an assumed 50% gross margin, that is $0.91 of margin lost per $1 saved. The cut was roughly break-even or better.

Value is leaking in two places. First, spend that the model cannot credit (OOH, search). Second, decisions built on figures that did not survive checking (§1.3).

### 1.3 What changed after the follow-ups
Four handoff claims should not reach Finance in their original form.

| Handoff claim | Corrected finding | Source |
|---|---|---|
| Moving 20% of TV to Facebook is "positive" | Net -$2,129/week on the curve basis; sign not established across re-fits | FU R1 item 3 |
| Event weeks lift revenue 18% across 15 weeks | Only 2 event weeks exist; lift +35% on 2 observations; not established | FU R1 item 6 |
| Total budget is flat (finding F4) | Spend fell 72% per week from 2017 to 2019 | FU R1 item 8 |
| Market demand is the largest driver | Competitor index tracks seasonality (r = 0.96); the two cannot be separated | FU R1 item 5 |
| OOH and search curves slope down due to collinearity [two inputs moving together] | Their fitted coefficients are negative; collinearity is moderate (r = 0.63) | FU R1 item 4 |
| Saturation is learned via adstock and Hill curves | Final model uses log(1+spend) only; every curve flattens by construction | FU R1 item 1 |

The last point matters most. "TV is saturated" is a property of the log formula, not a finding. Every channel's curve flattens as spend rises, by design.

### 1.4 Strategic lenses applied
Three lenses fit this data; others do not.

- **Decision economics under uncertainty (private equity rigor).** The model is good at forecasting weekly revenue (R² 0.94, MAPE 6.0%, HR §4). It is weak at splitting credit between channels. So the question is which wrong decision costs most.
- **Uplift thinking (prediction is not causation).** The model predicts revenue well, yet it cannot say what a spend change causes. Only a controlled test can.
- **Test-and-learn flywheel (Amazon-style compounding loop).** Each test calibrates the model. A better model picks better tests. Over 2-3 cycles the budget converges on proven returns.

Funnel and loyalty frameworks do not apply. There is no customer-level data in this dataset.

---

## 2. Internal vs External Benchmark Gap Analysis

**Conclusion:** The brand spends less on media than typical, and its model claims returns well above external norms for print. That gap is a warning sign, not an opportunity.

| Metric | This business | External benchmark | Gap reading |
|---|---|---|---|
| Paid media as % of revenue | 3.8% over 4 years; about 1.7% in 2019 (measured, HR §2; FU R2) | 2.4% of revenue on paid media (Gartner 2025 via MarTech; external) | Now below the cross-industry norm |
| Total marketing as % of revenue | Not available | 7.7% average; half of CMOs at 6% or less (Gartner 2025; external) | Cannot compare; non-media costs not in data |
| Linear TV return | Same-week only: $1.21 revenue per $1 at average spend; 4-year average $5.70 (modeled, FU R1 items 2, 7) | Full-profit ROI GBP 5.94 per GBP 1; short-term all-channel average GBP 1.87 (Thinkbox Profit Ability 2; external) | Average plausible; same-week figure likely understates TV (no carry-over in model) |
| Long-term vs short-term effect | Not measured; model has no carry-over term (FU R1 item 1) | Sustained effects lift average ROI from GBP 1.87 to GBP 4.11, about 2.2x (Thinkbox; external) | TV and print value may be understated by up to about 2x (assumed) |
| TV saturation point | Model says "saturated" at $16K-$34K/week (HR §5) | Linear TV has the highest saturation point of all channels, GBP 330K (Thinkbox; external; period basis not stated on page) | Model's TV saturation is a formula artifact, not evidence |
| Print return | 4-year average $19.2 revenue per $1 ($14.9M on $0.78M) (modeled, FU R1 item 7) | Thinkbox: print saturates at about a third of TV's point; no print ROI stated (external) | Implausibly high; print coefficient not identified (VIF 43.6) |
| Paid search incrementality | Marginal return -$0.08 per $1 (modeled) | eBay field test: brand-keyword ads near zero incremental; about $0.25 revenue per $1 short run (Blake, Nosko and Tadelis via Slate; external) | Consistent: search may capture demand that would arrive anyway |
| OOH return | Negative coefficient; -$8.1M modeled over 4 years (FU R1 item 7) | Vendor MMMs (700+ studies) report relative OOH gains, e.g. +39% for mixed formats; no per-dollar figure (Analytic Partners for oOh!media; external) | No external per-dollar OOH benchmark found; label unverified |
| Facebook / paid social return | $0.96 revenue per $1 at average spend (modeled) | Hourglass geo holdout: Meta lift 10.4%, incremental cost per acquisition $130 (Rockerbox; external, vendor) | Single vendor case; not comparable in units |

**Market shifts from research (external):**
- Budgets are flat and under scrutiny. Gartner reports 7.7% of revenue for a second year (MarTech, Campaign Asia).
- Only 32% of marketers measure traditional and digital media together, though 85% say they are confident (Nielsen 2025).
- Bayesian MMM tools now take experiment results as inputs. Google Meridian calls this "calibration" and advises prioritizing low-spend channels, which a model may over-credit.
- Geo tests below about $40K per channel per month rarely reach significance in 4 weeks (Elevarus; external, an operator rule of thumb). Every channel here is below that.

**What I could not verify:** Gartner's own press release, the Circana TV page and the mi-3 Thinkbox snapshot returned errors. I used secondary reports of Gartner. I found no per-dollar OOH benchmark and no consumer-brand gross margin benchmark.

---

## 3. Data-to-Dollars Translation

### 3.1 Channel unit economics
**Conclusion:** Only print clears break-even on the model's numbers, and print is the least reliable estimate.

Break-even assumes a 50% gross margin (assumed). At that margin a channel must return $2.00 of revenue per $1 to pay for itself.

| Channel | 2019 spend/week (share) | Revenue per extra $1 at average spend | Clears $2.00 break-even? | Reliability |
|---|---|---|---|---|
| TV | $7,298 (25.8%) | $1.21 | No on same-week basis; maybe with carry-over | Coefficient stable across re-fits |
| OOH | $7,556 (26.8%) | -$0.19 | No | Negative sign; cause unknown |
| Print | $2,470 (8.7%) | $4.74 | Yes | Not identified (VIF 43.6 with "print = 0" flag) |
| Facebook | $2,009 (7.1%) | $0.96 | No | Coefficient ranges 5x across re-fits |
| Search | $8,909 (31.5%) | -$0.08 | No | Near zero |

Spend figures measured (FU R2 item 2). Returns modeled (FU R1 item 2), at all-week average spend.

Two readings follow.
- Capital is concentrated where evidence is weakest. Search plus OOH took 58% of 2019 spend. The model credits neither.
- The brief's claim that Facebook is "the steepest curve" is not supported. At average spend, print ($4.74) and TV ($1.21) both beat Facebook ($0.96).

### 3.2 Controllable levers vs structural traits
**Conclusion:** Seasonality drives most of revenue; the levers marketing controls are small and must be tested.

| Type | Feature | Use it for | Evidence |
|---|---|---|---|
| Structural | Competitor index plus season (r = 0.96) | Forecasting and timing of flights | SHAP $392K mean (modeled, HR §5) |
| Structural | Trend | Baseline planning | SHAP $21K (modeled) |
| Semi-controllable | Event weeks | Not yet usable; only 2 weeks | +35% on 2 weeks (measured, FU R1 item 6) |
| Controllable | TV, print, OOH, Facebook, search spend | Testing, then reallocation | §3.1 |
| Controllable | Newsletter sends | Low-cost lever; untested | SHAP $12K (modeled, chart 02) |
| Controllable | Flighting (on/off weeks) | Concentrate spend in high-season weeks | Channels are on fewer than half of 2019 weeks (measured, FU R2 item 2) |

The decile chart (HR §6, chart 03) shows top-decile weeks earn 1.59x the mean. That is mostly season. It tells us when demand is high, not what media did.

### 3.3 Decision thresholds and the cost of being wrong
**Conclusion:** Require stronger proof to cut TV than to cut search or OOH, because TV's effect lasts longer than the model can see.

For a marketing mix model [MMM; a model linking weekly spend to weekly revenue], the "threshold" is the test result that triggers a budget move.

| Error | Meaning | Cost per $1 of spend | Most exposed channel |
|---|---|---|---|
| False positive | Keep paying for a channel that does nothing | $1.00 of wasted spend | Search ($401K in 2019), OOH |
| False negative | Cut a channel that works | Lost margin, = return x 50% margin; plus brand decay | TV (long carry-over per Thinkbox) |

**Decision rules (assumed 50% gross margin):**
- **Scale a channel** when the test's 90% confidence lower bound on incremental return [extra revenue caused per $1] is at least $2.00.
- **Cut a short-memory channel** (search, Facebook) when the upper bound is below $2.00.
- **Cut TV or print** only when the upper bound is below $1.00. This allows for the roughly 2.2x long-term multiplier Thinkbox reports (external).
- **Otherwise hold** and extend the test.

---

## 4. Dual-Track Recommendations

### Track A: Measurement, model and data (Data/Engineering owns)
**Conclusion:** The model should forecast and plan tests now; it should not allocate money until experiments calibrate it.

1. **Use the current model for forecasting only.** Its 6.0% weekly error (HR §4) is good enough for revenue planning. Do not use its channel returns for budget moves.
2. **Rebuild as a Bayesian, geo-level MMM** [a model that combines prior knowledge with data and uses regional variation]. Google Meridian supports this. Estimate carry-over and saturation from data, not fixed formulas (HR §7 G2-G4).
3. **Calibrate with the pilots in §5.** Meridian turns test results into ROI priors [starting beliefs the model updates]. Widen priors when a test's setup differs from the model's (Meridian docs; external).
4. **Fix the print feature.** The "print = 0" flag duplicates print spend (VIF 43.5). Drop one before re-fitting (FU R1 item 1).
5. **Separate season from the competitor index.** They move together at r = 0.96. Use one, or replace the index with a cleaner demand signal (FU R1 item 5).
6. **Instrument what is missing:**
   - Brand vs non-brand search spend and clicks (needed for Pilot 4).
   - Weekly price and promotion index (HR §7 G6).
   - Revenue and spend by region, at least 20 markets.
   - A verified event calendar. The current file has 2 events, not 15.
   - Online vs offline sales split, to read Facebook lift tests.
7. **Drift guardrails.** Track weekly forecast error. Re-fit when 8-week rolling MAPE exceeds 10% (assumed), against 6.0% today.

### Track B: Commercial, finance and media buying (Marketing/Finance owns)
**Conclusion:** Five policy moves capture value before any model goes live.

1. **Freeze the 2019 mix as next year's base, except OOH (item 3).** That is $28.2K/week: TV 26%, OOH 27%, search 32%, print 9%, Facebook 7% (measured, FU R2 item 2).
2. **Release the remaining $5.8K/week only as test money.** That closes the gap to the $34K/week plan in the brief. It is about $0.30M/year (assumed run-rate).
3. **Put OOH behind a gate.** No OOH above 2019 levels without a passed test. The 2017-2019 cut removed $3.3M/year of OOH with a 1-3% revenue dip (measured).
4. **Correct the record to Finance.** Withdraw the 18% event lift, the "flat budget" claim, and the TV-to-Facebook "positive" claim (§1.3).
5. **Tie agency pay to incremental results.** Pay on tested incremental return, not platform-attributed return. eBay's test showed attributed and incremental returns can differ greatly (external).
6. **Concentrate flights in high-season weeks.** Spend is already lumpy; align on-weeks with the seasonal peaks in chart 03. Validate within Pilot 2.

**Provisional plan at $34K/week (budget-neutral to the brief):**

| Line | $/week | Share | Basis |
|---|---|---|---|
| TV | 7,300 | 21% | 2019 level held |
| OOH | 4,000 | 12% | Cut from $7.6K; remainder reserved for re-entry only if tested |
| Print | 2,500 | 7% | 2019 level held pending Pilot 1 |
| Facebook | 2,000 | 6% | 2019 level; heavy-up funded inside Pilot 3 |
| Search | 8,900 | 26% | 2019 level held pending Pilot 4 |
| Test fund | 9,300 | 27% | $5.8K gap plus $3.5K from OOH |
| **Total** | **34,000** | **100%** | |

Line amounts assumed; base shares measured. Revisit after Day 90.

---

## 5. Pilot Experiments Portfolio (90-Day Growth Lab)

**Conclusion:** Test with big swings in a few regions, not small tweaks everywhere. Small tweaks are invisible against weekly noise.

### 5.1 Why small tests fail here
Each channel's 2019 spend is at most 0.54% of weekly revenue (measured). The model's weekly error is 12.7% of revenue in training ($231K SD; measured, FU R2 item 3).

Sizing for a regional test (assumed inputs flagged):

| Input | Value | Label |
|---|---|---|
| Weekly revenue variation per region | 27.6% (median CV, Meridian sample of 20 regions) | measured, FU R2 item 4 (simulated data) |
| Pre-period fit of test vs control regions | correlation 0.96-0.98 | external, Rockerbox Hourglass case |
| Remaining weekly noise after matching | about 5% of test-region revenue | assumed (27.6% x sqrt(1 - 0.97²) ≈ 6.7%, pooled across regions) |
| Minimum detectable effect [MDE; the smallest true lift a test can reliably see], 8 weeks | about 4.4% of test-region revenue | assumed (2.49 x 5% / sqrt 8; 80% power, 10% two-sided) |
| MDE, 12 weeks | about 3.6% | assumed |

Implication: a regional test can only falsify large claims. The model claims TV drives 4.6% of revenue and print 3.9% (modeled, FU R1 item 7). Those claims are testable. Facebook (0.5%) and search are not testable by region; they need platform or keyword-level designs.

**Region pool:** The brand needs real regional sales data. The Meridian file (20 regions, 7x size range) is a simulated stand-in for design only (FU R2 item 4).

### Pilot 1: Print go-dark falsification test
- **Playbook:** Regional holdout [some regions stop the channel; matched regions continue].
- **Internal trigger:** Print shows the highest modeled return, $4.74 per $1, and $14.9M over 4 years on $0.78M spend (FU R1 items 2, 7). Its coefficient is not identified (VIF 43.6).
- **External trigger:** A 19x average return is far above Thinkbox's all-channel full ROI of GBP 4.11 (external).
- **Hypothesis:** If we stop print in 30% of regions for 12 weeks, revenue there falls 0-4% versus control. If the fall is below 1%, print's modeled return is refuted.
- **Design:** 6 test regions, 14 controls, matched on 52 weeks of history. Synthetic control [a weighted blend of control regions built to track the test regions]. 12 weeks, inside a print flight.
- **Execution:** Data builds region matching and the read. Media pauses print by region. Finance books saved spend.
- **North Star:** Revenue in test vs synthetic control.
- **Guardrails:** Test-region revenue drop above 8% stops the test. Pre-period fit correlation must be at least 0.95.
- **Decision rules:**
  - Day 30: verify print is dark and fit holds; else fix or restart.
  - Day 60: harm check only; no early win calls.
  - Day 90 scale: drop of 2.5% or more, CI excludes zero; raise print to about $4K/week from the test fund.
  - Day 90 kill: drop below 1% with upper bound below 2.5%; cut print by half; re-fit model without print flag.
  - Otherwise: extend 6 weeks.
- **Cost at risk:** If the model is right, about $0.2M of revenue (3.9% x 30% x $1.66M x 12 weeks; modeled). Print saved: about $9K (measured base, assumed share).

### Pilot 2: TV go-dark falsification test
- **Playbook:** Regional holdout, run as a separate cell alongside Pilot 1.
- **Internal trigger:** TV's coefficient is the most stable across 11 re-fits (FU R1 item 3). The model credits TV with $17.6M over 4 years (modeled).
- **External trigger:** Thinkbox puts linear TV's full-profit ROI at GBP 5.94, highest of all channels (external).
- **Hypothesis:** If TV goes dark in 25% of regions for 12 weeks, revenue there falls 2-5%. TV's short-term effect then supports at least the 2019 TV budget.
- **Design:** 5 test regions, separate from Pilot 1's 6. Same controls. Measure for 6 weeks after the test to catch carry-over.
- **Execution:** Data builds cells. Media buys regional TV (or local cut-ins). Finance tracks post-test recovery.
- **North Star:** Test-period plus 6-week post-period revenue vs control.
- **Guardrails:** Revenue drop above 8%; brand search volume in test regions (early sign of brand decay).
- **Decision rules:**
  - Day 30: compliance and fit.
  - Day 90 scale: drop of 3% or more; hold TV and test a heavy-up next cycle.
  - Day 90 kill: upper bound below 1%; this implies under $1.00 per $1 even with carry-over; cut TV 25% next cycle.
  - Otherwise: hold TV; re-test with heavy-up design.
- **Note:** This replaces the TV-to-Facebook shift. The shift moves about 0.2% of revenue, far below any MDE.

### Pilot 3: Facebook heavy-up conversion lift
- **Playbook:** Platform-randomized lift test [the platform withholds ads from a random group of users].
- **Internal trigger:** Facebook's coefficient swings 5x across re-fits (3,772 to 19,760; FU R1 item 3). Facebook correlates 0.37 with the competitor index (FU R1 item 5), so the model may under-credit it.
- **External trigger:** Under $40K per channel per month, platform lift beats regional tests (Elevarus; external). Hourglass measured a 10.4% Meta lift in a holdout (external, vendor).
- **Hypothesis:** If we raise Facebook from $2K to $8K/week for 8 weeks, incremental return is $1.00-$3.00 per $1, because current spend reaches few people.
- **Design:** Meta Conversion Lift, 15% user holdout. 8 weeks. Extra spend about $48K ($6K x 8 weeks) from the test fund (assumed).
- **Execution:** Marketing runs creative and lift study. Data joins online orders. Finance applies the margin rule.
- **North Star:** Incremental revenue per $1, online orders.
- **Guardrails:** Cost per incremental order; frequency cap at 3 per week (assumed).
- **Decision rules:**
  - Day 30: delivery and holdout integrity.
  - Day 60 scale: lower bound at least $2.00; fund $6K/week ongoing.
  - Day 60 kill: upper bound below $1.00; return to $2K/week.
  - Otherwise: run to Day 90 and decide on point estimate vs $2.00.
- **Limit:** Measures online sales only. Offline effects need a later regional test.

### Pilot 4: Brand search holdout
- **Playbook:** Keyword holdout by region (eBay method).
- **Internal trigger:** Search is 31.5% of 2019 spend, rising from $264K (2017) to about $400K per year. Its modeled return is -$0.08 per $1 (FU R1 items 2, 8).
- **External trigger:** eBay found brand-keyword ads near zero incremental; customers clicked the free listing instead (external).
- **Hypothesis:** If we pause brand keywords in 50% of regions for 8 weeks, total brand-search orders (paid plus free clicks) fall less than 15%, because most clicks move to the free listing.
- **Design:** Split regions 50/50, matched on brand search volume. Non-brand keywords unchanged. 8 weeks.
- **Execution:** Data needs brand vs non-brand split (gap today). Search team pauses terms. Finance books savings.
- **North Star:** Total brand-search orders per region (paid plus free).
- **Guardrails:** Competitor bidding on our brand terms; total revenue in test regions.
- **Decision rules:**
  - Day 30: recapture rate. Above 85% recapture: extend pause to all regions.
  - Day 60 kill (keep brand search): recapture under 70%, or competitors take the top slot.
  - Day 90: set brand budget to defend-only levels.
- **Value:** If half of search is brand (assumed) and non-incremental, saving is about $0.2M/year.

### Pilot 5 (Wave 3): OOH re-entry gate
- **Trigger:** OOH was 62% of 4-year spend with a negative modeled coefficient (HR §6; FU R1 item 1). Revenue held as OOH fell 90% (FU R2 item 1).
- **Design:** Only if Marketing wants OOH back. Heavy-up in 5 regions for 12 weeks. Scale only if lift exceeds MDE and return is at least $2.00 per $1.

---

## 6. Prioritization Matrix

| Initiative | Financial impact (P&L driver) | Confidence | Ease / time-to-value | Wave |
|---|---|---|---|---|
| Correct the record to Finance (§1.3) | High (avoids misallocating $1.8M budget) | High (FU R1) | 1 week, low effort | 1 |
| Freeze 2019 mix; no TV-to-Facebook shift | Med (avoids modeled -$2.1K/week) | High | 1 week | 1 |
| OOH gate at 2019 level | High (up to $3.3M/year avoided) | Med (observational) | 2 weeks, policy | 1 |
| Ring-fenced test fund $5.8K/week | Med (enables all pilots) | High | 2 weeks, Finance | 1 |
| Pilot 4 brand search holdout | Med (about $0.2M/year margin) | Med (eBay external; model) | 4 weeks; needs keyword split | 2 |
| Pilot 3 Facebook lift | Low-Med (revenue) | Low (unstable coefficient) | 3 weeks; platform tool | 2 |
| Pilot 1 print go-dark | Med (validates or kills model) | Low (not identified) | 6 weeks; regional data needed | 2 |
| Pilot 2 TV go-dark | High (largest credited channel) | Med (stable coefficient; Thinkbox) | 8 weeks; regional TV buying | 2 |
| Incremental-based agency pay | Med (cost discipline) | Med | 1 quarter, contracts | 2 |
| Bayesian regional MMM with calibration | High (long-run allocation) | Med | 1-2 quarters | 3 |
| Pilot 5 OOH re-entry | Low-Med | Low | 12 weeks | 3 |
| Event-calendar program | Unknown | Not established (2 weeks) | Needs data first | 3 |

**Open questions:** True gross margin (assumed 50%). Real regional sales data. Brand vs non-brand search split. Whether the brand has offline sales that Facebook lift cannot see.

---

## 7. Verified Web Sources

| URL | What was extracted |
|---|---|
| [Thinkbox Profit Ability 2](https://www.thinkbox.tv/research/thinkbox-research/profit-ability-2-the-new-business-case-for-advertising) | Linear TV full-profit ROI GBP 5.94; all-channel GBP 1.87 short-term, GBP 4.11 with sustained effects; TV saturation point GBP 330K; 141 brands, GBP 1.8B |
| [MarTech on Gartner 2025 CMO Spend Survey](https://martech.org/cmos-brace-for-cuts-as-marketing-budgets-stay-flat/) | Marketing 7.7% of revenue; paid media 30.6% of budget, 2.4% of revenue; 402 leaders, Feb-Mar 2025 |
| [Campaign Asia on Gartner 2025](https://www.campaignasia.com/article/marketing-budgets-hold-at-7-7-in-2025-gartner-cmo-survey/502806) | Confirms 7.7%; half of CMOs at 6% or less |
| [Slate/HBR on eBay paid search study](https://www.slate.com/articles/business/harvard_business_review/2013/03/paid_search_ads_did_ebay_just_prove_they_don_t_work.html) | Brand keyword ads near zero incremental; about $0.25 revenue per $1 short run |
| [Google Meridian ROI priors and calibration](https://developers.google.com/meridian/docs/advanced-modeling/roi-priors-and-calibration) | How experiments become ROI priors; zero-spend vs reduced-spend mismatch; prioritize low-spend channels |
| [GeoLift walkthrough (Meta)](https://facebookincubator.github.io/GeoLift/docs/GettingStarted/Walkthrough/) | Power analysis first; test length at least one purchase cycle; market selection by pre-period fit |
| [Rockerbox: Hourglass geo holdout](https://www.rockerbox.com/customers/how-hourglass-cosmetics-validated-metas-true-impact-with-a-geo-holdout-test) | 10 holdout markets, 6 weeks; 10.4% lift; $130 incremental CPA; pre-test fit 0.96-0.98 |
| [Elevarus spend-tier framework](https://elevarus.com/incrementality-testing-agencies-spend-tier-framework/) | About $40K per channel per month floor for 4-week geo tests; 8-12 weeks for $40-80K; holdout under 15% of regions is too small |
| [Mediaweek on Analytic Partners OOH study](https://www.mediaweek.com.au/ooh-campaigns-perform-better-when-classic-and-digital-work-together/) | 700+ MMM studies; relative OOH gains (+39% mixed formats); no per-dollar ROI; vendor-supported |
| [Nielsen 2025 ROI Blueprint](https://www.nielsen.com/fr/news-center/2025/nielsen-unveils-makerting-roi-blueprint/) | 32% measure ROI holistically vs 85% confident |

**Fetch failures (not used as evidence):** Gartner press release (403), Circana linear TV blog (404), mi-3 Thinkbox snapshot (403), AdNews OOH article (403), ITV Media summary (404), NBER eBay PDF (unreadable).

---

## 8. Glossary

| Term | Plain meaning |
|---|---|
| MMM (marketing mix model) | A model linking weekly spend by channel to weekly revenue, controlling for season |
| Bayesian MMM | An MMM that combines prior beliefs (e.g. test results) with data |
| Prior / calibration | A starting belief in a Bayesian model; calibration sets it from experiments |
| Response curve | Predicted revenue at each spend level for one channel, others held fixed |
| Marginal return | Extra revenue from the next $1 of spend |
| Incremental return (iROAS) | Extra revenue caused by $1 of spend, measured by a test |
| Average return | Total credited revenue divided by total spend |
| Break-even return | Revenue per $1 needed to cover spend; $1 divided by gross margin |
| Gross margin | Revenue minus cost of goods, as % of revenue |
| Adstock / carry-over | Advertising effect that lasts into later weeks |
| Saturation / Hill curve | Diminishing returns as spend rises; Hill is one formula for it |
| SHAP | Average dollar amount each input adds to a prediction |
| Coefficient | The model's weight on an input |
| Collinearity | Two inputs moving together, so their effects cannot be separated |
| VIF (variance inflation factor) | How much collinearity inflates a coefficient's uncertainty; above 10 is severe |
| Re-fit / cross-validation | Re-training the model on earlier windows and testing on later ones |
| RMSE | Typical dollar size of a forecast error |
| MAPE | Average forecast error as % of actual |
| R² | Share of revenue variation the model explains |
| Residual | Actual minus predicted revenue |
| CV (coefficient of variation) | Standard deviation divided by mean |
| Baseline | Revenue expected with zero media |
| Counterfactual | The "what if" scenario a result is compared against |
| Geo holdout / regional test | Some regions change spend; matched regions do not |
| Go-dark / heavy-up | Turn a channel off / raise it sharply in test regions |
| Synthetic control | Weighted blend of control regions that tracks test regions |
| MDE (minimum detectable effect) | Smallest true lift a test can reliably detect |
| Power | Chance a test detects a real effect of a given size |
| Confidence interval (CI) | Range likely to contain the true value |
| Conversion lift | Platform test that withholds ads from random users |
| Brand search | Paid ads on searches for the brand's own name |
| Recapture rate | Share of brand-search orders that still arrive through free listings when ads pause |
| CPA / incremental CPA | Cost per acquisition; incremental version counts only caused sales |
| False positive / false negative | Funding a channel that does not work / cutting one that does |
| OOH (out-of-home) | Billboards and other outdoor ads |
| Linear TV / BVOD | Scheduled broadcast TV / broadcaster video on demand |
| Flighting | Running a channel in bursts of on and off weeks |
| Test-and-learn flywheel | Loop where tests improve the model, which picks better tests |
| P&L | Profit and loss statement |
