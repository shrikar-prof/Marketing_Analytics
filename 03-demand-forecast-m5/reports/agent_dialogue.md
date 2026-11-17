# Agent dialogue log

Questions sent by the growth-strategy-partner to the ml-statistician by direct agent message, verbatim as reported by the partner, with the memo section each affected and what changed. The statistician's answers are in `reports/ml_followups.md`. Two rounds; the fallback relay was not used.

## Round 1

**Preamble sent:** "Round 1 follow-up questions from growth-strategy-partner (M5 demand forecast). These are descriptive, from analysis already done. Please append answers to reports/ml_followups.md."

1. **(Memo s.3 dollar translation)** Average sell_price (USD) per unit by category over the test window d_1914–d_1941, and total test-window dollar sales by category (units × weekly sell_price).
   - Sections affected: 1 (thesis scale), 3.1, 3.3, 3.4.
   - What changed: Memo now has a dollar base of $3,900,976 over 28 days, annualised to ~$50.9M. Dollars per unit by category: FOODS $2.69, HOBBIES $4.34, HOUSEHOLD $4.10, overall $3.17. These feed the 3.1 segment table, the buffer and lost-sales dollars in 3.3, and the cost-of-a-miss column in 3.4. Without them, section 3 would have been in units only.

2. **(Memo s.2 gap table, s.3)** Rule-of-thumb RMSE and MAE by category (FOODS, HOBBIES, HOUSEHOLD) on the same test window, so the partner can state the improvement per category.
   - Sections affected: 1, 3.1.
   - What changed: Added per-category MAE gains (FOODS 21%, HOUSEHOLD 19%, HOBBIES 16%) to the thesis and 3.1 table. The statistician's caveat that the rule is reconstructed became open item 1 in section 7.

3. **(Memo s.3 asymmetric errors)** Error direction, model vs rule, by category: total over-forecast units (sum of max(pred−actual,0)) and total under-forecast units (sum of max(actual−pred,0)) over the 28 test days.
   - Sections affected: 1 (lever 1), 2 (empty-shelf row), 3.3 (lost-sales upper bound).
   - What changed: Lever 1 now rests on 108,337 fewer under-forecast units. Section 3.3 states $343K of demand at risk per 28 days. The gap table notes the rule under-forecasts 9% more than it over-forecasts.

4. **(Memo s.3 targeting)** Model vs rule MAE in the top decile of series (is_top_decile == 1) versus deciles 1–9.
   - Sections affected: 1 ("where value leaks"), 5 (Pilot 1 trigger).
   - What changed: Added the two leak bullets: top-decile shortfall 195,875 vs 129,244 units, and over-ordering on the other 90% of 309,403 vs 237,475 units. Confirms operations' "too little fast, too much slow" suspicion. Pilot 1's trigger cites the 52% larger rule shortfall. Answer also clarified the decile is of item-days, not series; memo wording follows that.

5. **(Memo s.4 HOBBIES rounding)** Share of HOBBIES test item-days with actual = 0 where model pred is between 0 and 0.5, and the MAE change if preds < 0.5 are set to 0 (one number per category).
   - Sections affected: 1 (lever 3), 3.4, 4 (Track A4), 5 (Pilot 3 trigger).
   - What changed: Lever 3 and Pilot 3 cite a 7% MAE cut in HOBBIES and HOUSEHOLD. Section 3.4 adds the caveat that RMSE rises slightly (1.707 to 1.715). Memo recommends rounding for order quantities only, not for volume planning.

6. **(Memo s.5 SNAP pilot)** Model MAE on FOODS for SNAP vs non-SNAP test days, and the same for the rule-of-thumb.
   - Sections affected: 2 (SNAP row), 3.1, 4 (Track B2), 5 (Pilot 2 trigger), 7 (open item 4).
   - What changed: Added a measured 14.8% SNAP-day lift on the test window. Track B2's "raise FOODS orders about 15%" comes from it. Added the finding that both forecasters miss more on SNAP days, which is the main reason Pilot 2 exists. Because the window is only 28 days, section 7 lists SNAP as open item 4.

**Closing line sent:** "If any item requires re-modeling, decline it and say which. Thank you."

---

## Round 2

**Preamble sent:** "Round 2 (final) follow-up from growth-strategy-partner. Thank you for round 1. Descriptive only, same test window, append to reports/ml_followups.md."

1. **(Memo s.3 inventory dollars)** Per-series error dispersion, dollar-weighted: for each item-store series compute RMSE over the 28 test days for the model and for the reconstructed rule, multiply by that series' mean weekly sell_price, and report the SUM across all 30,490 series (USD), by category and total.
   - Sections affected: 1 (lever 2 and the profit-share sentence), 3.3.
   - What changed: Headline stock release fell from $175K–$217K (one pooled error figure) to $102K–$127K at cost (per-series, $150,842 vs $119,635, 20.7% lower). Per-series rows added to 3.3 table, original rows relabelled "Pooled". Annual holding saving changed from $44K–$54K to $26K–$32K. Thesis "share of sales" sentence rewritten from "0.3–0.8%" to "0.1–0.3%".

2. **(Memo s.5 stockout audit pilot)** Possible hidden stockouts: among series with training-period mean ≥ 5 units/day, how many test item-days had zero sales, and how many series had a run of 3+ consecutive zero days? By category if easy.
   - Sections affected: 1 (new paragraph), 5 (Pilot 4).
   - What changed: Added a "bigger prize may be hidden" paragraph — 4,086 zero days (11.5%) and 213 series with runs of 3+ consecutive zero days. If these are stockouts, the assumed upper bound is ~$0.72M a year. Pilot 4 redesigned from 2 stores to all 10 stores and the 1,267 fast series, checking the 213 first, at ~150 checks a day.

3. **(Memo s.4 tiering)** For the velocity cut (series mean ≥ 5 vs < 1 unit/day vs in between): series count and share of test units in each tier.
   - Sections affected: 3.4, 5 (Pilots 1 and 3).
   - What changed: Velocity-tier table replaced the "open questions" line in 3.4. Pilot 1's group changed from 10,034 to 9,251 fast and mid series (74% of units, ~4,625 per arm). Pilot 3's group changed from 16,120 to 12,954 slow HOBBIES and HOUSEHOLD series.

**Closing line sent:** "If any needs re-modeling, decline it."

**Unrequested correction from the statistician (round 2):** The handoff report section 6 "series count" column counts items, not item-store series. True series counts: FOODS 14,370, HOUSEHOLD 10,470, HOBBIES 5,650. Logged as open item 5 in strategy memo section 7. No memo figures depended on the wrong counts.

Neither round had a declined question. Nothing from either round is still open.
