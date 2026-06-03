# Blogging & Content Creation System

**For: Sourov Deb | Health-Aware Writing & Automation**

---

## Philosophy

- **Quality over quantity**: Better 500 deep words than 2000 scattered ones
- **Consistency over perfection**: Write daily, refine weekly, publish monthly
- **Health first**: Adapt to energy levels; use templates when depleted
- **Active voice**: Human, direct, actionable writing
- **Official sources only**: Research from verified, legal sources
- **Token efficiency**: Reuse proven scripts and tools
- **Automation**: Focus energy on writing, not repetitive tasks

---

## Directory Structure

```
📁 my_professional_documents/
├── 📁 blog_drafts/              # Your writing workspace
│   ├── 📁 2026_06_essays/      # June essays (monthly folder)
│   ├── 📁 2026_07_essays/      # July essays, etc.
│   ├── ESSAY_TEMPLATE.md       # Start with this
│   └── README.md               # Writing guide
├── 📁 wordpress_ready/          # Final, formatted for WP
│   ├── published/              # Already on sourovdeb.com
│   ├── staging/                # Ready to publish (review before pushing)
│   └── README.md
├── 📁 job_automation/           # Indeed, LinkedIn, email automation
│   ├── indeed_scraper.py       # Find jobs matching your profile
│   ├── email_outreach.py       # Automated email generation
│   ├── linkedin_connector.py   # Potential collaborators
│   ├── contacts_db.json        # Your contacts
│   └── README.md
├── 📁 content_research/         # Research & ideas collection
│   ├── google_sheets_sync.py   # Sync with your Sheets
│   ├── sources_database.md     # Official sources library
│   ├── ideas_inbox.md          # Raw essay ideas
│   └── research_log.md         # What you've researched
├── 📁 health_and_productivity/  # Sustainable writing
│   ├── energy_tracker.md       # Track energy, not just words
│   ├── mood_based_tasks.md     # What to do when you're low
│   ├── templates/              # Pre-written snippets
│   └── weekly_review.md        # Sunday check-in
└── 📁 automation_scripts/       # All your .py scripts
    ├── wordpress_uploader.py    # Push to WP via deploy.php
    ├── draft_manager.py         # Organize & version control
    ├── email_scheduler.py       # Schedule bulk emails
    └── backup_and_sync.py       # GitHub + local backup
```

---

## Branching Strategy

**Main principle**: One essay = one branch. Keeps work organized, easily reviewable, mergeable.

### Branch Naming Pattern

```
essay/YYYY-MM-DD_topic-slug
job/YYYY-MM-DD_company-name
automation/feature-name
research/topic-name
```

### Example Workflow

```bash
# Create branch for today's essay
git checkout -b essay/2026-06-03_bipolar-work-strategies

# Write your essay in blog_drafts/2026_06_essays/
# ... (write 500 words)

# Commit
git add blog_drafts/2026_06_essays/
git commit -m "Essay: Bipolar work strategies - first draft"

# Push to branch (creates PR)
git push -u origin essay/2026-06-03_bipolar-work-strategies

# Later: Move to wordpress_ready/staging/ when ready
# Then merge to main once published on WordPress
```

---

## Daily Writing Workflow

### Morning Check-in (5 min)
1. Open `health_and_productivity/energy_tracker.md`
2. Rate your energy: 1-10
3. Check `mood_based_tasks.md` for today's task type
4. Create today's branch: `git checkout -b essay/YYYY-MM-DD_topic`

### Writing Session (45 min focus)
1. Open `ESSAY_TEMPLATE.md` as reference
2. Write in `blog_drafts/YYYY_MM_essays/your_essay.md`
3. Use `content_research/ideas_inbox.md` for inspiration
4. Link official sources in `content_research/sources_database.md`

### Editing (15 min)
1. Read aloud (catch tone issues)
2. Check: active voice, 500±50 words, official sources cited
3. Format for WordPress: headers, lists, links

### Commit
```bash
git add blog_drafts/
git commit -m "Essay: [Title] - [status: draft/ready]"
git push -u origin essay/2026-06-03_topic-slug
```

---

## Energy-Based Task Mapping

**High energy (8-10):**
- Write new essay
- Research for 2-3 essays
- Create automation script
- Outreach to potential collaborators

**Medium energy (5-7):**
- Edit existing draft
- Organize research
- Update job search spreadsheet
- Respond to emails

**Low energy (1-4):**
- Read sources without writing
- Reorganize existing files
- Use templates for quick post
- Update tracker, rest, medication check

**Zero energy (depressive episode):**
- No writing required
- Use pre-written templates
- Just push existing drafts to WordPress
- Commit to repo anyway (document the rest)

---

## Content Ideas Sources

Brainstorm from these reliable sources:

1. **Your lived experience** (bipolar, disability, career changes)
2. **Medical/mental health**: Mayo Clinic, SAMHSA, WebMD
3. **Career**: LinkedIn Research, INDEED salary guides, HackerRank
4. **Teaching**: Cambridge CELTA, EFL guides, methodology papers
5. **Tech**: Official docs (Microsoft Learn, Python docs, GitHub)
6. **Productivity**: GTD, Pomodoro, actual research (not Medium)
7. **France/EU**: Official government sources (French MDPH, Légifrance)

---

## WordPress Publishing Checklist

Before pushing to `wordpress_ready/staging/`:

- [ ] 500 words ±50
- [ ] Active voice throughout
- [ ] All sources cited with links
- [ ] No promotional fluff
- [ ] Markdown properly formatted
- [ ] Headers (H2, H3) break up text
- [ ] 1-2 key takeaways highlighted
- [ ] Category & tags filled in metadata

Before publishing to WordPress:

- [ ] Read on WordPress preview
- [ ] Check mobile formatting
- [ ] Verify all links work
- [ ] Test category/tags appear
- [ ] Update Google Sheets tracking spreadsheet

---

## Tools You'll Use

| Task | Tool | Cost |
|------|------|------|
| Writing | VS Code or GitHub Markdown | Free |
| Research | Google Scholar, official docs | Free |
| Job scraping | Python (Indeed API alternative) | Free |
| Email automation | Gmail API + Python | Free |
| WordPress upload | deploy.php gateway | Already set up |
| Job tracking | Google Sheets | Free |
| Collaboration | GitHub + Discord | Free |

---

## Recovery & Consistency

When you miss a day (and you will):
1. Don't guilt spiral—write the next day
2. If missed 3 days: write a shorter post (200 words)
3. If missed a week: write a reflection on the absence
4. If depressive episode: use templates, push old drafts
5. Weekly review every Sunday: celebrate what you did, plan next week

---

## Next Steps

1. Create monthly essay folders: `mkdir -p blog_drafts/2026_{06..12}_essays`
2. Customize `ESSAY_TEMPLATE.md` with your style
3. Set up `content_research/sources_database.md`
4. Run `job_automation/indeed_scraper.py` for first time
5. Schedule weekly review every Sunday at 6 PM

---

**Your writing matters. Your health comes first. Automation handles the repetition. You focus on the voice.**
