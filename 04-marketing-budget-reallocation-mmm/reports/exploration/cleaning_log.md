# Cleaning Log

| Dataset | Rule | Rows before | Rows affected | Rows after |
|---------|------|------------|--------------|-----------|
| robyn | events 'na'→0, other→1 (event_flag) | 208 | 2 | 208 |
| robyn | sort by DATE | 208 | 208 | 208 |
| meridian_geo | revenue = conversions × revenue_per_conversion | 3,120 | 3,120 | 3,120 |
| meridian_geo | add total_spend = sum of Channel*_spend | 3,120 | 3,120 | 3,120 |