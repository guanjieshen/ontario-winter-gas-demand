-- Databricks notebook source
-- MAGIC %md
-- MAGIC # 01 Explore: how weather drives Ontario gas demand
-- MAGIC
-- MAGIC Run `00_setup` first. Set the catalog and schema widgets to where the tables live, then run each cell and look at the result. Use the chart button on any result to plot it.

-- COMMAND ----------

CREATE WIDGET TEXT catalog DEFAULT 'main';
CREATE WIDGET TEXT schema DEFAULT 'winter_gas_demand';

-- COMMAND ----------

USE CATALOG IDENTIFIER(:catalog);
USE SCHEMA IDENTIFIER(:schema);

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 1. The seasonal cycle
-- MAGIC Residential, commercial and industrial use each month, in millions of cubic metres. Homes and businesses swing with the seasons; industry stays fairly flat.

-- COMMAND ----------

SELECT
  month_start,
  ROUND(residential_e3m3 / 1000, 1) AS residential_million_m3,
  ROUND(commercial_e3m3 / 1000, 1) AS commercial_million_m3,
  ROUND(industrial_e3m3 / 1000, 1) AS industrial_million_m3
FROM gas_monthly
ORDER BY month_start;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 2. Cold vs. demand
-- MAGIC Each dot is a month. Plot `hdd` (x) against `m3_per_customer` (y) as a scatter chart: it is close to a straight line.

-- COMMAND ----------

SELECT
  g.month,
  h.avg_toronto_london_hdd AS hdd,
  g.residential_m3_per_customer AS m3_per_customer
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE g.residential_m3_per_customer IS NOT NULL
ORDER BY g.month;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 3. How strong is the relationship?
-- MAGIC `r2` is the share of month-to-month variation that weather alone explains (1.0 = all of it).

-- COMMAND ----------

SELECT
  COUNT(*) AS months,
  ROUND(REGR_R2(g.residential_m3_per_customer, h.avg_toronto_london_hdd), 3) AS r2,
  ROUND(REGR_SLOPE(g.residential_m3_per_customer, h.avg_toronto_london_hdd), 3) AS m3_per_customer_per_hdd,
  ROUND(REGR_INTERCEPT(g.residential_m3_per_customer, h.avg_toronto_london_hdd), 1) AS base_m3_per_customer
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE g.residential_m3_per_customer IS NOT NULL;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 4. Januaries compared
-- MAGIC How cold each January was, and what Ontario homes used.

-- COMMAND ----------

SELECT
  g.month,
  h.avg_toronto_london_hdd AS hdd,
  ROUND(g.residential_e3m3 / 1000, 1) AS residential_million_m3,
  g.residential_m3_per_customer AS m3_per_customer
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE MONTH(g.month_start) = 1
ORDER BY hdd DESC;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 5. The storage cycle
-- MAGIC Storage fills from spring to fall and drains through the winter. Inventory is in billions of cubic metres.

-- COMMAND ----------

SELECT
  month_start,
  ROUND(storage_closing_e3m3 / 1e6, 2) AS inventory_billion_m3,
  ROUND(storage_injections_e3m3 / 1e6, 2) AS injections_billion_m3,
  ROUND(storage_withdrawals_e3m3 / 1e6, 2) AS withdrawals_billion_m3
FROM gas_monthly
ORDER BY month_start;

-- COMMAND ----------

-- MAGIC %md
-- MAGIC ## 6. How low does storage get each winter?
-- MAGIC The lowest month-end inventory in each heating season (November to March).

-- COMMAND ----------

SELECT
  CASE WHEN MONTH(month_start) >= 11 THEN YEAR(month_start) ELSE YEAR(month_start) - 1 END AS winter_starting,
  MIN_BY(month, storage_closing_e3m3) AS lowest_month,
  ROUND(MIN(storage_closing_e3m3) / 1e6, 2) AS lowest_inventory_billion_m3,
  ROUND(SUM(storage_withdrawals_e3m3) / 1e6, 2) AS winter_withdrawals_billion_m3
FROM gas_monthly
WHERE MONTH(month_start) IN (11, 12, 1, 2, 3)
GROUP BY 1
HAVING COUNT(*) = 5 -- complete winters only
ORDER BY 1;
