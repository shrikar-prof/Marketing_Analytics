# Hypotheses

Ten statements, written down before the group comparisons (see the pre-registration table in the notebook, section 5.1). Bar for reliable: p below 0.005 (5% divided by 10 tests) and a 95% interval that excludes zero (or 1 for odds ratios). These tests use the same data that suggested the ideas, so they are not independent confirmation.

## Pre-registered plan (fixed before the results)

| id | statement | predicted_direction | test | effect_size_and_why |
|---|---|---|---|---|
| H1 | Month-to-month leave more often than 1-2 year contracts | month-to-month higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Phi (0 to 1; about 0.1 small, 0.3 medium) can be compared across tests; points are what a manager can price. |
| H2 | Fiber-optic leave more often than DSL | fiber higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H1. |
| H3 | First 12 months leave more often than longer tenure | first-year higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H1. |
| H4 | Electronic-check payers leave more often than others | e-check higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H1. |
| H5 | Internet customers without tech support leave more often than with | no tech support higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H1. |
| H6 | Leavers pay a higher monthly bill than stayers | churners pay more | Mann-Whitney test + bootstrap interval on the gap in medians | common-language effect (chance a random leaver pays more than a random stayer; 50% = no difference). It needs no assumption about the shape of bills and reads as a plain chance. |
| H7 | Senior citizens leave more often than others | seniors higher | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H1. |
| H8 | Men and women leave at different rates | no difference expected | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. A phi near 0 shows how small the gap is, not only that it is unreliable. |
| H9 | Month-to-month penalty holds inside every internet type | holds in DSL, fiber, no internet | Mantel-Haenszel pooled test across internet types | pooled odds ratio (odds = leavers divided by stayers; ratio = month-to-month odds over longer-contract odds; 1 = no effect). One number that summarises the contract effect across the three internet types. |
| H10 | Phone service changes the churn rate | no difference expected | chi-square on two groups + bootstrap 95% interval on the gap | phi, plus the gap in points. Same reason as H8. |

Odds = leavers divided by stayers in a group. Odds ratio = odds in one group divided by odds in another. Stratum = one slice held fixed (one internet type). phi = strength of a 2-group link, 0 to 1.

## Scorecard

| id | statement | prediction | result_vs_prediction | reliable |
|---|---|---|---|---|
| H1 | Month-to-month leave more often than 1-2 year contracts | month-to-month higher | matches | yes |
| H2 | Fiber-optic leave more often than DSL | fiber higher | matches | yes |
| H3 | First 12 months leave more often than longer tenure | first-year higher | matches | yes |
| H4 | Electronic-check payers leave more often than others | e-check higher | matches | yes |
| H5 | Internet customers without tech support leave more often than with | no tech support higher | matches | yes |
| H6 | Leavers pay a higher monthly bill than stayers | churners pay more | matches | yes |
| H7 | Senior citizens leave more often than others | seniors higher | matches | yes |
| H8 | Men and women leave at different rates | no difference expected | matches | no |
| H9 | Month-to-month penalty holds inside every internet type | holds in DSL, fiber, no internet | matches | yes |
| H10 | Phone service changes the churn rate | no difference expected | matches | no |

**8 of 10 statements are reliable. Not supported by the data: H8, H10.**

## Detail

### H1. Month-to-month leave more often than 1-2 year contracts

- **Predicted:** month-to-month higher. Result matches the prediction.
- **Evidence seen:** Month-to-month: 42.7% left (3,875 customers). 1- or 2-year contract: 6.8% left (3,168 customers).
- **Size of effect:** Gap +36.0 points (95% interval +34.2 to +37.8); +360 extra leavers per 1,000 customers; phi (effect size) 0.41. If group A left at B's rate, about $101,734 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Contract terms that were assigned (not chosen) by customers, or a second quarter of data showing the gap shrinking.

### H2. Fiber-optic leave more often than DSL

- **Predicted:** fiber higher. Result matches the prediction.
- **Evidence seen:** Fiber optic: 41.9% left (3,096 customers). DSL: 19.0% left (2,421 customers).
- **Size of effect:** Gap +22.9 points (95% interval +20.5 to +25.2); +229 extra leavers per 1,000 customers; phi (effect size) 0.24. If group A left at B's rate, about $62,572 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Evidence that fiber customers differ in price or tenure in a way not captured here; the price gap is checked in section 6 but not removed.

### H3. First 12 months leave more often than longer tenure

- **Predicted:** first-year higher. Result matches the prediction.
- **Evidence seen:** Tenure 0-12 months: 47.4% left (2,186 customers). Tenure 13+ months: 17.1% left (4,857 customers).
- **Size of effect:** Gap +30.3 points (95% interval +27.9 to +32.6); +303 extra leavers per 1,000 customers; phi (effect size) 0.32. If group A left at B's rate, about $44,055 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Knowing whether tenure for leavers is measured at exit. If so, tenure partly reflects the outcome. Unclear from this data.

### H4. Electronic-check payers leave more often than others

- **Predicted:** e-check higher. Result matches the prediction.
- **Evidence seen:** Electronic check: 45.3% left (2,365 customers). Other payment: 17.1% left (4,678 customers).
- **Size of effect:** Gap +28.2 points (95% interval +25.9 to +30.5); +282 extra leavers per 1,000 customers; phi (effect size) 0.30. If group A left at B's rate, about $52,538 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Evidence that payment method is simply a stand-in for how customers were signed up. Unclear from this data.

### H5. Internet customers without tech support leave more often than with

- **Predicted:** no tech support higher. Result matches the prediction.
- **Evidence seen:** No tech support (internet customers): 41.6% left (3,473 customers). Has tech support (internet customers): 15.2% left (2,044 customers).
- **Size of effect:** Gap +26.5 points (95% interval +24.3 to +28.8); +265 extra leavers per 1,000 customers; phi (effect size) 0.27. If group A left at B's rate, about $70,382 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** A check that tech support was bought before, not after, the customer decided to stay. Unclear from this data.

### H6. Leavers pay a higher monthly bill than stayers

- **Predicted:** churners pay more. Result matches the prediction.
- **Evidence seen:** Median monthly bill is $79.65 for the 1,869 customers who left and $64.43 for the 5,174 who stayed.
- **Size of effect:** Gap in medians: $15.22 per month (95% interval $13.90 to $17.90). A random leaver pays more than a random stayer 62% of the time (50% would mean no difference).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Comparing like-for-like plans: leavers may pay more because they are mostly on fiber. Section 6.5 and H9 show overlap exists.

### H7. Senior citizens leave more often than others

- **Predicted:** seniors higher. Result matches the prediction.
- **Evidence seen:** Senior citizen: 41.7% left (1,142 customers). Not senior: 23.6% left (5,901 customers).
- **Size of effect:** Gap +18.1 points (95% interval +14.9 to +21.2); +181 extra leavers per 1,000 customers; phi (effect size) 0.15. If group A left at B's rate, about $16,661 of monthly revenue would stay (an upper bound, not a forecast).
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** Controlling for contract and tenure. We did not adjust, so some of the senior gap may come from other columns.

### H8. Men and women leave at different rates

- **Predicted:** no difference expected. Result matches the prediction.
- **Evidence seen:** Female: 26.9% left (3,488 customers). Male: 26.2% left (3,555 customers).
- **Size of effect:** Gap +0.8 points (95% interval -1.3 to +2.8); +8 extra leavers per 1,000 customers; phi (effect size) 0.01. No reliable gap, so no revenue effect is claimed.
- **Reliability:** Not reliable: no difference that luck could not explain was found (this is not proof that the groups are equal). p-value 0.4698, against the pre-set bar of 0.005.
- **What would change the conclusion:** A larger sample. With 7,043 customers we could detect a gap of about 3 points; a smaller gap would be invisible.

### H9. Month-to-month penalty holds inside every internet type

- **Predicted:** holds in DSL, fiber, no internet. Result matches the prediction.
- **Evidence seen:** Month-to-month versus longer contracts, churn rate by internet type: DSL 32% vs 5%; Fiber optic 55% vs 14%; No 19% vs 1%.
- **Size of effect:** Pooled odds ratio 8.2 (95% interval 7.0 to 9.6): the odds of leaving are about 8 times higher on month-to-month, after holding internet type fixed. Gap in points per type: DSL +27, Fiber optic +41, No +18.
- **Reliability:** Reliable: the data supports this statement. p-value below 0.0001, against the pre-set bar of 0.005.
- **What would change the conclusion:** A fourth internet type, or a stratum where month-to-month customers were chosen differently.

### H10. Phone service changes the churn rate

- **Predicted:** no difference expected. Result matches the prediction.
- **Evidence seen:** Has phone service: 26.7% left (6,361 customers). No phone service: 24.9% left (682 customers).
- **Size of effect:** Gap +1.8 points (95% interval -1.8 to +5.1); +18 extra leavers per 1,000 customers; phi (effect size) 0.01. No reliable gap, so no revenue effect is claimed.
- **Reliability:** Not reliable: no difference that luck could not explain was found (this is not proof that the groups are equal). p-value 0.3162, against the pre-set bar of 0.005.
- **What would change the conclusion:** A larger sample or a split of phone-only customers (only 682 have no phone service).

## Group-comparison table

| id | group_a | group_b | n_a | n_b | rate_a_pct | rate_b_pct | gap_pp | ci_95 | p | phi | reliable |
|---|---|---|---|---|---|---|---|---|---|---|---|
| H1 | Month-to-month | 1- or 2-year contract | 3,875 | 3,168 | 42.70 | 6.80 | 36.00 | 34.2 to 37.8 | below 0.0001 | 0.41 | 1 |
| H2 | Fiber optic | DSL | 3,096 | 2,421 | 41.90 | 19.00 | 22.90 | 20.5 to 25.2 | below 0.0001 | 0.24 | 1 |
| H3 | Tenure 0-12 months | Tenure 13+ months | 2,186 | 4,857 | 47.40 | 17.10 | 30.30 | 27.9 to 32.6 | below 0.0001 | 0.32 | 1 |
| H4 | Electronic check | Other payment | 2,365 | 4,678 | 45.30 | 17.10 | 28.20 | 25.9 to 30.5 | below 0.0001 | 0.30 | 1 |
| H5 | No tech support (internet customers) | Has tech support (internet customers) | 3,473 | 2,044 | 41.60 | 15.20 | 26.50 | 24.3 to 28.8 | below 0.0001 | 0.27 | 1 |
| H7 | Senior citizen | Not senior | 1,142 | 5,901 | 41.70 | 23.60 | 18.10 | 14.9 to 21.2 | below 0.0001 | 0.15 | 1 |
| H8 | Female | Male | 3,488 | 3,555 | 26.90 | 26.20 | 0.80 | -1.3 to 2.8 | 0.4698 | 0.01 | 0 |
| H10 | Has phone service | No phone service | 6,361 | 682 | 26.70 | 24.90 | 1.80 | -1.8 to 5.1 | 0.3162 | 0.01 | 0 |

Not checked: any adjustment for several columns at once, any time effect (the data is one snapshot), any cause.
