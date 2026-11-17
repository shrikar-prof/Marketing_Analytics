"""
Model utility functions for M5 demand forecasting.

Covers: metrics (RMSSE, MAE, RMSE), walk-forward CV splits,
threshold/decile tables adapted for regression (error quantiles),
and model comparison helpers.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Iterator


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Root Mean Squared Error.

    RMSE = sqrt( mean( (y_true - y_pred)^2 ) )

    Unit: same as y_true (units per day).
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Mean Absolute Error.

    MAE = mean( |y_true - y_pred| )

    Unit: same as y_true (units per day).
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def compute_rmsse(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_train: np.ndarray,
) -> float:
    """Root Mean Scaled Squared Error — the M5 competition metric per series.

    Formula
    -------
    For a single series:

        scale = (1 / (T_train - 1)) * sum_{t=2}^{T_train} (y_train[t] - y_train[t-1])^2

        RMSSE = sqrt( mean((y_true - y_pred)^2) / scale )

    The denominator is the RMSE of a naive one-step forecast on the training
    data. RMSSE = 1.0 means the model matches a naive yesterday-is-today
    benchmark. Lower is better; < 1.0 beats naive.

    Parameters
    ----------
    y_true  : actual sales in the forecast window (H steps)
    y_pred  : model forecasts
    y_train : historical training sales (T_train steps)

    Returns
    -------
    float — RMSSE for one series
    """
    scale = np.mean(np.diff(y_train) ** 2)
    if scale == 0:
        return np.nan   # constant series; undefined
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2) / scale))


def batch_rmsse(
    df: pd.DataFrame,
    pred_col: str = "pred",
    actual_col: str = "units",
    series_col: str = "series_id",
    split_col: str = "split",
    train_label: str = "train",
    eval_label: str = "val",
) -> pd.Series:
    """Compute per-series RMSSE for the evaluation split.

    Parameters
    ----------
    df          : long-format DataFrame with actual, predicted, and split columns
    pred_col    : column holding model predictions
    actual_col  : column holding ground truth
    series_col  : column identifying each series
    split_col   : column holding 'train' / 'val' / 'test' labels
    train_label : value in split_col for training data
    eval_label  : value in split_col for the split to evaluate

    Returns
    -------
    Series indexed by series_id, values = per-series RMSSE
    """
    results = {}
    train_df = df[df[split_col] == train_label]
    eval_df  = df[df[split_col] == eval_label]

    for sid, grp_eval in eval_df.groupby(series_col):
        grp_train = train_df[train_df[series_col] == sid]
        y_train = grp_train[actual_col].to_numpy(np.float32)
        y_true  = grp_eval[actual_col].to_numpy(np.float32)
        y_pred  = grp_eval[pred_col].to_numpy(np.float32)
        results[sid] = compute_rmsse(y_true, y_pred, y_train)

    return pd.Series(results, name="rmsse")


def mean_rmsse(rmsse_series: pd.Series) -> float:
    """Mean RMSSE across all series, ignoring NaN (constant series)."""
    return float(rmsse_series.dropna().mean())


# ---------------------------------------------------------------------------
# Walk-forward CV splits
# ---------------------------------------------------------------------------

def walk_forward_splits(
    d_col: np.ndarray,
    horizon: int = 28,
    n_folds: int = 3,
    min_train_days: int = 365,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Generate walk-forward train/val index splits.

    Each fold extends training by `horizon` days and evaluates the next
    `horizon` days. The last fold uses d_1885 as the last training day
    (val = d_1886 to d_1913) to match the handoff specification.

    Parameters
    ----------
    d_col         : 1-D array of day-index values in the frame (1-based)
    horizon       : number of forecast days per fold (default 28)
    n_folds       : number of CV folds (default 3)
    min_train_days: minimum training days in the first fold

    Returns
    -------
    list of (train_idx, val_idx) arrays of positional indices into d_col
    """
    from src.features import VAL_START, TEST_START

    # Last training day for the final fold
    last_train = VAL_START - 1   # d_1885
    last_val   = TEST_START - 1  # d_1913

    splits = []
    for fold in range(n_folds):
        val_end   = last_val   - fold * horizon
        val_start = val_end - horizon + 1
        train_end = val_start - 1

        train_idx = np.where((d_col <= train_end))[0]
        val_idx   = np.where((d_col >= val_start) & (d_col <= val_end))[0]

        if len(train_idx) < min_train_days * 100:  # very rough check
            break
        splits.append((train_idx, val_idx))

    return list(reversed(splits))   # chronological order: earliest fold first


# ---------------------------------------------------------------------------
# Rule-of-thumb baseline
# ---------------------------------------------------------------------------

def rule_of_thumb_forecast(
    units_long: pd.DataFrame,
    forecast_d_start: int,
    forecast_d_end: int,
    lookback_weeks: int = 4,
) -> pd.DataFrame:
    """Replicate the current business rule: average of same weekday over last N weeks.

    The rule uses only information available before forecast_d_start.

    Parameters
    ----------
    units_long    : long-format DataFrame with columns item_id, store_id, d_col, units,
                    plus a 'date' column (datetime64)
    forecast_d_start : first day index to forecast (1-based)
    forecast_d_end   : last day index to forecast (1-based)
    lookback_weeks   : how many prior same-weekday values to average (default 4)

    Returns
    -------
    DataFrame with columns: item_id, store_id, d_col, rot_pred
    """
    hist = units_long[units_long["d_col"] < forecast_d_start].copy()
    hist["dow"] = pd.to_datetime(hist["date"]).dt.dayofweek

    fcast_days = units_long[
        (units_long["d_col"] >= forecast_d_start) & (units_long["d_col"] <= forecast_d_end)
    ][["item_id", "store_id", "d_col", "date"]].drop_duplicates()
    fcast_days["dow"] = pd.to_datetime(fcast_days["date"]).dt.dayofweek

    preds = []
    for _, row in fcast_days.iterrows():
        same_dow = hist[
            (hist["item_id"] == row["item_id"]) &
            (hist["store_id"] == row["store_id"]) &
            (hist["dow"] == row["dow"])
        ].sort_values("d_col").tail(lookback_weeks)
        pred = same_dow["units"].mean() if len(same_dow) > 0 else 0.0
        preds.append({
            "item_id": row["item_id"],
            "store_id": row["store_id"],
            "d_col": row["d_col"],
            "rot_pred": max(0.0, pred),
        })

    return pd.DataFrame(preds)


# ---------------------------------------------------------------------------
# Decile / error table helpers
# ---------------------------------------------------------------------------

def make_decile_table(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    n_deciles: int = 10,
) -> pd.DataFrame:
    """Rank rows by predicted value into deciles; report actual mean, error, and lift.

    'Lift' here = (actual demand in decile) / (overall mean actual demand).
    Decile 10 = highest-predicted rows.

    Returns
    -------
    DataFrame with columns: decile, n_rows, mean_actual, mean_pred, mae,
        rmse, capture_pct (share of total units in this decile), cumulative_capture_pct
    """
    df = pd.DataFrame({"y_true": y_true, "y_pred": y_pred})
    df["decile"] = pd.qcut(df["y_pred"], q=n_deciles, labels=False, duplicates="drop") + 1

    rows = []
    total_units = df["y_true"].sum()
    for d, grp in df.groupby("decile"):
        rows.append({
            "decile": int(d),
            "n_rows": len(grp),
            "mean_actual": grp["y_true"].mean(),
            "mean_pred": grp["y_pred"].mean(),
            "mae": np.mean(np.abs(grp["y_true"] - grp["y_pred"])),
            "rmse": np.sqrt(np.mean((grp["y_true"] - grp["y_pred"]) ** 2)),
            "capture_pct": 100 * grp["y_true"].sum() / total_units if total_units > 0 else 0,
        })
    result = pd.DataFrame(rows)
    result["cumulative_capture_pct"] = result["capture_pct"].cumsum()
    return result


def make_error_distribution_table(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    quantiles: list[float] | None = None,
) -> pd.DataFrame:
    """Summarise absolute error distribution by quantile.

    Returns
    -------
    DataFrame with the requested quantiles of absolute error (in units).
    """
    if quantiles is None:
        quantiles = [0.5, 0.75, 0.9, 0.95, 0.99]
    errors = np.abs(y_true - y_pred)
    rows = [{"metric": f"q{int(q*100)}", "abs_error_units": np.quantile(errors, q)}
            for q in quantiles]
    rows.insert(0, {"metric": "mean", "abs_error_units": errors.mean()})
    rows.insert(0, {"metric": "rmse", "abs_error_units": np.sqrt(np.mean((y_true - y_pred)**2))})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Model comparison table
# ---------------------------------------------------------------------------

def compare_models(results: list[dict]) -> pd.DataFrame:
    """Collect per-model metrics into a comparison table.

    Parameters
    ----------
    results : list of dicts with keys: model, cv_rmsse_mean, cv_rmsse_std,
        cv_mae_mean, cv_mae_std, train_time_s

    Returns
    -------
    DataFrame sorted by cv_rmsse_mean ascending.
    """
    df = pd.DataFrame(results)
    df = df.sort_values("cv_rmsse_mean").reset_index(drop=True)
    return df
