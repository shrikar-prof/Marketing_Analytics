"""
features.py — shared feature definitions for the MMM budget-reallocation project.

Both notebooks/02_feature_engineering.ipynb and src/pipeline.py import from here
so the notebook analysis and the production pipeline cannot drift apart.
"""

import numpy as np
import pandas as pd

# ── Adstock (geometric decay) ────────────────────────────────────────────────

def geometric_adstock(series: pd.Series, decay: float) -> pd.Series:
    """
    Apply geometric adstock to a spend series.

    Formula:
        A_t = x_t + decay * A_{t-1}

    Parameters
    ----------
    series : weekly spend (sorted oldest to newest)
    decay  : carry-over fraction (0 = no carryover, 1 = permanent)

    Returns
    -------
    pd.Series of the same length, same index.
    """
    result = np.zeros(len(series))
    vals = series.values
    result[0] = vals[0]
    for t in range(1, len(vals)):
        result[t] = vals[t] + decay * result[t - 1]
    return pd.Series(result, index=series.index, name=series.name)


# ── Hill saturation ───────────────────────────────────────────────────────────

def hill_saturation(series: pd.Series, half_sat: float, slope: float) -> pd.Series:
    """
    Apply a Hill (Michaelis-Menten generalised) saturation curve.

    Formula:
        S(x) = x^slope / (half_sat^slope + x^slope)

    Maps any non-negative spend to [0, 1].

    Parameters
    ----------
    series   : adstocked spend (or raw spend)
    half_sat : spend level at which response is 0.5 of maximum
    slope    : steepness of the curve (Hill coefficient)
    """
    x = series.values.astype(float)
    h = half_sat ** slope
    with np.errstate(divide='ignore', invalid='ignore'):
        sat = np.where(x == 0, 0.0, x ** slope / (h + x ** slope))
    return pd.Series(sat, index=series.index, name=series.name)


# ── Log-spend (linearises diminishing returns for tree/linear models) ────────

def log1p_spend(series: pd.Series) -> pd.Series:
    """log(1 + spend) — avoids log(0) for zero-spend weeks."""
    return np.log1p(series).rename(series.name)


# ── Week-of-year seasonality (sine/cosine Fourier terms) ────────────────────

def add_fourier_terms(df: pd.DataFrame, date_col: str = "DATE",
                      periods: int = 52, order: int = 2) -> pd.DataFrame:
    """
    Add sine and cosine Fourier terms for annual seasonality.

    t = week number within the data (0-indexed).
    For k = 1 .. order:
        sin_k = sin(2 * pi * k * t / periods)
        cos_k = cos(2 * pi * k * t / periods)
    """
    df = df.copy()
    t = np.arange(len(df))
    for k in range(1, order + 1):
        df[f"sin_{k}"] = np.sin(2 * np.pi * k * t / periods)
        df[f"cos_{k}"] = np.cos(2 * np.pi * k * t / periods)
    return df


# ── Linear trend ─────────────────────────────────────────────────────────────

def add_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Add a normalised linear trend term: t / (n-1) in [0, 1]."""
    df = df.copy()
    n = len(df)
    df["trend"] = np.arange(n) / max(n - 1, 1)
    return df


# ── Print spend low-spend flag ────────────────────────────────────────────────

def print_low_flag(print_spend: pd.Series, q: float = 0.05) -> pd.Series:
    """
    Binary flag: 1 when print spend is in the bottom q-th percentile.
    Fit on training data only; apply to all splits.
    """
    threshold = print_spend.quantile(q)
    return (print_spend <= threshold).astype(int).rename("print_low_flag")


# ── Master feature-build function ─────────────────────────────────────────────

# Default adstock decay rates (motivated by typical MMM priors)
ADSTOCK_DECAYS = {
    "tv_S": 0.40,       # TV: moderate carryover (~2-3 weeks)
    "ooh_S": 0.30,      # Out-of-home: shorter carryover
    "print_S": 0.20,    # Print: near-immediate
    "facebook_S": 0.10, # Digital: very short
    "search_S": 0.05,   # Search: almost immediate
}

# Default Hill parameters (half-saturation at median spend level, slope=2)
HILL_PARAMS = {
    "tv_S": {"half_sat": 15000.0, "slope": 2.0},
    "ooh_S": {"half_sat": 8000.0, "slope": 2.0},
    "print_S": {"half_sat": 5000.0, "slope": 2.0},
    "facebook_S": {"half_sat": 3000.0, "slope": 2.0},
    "search_S": {"half_sat": 3000.0, "slope": 2.0},
}


def build_features(
    df: pd.DataFrame,
    date_col: str = "DATE",
    adstock_decays: dict = None,
    hill_params: dict = None,
    fourier_order: int = 2,
    print_low_q: float = 0.05,
    fit_print_threshold: float = None,
) -> pd.DataFrame:
    """
    Build the full feature matrix from the cleaned weekly data.

    Parameters
    ----------
    df                  : cleaned parquet (all 208 rows)
    adstock_decays      : override default decay rates
    hill_params         : override default Hill parameters
    fourier_order       : number of Fourier pairs for seasonality
    print_low_q         : quantile for the print low-spend flag
    fit_print_threshold : pre-computed threshold (use on test to avoid leakage)

    Returns
    -------
    DataFrame with all engineered features plus 'revenue', 'DATE', 'split'.
    """
    if adstock_decays is None:
        adstock_decays = ADSTOCK_DECAYS
    if hill_params is None:
        hill_params = HILL_PARAMS

    out = df[[date_col, "revenue", "competitor_sales_B",
              "event_flag", "newsletter"]].copy()

    spend_cols = ["tv_S", "ooh_S", "print_S", "facebook_S", "search_S"]

    # 1. Adstock (must be applied to full series in time order)
    for col in spend_cols:
        decay = adstock_decays.get(col, 0.0)
        out[f"{col}_adstock"] = geometric_adstock(df[col], decay)

    # 2. Hill saturation on adstocked series
    for col in spend_cols:
        hp = hill_params.get(col, {"half_sat": 5000.0, "slope": 2.0})
        out[f"{col}_sat"] = hill_saturation(
            out[f"{col}_adstock"], hp["half_sat"], hp["slope"]
        )

    # 3. Log-spend (for tree models and as an alternative to Hill)
    for col in spend_cols:
        out[f"{col}_log"] = log1p_spend(df[col])

    # 4. Total spend (budget constraint proxy)
    out["total_spend"] = df[spend_cols].sum(axis=1)
    out["total_spend_log"] = np.log1p(out["total_spend"])

    # 5. Print low-spend flag
    if fit_print_threshold is None:
        fit_print_threshold = df["print_S"].quantile(print_low_q)
    out["print_low_flag"] = (df["print_S"] <= fit_print_threshold).astype(int)

    # 6. Newsletter log
    out["newsletter_log"] = np.log1p(df["newsletter"])

    # 7. Competitor sales (log to compress scale)
    out["competitor_sales_log"] = np.log1p(df["competitor_sales_B"])

    # 8. Fourier terms
    out = add_fourier_terms(out, date_col=date_col, periods=52, order=fourier_order)

    # 9. Linear trend
    out = add_trend(out)

    return out


FEATURE_COLS_SAT = [
    "tv_S_sat", "ooh_S_sat", "print_S_sat", "facebook_S_sat", "search_S_sat",
    "newsletter_log", "competitor_sales_log", "event_flag",
    "total_spend_log", "print_low_flag", "trend",
    "sin_1", "cos_1", "sin_2", "cos_2",
]

FEATURE_COLS_LOG = [
    "tv_S_log", "ooh_S_log", "print_S_log", "facebook_S_log", "search_S_log",
    "newsletter_log", "competitor_sales_log", "event_flag",
    "total_spend_log", "print_low_flag", "trend",
    "sin_1", "cos_1", "sin_2", "cos_2",
]

TARGET_COL = "revenue"
DATE_COL = "DATE"
