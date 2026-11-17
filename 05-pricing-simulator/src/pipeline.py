"""
pipeline.py — production training, evaluation, and scoring pipeline.

Usage
-----
  python src/pipeline.py --train
      Fits the model on the full training split and writes
      models/pricing_model.joblib.

  python src/pipeline.py --train --evaluate
      Trains and then evaluates once on the held-out test split,
      printing RMSE_log, R², and MAPE_units.

  python src/pipeline.py --predict --input path/to/rows.parquet --output path/to/scores.csv
      Loads models/pricing_model.joblib, scores rows.parquet, writes scores.csv
      with columns: all input columns + pred_LOG_UNITS, pred_UNITS.

Design
------
All preprocessing is defined here using the same helpers as the notebooks so
the notebook and this script cannot drift apart.  The model type (LightGBM) and
the feature lists are imported from src/features.py and src/model_utils.py.
"""

import sys
import os
import argparse
import warnings

import numpy as np
import pandas as pd
import joblib
import lightgbm as lgb
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

warnings.filterwarnings("ignore")

# Allow running from any working directory
_HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(_HERE)
sys.path.insert(0, PROJECT)

from src.features import (
    build_features,
    add_split_column,
    NUMERIC_FEATURES,
    BINARY_FEATURES,
    CATEGORICAL_COLS,
    TARGET_COL,
    SEED,
)
from src.model_utils import (
    rmse,
    mape_units,
    make_preprocessor_no_scale,
)

MODEL_PATH = os.path.join(PROJECT, "models", "pricing_model.joblib")
FEATURES_PATH = os.path.join(PROJECT, "reports", "modeling", "features.parquet")


# ---------------------------------------------------------------------------
# Best hyperparameters (from Optuna tuning in notebook 03).
# Update these if re-tuning is run.
# ---------------------------------------------------------------------------
BEST_PARAMS = {
    "n_estimators": 600,
    "learning_rate": 0.02,
    "max_depth": 6,
    "num_leaves": 63,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_alpha": 0.1,
    "reg_lambda": 1.0,
    "min_child_samples": 30,
    "random_state": SEED,
    "n_jobs": -1,
    "verbose": -1,
}


def load_best_params():
    """Load best params from Optuna DB if available; fall back to defaults."""
    try:
        import optuna
        optuna.logging.set_verbosity(optuna.logging.WARNING)
        db = f"sqlite:///{PROJECT}/models/optuna_lgb.db"
        study = optuna.load_study(study_name="lgb_pricing", storage=db)
        p = study.best_params.copy()
        p.update({"random_state": SEED, "n_jobs": -1, "verbose": -1})
        return p
    except Exception:
        return BEST_PARAMS


def build_pipeline(params=None):
    """Return an unfitted sklearn Pipeline (preprocessor + LightGBM)."""
    if params is None:
        params = load_best_params()
    prep = make_preprocessor_no_scale(NUMERIC_FEATURES, BINARY_FEATURES, CATEGORICAL_COLS)
    model = lgb.LGBMRegressor(**params)
    return Pipeline([("prep", prep), ("model", model)])


def train(features_path=FEATURES_PATH, model_path=MODEL_PATH):
    """Fit on the training split and save the pipeline to model_path."""
    print(f"Loading features from {features_path}")
    feat = pd.read_parquet(features_path)

    # NaN fix: one row has PRICE = 0.0 → LOG_PRICE = NaN
    for col in NUMERIC_FEATURES:
        n = feat[col].isna().sum()
        if n > 0:
            med = feat.loc[feat["split"] == "train", col].median()
            feat[col] = feat[col].fillna(med)
            print(f"  Filled {n} NaN in {col} with training median {med:.4f}")

    train_df = feat[feat["split"] == "train"].copy()
    print(f"Training rows: {len(train_df):,}")

    pipe = build_pipeline()
    pipe.fit(train_df, train_df[TARGET_COL])

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(pipe, model_path)
    print(f"Model saved: {model_path}")
    return pipe, feat


def evaluate(pipe, feat):
    """Evaluate on the held-out test split (must be called only once)."""
    test_df = feat[feat["split"] == "test"].copy()
    y_test = test_df[TARGET_COL].values
    pred = pipe.predict(test_df)

    rmse_val = rmse(y_test, pred)
    r2_val = float(r2_score(y_test, pred))
    mape_val = mape_units(y_test, pred)

    print("\n=== Held-out test evaluation ===")
    print(f"  RMSE_log  : {rmse_val:.4f}  (error on log-unit scale)")
    print(f"  R²        : {r2_val:.4f}  (fraction of variance explained)")
    print(f"  MAPE_units: {mape_val:.1%}  (mean abs % error on actual units)")
    return {"RMSE_log": rmse_val, "R2": r2_val, "MAPE_units": mape_val}


def predict(input_path, output_path, model_path=MODEL_PATH):
    """Score rows from input_path and write predictions to output_path."""
    print(f"Loading model from {model_path}")
    pipe = joblib.load(model_path)

    print(f"Loading input rows from {input_path}")
    rows = pd.read_parquet(input_path)

    # Apply NaN fix
    for col in NUMERIC_FEATURES:
        if col in rows.columns and rows[col].isna().any():
            med = rows[col].median()
            rows[col] = rows[col].fillna(med)

    pred_log = pipe.predict(rows)
    rows["pred_LOG_UNITS"] = pred_log
    rows["pred_UNITS"] = np.expm1(pred_log)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    rows.to_csv(output_path, index=False)
    print(f"Predictions written: {output_path}  ({len(rows):,} rows)")


def main():
    parser = argparse.ArgumentParser(description="Pricing simulator pipeline")
    parser.add_argument("--train", action="store_true", help="Fit and save model")
    parser.add_argument("--evaluate", action="store_true",
                        help="Evaluate on held-out test (use with --train)")
    parser.add_argument("--predict", action="store_true", help="Score new rows")
    parser.add_argument("--input", default=None, help="Input parquet for --predict")
    parser.add_argument("--output", default=None, help="Output CSV for --predict")
    parser.add_argument("--features", default=FEATURES_PATH,
                        help="features.parquet path (default: reports/modeling/features.parquet)")
    parser.add_argument("--model", default=MODEL_PATH,
                        help="Model joblib path (default: models/pricing_model.joblib)")
    args = parser.parse_args()

    if args.train:
        pipe, feat = train(features_path=args.features, model_path=args.model)
        if args.evaluate:
            evaluate(pipe, feat)

    elif args.predict:
        if not args.input or not args.output:
            parser.error("--predict requires --input and --output")
        predict(args.input, args.output, model_path=args.model)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
