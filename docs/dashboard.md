# Dashboard spec: Ontario Winter Gas Outlook

An AI/BI dashboard with four pages. Every query below has been tested on the shipped data.

> [!NOTE]
> Run `notebooks/00_setup` and `notebooks/02_model_and_scenarios` first. In the dashboard's **Data** tab, set the default catalog and schema to yours so the queries below work as written.

## Datasets

Add each of these on the **Data** tab.

### `outlook_kpis`

```sql
SELECT
  ROUND((SELECT r2 FROM demand_model), 3) AS model_r2,
  ROUND((SELECT AVG(ABS(error_pct)) FROM backtest), 1) AS backtest_error_pct,
  ROUND(100 * (
    (SELECT SUM(residential_million_m3) FROM winter_scenarios WHERE scenario = 'Cold') /
    (SELECT SUM(residential_million_m3) FROM winter_scenarios WHERE scenario = 'Normal') - 1), 1) AS cold_vs_normal_pct
```

Expected: `0.981`, `3.7`, `16.1`.

### `scenarios`

```sql
SELECT month_start, scenario, hdd, m3_per_customer, residential_million_m3
FROM winter_scenarios
```

### `demand_vs_weather`

```sql
SELECT
  g.month_start,
  h.avg_toronto_london_hdd AS hdd,
  g.residential_m3_per_customer AS m3_per_customer,
  ROUND(g.residential_e3m3 / 1000, 1) AS residential_million_m3,
  ROUND(g.commercial_e3m3 / 1000, 1) AS commercial_million_m3,
  ROUND(g.industrial_e3m3 / 1000, 1) AS industrial_million_m3
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
```

### `storage`

```sql
SELECT
  month_start,
  CASE WHEN MONTH(month_start) >= 11 THEN YEAR(month_start) ELSE YEAR(month_start) - 1 END AS winter_starting,
  ROUND(storage_closing_e3m3 / 1e6, 2) AS inventory_billion_m3,
  ROUND(storage_withdrawals_e3m3 / 1e6, 2) AS withdrawals_billion_m3,
  MONTH(month_start) IN (11, 12, 1, 2, 3) AS is_winter
FROM gas_monthly
```

### `backtest`

```sql
SELECT month, hdd, actual_million_m3, predicted_million_m3, error_pct
FROM backtest
```

## Pages and widgets

### Page 1: Outlook

| Widget | Dataset | Settings |
|---|---|---|
| Counter: "Weather explains" | `outlook_kpis` | `model_r2`, formatted as a percentage |
| Counter: "Backtest error" | `outlook_kpis` | `backtest_error_pct`, suffix `%` |
| Counter: "Cold winter vs. normal" | `outlook_kpis` | `cold_vs_normal_pct`, prefix `+`, suffix `%` |
| Bar: "Winter 2026-27 total by scenario" | `scenarios` | X `scenario`, Y SUM(`residential_million_m3`) |
| Line: "Monthly forecast by scenario" | `scenarios` | X `month_start`, Y `residential_million_m3`, colour `scenario` |
| Text | | "Public, province-wide monthly data (Statistics Canada, ECCC). Method demo, not a utility forecast." |

### Page 2: Weather drives demand

| Widget | Dataset | Settings |
|---|---|---|
| Scatter: "Colder month, more gas" | `demand_vs_weather` | X `hdd`, Y `m3_per_customer` |
| Line: "Demand by sector" | `demand_vs_weather` | X `month_start`, Y `residential_million_m3`, `commercial_million_m3`, `industrial_million_m3` |

### Page 3: Storage

| Widget | Dataset | Settings |
|---|---|---|
| Line: "Storage inventory" | `storage` | X `month_start`, Y `inventory_billion_m3` |
| Bar: "Winter withdrawals" | `storage` | Filter `is_winter = true`, X `winter_starting`, Y SUM(`withdrawals_billion_m3`) |

The first winter (2015) and the latest (2026) are incomplete; filter them out of the bar or add a note.

### Page 4: Model check

| Widget | Dataset | Settings |
|---|---|---|
| Bar: "Winter 2025-26, actual vs. predicted" | `backtest` | X `month`, Y `actual_million_m3` and `predicted_million_m3` |
| Table | `backtest` | All columns |

## Finish

1. Add a filter on `scenario` to page 1.
2. Turn on **Ask Genie** so viewers can ask follow-up questions.
3. Publish and share with your team.
