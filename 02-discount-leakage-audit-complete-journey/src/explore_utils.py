"""
explore_utils.py – shared helpers for 01_exploration.ipynb.
No predictive modelling; only pandas / matplotlib / scipy.
"""
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from pathlib import Path
from scipy import stats

CHART_DIR = None
TWO_COLORS = ["#2166ac", "#d6604d"]
GREY = "#aaaaaa"


def save_chart(fig, filename):
    path = Path(CHART_DIR) / filename
    fig.savefig(path, dpi=200, bbox_inches="tight")
    plt.show()   # render inline in Jupyter before closing
    plt.close(fig)
    return str(path)


def hbar(values, labels, title, xlabel, filename=None, annot=None):
    fig, ax = plt.subplots(figsize=(8, max(3, 0.45 * len(values))))
    ax.barh(labels, values, color=TWO_COLORS[0], edgecolor="white")
    if annot is not None:
        for i, (v, a) in enumerate(zip(values, annot)):
            ax.text(v * 1.01, i, str(a), va="center", fontsize=8)
    ax.set_xlabel(xlabel)
    ax.set_title(title, fontweight="bold", pad=10)
    fig.tight_layout()
    if filename:
        save_chart(fig, filename)
    return fig


def hist_series(series, title, xlabel, filename=None, bins=40, log_y=False):
    fig, ax = plt.subplots(figsize=(7, 4))
    data = series.dropna()
    ax.hist(data, bins=bins, color=TWO_COLORS[0], edgecolor="white", alpha=0.85)
    med = data.median()
    ax.axvline(med, color=TWO_COLORS[1], linewidth=1.8, label=f"Median {med:.2f}")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    ax.set_title(title, fontweight="bold", pad=10)
    if log_y:
        ax.set_yscale("log")
    ax.legend()
    fig.tight_layout()
    if filename:
        save_chart(fig, filename)
    return fig


def waterfall_chart(labels, amounts, title, filename=None):
    """
    amounts: list of dollar values.
    First entry is the gross bar (blue, starts at 0).
    Middle entries: negative = deduction (red), positive = addition (blue).
    Last entry is the net/pocket bar (blue, starts at 0).

    Annotations:
    - Blue bars: label at top shows the value reached.
    - Red (deduction) bars: two labels — the deduction amount inside the bar,
      and the running total at the bottom of the bar.
    """
    running = amounts[0]
    xs = list(range(len(amounts)))
    bottoms, heights, colors = [], [], []

    # First bar: gross revenue
    bottoms.append(0)
    heights.append(amounts[0])
    colors.append(TWO_COLORS[0])

    for v in amounts[1:-1]:
        if v < 0:
            new_running = running + v
            bottoms.append(new_running)
            heights.append(-v)       # positive height (bar goes upward from bottom)
            colors.append(TWO_COLORS[1])
        else:
            bottoms.append(running)
            heights.append(v)
            colors.append(TWO_COLORS[0])
        running += v

    # Last bar: pocket revenue
    bottoms.append(0)
    heights.append(running)
    colors.append(TWO_COLORS[0])

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(xs, heights, bottom=bottoms, color=colors, edgecolor="white", width=0.55)

    top_val = amounts[0]  # maximum for padding annotations
    for xi, (b, h, v) in enumerate(zip(bottoms, heights, amounts)):
        if xi == 0 or xi == len(amounts) - 1:
            # Gross and pocket: label at top showing total
            ax.text(xi, b + h + top_val * 0.015, f"${b+h:,.0f}",
                    ha="center", fontsize=8, fontweight="bold")
        else:
            # Deduction bar: label the deduction amount inside the bar
            # and the running total (bottom of bar) below
            deduct = -v if v < 0 else v
            ax.text(xi, b + h / 2, f"-${deduct:,.0f}",
                    ha="center", va="center", fontsize=8, color="white", fontweight="bold")
            ax.text(xi, b - top_val * 0.03, f"${b:,.0f}",
                    ha="center", fontsize=7.5)

    ax.set_xticks(xs)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.set_ylabel("Revenue ($)")
    ax.set_title(title, fontweight="bold", pad=10)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    fig.tight_layout()
    if filename:
        save_chart(fig, filename)
    return fig


def mannwhitney_report(a, b, label_a, label_b, unit="$"):
    a = np.array(a.dropna() if hasattr(a, "dropna") else a)
    b = np.array(b.dropna() if hasattr(b, "dropna") else b)
    stat, p = stats.mannwhitneyu(a, b, alternative="two-sided")
    n1, n2 = len(a), len(b)
    r = 1 - 2 * stat / (n1 * n2)
    rng = np.random.default_rng(42)
    diffs = [
        np.median(rng.choice(a, n1, replace=True)) - np.median(rng.choice(b, n2, replace=True))
        for _ in range(2000)
    ]
    ci_lo, ci_hi = np.percentile(diffs, [2.5, 97.5])
    return dict(
        label_a=label_a, label_b=label_b, n_a=n1, n_b=n2,
        median_a=float(np.median(a)), median_b=float(np.median(b)),
        median_diff=float(np.median(a) - np.median(b)),
        ci_lo=ci_lo, ci_hi=ci_hi, U=stat, p=p, r=r, unit=unit,
        reliable="Yes" if p < 0.05 else "No"
    )


def chisq_report(ct):
    chi2, p, dof, _ = stats.chi2_contingency(ct)
    n = ct.values.sum()
    v = np.sqrt(chi2 / (n * (min(ct.shape) - 1)))
    return dict(chi2=chi2, p=p, dof=dof, n=n, cramers_v=v,
                reliable="Yes" if p < 0.05 else "No")
