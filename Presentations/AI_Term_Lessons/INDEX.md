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
| 4 | **Skill** | `04_Skill_Lesson_Script.md`, `04_Skill_Lesson.pptx` | A Word/Excel add-in and a browser extension (install once, bolted on) vs. learning to change a tire (one reusable, ready-when-needed capability) |

## Suggested next topic

**#5 — "Hook"** — what actually triggers an agent (or a skill) to run in the first
place, instead of it sitting idle waiting to be asked.

Other concepts still on the list, in a sensible teaching order:
`Hook → Workflow → JSON → Python`

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

## Note on this update (2026-07-17, later same day)

Yet another independent run of the same automated routine initially redrafted "Agent"
as Lesson 1 for a fourth time (opened as PR #61, on branch
`sourov/charming-clarke-3w6oth`). Per this index's own instruction, that draft was
discarded and the branch was reset onto this chain (#60) to add the lesson actually
queued next — **Skill** (Lesson 4) — instead of shipping another duplicate. If your
routine reads this index before starting work, please check the "Suggested next topic"
section above first.
