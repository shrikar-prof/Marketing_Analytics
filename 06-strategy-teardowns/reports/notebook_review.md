# Notebook review log

## 01_exploration

### Pass 1

**Verdict: FIX — 8 gaps**

1. Cell 53 (before hypothesis test cells 54–55) — H₀ for each of H1–H6 never stated in explicit null form in a markdown cell.
2. Cell 53 (before cells 54–55) — "Alternatives considered" and "How it works" absent for statistical methods; Spearman/Mann-Whitney formulas and effect-size scale missing.
3. Cells 29, 32, 38, 44, 47, 50 (before chart cells 30, 33, 39, 45, 48, 51) — "Alternatives considered" absent from six chart explanation cells.
4. Cell 35 (before cell 36, arm_usd chart) — "How it works" and "How to read it" absent; ARM formula missing.
5. Cell 41 (before cell 42, net_new_stores vs comp_sales_pct) — "How it works" absent; comparable sales definition missing.
6. hypotheses.md — "interval method" column missing; no confidence intervals beside any p-value or effect size.
7. Cell 19 (before cell 20, derived columns) — "Alternatives considered" and "How to read the output" absent.
8. Cell 14 (before quality-audit cells 15–16) — "How it works," "Alternatives considered," and "How to read the output" all absent.

All 8 gaps sent to data-explorer for fix. Notebook re-executed with 0 errors (65 cells: 27 code executed).

---

### Pass 2 (after data-explorer fix round)

**Verdict: FIX — 3 gaps remaining**

1. Cell 19 (before cell 20, derived columns) — "How it works" subsection still absent; formulas for op_margin_pct, rev_per_store_m, rev_yoy_pct, covid_affected not in markdown (only in code comments).
2. Cell 55 (H1–H6 test execution) — No markdown cell immediately before cell 55; cell 53 is separated by code cell 54.
3. data_dictionary.md derived columns table — Missing "hypothesis" column, "expected_direction" column, and name mismatch: `rev_per_store` vs `rev_per_store_m` in code.

**Max fix rounds reached (one fix round per stage). Proceeding to model-builder with 3 gaps noted.**

---

## 02_feature_engineering and 03_modeling

### Pass 1 (before model-builder fix round)

**Verdict: FIX — 12 gaps**

1. NB02 Cell [6] — Feature explanation cells [8]–[11] appear after the code, not before; no alternatives block for overall feature-set design.
2. NB03 Cell [15] — Cell [14] is one sentence; missing full 4-part markdown for LOOCV predictions assembly.
3. NB03 Cells [30], [31], [32] — Three final evaluation chart cells have no preceding explanatory markdown.
4. NB02 Cell [23] — No pre-cell markdown for Netflix distribution/correlation analysis.
5. NB03 Cell [23] — Cell [22] missing alternatives (single OLS refit, rolling-window), walk-forward algorithm, and held-out n=1 limitations.
6. NB03 Cell [26] — Cell [25] missing ARIMA/Holt-Winters/mean-lag alternatives, walk-forward algorithm for membership, coefficient-sign interpretation.
7. NB03 Cells [12], [20] — Normal equations, R² definition, t-test H0 formula, and column-reading guide missing from pre-cell markdown; Parts 3 and 4 only in post-output cells.
8. Post-output cells [10], [18] in NB03 and [14], [24] in NB02 — State expectations, not actual findings (e.g., expansion_rate r=+0.02 null not stated).
9. NB02 Cells [13], [26] — Cell [12] one sentence; cell [25] missing alternatives and Part 4 for split assignment.
10. features.md — Example row missing for 11 of 13 features.
11. No hypothesis pre-registration table in either notebook.
12. NB03 Cell [34] — No post-output interpretation of negative ARM coefficient (−$68.6M/quarter) collinearity artifact.

All 12 gaps sent to model-builder for fix. Both notebooks re-executed with 0 errors (NB02: 34 cells, 9 executed; NB03: 51 cells, 20 executed).

---

### Pass 2 (after model-builder fix round)

**Verdict: FIX — 7 gaps remaining**

1. NB03 Cell [30] — Parts 1–4 all absent; preceding cell [29] is a one-line section header only.
2. NB02 Cell [23] — Part 2 (alternatives for Netflix feature set) missing; no "Why these features, not others" block equivalent to Five Below.
3. NB02 Cell [23] — Part 4 (how to read the output) missing before code cell; expected shape, NaN rows, typical value ranges absent.
4. NB03 Cell [27] post-output — Cell [28] asks a question rather than stating what the comparison table output shows.
5. NB03 Cell [16] — No post-output markdown stating comp MAE result vs threshold and what it means.
6. NB03 Cell [24] post-output — Cell [25] never states the actual held-out test MAE ($88.2M).
7. NB02 Cell [12] — Cell [11] missing Part 4 (how to read the output: expected shape, NaN pattern, value ranges).

**Max fix rounds reached (one fix round per stage). Proceeding to ml-statistician with 7 gaps noted.**
