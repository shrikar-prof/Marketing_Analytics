# Data Science Consulting Portfolio

A collection of end-to-end consulting projects built on public datasets. Each project follows a structured consulting workflow: situation → question → approach → recommendation → measurable impact.

## Projects

| # | Project | Dataset | Status |
|---|---------|---------|--------|
| 01 | [Churn Driver Diagnostic](01-churn-driver-diagnostic-kkbox/) | KKBox (WSDM 2018) + IBM Telco | ✅ Complete |
| 02 | [Discount Leakage Audit](02-discount-leakage-audit-complete-journey/) | Dunnhumby Complete Journey | 🔜 Planned |
| 03 | [Demand Forecast](03-demand-forecast-m5/) | M5 (Walmart) | 🔜 Planned |
| 04 | [Marketing Budget Reallocation (MMM)](04-marketing-budget-reallocation-mmm/) | Google Meridian demo | 🔜 Planned |
| 05 | [Pricing Simulator](05-pricing-simulator/) | Dunnhumby Breakfast at the Frat | 🔜 Planned |
| 06 | [Strategy Teardowns](06-strategy-teardowns/) | SEC EDGAR + public filings | 🔜 Planned |

## What each project contains

- `problem_description.md` — business question, data tables, download instructions
- `notebooks/` — executed Jupyter notebooks with plain-language explanations at every step
  - `01_exploration.ipynb` — data dictionary, EDA, hypothesis testing
  - `02_feature_engineering.ipynb` — feature construction with formulas and rationale
  - `03_modeling.ipynb` — model comparison, Optuna tuning, evaluation, SHAP
- `src/` — shared Python modules (features, model utils, pipeline)
- `reports/` — plain-language findings, model card, strategy memo, interactive HTML report
- `models/` — trained pipeline artefact (`.joblib`) — *not tracked in git*

## Getting started

```bash
# Clone the repo
git clone <repo-url>
cd marketing-analytics

# Install dependencies (Python 3.13, conda recommended)
conda create -n portfolio python=3.13
conda activate portfolio
pip install pandas numpy scipy scikit-learn lightgbm xgboost catboost optuna shap statsmodels lifelines matplotlib seaborn nbformat nbconvert

# Download raw data for a project (instructions in each problem_description.md)
# Then run the notebooks in order: 01 → 02 → 03
```

## Methodology

Every analytical step in the notebooks follows a four-part explanation standard:
1. **Why this method** — what the step decides and why this method fits
2. **Alternatives considered** — at least two other approaches and why they weren't used
3. **How it works** — plain-language idea plus the formula with every symbol named
4. **How to read the output** — what to look at and what would change the decision

## Project 01 highlights — Churn Driver Diagnostic (KKBox + Telco)

- **Finding:** 916 month-to-month fiber customers in their first year (13% of base) churn at 70% and hold 38% of $139k/month in lost revenue.
- **Model:** Logistic regression (elastic-net GLM), held-out AUC 0.847. Top 20% by risk score captures 54% of lost revenue.
- **Strongest lever:** One-year contract reduces predicted churn by 18 points. Randomised save-offer pilots recommended before scaling.

## Author

Shrikar — data scientist and independent consultant.
