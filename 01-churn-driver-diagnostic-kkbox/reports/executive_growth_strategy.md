# Executive growth strategy: stopping first-year fiber churn

Prepared by the growth strategy advisor, 27 October 2026.
Inputs: `reports/ml_handoff_report.md` (cited as "Handoff s.N"), `reports/ml_followups.md` (cited as "Followups R1/R2"), eight charts in `reports/charts/`, and live web sources (section 7).

**Evidence labels.** Every number carries one label.
- **measured**: counted in the data (handoff report or follow-ups).
- **modeled**: a model association, not a cause.
- **external**: from a cited web source, with its URL in section 7.
- **assumed**: my estimate, chosen and not measured.

**Data caveat.** The data is IBM's fictional California telecom sample. It covers one quarter and has no dates. External figures describe real US operators in 2025. Read every gap as directional.

---

## 1. Executive thesis and diagnosis

**Bottom line: churn here is a first-year fiber onboarding and commitment problem. Fix the first 90 days and the sales default before buying more retention offers.**

The business loses 1,869 of 7,043 customers (26.5%) in the window (measured, Handoff s.2). Those leavers paid $139,131 per month, or $1,669,570 per year (measured, Handoff s.2). That is 30.5% of monthly revenue (measured).

The loss is concentrated. Month-to-month fiber customers in their first 12 months are 916 customers, 13.0% of the base (measured, Handoff s.3). They leave at 70.2% and hold 38.2% of lost revenue (measured). In their first two months, these customers leave at 80.5% (measured, Followups R2-Q2).

**Top three value levers.** The ranges are directional and before offer cost.

| # | Lever | Who | Directional impact, revenue kept per year | Basis |
|---|---|---|---|---|
| 1 | Commitment offer (a one-year price lock instead of plain month-to-month), sent by uplift-tested targeting | 2,548 month-to-month customers scored 0.3 or higher (measured, Followups R2-Q3) | $96k to $203k (assumed) | 4.1 to 8.7 point churn cut from uplift-targeted field tests (external, Ascarza); applied to this group's 55% churn and $76 mean bill (measured) |
| 2 | Fiber first-90-days programme (install check, first-bill call, free tech-support trial) | About 115 new month-to-month fiber customers per month (assumed, from 344 customers in months 0-2) | $66k to $132k per yearly cohort (assumed) | 5 to 10 point cut in year-one churn (assumed); Frontier credits installation and first-bill focus for lower churn (external) |
| 3 | Autopay switch for tenured electronic-check payers, plus autopay as the sign-up default | 676 month-to-month fiber customers past month 12 paying by electronic check (measured, derived from Followups R1-Q1 and R2-Q1) | About $19k (assumed) | 50.3% vs 33.6% churn gap (measured, derived); near-zero cost |

Together these levers could keep roughly $180k to $350k per year (assumed). That is 11% to 21% of the $1.67M annual loss (assumed). It is 3% to 6% of the $5.47M annual revenue base ($456,117 x 12, measured).

**What I am not saying.** No number in this data proves an offer works (Handoff s.1, s.7 item 1). Every lever above needs a randomised pilot with a holdout (a group that gets nothing) before scaling.

### 1.1 Internal vs market diagnosis

**This business churns several times faster than real US broadband operators, and its fiber product behaves backwards.**

- Even read as an annual rate, 26.5% is well above Frontier's annualised fiber churn of about 15.6%. That comes from 1.41% per month (external, Frontier Q3 2025).
- If the window is one quarter, 26.5% equals about 9.8% per month (assumed conversion). That is about seven times Frontier's 1.41% (external).
- In the US market, fiber is the stickiest product. Fiber providers scored 75 vs 70 for non-fiber in the 2025 customer satisfaction index (external, ACSI via BGR).
- Here, fiber customers leave at 41.9% vs 19.0% on DSL (measured, Handoff s.3). This holds inside every contract type (measured, chart 03).
- Fiber customers here pay a mean $91.50 per month (measured, $283,284 / 3,096). Frontier's fiber average revenue per user is $68.59 (external). Comcast sells 1.1 Gbps at $85 locked for five years (external).

**Where value leaks.** Three leaks explain most of the loss.
1. **The sales default.** 55.0% of customers are month-to-month (measured). They hold 86.9% of lost revenue (measured, chart 04).
2. **The first 90 days of fiber.** Fiber churn is 80.5% in months 0-2, then 66.2% in months 3-6 (measured, Followups R2-Q2).
3. **Fiber price-for-value.** Fiber bills are high and churn is high. The data cannot separate price from product (Handoff s.7 item 5).

### 1.2 Strategic lenses applied

**Three lenses explain this data. Others add little.**

- **Cohort survival economics (Bain).** Churn falls steeply with tenure: 52.9% in months 0-6 vs 9.5% after month 48 (measured, chart 02). A customer who survives year one is worth far more. So the money is in early survival, not late-stage rescue.
- **Uplift targeting (persuadability).** The model finds who will leave. It does not find who can be persuaded to stay. Field research shows that targeting by persuadability beats targeting by risk (external, Ascarza).
- **Input-metric flywheel (Amazon).** Controllable inputs are the sales default, autopay enrolment and first-90-day contact. These drive the output metric, twelve-month survival.

---

## 2. Internal vs external benchmark gap analysis

**The business trails the market on churn, fiber stickiness and pricing structure. The model's ranking is usable.**

| Metric | This business | External benchmark | Reading |
|---|---|---|---|
| Customer churn | 26.5% per window (measured); about 9.8% per month if the window is a quarter (assumed conversion) | Frontier consumer fiber 1.41% per month, Q3 2025, down from 1.49% (external) | Far worse on any reading of the window |
| Fiber vs non-fiber | Fiber churn 41.9% vs DSL 19.0% (measured) | Fiber index score 75 vs non-fiber 70, 2025 (external, ACSI via BGR) | Inverted. Fiber should be the stickiest product |
| Fiber monthly bill | $91.50 mean (measured) | Frontier fiber revenue per user $68.59 (external); Comcast 1.1 Gbps $85, 5-year lock (external) | Bill sits above market. Data is fictional and of another era |
| Commitment model | 55.0% month-to-month, no price lock (measured) | Comcast 5-year price guarantee, no annual contract; Verizon 3-year lock (external) | Market sells commitment as a price promise, not a penalty |
| Autopay structure | 33.6% pay by electronic check (measured) | Comcast charges $10 more per month without autopay and paperless billing (external) | Market prices the non-autopay path explicitly |
| Retention targeting | Top 10% by risk churn at 76.0% (measured, pooled, Handoff s.6.2) | Uplift targeting cut churn 4.1 to 8.7 points; risk-targeting sometimes raised churn (external, Ascarza) | High risk does not mean savable |
| Onboarding | Months 0-2 fiber churn 80.5% (measured) | Frontier credits installation and first-bill focus for better retention (external) | The first bill is the moment to fix |

**Competitor and market moves found in research.**
- **Price locks replace contracts.** Comcast launched a five-year price guarantee in April 2025, with no annual contract (external). Verizon offers a three-year lock on mobile and home internet (external).
- **Bundles lower churn.** Charter says churn is "much lower" for customers who take home and mobile together (external). Over a quarter of US households take a broadband-wireless bundle (external, Parks Associates via The Desk).
- **Fixed wireless and fiber pressure cable.** Comcast, Charter and Optimum had 280,000 broadband disconnects in Q1 2026 (external).
- **Cancellation rules tighten in California.** California's amended automatic renewal law took effect 1 July 2025. It regulates cancellation mechanisms (external). The federal click-to-cancel rule was vacated on 8 July 2025 (external). Save offers at the cancellation step need legal review.

**What I could not verify.**
- S&P Kagan's 1.25% average monthly churn (Q3 2025) appeared in search summaries only. The page returned 403. I do not use it.
- AT&T's Q1 2025 postpaid phone churn of 0.83% appeared in search summaries only. The pages returned 403. I do not use it.
- The Telenor uplift case (11-fold return gain) could not be fetched. I do not use it.
- I found no independent broadband save-rate benchmark or acquisition cost per customer. Those inputs stay assumed.

---

## 3. Data-to-dollars translation

### 3.1 Segment unit economics

**One micro-segment destroys most value. The two-year base compounds it.**

| Segment | Customers (% of base) | Churn | Lost revenue, $/month (% of total) | Role |
|---|---|---|---|---|
| Month-to-month fiber, months 0-12 | 916 (13.0%) | 70.2% | 53,178 (38.2%) | Main value leak (measured) |
| Month-to-month fiber, months 0-2 | 344 | 80.5% | not computed | Onboarding cliff (measured, R2-Q2) |
| Month-to-month fiber, months 13+ | 1,212 | 42.8% | not computed | Second leak, mid-life (measured, R2-Q2) |
| Two-year contract | 1,695 (24.1%) | 2.8% | 4,165 (3.0%) | Compounding base (measured) |

All rows from Handoff s.6.1 unless marked.

**Where effort is misallocated.**
- Payment method matters only after year one. In months 0-12, autopay payers leave at 72.2% vs 71.2% for electronic check (measured, R2-Q1). After month 12, the gap is 33.6% vs 50.3% (measured, derived from R1-Q1 and R2-Q1). An autopay push at new customers would waste effort.
- Tech support links to lower churn on month-to-month fiber: 38.9% with vs 57.5% without (measured, R1-Q3). Buyers self-select, so this is not proof.
- Treating everyone above 0.5 risk misses the middle. Month-to-month customers scored 0.3 to 0.5 number 1,042, leave at 37.3%, and pay $72.60 (measured, R2-Q3).

### 3.2 Controllable levers vs structural traits

**Use traits to pick who; use levers to change what. Never use age or gender to set offers.**

| Type | Columns | Use |
|---|---|---|
| Structural traits | tenure, SeniorCitizen, Partner, Dependents, gender | Targeting and timing only. Gender excluded. Seniors are 30.7% of the top-20% risk group vs 16.2% of the base (measured, R1-Q6). Cap offer differences by age |
| Slow levers (product and price) | InternetService, MonthlyCharges, MultipleLines | Fiber price-for-value review. Price and product cannot be separated in this data (Handoff s.7 item 5) |
| Fast levers (offer and process) | Contract, PaymentMethod, TechSupport, add-ons | Pilots. Contract is the strongest: modeled -18.0 points (95% interval -18.6 to -17.4) (modeled, Handoff s.5) |

**Do not size the add-on levers.** Their effect swings 5 to 13 times with the bill assumption (Handoff s.5).
**Do not act on paperless billing.** The model links paper bills to lower churn, but there is no business story (Handoff s.5).

### 3.3 Profit-maximising thresholds

**Contact a customer when predicted churn times monthly bill is at least about $32. On current inputs, that is a cutoff near 0.4 to 0.5.**

The two error costs are unequal.
- **False positive** (flagging a stayer): contact cost $5 plus a $60 credit to 30% of contacts who accept. Expected $23 per flag (assumed). Add the risk of prompting a stayer to leave (external, Ascarza).
- **False negative** (missing a leaver): lost save value. Assumed 10% save rate x $77 bill x 60% gross margin x 12 months kept = about $55 (assumed).
- A missed leaver costs about 2.4 times a wasted flag (assumed). So the cutoff should sit below 0.5, adjusted for the bill.
- Rule: contact if probability x bill x 0.72 is at least $23. The 0.72 is save rate x margin x months (assumed). For a $80 bill, the cutoff is 0.40. For a $50 bill, it is 0.64.

Held-out test results, using counts from Followups R1-Q5 (measured) and the assumptions above:

| Cutoff | Flagged of 1,409 | Leavers flagged | Bill of flagged leavers, $/month | Net value per campaign, $ (assumed) | Break-even save rate (assumed) |
|---|---|---|---|---|---|
| 0.3 | 531 | 286 | 21,656 | 3,379 | 7.8% |
| 0.4 | 422 | 246 | 19,003 | 3,976 | 7.1% |
| 0.5 | 299 | 200 | 15,370 | 4,189 | 6.2% |
| 0.6 | 197 | 142 | 11,000 | 3,389 | 5.7% |

**Reading.**
- Value peaks near 0.5 but is flat from 0.4 to 0.5.
- Scaled to the full base (x5.0), net value at 0.5 is about $21k per campaign (assumed).
- At a 5% save rate, every cutoff loses money (assumed). At 20%, net at 0.5 rises to about $76k on the full base (assumed).
- **The save rate decides everything. It is unknown.** Pilot 1 exists to measure it.

---

## 4. Dual-track recommendations

### Track A: Technical, product and AI operationalisation

**Ship the score as a weekly list into the customer system, with a permanent holdout, and switch from risk to uplift within two quarters.**

1. **Deployment.** Score all customers weekly in a batch job. Write score, decile and expected value at risk into the customer record (the CRM). The model is a calibrated logistic regression; error is 0.021 average calibration gap (measured, Handoff s.4).
2. **People in the loop.** Retention agents see the score, top reason codes and a scripted offer. Agents log the offer, acceptance and outcome. Without this log no return can be measured (Handoff s.7 item 7).
3. **Simple rule as fallback.** The segment rule captures 50.3% of lost revenue in the top 20% vs 53.8% for the model (measured, Handoff s.4). The difference is not proven. Launch with the rule if engineering is slow.
4. **From prediction to uplift.** Keep a random 10% to 20% untouched holdout in every campaign (assumed). After Pilot 1, fit an uplift model (one that predicts the change an offer causes) on treated vs holdout. Target persuadables. Avoid "sleeping dogs" (stayers an offer prompts to leave).
5. **Instrumentation to add**, in priority order:
   - Event dates: sign-up, contract change, cancellation request, churn (Handoff s.7 item 2).
   - Fiber quality: install date, missed installs, outages, speed tests, fault tickets.
   - First-bill data: bill amount vs quoted price, billing calls in month one.
   - Price history: list price, discounts, promo end dates (Handoff s.7 item 5).
   - Offer log: assignment, take-up, credit paid.
6. **Drift guardrails.** Recheck calibration monthly. Alert if the calibration gap passes 0.05 or top-20% capture falls below 45% (assumed thresholds). Confirm whether tenure is recorded at exit (Handoff s.7 item 3).
7. **Fairness guardrail.** Senior share of contacted customers must stay within 5 points of their share of the eligible group (assumed). No price or credit decisions from the score (Handoff s.7).

### Track B: Commercial, pricing and finance levers (no model needed)

**Change the sales default and the first 90 days now. These need no model.**

1. **Make commitment the default for new fiber sales.** Sell a one-year price lock as the standard offer, with a cancellation fee no higher than the lock's value. This mirrors Comcast's and Verizon's locks (external). One-year fiber customers churn 19% vs 55% month-to-month (measured, chart 03). Selection explains part of that gap.
2. **Fiber first-90-days programme.** Confirm install quality in week one. Call before the first bill to explain it. Give a free 3-month tech support trial. Frontier links lower churn to installation and first-bill focus (external).
3. **Autopay incentive, aimed at tenured customers.** Offer a small autopay credit to electronic-check payers past month 12. Make autopay the sign-up default. Do not bundle it with paperless billing, given the unexplained paperless signal (Handoff s.5).
4. **Fiber price-for-value review.** Finance should compare fiber price per Mbps with local offers. Bills here run above market references (section 2). Use list-price history to test this.
5. **Sales compensation.** Pay a share of acquisition commission only after the customer passes month 3 (assumed design). This rewards durable sales, not churn-prone ones.
6. **Retention-desk compliance.** Review save-offer scripts against California's amended renewal law (external). Prefer proactive offers before a cancellation request.

---

## 5. 90-day growth lab: four pilots

Sample sizes use a two-sided 5% test with 80% power. With 7,043 customers, some pilots can only detect large effects. On the client's real base, rerun the sizing.

### Pilot 1: Commitment offer with uplift holdout

- **Playbook.** Uplift holdout test.
- **Internal trigger.** Contract is the strongest controllable lever (modeled -18.0 points, chart 08). Month-to-month customers scored 0.3 or higher: 2,548, churn 55.3%, mean bill $76.41 (measured, derived from R2-Q3).
- **External trigger.** Uplift-based targeting cut churn 4.1 to 8.7 points (external, Ascarza). Price locks are now the market norm (external).
- **Hypothesis.** If we offer a one-year price lock with a $5 monthly credit to month-to-month customers scored 0.3 or higher, twelve-week churn will fall 4 to 9 points. Customers who commit lose the easy exit, and the credit signals value.
- **Design.** Randomise 2,548 customers 50/50 within score bands (0.3-0.5, 0.5-0.7, 0.7+). About 1,274 per arm detects a 5.5-point drop from 55% (assumed calculation). Each band alone detects only about 9 points or more. Run 90 days, follow for 6 months.
- **Execution.** Data builds the randomisation, list and holdout. Marketing writes the offer. Retention agents deliver it. Finance sets the credit.
- **North star.** Churn rate in treatment minus holdout, by score band.
- **Guardrails.** Credit cost per saved customer under $250 (assumed). Complaints flat. Senior share within 5 points.
- **Decisions.** Day 30: kill if take-up is below 5%. Day 60: pivot band targeting if any band shows higher churn under treatment. Day 90: scale if the gap is 4 points or more and saved-customer margin exceeds credit cost.

### Pilot 2: Fiber first-90-days concierge

- **Playbook.** Onboarding activation trigger.
- **Internal trigger.** Month-to-month fiber churn is 80.5% in months 0-2 and 66.2% in months 3-6 (measured, R2-Q2). Chart 02 shows the steepest drop after month 6.
- **External trigger.** Frontier ties lower fiber churn to installation and first-bill focus (external). Users complain about installs, support and speeds (external, BGR).
- **Hypothesis.** If new fiber customers get an install check, a pre-bill call and a 3-month tech support trial, 90-day churn will fall 5 to 10 points (assumed). Early problems are fixed before they become exits.
- **Design.** Randomise every new fiber sign-up 50/50. About 115 per month (assumed) gives about 345 per arm over 90 days. That detects only a 10-point drop from 80% (assumed calculation). Use leading metrics at day 90 and churn at month 6.
- **Execution.** Data flags new sign-ups daily. Field operations run install checks. Care runs pre-bill calls. Product enables the trial.
- **North star.** 90-day survival of new fiber customers.
- **Guardrails.** Cost per new customer under $40 (assumed). Tech-support trial conversion to paid at least 20% (assumed).
- **Decisions.** Day 30: fix delivery if under 70% of calls connect. Day 60: continue if first-month billing calls fall. Day 90: scale if 90-day churn falls 5 points or more; kill if under 2.

### Pilot 3: Autopay switch for tenured electronic-check payers

- **Playbook.** Payment-method split test.
- **Internal trigger.** Past month 12, electronic-check payers on month-to-month fiber leave at 50.3% vs 33.6% for autopay (measured, derived). In months 0-12 there is no gap (measured, R2-Q1). Modeled change is -6.1 points (modeled, Handoff s.5).
- **External trigger.** Comcast prices non-autopay $10 higher per month (external). Autopay friction may raise churn (external, AT&T commentary, not proven).
- **Hypothesis.** If tenured electronic-check payers get a $5 monthly credit to switch to autopay, 30% will enrol and their churn will fall 5 to 8 points (assumed). Autopay removes the monthly pay-or-leave decision.
- **Design.** 676 customers, 338 per arm (measured base). Enrolment is the primary 30-day metric. Churn can only show an 11-point effect at this size (assumed calculation).
- **Execution.** Billing adds the credit. Marketing sends email and SMS. Finance books the cost.
- **North star.** Autopay enrolment rate. Secondary: 90-day churn.
- **Guardrails.** Failed-payment rate under 2% (assumed). Opt-out rate flat.
- **Decisions.** Day 30: kill if enrolment is under 10%. Day 90: scale if enrolment is 25% or more and churn does not rise.

### Pilot 4: Tech support trial for month-to-month fiber

- **Playbook.** Packaging split test.
- **Internal trigger.** Month-to-month fiber: 57.5% churn without tech support vs 38.9% with (measured, R1-Q3). Of the top 1,060 contract-lever customers, 87.2% lack tech support (measured, R1-Q4).
- **External trigger.** Users cite weak support and installs at the top fiber provider (external, BGR).
- **Hypothesis.** If month-to-month fiber customers without support get 3 free months, churn will fall 3 to 6 points (assumed). Faster fixes lower the urge to switch.
- **Design.** Randomise 1,796 customers 50/50 (measured base). About 898 per arm detects about 7 points from 57% (assumed calculation). Run 90 days.
- **Execution.** Product enables the trial. Support staffs the extra load. Finance tracks paid conversion.
- **North star.** 90-day churn, treatment minus control.
- **Guardrails.** Support wait time up no more than 10% (assumed). Paid conversion at least 20% after trial (assumed).
- **Decisions.** Day 30: pause if wait times breach the guardrail. Day 90: scale if churn falls 4 points or more; kill if under 1.

---

## 6. Prioritisation

**Start with the free commercial fixes. Then run Pilots 1 and 2. Build the data foundation in parallel.**

| Initiative | Financial impact (P&L driver) | Confidence | Ease / time to value | Wave |
|---|---|---|---|---|
| Commitment price lock as default for new fiber sales | High (retention, revenue) | Medium: strong link, selection risk; market precedent | 4-6 weeks; sales and pricing | 1 |
| Retention-desk compliance and offer log | Low direct; enables all returns | High | 2-4 weeks; legal and care | 1 |
| Fairness and senior-share guardrail | Risk avoidance | High | 2 weeks | 1 |
| Pilot 2: fiber first-90-days concierge | High (retention, cohort value) | Medium: strong tenure cliff; external support | 6-8 weeks; field ops and care | 2 |
| Pilot 1: commitment offer with uplift holdout | Med-High (retention) | Medium: modeled effect, external uplift evidence | 4-6 weeks; data and care | 2 |
| Pilot 4: tech support trial | Medium (retention, add-on revenue) | Low-Medium: self-selection | 4 weeks; product and support | 2 |
| Pilot 3: autopay for tenured e-check payers | Low (retention, working capital) | Medium: gap holds past year one | 3 weeks; billing | 2 |
| Weekly score in the customer system, with holdout | Medium (efficiency) | Medium: model beats rules not proven | 6-10 weeks; data engineering | 2 |
| Event, quality and price telemetry | Enabler for everything | High | 3-6 months | 3 |
| Fiber price-for-value review | Potentially High (revenue, margin) | Low: price and product cannot be separated | 3 months; finance | 3 |
| Home and mobile bundle | High if feasible (retention) | Low: no mobile data here; external only | 6-12 months | 3 |

### Open questions

- Is the observation window a quarter or a year? It changes the benchmark gap sevenfold.
- Is tenure recorded at exit (Handoff s.7 item 3)? If so, the 0-2 month cliff partly reflects timing.
- Gross margin, offer cost, save rate and acquisition cost are not in the data. All profit figures above are assumed.

---

## 7. Verified web sources

Pages fetched and read:
- https://lightwaveonline.com/home/article/55326989/frontiers-ongoing-fiber-expansion-raises-customer-retention : Frontier Q3 2025 consumer fiber churn 1.41% per month (from 1.49%), revenue per user $68.59, retention credited to installation and first-bill focus.
- https://bgr.com/2146659/internet-provider-ranks-highest-customer-satisfaction-at-t/ : 2025 ACSI fiber average 75 vs non-fiber 70; AT&T Fiber 78; user complaints on installs, support, speeds.
- https://lightwaveonline.com/broadband/article/55088085/acsi-data-shows-customers-prefer-fiber : 2024 ACSI, AT&T Fiber 80, Verizon Fios 77; fiber leads on reliability and speed.
- https://www.engadget.com/big-tech/comcast-rolls-out-a-five-year-price-guarantee-for-new-internet-customers-173421830.html : Comcast five-year price guarantee, $55 to $105, no annual contract, $10 more without autopay and paperless.
- https://www.lightwaveonline.com/broadband/article/55284110/long-term-price-locks-signal-an-evolving-competitive-landscape : Verizon three-year price lock for new and existing customers; Comcast's lock the longest in market.
- https://thedesk.net/2026/07/parks-broadband-churn-tracker-q1-2026/ : Comcast, Charter, Optimum 280,000 broadband disconnects Q1 2026; over a quarter of households take a broadband-wireless bundle.
- https://broadbandbreakfast.com/charter-reports-177-000-broadband-sub-loss-in-q4.md : Charter lost 177,000 broadband subscribers Q4 2024; churn "much lower" for home-plus-mobile customers.
- https://ama.org/press-releases/eva-ascarza-receives-2023-weitz-winer-odell-award-for-retention-futility : Ascarza (2018) field studies; targeting by responsiveness cut churn about 4.1 to 8.7 points; risk-targeting sometimes raised churn.
- https://www.androidheadlines.com/2025/10/att-faces-customer-retention-problem-despite-strong-subscriber-growth.html : AT&T churn up 14 basis points year on year, Q3 2025; author links it to reduced autopay discounts (not proven).
- https://www.jdsupra.com/legalnews/ftc-click-to-cancel-rule-on-hold-but-2056488 : FTC click-to-cancel rule on hold; California amended renewal law effective 1 July 2025 covers cancellation mechanisms.
- https://www.bain.com/insights/telco-fiber-networks-if-you-build-it-will-they-come/ : Fiber returns need about 35% uptake; one US provider raised gross adds 15% with targeted campaigns.

Searched but not fetched (403 or timeout), not used for figures: S&P Global Kagan churn report, Frontier Q3 2025 release on Nasdaq, Businesswire ACSI 2024 release, Benzinga and Mobile World Live AT&T results, Telenor uplift article, Stochastic Solutions PDF (unreadable).

---

## 8. Glossary

- **Annualised churn:** a monthly churn rate converted to a yearly one, 1 - (1 - monthly)^12.
- **AUC:** chance the model scores a random leaver above a random stayer; 0.5 is a coin flip.
- **Autopay:** automatic bank or card payment each month.
- **Break-even save rate:** share of flagged leavers who must be kept for a campaign to cover its cost.
- **Calibration:** whether customers scored 40% actually leave about 40% of the time.
- **Churn:** a customer leaving in the observation window.
- **Cohort survival:** share of customers who signed up together and are still customers later.
- **Commitment offer / price lock:** a promise of a fixed price for a set term in return for staying.
- **Confidence interval (95% interval):** range likely to contain the true value.
- **Controllable lever:** a column the business can change quickly, such as contract or payment method.
- **CRM:** the customer system that holds account records.
- **False negative:** a leaver the model did not flag.
- **False positive:** a stayer the model flagged.
- **Flywheel:** a loop where input metrics drive an output that feeds back into the inputs.
- **Gross margin:** revenue minus direct cost of service, as a share of revenue.
- **Guardrail metric:** a metric that must not get worse during a test.
- **Holdout:** a random group that gets no treatment, used as the comparison.
- **Lost revenue:** monthly bills of customers who left.
- **Minimum detectable effect:** the smallest change a test of a given size can reliably detect.
- **Month-to-month:** a plan with no fixed term.
- **North star metric:** the single outcome a pilot is judged on.
- **Permutation importance:** AUC lost when one column is shuffled.
- **Persuadable:** a customer who would leave without an offer but stays with one.
- **Power (80%):** the chance a test detects a real effect of the planned size.
- **Precision / recall:** share of flagged who leave / share of all leavers who are flagged.
- **Revenue per user (ARPU):** average monthly revenue per customer.
- **Save rate:** share of targeted would-be leavers who are kept by an offer.
- **Selection bias:** a gap caused by who chose an option, not by the option itself.
- **SHAP:** a method that splits each prediction into per-column contributions.
- **Sleeping dog:** a customer who would have stayed but leaves because of an offer.
- **Structural trait:** a column the business cannot change, such as tenure or age.
- **Threshold (cutoff):** the score above which a customer is contacted.
- **Top-20% capture:** share of lost revenue held by the 20% of customers scored riskiest.
- **Uplift model:** a model that predicts how much an offer changes a customer's chance of leaving.
- **Value at risk:** predicted churn probability times monthly bill, summed.
