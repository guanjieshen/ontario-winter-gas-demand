# Ontario Winter Gas Demand

![Data: Statistics Canada](https://img.shields.io/badge/data-Statistics%20Canada-red)
![Data: ECCC](https://img.shields.io/badge/data-ECCC%20Climate-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## Overview

Public, open-licence data for forecasting **Ontario natural gas demand from weather**. The repo pairs monthly Ontario gas consumption and storage from Statistics Canada with daily temperature and heating degree days (HDD) from Environment and Climate Change Canada.

It is built as a starter kit for a one-day hackathon: load the CSVs, model demand against HDD, forecast the coming winter, and run "what if January is colder?" scenarios.

> [!NOTE]
> This is provincial, monthly, public data. It shows the **method**. For an operational forecast, swap in daily or hourly throughput from your own systems.

**How strong is the weather signal?** A simple straight-line fit on monthly HDD alone gives:

| Target | Period | Months | R² |
|---|---|---|---|
| Residential use per customer (m³) | 2019-01 to 2026-09 | 93 | 0.98 |
| Residential volume (10³ m³) | 2016-01 to 2026-09 | 129 | 0.96 |
| Total deliveries to consumers (10³ m³) | 2016-01 to 2026-09 | 129 | 0.88 |

HDD here is the Toronto and London average (`avg_toronto_london_hdd`).

## Repository layout

| Path | What it holds |
|---|---|
| `data/raw/statcan/` | StatCan table 25-10-0086-01, full table for all provinces, as published (`25100086.csv`, `25100086_MetaData.csv`) |
| `data/raw/eccc/` | ECCC daily climate CSVs, one file per station per year, as published |
| `data/processed/` | Tidy Ontario-only CSVs, ready to load |
| `scripts/download_raw.py` | Re-downloads everything in `data/raw/` |
| `scripts/build_processed.py` | Rebuilds `data/processed/` from `data/raw/` |

## Quick start

1. **Use the processed files directly.** Everything in `data/processed/` is ready to upload to a Unity Catalog volume or load as tables.
2. **Join on `month`.** `ontario_gas_monthly.csv` and `ontario_hdd_monthly.csv` share a `month` key in `YYYY-MM` format.
3. **Refresh (optional).** To pull the latest releases and rebuild:

```bash
python3 scripts/download_raw.py
python3 scripts/build_processed.py
```

Both scripts use the Python standard library only.

## Processed datasets

### `ontario_gas_monthly.csv`

One row per month, Jan 2016 to Sep 2026 (129 rows). Source: StatCan 25-10-0086-01, Ontario.

| Column pattern | Meaning |
|---|---|
| `month` | Reference month, `YYYY-MM` |
| `residential_*`, `commercial_*`, `industrial_*` | Consumption by sector |
| `total_deliveries_*` | Total deliveries to consumers |
| `storage_opening_*`, `storage_closing_*` | Storage inventory at start and end of month |
| `storage_injections_*`, `storage_withdrawals_*`, `storage_change_*` | Storage flows in the month (`storage_change` can be negative) |
| `*_m3_per_customer` | Derived: volume ÷ customers, in m³ per customer. **2019 onward only.** |

Unit suffixes:

| Suffix | Unit |
|---|---|
| `_e3m3` | Thousands of cubic metres |
| `_e3gj` | Thousands of gigajoules |
| `_k_cad` | Thousands of Canadian dollars |
| `_customers` | Number of customers |

### `ontario_hdd_monthly.csv`

One row per month, Jan 2016 to Nov 2026. Source: ECCC daily observations.

| Column | Meaning |
|---|---|
| `toronto_hdd`, `london_hdd`, `sarnia_hdd`, `windsor_hdd` | Monthly heating degree days (18 °C base) per city |
| `avg_toronto_london_hdd` | Average of Toronto and London. **Recommended model input** (complete for every full month). |
| `avg_4city_hdd` | Average of all four cities, only when all four are complete |
| `*_days_reported` | Days with HDD reported that month |

A city's month is kept only if at least 25 days were reported. Missing days are then filled in proportionally. Otherwise the month is left blank.

### `ontario_weather_daily.csv`

One row per station per day (about 15,000 rows): `date`, `city`, `station_name`, `climate_id`, `max_temp_c`, `min_temp_c`, `mean_temp_c`, `hdd`, `hdd_flag`, `total_precip_mm`, `snow_on_ground_cm`. Use it for daily scenarios or custom HDD bases.

## Weather stations

| City | Station | Climate ID | Years used |
|---|---|---|---|
| Toronto | TORONTO INTL A (Pearson) | 6158731 | 2016–2026 |
| London | LONDON A | 6144473 | 2016–2026 |
| Sarnia | SARNIA | 6127510 | 2016–2026 |
| Windsor | WINDSOR RIVERSIDE | 6139520 | 2016–2017 |
| Windsor | WINDSOR A | 6139530 | 2018–2026 |

> [!WARNING]
> Do not use climate ID 6158733 for Toronto Pearson. That older station stops publishing in 2013.

## Known data gotchas

> [!WARNING]
> **Customer counts change method in 2019.** StatCan did not collect customer counts from Jan 2016 to Dec 2018 (table note 8). The residential count jumps from about 2.06M to 3.42M in Jan 2019. Volumes are consistent across the break, but per-customer figures are only valid from 2019, so `*_m3_per_customer` is blank before then.

- **Pick one unit.** Consumption is published in four units (m³, GJ, dollars, customers). Filter to one per query or totals double-count.
- **Ontario-wide, not utility-specific.** StatCan figures cover all of Ontario, including storage operated by more than one company.
- **Sarnia and Windsor have gaps.** Some months fall below 25 reported days. Use `avg_toronto_london_hdd` for a gap-free series.
- **Latest month is partial.** The current month's HDD is blank until enough days are reported, and the 2026 ECCC files contain blank future-dated rows, which the build drops.
- **StatCan revises data.** Re-running the scripts may change recent months.

## Hackathon ideas

| Level | Idea |
|---|---|
| Core | Fit residential use per customer against HDD; chart actual vs fitted |
| Core | Dashboard: demand by sector, storage inventory over the year, HDD by city |
| Core | A Genie space over the two monthly tables ("How did January 2026 compare with January 2025?") |
| Stretch | Forecast the next six months with `ai_forecast` or an ML model |
| Stretch | Weather scenarios: rerun the forecast with a 20% colder January, or with the coldest winter on record |
| Stretch | Storage outlook: estimate end-of-winter inventory under each scenario (directional only) |

## Sources and licences

| Dataset | Source | Licence |
|---|---|---|
| Natural gas supply and disposition, monthly (table 25-10-0086-01) | [Statistics Canada](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2510008601) | [Statistics Canada Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence) |
| Daily climate observations | [ECCC MSC Datamart](https://dd.weather.gc.ca/today/climate/observations/daily/csv/ON/) | [ECCC Data Servers End-use Licence](https://eccc-msc.github.io/open-data/licence/readme_en/) |

**Attribution:**

- Source: Statistics Canada, Table 25-10-0086-01, Natural gas supply and disposition, monthly. Reproduced and distributed on an "as is" basis with the permission of Statistics Canada.
- Data Source: Environment and Climate Change Canada.

The processed files are derived from these sources by the scripts in this repo. This repo is not endorsed by Statistics Canada or ECCC.
