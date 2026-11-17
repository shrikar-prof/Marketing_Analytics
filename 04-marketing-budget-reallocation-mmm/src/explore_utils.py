"""
explore_utils.py — shared helpers for 01_exploration.ipynb
All functions are deterministic (no random state).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from scipy import stats


# ── colour palette ───────────────────────────────────────────────
PRIMARY   = "#2166ac"   # blue
SECONDARY = "#d6604d"   # red-orange
GREY      = "#bdbdbd"

CHANNEL_COLORS = {
    "tv_S":        "#2166ac",
    "ooh_S":       "#4dac26",
    "print_S":     "#d01c8b",
    "facebook_S":  "#f4a582",
    "search_S":    "#b2182b",
}


def style_fig(ax, title, xlabel, ylabel):
    """Apply consistent styling to a matplotlib Axes."""
    ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.tick_params(labelsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    return ax


def save_chart(fig, path):
    """Save figure at 200 dpi and close it."""
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def missing_summary(df):
    """Return a tidy missing-value summary DataFrame."""
    n = len(df)
    s = df.isnull().sum()
    pct = (s / n * 100).round(2)
    return pd.DataFrame({"missing_count": s, "missing_pct": pct}
                       ).sort_values("missing_count", ascending=False)


def band_cut(series, n=5, label_fmt="{:.0f}"):
    """Cut a numeric series into n quantile bands with descriptive labels."""
    quantiles = np.linspace(0, 1, n + 1)
    bins = series.quantile(quantiles).unique()
    labels = []
    for i in range(len(bins) - 1):
        labels.append(f"Q{i+1} ({label_fmt.format(bins[i])}–{label_fmt.format(bins[i+1])})")
    return pd.cut(series, bins=bins, labels=labels, include_lowest=True)


def effect_size_r(u_stat, n1, n2):
    """Rank-biserial r from Mann-Whitney U, range [-1, 1]."""
    return 1 - (2 * u_stat) / (n1 * n2)


def cramers_v(contingency_table):
    """Cramér's V from a contingency table (pandas DataFrame or 2-D array)."""
    chi2 = stats.chi2_contingency(contingency_table, correction=False)[0]
    n = contingency_table.values.sum()
    k = min(contingency_table.shape) - 1
    return np.sqrt(chi2 / (n * k)) if k > 0 else 0.0


def revenue_lift(df, group_col, revenue_col="revenue"):
    """Return lift (group mean / overall mean) for each group."""
    overall = df[revenue_col].mean()
    return df.groupby(group_col)[revenue_col].mean() / overall
