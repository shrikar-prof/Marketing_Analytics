# Feature Table — 05 Pricing Simulator

| Feature | Meaning | Source columns | Type | Why it exists |
|---|---|---|---|---|
| LOG_PRICE | Log of actual shelf price (the core elasticity input) | PRICE | numeric | Explorer finding 1: all categories have negative log-log slopes |
| DISCOUNT_PCT | Percentage markdown vs base price | PRICE, BASE_PRICE | numeric | Explorer finding 3: Feature+Display events are deeper markdowns |
| VISITS | Store traffic (shopping trips including this product) | VISITS | numeric | Explorer finding 5: VISITS chosen over HHS (r=0.99 collinearity) |
| AVG_WEEKLY_BASKETS | Average weekly transactions at the store | AVG_WEEKLY_BASKETS | numeric | Store size control |
| SALES_AREA_SIZE_NUM | Store selling floor area (sq ft) | SALES_AREA_SIZE_NUM | numeric | Store size control |
| LOG_BASE_PRICE | Log of regular everyday price (anchors price level) | BASE_PRICE | numeric | Explorer finding 2: different price levels across categories |
| PRICE_TO_BASE_RATIO | Markdown depth: PRICE/BASE_PRICE (1=no promo) | PRICE, BASE_PRICE | numeric | Explorer finding 3: captures promotional depth scale-free |
| WEEK_OF_YEAR | ISO week number (1-52) for seasonal demand | WEEK_END_DATE | numeric | Controls for seasonal demand cycles |
| YEAR | Calendar year (2009-2011) for trend | WEEK_END_DATE | numeric | Controls for 3-year demand trend |
| STORE_UPC_LAG1 | Last week's LOG_UNITS for same store-product pair | LOG_UNITS, WEEK_END_DATE | numeric | Serial correlation in demand |
| STORE_UPC_ROLL4 | 4-week rolling mean LOG_UNITS for same store-product | LOG_UNITS, WEEK_END_DATE | numeric | Short-run demand trend smoothing |
| CATEGORY_AVG_LOG_PRICE | Mean log-price of all products in same category+week | LOG_PRICE, CATEGORY | numeric | Explorer finding 2: cross-price proxy for competitive dynamics |
| FEATURE | 1 = in weekly advertising circular | FEATURE | binary | Explorer finding 3: Feature lifts units above TPR alone |
| DISPLAY | 1 = in-store display | DISPLAY | binary | Explorer finding 3: Display lifts units above TPR alone |
| TPR_ONLY | 1 = price reduction with no Feature or Display | TPR_ONLY | binary | Explorer finding 3: baseline promo type |
| IS_ON_PROMO | 1 = any promotion active (Feature OR Display OR TPR) | FEATURE, DISPLAY, TPR_ONLY | binary | Explorer finding 4: 28% of rows on promo |
| CATEGORY | High-level product category (4 levels) | CATEGORY | categorical | Explorer finding 2: category drives elasticity differences |
| SUB_CATEGORY | Product sub-category (7 levels) | SUB_CATEGORY | categorical | Fine-grained product grouping |
| SEG_VALUE_NAME | Store value segment (Value/Mainstream/Upscale) | SEG_VALUE_NAME | categorical | Store price-sensitivity segment |
| PROMO_TYPE | Promotion mechanic label (5 levels) | PROMO_TYPE | categorical | Explorer finding 3: mechanic type controls |