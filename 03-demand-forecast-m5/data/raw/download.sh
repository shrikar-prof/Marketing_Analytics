#!/usr/bin/env bash
# Download raw data for project 03 — Demand Forecast (M5 / Walmart)
# Run from the project root: bash data/raw/download.sh
set -e
cd "$(dirname "$0")"

echo "Downloading M5 dataset from Nixtla mirror (~48 MB zip)..."
curl -L --retry 3 -o m5.zip \
  "https://github.com/Nixtla/m5-forecasts/raw/main/datasets/m5.zip"

echo "Extracting..."
unzip -o -q m5.zip -d m5
rm m5.zip

echo "Done. Files in data/raw/m5/:"
ls -lh m5/
