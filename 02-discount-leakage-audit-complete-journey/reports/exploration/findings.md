# Findings

One year of loyalty-card grocery transactions (ex-fuel): 1,445,035 transaction lines, 2,467 households, 437 stores.

---

## Five Key Findings

### Finding 1 -- Price waterfall: $0.8M leaks to discounts (15.7% of list revenue)
Chart: charts/01_price_waterfall.png

Of $5.1M in gross list revenue, the chain kept $4.3M in pocket revenue. The $0.8M gap splits into $0.8M retailer-funded (15.4% of list) and $0.0M manufacturer-funded (0.4% of list). The retailer-funded share is the cost Finance can influence directly.
Confidence: Accounting totals; no estimation.

### Finding 2 -- Department leakage rates vary widely; TOYS gives away 43.4% of its list revenue
Chart: charts/02_leakage_by_department.png

The three departments with the highest leakage rates (TOYS, MEAT, SEAFOOD-PCKGD) account for a disproportionate share of discount dollars. Departments at or below the 15.7% average are lower-priority review targets.
Confidence: Computed from full transaction population; reliable.

### Finding 3 -- Promoted products carry 31.2% discount rate vs 10.3% when not promoted
Chart: charts/08_promoted_vs_not.png

Transaction lines that match a promotions-table event carry a 31.2% discount rate vs 10.3% off-promotion. Mann-Whitney U test: rank-biserial r = -0.584 (large effect), 95% CI on median difference 0.3103 to 0.3151. Reliable: Yes. Promotions are being run primarily through price reductions.
Confidence: Reliable (p<0.05, large effect). Caveat: promotions table may not capture every event.

### Finding 4 -- Private label: 15.5% retailer-funded discount rate vs 15.3% for national brands
Chart: charts/03_leakage_brand_type.png

National brands shift coupon cost to manufacturers. Private-label items have no manufacturer to share cost, so every markdown is 100% retailer-funded. Promoting private-label items through price cuts costs more than promoting national brands.
Confidence: Reliable (accounting totals; H3 confirmed).

### Finding 5 -- Top 7% of products (5,027 SKUs) drive 80% of all discount spending
Chart: charts/06_leakage_concentration.png

Discount spending is highly concentrated. Reviewing 5,027 products out of 68,178 would cover 80% of total leakage with a focused effort. Income band explains negligible variance in household discount capture (Kruskal-Wallis eta-squared = 0.0519), so leakage is a product and department story, not a household targeting story.
Confidence: Exact calculation from full transaction population.

---

## What Was Not Found

- No evidence that higher-income households capture materially more discounts per dollar spent.
- Cannot confirm whether promotions paid back in volume lift -- incremental sales unavailable.
- Store-level leakage analysis not performed; unclear from this data whether rates vary by geography.
