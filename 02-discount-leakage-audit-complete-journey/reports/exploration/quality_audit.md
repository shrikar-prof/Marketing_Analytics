# Quality Audit

| Check | Count | Action taken |
|---|---|---|
| Duplicate transaction rows | 0 | Drop if any |
| Zero sales_value lines | 11,226 | Exclude (returns/voids) |
| Negative sales_value lines | 0 | Exclude (returns/voids) |
| Zero quantity lines | 8,869 | Exclude |
| Negative retail_disc | 0 | Flag if any; none expected by design |
| Negative coupon_disc | 0 | Flag if any; none expected by design |
| Negative coupon_match_disc | 0 | Flag if any; none expected by design |
| FUEL department lines | 12,997 | Flag; exclude from per-unit analyses |
| Transaction product_ids missing from products table | 17 | Will have null dept/category after join |
| Households missing from demographics | 1,668 | Demographics optional; does not affect leakage calc |
| Week range (min=1, max=53) | 53 | Confirm 52 weeks expected |

## Notes

- All discount fields are positive numbers per the data guide — no sign correction needed.

- FUEL lines are retained but flagged; excluded from per-unit analyses.

- Zero and negative sales_value lines are returns/voids; excluded from leakage analysis.
