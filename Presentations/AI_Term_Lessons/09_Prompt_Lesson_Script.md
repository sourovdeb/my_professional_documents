# AI Explained, Plain and Simple — Lesson 9: What Is a "Prompt"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 24, 2026*
*Series: AI Explained, Plain and Simple — Lesson 9 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> A **prompt** is the message you actually hand the model — your ask, the details that
> pin it down, and any example of what "good" looks like — and it is the single biggest
> lever you have on what comes back, because the model sees only what you typed, never
> what you meant.

---

## Everyday analogy

Think about **an email brief to a colleague, a search box, and ordering food**:

- Send a colleague an email that says "handle the report" and you'll get something —
  probably not what you pictured. Send one with the deadline, the audience, the three
  points to cover, and last month's report attached as a sample, and you'll get close
  to what you wanted. Same colleague, same skill — the difference was entirely in the
  brief. A prompt is that brief, written to a model instead of a person.
- Type "restaurant" into a search box and you get a million results; type "cheap thai
  restaurant open now near the station" and you get the one you needed. The engine
  didn't get smarter between the two searches — the query got clearer. A prompt is a
  search query with room to stretch out: full sentences, background, constraints,
  even examples.
- Order "some food" at a café and the kitchen has to guess. Order "a 20-minute
  vegetarian pasta for two, no mushrooms" and the same kitchen nails it. The cook's
  skill never changed; the order did.
- One honest demystifier while we're here: a model is not a mind-reader and not magic —
  it's a huge pile of stored patterns (think of a hard drive full of everything it
  read) plus very fast math on graphics chips, like a friend who has read a whole
  library in many languages. It's brilliant at fetching and recombining what's in
  there — but *what to fetch, for whom, and why* has to come from your head. That's
  exactly what the prompt is: the place where your thinking enters the machine.

---

## Script (spoken narration, ~2m55s at a relaxed pace)

**[0:00–0:20] Hook**
"You've met the Agent, the Model, and the pieces they're built from. But every single
one of them sits idle until somebody types something. That something has a name: the
prompt. And it's the one part of AI that's entirely in your hands."

**[0:20–0:55] The everyday definition**
"A prompt is just the message you hand the model: what you want, the details that pin
it down, and — if you have one — an example of what a good answer looks like. Here's
the catch: the model sees only the words you typed. Not your situation, not your
taste, not what you meant to say. Vague words in, vague answer out."

**[0:55–1:30] Office Suite analogy**
"You already write prompts every day — they're called emails. 'Handle the report'
gets you a guess. Deadline, audience, three points to cover, plus last month's report
as a sample, gets you almost exactly what you pictured. Same colleague, same skill —
only the brief changed. A prompt is that brief, written to a model."

**[1:30–1:55] Browser analogy**
"Or think of a search box. 'Restaurant' gives you a million results; 'cheap thai
restaurant open now near the station' gives you the one you needed. The engine never
got smarter — the query got clearer. A prompt is a search query with room to stretch
out: sentences, background, constraints, even examples."

**[1:55–2:15] Everyday-task analogy**
"Or ordering food. 'Some food' makes the kitchen guess; 'a 20-minute vegetarian pasta
for two, no mushrooms' gets nailed. The cook's skill never changed. The order did."

**[2:15–2:40] Concrete example — Mistral Studio**
"In Mistral Studio you meet prompts in two places. The chat box, where every message
you send is a prompt for that one answer. And the agent's Instructions box, where you
write a prompt once — 'you summarize reports for busy teachers, plain language, five
bullets' — and it quietly steers every single run of Lesson 6's Hook → Agent → Skill
chain from then on. Same model underneath; the written instructions are what make it
*your* agent."

**[2:40–2:55] Recap + teaser**
"So: the model is stored patterns plus fast math — the prompt is where your thinking
gets in. Clearer ask, closer answer. Next time: what the model actually does with
your words the moment you hit send — it chops them into pieces called Tokens. See
you in Lesson 10."

---

## Scannable outline (for slides / written version)

1. **Hook** — every Agent and Model sits idle until somebody types something; that
   something is the prompt, and it's the part of AI entirely in your hands.
2. **Definition** — the message you hand the model: the ask + the pinned-down details
   + an example of "good." The model sees only what you typed, never what you meant.
3. **Office Suite analogy** — an email brief: "handle the report" vs. deadline +
   audience + sample attached. Same colleague, different brief, different result.
4. **Browser analogy** — a search query: "restaurant" vs. "cheap thai open now near
   the station." The engine didn't get smarter; the query got clearer.
5. **Everyday-task analogy** — ordering food: "some food" makes the kitchen guess;
   a precise order gets nailed. The cook's skill never changed.
6. **Real example: Mistral Studio** — the chat box (a prompt per message) and the
   agent's Instructions box (one written prompt steering every run of the Lesson 6
   chain).
7. **Recap** — model = stored patterns + fast math; prompt = where your thinking
   enters. Clearer ask, closer answer.
8. **Next up** — Lesson 10: Token.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Chat box with cursor | A large rounded input pill with a blinking-cursor line and a gold send arrow, a small robot head waiting to its right | "Everything starts with what you type here." |
| 2 | Three-part message | One speech bubble split into three labeled bands: ASK / DETAILS / EXAMPLE, an arrow to a robot head | "A good prompt carries all three — the model sees only these words." |
| 3 | Two email briefs | Two Outlook-style email cards: a short vague one ("handle the report") with a shrug reply, a full one (To / Subject / 3 bullet lines / 📎 sample) with a checkmark reply | "Same colleague, same skill — only the brief changed." |
| 4 | Two search boxes | A browser window with two search bars: "restaurant" → a messy pile of result lines; the long specific query → one highlighted result | "The engine didn't get smarter. The query got clearer." |
| 5 | Two order slips | Two café order tickets: "some food??" vs. "pasta · veggie · 20 min · for 2 · no 🍄", the second stamped with a check | "The cook never changed. The order did." |
| 6 | Instructions box feeding the chain | The familiar File → Hook → Agent → Skill → Notify chain, with a gold "Instructions" card above the Agent box and a dashed arrow dropping into it | "One written prompt, steering every run." |
| 7 | Checkmark + signpost | A checkmark badge "Prompt — done", an arrow pointing onward labeled "Token" | "Today: Prompt. Next: Token — what the model chops your words into." |

---

## User / speaker notes

- This lesson assumes Lessons 1–8 vocabulary (Agent, Model, Skill, Hook, Workflow) is
  familiar. Used standalone, add one sentence recapping "Agent" before slide 6, since
  the Mistral Studio example leans on Lesson 6's chain.
- Doodle 3 (the two email briefs) is the crux visual — everyone has written a vague
  email and been disappointed by the reply. Hold it a beat longer than the others.
- The demystifier ("stored patterns + fast math, not a mind-reader") is deliberately
  placed in the definition and recap, not as a separate slide — keep the tone matter-
  of-fact, not conspiratorial: the point is that *your* head supplies the direction,
  which is empowering, not scandalous.
- Keep on-screen prompt examples to one short line each; the goal is the *shape* of a
  good prompt (ask + details + example), not prompt-engineering technique — that can
  be its own later lesson.
- If delivering as a written lesson instead of video: keep the doodle table inline as
  the illustrations, one per section.
- Total runtime target: 2m55s narrated, stretchable to ~4m30s with pauses on doodles
  and a short live demo of typing the same ask twice (vague, then specific) in
  Mistral Studio's chat.
- Sources for the Mistral Studio claims: the platform's standard agent-builder layout
  (an instructions/system-prompt field on the agent, plus a chat/playground input) —
  verify the current field names in Mistral Studio's own documentation before quoting
  them as exact UI labels.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6) → JSON (Lesson 7) → Python
(Lesson 8) → **Prompt (Lesson 9)**
**Suggested next topic:** Token — "the pieces the model actually chops your words
into (and why every tool has a token limit)."
**Later candidates, in a sensible teaching order:** Token → Context Window → API →
Fine-tuning → RAG.
