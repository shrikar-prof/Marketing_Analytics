"""
pipeline.py — production training, evaluation, and prediction pipeline for the MMM project.

Usage:
  python src/pipeline.py --train --evaluate
  python src/pipeline.py --predict --input path/to/new_data.parquet

This script reuses the same feature-build functions as the notebooks so the two cannot drift.
"""

import argparse
import os
import sys
import numpy as np
import pandas as pd
import joblib

# Allow running from project root
_this_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _this_dir)

from features import build_features, FEATURE_COLS_LOG, FEATURE_COLS_SAT
from model_utils import compute_all_metrics

PROJECT = os.path.abspath(os.path.join(_this_dir, '..'))
MODEL_PATH = os.path.join(PROJECT, 'models', 'mmm_model.joblib')
DATA_PATH  = os.path.join(PROJECT, 'reports', 'exploration', 'clean.parquet')
SCORES_PATH = os.path.join(PROJECT, 'reports', 'modeling', 'scores.csv')

SEED = 42
N_TEST = 20


def load_and_split(data_path: str = DATA_PATH):
    df = pd.read_parquet(data_path)
    df = df.sort_values('DATE').reset_index(drop=True)
    n = len(df)
    df['split'] = 'train'
    df.loc[df.index >= (n - N_TEST), 'split'] = 'test'
    return df


def build_feature_matrix(df: pd.DataFrame):
    feat_df = build_features(df, date_col='DATE')
    return feat_df


def train(df: pd.DataFrame = None, feature_set: str = 'log'):
    """Train the final Ridge model and save it."""
    if df is None:
        df = load_and_split()

    feat_df = build_feature_matrix(df)
    train_mask = df['split'] == 'train'

    feat_cols = FEATURE_COLS_LOG if feature_set == 'log' else FEATURE_COLS_SAT
    X_train = feat_df.loc[train_mask, feat_cols]
    y_train = feat_df.loc[train_mask, 'revenue']

    from sklearn.linear_model import Ridge
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    # Use best alpha from tuning (default fallback)
    try:
        import optuna
        storage = f'sqlite:///{os.path.join(PROJECT, "models", "optuna_ridge.db")}'
        study = optuna.load_study(study_name='ridge', storage=storage)
        alpha = study.best_params['alpha']
    except Exception:
        alpha = 10.0
    print(f'Training Ridge with alpha={alpha:.4f} on {len(X_train)} rows...')

    model = Pipeline([('scaler', StandardScaler()), ('model', Ridge(alpha=alpha))])
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    print(f'Model saved: {MODEL_PATH}')
    return model, feat_cols


def evaluate(model=None, feat_cols=None, df: pd.DataFrame = None):
    """Evaluate on the held-out test set."""
    if df is None:
        df = load_and_split()
    feat_df = build_feature_matrix(df)

    if feat_cols is None:
        feat_cols = FEATURE_COLS_LOG
    if model is None:
        model = joblib.load(MODEL_PATH)

    test_mask = df['split'] == 'test'
    X_test = feat_df.loc[test_mask, feat_cols]
    y_test = feat_df.loc[test_mask, 'revenue']

    preds = model.predict(X_test)
    metrics = compute_all_metrics(y_test.values, preds, 'Ridge (test)')
    print('=== Evaluation on held-out test set ===')
    print(f'  RMSE:  ${metrics["RMSE"]:,.0f}')
    print(f'  MAE:   ${metrics["MAE"]:,.0f}')
    print(f'  MAPE:  {metrics["MAPE_%"]:.1f}%')
    print(f'  R²:    {metrics["R2"]:.3f}')
    return metrics


def predict(input_path: str, output_path: str = None, feat_cols=None):
    """Score new data from a parquet file."""
    df_new = pd.read_parquet(input_path)
    df_new = df_new.sort_values('DATE').reset_index(drop=True)
    feat_df = build_features(df_new, date_col='DATE')
    if feat_cols is None:
        feat_cols = FEATURE_COLS_LOG
    model = joblib.load(MODEL_PATH)
    X = feat_df[feat_cols]
    preds = model.predict(X)
    result = df_new[['DATE']].copy()
    result['predicted_revenue'] = preds
    if output_path:
        result.to_csv(output_path, index=False)
        print(f'Predictions saved: {output_path}')
    return result


def main():
    parser = argparse.ArgumentParser(description='MMM Pipeline')
    parser.add_argument('--train',    action='store_true', help='Train the model')
    parser.add_argument('--evaluate', action='store_true', help='Evaluate on test set')
    parser.add_argument('--predict',  action='store_true', help='Score new data')
    parser.add_argument('--input',    type=str, default=None, help='Input parquet for --predict')
    parser.add_argument('--output',   type=str, default=None, help='Output CSV for --predict')
    args = parser.parse_args()

    df = load_and_split()
    model, feat_cols = None, FEATURE_COLS_LOG

    if args.train or args.evaluate:
        model, feat_cols = train(df)
    if args.evaluate:
        evaluate(model, feat_cols, df)
    if args.predict:
        if not args.input:
            print('--input required for --predict')
            sys.exit(1)
        predict(args.input, args.output, feat_cols)


if __name__ == '__main__':
    main()
