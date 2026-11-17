# Notebook Review Log

## 01_exploration

### Review 1 (first pass)
**Verdict: FIX — 6 gaps**

1. Cells 62–66 (H1–H5 test execution) — no markdown immediately before any test cell; null hypotheses, Mann-Whitney rationale, rank-biserial formula, and reading guide absent.
2. Cell 24 (baseline rule-of-thumb) — no immediate pre-cell markdown; missing formula, alternatives, and decision rule.
3. Cell 23 (price join) — no immediate pre-cell markdown; missing revenue formula, rationale for latest price, and rejection of median price.
4. data_dictionary.md — six derived columns (zero_rate, nonzero_mean, cv_nonzero, total_revenue_approx, log_price, log_mean_demand) absent from the derived-columns table.
5. data_dictionary.md — five existing derived-column rows missing "expected direction" and "motivating finding/hypothesis" columns.
6. Cell 48 markdown (price-elasticity) — Pearson r effect-size scale not defined.

**Fix round applied by data-explorer. All 6 gaps addressed. Notebook re-executed: 77 cells, 0 errors.**

---

### Review 2 (post-fix pass)
**Verdict: FIX — 5 gaps remaining (proceeding per command rule)**

1. Cells [66]–[69] (H2–H5 tests) — shared methodology cell [64] covers only H1; cells [66]–[69] still lack an immediate pre-cell markdown each.
2. Cells [65]–[69] — no post-cell markdown after any individual hypothesis test stating direction and practical meaning.
3. Cell [26] pre-cell markdown — "Why this method" missing connection to data properties established in sections 7a–7c.
4. Cell [26] pre-cell markdown — "How to read the output" section absent.
5. Cell [24] — post-cell markdown missing to interpret $195M revenue output.

**No further fix round applied (max one fix round per stage). Proceeding to model-builder.**

---

## 02_feature_engineering and 03_modeling

### Pass 1 (model-builder first submission)

**Verdict: FIX — 13 gaps**

1. NB03 cells 25–27 (final evaluation) — missing all four parts before per-category RMSE, per-series RMSSE, and decile lift cells.
2. NB03 cell 12 (family comparison loop) — LightGBM default section header 2 cells away from first comparison code cell.
3. NB03 cell 9 (baselines) — missing post-output markdown explaining what 2.26 (RoT) and 2.66 (Lag7) mean.
4. NB03 cells 16/19 (Optuna plot cells for LGB and XGB) — no immediate pre-markdown before each plot cell.
5. NB03 cell 22 (model selection) — missing post-output verdict markdown explaining why LightGBM was selected.
6. NB02 cell 21 (SNAP feature) — missing post-output markdown for the SNAP lift output.
7. NB02 cell 18 (price-ratio chart) — no markdown immediately before chart code.
8. NB02 cell 31 (Pearson r) — missing alternatives (Spearman rank, mutual information).
9. NB02 cell 26 (encode_categoricals) — missing "how to read the output" (Part 4).
10. NB03 cell 6 (price imputation) — imputation explanation too thin; missing alternatives.
11. NB03 cells 30–31 (SHAP + driver classification) — no pre or post markdown.
12. NB03 cell 33 (counterfactual plot) — no pre or post markdown.
13. NB02 cell 11 (melt step) — markdown too thin; no alternatives; no row-count formula.

All 13 gaps sent to model-builder for fix. Both notebooks re-executed with 0 errors after fix.

| Notebook | Cells total | Code cells ran | Errors |
|---|---|---|---|
| 02_feature_engineering.ipynb | 40 | 17 | 0 |
| 03_modeling.ipynb | 49 | 27 | 0 |

Optuna studies loaded from saved DB (no re-tuning); all numbers identical.

---

### Pass 2 (after model-builder fix round)

**Verdict: FIX — 5 gaps remaining**

1. NB03 Cell 16 (Optuna section header) — XGBoost search space table (7 parameters, ranges, reasons) entirely absent; only LightGBM search space documented.
2. NB03 Cell 21 (xgb_objective code) — no markdown cell immediately before it; XGBoost-specific rationale missing.
3. NB02 Cell 18 (price-ratio diagnostic) — markdown present for Part 4 only; Parts 1 (why binned bar), 2 (alternatives: scatter, Spearman), and 3 (how pd.cut works) all absent.
4. NB03 Cell 32 (RMSSE per series code) — no immediate pre-markdown (Cell 31 is code; Cell 30 covers it but is not adjacent).
5. NB03 Cell 33 (decile table code) — no immediate pre-markdown (Cell 32 is code).

**Max fix rounds reached (one fix round per stage). Proceeding to ml-statistician with 5 gaps noted.**
