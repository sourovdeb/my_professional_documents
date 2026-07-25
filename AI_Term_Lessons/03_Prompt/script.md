---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-07-25
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. Episode 2 opened up the model itself. This episode is about the one thing that's entirely in **your** control: what you type in.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a steering wheel labeled "PROMPT" bolted onto a big engine labeled "MODEL". A hand turns the wheel; the engine's exhaust changes direction.

**Narration:**
> "Last time we said a model is a very powerful engine that guesses the next word. But an engine doesn't decide *where to go* — you do, with the steering wheel. In AI, that steering wheel is called the **prompt**. Let's see how much it actually changes the ride."

**User note:** Sticky-note version: **A prompt is the steering wheel. The model is the engine. You decide the direction.**

---

## 1. Demystifying it: it's just very specific instructions (0:20–1:05)

**On screen (doodle):** two speech bubbles side by side. Left bubble: "Tell me about dogs." Right bubble: "List 5 differences between Labradors and Poodles, for a 10-year-old, as bullet points." Left bubble gets a wobbly, generic-looking answer; right bubble gets a neat, useful one.

**Narration:**
> "A prompt is just the text you hand the model before it starts guessing. That's it — no hidden button, no secret setting. But because the model works by continuing your text, **whatever you write becomes the starting point it builds from.** Vague in, vague out. Specific in, specific out."

**Everyday analogy:** It's the difference between telling a new assistant "sort this out" and telling them "file these five invoices under Q3, flag anything over $500." Same person, wildly different result — because the *instruction* did the work, not the assistant's intelligence.

**User note — the honest bit:** Nobody is hiding a smarter model behind a paywall just for good prompts. A better prompt doesn't make the engine bigger — it just points the same engine more precisely. That's within everyone's reach for free.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** the same "The cat sat on the ___" box from Episode 2, except now the blank is preceded by a whole paragraph of extra instructions before the sentence, and the predicted word changes because of it.

**Narration:**
> "Remember: a model just predicts the next word, over and over. Your prompt is the text it's predicting *from*. Add the words 'Explain like I'm 10' before your question, and every next-word guess afterward is now nudged toward simpler words. Add 'Answer in French,' and the guesses shift language. You're not reprogramming the model — you're **reshaping the odds** for what comes next, one instruction at a time."

**Everyday analogy:** It's like a search engine query, but on steroids. Typing "dogs" into a search bar gets you everything; typing "best low-shedding dog breeds for apartments" gets you the page you actually wanted. A prompt is that same narrowing trick, except the model writes a fresh answer instead of listing links.

**User note:** Three things that make a prompt do more work: **be specific** (what, who it's for, how long), **give an example** if you can, and **say what format you want** (bullets, a table, a short paragraph).

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A large open text box at the bottom labeled "Message" — that's the prompt box. Above it, a smaller collapsed field labeled "System prompt" (a sneak peek at Episode 4).

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat**. The big text box at the bottom of the screen — where the cursor blinks, waiting for you to type — **that box is the prompt.** Everything you type there before hitting send is the entire steering wheel for that answer."

**HOW — try it in 3 steps:**
> "**Step 1:** Type a deliberately vague prompt: 'Tell me about volcanoes.' Send it, and skim the answer — long, generic, a bit of everything.
> **Step 2:** Now type a specific one: 'In 3 bullet points, explain why volcanoes erupt, for a curious 8-year-old.' Send it.
> **Step 3:** Compare the two answers side by side. Same model, same day, same person typing — but the second prompt did the steering, and the answer is shorter, clearer, and actually usable."

**Everyday analogy:** It's exactly like the difference between a blank search box and a well-filled-in web form. A blank box makes the engine guess what you meant; a filled-in form — with the fields you actually care about — gets you the specific result on the first try.

**Source used for this section:** [Mistral AI prompting/Le Chat overview](https://docs.mistral.ai/) — Le Chat's message box is the primary place users provide the prompt that steers each response.

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** a person with two folders — one thin folder labeled "vague prompts, redo, redo, redo" and one thick, tidy folder labeled "specific prompt, done first try."

**Narration:**
> "A good prompt is the cheapest upgrade in AI — it costs you nothing, needs no new subscription, and it's the one lever that's 100% yours. Learning to write a clear, specific prompt saves you the 'ask again, ask again' loop and gets you a usable answer the first time."

**Recap line:**
> "A model is the engine. A prompt is the steering wheel. Same engine, better steering, better ride."

---

## 5. Closing / next episode teaser (3:00–3:15)

**On screen (doodle):** the steering wheel from the cold open, now with a small dashboard label appearing above it: "SYSTEM PROMPT — sets the rules before you even start driving."

**Narration:**
> "Next time: there's actually a *second*, hidden steering wheel that's set before you even type — the **system prompt**. See you in Episode 4."

---

## 📊 POWERPOINT OUTLINE (5 slides + speaker notes)

**Slide 1 — Title:** What's a "Prompt"? — Explained Simply
- AI Explained Simply · Episode 3
- Anchor example: the message box in Mistral's Le Chat
- One core AI term · plain words · everyday analogies

**Slide 2 — The un-magic secret (What & Why):**
- A prompt = the instructions you type before the model starts guessing
- Vague in → vague out. Specific in → specific out.
- Better prompts don't make the engine bigger — they steer the same engine
- No hidden paywall smarts here — this lever is free and yours

**Slide 3 — How it works:**
- The model predicts the next word from *your text*, including your prompt
- Add "explain like I'm 10" → every next guess gets simpler
- It's a search query, but the engine writes a fresh answer instead of links
- 3 upgrades: be specific, give an example, name the format you want

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → Le Chat
- Bottom of screen: the big **message box** — that's the prompt
- A smaller "System prompt" field sits above it (teaser for Episode 4)
- Typing there = gripping the steering wheel

**Slide 5 — Try it yourself:**
- Step 1: Ask something vague — "Tell me about volcanoes"
- Step 2: Ask something specific — "3 bullets, why volcanoes erupt, for an 8-year-old"
- Step 3: Compare the two answers side by side
- Takeaway: **a good prompt is the cheapest upgrade in AI** — and it's entirely yours

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **steering_wheel_engine.png** — a steering wheel labeled "PROMPT" bolted onto an engine labeled "MODEL"; a hand turns the wheel.
2. **two_bubbles.png** — a vague speech bubble vs. a specific speech bubble, with a messy vs. a neat answer below each.
3. **next_word_shift.png** — "The cat sat on the ___" with extra instruction text stacked in front of it, changing the guessed word.
4. **search_bar_vs_form.png** — a blank search box next to a filled-in web form, same idea as a vague vs. specific prompt.
5. **mistral_message_box.png** — the Mistral console with the big message box highlighted at the bottom, a smaller "System prompt" field above it.
6. **two_folders.png** — a thin "redo, redo, redo" folder vs. a thick "done first try" folder.
7. **signpost_ep4.png** — a signpost: "Next → System Prompt: the hidden steering wheel."

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | The instructions you type before the model starts predicting — the steering wheel for its answer. |
| **Where** in Mistral? | The **message box** at the bottom of Le Chat on console.mistral.ai. |
| **How** does it work? | The model predicts its next words *from* your prompt text — specific wording shifts the odds toward a specific answer. |
| **Why** care? | It's the cheapest, fastest upgrade in AI — free, instant, and entirely under your control. |

---

*Disclaimer: informational and educational only. Console layout may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
