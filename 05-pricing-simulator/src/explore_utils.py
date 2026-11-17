"""Shared utility functions for 05-pricing-simulator exploration notebook."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats


CHART_DIR = None  # set by notebook after import


def set_chart_dir(path):
    global CHART_DIR
    CHART_DIR = path


def save_fig(fig, filename, dpi=200):
    """Save figure to chart dir and return path."""
    if CHART_DIR is None:
        raise ValueError("Call set_chart_dir() first.")
    p = f"{CHART_DIR}/{filename}"
    fig.savefig(p, dpi=dpi, bbox_inches="tight")
    return p


def promo_flags(df):
    """Return a string promo-type label for each row."""
    conds = [
        df["FEATURE"].eq(1) & df["DISPLAY"].eq(1),
        df["FEATURE"].eq(1),
        df["DISPLAY"].eq(1),
        df["TPR_ONLY"].eq(1),
    ]
    choices = ["Feature+Display", "Feature Only", "Display Only", "TPR Only"]
    return np.select(conds, choices, default="None")


def discount_pct(df):
    """Percent discount = (BASE_PRICE - PRICE) / BASE_PRICE * 100."""
    return (df["BASE_PRICE"] - df["PRICE"]) / df["BASE_PRICE"].replace(0, np.nan) * 100


def winsorise(series, lower=0.01, upper=0.99):
    """Clip series at given quantile bounds."""
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lo, hi)


def effect_size_label(d):
    """Cohen's d label: small <0.2, medium <0.5, large >=0.8."""
    d = abs(d)
    if d < 0.2:
        return "small"
    elif d < 0.5:
        return "small-medium"
    elif d < 0.8:
        return "medium-large"
    else:
        return "large"


def cramers_v(contingency):
    """Cramer's V from a 2-D contingency array."""
    chi2 = stats.chi2_contingency(contingency, correction=False)[0]
    n = contingency.sum()
    k = min(contingency.shape) - 1
    return np.sqrt(chi2 / (n * k)) if k > 0 else 0.0


def mannwhitney_summary(a, b, label_a="A", label_b="B"):
    """Return dict with U, p, rank-biserial r, 95% CI (bootstrap)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    a = a[~np.isnan(a)]
    b = b[~np.isnan(b)]
    u, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    n1, n2 = len(a), len(b)
    r = 1 - 2 * u / (n1 * n2)          # rank-biserial correlation
    # bootstrap CI on r (1000 resamples, capped to avoid huge runtime)
    rng = np.random.default_rng(42)
    n_boot = 500
    boot_r = []
    for _ in range(n_boot):
        sa = rng.choice(a, size=min(n1, 500), replace=True)
        sb = rng.choice(b, size=min(n2, 500), replace=True)
        u_b, _ = stats.mannwhitneyu(sa, sb, alternative="two-sided")
        boot_r.append(1 - 2 * u_b / (len(sa) * len(sb)))
    ci_lo, ci_hi = np.percentile(boot_r, [2.5, 97.5])
    return {
        "label_a": label_a,
        "label_b": label_b,
        "n_a": n1,
        "n_b": n2,
        "median_a": np.median(a),
        "median_b": np.median(b),
        "u_stat": u,
        "p_value": p,
        "rank_biserial_r": round(r, 3),
        "ci_95_lo": round(ci_lo, 3),
        "ci_95_hi": round(ci_hi, 3),
    }
