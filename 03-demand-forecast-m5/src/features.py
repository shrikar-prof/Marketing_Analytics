"""
Feature engineering functions for M5 demand forecasting.

All functions are pure (stateless given their inputs) so the notebook
and the production pipeline use identical logic without drift.

Design principles
-----------------
- Work in wide format (30 490 × T numpy array) before melting; this
  makes lag and rolling operations O(T) column-shifts rather than
  O(N x T) groupby-shift operations.
- Convert to float32 throughout; int16 for the sales matrix where the
  range is known (0–763 units).
- Slice to the modeling window AFTER computing features so we never
  read the full 59 M-row long frame into RAM.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------------------------
# Split boundaries (day indices, 1-based, matching M5 d_* column names)
# ---------------------------------------------------------------------------
# History available in clean.parquet: d_1 to d_1941
# Lag requirement: 28 days minimum → modeling window starts at d_29
# We use the last 2 years of training data to fit the model:
#   - Warm-up for lag validity: d_1183 to d_1210 (not in features.parquet)
#   - Training split: d_1211 to d_1885   (675 days)
#   - Validation split: d_1886 to d_1913 (28 days) — walk-forward fold 3
#   - Test split: d_1914 to d_1941       (28 days) — final held-out
TRAIN_START = 1211   # First day included in modeling frame (after warm-up)
VAL_START   = 1886   # First day of validation window
TEST_START  = 1914   # First day of held-out test
TEST_END    = 1941   # Last day available in clean.parquet
LAG_WARMUP  = 56     # Days of history needed before TRAIN_START for lag_56


def load_raw_data(project_dir: str | Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the three cleaned parquet files produced by the exploration notebook.

    Returns
    -------
    sales : wide DataFrame (30 490 rows × 1 946 cols: id cols + d_1…d_1941)
    calendar : long DataFrame (1 969 rows, one per day)
    prices : sell prices (store × item × wm_yr_wk × price)
    """
    p = Path(project_dir) / "reports" / "exploration"
    sales    = pd.read_parquet(p / "clean.parquet")
    calendar = pd.read_parquet(p / "calendar_clean.parquet")
    prices   = pd.read_parquet(p / "sell_prices_clean.parquet")
    return sales, calendar, prices


def _sales_matrix(sales: pd.DataFrame) -> np.ndarray:
    """Extract the (30 490 × 1 941) int16 sales matrix from the wide frame."""
    d_cols = [f"d_{i}" for i in range(1, 1942)]
    mat = sales[d_cols].to_numpy(dtype=np.int16)   # 118 MB
    return mat


# ---------------------------------------------------------------------------
# Calendar feature builder
# ---------------------------------------------------------------------------

def build_calendar_features(calendar: pd.DataFrame) -> pd.DataFrame:
    """Return a 1 969-row DataFrame with all calendar-derived model inputs.

    Features built
    --------------
    dow_sin, dow_cos  : cyclic day-of-week (period 7)
    doy_sin, doy_cos  : cyclic day-of-year (period 365)
    woy_sin, woy_cos  : cyclic week-of-year (period 52)
    is_weekend        : 1 if Saturday or Sunday
    is_month_start    : 1 if day-of-month ≤ 3
    is_month_end      : 1 if day-of-month ≥ 28 (approximation; works for all months)
    year_norm         : (year - 2011) / 5  — linear trend feature
    is_sporting       : 1 if any event type is Sporting
    is_cultural       : 1 if any event type is Cultural
    is_national       : 1 if any event type is National
    is_religious      : 1 if any event type is Religious
    any_event         : 1 if any event at all
    snap_CA, snap_TX, snap_WI : pass-through binary flags
    d_col             : integer day index (1-based)
    wm_yr_wk          : Walmart fiscal year-week (for price join)
    date              : parsed date (datetime64)
    """
    cal = calendar.copy()

    # Ensure date is datetime
    if cal["date"].dtype == object:
        cal["date"] = pd.to_datetime(cal["date"])
    if "date_parsed" in cal.columns:
        cal["date"] = pd.to_datetime(cal["date_parsed"])

    # Day-of-week (Python: Monday=0 … Sunday=6)
    dow = cal["date"].dt.dayofweek.astype(np.float32)
    cal["dow_sin"] = np.sin(2 * np.pi * dow / 7).astype(np.float32)
    cal["dow_cos"] = np.cos(2 * np.pi * dow / 7).astype(np.float32)

    # Day-of-year
    doy = cal["date"].dt.dayofyear.astype(np.float32)
    cal["doy_sin"] = np.sin(2 * np.pi * doy / 365).astype(np.float32)
    cal["doy_cos"] = np.cos(2 * np.pi * doy / 365).astype(np.float32)

    # Week-of-year
    woy = cal["date"].dt.isocalendar().week.astype(np.float32).values
    cal["woy_sin"] = np.sin(2 * np.pi * woy / 52).astype(np.float32)
    cal["woy_cos"] = np.cos(2 * np.pi * woy / 52).astype(np.float32)

    # Weekend flag
    cal["is_weekend"] = (dow >= 5).astype(np.int8)

    # Month-start / month-end proximity
    dom = cal["date"].dt.day
    cal["is_month_start"] = (dom <= 3).astype(np.int8)
    cal["is_month_end"]   = (dom >= 28).astype(np.int8)

    # Linear trend
    cal["year_norm"] = ((cal["date"].dt.year - 2011) / 5).astype(np.float32)

    # Event flags — handle NaN ("None")
    def _event_flag(col: str, val: str) -> pd.Series:
        s1 = cal.get("event_type_1", pd.Series(dtype=object)).fillna("None")
        s2 = cal.get("event_type_2", pd.Series(dtype=object)).fillna("None")
        return ((s1 == val) | (s2 == val)).astype(np.int8)

    cal["is_sporting"]  = _event_flag("event_type_1", "Sporting")
    cal["is_cultural"]  = _event_flag("event_type_1", "Cultural")
    cal["is_national"]  = _event_flag("event_type_1", "National")
    cal["is_religious"] = _event_flag("event_type_1", "Religious")
    cal["any_event"]    = (
        cal["is_sporting"] | cal["is_cultural"] |
        cal["is_national"] | cal["is_religious"]
    ).astype(np.int8)

    # d_col: row index + 1 (calendar runs d_1 to d_1969 by row)
    if "d_col" not in cal.columns:
        cal["d_col"] = np.arange(1, len(cal) + 1, dtype=np.int16)
    else:
        # d_col may be stored as string 'd_1', 'd_2', … — extract the integer
        dcol = cal["d_col"]
        if dcol.dtype == object:
            cal["d_col"] = dcol.str.replace("d_", "", regex=False).astype(np.int16)
        else:
            cal["d_col"] = dcol.astype(np.int16)

    keep = [
        "d_col", "date", "wm_yr_wk",
        "dow_sin", "dow_cos", "doy_sin", "doy_cos",
        "woy_sin", "woy_cos", "is_weekend",
        "is_month_start", "is_month_end", "year_norm",
        "is_sporting", "is_cultural", "is_national", "is_religious", "any_event",
        "snap_CA", "snap_TX", "snap_WI",
    ]
    return cal[keep].reset_index(drop=True)


# ---------------------------------------------------------------------------
# Wide-format lag / rolling feature computation
# ---------------------------------------------------------------------------

def _shift_right(mat: np.ndarray, n: int) -> np.ndarray:
    """Shift the sales matrix n columns to the right (introduce n NaN columns on left).

    Shape: (n_series, T)
    Result[i, t] = mat[i, t-n]  (i.e., the value n days ago)
    """
    out = np.empty(mat.shape, dtype=np.float32)
    out[:, :n] = np.nan
    out[:, n:] = mat[:, :-n].astype(np.float32)
    return out


def _rolling_mean(mat: np.ndarray, window: int) -> np.ndarray:
    """Rolling mean over the last `window` days (trailing, inclusive).

    Uses cumsum trick for O(T) complexity.
    """
    mat_f = mat.astype(np.float32)
    cs = np.cumsum(mat_f, axis=1)
    out = np.empty(mat_f.shape, dtype=np.float32)
    out[:, :window - 1] = np.nan
    out[:, window - 1:] = (cs[:, window - 1:] - np.hstack([np.zeros((mat_f.shape[0], 1)), cs[:, :-window]])) / window
    return out


def _rolling_std(mat: np.ndarray, window: int) -> np.ndarray:
    """Rolling std over the last `window` days (trailing, inclusive).

    Uses the identity var = E[x^2] - E[x]^2 evaluated with cumsum for O(T) speed.
    """
    mat_f = mat.astype(np.float32)
    cs    = np.cumsum(mat_f, axis=1)
    cs_sq = np.cumsum(mat_f ** 2, axis=1)
    out   = np.full(mat_f.shape, np.nan, dtype=np.float32)
    zeros = np.zeros((mat_f.shape[0], 1), dtype=np.float32)
    roll_sum    = cs[:, window - 1:] - np.hstack([zeros, cs[:, :-(window)]])
    roll_sum_sq = cs_sq[:, window - 1:] - np.hstack([zeros, cs_sq[:, :-(window)]])
    roll_mean   = roll_sum / window
    roll_var    = np.maximum(0, roll_sum_sq / window - roll_mean ** 2)
    out[:, window - 1:] = np.sqrt(roll_var)
    return out


def compute_wide_lag_features(sales_mat: np.ndarray) -> dict[str, np.ndarray]:
    """Compute all lag and rolling features in wide format.

    Parameters
    ----------
    sales_mat : int16 array of shape (n_series, 1941)

    Returns
    -------
    dict mapping feature name → float32 array of shape (n_series, 1941)
    """
    feats = {}
    for lag in [1, 7, 14, 28, 56]:
        feats[f"lag_{lag}"] = _shift_right(sales_mat, lag)
    for w in [7, 14, 28]:
        feats[f"roll_mean_{w}"] = _rolling_mean(sales_mat, w)
    # Rolling std for 7 days (volatility signal)
    # NOTE: std is expensive for large windows; compute only window=7
    feats["roll_std_7"] = _rolling_std(sales_mat, 7)
    return feats


# ---------------------------------------------------------------------------
# Price feature builder
# ---------------------------------------------------------------------------

def build_price_features(
    sales_id: pd.DataFrame,
    prices: pd.DataFrame,
    calendar_feats: pd.DataFrame,
    modeling_d_range: tuple[int, int],
) -> pd.DataFrame:
    """Build price features for the modeling window.

    For each (store_id, item_id, wm_yr_wk) in the modeling window:
      - sell_price: current week price
      - price_lag4: price 4 weeks ago (to detect promotions)
      - price_ratio: sell_price / price_lag4

    Returns a DataFrame indexed by (store_id, item_id, d_col).
    """
    d_start, d_end = modeling_d_range

    # Build a lookup: (store_id, item_id, wm_yr_wk) → sell_price
    price_lkp = prices.set_index(["store_id", "item_id", "wm_yr_wk"])["sell_price"]

    # Calendar for the modeling window
    cal_window = calendar_feats[
        (calendar_feats["d_col"] >= d_start) & (calendar_feats["d_col"] <= d_end)
    ][["d_col", "wm_yr_wk"]].copy()

    # Unique weeks in the modeling window + 4-week lookback
    min_wk = cal_window["wm_yr_wk"].min()
    max_wk = cal_window["wm_yr_wk"].max()

    # Build a price table per series × week
    price_weekly = prices[
        (prices["wm_yr_wk"] >= min_wk) & (prices["wm_yr_wk"] <= max_wk)
    ].copy()
    price_weekly = price_weekly.sort_values(["store_id", "item_id", "wm_yr_wk"])
    price_weekly["price_lag4"] = price_weekly.groupby(["store_id", "item_id"])["sell_price"].shift(4)
    price_weekly["price_ratio"] = (
        price_weekly["sell_price"] / price_weekly["price_lag4"].replace(0, np.nan)
    ).astype(np.float32)
    price_weekly["sell_price"] = price_weekly["sell_price"].astype(np.float32)
    price_weekly["price_lag4"] = price_weekly["price_lag4"].astype(np.float32)

    return price_weekly[["store_id", "item_id", "wm_yr_wk", "sell_price", "price_lag4", "price_ratio"]]


# ---------------------------------------------------------------------------
# State-matched SNAP feature
# ---------------------------------------------------------------------------

def add_snap_feature(df: pd.DataFrame) -> pd.DataFrame:
    """Add a single `snap` column that picks the right state's SNAP flag.

    Looks up snap_CA, snap_TX, snap_WI based on the series' state_id.
    """
    snap_map = {"CA": "snap_CA", "TX": "snap_TX", "WI": "snap_WI"}
    snaps = []
    for state, col in snap_map.items():
        mask = df["state_id"] == state
        snaps.append(df.loc[mask, col])
    df["snap"] = pd.concat(snaps).reindex(df.index).astype(np.int8)
    # Drop the per-state columns
    df = df.drop(columns=["snap_CA", "snap_TX", "snap_WI"], errors="ignore")
    return df


# ---------------------------------------------------------------------------
# Series-level metadata features (computed on training rows only)
# ---------------------------------------------------------------------------

def compute_series_stats(
    long_df: pd.DataFrame,
    train_mask: pd.Series,
) -> pd.DataFrame:
    """Compute per-series statistics from training rows only.

    Features
    --------
    series_zero_rate  : fraction of training days with 0 sales
    series_mean       : mean units across all training days
    series_std        : std of units on training days
    series_cv         : coefficient of variation on non-zero training days

    Returns a DataFrame indexed by (item_id, store_id).
    """
    train = long_df[train_mask].copy()
    grp = train.groupby(["item_id", "store_id"])["units"]

    stats = pd.DataFrame({
        "series_zero_rate": grp.apply(lambda x: (x == 0).mean()),
        "series_mean":      grp.mean(),
        "series_std":       grp.std(),
    }).astype(np.float32)

    # CV on non-zero days
    cv = grp.apply(lambda x: x[x > 0].std() / x[x > 0].mean() if (x > 0).any() else np.nan)
    stats["series_cv"] = cv.astype(np.float32)

    return stats.reset_index()


# ---------------------------------------------------------------------------
# Identifier encoding
# ---------------------------------------------------------------------------

def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Ordinal-encode the categorical ID columns.

    Encodes: cat_id (3), dept_id (7), store_id (10), state_id (3)
    Returns df with added *_enc columns (int8).
    """
    maps = {
        "cat_id": {v: i for i, v in enumerate(sorted(df["cat_id"].unique()))},
        "dept_id": {v: i for i, v in enumerate(sorted(df["dept_id"].unique()))},
        "store_id": {v: i for i, v in enumerate(sorted(df["store_id"].unique()))},
        "state_id": {v: i for i, v in enumerate(sorted(df["state_id"].unique()))},
    }
    for col, mapping in maps.items():
        df[col + "_enc"] = df[col].map(mapping).astype(np.int8)
    return df, maps


# ---------------------------------------------------------------------------
# Assembly: build the full modeling frame
# ---------------------------------------------------------------------------

def build_modeling_frame(
    project_dir: str | Path,
    d_window_start: int = TRAIN_START,
    d_window_end: int = TEST_END,
    warmup_days: int = LAG_WARMUP,
    verbose: bool = True,
) -> pd.DataFrame:
    """Build the complete modeling frame for the given day window.

    Steps
    -----
    1. Load raw parquets.
    2. Compute lag / rolling features in wide format.
    3. Melt the modeling window + warmup slice to long format.
    4. Merge calendar features.
    5. Merge price features.
    6. Add state-matched SNAP flag.
    7. Compute series-level stats from training rows only.
    8. Encode categoricals.
    9. Add `split` column.

    Parameters
    ----------
    d_window_start : first day index in the final modeling frame (no warmup)
    d_window_end   : last day index in the final modeling frame
    warmup_days    : extra days before d_window_start for lag validity

    Returns
    -------
    DataFrame with columns: item_id, dept_id, cat_id, store_id, state_id,
        d_col, units, [all features], split
    """
    if verbose:
        print("Loading raw parquets ...")
    sales, calendar, prices = load_raw_data(project_dir)

    if verbose:
        print("Building sales matrix ...")
    mat = _sales_matrix(sales)                     # (30490, 1941) int16

    if verbose:
        print("Computing lag features (wide format) ...")
    wide_feats = compute_wide_lag_features(mat)   # dict of (30490, 1941) float32

    # Slice to: warmup + modeling window
    slice_start = max(0, d_window_start - warmup_days - 1)   # 0-indexed
    slice_end   = d_window_end                                 # 1-indexed → exclusive

    # Build ID frame (stays wide with 30490 rows)
    id_cols = ["item_id", "dept_id", "cat_id", "store_id", "state_id"]
    id_frame = sales[id_cols].copy()

    # Collect d_col indices for the slice
    d_indices = list(range(slice_start, slice_end))   # 0-indexed positions
    d_names   = [f"d_{i+1}" for i in d_indices]

    if verbose:
        print(f"Melting {len(d_names)} day columns × {len(id_frame)} series → {len(d_names)*len(id_frame):,} rows ...")

    # Build long frame with units
    units_slice = mat[:, d_indices].astype(np.float32)   # (30490, len_d)
    n_series, n_days = units_slice.shape
    n_rows = n_series * n_days

    # Repeat id_frame for each day, tile days for each series
    id_rep = pd.concat([id_frame] * n_days, ignore_index=True)
    # Sort correctly: for each series, all days in order
    # id_rep: row 0 is series 0 for all days (wrong); need interleaved
    # Actually pd.concat([id_frame]*n_days) gives series-first order
    # Units_slice.T.ravel() gives day-first order
    # We need: for row r = series*n_days + day => series=r//n_days, day=r%n_days
    id_rep = id_frame.loc[id_frame.index.repeat(n_days)].reset_index(drop=True)
    d_col_arr = np.tile(np.array([i+1 for i in d_indices], dtype=np.int16), n_series)
    units_arr = units_slice.ravel()   # row-major: series0_day0, series0_day1, ...

    long = id_rep.copy()
    long["d_col"] = d_col_arr
    long["units"] = units_arr.astype(np.float32)

    # Add lag/rolling features
    for feat_name, feat_mat in wide_feats.items():
        long[feat_name] = feat_mat[:, d_indices].ravel().astype(np.float32)

    if verbose:
        print("Merging calendar features ...")
    cal_feats = build_calendar_features(calendar)
    long = long.merge(cal_feats, on="d_col", how="left")

    if verbose:
        print("Merging price features ...")
    price_feats = build_price_features(
        id_frame, prices, cal_feats,
        modeling_d_range=(d_window_start - warmup_days, d_window_end)
    )
    long = long.merge(price_feats, on=["store_id", "item_id", "wm_yr_wk"], how="left")

    if verbose:
        print("Adding state-matched SNAP flag ...")
    long = add_snap_feature(long)

    if verbose:
        print("Adding split column ...")
    long["split"] = "train"
    long.loc[long["d_col"] >= VAL_START, "split"]  = "val"
    long.loc[long["d_col"] >= TEST_START, "split"] = "test"
    # Warmup rows (before d_window_start) are marked 'warmup' — excluded from model
    long.loc[long["d_col"] < d_window_start, "split"] = "warmup"

    if verbose:
        print("Computing series stats from training rows ...")
    train_mask = long["split"] == "train"
    series_stats = compute_series_stats(long, train_mask)
    long = long.merge(series_stats, on=["item_id", "store_id"], how="left")

    if verbose:
        print("Encoding categoricals ...")
    long, cat_maps = encode_categoricals(long)

    if verbose:
        print(f"Final frame shape: {long.shape}")
        print(long["split"].value_counts().to_string())

    return long
