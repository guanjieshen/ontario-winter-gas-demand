-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 02 Model and scenarios: forecast the coming winter
-- MAGIC
-- MAGIC 1. **Model.** Fit residential use per customer against heating degree days (HDD).
-- MAGIC 2. **Backtest.** Train on earlier winters, then predict winter 2025-26 and compare with what actually happened.
-- MAGIC 3. **Scenarios.** Forecast winter 2026-27 (Nov to Mar) for a normal, cold, mild and "20% colder" winter.
-- MAGIC
-- MAGIC Results are saved as tables in your schema, ready for a dashboard and a Genie space. Run `00_setup` first.
-- MAGIC
-- MAGIC > This is a method demo on province-wide monthly data. The same steps work on a utility's own daily throughput.

-- COMMAND ----------

CREATE WIDGET TEXT catalog DEFAULT 'main';
CREATE WIDGET TEXT schema DEFAULT 'winter_gas_demand';

-- COMMAND ----------

USE CATALOG IDENTIFIER(:catalog);
USE SCHEMA IDENTIFIER(:schema);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 1. Model
-- MAGIC `m3 per customer = base + slope x HDD`. Customer counts are only comparable from 2019, so the model uses 2019 onward.

-- COMMAND ----------

CREATE OR REPLACE TABLE demand_model
COMMENT 'Linear model of Ontario residential gas use per customer (m3) against monthly heating degree days, fitted on 2019 onward'
AS
SELECT
  'all months from 2019-01' AS trained_on,
  COUNT(*) AS months,
  REGR_INTERCEPT(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS base_m3_per_customer,
  REGR_SLOPE(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS m3_per_customer_per_hdd,
  REGR_R2(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS r2
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE g.residential_m3_per_customer IS NOT NULL;

SELECT * FROM demand_model;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Backtest on winter 2025-26
-- MAGIC Train only on months before Nov 2025, then predict Nov 2025 to Mar 2026 from the actual weather. `error_pct` shows how far off the forecast was.

-- COMMAND ----------

CREATE OR REPLACE TABLE backtest
COMMENT 'Backtest: model trained on months before 2025-11, used to predict Ontario residential gas use for Nov 2025 to Mar 2026 from actual HDD'
AS
WITH model AS (
  SELECT
    REGR_INTERCEPT(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS a,
    REGR_SLOPE(g.residential_m3_per_customer, h.avg_toronto_london_hdd) AS b
  FROM gas_monthly g
  JOIN hdd_monthly h USING (month)
  WHERE g.residential_m3_per_customer IS NOT NULL AND g.month < '2025-11'
)
SELECT
  g.month,
  h.avg_toronto_london_hdd AS hdd,
  ROUND(g.residential_e3m3 / 1000, 1) AS actual_million_m3,
  ROUND((m.a + m.b * h.avg_toronto_london_hdd) * g.residential_customers / 1e6, 1) AS predicted_million_m3,
  ROUND(100 * ((m.a + m.b * h.avg_toronto_london_hdd) * g.residential_customers / 1000 - g.residential_e3m3)
        / g.residential_e3m3, 1) AS error_pct
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
CROSS JOIN model m
WHERE g.month BETWEEN '2025-11' AND '2026-03';

SELECT *, ROUND(AVG(ABS(error_pct)) OVER (), 1) AS mean_abs_error_pct FROM backtest ORDER BY month;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. Weather scenarios for winter 2026-27
-- MAGIC For each winter month, the scenarios use the HDD observed in past years (2016 to 2025):
-- MAGIC
-- MAGIC | Scenario | HDD used |
-- MAGIC |---|---|
-- MAGIC | Normal | Average for that month |
-- MAGIC | Cold | Coldest year on record for that month |
-- MAGIC | Mild | Mildest year on record for that month |
-- MAGIC | 20% colder | Normal x 1.2 |
-- MAGIC
-- MAGIC The customer count is held at the latest month available.

-- COMMAND ----------

CREATE OR REPLACE TABLE winter_scenarios
COMMENT 'Forecast Ontario residential gas use for winter 2026-27 (Nov to Mar) under normal, cold, mild and 20 percent colder weather scenarios'
AS
WITH normals AS (
  SELECT
    MONTH(month_start) AS month_num,
    AVG(avg_toronto_london_hdd) AS normal_hdd,
    MAX(avg_toronto_london_hdd) AS cold_hdd,
    MIN(avg_toronto_london_hdd) AS mild_hdd
  FROM hdd_monthly
  WHERE YEAR(month_start) BETWEEN 2016 AND 2025
  GROUP BY 1
),
scenarios AS (
  SELECT month_num, 'Normal' AS scenario, normal_hdd AS hdd FROM normals
  UNION ALL SELECT month_num, 'Cold', cold_hdd FROM normals
  UNION ALL SELECT month_num, 'Mild', mild_hdd FROM normals
  UNION ALL SELECT month_num, '20% colder', normal_hdd * 1.2 FROM normals
),
customers AS (
  SELECT MAX_BY(residential_customers, month) AS residential_customers FROM gas_monthly
)
SELECT
  MAKE_DATE(CASE WHEN s.month_num >= 11 THEN 2026 ELSE 2027 END, s.month_num, 1) AS month_start,
  s.scenario,
  ROUND(s.hdd, 1) AS hdd,
  ROUND(m.base_m3_per_customer + m.m3_per_customer_per_hdd * s.hdd, 1) AS m3_per_customer,
  ROUND((m.base_m3_per_customer + m.m3_per_customer_per_hdd * s.hdd) * c.residential_customers / 1e6, 1)
    AS residential_million_m3
FROM scenarios s
CROSS JOIN demand_model m
CROSS JOIN customers c
WHERE s.month_num IN (11, 12, 1, 2, 3);

SELECT * FROM winter_scenarios ORDER BY scenario, month_start;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4. Winter totals by scenario
-- MAGIC How much more gas homes need in a cold winter than in a normal one.

-- COMMAND ----------

WITH totals AS (
  SELECT scenario, SUM(residential_million_m3) AS total
  FROM winter_scenarios
  GROUP BY scenario
)
SELECT
  scenario,
  ROUND(total, 0) AS winter_total_million_m3,
  ROUND(total - MAX(total) FILTER (WHERE scenario = 'Normal') OVER (), 0) AS vs_normal_million_m3,
  ROUND(100 * (total / MAX(total) FILTER (WHERE scenario = 'Normal') OVER () - 1), 1) AS vs_normal_pct
FROM totals
ORDER BY total DESC;
