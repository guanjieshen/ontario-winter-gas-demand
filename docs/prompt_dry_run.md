# Dry-run checklist: starter prompts

Use this before the hackathon to check the [starter prompts](../PROMPTS.md) in the real Genie One and Genie Code, signed in as a participant would be.

**Allow about 45 minutes.** Paste each prompt exactly as written. When Genie asks about your project, give the standard reply below. Tick **Pass** if the answer matches "Looks like".

## Standard reply

When a prompt asks what your project is, paste:

```text
My project is about how cold weather drives Ontario winter gas demand. I don't know exactly where the data is. My team name is testteam.
```

Swap in any project that has data on your workspace.

## What's already been checked

| Prompt | Checked how | Result |
|---|---|---|
| 1, 2, 3 and its follow-up, 19, 20 (Genie One) | Live, through the Genie One CLI | Pass |
| 6, 7 first turn (Genie Code) | Live, through the Genie Code CLI | Pass: asked about the project first |
| 10: AI functions | `ai_classify`, `ai_analyze_sentiment`, `ai_summarize` on a SQL warehouse | Pass |
| 11: forecasting | `ai_forecast` on a SQL warehouse | Pass |
| 12, 13: create a dashboard and a Genie Agent | Created and deleted through the API as a regular user | Pass |

The rest needs Genie Code in the browser.

## Genie Code checks

| # | Prompt | Looks like | Pass |
|---|---|---|---|
| 6 | Is the data any good? | Asks about the project, **finds the tables itself**, then lists data problems in plain English. Changes nothing. | ☐ |
| 7 | Take the first step | Asks about the project, explains each step in one sentence before running it, and keeps it to one small step. | ☐ |
| 8 | Bring in my own spreadsheet | Says where to upload the file first (for example **New → Add or upload data**), then turns it into a table and shows rows. | ☐ |
| 9 | Make one clean table | Creates one table named with `testteam`, adds column descriptions, says where it's saved, shows 5 rows. | ☐ |
| 10 | Use AI on text | On data with no free text, says so and suggests something else. On data with text, shows results for 10 rows before running on all. | ☐ |
| 11 | Make a simple prediction | Picks one number, predicts it, and explains in plain English how close it's likely to be. | ☐ |
| 12 | Make a dashboard | Creates a dashboard named with `testteam`, with 3 headline numbers, a trend and a table, and explains how to share it. | ☐ |
| 13 | Let others ask questions | Creates a Genie Agent with instructions, 5 example questions and expected answers. | ☐ |
| 14 | Save and share my work | Lists what was created and where, and who can see it. Asks before changing anything. | ☐ |
| 15 | Something went wrong | Run a query with a typo first (for example a misspelled table name). Explains the error and **shows the fix before running it**. | ☐ |
| 16 | I can't see the data | Explains the likely cause and gives the exact words to ask a facilitator. | ☐ |
| 17 | Explain this to me | With a notebook open, explains each step in plain English and changes nothing. | ☐ |
| 18 | These numbers look wrong | After a result, checks for double-counting and shows the same total calculated two ways. | ☐ |

## If a prompt fails

- **It didn't ask about the project:** check the workspace skills are installed. Then add "Ask me about my project first" to the start of the prompt.
- **It couldn't find the data:** the participant may lack access. Check grants on their catalog and schema, then rerun prompt 16 to see what it suggests.
- **It changed something it shouldn't have:** remind participants to read before saying yes, and add "Don't change anything without asking me" to the prompt.
- **A prompt is too slow or too big:** split it, for example "Do just the first step."

After the dry run, delete anything named `testteam`.
