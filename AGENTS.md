# AGENTS.md

Guide for AI coding agents (Genie Code, Claude Code, Cursor and others) working in this repo.

## What this repo is

A one-day hackathon kit: public Ontario gas demand and weather data, Databricks notebooks, and agent skills for building a winter gas demand forecast. Participants are mostly business users working in Databricks.

## Layout

| Path | Purpose |
|---|---|
| `HACKATHON.md` | Participant brief: problem, steps, demo story |
| `DATASETS.md` | Column-by-column data guide |
| `PROMPTS.md` | Generic starter prompts for Genie One and Genie Code, for any project (no blanks to fill in). Tested on a live workspace. |
| `data/raw/` | Source files as published. Do not edit by hand. |
| `data/processed/` | Tidy Ontario CSVs, built by `scripts/build_processed.py` |
| `scripts/` | `download_raw.py` (fetch sources), `build_processed.py` (rebuild CSVs). Python standard library only. |
| `notebooks/` | `00_setup` (load to Unity Catalog), `01_explore`, `02_model_and_scenarios`, `03_next_week` (live forecast) |
| `docs/` | `genie_space.md`, `dashboard.md`: ready-to-use configs |
| `agents/skills/` | Genie Code skills, one folder per skill with a `SKILL.md` |

## Rules

1. **Simplicity first.** Prefer SQL over Python, one file over two, and deleting over adding. Participants must be able to follow every step.
2. **Never invent numbers.** Every figure in the docs and skills must come from running a query on the data. If you change data or logic, rerun the queries and update the figures.
3. **Keep it generic.** No company names or internal references. The data is province-wide public data; say so wherever forecasts are shown.
4. **Respect the data gotchas.** Per-customer values start in 2019-01; use one unit per query; `avg_toronto_london_hdd` is the default weather driver. See `agents/skills/winter-gas-data/SKILL.md`.
5. **Test on Databricks before you push.** Run the notebooks end to end, plus every SQL block in `docs/`. `03_next_week` uses live data, so check it runs and the numbers look sensible rather than matching fixed figures.
6. **Keep the licences.** Keep the StatCan and ECCC attribution in `README.md` and `DATASETS.md`.

## Where the hard-coded figures live

Update all of these after a data refresh or a logic change:

- `README.md` (R² table)
- `DATASETS.md` (ranges, row counts, examples)
- `HACKATHON.md` (demo story figures)
- `agents/skills/*/SKILL.md` (expected results)
- `docs/genie_space.md` (expected answers)
- `docs/dashboard.md` (expected KPI values)

## Refreshing the data

```bash
python3 scripts/download_raw.py
python3 scripts/build_processed.py
```

Then rerun the notebooks and update the figures listed above.
