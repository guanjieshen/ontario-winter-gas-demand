# Ontario Winter Gas Demand

![Databricks](https://img.shields.io/badge/Databricks-hackathon%20kit-FF3621)
![Data: Statistics Canada](https://img.shields.io/badge/data-Statistics%20Canada-red)
![Data: ECCC](https://img.shields.io/badge/data-ECCC%20Climate-blue)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

## Overview

A one-day **Databricks hackathon kit** for forecasting **Ontario natural gas demand from weather**. It pairs monthly Ontario gas consumption and storage from Statistics Canada with daily temperatures and heating degree days (HDD) from Environment and Climate Change Canada.

Teams load the data into Unity Catalog, model demand against cold weather, backtest the model, forecast the coming winter under several weather scenarios, and present it through a Genie space and an AI/BI dashboard.

**How strong is the weather signal?** A straight-line fit on monthly HDD alone gives:

| Target | Period | Months | R² |
|---|---|---|---|
| Residential use per customer (m³) | 2019-01 to 2026-09 | 93 | 0.98 |
| Residential volume (10³ m³) | 2016-01 to 2026-09 | 129 | 0.96 |
| Total deliveries to consumers (10³ m³) | 2016-01 to 2026-09 | 129 | 0.88 |

> [!NOTE]
> This is public, province-wide, monthly data. It shows the **method**. For an operational forecast, apply the same steps to a utility's own daily or hourly throughput.

## Start here

| If you are | Read |
|---|---|
| A participant | **[HACKATHON.md](HACKATHON.md)**: the problem, step-by-step build and demo story |
| Not sure what to ask | **[PROMPTS.md](PROMPTS.md)**: starter prompts to copy into Genie Code |
| Looking for column definitions | **[DATASETS.md](DATASETS.md)**: every dataset and column, with gotchas |
| Building the Genie space | **[docs/genie_space.md](docs/genie_space.md)**: instructions, example SQL, test questions |
| Building the dashboard | **[docs/dashboard.md](docs/dashboard.md)**: datasets and widgets |
| An AI agent working on this repo | **[AGENTS.md](AGENTS.md)** |

## Quick start on Databricks

1. **Clone** this repo as a Git folder: **Workspace → Create → Git folder**, paste the repo URL.
2. **Load** the data: open `notebooks/00_setup`, set the `catalog` and `schema` widgets, click **Run all**.
3. **Explore and model:** run `notebooks/01_explore`, then `notebooks/02_model_and_scenarios` with the same widgets.
4. **Live forecast (optional):** run `notebooks/03_next_week` to turn this week's ECCC forecast into expected demand. Needs internet access to `dd.weather.gc.ca`.
5. **Add the skills to Genie Code:** add the `agents/skills` folder with **Add from workspace folder**, then start a new chat.

Serverless compute works for all notebooks. The SQL notebooks also run on a SQL warehouse.

## Repository layout

| Path | What it holds |
|---|---|
| `notebooks/` | `00_setup` (load into Unity Catalog), `01_explore`, `02_model_and_scenarios`, `03_next_week` (live forecast) |
| `agents/skills/` | Genie Code skills (see below) |
| `docs/` | Genie space and dashboard specs |
| `data/processed/` | Tidy Ontario CSVs that the setup notebook loads |
| `data/raw/` | Source files exactly as published |
| `scripts/` | `download_raw.py` and `build_processed.py` to refresh the data (Python standard library only) |

## Agent skills

| Skill | Use it to |
|---|---|
| `winter-gas-data` | Load the tables and explain columns, units and gotchas |
| `demand-weather-model` | Fit, explain and backtest the demand vs. weather model |
| `winter-scenarios` | Forecast normal, cold and mild winters, the coming week from the live forecast, compare with `ai_forecast`, and give a storage outlook |
| `winter-dashboard` | Build the Ontario Winter Gas Outlook dashboard |
| `winter-genie-space` | Create and tune the Winter Gas Demand Assistant Genie space |

Each skill is a folder with a `SKILL.md` and works with Genie Code and other agents that support the [Agent Skills](https://agentskills.io) format.

> [!TIP]
> To make the skills available to everyone in a workspace, an admin can copy the skill folders into `/Workspace/.assistant/skills/`.

## Refresh the data

```bash
python3 scripts/download_raw.py
python3 scripts/build_processed.py
```

StatCan publishes monthly, about two months behind. After a refresh, rerun the notebooks and update the expected figures in the docs (see [AGENTS.md](AGENTS.md)).

## Sources and licences

| Dataset | Source | Licence |
|---|---|---|
| Natural gas supply and disposition, monthly (table 25-10-0086-01) | [Statistics Canada](https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=2510008601) | [Statistics Canada Open Licence](https://www.statcan.gc.ca/en/terms-conditions/open-licence) |
| Daily climate observations | [ECCC MSC Datamart](https://dd.weather.gc.ca/today/climate/observations/daily/csv/ON/) | [ECCC Data Servers End-use Licence](https://eccc-msc.github.io/open-data/licence/readme_en/) |

**Attribution:**

- Source: Statistics Canada, Table 25-10-0086-01, Natural gas supply and disposition, monthly. Reproduced and distributed on an "as is" basis with the permission of Statistics Canada.
- Data Source: Environment and Climate Change Canada.

The processed files are derived from these sources by the scripts in this repo. This repo is not endorsed by Statistics Canada or ECCC.
