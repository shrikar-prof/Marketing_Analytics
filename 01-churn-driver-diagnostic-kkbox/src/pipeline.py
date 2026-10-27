"""Production pipeline. Reuses src/features.py and src/model_utils.py so it cannot drift from the notebooks.

  python -I src/pipeline.py --train                      fit on the training split, save models/churn_driver_diagnostic_model.joblib
  python -I src/pipeline.py --evaluate                   score the held-out split with the saved model, write reports/modeling/tables/pipeline_evaluation.csv
  python -I src/pipeline.py --predict in.parquet out.csv score any table with the clean-table columns
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import joblib
import pandas as pd
import features as F
import model_utils as M

MODEL_PATH = os.path.join(M.MODEL_DIR, "churn_driver_diagnostic_model.joblib")
CONFIG_PATH = os.path.join(M.MODEL_DIR, "final_config.json")
CLEAN = os.path.join(M.PROJECT, "reports", "exploration", "clean.parquet")


def load_table():
    df = pd.read_parquet(CLEAN)
    df["split"] = F.split_data(df)
    return F.add_features(df)


def train():
    cfg = json.load(open(CONFIG_PATH)); df = load_table(); tr = df[df["split"] == "train"]
    pipe = M.make_pipeline(cfg["family"], cfg["params"], "eng", cfg["kept"], n_jobs=4).fit(tr, tr[F.TARGET])
    joblib.dump(pipe, MODEL_PATH); print("trained", cfg["family"], "on", len(tr), "rows ->", MODEL_PATH)


def evaluate():
    df = load_table(); te = df[df["split"] == "test"]; pipe = joblib.load(MODEL_PATH)
    p = pipe.predict_proba(te)[:, 1]
    out = M.bootstrap_metrics(te[F.TARGET].values, p, te["MonthlyCharges"].values)
    out.to_csv(os.path.join(M.REPORT_DIR, "tables", "pipeline_evaluation.csv")); print(out.round(4))


def predict(src, dst):
    X = pd.read_parquet(src) if src.endswith(".parquet") else pd.read_csv(src)
    pipe = joblib.load(MODEL_PATH); X = F.add_features(X)
    X["churn_risk"] = pipe.predict_proba(X)[:, 1]
    X["risk_decile"] = pd.qcut(X["churn_risk"].rank(method="first", ascending=False), 10, labels=range(1, 11)).astype(int)
    X[[c for c in [F.ID_COL, "churn_risk", "risk_decile"] if c in X.columns]].to_csv(dst, index=False); print("wrote", dst)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", action="store_true"); ap.add_argument("--evaluate", action="store_true")
    ap.add_argument("--predict", nargs=2, metavar=("INPUT", "OUTPUT"))
    a = ap.parse_args()
    if a.train: train()
    if a.evaluate: evaluate()
    if a.predict: predict(*a.predict)
