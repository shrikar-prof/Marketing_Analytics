"""
features.py — shared feature engineering for the strategy teardown project.

Both notebooks import from here so the feature definitions cannot drift.
All transformations are pure functions of their inputs; no global state.
"""

import numpy as np
import pandas as pd


# ──────────────────────────────────────────────────────────────
# Five Below features
# ──────────────────────────────────────────────────────────────

def build_five_below_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build analysis features from the Five Below annual panel.

    Parameters
    ----------
    df : raw clean Five Below frame (8 rows × 16 cols from clean.parquet)

    Returns
    -------
    DataFrame with original columns plus engineered features.
    Sorted by fiscal_year ascending.
    """
    df = df.sort_values("fiscal_year").copy()

    # 1. Expansion rate — how aggressive was store growth relative to base
    #    Formula:  expansion_rate = net_new_stores / stores_eop_prior
    #    Motivation: explorer finding — net_new_stores highly collinear with stores_eop;
    #    rate normalises by scale so years are comparable.
    df["expansion_rate"] = df["net_new_stores"] / df["stores_eop"].shift(1)

    # 2. Revenue-per-store growth (YoY)
    #    Formula:  rev_per_store_yoy = (rev_per_store_m_t - rev_per_store_m_{t-1})
    #                                  / rev_per_store_m_{t-1}
    #    Motivation: measures new-store productivity dilution hypothesis.
    df["rev_per_store_yoy"] = df["rev_per_store_m"].pct_change()

    # 3. Lag-1 comparable sales (autoregressive signal)
    #    Formula:  comp_lag1 = comp_sales_pct_{t-1}
    df["comp_lag1"] = df["comp_sales_pct"].shift(1)

    # 4. Lag-1 operating margin
    #    Formula:  op_margin_lag1 = op_margin_pct_{t-1}
    df["op_margin_lag1"] = df["op_margin_pct"].shift(1)

    # 5. COVID flag already present as covid_affected (bool); cast to int
    df["covid_flag"] = df["covid_affected"].astype(int)

    # 6. Trend index — simple 0-based integer year counter
    #    Formula:  t = fiscal_year - min(fiscal_year)
    df["t"] = df["fiscal_year"] - df["fiscal_year"].min()

    # 7. High-expansion flag — years when net_new_stores > historical median
    median_nns = df["net_new_stores"].median()
    df["high_expansion"] = (df["net_new_stores"] > median_nns).astype(int)

    # 8. SGA intensity — SGA as share of revenue (cost pressure proxy)
    #    Formula:  sga_intensity = sga_usd / revenue_usd
    df["sga_intensity"] = df["sga_usd"] / df["revenue_usd"]

    return df


# ──────────────────────────────────────────────────────────────
# Netflix features
# ──────────────────────────────────────────────────────────────

PRICE_EVENTS = {
    # quarter label → event description
    "Q4'20": "price_hike_oct2020",
    "Q1'22": "price_hike_jan2022",
    "Q4'22": "ads_launch_nov2022",
    "Q2'23": "paid_sharing_may2023",
    "Q4'23": "price_hike_oct2023",
}


def build_netflix_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build analysis features from the Netflix UCAN quarterly panel.

    Parameters
    ----------
    df : raw clean Netflix frame (24 rows × 9 cols from netflix_clean.parquet)

    Returns
    -------
    DataFrame with engineered features added, sorted by end_date ascending.
    """
    df = df.sort_values("end_date").reset_index(drop=True).copy()

    # 1. Quarter-of-year (1–4) — seasonality control
    df["qtr"] = df["end_date"].dt.quarter

    # 2. Trend index (quarter count from start)
    df["t"] = np.arange(len(df))

    # 3. Lag-1 revenue (autoregressive)
    df["rev_lag1"] = df["revenue_usd_m"].shift(1)

    # 4. Lag-4 revenue (same quarter prior year baseline)
    df["rev_lag4"] = df["revenue_usd_m"].shift(4)

    # 5. ARM (average revenue per member) — pricing power signal
    #    Use ARM as a feature for revenue prediction.
    #    Note: do NOT also include paid_members_m when predicting revenue
    #    to avoid near-perfect collinearity (revenue ≈ ARM × members × 3).
    # arm_usd is already in the frame; keep it.

    # 6. ARM lag-1 — price changes lag membership response by one quarter
    df["arm_lag1"] = df["arm_usd"].shift(1)

    # 7. ARM YoY growth (already in frame as arm_yoy_pct)
    # Keep as-is.

    # 8. Price-event indicator — 1 in the quarter a material price change occurred
    #    or the quarter immediately after (demand response shows up with lag).
    price_event_quarters = set(PRICE_EVENTS.keys())
    df["price_event"] = df["quarter"].isin(price_event_quarters).astype(int)

    # 9. Post-paid-sharing — structural break from May 2023 (Q2'23 onward)
    #    Formula:  post_paid_sharing = 1 if end_date >= 2023-04-01 else 0
    df["post_paid_sharing"] = (df["end_date"] >= pd.Timestamp("2023-04-01")).astype(int)

    # 10. Rolling-4-quarter ARM mean (smoothed pricing trend)
    df["arm_roll4"] = df["arm_usd"].rolling(4, min_periods=2).mean()

    # 11. Members lag-1 (for the members model only; not used in revenue model)
    df["members_lag1"] = df["paid_members_m"].shift(1)

    return df
