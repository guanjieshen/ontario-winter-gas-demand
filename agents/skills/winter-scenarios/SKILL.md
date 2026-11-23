---
name: winter-scenarios
description: Forecast Ontario winter gas demand under weather scenarios (normal, cold, mild, X% colder) and for the coming week from the live ECCC forecast, compare with ai_forecast, and give a directional storage outlook. Use when the user asks what happens if the winter is colder or milder, wants a forecast for this winter or this week, or asks whether storage is enough.
---

# Winter scenarios

Requires the `demand_model` table (see the `demand-weather-model` skill). The notebook `notebooks/02_model_and_scenarios` creates `winter_scenarios`; `notebooks/03_next_week` creates `demand_next_week`.

## 1. Build scenarios from past winters

No weather forecast is needed. For each winter month, use HDD from past years (2016 to 2025):

| Scenario | HDD |
|---|---|
| Normal | Average for that calendar month |
| Cold | Coldest year for that month |
| Mild | Mildest year for that month |
| X% colder | Normal × (1 + X/100) |

Forecast volume = `(base + slope × HDD) × latest residential_customers / 1000` (thousands of m³).

Expected winter 2026-27 (Nov to Mar) residential totals on the shipped data:

| Scenario | Million m³ | vs. normal |
|---|---|---|
| 20% colder | 6,875 | +17% |
| Cold | 6,811 | +16% |
| Normal | 5,866 | |
| Mild | 5,063 | −14% |

To add a custom scenario, for example "January 2022 repeated", take that month's `avg_toronto_london_hdd` from `hdd_monthly` (820.3) and apply the model.

## 2. Compare with ai_forecast (stretch)

`ai_forecast` is a time-series forecast that knows nothing about weather. Comparing it with the weather model makes a good demo point. The horizon is exclusive, so use the month after the last one you want:

```sql
SELECT *
FROM ai_forecast(
  TABLE(SELECT month_start, residential_e3m3 FROM gas_monthly),
  horizon   => '2027-04-01',
  time_col  => 'month_start',
  value_col => 'residential_e3m3'
);
```

Requires a SQL warehouse (Pro or Serverless) or serverless compute.

## 3. The coming week from the live forecast

Run `notebooks/03_next_week`. It fetches the latest ECCC city forecasts for Toronto and London, averages their HDD, and writes:

- `weather_forecast`: every forecast fetched (new forecasts are added on each run, so it builds a forecast history)
- `demand_next_week`: expected residential use per day vs. normal weather for the same dates

Daily use per customer = `base_m3_per_customer / days in month + m3_per_customer_per_hdd × daily HDD`. Daily mean temperature = (high + following night's low) / 2. The forecast covers today plus five days.

Weekly summary:

```sql
SELECT MIN(forecast_date) AS from_date, MAX(forecast_date) AS to_date,
       ROUND(SUM(residential_million_m3), 0) AS expected_million_m3,
       ROUND(100 * (SUM(residential_million_m3) / SUM(normal_million_m3) - 1), 1) AS vs_normal_pct
FROM demand_next_week
```

The numbers change with every forecast, so there is no fixed expected result. Check that `hdd` is roughly 10 to 25 per day in late November, and higher in January.

If the fetch fails, the compute probably cannot reach `dd.weather.gc.ca`; ask the workspace admin to allow it.

## 4. Storage outlook (directional only)

Storage covers the gap between winter demand and pipeline supply. Useful facts from `gas_monthly`:

- Lowest end-of-winter inventory: 2.68 billion m³ (Mar 2019).
- Largest winter withdrawals: 6.33 billion m³ (winter 2021-22, which had the coldest January in the data).
- Smallest: 3.70 billion m³ (winter 2023-24).

A simple directional estimate: assume the **extra** residential demand in a cold scenario (cold total − normal total) is met from storage, and subtract it from a typical end-of-winter inventory.

Always label this **directional**. Storage is province-wide and serves more than Ontario homes, and supply responds in ways this data does not show.

## Pitfalls

- Keep customers fixed at the latest month unless the user asks for a growth assumption.
- `winter_scenarios.month_start` is Nov 2026 to Mar 2027; label the winter "2026-27".
- Do not present scenario numbers as a prediction of a specific utility's volumes.
