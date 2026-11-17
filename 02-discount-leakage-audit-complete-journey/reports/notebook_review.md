# Notebook Review Log

## 01_exploration

### Review 1 (first pass)
**Verdict: FIX — 6 gaps**

1. Cell 47 (hypothesis pre-registration table) — missing "Null hypothesis," "Reason for test," and "CI method" columns.
2. Cells 49–53 (H2–H7 code cells) — five analytical cells each missing a pre-cell markdown with null hypothesis and output interpretation.
3. Cell 16 (leakage column derivations) — pre-cell markdown missing: why list_revenue formula was used, alternatives for disc_rate denominator, expected direction for each column.
4. Cell 20 (headline leakage totals) — no four-part explanation (alternatives, formula, how to read output).
5. data_dictionary.md — derived-column rows missing "motivating finding or hypothesis" and "expected direction" fields.
6. Cells 10 and 14 (quality audit and cleaning) — pre-cell markdowns missing alternatives considered, plain-language rules, and "how to read" guidance.

**Fix round applied by data-explorer. All 6 gaps addressed. Notebook re-executed: 68 cells, 0 errors.**

---

### Review 2 (post-fix pass)
**Verdict: FIX — 3 gaps remaining (proceeding per command rule)**

1. Cell 17 (leakage column derivations) — four named-symbol formulas (total_disc, disc_rate, retailer_disc, mfr_disc) appear only after the code in cell 18; they need to be in the "How it works" pre-cell section of cell 16.
2. Cells 51, 53, 55, 57, 59 (H2–H7 code cells) — immediately preceding markdowns have null hypothesis and "how to read" but are still missing "Why this method" and "Alternatives considered" as individual paragraphs (covered only in the shared cell 48 pre-cell for H1).
3. hypotheses.md — pre-registration table exists in the notebook but was not written to the companion file; only result rows are there.

**No further fix round applied (max one fix round per stage). Proceeding to model-builder.**

---

## 02_feature_engineering and 03_modeling

### Review 1 (first pass)
**Verdict: FIX — 10 gaps**

1. [03] Cells [31]-[34] — missing four-part bridge before decile/calibration/threshold/segment analysis.
2. [03] Cells [20]-[23] — Optuna study and plot cells not immediately preceded by markdown.
3. [03] Cells [43]-[44] — counterfactual cell missing bootstrap CI restatement and chart reading guide.
4. [02] Cell [11] — only one alternative considered for is_national encoding.
5. [02] Cell [26] — TargetEncoder missing second alternative and "how to read" guidance.
6. features.md — missing "Expected direction" and "Example row" columns.
7. [03] Cell [17] — Optuna search space bounds stated without per-parameter reasoning.
8. [03] Cell [40] — SHAP beeswarm missing immediate pre-cell reading guide.
9. [03] Cell [42] — driver classification missing explicit structural-vs-controllable rule.
10. [02] Cell [23] — Spearman r reported without bootstrap CI or effect-size scale.

**Fix round applied by model-builder. All 10 gaps addressed. NB02: 36 cells, 0 errors. NB03: 66 cells, 0 errors.**

---

### Review 2 (post-fix pass)
**Verdict: FIX — 2 gaps remaining (proceeding per command rule)**

1. 02_feature_engineering.ipynb cell 24 (bootstrap CI pre-cell markdown) — alternatives considered (Fisher z, asymptotic normal) and plain-language resampling procedure still absent.
2. features.md — Formula, Expected direction, and Example row columns added to some rows but three columns still missing for all features.

**No further fix round applied (max one fix round per stage). Proceeding to ml-statistician.**
