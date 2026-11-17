"""
model_utils.py — shared metric and evaluation utilities for the MMM project.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


# ── Metrics ───────────────────────────────────────────────────────────────────

def rmse(y_true, y_pred):
    return np.sqrt(mean_squared_error(y_true, y_pred))


def mae(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)


def mape(y_true, y_pred):
    """Mean absolute percentage error (%). Avoids division by zero."""
    y_true, y_pred = np.asarray(y_true, float), np.asarray(y_pred, float)
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def r2(y_true, y_pred):
    return r2_score(y_true, y_pred)


def compute_all_metrics(y_true, y_pred, label=""):
    """Return a dict of all four metrics."""
    return {
        "label": label,
        "RMSE": rmse(y_true, y_pred),
        "MAE": mae(y_true, y_pred),
        "MAPE_%": mape(y_true, y_pred),
        "R2": r2(y_true, y_pred),
    }


# ── Decile lift table ─────────────────────────────────────────────────────────

def decile_table(y_true, y_pred):
    """
    Rank rows by predicted revenue (highest first), split into 10 equal groups,
    and report actual revenue rate and lift over mean per decile.
    """
    df = pd.DataFrame({"actual": y_true, "predicted": y_pred})
    df = df.sort_values("predicted", ascending=False).reset_index(drop=True)
    df["decile"] = pd.qcut(df.index, 10, labels=False) + 1
    overall_mean = df["actual"].mean()
    tbl = (
        df.groupby("decile")
        .agg(
            n=("actual", "count"),
            mean_actual=("actual", "mean"),
            mean_predicted=("predicted", "mean"),
            sum_actual=("actual", "sum"),
        )
        .reset_index()
    )
    tbl["lift"] = tbl["mean_actual"] / overall_mean
    tbl["cum_actual_pct"] = tbl["sum_actual"].cumsum() / tbl["sum_actual"].sum() * 100
    return tbl


# ── Threshold table ───────────────────────────────────────────────────────────

def threshold_table(y_true, y_pred, thresholds=None, total_revenue=None):
    """
    For a regression MMM, interpret threshold as: flag weeks where
    predicted revenue is above percentile threshold.
    Returns how much of total revenue those weeks represent.
    """
    if thresholds is None:
        thresholds = [0.10, 0.25, 0.50, 0.75, 0.90]
    if total_revenue is None:
        total_revenue = np.sum(y_true)
    rows = []
    for t in thresholds:
        cutoff = np.quantile(y_pred, 1 - t)
        flag = y_pred >= cutoff
        rows.append({
            "threshold_pct": int(t * 100),
            "n_flagged": int(flag.sum()),
            "share_flagged_pct": flag.mean() * 100,
            "revenue_captured_pct": y_true[flag].sum() / total_revenue * 100,
            "mean_actual_flagged": y_true[flag].mean() if flag.sum() > 0 else 0,
        })
    return pd.DataFrame(rows)


# ── Rolling-origin cross-validation ──────────────────────────────────────────

def rolling_origin_splits(n: int, n_test: int = 20, min_train: int = 60, step: int = 10):
    """
    Generate (train_idx, val_idx) pairs for time-series cross-validation.
    Each fold uses all data up to the split point as training, and the
    next n_test weeks as validation.
    """
    splits = []
    for end in range(min_train, n - n_test + 1, step):
        train_idx = list(range(end))
        val_idx = list(range(end, min(end + n_test, n)))
        splits.append((train_idx, val_idx))
    return splits


def cv_score(model, X, y, splits, metric_fn=rmse):
    """Run rolling-origin CV and return mean and std of the metric."""
    scores = []
    for train_idx, val_idx in splits:
        model.fit(X.iloc[train_idx], y.iloc[train_idx])
        preds = model.predict(X.iloc[val_idx])
        scores.append(metric_fn(y.iloc[val_idx], preds))
    return np.mean(scores), np.std(scores)
