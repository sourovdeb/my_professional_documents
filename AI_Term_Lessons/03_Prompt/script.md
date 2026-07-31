---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-07-31
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. Episode 1: "Model talks, Agent walks." Episode 2: a model is remembered data + computing muscle + a language knack, all fused into a next-word guesser. This episode is the missing piece — **how you actually talk to it.** That message you type is called a **prompt.***

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a person typing into a chat box. An arrow carries the words over to the glowing MODEL box from Episode 2. The box thinks, then sends words back. Label the arrow going in: **PROMPT**.

**Narration:**
> "A model is powerful, but it just sits there. It does nothing until you *say* something. The thing you type to wake it up and steer it — that's a **prompt.** No magic word, no secret code. A prompt is just your instructions, in plain language."

**User note:** Sticky-note version → **Prompt = what you type in. It's the steering wheel; the model is the engine.**

---

## 1. What is it, really? (0:20–1:05)

**On screen (doodle):** a search bar labeled "Google" on the left, and a chat box labeled "AI" on the right. Under Google: "keywords." Under AI: "a full request, like talking to a helpful assistant."

**Narration:**
> "You already know how to prompt — you do it every day. Typing into a **Google search bar** is a prompt. Typing a subject line and asking a coworker for a favour is a prompt. Telling **Siri** or **Alexa** 'set a timer for ten minutes' is a prompt.
>
> The only difference with an AI model is that you don't need keywords or robot-speak. You write the way you'd write to a smart, brand-new assistant who is fast, eager, and knows nothing about *your* situation until you tell them."

**Everyday analogy:** A prompt is like the **instructions you'd write on a sticky note for a temp worker on their first day.** Vague note → confused results. Clear note → good work. Same person, wildly different outcome — and the *only* thing you changed was the note.

**User note — the honest bit:** The model can't read your mind and it doesn't remember yesterday. Everything it needs to know for *this* answer has to be *in the prompt*. Better prompt in → better answer out. This is the one skill that makes AI actually useful.

---

## 2. So how does a prompt actually work? (1:05–1:45)

**On screen (doodle):** the sentence "Write a birthday message for my mum" flowing into the box; the box breaks it into little tiles (tokens), then continues the sentence word by word into a finished message.

**Narration:**
> "Remember from Episode 2 that a model just predicts the next word? Your prompt is the **beginning of the sentence it's finishing.** When you type 'Write a birthday message for my mum,' the model treats that as the opening and keeps going in the most sensible direction: a warm, short birthday note.
>
> Change the opening and you change everything that follows. Add 'make it funny and rhyme' and the likely next words shift toward jokes and rhymes. You're not pressing hidden buttons — you're **setting the direction the guessing runs in.**"

**Everyday analogy:** It's like the **first domino.** Where you place it, and which way it faces, decides the whole chain that falls after it. Your prompt is that first domino.

**User note — three tiny upgrades that fix most bad answers:**
> 1. **Say who it's for** — "explain to a 7-year-old" vs "explain to a lawyer."
> 2. **Say the shape you want** — "in 3 bullet points," "as a table," "in one sentence."
> 3. **Give an example** — show one of what "good" looks like, and it copies the pattern.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A big text box in the middle labeled **"Message"** with a cursor blinking. A small **"System prompt"** box sits above it, greyed, with a note: "the standing instructions — next episode." A **Send** arrow on the right.

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat** or the **API playground.** That big empty text box in the middle — the one begging you to type — *that* is the prompt box. It's the single most important box on the whole screen. Everything the AI does starts there."

**HOW — try it in 3 steps (watch a weak prompt become a strong one):**
> "**Step 1 — weak prompt:** type just `holiday ideas` and hit send. You'll get a generic list that could be for anyone.
> **Step 2 — strong prompt:** now type `Suggest 5 budget holiday ideas for a family with two young kids who love the beach, in Europe, in July. One line each.` Send it.
> **Step 3 — compare.** Same model, same button — but the second answer is genuinely useful because *you told it who, what, and in what shape.* You didn't upgrade the AI. You upgraded the prompt."

**Everyday analogy:** It's the difference between typing **"cake"** into a search engine and typing **"easy 3-ingredient chocolate cake, no oven."** Same search box — but one of them actually gets you dinner.

**Source used for this section:** [Mistral AI prompting guide / docs](https://docs.mistral.ai/guides/prompting_capabilities/) and the [Mistral Studio product page](https://mistral.ai/products/studio/) — Mistral describes the message/prompt as the input you send to a model, and offers guidance on writing clearer prompts (role, context, examples) to get better outputs. *(Console layout may change — explore live.)*

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** two people at identical computers. One types a one-word prompt and gets a shrug; the other types a clear, detailed prompt and gets a gold star. Caption: "same tool, different results."

**Narration:**
> "Here's the freeing part: you don't need to code, and you don't need to be a genius, to get great results from AI. You just need to ask well. Prompting is the cheapest, fastest skill in all of AI — it's just clear thinking, written down. The person who writes the clearer note wins, every time."

---

## 5. Recap + memory hook (3:00–3:20)

**On screen (doodle):** the steering-wheel image — a hand on a wheel labeled PROMPT, steering the MODEL car down a road toward a clearly-labeled destination.

**Narration:**
> "So: a prompt is simply **what you type in** — your plain-language instructions. It's the first domino, the sticky note for your new assistant, the steering wheel on the model's engine. Say who it's for, say the shape you want, give an example — and a so-so answer turns into a genuinely useful one."

**User note — the one-line mnemonic:**
> **"The model is the engine; the prompt is the steering wheel. A better note gets a better answer — the thinking is still yours."**

---

## 📊 POWERPOINT OUTLINE (matches `03_Prompt.pptx`)

**Slide 1 — Title:** *What's a "Prompt"? — Explained Simply*
- One core AI term, ~3 minutes, plain words
- Anchor example: the **message box** in Mistral's console
- Episode 3 of "AI Explained Simply"

**Slide 2 — What & Why:**
- A prompt = **what you type in** — your plain-language instructions
- You already prompt daily: Google, Siri, a note to a coworker
- It's the **steering wheel**; the model is the engine
- Everything the AI needs for *this* answer must be *in the prompt*

**Slide 3 — How it works:**
- Your prompt is the **start of the sentence the model finishes**
- Change the opening → change everything that follows (the **first domino**)
- 3 upgrades: say **who** it's for, say the **shape**, give an **example**
- Better prompt in → better answer out

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → Le Chat / API playground
- The big **"Message" box** in the middle = the prompt box
- (The small **"System prompt"** box above it = next episode)
- Type, hit **Send**, watch the answer build word by word

**Slide 5 — Try it yourself:**
- Weak: `holiday ideas` → generic shrug
- Strong: `5 budget beach holiday ideas, family, 2 young kids, Europe, July, one line each` → useful
- Same model, same button — you upgraded the **prompt**, not the AI
- Takeaway: **ask well = clear thinking, written down**

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **prompt_arrow.png** — person types into a chat box; an arrow labeled PROMPT carries words to the glowing MODEL box, which sends words back.
2. **google_vs_ai.png** — a Google search bar ("keywords") beside an AI chat box ("a full request, like talking to an assistant").
3. **sticky_note_temp.png** — a sticky note for a first-day temp worker: vague note → confused face; clear note → thumbs up.
4. **first_domino.png** — a hand placing the first domino; the whole chain falls the way it faces. Labeled "your prompt = the first domino."
5. **mistral_message_box.png** — the Mistral console with the big "Message" box highlighted, a greyed "System prompt" box above, and a Send arrow.
6. **weak_vs_strong.png** — two computers: one-word prompt → shrug; detailed prompt → gold star. "Same tool, different results."
7. **steering_wheel.png** — a hand on a wheel labeled PROMPT steering the MODEL car toward a labeled destination.
8. **signpost.png** — a signpost: "Next → System Prompt: the standing instructions you set once."

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | The plain-language instructions you type in to tell the model what to do. |
| **Where** in Mistral? | The big **"Message" box** in the middle of Le Chat / the API playground on console.mistral.ai. |
| **How** does it work? | It becomes the start of the sentence the model finishes — so its wording steers the whole answer. |
| **Why** care? | It's the cheapest, fastest AI skill: no code needed. A clearer prompt gets a better answer, every time. |

---

*Disclaimer: informational and educational only. Product names and console layout may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
