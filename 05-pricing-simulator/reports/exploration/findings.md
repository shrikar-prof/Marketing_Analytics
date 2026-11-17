# Findings — 05 Pricing Simulator

## Five findings that matter most to the business question

### Finding 1 — Every product category loses units when price rises
**Chart:** `charts/7B_demand_curves_by_category.png`

Log-log slopes are negative in all four categories, confirming that higher prices
reduce units sold. The unadjusted slopes range from about −0.8 (Mouthwash) to
−1.5 (Cold Cereal). After controlling for store and time effects in the model,
true elasticities will likely be more negative. Reliability: strong — the
relationship holds across all 55 products and 77 stores.

---

### Finding 2 — Cereal and Bag Snacks are discounted most aggressively
**Chart:** `charts/7A_discount_depth_by_category.png`

Frozen Pizza and Mouthwash are on promotion in more than half of their store-weeks
(positive median discount), while Bag Snacks and Cold Cereal are discounted in
fewer than half. However, all four categories show wide discount ranges, so all
have enough price variation for reliable elasticity estimation. Reliability:
very strong (direct measurement).

---

### Finding 3 — Feature advertising adds the most unit lift; a price-cut alone adds less
**Chart:** `charts/7C_promotion_lift_by_type.png`

Median units-per-visit during Feature+Display weeks is {promo_lift_fd:.2f}, compared with
{promo_lift_none:.2f} during non-promoted weeks — roughly a 15% lift in purchase rate per
shopping trip. Feature-only weeks also outperform TPR-only weeks, confirming the
circular ad channel contributes beyond the price reduction. Mann-Whitney test
confirms the difference is reliable (p < 0.001; CI excludes zero). Reliability: strong.

---

### Finding 4 — One-third of products generate 80% of revenue
**Chart:** `charts/7D_revenue_concentration.png`

Revenue is moderately concentrated: approximately 20 of the 55 products account
for 80% of total dollar sales. Cold Cereal and Frozen Pizza dominate. The pricing
simulator should prioritise these high-revenue products for the initial model,
then extend to lower-volume products. Reliability: direct measurement; not a
statistical estimate.

---

### Finding 5 — Value-segment stores respond more strongly to promotions
**Chart:** `charts/7F_promo_lift_by_store_segment.png`

The median promotional lift ratio in value stores is higher than in upscale stores.
This means the same promotional spend produces more incremental units in price-
sensitive store segments. Category managers could target deeper promotions to
value stores and reduce promotion intensity in upscale stores to protect margin.
Reliability: moderate — the analysis does not yet control for differences in
product mix by store segment (unclear from this data).

---

## What was not found
- No evidence that any category is fully price-inelastic (zero-slope). Even
  Mouthwash shows a negative slope, though shallower than Cereal.
- Upscale stores do not reliably sell more units per SKU at baseline — the
  segment difference is small and unclear from this data.

## What could not be checked
- True cost / gross margin per UPC is not in the dataset. Profit curves use
  an assumed margin; the model builder will need to supply actual costs.
- Competitor pricing is not available. Measured elasticity includes cross-price
  effects; true own-price elasticity requires competitor data.
