# Dataset guide

This guide explains each dataset in the repo: what it measures, where it comes from, how to read every column, and what to watch out for. All figures quoted below come straight from the files in `data/processed/`.

> [!TIP]
> **Short on time?** Use two files: `ontario_gas_monthly.csv` (what Ontario burned) and `ontario_hdd_monthly.csv` (how cold it was). Join them on `month`.

## The use case

**Forecast how much gas Ontario will need this winter, and test what happens if it turns colder than expected.**

Gas demand in Ontario is driven mainly by space heating, so the weather drives it. A gas distributor plans around that: supply contracts, storage drawdown, staffing and budgets all depend on how cold the winter turns out. The workflow is the same at every scale:

1. **Learn the relationship.** How much does demand rise for each extra degree of cold?
2. **Forecast.** Apply that relationship to an expected winter.
3. **Stress test.** Rerun it for a cold winter and a mild one, and check whether storage holds up.

The data in this repo covers each step with public data. The fit is strong: monthly HDD alone explains **98%** of the variation in residential use per customer (2019 to 2026). That's what makes it a good one-day build.

> [!NOTE]
> This is a **method demo**. Provincial monthly totals show the pattern. An operational forecast would use the same steps on a utility's own daily or hourly throughput, by region and rate class.

**How each dataset fits:**

| Step | Dataset | Role |
|---|---|---|
| Learn the relationship | `ontario_gas_monthly.csv` + `ontario_hdd_monthly.csv` | The target (demand) and the driver (cold) |
| Forecast | `ontario_hdd_monthly.csv` | Normal and extreme winters to feed the model |
| Stress test | `ontario_gas_monthly.csv` (storage columns) | Shows whether storage can cover a colder winter |
| Go deeper | `ontario_weather_daily.csv` | Daily cold snaps and custom HDD definitions |
| Explore beyond Ontario | Raw StatCan and ECCC files | Other provinces and categories, and every published field |

## At a glance

| File | What it answers | One row is | Rows | Period |
|---|---|---|---|---|
| [`ontario_gas_monthly.csv`](#ontario_gas_monthlycsv) | How much gas did Ontario use, and how full was storage? | One month | 129 | Jan 2016 to Sep 2026 |
| [`ontario_hdd_monthly.csv`](#ontario_hdd_monthlycsv) | How cold was each month? | One month | 131 | Jan 2016 to Nov 2026 |
| [`ontario_weather_daily.csv`](#ontario_weather_dailycsv) | What was the weather each day? | One station, one day | 15,220 | 1 Jan 2016 to 22 Nov 2026 |
| [Raw StatCan table](#raw-statcan-table-25-10-0086-01) | Same as the gas file, for every province and every category | One month × province × category × unit | 108,876 | Jan 2016 to Sep 2026 |
| [Raw ECCC files](#raw-eccc-daily-climate-files) | Full daily weather as published | One station, one day | 44 files | 2016 to 2026 |

## Key concepts

| Term | Meaning |
|---|---|
| **HDD (heating degree days)** | How far the day's mean temperature fell below 18 °C. A day at −2 °C is 20 HDD; a day above 18 °C is 0. Add up the days to get a month's HDD. More HDD means more heating, which means more gas. |
| **10³ m³ (`e3m3`)** | Thousands of cubic metres of gas, the standard Canadian volume unit. 1,000,000 e3m3 = 1 billion m³. |
| **10³ GJ (`e3gj`)** | Thousands of gigajoules, the energy content of the gas. |
| **Storage injection / withdrawal** | Gas pumped into underground storage (mostly summer) or pulled out (mostly winter). |

## `ontario_gas_monthly.csv`

**Ontario's natural gas use by customer type, plus underground storage, month by month.**

| | |
|---|---|
| **Source** | Statistics Canada table 25-10-0086-01, Natural gas supply and disposition, monthly, filtered to Ontario |
| **Licence** | Statistics Canada Open Licence |
| **Grain** | One row per month (`month` = `YYYY-MM`) |
| **Coverage** | Jan 2016 to Sep 2026, 129 months, no gaps |
| **Updates** | StatCan releases monthly, about two months behind, and revises recent months |

### Why it matters for the use case

This is the **target** the forecast predicts:
- **Residential and commercial use is the weather-sensitive load.** It's heating, and it's what swings between a mild winter and a cold one.
- **Industrial use is the steadier base load.** It shows how much demand doesn't depend on weather.
- **`residential_m3_per_customer` takes out customer growth.** That leaves pure weather sensitivity, which is why it's the cleanest series to model. Multiply back by the customer count to get total volume.
- **The storage columns turn a demand forecast into an operational question:** "If January is 20% colder, how much more do we withdraw, and how low does inventory get by March?"
- **The `_k_cad` columns** support a rough dollar view of a cold winter.

### Columns

Each measure comes in up to four units. The suffix tells you which: `_e3m3` (10³ m³), `_e3gj` (10³ GJ), `_k_cad` (thousands of CAD), `_customers` (count).

**Consumption by sector**

| Column | Description | Observed range |
|---|---|---|
| `residential_e3m3` | Gas used by homes | 170,644 to 1,576,767 |
| `residential_e3gj` | Same, as energy | 6,684 to 61,904 |
| `residential_k_cad` | Value of the gas delivered | 92,430 to 651,829 |
| `residential_customers` | Residential customers | 1,971,384 to 3,689,388 (see the 2019 warning below) |
| `commercial_e3m3`, `_e3gj`, `_k_cad`, `_customers` | Same set for businesses, offices, schools and similar | 132,223 to 1,286,915 e3m3 |
| `industrial_e3m3`, `_e3gj`, `_k_cad`, `_customers` | Same set for industrial users | 669,757 to 2,259,820 e3m3 |
| `total_deliveries_e3m3`, `_e3gj`, `_k_cad`, `_customers` | All consumers combined | 1,123,396 to 5,080,419 e3m3 |

**Storage**

| Column | Description | Observed range (e3m3) |
|---|---|---|
| `storage_opening_e3m3` | Gas in Ontario storage at the start of the month | 2,684,110 to 9,417,337 |
| `storage_closing_e3m3` | Gas in storage at the end of the month | 2,684,110 to 9,417,337 |
| `storage_injections_e3m3` | Gas put into storage during the month | 0 to 1,484,884 |
| `storage_withdrawals_e3m3` | Gas taken out of storage during the month | 0 to 3,055,274 |
| `storage_change_e3m3` | Net change in inventory. Negative means a drawdown. | −2,995,541 to 1,476,051 |

Each storage column also has an `_e3gj` version.

**Derived**

| Column | Description | Observed range |
|---|---|---|
| `residential_m3_per_customer` | Residential volume ÷ residential customers, in m³ per customer | 48.4 to 446.0 |
| `commercial_m3_per_customer` | Same for commercial | 451.9 to 4,542.6 |
| `industrial_m3_per_customer` | Same for industrial | 65,942 to 184,656 |

### What a winter and a summer month look like

| Month | Residential use (e3m3) | Residential customers | m³ per customer | Storage withdrawals (e3m3) | Storage injections (e3m3) | Storage at month end (e3m3) |
|---|---|---|---|---|---|---|
| Jan 2026 | 1,570,468 | 3,679,622 | 426.8 | 2,357,477 | 0 | 5,018,118 |
| Jul 2026 | 247,774 | 3,686,980 | 67.2 | 0 | 743,358 | 7,196,279 |

An Ontario home used about six times more gas in January 2026 than in July 2026.

### Watch out for

> [!WARNING]
> **Customer counts before 2019 aren't comparable.** StatCan did not collect customer counts from Jan 2016 to Dec 2018 (table note 8). The residential count jumps from about 2.06 million to 3.42 million in Jan 2019. That's a method change, not real growth. The `*_m3_per_customer` columns are therefore blank before 2019. Volumes are consistent across the break.

- **Don't add units together.** Every measure appears in several units, so pick one suffix per query.
- **This covers all of Ontario.** It includes every distributor and every storage operator in the province, not one company.
- **`k_cad` is the delivered value reported to StatCan,** not a utility bill.

## `ontario_hdd_monthly.csv`

**How cold each month was in four southwestern Ontario cities.**

| | |
|---|---|
| **Source** | Built from ECCC daily climate observations (see the daily file below) |
| **Licence** | ECCC Data Servers End-use Licence (attribution required) |
| **Grain** | One row per month (`month` = `YYYY-MM`) |
| **Coverage** | Jan 2016 to Nov 2026. Nov 2026 is partial and therefore blank. |

### Why it matters for the use case

This is the **driver** of the forecast:
- **HDD is the industry-standard way to measure heating demand.** Demand rises close to linearly with HDD, which makes the model simple enough to build and explain in a day.
- **It's already at the same monthly grain as the gas data,** so teams can join on `month` and start modelling right away.
- **Past winters become ready-made scenarios.** Teams don't need a weather forecast. They can pick a real winter, such as the coldest January (2022) or the mildest (2023), and ask what demand would be.
- **The four cities sit in the heart of Ontario's gas-heated population and storage region.** The Toronto–London average stands in for the province's weather.

### Columns

| Column | Description | Blank months |
|---|---|---|
| `toronto_hdd` | Monthly HDD at Toronto Pearson | 1 (Nov 2026) |
| `london_hdd` | Monthly HDD at London airport | 1 (Nov 2026) |
| `sarnia_hdd` | Monthly HDD at Sarnia | 15 |
| `windsor_hdd` | Monthly HDD at Windsor | 14 |
| `avg_toronto_london_hdd` | Average of Toronto and London. **Use this one for modelling.** | 1 (Nov 2026) |
| `avg_4city_hdd` | Average of all four cities, filled only when all four are present | 25 |
| `toronto_days_reported` … `windsor_days_reported` | Number of days with HDD data in the month | 0 |

### How the monthly HDD is calculated

1. Add up the daily HDD for the month.
2. If at least 25 days were reported, scale the total up to the full month to cover any missing days.
3. If fewer than 25 days were reported, leave the month blank.

### Example: Januaries ranked by cold

Using `avg_toronto_london_hdd`, coldest first:

| January | HDD |
|---|---|
| 2022 | 820.3 (coldest) |
| 2026 | 775.2 |
| 2019 | 771.7 |
| 2025 | 751.2 |
| 2018 | 748.5 |
| 2016 | 685.0 |
| 2021 | 649.8 |
| 2024 | 636.1 |
| 2017 | 617.2 |
| 2020 | 603.8 |
| 2023 | 584.2 (mildest) |

These make good scenarios, for example: "What if this January is as cold as January 2022?"

### Watch out for

- **Sarnia and Windsor have gaps.** That's why `avg_4city_hdd` is blank in 25 months. Use `avg_toronto_london_hdd` for an unbroken series.
- **HDD uses an 18 °C base,** the ECCC standard. For a different base, recalculate from `mean_temp_c` in the daily file.

## `ontario_weather_daily.csv`

**Daily weather for each station, cleaned and combined into one file.**

| | |
|---|---|
| **Source** | ECCC daily climate observations, MSC Datamart |
| **Licence** | ECCC Data Servers End-use Licence (attribution required) |
| **Grain** | One row per station per day |
| **Coverage** | 1 Jan 2016 to 22 Nov 2026, 15,220 rows |

### Why it matters for the use case

This is the **detail behind** the monthly HDD, and it's optional for the core build:
- **Cold snaps stand out.** Gas systems are stressed by peak days, not monthly averages. Teams can find the coldest days, such as 30 Jan 2019, and see how extreme they get.
- **Teams can build custom scenarios,** such as "the week of 30 Jan 2019, repeated", or recalculate HDD with a different base temperature.
- **It's the bridge to production.** Real utility forecasts run daily. This file shows teams how they would join daily weather to daily throughput data.

### Columns

| Column | Description |
|---|---|
| `date` | Observation date, `YYYY-MM-DD` |
| `city` | Toronto, London, Sarnia or Windsor |
| `station_name` | ECCC station name |
| `climate_id` | ECCC climate ID |
| `max_temp_c`, `min_temp_c`, `mean_temp_c` | Daily temperatures in °C |
| `hdd` | Heating degree days, 18 °C base |
| `hdd_flag` | ECCC quality flag. `E` = estimated (13 rows). Blank = normal. |
| `total_precip_mm` | Rain plus melted snow, in mm (blank in 4,156 rows) |
| `snow_on_ground_cm` | Snow depth, in cm (blank in 13,551 rows, so mostly empty) |

### Rows per station

| City | Station | Climate ID | Rows |
|---|---|---|---|
| Toronto | TORONTO INTL A | 6158731 | 3,956 |
| London | LONDON A | 6144473 | 3,896 |
| Sarnia | SARNIA | 6127510 | 3,757 |
| Windsor | WINDSOR A | 6139530 | 2,893 (2018 onward) |
| Windsor | WINDSOR RIVERSIDE | 6139520 | 718 (2016 to 2017) |

The coldest day in the file is 30 Jan 2019 in Windsor, with a mean temperature of −21.3 °C.

### Watch out for

- **Windsor is two stations combined.** No single Windsor station publishes daily files for the whole period. Filter on `city`, not `station_name`, to get one Windsor series.
- **Missing days aren't stored as rows.** Days with no temperature or HDD reading are left out, so count rows before assuming a month is complete.

## Raw StatCan table 25-10-0086-01

`data/raw/statcan/25100086.csv` (17 MB) and `25100086_MetaData.csv`, exactly as StatCan publishes them.

| | |
|---|---|
| **Covers** | Canada and all 13 provinces and territories |
| **Rows** | 108,876 |
| **Key columns** | `REF_DATE` (month), `GEO` (province), `Supply and disposition` (category), `UOM` (unit), `SCALAR_FACTOR` (for example `thousands`), `VALUE`, `STATUS` |

**Why it matters for the use case:**
- **It's the audit trail.** Every number in `ontario_gas_monthly.csv` traces back to it, which matters for showing trust and governance in the demo.
- **Supply-side stretch work.** It adds imports from the US, receipts from other provinces and pipeline fuel, which help explain where winter gas comes from beyond storage.
- **Benchmarking.** Teams can compare Ontario's weather sensitivity with another province's.

**Watch out for:**
- **Suppressed values.** Some cells are blank with `STATUS` = `..` (not available) or `x` (suppressed). In Ontario this only affects imports from and exports to countries other than the US, and deliveries to processing plants.
- **The double space in `Closing  inventory, storage`** is in the source.
- **Read the notes.** The metadata file has the full list, including note 8 on customer counts.

## Raw ECCC daily climate files

`data/raw/eccc/climate_daily_ON_<climate_id>_<year>_P1D.csv`: 44 files, one per station per year, as published.

**Why it matters for the use case:** it's the audit trail for the weather data. It also has the columns the daily file leaves out, such as cooling degree days, rain and snow split out, and gust speed, along with every quality flag. Teams can test whether wind or snow explains any demand the HDD model misses.

**Watch out for:** blank rows for future dates in the current year's files, and older files that may use latin-1 text encoding.

## Live forecast (optional)

`notebooks/03_next_week` fetches the latest **ECCC city forecasts** for Toronto (site `s0000458`) and London (site `s0000326`) from the [MSC Datamart](https://dd.weather.gc.ca/today/citypage_weather/ON/). Same source and licence as the observed weather.

| Table | One row is | Notes |
|---|---|---|
| `weather_forecast` | One city, one forecast day, one issue | `issued_at`, `city`, `forecast_date`, `high_c`, `low_c`, `mean_c`, `hdd`, `fetched_at`. **New forecasts are added on every run; re-runs do not duplicate.** |
| `demand_next_week` | One forecast day | Expected residential use vs. normal weather for the latest forecast |

**Why it matters for the use case:** it turns the model into a live tool. A planner sees expected demand for the coming week, compared with normal, without waiting for the monthly StatCan data.

**Watch out for:**
- **Only about six days.** The forecast covers today plus five days. ECCC's seventh day has a high but no overnight low, so it is dropped.
- **Daily mean is estimated** as (daytime high + following night's low) / 2.
- **No forecast archive.** ECCC keeps only about the last month on the Datamart, so `weather_forecast` only holds forecasts you have fetched yourself.
- **Needs internet access** from your compute to `dd.weather.gc.ca`.

## Questions to try

| Question | Files |
|---|---|
| How much more gas does a home use for every extra HDD? | gas monthly + HDD monthly |
| How did January 2026 compare with January 2025, for both cold and demand? | gas monthly + HDD monthly |
| How low does storage get by the end of each winter, and in which month? | gas monthly |
| Does commercial demand follow the weather as closely as residential? | gas monthly + HDD monthly |
| If next January is as cold as January 2022, how much gas will homes use? | gas monthly + HDD monthly |
| Which city is coldest on average, and by how much? | HDD monthly or weather daily |

## Attribution

When you publish anything built on this data, credit the sources:

- *Source: Statistics Canada, Table 25-10-0086-01, Natural gas supply and disposition, monthly.*
- *Data Source: Environment and Climate Change Canada.*
