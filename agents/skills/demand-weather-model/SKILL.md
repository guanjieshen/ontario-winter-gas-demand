---
name: demand-weather-model
description: Build, explain and backtest a model of Ontario gas demand against heating degree days (HDD). Use when the user asks how weather drives gas demand, wants to fit or improve the demand model, check its accuracy, or compare residential, commercial and industrial weather sensitivity.
---

# Demand vs. weather model

Gas demand for heating rises almost linearly with heating degree days. The starter model is a straight line fitted in SQL; no ML libraries are needed.

Requires the tables from the `winter-gas-data` skill. The notebook `notebooks/02_model_and_scenarios` runs every step below.

## 1. Fit the model

Target: `residential_m3_per_customer` (removes customer growth). Driver: `avg_toronto_london_hdd`.

```sql
CREATE OR REPLACE TABLE demand_model AS
SELECT
  COUNT(*) AS months,
  REGR_INTERCEPT(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS base_m3_per_customer,
  REGR_SLOPE(g.residential_m3_per_customer, h.avg_toronto_london_hdd)     AS m3_per_customer_per_hdd,
  REGR_R2(g.residential_m3_per_customer, h.avg_toronto_london_hdd)        AS r2
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE g.residential_m3_per_customer IS NOT NULL;
```

Expected on the shipped data: 93 months, base ≈ 44.5 m³, slope ≈ 0.486 m³ per HDD, R² ≈ 0.981.

**How to explain it:** a home uses about 44 m³ a month for hot water and cooking, plus about half a cubic metre for every heating degree day.

## 2. Turn per-customer use into volume

`residential_e3m3 = (base + slope × HDD) × residential_customers / 1000`

## 3. Backtest

Train on months before the winter you test, predict that winter from its actual HDD, and compare. The notebook tests winter 2025-26 (Nov 2025 to Mar 2026) and saves the `backtest` table. On the shipped data the monthly errors run from −0.8% to +8.5%, averaging 3.7%.

Always show a backtest before showing a forecast. It is what makes the forecast credible.

## 4. Compare sectors

Swap the target column to see which loads depend on weather:

| Target | R² vs HDD (2019 onward) | Meaning |
|---|---|---|
| `residential_m3_per_customer` | 0.981 | Heating-driven |
| `commercial_m3_per_customer` | 0.963 | Heating-driven |
| `industrial_m3_per_customer` | 0.202 | Mostly process load, not weather |

## Ideas to improve the model

- Add a month-of-year or holiday effect (`MONTH(month_start)`) to capture shoulder-season behaviour.
- Fit separate slopes for each winter month.
- Use a different HDD base from `weather_daily.mean_temp_c` (for example 15.5 °C) and compare R².
- Train an ML model with Genie Code (for example gradient boosting) and compare its backtest error with the straight line.

## Pitfalls

- Do not train on 2016 to 2018 per-customer values; they are NULL by design (customer count method change).
- Report R² and backtest error together; a high R² on training data alone overstates accuracy.
- Province-wide monthly data shows the method. Say that an operational model would use a utility's own daily throughput.
