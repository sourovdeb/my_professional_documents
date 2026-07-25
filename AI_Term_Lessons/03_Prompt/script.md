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

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. In Episode 2 we opened up the model — the thing that "talks." This episode is about the words **you** give it: the prompt. Model = the engine. Prompt = you turning the key and steering.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a person typing one short line into a search bar, and a giant machine behind it whirring to life. Caption over the line: **"this is the whole steering wheel."**

**Narration:**
> "Silicon Valley loves the word 'prompt' because it sounds technical. Here's the un-magic version: a prompt is just **the thing you type to tell the AI what you want.** That's it. It's the search box, the email you're writing, the instruction you'd give a very fast, very literal assistant. Master this one word and you're already steering."

**User note:** Write this on a sticky note: **A prompt = the request you type. Better request in → better answer out.** Everything else in this lesson is how to make the request better.

---

## 1. Demystifying it: something you already do every day (0:20–1:05)

**On screen (doodle):** three familiar boxes side by side — a Google search bar, an email "To:/Subject:/Body" window, and a chat message box — all with a big arrow pointing to a single label: **PROMPT**.

**Narration:**
> "You've written thousands of prompts already; nobody called them that. Type 'weather in Paris' into a search bar — that's a prompt. Write 'Hi, can you send me the file by 5pm? Thanks' in an email — that's a prompt to a human. Talking to an AI is the same move: you type what you want, in plain language.
>
> The only new habit is this: the AI does **exactly** what your words say, not what's in your head. A vague request gets a vague answer. A specific request gets a specific one."

**Everyday analogy:** It's like the difference between telling a taxi driver "just drive" versus "take me to 12 Rue de Rivoli, avoid the motorway." Same driver, same car — wildly different trip, decided entirely by your instruction.

**User note — the honest bit:** The model isn't reading your mind; it's reading your **text**. If the answer is bad, 80% of the time the fix is a clearer prompt, not a smarter AI.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** a prompt sentence being chopped into little tiles (tokens) that slide into the MODEL box from Episode 2; the box then prints its answer word by word.

**Narration:**
> "Under the hood, your prompt is the model's **starting point.** Remember from last episode: a model just guesses the next word, over and over. Your prompt is the *beginning* of the text it's continuing. Type 'Write a poem about the sea' and the model thinks, 'given those words, what's the most likely thing to come next?' — and it keeps going from there.
>
> That's why the wording matters so much: you're not pressing a button, you're **handing it the first few sentences of the story** and asking it to finish them well."

**Everyday analogy:** It's like starting a sentence for someone who's great at finishing them. Start with "Once upon a time…" and you'll get a fairy tale. Start with "Dear Sir or Madam, I am writing to complain…" and you'll get a formal letter. The opening you give **sets the whole direction.**

**User note — three cheap upgrades to any prompt:**
> 1. **Say who it's for** — "explain to a 7-year-old" vs "for an expert."
> 2. **Say the shape you want** — "as 5 bullet points," "in one paragraph," "as a table."
> 3. **Give an example** — showing one good answer beats describing it.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A large text box in the middle labeled **"Message"** with a cursor blinking. To the side, a smaller box labeled **"System prompt"** greyed out (a teaser for next episode). A "Send" arrow sits at the bottom-right.

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat** (the chat playground). The big box at the bottom where you type — that **message box** is where your prompt lives. There's also a separate box called the **'System prompt'** for standing instructions; we'll cover that next episode. For now, everything you type in the main message box is your prompt."

**HOW — try the same idea two ways, in 3 steps:**
> "**Step 1:** In the message box, type a lazy prompt: **'write about dogs.'** Send it. Notice you get something generic.
> **Step 2:** Now type a sharp one: **'Write 3 bullet points for a 10-year-old on why dogs are good for your health. Keep each under 15 words.'** Send it.
> **Step 3:** Compare. Same model, same chat — but the second answer is tighter, aimed, and usable. You changed nothing but the **words you gave it.** That gap *is* prompting."

**Everyday analogy:** It's exactly like the **search box in your browser.** Type "restaurant" and you get chaos; type "vegetarian restaurant open now near Gare du Nord" and you get your dinner. The engine didn't change — your query did.

**Source used for this section:** [Mistral AI — prompting basics / Le Chat](https://docs.mistral.ai/getting-started/) and the [Mistral Studio product page](https://mistral.ai/products/studio/) — Studio lets you type user prompts in Le Chat and set standing "system" instructions for agents; the reply is generated by the selected model continuing your text.

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** a before/after split — left side a blurry photo labeled "vague prompt," right side the same photo in sharp focus labeled "clear prompt."

**Narration:**
> "Here's the payoff: prompting is the **one AI skill that pays off immediately**, with zero code and zero cost. You don't need a bigger model or a fancy plan — most 'the AI is dumb' moments vanish the second you ask more clearly. It's the cheapest upgrade in all of AI, and it lives entirely in your own words."

---

## 5. Recap + memory hook (3:00–3:20)

**On screen (doodle):** the taxi doodle again — a hand pointing at a clear address on a map — with the caption "you steer with words."

**Narration:**
> "So: a prompt is just the request you type. The model finishes what you start, so the clearer you start, the better it finishes. Say who it's for, say the shape you want, and — when in doubt — show an example. Same engine, better trip, decided by you."

**User note — the one-line mnemonic:**
> **"A prompt is the key and the steering wheel — the model's the engine, but you decide where it goes."**

---

## 📊 POWERPOINT OUTLINE (matches `03_Prompt.pptx`)

**Slide 1 — Title:** *What's a "Prompt"? — Explained Simply*
- One core AI term, ~3 minutes, plain words
- Anchor example: the **message box** in Mistral's Le Chat
- Episode 3 of "AI Explained Simply"

**Slide 2 — The un-magic secret (What & Why):**
- A prompt = **the request you type** to the AI
- You already write them: search bars, emails, chat messages
- The AI does what your **words** say, not what's in your head
- Better request in → better answer out (cheapest AI upgrade there is)

**Slide 3 — How it works:**
- Your prompt is the model's **starting point** — it continues your text
- Same next-word guessing from Episode 2, seeded by your words
- Wording sets the whole direction ("Once upon a time…" vs "Dear Sir…")
- Three upgrades: say **who it's for**, the **shape** you want, give an **example**

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → **Le Chat**
- The big **message box** at the bottom = where your prompt goes
- A separate **"System prompt"** box for standing rules (next episode)
- Hit **Send** to hand your text to the model

**Slide 5 — Try it yourself:**
- Step 1: Type a lazy prompt: "write about dogs"
- Step 2: Type a sharp one: "3 bullets, for a 10-year-old, under 15 words each…"
- Step 3: Compare — same model, far better answer, just clearer words
- Takeaway: **the fix is usually a better prompt, not a smarter AI**

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **one_line_steers.png** — a person typing one short line; a giant machine whirring behind it; caption "the whole steering wheel."
2. **three_boxes.png** — search bar + email window + chat box, all arrows pointing to one label "PROMPT."
3. **taxi_instruction.png** — a taxi with two speech bubbles: "just drive" vs "12 Rue de Rivoli, avoid the motorway."
4. **prompt_into_model.png** — a sentence chopped into token tiles sliding into the MODEL box, which prints an answer.
5. **message_box.png** — the Mistral console with the "Message" box highlighted and a greyed-out "System prompt" box beside it.
6. **vague_vs_clear.png** — a blurry photo ("vague prompt") next to the same photo in focus ("clear prompt").
7. **signpost.png** — a signpost: "Next → System Prompt: the standing rules you set once."

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | The request you type to tell the AI what you want — plain language, no code. |
| **Where** in Mistral? | The **message box** in Le Chat on console.mistral.ai (the "System prompt" box is for standing rules). |
| **How** does it work? | Your prompt is the starting text the model continues, guessing the next word from there — so wording steers everything. |
| **Why** care? | It's the cheapest, fastest AI skill: clearer words fix most "dumb AI" moments with zero code and zero cost. |

---

*Disclaimer: informational and educational only. Console layout and model names may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
