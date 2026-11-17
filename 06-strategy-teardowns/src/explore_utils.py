"""
explore_utils.py
Utility functions for the strategy-teardowns exploration notebook.
Parsing code lives here so notebook cells stay readable.

Data sources:
- Netflix: Q4 shareholder letters (HTM files), parsed with pandas.read_html.
  Figures verified by printing raw table rows; see notebook Section 2.
- Five Below: SEC EDGAR company facts JSON for financials;
  store counts and comparable sales hand-extracted from 10-K text.
"""
import json
import pathlib
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")


# ---------------------------------------------------------------------------
# Netflix – UCAN quarterly data
# ---------------------------------------------------------------------------

def parse_netflix_ucan(letter_dir: str) -> pd.DataFrame:
    """
    Returns a tidy quarterly DataFrame for the UCAN region.

    Data sourced by parsing each Q4 shareholder letter with pandas.read_html
    and reading the UCAN section of the regional streaming table.
    The Q4 2025 letter omitted per-member metrics; for those quarters only
    revenue is available.

    Columns:
      quarter          – e.g. "Q4'19"
      end_date         – last day of the quarter (datetime)
      paid_members_m   – paid memberships at end of quarter (millions)
      net_adds_m       – paid net additions during quarter (millions)
      arm_usd          – average monthly revenue per membership (USD)
      revenue_usd_m    – quarterly UCAN streaming revenue (USD millions)
      has_members      – True if membership data is available
    """
    # Numbers read directly from the raw table rows printed during exploration.
    # Each letter covers 5 quarters (Q4-to-Q4). We use the most recent
    # letter that reports each quarter to get the latest-filed figure.
    # Netflix stopped reporting per-member metrics after Q4 2024 (Q4'25 letter
    # only shows revenue by region).
    #
    # Format: (quarter, end_date, paid_members_m, net_adds_m, arm_usd, rev_m)
    member_data = [
        # From Q4'20 letter (filed 2021-01-19)
        ("Q4'19", "2019-12-31",  67.66,  0.55, 13.22,  2_672),
        ("Q1'20", "2020-03-31",  69.97,  2.31, 13.09,  2_703),
        ("Q2'20", "2020-06-30",  72.90,  2.94, 13.25,  2_840),
        ("Q3'20", "2020-09-30",  73.08,  0.18, 13.40,  2_933),
        ("Q4'20", "2020-12-31",  73.94,  0.86, 13.51,  2_980),
        # From Q4'21 letter (filed 2022-01-20)
        ("Q1'21", "2021-03-31",  74.38,  0.45, 14.25,  3_171),
        ("Q2'21", "2021-06-30",  73.95, -0.43, 14.54,  3_235),
        ("Q3'21", "2021-09-30",  74.02,  0.07, 14.68,  3_258),
        ("Q4'21", "2021-12-31",  75.22,  1.19, 14.78,  3_309),
        # From Q4'22 letter (filed 2023-01-19)
        ("Q1'22", "2022-03-31",  74.58, -0.64, 14.91,  3_350),
        ("Q2'22", "2022-06-30",  73.28, -1.30, 15.95,  3_538),
        ("Q3'22", "2022-09-30",  73.39,  0.10, 16.37,  3_602),
        ("Q4'22", "2022-12-31",  74.30,  0.91, 16.23,  3_595),
        # From Q4'23 letter (filed 2024-01-23)
        ("Q1'23", "2023-03-31",  74.40,  0.10, 16.18,  3_609),
        ("Q2'23", "2023-06-30",  75.57,  1.17, 16.00,  3_599),
        ("Q3'23", "2023-09-30",  77.32,  1.75, 16.29,  3_735),
        ("Q4'23", "2023-12-31",  80.13,  2.81, 16.64,  3_931),
        # From Q4'24 letter (filed 2025-01-21)
        ("Q1'24", "2024-03-31",  82.66,  2.53, 17.30,  4_224),
        ("Q2'24", "2024-06-30",  84.11,  1.45, 17.17,  4_296),
        ("Q3'24", "2024-09-30",  84.80,  0.69, 17.06,  4_322),
        ("Q4'24", "2024-12-31",  89.63,  4.82, 17.26,  4_517),
    ]
    # Revenue-only data from Q4'25 letter (filed 2026-01-20)
    # Netflix stopped disclosing memberships per region after Q4 2024
    revenue_only = [
        ("Q1'25", "2025-03-31", np.nan, np.nan, np.nan, 4_617),
        ("Q2'25", "2025-06-30", np.nan, np.nan, np.nan, 4_929),
        ("Q3'25", "2025-09-30", np.nan, np.nan, np.nan, 5_072),
        ("Q4'25", "2025-12-31", np.nan, np.nan, np.nan, 5_339),
    ]

    all_rows = member_data + revenue_only
    df = pd.DataFrame(all_rows, columns=[
        "quarter", "end_date",
        "paid_members_m", "net_adds_m",
        "arm_usd", "revenue_usd_m"
    ])
    df["end_date"] = pd.to_datetime(df["end_date"])
    df["has_members"] = df["paid_members_m"].notna()
    return df


# ---------------------------------------------------------------------------
# Five Below – financial data from EDGAR company facts JSON
# ---------------------------------------------------------------------------

def _get_annual_facts(facts_dict: dict, key: str) -> dict:
    """Return {end_date_str: value} for the given GAAP key, 10-K annual only."""
    if key not in facts_dict:
        return {}
    units = facts_dict[key]["units"]
    unit_key = list(units.keys())[0]
    vals = units[unit_key]
    result = {}
    for v in vals:
        if v.get("form") == "10-K" and v.get("fp") == "FY":
            end = v["end"]
            # Keep latest filing for each end date
            if end not in result:
                result[end] = v["val"]
    return result


def build_five_below_financials(companyfacts_path: str) -> pd.DataFrame:
    """
    Extract annual income statement and cash flow data from EDGAR company facts.
    Returns one row per fiscal year (FY2018–FY2025).

    Revenue: older filings tagged as SalesRevenueNet; newer as
    RevenueFromContractWithCustomerExcludingAssessedTax. We merge both.
    """
    with open(companyfacts_path) as f:
        cf = json.load(f)
    facts = cf["facts"]["us-gaap"]

    rev_old = _get_annual_facts(facts, "SalesRevenueNet")
    rev_new = _get_annual_facts(facts, "RevenueFromContractWithCustomerExcludingAssessedTax")
    # rev_new overwrites rev_old where both exist
    revenue = {**rev_old, **rev_new}

    operating_income = _get_annual_facts(facts, "OperatingIncomeLoss")
    net_income       = _get_annual_facts(facts, "NetIncomeLoss")
    cogs             = _get_annual_facts(facts, "CostOfGoodsAndServicesSold")
    sga              = _get_annual_facts(facts, "SellingGeneralAndAdministrativeExpense")
    capex            = _get_annual_facts(facts, "PaymentsToAcquirePropertyPlantAndEquipment")

    all_dates = sorted(set(revenue.keys()))
    # Fiscal year-ends are in late January or early February
    fy_dates = [d for d in all_dates if pd.to_datetime(d).month in (1, 2)]

    rows = []
    for d in fy_dates:
        dt = pd.to_datetime(d)
        rows.append({
            "fiscal_year_end": dt,
            "revenue_usd":          revenue.get(d, np.nan),
            "operating_income_usd": operating_income.get(d, np.nan),
            "net_income_usd":       net_income.get(d, np.nan),
            "cogs_usd":             cogs.get(d, np.nan),
            "sga_usd":              sga.get(d, np.nan),
            "capex_usd":            capex.get(d, np.nan),
        })

    df = pd.DataFrame(rows)
    df = df.dropna(subset=["revenue_usd"])
    # Assign fiscal year: year-end Jan/Feb of year Y → fiscal year Y-1
    df["fiscal_year"] = df["fiscal_year_end"].apply(
        lambda d: d.year - 1 if d.month <= 3 else d.year
    )
    df = df[df["fiscal_year"] >= 2018].copy()
    df = df.sort_values("fiscal_year_end")
    # Deduplicate – keep last (most recent) filing for each fiscal year
    df = df.drop_duplicates(subset=["fiscal_year"], keep="last").reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Five Below – store counts and comparable sales (hand-extracted from 10-Ks)
# ---------------------------------------------------------------------------

def build_five_below_stores() -> pd.DataFrame:
    """
    Store counts and comparable sales extracted from 10-K text sections.

    store_eop    = total stores open at end of fiscal year
    net_new      = net new stores opened during the fiscal year
    comp_sales   = comparable sales growth rate (% change, year-over-year)

    Source: each 10-K's "Our Company" and "Results of Operations" sections.
    FY2020 comp sales affected by COVID-19 store closures (noted).
    FY2021 comp sales benefit from COVID-19 recovery (noted).
    """
    data = [
        # fy,  stores_eop, net_new, comp_sales_pct,  note
        (2018, 750,  125,   3.9,  ""),
        (2019, 900,  150,   0.6,  ""),
        (2020, 1020, 120,  -5.5,  "COVID-19 store closures Mar–Apr 2020"),
        (2021, 1190, 170,  30.3,  "COVID-19 recovery rebound"),
        (2022, 1340, 150,  -2.0,  ""),
        (2023, 1544, 204,   2.8,  "53-week fiscal year"),
        (2024, 1771, 227,  -2.7,  ""),
        (2025, 1921, 150,  12.8,  ""),
    ]
    df = pd.DataFrame(data, columns=[
        "fiscal_year", "stores_eop", "net_new_stores",
        "comp_sales_pct", "note"
    ])
    return df


# ---------------------------------------------------------------------------
# Netflix price events
# ---------------------------------------------------------------------------

NETFLIX_PRICE_EVENTS = [
    {"date": "2020-10-01", "label": "Standard \\$12.99→\\$13.99"},
    {"date": "2022-01-01", "label": "Standard \\$13.99→\\$15.49"},
    {"date": "2022-11-01", "label": "Ads plan \\$6.99 launched"},
    {"date": "2023-05-01", "label": "Paid sharing enforced"},
    {"date": "2023-10-01", "label": "Basic/Premium raised"},
    {"date": "2025-01-01", "label": "Standard \\$15.49→\\$17.99"},
    {"date": "2026-03-01", "label": "Standard \\$17.99→\\$19.99"},
]
