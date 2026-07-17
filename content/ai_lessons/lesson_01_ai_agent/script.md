# AI Terms Explained — Lesson 1: What Is an "AI Agent"?

**Series:** AI Terms Explained (plain-language, doodle-illustrated)
**Runtime:** ~3 minutes
**Format:** Short video script / read-aloud lesson + companion slide deck
**Concrete example used:** Mistral Studio (Mistral AI's build-and-test workspace for AI apps)

---

## 0. Cold open (10 sec)

> **[DOODLE: a person at a desk juggling five browser tabs, sticky notes, and a coffee cup]**

**Narrator:** You know that feeling when a task needs five steps, three apps, and you have to do all of it by hand? That's the gap an "AI agent" is built to close.

**On-screen text:** *Today's term: AI AGENT*

---

## 1. The everyday definition (20 sec)

> **[DOODLE: a brain with a tiny gear turning inside it, connected by an arrow to a hand pressing buttons]**

**Narrator:** An AI agent is a program that doesn't just answer one question — it *takes a goal, plans the steps, and acts on its own* to get there, checking its work as it goes.

**Plain-language line:** Think of the difference between a calculator and an assistant. A calculator waits for you to type the exact numbers. An assistant hears "handle my expense report" and goes and does it — opens the app, finds the receipts, fills the form, tells you when it's done.

---

## 2. Analogy #1 — Office Suite (45 sec)

> **[DOODLE: two side-by-side desks. Left desk: a "Mail Merge" button being clicked once. Right desk: a tiny robot walking between a spreadsheet, an inbox, and a printer.]**

**Narrator:** You already know a cousin of this from Office Suite tools.

- A **macro** or **Mail Merge** is a fixed recipe: click one button, and it repeats the *same* steps on the *same* file, every time, no matter what.
- An **AI agent** is more like a new hire you hand a goal to: "Send this month's invoice to everyone who hasn't paid." It has to figure out *which* rows qualify, *how* to word each email, and *whether* something looks off — and adjust instead of just repeating a fixed script.

**Key line:** A macro follows steps. An agent chooses the steps.

---

## 3. Analogy #2 — Web Browser (45 sec)

> **[DOODLE: a browser window with a small robot hand clicking through a checkout flow, with a checklist floating beside it: "search → compare → fill form → confirm"]**

**Narrator:** Same idea in your browser.

- **Autofill** just pastes your saved name and address into a form you're already looking at. Useful, but it can't leave the page.
- An **AI agent** can be told "find the cheapest flight to Berlin next Friday and hold a seat," and it will open tabs, compare prices, fill the form, and stop to ask you before it pays — moving through the whole task, not just one field.

**Key line:** Autofill fills a box. An agent completes a mission.

---

## 4. Concrete example — Mistral Studio (60 sec)

> **[DOODLE: a simple flowchart — a lightbulb ("Goal") → a robot head ("Agent") → three small icon bubbles ("Web Search," "Code," "Calculator") → a checkmark ("Result")]**

**Narrator:** Here's what this looks like in a real tool: **Mistral Studio**, Mistral AI's workspace for building and testing AI apps.

In Mistral Studio, you don't just chat with a model — you can configure an **agent**: give it a goal or instructions, hand it *tools* (like web search, a code interpreter, or a document reader), and watch it work through a task step by step in the playground, the same way you'd test a macro before trusting it on real files.

**Plain-language line:** It's the difference between opening a chat window and asking a question, versus opening a workbench where you assemble a helper, give it tools, and set it loose on a job.

---

## 5. Recap (20 sec)

> **[DOODLE: a simple formula written like handwriting — "AI AGENT = A GOAL + A BRAIN + TOOLS + THE ABILITY TO ACT" — with a small robot giving a thumbs up]**

**Narrator, recap card:**
- A **model** answers questions.
- An **agent** *pursues goals* — it plans, uses tools, and acts across multiple steps until the job is done.
- Office macros and browser autofill hinted at this; agents generalize it.
- **Mistral Studio** is one concrete place you can build and test one yourself.

**On-screen text:** *AI Agent = Goal + Reasoning + Tools + Action*

---

## 6. Sign-off + next topic (10 sec)

> **[DOODLE: a signpost with one arrow labeled "You are here: AGENT" and a second, greyed-out arrow labeled "Next: MEMORY?"]**

**Narrator:** That's an AI agent. Next time, we'll open the hood on **"memory"** — how an AI remembers what you told it five minutes (or five days) ago.

---

## Viewer / User Notes (for the companion deck's notes pane)

- **One-line definition to remember:** *An agent doesn't just respond — it plans, acts, and checks its own work toward a goal.*
- **Everyday comparison:** macro = fixed recipe; autofill = fills one box; agent = takes the whole job.
- **Where to see it live:** Mistral Studio → create an agent → attach tools → give it a goal → watch it reason step by step.
- **Common confusion to avoid:** an agent is not a *smarter chatbot* — the defining feature is that it takes *actions* across *multiple steps*, not just better answers in one reply.
- **Try it yourself:** open Mistral Studio, create one agent, give it a single tool (e.g., web search), and ask it a task that needs 2-3 steps to complete.

---

## Series tracker

- **Covered so far:** Lesson 1 — *AI Agent*
- **Suggested next topics (via brainstorm-agent divergence pass — see `topics_covered.md`):** Memory → Skill → Hook → Model → Prompt/JSON basics
- **Next up:** Lesson 2 — *Memory*
