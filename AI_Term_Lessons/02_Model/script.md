# AI Terms in Plain English, Episode 2: What's a "Model"?

**Format:** video/voiceover script + written lesson + slide outline
**Length:** ~3.5 minutes spoken (about 480 words)
**Slides:** see `02_Model.pptx` in this folder (8 slides, same beats as below)

---

## SLIDE 1 — Title

**On screen:** "What's an AI Model?" / AI Terms in Plain English, Ep. 2

**[DOODLE]** A simple brain drawn inside a cube/box, with small gears turning inside it — labeled "MODEL."

**Script:**
Last time we covered "agent." Today's word is the thing every agent actually runs on: the "model." Under four minutes, plain English, let's go.

---

## SLIDE 2 — The everyday hook

**On screen:** Phone keyboard showing predictive-text suggestions above the letters

**[DOODLE]** A phone with three suggestion bubbles floating above the keyboard, each bubble slightly more confident-looking (bigger) than the last.

**Script:**
Think about the predictive text on your phone keyboard. You type "I'll see you," and it guesses "tomorrow," "later," or "soon." It's not reading your mind — it's guessing the next most likely word based on patterns it has seen before. An AI model does exactly that, just at a much bigger scale.

---

## SLIDE 3 — The plain-English definition

**On screen:** "AI Model = a trained pattern-guesser that predicts the next best word (or answer)"

**[DOODLE]** A funnel: millions of book/document icons pouring in at the top, one confident lightbulb icon coming out the bottom.

**Script:**
An AI model is software that has been trained on huge amounts of text, so it has learned the patterns of language, facts, and reasoning. When you give it words, it predicts — piece by piece — the most likely next words that make a good answer.

---

## SLIDE 4 — Model vs. Agent

**On screen:** two-column comparison

| A Model | An Agent |
|---|---|
| The "brain" — predicts text, answers questions | The "assistant" — uses a model plus tools and steps |
| Has no memory or goals of its own | Plans steps, remembers context, checks its own work |
| Like the engine in a car | Like the whole car, with a driver deciding where to go |

**[DOODLE]** A car engine block labeled "Model" sitting next to a full car with a tiny driver icon labeled "Agent."

**Script:**
From Episode 1, remember an agent plans its own steps toward a goal. A model doesn't do any of that by itself — it's just the engine. The agent is the whole car: it takes the model's engine, adds a driver (the goal), a steering wheel (tools), and a route (the plan).

---

## SLIDE 5 — Seeing it in a real product: Mistral Studio

**On screen:** Mistral Studio "Model" dropdown showing options like "Mistral Large," "Mistral Medium," "Mistral Small"

**[DOODLE]** A dropdown menu doodle with three boxes labeled Large, Medium, Small — a bigger brain icon next to "Large," a smaller brain icon next to "Small."

**Script:**
In Mistral Studio, when you build an agent, one of the first things you do is pick its model from a dropdown menu — options like Mistral Large, Medium, or Small. Large is the biggest, most capable brain, good for hard reasoning. Small is faster and cheaper, good for simple, high-volume tasks. Picking a model is like picking which size engine goes in your car: more power costs more fuel.

---

## SLIDE 6 — Why this matters

**On screen:** "Bigger model = smarter answers, but slower & pricier"

**[DOODLE]** A simple see-saw: "Quality & Power" on one side, "Speed & Cost" on the other, tipping back and forth.

**Script:**
Knowing what a model is means you can make a real choice: use a big model for the hard stuff, and a small, cheap one for simple stuff, instead of always defaulting to the most expensive option. That trade-off — power versus speed and cost — is one of the first real decisions anyone builds in on a platform like Mistral Studio.

---

## SLIDE 7 — Recap

**On screen:** 3 bullet recap

**Script:**
Quick recap. A model is a trained pattern-guesser that predicts the next best words — the engine, not the driver. An agent is the whole car that uses a model plus tools and a plan. And in Mistral Studio, you pick the model size for each agent from a simple dropdown.

---

## SLIDE 8 — Closing / next episode

**On screen:** "Next time: what's a 'Prompt'?"

**Script:**
That's "model" in plain English. Next time: "prompt" — how you actually talk to a model to get what you want. See you then.

---

## Sources used for accuracy

- Mistral Studio / Mistral AI platform documentation (mistral.ai) — description of model selection (Mistral Large / Medium / Small) as a per-agent configuration step.
- General description of language model next-token prediction — standard, widely documented mechanism behind large language models.

---

## User / presenter notes

- Keep the "engine vs. car" analogy consistent across future episodes — Episode 1 already set up "agent = assistant/car," so this episode should feel like a direct continuation, not a new metaphor.
- Common mistake to flag verbally: people often say "the AI" when they mean the model, then separately when they mean the agent. This episode's job is to make that distinction stick.
- If recording live: hold up (or point at) a real Mistral Studio model dropdown screenshot on Slide 5 rather than only describing it — it lands better than words alone.
