#!/usr/bin/env python
"""
pipeline.py — production training/evaluation/prediction CLI for strategy teardowns.

Usage:
  python pipeline.py --train             # Fit all models and save to models/
  python pipeline.py --evaluate          # Evaluate on training data (CV) and test set
  python pipeline.py --predict           # Predict on all rows in features parquet
  python pipeline.py --train --evaluate  # Train then evaluate (recommended)
"""
import argparse
import os
import sys

PROJECT = '/Users/shrikar/Documents/Marketing Analytics/06-strategy-teardowns'
sys.path.insert(0, os.path.join(PROJECT, 'src'))

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error
import joblib
import warnings
warnings.filterwarnings('ignore')

from features import build_five_below_features, build_netflix_features
from model_utils import loocv_ridge, walk_forward_cv


FEATS_COMP   = ['expansion_rate', 'covid_flag']
FEATS_MARGIN = ['sga_intensity', 'op_margin_lag1', 'covid_flag']
FEATS_NF_REV = ['arm_lag1', 'rev_lag1', 'post_paid_sharing', 'qtr']
FEATS_NF_MEM = ['members_lag1', 'price_event', 'post_paid_sharing']


def load_data():
    fb_raw = pd.read_parquet(os.path.join(PROJECT, 'reports/exploration/clean.parquet'))
    nf_raw = pd.read_parquet(os.path.join(PROJECT, 'reports/exploration/netflix_clean.parquet'))
    fb = build_five_below_features(fb_raw)
    nf = build_netflix_features(nf_raw)
    nf['split'] = np.where(nf['end_date'] >= '2025-01-01', 'test', 'train')
    fb['split'] = 'train'
    return fb, nf


def train(fb, nf):
    fb_s = fb.sort_values('fiscal_year').reset_index(drop=True)
    nf_tr = nf[nf['split'] == 'train'].sort_values('end_date').reset_index(drop=True)

    # Five Below comp model
    sub = fb_s[FEATS_COMP + ['comp_sales_pct']].dropna()
    res = loocv_ridge(sub[FEATS_COMP], sub['comp_sales_pct'])
    pipe = Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(alpha=res['best_alpha']))])
    pipe.fit(sub[FEATS_COMP], sub['comp_sales_pct'])
    joblib.dump(pipe, os.path.join(PROJECT, 'models/fivebelow_comp_model.joblib'))
    print(f"Five Below comp model saved  (alpha={res['best_alpha']}, LOOCV MAE={res['mae']:.2f} ppt)")

    # Five Below margin model
    sub = fb_s[FEATS_MARGIN + ['op_margin_pct']].dropna()
    res = loocv_ridge(sub[FEATS_MARGIN], sub['op_margin_pct'])
    pipe = Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(alpha=res['best_alpha']))])
    pipe.fit(sub[FEATS_MARGIN], sub['op_margin_pct'])
    joblib.dump(pipe, os.path.join(PROJECT, 'models/fivebelow_margin_model.joblib'))
    print(f"Five Below margin model saved (alpha={res['best_alpha']}, LOOCV MAE={res['mae']:.2f} ppt)")

    # Netflix revenue model
    sub = nf_tr[FEATS_NF_REV + ['revenue_usd_m']].dropna()
    res = walk_forward_cv(sub[FEATS_NF_REV], sub['revenue_usd_m'], min_train=8)
    pipe = Pipeline([('scaler', StandardScaler()), ('ridge', Ridge(alpha=res['best_alpha']))])
    pipe.fit(sub[FEATS_NF_REV], sub['revenue_usd_m'])
    joblib.dump(pipe, os.path.join(PROJECT, 'models/netflix_revenue_model.joblib'))
    print(f"Netflix revenue model saved  (alpha={res['best_alpha']}, WF-CV MAE=${res['mae']:.1f}M)")

    print('Training complete.')


def evaluate(fb, nf):
    fb_s = fb.sort_values('fiscal_year').reset_index(drop=True)
    nf_tr = nf[nf['split'] == 'train'].sort_values('end_date').reset_index(drop=True)

    sub = fb_s[FEATS_COMP + ['comp_sales_pct']].dropna()
    res = loocv_ridge(sub[FEATS_COMP], sub['comp_sales_pct'])
    print(f"Five Below comp_sales_pct  LOOCV MAE: {res['mae']:.2f} ppt  R2={res['r2']:.3f}")

    sub = fb_s[FEATS_MARGIN + ['op_margin_pct']].dropna()
    res = loocv_ridge(sub[FEATS_MARGIN], sub['op_margin_pct'])
    print(f"Five Below op_margin_pct   LOOCV MAE: {res['mae']:.2f} ppt  R2={res['r2']:.3f}")

    sub = nf_tr[FEATS_NF_REV + ['revenue_usd_m']].dropna()
    res = walk_forward_cv(sub[FEATS_NF_REV], sub['revenue_usd_m'], min_train=8)
    print(f"Netflix revenue_usd_m      WF-CV MAE: ${res['mae']:.1f}M  R2={res['r2']:.3f}")

    # Test set evaluation
    nf_te = nf[nf['split'] == 'test'].sort_values('end_date')
    pipe_nf = joblib.load(os.path.join(PROJECT, 'models/netflix_revenue_model.joblib'))
    sub_te = nf_te[FEATS_NF_REV + ['revenue_usd_m']].dropna()
    if len(sub_te) > 0:
        test_mae = mean_absolute_error(sub_te['revenue_usd_m'], pipe_nf.predict(sub_te[FEATS_NF_REV]))
        print(f"Netflix 2025 held-out test MAE: ${test_mae:.1f}M  (n={len(sub_te)})")
    else:
        print("Netflix 2025 test: not enough complete-feature rows for evaluation")


def predict(fb, nf):
    pipe_comp   = joblib.load(os.path.join(PROJECT, 'models/fivebelow_comp_model.joblib'))
    pipe_margin = joblib.load(os.path.join(PROJECT, 'models/fivebelow_margin_model.joblib'))
    pipe_nf     = joblib.load(os.path.join(PROJECT, 'models/netflix_revenue_model.joblib'))

    fb_s = fb.sort_values('fiscal_year').reset_index(drop=True)
    sub_comp = fb_s[FEATS_COMP + ['fiscal_year', 'comp_sales_pct']].dropna()
    sub_comp = sub_comp.copy()
    sub_comp['comp_pred'] = pipe_comp.predict(sub_comp[FEATS_COMP])

    sub_margin = fb_s[FEATS_MARGIN + ['fiscal_year', 'op_margin_pct']].dropna()
    sub_margin = sub_margin.copy()
    sub_margin['margin_pred'] = pipe_margin.predict(sub_margin[FEATS_MARGIN])

    nf_s = nf.sort_values('end_date').reset_index(drop=True)
    sub_nf = nf_s[FEATS_NF_REV + ['quarter', 'revenue_usd_m']].dropna()
    sub_nf = sub_nf.copy()
    sub_nf['rev_pred'] = pipe_nf.predict(sub_nf[FEATS_NF_REV])

    print("Five Below comp_sales predictions:")
    print(sub_comp[['fiscal_year', 'comp_sales_pct', 'comp_pred']].to_string(index=False))
    print("\nFive Below margin predictions:")
    print(sub_margin[['fiscal_year', 'op_margin_pct', 'margin_pred']].to_string(index=False))
    print("\nNetflix revenue predictions:")
    print(sub_nf[['quarter', 'revenue_usd_m', 'rev_pred']].to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--train',    action='store_true')
    parser.add_argument('--evaluate', action='store_true')
    parser.add_argument('--predict',  action='store_true')
    args = parser.parse_args()

    fb, nf = load_data()
    if args.train:
        train(fb, nf)
    if args.evaluate:
        evaluate(fb, nf)
    if args.predict:
        predict(fb, nf)
    if not any([args.train, args.evaluate, args.predict]):
        print("Use --train, --evaluate, or --predict")
