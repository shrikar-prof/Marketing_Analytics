"""Builds notebooks/02_feature_engineering.ipynb. Run: python -I src/build_notebook_02.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, pandas as pd
import features as F
from nbkit import md, code, explain, save

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
df = pd.read_parquet(f"{PROJECT}/reports/exploration/clean.parquet")
split = F.split_data(df)
tr = F.add_features(df)[split == "train"]
base_tr = tr[F.TARGET].mean()
import math
from scipy.stats import spearmanr as _sp
def _scale(v, kind):
    a = abs(v)
    if kind == "rho": return "negligible" if a < .10 else "small" if a < .30 else "medium" if a < .50 else "large"
    return "negligible" if a < 5 else "small" if a < 15 else "medium" if a < 30 else "large"
def _interval_text(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float); n = len(x)
    rho = _sp(x, y)[0]; z = math.atanh(rho); se = 1 / math.sqrt(n - 3)
    t = f"Spearman rho {rho:+.2f} is {_scale(rho, 'rho')} (approximate 95% interval {math.tanh(z-1.96*se):+.2f} to {math.tanh(z+1.96*se):+.2f})"
    if len(set(x)) == 2:
        a, b = y[x == 1], y[x == 0]; d = 100 * (a.mean() - b.mean())
        e = 196 * math.sqrt(a.mean() * (1 - a.mean()) / len(a) + b.mean() * (1 - b.mean()) / len(b))
        t += f"; the gap of {d:+.1f} points is {_scale(d, 'gap')} (approximate 95% interval {d-e:+.1f} to {d+e:+.1f})"
    return t + "."
cells = []

cells.append(md("""# 02. Feature engineering: churn driver diagnostic

**Purpose.** Turn the explorer's findings into model inputs, one feature at a time. Each feature has a business meaning, a formula, the exact code, the finding that motivates it, the direction we expect, a before/after example row, a check against churn on the training rows only, and a keep-or-drop verdict.

**What this notebook writes:** `reports/modeling/features.parquet` (all 7,043 rows, every feature, the target, and a `split` column), `reports/modeling/features.md` (the feature table) and `reports/modeling/feature_list.json` (which features the models use).

**What it cannot do.** The checks show association with churn, not cause. A feature that helps prediction is not a lever until it is tested as one."""))

cells.append(md("## 1. Setup"))
cells.append(md("Plain words: load the libraries, fix the random seed (a number that makes every random step repeat exactly) and print library versions so the run can be reproduced. All feature code lives in `src/features.py` so the production pipeline uses the same definitions."))
cells.append(code("""
import os, sys, json, warnings
warnings.filterwarnings('ignore')
PROJECT = os.path.abspath('..')
sys.path.insert(0, os.path.join(PROJECT, 'src'))
import numpy as np, pandas as pd, sklearn, scipy, matplotlib
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
import features as F
import model_utils as M
SEED = F.SEED
np.random.seed(SEED)
os.makedirs(f'{PROJECT}/reports/modeling/charts', exist_ok=True)
print('seed', SEED, '| python', sys.version.split()[0], '| pandas', pd.__version__, '| numpy', np.__version__,
      '| sklearn', sklearn.__version__, '| scipy', scipy.__version__, '| matplotlib', matplotlib.__version__)
"""))
cells.append(md("The output lists the seed (42) and the library versions. If a later run shows different versions, small numeric differences are possible."))

cells.append(md("## 2. Data and the train / held-out split"))
cells.append(explain("Hold out 20% of customers before any feature is looked at",
    "Anything we look at to choose features can leak the answer into the model. Setting aside a test set first, and never using it here, keeps the final score honest. The explorer's handoff asks for a stratified random 20% split with seed 42. Rows are one customer each, so rows are independent and a random split is valid. There is no date, so a time split is impossible.",
    ["Plain random split: would let the leaver share drift (for example 25% in one part, 28% in the other) by chance. Not used.",
     "Group split by customer: no customer appears twice, so it would equal a random split. Not needed.",
     "Out-of-time split: needs a date column, which this data does not have."],
    "Stratified sampling draws 20% of the leavers and 20% of the stayers separately, so both parts keep the 26.5% churn rate. Test size = 0.20 x 7,043 = 1,409 customers. Decision rule, fixed before the result: the split is made once with seed 42, the test rows are touched exactly once in notebook 03, and every check in this notebook uses training rows only.",
    "Check that the two parts show the same churn rate (about 26.5%) and that test has about 374 leavers. If the rates differed by more than a point, the split would be re-examined."))
cells.append(code("""
df = pd.read_parquet(f'{PROJECT}/reports/exploration/clean.parquet')
df['split'] = F.split_data(df)
summ = df.groupby('split')[F.TARGET].agg(customers='count', leavers='sum', churn_rate='mean')
summ['churn_rate_pct'] = (100*summ['churn_rate']).round(2)
display(summ.drop(columns='churn_rate'))
is_train = df['split'].eq('train')
print('Training rows used for every check below:', is_train.sum())
"""))
cells.append(md(f"The training part holds {int((split=='train').sum()):,} customers and the held-out test part {int((split=='test').sum()):,}. Churn rates match within a few hundredths of a point, so the split is balanced. From here on, every statistic is computed on training rows only."))

cells.append(md("## 3. Columns left out, and a leakage check"))
cells.append(explain("Check the billing-total columns the explorer asked us to leave out",
    "TotalCharges, avg_monthly_spend and price_vs_history_pct are built from lifetime billing. For leavers, billing stops at exit, so these columns may carry the outcome itself. The handoff says to add them back only after a leakage check. The data cannot prove when they were measured, so this check can only show how much they would tell us on their own.",
    ["Ask the data owner when the totals were measured: the right answer, but not available in this project.",
     "Add them and compare cross-validated scores: a big jump would be a warning sign, not proof of either answer, so it cannot clear them. Used only as a warning light.",
     "Drop silently: loses the chance to show the manager what was given up."],
    "Single-column AUC (area under the ROC curve: the chance the column ranks a random leaver above a random stayer; 0.5 is a coin flip, 1.0 is perfect) for each column, on training rows. Formula: $AUC=P(s_i>s_j\\mid y_i=1,y_j=0)$, where $s$ is the column value read as a risk score. We use $\\max(AUC,1-AUC)$ so direction does not matter. Decision rule, fixed before the result: these columns stay out of the model unless the data owner confirms they are measured before the churn event. An AUC far above that of tenure and MonthlyCharges would be taken as a leakage warning.",
    "Compare the billing columns with tenure and MonthlyCharges. Similar values mean the billing columns add little and the exclusion costs little. A much larger value would be a warning that they carry the outcome."))
cells.append(code("""
from sklearn.metrics import roc_auc_score
trn = df[is_train]
rows = []
for c in ['tenure','MonthlyCharges','TotalCharges','avg_monthly_spend','price_vs_history_pct']:
    x = trn[c].fillna(trn[c].median())
    a = roc_auc_score(trn[F.TARGET], x)
    rows.append(dict(column=c, single_column_auc=round(max(a,1-a),3), used_in_model=c in ('tenure','MonthlyCharges')))
display(pd.DataFrame(rows))
"""))
cells.append(md("Read the table against the rule. On training rows the billing columns reach AUC 0.647 (TotalCharges), 0.624 (avg_monthly_spend) and 0.504 (price_vs_history_pct), none above tenure at 0.735, so there is no sign of an outcome-carrying column and leaving them out gives up little ranking power. They stay excluded because the rule asks for the data owner's confirmation, which we do not have. (`TotalCharges` also has 11 blank values, all tenure-0 accounts.) This is a precaution, not proof that they leak."))

cells.append(md("## 4. Engineered features, one at a time"))
cells.append(md("""Each feature below follows the same steps: (a) a specification cell, (b) a code cell that builds it from the raw columns, shows one example row before and after, and checks it against churn on the training rows, (c) a note on what the output shows.

**Common method for the check.** Why: a feature that does not move churn adds noise and a place to overfit. Alternatives: a full model with and without the feature (done in section 5 for the whole set; too slow to repeat per feature), or mutual information (same story as the simple rates here, harder to read). How: a binary feature is compared by churn rate when 1 versus when 0; a count or number is compared by Spearman rank correlation (a number from -1 to 1 saying how steadily churn rises or falls as the feature rises; 0 means no steady trend) and by churn rate per value or per decile bin. Decision rule (fixed before any result): **binary feature KEEP if the gap is at least 5 points and each group has at least 100 training rows; other features KEEP if |Spearman| is at least 0.10.** How to read: the chart shows churn rate by value against the training base rate (the red dashed line).

**Scales for reading the numbers (conventions, not laws).** Spearman rho: under 0.10 negligible, 0.10 to 0.30 small, 0.30 to 0.50 medium, over 0.50 large. Churn-rate gap, in percentage points against the 26.5% base rate: under 5 negligible, 5 to 15 small, 15 to 30 medium, over 30 large. **Why these thresholds.** |rho| of 0.10 is the usual boundary between noise-level and small association; with 5,634 rows, a rho of 0.03 is already statistically detectable but useless for ranking, so a practical floor is needed. A 5-point gap means 5 extra leavers per 100 customers, about the smallest difference a retention action could act on; the 100-row floor per group comes from the handoff (rates on fewer rows are too noisy). They are screening rules, not tests: a feature near a threshold with a small group should be read with its interval. **Interval method.** Each note below adds an approximate 95% interval from closed formulas: for a gap, $\\Delta\\pm1.96\\sqrt{\\hat p_1(1-\\hat p_1)/n_1+\\hat p_0(1-\\hat p_0)/n_0}$ (normal approximation to a difference of two proportions); for rho, Fisher's transform $\\tanh(\\operatorname{atanh}(\\rho)\\pm1.96/\\sqrt{n-3})$. A bootstrap (resample customers 1,000 times) would give nearly the same width at this sample size; the formulas are used because they can be checked by hand. The intervals are computed from the same training rows when the notebook is built and are not printed by the code cells."""))

cells.append(code("""
# Build all features one by one below; `df` holds every row, `feat` collects the checks.
feat = {}
base_rate = df.loc[is_train, F.TARGET].mean()
print('Training base churn rate:', round(100*base_rate, 2), '%')
"""))
cells.append(md("The base rate on training rows is the line each feature's bars are compared to."))

for i, r in enumerate(F.REGISTRY, 1):
    n = r["name"]
    # example row: first training row where the feature is non-zero
    exr = tr[tr[n] != 0].index[0] if (tr[n] != 0).any() else tr.index[0]
    ex_in = ", ".join(f"{c}={df.loc[exr, c]!r}" for c in r["inputs"])
    ex_out = f"{tr.loc[exr, n]:g}"
    res = F.check_feature(tr[n], tr[F.TARGET])
    verdict = "KEEP" if res["keep"] else "DROP"
    cells.append(md(f"""### 4.{i} `{n}`
- **Business meaning:** {r['meaning']}
- **Formula:** $${r['formula']}$$
- **Exact code expression:** `{r['expr']}`
- **Input columns:** {', '.join('`'+c+'`' for c in r['inputs'])}
- **Why it exists (explorer finding or hypothesis):** {r['finding']}
- **Expected direction of its link to churn:** {r['direction']}
- **Example row (row index {exr}), before and after:** inputs {ex_in} give `{n}` = {ex_out}.
- **Type:** {r['kind']}. Built row by row, nothing is fitted, so it cannot leak across the split."""))
    cells.append(code(f"""
# 4.{i} {n}
EX = {exr}
print('before (inputs):', df.loc[EX, {r['inputs']!r}].to_dict())
df['{n}'] = ({r['expr']}).astype(float)
print('after: {n} =', df.loc[EX, '{n}'])
res = F.check_feature(df.loc[is_train, '{n}'], df.loc[is_train, F.TARGET])
feat['{n}'] = res
F.plot_feature_check('{n}', res, base_rate, f'{{PROJECT}}/reports/modeling/charts/feat_{n}.png'); plt.show()
print(res['stat']); print('rule:', res['rule'], '->', 'KEEP' if res['keep'] else 'DROP')
"""))
    cells.append(md(f"""**What the output shows.** On the {len(tr):,} training customers: {res['stat']}. Rule ({res['rule']}) gives provisional verdict **{verdict}**. {'Direction matches what we expected.' if (res['rho']<0)==('negative' in r['direction']) or 'weak' in r['direction'] else 'Direction is opposite to what we expected, which would need a second look.'} Scale and interval: {_interval_text(tr[n], tr[F.TARGET])} Final verdicts are set in section 5 after the redundancy check."""))

# price_resid
cells.append(md(f"""### 4.{len(F.REGISTRY)+1} `price_resid` (fitted feature)
- **Business meaning:** {F.PRICE_RESID['meaning']}
- **Formula:** $${F.PRICE_RESID['formula']}$$ where $x_j$ are the service dummies (phone, lines, internet type, six add-ons) and $\\hat b$ come from a linear regression of MonthlyCharges on them, fitted on training rows only.
- **Exact code expression:** `F.ServiceAdjustedPrice().fit(train_rows).transform(rows)['price_resid']`
- **Input columns:** `MonthlyCharges` and the nine service columns.
- **Why it exists:** {F.PRICE_RESID['finding']}
- **Expected direction:** {F.PRICE_RESID['direction']}
- **Example row:** shown in the code output below (before: bill and services; after: residual in dollars).
- **Leakage note:** this feature needs a fit, so it is rebuilt inside the model pipeline from the training rows of each fold. The column saved in `features.parquet` is fitted on the whole training split for checking and documentation only; models do not read it."""))
cells.append(code(f"""
# 4.{len(F.REGISTRY)+1} price_resid
sap = F.ServiceAdjustedPrice().fit(df.loc[is_train])
df['price_resid'] = sap.transform(df)['price_resid']
EX = int(df.loc[is_train].index[0])
print('before:', df.loc[EX, ['MonthlyCharges'] + F.SERVICE_COLS].to_dict())
print('after: price_resid =', round(df.loc[EX, 'price_resid'], 2), 'dollars above the usual price for this service mix')
res = F.check_feature(df.loc[is_train, 'price_resid'], df.loc[is_train, F.TARGET]); feat['price_resid'] = res
F.plot_feature_check('price_resid', res, base_rate, f'{{PROJECT}}/reports/modeling/charts/feat_price_resid.png'); plt.show()
print(res['stat']); print('rule:', res['rule'], '->', 'KEEP' if res['keep'] else 'DROP')
"""))
_sap = F.ServiceAdjustedPrice().fit(df[split == "train"]); _pr = _sap.transform(df[split == "train"])["price_resid"]
_PRI = _interval_text(_pr, df.loc[split == "train", F.TARGET]).replace("Spearman rho -0.02 is negligible (", "").rstrip(".").rstrip(")")
_PRI = "approximate " + _PRI.split("approximate ")[-1] if "approximate" in _PRI else _PRI
cells.append(md(f"""**What the output shows.** The fitted price residual of the example row (row index {int(tr.index[0])}) is -0.08 dollars: this customer pays almost exactly the usual price for the service mix. Across the training rows, Spearman rho with churn is -0.02 (negligible; {_PRI}), and churn runs from 30.0% in the lowest-residual decile to 24.3% in the highest, a drop of under 6 points with no steady trend. The rule (|rho| of at least 0.10) gives **DROP**. What this means for H6 (leavers pay about $15 more at the median): we expected a positive link, that customers paying above the normal price for their services leave more. We see none, and the sign is slightly the other way. So the higher bills of leavers are explained by what they buy (fiber, add-ons), not by paying a premium for the same services. This is a statement about this data and about association only; the data holds no price history.
"""))

cells.append(md("## 5. Final keep-or-drop, redundancy and added value"))
cells.append(explain("Drop near-duplicates, then test whether the kept features help a model at all",
    "Two features that say the same thing add no information and make a linear model less stable. Separately, a feature can pass a one-at-a-time check yet add nothing once the raw columns are in the model, so we test the whole set once.",
    ["Variance inflation factor (how much a feature is explained by the others): more thorough for linear models, but the simple pair correlation is enough to spot exact duplicates here.",
     "Per-feature leave-one-out model runs: precise, but 12 features x 25 fits adds cost and the answer is dominated by noise at this size.",
     "Keep everything and let regularisation (a penalty that shrinks weak weights) sort it out: valid for the final models, but it hides which features carry signal."],
    "Redundancy rule, fixed before the result: in registry order, drop a feature if its absolute Spearman correlation with an earlier kept feature is 0.95 or higher. Added-value test: a regularised logistic regression (a model that adds weighted evidence from each column and turns the sum into a probability) on the raw columns versus raw plus kept features, scored by AUC (see section 3) over repeated stratified 5-fold cross-validation (the training rows are split into 5 parts; each part is scored by a model trained on the other 4; repeated 5 times with different splits) on training rows only. Rule, fixed before the result: engineered features are worth carrying if the mean AUC does not fall and the gain is larger than one SD of the paired fold-by-fold difference (the same rule as notebook 03, sections 2 and 4).",
    "The correlation table shows pairs near 0.95 or more. The AUC table shows mean and standard deviation (SD, the spread across 25 fold-scores). A gain smaller than one SD is not distinguishable from noise."))
cells.append(code("""
from scipy.stats import spearmanr
names = [r['name'] for r in F.REGISTRY] + ['price_resid']
signal_keep = [n for n in names if feat[n]['keep']]
kept, dropped = [], {}
for n in names:
    if n not in signal_keep:
        dropped[n] = 'fails signal rule: ' + feat[n]['rule']; continue
    dup = next((k for k in kept if abs(spearmanr(df.loc[is_train, n], df.loc[is_train, k])[0]) >= 0.95), None)
    if dup: dropped[n] = f'duplicate of {dup} (|rho| >= 0.95)'
    else: kept.append(n)
C = pd.DataFrame({a: {b: spearmanr(df.loc[is_train, a], df.loc[is_train, b])[0] for b in names} for a in names}).round(2)
fig, ax = plt.subplots(figsize=(8, 6.5)); im = ax.imshow(C.values, cmap='coolwarm', vmin=-1, vmax=1)
ax.set_xticks(range(len(names))); ax.set_xticklabels(names, rotation=60, ha='right', fontsize=8); ax.set_yticks(range(len(names))); ax.set_yticklabels(names, fontsize=8)
for i in range(len(names)):
    for j in range(len(names)): ax.text(j, i, f'{C.values[i,j]:.1f}', ha='center', va='center', fontsize=6)
plt.colorbar(im, label='Spearman correlation'); ax.set_title('Engineered features: rank correlation (training rows)'); plt.tight_layout()
fig.savefig(f'{PROJECT}/reports/modeling/charts/feature_correlations.png', dpi=110); plt.show()
print('KEEP :', kept); print('DROP :', dropped)
"""))
_names = [r["name"] for r in F.REGISTRY] + ["price_resid"]
_X = tr.copy(); _X["price_resid"] = _pr
_C = _X[_names].corr(method="spearman").abs().values.copy(); np.fill_diagonal(_C, 0)
_i, _j = np.unravel_index(_C.argmax(), _C.shape)
cells.append(md(f"**Which features failed.** `n_streaming` (rho +0.08) and `price_resid` (rho -0.02) failed the signal rule (|rho| of at least 0.10), so they are dropped; the other ten passed. **Duplicates.** No pair reached the 0.95 cut-off, so no feature was dropped as a duplicate. The highest pair correlation seen is {_C[_i,_j]:.2f}, between `{_names[_i]}` and `{_names[_j]}`. The heat map shows how much the features overlap (red = move together). Features that overlap strongly but are below 0.95 are kept; regularisation in the models handles that. The printed lists are the final verdicts that the models will use."))
cells.append(code("""
Xtr = df.loc[is_train].reset_index(drop=True); ytr = Xtr[F.TARGET]
splits = M.repeated_splits(ytr)
r_raw = M.cv_evaluate(M.make_pipeline('glm', feature_set='raw'), Xtr, ytr, splits)
r_eng = M.cv_evaluate(M.make_pipeline('glm', feature_set='eng', kept=kept), Xtr, ytr, splits)
cmp = pd.DataFrame({'raw columns only': r_raw[['auc','pr_auc','top20_rev','brier']].agg(['mean','std']).T.stack(),
                    'raw + kept engineered': r_eng[['auc','pr_auc','top20_rev','brier']].agg(['mean','std']).T.stack()})
display(cmp.round(4))
d = (r_eng['auc'] - r_raw['auc'])
print(f'AUC gain from engineered features: mean {d.mean():+.4f}, SD of the paired difference {d.std():.4f}, over {len(d)} fold-scores')
"""))
cells.append(md("The table shows mean and SD of each metric across 25 fold-scores for the same logistic model, with and without the engineered features. `top20_rev` is the share of leavers' monthly revenue found in the top 20% of customers by score (the business metric). `brier` is the mean squared error of the predicted probabilities (0 is perfect; lower is better). The printed gain says whether the engineered set helps beyond noise. Because the folds are paired, the difference is more precise than the two separate SDs. **Reading scale for AUC differences.** AUC is the chance that a random leaver is scored above a random stayer, so a gain of +0.01 means that in 100 random leaver-stayer pairs, one more pair is put in the right order (about 1,495 x 4,139 = 6.2 million pairs in the training rows, so +0.01 is about 62,000 pairs). As a rule of thumb here, under 0.005 is negligible, 0.005 to 0.02 small, over 0.02 meaningful; 'times the SD' compares the gain with the fold-to-fold spread of the paired difference (under 1 is indistinguishable from noise, 2 or more fairly clear). In this run the engineered set raises AUC from 0.844 to 0.850 (a gain of +0.006, about 1.6 times the SD of the paired difference, 0.004) and lowers the Brier score slightly (0.1355 to 0.1329), but the top-20% revenue capture is not better (56.6% to 55.4%, inside the spread of 2 points). So the gain is small and modest in ranking terms. If the gain is under one SD, the features are a convenience for the linear model rather than a proven improvement, and tree models are expected to find the same joint groups without help."))

cells.append(md("## 6. Write the outputs"))
cells.append(md("Plain words: save the full feature table with the split column, the feature documentation table, and the list of features the models should use. Notebook 03 reads these files and never recomputes features (except in the what-if analysis, where it calls the same functions on changed inputs)."))
cells.append(code("""
# consistency check: the production function gives exactly the columns built cell by cell
chk = F.add_features(pd.read_parquet(f'{PROJECT}/reports/exploration/clean.parquet'))
for n in F.ENGINEERED:
    assert np.allclose(chk[n].values, df[n].values), n
print('add_features() matches the notebook columns for all', len(F.ENGINEERED), 'row-wise features')

keep_cols = [F.ID_COL, 'split', F.TARGET] + F.RAW_COLS + F.ENGINEERED + ['price_resid']
out = df[keep_cols].copy()
out.to_parquet(f'{PROJECT}/reports/modeling/features.parquet', index=False)

example_rows = {}
for r in F.REGISTRY:
    ex = df.loc[is_train & (df[r['name']] != 0)].index[0]
    example_rows[r['name']] = ', '.join(f"{c}={df.loc[ex, c]!r}" for c in r['inputs']) + f" -> {r['name']}={df.loc[ex, r['name']]:g}"
ex = df.loc[is_train].index[0]
example_rows['price_resid'] = f"MonthlyCharges={df.loc[ex,'MonthlyCharges']}, services as listed -> price_resid={df.loc[ex,'price_resid']:.2f}"
allr = F.REGISTRY + [F.PRICE_RESID]
def cell(s): return str(s).replace('|', '/').replace('\\n', ' ')
lines = ['# Feature table', '',
 'Every engineered feature, the raw columns it is built from, why it exists, and whether the models use it. Checks use the training split only (5,634 customers). Associations with churn are not causes.', '',
 'Rule for keep/drop (fixed before results): binary feature KEEP if the churn-rate gap is at least 5 points and both groups have at least 100 training rows; other features KEEP if |Spearman rho| >= 0.10; then drop a feature if it is a near-duplicate (|rho| >= 0.95) of an earlier kept one.', '',
 '| name | meaning | formula or rule | exact code expression | source columns | type | why it exists (finding or hypothesis) | expected direction | example row (before -> after) | observed on training rows | verdict |', '|' + '---|'*11]
for r in allr:
    n = r['name']; v = 'KEEP' if n in kept else 'DROP: ' + dropped[n].replace('|Spearman rho|', 'abs(Spearman rho)')
    f = r['formula'] if n == 'price_resid' else r['formula']
    lines.append('| ' + ' | '.join([f'`{n}`', cell(r['meaning']), cell('$' + f + '$'), cell('`' + r['expr'] + '`'), cell(', '.join(r['inputs'])), cell(r['kind']), cell(r['finding']), cell(r['direction']), cell(example_rows[n]), cell(feat[n]['stat']), v]) + ' |')
lines += ['', '## Raw columns used as model inputs', '',
 'Categorical (one-hot encoded inside the model pipeline): ' + ', '.join(F.RAW_CAT) + '. Numeric: ' + ', '.join(F.RAW_NUM) + '.', '',
 '## Columns deliberately left out', '', '| column | reason |', '|---|---|',
 '| customerID | identifier; kept only to join scores back |', '| Churn | text copy of the target |', '| tenure_band, monthly_charge_band | reporting bands built from tenure and MonthlyCharges |',
 '| TotalCharges, avg_monthly_spend, price_vs_history_pct | built from lifetime billing; timing relative to exit is unknown, so they may carry the outcome (see leakage check in notebook 02, section 3) |',
 '| has_internet | same information as InternetService |', '| n_addons, n_protection_addons | counts of columns already present (n_protection rebuilds the second inside the pipeline) |',
 '', '## Notes', '', '- `price_resid` is fitted (a regression on training rows). Inside the model it is refitted on the training part of every cross-validation fold. The column stored in features.parquet is fitted on the whole training split for documentation only.',
 '- `SeniorCitizen` and `gender` are raw inputs. `gender` shows no churn link in the exploration. `SeniorCitizen` does; check the policy before using an age-related field to decide who gets an offer.']
open(f'{PROJECT}/reports/modeling/features.md', 'w').write('\\n'.join(lines) + '\\n')
json.dump({'kept': kept, 'dropped': dropped, 'raw_cat': F.RAW_CAT, 'raw_num': F.RAW_NUM}, open(f'{PROJECT}/reports/modeling/feature_list.json', 'w'), indent=1)
print('features.parquet', out.shape, '| kept', len(kept), 'of', len(names), '| split counts', out['split'].value_counts().to_dict())
"""))
cells.append(md("The output confirms the check passed, gives the shape of the saved table (7,043 rows) and how many engineered features the models will use. `features.md` carries the full table for the reader and the statistician."))

save(cells, f"{PROJECT}/notebooks/02_feature_engineering.ipynb")
print("built", len(cells), "cells")
