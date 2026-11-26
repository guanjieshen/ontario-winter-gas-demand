# Advanced prompts: build an app

> [!TIP]
> New to Genie? Start with the [starter prompts](PROMPTS.md). Come here when you're ready to build something bigger.

These prompts help you build a **Databricks App** that reads your data through a **SQL warehouse** and saves what people do in it to **Lakebase**. The same moves work for any build.

**What makes these advanced:** you give Genie Code **standing rules**, a **written spec** and a **definition of done**, then build in **small slices** and ask for **proof** at each one. That's how you get a working demo instead of a pile of half-finished code.

**Before you start:**
- **Ask your facilitator** for your SQL warehouse, your Lakebase database, and the catalog and schema for your team.
- **Turn off Auto-approve:** in Genie Code settings, pick the mode where you click **Allow** for each action.
- **Fill in the blanks:** replace anything in `<angle brackets>` before you press Enter.

## Moves that work in any prompt

| Move | Say something like |
|---|---|
| **Point at the exact data** | "Use @`<table>`" (type `@` to pick a table, notebook or file) |
| **Give it a file to follow** | "Read SPEC.md first and follow it" |
| **Set a stop point** | "Stop after step 1 and wait for my OK" |
| **Ask for proof** | "Run it and show me the output, not just the code" |
| **Diagnose before fixing** | "Don't fix it yet. Tell me the likeliest causes first" |
| **Keep it honest** | "If you're not sure, say so. Don't guess numbers or prices" |

---

## Set up (5 minutes)

### A1. Give Genie Code standing rules

**Use in:** Genie Code

```text
Create a file named AGENTS.md in my project folder <folder>. It holds standing rules for everything you build for me in this project:
- Team name: <team>. Start the name of every app, table and file with it.
- Read data from <catalog.schema> through the SQL warehouse <warehouse>.
- Save app data to the Lakebase database <database>.
- Test rows start with TEST_.
- Use parameterized queries. Never put passwords or tokens in code.
- Never deploy, share or delete anything without asking me first.
- Prefer the simplest working option and tell me when you're unsure.
Show me the file before you save it.
```

**You'll get:** a rules file Genie Code reads every time you work in that folder, so you stop repeating yourself.
**Try next:** "Read AGENTS.md and tell me, in 3 lines, how you'll follow it."

---

## Design

### A2. Find an idea worth building

**Use in:** Genie Code

```text
I want to build a Databricks App for a hackathon using the data in @<catalog.schema>. Skip plain dashboards. Suggest 5 apps where a person makes a decision and the app records it, for example approving, overriding a forecast, triaging an exception, assigning an owner, or saving a what-if scenario.
For each idea, give me:
- the user and the decision they make
- the tables it reads, and the columns that matter
- what it saves to Lakebase, and why a dashboard alone can't do it
- the moment in the demo that makes people lean in
- the riskiest part to build
Then rank them by demo impact against build risk for a team with <hours> hours, and recommend one.
```

**You'll get:** 5 ranked ideas with a clear recommendation.
**Try next:** "Make idea 2 more valuable for <who the judges are>, without making it harder to build."

### A3. Write the spec

**Use in:** Genie Code

```text
Write a build spec for this app idea: <idea, or "the one you recommended">. Save it as SPEC.md in my project folder. Include:
1. Problem and user, in 2 sentences.
2. User stories: up to 3, as "As a <user>, I want to <action> so that <outcome>".
3. Data it reads: tables and columns. Run a sample query on each table to prove the columns exist and show me 5 rows.
4. Lakebase tables: the SQL to create them, with a key, created_by and created_at columns.
5. Screens: up to 3, with what each button does and the query behind it.
6. Who can open the app, and whether it runs as the app or as the signed-in user. Recommend one and say why.
7. Out of scope for today.
8. Acceptance tests: numbered checks I can run by hand, such as "saving an override shows up in the list within 5 seconds".
Recommend the app framework to use and say why. Stop when SPEC.md is written and wait for my review.
```

**You'll get:** a one-page spec, with its data checked against the real tables, and tests that define done.
**Try next:** "Cut the spec down so it fits in <hours> hours. Tell me what you removed."

---

## Build

### A4. Build slice 1: show the data

**Use in:** Genie Code

```text
Read SPEC.md and AGENTS.md. Build only slice 1: the main screen that reads data through the SQL warehouse, with its filters. No Lakebase yet.
Use parameterized queries and limit results so the screen loads quickly.
Test it before anyone else can see it, and tell me how you tested it.
Show me acceptance tests that cover this screen passing, with the output. Then stop.
```

**You'll get:** one working screen on real data, with proof that it works.
**Try next:** "It's slow. Show me the query, explain why, and suggest a fix before changing anything."

### A5. Build slice 2: save decisions to Lakebase

**Use in:** Genie Code

```text
Read SPEC.md. Build slice 2: the save path.
1. Create the Lakebase tables from the spec. Show me the SQL first.
2. Add the form or buttons that save a decision, with validation and a clear error message if the save fails.
3. Show each saved decision next to the data it's about, on the main screen.
4. Save 2 TEST_ rows, read them back, and show me both.
Run the acceptance tests for this slice and show me the results. Then stop.
```

**You'll get:** the app reading from the warehouse and writing to Lakebase, joined on one screen.
**Try next:** "Add an edit history, so we can see who changed a decision and when."

### A6. Close the loop

**Use in:** Genie Code

```text
The decisions saved in Lakebase should also be usable in Databricks SQL, so a dashboard or Genie Agent can report on them. Tell me the options for doing that in this workspace, with the trade-offs of each, and recommend the simplest. Don't build anything until I pick one.
```

**You'll get:** a way to report on what users decided, not just on the source data.
**Try next:** "Write the SQL for a 'decisions this week' summary, then build it."

### A7. Add one AI feature

**Use in:** Genie Code

```text
Read SPEC.md. Suggest 3 AI features that would make this app more useful, for example summarizing saved notes, explaining an unusual row in plain English, or letting users ask questions about the data. For each one, tell me what it costs to run (what gets called and how often, no prices) and what could go wrong in a live demo. Recommend the safest one, then build it behind a button after I say yes.
```

**You'll get:** one AI feature that you know will hold up in front of an audience.
**Try next:** "Show me 3 examples of its output on real rows. Are any of them wrong?"

---

## Harden and demo

### A8. Review it like a senior engineer

**Use in:** Genie Code

```text
Review the app code against SPEC.md and AGENTS.md as a senior engineer would. List the issues, worst first:
- acceptance tests that fail
- security: injection risks, secrets in code, anyone seeing data they shouldn't
- what happens with an empty table, a slow query or a failed save
- anything that breaks AGENTS.md
For each issue, show where it is and how you'd fix it. Don't change anything until I choose which to fix.
```

**You'll get:** a ranked list of real problems, fixed only with your OK.
**Try next:** "Fix the top 3, then rerun all the acceptance tests."

### A9. Debug without guessing

**Use in:** Genie Code

```text
Something's broken. Here's what I did: <what you clicked or ran>. Here's what happened: <paste the error or describe it>.
Don't fix it yet. Check the app logs, then give me the 3 likeliest causes, ranked, and how to confirm each. Confirm the top one, show me the evidence, then propose a fix and wait for my OK.
```

**You'll get:** the real cause, with evidence, before anything changes.
**Try next:** "That didn't work. What did we rule out, and what's next on the list?"

### A10. Get demo ready

**Use in:** Genie Code

```text
Get the app ready for a 3-minute demo:
1. Load about 20 realistic TEST_ rows so the screens don't look empty, and add a way for me to reset them.
2. Write a demo script: the problem, the decision a user makes in the app, what gets saved, and why it matters. Mark where to click.
3. List the things most likely to fail live, with a backup plan for each.
4. Tell me what you'll do to deploy and share it with <team or group>, then wait for my yes.
5. Give me an end-of-day checklist to stop the app and anything else that keeps running.
```

**You'll get:** demo data, a script, a backup plan and a clean shutdown.
**Try next:** "Play a skeptical judge and ask me 3 hard questions about this app."

---

## For facilitators

Check these before the event. The app prompts aren't in the [dry-run checklist](docs/prompt_dry_run.md) yet, so run A1 to A10 by hand in the event workspace.

- Confirm in the dry run which tool builds apps in this workspace: Genie Code, or Genie App Builder (Beta: admin enables "Governed agentic app-building" under Previews; users need CAN CREATE APP on an App Space). If it's Genie App Builder, tell teams to use A4 to A10 there.
- Pre-create one Lakebase database per team (or one shared one) and give teams the rights to create tables in it.
- Grant Unity Catalog SELECT on the hackathon tables to teams and to the app identity. "Can use" on a warehouse doesn't grant data access.
- Check that Genie Code picks up the AGENTS.md file from A1 in the event workspace.
- Optional: add workspace-wide rules ("ask before creating, deploying or sharing") to `.assistant_workspace_instructions.md`.
- End of day: stop apps. They keep billing while running, and so does Lakebase while it's active.
