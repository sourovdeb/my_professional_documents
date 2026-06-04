# Sourov's Complete Remote Automation System
## Master Guide — Everything in One Place

---

## What This System Does For You

You write (or speak, or think). The machine does everything else.

This guide is the single reference document for your entire publishing and job-hunting automation system. It links to all the scripts, tutorials, and tools in this repository.

---

## Repository Structure

```
my_professional_documents/
├── tutorials/
│   └── csv_google_apps_script_tutorial.md   ← START HERE if you are new
├── scripts/
│   ├── sheet_publisher.gs     ← Google Apps Script (paste into Sheets)
│   ├── auto_publisher.py      ← Python: folder watcher → WordPress
│   ├── fix_wp_categories_tags.py  ← Python: bulk-fix all WP posts
│   ├── folder_watcher.js      ← Node.js: real-time folder watcher
│   └── wp_publisher.py        ← Python: Tkinter desktop GUI app
├── resources/
│   ├── tools_collection.md    ← All automation & productivity tools
│   ├── audio_video_banner_tools.md  ← Audio/video/design tools
│   └── free_ai_remote_publishing.md ← Claude, ChatGPT, Mistral guide
└── docs/
    └── master_guide.md        ← This file
```

---

## Quick Start: Which Path Is Right for You?

### Path A: "I just want to write and have it published" (Recommended to start)
1. Read `tutorials/csv_google_apps_script_tutorial.md`
2. Set up your Google Sheet with the Queue tab
3. Paste `scripts/sheet_publisher.gs` into Apps Script
4. Set the time trigger to run every hour
5. Done — fill in the sheet to publish

### Path B: "I write in Logseq and want drafts auto-published"
1. Install Node.js: https://nodejs.org
2. Run `npm install chokidar node-fetch dotenv marked`
3. Create `.env` with your credentials
4. Run `node scripts/folder_watcher.js`
5. Drop `.md` files into `~/wordpress_queue/` to publish

### Path C: "I want a desktop app with buttons"
1. Install Python 3: https://python.org
2. Run `pip install requests python-dotenv`
3. Create `.env` with credentials
4. Run `python scripts/wp_publisher.py`
5. A GUI opens — fill in the form and click Publish

### Path D: "I write on GitHub and want instant publishing"
1. Add `WP_API_KEY` secret to your GitHub repo settings
2. Create `.github/workflows/publish_draft.yml` (see `resources/free_ai_remote_publishing.md`)
3. Push any `.md` file to the `drafts/` folder
4. GitHub Action auto-publishes it

---

## Daily Workflow (Minimum Effort)

### On a good day (10 minutes total)
```
09:00 — Open Mistral Canvas or Claude
09:01 — Type: "Write 500 words about [teaching topic]"
09:03 — Review and copy the text
09:04 — Open Google Sheet → paste title + content → set status to 'ready'
09:05 — Done. System publishes automatically within the hour.
```

### On a hard day (2 minutes total)
```
Open Google Sheet.
Type a single line title in Column A.
Write one sentence in Column B.
Mark as 'ready'.
Leave. The AI system will expand it later if you want.
Or just leave the draft incomplete — it's fine.
```

### On the worst days (0 minutes)
```
Do nothing.
Drafts queue up for later.
The system does not break.
You are not behind.
```

---

## Fixing Your WordPress Posts (Run Once)

Your existing WordPress posts may have:
- Posts stuck in 'Uncategorized'
- Posts with no tags
- Posts with no SEO meta descriptions

To fix all of these at once:

1. Create WordPress Application Password:
   - WordPress Admin → Users → Profile → Application Passwords → Add New
   - Copy the password (shown only once)

2. Create `.env` file:
```
WP_BASE_URL=https://sourovdeb.com
WP_USER=your_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx
```

3. Run dry-run first (preview only, no changes):
```bash
python scripts/fix_wp_categories_tags.py --dry-run
```

4. If the preview looks correct, run for real:
```bash
python scripts/fix_wp_categories_tags.py
```

The script automatically:
- Detects the correct category from post content keywords
- Adds relevant tags based on the same keyword analysis
- Creates any missing categories/tags in WordPress
- Logs every change made

---

## Job Hunting Automation

### Set Up Daily Job Alerts (No-Code)
1. **Indeed RSS:** `https://rss.indeed.com/rss?q=ELT+teacher&l=La+Reunion`
   - Add to your RSS reader (Feedly: https://feedly.com — free)
   - Or set up email alert via https://blogtrottr.com (RSS → email for free)

2. **Google Jobs Alert:**
   - Search "ELT teacher Réunion" on Google
   - Click Tools → Any time → turn on alerts
   - Receive daily email when new positions are posted

3. **LinkedIn Jobs:** Set weekly digest with saved search

### AI-Powered Job Application
- Tool: https://github.com/surapuramakhil-org/Job_search_agent (150 stars)
- Tool: https://github.com/srbhr/Resume-Matcher (5000+ stars) — match your CV to jobs
- These require Python setup — tackle after publishing system is running

---

## Health Management Automation

### Mood Tracking (Automatic)
1. Create a Google Form with:
   - Date (auto-filled)
   - Mood (1-10 scale)
   - Energy level (1-10)
   - Sleep hours
   - Medications taken (yes/no)
2. Responses auto-save to a Google Sheet
3. Use Apps Script to send you a weekly mood summary email
4. Apps Script can alert you if mood stays below 4 for 3+ consecutive days

### Low-Energy Publishing Strategy
- **Template library:** Save 5-10 post templates in your Google Sheet for common post types
- **Speech-to-text:** Google Docs → Tools → Voice Typing (no app needed)
- **AI expansion:** Write 3 bullet points → ask Mistral to expand into 500 words
- **Pre-scheduled content:** When energy is high, write 10 posts → schedule across 2 weeks

---

## Official Mental Health Resources

| Condition | Resource | URL |
|-----------|----------|-----|
| Bipolar disorder | NIMH | https://www.nimh.nih.gov/health/topics/bipolar-disorder |
| Bipolar support | IBPF | https://ibpf.org |
| Depression | WHO | https://www.who.int/news-room/fact-sheets/detail/depression |
| Medication info | PubMed | https://pubmed.ncbi.nlm.nih.gov |
| Self-management | eMoods | https://emoodtracker.com |
| Peer support | NAMI | https://www.nami.org |

---

## Credentials & Security

**Never commit real credentials to GitHub.**

Store them in:
- A `.env` file (excluded by `.gitignore`)
- Google Apps Script Properties (File > Project Properties > Script Properties)
- GitHub Secrets (repo Settings > Secrets > Actions)
- A password manager (Bitwarden: https://bitwarden.com — free, open source)

Your `.gitignore` should include:
```
.env
*.log
credentials.json
*.pyc
__pycache__/
.DS_Store
```

---

## Support & Updates

If something stops working:
1. Check the WordPress plugin is active at `sourovdeb.com/wp-admin`
2. Check Apps Script logs: Extensions > Apps Script > Executions
3. Run `python scripts/auto_publisher.py` manually in terminal to see error messages
4. Check this repository for updated scripts

---

*This guide covers the complete system as of June 2026.*
*All tools listed are verified as functional and free (or free-tier available) at time of writing.*
