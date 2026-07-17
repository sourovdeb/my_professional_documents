# AI Term Lessons — Index

Short (2–5 minute) educational lessons that explain one core AI term at a time, in plain
language, using everyday software analogies (Office apps, browsers, basic computer tasks)
and **Mistral Studio** as the running concrete example of each concept in practice.

Each lesson ships as a matched pair:
- `NN_<Term>_Lesson_Script.md` — read-aloud script / outline, timed for video, and also
  usable as a written lesson or slide outline.
- `NN_<Term>_Lesson.pptx` — a doodle-illustrated companion deck with matching speaker
  notes on every slide.

## Covered so far

| # | Term | Files | Everyday analogy used |
|---|------|-------|------------------------|
| 1 | **Agent** | `01_AI_Agent_Lesson_Script.md`, `01_AI_Agent_Lesson.pptx` | Word spell-check (model, no hands) vs. an assistant with a browser, email, and a checklist (agent, acts on a goal) |
| 2 | **Model** | `02_Model_Lesson_Script.md`, `02_Model_Lesson.pptx` | Excel's calculation engine (model — predicts, no memory or buttons) vs. the full Excel app (agent — the vehicle built around the engine) |
| 3 | **Memory** | `03_Memory_Lesson_Script.md`, `03_Memory_Lesson.pptx` | A blank search tab (no memory) vs. Word's Undo history (short-term, within one document) and its "recent documents" list (long-term, across sessions) |

## Suggested next topic

**#4 — "Skill"** — how an agent gets a new, reusable capability bolted on, instead of
just remembering more — the way an Office add-in bolts a new button onto the ribbon.

Other concepts still on the list, in a sensible teaching order:
`Skill → Hook → Workflow → JSON → Python`

## Note on prior duplicate drafts

Two earlier, independently-generated drafts of the "Agent" lesson exist as open PRs on
this repo (**#56** and **#57**) — they were produced by earlier runs of the same
automated content routine, before this branch consolidated the series into one place.
Once this PR is reviewed, #56 and #57 can be closed as superseded.

## Note on this update (2026-07-17)

Another independent run of the same automated routine initially redrafted "Agent" as
Lesson 1 again (as PR #60). Rather than ship a third duplicate Agent lesson, that PR was
rebuilt on top of this branch (#58) to add the next lesson the index actually asked
for — **Memory** (Lesson 3) — so the series moves forward instead of circling back.
