# Sourov Deb — Personal Repository

This repository holds everything: writing, career documents, automation tools, health notes, legal documents, and the record of a life examined.

**Owner:** Sourov Deb | **Site:** [sourovdeb.com](https://www.sourovdeb.com) | **Location:** La Réunion, France

---

## Who This Repository Is For

Me. And for anyone I choose to show it to.

It documents:
- My story (Bangladesh → Australia → France, 40 years of becoming myself)
- My writing system (daily 500-word essays, six topic pillars)
- My job search (automated, tracked)
- My tools (scripts that do the repetitive work so I can write)
- My health (plain-language notes on living with Bipolar I, ADHD, and complex trauma)

---

## Structure

```
my_professional_documents/
│
├── 02_health/              ← Conditions, treatment plan, wellbeing notes
├── 03_writing/             ← The writing system ← START HERE for writing
├── 05_automation/          ← Scripts: WordPress, job search, outreach
│
├── Biography_and_Medical/  ← Biography, medical synthesis (2026), therapy transcripts
├── CELTA_Teaching_Materials/ ← Teaching certification resources
├── Communications/         ← LinkedIn, Substack, Medium content
├── Legal_Documents/        ← CELTA appeal, medical letters, MDPH
├── Story_of_Sourov/        ← Master documents, analysis, reusable skills
├── browser_extension/      ← AI Hub Chrome extension (email automation)
├── cv_and_applications/    ← CVs by sector: aeronautics, hospitality, general
├── gmail_and_email_tools/  ← Gmail automation scripts
├── therapy_and_wellbeing/  ← Harmony therapy session transcripts
├── tools_and_scripts/      ← Legacy skills and scripts
│
├── .env.example            ← Credential template (copy to .env, never commit)
└── .gitignore
```

---

## Quick Start — Writing

```bash
# 1. Pick a topic from the backlog
open 03_writing/_ideas/ideas_backlog.md

# 2. Copy the template
cp 03_writing/_templates/essay_500words.md 03_writing/drafts/$(date +%Y-%m-%d)-your-title.md

# 3. Write (aim for 500 words, active voice, one idea)

# 4. Push to WordPress as draft
python 05_automation/wordpress/publish_to_wp.py 03_writing/drafts/your-essay.md

# 5. Commit on its own branch
git checkout -b essay/$(date +%Y-%m-%d)-your-title
git add 03_writing/drafts/your-essay.md
git commit -m "essay: your title"
```

See `03_writing/README.md` for the full system.

---

## Quick Start — Job Search

```bash
# Install once
pip install python-jobspy

# Run all search profiles (English teacher, content writer, hospitality...)
python 05_automation/job_search/search_jobs.py --all-profiles

# Results in: 05_automation/job_search/results/
# Track applications in: 05_automation/job_search/job_tracker.md
```

---

## Quick Start — Find Writing Partners

```bash
python 05_automation/outreach/find_writers.py
# Results in: 05_automation/outreach/results/
```

---

## The Six Writing Pillars

| Pillar | What it covers |
|--------|---------------|
| The Immigrant Mind | Language, belonging, four countries |
| Rewiring the Brain | Bipolar, ADHD, trauma recovery |
| The Child Who Survived | Generational trauma, parenting |
| Work & Worth | Hospitality, disability, disclosure |
| Language & Teaching | CELTA, adult learning, code-switching |
| The Examined Life | Jung, philosophy, addiction, recovery |

---

## Branch Convention

| Branch type | Pattern | When to use |
|-------------|---------|-------------|
| Essay | `essay/YYYY-MM-DD-slug` | Each piece of writing |
| Feature | `feature/description` | New tools or automation |
| Health update | `health/YYYY-MM-DD` | Medical document updates |
| Job application | `job/company-role` | Tailored CV/cover letter |

All content starts on its own branch. Merge to `main` when done.

---

## Platforms Where You Publish

| Platform | Role | Link |
|----------|------|------|
| WordPress (sourovdeb.com) | Home base | Your site |
| Medium | Essays with wide reach | Pays via Partner Program |
| Substack | Personal letters, email list | Most direct reader relationship |
| LinkedIn | Professional / teaching angle | Job visibility |

---

## Health Notes

See `02_health/condition_notes.md` for plain-language notes on living with:
- Bipolar I (Dr. Padovani, monthly follow-up)
- ADHD
- Complex PTSD
- Dissociation

Key principle: **routine protects the brain**. Writing every day is both creative output and mental health practice.

---

## Credentials

Stored in `.env` (gitignored). Template in `.env.example`.

Never commit the `.env` file. Never paste credentials into markdown files or commit messages.
