---
type: inventory
source: GitHub
captured: 2026-07-31
repos: [sourovdeb/my_professional_documents, sourovdeb/free_education]
---

# GitHub Inventory

Two repositories are in scope for this session. Both are content repositories
rather than software projects: the commit history *is* the session history,
because almost every commit was authored by a Claude Code session or routine.

---

## `sourovdeb/my_professional_documents`

Default branch `main`. Head at capture: `4750f07` — *Merge pull request #101
from sourovdeb/claude/devto-blog-automation-llaguj* (2026-07-25).

### Tracked files by top-level directory

| Directory | Files | Subject | Tags |
|---|---|---|---|
| `archives/` | 218 | Infrastructure & Archival | `#backup-and-archive` |
| `Story_of_Sourov/` | 138 | Health, Wellbeing & Productivity | `#personal-sensitive` `#biography-and-life-history` |
| `agents/` | 37 | AI & Agent Engineering | `#agent-skill-authoring` |
| `Claude_Code_Artifacts/` | 34 | Infrastructure & Archival | `#automated` |
| `cv_and_applications/` | 25 | Career, CV & Job Search | `#cv-and-letters` |
| `Presentations/` + `presentations/` | 23 + 6 | Education & Language Teaching | `#artifact-slides` |
| `CELTA_Teaching_Materials/` | 21 | Education & Language Teaching | `#teacher-training` |
| `Email_Extension/` | 19 | Infrastructure & Archival | `#gmail` `#artifact-script` |
| `AI_Term_Lessons/` | 19 | AI & Agent Engineering | `#artifact-lesson` |
| `tools_and_scripts/` | 17 | Infrastructure & Archival | `#artifact-script` |
| `docs/` | 17 | Infrastructure & Archival | — |
| `00_COMMAND_CENTER/` | 17 | Infrastructure & Archival | `#repo-organisation` |
| `content/` | 16 | Content Publishing & Web Ops | `#public-facing` |
| `Growth_Hub/` | 16 | Health, Wellbeing & Productivity | — |
| `Legal_Documents/` | 12 | Migration, Law & Admin | `#personal-sensitive` |
| `wordpress_integration/` | 11 | Content Publishing & Web Ops | `#wordpress` `#artifact-script` |
| `Biography_and_Medical/` | 11 | Health, Wellbeing & Productivity | `#personal-sensitive` |
| `initiatives/` + `Initiatives/` | 10 + 4 | Infrastructure & Archival | — |
| `browser_extension/` | 9 | Infrastructure & Archival | `#artifact-script` |
| `therapy_and_wellbeing/` | 8 | Health, Wellbeing & Productivity | `#personal-sensitive` |
| `posts/`, `guides/` | 8, 8 | Content Publishing & Web Ops | `#public-facing` |
| `Communications/` | 7 | Career, CV & Job Search | `#gmail` |
| `weekly-briefings/` | 5 | Research & Trend Monitoring | `#artifact-report` |
| `scripts/` | 5 | Infrastructure & Archival | `#artifact-script` |
| `migration-law/`, `microblog/`, `legal/` | 4, 4, 2 | Migration, Law & Admin | `#migration-policy` |
| `bengali-radio/`, `eu-education/`, `contact_network/` | 4 each | mixed | — |
| `devto_integration/` | 1 | Content Publishing & Web Ops | `#devto` `#artifact-script` |
| `gmail_and_email_tools/` | 4 | Infrastructure & Archival | `#gmail` |
| `job_leads/` | 3 | Career, CV & Job Search | `#indeed` |
| `Uncertainty_Growth_Science.pptx` | 1 | Education & Language Teaching | `#artifact-slides` |

**Naming defects worth fixing.** Four case-duplicate pairs exist —
`Presentations`/`presentations`, `Initiatives`/`initiatives`,
`Profile_Documents` as both a directory and a stray file — and five paths are
tracked with a **literal leading double-quote** in the filename
(`"cv_and_applications`, `"Profile_Documents`, `"tools_and_scripts`,
`"Email_Extension`). Those came from a shell quoting error in an earlier
automated commit and will break any script that globs those directories.

### Commit and PR pattern

The visible history runs 2026-07-19 → 2026-07-25. **2026-07-19 alone carries
roughly 35 merge commits** (PRs #40–#79), nearly all auto-generated branch names
of the form `sourov/<adjective>-<surname>-<hash>` or
`claude/<slug>-<hash>`. This is the multi-platform sync build-out
(`feat: multi-platform sync system (WordPress, Dev.to, Box, IndexNow)`) plus the
aggressive WordPress content push described in `CLAUDE.md`.

Later, lower-volume work:
- 2026-07-22 — Three Operational Modes ELT tutorial draft
- 2026-07-24 — site monetization & compliance package (PR #90, #93), advertiser
  attraction plan, Episode 2 AI-model lesson, daily human-nature articles
- 2026-07-25 — AI Explained Simply mindmap (`.mm`), Dev.to publisher script (PR #101)

One revert is recorded: *Revert "Sync: 1 essay ready for WordPress (auth pending
fix)"* (PR #79 reverting #77) — the WordPress auth failure referenced in
`CLAUDE.md`'s known issues.

---

## `sourovdeb/free_education`

Default branch `main`. Head at capture: `f1af4c4` — *Merge pull request #50 from
sourovdeb/claude/dissident-academic-reinsertion-b7cdcp*.

| Path | Files | Subject | Tags |
|---|---|---|---|
| `routines/02_python_toolkit_routine/` | 10 | AI & Agent Engineering | `#artifact-script` |
| `routines/01_elt365_lessons_routine/` | 5 | Education & Language Teaching | `#elt-lesson-series` |
| `routines/03_human_nature_routine/` | 4 | Psychology & Human Nature | `#artifact-article` |
| `python_toolkit/` | 10 | AI & Agent Engineering | `#artifact-script` |
| `elt365_lessons/` | 5 | Education & Language Teaching | `#elt-lesson-series` |
| root (`CLAUDE.md`, `README.md`, `MASTER_INDEX.md`, `LICENSE`, `sync_verification.py`) | 5 | Infrastructure & Archival | — |

`elt365_lessons/` contains `LESSON_INDEX.md`,
`ELT365_M06_Receptive_Skills_D152-181.md`,
`YL_Young_Learners_10_Lessons.md`,
`PRO_Professional_Development_10_Lessons.md`, and a `publisher` entry.

`python_toolkit/` carries **five duplicate pairs** — `audio2txt.py` /
`audio2txt (1).py`, `pdf2txtv2.py` / `pdf2txtv2 (1).py`, `webscrapper.py` /
`webscrapper (1).py`, `ai_file_organizer_pro.py` / `ai_file_organizer_pro_v2.py`
— the browser-download `(1)` suffix committed as-is.

Recent work: 3 human-nature deep-dive articles (covert ops, dissident
reinsertion, primal obedience), a 19-slide deck for that series, 3 university
slides on narrative capture, and an ELT-keyword pass for organic search.

---

## What the repo history does and does not preserve

**Preserved:** what each session produced, when, and on which branch. Commit
messages are unusually descriptive here, so the history reads as a decent
activity log.

**Not preserved:** why. The auto-generated branch names
(`sourov/nifty-goodall-asx1xb`) carry no meaning, and no commit records what was
considered and rejected. Reconstructing intent from this history alone is
guesswork — which is the gap `../sessions/` and the reasoning logs are meant to
close from now on.

**Note on `CLAUDE.md`.** Both repositories' `CLAUDE.md` files carry a
`Session history` section that is the closest existing thing to a chat log —
`my_professional_documents` records three 2026-07-19 sync sessions with times
and push counts. It is a good habit and this archive is a formalisation of it,
not a replacement.
