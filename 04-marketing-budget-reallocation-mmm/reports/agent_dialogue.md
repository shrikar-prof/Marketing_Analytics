# Agent dialogue log

Questions sent by the growth-strategy-partner to the ml-statistician by direct agent message, verbatim as reported by the partner, with the memo section each affected and what changed. The statistician's answers are in `reports/ml_followups.md`. Two rounds; the fallback relay was not used.

## Round 1

**Preamble sent:** "Round 1 follow-up questions from growth-strategy-partner on the MMM handoff report. These are descriptive reads of the existing fitted Ridge model and data only. Please append answers to reports/ml_followups.md."

1. **(Memo s.3 marginal return per channel)** Final model features: which features are in the fitted Ridge model (the _log set, the _sat set, or both)? Give the Ridge coefficient for each of the five channel features (tv/ooh/print/facebook/search).
   - Sections affected: §1.3, §3.1, §4 Track A item 4.
   - What changed: Model uses only the _log set; no adstock or Hill terms. "TV and Print are saturated" reframed as a result of the log formula, not a finding (§1.3). Print marked "not identified" because its VIF with the print-zero flag is 43.6 (§3.1 reliability column). Track A item 4 added: drop either print spend or its zero flag before re-fitting.

2. **(Sections 1, 3, 4)** Marginal return at current spend: for each channel, the predicted weekly revenue change for +$1K spend at (a) the mean active-week spend and (b) the all-week average marked on 01_channel_response_curves.png. Same method as the existing response curves (others at training mean).
   - Sections affected: §3.1, §3.3, §2.
   - What changed: Fills the §3.1 return column — TV $1.21, OOH -$0.19, Print $4.74, Facebook $0.96, Search -$0.08 per $1. Supports the conclusion that only Print clears the $2.00 break-even (50% gross margin assumed). Overturned the brief's claim that Facebook is "the steepest curve". TV, Print, Search and Facebook rows in the §2 benchmark table now use these numbers.

3. **(Sections 1, 5)** Table 04 scenario (TV -$6,712, Facebook +$6,712 per week): the model's predicted weekly revenue change in USD, and the range across the 10 CV folds' refits if those fitted coefficients exist. My read of chart 01 is that the TV loss may exceed the Facebook gain; please confirm or correct.
   - Sections affected: §1.1, §1.3, §5 Pilots 2 and 3, §6.
   - What changed: Shift nets -$2,129 per week; 11 re-fits split 6 to 5 on the sign. Main recommendation changed to "do not move budget yet" (§1.1). TV-to-Facebook shift replaced by Pilot 2 (TV switched off in some regions). Facebook coefficient ranging from $3,772 to $19,760 became trigger for Pilot 3. §6 gained the row "Freeze 2019 mix; no TV-to-Facebook shift".

4. **(Section 3, gap G1)** Collinearity: Pearson r (or VIF) for ooh_S_log vs total_spend_log, and search_S_log vs trend.
   - Sections affected: §1.3, §3.1.
   - What changed: Answer was r = 0.63, VIF 2.1 to 2.9. §1.3 now corrects the handoff's claim that collinearity caused OOH and Search to slope down. In §3.1, OOH reliability reads "negative sign; cause unknown". Did not alter any recommendation.

5. **(Sections 1, 3)** Pearson r of competitor_sales_log with cos_1, and with each of the five channel _log features. I want to know if the competitor index may be absorbing media or seasonal effect.
   - Sections affected: §1.3, §3.2, §4 Track A item 5, Pilot 3.
   - What changed: Answer was r = 0.96 with cos_1. "Market demand is the largest driver" became "competitor index plus season" (§1.3 and §3.2 structural row). Track A item 5 added: use either the competitor index or the seasonal terms, not both. The 0.37 correlation with Facebook went into Pilot 3's trigger as a sign the model may under-credit Facebook.

6. **(Section 3)** Event weeks: chart 08 shows medians near $2.45M vs $1.85M (~32%), while the report says 18%. Please give mean and median for each group and which statistic the 18% uses.
   - Sections affected: §1.3, §3.2, §4 Track A item 6, §6.
   - What changed: Data has only 2 event weeks, not 15. Events removed as a usable lever. §3.2 now says "not yet usable; only 2 weeks". §1.3 withdraws the 18% figure. Track A item 6 asks for a verified event calendar. Event program in §6 rated "Not established" and placed in Wave 3. Track B item 4 tells Finance to withdraw the claim.

7. **(Section 1)** Media vs baseline decomposition: share of 4-year predicted revenue attributable to the five channels combined (signed contributions vs a zero-spend counterfactual), if computable from the existing model.
   - Sections affected: §2, §5.1, Pilots 1, 2 and 5.
   - What changed: Gave 4-year average returns in §2 table — TV 5.7x, Print 19.2x, -$8.1M for OOH. Revenue shares: TV 4.6%, Print 3.9%. These became the claims Pilots 1 and 2 are designed to disprove. Set up §5.1 point that regional tests only catch large claims. Print's 19x became "implausible vs external" trigger for Pilot 1. 6.8% and 16.9% totals not used in §1 because statistician called the all-spend-zero figure an extrapolation.

8. **(Section 2)** Total media spend by calendar year (2016, 2017, 2018, 2019 partial) in USD, and OOH share by year. Chart 07 looks like spend fell after 2017.
   - Sections affected: §1.1, §1.2, §1.3, §2, §4 Track B item 3, Pilots 4 and 5.
   - What changed: Largest single effect. Created the §1.2 finding that spend fell 72% while revenue barely moved. Sized lever 1 in §1.1 (up to $3.3M/yr of OOH avoided). Withdrew the "flat budget" claim in §1.3. Gave §2 row for media as share of revenue. Led to Track B OOH gate, search growth as Pilot 4's trigger, and Pilot 5.

**Closing line sent:** None stated explicitly. All eight questions were answered.

---

## Round 2

**Preamble sent:** "Round 2 (final) from growth-strategy-partner. Thank you for the corrections in round 1; they change the memo. Descriptive only; please append to reports/ml_followups.md."

1. **(Memo section 2 and 3, OOH lever)** Revenue by calendar year (2016, 2017, 2018, 2019 to 11 Nov): total, mean weekly, and mean weekly for the same weeks-of-year in 2018 vs 2019 (weeks 1–45). Plus mean residual (actual minus predicted) by year. This tests whether revenue held as OOH fell from $3.70M to $0.34M.
   - Sections affected: §1.2, §4 Track B item 3, Pilot 5, §6.
   - What changed: Like-for-like revenue fell 3.1%. Added "each cut dollar cost at most $1.82 of revenue" and "the cut was roughly break-even or better" (§1.2), labelled assumed. OOH gate rated "Med (observational)" in §6. Mean residuals by year produced no change.

2. **(Section 3, reallocation base)** 2019 spend split: per-week spend by channel (TV, OOH, Print, Facebook, Search) for 2019 weeks, and share of 2019 total. This is the true "current plan" base.
   - Sections affected: §1.1, §3.1, §4 Track B, §5.1, Pilot 4.
   - What changed: Became the base for the plan. Fills §3.1 spend column and §1.1 lever 2 figure (Search is 31.5% of spend, $401K). Supports finding that Search plus OOH took 58% of 2019 spend. Base for provisional $34K/week plan in Track B. Gives §5.1 figure that no channel's 2019 weekly spend exceeds 0.54% of weekly revenue. Active-week counts backed up the flighting point in §3.2.

3. **(Section 5, minimum detectable effect)** Noise for test sizing: SD of training residuals in USD per week, and lag-1 autocorrelation of residuals.
   - Sections affected: §5.1.
   - What changed: $231K residual SD (12.7% of revenue) cited in §5.1 to explain why small tests fail. Low autocorrelation (+0.077) not cited in memo but supports assumption of independent weekly errors. No other change.

4. **(Section 5, geo test design)** Meridian geo file (data/raw/meridian_geo_media.csv): number of geos, median weekly revenue per geo, and median across geos of the coefficient of variation of weekly revenue.
   - Sections affected: §5.1, Pilots 1 and 2.
   - What changed: 27.6% variability drives the §5.1 sizing table. With external 0.96–0.98 pre-period fit, gives smallest detectable effects of ~4.4% over 8 weeks and ~3.6% over 12. 20 regions and 7x size range set the region pool note and pilot cells (6 test + 14 controls in Pilot 1, 5 test in Pilot 2). Median weekly revenue per region ($320.7K) produced no change.

Neither round had a declined question. Nothing from either round is still open.
