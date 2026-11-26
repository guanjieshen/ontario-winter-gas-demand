# Advanced prompts for Genie Code

> [!TIP]
> New to Genie? Start with the [starter prompts](PROMPTS.md). Come here when your team has a problem picked and wants to build something judges will score well.

These prompts are for the person on your team who's driving Genie Code. They follow the hackathon day: **plan, build a trusted base, add AI, make it answer questions, then demo**. Each one asks Genie Code for **proof** (real query output), not just code, because judges check that it works and that the numbers are right.

**Before you start:**
- **Turn off Auto-approve:** in Genie Code settings, pick the mode where you click **Allow** for each action.
- **Know your locations:** the shared schema you read from, your team schema you write to, and the SQL warehouse to use.
- **Using a ready-made kit?** If it has a skills folder, add it to Genie Code first (**Add from workspace folder**), then start a new chat.
- **Fill in the blanks:** replace anything in `<angle brackets>` before you press Enter.

## Pick a prompt

| I want to | Prompt |
|---|---|
| Turn our idea into a plan that scores well | [A1](#a1-plan-the-day-around-the-judging) |
| Stop repeating the same instructions | [A2](#a2-give-genie-code-standing-rules) |
| Build one table we can trust | [A3](#a3-build-one-trusted-table) |
| Sort or summarize thousands of text notes | [A4](#a4-use-ai-on-text-and-prove-its-right) |
| Pull facts out of PDFs and check them against a policy | [A5](#a5-pull-facts-out-of-pdfs-and-check-them) |
| Predict or forecast something | [A6](#a6-predict-something-honestly) |
| Build a Genie Agent that gets hard questions right | [A7](#a7-build-a-genie-agent-that-passes-its-own-tests) |
| Answer questions from policy or procedure documents | [A8](#a8-answer-questions-from-documents) |
| Build an app where people act on the data (stretch) | [A9](#a9-stretch-design-an-app-where-people-act) |
| Fix something that's broken | [A11](#a11-debug-without-guessing) |
| Check we're ready for the judges | [A12](#a12-score-us-like-a-judge) |
| Get demo ready | [A13](#a13-get-demo-ready) |

## Moves that work in any prompt

| Move | Say something like |
|---|---|
| **Point at the exact data** | "Use @`<table>`" (type `@` to pick a table, notebook or file) |
| **Test small first** | "Try it on 20 rows and show me before you run it on everything" |
| **Ask for proof** | "Run it and show me the output, not just the code" |
| **Set a stop point** | "Stop after step 1 and wait for my OK" |
| **Diagnose before fixing** | "Don't fix it yet. Tell me the likeliest causes first" |
| **Keep it honest** | "If you're not sure, say so. Don't invent numbers" |

---

## Plan

### A1. Plan the day around the judging

**Use in:** Genie Code

```text
Our hackathon team (<number> people, <hours> hours left) wants to solve this problem: <problem in one sentence>. Our data is in @<shared schema>.
Judges score business value, a working solution, use of the platform, trust in the answers, and the demo. Write a plan that scores well on all five:
1. The problem, who acts on the answer, and the decision they'd make differently.
2. The insight we expect to show, and the query that would prove it. Run it and show me the result.
3. An impact measure we can calculate from this data. Don't invent figures.
4. A core path we're sure to finish, and 2 stretch steps if we have time.
5. Who on the team does what, and a timeline.
Save it as PLAN.md in my project folder. Stop and wait for my review.
```

**You'll get:** a plan grounded in a real query, with a core path and stretch steps.
**Try next:** "What's the biggest risk in this plan, and how do we avoid it?"

### A2. Give Genie Code standing rules

**Use in:** Genie Code

```text
Create a file named AGENTS.md in my project folder. It holds standing rules for everything you build for my team:
- Read from @<shared schema>. Write only to <team schema>. Never change the shared schema.
- Use the SQL warehouse <warehouse>.
- Our definitions: <for example, "overdue means more than 90 days past due">.
- Every number you show must come from a query you ran. If you're unsure, say so.
- Test on a small sample before running on everything.
- Never share, deploy or delete anything without asking me first.
Show me the file before you save it.
```

**You'll get:** rules Genie Code reads every time you work in that folder.
**Try next:** "Read AGENTS.md and tell me, in 3 lines, how you'll follow it."

---

## Build a trusted base

### A3. Build one trusted table

**Use in:** Genie Code

```text
Read PLAN.md. Build the one table that everything else (dashboard, Genie Agent, demo) will use. Save it in <team schema> as <table name>.
Before saving, show me the query and 10 sample rows.
After saving, run these checks and show me the results: row count, date range, duplicate keys, missing values in key columns, and totals compared with the source tables.
Add a one-line description to the table and to every column, including how each calculated column is worked out.
```

**You'll get:** one documented table, with checks that prove it matches the source.
**Try next:** "Show me 3 rows where the calculation could be wrong, and walk me through them."

### A4. Use AI on text, and prove it's right

**Use in:** Genie Code

```text
I want to label every row of the text column <column> in @<table> with <what you want, for example "a reason and a sentiment">.
1. Look at 30 rows and suggest a short list of labels that fits the data. Wait for my OK on the list.
2. Use AI Functions (for example ai_classify or ai_summarize) on 20 rows. Show me the text next to each label.
3. I'll tell you which are wrong. Improve the labels or the prompt, and test again.
4. Then run it on all rows, save the result in <team schema>, and show me the count for each label.
```

**You'll get:** labelled text you've spot-checked yourself, ready for charts and your Genie Agent.
**Try next:** "Which label has the most borderline cases? Show me 5."

### A5. Pull facts out of PDFs and check them

**Use in:** Genie Code

```text
There are PDF documents in the volume folder <path>. Use ai_parse_document and ai_extract to pull out these fields from each one: <fields, for example "document number, amount, status, approver">.
1. Try it on 3 files first and show me the fields next to the file name. Wait for my OK.
2. Run it on all files and save the result in <team schema>.
3. Compare the extracted fields with <the rule, policy or table to check against>. List every mismatch with the file name, so I can open the PDF and check it.
```

**You'll get:** a table built from the PDFs, plus a list of exceptions you can prove one by one.
**Try next:** "Which fields did the extraction struggle with? Show me the files."

### A6. Predict something honestly

**Use in:** Genie Code

```text
I want to predict <target> using @<tables>.
1. Only use data up to <cutoff date> to train, so the model can't peek at the answer. Tell me how you're making sure of that.
2. Start with the simplest reasonable baseline, then try one better model.
3. Test both on data after the cutoff. Report the accuracy in plain English (for example, "within 8% on average") and in a standard measure.
4. Show the top 5 drivers in plain English.
5. If the better model doesn't beat the baseline clearly, tell me and keep the baseline.
Save the predictions in <team schema>.
```

**You'll get:** a prediction you can defend, with its accuracy shown against a simple baseline.
**Try next:** "Where is the model most wrong? Is there a pattern?"

---

## Make it answer questions

### A7. Build a Genie Agent that passes its own tests

**Use in:** Genie Code

```text
Help me set up a Genie Agent for <who will use it> over <the tables we built, plus any source tables>.
1. Write instructions with our definitions from AGENTS.md, in plain English.
2. Write 8 questions those users would really ask, including 3 hard ones (a comparison, a time period and a "why").
3. For each question, write the SQL answer, run it, and show me the result.
4. Add the questions and SQL to the agent as example queries and as benchmarks.
5. Run the benchmarks, and show me any that fail and why.
If you can't do a step yourself, give me click-by-click steps for it.
```

**You'll get:** a Genie Agent whose answers are checked against SQL you've reviewed.
**Try next:** "Ask each hard question two other ways. Does the agent still get them right?"

### A8. Answer questions from documents

**Use in:** Genie Code

```text
I want people to ask questions about the documents in <path> (for example policies or procedures) and get answers that cite the document they came from. Use the document Q&A option that's turned on in this workspace (ask me if you're not sure which).
Set it up, or give me click-by-click steps if you can't. Then test it with 5 questions: 3 the documents answer, 1 that needs two documents, and 1 they don't answer at all, where it should say it doesn't know.
```

**You'll get:** a document Q&A agent, tested on whether it admits what it doesn't know.
**Try next:** "Which answer was weakest? What would make it better?"

---

## Stretch: build an app

Check with your facilitator before you start. Apps need setup that not every workspace has.

### A9. Stretch: design an app where people act

**Use in:** Genie Code

```text
Read PLAN.md. Design a Databricks App where a user acts on our results: for example, approving, assigning an owner, or overriding a value. It reads our tables through the SQL warehouse and saves what users do to the Lakebase database <database>.
Write SPEC.md with: the user and their decision, the tables it reads, the Lakebase tables it saves to (with the SQL to create them), up to 2 screens, who can open it, and numbered tests that define done. Keep it small enough to build in <hours> hours. Stop and wait for my review.
```

**You'll get:** a small, testable app spec.
**Try next:** "Cut it to one screen. What do we lose?"

### A10. Stretch: build the app in slices

**Use in:** Genie Code

```text
Read SPEC.md and AGENTS.md. Build the app in 2 slices, and stop after each for my OK:
1. A screen that reads our data through the SQL warehouse. Show me it working.
2. Saving a user's action to Lakebase, shown next to the data it's about. Save 2 TEST_ rows and read them back.
Use parameterized queries and no secrets in code. Run the tests in SPEC.md and show me the results. Ask me before you deploy or share it.
```

**You'll get:** a working app, checked one slice at a time.
**Try next:** "Show me how the saved actions could feed our dashboard or Genie Agent."

---

## Get ready to demo

### A11. Debug without guessing

**Use in:** Genie Code

```text
Something's broken. Here's what I did: <what you clicked or ran>. Here's what happened: <paste the error or describe it>.
Don't fix it yet. Give me the 3 likeliest causes, ranked, and how to confirm each. Confirm the top one and show me the evidence. Then propose a fix and wait for my OK.
```

**You'll get:** the real cause, with evidence, before anything changes.
**Try next:** "That didn't work. What did we rule out, and what's next?"

### A12. Score us like a judge

**Use in:** Genie Code

```text
Read PLAN.md and look at what we've built in <team schema>. Act as a hackathon judge scoring business value, working solution, use of the platform, trust in the answers, and the demo.
For each one, give a score out of 5 with one line of evidence. Then list every number we plan to show in the demo, rerun the query behind it, and flag any that don't match. Finish with the 3 changes that would raise our score most in the <minutes> minutes we have left.
```

**You'll get:** an honest scorecard, numbers you've rechecked, and a short fix list.
**Try next:** "Do the first fix."

### A13. Get demo ready

**Use in:** Genie Code

```text
Write a <minutes>-minute demo script for our project: problem, insight, action, impact. For each beat, say what to show on screen and which number to say out loud, with the query it comes from.
Add 2 live questions to ask our Genie Agent that we've tested and know it answers correctly.
List what's most likely to fail live, with a backup for each, such as a screenshot.
```

**You'll get:** a timed script with every number traced to a query, and a backup plan.
**Try next:** "Play a skeptical judge and ask me 3 hard questions about our numbers."

---

## For facilitators

Run these prompts in the event workspace before the day. They aren't in the [dry-run checklist](docs/prompt_dry_run.md) yet.

- **A2:** check that Genie Code picks up the AGENTS.md file from the project folder.
- **A5:** check that the AI Functions `ai_parse_document` and `ai_extract` are available on the event warehouse.
- **A7:** check that participants can create Genie Agents and add benchmarks.
- **A8:** decide which document Q&A option teams use (a Genie Agent in Agent mode, or Knowledge Assistant) and tell them.
- **A9 and A10 (stretch):** confirm which tool builds apps in this workspace (Genie Code, or Genie App Builder, which is in Beta and needs an admin to enable "Governed agentic app-building" under Previews). Pre-create a Lakebase database and grant teams access. Grant Unity Catalog SELECT on the tables to the app identity. "Can use" on a warehouse doesn't grant data access. Stop apps at the end of the day, because they bill while running.
- **Optional:** add workspace-wide rules ("ask before creating, deploying or sharing") to `.assistant_workspace_instructions.md`.
