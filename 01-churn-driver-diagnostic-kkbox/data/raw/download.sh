#!/usr/bin/env bash
# Download raw data for project 01 — Churn Driver Diagnostic
# Run from the project root: bash data/raw/download.sh
set -e
cd "$(dirname "$0")"

echo "Downloading IBM Telco Customer Churn (948 KB)..."
curl -L --retry 3 -o telco_customer_churn.csv \
  "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

echo "Downloading KKBox transactions from Mendeley (82 MB) — may take a few minutes..."
curl -L -C - --retry 5 -o kkbox_transactions_v2.csv \
  "https://data.mendeley.com/public-files/datasets/mv3f8bdrvy/files/503be31b-1630-4732-8ad7-f07856aae192/file_downloaded"

echo "Done. Files in data/raw/:"
ls -lh .
