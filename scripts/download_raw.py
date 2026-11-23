"""Download the raw public datasets into data/raw/.

Sources:
  - Statistics Canada table 25-10-0086-01, natural gas supply and disposition, monthly
  - Environment and Climate Change Canada (ECCC) daily climate observations, MSC Datamart

Usage:
  python3 scripts/download_raw.py [repo_root]

Standard library only. Safe to re-run; existing files are overwritten.
"""

import io
import sys
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

STATCAN_ZIP_URL = "https://www150.statcan.gc.ca/n1/tbl/csv/25100086-eng.zip"

ECCC_URL = (
    "https://dd.weather.gc.ca/today/climate/observations/daily/csv/ON/"
    "climate_daily_ON_{climate_id}_{year}_P1D.csv"
)

FIRST_YEAR = 2016  # first year in the StatCan table
LAST_YEAR = 2026

# (city, climate_id, first_year, last_year). Windsor is stitched from two stations
# because no single Windsor station publishes daily files for the whole period.
STATIONS = [
    ("Toronto", "6158731", FIRST_YEAR, LAST_YEAR),  # TORONTO INTL A (Pearson)
    ("London", "6144473", FIRST_YEAR, LAST_YEAR),  # LONDON A
    ("Sarnia", "6127510", FIRST_YEAR, LAST_YEAR),  # SARNIA
    ("Windsor", "6139520", FIRST_YEAR, 2017),  # WINDSOR RIVERSIDE
    ("Windsor", "6139530", 2018, LAST_YEAR),  # WINDSOR A
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ontario-winter-gas-demand/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def download_statcan(raw_dir: Path) -> None:
    out_dir = raw_dir / "statcan"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"StatCan: {STATCAN_ZIP_URL}")
    with zipfile.ZipFile(io.BytesIO(fetch(STATCAN_ZIP_URL))) as zf:
        for name in zf.namelist():
            # Extract by base name only, so archive paths cannot escape out_dir.
            target = out_dir / Path(name).name
            target.write_bytes(zf.read(name))
            print(f"  wrote {target}")


def download_eccc(raw_dir: Path) -> None:
    out_dir = raw_dir / "eccc"
    out_dir.mkdir(parents=True, exist_ok=True)
    for city, climate_id, first, last in STATIONS:
        for year in range(first, last + 1):
            url = ECCC_URL.format(climate_id=climate_id, year=year)
            target = out_dir / Path(url).name
            try:
                target.write_bytes(fetch(url))
                print(f"  {city} {climate_id} {year}: ok")
            except urllib.error.HTTPError as err:
                print(f"  {city} {climate_id} {year}: HTTP {err.code}, skipped")


def main() -> None:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    raw_dir = root / "data" / "raw"
    download_statcan(raw_dir)
    print("ECCC daily climate:")
    download_eccc(raw_dir)


if __name__ == "__main__":
    main()
