"""Builds notebooks/03_modeling.ipynb. Run: python -I src/build_notebook_03.py
Interpretation notes that quote results live in src/notes_03.py (written after the first run)."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nbkit import md, code, explain, save
try:
    from notes_03 import NOTES
except ImportError:
    NOTES = {}
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
C = []
FAMTXT = {0: 'GLM: the two searched numbers decide how much the weights are shrunk. C (log scale, 0.001 to 10) covers from near-constant predictions to almost no shrinkage; l1_ratio (0 to 1) moves between ridge and lasso. This suits a linear model, whose only real freedom is penalty strength and type. Look for: a best C at the top edge of the range (10) would mean the data wants even less shrinkage than allowed; a score barely above the section 4 default means the family has nothing left to tune.', 1: 'XGBoost: seven parameters, all aimed at overfitting control on 4,500 rows: small learning rates with 100 to 600 rounds, depth 2 to 7, a minimum leaf weight, row and column sampling and an L2 penalty. Pruning helps most here because slow-learning, deep settings are expensive and often poor. Look for: a best depth at the bottom edge (2) means interactions add little, a best learning rate near the top means too few rounds were allowed, and compare the nested score with the final-study best (a big gap means tuning luck).', 2: "Random forest: four parameters. Depth (3 to 14) and minimum leaf size (1 to 40) control how closely single trees can memorise customers; max_features (0.1 to 0.8) controls how different the trees are; the number of trees mostly steadies the average. A forest has no learning rate, so tuning is mainly about making trees shallower than the default. Look for: best depth and leaf size well away from 'deep and tiny' (the defaults), which signals the default forest was overfitting."}
def N(key, default="(interpretation to be written after the run)"):
    return md(NOTES.get(key, default))

C.append(md("""# 03. Modeling: churn driver diagnostic

**Question.** Which customers are most likely to leave, how well can we rank them, and which of the drivers could the business act on?

**Plan, in order:** validation design, baselines, model family comparison, Optuna tuning, model selection, one-touch held-out evaluation, explanation and what-if analysis, artifacts, model card.

**Reading guide.** Every analytical step has an explanation cell before it (why this method, alternatives, how it works, how to read the output) and a note after it that says what the output showed. Decision rules are written before results.

**What the model cannot do.** It ranks customers by how much they look like past leavers. It does not say why anyone left, and a feature that predicts churn is not automatically a lever that reduces it."""))

# ------------------------------------------------------------ 1 setup
C.append(md("## 1. Setup and data"))
C.append(md("Plain words: load the feature table written by notebook 02 and keep only the training rows for now. The held-out test rows are loaded once, in section 7. Print the library versions and the seed so the run can be repeated."))
C.append(code("""
import os, sys, json, time, warnings, subprocess
warnings.filterwarnings('ignore')
PROJECT = os.path.abspath('..'); sys.path.insert(0, os.path.join(PROJECT, 'src'))
import numpy as np, pandas as pd, sklearn, scipy, matplotlib, optuna, lightgbm, xgboost, catboost, shap, joblib
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import features as F, model_utils as M
SEED = F.SEED; np.random.seed(SEED)
CH = f'{PROJECT}/reports/modeling/charts'; TB = f'{PROJECT}/reports/modeling/tables'
for d in (CH, TB, f'{PROJECT}/models'): os.makedirs(d, exist_ok=True)
plt.rcParams.update({'figure.dpi': 100, 'axes.grid': True, 'grid.alpha': .3})
print('seed', SEED, '| sklearn', sklearn.__version__, '| lightgbm', lightgbm.__version__, '| xgboost', xgboost.__version__,
      '| catboost', catboost.__version__, '| optuna', optuna.__version__, '| shap', shap.__version__, '| pandas', pd.__version__, '| numpy', np.__version__)
df = M.load_features(); FL = M.load_feature_list(); kept = FL['kept']
train = df[df['split'] == 'train'].reset_index(drop=True)
Xtr = train.drop(columns=[F.ID_COL, 'split', F.TARGET]); ytr = train[F.TARGET]
print('training rows', len(train), '| leavers', int(ytr.sum()), f'({100*ytr.mean():.1f}%) | engineered features kept:', kept)
"""))
C.append(N("s1"))

# ------------------------------------------------------------ 2 validation
C.append(md("## 2. Validation design"))
C.append(explain("Repeated stratified 5-fold cross-validation on the training rows, with a held-out test set touched once",
    "We need an honest estimate of how the model will do on customers it has not seen, and we need to choose between models without using the test set. The handoff gives the design: one row per customer (rows independent, no grouping needed) and no date (no time split). A fixed 20% test set (1,409 customers) stays locked until section 7.",
    ["Single train/validation split: cheap, but with about 1,500 leavers in training one split gives a noisy score. Not used.",
     "Group k-fold by customer or out-of-time split: not applicable here (one row per customer, no date).",
     "Leave-one-out: nearly unbiased but expensive and high-variance for ranking metrics. Not used."],
    "Cross-validation (CV) cuts the training rows into 5 parts that each keep 26.5% leavers (stratified). Each part is scored by a model trained on the other four. The cut is repeated 5 times with different shuffles, giving 25 scores per model. We report their mean and standard deviation (SD, the spread). All preprocessing (one-hot coding, scaling, any fitted feature) sits inside a scikit-learn Pipeline, which is refitted on the training part of every fold, so nothing is learned from the validation part. **Primary ranking metric:** AUC (area under the ROC curve: the chance a random leaver gets a higher score than a random stayer; 0.5 is a coin flip, 1.0 is perfect), $AUC=P(s_i>s_j\\mid y_i=1,y_j=0)$. **Business metric:** top-20% revenue capture = (monthly bills of leavers inside the 20% of customers with the highest score) / (monthly bills of all leavers); a random ranking gives 20%, the explorer's rule gave about 52% in-sample. **Also recorded:** PR-AUC (average precision: how pure the flagged group stays as we flag more; the leaver base rate 0.265 is the no-skill level), Brier score ($\\frac1n\\sum(\\hat p_i-y_i)^2$; 0 is perfect, always guessing 0.265 gives about 0.195) and ECE (expected calibration error: the average gap between predicted and actual churn rate across 10 probability bins; under 0.05 is a useful target). Decision rules, fixed before any result: models are compared on AUC; ties are read together with top-20% capture and Brier; in section 4 (untuned comparison) and in notebook 02 a model counts as better only if its mean exceeds the other by more than the SD of the paired fold differences. Section 6 uses a different, simpler band for the tuned families, explained there, because paired differences between tuned families were not computed.",
    "Look at the fold sizes: each validation part should have a similar leaver count. An SD larger than the gap between two models means the models cannot be told apart on this data."))
C.append(code("""
splits = M.repeated_splits(ytr, 5, 5)            # 25 (train_idx, validation_idx) pairs, same for every model
cnt = pd.DataFrame([dict(fold=i, train_rows=len(a), valid_rows=len(b), valid_leavers=int(ytr.iloc[b].sum()), valid_rate_pct=round(100*ytr.iloc[b].mean(), 2)) for i, (a, b) in enumerate(splits)])
display(cnt.describe().loc[['min', 'max']].round(2))
print('number of fold-scores per model:', len(splits))
"""))
C.append(N("s2"))

# ------------------------------------------------------------ 3 baselines
C.append(md("## 3. Baselines: the floor to beat"))
C.append(explain("Two business rules and a plain regularised logistic regression on the raw columns",
    "A model is only useful if it beats what a manager could do without it. Rule 1 is the simplest heuristic: flag month-to-month fiber customers in their first 12 months (finding 5). Rule 2 is the explorer's ranking: the churn rate of each contract x internet x first-year segment, learned on the training part of each fold. The logistic model on raw columns sets the floor for statistical modelling.",
    ["Rank by a single column (for example contract only): even simpler, but the segment rule already contains it.",
     "Rank by MonthlyCharges: tests the idea that big bills churn, but H6 shows the link is only moderate.",
     "A decision tree of depth 3: a rule found by data, but it is close to Rule 2 and less stable."],
    "Rule 1 scores 1 for the flagged group and 0 for everyone else. Rule 2 scores each segment with $\\hat p_g=\\frac{k_g+m\\,\\bar y}{n_g+m}$, where $k_g$ is the number of leavers and $n_g$ the customers of segment $g$ in the training part, $\\bar y$ the overall churn rate and $m=20$ pseudo-customers that pull small segments toward the average. Logistic regression models the log-odds of leaving as a weighted sum of the inputs, $\\log\\frac{p}{1-p}=b_0+\\sum_j b_jx_j$, with an L2 penalty (a pull that shrinks every weight toward zero so no single column dominates; strength set by C, here the default 1.0). Categorical columns are one-hot coded (one 0/1 column per category) and numbers are standardised, both inside the pipeline. Ties in rule scores are broken at random with a fixed seed, so the top-20% group is well defined.",
    "Compare the AUC, top-20% revenue capture and Brier of each baseline. Rule 1 gives only two score values, so its AUC and ECE are crude and its calibration is not meaningful. Whatever the best baseline achieves is the number the tuned models must beat."))
C.append(code("""
results = {}     # name -> per-fold DataFrame
def run(name, est, X=None):
    results[name] = M.cv_evaluate(est, Xtr if X is None else X, ytr, splits)
    return results[name]
run('Rule 1: m2m fiber first-year flag', M.RuleFlag())
run('Rule 2: segment churn rate', M.RuleSegmentRate(m=20))
run('Logistic regression, raw columns', M.make_pipeline('glm', feature_set='raw'))
COLS = ['auc', 'pr_auc', 'top20_rev', 'top20_precision', 'brier', 'ece']
def table(names):
    rows = []
    for n in names:
        r = results[n]; row = {'model': n}
        for c in COLS: row[c + ' mean'] = r[c].mean(); row[c + ' sd'] = r[c].std()
        row['fit s'] = r['fit_s'].mean(); rows.append(row)
    return pd.DataFrame(rows)
base_tbl = table(list(results)); display(base_tbl.round(4))
base_tbl.to_csv(f'{TB}/baselines_cv.csv', index=False)
"""))
C.append(N("s3"))

# ------------------------------------------------------------ 4 families
C.append(md("## 4. Model family comparison"))
C.append(explain("Five model families, same folds, engineered features",
    "Different families capture different shapes: straight-line effects, interactions, thresholds. With 5,634 training customers and about 28 inputs, we expect small differences, so the comparison also tests whether a simple model is enough.",
    ["Fit only one favourite family (for example LightGBM): fast, but we could not show that a simpler or different family is not better.",
     "Add neural networks or stacked ensembles: more flexible, but for 5,600 rows of mostly 0/1 inputs they rarely beat boosting and they cost explainability. Not used.",
     "Compare on a single split: noisy; the 25-fold design above is more stable."],
    "**Regularised logistic regression (GLM, generalised linear model)**: a weighted sum of inputs turned into a probability; the L2 penalty shrinks weights; C controls strength (smaller C, stronger shrinkage). **Random forest**: many deep decision trees, each fit on a random resample of rows and a random subset of columns, averaged; averaging cancels their individual overfitting; main knobs are tree depth, minimum leaf size and columns tried per split. **LightGBM, XGBoost, CatBoost (gradient boosting)**: trees fitted one after another, each correcting the errors of the sum so far, $F_m(x)=F_{m-1}(x)+\\eta\\,h_m(x)$, where $h_m$ is the new small tree and $\\eta$ the learning rate; they avoid overfitting through a small $\\eta$, shallow trees, minimum rows per leaf, row and column sampling and an L2 penalty on leaf values. CatBoost uses symmetric trees and ordered boosting, which is steadier on small data. All five receive the same one-hot coded inputs and the same 25 folds. Decision rule, fixed before the result: **the three families with the highest mean CV AUC go to Optuna tuning.**",
    "Read AUC and top-20% capture with their SDs. Differences smaller than the SD are noise. The chart shows mean with one SD whiskers."))
C.append(code("""
fam_names = {'glm': 'GLM (logistic, engineered)', 'rf': 'Random forest', 'lgbm': 'LightGBM', 'xgb': 'XGBoost', 'catboost': 'CatBoost'}
for f, nm in fam_names.items():
    t0 = time.time(); run(nm, M.make_pipeline(f, feature_set='eng', kept=kept)); print(f'{nm}: {time.time()-t0:.0f}s')
fam_tbl = table(list(fam_names.values()) + ['Logistic regression, raw columns', 'Rule 2: segment churn rate']).round(4)
display(fam_tbl)
fam_tbl.to_csv(f'{TB}/family_comparison_cv.csv', index=False)
ranked = sorted(fam_names, key=lambda f: -results[fam_names[f]]['auc'].mean())
top3 = ranked[:3]; print('families ranked by mean CV AUC:', ranked, '\\n-> tuned:', top3)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))
labs = list(fam_names.values()) + ['Logistic, raw', 'Rule 2 segment']; keys = list(fam_names.values()) + ['Logistic regression, raw columns', 'Rule 2: segment churn rate']
for a, (c, ttl) in zip(ax, [('auc', 'AUC (higher is better)'), ('top20_rev', 'Top-20% revenue capture (higher is better)'), ('brier', 'Brier score (lower is better)')]):
    m = [results[k][c].mean() for k in keys]; s = [results[k][c].std() for k in keys]
    a.barh(labs, m, xerr=s, color='#3b6ea5'); a.set_title(ttl, fontsize=10); a.invert_yaxis()
    lo = min(m) - 3*max(s); a.set_xlim(max(0, lo), max(m) + 3*max(s))
plt.suptitle('Cross-validated comparison (25 folds, mean and 1 SD)'); plt.tight_layout(); plt.savefig(f'{CH}/model_comparison.png', dpi=110); plt.show()
"""))
C.append(N("s4"))

# ------------------------------------------------------------ 5 optuna
C.append(md("## 5. Optuna tuning with nested cross-validation"))
C.append(explain("Tune the top three families with Optuna, scored by nested cross-validation",
    "Default settings are rarely the best settings, but tuning on the same folds you report from gives an optimistic score, because the best of many trials is partly luck. Nested CV keeps the estimate honest: parameters are always chosen on rows that the scoring part has never seen.",
    ["Grid search: tries every combination on a fixed grid; wastes trials on poor regions and grows too fast with more parameters.",
     "Random search: simple and decent; TPE (below) usually finds good settings in fewer trials by learning from past ones.",
     "Skip tuning and keep defaults: the comparison in section 4 already shows how close defaults are; tuning checks whether there is anything left to gain."],
    "**Sampler:** TPE (Tree-structured Parzen Estimator): after 10 random start trials it models which parameter values gave good scores and which gave poor ones, and samples more from the good region. Seed fixed to 42 (outer fold k uses 42+k). **Pruner:** median pruner: after each inner fold the trial's running mean AUC is compared with the median of earlier trials at the same step, and the trial stops early if it is below (10 start trials, no pruning on the first fold). Median pruning suits 3-fold inner CV because there are only 3 checkpoints per trial: a rule based on the median of earlier trials needs no tuning, never stops a trial before it has seen one fold, and cannot be fooled by a noisy single fold as a stricter rule (for example stopping at the best-so-far) could. It saves time without removing the good region, because only trials below the median after the first or second fold are stopped. **Objective:** mean AUC over the inner folds. We optimise AUC (the ranking metric) because the ranking is what the retention list is built from; for every trial we also store top-20% revenue capture, PR-AUC, Brier and fit time, so the final choice weighs all of them. **Nested design (two levels):** (1) Outer loop, honest estimate: the 5,634 training rows are cut into 5 outer folds. For each, a separate study of 60 trials tunes on the outer-training rows with 3-fold inner CV, then the best parameters are refitted on all outer-training rows and scored once on the outer-validation rows. The mean and SD of those 5 scores is the nested estimate. (2) Final study: one study of 60 trials on 5-fold CV of the whole training set; its best parameters are the ones used for the final model. It is saved to `models/optuna_<family>.db`. Time cap 15 minutes per study (30 per family); in practice all studies finish all 60 trials. **Search spaces** are shown below with the reason for each range. Ranges are wide enough to include the defaults and narrow enough that small data cannot be overfitted by deep trees.",
    "The key number is the nested outer-fold AUC (mean and SD). The final-study best AUC will be a little higher, because it is the best of 60 trials on the same folds that picked it; the gap between the two shows how much of the tuning gain was luck. The importance table says which parameters mattered; low importance across the board means the family is insensitive to tuning."))
C.append(code("""
rows = []
for f in top3:
    for p, rng, why in M.SEARCH_SPACE_TEXT[f]: rows.append({'family': f, 'parameter': p, 'range': rng, 'why this range': why})
space_tbl = pd.DataFrame(rows); space_tbl.to_csv(f'{TB}/optuna_search_space.csv', index=False); display(space_tbl)
"""))
C.append(N("s5a"))
tune_cell = """
fam = top3[{k}]; t0 = time.time()
tuned = globals().setdefault('tuned', {{}})
tuned[fam] = M.tune_family(fam, Xtr, ytr, feature_set='eng', kept=kept, n_trials=60, timeout=900, reuse=True, threads=2)
r = tuned[fam]; nest = pd.DataFrame(r['nested'])
print(fam, '| wall time', round(time.time()-t0), 's | stored: nested', round(r['nested_seconds']), 's, final study', round(r['final_study_seconds']), 's')
print('final study: trials', r['n_trials'], '| completed', r['n_complete'], '| pruned', r['n_pruned'])
print(f"final study best AUC {{r['best_value']:.4f}} (SD over 5 folds {{r['best_auc_sd']:.4f}}) | top-20% capture {{r['best_top20']:.3f}} | Brier {{r['best_brier']:.4f}}")
print(f"nested outer AUC {{nest['auc'].mean():.4f}} +/- {{nest['auc'].std():.4f}} | top-20% capture {{nest['top20_rev'].mean():.3f}} +/- {{nest['top20_rev'].std():.3f}} | Brier {{nest['brier'].mean():.4f}}")
print('best parameters:', r['best_params'])
display(nest[['outer_fold', 'auc', 'pr_auc', 'top20_rev', 'brier', 'ece', 'inner_best_auc', 'n_trials', 'n_pruned']].round(4))
"""
for k in range(3):
    C.append(md(f"### 5.{k+2} Tune family number {k+1} of the top three (chosen in section 4)\n**What is different about this family (in this run family {k+1} is " + {0:'the GLM', 1:'XGBoost', 2:'the random forest'}[k] + ").** " + FAMTXT[k] + f"\n\nPlain words: run the nested study for the family ranked {k+1} in section 4. The result is cached in `models/tuning_<family>.json` and `models/optuna_<family>.db`, so re-running the notebook reloads it instead of tuning again. The table lists the five outer folds: each row is the score of parameters tuned without seeing that fold."))
    C.append(code(tune_cell.format(k=k)))
    C.append(N(f"s5_{k}"))
C.append(md("### 5.5 Optimization history, parameter importance and tuning.md\nPlain words: draw, for each tuned family, how the best score improved over trials and which parameters mattered, save the PNGs, and write `tuning.md`."))
C.append(code("""
for f in top3:
    M.plot_optuna(f, CH)
nest_rows = []
for f in top3:
    n = pd.DataFrame(tuned[f]['nested']); nest_rows.append(dict(family=f, nested_auc_mean=n['auc'].mean(), nested_auc_sd=n['auc'].std(), nested_top20_mean=n['top20_rev'].mean(), nested_top20_sd=n['top20_rev'].std(),
        nested_prauc_mean=n['pr_auc'].mean(), nested_brier_mean=n['brier'].mean(), nested_ece_mean=n['ece'].mean(), final_best_auc=tuned[f]['best_value'], final_best_auc_sd=tuned[f]['best_auc_sd'],
        trials=tuned[f]['n_trials'], pruned=tuned[f]['n_pruned']))
nest_tbl = pd.DataFrame(nest_rows).set_index('family'); nest_tbl.round(4).to_csv(f'{TB}/tuning_summary.csv'); display(nest_tbl.round(4))
L = ['# Tuning report', '', 'Nested cross-validation with Optuna (TPE sampler, seed 42, median pruner, 60 trials per study). Training split only (5,634 customers). Associations only; nothing here is a causal effect.', '',
 'Design: (1) outer loop for an honest score: 5 outer folds, each with its own 60-trial study on 3-fold inner CV of the outer-training rows, scored once on the outer-validation rows; (2) final study: 60 trials on 5-fold CV of the whole training split, saved to `models/optuna_<family>.db`, whose best parameters are used for the final model. Objective: mean AUC (how well the model ranks who will leave; 0.5 is a coin flip, 1.0 is perfect). For every trial we also stored top-20% revenue capture, PR-AUC, Brier (average squared error of the probability; lower is better) and fit time: see `tables/optuna_trials_<family>.csv`.', '',
 '## Summary', '', M.md_table(nest_tbl.round(4), '{:.4f}', index=True), '',
 'The nested score is the honest one. The final-study best AUC is optimistic by construction (best of 60 trials on the same folds).', '']
for f in top3:
    r = tuned[f]; n = pd.DataFrame(r['nested'])
    L += [f'## {f}', '', '### Search space', '', M.md_table(space_tbl[space_tbl.family == f].drop(columns='family')), '',
          '### Best parameters (final study)', '', '```', json.dumps(r['best_params'], indent=1), '```', '',
          f"Best final-study AUC {r['best_value']:.4f} (SD across its 5 folds {r['best_auc_sd']:.4f}); top-20% revenue capture {r['best_top20']:.3f}; Brier {r['best_brier']:.4f}; mean fit time {r['best_fit_seconds']:.2f} s per fit. Trials {r['n_trials']} (completed {r['n_complete']}, pruned {r['n_pruned']}). Time: nested part {r['nested_seconds']/60:.1f} min, final study {r['final_study_seconds']/60:.1f} min.",
          f"Nested outer-fold AUC {n['auc'].mean():.4f} +/- {n['auc'].std():.4f} (5 folds); top-20% capture {n['top20_rev'].mean():.3f} +/- {n['top20_rev'].std():.3f}.", '',
          '### Parameter importance (Optuna fANOVA-style, share of score variation explained; sums to 1)', '',
          M.md_table(pd.DataFrame({'parameter': list(r['importance']), 'importance': list(r['importance'].values())}), '{:.3f}'), '',
          '### Plots', '', f'![history](charts/optuna_{f}_history.png)', '', f'![importance](charts/optuna_{f}_importance.png)', '']
open(f'{PROJECT}/reports/modeling/tuning.md', 'w').write('\\n'.join(L)); print('tuning.md written')
"""))
C.append(N("s5b"))

# ------------------------------------------------------------ 6 selection
C.append(md("## 6. Model selection"))
C.append(explain("Pick one model on all aspects, preferring the simpler model when it is as good within noise",
    "A single best number invites overfitting to the comparison. We weigh ranking, calibration, stability across folds, simplicity and inference cost, and we do not use the held-out test set to choose.",
    ["Pick the highest mean AUC: simple, but a 0.002 gain bought with a much more complex model is not worth the explanation cost.",
     "Average several models (ensemble): can add a point of AUC, but costs explainability and a second model to maintain.",
     "Choose on the held-out test set: would use the test rows twice. Not allowed."],
    "Decision rule, fixed before the result: (1) the nested outer-fold mean AUC of each tuned family is the main score; (2) take the best family and its SD across the 5 outer folds; (3) every family whose mean AUC is within one SD of the best is eligible (**this band governs selection**: it is the spread of the best family's own outer-fold scores, 5 values, which is wider than the SD of paired differences between two models on the same folds, because paired differences cancel the fold-to-fold difficulty that both models share; a wider band errs toward choosing the simpler model, which is the intended direction, and the paired SD was not computed for the tuned families; with the numbers seen, GLM and XGBoost tie to four decimals, so a narrower band would not change the choice); (4) among the eligible, choose the simplest (order: GLM, then LightGBM and XGBoost, then random forest and CatBoost); if still tied, the higher mean AUC. Calibration (ECE under 0.05), top-20% capture and Brier are shown beside the choice and are checked as vetoes: a model with ECE over 0.05 would need recalibration before use. Inference cost is the time to score 1,000 customers. **Why this simplicity order.** It is a judgement made before the results, ranking by how many numbers define the model and how easily a manager or auditor can follow its predictions: a GLM is one weight per input and fully additive (rank 1); LightGBM and XGBoost are sums of a few hundred small trees, standard and checked with SHAP (rank 2); a random forest stores hundreds of deep trees and CatBoost adds symmetric trees, ordered boosting and a heavier dependency (rank 3). Measured scoring time agrees with the order. Ties inside a rank do not matter here, because the GLM is eligible and ranks first.",
    "If the simplest eligible model is the GLM, the extra flexibility of trees does not pay on this data. Read the table for any family that wins on one metric but loses on the others."))
C.append(code("""
Xs = Xtr.sample(1000, random_state=SEED, replace=True); sel_rows = []
for f in top3:
    est = M.make_pipeline(f, tuned[f]['best_params'], 'eng', kept, n_jobs=1).fit(Xtr, ytr)
    t0 = time.time(); [est.predict_proba(Xs) for _ in range(5)]; inf = (time.time()-t0)/5
    n = pd.DataFrame(tuned[f]['nested'])
    sel_rows.append(dict(family=f, nested_auc=n['auc'].mean(), auc_sd=n['auc'].std(), top20_capture=n['top20_rev'].mean(), pr_auc=n['pr_auc'].mean(), brier=n['brier'].mean(), ece=n['ece'].mean(),
                         simplicity_rank=M.SIMPLICITY_RANK[f], seconds_to_score_1000=inf))
sel = pd.DataFrame(sel_rows).set_index('family')
best_f = sel['nested_auc'].idxmax(); thr = sel.loc[best_f, 'nested_auc'] - sel.loc[best_f, 'auc_sd']
sel['within_1sd_of_best'] = sel['nested_auc'] >= thr
elig = sel[sel['within_1sd_of_best']].sort_values(['simplicity_rank', 'nested_auc'], ascending=[True, False])
chosen = elig.index[0]
sel['chosen'] = sel.index == chosen
display(sel.round(4)); sel.round(4).to_csv(f'{TB}/model_selection.csv')
print(f'best by mean AUC: {best_f} ({sel.loc[best_f, "nested_auc"]:.4f}, SD {sel.loc[best_f, "auc_sd"]:.4f}); eligibility threshold {thr:.4f}')
print('CHOSEN:', chosen)
"""))
C.append(N("s6"))

# ------------------------------------------------------------ 7 final evaluation
C.append(md("## 7. One-touch evaluation on the held-out test set"))
C.append(explain("Fit the chosen model on all training rows and score the 1,409 held-out customers once",
    "The test set is the only data that played no part in feature checks, model comparison, tuning or selection. One look gives an unbiased estimate of performance on new customers of the same kind. Rule for this section, fixed before the result: the test set is scored in one cell, once, for the chosen model and for the baselines (so they are compared on the same rows; no choice depends on these scores). **The model is called better than a baseline only if the 95% bootstrap interval of the paired difference in top-20% revenue capture (and in AUC) excludes zero.** Calibration is called acceptable if ECE is 0.05 or lower.",
    ["Report a cross-validation score only: honest for choosing, but it comes from rows that influenced choices.",
     "Refit on train plus test before reporting: gives a slightly better model, but leaves nothing to test on. Not done.",
     "A time-based holdout: not possible without a date column."],
    "The bootstrap resamples the 1,409 test customers with replacement 1,000 times and recomputes each metric; the 2.5th and 97.5th percentiles are the 95% interval, the range that would hold the true value in about 95 of 100 repeated studies of this size. With only about 374 leavers in the test set, intervals are wide (about +/-5 points for rates), and we show them. Reliability curve: customers are grouped by predicted risk; for each group the predicted rate is plotted against the actual rate; points on the diagonal mean calibrated. Decile table: customers ranked by score and cut into 10 equal groups; lift = group churn rate / overall churn rate (1.0 is average). Threshold table: for each cutoff, who would be flagged. Precision = flagged who leave / flagged; recall = leavers flagged / all leavers; false-positive rate = stayers flagged / all stayers.",
    "Compare each estimate with its interval and with the baselines. A point estimate whose interval overlaps a baseline's cannot be called better. Check that the reliability points sit near the diagonal."))
C.append(code("""
# ---- THE ONE TOUCH: the test rows are read here and scored once ----
test = df[df['split'] == 'test'].reset_index(drop=True)
Xte = test.drop(columns=[F.ID_COL, 'split', F.TARGET]); yte = test[F.TARGET]; rev_te = Xte['MonthlyCharges']
best = tuned[chosen]['best_params']
final = M.make_pipeline(chosen, best, 'eng', kept, n_jobs=4).fit(Xtr, ytr)
p_te = final.predict_proba(Xte)[:, 1]
rule2 = M.RuleSegmentRate(m=20).fit(Xtr, ytr); p_rule2 = rule2.predict_proba(Xte)[:, 1]
rule1 = M.RuleFlag().fit(Xtr, ytr); p_rule1 = rule1.predict_proba(Xte)[:, 1]
glm_raw = M.make_pipeline('glm', feature_set='raw').fit(Xtr, ytr); p_glm = glm_raw.predict_proba(Xte)[:, 1]
preds = {f'FINAL: {chosen}': p_te, 'Rule 1: m2m fiber first-year flag': p_rule1, 'Rule 2: segment churn rate': p_rule2, 'Logistic regression, raw columns': p_glm}
print('test customers', len(yte), '| leavers', int(yte.sum()), f'| lost monthly revenue in test ${float((rev_te*yte).sum()):,.0f}')
ci = {k: M.bootstrap_metrics(yte, p, rev_te) for k, p in preds.items()}
rows = []
for k, t in ci.items():
    for m in ['auc', 'pr_auc', 'top20_rev', 'top20_precision', 'top20_recall', 'brier', 'ece']:
        rows.append(dict(model=k, metric=m, estimate=t.loc[m, 'estimate'], ci_low=t.loc[m, 'ci_low_2.5%'], ci_high=t.loc[m, 'ci_high_97.5%']))
test_metrics = pd.DataFrame(rows); test_metrics.to_csv(f'{TB}/test_metrics.csv', index=False)
display(test_metrics.pivot(index='model', columns='metric', values='estimate').round(3))
display(ci[f'FINAL: {chosen}'].round(3))
diffs = []
for k in list(preds)[1:]:
    for m in ['top20_rev', 'auc']:
        e, lo, hi = M.paired_bootstrap(yte, p_te, preds[k], rev_te, m); diffs.append(dict(final_minus=k, metric=m, difference=e, ci_low=lo, ci_high=hi, excludes_zero=bool(lo > 0 or hi < 0)))
diffs = pd.DataFrame(diffs); diffs.to_csv(f'{TB}/test_paired_differences.csv', index=False); display(diffs.round(3))
"""))
C.append(N("s7a"))
C.append(md("### 7.2 Decile table, threshold table and charts\nHow to read (method as explained in section 7 above): in the decile table, compare `actual_churn_rate` with `mean_predicted_risk` row by row and read `lift_vs_base` as a multiple of the overall rate; in the threshold table, a higher cut-off flags fewer customers with higher precision and lower recall. Plain words: the lift and capture tables a retention team would use, and the charts for ranking, precision-recall, calibration and cut-off choice. All from the same single scoring of the test rows."))
C.append(code("""
dec = M.decile_table(yte, p_te, rev_te); thr_tbl = M.threshold_table(yte, p_te, rev_te)
dec.to_csv(f'{TB}/decile_table.csv', index=False); thr_tbl.to_csv(f'{TB}/threshold_table.csv', index=False)
display(dec.round(3)); display(thr_tbl.round(3))
from sklearn.metrics import roc_curve, precision_recall_curve
fig, ax = plt.subplots(2, 3, figsize=(17, 9))
for k, p in preds.items():
    fpr, tpr, _ = roc_curve(yte, p); ax[0, 0].plot(fpr, tpr, label=f'{k} (AUC {ci[k].loc["auc","estimate"]:.3f})')
    pr, rc, _ = precision_recall_curve(yte, p); ax[0, 1].plot(rc, pr, label=k)
ax[0, 0].plot([0, 1], [0, 1], 'k:'); ax[0, 0].set_xlabel('False-positive rate (stayers flagged)'); ax[0, 0].set_ylabel('Recall (leavers flagged)'); ax[0, 0].set_title('ROC curve, test set'); ax[0, 0].legend(fontsize=7)
ax[0, 1].axhline(yte.mean(), color='k', ls=':'); ax[0, 1].set_xlabel('Recall'); ax[0, 1].set_ylabel('Precision'); ax[0, 1].set_title(f'Precision-recall, test set (base rate {100*yte.mean():.1f}%)')
# reliability
q = pd.qcut(pd.Series(p_te).rank(method='first'), 10, labels=False); rel = pd.DataFrame({'p': p_te, 'y': yte.values, 'b': q}).groupby('b').agg(pred=('p', 'mean'), act=('y', 'mean'), n=('y', 'size'))
ax[0, 2].plot([0, 1], [0, 1], 'k:'); ax[0, 2].plot(rel['pred'], rel['act'], 'o-'); ax[0, 2].set_xlabel('Predicted churn probability (decile mean)'); ax[0, 2].set_ylabel('Actual churn rate'); ax[0, 2].set_title(f'Reliability curve (ECE {ci[f"FINAL: {chosen}"].loc["ece","estimate"]:.3f})')
rel.to_csv(f'{TB}/reliability_deciles.csv')
ax[1, 0].bar(dec['decile'], 100*dec['actual_churn_rate'], color='#3b6ea5'); ax[1, 0].axhline(100*yte.mean(), color='r', ls='--', label='overall rate')
for d, l in zip(dec['decile'], dec['lift_vs_base']): ax[1, 0].text(d, 100*dec.loc[d-1, 'actual_churn_rate'] + 1, f'{l:.1f}x', ha='center', fontsize=8)
ax[1, 0].set_xlabel('Risk decile (1 = highest predicted risk)'); ax[1, 0].set_ylabel('Actual churn rate (%)'); ax[1, 0].set_title('Churn rate and lift by decile, test set'); ax[1, 0].legend()
x = np.r_[0, dec['cum_share_customers']]; ax[1, 1].plot(x, np.r_[0, dec['cum_share_lost_revenue_captured']], 'o-', label='model: lost revenue'); ax[1, 1].plot(x, np.r_[0, dec['cum_share_leavers_captured']], 's-', label='model: leavers')
ax[1, 1].plot([0, 1], [0, 1], 'k:', label='random'); ax[1, 1].axvline(.2, color='gray', ls='--'); ax[1, 1].set_xlabel('Share of customers contacted (highest risk first)'); ax[1, 1].set_ylabel('Share captured'); ax[1, 1].set_title('Cumulative capture'); ax[1, 1].legend(fontsize=8)
g = np.linspace(0.02, 0.98, 49); tt = M.threshold_table(yte, p_te, rev_te, g)
ax[1, 2].plot(g, tt['precision'], label='precision'); ax[1, 2].plot(g, tt['recall'], label='recall'); ax[1, 2].plot(g, tt['share_flagged'], label='share flagged'); ax[1, 2].plot(g, tt['share_lost_revenue_captured'], label='lost revenue captured')
ax[1, 2].set_xlabel('Cut-off on predicted probability'); ax[1, 2].set_title('Threshold curves'); ax[1, 2].legend(fontsize=8)
plt.tight_layout(); plt.savefig(f'{CH}/evaluation_panel.png', dpi=105); plt.show()
# also single-purpose copies for the report
for nm, (a, b) in {'reliability_curve': (0, 2), 'decile_lift': (1, 0), 'threshold_curves': (1, 2)}.items():
    ext = ax[a, b].get_tightbbox(fig.canvas.get_renderer()).transformed(fig.dpi_scale_trans.inverted()).padded(0.03); fig.savefig(f'{CH}/{nm}.png', bbox_inches=ext, dpi=110)
"""))
C.append(N("s7b"))
C.append(explain("Performance inside segments, to check the model works for every group",
    "An overall AUC can hide a group where the model fails. The explorer named the segments that matter (contract, internet type, tenure, payment method, seniors) and gender is included as a fairness check. The question is whether ranking and calibration hold inside each.",
    ["Subgroup confidence intervals (bootstrap inside each segment): more rigorous about noise, but with 222 to 1,187 customers per segment the intervals are wide and would mostly say 'cannot tell'. Used only through the 100-row rule.",
     "Interaction tests (does the model's error depend on segment?): a formal test of fairness, but it needs a model of the errors and more leavers per cell than the test set has.",
     "Refit a model per segment: answers a different question (would a specialist model do better) and splits an already small sample."],
    "For each segment value we compute AUC inside the segment (the chance a leaver outranks a stayer among that segment's customers only), the actual churn rate, the mean predicted churn, and `gap_pts` = mean predicted % minus actual % (positive means the model over-predicts). Segments with fewer than 100 customers are flagged `small` and not interpreted, because a rate on under 100 customers has a margin of about +/-10 points, the handoff's own limit.",
    "Within-segment AUC is naturally lower than the overall AUC in a high-risk group, because customers there look alike; a drop to near 0.5 would signal a problem. `gap_pts` near zero (within about 3 points here) means the average prediction is right for the segment; a large gap means the model is systematically too high or too low there and would need recalibration."))
C.append(md("### 7.3 Performance inside segments\nPlain words: does the model work as well in the segments the explorer flagged (contract, internet type, tenure, payment method, seniors)? A model can be good overall and poor in one group. Segments with fewer than 100 test customers are marked and not interpreted, as the handoff warns."))
C.append(code("""
segs = {'Contract': Xte['Contract'], 'InternetService': Xte['InternetService'], 'Tenure': np.where(Xte['tenure'] <= 12, 'first 12 months', '13+ months'),
        'PaymentMethod': Xte['PaymentMethod'], 'SeniorCitizen': Xte['SeniorCitizen'].map({0: 'not senior', 1: 'senior'}), 'gender': Xte['gender']}
rows = []
for sname, s in segs.items():
    s = pd.Series(np.asarray(s), index=Xte.index)
    for v in sorted(s.unique()):
        m = (s == v).values; yy = yte.values[m]; pp = p_te[m]
        a = M.roc_auc_score(yy, pp) if 0 < yy.sum() < len(yy) else np.nan
        rows.append(dict(segment=sname, value=v, customers=int(m.sum()), leavers=int(yy.sum()), actual_churn_pct=100*yy.mean(), mean_predicted_pct=100*pp.mean(),
                         gap_pts=100*(pp.mean()-yy.mean()), auc_within_segment=a, top20_capture=M.topk_capture(yy, pp, rev_te.values[m]) if yy.sum() else np.nan, small=m.sum() < 100))
seg_tbl = pd.DataFrame(rows); seg_tbl.to_csv(f'{TB}/segment_performance.csv', index=False); display(seg_tbl.round(2))
print('overall AUC', round(ci[f'FINAL: {chosen}'].loc['auc', 'estimate'], 3))
"""))
C.append(N("s7c"))

# ------------------------------------------------------------ 8 explanation
C.append(md("## 8. Explanation: what drives the score, and what-if sensitivity"))
C.append(explain("Permutation importance and SHAP, grouped by original column",
    "A manager needs to know which customer facts the score leans on, in terms of the original columns, not 30 coded inputs. Two views guard against the quirks of either: permutation importance measures what the model loses without a column; SHAP measures how much each column moves individual predictions.",
    ["The model's own importance (tree gain or logistic weights): quick, but depends on the family and is biased toward many-valued columns.",
     "Partial-dependence plots: show the shape of one effect, but not how much it matters overall. Used implicitly through the what-if tests.",
     "Drop-column refits: the most direct, but 18 refits with noisy results at this sample size."],
    "**Permutation importance (on the test set):** shuffle one original column across customers, rebuild every engineered feature from the shuffled data (so derived features move with it), score again, and record the fall in AUC (and in top-20% revenue capture). Repeated 20 times; we report mean and SD. A bigger fall means the model relied on the column more. Correlated columns share credit, so a column can look unimportant when a near twin carries the same signal. **SHAP (SHapley Additive exPlanations):** for each customer, the prediction is split into additive contributions per input, $\\hat f(x)=\\phi_0+\\sum_j\\phi_j$, where $\\phi_0$ is the average prediction (log-odds scale) and each $\\phi_j$ is that input's average marginal contribution over all orders of adding inputs. We add the contributions of all inputs that come from the same original column (engineered features are credited to their primary source column: m2m_fiber, m2m_first_year and contract_ord to Contract; m2m_echeck to PaymentMethod; first_year and log_tenure to tenure; the protection features to OnlineSecurity or TechSupport; household_size to Partner), then average the absolute value over customers. **Classification of drivers** (structural: cannot be changed by the business; semi-controllable: can be influenced slowly or by pricing/product design; controllable: can be changed by an offer or a process) is a judgement made from the column meaning, not from data.",
    "Compare the two rankings. Columns that rank high in both are the robust drivers. Importance says how much the model uses a column, not that changing it would change churn."))
C.append(code("""
groups = F.RAW_COLS
perm = M.grouped_permutation_importance(final, Xte[F.RAW_COLS], yte.values, F.add_features, groups, n_repeats=20)
Zte, sv, shap_mean, signed = M.shap_values_by_group(final, F.add_features(Xte[F.RAW_COLS]), chosen)
shap_df = shap_mean.rename('mean_abs_shap').reset_index().rename(columns={'index': 'column'})
KIND = {'tenure': 'structural', 'SeniorCitizen': 'structural', 'gender': 'structural', 'Partner': 'structural', 'Dependents': 'structural',
        'InternetService': 'semi-controllable', 'MonthlyCharges': 'semi-controllable', 'PhoneService': 'semi-controllable', 'MultipleLines': 'semi-controllable',
        'Contract': 'controllable', 'PaymentMethod': 'controllable', 'PaperlessBilling': 'controllable', 'OnlineSecurity': 'controllable', 'OnlineBackup': 'controllable',
        'DeviceProtection': 'controllable', 'TechSupport': 'controllable', 'StreamingTV': 'controllable', 'StreamingMovies': 'controllable'}
drivers = perm.merge(shap_df, on='column', how='outer'); drivers['rank_perm'] = drivers['auc_drop_mean'].rank(ascending=False); drivers['rank_shap'] = drivers['mean_abs_shap'].rank(ascending=False)
drivers['driver_type'] = drivers['column'].map(KIND); drivers = drivers.sort_values('rank_shap'); drivers.to_csv(f'{TB}/driver_importance.csv', index=False)
display(drivers.round(4))
cols = {'structural': '#7f8c8d', 'semi-controllable': '#e67e22', 'controllable': '#2e86c1'}
fig, ax = plt.subplots(1, 2, figsize=(15, 6.5)); d = drivers.sort_values('auc_drop_mean')
ax[0].barh(d['column'], d['auc_drop_mean'], xerr=d['auc_drop_sd'], color=[cols[k] for k in d['driver_type']]); ax[0].set_xlabel('Fall in AUC when the column is shuffled (test set, 20 repeats)'); ax[0].set_title('Permutation importance')
d = drivers.sort_values('mean_abs_shap'); ax[1].barh(d['column'], d['mean_abs_shap'], color=[cols[k] for k in d['driver_type']]); ax[1].set_xlabel('Mean |SHAP| (log-odds), summed over engineered copies'); ax[1].set_title('SHAP importance')
from matplotlib.patches import Patch
ax[1].legend(handles=[Patch(color=v, label=k) for k, v in cols.items()], loc='lower right'); plt.tight_layout(); plt.savefig(f'{CH}/driver_importance.png', dpi=110); plt.show()
"""))
C.append(N("s8a"))
C.append(explain("What-if sensitivity for the controllable levers (an association, not a causal effect)",
    "Leadership wants to know which lever might be worth an offer. The model can say how its predicted risk changes if a lever were different, holding everything else as is. That is a model association, not what would happen: customers who chose a one-year contract may differ in ways the data does not record.",
    ["A randomised pilot (offer to a random half): the only way to measure a causal effect; it is the next step, not something this data can give.",
     "Causal models (uplift, double machine learning): need treatment-assignment data that is not in this snapshot.",
     "Read the coefficient or SHAP value of the column: shows model use, not the effect of changing the lever for a defined group."],
    "For each lever we pick the eligible customers in the test set (those who do not have the lever now), set the column to the target value, rebuild all engineered features, and re-score with the final model. Because the model also reads MonthlyCharges, and an add-on normally raises the bill, the two add-on levers are run twice: once with the bill unchanged and once with the bill raised by the add-on's typical price (estimated from the training rows by regressing the bill on the service mix). The other levers assume no price change. **(a) Where the add-on price comes from.** Fitted on training rows by ordinary least squares: $bill_i=b_0+\\sum_j b_j x_{ij}+e_i$, where $x_{ij}$ are 0/1 dummies for the levels of the nine service columns (phone service, multiple lines, internet type and the six add-ons) and $b_j$ is the dollars each level adds to the bill. The price step of an add-on is $\\hat b_{Yes}-\\hat b_{No}$ for that column. It proxies the list price because, across thousands of customers who differ in what they buy, the regression recovers what each service adds on average to the bill; it is an average, not a price list, and it is only as good as the bill being roughly additive in services. **(b) Why contract, payment and paperless levers keep the bill unchanged.** The data has no discount field, so any discount size would be invented. Holding the bill fixed isolates the effect of the switch itself. Real offers are often discounted, which would lower the bill; so these rows describe a no-discount switch, not a typical offer. **(c) Sensitivity.** The model reads MonthlyCharges, and in this logistic model its weight is negative when services are held fixed (see section 8), so any assumption about the bill moves the answer: the add-on levers differ by about 5 to 13 times between 'bill unchanged' and 'bill up by the add-on price'. A discounted-bill scenario would need the client's actual discount terms, entered as a negative `bill_delta` for the eligible customers, and, because a negative bill weight would wrongly make a discount look harmful, a model that separates price from service mix first (for example with the `price_resid` idea tested in notebook 02, which had no signal) before such a scenario could be trusted. Average change in predicted churn probability = mean over eligible customers of $\\hat p_{after}-\\hat p_{before}$, in percentage points. The 95% interval comes from 1,000 bootstrap resamples of the eligible customers. The revenue column is $\\sum_i(\\hat p_{after,i}-\\hat p_{before,i})\\times bill_i$ over eligible test customers: the model's change in expected monthly revenue lost, in dollars per month for those customers only (the test set is 20% of all customers). No cost, take-up or save rate is included, because the data does not contain them.",
    "A negative change means the model scores those customers as less likely to leave if they had the lever. The size says how far the model's score moves, not how many customers an offer would actually keep. A wide interval means the estimate is uncertain. Moving a customer to a contract the model has rarely seen for that profile (for example a very new customer on a two-year plan) makes the estimate less reliable."))
C.append(md("""**The levers tested** (eligible = test customers to whom the change applies; direction is what we expect from the exploration, not a result).

| lever | eligible customers | target value | bill treatment | expected direction and reason |
|---|---|---|---|---|
| Contract | month-to-month | One year | unchanged | lower risk: H1, month-to-month churn 42.7% against 11.3% for one year |
| PaymentMethod | electronic check | Bank transfer (automatic) | unchanged | lower risk: H4, electronic check 45.3% against 15% to 19% for automatic methods |
| TechSupport | internet customers without it | Yes | unchanged, then raised by estimated add-on price | lower risk: H5, 42% without against 15% with |
| OnlineSecurity | internet customers without it | Yes | unchanged, then raised by estimated add-on price | lower risk: chart 08, 42% without against 15% with |
| PaperlessBilling | customers on paperless billing | No | unchanged | lower risk if paperless is a sign of a less engaged customer; weak exploration link (33.6% against 16.3%) and the direction is a guess |"""))
C.append(code("""
Xr = Xte[F.RAW_COLS]
# list-price step of an add-on, estimated on TRAINING rows by regressing the bill on the service mix (F.ServiceAdjustedPrice)
sap = F.ServiceAdjustedPrice().fit(Xtr); coef = dict(zip(sap.cols_, sap.lr_.coef_))
step = lambda col: coef[f'{col}_Yes'] - coef[f'{col}_No']
print({c: round(step(c), 2) for c in ['TechSupport', 'OnlineSecurity']}, 'dollars per month added to the bill by the add-on (training-row regression)')
inet = (Xr['InternetService'] != 'No')
levers = [('Contract: month-to-month -> one year (bill unchanged)', (Xr['Contract'] == 'Month-to-month'), 'Contract', 'One year', 0.0),
          ('PaymentMethod: electronic check -> bank transfer (automatic) (bill unchanged)', (Xr['PaymentMethod'] == 'Electronic check'), 'PaymentMethod', 'Bank transfer (automatic)', 0.0),
          ('TechSupport: no -> yes, internet customers (bill unchanged)', inet & (Xr['TechSupport'] == 'No'), 'TechSupport', 'Yes', 0.0),
          ('TechSupport: no -> yes, internet customers (bill rises by add-on price)', inet & (Xr['TechSupport'] == 'No'), 'TechSupport', 'Yes', step('TechSupport')),
          ('OnlineSecurity: no -> yes, internet customers (bill unchanged)', inet & (Xr['OnlineSecurity'] == 'No'), 'OnlineSecurity', 'Yes', 0.0),
          ('OnlineSecurity: no -> yes, internet customers (bill rises by add-on price)', inet & (Xr['OnlineSecurity'] == 'No'), 'OnlineSecurity', 'Yes', step('OnlineSecurity')),
          ('PaperlessBilling: yes -> no (bill unchanged)', (Xr['PaperlessBilling'] == 'Yes'), 'PaperlessBilling', 'No', 0.0)]
cf = pd.DataFrame([dict(lever=n, bill_change_usd=b, **M.counterfactual(final, Xr, m.values, c, v, F.add_features, bill_delta=b)) for n, m, c, v, b in levers])
cf.to_csv(f'{TB}/counterfactual_levers.csv', index=False); display(cf.round(3))
fig, ax = plt.subplots(figsize=(12, 4.6)); y = np.arange(len(cf))[::-1]
ax.errorbar(cf['mean_change_pts'], y, xerr=[cf['mean_change_pts']-cf['ci_low_pts'], cf['ci_high_pts']-cf['mean_change_pts']], fmt='o', capsize=4)
ax.set_yticks(y); ax.set_yticklabels([f"{l} (n={n})" for l, n in zip(cf['lever'], cf['eligible'])], fontsize=8); ax.axvline(0, color='k', lw=1)
ax.set_xlabel('Change in predicted churn (points, 95% interval)'); ax.set_title('What-if sensitivity: a model association, not a causal effect', fontsize=11); plt.tight_layout(); plt.savefig(f'{CH}/counterfactual_levers.png', dpi=110); plt.show()
"""))
C.append(N("s8b"))

# ------------------------------------------------------------ 9 artifacts
C.append(md("## 9. Artifacts"))
C.append(md("Plain words: save the fitted model, its configuration, and one score for every customer. Customers in the training split get an out-of-fold score (from a model that never saw them, so it is an honest score); test customers get the held-out score. Then run the production pipeline script once to confirm it reproduces the model and the test result."))
C.append(code("""
joblib.dump(final, f'{PROJECT}/models/churn_driver_diagnostic_model.joblib')
cfg = dict(family=chosen, params=best, kept=kept, feature_set='eng', seed=SEED); json.dump(cfg, open(f'{PROJECT}/models/final_config.json', 'w'), indent=1, default=float)
from sklearn.model_selection import StratifiedKFold
sp5 = list(StratifiedKFold(5, shuffle=True, random_state=SEED + 3).split(np.zeros(len(ytr)), ytr))
oof = M.oof_predictions(M.make_pipeline(chosen, best, 'eng', kept, n_jobs=4), Xtr, ytr, sp5)
sc = pd.concat([pd.DataFrame({F.ID_COL: train[F.ID_COL], 'split': 'train', 'score_type': 'out_of_fold', 'churn_risk': oof, F.TARGET: ytr, 'MonthlyCharges': train['MonthlyCharges']}),
                pd.DataFrame({F.ID_COL: test[F.ID_COL], 'split': 'test', 'score_type': 'held_out_test', 'churn_risk': p_te, F.TARGET: yte, 'MonthlyCharges': test['MonthlyCharges']})], ignore_index=True)
sc['risk_rank'] = sc['churn_risk'].rank(method='first', ascending=False).astype(int)
sc['risk_decile'] = pd.qcut(sc['risk_rank'], 10, labels=range(1, 11)).astype(int)   # 1 = highest risk 10%
sc.sort_values('risk_rank').to_csv(f'{PROJECT}/reports/modeling/scores.csv', index=False)
print('scores.csv', sc.shape, '| out-of-fold AUC on training rows', round(M.roc_auc_score(ytr, oof), 4))
display(sc.groupby('risk_decile').agg(customers=(F.TARGET, 'size'), actual_churn_rate=(F.TARGET, 'mean'), mean_risk=('churn_risk', 'mean'), monthly_revenue=('MonthlyCharges', 'sum')).round(3))
out = subprocess.run([sys.executable, '-I', f'{PROJECT}/src/pipeline.py', '--train', '--evaluate'], capture_output=True, text=True); print(out.stdout[-1500:]); print(out.stderr[-500:] if out.returncode else 'pipeline.py exit code 0')
pipe_eval = pd.read_csv(f'{TB}/pipeline_evaluation.csv', index_col=0)
print('notebook test AUC', round(ci[f'FINAL: {chosen}'].loc['auc', 'estimate'], 6), '| pipeline.py test AUC', round(pipe_eval.loc['auc', 'estimate'], 6))
"""))
C.append(N("s9"))

# ------------------------------------------------------------ 10 model card
C.append(md("## 10. Model card"))
C.append(md("Plain words: write `model_card.md`, a plain-language description for a non-technical reader followed by a technical appendix with the full tables. All numbers come from the variables above."))
C.append(code(open(os.path.join(os.path.dirname(__file__), "model_card_cell.py")).read()))
C.append(N("s10"))
C.append(md("## 11. Files written\nThe cell below lists every file this notebook wrote and checks that each exists."))
C.append(code("""
import glob
for pat in ['reports/modeling/*.md', 'reports/modeling/*.csv', 'reports/modeling/*.parquet', 'reports/modeling/tables/*.csv', 'reports/modeling/charts/*.png', 'models/*']:
    for f in sorted(glob.glob(f'{PROJECT}/{pat}')): print(os.path.relpath(f, PROJECT))
"""))
C.append(md("The list is the full set of deliverables: model card, tuning report, features table (from notebook 02), scores, tables, charts, the fitted model, its configuration and the Optuna study databases."))
save(C, f"{PROJECT}/notebooks/03_modeling.ipynb")
print("built", len(C), "cells")
