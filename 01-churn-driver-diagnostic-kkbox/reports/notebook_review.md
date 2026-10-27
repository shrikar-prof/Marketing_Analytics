# Notebook review log

## 01_exploration

### Review 1 (before fixes)
61 cells checked (20 code, 41 markdown). All 20 code cells executed, no errors. 14 analytical cells; every one has a why/how/read block before and a what-it-shows note after. Strictly against the four-part standard, 2 of 14 fully explained; the other 12 each miss one sub-part, almost always the second alternative. Builder script not in the project (helper `src/explore_utils.py` is imported openly).

Gaps:
1. Pre-registration table lacks the effect-size measure and the reason for it (cell 22); same table missing from hypotheses.md.
2. Derived-columns table missing expected direction, motivating finding/hypothesis, and an example row (cell 13); same in data_dictionary.md.
3. `segment` derived column (cell 41) has no entry in the derived-columns table or data dictionary.
4. Only one alternative named where two are required: cells 4, 7, 10, 19, 22, 25, 28, 31, 34, 37, 40, 43.
5. Mann-Whitney (H6) and Mantel-Haenszel (H9) have no alternatives listed (cell 46).
6. Breslow-Day homogeneity test reported (cell 47) but never introduced (cell 46).
7. Cramér's V ranking (cell 26) reports p-values without intervals.
8. "Odds" and "stratum" used without definition (cells 46, 50).
9. Holdout margin-of-error formula (cell 56) not explained in cell 55.
10. Output note says 18 segments, table shows 17 (cells 40, 41, 42, 53).

Verdict: FIX, 10 gaps (1 to 3 substantive, 4 to 10 one-line additions).

### Author fix round 1
All 10 gaps addressed; builder script added at src/build_notebook_01.py; notebook rebuilt and re-executed (20 of 20 cells, 0 errors); no result or finding changed.

### Review 2 (after fixes)
61 cells, 20 code, all executed, no errors. 13 of about 17 analytical cells fully explained. First-round gaps 2 to 10 resolved; gap 1 resolved in content but its table is malformed.

Remaining gaps:
A. Cell 22 pre-registration table malformed (missing pipe between "Reliable if" and "Effect size and why"; H10 effect-size text absent from the rendered table; no per-hypothesis reason-for-test or interval-method column).
B. Cell 13 derived-columns table, `segment` row misaligned by unescaped " | " in the formula and example; notebook and data_dictionary.md differ.
C. Cramér's V ranking (cells 25, 26) still prints p-values without intervals, now disclosed as descriptive.
D. Cells 28, 31, 34 have only an implied "how it works"; cell 49 business-sized effect has no alternatives or interval guidance.

Verdict: FIX, 4 gaps (A, B substantive; C, D minor).

### Orchestrator note
A and B are formatting defects introduced by the fix round, so one extra formatting-only fix was requested from the author before proceeding (deviation from the one-round rule, recorded here). No third review was run.

### Author fix round 2 (formatting only)
A and B repaired: pre-registration table has seven columns per row with "Test and why" and "Interval method and why" added; `segment` row uses "/" in table text. Rebuilt and re-executed, 20 of 20 cells, 0 errors; a check of every markdown table found no mismatched column counts. C and D skipped by the author (C already disclosed as descriptive). Remaining: C, D (minor).

## 02_feature_engineering and 03_modeling

### Review 1 (before fixes)
02: 63 cells, 19 code, all executed, no errors; 17 analytical cells, 16 fully explained. 03: 65 cells, 18 code, all executed, no errors; 14 analytical cells, 11 fully explained. All 12 engineered features carry name, meaning, formula, code, inputs, motivating finding, expected direction, example row, result and verdict, matching features.md. Optuna sampler, pruner, objective, nested design and search spaces are stated before the run. Decision rules precede results for validation, comparison, selection and final evaluation.

Gaps:
1. 02 cell 52: `price_resid` output note is generic; states no result (rho -0.02, DROP).
2. 03 cells 51/52: counterfactual bill assumption only partly explained (add-on price regression not written out; why other levers keep the bill unchanged; sensitivity to MonthlyCharges).
3. 03 cell 51: lever table (eligibility, target, bill treatment, direction, reason) missing before the code.
4. 03 cells 6 vs 34: selection decision rules inconsistent (paired-fold SD vs best model's outer-fold SD).
5. 03 cells 22, 25, 28: no family-specific tuning explanation; cell 18 does not say why median pruning suits 3-fold inner CV.
6. 02 cell 14 and per-feature notes: effect sizes without scale, interval, or reason for the thresholds.
7. 03 cell 40, 02 cell 58: no reading scale for AUC differences.
8. 03 cell 35: simplicity order unexplained.

Verdict: FIX, 8 gaps (1 to 3 first; 6 to 8 minor).

### Author fix round 1
All 8 gaps addressed in the builder scripts (markdown only). Both notebooks rebuilt and re-executed with the saved Optuna studies reloaded; test AUC unchanged at 0.84742; chosen model unchanged (GLM). 02: 19 of 19 cells, 03: 18 of 18, 0 errors. All markdown tables checked for equal column counts.

### Review 2 (after fixes)
02: 63 cells, all code executed, no errors; 17 of about 18 analytical cells fully explained. 03: 66 cells, all executed, no errors; 15 of about 17 fully explained. All 8 first-round gaps resolved.

Remaining and new gaps:
1. features.md rows for `n_streaming` and `price_resid` malformed by unescaped pipes in the verdict text (02 cell 61).
2. 02 cell 56 after-note generic (does not name the features that failed the signal rule or the highest pair correlation).
3. 03 cell 44 (segment performance) and cell 41 (decile and threshold charts) introduced only by a "plain words" cell; missing why, alternatives and how-to-read.
4. 02 cell 54 does not name which SD the added-value rule uses.
5. 03 cells 51 and 54 say "tenfold" where the quoted ratios are about 5 and 14.
6. 03 cell 29 random-forest note lacks the overfitting check and the untuned comparison promised in cell 27.
7. 02 cell 14 intervals quoted in markdown are not printed by any code cell.
8. 03 cells 23, 26, 29 "All 60 trials ran; 21 pruned" loosely worded.

Verdict: FIX, 8 gaps (1 formatting defect, 3 missing explanation, others short edits).

### Orchestrator note
Item 1 is a formatting defect in a file the ml-statistician reads, so one extra fix (items 1 to 8, explanations and formatting only) was requested before proceeding; deviation from the one-round rule recorded here. No third review was run.

### Author fix round 2
All 8 items fixed (features.md table repaired; redundancy, segment and decile notes added; paired-SD rule named; "tenfold" replaced with the actual 5 to 13 times; forest overfitting check added; intervals now printed by code; trial counts reworded). Rebuilt from saved Optuna studies; test AUC unchanged at 0.84742; 02: 19 of 19, 03: 18 of 18, 0 errors. No remaining gaps noted by the author; no third review run.
