# AI Explained, Plain and Simple — Lesson 7: What Is "JSON"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 18, 2026*
*Series: AI Explained, Plain and Simple — Lesson 7 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> **JSON** is the plain-text format almost every one of these tools — Agents, Skills,
> Hooks, Workflows — actually uses to write down data, as simple labeled pairs like
> `"name": "value"`, so one step can hand its result to the next without any guesswork.

---

## Everyday analogy

Think about an **Outlook contact card, a browser's "page data," and a recipe card**:

- An Outlook contact isn't a paragraph of prose — it's labeled fields: Name: ,
  Email: , Phone: . You always know which value is which, because each one has a
  label attached to it. JSON is that exact shape, written as text: `"name": "Sourov"`,
  `"email": "..."`.
- Your browser already speaks this format constantly. Open any modern webpage's
  developer tools and watch the Network tab — most of what your browser quietly
  downloads to build the page isn't more webpage, it's JSON: labeled data the page's
  code reads and displays.
- A recipe card is the same idea with a list folded in: "Ingredients: flour, eggs,
  milk" isn't one field, it's a label pointing at a *list* of values. JSON does this
  too — a value can itself be a list, nested right inside the pair.
- **JSON** is that shape, applied to Lesson 6's Workflow: when a Hook triggers an
  Agent, or an Agent hands a Skill its input, the thing actually moving between them
  is JSON — a small labeled package like `{"file": "report.pdf", "status": "ready"}`.
  Nothing about what an Agent, Skill, Hook, or Workflow *does* changes; JSON is just
  the envelope they write their data into to hand it to each other.

---

## Script (spoken narration, ~2m50s at a relaxed pace)

**[0:00–0:20] Hook**
"You've met Agent, Model, Memory, Skill, Hook, and Workflow. Every time one of those
hands data to another — a Hook triggering an Agent, an Agent calling a Skill — that
data has to be written down in *some* format both sides understand. That format is
almost always JSON."

**[0:20–0:55] The everyday definition**
"JSON is just labeled pairs, written as plain text: a name in quotes, a colon, then
the value — `"status": "ready"`. Wrap a few pairs in curly braces and you have one
object. It's not a new kind of building block; it's the plain-text envelope the
blocks you already know use to pass data to each other."

**[0:55–1:35] Office Suite analogy**
"You've seen this shape a thousand times without naming it. An Outlook contact card
is never one blob of text — it's Name: , Email: , Phone: , each value sitting next to
its own label. JSON writes that exact idea as text: `"name": "Sourov"`,
`"email": "sourov@example.com"`. Same shape, just typed out so a computer can read it
too."

**[1:35–2:05] Browser analogy**
"Or open any webpage's developer tools and click the Network tab. Most of what your
browser fetches to build that page isn't more webpage — it's JSON, labeled data the
page's own code unpacks and displays. You've been *using* JSON every time you've
opened a browser; you've just never had to look at it directly."

**[2:05–2:20] Everyday-task analogy**
"Or think of a recipe card: 'Ingredients:' isn't one value, it's a label pointing at
a whole list — flour, eggs, milk. JSON does that too — a value can be a list, nested
right inside the pair, the same way a recipe nests its ingredient list inside one
card."

**[2:20–2:50] Concrete example — Mistral Studio**
"In Mistral Studio, this is the envelope every step in Lesson 6's Workflow actually
uses: a Hook notices a new file and hands the Agent a small JSON package —
`{"file": "report.pdf"}`. The Agent finishes and hands the Skill
`{"status": "ready"}`. Nobody's typing prose between steps; every handoff in that
whole chain is JSON, labeled pairs, wrapped in braces."

**[2:50–3:10] Recap + teaser**
"So: JSON is the plain-text format of labeled pairs — `"label": "value"` — wrapped in
braces, that Agents, Skills, Hooks, and Workflows use to actually pass data to each
other. It's not a new building block; it's the envelope the blocks already write to.
Next time: the language most of those blocks are actually built *in* — Python. See
you in Lesson 8."

---

## Scannable outline (for slides / written version)

1. **Hook** — every handoff between an Agent, Skill, Hook, or Workflow has to be
   written down in some shared format — that format is almost always JSON.
2. **Definition** — labeled pairs, `"label": "value"`, wrapped in curly braces as one
   object; a value can itself be a nested list.
3. **Office Suite analogy** — an Outlook contact card: Name: , Email: , Phone: — each
   value already has its own label, exactly like a JSON pair.
4. **Browser analogy** — a webpage's Network tab: most of what a browser fetches to
   build a page is JSON, not more webpage.
5. **Everyday-task analogy** — a recipe card: "Ingredients:" is a label pointing at a
   whole list, the same way a JSON value can be a nested list.
6. **Real example: Mistral Studio** — a Hook hands an Agent `{"file": "report.pdf"}`;
   the Agent hands a Skill `{"status": "ready"}` — every handoff is JSON.
7. **Recap** — JSON = the plain-text envelope for labeled data; it's how the blocks
   from Lessons 1–6 actually talk to each other, not a new block itself.
8. **Next up** — Lesson 8: Python.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Braces with a pair | Large teal `{` and `}` with one small navy `"name": "value"` line centered between them | "Labeled data, wrapped in braces — that's JSON." |
| 2 | Stacked label:value pills | Three rows, each a small navy "key" pill, a colon, and a teal "value" pill, inside a loose teal-outlined box | "Every pair has a label — nothing is left guessing what a value means." |
| 3 | Contact card | A rounded card with a small circle avatar and three label rows: Name, Email, Phone | "Already familiar — a contact card is labeled pairs, same as JSON." |
| 4 | Browser network flow | A browser window (rounded rect + 3 corner dots) with an arrow to a `{ }` braces icon, then an arrow to a page icon | "The browser fetches `{ }`, not more webpage — then draws the page from it." |
| 5 | Recipe card with nested list | A card headed "Ingredients" with one label pointing at three stacked sub-items | "One label, a whole list inside it — a JSON value can nest like this too." |
| 6 | Mistral Studio chain with JSON tags | Same File → Hook → Agent → Skill → Notify chain as Lesson 6, with a small `{ }` tag on each connecting arrow | "Every arrow in the chain is carrying JSON — that's what's actually moving." |
| 7 | Checkmark + signpost | A checkmark badge, an arrow pointing onward labeled "Python" | "Today: JSON. Next time: Python — the language most of these blocks are built in." |

---

## User / speaker notes

- This lesson assumes the viewer has seen Lessons 1–6 (Agent, Model, Memory, Skill,
  Hook, Workflow) — it treats those five terms as already-familiar vocabulary. If used
  standalone, add one sentence recapping "Workflow" before the hook, since JSON is
  framed as the data those steps pass to each other.
- Doodle 3 (contact card) is the crux visual — nearly every viewer has already seen
  labeled-field data in an address book or contact app, so hold it a beat longer than
  the others.
- Avoid showing raw, deeply nested JSON on screen for beginners — doodle 1 and 2
  intentionally use only one or two pairs so the shape stays readable at a glance.
- If delivering as a written lesson instead of video: keep the table above inline as
  the illustrations, one per section.
- Total runtime target: 2m50s narrated, stretchable to ~4m with pauses for doodles and
  a short live look at a browser's Network tab or Mistral Studio's own request/response
  data.
- Sources for the Mistral Studio claims: general agent-platform data-interchange
  patterns (steps passing labeled JSON payloads to each other) — verify the exact
  current UI/feature name in Mistral Studio's own documentation before quoting it as a
  specific product claim.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2) → Memory (Lesson 3) → Skill
(Lesson 4) → Hook (Lesson 5) → Workflow (Lesson 6) → JSON (Lesson 7)
**Suggested next topic:** Python — "the language most of these blocks (Agents,
Skills, Hooks) are actually built in."
**Later candidates, in a sensible teaching order:** (list exhausted for now — after
Python, consider branching into: Prompt, Token, Context Window, or API)
