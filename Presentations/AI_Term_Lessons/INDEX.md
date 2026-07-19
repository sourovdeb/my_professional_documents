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
| 6 | **Workflow** | `06_Workflow_Lesson_Script.md`, `06_Workflow_Lesson.pptx` | An Outlook rule with several chained actions, an online checkout (cart → shipping → payment → confirmation), and a coffee maker's "brew" button (grind → brew → keep-warm) |
| 7 | **JSON** | `07_JSON_Lesson_Script.md`, `07_JSON_Lesson.pptx` | An Outlook contact card (Name: , Email: , Phone: — already-labeled fields), a browser's Network tab (pages quietly fetch `{ }`, not more webpage), and a recipe card's "Ingredients:" list (one label pointing at a whole list — nesting) |
| 8 | **Python** | `08_Python_Lesson_Script.md`, `08_Python_Lesson.pptx` | An Excel formula bar (`=SUM(A1:A10)` is already a tiny program), a browser's Console tab (type a line, it runs instantly), and a recipe's numbered steps (done in order, step 2 waits on step 1) |

## Suggested next topic

**#9 — "Prompt"** — the instruction you actually hand the model to get it started.

Lesson 8 (Python) closes out the original seed list from the task brief
(`memory, hook, skill, agent, model, JSON, Python`) — it is now fully covered. Good
candidates for a next batch, in a sensible teaching order:
`Prompt → Token → Context Window → API → Fine-tuning`.

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

## Note on this update (2026-07-17, seventh run)

A **seventh** independent run of this automated routine also began by drafting
"Agent" as Lesson 1 from scratch — full script, doodles (matplotlib/xkcd-style), and
a PowerPoint deck — under yet another new path
(`Presentations/AI_Concepts_Lessons/01_AI_Agent/`), including uploading a script and
an HTML slide view to this repo's Box folder, all before reading this index. Once the
draft reached the Box-upload step, it surfaced this same `AI_Term_Lessons` folder
already containing Lessons 1–5 and this INDEX.md — at which point the duplicate work
was discarded (deleted from the local working tree before committing), the designated
branch was reset onto the tip of the existing chain
(`sourov/charming-clarke-b64gnd`, PR **#63**), and this run instead added the lesson
actually queued next — **Workflow** (Lesson 6) — reusing the same doodle-generation
approach (matplotlib line icons, not xkcd-sketch) but matched to this series'
established navy/teal/gold palette and two-column layout (extracted directly from
`05_Hook_Lesson.pptx`'s XML) rather than inventing a new visual style.

**If you are an automated run reading this: check this INDEX.md's "Suggested next
topic" section, and confirm you are working in `Presentations/AI_Term_Lessons/` (not
`Presentations/AI_Concepts_Lessons/`, `content/ai_lessons/`, or any other path),
BEFORE generating any content — including before creating doodles, a deck, or
uploading anything to Box.**

## Note on this update (2026-07-18, eighth run)

This run was assigned a brand-new, unrelated branch (`sourov/charming-clarke-vqbtki`,
carrying one stray, out-of-series commit) with no open PR. Rather than start an eighth
duplicate "Agent" draft on it, this run checked this INDEX.md and Box's
`AI_Term_Lessons` folder first, found the existing chain (Lessons 1–6, PR **#64**,
branch `sourov/charming-clarke-rmnwkw`), and reset the assigned branch onto that
chain's tip before adding genuine forward progress:

- Adds **Lesson 7 — JSON**: `07_JSON_Lesson_Script.md` + `07_JSON_Lesson.pptx` (7
  slides, doodle-illustrated via native PowerPoint shapes — circles, rounded-rect
  pills, triangle arrows — matching the established navy (`1E3A5F`) / teal (`0FA3A3`)
  / gold (`F2C94C`) palette and two-column layout, coordinates and colors extracted
  directly from `06_Workflow_Lesson.pptx`'s XML). Explains JSON as the labeled-pair
  data format via an Outlook-contact-card analogy, a browser Network-tab analogy, and
  a recipe-card analogy, grounded in the same Hook → Agent → Skill → Notify chain from
  Lesson 6 (Mistral Studio) — now shown carrying `{ }` JSON payloads on each arrow.
- Updates this INDEX.md: adds the JSON row, advances the suggested next topic to
  **Python**, and notes that the original seed topic list is exhausted after Python.

The series currently stops at Lesson 7 (JSON); the next lesson to write is Python.

## Note on this update (2026-07-18, ninth run)

This run was assigned a brand-new, unrelated branch (`sourov/charming-clarke-wsxdvy`,
carrying one stray, out-of-series commit — an interdisciplinary-insights presentation)
with no open PR. Before generating anything, it checked this INDEX.md and Box's
`AI_Term_Lessons` folder (which carries the same chain plus its own housekeeping
notes) first, found the existing chain (Lessons 1–7, PR **#65**, branch
`sourov/charming-clarke-vqbtki`) with **Python** explicitly flagged as next, and reset
the assigned branch onto that chain's tip before adding genuine forward progress:

- Adds **Lesson 8 — Python**: `08_Python_Lesson_Script.md` + `08_Python_Lesson.pptx`
  (7 slides, doodle-illustrated via native PowerPoint shapes — parentheses, numbered
  badges, browser-console and formula-bar mocks, the recurring Hook → Agent → Skill →
  Notify chain — matching the established navy (`1E3A5F`) / teal (`0FA3A3`) / gold
  (`F2C94C`) palette and two-column layout, colors extracted directly from
  `07_JSON_Lesson.pptx`'s XML). Explains Python as the ordered, readable
  instruction-language via an Excel-formula-bar analogy, a browser-Console-tab
  analogy, and a recipe's-numbered-steps analogy, grounded in the same Lesson 6–7
  chain (Mistral Studio) — now shown with a `<>` Python tag on every box alongside the
  `{ }` JSON tag already on every arrow.
- Updates this INDEX.md: adds the Python row, advances the suggested next topic to
  **Prompt**, and notes that Lesson 8 closes out the original seed topic list from the
  task brief.

**If you are an automated run reading this: check this INDEX.md's "Suggested next
topic" section, AND confirm you are working in `Presentations/AI_Term_Lessons/` (not
`Presentations/AI_Concepts_Lessons/`, `content/ai_lessons/`, or any other path),
BEFORE generating any content — including before creating doodles, a deck, or
uploading anything to Box.** The series currently stops at Lesson 8 (Python); the next
lesson to write is Prompt.

## Test plan (this run)

- [x] `python scripts/office/validate.py 08_Python_Lesson.pptx` — all structural
  checks passed
- [x] `markitdown 08_Python_Lesson.pptx` — content reviewed slide-by-slide, no
  placeholder text
- [x] Full LibreOffice headless PDF conversion + per-slide visual QA (all 7 slides) —
  `libreoffice-impress`/`libreoffice-writer`/`libreoffice-calc` and `poppler-utils`
  were missing in this sandbox and were installed first; QA caught and fixed a real
  subtitle/body text-overlap bug on three slides (long, 3-line subtitles collided with
  the body paragraph below them) plus two body-paragraph/bullet overlaps caused by
  overlong body copy — all fixed by widening the subtitle's reserved height and
  trimming body-paragraph length, then re-rendered clean.

## Test plan (Lesson 7 — prior run)

- [x] `python scripts/office/validate.py 07_JSON_Lesson.pptx` — all structural checks
  passed
- [x] `markitdown 07_JSON_Lesson.pptx` — content reviewed slide-by-slide, no
  placeholder text
- [x] Full LibreOffice headless PDF conversion + per-slide visual QA (all 7 slides) —
  `libreoffice-impress`/`libreoffice-writer`/`libreoffice-calc` and `poppler-utils`
  were missing in this sandbox and were installed first, then all 7 renders were
  inspected for overflow, overlap, and contrast issues; none found.
