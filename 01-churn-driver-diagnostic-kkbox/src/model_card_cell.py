FK = f'FINAL: {chosen}'
_el = [f for f in sel.index[sel['within_1sd_of_best']] if f != chosen]
sel_reason = (f"it had the best nested AUC, {sel.loc[chosen,'nested_auc']:.4f}, and is the simplest family; " if chosen == best_f else "it was the simplest model within one standard deviation of the best; ") + (f"{', '.join(_el)} were also within one standard deviation but are more complex, so the rule preferred {chosen}" if _el else "no other tuned family was within one standard deviation") + ' (section 6 of notebook 03)'
def g(m, pct=False, k=FK):
    t = ci[k]; e, lo, hi = t.loc[m, 'estimate'], t.loc[m, 'ci_low_2.5%'], t.loc[m, 'ci_high_97.5%']
    return f'{100*e:.1f}% (95% interval {100*lo:.1f}% to {100*hi:.1f}%)' if pct else f'{e:.3f} (95% interval {lo:.3f} to {hi:.3f})'
r2, r1, gr = 'Rule 2: segment churn rate', 'Rule 1: m2m fiber first-year flag', 'Logistic regression, raw columns'
top_drv = drivers.sort_values('rank_shap').head(5)
ctrl = drivers[drivers['driver_type'] == 'controllable'].sort_values('rank_shap').head(3)['column'].tolist()
d_rule2 = diffs[(diffs.final_minus == r2) & (diffs.metric == 'top20_rev')].iloc[0]
d_glm = diffs[(diffs.final_minus == gr) & (diffs.metric == 'top20_rev')].iloc[0]
d_rule2_auc = diffs[(diffs.final_minus == r2) & (diffs.metric == 'auc')].iloc[0]
t20 = dec.iloc[:2]
tot_lost = float((rev_te * yte).sum())
cf_txt = '; '.join(f"{r.lever} ({r.mean_change_pts:+.1f} points, interval {r.ci_low_pts:+.1f} to {r.ci_high_pts:+.1f})" for r in cf.itertuples())
plain = f'''# Model card: customer churn risk score

## Plain-language summary

- **What it predicts.** For each customer, the chance of leaving (churning) in the observation window, as a probability from 0 to 1. The use is to rank customers so a retention team can start with the riskiest. It does not say why anyone leaves.
- **Data it learned from.** The IBM Telco sample: 7,043 customers, one row each, one fiscal quarter; 26.5% left. 5,634 customers (80%) were used to build and tune the model; 1,409 (20%, with {int(yte.sum())} leavers) were locked away and scored once at the end. Billing-total columns were left out because their timing relative to exit is unknown.
- **How it was tested.** Five model types were compared on 25 cross-validation folds. The top three were tuned with Optuna (60 trials per study, nested cross-validation so the tuning score is honest). The chosen model is **{chosen}** ({sel_reason}).
- **How good it is (held-out test, 1,409 customers).** AUC (chance that a random leaver is scored above a random stayer; 0.5 is a coin flip) is {g('auc')}. The 20% of customers with the highest scores contain **{g('top20_rev', True)}** of the monthly revenue of customers who left (${float((rev_te*yte)[np.argsort(-p_te)[:int(np.ceil(.2*len(yte)))]].sum()):,.0f} of ${tot_lost:,.0f}); picking at random would capture 20%. In that group {g('top20_precision', True)} really leave (base rate {100*yte.mean():.1f}%) and it holds {g('top20_recall', True)} of all leavers.
- **Against simple alternatives (same test rows).** The explorer-style segment rule captures {100*ci[r2].loc['top20_rev','estimate']:.1f}% of lost revenue in its top 20%; the plain logistic model on raw columns {100*ci[gr].loc['top20_rev','estimate']:.1f}%. The paired difference of the final model over the segment rule is {100*d_rule2.difference:+.1f} points (95% interval {100*d_rule2.ci_low:+.1f} to {100*d_rule2.ci_high:+.1f}); over the raw logistic {100*d_glm.difference:+.1f} points ({100*d_glm.ci_low:+.1f} to {100*d_glm.ci_high:+.1f}). Where the interval includes zero, the model is not shown to beat that alternative on this test set.
- **Calibration (do customers scored 40% leave about 40% of the time?).** ECE (average gap between predicted and actual rate) is {g('ece')}; Brier score (mean squared error of the probability; 0 is perfect, about 0.195 for always guessing the base rate) is {g('brier')}. Our target was ECE of 0.05 or lower.
- **What drives the score** (top five original columns by SHAP): {', '.join(top_drv['column'])}. Contract, tenure, internet type and payment method overlap, so their individual shares are partly shared. MonthlyCharges and InternetService rank high partly because the bill and the service mix measure nearly the same thing and the model uses them together; this does not show that price alone drives churn. Types: structural (cannot be changed) {', '.join(drivers[drivers.driver_type=='structural'].sort_values('rank_shap').head(2)['column'])}; controllable by the business, most used: {', '.join(ctrl)}.
- **What-if sensitivity (association, not cause).** Changing a lever in the model for eligible test customers moves their predicted churn probability by: {cf_txt}. These are model associations. The two add-on levers change by about 5 to 13 times (security 4.6 times, tech support 12.7 times) with the assumption about the bill, so they are not stable and must not be used to size anything. Customers who choose long contracts or automatic payment may differ in ways the data does not record. A randomised pilot is needed to measure what an offer really saves.
- **Must not be used for.** Deciding prices, service or credit for an individual on the basis of age (SeniorCitizen) or gender; treating a score as the reason a customer left; estimating the revenue an offer will save (no save rate or offer cost is in the data); using it on a different business or a different period without re-testing.
- **Known weaknesses.** One quarter of data and one company: no sign of how it behaves over time. About {int(yte.sum())} leavers in the test set, so every estimate carries a wide interval (about +/-5 points). Tenure and billing may be measured at exit for leavers (unclear from this data), which could flatter the model. Segments with fewer than 100 test customers are not interpreted. Scores in `scores.csv` for training customers are out-of-fold; the model is not recalibrated.
'''
appx = ['', '# Technical appendix', '',
 '## A. Validation design', '', 'Stratified random 80/20 split (seed 42): 5,634 train, 1,409 test. Model choice and tuning used repeated stratified 5-fold cross-validation (5 repeats, 25 fold-scores) on the training rows; the test set was scored once. Preprocessing is inside a scikit-learn Pipeline. Primary metric AUC; business metric top-20% revenue capture.', '',
 f'Final model: **{chosen}**, parameters: `{json.dumps(best, default=float)}`. Inputs: 15 categorical and 3 numeric raw columns plus engineered features {kept} (see features.md).', '',
 '## B. Baselines and model families (25-fold cross-validation, training rows; mean and SD)', '', M.md_table(fam_tbl, '{:.4f}'), '', M.md_table(base_tbl.round(4), '{:.4f}'), '',
 '## C. Tuning summary (nested cross-validation)', '', M.md_table(nest_tbl.round(4).reset_index(), '{:.4f}'), '', 'Full search spaces, best parameters, importance tables and plots: tuning.md.', '',
 '## D. Model selection', '', M.md_table(sel.round(4).reset_index(), '{:.4f}'), '',
 '## E. Held-out test metrics with 95% bootstrap intervals', '', M.md_table(test_metrics.round(4), '{:.4f}'), '', 'Paired differences (final minus baseline) on the same bootstrap resamples:', '', M.md_table(diffs.round(4), '{:.4f}'), '',
 '## F. Decile table (test set, 1 = highest predicted risk)', '', M.md_table(dec.round(3), '{:.3f}'), '', '## G. Threshold table (test set)', '', M.md_table(thr_tbl.round(3), '{:.3f}'), '',
 '## H. Segment performance (test set; small = fewer than 100 customers)', '', M.md_table(seg_tbl.round(2), '{:.2f}'), '',
 '## I. Driver importance', '', M.md_table(drivers.round(4), '{:.4f}'), '', '## J. What-if sensitivity (association, not causal)', '', M.md_table(cf.round(3), '{:.3f}'), '',
 '## K. Files', '', 'Model: models/churn_driver_diagnostic_model.joblib; config: models/final_config.json; scores: reports/modeling/scores.csv; tables: reports/modeling/tables/; charts: reports/modeling/charts/; pipeline: src/pipeline.py (`--train`, `--evaluate`, `--predict`).']
open(f'{PROJECT}/reports/modeling/model_card.md', 'w').write(plain + '\n'.join(appx) + '\n')
print(plain)
