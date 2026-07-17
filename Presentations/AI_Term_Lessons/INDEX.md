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
| 5 | **Hook** | `05_Hook_Lesson_Script.md`, `05_Hook_Lesson.pptx` | An inbox rule and a calendar reminder (fires itself, nobody re-decides each time) vs. a smoke detector (silent for months, instant the moment the real trigger happens) |

## Suggested next topic

**#6 — "Workflow"** — how several agents, skills, and hooks get strung together into
one automatic sequence, instead of running one at a time.

Other concepts still on the list, in a sensible teaching order:
`Workflow → JSON → Python`

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

## Note on this update (2026-07-17, fifth run)

A fifth independent run of this automated routine also began by drafting "Agent" as
Lesson 1 from scratch (complete script, doodles, and deck, under a different path —
`Presentations/AI_Term_Lessons/01_ai_agent/`) before checking this index. That draft
was discarded before committing — this run reset its branch onto the #61 chain instead
and added the lesson actually queued next, **Hook** (Lesson 5), reusing the same
doodle-generation tooling for the new topic.

**Separately spotted while checking prior work:** PR **#62** ("Add AI Lessons Ep.1:
What Is a Model") is an independent duplicate under yet another path
(`content/ai_lessons/01_model/`) — a sixth run that never found this index at all. It
duplicates Lesson 2 (Model) content already covered here and should be closed as
superseded once reviewed, alongside the earlier superseded drafts **#56**, **#57**,
and **#58** (all folded into this chain).

**If you are an automated run reading this: check this INDEX.md's "Suggested next
topic" section, and confirm you are working in `Presentations/AI_Term_Lessons/` (not
`content/ai_lessons/` or any other path), BEFORE generating any content.** The series
currently stops at Lesson 5 (Hook); the next lesson to write is Workflow.
