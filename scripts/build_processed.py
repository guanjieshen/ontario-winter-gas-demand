"""Build tidy Ontario CSVs in data/processed/ from the raw files in data/raw/.

Outputs:
  ontario_gas_monthly.csv    one row per month: demand by sector, customers, storage
  ontario_weather_daily.csv  one row per station per day: temperatures and HDD
  ontario_hdd_monthly.csv    one row per month: HDD per city plus a 4-city average

Usage:
  python3 scripts/build_processed.py [repo_root]

Standard library only.
"""

import calendar
import csv
import sys
from collections import defaultdict
from pathlib import Path

from download_raw import STATIONS

# StatCan "Supply and disposition" member -> output column prefix
GAS_SERIES = {
    "Residential consumption": "residential",
    "Commercial consumption": "commercial",
    "Industrial consumption": "industrial",
    "Total deliveries to consumers, disposition": "total_deliveries",
    "Opening inventory, storage": "storage_opening",
    "Closing  inventory, storage": "storage_closing",  # double space is in the source
    "Injections to storage, disposition": "storage_injections",
    "Withdrawals from storage, supply": "storage_withdrawals",
    "Inventory change, storage": "storage_change",
}

# StatCan UOM -> output column suffix
UOMS = {
    "Cubic metres": "e3m3",  # thousands of cubic metres
    "Gigajoules": "e3gj",  # thousands of gigajoules
    "Canadian dollars": "k_cad",  # thousands of dollars
    "Customers": "customers",
}

CUSTOMER_SECTORS = ["residential", "commercial", "industrial"]
CUSTOMER_COUNTS_VALID_FROM = "2019-01"
CITIES = ["Toronto", "London", "Sarnia", "Windsor"]

# A month's HDD is kept only if at least this many days were reported; missing days
# are then filled in proportionally. Below this the month is left blank.
MIN_DAYS_FOR_MONTH = 25


def read_csv(path: Path) -> list[dict]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("latin-1")
    return list(csv.DictReader(text.splitlines()))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {path} ({len(rows)} rows)")


def build_gas_monthly(raw_dir: Path, out_dir: Path) -> None:
    months: dict[str, dict] = defaultdict(dict)
    columns: set[str] = set()
    for row in read_csv(raw_dir / "statcan" / "25100086.csv"):
        if row["GEO"] != "Ontario":
            continue
        prefix = GAS_SERIES.get(row["Supply and disposition"])
        suffix = UOMS.get(row["UOM"])
        if not prefix or not suffix or row["VALUE"] == "":
            continue
        col = f"{prefix}_{suffix}"
        columns.add(col)
        months[row["REF_DATE"]][col] = float(row["VALUE"])

    # StatCan note 8: customer counts were not collected Jan 2016 - Dec 2018 and use a
    # different method, so per-customer use is only comparable from 2019 onward.
    for month, values in months.items():
        if month < CUSTOMER_COUNTS_VALID_FROM:
            continue
        for sector in CUSTOMER_SECTORS:
            volume = values.get(f"{sector}_e3m3")
            customers = values.get(f"{sector}_customers")
            if volume is not None and customers:
                values[f"{sector}_m3_per_customer"] = round(volume * 1000 / customers, 2)

    order = [f"{p}_{s}" for p in GAS_SERIES.values() for s in UOMS.values()
             if f"{p}_{s}" in columns]
    derived = [f"{s}_m3_per_customer" for s in CUSTOMER_SECTORS]
    fieldnames = ["month"] + order + derived
    rows = [{"month": m, **months[m]} for m in sorted(months)]
    write_csv(out_dir / "ontario_gas_monthly.csv", fieldnames, rows)


def build_weather(raw_dir: Path, out_dir: Path) -> None:
    city_by_id = {climate_id: city for city, climate_id, _, _ in STATIONS}
    daily: list[dict] = []
    for path in sorted((raw_dir / "eccc").glob("climate_daily_ON_*_P1D.csv")):
        for row in read_csv(path):
            col = {k.split(" (")[0]: v for k, v in row.items()}  # drop "(°C)" units from names
            if col["Mean Temp"] == "" and col["Heat Deg Days"] == "":
                continue  # future-dated or empty rows
            daily.append({
                "date": col["Date/Time"],
                "city": city_by_id.get(col["Climate ID"], ""),
                "station_name": col["Station Name"],
                "climate_id": col["Climate ID"],
                "max_temp_c": col["Max Temp"],
                "min_temp_c": col["Min Temp"],
                "mean_temp_c": col["Mean Temp"],
                "hdd": col["Heat Deg Days"],
                "hdd_flag": col["Heat Deg Days Flag"],
                "total_precip_mm": col["Total Precip"],
                "snow_on_ground_cm": col["Snow on Grnd"],
            })
    daily.sort(key=lambda r: (r["date"], r["city"]))
    write_csv(out_dir / "ontario_weather_daily.csv", list(daily[0].keys()), daily)

    totals: dict[tuple[str, str], list[float]] = defaultdict(list)
    for r in daily:
        if r["hdd"] != "":
            totals[(r["date"][:7], r["city"])].append(float(r["hdd"]))

    rows = []
    for month in sorted({m for m, _ in totals}):
        year, mon = int(month[:4]), int(month[5:7])
        days_in_month = calendar.monthrange(year, mon)[1]
        row = {"month": month}
        complete = []
        for city in CITIES:
            vals = totals.get((month, city), [])
            row[f"{city.lower()}_days_reported"] = len(vals)
            if len(vals) >= MIN_DAYS_FOR_MONTH:
                hdd = sum(vals) * days_in_month / len(vals)
                row[f"{city.lower()}_hdd"] = round(hdd, 1)
                complete.append(hdd)
        if len(complete) == len(CITIES):
            row["avg_4city_hdd"] = round(sum(complete) / len(complete), 1)
        if row.get("toronto_hdd") is not None and row.get("london_hdd") is not None:
            row["avg_toronto_london_hdd"] = round((row["toronto_hdd"] + row["london_hdd"]) / 2, 1)
        rows.append(row)

    fieldnames = (["month"] + [f"{c.lower()}_hdd" for c in CITIES]
                  + ["avg_toronto_london_hdd", "avg_4city_hdd"]
                  + [f"{c.lower()}_days_reported" for c in CITIES])
    write_csv(out_dir / "ontario_hdd_monthly.csv", fieldnames, rows)


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    raw_dir, out_dir = root / "data" / "raw", root / "data" / "processed"
    build_gas_monthly(raw_dir, out_dir)
    build_weather(raw_dir, out_dir)


if __name__ == "__main__":
    main()
