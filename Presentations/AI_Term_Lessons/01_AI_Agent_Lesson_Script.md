# AI Term Lesson #1: What Is an "AI Agent"?

**Format:** Short video script / read-aloud lesson
**Length:** ~3.5 minutes (≈520 words at conversational pace)
**Companion deck:** `01_AI_Agent_Lesson.pptx` (6 slides, timings noted below)

---

## SCRIPT

### [0:00–0:15] — Hook
**(Slide 1 — Title)**

> Quick question: what's the difference between a chatbot that just *answers* you, and one that actually *goes and does the thing*? That difference has a name — it's called an **AI agent**. Let's unpack it in three minutes.

### [0:15–0:50] — Plain-language definition
**(Slide 2 — Definition)**

> An AI agent is an AI that doesn't just talk — it **acts**. You give it a goal, and it decides the steps, uses tools, and checks its own work until the goal is done.
>
> Think of the difference between a GPS that only *tells* you the directions, versus a self-driving car that actually *takes* those directions and drives. A plain AI model is the GPS. An agent is the self-driving car — same map, but one of them takes the wheel.

### [0:50–1:40] — The familiar-software analogy
**(Slide 3 — Analogy)**

> You've actually used something like this before, even outside AI.
>
> In an Office spreadsheet, a **macro** doesn't just show you a formula's answer — you press one button, and it opens files, copies data, formats cells, and saves the result. That's a fixed script, though: it only ever does the exact steps you recorded.
>
> An AI agent is like a macro that can also **think for itself**. Instead of following a fixed recording, you tell it the *goal* — "clean up this spreadsheet and email me a summary" — and it figures out the steps on its own, adapting if something looks wrong along the way.
>
> Or picture a browser: a normal browser tab shows you a webpage and waits for you to click. An agent is more like that tab *plus* someone sitting at the keyboard — clicking links, filling in forms, and reading the results, on your behalf.

### [1:40–2:50] — Concrete example: Mistral Studio
**(Slide 4 & 5 — Mistral Studio walkthrough)**

> Here's what that looks like in a real product: **Mistral Studio's "Agents"** feature.
>
> In Mistral Studio, you don't just chat with the model — you build an **Agent**: you give it a name, a job description in plain English ("You are a research assistant who summarizes PDFs and drafts follow-up emails"), and you switch on **tools** — web search, code execution, a document library, or connections to other apps.
>
> From there, when someone asks that Agent a question, it doesn't just generate one reply. It plans: *"I need to search the web first, then read this document, then write the summary."* It calls the web-search tool itself, reads what comes back, and only then writes your answer — all without you clicking through each step.
>
> That planning-and-tool-use loop — decide, act, check, repeat — is the whole idea of an agent. Mistral Studio just gives you a visual, no-code way to build one.

### [2:50–3:20] — Recap
**(Slide 6 — Recap)**

> So, in one sentence: **a plain AI model answers; an AI agent acts** — planning steps and using tools to actually finish a job, the way a self-driving car uses a map instead of just reading it aloud.
>
> Next time you open an "Agents" tab in a tool like Mistral Studio, ChatGPT, or Claude, you'll know exactly what's happening under the hood.

### [3:20–3:30] — Teaser for next lesson
**(Slide 6, footer note)**

> Next time: what's a **"model"**, really — and how is it different from the agent we just described? See you then.

---

## SPEAKER / PRODUCTION NOTES
- Pace: ~150 words per minute; pause ~1 second between slides.
- On-screen text should mirror the **bolded phrases only** — keep slides sparse, let the narration carry detail.
- If recording as a talking-head video: cut to a screen-recording of Mistral Studio's Agent builder during the [1:40–2:50] section if available; otherwise use the diagram on Slide 5.
