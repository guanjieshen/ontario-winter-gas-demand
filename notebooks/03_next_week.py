# Databricks notebook source
# MAGIC %md
# MAGIC # 03 Next week: live forecast to expected demand
# MAGIC
# MAGIC Pulls the latest Environment and Climate Change Canada (ECCC) city forecasts for Toronto and London, turns them into heating degree days (HDD), and runs them through the demand model to show **expected residential gas use for the coming week**, compared with normal weather. The forecast covers today plus five days; ECCC's last forecast day has no overnight low, so it is dropped.
# MAGIC
# MAGIC | Table | What it holds |
# MAGIC |---|---|
# MAGIC | `weather_forecast` | Every forecast fetched. Each run **appends**, so you build up your own forecast history. |
# MAGIC | `demand_next_week` | Expected demand for the latest forecast, day by day, vs. normal |
# MAGIC
# MAGIC Run `00_setup` and `02_model_and_scenarios` first. This notebook needs internet access to `dd.weather.gc.ca`.
# MAGIC
# MAGIC > The model was fitted on monthly data and is applied here to daily forecasts. Treat the result as an estimate.

# COMMAND ----------

dbutils.widgets.text("catalog", "main", "Catalog")
dbutils.widgets.text("schema", "winter_gas_demand", "Schema")
spark.sql(f"USE CATALOG `{dbutils.widgets.get('catalog')}`")
spark.sql(f"USE SCHEMA `{dbutils.widgets.get('schema')}`")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Fetch the latest forecasts
# MAGIC ECCC publishes city forecasts as XML several times a day. Each day's mean temperature is estimated as (daytime high + following night's low) / 2, the same way ECCC calculates the observed daily mean. HDD = max(0, 18 − mean).

# COMMAND ----------

import re
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone

BASE_URL = "https://dd.weather.gc.ca/today/citypage_weather/ON/"
CITIES = {"Toronto": "s0000458", "London": "s0000326"}  # ECCC city page site codes


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ontario-winter-gas-demand/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def latest_file_url(site_code):
    """Return the newest English forecast file for a site, searching hour folders newest first."""
    hours = sorted(set(re.findall(r'href="(\d{2})/"', get(BASE_URL).decode())), reverse=True)
    for hour in hours:
        listing = get(f"{BASE_URL}{hour}/").decode()
        files = sorted(re.findall(rf'href="([^"]*_{site_code}_en\.xml)"', listing))
        if files:
            return f"{BASE_URL}{hour}/{files[-1]}"
    raise RuntimeError(f"No forecast file found for {site_code}")


def parse_forecast(xml_bytes, city):
    root = ET.fromstring(xml_bytes)
    group = root.find("forecastGroup")
    issue = next(d for d in group.findall("dateTime") if d.get("zone") == "UTC")
    issued_at = datetime.strptime(issue.find("timeStamp").text, "%Y%m%d%H%M%S").replace(tzinfo=timezone.utc)
    local = next(d for d in group.findall("dateTime") if d.get("zone") != "UTC")
    issue_date = date(int(local.find("year").text), int(local.find("month").text), int(local.find("day").text))

    # Walk the periods in order: a daytime period carries the high, the night after it the low.
    days, current = [], None
    for f in group.findall("forecast"):
        name = f.find("period").text  # for example "Tuesday" or "Tuesday night"
        temp = f.find("temperatures/temperature")
        value = float(temp.text) if temp is not None and temp.text else None
        if not name.endswith("night"):
            current = {"weekday": name, "high_c": value}
        elif current is not None and name == f"{current['weekday']} night":
            current["low_c"] = value
            days.append(current)
            current = None

    rows = []
    for d in days:
        # Map the weekday name to the first matching date on or after the issue date.
        offset = next(i for i in range(7) if (issue_date + timedelta(days=i)).strftime("%A") == d["weekday"])
        if d["high_c"] is None or d["low_c"] is None:
            continue
        mean_c = (d["high_c"] + d["low_c"]) / 2
        rows.append({
            "issued_at": issued_at,
            "city": city,
            "forecast_date": issue_date + timedelta(days=offset),
            "high_c": d["high_c"],
            "low_c": d["low_c"],
            "mean_c": mean_c,
            "hdd": max(0.0, 18 - mean_c),
        })
    return rows


rows = []
for city, code in CITIES.items():
    url = latest_file_url(code)
    city_rows = parse_forecast(get(url), city)
    print(f"{city}: {len(city_rows)} days from {url}")
    rows += city_rows

forecast = spark.createDataFrame(rows).selectExpr(
    "issued_at", "city", "forecast_date", "high_c", "low_c", "mean_c", "hdd", "current_timestamp() AS fetched_at")
forecast.write.mode("append").saveAsTable("weather_forecast")
spark.sql("COMMENT ON TABLE weather_forecast IS 'ECCC city forecasts for Toronto and London, one row per city per forecast day per issue. Appended on every run of notebook 03, so it builds a forecast history. HDD = max(0, 18 - (high + low) / 2)'")
display(forecast)

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Expected demand for the coming week
# MAGIC Daily use per customer = monthly base use ÷ days in the month + slope × daily HDD. "Normal" is the average daily HDD for the same dates (±3 days) in 2016 to 2025.

# COMMAND ----------

spark.sql("""
CREATE OR REPLACE TABLE demand_next_week
COMMENT 'Expected Ontario residential gas use for each day of the latest ECCC forecast, compared with normal weather for the same dates'
AS
WITH latest AS (
  SELECT forecast_date, AVG(hdd) AS hdd, MAX(issued_at) AS issued_at
  FROM weather_forecast
  WHERE issued_at = (SELECT MAX(issued_at) FROM weather_forecast)
  GROUP BY forecast_date
  HAVING COUNT(DISTINCT city) = 2              -- both Toronto and London
),
normal AS (
  SELECT l.forecast_date, AVG(w.hdd) AS normal_hdd
  FROM latest l
  JOIN weather_daily w
    ON w.city IN ('Toronto', 'London')
   AND YEAR(w.date) BETWEEN 2016 AND 2025
   AND LEAST(ABS(DAYOFYEAR(w.date) - DAYOFYEAR(l.forecast_date)),
             365 - ABS(DAYOFYEAR(w.date) - DAYOFYEAR(l.forecast_date))) <= 3
  GROUP BY l.forecast_date
),
customers AS (
  SELECT MAX_BY(residential_customers, month) AS n FROM gas_monthly
)
SELECT
  l.forecast_date,
  l.issued_at,
  ROUND(l.hdd, 1) AS hdd,
  ROUND(n.normal_hdd, 1) AS normal_hdd,
  ROUND(m.base_m3_per_customer / DAY(LAST_DAY(l.forecast_date)) + m.m3_per_customer_per_hdd * l.hdd, 2)
    AS m3_per_customer,
  ROUND((m.base_m3_per_customer / DAY(LAST_DAY(l.forecast_date)) + m.m3_per_customer_per_hdd * l.hdd)
        * c.n / 1e6, 1) AS residential_million_m3,
  ROUND((m.base_m3_per_customer / DAY(LAST_DAY(l.forecast_date)) + m.m3_per_customer_per_hdd * n.normal_hdd)
        * c.n / 1e6, 1) AS normal_million_m3
FROM latest l
JOIN normal n USING (forecast_date)
CROSS JOIN demand_model m
CROSS JOIN customers c
""")

display(spark.sql("""
SELECT *, ROUND(100 * (residential_million_m3 / normal_million_m3 - 1), 1) AS vs_normal_pct
FROM demand_next_week ORDER BY forecast_date
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. The week in one line

# COMMAND ----------

display(spark.sql("""
SELECT
  MIN(forecast_date) AS from_date,
  MAX(forecast_date) AS to_date,
  ROUND(SUM(residential_million_m3), 0) AS expected_million_m3,
  ROUND(SUM(normal_million_m3), 0) AS normal_million_m3,
  ROUND(100 * (SUM(residential_million_m3) / SUM(normal_million_m3) - 1), 1) AS vs_normal_pct
FROM demand_next_week
"""))
