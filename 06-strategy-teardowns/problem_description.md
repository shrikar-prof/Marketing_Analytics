# Project 06: Public-Data Strategy Teardowns

## Problem
Prospective clients want to see how a consultant reasons from messy public data to a decision before trusting them with internal data. Each teardown takes a real company's public filings and answers one strategic question in a short memo.

## Questions to answer
1. **Netflix:** what did the US price increases do to memberships, revenue per member and revenue? (US and Canada region, Q4 2019 to Q4 2024, the full period for which Netflix reported memberships.)
2. **Five Below:** does the store expansion pace make sense? Are new stores as productive as the base, and what did the fast-opening years do to comparable sales and operating margin? (Fiscal 2018 to fiscal 2025.)

## Deliverable expected
One memo per question (4 to 6 pages with charts, data tables and sources), reusable EDGAR download and parsing code, and an offer sheet for a teardown on a company of the client's choosing.

## Data: SEC EDGAR
All data is public domain. EDGAR requires a `User-Agent` header with a name and contact email (SEC fair-access policy); keep requests under 10 per second.

### Netflix (CIK 1065280)
The quarterly shareholder letter is filed as Exhibit 99.1 to an 8-K. Each Q4 letter contains a regional table (UCAN, EMEA, LATAM, APAC) with five quarters of revenue, paid memberships, paid net additions and average revenue per membership (ARM). The Q4 letters for 2020 to 2024 cover Q4'19 to Q4'24 without gaps. `pandas.read_html` extracts the tables.

Files: `data/raw/netflix_letters/*.htm`, `data/raw/netflix_submissions.json`

```
UA="Your Name your@email.com"
curl -H "User-Agent: $UA" -o data/raw/netflix_submissions.json https://data.sec.gov/submissions/CIK0001065280.json
mkdir -p data/raw/netflix_letters
for pair in "2021-01-19 000106528021000037 ex991_q420.htm" "2022-01-20 000106528022000035 ex991_q421.htm" \
            "2023-01-19 000106528023000034 ex991_q422.htm" "2024-01-23 000106528024000029 ex991_q423.htm" \
            "2025-01-21 000106528025000033 ex991_q424.htm" "2026-01-20 000106528026000033 ex991_q425.htm"; do
  set -- $pair
  curl -H "User-Agent: $UA" -o "data/raw/netflix_letters/$1_$3" "https://www.sec.gov/Archives/edgar/data/1065280/$2/$3"; sleep 0.3
done
```
Price events to mark (US): Standard plan $12.99 to $13.99 (Oct 2020); $13.99 to $15.49 (Jan 2022); ads plan launched at $6.99 (Nov 2022); paid-sharing enforcement (May 2023); Basic $9.99 to $11.99 and Premium $19.99 to $22.99 (Oct 2023); Standard to $17.99 (Jan 2025); Standard to $19.99 (Mar 2026). Netflix stopped reporting memberships after Q4 2024.

### Five Below (CIK 1177609)
- XBRL financial facts (revenue, operating income, net income, SG&A, capex, by fiscal year) from the companyfacts API: `data/raw/five_below_companyfacts.json`.
- Store counts, net new stores and comparable sales are not XBRL-tagged; they come from the 10-K text ("As of January 31, 2026, we operated 1,921 stores in 46 states", "comparable sales increased by 12.8% in fiscal 2025"). Eight 10-Ks, FY2018 to FY2025, saved as stripped text in `data/raw/five_below_10k/*.txt`; `data/raw/five_below_submissions.json` lists the filings.

```
UA="Your Name your@email.com"
curl -H "User-Agent: $UA" -o data/raw/five_below_companyfacts.json https://data.sec.gov/api/xbrl/companyfacts/CIK0001177609.json
curl -H "User-Agent: $UA" -o data/raw/five_below_submissions.json https://data.sec.gov/submissions/CIK0001177609.json
# 10-K primary documents: list accession numbers from the submissions JSON (form == "10-K"),
# then fetch https://www.sec.gov/Archives/edgar/data/1177609/<accession-without-dashes>/<primaryDocument>
```
Fiscal years end late January or early February; FY2025 ended 2026-01-31.

### Store-location data (not downloaded, for a trade-area extension)
Foursquare Open Source Places (Apache 2.0, 100M+ POIs, chain queries) or Overture Maps Places (GeoParquet); US Census ACS for demographics.
