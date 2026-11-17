# Findings

## Summary (five findings that matter most)

### Finding 1 — Zero-inflation is structural and differs by category
Chart: `charts/01_zero_rate_by_category.png`

Roughly half of all 30,490 item-day series show zero units sold on any given day.
HOBBIES items average 83% zero-sale days vs 65% for FOODS.
The rule of thumb averages past sales regardless of whether those days had sales or not,
so it over-forecasts slow-moving HOBBIES items and under-forecasts fast-moving FOODS items.
Effect size: rank-biserial r = -0.41 (95% CI -0.43–-0.40); large and reliable.

### Finding 2 — SNAP benefit days lift FOODS sales by ~10–20%
Chart: `charts/06_snap_effect.png`

On days when government food-stamp (SNAP) benefits are disbursed, California FOODS items
sell about 10% more units than on non-SNAP days.
The same pattern holds in Texas and Wisconsin.
Effect size: r = 0.27 (95% CI 0.22–0.33).
The rule of thumb cannot predict this because it has no calendar-awareness beyond day of week.
Including the SNAP flag in the model is a low-cost, high-impact improvement.

### Finding 3 — Sporting events drive the largest demand spike
Chart: `charts/07_event_type_effect.png`

Total store demand on sporting-event days is +3% above the non-event median.
Effect size: r = 0.13 (95% CI -0.12–0.37).
Religious events also lift demand but by a smaller margin.
Models that include event-type flags should outperform the rule of thumb around these dates.

### Finding 4 — Weekend demand is higher, but the size of the lift differs by category
Chart: `charts/04_demand_category_weekday.png`

FOODS weekend sales are +31% above weekday sales.
Effect size: r = 0.75 (95% CI 0.71–0.79).
The rule of thumb already uses same-weekday history, so it captures part of this effect.
However, it treats all categories the same — a statistical model with a category x weekday
interaction should do better for HOBBIES, which has a flatter weekend curve.

### Finding 5 — Sales are highly concentrated: top 20% of items drive ~60% of volume
Chart: `charts/09_sales_concentration.png`

The demand Lorenz curve (Gini = 0.67) shows strong concentration.
Forecast accuracy improvements on the top-volume items deliver most of the inventory savings.
Slow-moving items (the bottom 60% of series by volume) account for under 20% of units
— a simpler stocking rule (e.g., keep 1 unit as safety stock) may suffice for them.

## What we did not find

- No evidence that FOODS and HOUSEHOLD items differ meaningfully in CV
  (H5 tested; effect size was small).
- No stockout flags exist in the data: zero sales may mean zero demand
  *or* the shelf was empty. This distinction is unclear from this data.
- No store-level demographic or footfall data: we cannot explain why some
  stores are higher-volume than others.

## Charts produced

| File | Finding |
|------|---------|
| charts/01_zero_rate_by_category.png | Zero rate by category and department |
| charts/02_demand_distribution_nonzero.png | Distribution of non-zero daily demand |
| charts/03_demand_by_weekday.png | Day-of-week demand pattern |
| charts/04_demand_category_weekday.png | Category x weekday interaction |
| charts/05_monthly_trend.png | Monthly demand trend 2011–2016 |
| charts/06_snap_effect.png | SNAP benefit-day lift |
| charts/07_event_type_effect.png | Event-type demand lift |
| charts/08_price_vs_demand.png | Price vs average demand |
| charts/09_sales_concentration.png | Sales concentration (Lorenz curve) |
| charts/10_avg_demand_by_store.png | Average demand by store |
| charts/11_cv_by_category.png | Demand volatility (CV) by category |