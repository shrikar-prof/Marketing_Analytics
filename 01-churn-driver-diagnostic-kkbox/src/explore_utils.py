"""Helpers for notebooks/01_exploration.ipynb. Plain functions, no hidden state."""
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
import matplotlib.pyplot as plt

BLUE, ORANGE, GREY = "#1f5fa8", "#d95f02", "#9a9a9a"
SEED = 42


def style():
    plt.rcParams.update({"figure.dpi": 100, "savefig.dpi": 200, "axes.spines.top": False,
                         "axes.spines.right": False, "axes.titlesize": 13, "axes.titleweight": "bold",
                         "axes.labelsize": 11, "font.size": 10, "text.parse_math": False})


def save(fig, path):
    fig.savefig(path, dpi=200, bbox_inches="tight", facecolor="white")


def rate_table(df, col, target="churn_flag", money="MonthlyCharges", order=None):
    """Churn rate, counts, share of base, share of all churners, lift, monthly money lost per group."""
    base_rate = df[target].mean()
    g = df.groupby(col, observed=True).agg(customers=(target, "size"), churned=(target, "sum"),
                                           monthly_rev=(money, "sum"))
    g["churn_rate_pct"] = 100 * g["churned"] / g["customers"]
    g["share_of_base_pct"] = 100 * g["customers"] / len(df)
    g["share_of_churners_pct"] = 100 * g["churned"] / df[target].sum()
    g["lift_vs_avg"] = g["churn_rate_pct"] / (100 * base_rate)
    lost = df[df[target] == 1].groupby(col, observed=True)[money].sum()
    g["monthly_rev_lost_usd"] = lost.reindex(g.index).fillna(0)
    g = g.drop(columns="monthly_rev")
    if order is not None:
        g = g.reindex(order)
    return g.round(2)


def cramers_v(x, y):
    ct = pd.crosstab(x, y)
    chi2, p, dof, _ = stats.chi2_contingency(ct, correction=False)
    n = ct.values.sum()
    return float(np.sqrt(chi2 / (n * (min(ct.shape) - 1)))), chi2, p, dof


def two_group_rate_test(a, b, n_boot=2000, seed=SEED):
    """a, b: 0/1 arrays. Returns rates, difference in percentage points, 95% CI (bootstrap), chi-square p."""
    a, b = np.asarray(a), np.asarray(b)
    rng = np.random.default_rng(seed)
    ra, rb = a.mean(), b.mean()
    diffs = [rng.choice(a, len(a)).mean() - rng.choice(b, len(b)).mean() for _ in range(n_boot)]
    lo, hi = np.percentile(diffs, [2.5, 97.5])
    ct = np.array([[a.sum(), len(a) - a.sum()], [b.sum(), len(b) - b.sum()]])
    chi2, p, _, _ = stats.chi2_contingency(ct, correction=False)
    n = ct.sum()
    phi = float(np.sqrt(chi2 / n))
    return dict(rate_a=100 * ra, rate_b=100 * rb, diff_pp=100 * (ra - rb), ci_lo=100 * lo, ci_hi=100 * hi,
                p=p, phi=phi, n_a=len(a), n_b=len(b))


def mann_whitney(x, y, n_boot=2000, seed=SEED):
    """x, y numeric. Effect = probability a random x exceeds a random y (0.5 = no difference)."""
    x, y = np.asarray(x, float), np.asarray(y, float)
    u, p = stats.mannwhitneyu(x, y, alternative="two-sided")
    cles = u / (len(x) * len(y))
    rng = np.random.default_rng(seed)
    d = [np.median(rng.choice(x, len(x))) - np.median(rng.choice(y, len(y))) for _ in range(n_boot)]
    lo, hi = np.percentile(d, [2.5, 97.5])
    return dict(median_x=np.median(x), median_y=np.median(y), diff=np.median(x) - np.median(y),
                ci_lo=lo, ci_hi=hi, p=p, cles=cles, n_x=len(x), n_y=len(y))


def fmt_p(p):
    return "below 0.0001" if p < 1e-4 else f"{p:.4f}"


def md_table(df, index=True, floatfmt="{:,.2f}"):
    d = df.reset_index() if index else df.copy()
    cols = [str(c) for c in d.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in d.iterrows():
        cells = []
        for v in r.values:
            if isinstance(v, (float, np.floating)):
                cells.append("" if np.isnan(v) else floatfmt.format(v))
            elif isinstance(v, (int, np.integer)):
                cells.append(f"{v:,}")
            else:
                cells.append(str(v).replace("|", "/"))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)
