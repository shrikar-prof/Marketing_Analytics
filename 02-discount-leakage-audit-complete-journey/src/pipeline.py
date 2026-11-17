# src/pipeline.py -- Discount Leakage Audit production pipeline.
#
# Usage:
#   python pipeline.py --train    [--features FEAT_PATH] [--model-out MODEL_PATH]
#   python pipeline.py --evaluate [--features FEAT_PATH] [--model-in  MODEL_PATH]
#   python pipeline.py --predict  --input INPUT_PATH [--model-in MODEL_PATH] [--output OUT_PATH]
#
# All preprocessing is inside the joblib pipeline; no external state.

import argparse, json, os, sys
import numpy as np
import pandas as pd
import joblib

sys.path.insert(0, os.path.dirname(__file__))
from features import ALL_FEATURES, TARGET, build_features
from model_utils import build_pipeline, SEED, capture_rate_top10, compute_ece, recoverable_margin

PROJECT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_FEAT  = os.path.join(PROJECT, "reports/modeling/features.parquet")
DEFAULT_MODEL = os.path.join(PROJECT, "models/discount_leakage_model.joblib")
DEFAULT_CFG   = os.path.join(PROJECT, "models/final_config.json")


def load_config():
    with open(DEFAULT_CFG) as fh:
        return json.load(fh)


def do_train(features_path, model_out):
    cfg = load_config()
    df = pd.read_parquet(features_path)
    train = df[df["split"] == "train"].sort_values("week")
    X = train[ALL_FEATURES]
    y = train[TARGET].values.astype("float32")

    import lightgbm as lgb, xgboost as xgb, catboost as cb
    from sklearn.linear_model import Ridge

    family = cfg["model_family"]
    # params already includes all constructor keys (random_state/seed, verbose, n_jobs)
    # because they were saved from the chosen_params dict. Do not re-pass them.
    params = cfg["model_params"]
    if family == "LightGBM":
        est = lgb.LGBMRegressor(**params)
    elif family == "XGBoost":
        est = xgb.XGBRegressor(**params)
    elif family == "CatBoost":
        est = cb.CatBoostRegressor(**params)
    else:
        est = Ridge(alpha=1.0, random_state=SEED)

    pipe = build_pipeline(est)
    print("Training %s on %d rows..." % (family, len(X)))
    pipe.fit(X, y)
    joblib.dump(pipe, model_out)
    print("Saved model: %s" % model_out)


def do_evaluate(features_path, model_in):
    df   = pd.read_parquet(features_path)
    pipe = joblib.load(model_in)
    test = df[df["split"] == "test"].sort_values("week")
    X = test[ALL_FEATURES]
    y = test[TARGET].values.astype("float32")
    lr = test["list_revenue"].values
    td = test["total_disc"].values

    preds = pipe.predict(X).clip(0, 1).astype("float32")
    from sklearn.metrics import mean_squared_error, r2_score
    rmse = float(np.sqrt(mean_squared_error(y, preds)))
    r2   = float(r2_score(y, preds))
    ece  = compute_ece(y, preds)
    cap  = capture_rate_top10(y, preds, td)
    rec  = recoverable_margin(y, preds, lr)

    print("RMSE              : %.4f" % rmse)
    print("R2                : %.4f" % r2)
    print("ECE               : %.4f" % ece)
    print("Capture @ top-10%% : %.4f" % cap)
    print("Recoverable margin: $%s" % f"{rec:,.0f}")
    return {"rmse": rmse, "r2": r2, "ece": ece, "capture_top10": cap, "recoverable_margin": rec}


def do_predict(input_path, model_in, output_path):
    pipe = joblib.load(model_in)
    raw  = pd.read_parquet(input_path) if input_path.endswith(".parquet") else pd.read_csv(input_path)
    X    = raw[ALL_FEATURES]
    preds = pipe.predict(X).clip(0, 1).astype("float32")
    raw["pred_disc_rate"] = preds
    raw.to_csv(output_path, index=False)
    print("Predictions saved: %s  (%d rows)" % (output_path, len(raw)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train",    action="store_true")
    parser.add_argument("--evaluate", action="store_true")
    parser.add_argument("--predict",  action="store_true")
    parser.add_argument("--features", default=DEFAULT_FEAT)
    parser.add_argument("--model-in",  default=DEFAULT_MODEL)
    parser.add_argument("--model-out", default=DEFAULT_MODEL)
    parser.add_argument("--input",     default=None)
    parser.add_argument("--output",    default="predictions.csv")
    args = parser.parse_args()

    if args.train:
        do_train(args.features, args.model_out)
    if args.evaluate:
        do_evaluate(args.features, args.model_in)
    if args.predict:
        if not args.input:
            raise ValueError("--predict requires --input")
        do_predict(args.input, args.model_in, args.output)
