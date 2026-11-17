"""
features.py — shared feature definitions for 05-pricing-simulator.

Both notebooks/02_feature_engineering.ipynb and src/pipeline.py import
from here so the production pipeline cannot drift from the notebooks.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
TRAIN_CUTOFF_WEEKS = 130   # first 130 weeks = train; last 26 = test
SEED = 42
TARGET_COL = "LOG_UNITS"
LOG_PRICE_COL = "LOG_PRICE"

CATEGORICAL_COLS = [
    "CATEGORY",
    "SUB_CATEGORY",
    "SEG_VALUE_NAME",
    "PROMO_TYPE",
]

NUMERIC_FEATURES = [
    "LOG_PRICE",
    "DISCOUNT_PCT",
    "VISITS",
    "AVG_WEEKLY_BASKETS",
    "SALES_AREA_SIZE_NUM",
    "LOG_BASE_PRICE",
    "PRICE_TO_BASE_RATIO",
    "WEEK_OF_YEAR",
    "YEAR",
    "STORE_UPC_LAG1",
    "STORE_UPC_ROLL4",
    "CATEGORY_AVG_LOG_PRICE",
]

BINARY_FEATURES = ["FEATURE", "DISPLAY", "TPR_ONLY", "IS_ON_PROMO"]


def build_features(df: pd.DataFrame, train_mask: pd.Series = None) -> pd.DataFrame:
    """
    Build all engineered features from the clean dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The clean.parquet dataframe (all rows).
    train_mask : pd.Series, optional
        Boolean mask marking training rows. Required for lag/roll features
        (leak-safe): rolling stats are computed only on training rows and
        looked-up for test rows.

    Returns
    -------
    pd.DataFrame with the same index as df, containing all feature columns
    plus the target (LOG_UNITS), the split label, and identifiers.
    """
    out = df.copy()

    # -- 1. Log of base price --------------------------------------------------
    # BASE_PRICE is the everyday non-promotional price. Its log enters the
    # model so the elasticity on LOG_PRICE is relative to that anchor.
    out["LOG_BASE_PRICE"] = np.log(out["BASE_PRICE"].clip(lower=0.01))

    # -- 2. Price-to-base ratio ------------------------------------------------
    # PRICE / BASE_PRICE. When < 1 the product is on markdown. This feature
    # captures the depth of the discount in a scale-free way.
    out["PRICE_TO_BASE_RATIO"] = (
        out["PRICE"].clip(lower=0.01) / out["BASE_PRICE"].clip(lower=0.01)
    )

    # -- 3. Week-of-year and year ----------------------------------------------
    # Seasonal demand cycles (back-to-school for cereal, holiday snacking) are
    # captured by week-of-year. Year captures any trend across 2009-2011.
    out["WEEK_OF_YEAR"] = out["WEEK_END_DATE"].dt.isocalendar().week.astype(int)
    out["YEAR"] = out["WEEK_END_DATE"].dt.year

    # -- 4. Binary promotion flag ---------------------------------------------
    # Collapses FEATURE, DISPLAY, TPR_ONLY into a single on/off promo flag.
    # Useful as a simple baseline feature; individual flags remain separately.
    out["IS_ON_PROMO"] = (
        (out["FEATURE"] == 1) | (out["DISPLAY"] == 1) | (out["TPR_ONLY"] == 1)
    ).astype(int)

    # -- 5. Category-week average log-price ------------------------------------
    # Average log-price of all products in the same category and week.
    # Acts as a cross-price proxy: when competitors mark down, relative price
    # for a focal product increases.
    cat_week_avg = (
        out.groupby(["CATEGORY", "WEEK_END_DATE"])["LOG_PRICE"]
        .mean()
        .rename("CATEGORY_AVG_LOG_PRICE")
    )
    out = out.join(cat_week_avg, on=["CATEGORY", "WEEK_END_DATE"])

    # -- 6. Store × UPC lag-1 log units ----------------------------------------
    # Last week's sales for the same store-product pair. Captures serial
    # correlation in demand (inventory cycles, habit buying). Computed on
    # training rows only; test rows filled with training-period mean to avoid
    # future leakage.
    out = out.sort_values(["STORE_NUM", "UPC", "WEEK_END_DATE"])
    out["STORE_UPC_LAG1"] = (
        out.groupby(["STORE_NUM", "UPC"])["LOG_UNITS"].shift(1)
    )

    # -- 7. Store × UPC 4-week rolling mean log units --------------------------
    # Rolling 4-week average of log units (excluding current week). Smooths
    # out one-off shocks and captures short-run demand trend.
    out["STORE_UPC_ROLL4"] = (
        out.groupby(["STORE_NUM", "UPC"])["LOG_UNITS"]
        .transform(lambda x: x.shift(1).rolling(4, min_periods=1).mean())
    )

    # Fill NaN in lag/rolling features with global training mean (safe default)
    for col in ["STORE_UPC_LAG1", "STORE_UPC_ROLL4"]:
        if train_mask is not None:
            fill_val = out.loc[train_mask, col].mean()
        else:
            fill_val = out[col].mean()
        out[col] = out[col].fillna(fill_val)

    return out


def add_split_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add a 'split' column: 'train' for the first 130 weeks, 'test' for the last 26.
    The last 26 weeks correspond to the final 26 unique WEEK_END_DATE values.
    """
    weeks_sorted = sorted(df["WEEK_END_DATE"].unique())
    test_weeks = set(weeks_sorted[-26:])
    df = df.copy()
    df["split"] = df["WEEK_END_DATE"].apply(
        lambda w: "test" if w in test_weeks else "train"
    )
    return df


def get_feature_columns():
    """Return the full list of feature columns used in the model."""
    return NUMERIC_FEATURES + BINARY_FEATURES + CATEGORICAL_COLS
