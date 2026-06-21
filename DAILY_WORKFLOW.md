# 📅 Daily Writing + Job Search + Automation Workflow

**Goal:** Write daily (500 words) + Auto-scrape jobs + Find collaborators + Publish to WordPress

**Time investment:** 1-2 hours/day with automation

---

## MORNING ROUTINE (30 mins)

### 1. Check Overnight Automation Results (5 mins)
```bash
# See what ran while you slept
cd my_professional_documents

# View new jobs found
cat job_leads/indeed_leads.json | head -20

# View new contacts discovered
cat contact_network/potential_contacts.json | head -10

# Check WordPress drafts
ls wordpress_integration/scheduled/
```

### 2. Review Job Leads (10 mins)
```bash
# Open job tracker
# Option A: View JSON directly
cat job_leads/indeed_leads.json

# Option B: Better - use Notion/Airtable
# Create a Notion database linked to this repo
```

**Action:** Mark 2-3 jobs as "interesting" → Add to your Airtable/Notion

### 3. Check Email for Opportunities (5 mins)
- Check Gmail for recruiter messages
- Scan LinkedIn for connection requests
- Check Substack/Twitter mentions

### 4. Read One Contact's Latest Work (10 mins)
- Open a recent contact from `contact_network/potential_contacts.json`
- Read their latest essay/post
- Note ideas for collaboration

---

## WRITING BLOCK (45-60 mins)

### 1. Choose Today's Topic (5 mins)
**Sources for ideas:**
- Your therapy notes (therapy_and_wellbeing/)
- Recent job rejections/accepts
- Interesting problem you solved
- Question someone asked you
- Your health journey
- A tool you discovered

**Avoid:** Overthinking. Just pick something.

### 2. Write Your 500-Word Essay (30-40 mins)
```bash
# Create today's essay
cp daily_essays/templates/ESSAY_TEMPLATE.md daily_essays/2026-06-02_topic_name.md

# Edit in your editor
vim daily_essays/2026-06-02_topic_name.md

# Guidelines:
# - 500 words (450-550 OK)
# - Active voice ("I discovered" not "It was found")
# - One clear structure (hook → problem → solution → reflection)
# - Include health note at top
# - Include 1-2 tags/keywords
```

### 3. Edit & Check SEO (10-15 mins)
```bash
# Copy essay to Hemingway Editor
# hemingwayapp.com

# Check:
# ✓ Passive voice → active
# ✓ Sentence clarity
# ✓ Adverb overuse
# ✓ Meta description < 160 chars
```

### 4. Publish to WordPress
```bash
# Direct publish (immediate)
python3 wordpress_integration/wp_publisher.py \
  --file daily_essays/2026-06-02_topic_name.md \
  --category Writing \
  --tags essay,career,learning \
  --publish

# OR schedule for later
python3 wordpress_integration/wp_publisher.py \
  --file daily_essays/2026-06-02_topic_name.md \
  --category Writing \
  --tags essay,career,learning \
  --schedule "2026-06-03 08:00"
```

**Watch for:** ✓ Green checkmark = published successfully

---

## AFTERNOON AUTOMATION (20 mins)

### 1. Run Job Scraper (5 mins)
```bash
# Scrape Indeed for new jobs
python3 automation_scripts/indeed_scraper.py \
  --keywords "English teacher" \
  --location "France" \
  --max-pages 3

# Results saved to job_leads/indeed_leads.json
```

### 2. Find New Contacts/Collaborators (5 mins)
```bash
# Find writers interested in your topic
python3 automation_scripts/contact_finder.py \
  --search "disability writing" \
  --type writers \
  --limit 10

# Results saved to contact_network/potential_contacts.json
```

### 3. Review & Respond to Opportunities (10 mins)
- Check job_leads for "interesting" ones
- Mark 1-2 for formal applications
- Copy interesting contact templates to a "to-reach-out" list
- If interesting person found → send outreach email

---

## WEEKLY TASKS (Sunday Evening)

### 1. Create Essay Index (5 mins)
```bash
# Update daily_essays/LATEST.md with this week's essays
# Format:
# - Title | Date | Category | Word Count | SEO Keywords
```

### 2. Analyze Blog Analytics (5 mins)
```bash
# Check Google Analytics
# Which essays got traffic?
# Which keywords ranked?
# Adjust next week's topics
```

### 3. Job Application Push (15 mins)
```bash
# Review all "interesting" jobs from the week
# Write and send 2-3 formal applications
# Update job_leads/applications.json with submission dates
```

### 4. Contact Outreach Batch (20 mins)
```bash
# Select 3-5 potential collaborators
# Personalize outreach emails
# Send from Gmail
# Log in contact_network/outreach_log.json
```

### 5. Git Commit & Push Everything (5 mins)
```bash
git add daily_essays/ job_leads/ contact_network/
git commit -m "Weekly update: essays + jobs + contacts"
git push origin claude/dazzling-curie-9WLUZ
```

---

## AUTOMATION YOU CAN SET UP (One-Time Setup)

### Daily Job Scraper (Runs at 9 AM)
```bash
# Add to crontab
crontab -e

# Add this line:
0 9 * * * cd /home/user/my_professional_documents && python3 automation_scripts/indeed_scraper.py --keywords "English teacher" --location "France" 2>&1 >> cron.log
```

### GitHub Actions - Daily Auto-Backup
```yaml
# Create .github/workflows/daily_backup.yml
name: Daily Auto-Backup
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      - name: Auto-commit changes
        run: |
          git add .
          git config user.email "auto@bot.local"
          git config user.name "Auto Backup"
          git commit -m "Auto-backup: $(date)" || true
          git push
```

### Email Digest (Weekly Summary)
```python
# Save as automation_scripts/weekly_digest.py
# Reads job_leads + contacts + essay count
# Sends email summary every Sunday

import smtplib
import json
from email.mime.text import MIMEText

# Generates: "This week: 5 essays, 23 jobs, 8 new contacts"
```

---

## HEALTH & WELLBEING CHECKS

**Important:** Quality over perfection.

### If Energy is Low:
- Write 250 words instead of 500 (still publish)
- Skip job scraping, focus on writing
- Rest is productivity

### If Overwhelmed:
- Write a short reflection (300 words) instead
- Don't force it
- Mark as "recharge day" in frontmatter

### If Having a Good Day:
- Write 750 words if energy permits
- Reach out to 5 contacts instead of 3
- Schedule multiple essays ahead

**Track in essay frontmatter:**
```yaml
health_note: "Good energy today. Pain level 3/10. Wrote easily."
```

This helps you identify patterns (good writing days correlate with X condition state).

---

## SAMPLE WEEK AT A GLANCE

| Day | Action | Time | Output |
|-----|--------|------|--------|
| Mon | Write essay + publish | 60 min | 1 blog post |
| Tue | Write essay + jobs scraping | 60 min | 1 blog post + 15 jobs |
| Wed | Write essay + find contacts | 60 min | 1 blog post + 8 contacts |
| Thu | Write essay + email review | 60 min | 1 blog post + 2 outreach emails |
| Fri | Write essay + WordPress check | 60 min | 1 blog post + analytics review |
| Sat | Light writing or edit backlog | 30 min | Polish 2 old essays or rest |
| Sun | Job applications + batch outreach | 45 min | 3 job applications + 5 emails sent |

**Total weekly output:**
- ✅ 5-6 published essays (2,500-3,000 words)
- ✅ ~75 new job leads (tracked)
- ✅ ~30 potential contacts discovered
- ✅ ~8 new professional outreach emails sent
- ✅ Everything backed up to GitHub + WordPress

---

## TOOLS YOU NEED RUNNING

**Installed:**
- Python 3.8+
- Git
- A text editor (VS Code, Vim, etc.)

**Services:**
- WordPress (sourovdeb.com) - already live
- GitHub (your repo) - already live
- Gmail - already set up
- Google Analytics - link your blog

**Optional but recommended:**
- Notion (free) for job/contact dashboard
- Airtable (free) for job tracking
- Hemingway Editor (free) for editing

---

## QUICK START TODAY

**Right now:**
```bash
# 1. Create today's essay
cp daily_essays/templates/ESSAY_TEMPLATE.md daily_essays/2026-06-02_my_first_essay.md

# 2. Write (45 mins)
vim daily_essays/2026-06-02_my_first_essay.md

# 3. Publish
python3 wordpress_integration/wp_publisher.py \
  --file daily_essays/2026-06-02_my_first_essay.md \
  --category Writing \
  --tags essay,career \
  --publish

# 4. Check it live at https://www.sourovdeb.com/

# 5. Scrape some jobs
python3 automation_scripts/indeed_scraper.py

# 6. Commit everything
git add .
git commit -m "First daily essay + jobs"
git push origin claude/dazzling-curie-9WLUZ
```

**Done.** That's the entire workflow. Just repeat daily.

---

**Remember:**
- 500 words = 25-30 mins of writing
- Everything else is automation
- Your job: Write good essays + Choose 2-3 promising leads/contacts/opportunities per week
- The scripts do the rest
