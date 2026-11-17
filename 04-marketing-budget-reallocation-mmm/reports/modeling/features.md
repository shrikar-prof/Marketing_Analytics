# Feature Table — MMM Budget Reallocation

| Feature | Business meaning | Source columns | Type | Why it exists |
|---------|-----------------|----------------|------|---------------|
| tv_S_sat | TV Hill saturation (0–1) | tv_S, tv_S_adstock | float [0,1] | Adstock+Hill; Pitfall 1&2 in handoff |
| ooh_S_sat | Out-of-home Hill saturation (0–1) | ooh_S, ooh_S_adstock | float [0,1] | Adstock+Hill; Pitfall 1&2 |
| print_S_sat | Print Hill saturation (0–1) | print_S, print_S_adstock | float [0,1] | Adstock+Hill; Pitfall 1&2 |
| facebook_S_sat | Facebook Hill saturation (0–1) | facebook_S, facebook_S_adstock | float [0,1] | Adstock+Hill; Pitfall 1&2 |
| search_S_sat | Search Hill saturation (0–1) | search_S, search_S_adstock | float [0,1] | Adstock+Hill; Pitfall 1&2 |
| tv_S_log | log(1+TV spend) | tv_S | float | Log linearises spend-revenue curve for Ridge; Pitfall 2 |
| ooh_S_log | log(1+OOH spend) | ooh_S | float | Same as tv_S_log motivation |
| print_S_log | log(1+print spend) | print_S | float | Same; also compresses zero weeks |
| facebook_S_log | log(1+Facebook spend) | facebook_S | float | Same |
| search_S_log | log(1+search spend) | search_S | float | Same |
| newsletter_log | log(1+newsletter sends) | newsletter | float | Handoff: newsletter is a marketing lever |
| competitor_sales_log | log(1+competitor sales index) | competitor_sales_B | float | Handoff: control for market-level demand; Pitfall 3 |
| event_flag | Binary: 1 in event weeks | events | int {0,1} | Handoff: 15 event weeks; Pitfall 4 |
| total_spend_log | log(1+sum of all 5 channel spends) | tv_S…search_S | float | Budget constraint proxy; H4 from exploration |
| print_low_flag | 1 if print spend ≤ 5th pct of training | print_S | int {0,1} | Handoff Pitfall 5: unstable ROI at near-zero print |
| trend | Normalised time index [0,1] | DATE row order | float | Handoff Pitfall 3: mild upward revenue trend |
| sin_1 | Fourier sin, order 1 (annual) | DATE row order | float [-1,1] | Annual seasonality; period=52 weeks |
| cos_1 | Fourier cos, order 1 (annual) | DATE row order | float [-1,1] | Annual seasonality |
| sin_2 | Fourier sin, order 2 (semi-annual) | DATE row order | float [-1,1] | Semi-annual harmonic of seasonality |
| cos_2 | Fourier cos, order 2 (semi-annual) | DATE row order | float [-1,1] | Semi-annual harmonic |
| tv_S_adstock | TV adstock (decay=0.40) | tv_S | float | Intermediate; used in tv_S_sat |
| ooh_S_adstock | OOH adstock (decay=0.30) | ooh_S | float | Intermediate; used in ooh_S_sat |
| print_S_adstock | Print adstock (decay=0.20) | print_S | float | Intermediate |
| facebook_S_adstock | Facebook adstock (decay=0.10) | facebook_S | float | Intermediate |
| search_S_adstock | Search adstock (decay=0.05) | search_S | float | Intermediate |