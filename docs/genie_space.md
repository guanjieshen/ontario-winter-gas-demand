# Genie space: Winter Gas Demand Assistant

Ready-to-paste configuration. Every expected answer below was checked against the shipped data.

## Tables

Add these from your schema:

- `gas_monthly`
- `hdd_monthly`
- `winter_scenarios`
- `backtest`
- `demand_model`

## General instructions

Paste this into the space's instructions:

```text
You help analysts understand how weather drives Ontario natural gas demand and storage.

Data:
- gas_monthly: Ontario gas consumption by sector and underground storage, monthly, from Statistics Canada. Province-wide, all utilities.
- hdd_monthly: monthly heating degree days (HDD) by city. More HDD means colder weather.
- demand_model: a straight-line model of residential use per customer against HDD.
- backtest: the model's predictions for winter 2025-26 compared with actual use.
- winter_scenarios: forecasts of residential use for winter 2026-27 (Nov 2026 to Mar 2027) under Normal, Cold, Mild and 20% colder weather.

Definitions:
- "Demand" or "use" means consumption. Default to residential_e3m3 unless the user names a sector.
- Volumes ending in _e3m3 are thousands of cubic metres. Show results in million m3 (divide by 1,000), or billion m3 for storage (divide by 1,000,000).
- Never add columns with different unit suffixes (_e3m3, _e3gj, _k_cad, _customers).
- "Cold" or "weather" means heating degree days. Use avg_toronto_london_hdd unless the user names a city.
- "Winter" means November to March. Label a winter by both years, for example "winter 2025-26".
- "Per customer" columns (*_m3_per_customer) are only populated from 2019-01. Customer counts before 2019 use a different method; do not compare them with later years.
- Negative storage_change_e3m3 means storage was drawn down.

Always say that this is public, province-wide monthly data, not a single utility's figures, when giving forecasts.
```

## Example SQL queries

Add these as example queries so Genie learns the patterns.

**"How cold was each January and how much gas did homes use?"**

```sql
SELECT g.month, h.avg_toronto_london_hdd AS hdd,
       ROUND(g.residential_e3m3 / 1000, 1) AS residential_million_m3
FROM gas_monthly g
JOIN hdd_monthly h USING (month)
WHERE MONTH(g.month_start) = 1
ORDER BY hdd DESC
```

**"How much gas was withdrawn from storage each winter?"**

```sql
SELECT
  CASE WHEN MONTH(month_start) >= 11 THEN YEAR(month_start) ELSE YEAR(month_start) - 1 END AS winter_starting,
  ROUND(SUM(storage_withdrawals_e3m3) / 1e6, 2) AS withdrawals_billion_m3,
  ROUND(MIN(storage_closing_e3m3) / 1e6, 2) AS lowest_inventory_billion_m3
FROM gas_monthly
WHERE MONTH(month_start) IN (11, 12, 1, 2, 3)
GROUP BY 1
HAVING COUNT(*) = 5
ORDER BY 1
```

**"How much more gas would homes need in a cold winter?"**

```sql
SELECT scenario, ROUND(SUM(residential_million_m3), 0) AS winter_total_million_m3
FROM winter_scenarios
GROUP BY scenario
ORDER BY winter_total_million_m3 DESC
```

## Test questions and expected answers

| Question | Expected answer |
|---|---|
| Which January was the coldest? | January 2022, 820.3 HDD |
| How did January 2026 compare with January 2025? | Colder (775.2 vs. 751.2 HDD); residential use 1,570.5 vs. 1,528.1 million m³ |
| How well does weather explain residential demand? | R² ≈ 0.98 over 93 months (2019 onward) |
| How accurate was the model last winter? | Errors of −0.8% to +8.5% per month, 3.7% on average (winter 2025-26) |
| How much gas will homes need this winter if it's cold? | About 6,811 million m³ (Nov 2026 to Mar 2027), about 16% more than normal (5,866) |
| Which winter drew the most gas from storage? | Winter 2021-22, 6.33 billion m³ |
| What was the lowest storage level at the end of a winter? | 2.68 billion m³, March 2019 |
| Does industrial demand depend on the weather? | Much less: R² ≈ 0.20, vs. 0.96 commercial and 0.98 residential |

The last question needs `gas_monthly` and `hdd_monthly`; Genie should compute `REGR_R2` per sector.
