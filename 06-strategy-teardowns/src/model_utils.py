"""
model_utils.py — shared modelling helpers for the strategy teardown project.

Provides:
  - loocv_ridge   : leave-one-out cross-validation for Ridge on a small panel
  - walk_forward_cv: walk-forward (time-series) cross-validation
  - fit_ols       : fit statsmodels OLS and return a results object
  - bootstrap_sensitivity: bootstrap-based sensitivity analysis for a feature
  - decile_table  : rank predictions into deciles and compute lift
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import statsmodels.api as sm


# ──────────────────────────────────────────────────────────────
# Cross-validation helpers
# ──────────────────────────────────────────────────────────────

def loocv_ridge(X: pd.DataFrame, y: pd.Series,
                alphas=(0.01, 0.1, 1.0, 10.0, 100.0)) -> dict:
    """
    Leave-one-out cross-validation for a Ridge regression.

    With n=8 rows, LOOCV gives 8 folds and uses n-1=7 observations for each
    training fold — the maximum possible for small-N evaluation.

    Parameters
    ----------
    X       : feature matrix (rows = observations, all numeric)
    y       : target series aligned with X
    alphas  : Ridge regularisation strengths to search over

    Returns
    -------
    dict with keys:
        mae          : mean absolute error across folds
        r2           : R² computed on out-of-fold predictions vs actuals
        best_alpha   : alpha chosen by inner RidgeCV (most common across folds)
        oof_preds    : array of out-of-fold predictions (same length as y)
        pipeline     : fitted Pipeline on full data with best_alpha
    """
    n = len(X)
    oof_preds = np.full(n, np.nan)
    best_alphas = []

    for i in range(n):
        # Train mask: all rows except i
        train_idx = [j for j in range(n) if j != i]
        X_tr = X.iloc[train_idx]
        y_tr = y.iloc[train_idx]
        X_te = X.iloc[[i]]

        # Inner alpha selection via RidgeCV on training fold
        inner = Pipeline([
            ("scaler", StandardScaler()),
            ("ridge", RidgeCV(alphas=alphas)),
        ])
        inner.fit(X_tr, y_tr)
        best_alphas.append(inner.named_steps["ridge"].alpha_)
        oof_preds[i] = inner.predict(X_te)[0]

    # Refit on full data with median best_alpha
    final_alpha = float(np.median(best_alphas))
    final_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=final_alpha)),
    ])
    final_pipe.fit(X, y)

    mae = mean_absolute_error(y, oof_preds)
    ss_res = np.sum((np.array(y) - oof_preds) ** 2)
    ss_tot = np.sum((np.array(y) - np.mean(y)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return {
        "mae": mae,
        "r2": r2,
        "best_alpha": final_alpha,
        "oof_preds": oof_preds,
        "pipeline": final_pipe,
    }


def walk_forward_cv(X: pd.DataFrame, y: pd.Series,
                    min_train: int = 8,
                    alphas=(0.01, 0.1, 1.0, 10.0, 100.0)) -> dict:
    """
    Walk-forward (expanding-window) cross-validation for time-ordered data.

    Train on [0..t-1], predict t, expand, repeat.
    Preserves temporal order so future data never leaks into training.

    Parameters
    ----------
    X         : feature matrix, rows in time order
    y         : target series aligned with X
    min_train : minimum number of rows to start training (default 8)
    alphas    : Ridge alpha grid

    Returns
    -------
    dict with mae, r2, best_alpha, oof_preds, pipeline (fitted on full data)
    """
    n = len(X)
    oof_preds = np.full(n, np.nan)
    best_alphas = []

    for t in range(min_train, n):
        X_tr = X.iloc[:t]
        y_tr = y.iloc[:t]
        X_te = X.iloc[[t]]

        inner = Pipeline([
            ("scaler", StandardScaler()),
            ("ridge", RidgeCV(alphas=alphas)),
        ])
        inner.fit(X_tr, y_tr)
        best_alphas.append(inner.named_steps["ridge"].alpha_)
        oof_preds[t] = inner.predict(X_te)[0]

    final_alpha = float(np.median(best_alphas))
    final_pipe = Pipeline([
        ("scaler", StandardScaler()),
        ("ridge", Ridge(alpha=final_alpha)),
    ])
    final_pipe.fit(X, y)

    # Only score on rows where we made predictions
    mask = ~np.isnan(oof_preds)
    mae = mean_absolute_error(y[mask], oof_preds[mask])
    ss_res = np.sum((np.array(y)[mask] - oof_preds[mask]) ** 2)
    ss_tot = np.sum((np.array(y)[mask] - np.mean(np.array(y)[mask])) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    return {
        "mae": mae,
        "r2": r2,
        "best_alpha": final_alpha,
        "oof_preds": oof_preds,
        "pipeline": final_pipe,
        "mask": mask,
    }


def fit_ols(X: pd.DataFrame, y: pd.Series,
            add_const: bool = True) -> object:
    """
    Fit a statsmodels OLS model and return the fitted Results object.

    Parameters
    ----------
    X         : feature matrix (all numeric)
    y         : target series
    add_const : if True, add an intercept column (default True)

    Returns
    -------
    statsmodels RegressionResultsWrapper
    """
    Xc = sm.add_constant(X, has_constant="add") if add_const else X
    model = sm.OLS(y, Xc)
    return model.fit()


# ──────────────────────────────────────────────────────────────
# Sensitivity / counterfactual
# ──────────────────────────────────────────────────────────────

def bootstrap_sensitivity(pipeline, X: pd.DataFrame,
                           feature: str, delta: float,
                           n_boot: int = 1000,
                           seed: int = 42) -> dict:
    """
    Bootstrap sensitivity: shift one feature by delta, re-score, report
    mean change and 95 % CI.

    This is an ASSOCIATION not a causal effect.  The model was trained on
    observational data; unmeasured confounders may explain part of the
    relationship.

    Parameters
    ----------
    pipeline : fitted sklearn Pipeline with a predict method
    X        : feature matrix used for prediction (full set, all rows)
    feature  : column name in X to perturb
    delta    : additive shift applied to that column
    n_boot   : bootstrap resamples
    seed     : random seed

    Returns
    -------
    dict with mean_change, ci_lower, ci_upper
    """
    rng = np.random.default_rng(seed)
    base_pred = pipeline.predict(X)

    X_shifted = X.copy()
    X_shifted[feature] = X_shifted[feature] + delta
    shifted_pred = pipeline.predict(X_shifted)
    point_change = np.mean(shifted_pred - base_pred)

    # Bootstrap over rows
    changes = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(X), size=len(X))
        c = np.mean(shifted_pred[idx] - base_pred[idx])
        changes.append(c)

    return {
        "mean_change": point_change,
        "ci_lower": float(np.percentile(changes, 2.5)),
        "ci_upper": float(np.percentile(changes, 97.5)),
    }


# ──────────────────────────────────────────────────────────────
# Decile / threshold tables
# ──────────────────────────────────────────────────────────────

def decile_table(y_true: np.ndarray, y_pred: np.ndarray,
                 label: str = "target") -> pd.DataFrame:
    """
    Rank observations by predicted value, group into deciles (or fewer
    for small N), and compute mean actual vs mean predicted per group.

    For small N (n < 20), uses quartiles instead of deciles.
    """
    n = len(y_true)
    n_bins = 4 if n < 20 else 10
    df = pd.DataFrame({"actual": y_true, "predicted": y_pred})
    df["bin"] = pd.qcut(df["predicted"], q=n_bins, labels=False, duplicates="drop")
    grouped = df.groupby("bin").agg(
        mean_actual=("actual", "mean"),
        mean_predicted=("predicted", "mean"),
        count=("actual", "count"),
    ).reset_index()
    grouped.rename(columns={"bin": "group"}, inplace=True)
    return grouped
