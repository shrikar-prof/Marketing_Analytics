"""
model_utils.py — shared model helpers for 05-pricing-simulator.

Imported by notebooks/03_modeling.ipynb and src/pipeline.py.
"""
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


SEED = 42
TARGET_COL = "LOG_UNITS"


# ---------------------------------------------------------------------------
# Metric helpers
# ---------------------------------------------------------------------------

def rmse(y_true, y_pred):
    """Root Mean Squared Error on log scale."""
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def mape_units(log_y_true, log_y_pred):
    """
    MAPE on original unit scale (exponentiated predictions).

    Formula: mean( |units_true - units_pred| / max(units_true, 1) )
    Avoids division by zero; clips at 1 for near-zero actuals.
    """
    units_true = np.expm1(log_y_true)
    units_pred = np.expm1(log_y_pred)
    denom = np.maximum(units_true, 1.0)
    return float(np.mean(np.abs(units_true - units_pred) / denom))


def eval_metrics(y_true, y_pred, label=""):
    """Return dict of RMSE, R2, MAPE_units."""
    return {
        "label": label,
        "RMSE_log": rmse(y_true, y_pred),
        "R2": float(r2_score(y_true, y_pred)),
        "MAPE_units": mape_units(y_true, y_pred),
    }


# ---------------------------------------------------------------------------
# Preprocessor factory
# ---------------------------------------------------------------------------

def make_preprocessor(numeric_cols, binary_cols, categorical_cols):
    """
    Build a ColumnTransformer that:
    - StandardScales numeric columns
    - Passes binary columns through unchanged
    - OneHotEncodes categorical columns (drop first to avoid multicollinearity)

    Nothing is fitted here; call .fit_transform() on training data inside a Pipeline.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numeric_cols),
            ("bin", "passthrough", binary_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorical_cols),
        ],
        remainder="drop",
    )


def make_preprocessor_no_scale(numeric_cols, binary_cols, categorical_cols):
    """
    Same as make_preprocessor but without StandardScaler on numeric columns.
    Used for tree-based models that do not need scaled inputs.
    """
    return ColumnTransformer(
        transformers=[
            ("num", "passthrough", numeric_cols),
            ("bin", "passthrough", binary_cols),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore", sparse_output=False), categorical_cols),
        ],
        remainder="drop",
    )


# ---------------------------------------------------------------------------
# Elasticity extractor
# ---------------------------------------------------------------------------

def extract_elasticity_from_ridge(model_pipeline, feature_names_out, numeric_cols):
    """
    Extract the LOG_PRICE coefficient from a fitted Ridge pipeline.
    Returns (elasticity, coef_array, feature_names).
    """
    ridge = model_pipeline.named_steps["model"]
    coefs = ridge.coef_
    # The numeric columns are first after the ColumnTransformer
    log_price_idx = numeric_cols.index("LOG_PRICE")
    elasticity = coefs[log_price_idx]
    return elasticity, coefs, feature_names_out


# ---------------------------------------------------------------------------
# Time-series CV splitter
# ---------------------------------------------------------------------------

def time_series_cv_indices(weeks_array, n_splits=5):
    """
    Expanding-window time-series cross-validation on training data.

    Given a sorted array of unique week end dates (training weeks only),
    returns (train_indices, val_indices) pairs for n_splits folds, where
    each fold uses strictly earlier weeks for training and later weeks for
    validation.

    Parameters
    ----------
    weeks_array : array-like of datetime
        Sorted unique week end dates in the training set.
    n_splits : int
        Number of CV folds.

    Yields
    ------
    (train_weeks_set, val_weeks_set) for each fold.
    """
    n = len(weeks_array)
    fold_size = n // (n_splits + 1)
    for i in range(1, n_splits + 1):
        train_end = fold_size * i
        val_end = min(fold_size * (i + 1), n)
        train_set = set(weeks_array[:train_end])
        val_set = set(weeks_array[train_end:val_end])
        yield train_set, val_set
