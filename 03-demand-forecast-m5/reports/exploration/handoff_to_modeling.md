# Handoff to Model Builder

## Cleaned files

| File | Description |
|------|-------------|
| `reports/exploration/clean.parquet` | sales_train_evaluation, wide format, 30,490 rows x 1,946 cols. Melt d_* columns to long format before modelling. |
| `reports/exploration/calendar_clean.parquet` | Calendar with event nulls filled, d_col column added. |
| `reports/exploration/sell_prices_clean.parquet` | Weekly prices; no changes from raw. |

## Target column

The target is **daily unit sales**, one value per item x store x day.
In the wide parquet, columns `d_1` … `d_1941` are the target values.
After melting, the target column should be named `units`.

## Columns to exclude and why

| Column | Reason to exclude |
|--------|------------------|
| `item_id` alone | String identifier; use as a grouping key or embed, not a raw numeric. |
| `d_col` in calendar | Helper index; use `date` or `wm_yr_wk` instead. |
| `weights_evaluation.csv` | For WRMSSE metric computation only, not a model input. |
| `sales_test_evaluation.csv` | Hold-out actuals; keep sealed until final evaluation. |

## Columns that need encoding

| Column | Suggested encoding |
|--------|-------------------|
| `cat_id` (3 levels) | One-hot or ordinal |
| `dept_id` (7 levels) | One-hot or target-encode |
| `store_id` (10 levels) | One-hot or target-encode |
| `state_id` (3 levels) | One-hot |
| `weekday` | One-hot or Fourier (cyclic) |
| `month` | Fourier (cyclic) |
| `event_type_1/2` | One-hot (5 levels including 'None') |
| `snap_CA/TX/WI` | Binary flag; match to item's state |

## Suggested validation design

Use a **walk-forward validation** (time-series cross-validation):
- Training: d_1 … d_1885 (last 28 days of training = validation window 1)
- Validation: d_1886 … d_1913 (next 28 days)
- Then shift forward and repeat.
- Final hold-out: d_1942 … d_1969 (sales_test_evaluation.csv).

Why walk-forward: demand is a time series. Random train/test splits leak future
information (a 2016 day would appear in training while a 2011 day is in the test
set), producing optimistic error estimates that do not reflect live performance.

## Known pitfalls

1. **Zero inflation.** ~50% of item-days are zero. Models that minimise squared
   error will under-forecast. Consider Tweedie, negative-binomial, or a
   two-stage (zero/non-zero x volume) approach.
2. **Stockout ambiguity.** Zero sales may be stockouts, not zero demand.
   The data contains no stockout flags. Downstream replenishment decisions
   based on these forecasts carry this uncertainty.
3. **New items.** Some series begin with many zeros before the item launches.
   Filter these using the first non-zero date per series rather than including
   leading zeros in the training window.
4. **Collinear calendar features.** `weekday`, `wday`, `month`, and `year`
   are all derivable from `date`. Use `date` as the master and derive features
   rather than including all calendar columns simultaneously.
5. **State–SNAP interaction.** The SNAP flags are state-specific: `snap_CA`
   applies only to California stores. Apply the right SNAP flag per series.
6. **Price leakage.** Future sell prices (after the forecast horizon) must
   not be used as inputs. Use only prices from the last known week before the
   forecast origin.
7. **Small cells.** Some department x store combinations have very few series
   (< 50). Estimates for these will be noisy; consider pooling with similar
   departments.

## Business metric

The M5 competition metric is WRMSSE (weighted root mean scaled squared error),
which weights each series by its dollar-sales share. For the business question
in this project, track:
- **WRMSSE** at Level 12 (item x store): the official competition metric.
- **MAE in units** vs the rule-of-thumb baseline (computed in notebook Section 6).
- **Dollar over-stock and under-stock** in a replenishment simulation at a
  stated service level (e.g., 95%): the most direct business metric.

The rule-of-thumb baseline MAE is computed in Section 6 of the exploration notebook
and should be used as the minimum bar any model must beat.