# Notebook review log

## 01_exploration

### Pass 1

**Verdict: FIX — 10 gaps**

1. Cell 37 (hypothesis tests) — Alternatives considered missing for Mann-Whitney U and Spearman ρ.
2. Cell 37 (hypothesis tests) — Null hypotheses absent; U-statistic and ρ formulas missing.
3. Cell 25 (scatter/LOWESS charts) — Cell 24 missing alternatives, LOWESS formula, and how-to-read.
4. Cell 27 (ROI calculation) — No preceding markdown; all four parts missing.
5. Cell 28 (correlation matrix) — No preceding markdown; Pearson formula and collinearity guidance absent.
6. Cells 30–34 (Charts 5–9) — No preceding markdown for any of these five cells.
7. Cells 20–22 (revenue stats and charts) — Cell 19 missing alternatives, CV formula, and how-to-read.
8. Cell 12 (QA audit) — Cell 11 missing alternatives, decision rule, and how-to-read.
9. Cell 16 (derived columns) — Missing code expression, example rows, and expected direction per column.
10. data_dictionary.md derived columns — Missing python_expr, example, expected_direction, and hypothesis for all five rows.

All 10 gaps sent to data-explorer for fix. Notebook re-executed with 0 errors (53 cells: 26 code, 27 markdown).

---

### Pass 2 (after data-explorer fix round)

**Verdict: FIX — 7 gaps remaining**

1. Cells 21–22 (Charts 1–2) — No preceding markdown; all four parts missing for revenue-over-time and channel-spend-mix charts.
2. Cell 16 (cleaning code) — Cell 15 names zero alternative cleaning approaches; standard requires at least two.
3. Cells 32, 34, 36, 38, 40 (preambles for Charts 5–9) — Only one alternative named in each; standard requires at least two.
4. Cells 32, 34, 36, 38, 40 — "How it works" (Part 3) absent in all five preambles; formulas missing (quintile threshold rule, IQR whisker formula, cumulative-sum formula for Lorenz curve, etc.).
5. Cell 46 (post-hypothesis markdown) — Summary labels H1 and H2 "Reliable" but computed output shows "UNCLEAR" for both; must match actual verdicts.
6. hypotheses.md — H6 verdict "RELIABLE" in table contradicts "no reliable correlation" in plain-language section; needs reconciliation.
7. Cell 28 (ROI cell) — No post-output markdown after the ROI results cell.

**Max fix rounds reached (one fix round per stage). Proceeding to model-builder with 7 gaps noted.**

---

## 02_feature_engineering and 03_modeling

### Pass 1

**Verdict: FIX — 11 gaps**

1. NB03 cell 18 (Optuna header) — Search space with reasons for each parameter absent from notebook markdown (only in tuning.md).
2. NB03 cells 31–35 (segment eval, decile lift, threshold table, calibration plot, decile chart) — No preceding markdown for any of these five sub-steps.
3. NB02 cells 12, 15, 18, 21, 24 (adstock, Hill, log, print flag, Fourier) — Part 2 (Alternatives) absent from all five pre-cell markdowns.
4. NB03 cells 39–43 (SHAP, driver classification, counterfactuals, response curves) — No markdown immediately before cells 42 and 43.
5. NB03 cell 28 (final model build) — No preceding markdown; all four parts missing.
6. NB03 cells 29–30 (final evaluation) — Part 2 (alternatives) and Part 3 (metric formulas) absent.
7. NB03 cell 12 (Ridge baseline) — Covering markdown not immediately adjacent; baseline and Ridge share one markdown.
8. NB02 cell 8 (validation split) — Part 4 (how to read output) absent.
9. NB02 cell 27 (distribution check chart) — Parts 2 and 3 absent from pre-cell markdown.
10. NB03 cell 16 (model comparison bar chart) — No markdown immediately before chart cell.
11. NB03 cell 26 (model selection table) — Part 4 absent.

All 11 gaps sent to model-builder for fix. Both notebooks re-executed with 0 errors (NB02: 11 code cells; NB03: 31 code cells). Optuna studies loaded from saved DB; no re-tuning.

---

### Pass 2 (after model-builder fix round)

**Verdict: FIX — 1 gap remaining**

1. NB03 cell 49 (response curves code) — Markdown 48 covers Parts 3 and 4 only; missing Part 1 (why response curves for MMM budget allocation) and Part 2 (alternatives: partial dependence plots, ICE plots, Shapley interaction values).

**Max fix rounds reached (one fix round per stage). Proceeding to ml-statistician with 1 gap noted.**
