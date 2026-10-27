"""Feature definitions shared by notebook 02, notebook 03 and src/pipeline.py.

Every engineered feature is one registry entry. The code expression in `expr`
is the exact string that is evaluated, so the notebook text and the code cannot drift.
"""
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

SEED = 42
TARGET = "churn_flag"
ID_COL = "customerID"

RAW_CAT = ["gender", "Partner", "Dependents", "PhoneService", "MultipleLines", "InternetService",
           "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
           "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod"]
RAW_NUM = ["SeniorCitizen", "tenure", "MonthlyCharges"]
RAW_COLS = RAW_CAT + RAW_NUM
ADDON_COLS = ["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies"]
SERVICE_COLS = ["PhoneService", "MultipleLines", "InternetService"] + ADDON_COLS

# Columns the explorer said to leave out of the model (leakage or redundancy).
EXCLUDED = ["customerID", "Churn", "tenure_band", "monthly_charge_band", "TotalCharges",
            "avg_monthly_spend", "price_vs_history_pct", "has_internet", "n_addons", "n_protection_addons"]

_I = "(df['InternetService'] != 'No')"
REGISTRY = [
    dict(name="contract_ord", kind="numeric (0/1/2)",
         meaning="Contract length as an ordered number: 0 month-to-month, 1 one year, 2 two years.",
         formula=r"\text{contract\_ord}=\begin{cases}0&\text{month-to-month}\\1&\text{one year}\\2&\text{two year}\end{cases}",
         expr="df['Contract'].map({'Month-to-month': 0, 'One year': 1, 'Two year': 2})",
         inputs=["Contract"], primary="Contract",
         finding="H1 / finding 1: churn is 42.7%, 11.3%, 2.8% by contract. The order is monotone, so one ordered number lets a linear model use the order with one coefficient.",
         direction="negative (longer contract, less churn)"),
    dict(name="m2m_fiber", kind="binary",
         meaning="Month-to-month contract and fiber-optic internet together.",
         formula=r"\text{m2m\_fiber}=\mathbb{1}[\text{Contract}=\text{Month-to-month}]\cdot\mathbb{1}[\text{InternetService}=\text{Fiber optic}]",
         expr="((df['Contract'] == 'Month-to-month') & (df['InternetService'] == 'Fiber optic'))",
         inputs=["Contract", "InternetService"], primary="Contract",
         finding="H2, H9 / finding 3: fiber on month-to-month leaves at 55% against 32% for DSL. A linear model adds effects; this flag lets it see the joint group.",
         direction="positive"),
    dict(name="m2m_echeck", kind="binary",
         meaning="Month-to-month contract and electronic-check payment together.",
         formula=r"\text{m2m\_echeck}=\mathbb{1}[\text{Contract}=\text{Month-to-month}]\cdot\mathbb{1}[\text{PaymentMethod}=\text{Electronic check}]",
         expr="((df['Contract'] == 'Month-to-month') & (df['PaymentMethod'] == 'Electronic check'))",
         inputs=["Contract", "PaymentMethod"], primary="PaymentMethod",
         finding="H4 / finding 4: electronic-check payers on month-to-month leave at 54%, against about 33% for automatic payers on the same contract.",
         direction="positive"),
    dict(name="m2m_first_year", kind="binary",
         meaning="Month-to-month contract and 12 months or less with the company.",
         formula=r"\text{m2m\_first\_year}=\mathbb{1}[\text{Contract}=\text{Month-to-month}]\cdot\mathbb{1}[\text{tenure}\le 12]",
         expr="((df['Contract'] == 'Month-to-month') & (df['tenure'] <= 12))",
         inputs=["Contract", "tenure"], primary="Contract",
         finding="H1, H3 / finding 5: month-to-month customers in year one are 28% of the base and hold 55% of leavers.",
         direction="positive"),
    dict(name="first_year", kind="binary",
         meaning="Customer is in the first 12 months.",
         formula=r"\text{first\_year}=\mathbb{1}[\text{tenure}\le 12]",
         expr="(df['tenure'] <= 12)",
         inputs=["tenure"], primary="tenure",
         finding="H3 / finding 2: 47.4% churn in months 0-12 against 17.1% after. A step is easier for a linear model than a curve.",
         direction="positive"),
    dict(name="log_tenure", kind="numeric",
         meaning="Log of tenure, so early months count more than late months.",
         formula=r"\text{log\_tenure}=\ln(1+\text{tenure})",
         expr="np.log1p(df['tenure'])",
         inputs=["tenure"], primary="tenure",
         finding="Finding 2 / chart 04: churn falls fast in the first months and flattens after. A log curve matches that shape.",
         direction="negative"),
    dict(name="internet_no_techsupport", kind="binary",
         meaning="Has internet but no tech-support add-on.",
         formula=r"\text{internet\_no\_techsupport}=\mathbb{1}[\text{InternetService}\ne\text{No}]\cdot\mathbb{1}[\text{TechSupport}=\text{No}]",
         expr=f"({_I} & (df['TechSupport'] == 'No'))",
         inputs=["InternetService", "TechSupport"], primary="TechSupport",
         finding="H5 / finding 'also notable': internet customers without tech support leave at 42% against 15% with it. Customers with no internet are 'No' on tech support but leave rarely (7%), so the flag keeps them apart.",
         direction="positive"),
    dict(name="internet_no_protection", kind="binary",
         meaning="Has internet and none of the four protection add-ons (security, backup, device protection, tech support).",
         formula=r"\text{internet\_no\_protection}=\mathbb{1}[\text{InternetService}\ne\text{No}]\cdot\mathbb{1}\Big[\sum_{k\in P}\mathbb{1}[k=\text{Yes}]=0\Big]",
         expr=f"({_I} & ((df[['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport']] == 'Yes').sum(axis=1) == 0))",
         inputs=["InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport"], primary="OnlineSecurity",
         finding="Chart 08: internet customers with four protection add-ons leave at 5%, with none at 57%.",
         direction="positive"),
    dict(name="n_protection", kind="count (0-4)",
         meaning="How many of the four protection add-ons the customer has.",
         formula=r"\text{n\_protection}=\sum_{k\in P}\mathbb{1}[k=\text{Yes}],\ P=\{\text{security, backup, device, tech support}\}",
         expr="(df[['OnlineSecurity','OnlineBackup','DeviceProtection','TechSupport']] == 'Yes').sum(axis=1)",
         inputs=["OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport"], primary="OnlineSecurity",
         finding="Chart 08: churn falls steadily as protection add-ons rise. It matches the explorer's `n_protection_addons`; it is rebuilt here from the raw columns so the pipeline needs no extra column.",
         direction="negative"),
    dict(name="n_streaming", kind="count (0-2)",
         meaning="How many streaming add-ons (TV, movies) the customer has.",
         formula=r"\text{n\_streaming}=\mathbb{1}[\text{StreamingTV}=\text{Yes}]+\mathbb{1}[\text{StreamingMovies}=\text{Yes}]",
         expr="(df[['StreamingTV','StreamingMovies']] == 'Yes').sum(axis=1)",
         inputs=["StreamingTV", "StreamingMovies"], primary="StreamingTV",
         finding="Chart 08: streaming add-ons show a small gap (about 4 points), unlike protection add-ons. Tested here to see whether it adds anything beyond protection.",
         direction="weak positive"),
    dict(name="household_size", kind="count (0-2)",
         meaning="Partner and dependents counted together: a proxy for household ties.",
         formula=r"\text{household\_size}=\mathbb{1}[\text{Partner}=\text{Yes}]+\mathbb{1}[\text{Dependents}=\text{Yes}]",
         expr="((df['Partner'] == 'Yes').astype(int) + (df['Dependents'] == 'Yes').astype(int))",
         inputs=["Partner", "Dependents"], primary="Partner",
         finding="Ranked drivers: Dependents (V 0.16) and Partner (V 0.15) both link to lower churn. One count pools two weak signals.",
         direction="negative"),
]
# price_resid is different: it must be fitted, so it lives in the pipeline (ServiceAdjustedPrice below).
PRICE_RESID = dict(
    name="price_resid", kind="numeric (fitted)",
    meaning="Monthly bill minus the bill the customer's service mix would normally cost. Positive means paying above the normal price for the same services.",
    formula=r"\text{price\_resid}=\text{MonthlyCharges}-\hat{b}_0-\sum_j \hat{b}_j\,x_j",
    expr="MonthlyCharges - LinearRegression().fit(service dummies, MonthlyCharges).predict(service dummies)  [fitted on training rows only]",
    inputs=["MonthlyCharges"] + SERVICE_COLS, primary="MonthlyCharges",
    finding="H6 / chart 07: leavers pay $15 more at the median, but price overlaps with fiber and add-ons. The residual isolates price from the service mix.",
    direction="positive")
ENGINEERED = [r["name"] for r in REGISTRY]


def add_features(df):
    """Return a copy of df with every row-wise engineered feature added. Nothing is fitted here."""
    out = df.copy()
    for r in REGISTRY:
        out[r["name"]] = eval(r["expr"], {"np": np, "df": out}).astype(float)
    return out


def split_data(df, seed=SEED, test_size=0.20):
    """Stratified 80/20 split on the target. Returns a Series 'train'/'test' indexed like df."""
    idx_tr, idx_te = train_test_split(df.index, test_size=test_size, stratify=df[TARGET], random_state=seed)
    s = pd.Series("train", index=df.index)
    s.loc[idx_te] = "test"
    return s


class ServiceAdjustedPrice(BaseEstimator, TransformerMixin):
    """Adds `price_resid`: bill minus the bill predicted from the service mix. Fitted on training rows only."""
    def _design(self, X):
        D = pd.get_dummies(X[SERVICE_COLS].astype(str), dtype=float)
        if hasattr(self, "cols_"):
            D = D.reindex(columns=self.cols_, fill_value=0.0)
        return D

    def fit(self, X, y=None):
        D = pd.get_dummies(X[SERVICE_COLS].astype(str), dtype=float)
        self.cols_ = list(D.columns)
        self.lr_ = LinearRegression().fit(D, X["MonthlyCharges"])
        return self

    def transform(self, X):
        X = X.copy()
        X["price_resid"] = X["MonthlyCharges"].values - self.lr_.predict(self._design(X))
        return X

    def get_feature_names_out(self, names=None):
        return None


def check_feature(x, y, min_group=100):
    """Training-split check of one feature against the target.
    Rule (fixed before looking): binary feature is KEEP if |churn-rate gap between 1 and 0| >= 5 points and both groups
    have >= 100 rows; any other feature is KEEP if |Spearman rho with the target| >= 0.10."""
    from scipy.stats import spearmanr
    x = pd.Series(np.asarray(x, float)); y = pd.Series(np.asarray(y))
    rho = spearmanr(x, y)[0]
    import math
    z, se = math.atanh(rho), 1 / math.sqrt(len(x) - 3)
    rho_ci = f"(approx. 95% interval {math.tanh(z-1.96*se):+.2f} to {math.tanh(z+1.96*se):+.2f})"
    if x.nunique() <= 6:
        g = pd.DataFrame({"value": x, "y": y}).groupby("value")["y"].agg(customers="count", churn_rate="mean").reset_index()
        label = g["value"].map(lambda v: f"{v:g}")
    else:
        b = pd.qcut(x, 10, duplicates="drop")
        g = pd.DataFrame({"bin": b, "y": y}).groupby("bin", observed=True)["y"].agg(customers="count", churn_rate="mean").reset_index()
        label = g["bin"].astype(str)
    g["label"] = label
    out = dict(table=g, rho=rho)
    if x.nunique() == 2:
        r1, r0 = y[x == 1].mean(), y[x == 0].mean(); n1, n0 = int((x == 1).sum()), int((x == 0).sum())
        out.update(stat=f"churn {100*r1:.1f}% when 1 (n={n1:,}) vs {100*r0:.1f}% when 0 (n={n0:,}); gap {100*(r1-r0):+.1f} points (approx. 95% interval {100*(r1-r0)-196*math.sqrt(r1*(1-r1)/n1+r0*(1-r0)/n0):+.1f} to {100*(r1-r0)+196*math.sqrt(r1*(1-r1)/n1+r0*(1-r0)/n0):+.1f}); Spearman rho {rho:+.2f} {rho_ci}",
                   keep=bool(abs(r1 - r0) >= 0.05 and min(n1, n0) >= min_group), rule="gap >= 5 points and both groups >= 100 rows")
    else:
        out.update(stat=f"Spearman rho with churn {rho:+.2f} {rho_ci}; churn rate from {100*g['churn_rate'].iloc[0]:.1f}% (lowest value/bin) to {100*g['churn_rate'].iloc[-1]:.1f}% (highest)",
                   keep=bool(abs(rho) >= 0.10), rule="|Spearman rho| >= 0.10")
    return out


def plot_feature_check(name, res, base_rate, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    g = res["table"]
    fig, ax = plt.subplots(figsize=(7, 3.6))
    ax.bar(g["label"], 100 * g["churn_rate"], color="#3b6ea5")
    for i, (r, n) in enumerate(zip(g["churn_rate"], g["customers"])):
        ax.text(i, 100 * r + 0.8, f"n={n:,}", ha="center", fontsize=7)
    ax.axhline(100 * base_rate, color="#c0392b", ls="--", lw=1, label=f"training base rate {100*base_rate:.1f}%")
    ax.set_ylabel("Churn rate (% of customers)"); ax.set_xlabel(name + " (value or decile bin)")
    ax.set_title(f"{name}: churn rate by value, training split"); ax.legend(fontsize=8)
    plt.xticks(rotation=30 if len(g) > 4 else 0, ha="right" if len(g) > 4 else "center", fontsize=8)
    plt.tight_layout(); fig.savefig(path, dpi=110); return fig
