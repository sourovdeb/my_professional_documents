---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-08-02
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. Episode 1: "Model talks, Agent walks." Episode 2: what a model **is**. This episode is the missing half — **how you actually talk to it.** A model is a genie; a prompt is the wish. And how you word the wish decides what you get.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a person at a keyboard with a speech bubble. Inside the bubble, the words "make it good" get crossed out and replaced with "write a 3-line thank-you email to my landlord, friendly, no slang." An arrow points to a smiling robot holding a neat little note.

**Narration:**
> "Silicon Valley calls it 'prompt engineering' so it sounds like a job you need a degree for. Here's the plain version: a **prompt is just the instruction you type**. That's it. The trick isn't magic words — it's being clear, the same way you'd be clear asking a new coworker for a favour."

**User note:** Sticky-note version: **A prompt = what you ask + how clearly you ask it.** Vague in, vague out. Specific in, useful out.

---

## 1. Demystifying it: it's a request, not a spell (0:20–1:05)

**On screen (doodle):** a split panel. Left: a fuzzy speech bubble "help me" → a confused robot with a "?". Right: a crisp speech bubble "summarise this 2-page report into 3 bullet points for my boss" → a robot handing over 3 tidy bullets.

**Narration:**
> "The model doesn't read your mind — it reads your words. A prompt is a **request**: what you want, plus any details that pin it down. Who's it for? How long? What tone? What must it include or avoid?
>
> Add those and the answer sharpens instantly. Leave them out and the model has to *guess* — and it guesses average, because average is the safest bet."

**Everyday analogy:** It's a **search box, grown up.** In Google you type keywords and get links. In a model you type a full request — 'act as a French tutor and quiz me on past-tense verbs' — and it *does the task*, not just point at it. Same muscle memory (type what you want), bigger payoff.

**User note — the honest bit:** There are no secret magic words. The whole skill is **clarity + a little context.** If a human coworker would need to ask you a follow-up question, so will the model — so answer that question *inside* the prompt.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** the typed prompt sliding into the MODEL box from Episode 2. Inside, it gets chopped into little puzzle pieces (tokens); the box then prints words out one at a time, each new word "leaning on" the prompt pieces still sitting on the table.

**Narration:**
> "When you hit send, your prompt goes into the model as its **starting context** — the pile of words it looks back at before every single guess. Remember Episode 2: a model just predicts the next word. Your prompt is *what it's predicting from.*
>
> So a longer, clearer prompt literally gives it more to lean on. Change the prompt and you change the whole chain of guesses that follows. You're not casting a spell — you're **setting the starting conditions.**"

**Everyday analogy:** It's like the **opening line of a story.** Start with 'Once upon a time, a dragon…' and the rest writes itself one way; start with 'The quarterly budget shows…' and it goes somewhere completely different. Same writer, different opening — different everything after.

**User note:** This is why "add an example" works so well. Show the model one sample of what "good" looks like, and every next-word guess now aims at *that* target instead of the average.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A big text box at the bottom labeled with a blinking cursor. Someone types a short vague line, gets a shrug; then edits it into a detailed line and gets a tidy answer. A little "＋ Attach" clip and a "System" tab sit nearby.

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat** (or the **API playground**). The **big message box at the bottom** — that's the prompt box. Everything you type there *is* the prompt. Above or beside it you'll often see a **'System' field** — that's a special standing prompt we'll cover next episode."

**HOW — try it in 3 steps:**
> "**Step 1 — the lazy way:** type `write an email`. Send it. You'll get something generic and probably wrong for your situation.
> **Step 2 — the clear way:** edit it to `Write a short, friendly email to my landlord asking to fix a leaking tap. Polite, 3 sentences, no slang. Sign it 'Sourov.'` Send that.
> **Step 3 — compare.** Same model, same button. The only thing that changed was the **prompt** — and the second answer is one you could actually send."

**Everyday analogy:** It's the difference between telling a **printer** just "print" versus setting the page size, colour, and copies first. The machine is identical; your *instructions* decide the output.

**Source used for this section:** [Mistral prompting guide / basic prompting](https://docs.mistral.ai/guides/prompting_capabilities/) and the [Mistral Studio product page](https://mistral.ai/products/studio/) — Mistral documents prompting patterns (clear instructions, roles, and examples) as the primary way users steer a model inside Le Chat and the API.

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** two people at identical laptops. One types one word and gets a tangled scribble; the other types three clear lines and gets a gift box. Caption: "same tool, different wording."

**Narration:**
> "Two people with the exact same AI get wildly different results — and the only difference is how they ask. Prompting is the **one skill that makes every other AI tool better**, and it costs nothing to practise. Get clearer at asking, and you get more out of *everything* — chat, agents, image tools, all of it."

---

## 5. Recap + memory hook (3:00–3:20)

**On screen (doodle):** the fuzzy "help me" bubble morphing into a crisp, detailed bubble, with the caption "what + who + how long + tone."

**Narration:**
> "So: a prompt is just your instruction. The model reads your words, not your mind, and predicts from them. Be clear, add a scrap of context, show an example when you can — and average answers turn into useful ones."

**User note — the one-line mnemonic:**
> **"A prompt is a wish you type — word it like you mean it, because the genie takes you literally."**

---

## 📊 POWERPOINT OUTLINE (matches `03_Prompt.pptx`)

**Slide 1 — Title:** *What's a "Prompt"? — Explained Simply*
- One core AI term, ~3 minutes, plain words
- Anchor example: the **message box** in Mistral's console
- Episode 3 of "AI Explained Simply"

**Slide 2 — It's a request, not a spell (What & Why):**
- A prompt = **what you ask + how clearly you ask it**
- The model reads your **words**, not your **mind**
- No magic words — just **clarity + a little context**
- Vague in → average out. Specific in → useful out
- It's a **search box, grown up**: type the task, it does the task

**Slide 3 — How it works:**
- Your prompt becomes the model's **starting context**
- A model predicts the next word — the prompt is **what it predicts from**
- Longer/clearer prompt = more for it to lean on
- Like the **opening line of a story** — it steers everything after
- Adding **one example** aims every guess at "good"

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → **Le Chat** / API playground
- The **big message box at the bottom** = the prompt
- Nearby: a **"System" field** (a standing prompt — next episode)
- Type there, hit send, read the answer

**Slide 5 — Try it yourself:**
- Step 1: type `write an email` → generic result
- Step 2: type `Write a short, friendly email to my landlord asking to fix a leaking tap. Polite, 3 sentences, no slang.`
- Step 3: compare — same model, only the **prompt** changed
- Takeaway: **clarity is the whole skill** — it makes every AI tool better

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **vague_vs_clear.png** — split panel: fuzzy "help me" → confused robot; crisp "summarise into 3 bullets for my boss" → robot with 3 tidy bullets.
2. **wish_and_genie.png** — a person typing a wish; a genie/robot taking it literally.
3. **prompt_into_model.png** — the typed prompt sliding into the MODEL box, chopped into token puzzle-pieces, words printing out one at a time.
4. **opening_line.png** — two story openings ("Once upon a time…" vs "The quarterly budget…") branching into two different pages.
5. **mistral_promptbox.png** — the Mistral console message box: a vague line getting a shrug, then an edited detailed line getting a tidy answer.
6. **two_laptops.png** — two people, same laptop: one word → scribble; three clear lines → gift box.
7. **signpost.png** — a signpost: "Next → System Prompt: the standing instruction that shapes every answer."

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | The instruction you type — what you want, plus the context that pins it down. |
| **Where** in Mistral? | The **message box at the bottom** of Le Chat / the API playground on console.mistral.ai. |
| **How** does it work? | It becomes the model's **starting context** — the words it looks back at before predicting each next word. |
| **Why** care? | It's the one free skill that makes *every* AI tool give you better answers. |

---

*Disclaimer: informational and educational only. Console layout and model names may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
