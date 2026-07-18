---
series: "AI Explained Simply"
episode: 1
term: "AI Agent"
date: 2026-07-18
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:00 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio)"
---

# Episode 1: What's an "AI Agent"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it.*

---

## 0. Cold open (0:00–0:15)

**On screen (doodle):** a stick figure staring at a glowing box labeled "MODEL" with a speech bubble that just says "42."

**Narration:**
> "You've probably heard 'AI model' and 'AI agent' used like they're the same thing. They're not. One *answers*. The other *acts*. Let's fix that in three minutes — using Mistral Studio as our example."

**User note:** Write this on a sticky note: **Model = answers. Agent = acts.** Everything else in this lesson is just unpacking that one sentence.

---

## 1. The Model — a really smart friend who only speaks when spoken to (0:15–0:45)

**On screen (doodle):** a brain in a box. Someone knocks, asks a question, brain answers, box closes again.

**Narration:**
> "A model is like a brilliant friend you can only reach by text. Ask a question, get an answer. Ask it to 'find a cheaper flight and book it' — it can *describe* how, but it can't actually go do it. It has no hands."

**Everyday analogy:** Opening a blank Word document and typing "what's the capital of France?" into it. The document can hold the answer — it can't go look anything up for you.

---

## 2. The Agent — same brain, now with hands and a to-do list (0:45–1:20)

**On screen (doodle):** the same brain, now with stick-figure arms, holding a checklist, walking through an open door toward a row of labeled buttons: Calendar, Email, Spreadsheet.

**Narration:**
> "An agent is that same model, wired up to *tools* and given a goal instead of a question. Give it 'find a cheaper flight and book it,' and it checks a flights tool, compares prices, fills the booking form, and stops only when the ticket exists — not when it's said something clever."

**Office Suite analogy:** Think of an Excel **macro** you recorded once — it clicks the exact same five cells in the exact same order, every time, no matter what's actually in the sheet. That's a fixed script, not an agent. An agent is more like handing the job to a new hire and saying: *"Check the inventory sheet. If stock's below 10, draft the reorder email, send it, then update the tracker."* It decides each step from what it actually finds — and if row 12 looks different today, it adapts instead of blindly clicking the same five cells.

**Browser analogy:** You, clicking through ten tabs by hand, is a human doing the deciding. An autofill bot that fills one fixed form is a **hook** (one trigger, one action — more on that in a future episode). An agent is the browser assistant that reads *each* page as it loads, decides what to click next based on what's actually there, and keeps going across all ten tabs until the task is done — retrying if a page didn't load right.

**User note:** The tell isn't "does it use AI" — a spellchecker uses AI and isn't an agent. The tell is: **does it loop, decide, and act toward a goal without you clicking each step?**

---

## 3. Seeing it for real: Mistral Studio (1:20–2:10)

**On screen (doodle):** a robot standing inside a glass box (sturdy walls, a few cracks patched with tape — "it survives retries"). Around it: pegs labeled Tools, Connectors, Guardrails. Above it, a clipboard labeled "Logbook" writing down everything it does.

**Narration:**
> "Mistral Studio is a real place this happens. You don't just ask its model a question — you build an *agent* that runs inside what Mistral calls the **Agent Runtime**. That runtime is the glass box: it keeps the agent's task alive even through retries and multi-step jobs, so a hiccup halfway through doesn't lose the work."
>
> "The pegs are the hands: **tools and connectors** the agent can reach for — a database, a calculator, a search function. And the clipboard is **Observability** — every action the agent takes gets logged, so you can trace exactly *why* it did what it did, the same way you'd want a new employee's work written in a logbook you can check."

**Everyday analogy:** It's the difference between hiring someone and just leaving them a phone number. Mistral Studio hires the model: gives it a desk (the runtime), a toolbox (tools/connectors), and a supervisor's logbook (observability) — instead of just a line to call when you have a question.

**Source used for this section:** [Mistral Studio product page](https://mistral.ai/products/studio/) and [Mistral AI Studio announcement](https://mistral.ai/news/ai-studio/) — Agent Runtime (built on Temporal, for durable multi-step tasks), reusable blocks (agents, tools, connectors, guardrails), and Observability (tracing agent actions) are described there as Studio's core pillars.

---

## 4. Recap + memory hook (2:10–2:40)

**On screen (doodle):** side-by-side split panel. Left: the brain-in-a-box from Slide 1, labeled "MODEL — answers." Right: the brain-with-arms from Slide 2, now standing inside the Slide 3 glass box, labeled "AGENT — acts, with tools + a logbook."

**Narration:**
> "So: a model answers. An agent takes that same model, adds tools, a goal, and a loop, and lets it act — with every step logged so a human can check its work. That's it. That's the whole term."

**User note — the one-line mnemonic:**
> **"Model talks. Agent walks — and writes down where it went."**

---

## 5. Close + what's next (2:40–3:00)

**On screen (doodle):** a signpost with one arrow pointing back ("Episode 1: Agent ✓") and one pointing forward, blank, waiting to be labeled.

**Narration:**
> "Next episode, we'll cover **Hooks** — the AI equivalent of a doorbell: one trigger, one automatic action, no judgment involved. That's the piece that's *not* an agent, and knowing the difference is what makes the rest of this stuff click."

**On-screen text:** *AI Explained Simply — Episode 2: "Hooks" — coming next.*

---

## PowerPoint slide map (for the deck)

| # | Slide title | Visual | Speaker note source |
|---|---|---|---|
| 1 | Title — "What's an AI Agent?" | Doodle: brain in a box | Cold open |
| 2 | The Model: answers when asked | Doodle: brain in a box, knock-answer-close | Section 1 |
| 3 | The Agent: same brain, now with hands | Doodle: brain with arms + checklist + door | Section 2 |
| 4 | Office Suite analogy: macro vs. agent | Doodle: recorded-macro clicking loop vs. adaptive checklist | Section 2 |
| 5 | Browser analogy: autofill vs. agent | Doodle: ten tabs, one bot reading & deciding | Section 2 |
| 6 | Real example: Mistral Studio | Doodle: robot in glass box, tool pegs, logbook | Section 3 |
| 7 | Recap + mnemonic | Doodle: split panel, model vs. agent | Section 4 |
| 8 | Next up: Hooks | Doodle: signpost | Section 5 |

## User notes (print or keep beside the deck)

- **One sentence to remember:** Model = answers. Agent = acts (with tools, a goal, and a loop).
- **The test to apply to anything called "AI [X]":** does it loop, decide, and act on its own toward a goal — or does it just answer once when asked?
- **Real anchor:** Mistral Studio's *Agent Runtime* (the durable "workspace" an agent runs in), *tools/connectors* (its hands), and *Observability* (the logbook of what it did).
- **Don't confuse with:** a *hook* (fixed trigger → fixed action, no deciding) — that's next episode's term.

## Topic coverage tracker

**Covered so far (1):** AI Agent (Episode 1, 2026-07-18)

**Suggested next topics (in a sensible teaching order):**
1. **Hook** — a fixed trigger → fixed action (contrasts directly with "Agent," referenced above)
2. **Model** — the "brain" itself, weights and training, no tools attached
3. **Skill** — a packaged, reusable instruction set an agent can call on demand
4. **Memory** — how an agent keeps track of things across steps or sessions
5. **Tool / Connector** — the specific hands an agent reaches for (search, database, calendar)
6. **Prompt** — the instruction you give a model or agent to start it working
7. **Token** — the unit AI reads/writes text in, and why it affects cost and speed
8. **JSON** — the structured "form" agents and tools use to hand data to each other
9. **Fine-tuning vs. prompting** — teaching a model permanently vs. just asking it well
10. **Guardrail** — the fence that keeps an agent's actions inside safe bounds

*Recommendation: run "Hook" next — it is the direct contrast case set up in this episode's closing beat, so the audience arrives already primed for it.*
