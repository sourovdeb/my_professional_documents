# Repository Architecture & Content System

## Vision
Build exposure through consistent, quality writing + automation of busywork + health-aware productivity.

**Core Principles:**
- Active voice, human tone (not passive, not monotone)
- Quality over quantity
- Research from official/legal sources only
- Token-efficient, reusable tools
- Health-first scheduling (bipolar/depression-aware)
- Everything personalized to your wellbeing

---

## Repository Structure (New)

```
/my_professional_documents
├── 📝 BLOG/
│   ├── DRAFTS/              # Working essays (branch-based)
│   │   ├── 2026-06/
│   │   │   └── essay-slug.md
│   │   └── publishing_tracker.csv
│   ├── PUBLISHED/           # Final, published essays
│   ├── TEMPLATES/           # Essay + Blog templates
│   └── WORDPRESS/           # WP sync (branched, then copy-paste)
│
├── 💼 CAREER/
│   ├── JOB_OPPORTUNITIES/   # Automated job scraping results
│   ├── CONTACTS/            # Discovered writers/partners
│   ├── cv_and_applications/ # CVs, tailored letters
│   └── LINKEDIN/            # LinkedIn profile data
│
├── 🛠️ TOOLS/
│   ├── automation/          # Python scripts (jobs, email, social)
│   ├── google_sheets_sync/  # Google Sheets API integration
│   ├── wordpress_deploy/    # WordPress API & FTP
│   ├── browser_extension/   # Chrome extension (AI assistant)
│   └── scripts/             # Utility scripts
│
├── 📚 KNOWLEDGE/
│   ├── Biography_and_Medical/      # Your story, health docs
│   ├── therapy_and_wellbeing/      # Mental health resources
│   ├── Legal_Documents/             # Regulatory, appeals
│   ├── CELTA_Teaching_Materials/   # CELTA content
│   ├── Communications/              # Past emails, contacts
│   └── Story_of_Sourov/            # Personal narrative
│
├── 📊 TRACKING/
│   ├── content_calendar.csv         # Editorial calendar
│   ├── publishing_tracker.csv       # Blog → WP status
│   ├── job_applications.csv         # Application log
│   ├── contacts_discovered.csv      # Potential partners
│   └── health_log.csv               # Mood/energy tracking
│
├── 🔐 CONFIG/
│   ├── .env.example                 # API keys (DO NOT COMMIT)
│   ├── wordpress_config.json        # WP host, user, key
│   ├── google_sheets_config.json    # Google API config
│   └── automation_settings.json     # Script preferences
│
├── README.md                        # Start here
├── ARCHITECTURE.md                  # This file
├── SUSTAINABILITY.md                # Health-first workflows
└── QUICK_START.md                  # First steps
```

---

## Content Creation Workflow

### Phase 1: Idea → Draft (Weekly)
```
1. Open Google Sheet "Essay Ideas"
   - Topic, angle, sources, health status
2. Research using official sources only
   - Collect links, quotes, data
3. Write 500-word essay (active voice, human tone)
   - Branch: essay/topic-name-YYYY-MM-DD
   - File: BLOG/DRAFTS/YYYY-MM/essay-slug.md
4. Self-edit using AI assistant (Chrome extension)
5. Commit with message: "Draft: [Topic] - ready for review"
```

### Phase 2: Review → Polish (Bi-weekly)
```
1. Add to publishing_tracker.csv
   - Status: "Draft Review"
2. Proofread, fact-check sources
3. Format for both blog and WordPress
4. Update essay front matter (metadata)
5. Commit: "Polish: [Topic] - ready to publish"
```

### Phase 3: Publish → Syndicate (Weekly)
```
1. Copy to BLOG/PUBLISHED/
2. Create WordPress post (branch-based)
   - Branch: wordpress/post-slug-YYYY-MM-DD
   - File: BLOG/WORDPRESS/post-slug.md (with WP formatting)
3. Update publishing_tracker.csv
   - Status: "Published"
   - URL: [blog], [wordpress], [medium], [substack]
4. Share on LinkedIn, Medium, Substack
5. Log in contacts_discovered.csv if new partnerships found
```

---

## Automation Scripts Overview

### 1. Job Hunter (`tools/automation/job_hunter.py`)
**Purpose:** Auto-scrape Indeed, LinkedIn, email lists every Monday

```
Input:  Job titles, locations, keywords
Output: job_applications.csv with:
  - Job title, company, location, link
  - Posted date, salary (if available)
  - Application status
  - Notes for follow-up

Schedule: Weekly Monday 8 AM
Runs:     Parallel searches across 5 job boards
```

### 2. Email Drafter (`tools/automation/email_drafter.py`)
**Purpose:** Batch-create personalized emails from CSV

```
Input:  CSV with [company, contact, sector, subject]
Output: Gmail drafts ready to send

Uses:   Google Sheets sync + Gmail API
Tone:   Active voice, professional but human
```

### 3. Writer Discovery (`tools/automation/writer_discovery.py`)
**Purpose:** Find writers, editors, collaborators on Medium, Substack, Twitter

```
Input:  Topics you write about
Output: contacts_discovered.csv with:
  - Name, email, platform, current work
  - Collaboration potential
  - Follow-up date

Schedule: Weekly Thursday
```

### 4. Google Sheets Sync (`tools/google_sheets_sync/`)
**Purpose:** Keep local CSVs synced with Google Sheets

```
Input:  Google Sheet URLs (from config)
Output: Local CSV files auto-updated

Files synced:
  - Essay ideas sheet
  - Job opportunities
  - Contacts discovered
  - Publishing calendar
  - Health tracking
```

### 5. WordPress Deploy (`tools/wordpress_deploy/`)
**Purpose:** Push drafted posts to WordPress automatically

```
Input:  BLOG/WORDPRESS/*.md
Output: WordPress drafts (via deploy.php gateway)

Uses:   FTP + WordPress REST API
Branch: Create separate branch per post
```

---

## Health-Aware Sustainability System

### Energy Levels & Task Mapping

**High Energy Days:**
- Write essays (deep focus)
- Research new topics
- Reach out to contacts
- Strategic planning

**Medium Energy Days:**
- Edit & polish existing drafts
- Update CSVs and tracking
- Reply to messages
- Learn new automation tools

**Low Energy Days:**
- Run automation scripts (no input needed)
- Review auto-generated opportunities
- Passive learning (read others' essays)
- Admin tasks (small, 15-min chunks)

### Weekly Template

```
Monday:     Automation runs (job hunter) + light admin
Tuesday:    Research + first draft
Wednesday:  Continue draft (if energy allows)
Thursday:   Automation runs (writer discovery) + light edit
Friday:     Polish + prepare WordPress post
Weekend:    Rest (only engage if inspired)

Flexible:   All dates adjust based on mood log
```

### Health Tracking

Log daily in `TRACKING/health_log.csv`:
```
Date,Energy(1-10),Mood(1-10),Tasks_Completed,Notes
2026-06-02,6,7,"Email,Draft","Started new essay idea"
```

Use this to:
- Identify energy patterns
- Adjust weekly schedule
- Communicate needs to collaborators
- Build sustainable pace

---

## Publishing Destinations

Each essay publishes to multiple platforms (same content, different formats):

1. **Your Blog** (sourovdeb.com)
   - Custom domain, SEO benefit
   - Full control, newsletter integration
   - Branch: `wordpress/post-slug-YYYY-MM-DD`

2. **Medium**
   - Built-in audience, discovery
   - Republish with "Originally published" link
   - Link back to your blog

3. **Substack**
   - Newsletter audience
   - Newsletter formatting (shorter, punchier)
   - Automation: auto-send to subscribers

4. **LinkedIn**
   - Professional network visibility
   - Job opportunities from audience
   - Repurpose as LinkedIn article

5. **Dev.to** (technical essays)
   - Tech community, SEO
   - Code-friendly formatting

---

## Google Sheets Integration

All tracking lives in your Google Sheet:
`https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/`

**Tabs:**
1. **Essay Ideas** — Topic, angle, status, sources
2. **Publishing Calendar** — Due dates, published dates
3. **Job Opportunities** — Auto-populated weekly
4. **Contacts Discovered** — Writers, collaborators, follow-ups
5. **Health Tracking** — Energy, mood, tasks
6. **Application Log** — Job applications + status

Automation syncs bidirectionally:
- Sheets → CSVs → Automation scripts
- Scripts → CSVs → Sheets (updates pulled)

---

## Security & Privacy

- **No hardcoded credentials** — Use `.env` files + environment variables
- **FTP/WordPress keys** — Stored locally only, never committed
- **Google API** — Uses OAuth2 (user grants permission)
- **Health data** — Local-only, never synced externally
- **GitHub** — Public repo but sensitive data in `.gitignore`

---

## First Steps

1. Create `BLOG/DRAFTS/` directories
2. Copy essay template to `BLOG/TEMPLATES/essay.md`
3. Set up Google Sheets sync (see `QUICK_START.md`)
4. Run first automation script (job hunter)
5. Write first essay, commit to branch
6. Publish to blog, update tracking sheet

**Start with one essay.** Build from there.

---

## Success Metrics

Not vanity metrics. Real impact:

- **Consistency:** 1 essay per week (adjustable)
- **Quality:** 0 fact errors (verify all claims)
- **Audience:** Identify engaged readers, build relationships
- **Opportunities:** Job leads, collaborations from audience
- **Health:** Sustainable energy levels (no burnout)

---

Last updated: 2026-06-02
