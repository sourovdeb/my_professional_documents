# AI Explained, Plain and Simple — Lesson 6: What Is a "Workflow"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 17, 2026*
*Series: AI Explained, Plain and Simple — Lesson 6 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> A **Workflow** is a saved chain of steps — Hooks, Agents, and Skills, strung
> together in order — so one trigger sets off the whole sequence automatically,
> instead of you running each piece by hand.

---

## Everyday analogy

Think about an **Outlook rule with several chained actions, an online checkout, and a
coffee maker**:

- A simple inbox rule does one thing: move a message. But Outlook also lets you chain
  actions onto one trigger — "if sender is X: move it, AND forward it, AND flag it,
  AND create a follow-up task" — four separate actions, one trigger, always in the
  same order, no re-clicking between them.
- An online checkout is the same shape from the customer's side: cart hands off to
  shipping, shipping hands off to payment, payment hands off to confirmation. Each
  page's output becomes the next page's input, automatically, without you re-typing
  anything or restarting.
- A coffee maker with a "brew" button is the clearest version: press once, and grind
  → brew → keep-warm happen in sequence, each stage starting only after the one
  before it finishes, with nobody standing there operating three separate machines.
- A **Workflow** is that exact shape, applied to Lessons 1–5: instead of one Hook
  firing one Agent that uses one Skill, a Workflow chains several of them —
  Hook → Agent → Skill → Hook again — into a single saved sequence. Nothing about what
  an Agent, Skill, or Hook *is* changes; a Workflow just decides *what runs next after
  what*.

---

## Script (spoken narration, ~2m55s at a relaxed pace)

**[0:00–0:20] Hook**
"You've met Agent, Model, Memory, Skill, and Hook. Every one of those, so far, has been
one piece acting alone. But what happens when a trigger needs to set off several
pieces, in order, without you babysitting each handoff? That's a Workflow."

**[0:20–0:55] The everyday definition**
"A Workflow is a saved sequence: step one finishes, its result feeds step two, step
two finishes, its result feeds step three — all from one starting trigger, with no
person re-clicking 'go' in between. It's not a new kind of building block; it's the
wiring between the blocks you already know."

**[0:55–1:35] Office Suite analogy**
"You've probably seen the seed of this in Outlook. A basic rule does one thing — move
a message. But you can chain actions onto a single rule: if the sender is my
accountant, move it to Finance, AND forward it to my bookkeeper, AND flag it, AND
create a follow-up task. Four actions, one trigger, always the same order. That's a
Workflow in miniature, already sitting in your inbox settings."

**[1:35–2:05] Browser analogy**
"Or think about any online checkout. Cart hands off to shipping. Shipping hands off to
payment. Payment hands off to confirmation. You never re-enter your address on the
payment page — each step's output is already sitting there, waiting, because the
pages are chained. A Workflow chains Agents and Skills the exact same way."

**[2:05–2:25] Everyday-task analogy**
"Or simplest of all: a coffee maker with one 'brew' button. Press it once, and grind,
brew, and keep-warm happen in order, each starting only when the last one finishes.
You don't operate three machines — you press one button and walk away."

**[2:25–2:55] Concrete example — Mistral Studio**
"In Mistral Studio, this is what turns a single automation into a real pipeline: a
Hook notices a new file lands in a connected library, that triggers an Agent to draft
a summary, the Agent calls on a Skill to format it correctly, and a final step notifies
you it's ready — all chained from that one file arriving. You configure the chain
once, in order; after that, one trigger runs the whole thing."

**[2:55–3:15] Recap + teaser**
"So: a Workflow is a saved chain of steps — Hooks, Agents, Skills — where one trigger
sets off the whole sequence, each step handing its result to the next. It's what turns
separate building blocks into one automatic pipeline. Next time: the plain-text format
almost every one of these tools uses to actually pass that data between steps — JSON.
See you in Lesson 7."

---

## Scannable outline (for slides / written version)

1. **Hook** — Agent, Model, Memory, Skill, and Hook have all been one piece acting
   alone so far — a Workflow is what happens when a trigger needs to set off several
   of them, in order.
2. **Definition** — a saved sequence: each step's result feeds the next step, from one
   starting trigger, with no person re-clicking "go" in between.
3. **Office Suite analogy** — an Outlook rule with chained actions: move it, AND
   forward it, AND flag it, AND create a task — one trigger, several ordered actions.
4. **Browser analogy** — an online checkout: cart → shipping → payment → confirmation,
   each page's output already waiting on the next.
5. **Everyday-task analogy** — a coffee maker's "brew" button: grind → brew →
   keep-warm, one press, three stages, no one operating three machines.
6. **Real example: Mistral Studio** — a new file triggers a Hook, which starts an
   Agent, which calls a Skill to format the result, which notifies you — all chained
   from one trigger.
7. **Recap** — Workflow = the wiring between Agents, Skills, and Hooks; it decides
   *what runs next after what*, not what any single piece does.
8. **Next up** — Lesson 7: JSON.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Three chained nodes | Three connected circles, small curved arrows linking them left to right | "Several steps, chained — that's a workflow." |
| 2 | GO box into a pipeline | A "GO" box on the left, three plain circles in a row, arrows carrying straight through to the end | "One trigger. Every step fires in order, automatically." |
| 3 | Inbox rule fanning out | An envelope with three arrows branching to three action boxes: Move, Forward, Flag | "One trigger, several chained actions — already in your inbox." |
| 4 | Browser checkout pipeline | A browser window containing four boxes in sequence: Cart, Ship, Pay, Done, connected by arrows | "Each page hands its result to the next — nothing re-entered." |
| 5 | Coffee stations | Three circles — Grind, Brew, Cup — connected by gold arrows | "Press once. Three stages run themselves, in order." |
| 6 | Mistral Studio chain | A studio box containing five linked circles: File, Hook, Agent, Skill, Notify | "New file lands → the whole chain runs itself, no restarting between steps." |
| 7 | Checkmark + signpost | A checkmark badge, an arrow pointing onward labeled "JSON" | "Today: Workflow. Next time: JSON — the format the steps actually pass to each other." |

---

## User / speaker notes

- This lesson assumes the viewer has seen Lessons 1–5 (Agent, Model, Memory, Skill,
  Hook) — it treats "agent," "skill," and "hook" as already-familiar vocabulary. If
  used standalone, add one sentence recapping those three terms before the hook.
- Doodle 3 (inbox rule fanning out) is the crux visual — it's the one analogy nearly
  every viewer has already configured themselves, so hold it a beat longer than the
  others.
- If delivering as a written lesson instead of video: keep the table above inline as
  the illustrations, one per section.
- Total runtime target: 2m55s narrated, stretchable to ~4m with pauses for doodles and
  a short live look at Mistral Studio's workflow/chaining settings.
- Sources for the Mistral Studio claims: general agent-platform automation-chaining
  patterns (trigger → agent → formatting step → notification) — verify the exact
  current UI/feature name in Mistral Studio's own documentation before quoting it as a
  specific product claim.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6)
**Suggested next topic:** JSON — "the plain-text format almost every one of these
tools actually uses to pass data between steps."
**Later candidates, in a sensible teaching order:** Python
