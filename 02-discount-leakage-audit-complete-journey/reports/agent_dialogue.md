# Agent dialogue log

Questions sent by the growth-strategy-partner to the ml-statistician by direct agent message, verbatim as reported by the partner, with the memo section each affected and what changed. The statistician's answers are in `reports/ml_followups.md`. Two rounds; the fallback relay was not used.

## Round 1

**Preamble sent:** "Growth-strategy partner here: round 1 of follow-up questions on the Discount Leakage handoff (project 02). Each needs a number or a small table from the analysis already done. Please append them to reports/ml_followups.md and reply here."

1. **(Memo s.3 Segment economics)** Discount $ share of total by department: GROCERY, MEAT, MEAT-PCKGD, DRUG GM, PRODUCE, SEAFOOD-PCKGD, TOYS. I want to show that the dollar pool is GROCERY-led even though TOYS has the top rate.
   - Sections affected: 1 (Diagnosis) and 3a (segment table).
   - What changed: Memo now says GROCERY holds 58.9% ($469.6K). TOYS has the top rate (43.4%) but under $1K. Added a warning that chart 02 ranks by rate and overstates TOYS.

2. **(Memo s.3 Cap economics)** Using ACTUAL disc_rate on all 52 weeks (not predicted): discount $ above a 25% cap, a 35% cap and a 50% cap. Plus the share of discount $ sitting on lines with actual rate >= 25%, >= 40%, >= 50%.
   - Sections affected: 1 (Bottom line, Lever 1), 3c (scenarios), 4B (depth sign-off rule), 5 (Pilot 1 trigger).
   - What changed: Ceiling of $227.6K above a 25% cap (28.5% of discount $), $107.1K above 35%. Lines at 25% or deeper hold 75.8% of discount $. This became the upper end of Lever 1 and the Pilot 1 trigger.

3. **(Memo s.3 Annualisation)** Overall disc_rate and discount $ in the test window, weeks 40-52, vs weeks 1-39. Is annualising the $20,585 an over- or understatement?
   - Sections affected: 1 (scope and corrections note), 2 (benchmark row), 3c (scenario table).
   - What changed: Test window is 14 weeks, not 13. Model-based saving drops to $76.5K a year. Corrections note added.

4. **(Memo s.5 Pilot - payback test)** Volume response proxy: for the top 100 SKUs by discount $, the median ratio of units sold per week when disc_rate >= 20% vs < 5%, and the IQR.
   - Sections affected: 2 (benchmark row), 3b (below-cost test), 5 (Pilot 2).
   - What changed: Median ratio 4.5x (IQR 3.3x–6.7x), labelled as not causal. Assumed true lift ~1.9x fails break-even at 20%+ depth, justifying Pilot 2 payback hold-out.

5. **(Memo s.4 Store ceiling)** Store spread: across stores with >= $10K list revenue, count, p10/median/p90 disc_rate, and stores above 20%.
   - Sections affected: 1 (Diagnosis), 3d (levers table), 5 (pilot store pool).
   - What changed: Stores are tightly bunched (13.8%/15.9%/18.5%); only 4 above 20%. Store-level ceiling dropped as a lever; pilot draws on all 437 stores for matched pairs.

6. **(Memo s.3 Promotion mechanics)** From the promotions join: disc_rate and discount $ for display only / mailer only / both / neither. Plus the share of discount $ on promo-matched lines.
   - Sections affected: 1 (Lever 3, Diagnosis), 2, 3a, 4B, 5 (Pilots 2 and 4).
   - What changed: Mailer lines hold $255.9K at 34.4%, plus display $104.0K at 36.5% → Lever 3 (~$360K). Display-only runs at 17.6% → Pilot 4. Unmatched lines hold 48.5% ($386.8K) → "silent markdown" finding and recommendation 4B item 4.

7. **(Memo s.3 Brand)** Discount $ split national vs private label (dollars and share).
   - Sections affected: 1 (Lever 2), 3a, 4B, 5 (Pilots 3 and 4).
   - What changed: National $618.3K (77.6%) → Lever 2 (supplier funding $31K–$62K at 5–10% assumed) and Pilot 3. Private label $178.9K (15.6% depth, same as national) → "cash trap" policy and Pilot 4.

8. **(Memo s.3 Households)** Share of total discount $ captured by top 10% and top 20% of households ranked by disc_rate, and their list revenue share.
   - Sections affected: 1 (Diagnosis).
   - What changed: Top 10% hold 12.9% of discount $ on 7.6% of list revenue. Household targeting ruled out; backs up income finding.

**Closing line sent:** "If any item requires re-modeling, decline it and say which. Thank you."

**Corrections the statistician volunteered (used in memo):**
- Handoff section 7a shows modeled dollars, not actual; memo section 3e now uses actual figures.
- Decile dollars come from tables/01_decile_targeting.csv.
- Finding 2 figures (2.9% vs 16.6%) are medians, not averages.

---

## Round 2

**Preamble sent:** "Round 2 (final) follow-up questions from the growth-strategy partner on project 02. Thanks for round 1; corrections noted and will be cited. Same rules: descriptive groupbys only, append to reports/ml_followups.md."

1. **(Memo s.3 Below-cost test)** List revenue on lines with actual rate >= 25% and >= 40% (discount $ already given; need list $ for average rate).
   - Sections affected: 1 (Bottom line), 3b, 3c.
   - What changed: List $1,507K at 40.1% depth, $719K at 49.2%. Below-cost table added. At assumed 33% margin, 25%-plus lines lose ~$107K a year. Planning case: each 10% of lost volume costs only ~$12K.

2. **(Memo s.3 / Pilot 1)** Split $227,564 above the 25% cap by promo group (both/mailer only/display only/unmatched) and by brand (national/private).
   - Sections affected: 3a (new "Where the above-cap dollars sit" table).
   - What changed: Mailer-linked lines hold 59.6% of above-cap dollars; unmatched 34.5%; national 80.5%. Strengthens Pilots 2 and 3.

3. **(Memo s.3 / Pilot 1)** $227,564 above the 25% cap by department: top 5 departments and top 10 product categories.
   - Sections affected: 3a, 3c, 5 (Pilot 1 design).
   - What changed: Five traffic categories (soft drinks, chicken, milk, beef, ice cream) hold $69K (30.4%). They became the traffic carve-out in Pilot 1.

4. **(Memo s.4 SKU review list)** How many SKUs hold 50% and 80% of the $227,564 above the 25% cap?
   - Sections affected: 1 (Bottom line), 3a, 5 (Pilot 1).
   - What changed: 383 SKUs hold 50%, 2,529 hold 80%. Pilot 1 target changed from "top 500 non-traffic SKUs" to "the 383 SKUs, less traffic items".

5. **(Memo s.3 Seasonality)** Discount $ in week 27 and weeks 21–23, and the excess over the 53-week weekly mean.
   - Section affected: 3a (seasonality).
   - What changed: Week 27 is $5,668 (37.7%) above mean. Weeks 21–23 together $5,948 above mean. Calendar called "worth managing, not a main lever". Chart 04 title noted as incorrect ("more than double"; true is 1.27x).

**Closing line sent:** "If any needs re-modeling, decline it."

Neither round had a declined question. Nothing from either round is still open.
