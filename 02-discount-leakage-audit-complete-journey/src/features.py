"""
Feature definitions for the Discount Leakage Audit model.

All feature computation lives here so that notebooks/02_feature_engineering.ipynb
and src/pipeline.py share identical logic and cannot drift apart.
"""

import numpy as np
import pandas as pd

# ── Column lists ──────────────────────────────────────────────────────────────

# Numeric features computed directly from raw columns.
# These are safe to use as-is after compute_numeric_features().
NUMERIC_FEATURES = [
    "is_national",    # 1 if National brand, 0 if Private/Unknown
    "week_sin",       # sin(2π·week/52): cyclical week encoding
    "week_cos",       # cos(2π·week/52): cyclical week encoding
    "quarter",        # calendar quarter 0–3 derived from week
    "is_top3_dept",   # 1 if department is one of the top-3 high-leakage depts
    "log_quantity",   # log1p(quantity): scaled unit count
]

# Categorical features that the sklearn TargetEncoder will transform inside
# every Pipeline/CV fold.  They must NOT be encoded before the pipeline runs.
CATEGORICAL_FEATURES = [
    "department",
    "product_category",
    "product_type",
    "store_id",
]

ALL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES

# Target and split marker
TARGET = "disc_rate"
SPLIT_COL = "split"

# Extra columns kept in features.parquet for business-metric computation.
# They are not fed to the model.
PASSTHROUGH_COLS = ["week", "list_revenue", "total_disc"]

# ── Constants ─────────────────────────────────────────────────────────────────

# Departments with the three highest median leakage rates (Finding 2 / H4).
TOP3_DEPTS = {"TOYS", "MEAT", "SEAFOOD-PCKGD"}

# Temporal split boundary (Explorer recommendation: train ≤ week 39).
TRAIN_WEEK_MAX = 39

# ── Feature computation ───────────────────────────────────────────────────────

def compute_numeric_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add all numeric features to df in-place (returns a copy).

    Parameters
    ----------
    df : pd.DataFrame
        Must contain: brand, week, department, quantity.

    Returns
    -------
    pd.DataFrame with NUMERIC_FEATURES columns added.
    """
    out = df.copy()

    # is_national ─────────────────────────────────────────────────────────────
    # brand is a Categorical with values 'National' | 'Private'.
    # NaN rows → treated as non-national (0).
    brand_str = out["brand"].astype(str)
    out["is_national"] = (brand_str == "National").astype(np.float32)

    # week_sin / week_cos ─────────────────────────────────────────────────────
    week_f = out["week"].astype(float)
    out["week_sin"] = np.sin(2 * np.pi * week_f / 52).astype(np.float32)
    out["week_cos"] = np.cos(2 * np.pi * week_f / 52).astype(np.float32)

    # quarter ─────────────────────────────────────────────────────────────────
    out["quarter"] = ((out["week"].astype(int) - 1) // 13).astype(np.int8)

    # is_top3_dept ────────────────────────────────────────────────────────────
    dept_str = out["department"].astype(str)
    out["is_top3_dept"] = dept_str.isin(TOP3_DEPTS).astype(np.float32)

    # log_quantity ────────────────────────────────────────────────────────────
    qty = out["quantity"].clip(lower=0)
    out["log_quantity"] = np.log1p(qty).astype(np.float32)

    return out


def fill_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fill NaN values in categorical feature columns with the string 'UNKNOWN'.

    TargetEncoder handles unseen strings at prediction time by falling back to
    the global target mean, so this sentinel value is safe.
    """
    out = df.copy()
    for col in ["department", "product_category", "product_type"]:
        if col in out.columns:
            out[col] = out[col].astype(str).replace("nan", "UNKNOWN")
    return out


def add_split_column(df: pd.DataFrame, train_week_max: int = TRAIN_WEEK_MAX) -> pd.DataFrame:
    """
    Add a 'split' column: 'train' for weeks ≤ train_week_max, 'test' otherwise.
    """
    out = df.copy()
    out[SPLIT_COL] = np.where(out["week"] <= train_week_max, "train", "test")
    return out


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full feature engineering pipeline.

    1. Filters fuel rows.
    2. Adds split column.
    3. Computes numeric features.
    4. Fills categorical NaNs.
    5. Returns a lean DataFrame with ALL_FEATURES + TARGET + SPLIT_COL + PASSTHROUGH_COLS.
    """
    # Filter fuel rows
    df = df[~df["is_fuel"]].copy()

    # Temporal split
    df = add_split_column(df)

    # Numeric features
    df = compute_numeric_features(df)

    # Categorical NaN fill
    df = fill_categoricals(df)

    # Select output columns
    keep = ALL_FEATURES + [TARGET, SPLIT_COL] + PASSTHROUGH_COLS
    # Only keep columns that exist (PASSTHROUGH_COLS may not all be present in test contexts)
    keep = [c for c in keep if c in df.columns]
    return df[keep].reset_index(drop=True)
