# Repository Organization Guide

> **Your professional documents, organized for growth, accessibility, and wellbeing.**

---

## Directory Structure (Updated)

```
my_professional_documents/
│
├── blog_and_essays/              [👈 NEW: Your writing system]
│   ├── drafts/                   (Work in progress)
│   ├── published/                (Published essays)
│   ├── templates/                (ESSAY_TEMPLATE.md)
│   └── daily_prompts/            (18+ daily writing prompts)
│
├── automation/                   [👈 NEW: Your automation system]
│   ├── job_search/               (Indeed/LinkedIn search automation)
│   ├── wordpress/                (WP_PUBLISH_HELPER.py)
│   ├── email/                    (Email automation - planned)
│   ├── content_tracking/         (Google Sheet reference)
│   └── AUTOMATION_README.md
│
├── tools/                        [👈 Reorganized: Your toolkit]
│   ├── scripts/                  (Python, Bash scripts)
│   ├── templates/                (Reusable templates)
│   └── config/                   (Config files for tools)
│
├── resources/                    [👈 NEW: Learning & support]
│   ├── writing_guides/           (Writing tips, style guides)
│   ├── research_sources/         (Official docs, links)
│   └── mental_health/            (Self-care, accessibility)
│
├── Story_of_Sourov/              [Existing: Your biography]
│   ├── 01_MASTER_DOCUMENTS/
│   ├── 03_TOOLS_SCRIPTS/
│   ├── 05_INDEX_GUIDES/
│   └── 06_ARCHIVES/
│
├── Biography_and_Medical/        [Existing: Health & medical]
│   ├── BIOGRAPHY_SOUROV_DEB.md
│   ├── TREATMENT_PLAN_EXPLAINED_PLAIN_LANGUAGE.md
│   └── FRANCE_EU_DISABILITY_REGISTRATION_GUIDE.md
│
├── Legal_Documents/              [Existing: Legal records]
│   ├── Stage_1_appeal_report__Sourov_Deb.md
│   ├── DEB_Sourov_courrier-dadressage_2026-05-19_LETTER.md
│   └── DEB_Sourov_courrier-dadressage_2026-05-19_DIAGNOSTIC.md
│
├── cv_and_applications/          [Existing: Career materials]
│   ├── aeronautics/
│   ├── hospitality/
│   └── general/
│
├── therapy_and_wellbeing/        [Existing: Mental health resources]
│   ├── harmony-academic-gatekeeping-and-the-forensic-audit-2026-02-13.md
│   ├── harmony-reclaiming-your-voice-after-public-criticism-2026-03-09.md
│   └── [Essays on wellbeing & growth]
│
├── Communications/               [Existing: Contacts & outreach]
│   └── CONTACTS_AND_EMAILS_FOUR_CHANNELS.md
│
├── gmail_and_email_tools/        [Existing: Email resources]
│   ├── GMAIL_EMAIL_ARCHAEOLOGY_REPORT.md
│   └── README_DRAFT_GENERATOR.md
│
├── CELTA_Teaching_Materials/     [Existing: Teaching resources]
├── archives/                     [Existing: Old files & history]
├── browser_extension/            [Existing: Browser tools]
│
└── README.md                     [← Update this]
```

---

## What Goes Where

### `blog_and_essays/` - Your Writing Home

**Purpose**: Everything related to daily writing and WordPress publishing

**Subdirs**:
- `drafts/` - Work in progress (named: `YYYY-MM-DD-title.md`)
- `published/` - Published to WordPress (same naming)
- `templates/` - ESSAY_TEMPLATE.md (copy for each new essay)
- `daily_prompts/` - All 18+ prompts with research sources

**Add here when**: You write a new essay or want to update prompts

---

### `automation/` - Your Productivity Multiplier

**Purpose**: Scripts and systems that do work for you

**Subdirs**:
- `job_search/` - Automated job searches (Indeed, LinkedIn)
- `wordpress/` - WP_PUBLISH_HELPER.py and publishing docs
- `email/` - Email automation (planned)
- `content_tracking/` - Google Sheet integration (in progress)

**Add here when**: You create a new script or tool

---

### `tools/` - Reusable Toolkit

**Purpose**: Scripts, templates, configs you use repeatedly

**Subdirs**:
- `scripts/` - Python, Bash, JS scripts (alphabetical by purpose)
- `templates/` - Markdown, HTML, config templates
- `config/` - Configuration files (.gitignore, .env templates, etc.)

**Add here when**: You build something generic that multiple projects use

---

### `resources/` - Learning Materials

**Purpose**: Writing guides, research sources, mental health support

**Subdirs**:
- `writing_guides/` - Style guides, grammar tips, voice exercises
- `research_sources/` - Links to official docs, verified sources
- `mental_health/` - Accessibility tips, self-care routines, support resources

**Add here when**: You find a useful guide or want to document learning

---

### `Biography_and_Medical/` - Your Health & Identity

**Purpose**: Medical records, diagnosis, treatment plans, accessibility info

**Keep**: These are reference docs (don't edit unless major change)
**Private**: Yes (don't share publicly)

---

### `Legal_Documents/` - Your Legal Record

**Purpose**: Appeals, diagnoses, official correspondence, disability documentation

**Keep**: Organized by date and type
**Private**: Yes
**Use for**: Job appeals, disability claims, legal references

---

### `Story_of_Sourov/` - Your Narrative

**Purpose**: Life story, philosophy, experiences, observations

**Already organized**: Into master documents, archives, guides, tools

**Relationship**: Essays in `blog_and_essays/` often pull from here
**Public**: Yes (parts of it anyway)

---

### `cv_and_applications/` - Career Materials

**Purpose**: Resumes, cover letters, application templates by field

**Organization**: By industry (aeronautics, hospitality, general)
**Update**: Before each job search
**Use**: When applying on Indeed, LinkedIn

---

### `therapy_and_wellbeing/` - Mental Health Essays

**Purpose**: Essays and resources about mental health, growth, resilience

**Relationship**: These could become blog posts in `blog_and_essays/`
**Public**: Yes (these are empowering resources)

---

## Git Workflow

### Branch Strategy

```
main                              [Your published, stable content]
├── essay/2026-06-03-title1      [Draft → Publish → Merge]
├── essay/2026-06-04-title2      [Draft → Publish → Merge]
├── automation/job-search-v2      [New script → Test → Merge]
└── feature/wordpress-integration [Feature work → Merge]
```

**Rule**: One branch per essay or feature. Merge to `main` when done.

### Daily Workflow

```bash
# 1. Create branch for today's essay
git checkout -b essay/2026-06-03-my-essay-title

# 2. Write essay
# blog_and_essays/drafts/2026-06-03-my-essay-title.md

# 3. Validate & test
python3 automation/wordpress/WP_PUBLISH_HELPER.py blog_and_essays/drafts/2026-06-03-my-essay-title.md

# 4. Commit
git add blog_and_essays/
git commit -m "draft: essay title

- Prompt: #X
- Word count: 497
- Status: ready"

# 5. Push
git push -u origin essay/2026-06-03-my-essay-title

# 6. (Later) After publishing to WordPress:
# Move to published, update metadata, merge to main

git add blog_and_essays/
git commit -m "published: essay title

WordPress URL: https://www.sourovdeb.com/?p=123"

git checkout main
git pull origin main
git merge essay/2026-06-03-my-essay-title
git push origin main
```

---

## Naming Conventions

### Essays (Markdown)
```
YYYY-MM-DD-short-descriptive-title.md

Examples:
2026-06-03-what-i-wish-i-knew-about-bipolar.md
2026-06-04-why-remote-work-saves-lives.md
2026-06-05-open-source-tools-that-actually-work.md
```

### Branches (Git)
```
essay/YYYY-MM-DD-title          [For writing projects]
automation/feature-name          [For new scripts]
feature/feature-name             [For major features]
fix/bug-description              [For bug fixes]

Examples:
essay/2026-06-03-bipolar-essay
automation/linkedin-job-search
feature/email-automation
fix/wordpress-metadata-validation
```

### Commits (Git)
```
draft: title name
[Blank line]
- Prompt: #X (if applicable)
- Word count: XXX
- Status: [ready/needs-review/published]
- Notes: [optional]

---

published: title name
[Blank line]
WordPress URL: https://www.sourovdeb.com/?p=123
Categories: [category1, category2]
Updated Google Sheet: [date]
```

---

## File Organization Rules

### DO:
- ✓ Use clear, descriptive names
- ✓ Group related files together
- ✓ Include metadata (date, type, status)
- ✓ Use consistent folder structure
- ✓ Archive old versions (but keep them)

### DON'T:
- ✗ Duplicate files across folders (use symlinks if needed)
- ✗ Store credentials in files (use .env or environment variables)
- ✗ Mix different types of content (essays ≠ scripts)
- ✗ Leave "untitled" or "new file" names
- ✗ Delete old files (archive them instead)

---

## Integration Points

### Google Sheet (Content Tracking)
- **Link**: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/
- **Update**: After each essay is published
- **Columns**: Date, Prompt, Title, Word Count, Status, URL, Category, Tags, Notes

### WordPress (Publishing)
- **Site**: https://www.sourovdeb.com/
- **Admin**: https://www.sourovdeb.com/wp-admin/
- **Publishing**: Via manual copy-paste from WP_PUBLISH_HELPER.py output

### GitHub (This Repo)
- **URL**: https://github.com/sourovdeb/my_professional_documents
- **Main branch**: `main` (stable, published content)
- **Development**: Feature branches, merged when ready

---

## Maintenance Checklist

### Weekly
- [ ] Write 4-5 essays
- [ ] Publish to WordPress
- [ ] Update Google Sheet
- [ ] Commit to branches
- [ ] Merge to main (Friday)

### Monthly
- [ ] Review job search results
- [ ] Update CV if needed
- [ ] Archive old drafts
- [ ] Clean up abandoned branches

### Quarterly
- [ ] Review overall repo structure
- [ ] Update README files
- [ ] Reorganize if needed
- [ ] Update mental health resources

---

## Quick Navigation

**I want to...**

| Goal | Location | File |
|------|----------|------|
| Write today | `blog_and_essays/` | `daily_prompts/DAILY_WRITING_PROMPTS.md` |
| Publish essay | `automation/wordpress/` | `WP_PUBLISH_HELPER.py` |
| Search jobs | `automation/job_search/` | `INDEED_SEARCH_AUTOMATION.sh` |
| View my writing | `blog_and_essays/published/` | All `.md` files |
| Track progress | Google Sheet | [Link in AUTOMATION_README] |
| Update my story | `Story_of_Sourov/` | Any folder |
| Find contacts | `Communications/` | `CONTACTS_AND_EMAILS_FOUR_CHANNELS.md` |
| Mental health info | `therapy_and_wellbeing/` | Essays |
| Medical records | `Biography_and_Medical/` | Specific docs |
| Teaching materials | `CELTA_Teaching_Materials/` | By subject |

---

## Why This Structure Works

1. **Clear purpose**: Each folder has one job
2. **Scalable**: Easy to add new sections
3. **Findable**: Naming conventions = searchable
4. **Git-friendly**: Clean history, logical branches
5. **Sustainable**: Supports daily writing + automation
6. **Accessible**: Easy for you to navigate + understand
7. **Shareable**: Can share parts without exposing everything
8. **Health-first**: Supports consistency without burnout

---

## Start Here

1. Read `automation/AUTOMATION_README.md`
2. Read `blog_and_essays/daily_prompts/DAILY_WRITING_PROMPTS.md`
3. Pick a prompt, write 500 words
4. Test `automation/wordpress/WP_PUBLISH_HELPER.py`
5. Publish to WordPress
6. Update Google Sheet
7. Commit + merge to main

---

**Your repository is your second brain. Keep it organized, keep it growing.**

Last updated: 2026-06-03
