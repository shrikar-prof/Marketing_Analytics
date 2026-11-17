"""
Modeling utilities for the Discount Leakage Audit.

Shared between notebooks/03_modeling.ipynb and src/pipeline.py so that
the notebook and the production pipeline cannot drift apart.
"""

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import TargetEncoder

from features import (
    ALL_FEATURES,
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    TARGET,
    PASSTHROUGH_COLS,
)

# Random seed used throughout
SEED = 42


# ── Pipeline builder ──────────────────────────────────────────────────────────

def build_pipeline(model) -> Pipeline:
    """
    Build a sklearn Pipeline with:
      - TargetEncoder (smooth='auto', target_type='continuous') for categoricals
      - passthrough for numeric features
      - the supplied model estimator

    The encoder is fit only on training data within each CV fold, preventing
    any target leakage from the validation or test rows.
    """
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "cat",
                TargetEncoder(
                    target_type="continuous",
                    smooth="auto",
                    random_state=SEED,
                ),
                CATEGORICAL_FEATURES,
            ),
            ("num", "passthrough", NUMERIC_FEATURES),
        ],
        remainder="drop",
    )
    return Pipeline(steps=[("prep", preprocessor), ("model", model)])


# ── Business metrics ──────────────────────────────────────────────────────────

def capture_rate_top10(y_true: np.ndarray, y_pred: np.ndarray,
                       total_disc: np.ndarray) -> float:
    """
    Fraction of total discount dollars captured by flagging the top-10% of
    rows sorted by predicted disc_rate.

    A value of 1.0 means the model's top decile contains ALL discount spending.
    A baseline random model scores ~0.10.
    """
    n = len(y_true)
    n_flag = max(1, int(np.ceil(0.10 * n)))
    top_idx = np.argsort(y_pred)[::-1][:n_flag]
    return float(total_disc[top_idx].sum() / (total_disc.sum() + 1e-12))


def recoverable_margin(y_true: np.ndarray, y_pred: np.ndarray,
                       list_revenue: np.ndarray,
                       threshold: float = 0.25) -> float:
    """
    Estimated recoverable margin in dollars.

    For rows where predicted disc_rate > threshold AND actual disc_rate >
    threshold, the excess discount above threshold × list_revenue is counted
    as recoverable (i.e., what could be saved by capping those promotions at
    the threshold rate).
    """
    flagged = (y_pred > threshold) & (y_true > threshold)
    excess = (y_true[flagged] - threshold) * list_revenue[flagged]
    return float(excess.sum())


def compute_ece(y_true: np.ndarray, y_pred: np.ndarray,
                n_bins: int = 10) -> float:
    """
    Expected Calibration Error (ECE) for regression, measured as the mean
    absolute difference between average predicted value and average actual
    value within equal-width bins of predicted values.

    A lower value means predictions are better calibrated (on average the
    predicted disc_rate equals the true disc_rate).
    """
    bins = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    n = len(y_true)
    for lo, hi in zip(bins[:-1], bins[1:]):
        mask = (y_pred >= lo) & (y_pred < hi)
        if mask.sum() == 0:
            continue
        ece += mask.sum() / n * abs(y_pred[mask].mean() - y_true[mask].mean())
    return float(ece)


def decile_table(y_true: np.ndarray, y_pred: np.ndarray,
                 list_revenue: np.ndarray,
                 total_disc: np.ndarray) -> pd.DataFrame:
    """
    Build a decile table: rows ranked by predicted disc_rate, 10 equal groups.

    Columns:
      decile            – 1 (highest predicted) to 10 (lowest)
      n_rows            – rows in decile
      mean_pred_disc    – mean predicted disc_rate
      mean_actual_disc  – mean actual disc_rate
      actual_disc_$     – total discount dollars in decile
      list_rev_$        – total list revenue in decile
      actual_rate       – actual_disc_$ / list_rev_$
      capture_pct       – share of all discount dollars in this decile
      cum_capture_pct   – cumulative capture
      lift              – actual_rate / overall_actual_rate
    """
    overall_rate = total_disc.sum() / (list_revenue.sum() + 1e-12)
    order = np.argsort(y_pred)[::-1]
    n = len(y_pred)
    rows = []
    for d in range(10):
        lo = d * n // 10
        hi = (d + 1) * n // 10
        idx = order[lo:hi]
        rows.append({
            "decile": d + 1,
            "n_rows": len(idx),
            "mean_pred_disc_rate": float(y_pred[idx].mean()),
            "mean_actual_disc_rate": float(y_true[idx].mean()),
            "actual_disc_$": float(total_disc[idx].sum()),
            "list_rev_$": float(list_revenue[idx].sum()),
            "actual_disc_rate": float(total_disc[idx].sum() / (list_revenue[idx].sum() + 1e-12)),
            "capture_pct": float(total_disc[idx].sum() / (total_disc.sum() + 1e-12) * 100),
        })
    df_d = pd.DataFrame(rows)
    df_d["cum_capture_pct"] = df_d["capture_pct"].cumsum()
    df_d["lift"] = df_d["actual_disc_rate"] / (overall_rate + 1e-12)
    return df_d


def threshold_table(y_true: np.ndarray, y_pred: np.ndarray,
                    list_revenue: np.ndarray,
                    total_disc: np.ndarray,
                    thresholds=(0.10, 0.25, 0.50, 0.75, 0.90)) -> pd.DataFrame:
    """
    For each threshold: fraction flagged, precision, recall, FPR, margin captured.

    'High leakage' is defined as actual disc_rate > 0.25 (a threshold where
    the promotion is giving away more than a quarter of list revenue).
    """
    HIGH = 0.25
    actual_high = y_true > HIGH
    rows = []
    for t in thresholds:
        flagged = y_pred > t
        tp = (flagged & actual_high).sum()
        fp = (flagged & ~actual_high).sum()
        fn = (~flagged & actual_high).sum()
        tn = (~flagged & ~actual_high).sum()
        precision = tp / (tp + fp + 1e-12)
        recall = tp / (tp + fn + 1e-12)
        fpr = fp / (fp + tn + 1e-12)
        disc_captured = total_disc[flagged].sum() / (total_disc.sum() + 1e-12)
        rows.append({
            "threshold": t,
            "share_flagged_%": flagged.mean() * 100,
            "precision": precision,
            "recall": recall,
            "false_positive_rate": fpr,
            "disc_$ captured_%": disc_captured * 100,
        })
    return pd.DataFrame(rows)
