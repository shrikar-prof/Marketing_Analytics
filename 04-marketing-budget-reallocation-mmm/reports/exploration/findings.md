# Findings — Marketing Budget Reallocation (MMM)

## Key Numbers at a Glance

| Metric | Value |
|--------|-------|
| Weeks analysed | 208 (Nov 2015 – Nov 2019) |
| Mean weekly revenue | $2.9 M |
| Mean weekly total media spend | ~$34 K |
| Media spend as % of revenue | ~1.2% |
| Channels | TV, OOH, Print, Facebook, Search |
| Event weeks | 15 of 208 (7%) |

---

## Finding 1: TV dominates the budget but shows the weakest revenue lift

TV takes 46% of total weekly spend (~$15.6K). Yet weeks in the top TV-spending quintile generate only about 5% more revenue than weeks in the bottom quintile (rank-biserial r = -0.58 — a small effect). This is consistent with TV operating at or near saturation. At the current level, an extra dollar in TV produces very little incremental revenue.

**Chart:** 05_revenue_by_spend_quintile.png, 03_spend_revenue_scatter.png

---

## Finding 2: Search has the highest revenue lift per quintile

Search takes only ~11% of total spend (~$3.7K/week) yet weeks in the top search quintile average 49% more revenue than the bottom quintile. The slope on the spend-revenue scatter remains steep in the mid-range before flattening — suggesting there is room to grow search spend before hitting saturation.

**Chart:** 05_revenue_by_spend_quintile.png, 03_spend_revenue_scatter.png

---

## Finding 3: Event weeks add an average 18% revenue lift

The 15 event weeks earn, on average, 18% more revenue than the 193 non-event weeks. This effect is statistically reliable (Mann-Whitney p < 0.001, r ≈ 0.37). Any MMM must include event flags as controls, otherwise the model will credit the channels that happened to run heavy spend in those same weeks.

**Chart:** 06_event_vs_nonevent_revenue.png

---

## Finding 4: The total budget is flat; reallocation is a zero-sum decision

Total weekly spend across all five channels has shown no statistically significant trend over four years (Spearman ρ = -0.089, p = 0.200). Every dollar shifted to a higher-ROI channel is a dollar taken from a lower-ROI one. The reallocation question is: take from TV (which appears saturated) and give to Search (which appears under-invested).

**Chart:** 08_spend_mix_over_time.png

---

## Finding 5: Channels are largely independent — attribution is feasible

The five spend channels correlate weakly with each other (most pairwise r below 0.2). This is good news: a Marketing Mix Model can separate the contribution of each channel without serious collinearity (two measures that move together and are hard to tell apart). Facebook impressions and search clicks are highly correlated with their respective spend columns (r > 0.95) and should be excluded from the model to avoid confusion.

**Chart:** 04_correlation_matrix.png

---

## What we did not find / could not check

- **Causal ROI.** The lift numbers above are associations, not causal estimates. A proper MMM with adstock and saturation curves is required.
- **Carry-over effects.** TV and OOH likely affect revenue in future weeks. This notebook does not model adstock (decay of past spend). The model builder must.
- **Price and promotions.** No pricing data is in the Robyn file. If prices changed over the period, revenue trends may be partly driven by pricing, not media.
- **Meridian cross-geo patterns.** The geo-level data confirms spend drives revenue across geos, but geo-level MMM analysis is deferred to the model builder.
