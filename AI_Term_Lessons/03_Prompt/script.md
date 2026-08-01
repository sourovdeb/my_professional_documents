---
series: "AI Explained Simply"
episode: 3
term: "Prompt"
date: 2026-08-01
format: ["video script", "PowerPoint outline", "doodle notes"]
duration_target: "2:30–3:30 (fits the 2–5 min window)"
worked_example: "Mistral Studio (mistral.ai/products/studio) + console.mistral.ai"
---

# Episode 3: What's a "Prompt"? (in about 3 minutes)

*One core term per episode. Plain words, everyday analogies, one real product to anchor it. In Episode 1: "Model talks. Agent walks." In Episode 2 we opened up the model — a big pile of remembered data + computing muscle + language skill. This episode is about the one thing that turns all that muscle on: the **prompt** — what you actually type.*

---

## 0. Cold open (0:00–0:20)

**On screen (doodle):** a search bar exactly like Google's, and next to it a chat bubble with a blinking cursor. A big arrow points from your fingers on a keyboard into the box. Caption underneath in marker pen: **"A prompt = the thing you type."**

**Narration:**
> "Silicon Valley has a fancy job title now — 'prompt engineer' — and it makes this sound complicated. It isn't. A prompt is just the words you type to an AI. If you've ever typed something into a Google search box, you've written a prompt. That's the whole idea. The rest of this lesson is about typing *better* ones."

**User note:** Sticky-note version: **A prompt is your instruction to the AI — the message you send it.** Nothing more. The skill isn't magic; it's just being clear about what you want.

---

## 1. Demystifying it: it's an instruction, like any other (0:20–1:05)

**On screen (doodle):** three familiar boxes in a row, each with a plus sign — a Google search bar ("weather Paris"), an Office "Find & Replace" box, and a text-message bubble ("bring milk"). Then an equals sign and one glowing box labeled **PROMPT**.

**Narration:**
> "You already give instructions to software all day. You type 'weather Paris' into a browser. You type what you're hunting for into Word's Find box. You text a friend 'can you bring milk?'. Every one of those is an instruction in plain words.
>
> A prompt is the same move, pointed at a model. The difference is the model can handle a *much* bigger, messier instruction — a whole paragraph, not just two words — and it writes something back instead of just finding a match."

**Everyday analogy:** A search engine takes a few keywords and hands you a list of links. A prompt takes a full request — *"write a polite email declining this meeting"* — and hands you the finished thing. Same slot, bigger order.

**User note — the honest bit:** The AI can't read your mind; it can only read your words. A vague prompt gets a vague answer. A specific prompt gets a specific answer. **The quality of what comes out is mostly decided by what you put in.** You still bring the intent; it brings the typing.

---

## 2. So how does it actually work? (1:05–1:45)

**On screen (doodle):** the prompt "Write a haiku about rain" flowing into the MODEL box from Episode 2. Inside, the words break into little tiles (tokens), the machinery whirs, and out comes three lines of a poem, printed one word at a time.

**Narration:**
> "Here's the mechanism, no mystery. Your prompt goes into the model as the *opening* of the text. Remember Episode 2 — the model does one thing: guess the next word. So it reads your words and starts continuing them.
>
> Type 'Write a haiku about rain', and the most likely continuation *isn't* a chat about rain — it's an actual haiku. Your prompt sets the direction; the next-word guessing does the rest. Change the prompt and you change the starting point, so you change everything that comes after."

**Everyday analogy:** It's like the first domino. You place one domino — the prompt — and the whole line of guesses falls in that direction. Nudge the first domino a different way and the pattern changes completely.

**User note:** This is *why* small wording changes matter so much. "Explain this" and "Explain this to a 10-year-old in three sentences" send the dominoes down two very different tracks. Be specific about **who it's for, how long, and what format** — and you'll steer the output on purpose instead of by luck.

---

## 3. Seeing it for real: Mistral Studio (1:45–2:40)

**On screen (doodle):** a simple sketch of the Mistral chat screen — a wide message box at the bottom labeled "type your prompt here", a send arrow, and the reply appearing above it.

**Narration:**
> "Let's make it real in Mistral Studio — Mistral AI's platform for building and running agents. Open **console.mistral.ai** and go to **Le Chat** (their chat playground). At the bottom there's one big text box. That box is where your prompt lives.
>
> Type a lazy prompt first: 'email about the picnic'. Send it — you'll get something generic. Now type a *good* prompt in the same box: 'Write a short, cheerful email inviting my team to a Saturday picnic at 12pm, mention to bring an umbrella, keep it under 80 words.' Send that. Same model, same box — but a sharper instruction, so a sharper result."

**On screen (doodle):** two reply bubbles side by side — a thin vague one labeled "lazy prompt" and a full, tidy one labeled "clear prompt" with a little star.

**Narration:**
> "One more thing you'll spot in Studio: separate from that chat box, there's a **System Prompt** field — a place to set standing rules like 'always answer in simple English'. That's a prompt too, just a permanent one. We'll give it its own episode."

**User note:** In Studio, your prompt is the message box at the bottom of Le Chat. Try the same request twice — once lazy, once specific — and read both replies. That five-second experiment teaches prompting better than any course.

---

## 4. Why should you care? (2:40–3:10)

**On screen (doodle):** a hand turning a steering wheel; the road ahead splits into several paths labeled "email", "summary", "poem", "code".

**Narration:**
> "Prompting is the steering wheel for every AI tool you'll ever touch — the chatbot, the image maker, the coding helper, the agent. You don't need to know the math inside the model. You need to know how to ask. Learn to write clear prompts and you can get useful work out of any of these tools today, for free."

**User note — takeaway:** Better prompts, not fancier tools, is the fastest upgrade available to you. Ask like you'd brief a smart new assistant: **say who it's for, what you want, how long, and in what format.**

---

## 5. Close (3:10–3:30)

**On screen (doodle):** the sticky note from the start, now with a checkmark: **"Prompt = what you type. Be specific → get specific."**

**Narration:**
> "So — a prompt is just the words you send the AI, and how clearly you say them decides how good the answer is. It's the first domino. Place it on purpose. Next episode: **Token** — the little tiles a model actually chops your words into. See you there."

---

## 📊 PowerPoint outline (5 slides)

**Slide 1 — Title:** What's a "Prompt"?
- Explained Simply — in about 3 minutes
- AI Explained Simply · Episode 3
- Anchor example: the message box in Mistral's Le Chat

**Slide 2 — What & Why:** It's just the thing you type
- A prompt = your instruction to the AI, in plain words
- If you've searched Google, you've written a prompt
- Vague prompt → vague answer; specific prompt → specific answer
- You bring the intent; the model brings the typing

**Slide 3 — How it works:** The first domino
- Your prompt = the opening the model continues
- The model guesses the next word from where you started
- "Write a haiku about rain" → the likely continuation IS a haiku
- Small wording changes send the dominoes down different tracks

**Slide 4 — Where in Mistral:** The message box
- console.mistral.ai → Le Chat → the wide box at the bottom
- Type there, hit send — that's a prompt
- Separate "System Prompt" field = a standing, permanent prompt
- Lazy prompt vs. clear prompt: same model, different result

**Slide 5 — Try it yourself!**
- Step 1: Open Le Chat and type "email about the picnic" — send
- Step 2: Now type a specific version (who, what, length, tone) — send
- Step 3: Compare the two replies side by side
- Takeaway: brief the AI like a smart new assistant — who, what, how long, what format
- Next episode → Token: the tiles a model chops your words into

---

## 🎨 Doodle checklist (for the illustrator)

1. **Cold open:** search bar + chat bubble, arrow from keyboard, caption "A prompt = the thing you type."
2. **Demystify:** three familiar boxes (Google search, Word Find, text message) + = PROMPT.
3. **Mechanism:** prompt flowing into the MODEL box, words breaking into tiles, poem printing out.
4. **Domino:** first domino labeled "prompt" tipping a whole line.
5. **Mistral screen:** message box at bottom, send arrow, reply above; two reply bubbles (lazy vs. clear).
6. **Why:** hand on steering wheel, road forking into email/summary/poem/code.
7. **Close:** sticky note "Prompt = what you type. Be specific → get specific." with a checkmark.
