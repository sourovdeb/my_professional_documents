# Repository Map — my_professional_documents

A single index so anyone (including future you, on a low day) can find anything in one look.

## Start here

- **[Growth_Hub/00_START_HERE.md](Growth_Hub/00_START_HERE.md)** — the writing, exposure,
  tools, ideas, contacts, consistency, wellbeing, and automation system. **Read this first.**
- **[posts/README.md](posts/README.md)** — the daily 500-word publishing workflow (git as platform).
- **Daily Living Strategy** (`personal_doc_extracted/.../daily-living/DAILY_LIVING_STRATEGY.md`)
  — the daily operating system the Growth Hub sits on.

## The repository at a glance

| Folder / file | What's inside |
|---------------|---------------|
| `Growth_Hub/` | **The engine.** Eight parts: 01 Write · 02 Exposure · 03 Tools · 04 Ideas · 05 Contacts · 06 Consistency · 07 Wellbeing · 08 Automation. Plus `drafts/`, `IDEA_INBOX.md`, `PUBLISHED_LOG.md`, and `job_search_config.yml`. |
| `posts/` | Public 500-word essays, version-controlled. `drafts/` = banked; `published/` = live. |
| `Story_of_Sourov/` | Organized story, analysis docs, reusable skills, scripts, index guides, archives. |
| `Biography_and_Medical/` | Life story, treatment plan (plain language), medical-document explanations. |
| `Profile_Documents/` | CV models, motivation letters, the CELTA certified-trainer profile PDF. |
| `CELTA_Teaching_Materials/` | Cambridge CELTA guidance notes and lesson frameworks. |
| `Communications/` | Published writing (CELTA on LinkedIn / Medium / Substack) and message records. |
| `Legal_Documents/` | Legal paperwork (Cambridge / CELTA case, French). |
| `Email_Extension/` | The AI Hub Chrome extension + Gmail bulk-draft scripts. README inside. |
| `personal_doc_extracted/` · `personal_doc2_extracted/` | Extracted document sets. Unique content preserved (research-writing, skills, `MASTER_CONTACT_DIRECTORY.md`). |
| `_archive/` | `personal_doc.zip`, `personal_doc2.zip` — raw backups only. |

## Housekeeping notes

- **Consolidated, not deleted.** Removed only byte-identical duplicate folders
  (`personal_doc_extracted_1/2`, `personal_doc2_extracted_1/2`, and the verified-identical
  nested `My_Personal_Documents_extracted_1`). All **unique** content — your research-writing
  papers, reusable skills, and the master contact directory — is preserved. Full history
  stays in git regardless.
- **Organized the root.** Loose Chrome-extension and email-system files → `Email_Extension/`;
  CV and letters → `Profile_Documents/`; big `.zip` exports → `_archive/`.
- **Suggested next tidy (not done — your call):** the triple-nested re-extractions and
  `files*.zip` inside `Story_of_Sourov/06_ARCHIVES/` (~22 MB) could collapse to one copy.
  Convert the `*.py.docx` wrappers in `Email_Extension/` back to plain `.py` so the scripts run.

## Conventions going forward

- One home per thing. New writing → `posts/drafts/` or `Growth_Hub/drafts/`. New ideas → `Growth_Hub/IDEA_INBOX.md`.
- Plain `.md` for anything you'll edit or want diffed in git.
- No credentials in git — env vars or an untracked local file only.
- Decide the structure once, on a stable day, then stop redesigning it.
