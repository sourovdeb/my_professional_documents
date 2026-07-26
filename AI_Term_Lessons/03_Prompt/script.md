---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-07-26
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. In Episode 2 we opened up the model — the thing that "talks." This episode is about the one skill that decides whether it talks sense: how you **ask**.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a kid at a search box. Above it, two speech bubbles: a tiny one saying "dog" with a confused shrug, and a big one saying "Draw a friendly cartoon dog, brown, wagging its tail, sitting on grass" with a happy tail-wag. Same box, two very different results.

**Narration:**
> "Silicon Valley makes 'talking to AI' sound like a secret art. It isn't. A prompt is just the thing you type. And the whole trick is embarrassingly simple: **the clearer you ask, the better you get back.** Let me show you."

**User note:** Write this on a sticky note: **A prompt is your instruction to the AI — and vague in means vague out.** That's the whole lesson. The rest just unpacks it.

---

## 1. Demystifying it: you already do this every day (0:20–1:05)

**On screen (doodle):** three familiar boxes side by side — a Google search bar, an email "To/Subject/Body," and a text message. Each gets a label: "all of these are prompts."

**Narration:**
> "You've been writing prompts your whole life without the fancy word.
>
> When you type into **Google**, that search box is a prompt. When you write an **email** — who it's for, the subject, the message — that's a prompt with structure. When you text a friend 'grab milk on the way home,' that's a prompt with an instruction *and* the details it needs.
>
> An AI prompt is the same move: you type what you want, and the model reads every word to decide what to write back."

**Everyday analogy:** It's like **ordering at a café**. "A coffee" gets you *something*. "A large oat-milk latte, extra hot, one sugar" gets you *exactly* what you pictured. The barista didn't get smarter — you got clearer.

**User note — the honest bit:** The model can't read your mind. It only has the words in the box. Everything you leave out, it has to *guess* — and it will guess confidently. So the detail you add is not decoration; it's the steering wheel.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** a prompt sentence being fed into the MODEL box from Episode 2. The box reads the words left-to-right, then starts printing an answer. A little caption: "your words set the direction; it fills in the rest."

**Narration:**
> "Remember from Episode 2 — a model just guesses the next word, over and over. Your prompt is the *running start* it guesses from. Give it 'Write a poem' and it has a whole ocean of directions. Give it 'Write a four-line, funny poem about a cat who won't share the sofa' and you've narrowed that ocean down to a puddle. Same engine — you just aimed it.
>
> That's why the three things that matter most are: **say who it's talking to, say what you want, and give an example if you can.**"

**Everyday analogy:** Think of the **filters in an online shop**. "Shoes" shows you ten thousand. Add size, colour, price, and brand, and you're down to the three you actually want. Each word in your prompt is a filter.

**User note:** A quick recipe you can memorise — **Role + Task + Detail + Format.** "You're a friendly teacher (role). Explain gravity (task) to a 7-year-old (detail) in three short bullet points (format)." Add the parts you're missing and answers jump in quality.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A big text box in the middle labeled **"Message"** with a cursor blinking. Off to the side, a smaller box labeled **"System prompt"** with a note: "the standing instructions." A send arrow at the bottom.

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat** (or the API playground). The **big message box** where you type is where your prompt goes. Above or beside it you'll often see a **'System prompt'** box — that's a prompt too, just a *standing* one that sets the ground rules before you say anything."

**HOW — try it in 3 steps:**
> "**Step 1:** In the message box, type the lazy version — **'Tell me about France.'** Send it. Notice you get a giant, unfocused essay.
> **Step 2:** Now type the aimed version — **'In 5 bullet points, give a first-time traveller the practical basics for visiting France: currency, language, best season, one etiquette tip, one safety tip.'** Send it.
> **Step 3:** Compare. Same model, same second — but the second answer is usable because *you* did the aiming."

**Bonus:** Put a rule in the **System prompt** box — 'Always answer in simple English a 12-year-old could read.' Now every reply obeys it without you repeating yourself. That's the power of a standing prompt.

**Everyday analogy:** The **System prompt** is like the **default settings** in Word — margins, font, language — set once, applied to everything. Your **message** is what you actually type on the page each time.

**Source used for this section:** [Mistral AI prompting / getting-started docs](https://docs.mistral.ai/getting-started/quickstart/) and the [Mistral Studio product page](https://mistral.ai/products/studio/) — Le Chat and the API take a user message plus an optional system prompt, which is how you set an agent's standing behaviour in Studio.

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** a person turning a blurry photo into a sharp one with a focus dial labeled "better prompt."

**Narration:**
> "Here's the payoff: you don't need a better AI to get better answers — you usually just need a better prompt. It's the cheapest, fastest upgrade there is, and it's a skill, not a subscription. The people who seem to get 'magic' out of AI mostly just ask well."

---

## 5. Recap + memory hook (3:00–3:20)

**On screen (doodle):** the café order from Section 1 turning into a perfect latte, with the caption "Role + Task + Detail + Format."

**Narration:**
> "So: a prompt is just what you type — the instruction the model reads word for word. Vague in, vague out. Add **who, what, the details, and the format**, and ordinary AI starts to look brilliant. The engine was always the same; you got clearer."

**User note — the one-line mnemonic:**
> **"A prompt is a café order: the barista's the same — say it clearly and you get exactly what you pictured."**

---

## 📊 POWERPOINT OUTLINE (matches `03_Prompt.pptx`)

**Slide 1 — Title:** *What's a "Prompt"? — Explained Simply*
- One core AI term, ~3 minutes, plain words
- Anchor example: the **Message** and **System prompt** boxes in Mistral's console
- Episode 3 of "AI Explained Simply"

**Slide 2 — You already do this (What & Why):**
- A prompt = **the instruction you type** to the AI
- You already write them: Google searches, emails, texts
- The model only knows the words in the box — it can't read your mind
- **Vague in → vague out;** detail is the steering wheel

**Slide 3 — How it works:**
- The model guesses the next word — your prompt is its **running start**
- More detail = you aim it (an ocean of answers → one puddle)
- Each word is a **filter**, like filters in an online shop
- Recipe: **Role + Task + Detail + Format**

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → Le Chat / API playground
- Big **"Message"** box = your prompt each time
- **"System prompt"** box = standing rules set once
- System prompt = the **default settings** in Word

**Slide 5 — Try it yourself:**
- Step 1: Ask the lazy way — "Tell me about France"
- Step 2: Ask the aimed way — 5 bullets, specific angles
- Step 3: Compare — same model, far better answer
- Takeaway: **you don't need a better AI, just a better prompt**

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **vague_vs_clear.png** — one search box, two speech bubbles: tiny "dog" (confused) vs a detailed request (happy tail-wag).
2. **everyday_prompts.png** — Google bar + email + text message, all labeled "these are prompts."
3. **cafe_order.png** — "a coffee" (mystery cup) vs "large oat latte, extra hot, one sugar" (perfect cup).
4. **aim_the_ocean.png** — a wide ocean of answers narrowing to a puddle as words are added.
5. **filters.png** — an online-shop filter panel (size/colour/price) labeled "each word is a filter."
6. **mistral_boxes.png** — the Mistral console: big "Message" box + smaller "System prompt" box + send arrow.
7. **recipe_card.png** — a card reading "Role + Task + Detail + Format."
8. **signpost.png** — a signpost: "Next → Token: the units a model reads and writes in."

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | The instruction you type — everything the model reads to decide its answer. |
| **Where** in Mistral? | The **Message** box in Le Chat / the API playground, plus the **System prompt** box for standing rules (console.mistral.ai). |
| **How** does it work? | Your words are the model's running start; more detail narrows its next-word guesses toward what you want. |
| **Why** care? | Better prompts beat a better AI — it's the cheapest, fastest way to get sharper answers, and it's a skill you own. |

---

*Disclaimer: informational and educational only. Console layout and model names may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
