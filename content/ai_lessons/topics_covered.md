# AI Terms Explained — Series Tracker

A running log of the "AI Terms Explained" doodle lesson series: one core AI concept per
lesson, explained with Office Suite / browser analogies and a live Mistral Studio example.

## Covered

| # | Topic | Folder | Status |
|---|-------|--------|--------|
| 1 | AI Agent | `lesson_01_ai_agent/` | Done |

## Topic pipeline (via brainstorm-agent diverge → debate pass)

Reference: [`brainstorm-agent.skill`](https://github.com/sourovdeb/ai_agent_skills/blob/main/skills/brainstorm-agent.skill)
was used to generate and stress-test the candidate list below — diverge (list every
plausible everyday AI term), then debate (drop anything too niche, too overlapping with
an already-covered term, or too hard to show live in Mistral Studio).

**Diverge pool:** memory, hook, skill, model, prompt, JSON, Python, context window, token,
fine-tuning, embedding, RAG, temperature, system prompt, function/tool calling, hallucination,
inference, API, guardrail, multimodal.

**Debate cuts:** dropped *fine-tuning*, *embedding*, *RAG* for now — each needs its
predecessor terms (model, tool calling) explained first, or it overloads a 2–5 min format.
Dropped *temperature* and *context window* as second-tier — useful, but less "everyday"
than the next five.

**Selected order (next up first):**

1. **Memory** — how an AI keeps track of what you said earlier (vs. starting fresh every time)
2. **Skill** — a packaged, reusable set of instructions (like a Word template or Office add-in)
3. **Hook** — an automatic trigger that runs on an event (like a mail rule or a spreadsheet macro-on-open)
4. **Model** — the "engine" underneath, vs. the app/agent built on top of it
5. **JSON / structured output** — how apps hand data to each other, like a filled-in form vs. free text
6. **Python (for non-coders)** — what it is in the "why does everything run on it" sense
7. **Prompt** — the instructions you give, and why wording changes the result (like a search query)
8. **Tool calling / function calling** — how an agent actually "reaches out" to use a tool

Each future lesson should append its entry to the **Covered** table above and trim the
completed topic off the **Selected order** list.
