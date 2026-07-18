# AI Explained, Plain and Simple — Lesson 8: What Is "Python"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 18, 2026*
*Series: AI Explained, Plain and Simple — Lesson 8 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> **Python** is the plain, readable programming language that most of these tools —
> Agents, Skills, Hooks, Workflows — are actually written in: a list of instructions,
> one per line, that the computer runs in order, exactly as written, every single time.

---

## Everyday analogy

Think about an **Excel formula bar, a browser's console tab, and a recipe card**:

- A formula like `=SUM(A1:A10)` is already a tiny program: it names cells, states one
  operation, and Excel follows it exactly, in order, every time you open the sheet.
  Python is that same idea, freed from a single cell — a whole page of ordered
  instructions instead of one formula, but the same relationship between what's typed
  and what the computer does.
- Open any browser's developer tools and click the Console tab. Type a line of code
  and it runs immediately, exactly as typed — nothing is left to guesswork. Python is
  that same relationship between typed instructions and a computer obeying them,
  usually running behind the scenes instead of inside a webpage.
- A recipe's steps aren't a pile of options to pick from — they're numbered and done
  in order: preheat, then mix, then bake. Step 2 waits for step 1. Python reads the
  same way: line 1, then line 2, then line 3, run in that exact order, every time.
- **Python** is that shape, applied to Lessons 6–7's chain: the Hook, Agent, Skill, and
  Notify boxes that pass each other JSON aren't magic — every one of those boxes *is*
  Python code, reading the JSON that arrives, deciding what to do about it, and calling
  the next box. JSON is the data moving on the arrows; Python is the code doing the
  reading and deciding inside each box.

---

## Script (spoken narration, ~2m50s at a relaxed pace)

**[0:00–0:20] Hook**
"You've met Agent, Model, Memory, Skill, Hook, Workflow, and JSON. Every one of those
boxes — a Hook, an Agent, a Skill — has to actually be built out of something. Almost
always, that something is Python."

**[0:20–0:55] The everyday definition**
"Python is just a list of instructions, one per line, written as plain, readable text.
The computer runs them top to bottom, in order, exactly as written — no guessing, no
skipping. It's not a new kind of building block; it's the language the blocks you
already know are actually written in."

**[0:55–1:35] Office Suite analogy**
"You've already written a tiny program without calling it one. Type `=SUM(A1:A10)`
into Excel and it names some cells, states one operation, and runs it exactly, every
time. Python is that same idea, just not stuck in one cell — a whole page of ordered
steps instead of a single formula."

**[1:35–2:05] Browser analogy**
"Or open any webpage's developer tools and click the Console tab. Type a line of code
and watch it run immediately, exactly as typed. Python is that same relationship
between typed instructions and a computer obeying them — usually running quietly
behind the scenes, rather than inside a webpage where you can watch it."

**[2:05–2:20] Everyday-task analogy**
"Or think of a recipe: the steps aren't options, they're numbered and done in order —
preheat, then mix, then bake. Step 2 waits for step 1 to finish. Python runs the same
way: one line at a time, top to bottom, in the exact order it's written."

**[2:20–2:50] Concrete example — Mistral Studio**
"In Mistral Studio, this is what's actually inside Lesson 6's chain. When a Hook
notices a new file and hands the Agent `{"file": "report.pdf"}`, that Hook and that
Agent are Python code — reading the JSON that just arrived, deciding what to do, and
calling the next step. The JSON from Lesson 7 is the data moving on the arrows;
Python is the code doing the work inside every box."

**[2:50–3:10] Recap + teaser**
"So: Python is the plain-text language of ordered instructions — one line, then the
next, run exactly as written — that most Agents, Skills, Hooks, and Workflows are
actually built in. It's not a new building block; it's the language the blocks
already use. That closes out our original list of terms. Next time: the instruction
you actually hand the model to get it started — Prompt. See you in Lesson 9."

---

## Scannable outline (for slides / written version)

1. **Hook** — every Agent, Skill, Hook, and Workflow you've met has to be built out of
   something — almost always, that something is Python.
2. **Definition** — a list of plain-text instructions, one per line, run top to bottom,
   in order, exactly as written.
3. **Office Suite analogy** — an Excel formula bar: `=SUM(A1:A10)` is already a tiny
   program; Python is that same idea, freed from a single cell.
4. **Browser analogy** — a browser's Console tab: type a line, watch it run instantly;
   Python is the same relationship, usually running behind the scenes.
5. **Everyday-task analogy** — a recipe card: numbered steps, done in order, step 2
   waiting on step 1 — the same way Python runs line by line.
6. **Real example: Mistral Studio** — every box in the Hook → Agent → Skill → Notify
   chain is Python code reading the JSON that arrives and calling the next step.
7. **Recap** — Python = the readable, ordered language the blocks from Lessons 1–7 are
   actually written in, not a new block itself.
8. **Next up** — Lesson 9: Prompt.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Parentheses with a call | Large teal `(` and `)` with one small navy/teal pill `agent.run()` centered between them | "Ordered instructions, run exactly as written — that's Python." |
| 2 | Stacked numbered steps | Three rows, each a small navy "1 / 2 / 3" badge and a teal instruction pill, joined by short down-arrows, inside a loose teal-outlined box | "Every line is one instruction — and they run in exactly this order." |
| 3 | Formula bar → code lines | A rounded "fx" formula-bar mock reading `=SUM(A1:A10)`, an arrow, then a small code panel with three Courier lines | "Already familiar — a formula is a tiny program; Python is the same idea, scaled up." |
| 4 | Browser console flow | A browser window (rounded rect + 3 corner dots) with a `>>>` console prompt line and a result line below it | "Type a line, it runs instantly — Python usually does this behind the scenes instead." |
| 5 | Recipe card with numbered steps | A card headed "Steps" with three numbered rows: Preheat, Mix, Bake | "Numbered, in order, step 2 waits on step 1 — same as a line of Python." |
| 6 | Mistral Studio chain with Python + JSON tags | Same File → Hook → Agent → Skill → Notify chain as Lessons 6–7, with a small `{ }` tag on each arrow (JSON) and a small `<>` tag on each box (Python) | "JSON on the arrows is the data; Python inside the boxes is the code reading it." |
| 7 | Checkmark + signpost | A checkmark badge, an arrow pointing onward labeled "Prompt" | "Today: Python. Next time: Prompt — the instruction you actually hand the model." |

---

## User / speaker notes

- This lesson assumes the viewer has seen Lessons 1–7 (Agent, Model, Memory, Skill,
  Hook, Workflow, JSON) — it treats those six terms as already-familiar vocabulary. If
  used standalone, add one sentence recapping "JSON" before the hook, since Python is
  framed as the language that writes the code moving that JSON around.
- Doodle 3 (formula bar → code) is the crux visual — nearly every viewer has typed an
  Excel formula, so hold it a beat longer than the others before moving to the
  browser-console doodle.
- Keep the on-screen Python example to one short line (`agent.run()`, `total += cell`)
  — avoid showing a full script for beginners; the goal is to show the *shape* of
  instructions, not to teach syntax.
- If delivering as a written lesson instead of video: keep the table above inline as
  the illustrations, one per section.
- Total runtime target: 2m50s narrated, stretchable to ~4m with pauses for doodles and
  a short live demo of a browser's Console tab or an Excel formula bar.
- Sources for the Mistral Studio claims: general agent-platform implementation
  patterns (agent/skill/hook logic implemented in Python) — verify the exact current
  implementation language in Mistral Studio's own documentation before quoting it as a
  specific product claim.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6) → JSON (Lesson 7) → Python
(Lesson 8)
**This closes the original seed list from the task brief** (`memory, hook, skill,
agent, model, JSON, Python`).
**Suggested next topic:** Prompt — "the instruction you actually hand the model to
get it started."
**Later candidates, in a sensible teaching order:** Token → Context Window → API →
Fine-tuning.
