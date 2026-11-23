---
name: winter-genie-space
description: Create and tune a Genie space ("Winter Gas Demand Assistant") over the Ontario winter gas demand tables. Use when the user wants a Genie agent or space, needs Genie instructions or example questions, or a Genie answer is wrong and needs fixing.
---

# Winter gas Genie space

Requires the tables from notebooks `00_setup` and `02_model_and_scenarios`.

The ready-to-paste instructions, example SQL and test questions are in `docs/genie_space.md` in the repo root.

## Steps

1. Create a Genie space named **Winter Gas Demand Assistant**.
2. Add tables: `gas_monthly`, `hdd_monthly`, `winter_scenarios`, `backtest`, `demand_model`. Leave `weather_daily` out at first; add it only if users ask daily questions.
3. Paste the **General instructions** from `docs/genie_space.md`.
4. Add the **example SQL queries** from the same file.
5. Ask every **test question** and compare with the expected answer. Fix wrong answers by improving instructions or adding an example query, not by editing the data.

## Tuning tips

- If Genie mixes units, add an instruction naming the exact column to use (for example `residential_e3m3`).
- If Genie uses per-customer values before 2019, restate that `*_m3_per_customer` starts in 2019-01.
- If Genie picks the wrong HDD column, restate that `avg_toronto_london_hdd` is the default.
- Table and column comments are set by `00_setup`; improve those too, since Genie reads them.
