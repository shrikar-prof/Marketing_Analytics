# Strategy Teardowns: Netflix Pricing and Five Below Store Expansion

Final report. Date: 17 November 2026. Prepared for Shrikar (shrikar.p@triiqinnovations.com).

**How to read this report.** Part A gives the answer in plain language. Part B shows how the work got there, stage by stage. Part C lists the checks and the limits. Part D is the glossary, chart list, sources and file list.

**Evidence labels.** Every number carries one of four labels.

| Label | Meaning |
|---|---|
| measured | Read directly from the SEC filings, or simple arithmetic on them |
| modeled | Estimated by a fitted statistical model. It shows two things move together, not that one causes the other |
| external | From a cited web page or filing outside the project data. URL in Part D |
| assumed | A number someone chose as an input. You can change it |

**Source keys used in citations.**

| Key | File |
|---|---|
| problem | `problem_description.md` |
| findings | `reports/exploration/findings.md` |
| dictionary | `reports/exploration/data_dictionary.md` |
| hypotheses | `reports/exploration/hypotheses.md` |
| audit | `reports/exploration/quality_audit.md` |
| cleaning | `reports/exploration/cleaning_log.md` |
| handoff-to-modeling | `reports/exploration/handoff_to_modeling.md` |
| model card | `reports/modeling/model_card.md` |
| tuning | `reports/modeling/tuning.md` |
| handoff | `reports/ml_handoff_report.md` |
| followups | `reports/ml_followups.md` (R1 = round 1, R2 = round 2) |
| memo | `reports/executive_growth_strategy.md` |
| dialogue | `reports/agent_dialogue.md` |
| review | `reports/notebook_review.md` |

**Corrections applied.** The statistician found errors in the handoff report. This report uses the corrected values from followups and the memo. The wrong values appear only in Part C, where each one is listed.

---

# Part A. The answer in plain language

## The questions, as the client asked them

1. **Netflix:** what did the US price increases do to memberships, revenue per member and revenue? (US and Canada, Q4 2019 to Q4 2024.)
2. **Five Below:** does the store expansion pace make sense? Are new stores as productive as the base? What did the fast-opening years do to comparable sales and operating margin? (Fiscal 2018 to fiscal 2025.)

Source: problem, "Questions to answer".

## The answer

Netflix raised prices six times and kept its customers. US and Canada revenue doubled. But since 2023 most new revenue came from adding paying households, mainly through the crackdown on password sharing. Price rises do seem to cost some members, though the signal is borderline. Five Below's weak years followed its two biggest opening years by store count. The link holds for the number of stores opened, not for the percent growth of the fleet. New stores stayed productive: sales per store dipped only 2%. Around 150 openings a year, as management now plans, fits the evidence. Every result rests on 8 to 24 data points, so each is a lead to test, not proof.

## The five numbers that matter

| # | Number | What it means for the decision | Label | Source |
|---|---|---|---|---|
| 1 | US and Canada quarterly revenue rose from $2,672M (Q4 2019) to $5,339M (Q4 2025), +100% | Price rises did not shrink revenue. No price step was followed by a revenue fall | measured | handoff §1; chart 01 |
| 2 | Member growth supplied 72% (2023) and 68% (2024) of yearly revenue growth. In 2022, price supplied it all (members −0.7%) | Recent growth came from more paying households, not higher prices. Protect member growth before the next price step | measured (descriptive arithmetic) | followups R2 Q2 |
| 3 | Higher price-per-member growth went with weaker next-quarter member additions: rho [rank correlation] = −0.474, p = 0.064, 16 quarters | Price has a cost. The result is borderline, so it is a warning that needs a proper test | measured | followups R1 Q4 |
| 4 | Each +$1 a month of price per member is worth about $1.08B a year on 89.63M members. It breaks even if about 4.9M members (5.5%) leave. The worst single quarter lost 1.3M | Past price steps had a wide safety margin. The margin shrinks if cheaper ad-plan sign-ups pull the average price down | measured arithmetic; flat membership is assumed | followups R1 Q1; memo N3 |
| 5 | Five Below's operating margin fell as yearly store openings rose: rho = −0.82, p = 0.033, 6 normal years. By percent fleet growth there is no such link (rho = +0.50) | The limit is how many stores teams can open well each year. Cap openings by count, near 150 | measured | followups R1 Q5; memo F2 |

## What should happen next

| # | Action | Company | Why | Source |
|---|---|---|---|---|
| 1 | Run a billing-cycle price test: delay the March 2026 increase for a random 5% of members for 60 days and compare cancellations | Netflix | Turns the borderline price signal (number 3) into a measured answer | memo N4, NF-1 |
| 2 | Offer the $8.99 ad plan to people at the cancel screen, with a random no-offer group | Netflix | Keeping a member at $8.99 beats losing a $19.99 member | memo N4, NF-2 |
| 3 | Keep at least 12 months between price steps | Netflix | The negative link in number 3 argues against tighter spacing | memo N3, Track B |
| 4 | Hold FY2026 at about 150 new stores. Raise the count by about 25 only when the last class of new stores reaches $2.0M first-year sales | Five Below | Margin tracked opening count, and management already guides about 150 | memo F3 |
| 5 | Test an opening-cadence cap (two openings per district manager per quarter) in matched regions | Five Below | Checks whether pace itself, rather than merchandise changes, drives results | memo F4, FB-1 |

## What is uncertain

- Every effect is an association from 6 to 24 data points. None is proven cause.
- Netflix stopped reporting members after Q4 2024, so 2025 members and price per member cannot be checked.
- Five Below's FY2025 rebound coincides with a pricing and merchandise reset, which the data cannot separate from slower openings.

---

# Part B. How we got there

## B1. The data: 33 rows of public filings, checked and kept whole

**What it is.** Two small tables built from public SEC filings (problem; handoff §2).

| Item | Netflix US and Canada | Five Below |
|---|---|---|
| Source | 8-K shareholder letters, Exhibit 99.1 | 10-K annual reports, plus XBRL [machine-readable tagged financial data] company facts |
| Grain | One row per quarter | One row per fiscal year |
| Period | Q4 2019 to Q4 2025 | FY2018 to FY2025 |
| Rows | 25 in the cleaning log; 24 per handoff-to-modeling (see Part C) | 8 |
| Rows with members | 20 quarters with membership data, through Q4 2024 (model card) | n/a |
| Key columns | Revenue, paid members, net additions, ARM [average revenue per member per month] | Stores, net new stores, comparable sales, revenue, operating income, SG&A [selling, general and administrative costs], capex [capital spending] |

All data is public domain. Sources: dictionary; cleaning; handoff §2.

**How it was checked.** The explorer logged six quality issues (audit). None blocked the analysis.

| Issue | Rows | What was done |
|---|---|---|
| Netflix members missing for 2025 (Netflix stopped reporting) | 4 | Kept; 2025 used for revenue only |
| Members × ARM × 3 differs from reported revenue by up to ~8% | 0 | No change; reported revenue used |
| Five Below FY2020 comps distorted by COVID store closures | 1 | Kept; FY2020 and FY2021 flagged as COVID years |
| FY2023 was a 53-week year | 1 | Kept; noted |
| Cost of goods missing FY2018 to FY2022 (different XBRL tag) | 5 | Gross margin computed only where available |
| FY2021 net new stores off by one versus store count | 1 | Stated figures used |

**How it was cleaned.** No rows were dropped (cleaning). Five new columns were added: operating margin, revenue per store, yearly revenue growth, a COVID flag, and Netflix year-on-year growth.

**What was excluded and why** (handoff-to-modeling).

| Excluded | Reason |
|---|---|
| Quarter label, fiscal-year-end date | Date keys, not inputs |
| Has-members flag | A filter, not a predictor |
| Five Below note text | Replaced by the COVID flag |
| Using ARM and members together to predict revenue | Revenue is roughly ARM × members × 3, so this would leak the answer [leakage] |

The cost-of-goods field later proved inconsistent from FY2023 onward (followups R2 Q1). Gross margin after FY2022 is not comparable with earlier years.

## B2. What exploration found: five findings, two of them since corrected

Each finding is shown with its corrected number where the statistician changed it. Reliability verdicts come from hypotheses and followups.

| # | Finding | Number | Label | Reliability | Chart |
|---|---|---|---|---|---|
| 1 | Price per member rose steadily and price steps stuck | ARM $13.22 → $17.26 a month (+31%); rho = 0.971, 95% CI 0.861 to 0.996 | measured | Reliable (hypotheses H1) | exploration 03; chart 01 |
| 2 | Paid-sharing enforcement lifted members; the revenue lift is mostly time trend | Members +2.23M per quarter (CI +0.36M to +4.10M, p = 0.022). Revenue +$92M per quarter after removing the trend (CI −$46M to +$231M, p = 0.17) | modeled | Members: firm but small sample. Revenue: not significant | exploration 02, 04 |
| 3 | Higher price growth went with weaker next-quarter member additions | rho = −0.474, p = 0.064, 95% CI −0.810 to 0.033, N = 16 | measured | Borderline; interval crosses zero | chart 05 |
| 4 | Five Below margin fell in the biggest opening years, by count not by rate | Margin vs openings rho = −0.820 (p = 0.033). Comps vs openings rho = −0.577 (p = 0.142). Margin vs rate rho = +0.50 | measured | Margin link: supported in direction on 6 points. Comps: too little data | charts 02, 03 |
| 5 | Sales per store dipped only slightly and stayed above the company's $2M new-store model | FY2022 $2.30M; FY2023–24 average $2.25M (−2%); FY2024 $2.19M; FY2025 $2.48M | measured; $2M model is external (10-K) | Descriptive only; 2 comparison years | chart 04 |

Sources: findings §1–5; hypotheses H1–H6; followups R1 Q1, Q3–Q5, Q7, Q9, R2 Q3.

**Important corrections to the explorer's text.** FY2023 comparable sales were +2.8%, not −2.0%. Only FY2024 of the two peak years was negative. The FY2022 sales-per-store figure is $2.30M, not $2.60M. Chart 01's title says revenue "quadrupled"; it doubled. Details in Part C.

**What exploration could not find.** It could not tell bad new sites from normal new-store ramp-up. Store-level profit is not public (findings, "What we did not find").

## B3. How the models were built: simple models, because the data is tiny

**What was compared.** Four small model families, each a Ridge regression [a straight-line model with a penalty that shrinks its weights to avoid overfitting]. Source: model card; tuning.

| Target | Models compared | Selected | Test method | Error of selected | Naive baseline error | Label |
|---|---|---|---|---|---|---|
| Netflix quarterly revenue | 6 | Last quarter's ARM + last quarter's revenue | Walk-forward [train on past quarters, predict the next, repeat], 12 predictions | MAE [average miss] $92.7M per quarter, R² 0.908 | $99.5M | modeled |
| Netflix paid members | 4 | Last quarter's members + paid-sharing flag | Walk-forward | 1.19M members, R² 0.893 | 1.40M (last-quarter-only model) | modeled |
| Five Below comparable sales | 4 | Expansion rate only | Leave-one-out [hold out one year, train on the rest] | 11.07 percentage points, R² −0.39 | 13.07 points | modeled |
| Five Below operating margin | 4 | SG&A share of revenue only | Leave-one-out | 1.79 points, R² −0.46 | 2.17 points | modeled |

**Tuning, in plain words.** No Optuna [an automated search tool for model settings] was used. With 8 to 24 rows, a large search would fit noise. The only setting tuned was the penalty strength, alpha, over five values: 0.01, 0.1, 1, 10 and 100. There were no tuning trials and no parameter-importance chart. Source: tuning, "Approach (no Optuna)".

**Why the chosen models won.** The rule was set before results: lowest error, at most two features for Five Below, at most four for Netflix, signs that make economic sense, and the simpler model on near-ties (tuning, "Model selection rule").

**How good they are on held-out data.**

| Model | Result | What it means |
|---|---|---|
| Netflix revenue | Walk-forward MAE $92.7M, inside the $100M target set before modeling | Good at tracking the trend one quarter ahead |
| Netflix revenue, held-out Q1 2025 | Predicted $4,705M vs actual $4,617M; residual −$88M | One test point only. The model over-predicted (the handoff text says "underpredicted"; see Part C) |
| Five Below comps | 11.07 points, far above the 1.5-point target | Not usable for forecasts. It cannot predict the COVID swings |
| Five Below margin | 1.79 points, close to the 1.5-point target | Weak but better than guessing the average |

Sources: model card "How good it is"; handoff §4; `reports/modeling/scores.csv`.

**Where the models are weaker.**
- The Netflix revenue model is a momentum model. Last quarter's revenue carries it (weight 1.23, p < 0.001). The ARM weight is −72, p = 0.18, because ARM and revenue move together [collinearity]. It cannot price a price change (memo N2; coefficient table).
- Both Five Below models have negative R² [worse than predicting the average]. Their single weights are not significant (p = 0.96 and 0.97).
- The Five Below comp model's weight on expansion rate is +7.87, not negative, and p = 0.96 (coefficient table). The model card's statement that higher expansion goes with lower comps is not supported by this weight.

## B4. What drives the predictions, and which drivers the business controls

| Driver | Company | Effect | Can the business change it? | Label | Source |
|---|---|---|---|---|---|
| Last quarter's revenue (momentum) | Netflix | Weight +1.23 per $1 of prior revenue, p < 0.001 | No; it is history | modeled | coefficient table |
| Paid-sharing enforcement | Netflix | +2.23M members per quarter, CI +0.36M to +4.10M | Yes; policy and add-on pricing | modeled | followups R2 Q3 |
| Price per member (ARM) | Netflix | Weight −72, not significant; captured through momentum | Yes; price level and plan mix | modeled | coefficient table |
| Price-step quarter | Netflix | Not significant once momentum is included | Yes; timing of steps | modeled | handoff §5 |
| Stores opened per year (count) | Five Below | Margin rho −0.820; comps rho −0.577 | Yes; opening plan | measured | followups R1 Q5 |
| SG&A share of revenue | Five Below | Weight −2.16, p = 0.97 | Partly; cost structure | modeled | coefficient table |
| COVID | Five Below | Dominates FY2020–21 errors | No | measured | handoff §5 |

**Sensitivities ("what if" arithmetic).** These come from the identity revenue ≈ price per member × members × months. They are not model forecasts.

| What if | Result | Label | Source |
|---|---|---|---|
| Netflix adds $1 a month to price per member, members hold at 89.63M | About +$1,076M a year (about $1,050M on the 87.2M average implied by Q4 2024 revenue) | measured arithmetic; members holding is assumed | followups R1 Q1 |
| Same $1 step, how many members can leave before revenue falls | About 4.9M (5.5%) | measured arithmetic | followups R1 Q1 |
| Netflix March 2026 Standard step (+11.1%) | Break-even if Standard members fall less than about 10% | external price; arithmetic | memo N3 |
| Each 1M Netflix members at $17.26 | About $207M a year | measured arithmetic | memo N1 |
| Each 1M members who move from Standard to the ad plan | About −$132M a year in fees unless ads fill the $11 a month gap | external prices; arithmetic | memo N1 |
| Five Below FY2024 margin at FY2023's level | About $96M more operating income on $3,877M revenue | measured arithmetic | memo F1 |
| Five Below opens 50 fewer stores a year | About $100M of sales and $10M of operating income deferred | assumed | memo F1 |
| One percentage point of Five Below comparable sales | About $44M of sales (on an assumed ~$4.4B base) | assumed | memo F1 |

## B5. Value at risk: the corrected scenario tables

The handoff's scenario tables used wrong inputs (83M members; FY2023 comps −2.0%). The corrected rows are below.

**Netflix: price step against member loss.**

| Scenario | Figure | Label | Source |
|---|---|---|---|
| Members at Q4 2024 | 89.63M | measured | followups R1 Q1 |
| Value of +$1 a month, members flat | About +$1.08B a year | measured arithmetic; assumed flat members | followups R1 Q1 |
| Member loss that cancels the +$1 | About 4.9M (5.5%) | measured arithmetic | followups R1 Q1 |
| Worst observed single-quarter loss | −1.3M (Q2 2022), reversed within two quarters | measured | handoff §6; exploration chart 04 |
| Members gained Q1 2023 to Q4 2024 | +15.23M (74.40M → 89.63M) | measured | followups R2 Q3 |

**Five Below: opening pace against results** (memo F2; followups R1 Q6–Q7).

| Year | Net new stores | Expansion rate | Comparable sales | Operating margin | Label |
|---|---|---|---|---|---|
| FY2023 | 204 | 15.2% | +2.8% | 10.8% | measured |
| FY2024 | 227 | 14.7% | −2.7% | 8.4% | measured |
| FY2025 | 150 | 8.5% | +12.8% | 9.6% | measured |

**Netflix model error by revenue level** (handoff §6, top rows). The handoff calls this the "decile view"; it is in quartiles. Values come from in-sample fits, not true out-of-sample predictions (followups R1 Q8).

| Revenue quartile | Period | Average actual ($M per quarter) | Average predicted ($M) | Average miss ($M) |
|---|---|---|---|---|
| Lowest | Q4'19–Q2'21 | 2,980 | 2,982 | 42 |
| Second | Q3'21–Q4'22 | 3,420 | 3,448 | 52 |
| Third | Q1'23–Q3'24 | 3,836 | 3,780 | 80 |
| Highest | Q4'24–Q1'25 | 4,567 | 4,593 | 103 |

Error grows with revenue level. Label: modeled.

**Smallest intervention.** The handoff names no smallest intervention. The memo's decision rules play that role. For Netflix: a price step is safe while expected member loss stays under x/(1+x) of the base, where x is the percent price rise. For Five Below: hold at 150 openings and add about 25 only when the previous class tracks at $2.0M first-year sales and nearby comps stay within 1 point of the chain (assumed thresholds; memo F3).

## B6. The strategy: fund each price step with member growth, and earn each extra store

### Internal metrics against external benchmarks

| Metric | Internal | Benchmark | Read-across | Label | Source |
|---|---|---|---|---|---|
| Netflix revenue growth 2025 | US and Canada +15.0% ($19,957M vs $17,359M) | Netflix global 2025 guide +16% | Keeps pace with the global business | measured; external | followups R1 Q2; TheWrap Q3 2025 |
| Netflix monthly churn [share cancelling each month] | ~2.1% | Disney+ ~5.5%, Max ~6–6.9%, Hulu ~5.3% | Under half the rival rate | external, unverified secondary source | Churnkey |
| Netflix ad revenue | >$1.5B in 2025, ~2.5× 2024 | Target ~$9B by 2030 | Ads ~3% of 2025 revenue | external | Q4 2025 letter; TheWrap upfront |
| Ad-plan share of new sign-ups | >60% (Q1 2026) | 2024: >40% | New members enter at the cheapest price | external | TheWrap upfront |
| Five Below comparable sales | FY2025 +12.8% | Ollie's Q3 FY2025 +3.3% | ~9 points ahead | measured; external | Ollie's 8-K |
| Fleet growth | 8.5% | Ollie's +18.1% (86 openings, 645 stores) | Ollie's grows faster in percent from far fewer stores | measured; external | Ollie's 8-K |
| Operating margin | FY2025 9.6% | Ollie's Q3 FY2025 9.0% (one quarter) | Not like-for-like | measured; external | Ollie's 8-K |
| Sales per store | $2.48M | Company new-store model $2M first year, $0.4M investment, ~1-year payback | Average store 24% above the model | measured; external (10-K) | memo F2 |
| FY2026 outlook | n/a | Sales $5.20–5.30B; comps +3–5%; ~150 net new; capex $230–250M | Management chose ~150 again | external | Five Below 8-K |

### The levers

| Company | Lever | Size | Label |
|---|---|---|---|
| Netflix | Price per member | +$1 a month ≈ $1.08B a year if members hold | measured arithmetic; assumed |
| Netflix | Paid member conversion | +15.23M members Q1'23 to Q4'24; 1M members ≈ $207M a year | measured |
| Netflix | Ad monetization | 1M Standard-to-ads moves ≈ −$132M a year in fees | external; arithmetic |
| Five Below | Cap openings near 150 | FY2024 margin dip ≈ $96M of operating income | measured arithmetic |
| Five Below | Keep the pricing and merchandise reset | FY2025 comps +12.8%; Q2 transactions +8.7% | external |
| Five Below | Bank capital efficiency | Capex fell $324.0M → $174.7M while revenue rose 22.9% | measured |

### Recommendations by track (memo N3, F3)

| Track | Netflix | Five Below |
|---|---|---|
| A. Capability | Household-level price-response model; separate cancel-risk and persuadability scoring [uplift model]; blended fees-plus-ads revenue per member; restore an internal member series | New-store class dashboard (month 1–24 vs model); cannibalization model [sales new stores take from nearby stores]; trade-area site scoring; opening-capacity planning |
| B. Quick wins | Ad plan as a save offer; push extra-member slots to borrowers; space price steps ≥12 months; pair each step with a content or live-event moment | Hold FY2026 at ~150; pay teams on year-2 store sales; protect whole-number pricing; route freed capex to remodels |

### Pilots, with design and decision rules (memo N4, F4)

| Pilot | Design | Size and run time | North Star [the one outcome judged] | Decision rule |
|---|---|---|---|---|
| NF-1 Billing-cycle price test | Random 5% of Standard members get the March 2026 rise 60 days late | ~77,000 per group needed to detect 0.2 points (assumed); 90 days | Net revenue per member over 90 days | Day 30: pause next wave if holdout cancels >0.5 points lower. Day 90: scale if treated revenue per member ≥8% higher |
| NF-2 Ad-plan save offer | Cancel-screen visitors split 50/50, offer vs no offer | ~1,600 per group for a 3-point lift from 10% (assumed); 8 weeks + 6-month follow-up | 6-month revenue per visitor | Day 30: save rate ≥+2 points. Kill if downgrades cost more than saves |
| NF-3 Extra-member slot price | Three groups: list price, 50% off first month, first month free | 60 days; 120-day retention | 120-day revenue per borrowing household | Kill any group below list-price revenue |
| FB-1 Opening cadence | Matched regions; half capped at two openings per district manager per quarter | ~75 stores per group; detects ~3.7 points (assumed); 12 months, 6-month read | First-12-month sales per new store vs $2.0M | Day 90: scale nationally if treated stores lead by ≥3%. Kill if they trail |
| FB-2 Infill holdout | ~40 infill sites, 20 open on time, 20 deferred two quarters | 6 months | New store plus sister-store sales | Raise infill hurdle if net gain < $1.5M a year (assumed) |
| FB-3 Above-$5 bay | 100 treated vs 100 matched stores | 12 weeks, avoid holidays | Gross margin dollars per store per week | Scale if +2%. Kill if transactions fall >2% |

### Prioritization (memo §7)

| Wave | Initiative | Company | Impact | Confidence | Time to value |
|---|---|---|---|---|---|
| 1 | Hold ~150 openings; pay on year-2 sales | Five Below | High | Medium | 2–4 weeks |
| 1 | Ad-plan save offer (NF-2) | Netflix | Medium | Medium | 4–6 weeks |
| 1 | Space price steps ≥12 months | Netflix | Medium | Low–medium | Immediate |
| 1 | Protect whole-number price reset | Five Below | High | Medium | Immediate |
| 2 | Billing-cycle price test (NF-1) | Netflix | High | High as a design | 6–8 weeks |
| 2 | Opening-cadence pilot (FB-1) | Five Below | High | Medium | 8–12 weeks |
| 2 | Extra-member slot test (NF-3) | Netflix | Medium | Medium | 6 weeks |
| 2 | Above-$5 bay test (FB-3) | Five Below | Medium | Medium | 6 weeks |
| 3 | Infill holdout (FB-2) | Five Below | Medium | Low–medium | 2 quarters |
| 3 | New-store dashboard and site scoring | Five Below | High over time | Medium | 3–6 months |
| 3 | Price-response and uplift models | Netflix | High over time | Medium | 6 months |

## B7. The agent dialogue: 12 questions in two rounds changed four headline claims

The strategy partner sent 12 questions to the statistician. None was declined. Nothing remains open (dialogue). Questions are as reported in `agent_dialogue.md`; answers are quoted from `ml_followups.md`.

### Round 1

**R1 Q1 (Netflix §1 levers, §2).** *Question:* "UCAN end-of-quarter paid memberships at Q4'24: chart exploration/02 shows ~89.6M, but handoff §6 uses 83M. Which is right? Please restate the $1/month ARM → annual revenue arithmetic at the correct base. Also explain the "~$360M/year per $1/month" in handoff §2 and actionability_netflix.csv; at 83M × $1 × 12 I get ~$1.0B, not $360M."
*Answer:* "Q4'24 UCAN paid members = 89.63M (clean table; chart 02 is right). 83M in the handoff was wrong. ARM is $ per member per month, so $1/month x 89.63M x 12 = $1,076M per year (about $1,050M on the 87.2M average members implied by Q4'24 revenue 4,517/3/17.26). The "$360M/year" was an arithmetic error in the handoff (it is not 83M x $1 x 12 = $996M, nor any other defensible figure). Break-even: a $1 rise at ARM 17.26 is offset by losing about 4.9M members (5.5%). Assumed: flat membership; modeled-free arithmetic, not a causal estimate."
*Memo sections:* Netflix §1 lever 1, §3 decision rule. *What changed:* members corrected to 89.63M; $1 a month ≈ $1.08B a year; break-even ≈ 4.9M.

**R1 Q2 (Netflix §1, §2).** *Question:* "Exact UCAN quarterly revenue for Q2'25, Q3'25, Q4'25, plus calendar-2025 total vs 2024 total and % growth."
*Answer:* "Revenue USD M: Q2'25 4,929; Q3'25 5,072; Q4'25 5,339. CY2025 = 19,957; CY2024 = 17,359; growth +14.97% (+2,598M)."
*Memo sections:* Netflix §2, benchmark table. *What changed:* 2025 revenue added.

**R1 Q3 (Netflix §2).** *Question:* "H2 paid-sharing lift: handoff says Hodges-Lehmann +$1,218M/qtr, findings.md says median +$1,060M. Which is correct? Please give the post_paid_sharing coefficient and SE from the fitted revenue model."
*Answer:* "Pre = Q4'19-Q1'23 (14 quarters, median 3,246.5M); post = Q2'23-Q4'25 (11 quarters, median 4,322M). Median difference = 1,075.5M (findings.md 1,060M does not reproduce). Hodges-Lehmann = 1,218M (reproduces; this is what hypotheses.md reports). Both mix in the time trend and include 2025. Trend-adjusted: OLS (Ridge alpha 0.01 is ~OLS) of revenue on arm_lag1, rev_lag1, post_paid_sharing, quarter dummies, fitted on 20 training quarters Q1'20-Q4'24: post_paid_sharing = +92.4M/qtr, SE 64.1, 95% CI [-46, +231], p = 0.17. Without quarter dummies: +86.9M, SE 59.8. The model does not support a $1.2B/qtr step. (Members model: post_paid_sharing +2.23M members, SE 0.89, p = 0.022, model_card.)"
*Memo sections:* Netflix thesis, §2, §5 pattern 2. *What changed:* thesis moved from "paid sharing added $1.2B a quarter" to "paid sharing worked through members".

**R1 Q4 (Netflix §2).** *Question:* "H6 sign conflict: handoff says rho = +0.19; hypotheses.md says rho = −0.474 (p = 0.064, CI −0.810 to 0.033). Which is correct?"
*Answer:* "rho = -0.474 (p = 0.064, bootstrap CI [-0.810, 0.033]) is correct; reproduced. Pair: ARM YoY growth in quarter t vs net adds in quarter t+1, quarters Q4'20-Q3'24, N = 16 (hypotheses.md says N=15; notebook prints 16). I could not reproduce +0.19 anywhere. Sign meaning: higher ARM growth goes with lower next-quarter net adds (borderline). Variants: QoQ ARM change vs next net adds rho -0.23 (N=19, p 0.35); same-quarter ARM YoY vs net adds rho -0.54 (N=17, p 0.026)."
*Memo sections:* Netflix §2, §3 Track B item 3, pilot NF-1, risk 5. *What changed:* price risk treated as real; trigger for NF-1.

**R1 Q5 (Five Below thesis, §2).** *Question:* "For H3/H4, is "expansion" measured as absolute net new stores or as a rate (net new / prior-year fleet)? Please give Spearman rho and permutation p for margin and comps vs rate on non-COVID years."
*Answer:* "Both H3 and H4 use ABSOLUTE net_new_stores, on six non-COVID years FY2018, 2019, 2022, 2023, 2024, 2025. Results: comps vs stores rho -0.577, exact p 0.1417 (102/720); margin vs stores rho -0.820, p 0.0333 (24/720). Rate (net new / prior fleet; FY2018 undefined so 5 years FY2019, 2022-25): comps vs rate rho -0.20, one-sided exact p 0.39 (47/120); margin vs rate rho +0.50, p 0.825. Your hand calculation is right: the negative link holds for store count, not for rate."
*Memo sections:* Five Below thesis, §1, §2, FB-1, §5 pattern 3. *What changed:* lever reframed from expansion rate to openings per year.

**R1 Q6 (Five Below §2, §4 sizing).** *Question:* "Full FY2018–FY2025 table: year-end stores, net new stores, total revenue ($M), operating income ($M), SG&A % of revenue, capex ($M)."
*Answer:* The eight-year table in followups R1 item 6 (reproduced in the memo F2 table and in the HTML version).
*Memo sections:* Five Below §2 table, capex lever, cost of going slower. *What changed:* the table now drives capex and deferral estimates.

**R1 Q7 (Five Below §2).** *Question:* "Comps check: chart shows FY2023 = +2.8% but handoff §1 says FY2023 = −2.0%. Please confirm FY2023 and FY2023 margin."
*Answer:* "Comps: FY2022 -2.0, FY2023 +2.8, FY2024 -2.7 (clean table). Handoff section 1 and findings.md wrongly put -2.0 on FY2023. Only FY2024 of the two peak-expansion years was negative. FY2023 margin = 10.83% (rounds to 10.8; 10.7 in findings is a slip)."
*Memo sections:* Five Below §2. *What changed:* FY2023 comps +2.8% and margin 10.83% confirmed.

**R1 Q8 (Model confidence, risk table).** *Question:* "customer_risk_scores.csv shows near-flat LOOCV predictions; chart 07 shows varying ones. Which is the selected model's out-of-sample result?"
*Answer:* "Neither file is the full story. scores.csv holds full-sample fitted values (in-sample MAE: comps 9.36, margin 1.51; Netflix 63.6M), flat because alpha = 100 shrinks the slope to ~0. The chart plots true leave-one-out predictions (leave-one-out mean reproduces its FY2021 value ~0.8-1.0; LOO MAE 10.9 and 1.7, matching the model card 11.07 and 1.79). Selected model is the same; the chart is the honest out-of-sample view. My customer_risk_scores.csv inherited the in-sample values but labels them "loocv" and "wf-CV OOF": that labelling is wrong. Only Netflix Q1'25 is a held-out score; Q2-Q4'25 were not scored."
*Memo sections:* §2 model rows, risk 2. *What changed:* memo uses chart 07 and the model card for out-of-sample accuracy.

**R1 Q9 (Five Below §2).** *Question:* "Is revenue per store calculated on year-end stores or average stores? Confirm FY2022 = $2.30M."
*Answer:* "Revenue per store = revenue / year-end stores (data dictionary). FY2022 = $2.2958M = $2.30M. $2.60M in findings.md is wrong. On average-fleet basis FY2022 = $2.43M. Note FY2022 to FY2023-24 average is -$0.05M (-2%) per hypotheses H5; "dilution" is small."
*Memo sections:* Five Below §2. *What changed:* FY2022 = $2.30M; peak-year dilution −2%.

### Round 2

**R2 Q1 (Five Below §2 margin bridge).** *Question:* "Gross margin % for FY2018–FY2025. Split the FY2023→FY2024 drop (10.83% to 8.35%) and FY2024→FY2025 recovery into gross-margin and SG&A-% components, in ppt."
*Answer (key lines):* "Identity check: gross margin - SG&A % = operating margin holds exactly for FY2018-FY2022 (residual 0.00 ppt) but NOT for FY2023-FY2025 (residual 3.67, 4.32, 4.03 ppt). So cogs_usd for FY2023+ appears to exclude a cost line that the earlier years include ... Status: OPEN, needs a check of the 10-K cost lines." "FY23->24 op margin -2.48 = gross margin -0.89, SG&A -0.94 (22.22 vs 21.28), unexplained other cost -0.65. FY24->25 +1.25 = gross margin +1.10, SG&A -0.14, other +0.29. The "other" line is the unreconciled residual; do not read it as a finding."
*Memo sections:* Five Below open question 1, risk 8. *What changed:* margin bridge marked provisional and open.

**R2 Q2 (Netflix §2 decomposition).** *Question:* "For calendar 2022, 2023 and 2024: share of UCAN YoY revenue growth from average-member growth vs ARM growth."
*Answer:* "2022: revenue +8.6%; members -0.7%, ARM +9.3%; share members -8%, ARM 108% [reported ARM +8.9%, 104%]. 2023: revenue +5.6%; members +4.0%, ARM +1.5%; share members 72%, ARM 28% [reported ARM +2.6%, 47%]. 2024: revenue +16.7%; members +11.0%, ARM +5.2%; share members 68%, ARM 33% [reported ARM +5.7%, 36%]. You are right: 2023 and 2024 were member-led; 2022 was ARM-led. Handoff section 8 / chart-05 wording was wrong. Descriptive arithmetic, not causal."
*Memo sections:* Netflix thesis, §1 opening, §5 pattern 1. *What changed:* became the headline thesis.

**R2 Q3 (Netflix §2).** *Question:* "95% CI for post_paid_sharing members coefficient (+2.23M, SE 0.89), and UCAN membership change from Q1'23 to Q4'24."
*Answer:* "post_paid_sharing in lag1+post_sharing members model: +2.23M, SE 0.89, 95% CI [+0.36M, +4.10M], p 0.022 (coefficient_table.csv; n=20, so fragile). Q1'23 74.40M to Q4'24 89.63M = +15.23M. Association, not a causal effect of enforcement."
*Memo sections:* Netflix §1 lever 2, §2, NF-3 trigger. *What changed:* interval confirmed; member gain +15.23M.

### Notebook review: 20 gaps found, 10 fixed, 10 remaining

| Notebook | Gaps found (pass 1) | Fixed | Remaining (pass 2) | Main remaining gaps |
|---|---|---|---|---|
| 01 exploration | 8 | 5 | 3 | Derived-column formulas only in code comments; no explanation directly before the hypothesis-test cell; data dictionary lacks hypothesis and expected-direction columns and has a column-name mismatch |
| 02 feature engineering and 03 modeling | 12 | 5 | 7 | Final chart cell (NB03 cell 30) unexplained; Netflix feature alternatives missing; held-out test result ($88.2M) never stated in text; comp-model result vs target not stated |

The review allowed one fix round per stage, so remaining gaps were passed on, not fixed (review).

---

# Part C. Checks and limits

## C1. Consistency check: numbers that appear in two or more reports

| Number | Values found | Verdict | Use |
|---|---|---|---|
| Netflix members at Q4 2024 | 83M (handoff §6) vs 89.63M (followups R1 Q1; exploration chart 02) | Discrepancy; handoff wrong | 89.63M |
| Revenue per +$1 a month | $360M (handoff §2; actionability_netflix.csv) vs ~$1.0B (handoff §6 table) vs $1,076M (followups) | Discrepancy; arithmetic error | ~$1.08B |
| Break-even member loss | 5.8M (handoff §6) vs 4.9M (followups) | Discrepancy | 4.9M |
| Price growth vs next-quarter member adds | rho +0.19 (findings F3; handoff F3; actionability CSV) vs −0.474 (hypotheses H6; followups) | Discrepancy; +0.19 not reproducible | −0.474, p = 0.064 |
| Sample size for that test | N = 15 (hypotheses) vs N = 16 (followups; notebook) | Minor discrepancy | 16 |
| Paid-sharing revenue lift | Median +$1,060M (findings) vs Hodges-Lehmann +$1,218M (handoff; hypotheses) vs median gap $1,075.5M vs trend-adjusted +$92M, p = 0.17 (followups) | Discrepancy; $1,060M not reproducible; pre/post gaps include trend | +$92M, not significant |
| Paid-sharing member lift | +2.23M, p = 0.022 (model card; handoff; followups; memo) | Agree | +2.23M |
| FY2023 comparable sales | −2.0% (findings F4; handoff §1, §3) vs +2.8% (chart 02; followups R1 Q7; handoff §6 table) | Discrepancy | +2.8% |
| FY2023 operating margin | 10.7% (findings) vs 10.8% (handoff) vs 10.83% (followups) | Rounding slip | 10.83% |
| Five Below FY2022 revenue per store | $2.60M (findings F5) vs $2.30M (chart 04; hypotheses H5; followups) | Discrepancy | $2.30M |
| "Peak" revenue per store in FY2022 | Chart 04 title says FY2022 peak; its own labels show FY2023 $2.31M, FY2021 $2.39M, FY2025 $2.48M | Chart title does not match its data | Use labels |
| Margin vs expansion link | Called "expansion rate" (handoff §5; actionability_five_below.csv) vs absolute store count (followups R1 Q5) | Discrepancy in definition | Count: rho −0.82. Rate: rho +0.50 |
| Peak-year expansion rate | "20%+" (handoff §1); "~20%" (actionability CSV); "~12%" for 200 stores (handoff §6) vs 15.2% and 14.7% (memo F2) | Discrepancy | 15.2%, 14.7% |
| Margin per 100 stores | 1.6 points (handoff §2) | Unsupported; withdrawn | Not used |
| What drove 2023–24 Netflix revenue | "ARM dominates post-2023" (handoff §8, chart 05 note) vs member-led 72% and 68% (followups R2 Q2) | Discrepancy | Member-led |
| Netflix revenue growth Q4'19 to Q4'25 | "Quadrupled" (chart 01 title) vs +100% (findings; handoff) | Chart title wrong | Doubled |
| Netflix walk-forward MAE | $92.7M (model card; tuning; handoff; memo) | Agree | $92.7M |
| Held-out Q1 2025 | Residual −$88.2M (scores.csv); handoff says "underpredicted by 1.9%"; review says MAE $88.2M | Size agrees; direction wording wrong (predicted $4,705M > actual $4,617M) | Over-predicted by $88M |
| ARM weight in revenue model | −72.26 (model card; coefficient table) vs −$68.6M (review) | Minor discrepancy | −72.26 |
| Netflix row count | 24 (handoff-to-modeling; handoff) vs 25 (cleaning log) | Minor discrepancy (Q4'19–Q4'25 is 25 quarters) | Not resolved |
| Q1 2024 residual cause | Handoff ties it to the Jan 2025 price announcement | Wrong time order (memo open question 4) | Not used |
| Model labels in `customer_risk_scores.csv` | Labelled "loocv" and "wf-CV OOF" | Mislabelled; values are in-sample fits (followups R1 Q8) | Use chart 07 and model card |
| Five Below comp model direction | Model card: higher expansion → lower comps. Coefficient +7.87, p = 0.96 | Text not supported by the weight | Direction unproven |

## C2. Strategy claims with no supporting number in the handoff report

| Memo claim | Basis given in memo |
|---|---|
| About 150 openings a year looks sustainable | Inference from count link plus external FY2026 guide |
| Cost of going slower ~$10M vs ~$96M for a stumble | Assumed; arithmetic |
| $44M per point of comparable sales | Assumed ~$4.4B comp base |
| $132M per 1M ad-plan moves; $207M per 1M members | External prices; arithmetic |
| Capex fell $149M | Followups R1 Q6, not the handoff |
| Netflix churn ~2.1% vs rivals 5–7% | External, secondary |
| Ad plan >60% of sign-ups | External |
| WWE retains ~1.25M subscribers a quarter | External, model-based |
| Tariff pressure ~150 bps | Search summary, not fetched |
| All pilot sample sizes and effect ranges | Assumed calculations |
| Bottleneck is real estate and opening teams | Inference; no data in project |

## C3. Benchmarks the memo marked unverified

| Benchmark | Status |
|---|---|
| Netflix ~2.1% monthly churn and rival rates | Third-party tables cite one another; primary source not reached |
| WWE retention ~1.25M per quarter | Analyst model estimate (Parrot Analytics via TheWrap) |
| Five Below tariff pressure ~150 bps | Search result only; page not fetched |
| Ollie's full-year operating margin | Not verified; one quarter used |
| Netflix 2025 US and Canada members and ARM | Not publicly reported |
| Base churn of ~2% used in NF-1 sizing | External, unverified |

## C4. Limitations and failure modes (merged from all reports)

| # | Limitation | Effect | Source |
|---|---|---|---|
| 1 | Tiny samples: 6 normal Five Below years, 16–24 Netflix quarters | Every result is direction only; p-values unreliable below ~15 rows | handoff §7; tuning |
| 2 | All effects are associations | Content, competition, macro, merchandising can drive both sides | model card; memo risk 1 |
| 3 | COVID years dominate Five Below errors | Comp model cannot forecast | handoff §7 |
| 4 | No Netflix members after Q4 2024 | Membership model cannot be tested on 2025 | audit; model card |
| 5 | Price per member and revenue move together | ARM effect cannot be isolated | model card |
| 6 | One held-out test quarter | No reliable out-of-sample confidence | handoff §7 |
| 7 | No store-level profit data | Cannot tell bad sites from ramp-up | findings |
| 8 | Cost-of-goods field changes in FY2023 | Margin bridge unreliable | followups R2 Q1 |
| 9 | Ad plan may dilute ARM faster than ad revenue grows | Price lever weakens | memo risk 3 |
| 10 | FY2025 comps surge may reverse (guide +3–5%) | Judging pace by chain comps misleads | memo risk 6 |
| 11 | Pre/post comparisons include time trend | Overstate effects ($1,218M vs $92M) | followups R1 Q3 |
| 12 | Scores file mislabelled | Readers may mistake in-sample fits for test results | followups R1 Q8 |

## C5. Instrumentation gaps, in priority order

| Priority | Gap | Fix | Source |
|---|---|---|---|
| 1 | No randomized price evidence | Billing-cycle holdout (NF-1) | handoff §7 item 2; memo |
| 2 | No member series after Q4 2024 | Internal member and household series | handoff §7 item 4 |
| 3 | No store-level sales and cost by opening class | New-store class dashboard | handoff §7 item 6 |
| 4 | Ad revenue per ad-plan member not disclosed | Blended fees-plus-ads metric | memo open question 3 |
| 5 | Inconsistent cost-of-goods tags | Rebuild from 10-K cost lines | followups R2 Q1 |
| 6 | No competitor or content-spend covariates | Add rival subscriber counts and content spend | handoff §7 item 7 |
| 7 | Single test quarter | Re-score quarterly as data arrives | handoff §7 item 8 |

---

# Part D. Appendix

## D1. Glossary

| Term | Plain meaning |
|---|---|
| ARM | Average revenue per member per month: revenue ÷ average members ÷ months |
| UCAN | Netflix's US and Canada reporting region |
| Paid sharing | Netflix's 2023 policy charging for accounts used outside the household |
| Extra-member slot | A paid add-on that lets an outside user join an account |
| Net additions (net adds) | Members gained minus members lost in a quarter |
| Churn | Share of subscribers who cancel in a period |
| Break-even member loss | Member loss at which a price rise leaves revenue unchanged: x/(1+x) |
| Elasticity | How much demand changes when price changes |
| Comparable sales (comps) | Sales growth in stores open at least 15 months |
| Expansion rate | Net new stores ÷ prior year-end stores |
| Operating margin | Operating income ÷ revenue |
| Gross margin | (Revenue − cost of goods) ÷ revenue |
| SG&A | Selling, general and administrative expenses |
| SG&A intensity | SG&A ÷ revenue |
| Capex | Cash spent on stores, distribution centers and systems |
| Payback period | Time for a store's profit to repay its investment |
| Cannibalization | Sales a new store takes from nearby stores |
| Infill | A new store inside an existing market |
| Shrink | Inventory lost to theft, damage or error |
| Ticket | Average spend per transaction |
| bps | Basis points; 100 bps = 1 percentage point |
| ppt / percentage point | The plain difference between two percentages |
| XBRL | Machine-readable tags on financial filings |
| 8-K / 10-K | SEC current-event report / SEC annual report |
| Leakage | When a model input already contains the answer |
| Ridge regression | Straight-line model with a penalty that shrinks weights to avoid overfitting |
| Alpha | The strength of the Ridge penalty |
| Overfitting | A model that memorizes noise and fails on new data |
| Optuna | An automated tool that searches model settings; not used here |
| Naive baseline | A simple guess (e.g. last value or average) a model must beat |
| MAE | Mean absolute error: the average size of a miss |
| R² | Share of variation a model explains; negative means worse than the average |
| Walk-forward validation | Train on past periods, predict the next, repeat |
| Leave-one-out validation (LOOCV) | Hold out one year, train on the rest, predict it; repeat for each year |
| OOF (out-of-fold) | A prediction for a row the model did not train on |
| In-sample fit | A prediction for a row the model trained on; flatters accuracy |
| Held-out test | Data kept aside and used once, at the end |
| Coefficient (weight) | How much a model's output moves per unit of an input |
| Collinearity | Two inputs moving together so a model cannot separate their effects |
| Momentum model | A model that mostly predicts from the previous value |
| Structural break | A point where the pattern in the data changes, e.g. a policy change |
| Spearman rho | Rank correlation from −1 to +1 |
| p-value | Chance of a result this extreme if there were no real link |
| 95% CI | Confidence interval: a range likely to contain the true value |
| Bootstrap | Re-sampling the data many times to estimate an interval |
| Exact permutation test | A significance test that checks every possible ordering of a small sample |
| Mann-Whitney test | A test of whether one group's values tend to be higher than another's |
| Hodges-Lehmann | A robust estimate of the median gap between two groups |
| OLS | Ordinary least squares: the standard straight-line fit |
| Uplift model | Estimates how much an action changes a person's behavior |
| Persuadable | A customer whose behavior an offer actually changes |
| Holdout | A random group that does not get a treatment, kept for comparison |
| Natural experiment | A real-world split that acts like random assignment |
| Minimum detectable effect | Smallest true effect a test can reliably detect |
| North Star metric | The one outcome a pilot is judged on |
| Guardrail metric | A metric that must not get worse during a pilot |
| Measured / modeled / external / assumed | The four evidence labels defined at the top |

## D2. Chart manifest

Duplicate files (same image in two folders) are listed once.

| File | What it shows | Key takeaway |
|---|---|---|
| `reports/charts/01_netflix_ucan_revenue.png` (= exploration 01) | Quarterly US and Canada revenue Q4'19–Q4'25 with price-event lines | Revenue doubled; title wrongly says "quadrupled" |
| `reports/exploration/charts/02_netflix_ucan_memberships.png` | Paid members Q4'19–Q4'24 | Flat 2021–22 near 73–75M, then up to 89.6M after paid sharing |
| `reports/exploration/charts/03_netflix_arm.png` | ARM by quarter with price events | $13.22 to $17.26; each step held |
| `reports/exploration/charts/04_netflix_net_adds.png` | Net member additions by quarter | Three loss quarters in 2021–22, worst −1.3M; strong gains from 2023 |
| `reports/charts/02_five_below_stores_vs_comp.png` (= exploration 05) | Net new stores (bars) and comps (line), two axes | FY2024 is the only negative peak year; FY2023 was +2.8% |
| `reports/charts/03_five_below_op_margin.png` (= exploration 06) | Operating margin FY2018–FY2025 | Low of 8.4% in FY2024, up to 9.6% in FY2025 |
| `reports/charts/04_five_below_rev_per_store.png` (= exploration 07) | Revenue per year-end store | Dip to $2.19M in FY2024; all years above $1.9M |
| `reports/charts/05_netflix_revenue_decomposition.png` (= exploration 08) | Member, ARM and revenue year-on-year growth | 2022 ARM-led; 2023–24 member-led (title wording overstated) |
| `reports/charts/06_netflix_revenue_model.png` (= modeling netflix_revenue_pred) | Actual vs walk-forward predicted revenue; 2025 actuals | Model tracks the trend; 2025 shown as actuals only |
| `reports/charts/07_five_below_model_fit.png` (= modeling fb_actual_vs_pred) | Leave-one-out actual vs predicted comps and margin | Comp model misses the swings; margin model tighter |
| `reports/modeling/charts/model_comparison.png` | Error of each candidate model vs baseline and target | Selected models are lowest; Five Below comps far above target |
| `reports/modeling/charts/netflix_arm_timeline.png` | ARM with labelled events | Same story as exploration 03 |
| `reports/modeling/charts/nf_feature_vs_revenue.png` | Each Netflix input against revenue | Prior revenue and ARM line up tightly with revenue |
| `reports/modeling/charts/fb_feature_vs_target.png` | Each Five Below input against comps and margin | No clear single-input pattern on 8 points |
| `reports/modeling/charts/fb_expansion_scatter.png` | Expansion rate vs comps and vs margin | No downward pattern by rate |

## D3. Web sources

| Source | One-line summary |
|---|---|
| [Five Below Q4 FY2025 release (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/1177609/000117760926000006/q42025fivebelowexhibit991.htm) | FY2025 sales $4.76B, comps +12.8%, 150 net new stores, FY2026 guide |
| [Motley Fool, Five Below Q2 FY2025](https://www.fool.com/data-news/2025/08/27/five-below-q2-sales-top-1-billion) | Comps +12.4%, transactions +8.7%, whole-number pricing |
| [Ollie's Q3 FY2025 release (SEC 8-K)](https://www.sec.gov/Archives/edgar/data/1639300/000114036125044934/ef20060895_ex99-1.htm) | Comps +3.3%, 645 stores (+18.1%), 9.0% operating margin |
| [TheWrap, Netflix Q3 2025 earnings](https://www.thewrap.com/netflix-earnings-q3-2025/) | US and Canada Q3 revenue $5.07B (+17%); 2025 guide +16% |
| [TheWrap, Netflix 2026 price increase](https://www.thewrap.com/industry-news/business/netflix-price-increase-2026) | Ads $8.99, Standard $19.99, Premium $26.99 |
| [TheWrap, Netflix 2026 upfront](https://www.thewrap.com/media-platforms/streaming/netflix-ad-tier-monthly-active-viewers-update-upfronts-2026/) | >250M ad-tier viewers; >60% of sign-ups on ads; ~$9B ad target by 2030 |
| [Marketing Brew, Netflix 2025 upfront](https://www.marketingbrew.com/stories/2025/05/15/netflix-94-million-monthly-active-users-ads-tier-upfronts) | 94M ad-tier monthly users |
| [Churnkey, streaming churn rates](https://churnkey.co/blog/churn-rates-for-streaming-services/) | Netflix ~2.1% monthly vs rivals 5–7%; secondary source |
| [TheWrap / Parrot Analytics, churn economics](https://www.thewrap.com/?p=8011678) | WWE retains ~1.25M subscribers a quarter (model estimate) |

## D4. Files produced

| File | What it is |
|---|---|
| `notebooks/01_exploration.ipynb` | Loads and cleans the filings data, runs the quality audit, draws the exploration charts and tests H1–H6 (65 cells) |
| `notebooks/02_feature_engineering.ipynb` | Builds the model inputs (expansion rate, lags, COVID and paid-sharing flags) and the train/test split (34 cells) |
| `notebooks/03_modeling.ipynb` | Compares Ridge models by walk-forward and leave-one-out tests, picks the winners, scores the 2025 held-out quarter (51 cells) |
| `reports/final_report.md`, `reports/final_report.html` | This report, Markdown and interactive versions |
| `reports/executive_growth_strategy.md` | Strategy memo |
| `reports/ml_handoff_report.md` | Statistician's handoff (contains errors listed in Part C) |
| `reports/ml_followups.md`, `reports/agent_dialogue.md` | Follow-up answers and question log |
| `reports/notebook_review.md` | Notebook review log |
| `reports/customer_risk_scores.csv` | Per-row fits and residuals (mislabelled; in-sample) |
| `reports/tables/actionability_netflix.csv`, `actionability_five_below.csv` | Effect sizes (contain superseded values) |
| `reports/charts/01`–`07` PNG | Seven report charts |
| `reports/exploration/` | findings, hypotheses, data dictionary (md, csv), cleaning log, quality audit, handoff to modeling, 8 charts, 3 clean parquet tables |
| `reports/modeling/` | model card, tuning, features catalogue, scores.csv, 3 feature parquet tables, 7 charts, 6 comparison and coefficient tables |
| `models/netflix_revenue_model.joblib`, `fivebelow_comp_model.joblib`, `fivebelow_margin_model.joblib` | Saved models |
| `src/pipeline.py`, `features.py`, `model_utils.py`, `explore_utils.py` | Reusable training, feature and helper code |
