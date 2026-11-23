---
name: winter-gas-data
description: Load and explain the Ontario winter gas demand hackathon data (gas_monthly, hdd_monthly, weather_daily). Use when the user wants to set up the tables in Unity Catalog, asks what a table or column means, which units to use, or why per-customer values are missing before 2019.
---

# Ontario winter gas demand data

Public data for forecasting Ontario natural gas demand from weather. Statistics Canada provides monthly gas use and storage; Environment and Climate Change Canada (ECCC) provides weather and heating degree days (HDD).

## Load the tables

1. The repo should be cloned as a Databricks Git folder. Ask the user for the target `catalog` and `schema` if they have not said.
2. Run the notebook `notebooks/00_setup` with widgets `catalog` and `schema`. It reads `data/processed/*.csv` from the repo, writes three Delta tables, and adds table and column comments.
3. Check the load:

```sql
SELECT 'gas_monthly' AS t, COUNT(*) AS n FROM gas_monthly      -- expect 129 (2016-01 to 2026-09)
UNION ALL SELECT 'hdd_monthly', COUNT(*) FROM hdd_monthly       -- expect 131 (2016-01 to 2026-11)
UNION ALL SELECT 'weather_daily', COUNT(*) FROM weather_daily;  -- expect 15,220
```

Row counts grow if the data has been refreshed with `scripts/download_raw.py` and `scripts/build_processed.py`.

## Tables

| Table | Grain | Key columns |
|---|---|---|
| `gas_monthly` | One row per month | `month` (YYYY-MM), `month_start` (DATE), consumption by sector, customers, storage |
| `hdd_monthly` | One row per month | `month`, `month_start`, `<city>_hdd`, `avg_toronto_london_hdd`, `avg_4city_hdd` |
| `weather_daily` | One row per station per day | `date`, `city`, `mean_temp_c`, `hdd` |

Join `gas_monthly` and `hdd_monthly` on `month`.

## Column naming in `gas_monthly`

`<measure>_<unit>`. Measures: `residential`, `commercial`, `industrial`, `total_deliveries`, `storage_opening`, `storage_closing`, `storage_injections`, `storage_withdrawals`, `storage_change`.

| Suffix | Unit | To convert |
|---|---|---|
| `_e3m3` | Thousands of m³ | ÷ 1,000 for million m³, ÷ 1,000,000 for billion m³ |
| `_e3gj` | Thousands of GJ | |
| `_k_cad` | Thousands of CAD | |
| `_customers` | Customer count | |
| `_m3_per_customer` | m³ per customer (derived) | |

## Rules to follow

- **Use one unit per query.** Never add `_e3m3` and `_e3gj` values together.
- **Per-customer data starts in 2019.** StatCan did not collect customer counts from 2016 to 2018, so `*_m3_per_customer` is NULL before 2019-01 and `*_customers` jumps in Jan 2019 (about 2.06M to 3.42M residential). That is a method change, not growth. For 2016 to 2018 use volumes only.
- **Use `avg_toronto_london_hdd` as the weather driver.** It has no gaps. Sarnia and Windsor have missing months, so `avg_4city_hdd` is NULL in 25 months.
- **HDD = max(0, 18 − mean temperature °C)**, summed over the month. More HDD means colder.
- **This is province-wide data.** It covers all of Ontario, not a single utility. Say so when presenting results.
- `storage_change_e3m3` is negative in withdrawal months.

## Reference

Full column-by-column guide: `DATASETS.md` in the repo root.
