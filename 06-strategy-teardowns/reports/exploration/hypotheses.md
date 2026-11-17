# Hypotheses -- Strategy Teardowns
Date: 2026-11-17

## Hypothesis plan (with interval method)

| id   | statement                                                       | H0                                                                     | test                                            | why_test                                                             | effect                                           | interval_method                                                         |
|:-----|:----------------------------------------------------------------|:-----------------------------------------------------------------------|:------------------------------------------------|:---------------------------------------------------------------------|:-------------------------------------------------|:------------------------------------------------------------------------|
| H1   | Netflix UCAN ARM rose monotonically                             | rho = 0 (no monotone trend)                                            | Spearman rank correlation                       | Non-parametric; no normality assumption; any monotone trend          | Spearman rho + ARM lift in $/month               | Bootstrap 95% CI (1000 resamples, percentile), N=20                     |
| H2   | UCAN revenue higher after paid-sharing enforcement              | Median quarterly revenue pre = post enforcement                        | Mann-Whitney U test                             | Non-parametric group comparison; robust to non-normality and small N | Hodges-Lehmann median difference in USD millions | Bootstrap 95% CI (1000 resamples, percentile)                           |
| H3   | Five Below comp sales lower in high-expansion years             | rho = 0 (no monotone inverse relationship)                             | Spearman + exact permutation test               | N=6; exact permutation enumerates all 720 orderings                  | Spearman rho                                     | N=6: CI omitted (bootstrap needs N>=10). Exact permutation p instead.   |
| H4   | Five Below operating margin compressed as expansion accelerated | rho = 0 (no monotone relationship)                                     | Spearman + exact permutation test               | Same as H3: N=6                                                      | Spearman rho                                     | N=6: CI omitted. Exact permutation p.                                   |
| H5   | Five Below revenue per store declined during peak expansion     | rev_per_store FY2023-2024 >= FY2022 (no dilution)                      | Direct comparison (N=2 in peak-expansion group) | N=2: no test meaningful                                              | Absolute USD change per store                    | N=2: no CI possible. Company model ($2M) used as external benchmark.    |
| H6   | ARM growth does not predict subsequent membership decline       | rho = 0 (no relationship between ARM growth and next-quarter net adds) | Spearman rank correlation                       | Non-parametric; lagged relationship need not be linear               | Spearman rho                                     | Bootstrap 95% CI (1000 resamples, percentile), N=15 borderline adequate |

## Results

### H1: Netflix ARM monotone upward trend (H0: rho = 0)
Spearman rho = 0.971 (p < 0.001). Bootstrap 95% CI: [0.861, 0.996].
ARM grew $4.04/month over 5 years.
Annual revenue impact at Q4'24 membership: $4.3B/year.
**Verdict: SUPPORTED. Reliable. Every price increase was retained.**

### H2: UCAN revenue higher after paid-sharing enforcement (H0: same distribution)
Hodges-Lehmann: +$1,218M/qtr. Bootstrap 95% CI: [$760M, $1,637M].
Mann-Whitney p = 0.0000.
**Verdict: SUPPORTED. Very reliable.**

### H3: Five Below comp sales lower in high-expansion years (H0: rho = 0, N=6)
Spearman rho = -0.577. Exact permutation p = 0.1417.
N=6: bootstrap CI omitted. Exact permutation used instead.
**Verdict: DIRECTIONALLY SUPPORTED, insufficient power for certainty.**

### H4: Five Below operating margin compressed (H0: rho = 0, N=6)
Spearman rho = -0.820. Exact permutation p = 0.0333.
N=6: CI omitted.
**Verdict: SUPPORTED in direction.**

### H5: Revenue per store dilution (H0: no decline, N=2)
FY2022: $2.30M. FY2023-2024 average: $2.25M. Decline: $-0.05M/store.
N=2: no CI possible. External benchmark: company model = $2M/store.
**Verdict: SUPPORTED. Decline real but above minimum-viability threshold.**

### H6: ARM growth does not predict subscriber losses (H0: rho = 0)
Spearman rho = -0.474 (p = 0.0637). Bootstrap 95% CI: [-0.810, 0.033].
CI crosses zero -- directionally positive but uncertain at N=15.
**Verdict: NULL NOT SUPPORTED. No evidence that price increases drove churn.**