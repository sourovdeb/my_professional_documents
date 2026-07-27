---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-07-27
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. Episode 2 said a model is grown-up autocomplete. This episode is about the thing that switches it on: **what you type**.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a person at a keyboard. A speech bubble goes from them into a glowing box labeled **MODEL**. Under the bubble, one word: **PROMPT**.

**Narration:**
> "You already know how to use the most 'advanced' AI feature there is. It's this: you type something, and it answers. That thing you type has a name — a **prompt** — and once you understand it, you stop getting rubbish answers and start getting useful ones. No magic. Just better typing."

**User note:** Sticky-note version: **A prompt is just your instruction to the AI — the words you hand it so it knows what to do.** That's the whole term. The rest is how to hand it good words.

---

## 1. Demystifying it: it's a search box that talks back (0:20–1:05)

**On screen (doodle):** a Google search bar on the left with an arrow to a Mistral chat box on the right. Caption: "same habit, richer answer".

**Narration:**
> "You've typed into a Google search box a thousand times. A prompt is that same habit — you type what you want — except instead of a list of blue links, you get a written answer back.
>
> There's one big difference, and it changes everything: a search engine matches keywords, so 'best' vs 'top' barely matters. An AI **reads your whole sentence**. So the *way* you ask isn't decoration — it's the steering wheel."

**Everyday analogy:** Think of ordering coffee. "Coffee" gets you *something* hot and brown. "Large oat-milk flat white, extra hot, one sugar" gets you exactly what you wanted. Same barista, same machine — the **order** did the work. A prompt is your order.

**User note — the honest bit:** The AI is not reading your mind; it's reading your text. Ninety percent of "the AI is dumb" moments are really "my prompt was vague." Fix the order, fix the coffee.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** the typed sentence breaking into little tiles (tokens) that drop into the MODEL box; the box then prints an answer word by word.

**Narration:**
> "Here's the mechanism. Your prompt gets chopped into small chunks — tokens, roughly pieces of words — and fed into the model. Remember Episode 2: the model does one thing, guess the next word. Your prompt is the *running start* it guesses from.
>
> So a rich, specific prompt points those guesses in a clear direction. A one-word prompt leaves the model to fill in the blanks itself — and it'll fill them with the most *average* thing it's seen. Vague in, generic out."

**Everyday analogy:** It's like the difference between telling a new assistant "handle the emails" versus "reply to the three from clients, thank them, and say I'll call Friday." Same assistant — one instruction produces a mess, the other produces exactly what you meant.

**User note — the 4-part recipe for a good prompt:** **Role + Task + Context + Format.** "Act as a travel agent (*role*). Plan a 3-day Paris trip (*task*) for a family with two kids on a small budget (*context*). Give it as a day-by-day bullet list (*format*)." Hit those four and the quality jumps instantly.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** the Mistral console. A big text box at the bottom labeled **"Message"** where a cursor is typing. Separately, higher up, a second box labeled **"System Prompt"** with a little gear icon.

**WHERE — in the Mistral console:**
> "Go to **console.mistral.ai** and open **Le Chat** or the **API playground**. The wide box at the bottom where you type — that **'Message' box is where your prompt goes.** Look a little higher and you'll often see a second box called **'System Prompt'.** Same idea, different job: the system prompt is the standing instruction ('always answer in simple English, like a teacher'), and the message is today's actual request. That's our next episode."

**HOW — try it in 3 steps:**
> "**Step 1:** In the message box, type a lazy prompt on purpose — just **'marketing'** — and send it. Watch it hand back something vague and generic.
> **Step 2:** Now type the rich version: **'Act as a marketing coach. Write 3 Instagram caption ideas for a small Bengali sweet shop opening in Paris. Keep each under 15 words, friendly tone.'** Send that.
> **Step 3:** Compare the two answers side by side. You didn't change the model or pay a penny more — you only improved the **order**. That gap *is* the whole lesson."

**Everyday analogy:** A prompt is like the **subject line and brief of an email** you send a colleague. "Question" gets you a slow, confused reply. "Need Friday's sales figures as a table by 3pm" gets you the right thing, fast. Specific ask, specific answer.

**Source used for this section:** [Mistral AI prompting basics](https://docs.mistral.ai/getting-started/prompting_capabilities/) and the [Mistral Studio product page](https://mistral.ai/products/studio/) — the console exposes a message input plus a configurable system prompt for shaping how agents respond.

---

## 4. Why should you care? (2:40–3:00)

**On screen (doodle):** two coffee cups side by side — one labeled "coffee" looking sad and generic, one labeled "large oat flat white, extra hot" looking great — under a heading "same machine".

**Narration:**
> "Because prompting is the one AI skill that pays off no matter which tool you use — Mistral, a search bar, a phone assistant, anything. Learn to write a clear order and you get better results everywhere, today, for free. It's the cheapest upgrade in tech: you don't buy a smarter AI, you become a clearer asker."

---

## 5. Recap + memory hook (3:00–3:20)

**On screen (doodle):** the coffee order turning into a neat answer coming out of the MODEL box, with the caption "Role + Task + Context + Format".

**Narration:**
> "So: a prompt is just your instruction to the AI — the words you hand it. Vague words get vague answers; a clear order with a role, a task, some context, and a format gets you exactly what you pictured. Same machine every time. The difference is you."

**User note — the one-line mnemonic:**
> **"A prompt is your coffee order — say it clearly and you get what you wanted; mumble it and you get whatever."**

---

## 📊 POWERPOINT OUTLINE (matches `03_Prompt.pptx`)

**Slide 1 — Title:** *What's a "Prompt"? — Explained Simply*
- One core AI term, ~3 minutes, plain words
- Anchor example: the **Message** and **System Prompt** boxes in Mistral's console
- Episode 3 of "AI Explained Simply"

**Slide 2 — The un-magic secret (What & Why):**
- A prompt = **your instruction to the AI — the words you type**
- Like a search box, but it reads your *whole sentence*, not just keywords
- The *way* you ask is the steering wheel, not decoration
- Like a coffee order: "coffee" vs "large oat flat white, extra hot"
- Most "dumb AI" moments are really vague-prompt moments

**Slide 3 — How it works:**
- Your prompt is chopped into **tokens** and fed to the model
- It becomes the *running start* for next-word guessing (Episode 2)
- Specific prompt → focused guesses; vague prompt → average, generic output
- The recipe: **Role + Task + Context + Format**

**Slide 4 — Where in Mistral (screenshot description):**
- Open **console.mistral.ai** → Le Chat / API playground
- Bottom of screen: the wide **"Message"** box — your prompt goes here
- Higher up: a **"System Prompt"** box — the standing instruction (next episode)
- A prompt = the subject line + brief of an email

**Slide 5 — Try it yourself:**
- Step 1: Send the lazy prompt — just "marketing" — see the generic reply
- Step 2: Send the rich prompt — role + task + context + format
- Step 3: Compare — same model, no extra cost, far better answer
- Takeaway: **you don't buy a smarter AI — you become a clearer asker**

---

## 🎨 DOODLE LIST (simple enough for anyone to sketch)

1. **prompt_bubble.png** — a person typing, a speech bubble labeled PROMPT flowing into a glowing MODEL box.
2. **search_vs_chat.png** — a Google search bar on the left, an arrow, a chat answer on the right: "same habit, richer answer".
3. **coffee_order.png** — two cups: "coffee" (sad, generic) vs "large oat flat white, extra hot" (great), caption "same machine".
4. **tokens_drop.png** — a sentence breaking into little tiles dropping into the MODEL box, answer printing word by word.
5. **recipe_card.png** — a recipe card reading "Role + Task + Context + Format".
6. **two_boxes.png** — the Mistral console: a bottom "Message" box and a higher "System Prompt" box with a gear icon.
7. **signpost.png** — a signpost: "Next → System Prompt: the standing instruction behind every answer".

---

## ✅ WHAT / WHERE / HOW / WHY — quick reference card

| Question | One-line answer |
|----------|-----------------|
| **What** is a prompt? | Your instruction to the AI — the words you type to tell it what you want. |
| **Where** in Mistral? | The **"Message" box** at the bottom of Le Chat / the API playground on console.mistral.ai (with a separate **"System Prompt"** box above). |
| **How** does it work? | It's split into tokens and becomes the running start for the model's next-word guessing — specific in, specific out. |
| **Why** care? | Prompting is the one AI skill that improves results in every tool, today, for free — you become a clearer asker instead of buying a smarter AI. |

---

*Disclaimer: informational and educational only. Console layout and model names may change — explore live at console.mistral.ai. This lesson is a draft for review, not legal or professional advice.*
