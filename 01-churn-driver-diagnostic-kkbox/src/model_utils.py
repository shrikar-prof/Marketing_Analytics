"""Shared modeling code: pipelines, metrics, cross-validation, Optuna tuning, tables.
Used by notebooks/03_modeling.ipynb and src/pipeline.py."""
import json, math, os, time, warnings
import numpy as np
import pandas as pd
import optuna
from joblib import Parallel, delayed
from sklearn.base import BaseEstimator, ClassifierMixin, clone
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

import features as F

warnings.filterwarnings("ignore")
optuna.logging.set_verbosity(optuna.logging.WARNING)
SEED = F.SEED
PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_DIR = os.path.join(PROJECT, "models")
REPORT_DIR = os.path.join(PROJECT, "reports", "modeling")
SIMPLICITY_RANK = {"glm": 1, "lgbm": 2, "xgb": 2, "rf": 3, "catboost": 3}
FAMILIES = ["glm", "rf", "lgbm", "xgb", "catboost"]


# ---------------------------------------------------------------- data
def load_features():
    df = pd.read_parquet(os.path.join(REPORT_DIR, "features.parquet"))
    return df


def load_feature_list():
    with open(os.path.join(REPORT_DIR, "feature_list.json")) as f:
        return json.load(f)


# ---------------------------------------------------------------- baselines
class RuleFlag(BaseEstimator, ClassifierMixin):
    """Manager rule: score 1 for month-to-month fiber customers in their first 12 months, else 0. Nothing is fitted."""
    def fit(self, X, y=None):
        self.classes_ = np.array([0, 1]); return self
    def predict_proba(self, X):
        s = ((X["Contract"] == "Month-to-month") & (X["InternetService"] == "Fiber optic") & (X["tenure"] <= 12)).astype(float).values
        return np.c_[1 - s, s]


class RuleSegmentRate(BaseEstimator, ClassifierMixin):
    """Explorer's ranking rule: churn rate of the contract x internet x first-year segment, learned on training rows only.
    Rates are shrunk toward the overall rate with `m` pseudo-customers so tiny segments do not get extreme scores."""
    def __init__(self, m=20):
        self.m = m
    def _key(self, X):
        return X["Contract"].astype(str) + "|" + X["InternetService"].astype(str) + "|" + (X["tenure"] <= 12).astype(str)
    def fit(self, X, y):
        y = np.asarray(y); self.prior_ = y.mean()
        g = pd.DataFrame({"k": self._key(X).values, "y": y}).groupby("k")["y"].agg(["sum", "count"])
        self.rate_ = ((g["sum"] + self.m * self.prior_) / (g["count"] + self.m)).to_dict()
        self.classes_ = np.array([0, 1]); return self
    def predict_proba(self, X):
        p = self._key(X).map(self.rate_).fillna(self.prior_).values.astype(float)
        return np.c_[1 - p, p]


# ---------------------------------------------------------------- pipelines
def column_sets(feature_set="eng", kept=None):
    """Return (cat_cols, num_cols, use_price) for 'raw' (18 raw columns) or 'eng' (raw + kept engineered features)."""
    cat, num = list(F.RAW_CAT), list(F.RAW_NUM)
    use_price = False
    if feature_set == "eng":
        kept = kept or []
        num += [k for k in kept if k in F.ENGINEERED]
        use_price = "price_resid" in kept
        if use_price:
            num.append("price_resid")
    return cat, num, use_price


def default_params(family):
    return {
        "glm": dict(C=1.0, penalty="l2", l1_ratio=None),
        "rf": dict(n_estimators=500, min_samples_leaf=5, max_features="sqrt", max_depth=None),
        "lgbm": dict(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=30, subsample=0.8, colsample_bytree=0.8, reg_lambda=1.0),
        "xgb": dict(n_estimators=300, learning_rate=0.03, max_depth=3, subsample=0.8, colsample_bytree=0.8, min_child_weight=3, reg_lambda=1.0),
        "catboost": dict(iterations=400, learning_rate=0.05, depth=4, l2_leaf_reg=3.0),
    }[family]


def make_clf(family, params, n_jobs=1, seed=SEED):
    p = dict(params)
    if family == "glm":
        if p.get("penalty") == "elasticnet":
            return LogisticRegression(solver="saga", penalty="elasticnet", C=p["C"], l1_ratio=p["l1_ratio"], max_iter=3000, tol=1e-3, random_state=seed)
        return LogisticRegression(C=p["C"], max_iter=3000, random_state=seed)
    if family == "rf":
        return RandomForestClassifier(n_jobs=n_jobs, random_state=seed, **p)
    if family == "lgbm":
        import lightgbm as lgb
        return lgb.LGBMClassifier(subsample_freq=1, n_jobs=n_jobs, random_state=seed, verbose=-1, **p)
    if family == "xgb":
        import xgboost as xgb
        return xgb.XGBClassifier(tree_method="hist", n_jobs=n_jobs, random_state=seed, eval_metric="logloss", verbosity=0, **p)
    if family == "catboost":
        from catboost import CatBoostClassifier
        return CatBoostClassifier(thread_count=n_jobs, random_seed=seed, verbose=0, allow_writing_files=False, **p)
    raise ValueError(family)


def make_pipeline(family, params=None, feature_set="eng", kept=None, n_jobs=1, seed=SEED):
    """Full model: [service-adjusted price] -> one-hot + scale -> classifier. All fitting happens on the rows passed to .fit()."""
    cat, num, use_price = column_sets(feature_set, kept)
    scale = StandardScaler() if family == "glm" else "passthrough"
    ct = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat), ("num", scale, num)],
                           verbose_feature_names_out=False)
    ct.set_output(transform="pandas")
    steps = []
    if use_price:
        steps.append(("price", F.ServiceAdjustedPrice()))
    steps += [("prep", ct), ("clf", make_clf(family, params or default_params(family), n_jobs, seed))]
    return Pipeline(steps)


# ---------------------------------------------------------------- metrics
def ece_score(y, p, bins=10):
    """Expected calibration error: weighted mean gap between predicted and actual rate over equal-width probability bins."""
    y = np.asarray(y); p = np.asarray(p)
    idx = np.minimum((p * bins).astype(int), bins - 1)
    e = 0.0
    for b in range(bins):
        m = idx == b
        if m.any():
            e += m.mean() * abs(p[m].mean() - y[m].mean())
    return e


def order_desc(p, seed=0):
    """Indices from highest to lowest score; ties broken by a fixed random key so rule scores with ties are ranked fairly."""
    rng = np.random.RandomState(seed)
    return np.lexsort((rng.rand(len(p)), -np.asarray(p)))


def topk_capture(y, p, rev, frac=0.20):
    """Share of the leavers' monthly revenue that sits in the top `frac` of customers by score."""
    y = np.asarray(y); rev = np.asarray(rev, float)
    o = order_desc(p); k = int(math.ceil(frac * len(y)))
    lost = rev * y
    return lost[o[:k]].sum() / lost.sum()


def metrics(y, p, rev):
    y = np.asarray(y); p = np.asarray(p)
    o = order_desc(p); k = int(math.ceil(0.2 * len(y))); top = o[:k]
    return dict(auc=roc_auc_score(y, p), pr_auc=average_precision_score(y, p), brier=brier_score_loss(y, p),
                ece=ece_score(y, p), top20_rev=topk_capture(y, p, rev), top20_recall=y[top].sum() / y.sum(),
                top20_precision=y[top].mean())


def bootstrap_metrics(y, p, rev, n_boot=1000, seed=SEED):
    y = np.asarray(y); p = np.asarray(p); rev = np.asarray(rev)
    rng = np.random.RandomState(seed); rows = []
    for _ in range(n_boot):
        i = rng.randint(0, len(y), len(y))
        rows.append(metrics(y[i], p[i], rev[i]))
    b = pd.DataFrame(rows)
    point = metrics(y, p, rev)
    return pd.DataFrame({"estimate": point, "ci_low_2.5%": b.quantile(0.025), "ci_high_97.5%": b.quantile(0.975)})


# ---------------------------------------------------------------- cross-validation
def repeated_splits(y, n_splits=5, n_repeats=5, seed=SEED):
    return list(RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=seed).split(np.zeros(len(y)), y))


def _fit_eval(est, X, y, tr, va, rev):
    est = clone(est)
    t0 = time.time(); est.fit(X.iloc[tr], y.iloc[tr]); ft = time.time() - t0
    t0 = time.time(); p = est.predict_proba(X.iloc[va])[:, 1]; pt = time.time() - t0
    m = metrics(y.iloc[va].values, p, rev.iloc[va].values)
    m.update(fit_s=ft, predict_s=pt)
    return m


def cv_evaluate(est, X, y, splits, n_jobs=5):
    rev = X["MonthlyCharges"]
    rows = Parallel(n_jobs=n_jobs)(delayed(_fit_eval)(est, X, y, tr, va, rev) for tr, va in splits)
    return pd.DataFrame(rows)


def summarize(df):
    return {f"{c}_mean": df[c].mean() for c in df.columns} | {f"{c}_sd": df[c].std() for c in df.columns}


def oof_predictions(est, X, y, splits_5):
    """Out-of-fold probabilities from one 5-fold split (each row scored by a model that never saw it)."""
    p = np.zeros(len(y))
    for tr, va in splits_5:
        m = clone(est).fit(X.iloc[tr], y.iloc[tr]); p[va] = m.predict_proba(X.iloc[va])[:, 1]
    return p


# ---------------------------------------------------------------- Optuna
def suggest(trial, family):
    if family == "glm":
        return dict(penalty="elasticnet", C=trial.suggest_float("C", 1e-3, 10, log=True), l1_ratio=trial.suggest_float("l1_ratio", 0.0, 1.0))
    if family == "rf":
        return dict(n_estimators=trial.suggest_int("n_estimators", 200, 600, step=100), max_depth=trial.suggest_int("max_depth", 3, 14),
                    min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 40, log=True), max_features=trial.suggest_float("max_features", 0.1, 0.8))
    if family == "lgbm":
        return dict(n_estimators=trial.suggest_int("n_estimators", 100, 600, step=50), learning_rate=trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
                    num_leaves=trial.suggest_int("num_leaves", 4, 48, log=True), min_child_samples=trial.suggest_int("min_child_samples", 5, 100, log=True),
                    subsample=trial.suggest_float("subsample", 0.5, 1.0), colsample_bytree=trial.suggest_float("colsample_bytree", 0.4, 1.0),
                    reg_lambda=trial.suggest_float("reg_lambda", 1e-2, 30, log=True))
    if family == "xgb":
        return dict(n_estimators=trial.suggest_int("n_estimators", 100, 600, step=50), learning_rate=trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
                    max_depth=trial.suggest_int("max_depth", 2, 7), min_child_weight=trial.suggest_float("min_child_weight", 1, 30, log=True),
                    subsample=trial.suggest_float("subsample", 0.5, 1.0), colsample_bytree=trial.suggest_float("colsample_bytree", 0.4, 1.0),
                    reg_lambda=trial.suggest_float("reg_lambda", 1e-2, 30, log=True))
    if family == "catboost":
        return dict(iterations=trial.suggest_int("iterations", 150, 600, step=50), learning_rate=trial.suggest_float("learning_rate", 0.01, 0.2, log=True),
                    depth=trial.suggest_int("depth", 2, 7), l2_leaf_reg=trial.suggest_float("l2_leaf_reg", 1.0, 30, log=True))
    raise ValueError(family)


SEARCH_SPACE_TEXT = {
    "glm": [("C", "log 0.001 to 10", "inverse penalty strength; log scale because useful values span orders of magnitude"),
            ("l1_ratio", "0 to 1", "mix of ridge (0) and lasso (1) penalty; lasso can zero out weak columns")],
    "rf": [("n_estimators", "200 to 600 step 100", "more trees steady the average; gains stop early"),
           ("max_depth", "3 to 14", "shallow trees cannot overfit; deep ones can"),
           ("min_samples_leaf", "1 to 40 (log)", "bigger leaves smooth the prediction; 40 of 4,500 rows is under 1%"),
           ("max_features", "0.1 to 0.8", "share of columns tried at each split; lower decorrelates trees")],
    "lgbm": [("n_estimators", "100 to 600 step 50", "number of boosting rounds; pairs with learning rate"),
             ("learning_rate", "log 0.01 to 0.2", "step size; small steps need more rounds but overfit less"),
             ("num_leaves", "log 4 to 48", "tree size; small data wants small trees"),
             ("min_child_samples", "log 5 to 100", "rows needed in a leaf; main guard against fitting noise"),
             ("subsample", "0.5 to 1.0", "share of rows per round; adds randomness that reduces overfitting"),
             ("colsample_bytree", "0.4 to 1.0", "share of columns per tree"),
             ("reg_lambda", "log 0.01 to 30", "L2 penalty on leaf values")],
    "xgb": [("n_estimators", "100 to 600 step 50", "number of boosting rounds"),
            ("learning_rate", "log 0.01 to 0.2", "step size"),
            ("max_depth", "2 to 7", "tree depth; small data wants shallow trees"),
            ("min_child_weight", "log 1 to 30", "minimum summed weight in a leaf; guards against noise"),
            ("subsample", "0.5 to 1.0", "share of rows per round"),
            ("colsample_bytree", "0.4 to 1.0", "share of columns per tree"),
            ("reg_lambda", "log 0.01 to 30", "L2 penalty on leaf values")],
    "catboost": [("iterations", "150 to 600 step 50", "number of boosting rounds"),
                 ("learning_rate", "log 0.01 to 0.2", "step size"),
                 ("depth", "2 to 7", "tree depth (symmetric trees)"),
                 ("l2_leaf_reg", "log 1 to 30", "L2 penalty on leaf values")],
}


def _objective(family, feature_set, kept, X, y, splits, threads):
    rev = X["MonthlyCharges"]
    def obj(trial):
        params = suggest(trial, family)
        aucs, tops, briers, prs, times = [], [], [], [], []
        for i, (tr, va) in enumerate(splits):
            est = make_pipeline(family, params, feature_set, kept, n_jobs=threads)
            t0 = time.time(); est.fit(X.iloc[tr], y.iloc[tr]); times.append(time.time() - t0)
            p = est.predict_proba(X.iloc[va])[:, 1]
            m = metrics(y.iloc[va].values, p, rev.iloc[va].values)
            aucs.append(m["auc"]); tops.append(m["top20_rev"]); briers.append(m["brier"]); prs.append(m["pr_auc"])
            trial.report(float(np.mean(aucs)), i)
            if trial.should_prune():
                raise optuna.TrialPruned()
        trial.set_user_attr("auc_sd", float(np.std(aucs, ddof=1)))
        trial.set_user_attr("top20_rev", float(np.mean(tops)))
        trial.set_user_attr("brier", float(np.mean(briers)))
        trial.set_user_attr("pr_auc", float(np.mean(prs)))
        trial.set_user_attr("fit_seconds", float(np.mean(times)))
        return float(np.mean(aucs))
    return obj


def make_study(seed, storage=None, name=None):
    return optuna.create_study(direction="maximize", sampler=optuna.samplers.TPESampler(seed=seed),
                               pruner=optuna.pruners.MedianPruner(n_startup_trials=10, n_warmup_steps=1),
                               storage=storage, study_name=name, load_if_exists=False)


def _outer_fold(family, feature_set, kept, X, y, k, tr, va, n_trials, timeout, threads):
    Xtr, ytr = X.iloc[tr].reset_index(drop=True), y.iloc[tr].reset_index(drop=True)
    inner = list(StratifiedKFold(3, shuffle=True, random_state=100 + k).split(np.zeros(len(ytr)), ytr))
    st = make_study(SEED + k)
    st.optimize(_objective(family, feature_set, kept, Xtr, ytr, inner, threads), n_trials=n_trials, timeout=timeout)
    best = {**default_params(family), **st.best_params} if family != "glm" else dict(penalty="elasticnet", **st.best_params)
    est = make_pipeline(family, best, feature_set, kept, n_jobs=threads).fit(Xtr, ytr)
    p = est.predict_proba(X.iloc[va])[:, 1]
    m = metrics(y.iloc[va].values, p, X["MonthlyCharges"].iloc[va].values)
    m.update(outer_fold=k, inner_best_auc=st.best_value, n_trials=len(st.trials),
             n_pruned=sum(t.state == optuna.trial.TrialState.PRUNED for t in st.trials), best_params=json.dumps(best))
    return m


def tune_family(family, X, y, feature_set="eng", kept=None, n_trials=60, timeout=1800, outer_splits=5, reuse=True, threads=2):
    """Nested tuning. Outer loop: 5 folds of the training set give an honest score. For each outer fold a separate
    Optuna study (inner 3-fold CV on the outer-training rows only) picks parameters, which are scored once on the outer
    validation rows. Final study: tuned on 5-fold CV of the whole training set and saved to SQLite; its best parameters
    are the ones used for the final model."""
    cache = os.path.join(MODEL_DIR, f"tuning_{family}.json"); db = os.path.join(MODEL_DIR, f"optuna_{family}.db")
    if reuse and os.path.exists(cache) and os.path.exists(db):
        return json.load(open(cache))
    if os.path.exists(db):
        os.remove(db)
    t0 = time.time()
    outer = list(StratifiedKFold(outer_splits, shuffle=True, random_state=SEED + 1).split(np.zeros(len(y)), y))
    rows = Parallel(n_jobs=outer_splits)(delayed(_outer_fold)(family, feature_set, kept, X, y, k, tr, va, n_trials, timeout, threads) for k, (tr, va) in enumerate(outer))
    nested_seconds = time.time() - t0
    # final study on 5-fold CV of the full training set, stored in SQLite
    t1 = time.time()
    splits = list(StratifiedKFold(5, shuffle=True, random_state=SEED + 2).split(np.zeros(len(y)), y))
    storage = f"sqlite:///{db}"
    st = make_study(SEED, storage, f"{family}_final")
    st.optimize(_objective(family, feature_set, kept, X.reset_index(drop=True), y.reset_index(drop=True), splits, threads * 2), n_trials=n_trials, timeout=timeout)
    best = {**default_params(family), **st.best_params} if family != "glm" else dict(penalty="elasticnet", **st.best_params)
    trials = st.trials_dataframe(attrs=("number", "value", "state", "params", "user_attrs", "duration"))
    trials.to_csv(os.path.join(REPORT_DIR, "tables", f"optuna_trials_{family}.csv"), index=False)
    try:
        imp = optuna.importance.get_param_importances(st)
    except Exception:
        imp = {}
    done = [t for t in st.trials if t.state == optuna.trial.TrialState.COMPLETE]
    bt = st.best_trial
    res = dict(family=family, best_params=best, best_value=st.best_value, best_auc_sd=bt.user_attrs.get("auc_sd"),
               best_top20=bt.user_attrs.get("top20_rev"), best_brier=bt.user_attrs.get("brier"), best_fit_seconds=bt.user_attrs.get("fit_seconds"),
               n_trials=len(st.trials), n_complete=len(done), n_pruned=len(st.trials) - len(done), importance=imp,
               final_study_seconds=time.time() - t1, nested_seconds=nested_seconds, nested=rows)
    json.dump(res, open(cache, "w"), default=float, indent=1)
    return res


# ---------------------------------------------------------------- tables
def decile_table(y, p, rev):
    y = np.asarray(y); p = np.asarray(p); rev = np.asarray(rev, float)
    o = order_desc(p); parts = np.array_split(o, 10)
    base = y.mean(); lost_total = (rev * y).sum(); rows = []
    cum_l = cum_r = cum_n = 0
    for d, idx in enumerate(parts, 1):
        l = y[idx].sum(); r = (rev * y)[idx].sum(); cum_l += l; cum_r += r; cum_n += len(idx)
        rows.append(dict(decile=d, customers=len(idx), mean_predicted_risk=p[idx].mean(), actual_churn_rate=y[idx].mean(),
                         lift_vs_base=y[idx].mean() / base, leavers=int(l), monthly_revenue_lost_usd=r,
                         cum_share_customers=cum_n / len(y), cum_share_leavers_captured=cum_l / y.sum(), cum_share_lost_revenue_captured=cum_r / lost_total))
    return pd.DataFrame(rows)


def threshold_table(y, p, rev, cutoffs=(0.10, 0.25, 0.50, 0.75, 0.90)):
    y = np.asarray(y); p = np.asarray(p); rev = np.asarray(rev, float); rows = []
    for c in cutoffs:
        f = p >= c; tp = (f & (y == 1)).sum(); fp = (f & (y == 0)).sum()
        rows.append(dict(cutoff=c, customers_flagged=int(f.sum()), share_flagged=f.mean(), precision=tp / f.sum() if f.sum() else np.nan,
                         recall=tp / y.sum(), false_positive_rate=fp / (y == 0).sum(),
                         share_lost_revenue_captured=(rev * y)[f].sum() / (rev * y).sum()))
    return pd.DataFrame(rows)


def grouped_permutation_importance(est, X_raw, y, feature_fn, groups, n_repeats=20, seed=SEED):
    """Shuffle one ORIGINAL column at a time in the raw table, rebuild every engineered feature from it, re-score.
    Drop in AUC and in top-20% revenue capture versus the unshuffled score."""
    y = np.asarray(y); rng = np.random.RandomState(seed)
    base = metrics(y, est.predict_proba(feature_fn(X_raw))[:, 1], X_raw["MonthlyCharges"].values)
    rows = []
    for g in groups:
        da, dt = [], []
        for _ in range(n_repeats):
            Xp = X_raw.copy(); Xp[g] = Xp[g].values[rng.permutation(len(Xp))]
            m = metrics(y, est.predict_proba(feature_fn(Xp))[:, 1], X_raw["MonthlyCharges"].values)  # revenue weights stay with true rows
            da.append(base["auc"] - m["auc"]); dt.append(base["top20_rev"] - m["top20_rev"])
        rows.append(dict(column=g, auc_drop_mean=np.mean(da), auc_drop_sd=np.std(da, ddof=1), top20_drop_mean=np.mean(dt), top20_drop_sd=np.std(dt, ddof=1)))
    return pd.DataFrame(rows).sort_values("auc_drop_mean", ascending=False).reset_index(drop=True)


def shap_group_map(names):
    """Map each model input column to its original column. One-hot columns by prefix; engineered features by their primary source."""
    prim = {r["name"]: r["primary"] for r in F.REGISTRY}; prim["price_resid"] = "MonthlyCharges"
    out = {}
    for n in names:
        if n in prim: out[n] = prim[n]
        elif n in F.RAW_NUM: out[n] = n
        else:
            out[n] = next((c for c in sorted(F.RAW_CAT, key=len, reverse=True) if n.startswith(c + "_")), n)
    return out


def shap_values_by_group(est, X, family):
    import shap
    Z = est[:-1].transform(X); clf = est[-1]
    if family == "glm":
        sv = shap.LinearExplainer(clf, shap.maskers.Independent(Z, max_samples=len(Z))).shap_values(Z)
    else:
        sv = shap.TreeExplainer(clf).shap_values(Z)
        if isinstance(sv, list): sv = sv[1]
        sv = np.asarray(sv)
        if sv.ndim == 3: sv = sv[:, :, 1]
    gm = shap_group_map(list(Z.columns))
    sv_df = pd.DataFrame(sv, columns=Z.columns)
    signed = sv_df.T.groupby(gm).sum().T  # signed values add up inside a group, then |.| is averaged over rows
    return Z, sv, signed.abs().mean().sort_values(ascending=False), signed


def counterfactual(est, X_raw, mask, column, new_value, feature_fn, n_boot=1000, seed=SEED, bill_delta=0.0):
    """Set `column` to `new_value` for eligible rows (mask), rebuild features, re-score. Returns mean change in predicted
    churn probability (points) with a bootstrap interval over the eligible customers."""
    E = X_raw[mask]
    p0 = est.predict_proba(feature_fn(E))[:, 1]
    E2 = E.copy(); E2[column] = new_value; E2['MonthlyCharges'] = E2['MonthlyCharges'] + bill_delta
    p1 = est.predict_proba(feature_fn(E2))[:, 1]
    d = p1 - p0; rev = E["MonthlyCharges"].values
    rng = np.random.RandomState(seed); b = []; bl = []
    for _ in range(n_boot):
        i = rng.randint(0, len(d), len(d)); b.append(d[i].mean()); bl.append((d[i] * rev[i]).sum())
    return dict(eligible=int(mask.sum()), mean_risk_before=p0.mean(), mean_risk_after=p1.mean(), mean_change_pts=100 * d.mean(),
                ci_low_pts=100 * np.percentile(b, 2.5), ci_high_pts=100 * np.percentile(b, 97.5),
                change_in_expected_monthly_revenue_lost_usd=(d * rev).sum(), rev_ci_low=np.percentile(bl, 2.5), rev_ci_high=np.percentile(bl, 97.5))


def paired_bootstrap(y, p_a, p_b, rev, metric="top20_rev", n_boot=1000, seed=SEED):
    """Difference (A minus B) in one metric on the same bootstrap resamples. Returns estimate and 95% interval."""
    y = np.asarray(y); p_a = np.asarray(p_a); p_b = np.asarray(p_b); rev = np.asarray(rev)
    rng = np.random.RandomState(seed); d = []
    for _ in range(n_boot):
        i = rng.randint(0, len(y), len(y))
        d.append(metrics(y[i], p_a[i], rev[i])[metric] - metrics(y[i], p_b[i], rev[i])[metric])
    est = metrics(y, p_a, rev)[metric] - metrics(y, p_b, rev)[metric]
    return est, np.percentile(d, 2.5), np.percentile(d, 97.5)


def md_table(df, floatfmt="{:.3f}", index=False):
    """Markdown table without extra dependencies."""
    d = df.reset_index() if index else df
    cols = [str(c) for c in d.columns]
    def f(v):
        if isinstance(v, (float, np.floating)):
            return "" if np.isnan(v) else floatfmt.format(v)
        return str(v).replace("|", "/")
    rows = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    rows += ["| " + " | ".join(f(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join(rows)


def plot_optuna(family, charts_dir):
    """Optimization history and parameter importance for the saved final study. Returns the two PNG paths."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from optuna.visualization.matplotlib import plot_optimization_history, plot_param_importances
    st = optuna.load_study(study_name=f"{family}_final", storage=f"sqlite:///{MODEL_DIR}/optuna_{family}.db")
    paths = []
    for fn, tag, ttl in [(plot_optimization_history, "history", "Optimization history"), (plot_param_importances, "importance", "Parameter importance")]:
        ax = fn(st); fig = ax.figure; fig.set_size_inches(7, 4)
        for a in fig.axes: a.set_title("")
        fig.suptitle(f"{family}: {ttl} (final study, AUC)"); fig.tight_layout(); p = f"{charts_dir}/optuna_{family}_{tag}.png"; fig.savefig(p, dpi=110); paths.append(p); plt.show()
    return paths
