# AI Explained, Plain and Simple — Lesson 1: What Is an "Agent"?

**A 2–5 minute script/outline for a video lesson or written explainer, with doodle notes**
*Created by Sourov Deb | July 17, 2026*
*Series: AI Explained, Plain and Simple — Lesson 1 of an ongoing series decoding one AI term at a time*

---

## The one-sentence version

> A **model** is a brain that answers questions. An **agent** is that same brain given hands, a toolbox, and a goal — so instead of just *telling* you what to do, it goes and *does* it.

---

## Everyday analogy

Think about the difference between **Word's spell-check** and **Excel's Mail Merge that also reads the replies and follows up**:

- Spell-check looks at what you typed and answers one question: "is this right?" It never touches anything else on your computer. That's a **model**.
- Now imagine a assistant with a checklist, a browser, and your email open, who reads your goal ("get this contract signed"), decides the steps, sends the email, checks for a reply, and nudges again if nobody answers by Friday. That's an **agent** — a model plus tools plus a goal it keeps working at until done.

---

## Script (spoken narration, ~2m30s at a relaxed pace)

**[0:00–0:20] Hook**
"Ever asked a chatbot a question, gotten a perfect answer... and then had to go do all the work yourself anyway? That gap — between *answering* and *doing* — is exactly what the word 'agent' fixes. Let's break it down in plain English."

**[0:20–0:55] Model vs. Agent**
"A **model** is the part of AI that thinks. Give it a question, it gives you an answer — like typing into a search bar, or running spell-check in Word. Smart, but it can't act. It has no hands.

An **agent** takes that same brain and gives it hands: a toolbox of things it's allowed to use — a web browser, your email, a calendar, a document. You give it a goal instead of a question, and it figures out the steps on its own."

**[0:55–1:20] The loop**
"Here's the trick that makes it work: an agent runs in a loop. It **thinks** of the next step, **acts** on it, **checks** whether that worked, and repeats — until the goal is actually done, not just described."

**[1:20–1:55] Concrete example — Mistral Studio**
"You can see this exact split in a real product: Mistral Studio. It's a platform for building AI systems, and it literally keeps 'Models' and 'Agents' as two separate building blocks in its catalog. A **Model** there is just the reasoning engine. An **Agent** wraps that model with instructions and tools — web search, code execution, a document library — so it can plan and act on its own. Studio even lets agents hand work off to *other* agents inside a workflow that remembers where it left off if something fails. Same brain. Very different job description."

**[1:55–2:20] Recap**
"So next time you hear 'AI agent,' don't picture something mysterious. Picture the intern who used to just answer your questions, now handed a laptop, a toolbox, and a to-do list — going off to actually finish the task and reporting back when it's done."

**[2:20–2:30] Teaser for next lesson**
"Next time: how does an agent remember what happened five minutes ago? That's 'memory' — see you in Lesson 2."

---

## Scannable outline (for slides / written version)

1. **Hook** — Chatbots answer; they don't act. "Agent" closes that gap.
2. **Model** = a brain that only answers. Like Word's spell-check: smart, but no hands.
3. **Agent** = that brain + a toolbox + a goal. Like an assistant with a browser, email, and a checklist.
4. **The loop** — Think → Act → Check → Repeat, until the goal is actually finished.
5. **Real example: Mistral Studio** — "Models" and "Agents" are literally separate, connected building blocks in its catalog; an Agent wraps a Model with tools (web search, code execution, documents) and can hand off to other agents.
6. **Recap** — Same brain, different job: answering vs. doing.
7. **Next up** — Lesson 2: Memory.

---

## Doodle notes (whiteboard / stick-figure style — see companion slide deck)

| # | Doodle | What it shows | Caption |
|---|--------|----------------|---------|
| 1 | Brain in a jar | A jar labeled MODEL, a brain floating inside, a small speech bubble with one answer, no arms or legs on the jar | "A MODEL only thinks and answers. It can't do anything by itself." |
| 2 | Brain grows a body | Same brain, now with stick-figure arms and legs and a tool belt holding a browser icon, an envelope, and a checklist | "An AGENT is a model + tools + a goal. It can act, not just answer." |
| 3 | The loop | A circular arrow with three stops: THINK, ACT, CHECK, and a tiny stick figure walking around it | "Agents work in a loop: think, act, check — repeat until done." |
| 4 | Old way vs. new way | Split panel: left, a person asks a question and gets a text bubble back; right, a person gives a goal and a stick figure walks off-panel and returns holding a finished folder | "Ask a MODEL a question, get an answer. Give an AGENT a goal, get a finished task." |
| 5 | The Mistral Studio shelf | A toolbox/shelf doodle with labeled bins: MODELS, AGENTS, SKILLS, WORKFLOWS — an arrow shows a Model bin feeding into an Agent bin, feeding into a Workflow bin | "Mistral Studio really does organize these as separate building blocks that snap together." |
| 6 | Recap ladder | A 3-rung ladder: 1) Model = the brain, 2) Agent = brain + hands + goal, 3) Workflow = many agents working together | "Today: Agent. Next time: Memory — how an agent remembers what happened five minutes ago." |

---

## User / speaker notes

- Keep each doodle on screen for the full sentence it supports — don't rush past doodle 2 or 4, they carry the core "answering vs. doing" distinction.
- If recording as video: draw or reveal each doodle live (or animate it in) rather than showing it all at once — the "brain grows a body" reveal on doodle 2 is the payoff moment.
- If delivering as a written lesson instead of video: keep the table above inline as the illustrations, one per section.
- Total runtime target: 2m30s narrated, stretchable to ~4m with pauses for the doodles and a short live look at Mistral Studio's Agents catalog page.
- Sources for the Mistral Studio claims: Mistral Studio product page (mistral.ai/products/studio) and Mistral's Agents documentation (docs.mistral.ai/studio-api/agents/introduction), checked July 17, 2026.

---

## Series tracker

**Covered so far:** Agent (Lesson 1) → Model (Lesson 2)
**Suggested next topic:** Memory — "how does an agent remember what happened five minutes ago, across a whole conversation, the way Word remembers your last 20 actions in Undo history?"
**Later candidates, in a sensible teaching order:** Skill → Hook → Workflow → JSON → Python
