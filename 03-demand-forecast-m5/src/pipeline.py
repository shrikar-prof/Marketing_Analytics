"""
Pipeline CLI for M5 demand forecasting.

Usage
-----
  python src/pipeline.py --train
      Fit the model on the full training set and save to models/.

  python src/pipeline.py --evaluate
      Load the saved model and evaluate on the held-out test set,
      printing RMSE, MAE, and mean RMSSE.

  python src/pipeline.py --train --evaluate
      Fit and immediately evaluate. Replicates Section 8 of notebook 03.

  python src/pipeline.py --predict --d-start 1942 --d-end 1969
      Load the saved model and produce forecasts for the given day range,
      saving to reports/modeling/forecast_d{start}_d{end}.csv.

This script imports from src.features and src.model_utils so the
notebook and the production pipeline use identical logic.

Notes
-----
- All data is read from reports/exploration/*.parquet (cleaned inputs).
- The model artefact is read from / written to models/demand_forecast_model.joblib.
- The script is NOT run with -I (isolated mode) to allow relative imports;
  it must be run from the project root directory.
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import time
import json

import numpy as np
import pandas as pd
import joblib

# Project root is the cwd when this script is run from the repo root.
PROJECT = pathlib.Path(__file__).parent.parent

sys.path.insert(0, str(PROJECT))
from src.features import (
    build_modeling_frame,
    TRAIN_START, VAL_START, TEST_START, TEST_END,
)
from src.model_utils import rmse, mae, compute_rmsse


FEATURE_COLS = [
    "lag_1", "lag_7", "lag_14", "lag_28", "lag_56",
    "roll_mean_7", "roll_mean_14", "roll_mean_28", "roll_std_7",
    "dow_sin", "dow_cos", "doy_sin", "doy_cos", "woy_sin", "woy_cos",
    "is_weekend", "is_month_start", "is_month_end", "year_norm",
    "is_sporting", "is_cultural", "is_national", "is_religious", "any_event",
    "snap",
    "sell_price", "price_ratio",
    "series_zero_rate", "series_mean", "series_std", "series_cv",
    "cat_id_enc", "dept_id_enc", "store_id_enc", "state_id_enc",
]
TARGET = "units"
MODEL_PATH = PROJECT / "models" / "demand_forecast_model.joblib"
FEATURES_PATH = PROJECT / "reports" / "modeling" / "features.parquet"


# ---------------------------------------------------------------------------
# --train
# ---------------------------------------------------------------------------

def train(args: argparse.Namespace) -> None:
    """Fit model on training split and save artefact."""
    import lightgbm as lgb

    print("[train] Loading feature frame ...")
    df = pd.read_parquet(str(FEATURES_PATH))
    train_mask = df["split"] == "train"
    val_mask   = df["split"] == "val"

    # Fill NaN in features
    for col in FEATURE_COLS:
        n_nan = df[col].isna().sum()
        if n_nan > 0:
            med = df.loc[train_mask, col].median()
            df[col] = df[col].fillna(med).astype(np.float32)

    X_tr = df.loc[train_mask, FEATURE_COLS].to_numpy(np.float32)
    y_tr = df.loc[train_mask, TARGET].to_numpy(np.float32)
    X_va = df.loc[val_mask,   FEATURE_COLS].to_numpy(np.float32)
    y_va = df.loc[val_mask,   TARGET].to_numpy(np.float32)
    print(f"[train] X_train={X_tr.shape}  X_val={X_va.shape}")

    # Load best params from saved artefact (if available) or use defaults
    if MODEL_PATH.exists():
        saved = joblib.load(str(MODEL_PATH))
        best_params = saved.get("best_params", {})
        print(f"[train] Using stored best params: {best_params}")
    else:
        best_params = {}
        print("[train] No saved params found; using LightGBM defaults.")

    default_params = dict(
        n_estimators=1000,
        learning_rate=0.05,
        num_leaves=127,
        min_child_samples=50,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_alpha=0.1,
        reg_lambda=0.1,
        n_jobs=-1,
        random_state=42,
        verbosity=-1,
    )
    default_params.update(best_params)

    model = lgb.LGBMRegressor(**default_params)
    t0 = time.time()
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_va, y_va)],
        callbacks=[lgb.early_stopping(50, verbose=False), lgb.log_evaluation(-1)],
    )
    elapsed = time.time() - t0
    print(f"[train] Training complete in {elapsed:.1f}s  best_iter={model.best_iteration_}")

    artefact = {
        "model":        model,
        "feature_cols": FEATURE_COLS,
        "best_params":  best_params,
        "train_shape":  X_tr.shape,
        "train_time_s": elapsed,
    }
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(artefact, str(MODEL_PATH))
    print(f"[train] Saved artefact to {MODEL_PATH}")


# ---------------------------------------------------------------------------
# --evaluate
# ---------------------------------------------------------------------------

def evaluate(args: argparse.Namespace) -> None:
    """Evaluate saved model on the held-out test set."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model artefact not found at {MODEL_PATH}. Run --train first.")

    artefact = joblib.load(str(MODEL_PATH))
    model       = artefact["model"]
    feat_cols   = artefact.get("feature_cols", FEATURE_COLS)

    print("[evaluate] Loading feature frame ...")
    df = pd.read_parquet(str(FEATURES_PATH))
    test_mask  = df["split"] == "test"
    train_mask = df["split"] == "train"

    for col in feat_cols:
        n_nan = df[col].isna().sum()
        if n_nan > 0:
            med = df.loc[train_mask, col].median()
            df[col] = df[col].fillna(med).astype(np.float32)

    X_te  = df.loc[test_mask, feat_cols].to_numpy(np.float32)
    y_te  = df.loc[test_mask, TARGET].to_numpy(np.float32)
    y_tr  = df.loc[train_mask, TARGET].to_numpy(np.float32)
    print(f"[evaluate] X_test={X_te.shape}")

    pred_te = np.maximum(0, model.predict(X_te))
    test_rmse = rmse(y_te, pred_te)
    test_mae  = mae(y_te, pred_te)

    # Per-series RMSSE
    train_df  = df[train_mask][["item_id", "store_id", "units"]].copy()
    test_df_e = df[test_mask][["item_id", "store_id", "units"]].copy()
    test_df_e["pred"] = pred_te

    series_scales = train_df.groupby(["item_id", "store_id"])["units"].apply(
        lambda x: np.mean(np.diff(x.to_numpy(np.float32)) ** 2)
    ).reset_index()
    series_scales.columns = ["item_id", "store_id", "scale"]

    test_rmsse_parts = test_df_e.groupby(["item_id", "store_id"]).apply(
        lambda g: pd.Series({"mse": np.mean((g["units"].to_numpy() - g["pred"].to_numpy()) ** 2)})
    ).reset_index()
    test_rmsse_parts = test_rmsse_parts.merge(series_scales, on=["item_id", "store_id"], how="left")
    test_rmsse_parts["rmsse"] = np.sqrt(
        test_rmsse_parts["mse"] / test_rmsse_parts["scale"].replace(0, np.nan)
    )
    mean_rmsse_val = test_rmsse_parts["rmsse"].dropna().mean()

    print("\n=== Evaluation Results (held-out test set) ===")
    print(f"  RMSE:       {test_rmse:.4f} units/item-day")
    print(f"  MAE:        {test_mae:.4f} units/item-day")
    print(f"  Mean RMSSE: {mean_rmsse_val:.4f}  (< 1.0 beats naive)")

    return {
        "test_rmse":       test_rmse,
        "test_mae":        test_mae,
        "mean_rmsse_test": mean_rmsse_val,
    }


# ---------------------------------------------------------------------------
# --predict
# ---------------------------------------------------------------------------

def predict(args: argparse.Namespace) -> None:
    """Score a forecast window and write predictions to CSV."""
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model artefact not found at {MODEL_PATH}. Run --train first.")

    artefact = joblib.load(str(MODEL_PATH))
    model     = artefact["model"]
    feat_cols = artefact.get("feature_cols", FEATURE_COLS)

    d_start = getattr(args, "d_start", TEST_START)
    d_end   = getattr(args, "d_end",   TEST_END)

    print(f"[predict] Building feature frame for d_{d_start} to d_{d_end} ...")
    df = build_modeling_frame(
        project_dir=PROJECT,
        d_window_start=d_start,
        d_window_end=d_end,
        verbose=True,
    )

    predict_mask = (df["d_col"] >= d_start) & (df["d_col"] <= d_end)

    for col in feat_cols:
        n_nan = df.loc[predict_mask, col].isna().sum()
        if n_nan > 0:
            med = df.loc[~predict_mask, col].median() if (~predict_mask).sum() > 0 else 0
            df[col] = df[col].fillna(med).astype(np.float32)

    X_pred = df.loc[predict_mask, feat_cols].to_numpy(np.float32)
    preds  = np.maximum(0, model.predict(X_pred))

    out = df.loc[predict_mask, ["item_id", "dept_id", "cat_id", "store_id", "state_id", "d_col", "date"]].copy()
    out["forecast_units"] = preds.astype(np.float32)

    out_path = PROJECT / "reports" / "modeling" / f"forecast_d{d_start}_d{d_end}.csv"
    out.to_csv(str(out_path), index=False)
    print(f"[predict] Saved {len(out):,} forecasts to {out_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="M5 Demand Forecast Pipeline")
    p.add_argument("--train",    action="store_true", help="Fit model on training data.")
    p.add_argument("--evaluate", action="store_true", help="Evaluate on held-out test set.")
    p.add_argument("--predict",  action="store_true", help="Produce forecast for a day range.")
    p.add_argument("--d-start",  type=int, default=TEST_START, help="First day to forecast (1-based).")
    p.add_argument("--d-end",    type=int, default=TEST_END,   help="Last day to forecast (1-based).")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if not args.train and not args.evaluate and not args.predict:
        print("Specify at least one of --train, --evaluate, --predict.")
        sys.exit(1)

    if args.train:
        train(args)

    if args.evaluate:
        evaluate(args)

    if args.predict:
        predict(args)
