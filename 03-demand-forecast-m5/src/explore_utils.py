"""
explore_utils.py — shared helper functions for notebook 01_exploration.ipynb.
All functions are documented so the notebook can import and use them without
hiding logic from the reader.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from pathlib import Path
from scipy import stats

# ── Colour palette (two colours + grey, colour-blind friendly) ──────────────
C1 = "#2166ac"   # blue
C2 = "#d6604d"   # red-orange
CG = "#bdbdbd"   # grey

CHART_DPI = 200


def set_style():
    """Apply a clean, readable matplotlib style."""
    plt.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#e0e0e0",
        "grid.linewidth": 0.6,
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
    })


def save_chart(fig, path: Path, name: str) -> Path:
    """Save a figure as PNG at CHART_DPI and return the path."""
    path.mkdir(parents=True, exist_ok=True)
    fpath = path / name
    fig.savefig(fpath, dpi=CHART_DPI, bbox_inches="tight")
    plt.close(fig)
    return fpath


def pct(n, total):
    """Return 'n (x%)' string."""
    return f"{n:,} ({n / total:.1%} of {total:,})"


def zero_rate(series: pd.Series) -> float:
    """Fraction of values equal to zero."""
    return (series == 0).mean()


def mann_whitney_with_es(a: np.ndarray, b: np.ndarray):
    """
    Two-sample Mann-Whitney U test with rank-biserial correlation r.
    r = 2*U/(n1*n2) - 1; |r|<0.1 small, 0.1-0.3 medium, >0.3 large.
    Returns: stat, p_value, r, ci_lower, ci_upper (95% bootstrap CI on r).
    """
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    stat, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    n1, n2 = len(a), len(b)
    r = 2 * stat / (n1 * n2) - 1  # rank-biserial correlation

    # Bootstrap CI on r
    rng = np.random.default_rng(42)
    boot_r = []
    for _ in range(2000):
        sa = rng.choice(a, size=n1, replace=True)
        sb = rng.choice(b, size=n2, replace=True)
        u, _ = stats.mannwhitneyu(sa, sb, alternative="two-sided")
        boot_r.append(2 * u / (n1 * n2) - 1)
    ci = np.percentile(boot_r, [2.5, 97.5])
    return stat, p, r, ci[0], ci[1]


def chi2_with_cramersv(obs: np.ndarray):
    """
    Chi-square test of independence with Cramer's V.
    V = sqrt(chi2 / (n * (min(r,c)-1))); V<0.1 small, 0.1-0.3 medium, >0.3 large.
    Returns: chi2_stat, p_value, cramers_v.
    """
    chi2, p, _, _ = stats.chi2_contingency(obs)
    n = obs.sum()
    r, c = obs.shape
    v = np.sqrt(chi2 / (n * (min(r, c) - 1)))
    return chi2, p, v


def band_label(series: pd.Series, q=(0, 0.25, 0.5, 0.75, 1.0),
               labels=("Q1 (low)", "Q2", "Q3", "Q4 (high)")):
    """Assign quartile band labels to a numeric series."""
    cuts = series.quantile(q).values
    # Ensure unique edges
    cuts = np.unique(cuts)
    if len(cuts) < 2:
        return pd.Series(["single-value"] * len(series), index=series.index)
    return pd.cut(series, bins=cuts, labels=labels[:len(cuts) - 1],
                  include_lowest=True)


def lift(rate: float, baseline: float) -> str:
    """Express a rate relative to a baseline as '+X%' or '-X%' lift."""
    l = (rate - baseline) / baseline * 100
    sign = "+" if l >= 0 else ""
    return f"{sign}{l:.0f}%"


def format_effect(r, ci_lo, ci_hi):
    """Format rank-biserial r with 95% CI for plain-language reporting."""
    mag = "small" if abs(r) < 0.1 else ("medium" if abs(r) < 0.3 else "large")
    return (f"r = {r:.2f} (95% CI {ci_lo:.2f} to {ci_hi:.2f}); "
            f"effect size is {mag}")
