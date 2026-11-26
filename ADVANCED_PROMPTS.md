# Advanced prompts: build an app

> [!TIP]
> New to Genie? Start with the [starter prompts](PROMPTS.md). Come here when you're ready to build something bigger.

Use these when you want to build a Databricks App that reads your data and saves what users type in (Lakebase). The same pattern works for any build.

**Before you start:**
- **Ask your facilitator** which SQL warehouse and Lakebase database your team uses.
- **Turn off Auto-approve:** in Genie Code settings, pick the mode where you click **Allow** for each action.

**The pattern that gets good results:** say what you're building and with what data, set limits, ask for a plan, approve it, then build in small steps and check each one.

### A1. Give me app ideas

**Use in:** Genie One

```text
I want to build a Databricks App for my hackathon. It should read my data and save what users type in, like notes, approvals or status. Look at the data I have access to and suggest 3 app ideas. For each one, give me who uses it, the tables it reads, what it saves, and its 2 or 3 screens. Start with the simplest.
```

**You'll get:** 3 app ideas you can compare.
**Try next:** "Ask me 3 questions about my users, then improve idea 1."

### A2. Plan it first

**Use in:** Genie Code

```text
Plan the app idea I picked. Show me the tables it reads, the Lakebase tables it saves to with their columns, the screens, and who can open it. Use the SQL warehouse and Lakebase database my facilitator named. Don't guess prices. Don't create anything until I say yes.
```

**You'll get:** a plan to approve before anything gets built.
**Try next:** "Make it simpler: one screen only."

### A3. Build it in steps

**Use in:** Genie Code

```text
Build the app from our plan, one step at a time, and wait for my OK after each:
1. One screen that shows 10 rows of my data.
2. A form that saves an entry to Lakebase, in a table named after my team.
3. Save 2 test entries and read them back to me.
Ask me before you deploy or share the app.
```

**You'll get:** a working app, checked at each step.
**Try next:** "Add one filter to the main screen. Ask me which column first."

### A4. Turn my idea into a strong prompt

**Use in:** Genie One or Genie Code

```text
Ask me up to 5 quick questions about my hackathon idea, one at a time. Then write me one detailed prompt I can paste into Genie Code to build it, including what data to use, what to avoid, and how we'll know it works.
```

**You'll get:** a ready-to-paste prompt for your own idea.
**Try next:** paste it into Genie Code.

---

## For facilitators

Check these before the event. The app prompts aren't in the [dry-run checklist](docs/prompt_dry_run.md) yet, so run A1 to A4 by hand in the event workspace.

- Confirm in the dry run which tool builds apps in this workspace: Genie Code, or Genie App Builder (Beta: admin enables "Governed agentic app-building" under Previews; users need CAN CREATE APP on an App Space).
- Pre-create one Lakebase database per team (or shared) and give teams CAN MANAGE / connect rights.
- Grant Unity Catalog SELECT on the hackathon tables. "Can use" on a warehouse doesn't grant data access.
- Optional: add standing rules ("ask before creating, deploying or sharing") to .assistant_workspace_instructions.md.
- End of day: stop apps. They keep billing while running, and so does Lakebase while it's active.
