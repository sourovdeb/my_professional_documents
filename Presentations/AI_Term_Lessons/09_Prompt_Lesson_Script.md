# AI Explained, Plain and Simple — Lesson 9: What Is a "Prompt"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 18, 2026*
*Series: AI Explained, Plain and Simple — Lesson 9 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> A **Prompt** is the actual instruction you hand a model or agent to make it do
> something *right now* — the specific ask, in plain words, that everything else
> (Memory, Skills, Hooks, Python code) just sits idle waiting for.

---

## Everyday analogy

Think about **a blank email, a browser's address bar, and ordering food at a
restaurant**:

- Open a new email in Outlook and the signature, the formatting, the address book are
  all already sitting there, fully set up — and none of it does anything until you
  actually type the message. That typed message is the Prompt: not the tool, not what
  it's capable of, just the specific ask.
- A browser sits open with your whole history and every bookmark already loaded —
  nothing happens until you type something into the address bar and hit enter. "Best
  pizza near me" is a Prompt: one specific request, handed to a system that was doing
  nothing until you asked.
- A fully stocked kitchen with a great chef changes nothing on its own. Walk up and
  say "a medium-rare steak, no onions" and *that* is what turns capability into a
  specific dish. The kitchen is the Model and Skills from earlier lessons; your order
  is the Prompt.
- In **Mistral Studio**, the Prompt is what actually tells the Agent box in our
  running chain what to do with the JSON that just arrived. The Hook can hand the
  Agent `{"file": "report.pdf"}` all day — nothing happens until a Prompt like
  "summarize this file and email the result to finance" is the specific instruction
  the Agent's underlying model is actually run with.

---

## Script (spoken narration, ~2m50s at a relaxed pace)

**[0:00–0:20] Hook**
"You've met Agent, Model, Memory, Skill, Hook, Workflow, JSON, and Python — the whole
machine. But none of it moves on its own. Something has to actually tell it what to
do, right now. That's a Prompt."

**[0:20–0:55] The everyday definition**
"A Prompt is just the specific instruction you hand a model or agent — plain words,
stating the actual ask. Not the model's knowledge, not its tools, not the code
underneath. Just: here's what I want, right now."

**[0:55–1:30] Office Suite analogy**
"Open a new email in Outlook and the signature, the formatting, the address book are
already sitting there, fully set up. None of it does anything until you type the
actual message. That typed message is the Prompt — everything else was just waiting."

**[1:30–1:55] Browser analogy**
"Or open a browser: your whole history and every bookmark are already loaded, and
nothing happens until you type something into the address bar and hit enter. 'Best
pizza near me' is a Prompt — one specific request, handed to a system that was
sitting idle until you asked."

**[1:55–2:15] Everyday-task analogy**
"Or think of a fully stocked kitchen with a great chef — on its own, it makes
nothing. Walk up and say 'a medium-rare steak, no onions,' and that's what turns
capability into an actual dish. The kitchen is the Model and Skills you already know;
your order is the Prompt."

**[2:15–2:40] Concrete example — Mistral Studio**
"In our running Mistral Studio chain, the Hook can hand the Agent
`{"file": "report.pdf"}` all day long — nothing happens until a Prompt, something
like 'summarize this file and email the result to finance,' is the actual instruction
the Agent's underlying model gets run with. The JSON is the data arriving; the
Prompt is what says what to *do* with it, right now."

**[2:40–3:00] Recap + teaser**
"So: a Prompt is the specific instruction that kicks off the work — layered on top
of whatever data and code already exist, and the one thing that turns a sitting-idle
system into action. Next time: the unit AI actually reads and writes text in, and why
it quietly controls cost and speed — Token. See you in Lesson 10."

---

## Scannable outline (for slides / written version)

1. **Hook** — you've met the whole machine (Agent, Model, Memory, Skill, Hook,
   Workflow, JSON, Python) — none of it moves until something tells it what to do,
   right now. That's a Prompt.
2. **Definition** — the specific instruction you hand a model or agent: plain words,
   stating the actual ask, not the tools or knowledge sitting behind it.
3. **Office Suite analogy** — a blank Outlook email: signature and formatting are
   ready, but nothing happens until you type the actual message.
4. **Browser analogy** — an open browser with history and bookmarks already loaded;
   nothing happens until you type into the address bar and hit enter.
5. **Everyday-task analogy** — a fully stocked kitchen with a great chef does
   nothing until you place a specific order.
6. **Real example: Mistral Studio** — the Hook can hand the Agent JSON all day;
   nothing happens until a Prompt tells the Agent's model what to actually do with it.
7. **Recap** — Prompt = the specific instruction that turns a sitting-idle system
   into action, layered on top of the data (JSON) and code (Python) already there.
8. **Next up** — Lesson 10: Token.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Speech bubble into a gear | A teal speech-bubble shape with short instruction text, an arrow into a navy gear/cog | "The specific instruction that makes the machine actually move." |
| 2 | Idle vs. asked | Two small panels: left, a dimmed/greyed box labeled "waiting…"; right, the same box lit up navy, labeled "on it" — joined by an arrow with a small speech-bubble icon on it | "Everything sits idle until a Prompt arrives." |
| 3 | Blank email card | A rounded card mimicking an email compose window — signature line already filled in grey, subject/body blank except one typed teal line | "The signature was ready. Nothing happened until you typed the message." |
| 4 | Address bar | A rounded browser chrome bar with three corner dots, a teal typed line "best pizza near me", and a small arrow/enter icon | "One line, hit enter — that's a Prompt." |
| 5 | Order ticket | A small ticket/receipt shape reading "medium-rare, no onions" with a chef's hat icon beside it | "The kitchen could do it all along. The order is what makes it happen." |
| 6 | Mistral Studio chain with Prompt tag | Same Hook → Agent → Skill → Notify chain as Lessons 6–8, with the `{ }` (JSON) and `<>` (Python) tags from Lesson 8, plus a new small speech-bubble tag directly over the Agent box | "The Prompt is what tells the Agent's model what to do with the JSON that just arrived." |
| 7 | Checkmark + signpost | A checkmark badge, an arrow pointing onward labeled "Token" | "Today: Prompt. Next time: Token — the unit AI actually reads and writes in." |

---

## User / speaker notes

- This lesson assumes the viewer has seen Lessons 1–8 — it treats Agent, Model,
  Memory, Skill, Hook, Workflow, JSON, and Python as already-familiar vocabulary. If
  used standalone, add one sentence recapping "Python" before the hook, since Prompt
  is framed as the missing ingredient that makes that code actually do something.
- Doodle 2 (idle vs. asked) is the crux visual — it's the cleanest single image for
  "nothing happens without a Prompt." Hold it a beat longer than the others.
- Keep the on-screen prompt example to one short, concrete line (as in the script) —
  avoid a long multi-paragraph prompt; the goal is to show the *shape* of an
  instruction, not to teach prompt-engineering technique (that's a later, deeper
  topic, not this lesson).
- If delivering as a written lesson instead of video: keep the table above inline as
  the illustrations, one per section.
- Total runtime target: 2m50s narrated, stretchable to ~4m with pauses for doodles.
- Sources for the Mistral Studio claims: this lesson continues the fictional-but-
  consistent Hook → Agent → Skill → Notify worked example built up across Lessons
  6–8 in this same series, rather than citing new external Mistral Studio product
  documentation — keep that continuity rather than reintroducing outside claims.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6) → JSON (Lesson 7) → Python
(Lesson 8) → Prompt (Lesson 9)
**This lesson starts the second batch**, suggested at the end of Lesson 8:
`Prompt → Token → Context Window → API → Fine-tuning`.
**Suggested next topic:** Token — "the unit AI actually reads and writes text in, and
why it quietly controls cost and speed."
**Later candidates, in a sensible teaching order:** Context Window → API →
Fine-tuning.
