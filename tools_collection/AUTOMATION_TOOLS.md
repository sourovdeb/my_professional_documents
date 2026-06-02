# 🤖 Free & Open Source Automation Tools

**Principle:** Automate everything. Write once. Collect proven tools. Recycle scripts.

---

## JOB SCRAPING & TRACKING

### Indeed Scraper (Custom)
- **What:** Scrapes Indeed.com for jobs
- **Tool:** `automation_scripts/indeed_scraper.py`
- **Free:** Yes (no API key needed)
- **Use:** Find teaching/writing/tech jobs daily
- **Command:** 
  ```bash
  python3 automation_scripts/indeed_scraper.py --keywords "English teacher" --location "France"
  ```

### LinkedIn Job Alerts (Browser Extension)
- **What:** Email alerts for LinkedIn jobs
- **Tool:** LinkedIn Built-in
- **Free:** Yes (premium adds filters)
- **Use:** Set up job alerts, export to CSV
- **Setup:** linkedin.com/jobs → Alerts → Email me

### FlexJobs (Paid Alternative)
- **What:** Hand-curated remote jobs
- **Cost:** $15/month
- **Worth it?** If you want verified remote-only positions
- **Link:** flexjobs.com

### ScraperAPI (Free tier)
- **What:** Headless browser scraping
- **Free:** 1000 requests/month
- **Use:** Advanced job scraping with JavaScript rendering
- **Link:** scraperapi.com

---

## EMAIL AUTOMATION

### n8n (Self-Hosted)
- **What:** Visual workflow automation (IFTTT-like)
- **Free:** Self-hosted open source
- **Use:** Email sequences, job alerts → Gmail drafts, outreach campaigns
- **Install:** `docker run -it -p 5678:5678 n8nio/n8n`
- **Link:** n8n.io

### Zapier (Paid)
- **What:** Connect 5000+ apps without code
- **Cost:** $19-49/month (free tier: 100 tasks/month)
- **Use:** Job alerts → Email → Spreadsheet, LinkedIn → CRM
- **Link:** zapier.com

### Make.com (Integromat)
- **What:** Like Zapier, European-based
- **Cost:** Similar to Zapier
- **Free:** 1000 operations/month free tier
- **Use:** Job routing, contact enrichment workflows
- **Link:** make.com

### Email Hunter / Hunter.io
- **What:** Find email addresses of professionals
- **Cost:** Free: 50 searches/month; Paid: $50+/month
- **Use:** Find contact emails for cold outreach
- **Accuracy:** 95%+
- **Link:** hunter.io

---

## CONTENT MANAGEMENT & PUBLISHING

### WordPress (Your Site)
- **What:** `wordpress_integration/wp_publisher.py` (direct publish)
- **Cost:** Hosting (~€5-10/month), Domain
- **Custom Plugins:** Create your own (already set up)
- **SEO:** Yoast, RankMath (free + paid)

### Markdown to WordPress Converter
- **Tool:** `wordpress_integration/wp_publisher.py`
- **Features:** Auto SEO metadata, categories, tags, scheduling
- **Use:** `python3 wp_publisher.py --file daily_essays/essay.md --publish`

### Hugo + Netlify (Static Site)
- **What:** Fast static site generator + free hosting
- **Free:** Yes (Netlify tier)
- **Use:** Backup blog, faster load times
- **Deploy:** Push to GitHub → Auto-deploy
- **Link:** hugo.io + netlify.com

### Ghost (Hosted)
- **What:** Modern publishing platform
- **Cost:** $9/month hosted (open source free)
- **Features:** Newsletters, membership, clean interface
- **Worth it?** Better UX than WordPress if writing is priority
- **Link:** ghost.org

---

## CONTACT & RELATIONSHIP MANAGEMENT

### Contact Finder (Custom)
- **Tool:** `automation_scripts/contact_finder.py`
- **Search:** GitHub, Substack, Medium writers
- **Auto-email:** Generate outreach templates
- **Track:** potential_contacts.json

### Airtable (Free + Paid)
- **What:** Spreadsheet-database hybrid
- **Free:** Unlimited records, basic automation
- **Use:** Track contacts, writing projects, job applications
- **Link:** airtable.com

### HubSpot CRM (Free)
- **What:** Contact relationship management
- **Free:** Full CRM + 1000 contacts
- **Use:** Email tracking, deal pipeline (job applications)
- **Link:** hubspot.com/crm

### Dex (Personal CRM)
- **What:** Lightweight contact management for writers
- **Cost:** Free/$5/month
- **Use:** Remember people, track conversations
- **Link:** getdex.com

---

## WRITING & PRODUCTIVITY

### Obsidian (Free + Paid)
- **What:** Local markdown vault, PKM system
- **Free:** Personal use
- **Use:** Organize essays, ideas, health notes
- **Plugins:** Link essays to jobs, contacts, health tracking
- **Link:** obsidian.md

### Notion (Free)
- **What:** All-in-one workspace
- **Free:** Unlimited personal use
- **Use:** Essay drafts, job tracker, contact database, health journal
- **Link:** notion.so

### Hemingway Editor
- **What:** Simplify writing (active voice, passive detection)
- **Cost:** Free web version (hemingwayapp.com) or $19 desktop
- **Use:** Before publishing, catch passive voice
- **Link:** hemingwayapp.com

### Grammarly
- **What:** Grammar + plagiarism checker
- **Free:** Browser extension, basic checks
- **Paid:** $12/month for advanced
- **Use:** Polish essays before WordPress publish
- **Link:** grammarly.com

### Copyscape
- **What:** Check for plagiarism, duplicate content
- **Cost:** Free (limited searches)
- **Use:** Verify no accidental duplication before publish
- **Link:** copyscape.com

---

## SEO OPTIMIZATION

### Yoast SEO (WordPress Plugin)
- **What:** On-page SEO analysis
- **Free:** Plugin (free version)
- **Use:** Check keyword density, readability, meta descriptions
- **Link:** wordpress.org/plugins/wordpress-seo/

### RankMath (WordPress Plugin)
- **What:** Advanced SEO + Schema markup
- **Free:** Core features
- **Use:** Better than Yoast for some users
- **Link:** rankmath.com

### Google Search Console
- **What:** Monitor your site's performance in Google
- **Cost:** Free
- **Use:** Track rankings, fix indexing issues, check CTR
- **Setup:** search.google.com/search-console

### Ahrefs (Paid Alternative)
- **What:** SEO tools (competitor analysis, backlinks)
- **Cost:** $99+/month
- **Worth it?** No, for a solo writer blog
- **Link:** ahrefs.com

### AnswerThePublic
- **What:** See what people search for
- **Free:** 2 searches/day
- **Use:** Find essay topics, keywords people actually search
- **Link:** answerthepublic.com

---

## SOCIAL MEDIA AUTOMATION

### Buffer (Paid)
- **What:** Schedule posts to Twitter, LinkedIn, etc.
- **Cost:** $5-99/month
- **Use:** Auto-share essays across platforms
- **Link:** buffer.com

### Later (Paid)
- **What:** Social media scheduler
- **Cost:** $15-80/month
- **Link:** later.com

### IFTTT (Free)
- **What:** If This Then That - simple automation
- **Free:** 3 applets max
- **Use:** WordPress new post → Tweet, LinkedIn share
- **Link:** ifttt.com

### Custom Script (Best for Cost)
```python
# Save as automation_scripts/social_sharer.py
# Cross-post to Twitter/LinkedIn when essay published
# Use API keys + Tweepy (Twitter) + linkedin-api
```

---

## SCHEDULING & CRON JOBS

### Cron (Built-in Linux)
- **What:** Schedule scripts to run automatically
- **Free:** Built into Linux/Mac
- **Use:** Run job scraper daily, check emails, publish scheduled posts
- **Setup:**
  ```bash
  # Edit crontab
  crontab -e
  
  # Run job scraper every morning at 9 AM
  0 9 * * * python3 /path/to/automation_scripts/indeed_scraper.py --keywords "teacher"
  
  # Check email every hour
  0 * * * * python3 automation_scripts/email_checker.py
  ```

### GitHub Actions (Free)
- **What:** Run workflows on GitHub push/schedule
- **Free:** 2000 minutes/month
- **Use:** Auto-scrape jobs, publish scheduled essays, send weekly digest
- **Setup:** `.github/workflows/daily_job_scraper.yml`

### n8n Scheduled Workflows
- **What:** Schedule tasks in n8n
- **Free:** Self-hosted
- **Use:** Email sequences, daily digest emails

---

## ANALYTICS & TRACKING

### Google Analytics (Free)
- **What:** Track blog visitors
- **Free:** Yes
- **Use:** See which essays get traffic
- **Setup:** analytics.google.com

### Plausible (Privacy-Friendly)
- **What:** Simple analytics, no cookies
- **Cost:** $9/month
- **Use:** If you care about privacy (vs Google Analytics)
- **Link:** plausible.io

### StatCounter (Free)
- **What:** Alternative analytics
- **Free:** Basic stats
- **Link:** statcounter.com

### UTM Parameter Builder
- **What:** Track which links drive traffic
- **Free:** Use campaign utm params
- **Use:** Track LinkedIn posts → blog traffic
- **Tool:** google.com/analytics/features/utm_builder/

---

## HEALTH & WELLBEING TRACKING

### Health Notes (Custom JSON)
- **What:** Store health journey alongside writing
- **Use:** Tag essays with energy level, condition state
- **Tool:** Your `daily_essays/` frontmatter includes `health_note`

### Simple Health Journal
- **Free:** Notion or Obsidian template
- **Use:** Track how your condition affects writing productivity
- **Example:**
  ```yaml
  health_note: "Good day, high energy. Wrote 600 words. No pain."
  ```

### Apple Health / Google Fit
- **What:** Track sleep, activity, mood
- **Free:** Built into devices
- **Use:** Correlate with writing productivity

---

## BACKUP & VERSION CONTROL

### GitHub (Free Public Repo)
- **What:** Version control + backup
- **Free:** Unlimited public repos
- **Use:** Your essays, scripts, everything tracked
- **Push:** Daily automated commits

### GitHub Actions Backup
- **Automation:** Auto-commit changes daily
- **Workflow:**
  ```yaml
  name: Daily Backup
  on:
    schedule:
      - cron: '0 2 * * *'  # 2 AM daily
  jobs:
    backup:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v3
        - run: |
            git add .
            git commit -m "Daily auto-backup"
            git push
  ```

### Backblaze (Paid Cloud Backup)
- **What:** Unlimited cloud backup
- **Cost:** $7/month
- **Use:** Backup entire laptop (overkill for this)

---

## DEPLOYMENT & HOSTING

### Netlify (Free)
- **What:** Deploy static sites instantly
- **Free:** Unlimited sites, basic features
- **Use:** Static site backup of blog
- **Deploy:** Push to GitHub → Auto-deploy

### Vercel (Free)
- **What:** Deploy Node/Python apps
- **Free:** Basic tier
- **Use:** Deploy Flask app for job scraper dashboard
- **Link:** vercel.com

### PythonAnywhere (Free)
- **What:** Python web hosting
- **Free:** Limited resources
- **Use:** Run scripts in cloud (vs local cron)
- **Link:** pythonanywhere.com

### Railway (Free)
- **What:** Modern app hosting
- **Free:** $5 credit/month
- **Link:** railway.app

---

## DASHBOARD & MONITORING

### Grafana (Open Source)
- **What:** Visualize data
- **Free:** Self-hosted
- **Use:** Dashboard of: blog stats, job applications, essay count
- **Link:** grafana.com

### Superset (Open Source)
- **What:** Business intelligence dashboards
- **Free:** Self-hosted
- **Use:** Visualize job tracker, writing stats
- **Link:** superset.apache.org

### Simple JSON Dashboard
- **Create:** Custom HTML dashboard reading from JSON files
- **Track:** Daily word count, jobs scraped, contacts found

---

## RECOMMENDED WORKFLOW

**Free Stack (Best for starting):**
1. **Writing:** Obsidian (local) + WordPress (publish) + GitHub (backup)
2. **Jobs:** Custom scraper + Airtable (free tier)
3. **Contacts:** Contact Finder + HubSpot CRM (free)
4. **Email:** Gmail + n8n (self-hosted)
5. **Analytics:** Google Analytics
6. **Automation:** Cron jobs + GitHub Actions

**Paid Upgrade (When making money):**
1. Add Zapier for complex workflows
2. Add Hunter.io for email finding
3. Add RankMath for advanced SEO
4. Add Buffer for social sharing

---

## QUICK COMMAND CHEAT SHEET

```bash
# Scrape jobs daily
python3 automation_scripts/indeed_scraper.py --keywords "English teacher" --location "France"

# Find collaborators
python3 automation_scripts/contact_finder.py --search "disability writing"

# Publish essay to WordPress
python3 wordpress_integration/wp_publisher.py --file daily_essays/my_essay.md --publish

# Check spelling before publish
hemingwayapp.com  # Paste your essay

# Track in Notion
notion.so  # Manual or via Zapier integration

# Schedule daily jobs scraping
crontab -e
# Add: 0 9 * * * cd /path/repo && python3 automation_scripts/indeed_scraper.py
```

---

**Last Updated:** 2026-06-02  
**Next Review:** Monthly (remove unused, test new tools)
