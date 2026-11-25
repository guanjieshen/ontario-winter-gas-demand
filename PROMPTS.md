# Starter prompts for Genie One and Genie Code

**First time prompting? Start here.** Copy a prompt, paste it in, and press Enter. There's nothing to fill in. Then keep chatting, just as you would with a colleague.

These prompts work for **any hackathon project, on any data**: a ready-made track, your own data, or the winter gas demand kit in this repo.

## Start here

1. **Open Genie One** using the link your facilitator shares. It's a chat where you ask questions about your data.
2. **Paste [prompt 1](#1-what-data-do-i-have)** and press Enter.
3. **Reply to keep going:** "tell me more about idea 2", "show me that as a chart", "what should I do next?"

When you're ready to build, open **Genie Code** using the full-screen link your facilitator shares. If it asks you to pick compute or a SQL warehouse, choose the one your facilitator names.

## Which one do I use?

| | Genie One | Genie Code |
|---|---|---|
| **Use it to** | Ask questions, explore data, get ideas, make quick charts | Build things: tables, notebooks, dashboards, Genie Agents |
| **It gives you** | Answers, tables and charts | Work it creates for you, step by step |
| **Good to know** | Asking questions doesn't change your data | It tells you what it's about to do. Read it before you say yes. |

## Databricks words you'll see

| Word | Means |
|---|---|
| **Table** | Data in rows and columns, like a spreadsheet tab |
| **Notebook** | A page where Genie Code writes and runs steps, one block at a time |
| **Dashboard** | A shared page of charts and headline numbers |
| **Genie Agent** | A chat set up over specific data, so others can ask it questions (sometimes called a Genie space) |
| **AI functions** | Built-in AI that reads text, for example to sort comments or pull details out of documents |

---

## Get started

### 1. What data do I have?

**Use in:** Genie One

```text
I'm new to Databricks and at a hackathon today. What data do I have access to? Give me a short, plain-English summary of the main datasets and what each one could be useful for.
```

**You'll get:** a list of datasets, each with a one-line description.
**Try next:** "Tell me more about the first one. What questions could I answer with it?"

### 2. Give me hackathon ideas

**Use in:** Genie One

```text
I'm at a hackathon and looking for ideas. Look at the data I have access to and suggest 3 to 5 projects I could build in a couple of hours. For each one, tell me the problem it solves, the data it uses, and what the demo would show. Start with the easiest.
```

**You'll get:** 3 to 5 ideas, each with a problem, the data and a demo.
**Try next:** "Ask me a few questions about my team, then suggest ideas that would help us most."

### 3. Help me plan my idea

**Use in:** Genie One

```text
I have a hackathon idea. Ask me to describe it in a sentence, then help me plan it: whether I have the data for it, the simplest version I could build in a few hours, and the steps to get there.
```

**You'll get:** a question about your idea, then a short plan.
**Try next:** "Write step 1 as a request I can paste into Genie Code, the Databricks assistant that builds things for me."

---

## Explore the data

### 4. Give me a tour

**Use in:** Genie One

```text
Give me a tour of the data for my hackathon project. If you don't know my project yet, ask me what it is, then find the data for it yourself. For each table, explain in plain English what one row is, what time period it covers, and the most useful columns. How do the tables connect?
```

**You'll get:** a plain-English description of each table and how they link.
**Try next:** "Which of these columns would matter most for my project?"

### 5. Show me something interesting

**Use in:** Genie One

```text
What are the 3 most interesting patterns or trends in the data for my hackathon project? If you don't know my project yet, ask me what it is, then find the data for it yourself. Show each one as a chart with a one-sentence explanation.
```

**You'll get:** 3 charts, each with a sentence explaining it.
**Try next:** "Dig into the first one. What's driving it?"

### 6. Is the data any good?

**Use in:** Genie Code

```text
Check the quality of the data for my hackathon project. If you don't know my project yet, ask me what it is, then find the data for it yourself. Look for missing values, duplicates, odd values and gaps in dates. Explain in plain English what could trip me up, and don't change any data.
```

**You'll get:** a short list of data problems to watch out for.
**Try next:** "How should I handle the biggest problem?"

---

## Build something

### 7. Take the first step

**Use in:** Genie Code

```text
I'm new to Databricks. Help me take the first step on my hackathon project. If you don't know my project yet, ask me what it is, then find the data for it yourself. Before each step, explain in one sentence what you're about to do and why. Keep it simple.
```

**You'll get:** a first piece of work, explained as it goes.
**Try next:** "Great. What's the next step?"

### 8. Bring in my own spreadsheet

**Use in:** Genie Code

```text
I have a spreadsheet (CSV or Excel) on my computer that I'd like to use in my hackathon project. First tell me where and how to upload it, then walk me through turning it into a table, and show me the first few rows.
```

**You'll get:** upload instructions, then your spreadsheet as a table.
**Try next:** "Check this table for problems before I use it."

### 9. Make one clean table

**Use in:** Genie Code

```text
Build me one clean table for my hackathon project that combines the data I need. If you don't know my project yet, ask me what it is, then find the data for it yourself. Add a plain-English description to the table and each column, start its name with my team's name, tell me where you saved it, and show me 5 sample rows.
```

**You'll get:** one new table ready to use, and where to find it.
**Try next:** "Show me a chart of this table."

### 10. Use AI on text

**Use in:** Genie Code

```text
Look at the data for my hackathon project for free text, like notes, comments or documents. If you find some, show me how AI functions can sort, summarise or pull key details out of it, on 10 rows first so I can check the results. If there's no free text, tell me and suggest something else.
```

**You'll get:** AI results on 10 sample rows, for you to check.
**Try next:** "Those look right. Run it on everything and save it as a table."

### 11. Make a simple prediction

**Use in:** Genie Code

```text
Help me make one simple prediction with the data for my hackathon project. If you don't know my project yet, ask me what it is, then find the data for it yourself. Pick one number that's worth predicting, such as next month's total, predict it, and tell me in plain English how close the prediction is likely to be.
```

**You'll get:** one prediction, and how much to trust it.
**Try next:** "What would make this prediction better?"

---

## Share it

### 12. Make a dashboard

**Use in:** Genie Code

```text
Build me a dashboard that tells the story of my hackathon project: 3 headline numbers, one trend chart and one detail table, with clear titles. If you don't know my project yet, ask me what it is, then find the data for it yourself. Start its name with my team's name, and tell me how to share it with my team.
```

**You'll get:** a dashboard, and how to share it.
**Try next:** "Make the titles shorter and easier to read."

### 13. Let others ask questions

**Use in:** Genie Code

```text
Help me set up a Genie Agent so people can ask questions about my hackathon project's data in plain English. If you don't know my project yet, ask me what it is, then find the data for it yourself. Write the instructions, 5 example questions, and the answers I should expect so I can test it.
```

**You'll get:** a Genie Agent set up, with test questions and expected answers.
**Try next:** "I asked one of the test questions and the answer was wrong. Help me fix it."

### 14. Save and share my work

**Use in:** Genie Code

```text
List everything I've created today (tables, notebooks, dashboards and Genie Agents), where each one is saved, and whether my teammates can see it. Tell me how to give my team access to anything they can't see yet. Don't change anything without asking me.
```

**You'll get:** a checklist of your work and who can see it.
**Try next:** "Give my teammates access to the dashboard."

---

## Get unstuck

### 15. Something went wrong

**Use in:** Genie Code

```text
I got an error in the step I just ran. Explain in plain English what happened, then show me your fix before you run it.
```

**You'll get:** what went wrong, and a fix for you to approve.
**Try next:** "Yes, run the fix."

### 16. I can't see the data

**Use in:** Genie Code

```text
I can't see or open some data I need for my hackathon project, or I'm getting a "permission denied" message. Explain in plain English what's wrong and exactly what I should ask my facilitator for.
```

**You'll get:** the likely cause, and the words to use when you ask for help.

### 17. Explain this to me

**Use in:** Genie Code

```text
Explain what this notebook does, step by step, as if I'm new to Databricks. Don't change anything, just explain.
```

**You'll get:** a plain-English walkthrough of each step.
**Try next:** "What does step 3 mean in simpler words?"

### 18. These numbers look wrong

**Use in:** Genie Code

```text
These numbers don't look right to me. Check for common mistakes like double-counting or missing rows, then calculate the same total two different ways and show me both.
```

**You'll get:** a check for mistakes, and the number worked out two ways.
**Try next:** "Which one is right, and why?"

---

## Get ready to demo

### 19. Write my demo

**Use in:** Genie One

```text
Help me prepare a 3-minute hackathon demo. Ask me what I built and what I found, then write a short script with four parts: the problem, what we found, what we built, and why it matters. Suggest what to show on screen for each part.
```

**You'll get:** questions about your project, then a demo script.
**Try next:** "Make it shorter, and add one sentence about the business impact."

### 20. Practise the tough questions

**Use in:** Genie One

```text
Pretend you're a hackathon judge. Ask me the 5 hardest questions about my project, one at a time. After each of my answers, tell me how to make it clearer.
```

**You'll get:** judge questions, one at a time, with feedback on your answers.

---

## Phrases that keep the conversation going

| Say this | When |
|---|---|
| "Explain that more simply." | The answer is too technical |
| "Show me that as a chart." | You want a picture, not a table |
| "Show me 5 example rows." | You want to check a result |
| "That's not right, because…" | The answer is wrong. Say why, and it will try again. |
| "What should I do next?" | You're not sure where to go |
| "Do just the first step." | It's doing too much at once |

## Good habits

- **One step at a time.** Small requests give better answers than "build everything".
- **Check the numbers.** Ask for sample rows, or for the same number worked out another way.
- **Read before you say yes.** Genie Code tells you what it's about to do. If you're unsure, ask "what will this do?"
- **Name things after your team.** Start table, notebook and dashboard names with your team name so teammates can find them.
- **Keep private things out of the chat.** Don't paste passwords, or customer details copied from emails or other systems. Point Genie at the approved data in Databricks instead.

---

## For facilitators

Share these links in place of "the link your facilitator shares", and test them before the event:

| Link | Format |
|---|---|
| Genie One | `https://<workspace-host>/one?o=<workspace-id>` |
| Genie One with a prompt already typed | `https://<workspace-host>/one/chat?o=<workspace-id>&q=<url-encoded prompt>` |
| Genie Code, full screen | `https://<workspace-host>/editor/folders/workspace?o=<workspace-id>&mode=chat` |

Also tell participants which compute or SQL warehouse to pick, and confirm they can create tables, dashboards and Genie Agents in their team's area.

Before the event, run the 45-minute [dry-run checklist](docs/prompt_dry_run.md) to check every prompt in the real Genie One and Genie Code.
