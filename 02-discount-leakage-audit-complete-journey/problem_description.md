# Project 02: Pricing and Discount Leakage Audit

## Problem
A regional grocery chain runs loyalty-card markdowns on about half of all items sold. Finance sees the discount line growing faster than sales and wants to know whether promotions pay for themselves. Merchandising believes promotions drive traffic and defends the budget. Nobody has a line-item view of where the money goes.

## Question to answer
How much list revenue leaks to discounts, where does it concentrate (department, category, brand, household), which promotions fail to pay back, and what margin is recoverable if the worst ones are trimmed?

## Deliverable expected
A price waterfall from gross list to pocket revenue (retailer-funded vs manufacturer-funded), a leakage map, a promotion pay-back test, a discount policy recommendation, an estimated recoverable margin with the assumptions stated, and an offer sheet.

## Data

### Dunnhumby "The Complete Journey" (via the completejourney R package, CC0)
One year of grocery transactions for a panel of loyalty households, as R data objects. Read in Python with `pyreadr`.

| File | Rows | Columns |
|---|---|---|
| transactions.rds | 1,469,307 | household_id, store_id, basket_id, product_id, quantity, sales_value, retail_disc, coupon_disc, coupon_match_disc, week, transaction_timestamp |
| products.rda | 92,331 | product_id, manufacturer_id, department, brand (National/Private), product_category, product_type, package_size |
| promotions.rds | 20,940,529 | product_id, store_id, display_location, mailer_location, week |
| coupons.rda | 116,204 | coupon_upc, product_id, campaign_id |
| coupon_redemptions.rda | 2,102 | household_id, coupon_upc, campaign_id, redemption_date |
| campaigns.rda | 6,589 | campaign_id, household_id |
| campaign_descriptions.rda | 27 | campaign_id, campaign_type, start_date, end_date |
| demographics.rda | 801 | household_id, age, income, home_ownership, marital_status, household_size, household_comp, kids_count |

Field meanings (from the package guide): `sales_value` is the amount the retailer receives after the loyalty discount and coupon match; `retail_disc` is the loyalty-card markdown; `coupon_disc` is a manufacturer coupon (reimbursed to the retailer); `coupon_match_disc` is the retailer matching a manufacturer coupon. All discounts are stored as positive numbers. Dates run 2017-01-01 to 2017-12-31 (re-indexed from the original). 2,469 households, 457 stores, 68,509 products.

Known quirks: FUEL department quantities are in different units (large values); some lines have zero quantity or zero value (returns); the original Dunnhumby release covers two years, this package slice covers one.

Files: `data/raw/*.rda`, `data/raw/*.rds`

```
for f in campaign_descriptions.rda campaigns.rda coupon_redemptions.rda coupons.rda demographics.rda products.rda promotions.rds transactions.rds; do
  curl -L --retry 3 -o "data/raw/$f" "https://raw.githubusercontent.com/bradleyboehmke/completejourney/master/data/$f"
done
pip install pyreadr
```
Original two-year release: dunnhumby.com/source-files (The Complete Journey).
