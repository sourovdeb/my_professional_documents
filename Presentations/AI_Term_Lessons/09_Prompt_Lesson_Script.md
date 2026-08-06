# AI Explained, Plain and Simple — Lesson 9: What Is a "Prompt"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 21, 2026*
*Series: AI Explained, Plain and Simple — Lesson 9 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> A **prompt** is the instruction you actually type (or say) to a model or agent to get
> it moving — words in, an answer or an action out, and how precise those words are
> decides how precise the result is.

---

## Everyday analogy

Think about a **search engine's search bar, an email to a very literal assistant, and
giving directions to a taxi driver**:

- Type "restaurant" into a search bar and you get thousands of unfocused results. Type
  "vegetarian restaurant open now near Gare de Lyon" and you get three good ones. Same
  search bar, same engine underneath — the only thing that changed is the prompt, and
  that's what changed the answer.
- Email a very literal new assistant "send that thing to the client" and you'll get a
  confused reply back. Email "send the July invoice PDF to client@example.com with the
  subject 'Invoice — July 2026'" and it's just done. The assistant didn't get smarter —
  the instruction got more specific.
- Tell a taxi driver "somewhere nice" and you'll circle the block. Tell them "Rue de
  Rivoli, number 12, the blue door" and you're there in five minutes. A prompt is
  exactly that: the destination you actually state, out loud, instead of leaving the
  driver to guess.
- **Prompt** is that same idea aimed at Lesson 1's model and agent. The model or agent
  from Lessons 1–8 doesn't do anything until a prompt arrives — the System Prompt sets
  its standing instructions (like a driver's standing orders — "always take the
  fastest route, avoid tolls"), and the User Prompt is the specific ride requested each
  time ("Rue de Rivoli, number 12"). Vague in, vague out. Specific in, specific out.

---

## Script (spoken narration, ~2m50s at a relaxed pace)

**[0:00–0:20] Hook**
"Every Agent, Model, Skill, and Hook you've met so far has to be *told* what to do
before it does anything. The thing that tells it? That's a prompt — and it's the
single biggest lever you actually control."

**[0:20–0:55] The everyday definition**
"A prompt is just the words you type or say to a model or agent to get it started.
Nothing happens before it, and what happens after it depends entirely on how precise
those words are. Vague prompt in, vague result out. Specific prompt in, specific
result out — same model, same agent, different words."

**[0:55–1:35] Office Suite analogy**
"You've felt this already: email a new assistant 'send that thing to the client' and
you'll get a confused reply. Email 'send the July invoice PDF to
client@example.com, subject Invoice — July 2026' and it's just done. The assistant
didn't get any smarter between those two emails — the instruction did."

**[1:35–2:05] Browser analogy**
"Or open any search engine. Type 'restaurant' and you get a wall of noise. Type
'vegetarian restaurant open now near Gare de Lyon' and you get three good answers.
Same search bar, same engine — the prompt is the only thing that changed, and that's
what changed the result."

**[2:05–2:20] Everyday-task analogy**
"Or think about telling a taxi driver 'somewhere nice' versus 'Rue de Rivoli, number
12, the blue door.' One gets you circling the block. The other gets you there in five
minutes. A prompt is the destination you actually say out loud, instead of leaving the
driver — or the model — to guess."

**[2:20–2:50] Concrete example — Mistral Studio**
"In Mistral Studio, this shows up as two boxes when you build an agent. The **System
Prompt** is the standing instruction, set once — like telling a driver 'always take
the fastest route, avoid tolls' before the ride even starts. The **User Prompt** is
each specific ride you ask for after that — 'Rue de Rivoli, number 12.' Every box in
Lesson 6's Hook → Agent → Skill → Notify chain starts from a prompt just like this —
that's what tells it what today's job actually is."

**[2:50–3:10] Recap + teaser**
"So: a prompt is the words you hand a model or agent to get it moving — and how
precise those words are decides how precise the result is. It's the one lever you
control every single time. Next time: the units a model actually reads those words
in — Token. See you in Lesson 10."

---

## Scannable outline (for slides / written version)

1. **Hook** — every Agent, Model, Skill, and Hook you've met needs to be told what to
   do first — that's a prompt, and it's the biggest lever you control.
2. **Definition** — the words you type or say to a model or agent to get it started;
   vague words in, vague result out — specific words in, specific result out.
3. **Office Suite analogy** — an email to a literal assistant: "send that thing" gets
   confusion, a fully specific request just gets done.
4. **Browser analogy** — a search bar: "restaurant" is noise, "vegetarian restaurant
   open now near Gare de Lyon" is three good answers — same engine, different prompt.
5. **Everyday-task analogy** — a taxi driver: "somewhere nice" circles the block, "Rue
   de Rivoli, number 12" gets you there in five minutes.
6. **Real example: Mistral Studio** — the System Prompt (standing instructions, set
   once) and the User Prompt (the specific ask each time) are what start every box in
   the Hook → Agent → Skill → Notify chain.
7. **Recap** — Prompt = the words that start a model or agent moving, and precision in
   is precision out.
8. **Next up** — Lesson 10: Token.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Speech bubble into a box | A large teal speech bubble with "?" flowing through an arrow into a small navy box labeled `MODEL`, which lights up gold | "Words in — that's what wakes the model or agent up." |
| 2 | Vague vs. specific arrows | Two parallel arrows: a wavy, thin, grey arrow labeled "restaurant" ending in a scattered cloud of dots; a straight, bold teal arrow labeled "vegetarian, open now, near Gare de Lyon" ending in one gold pin | "Vague prompt in, scattered result out. Specific prompt in, one exact result out." |
| 3 | Email envelope, two versions | A grey envelope reading "send that thing to the client" with a confused "?" reply below it; a teal envelope reading "send July invoice PDF, subject: Invoice — July 2026" with a green checkmark reply below it | "Same assistant, same inbox — the only thing that changed is the prompt." |
| 4 | Search bar, two queries | A rounded search-bar mock; top row shows "restaurant" with a scattered results icon; bottom row shows the full specific query with three clean pin icons | "Same search bar, same engine — the prompt decides how good the answer is." |
| 5 | Taxi with two destinations | A small taxi icon with two speech-bubble destinations above it: "somewhere nice" (dotted, circling arrow back to itself) and "Rue de Rivoli, 12, blue door" (straight teal arrow to a gold pin) | "Vague destination, circling the block. Exact address, five minutes." |
| 6 | Mistral Studio chain with two prompt tags | The familiar File → Hook → Agent → Skill → Notify chain from Lessons 6–8, now with a small navy "System Prompt" plate mounted above the Agent box (set once) and a small teal "User Prompt" speech bubble feeding into it (asked each time) | "System Prompt sets the standing rules. User Prompt is the specific ask — together they start the whole chain." |
| 7 | Checkmark + signpost | A checkmark badge, an arrow pointing onward labeled "Token" | "Today: Prompt. Next time: Token — the units a model actually reads those words in." |

---

## User / speaker notes

- This lesson assumes the viewer has seen Lessons 1–8 (Agent, Model, Memory, Skill,
  Hook, Workflow, JSON, Python) — it treats those as already-familiar vocabulary. If
  used standalone, add one sentence recapping "Agent" before the hook, since a prompt
  is framed as the thing that starts an agent or model moving.
- Doodle 3 (the two emails) is the crux visual — nearly everyone has sent or received
  a vague work email, so hold it a beat longer than the search-bar doodle that follows.
- Keep the on-screen prompt examples short and concrete (one search query, one email
  subject line) — avoid a long multi-paragraph prompt example for beginners; the goal
  is to show the *shape* of "vague vs. specific," not to teach prompt-engineering
  technique.
- If delivering as a written lesson instead of video: keep the table above inline as
  the illustrations, one per section.
- Total runtime target: 2m50s narrated, stretchable to ~4m with pauses for doodles and
  a short live demo of typing the same request two ways into a search bar.
- Sources for the Mistral Studio claims: general agent-platform conventions
  (separating a standing "system" instruction from each turn's "user" instruction) —
  verify the exact current System Prompt / User Prompt field names and behavior in
  Mistral Studio's own documentation before quoting them as a specific product claim.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6) → JSON (Lesson 7) → Python
(Lesson 8) → Prompt (Lesson 9)
**This is the first lesson of the second batch**, suggested in Lesson 8's index note:
`Prompt → Token → Context Window → API → Fine-tuning`.
**Suggested next topic:** Token — "the units a model actually reads and writes text
in, and why it affects cost and speed."
**Later candidates, in a sensible teaching order:** Context Window → API →
Fine-tuning.
