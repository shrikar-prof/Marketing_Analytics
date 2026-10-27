# Project 04: Marketing Budget Reallocation (Marketing Mix Model)

## Problem
A consumer brand spends roughly $34K a week across TV, out-of-home, print, Facebook and search. Budget shares have been set by precedent. Finance wants evidence the mix is right before approving next year's plan. Attribution tools cover only the digital channels, so there is no common yardstick across the five.

## Question to answer
What does each channel contribute to revenue, where does each one saturate, and how should the same total budget be split to maximize revenue?

## Deliverable expected
A revenue decomposition (baseline vs media), average and marginal ROI per channel, response curves with the current spend marked, a reallocation plan at the same budget with a validation (geo test) design, and an offer sheet.

## Data

### Meta Robyn simulated weekly dataset (MIT), primary
208 weeks, 2015-11-23 to 2019-11-11, one row per week.

| Column | Meaning |
|---|---|
| DATE | week start |
| revenue | weekly revenue (target) |
| tv_S, ooh_S, print_S, facebook_S, search_S | spend by channel |
| facebook_I | Facebook impressions |
| search_clicks_P | search clicks |
| competitor_sales_B | competitor sales index (control) |
| events | event flag ("na" when none) |
| newsletter | newsletter sends |

Also `dt_prophet_holidays.RData`: holiday calendar by country for seasonality controls. Both are R data files; read with `pyreadr`.

Files: `data/raw/dt_simulated_weekly.RData`, `data/raw/dt_prophet_holidays.RData`

```
curl -L -o data/raw/dt_simulated_weekly.RData https://raw.githubusercontent.com/facebookexperimental/Robyn/main/R/data/dt_simulated_weekly.RData
curl -L -o data/raw/dt_prophet_holidays.RData https://raw.githubusercontent.com/facebookexperimental/Robyn/main/R/data/dt_prophet_holidays.RData
```

### Google Meridian simulated data (Apache 2.0), second instance
Geo-level and national versions of a 4-channel simulation, 156 weeks (2021-01-25 to 2024-01-15), 20 geos.

| File | Columns |
|---|---|
| meridian_geo_media.csv | geo, time, Channel0..3_impression, Channel0..3_spend, competitor_activity_score_control, sentiment_score_control, conversions, revenue_per_conversion, population |
| meridian_geo_all_channels.csv | geo version with reach/frequency and organic channels |
| meridian_national_media.csv, meridian_national_all_channels.csv | national aggregates |

```
for f in geo_media.csv geo_all_channels.csv national_media.csv national_all_channels.csv; do
  curl -L -o "data/raw/meridian_$f" "https://raw.githubusercontent.com/google/meridian/main/meridian/data/simulated_data/csv/$f"
done
```

Both datasets are simulated. The method and the deliverable structure are what a client receives on real weekly spend and revenue data (at least two years, ideally by region).
