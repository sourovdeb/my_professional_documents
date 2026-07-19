# AI Concepts Made Simple — Lesson Series Tracker

A recurring series of 2–5 minute lessons that explain one core AI term at a time in plain, everyday language — using Office Suite and web browser analogies, with Mistral Studio as the concrete real-world example. Each episode ships as a video script/outline (with doodle-visual and presenter-notes callouts) plus a matching PowerPoint deck.

Each episode lives in its own numbered folder:

```
AI_Lessons/
  01_AI_Agent/
    Lesson_01_AI_Agent_Script.md   <- video script, slide outline, doodle descriptions, presenter/user notes
    Lesson_01_AI_Agent.pptx        <- matching slide deck with doodle-style graphics + speaker notes
```

## Covered so far

| # | Topic | Folder |
|---|-------|--------|
| 1 | Agent | `01_AI_Agent/` |

## Suggested next topics (in build order)

Each builds on the last, so later lessons can reference earlier ones without re-explaining them.

2. **Model** — the "brain" that powers an agent's reasoning
3. **Prompt** — the instruction you hand the model
4. **Token** — how the model reads/measures text
5. **Memory** — what an agent remembers between turns
6. **Skill / Tool** — a capability an agent can call on
7. **System Prompt** — the standing instructions behind the scenes
8. **Context Window** — how much the model can "see" at once
9. **RAG (Retrieval-Augmented Generation)** — looking things up before answering
10. **Fine-tuning vs. off-the-shelf** — teaching a model new habits

## Adding a new episode

1. Pick the next topic from the list above (or propose a new one if the backlog runs out — check this table first so topics aren't repeated).
2. Create `AI_Lessons/0N_Topic_Name/`.
3. Write `LessonN_Topic_Name_Script.md` following the structure used in Lesson 1 (hook → plain definition → 2 everyday analogies → Mistral Studio example → recap → next-episode teaser), including `[DOODLE]` visual descriptions and presenter/user notes per beat.
4. Build the matching `.pptx` with the same beats, doodle-style graphics, and speaker notes.
5. Update the "Covered so far" table and trim the "Suggested next topics" list above.
