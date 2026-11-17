# Feature Table — Discount Leakage Audit

| Feature | Meaning | Source columns | Type | Motivation |
|---|---|---|---|---|
| `is_national` | 1 if National brand, 0 if Private/Unknown | `brand` | binary | Finding 4 / H3 — brand type affects retailer vs manufacturer funding |
| `week_sin` | sin(2π·week/52) — cyclical week position | `week` | continuous | H7 — seasonal promotional activity; avoids discontinuity at week 52→1 |
| `week_cos` | cos(2π·week/52) — cyclical week position | `week` | continuous | H7 — paired with week_sin to fully encode circular week position |
| `quarter` | (week−1)//13, range 0–3 | `week` | ordinal | Quarterly promotional budget cycles; coarser but lower-variance than week |
| `is_top3_dept` | 1 if department in {TOYS, MEAT, SEAFOOD-PCKGD} | `department` | binary | Finding 2 / H4 — top-3 depts have 0.138 higher median disc_rate |
| `log_quantity` | log(1 + quantity) | `quantity` | continuous | Volume-discount tiers; log compresses right tail |
| `department` | Broad merchandise department (32 levels) | `department` | categorical | Finding 2 — primary driver; target-encoded in pipeline |
| `product_category` | Mid-level category (~303 levels) | `product_category` | categorical | Category-level promotional patterns; target-encoded in pipeline |
| `product_type` | Fine-grained type (~2378 levels) | `product_type` | categorical | SKU-level leakage patterns; target-encoded in pipeline |
| `store_id` | Store identifier (437 levels) | `store_id` | categorical | Store-specific promotional aggressiveness; target-encoded in pipeline |
