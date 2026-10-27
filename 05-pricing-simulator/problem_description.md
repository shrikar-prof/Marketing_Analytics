# Project 05: Price Elasticity and a Reusable Pricing Simulator

## Problem
A grocery chain prices and promotes by category: one markdown depth, one feature cadence, one set of rules for every product in the aisle. Category managers suspect some products are over-promoted and others could carry a higher everyday price, but have no product-level evidence to argue with vendors or finance.

## Question to answer
How price-sensitive is each product (own-price elasticity), how much do feature advertising and in-store display add beyond the price cut, and which products can take a price increase without losing profit?

## Deliverable expected
An elasticity table with confidence intervals per product, promotion lift by category, profit curves, a repricing shortlist, and a reusable decision tool: a pricing simulator (single HTML file) that shows units, revenue and gross profit for any price move on any product, with an uncertainty band, and accepts a client's own product. Plus an offer sheet.

## Data

### Dunnhumby "Breakfast at the Frat"
Weekly store-level sales and promotion data for the top 5 products from each of the top 3 brands in four categories (mouthwash, pretzels, frozen pizza, boxed cereal), 156 weeks, January 2009 to December 2011, 77 stores.

One Excel workbook with four sheets (note: each sheet has a title row, so read with `header=1`):

| Sheet | Columns |
|---|---|
| dh Transaction Data | WEEK_END_DATE, STORE_NUM, UPC, UNITS, VISITS, HHS, SPEND, PRICE, BASE_PRICE, FEATURE (0/1 in weekly ad), DISPLAY (0/1 in-store display), TPR_ONLY (0/1 temporary price reduction without feature or display) |
| dh Products Lookup | UPC, DESCRIPTION, MANUFACTURER, CATEGORY, SUB_CATEGORY, PRODUCT_SIZE |
| dh Store Lookup | STORE_ID, STORE_NAME, ADDRESS_CITY_NAME, ADDRESS_STATE_PROV_CODE, MSA_CODE, SEG_VALUE_NAME, PARKING_SPACE_QTY, SALES_AREA_SIZE_NUM, AVG_WEEKLY_BASKETS |
| Glossary | variable definitions |

`PRICE` is the shelf price that week; `BASE_PRICE` is the regular price; their difference is the discount. About 60 UPCs in total, around 55 with enough price variation to model.

File: `data/raw/dunnhumby_breakfast_at_the_frat.xlsx` (34 MB)

```
curl -L --retry 3 -o data/raw/dunnhumby_breakfast_at_the_frat.xlsx \
  "https://raw.githubusercontent.com/mehwish2525/dunnhumby-_Breakfast-at-the-Frat/HEAD/dunnhumby%20-%20Breakfast%20at%20the%20Frat.xlsx"
pip install openpyxl
```
Official source: dunnhumby.com/source-files ("Breakfast at the Frat"; the page's download links are JavaScript-rendered). The GitHub mirror has the same file size as the original workbook (34,051,636 bytes).

### Deeper alternative (not downloaded)
Dominick's Finer Foods, Kilts Center, Chicago Booth: ~98.7M weekly store-UPC observations, 1989 to 1997, with price, units, margin and deal codes. Requires registration.
