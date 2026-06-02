# My Professional Documents: Complete System

**Your personal hub for writing, exposure, jobs, and health-aware consistency.**

## Vision

Build a sustainable system where:
- You write quality essays when you have energy
- Automation handles busywork
- Health always comes first
- Opportunities flow in through consistent output

---

## The System in 3 Parts

### 1. 📝 **Writing & Publishing** (BLOG/)
- Essay templates & workflow
- Local drafts → Personal blog → Medium/Substack/LinkedIn
- Tracked in Google Sheets, published via git branches
- Health-aware scheduling (write when energized, publish when stable)

### 2. 🛠️ **Automation Tools** (tools/)
- Job hunting (auto-scrape Indeed, LinkedIn, WTTJ)
- Email drafting (batch personalized outreach)
- Google Sheets sync (centralized tracking)
- Writer discovery (find collaborators)
- All zero-input: schedule and forget

### 3. 📚 **Knowledge Base** (Biography_and_Medical/, Communications/, etc.)
- Your complete story
- Medical/therapy notes
- Teaching materials
- Contact database
- Everything organized, searchable, version-controlled

---

## Getting Started (30 minutes)

### Step 1: Understand the Framework
Read these in order:
1. `ARCHITECTURE.md` — System overview (5 min)
2. `SUSTAINABILITY.md` — Health-first productivity (10 min)
3. `QUICK_START.md` — First essay workflow (5 min)

### Step 2: Set Up Automation
```bash
# Install Python dependencies
pip install -r tools/requirements.txt

# Initialize Google Sheets sync
python3 tools/google_sheets_sync/sheets_sync.py --init-config

# Set up Google API credentials
# https://console.cloud.google.com/apis/credentials
# Save to: ~/.config/google_sheets_config.json

# Test job hunter (will use mock data if no network access)
python3 tools/automation/job_hunter.py
```

### Step 3: Write Your First Essay
```bash
# Follow QUICK_START.md
# 1. Create BLOG/DRAFTS/2026-06/my-essay.md
# 2. Write (60 min)
# 3. Commit & track
# 4. Publish to blog
```

### Step 4: Schedule Automation
```bash
# Edit crontab
crontab -e

# Add:
0 8 * * 1 cd ~/my_professional_documents && python3 tools/automation/job_hunter.py
0 9 * * 1 cd ~/my_professional_documents && python3 tools/google_sheets_sync/sheets_sync.py --sync-all
```

Done! Now you have:
- ✅ Automated job hunting (weekly)
- ✅ Google Sheets sync (centralized tracking)
- ✅ Essay workflow ready
- ✅ Health-aware scheduling

---

## Weekly Workflow

### Monday (8 AM - Automation runs)
- Job opportunities auto-populated
- Google Sheets auto-synced
- Your action: Review results during breakfast

### Tuesday (Morning - High energy if available)
- Research new essay topic
- Write first draft
- Commit to git branch

### Wednesday
- Edit & polish
- Self-check sources
- Continue draft if energy allows

### Thursday (8 AM - Automation runs again)
- Writer discovery results in
- Your action: Light edit, reply to messages

### Friday
- Final polish
- Create WordPress branch
- Schedule publication

### Weekend
- Rest (genuinely)
- Optional: Light reading, inspiration
- Track energy/mood in health log

---

## Directory Guide

```
my_professional_documents/
│
├── 📋 SYSTEM DOCS
│   ├── README.md                    ← You are here
│   ├── ARCHITECTURE.md              ← System blueprint
│   ├── SUSTAINABILITY.md            ← Health-first framework
│   └── QUICK_START.md               ← First essay guide
│
├── 📝 BLOG/ (Your Publishing)
│   ├── DRAFTS/2026-06/              ← Working essays
│   ├── PUBLISHED/                   ← Finished essays
│   ├── WORDPRESS/                   ← WP-formatted posts
│   └── TEMPLATES/essay.md           ← Template to copy
│
├── 💼 CAREER/ (Job Hunting)
│   ├── cv_and_applications/         ← CVs, cover letters
│   ├── job_opportunities.csv        ← Auto-populated weekly
│   └── contacts_discovered.csv      ← Potential collaborators
│
├── 🛠️ TOOLS/ (Automation)
│   ├── automation/
│   │   ├── job_hunter.py            ← Scrape job boards
│   │   ├── email_drafter.py         ← Batch emails
│   │   └── writer_discovery.py      ← Find writers
│   ├── google_sheets_sync/          ← Centralized tracking
│   ├── wordpress_deploy/            ← Publish to blog
│   └── requirements.txt             ← Python deps
│
├── 📊 TRACKING/ (Centralized Data)
│   ├── essay_ideas.csv              ← Ideas to write
│   ├── job_opportunities.csv        ← Jobs to apply to
│   ├── publishing_tracker.csv       ← Publication status
│   ├── contacts_discovered.csv      ← People to reach out to
│   └── health_log.csv               ← Energy/mood tracking
│
├── 📚 KNOWLEDGE BASE (Your Story)
│   ├── Biography_and_Medical/       ← Your narrative
│   ├── therapy_and_wellbeing/       ← Mental health resources
│   ├── Communications/              ← Past emails, contacts
│   ├── Legal_Documents/             ← Regulatory, appeals
│   ├── CELTA_Teaching_Materials/    ← Teaching content
│   └── Story_of_Sourov/             ← Personal archive
│
└── 🔧 CONFIG
    ├── .env.example                 ← Environment template
    └── .gitignore                   ← Excludes secrets
```

---

## Quick Command Reference

### Writing
```bash
# Create new essay
mkdir -p BLOG/DRAFTS/2026-06
cp BLOG/TEMPLATES/essay.md BLOG/DRAFTS/2026-06/my-essay.md

# Track progress
echo "Title,Status,Date,URL" >> TRACKING/publishing_tracker.csv

# Publish
git checkout -b wordpress/my-essay-2026-06
cp BLOG/PUBLISHED/my-essay.md BLOG/WORDPRESS/
git add BLOG/WORDPRESS/ && git commit -m "WordPress: My Essay"
```

### Automation
```bash
# Run all automation
bash tools/scripts/run_all_automation.sh

# Check results
cat TRACKING/job_opportunities.csv | head -20
```

### Tracking
```bash
# View health log
tail -20 TRACKING/health_log.csv

# Sync with Google Sheets
python3 tools/google_sheets_sync/sheets_sync.py --sync-all
```

### Git Workflow
```bash
# Create branch for work
git checkout -b essay/topic-name-date

# Commit regularly
git add BLOG/DRAFTS/
git commit -m "Draft: Topic - [status]"

# Push to develop branch
git push origin claude/nifty-clarke-uSGrd
```

---

## Key Principles

### 1. Health First
- Meds + therapy are non-negotiable
- Sustainable pace > burnout
- Rest is productive
- Track energy to predict cycles

### 2. Quality Over Quantity
- 1 verified essay per week > 7 unverified
- All claims have sources (official/legal)
- Active voice, human tone
- Done > perfect

### 3. Automation for Humans
- Eliminate repetitive work
- Run scripts on schedule
- Review results at your pace
- Technology serves health, not vice versa

### 4. Everything Tracked
- Essays in git (version history)
- Jobs in Google Sheets (easy filtering)
- Health in CSV (pattern recognition)
- Contacts in database (relationship management)

### 5. Sustainability Over Hustle
- Create when energized
- Publish when stable
- Rest guilt-free
- Success is consistent, not constant

---

## Mental Health Support

If you're in a difficult place:
- **Immediate crisis:** Call 988 (US) or your local crisis line
- **Regular support:** Therapist + medication (non-negotiable)
- **Community:** Find others with bipolar/depression (online or local)
- **Permission:** You don't need to be 100% to create. Imperfect is published.

This system is built with your wellbeing in mind. Use it as a tool to support yourself.

---

## Success Looks Like

**After 1 month:**
- 4-5 essays written & published
- 40+ job opportunities reviewed
- 5+ potential collaborators identified
- Health patterns tracked
- Zero burnout

**After 3 months:**
- 12+ essays building reputation
- Consistent weekly publication
- Job leads from audience
- 1-2 collaboration inquiries
- Sustainable rhythm established

**After 6 months:**
- 25+ published essays
- 500+ regular readers
- 3-5 serious opportunities
- Established writer identity
- Sustainable income opportunities possible

---

## Frequently Asked Questions

**Q: Do I need to code to use this?**
A: No. Scripts are ready to use. No coding required. Just run and review results.

**Q: What if I miss a week?**
A: You have banked content. Publish something. No guilt. Return next week.

**Q: Can I use this without sharing my health info?**
A: Yes. The health tracking is private (local only, never synced externally).

**Q: How much time does this take?**
A: ~2 hours for essay + 1 hour for admin = 3 hours per week on baseline.
Automation handles the busywork.

**Q: What if I have a depressive episode?**
A: Automation keeps running. You publish pre-written content. You rest.

**Q: Can I customize this?**
A: Absolutely. It's your system. Modify as needed. Document changes.

---

## Getting Help

- **System questions?** See `ARCHITECTURE.md`
- **Health/sustainability?** See `SUSTAINABILITY.md`
- **First essay?** See `QUICK_START.md`
- **Automation issues?** See `tools/README.md`
- **General support?** Check repo issues or reach out

---

## Next Steps

1. **Read** `ARCHITECTURE.md` (understand the vision)
2. **Read** `SUSTAINABILITY.md` (understand yourself)
3. **Follow** `QUICK_START.md` (write first essay)
4. **Set up** automation (let the robots work)
5. **Publish** consistently (build your reputation)
6. **Thrive** (capture opportunities)

---

**You're building something real. At your pace. For your life.**

**Start with one essay. Build from there.**

---

Last updated: 2026-06-02  
Author: Sourov Deb  
License: Personal use + collaborators
