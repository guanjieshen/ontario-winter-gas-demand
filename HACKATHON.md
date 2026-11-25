# Hackathon track: Winter Gas Demand Outlook

**Forecast how much gas Ontario will need this winter, and what happens if it turns cold.**

Teams finish the day with a demand model they can explain, a backtest that shows it works, a winter scenario forecast, a Genie space and a dashboard. Everything runs on public data on Databricks.

## The business problem

Gas demand for heating follows the weather. A cold January can push demand far above plan: more gas has to be bought or drawn from storage, and costs and operations come under pressure. Planners need to answer three questions before every winter:

1. **How much does demand rise when it gets colder?**
2. **What should we expect this winter?**
3. **What if it's a cold one, and do we have enough in storage?**

## Value

| Value | How this track shows it |
|---|---|
| **Better winter planning** | A forecast for normal, cold and mild winters, made before the winter starts |
| **Earlier risk warning** | A cold-winter scenario shows the extra demand, and how it compares with past storage draws |
| **Trusted numbers** | A backtest against last winter, and one governed dataset behind the dashboard and Genie |
| **A path to production** | The same steps work on a utility's own daily throughput data |

> [!NOTE]
> The data is public and province-wide (Statistics Canada and Environment and Climate Change Canada). It proves the method, not a specific utility's forecast.

## The data

| Table | What it contains |
|---|---|
| `gas_monthly` | Ontario gas use by homes, businesses and industry, customer counts, and underground storage, monthly from Jan 2016 |
| `hdd_monthly` | Monthly heating degree days (how cold it was) for Toronto, London, Sarnia and Windsor |
| `weather_daily` | Daily temperatures and heating degree days for the same four cities |

Full column guide: [DATASETS.md](DATASETS.md).

## Before you start

1. **Clone the repo** into your workspace as a Git folder: **Workspace → Create → Git folder**, then paste the repo URL.
2. **Load the data.** Open `notebooks/00_setup`, set `catalog` and `schema` to your team schema, and click **Run all**. Your facilitator may have done this already; if so, use their shared schema.
3. **Turn on the skills (optional, recommended).** In Genie Code, add the repo's `agents/skills` folder as a skills folder (**Add from workspace folder**). Genie Code then knows the data, the gotchas and each build step. Start a new chat after adding them.

> [!TIP]
> **Not sure what to type?** Copy a starter prompt from [PROMPTS.md](PROMPTS.md) into Genie Code.

## Build it step by step

### Core path (everyone)

| Step | What to do | Where |
|---|---|---|
| **1. Explore** | See the seasonal cycle, the link between cold and demand, and the storage cycle. Or ask Genie Code: *"@gas_monthly @hdd_monthly plot residential use per customer against HDD"*. | `notebooks/01_explore` |
| **2. Model** | Fit residential use per customer against HDD. Explain the slope in plain words: how much more gas a home uses per degree of cold. | `notebooks/02_model_and_scenarios`, step 1 |
| **3. Backtest** | Train on earlier winters, predict winter 2025-26, and compare with what happened. | `notebooks/02_model_and_scenarios`, step 2 |
| **4. Scenarios** | Forecast winter 2026-27 for normal, cold, mild and 20% colder weather. | `notebooks/02_model_and_scenarios`, steps 3 and 4 |
| **5. Genie space** | Create the **Winter Gas Demand Assistant** with the instructions and examples provided, then test it. | [docs/genie_space.md](docs/genie_space.md) |
| **6. Dashboard** | Publish the **Ontario Winter Gas Outlook** dashboard and turn on Ask Genie. | [docs/dashboard.md](docs/dashboard.md) |

### Go further

| Idea | Hint |
|---|---|
| **Beat the straight line** | Ask Genie Code to train an ML model (for example gradient boosting with month-of-year) and compare its backtest error with the simple model. |
| **The coming week, live** | Run `notebooks/03_next_week`: it pulls today's ECCC forecast for Toronto and London and shows expected demand for each day vs. normal. Run it again tomorrow; each run is saved, so you start building your own forecast history. |
| **Weather vs. no weather** | Run `ai_forecast` on `residential_e3m3` and compare it with the weather model. Which handles a cold January better? |
| **Your own scenario** | "What if this January is as cold as January 2022?" Build it from `hdd_monthly`. |
| **Storage outlook** | Estimate how much the extra cold-winter demand would draw storage down, against past winters. Label it directional. |
| **Commercial customers** | Repeat the model for `commercial_m3_per_customer`. Is it as weather-sensitive as residential? |
| **Cold snaps** | Use `weather_daily` to find the coldest days and weeks. Peak days, not monthly totals, stress a gas system. |
| **Where people work** | Open the Genie space from Genie One, or pull the scenario table into Excel with the Databricks Excel Add-in. |

## Questions to try

- How much more gas does a home use for each extra heating degree day?
- Which January was the coldest, and how much gas did homes use that month?
- How accurate was the model for last winter?
- How much more gas would homes need this winter if it's as cold as the coldest winters on record?
- Which winter drew the most gas from storage, and was it a cold one?
- Does industrial demand depend on the weather?

Expected answers are in [docs/genie_space.md](docs/genie_space.md).

## The demo story

| Beat | What to show |
|---|---|
| **Problem** | Heating demand follows the weather, and a cold winter strains supply and storage. |
| **Insight** | The scatter chart: weather explains about 98% of monthly residential use per customer. |
| **Proof** | The backtest: last winter predicted within a few percent from weather alone. |
| **Action** | The scenarios: a cold winter needs about 16% more gas than a normal one. Ask the Genie space a live "what if" question, or show this week's forecast turned into expected demand. |
| **Impact** | Plan supply and storage before winter starts. Next step: run the same model on our own daily data. |

## Judging tips

- **Correct beats clever.** Show the backtest, and say clearly what the data can and cannot tell you.
- **Explain the model in one sentence** a non-analyst understands.
- **Make Genie answer correctly.** Test it with the questions above before the demo.
