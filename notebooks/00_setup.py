# Databricks notebook source
# MAGIC %md
# MAGIC # 00 Setup: load the data into Unity Catalog
# MAGIC
# MAGIC Loads the three processed CSVs from this repo into Delta tables, with table and column descriptions so Genie understands them.
# MAGIC
# MAGIC | Table | From |
# MAGIC |---|---|
# MAGIC | `gas_monthly` | `data/processed/ontario_gas_monthly.csv` |
# MAGIC | `hdd_monthly` | `data/processed/ontario_hdd_monthly.csv` |
# MAGIC | `weather_daily` | `data/processed/ontario_weather_daily.csv` |
# MAGIC
# MAGIC **How to run:** clone this repo as a Git folder, set the catalog and schema widgets above, then **Run all**. Serverless compute works. Safe to re-run; tables are overwritten.

# COMMAND ----------

dbutils.widgets.text("catalog", "main", "Catalog")
dbutils.widgets.text("schema", "winter_gas_demand", "Schema")
catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS `{catalog}`.`{schema}`")
print(f"Loading into {catalog}.{schema}")

# COMMAND ----------

import os

import pandas as pd
from pyspark.sql import functions as F

DATA_DIR = os.path.abspath(os.path.join(os.getcwd(), "..", "data", "processed"))

STRING_COLUMNS = {"month", "city", "station_name", "climate_id", "hdd_flag"}
INTEGER_SUFFIXES = ("_customers", "_days_reported")


def load_csv(file_name):
    """Read a CSV as strings, then cast: blanks become NULL, numbers become DOUBLE or BIGINT."""
    pdf = pd.read_csv(os.path.join(DATA_DIR, file_name), dtype=str, keep_default_na=False)
    df = spark.createDataFrame(pdf)
    cols = []
    for c in df.columns:
        value = F.when(F.col(c) == "", None).otherwise(F.col(c))
        if c in STRING_COLUMNS:
            cols.append(value.alias(c))
        elif c == "date":
            cols.append(F.to_date(value).alias(c))
        elif c.endswith(INTEGER_SUFFIXES):
            cols.append(value.cast("double").cast("bigint").alias(c))
        else:
            cols.append(value.cast("double").alias(c))
    df = df.select(cols)
    if "month" in df.columns:  # add a real DATE next to the YYYY-MM key
        df = df.withColumn("month_start", F.to_date(F.concat("month", F.lit("-01"))))
        df = df.select("month", "month_start", *[c for c in df.columns if c not in ("month", "month_start")])
    return df


def save(df, table, table_comment, column_comments):
    name = f"`{catalog}`.`{schema}`.`{table}`"
    df.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable(name)
    spark.sql(f"COMMENT ON TABLE {name} IS '{table_comment}'")
    for col, comment in column_comments.items():
        if col in df.columns:
            spark.sql(f"ALTER TABLE {name} ALTER COLUMN `{col}` COMMENT '{comment}'")
    print(f"{name}: {spark.table(name).count()} rows")

# COMMAND ----------

# MAGIC %md
# MAGIC ## gas_monthly

# COMMAND ----------

SERIES = {
    "residential": "Natural gas consumed by Ontario homes",
    "commercial": "Natural gas consumed by Ontario commercial customers (businesses, offices, schools)",
    "industrial": "Natural gas consumed by Ontario industrial customers",
    "total_deliveries": "Total natural gas delivered to all Ontario consumers",
    "storage_opening": "Natural gas in Ontario underground storage at the start of the month",
    "storage_closing": "Natural gas in Ontario underground storage at the end of the month",
    "storage_injections": "Natural gas injected into Ontario storage during the month",
    "storage_withdrawals": "Natural gas withdrawn from Ontario storage during the month",
    "storage_change": "Net change in Ontario storage inventory during the month; negative means a drawdown",
}
UNITS = {
    "e3m3": "in thousands of cubic metres (10^3 m3)",
    "e3gj": "in thousands of gigajoules",
    "k_cad": "value in thousands of Canadian dollars",
}

gas_comments = {
    "month": "Reference month as YYYY-MM. Join key to hdd_monthly",
    "month_start": "First day of the reference month as a DATE",
}
for prefix, what in SERIES.items():
    for suffix, unit in UNITS.items():
        gas_comments[f"{prefix}_{suffix}"] = f"{what}, {unit}"
for sector in ("residential", "commercial", "industrial", "total_deliveries"):
    label = "all" if sector == "total_deliveries" else sector
    gas_comments[f"{sector}_customers"] = (
        f"Number of {label} natural gas customers in Ontario. "
        "Counts before 2019-01 use a different StatCan method and are not comparable"
    )
for sector in ("residential", "commercial", "industrial"):
    gas_comments[f"{sector}_m3_per_customer"] = (
        f"Average {sector} use per customer in cubic metres for the month "
        "(volume / customers). Only populated from 2019-01"
    )

save(
    load_csv("ontario_gas_monthly.csv"),
    "gas_monthly",
    "Ontario natural gas consumption by sector and underground storage, monthly, Jan 2016 onward. "
    "Source: Statistics Canada table 25-10-0086-01 (Ontario). Province-wide, all utilities. "
    "Each measure appears in several units; use one unit suffix per query.",
    gas_comments,
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## hdd_monthly

# COMMAND ----------

hdd_comments = {
    "month": "Reference month as YYYY-MM. Join key to gas_monthly",
    "month_start": "First day of the reference month as a DATE",
    "avg_toronto_london_hdd": "Average monthly heating degree days of Toronto and London. Recommended weather driver for modelling; gap-free",
    "avg_4city_hdd": "Average monthly heating degree days of Toronto, London, Sarnia and Windsor; NULL unless all four are complete",
}
for city in ("toronto", "london", "sarnia", "windsor"):
    hdd_comments[f"{city}_hdd"] = (
        f"Monthly heating degree days (18 C base) for {city.title()}; NULL if fewer than 25 days were reported"
    )
    hdd_comments[f"{city}_days_reported"] = f"Days with heating degree day data for {city.title()} that month"

save(
    load_csv("ontario_hdd_monthly.csv"),
    "hdd_monthly",
    "Monthly heating degree days (HDD, 18 C base) for four southwestern Ontario cities, Jan 2016 onward. "
    "Built from Environment and Climate Change Canada daily observations. More HDD means colder weather and more gas heating.",
    hdd_comments,
)

# COMMAND ----------

# MAGIC %md
# MAGIC ## weather_daily

# COMMAND ----------

save(
    load_csv("ontario_weather_daily.csv"),
    "weather_daily",
    "Daily weather observations for Toronto, London, Sarnia and Windsor weather stations, Jan 2016 onward. "
    "Source: Environment and Climate Change Canada. One row per station per day.",
    {
        "date": "Observation date",
        "city": "City: Toronto, London, Sarnia or Windsor. Windsor combines two stations; filter on city, not station_name",
        "station_name": "ECCC weather station name",
        "climate_id": "ECCC climate station ID",
        "max_temp_c": "Daily maximum temperature in degrees Celsius",
        "min_temp_c": "Daily minimum temperature in degrees Celsius",
        "mean_temp_c": "Daily mean temperature in degrees Celsius",
        "hdd": "Heating degree days for the day: max(0, 18 - mean temperature)",
        "hdd_flag": "ECCC quality flag for hdd. E means estimated; NULL means normal",
        "total_precip_mm": "Total precipitation in millimetres; often NULL",
        "snow_on_ground_cm": "Snow depth in centimetres; mostly NULL",
    },
)
