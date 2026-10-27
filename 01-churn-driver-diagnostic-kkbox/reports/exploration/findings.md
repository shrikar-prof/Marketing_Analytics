# Findings: what the data says about churn

## Summary: the five findings that matter most

Base: 7,043 customers, 1,869 left (26.5%). They paid $139,131 a month, 30.5% of $456,117 monthly revenue. Rates below are shares of the customers in each group. None says why customers leave.

1. **Contract type is the strongest single link to churn.** Month-to-month customers leave at 42.7% (3,875 customers); two-year customers at 2.8%. Month-to-month holds 88.5% of leavers and 86.9% of lost revenue. Reliable (H1). Chart: `charts/03_churn_by_contract.png`.
2. **New customers leave at the highest rate.** Months 0-6: 52.9% (1,481 customers, 21% of base), holding 42% of leavers. After 4 years: 9.5%. Reliable (H3). Chart: `charts/04_churn_by_tenure.png`.
3. **Fiber-optic customers leave at about twice the DSL rate, and the gap is not just a contract effect.** Fiber 41.9% versus DSL 19.0%; fiber holds 69% of leavers. On month-to-month alone: fiber 55% versus DSL 32%. Reliable (H2). Chart: `charts/10_heat_contract_by_internet.png`.
4. **Electronic-check payers leave at 45.3%, against 15.2% to 19.1% for the other three methods.** They are 34% of customers and 57% of leavers. The gap holds on month-to-month contracts (54% versus about 33% for automatic payers). Reliable (H4). Chart: `charts/12_heat_payment_by_contract.png`.
5. **A small, well-defined group holds a large share of the loss: month-to-month fiber customers in their first 12 months.** 916 customers (13% of base) leave at 70%, and hold 34% of leavers and $53,178 of monthly revenue lost (38% of the total). Each 10% of that group's leavers kept is worth $5,318 a month ($63,814 a year). Widening to all month-to-month customers in year one covers 55% of leavers. Chart: `charts/15_candidate_groups_revenue.png`.

Also notable: internet customers without tech support leave at 42% versus 15% with it (H5, reliable); no link was found for gender or for having phone service (H8, H10).

## Business framing

| measure | value |
|---|---|
| Customers | 7,043 |
| Churned customers | 1,869 |
| Churn rate (% of customers) | 26.5% |
| Total monthly revenue (all customers) | $456,117 |
| Monthly revenue of churned customers | $139,131 |
| Share of monthly revenue lost (% of total) | 30.5% |
| Annualised revenue of churned customers | $1,669,570 |
| Average monthly bill, churned | $74.44 |
| Average monthly bill, stayed | $61.27 |
| Median monthly bill, churned | $79.65 |
| Median monthly bill, stayed | $64.43 |
| Monthly revenue per 1 point of churn (70 customers x avg churned bill) | $5,243 per month ($62,915 per year) |

All money is monthly recurring revenue from `MonthlyCharges`. Margin, acquisition cost and lifetime value are not in the data, so they are not estimated.

## Ranked drivers (how strongly each column is linked to churn)

Cramér's V runs from 0 (no link) to 1 (perfect link). Under 0.1 is weak, 0.1 to 0.3 moderate, over 0.3 strong. Top three: Contract, InternetService, PaymentMethod. Gender and phone service are at or near zero.

| column | cramers_v | highest_rate_category | highest_rate_pct | lowest_rate_category | lowest_rate_pct |
|---|---|---|---|---|---|
| Contract | 0.41 | Month-to-month | 42.71 | Two year | 2.83 |
| InternetService | 0.32 | Fiber optic | 41.89 | No | 7.40 |
| PaymentMethod | 0.30 | Electronic check | 45.29 | Credit card (automatic) | 15.24 |
| PaperlessBilling | 0.19 | Yes | 33.57 | No | 16.33 |
| OnlineSecurity | 0.17 | No | 31.33 | Yes | 14.61 |
| TechSupport | 0.17 | No | 31.19 | Yes | 15.17 |
| Dependents | 0.16 | No | 31.28 | Yes | 15.45 |
| SeniorCitizen | 0.15 | 1 | 41.68 | 0 | 23.61 |
| Partner | 0.15 | No | 32.96 | Yes | 19.66 |
| OnlineBackup | 0.08 | No | 29.17 | Yes | 21.53 |
| DeviceProtection | 0.07 | No | 28.65 | Yes | 22.50 |
| StreamingTV | 0.06 | Yes | 30.07 | No | 24.33 |
| StreamingMovies | 0.06 | Yes | 29.94 | No | 24.38 |
| MultipleLines | 0.04 | Yes | 28.61 | No | 25.02 |
| PhoneService | 0.01 | Yes | 26.71 | No | 24.93 |
| gender | 0.01 | Female | 26.92 | Male | 26.16 |

Note: for the six add-on columns the table above includes customers with no internet in the "No" group, who rarely leave (7.4%). Chart 08 compares internet customers only, which is the fairer view.

## Where churn concentrates

Revenue lost per segment, riskiest first (segments under 100 customers are noisy):

| segment | customers | churn_rate_pct | share_of_base_pct | share_of_churners_pct | monthly_rev_lost_usd | share_of_rev_lost_pct |
|---|---|---|---|---|---|---|
| Month-to-month / Fiber optic / tenure 0-12 | 916 | 70.20 | 13.00 | 34.40 | 53,178.30 | 38.20 |
| Month-to-month / Fiber optic / tenure 13+ | 1,212 | 42.80 | 17.20 | 27.80 | 47,303.70 | 34.00 |
| Month-to-month / DSL / tenure 0-12 | 690 | 42.50 | 9.80 | 15.70 | 13,351.90 | 9.60 |
| One year / Fiber optic / tenure 0-12 | 7 | 28.60 | 0.10 | 0.10 | 201.20 | 0.10 |
| Month-to-month / No / tenure 0-12 | 388 | 22.70 | 5.50 | 4.70 | 1,771.20 | 1.30 |
| One year / Fiber optic / tenure 13+ | 532 | 19.20 | 7.60 | 5.50 | 10,370.80 | 7.50 |
| Month-to-month / DSL / tenure 13+ | 533 | 19.00 | 7.60 | 5.40 | 5,015.40 | 3.60 |
| One year / DSL / tenure 0-12 | 42 | 16.70 | 0.60 | 0.40 | 373.00 | 0.30 |
| One year / DSL / tenure 13+ | 528 | 8.70 | 7.50 | 2.50 | 2,983.30 | 2.10 |
| Month-to-month / No / tenure 13+ | 136 | 8.10 | 1.90 | 0.60 | 226.60 | 0.20 |
| Two year / Fiber optic / tenure 13+ | 429 | 7.20 | 6.10 | 1.70 | 3,246.10 | 2.30 |
| One year / No / tenure 0-12 | 75 | 5.30 | 1.10 | 0.20 | 78.70 | 0.10 |
| Two year / DSL / tenure 13+ | 610 | 2.00 | 8.70 | 0.60 | 805.70 | 0.60 |
| One year / No / tenure 13+ | 289 | 1.70 | 4.10 | 0.30 | 111.60 | 0.10 |
| Two year / No / tenure 13+ | 588 | 0.80 | 8.40 | 0.30 | 113.50 | 0.10 |
| Two year / DSL / tenure 0-12 | 18 | 0.00 | 0.30 | 0.00 | 0.00 | 0.00 |
| Two year / No / tenure 0-12 | 50 | 0.00 | 0.70 | 0.00 | 0.00 | 0.00 |

## Candidate groups for a first intervention

Counts are descriptive. "Monthly revenue lost" is the sum of monthly bills of the group's leavers.

| group | customers | share_of_base_pct | churn_rate_pct | churned | share_of_all_churners_pct | monthly_rev_lost_usd | share_of_lost_rev_pct |
|---|---|---|---|---|---|---|---|
| Month-to-month (any) | 3,875 | 55.00 | 42.70 | 1,655 | 88.60 | 120,847.10 | 86.90 |
| Month-to-month, first 12 months | 1,994 | 28.30 | 51.40 | 1,024 | 54.80 | 68,301.40 | 49.10 |
| Month-to-month on fiber | 2,128 | 30.20 | 54.60 | 1,162 | 62.20 | 100,482.00 | 72.20 |
| Month-to-month on fiber, first 12 months | 916 | 13.00 | 70.20 | 643 | 34.40 | 53,178.30 | 38.20 |
| Month-to-month, electronic check | 1,850 | 26.30 | 53.70 | 994 | 53.20 | 77,315.60 | 55.60 |
| Month-to-month, fiber, electronic check | 1,307 | 18.60 | 60.40 | 789 | 42.20 | 68,281.50 | 49.10 |
| Month-to-month, fiber, no tech support | 1,796 | 25.50 | 57.50 | 1,033 | 55.30 | 88,165.80 | 63.40 |

Reading it: the narrower the group, the higher its churn rate, but the fewer leavers it reaches. The group in finding 5 reaches 34% of leavers by contacting 13% of customers. Month-to-month customers in year one reach 55% of leavers by contacting 28%. Which is smaller-but-enough depends on offer cost and save rate, which this data does not contain.

## Charts

### `charts/01_target_customers_vs_revenue.png`
- **Shows:** Leavers are a bigger share of revenue than of customers.
- **Means for the business question:** 26.5% of customers left, taking 30.5% of monthly revenue. Leavers pay $74.44 a month on average against $61.27 for stayers.
- **How sure:** Sure of the arithmetic. The bill difference is reliable (H6).

### `charts/02_churn_rate_all_categories.png`
- **Shows:** Churn rate of every category of every column, sorted.
- **Means for the business question:** The spread is wide: from 3% to 45%. Contract, internet type and payment method hold the extremes. Gender and phone service sit on the average line.
- **How sure:** Every category has 300+ customers, so each rate is stable to about +/- 5 points.

### `charts/03_churn_by_contract.png`
- **Shows:** Churn rate by contract type.
- **Means for the business question:** Month-to-month 42.7%, one-year 11.3%, two-year 2.8%. Any retention budget starts with month-to-month customers (55% of base).
- **How sure:** High. Gap 36 points, 95% interval 34 to 38 (H1). Contracts are chosen by customers, so the gap is a link, not proof that a contract changes behaviour.

### `charts/04_churn_by_tenure.png`
- **Shows:** Churn rate by months with the company.
- **Means for the business question:** Falls from 53% to 10% as tenure grows. The first 6 months hold 42% of leavers. Early-life offers have the most customers to act on.
- **How sure:** High on size (H3: first 12 months 47% versus 17%). Unclear from this data whether tenure of leavers is measured at exit, which would make low-tenure leavers partly built in.

### `charts/05_churn_by_internet.png`
- **Shows:** Churn rate by internet type.
- **Means for the business question:** Fiber 41.9%, DSL 19.0%, no internet 7.4%. Fiber is 44% of customers and 69% of leavers.
- **How sure:** High (H2: gap 23 points). The data has no service-quality or price-history field, so why fiber leaves more is unclear from this data.

### `charts/06_churn_by_payment.png`
- **Shows:** Churn rate by payment method.
- **Means for the business question:** Electronic check 45.3%; the other three 15-19%. Automatic payers are the most loyal group.
- **How sure:** High (H4: gap 28 points). Payment method may stand in for contract or sign-up route; the two-way chart 12 checks contract only.

### `charts/07_churn_by_monthly_charge.png`
- **Shows:** Churn rate by monthly bill band.
- **Means for the business question:** Lowest under $30 (10%), highest at $70-90 (38%). The pattern is not a straight climb: $30-50 (31%) beats $50-70 (20%). The $70+ bands hold 81% of lost revenue.
- **How sure:** Medium. Leavers pay $15 more at the median (H6, reliable), but price overlaps with fiber and add-ons, so price on its own is unclear from this data.

### `charts/08_churn_by_addon.png`
- **Shows:** Churn with and without each add-on, internet customers only.
- **Means for the business question:** Security (15% versus 42%), tech support (15% versus 42%), backup and device protection show large gaps. Streaming add-ons show a much smaller gap (about 4 points). Customers with four protection add-ons leave at 5%; with none, 57%.
- **How sure:** High for tech support (H5: gap 26 points). Customers who choose add-ons may differ in other ways; unclear from this data whether adding one changes anything.

### `charts/10_heat_contract_by_internet.png`
- **Shows:** Churn by contract and internet type.
- **Means for the business question:** Month-to-month is highest in all three internet types (fiber 55%, DSL 32%, none 19%). Fiber and contract each add risk.
- **How sure:** High (H9: pooled odds ratio 8.2, 95% interval 7.0 to 9.6). All cells have 100+ customers.

### `charts/11_heat_tenure_by_contract.png`
- **Shows:** Churn by tenure band and contract.
- **Means for the business question:** Churn falls with tenure inside month-to-month (55% to 26%). Two-year contracts stay low at every age.
- **How sure:** Medium. 5 of 15 cells have under 100 customers (marked *), mostly long contracts in the first months. Read only the large cells.

### `charts/12_heat_payment_by_contract.png`
- **Shows:** Churn by payment method and contract.
- **Means for the business question:** Within month-to-month, electronic check 54% against about 33% for automatic payers. The payment gap is not just a contract effect.
- **How sure:** High on the month-to-month row (large cells). Unclear for other contracts where cells are smaller.

### `charts/13_heat_techsupport_by_internet.png`
- **Shows:** Churn by tech support and internet type, internet customers only.
- **Means for the business question:** Tech support goes with lower churn on DSL (10% versus 28%) and fiber (23% versus 49%).
- **How sure:** High. All four cells have 100+ customers.

### `charts/14_concentration_curve.png`
- **Shows:** Cumulative share of churn against customers, riskiest of 17 observed segments first.
- **Means for the business question:** The riskiest 20% of customers hold about 46% of leavers and 52% of lost revenue; the riskiest 30%, 62% and 72%. Churn is concentrated; broad programmes waste most of their budget.
- **How sure:** Medium. The ranking is built and read on the same customers, so the picture is slightly flattering; five tiny segments (under 100 customers) hold under 2% of customers.

### `charts/15_candidate_groups_revenue.png`
- **Shows:** Seven simple, targetable groups: share of customers against share of lost revenue.
- **Means for the business question:** Month-to-month on fiber in year one: 13% of customers, 38% of lost revenue. Every group on the chart takes a bigger share of loss than of customers.
- **How sure:** High on the counts (each group has 900+ customers). Whether an offer would keep these customers is not testable from this data.

### `charts/16_correlations.png`
- **Shows:** Correlation among numeric columns and with churn.
- **Means for the business question:** Tenure and TotalCharges move together (r = 0.83); MonthlyCharges and avg_monthly_spend are almost the same (r = 1.00); add-on counts overlap (r = 0.91). Tenure has the strongest link to churn (r = -0.35); the model builder should not use these overlapping columns together without care.
- **How sure:** High for the numbers; a correlation measures a straight-line link only.

### `charts/17_tenure_distribution.png`
- **Shows:** Tenure of leavers against stayers.
- **Means for the business question:** Leavers bunch at the start (median 10 months); stayers bunch at the far end.
- **How sure:** High on the shape. Whether leavers' tenure is recorded at exit is unclear from this data.

## What we did not find, and what we could not check

- No reliable link between gender and churn (26.9% versus 26.2%) or between phone service and churn (26.7% versus 24.9%).
- Causes: none. The data is one snapshot. "Customers with X leave more often" is as far as it goes.
- Time: no date column, so no trend, seasonality or "who left first". Unclear from this data.
- Tenure and TotalCharges for leavers may be measured at exit: could make them look more predictive than they are. Unclear from this data.
- Several columns at once: tables look at one or two columns. Nothing here separates their combined effects; that is for the model.
- Prices, discounts and service faults are not in the data.
- The data is IBM's fictional sample, so conclusions describe the data, not a real company.
- KKBox transactions were profiled only (no outcome label); nothing from them is in these findings.
