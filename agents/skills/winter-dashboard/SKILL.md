---
name: winter-dashboard
description: Build the "Ontario Winter Gas Outlook" AI/BI (Lakeview) dashboard from the winter gas demand tables. Use when the user wants a dashboard, charts or a visual summary of gas demand, weather, storage, the backtest or winter scenarios.
---

# Winter gas outlook dashboard

Requires `gas_monthly`, `hdd_monthly`, `demand_model`, `backtest` and `winter_scenarios` (run notebooks `00_setup` and `02_model_and_scenarios`).

The full spec, with every dataset query and widget, is in `docs/dashboard.md` in the repo root. Follow it page by page.

## Layout

| Page | Widgets |
|---|---|
| **Outlook** | Counters: model R², backtest error, cold vs. normal %. Bar: winter total by scenario. Line: monthly forecast by scenario. |
| **Weather drives demand** | Scatter: HDD vs. m³ per customer. Line: demand by sector over time. |
| **Storage** | Line: month-end inventory. Bar: winter withdrawals by winter. |
| **Model check** | Bar or line: backtest actual vs. predicted. Table: backtest with error %. |

## Steps

1. Create a new dashboard. Add each dataset from `docs/dashboard.md` on the **Data** tab, using the user's catalog and schema.
2. Build the widgets page by page as in the table above.
3. Add a global filter on `scenario` for the Outlook page.
4. Turn on **Ask Genie** in the dashboard settings so viewers can ask follow-up questions.
5. Publish.

## Pitfalls

- Show volumes in million m³ (`_e3m3 / 1000`) or billion m³ for storage (`_e3m3 / 1e6`); raw thousands are hard to read.
- Add a text widget: "Public, province-wide monthly data. Method demo, not a utility forecast."
