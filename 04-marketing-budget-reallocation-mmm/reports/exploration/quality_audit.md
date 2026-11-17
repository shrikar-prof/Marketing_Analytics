# Quality Audit

| File | Issue | Rows affected | Action taken |
|------|-------|--------------|--------------|
| robyn | string 'na' in events column | 206 | recode to 0; non-na → 1 |
| robyn | zero or negative revenue | 0 | none — all positive |
| robyn | duplicate rows | 0 | none found |
| geo_media | duplicate rows | 0 | none found |
| meridian | geo sum vs national revenue match | 156 | avg pct diff = 0.08% — acceptable (rounding) |
| robyn | facebook_S / facebook_I correlation = 0.991 | 0 | keep spend; drop impressions for modelling |
| robyn | search_S / search_clicks_P correlation = 0.983 | 0 | keep spend; drop clicks for modelling |