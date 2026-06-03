# Sourov Deb — Personal Documents & Writing Repository

This repository is the operational hub for Sourov Deb's writing, job search, automation tools, and professional life. It is private, organised, and health-adapted — designed for someone managing bipolar I disorder, ADHD, and complex PTSD while building a public voice and teaching practice.

**Website:** [sourovdeb.com](https://www.sourovdeb.com)
**Email:** sourovdeb.is@gmail.com
**Location:** Saint-Pierre, La Réunion, France

---

## Repository Structure

```
my_professional_documents/
│
├── blog_drafts/              ← 7 original essays, ~500 words each
│   ├── 2026-06-03-ship-with-broken-compass.md        (WP Draft #155)
│   ├── 2026-06-03-bipolar-productivity-truth.md      (WP Draft #156)
│   ├── 2026-06-03-forensic-auditor.md                (WP Draft #157)
│   ├── 2026-06-03-five-languages-one-voice.md        (WP Draft #158)
│   ├── 2026-06-03-generational-trauma-stops-here.md  (WP Draft #159)
│   ├── 2026-06-03-tools-for-neurodivergent-writers.md (WP Draft #160)
│   ├── 2026-06-03-when-cambridge-failed-me.md        (Pitch: The Guardian)
│   └── WORDPRESS_CSV_QUEUE.md                        ← Copy-paste for Google Sheets
│
├── automation/               ← Free open source scripts, no paid APIs
│   ├── job_search_automation.py      ← Indeed RSS → Gmail daily digest
│   ├── wordpress_draft_publisher.py  ← .md files → WordPress drafts via REST API
│   ├── partner_finder.py             ← Find writers on Medium + Substack
│   └── create_wp_drafts.php          ← Batch WordPress draft creator
│
├── cv_and_applications/
│   ├── aeronautics/          ← Aviation English specialist applications
│   ├── hospitality/          ← Luxury hospitality management applications
│   ├── general/              ← General educator / content roles
│   └── JOB_SEARCH_STRATEGY.md  ← Platform list, automation, action plan
│
├── Communications/
│   ├── CONTACTS_AND_EMAILS_FOUR_CHANNELS.md
│   └── PAID_PUBLICATIONS_PITCH_LIST.md  ← Headspace, Guardian, ADDitude, etc.
│
├── therapy_and_wellbeing/
│   ├── DAILY_STABILITY_GUIDE.md  ← Bipolar/ADHD/PTSD daily routine
│   └── harmony-*.md              ← AI therapy session notes (private)
│
├── Story_of_Sourov/           ← Source material for essays (DO NOT publish directly)
│   ├── 01_MASTER_DOCUMENTS/
│   ├── 02_ANALYSIS_DOCUMENTS/
│   ├── 03_TOOLS_SCRIPTS/
│   ├── 04_REUSABLE_SKILLS/
│   ├── 05_INDEX_GUIDES/
│   └── 06_ARCHIVES/
│
├── Biography_and_Medical/     ← Private medical records (DO NOT publish)
├── Legal_Documents/           ← CELTA appeal, Ofqual complaint docs
├── CELTA_Teaching_Materials/  ← Teaching resources
├── browser_extension/         ← AI Hub Chrome Extension source
├── archives/                  ← Historical documents
│
└── CONTENT_INDEX.md           ← Master map — everything in one place
```

---

## WordPress Drafts Live on sourovdeb.com

All 7 essays are available as drafts in the WordPress admin. Review and publish on your schedule.

| Post ID | Title | Suggested Date |
|---------|-------|----------------|
| 155 | The Ship With a Broken Compass | 2026-06-10 |
| 156 | What Bipolar Taught Me That Productivity Gurus Got Wrong | 2026-06-17 |
| 157 | The Forensic Auditor: How Documentation Became My Therapy | 2026-06-24 |
| 158 | Five Languages, One Voice | 2026-07-01 |
| 159 | Generational Trauma Stops Here | 2026-07-08 |
| 160 | The Neurodivergent Writer's Toolkit (2026) | 2026-07-15 |

**WordPress admin:** https://sourovdeb.com/wp-admin

---

## Automation — Quick Start

```bash
# Install dependencies
pip install requests feedparser beautifulsoup4 markdown python-frontmatter

# Job search digest (set GMAIL_APP_PASSWORD env var first)
python automation/job_search_automation.py

# Push markdown drafts to WordPress (set WP_APP_PASSWORD env var first)
python automation/wordpress_draft_publisher.py --dry-run

# Find writing partners on Medium + Substack
python automation/partner_finder.py
```

---

## Writing Principles

1. **Active voice.** Always. Not "mistakes were made" — "I made mistakes."
2. **500 words.** Quality over length. Say it once, say it well.
3. **Human, not monotone.** Vary the rhythm. Let the pace breathe.
4. **Official sources only.** Research before you claim. Link when you can.
5. **Protect the rhythm.** One post per week beats a burst and a crash.

---

## Branching Convention

- `main` — stable, reviewed content
- `claude/determined-brown-TZOiX` — active development
- `blog/YYYY-MM-DD-post-name` — individual blog posts (one branch per post)

---

## Important Reminders

- **Biography_and_Medical/** is private source material — draw from it, do not publish it
- **Legal_Documents/** contains active complaint files — handle with care
- **Credentials** are stored as environment variables, never in this repo
- **Every new blog post** gets its own branch before publishing

---

*This repository was organised on 2026-06-03. Previous work is archived in `archives/`.*
