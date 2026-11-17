# Notebook review log

## 01_exploration

### Pass 1

**Verdict: FIX — 11 gaps**

1. Cells 49–53 (H2–H6) — No markdown immediately before any hypothesis test cell; all four parts missing.
2. Cell 48 (H1) — Preceding markdown missing Parts 2, 3, and 4 (alternatives, U statistic formula, interpretation guidance).
3. Cells 48–52 (H1–H5) — No post-output markdown after any individual test cell.
4. Cell 36 (UPV derived column) — Formula UPV = UNITS/VISITS absent from pre-cell markdown and data_dictionary.md.
5. Cell 51 (H4) — String match bug: "Upscale" vs actual value "UPSCALE", causing all-NaN output.
6. Cell 44 (7F chart) — No alternatives to the lift-ratio approach in pre-cell markdown.
7. Cell 32 (7B demand curves) — Log-log formula log(Q) = α + β·log(P) with symbols absent.
8. Cell 47 (hypothesis table) — Missing "Why this effect-size measure" column; H3 null hypothesis absent; slope-difference t-test described but not computed.
9. Cell 41 (7E correlation) — Pearson formula r = Cov(X,Y)/(σ_X·σ_Y) absent.
10. Cell 16 (QA audit) — Parts 2 and 4 missing (no alternatives named, no fail threshold stated).
11. Cell 20 (cleaning) — Parts 2 and 4 missing (no alternatives to row-dropping, no verification guidance).

All 11 gaps sent to data-explorer for fix. H4 string bug corrected. Notebook re-executed with 0 errors (72 cells: 27 code).

---

### Pass 2 (after data-explorer fix round)

**Verdict: FIX — 3 gaps remaining**

1. Cell 44 (7F lift-ratio block) — Part 2 (Alternatives considered) still absent; no alternatives named.
2. Cells 47–62 (H1–H6 test cells) — Formal H₀ null hypothesis statement missing for H1, H2, H4, H5, and H6 (only H3 has an explicit H₀).
3. data_dictionary.md derived columns — DISCOUNT_PCT missing expected direction ("higher DISCOUNT_PCT → higher UNITS").

**Max fix rounds reached (one fix round per stage). Proceeding to model-builder with 3 gaps noted.**

---

## 02_feature_engineering and 03_modeling

### Pass 1 (before model-builder fix round)

**Verdict: FIX — 10 gaps**

1. NB02 Cell 7 — LOG_PRICE formula absent from pre-cell markdown.
2. NB02 Cell 7 — No alternatives for log transformation of price.
3. NB02 Cell 11 — DISCOUNT_PCT formula absent; no alternatives for discount encoding.
4. NB02 Cell 15 — Lag feature formulas and rationale absent.
5. NB02 Cell 18 — Seasonal terms (Fourier) formula and rationale absent.
6. NB02 Cell 44 — Store segment choice lacks alternatives (lift-ratio alternatives not compared).
7. NB03 Cell 15 — Optuna search space for LightGBM: reasons per parameter range absent.
8. NB03 Cell 28 — Optuna search space for XGBoost: reasons per parameter range absent.
9. NB03 Cell 38 — Ridge FE elasticity model: no pre-cell 4-part markdown.
10. NB03 Cells 41–44 — Section 8 diagnostics (reliability plot, decile table, lift chart, threshold table): no individual pre-cell markdowns.

All 10 gaps sent to model-builder for fix. Both notebooks re-executed with 0 errors (NB02: 49 cells, 18 executed; NB03: 67 cells, 44 executed).

---

### Pass 2 (after model-builder fix round)

**Verdict: FIX — 7 gaps remaining**

1. NB03 Cells 43, 47, 49 — Zero captured outputs (decile lift chart, permutation importance plot, SHAP summary plot): execution counts present but no inline image or stream text.
2. NB03 Cells 41–44 — Section 8 diagnostics still missing individual pre-cell 4-part markdown; Section 8 header does not substitute.
3. NB03 Cells 41, 42, 44 — No post-output "Finding:" markdown after residual plot, decile table, threshold table.
4. NB03 Cell 38 — No dedicated pre-cell 4-part markdown for Ridge FE elasticity fit; rationale is 7 cells later in Section 10.
5. NB03 Cells 46, 48 — No post-output markdown after permutation importance ranking and SHAP ranking.
6. NB03 Cell 25 + tuning.md — XGBoost `min_child_weight` (range 1–50) missing from search space table; tuning.md omits XGBoost search space section entirely.
7. reports/modeling/features.md — Missing three fields per feature: formula/code expression, expected direction of effect, example row.

**Max fix rounds reached (one fix round per stage). Proceeding to ml-statistician with 7 gaps noted.**
