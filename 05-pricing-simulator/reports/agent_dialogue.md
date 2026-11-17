# Agent dialogue log

Questions sent by the growth-strategy-partner to the ml-statistician by direct agent message, verbatim as reported by the partner, with the memo section each affected and what changed. The statistician's answers are in `reports/ml_followups.md`. Two rounds; the fallback relay was not used.

## Round 1

**Preamble sent:** "Growth-strategy round 1: 8 descriptive questions from existing data/fitted models only (no re-modeling). Please append answers to reports/ml_followups.md and reply with a short summary."

1. **(Memo §1, §2, §3 revenue sizing)** Total revenue. decile_revenue.csv and category_segment_detail.csv sum SPEND to about $30.2M over 156 weeks. Handoff §2 and §6b state $1.49B total / $801M Cereal "annualised". Which is correct? Please give total SPEND and annual SPEND (total/3) by category.
   - Sections affected: §1, §2, §3.1.
   - What changed: Revenue corrected to $28.69M total, $9.56M a year (Cereal $5.14M, Pizza $2.21M, Bag Snacks $1.62M, Oral Hygiene $0.59M). The handoff's $1.49B was an arithmetic error (3-year total multiplied by 52 again). Every lever was re-sized and a corrections box added to the top of the memo.

2. **(§3 drivers, §4 Track A)** VISITS definition. data_dictionary.md defines VISITS as "shopping trips including this product" (an outcome, r=0.99 with UNITS), not store traffic as handoff §5 states. Please confirm, and confirm the §6e counterfactual held VISITS fixed at observed values when price was cut 10%. Also give median UNITS/VISITS overall.
   - Sections affected: §3.3, §3.4, Track A2, B1.
   - What changed: VISITS confirmed as an outcome (median UNITS/VISITS = 1.038, r=0.987). The demand simulator is frozen for price decisions. The 10% price-cut counterfactual result (+0.8% to +3.2% units) is relabelled a lower bound throughout.

3. **(§3 response curves)** Exploration slopes (−1.44, −1.16, −0.34, −0.38): are they each fit across one point per UPC (~10–15 points per chart 01)? Give n and SE for each slope; reconcile with hypotheses.md H3 and findings.md F1.
   - Sections affected: §3.3, §1.
   - What changed: Slopes labelled "measured association; not reproducible". Between-product, row-level, and within-product alternatives presented side by side. The thesis that Bag Snacks and Pizza are most price-sensitive was withdrawn. Pilot 2 moved to Cereal.

4. **(§2 benchmark, §5 pilots)** By category: % of store-weeks with PRICE < BASE_PRICE; % with FEATURE=1; % with DISPLAY=1; mean discount depth; % of SPEND sold in discounted weeks.
   - Sections affected: §1 thesis, §2, §3.2.
   - What changed: Discount share ~37% of SPEND, ~$1.0M/year in markdown derived. Finding F2 ("Bag Snacks and Cereal rarely discounted") exposed as a median artifact — all four categories discounted in 23–29% of rows.

5. **(§3 promo lift, §5 pilot sizing)** By category × promo type (None, TPR only, Display only, Feature only, Feature+Display): row count, median UNITS per store-week, median UPV.
   - Sections affected: §3.2, Pilot 4.
   - What changed: Promotions lift units 2–4x; units-per-trip rise only 0–15%. Display-only results for Bag Snacks prompted Pilot 4 (display without price cut).

6. **(§3 segment economics)** Promo lift ratio (promoted / non-promoted median units) by store segment within each category.
   - Sections affected: §3.4, B1, risk table.
   - What changed: Value-store advantage does not hold within any category (Bag Snacks: Mainstream 1.80, Upscale 1.56, Value 1.75). Value-store targeting recommendation withdrawn.

7. **(§3 price-increase evidence)** For rows with PRICE > BASE_PRICE (~2%): count by category, and median units in those weeks vs median units at PRICE = BASE_PRICE for the same UPC-store pairs.
   - Sections affected: §3.3.
   - What changed: Units are higher in price-increase weeks — the same positive direction as Ridge FE, confirming price moves follow demand rather than cause it. This backs test-before-rollout.

8. **(§4 Track B private label)** Revenue share of private-label UPCs by category; mean shelf price of PL vs national-brand UPCs within each category.
   - Sections affected: §2, Lever 3, Pilot 5, B5.
   - What changed: Store-brand share benchmarked to 21.3% PLMA average. Cereal (13.9%) and Oral Hygiene (17.2%) are the gaps. Lever 3 and Pilot 5 added.

**Optional** (week-to-week CV for pilot sizing) → §5 pilot minimum-detectable-effect calculations.

---

## Round 2

**Preamble sent:** "Growth-strategy round 2 (final): 6 descriptive questions, existing data only. Thank you for round 1; it reshaped the memo. Please append to reports/ml_followups.md under 'Round 2' and reply with a short summary."

1. **(§5 pilot sizing)** Number of stores by segment (Mainstream / Upscale / Value), and number of distinct stores selling each category.
   - Sections affected: §5.
   - What changed: Store split 43 Mainstream / 15 Upscale / 19 Value. Sets the 38 vs 39 store arms and tier stratification for all five pilots.

2. **(§1 Lever 1, §3 promo economics)** By category: median SPEND per store-UPC-week in discounted vs undiscounted rows (same store-UPC pairs). Revenue lift ratio.
   - Sections affected: §3.2 break-even table, Lever 1, Pilots 1 and 3.
   - What changed: Revenue lift ratios: Bag 1.15×, Cereal 1.55×, Pizza 2.29×, Oral 1.23×. At assumed 30% margin, no category breaks even. Break-even table added to §3.2.

3. **(§3, Pilot 1)** Post-promotion dip. By category: median units in the first undiscounted week after a discounted week vs undiscounted weeks ≥3 weeks away from any discount.
   - Sections affected: §3.2.
   - What changed: No post-promotion dip in medians. Main risk is markdown waste, not pull-forward cannibalization.

4. **(§4 Track B cadence)** By category: median discounted weeks per store-UPC per year; median length of consecutive discount runs.
   - Sections affected: §3.1 table, B4.
   - What changed: Cadence 11–16 weeks/year per store-product. Run length 2–4 weeks. Informs promotion-holdout design.

5. **(§5 pilot design)** By category: median BASE_PRICE changes per UPC over 156 weeks; share that are chain-wide (same week, ≥90% of stores).
   - Sections affected: §3.3, Pilot 2.
   - What changed: Only 3–9% of base-price changes are chain-wide. Stores already differ on everyday price, making store-randomised price tests operationally normal.

6. **(§3 concentration)** Number of UPCs making up 80% of SPEND, out of 55 total.
   - Sections affected: §3.1.
   - What changed: 25 of 55 UPCs (45%) make 80% of SPEND. Finding F4 ("~20 of 55") corrected. Pilot 2 targets this top-25 group.

Neither round had a declined question. Nothing from either round is still open.

**Consistency flags raised by statistician (not in the memo yet; for report-writer):**
- Handoff §2 and §6b revenue figures ($1.49B / $801M Cereal) are arithmetic errors; correct figures are in ml_followups.md.
- Exploration slopes (−1.44, −1.16, −0.34, −0.38) could not be reproduced; within-product order differs. The memo labels them "measured association; not reproducible".
- VISITS is an outcome variable (trips including the product), not store traffic. Simulator results are a lower bound.
- clean.parquet has 13,693 duplicate store-product-week keys; all follow-up sums include duplicates.
- Finding F2 ("Bag Snacks and Cereal rarely discounted") is a median artifact; all four categories discount 23–29% of rows.
- Finding F4 (~20 of 55 products make 80% of SPEND) corrected to 25 of 55.
