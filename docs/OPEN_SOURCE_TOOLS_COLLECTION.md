# Curated Open-Source Tools for Automation

## Workflow Automation

### n8n ⭐ Recommended
- **GitHub**: github.com/n8n-io/n8n (65k+ stars)
- **What**: Visual workflow automation — connect Google Sheets → AI → WordPress with drag-and-drop
- **Self-host free**: `docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n`
- **Cloud**: $20/month
- **Best for you**: Google Sheet row → HTTP call → WordPress API, no code

### Huginn
- **GitHub**: github.com/huginn/huginn (43k+ stars)
- **What**: Agent-based automation — agents watch, react, act
- **Best use**: Monitor Indeed RSS → email job matches; monitor news → auto-post to WordPress

### Activepieces
- **GitHub**: github.com/activepieces/activepieces (12k+ stars)
- **What**: Open-source Zapier alternative with WordPress integration built in

---

## WordPress Tools

### WP-CLI (Essential)
- **URL**: wp-cli.org
- Command-line WordPress control (requires SSH access)

```bash
# Fix posts with no category
wp post list --cat=0 --format=ids | xargs wp post term add post_tag elt

# List all empty categories
wp term list category --fields=term_id,name,count | awk '$3 == 0'

# Backup before fixing
wp export --post_type=post > backup_$(date +%Y%m%d).xml

# Update all plugins
wp plugin update --all

# Check site health
wp doctor check --all
```

### WP Scheduled Posts Plugin
- **URL**: wordpress.org/plugins/wp-scheduled-posts/
- Bulk schedule from CSV without code

### Rank Math SEO
- **URL**: wordpress.org/plugins/seo-by-rank-math/
- Free SEO plugin with REST API support — your scripts can set SEO metadata via API

---

## Job Hunting Tools

### JobSpy ⭐ Recommended
- **GitHub**: github.com/Bunsly/JobSpy
- Multi-site scraper: Indeed, LinkedIn, Glassdoor, ZipRecruiter

```python
pip install python-jobspy

from jobspy import scrape_jobs
import pandas as pd

jobs = scrape_jobs(
    site_name=['indeed', 'linkedin'],
    search_term='ELT teacher OR TEFL OR English teacher',
    location='Reunion Island',
    results_wanted=20,
    hours_old=48
)
jobs.to_csv('jobs_today.csv', index=False)
print(jobs[['title','company','location','job_url']].to_string())
```

### JobFunnel
- **GitHub**: github.com/PaulMcInnis/JobFunnel
- Scrapes job boards into a spreadsheet, deduplicates, scores matches

### Resume Matcher
- **GitHub**: github.com/srbhr/Resume-Matcher
- Compares your CV to job descriptions, gives ATS match score

---

## Writing & Productivity (Neurodivergent-Friendly)

### Obsidian
- **URL**: obsidian.md (free desktop app)
- **Best plugins**:
  - `obsidian-tasks` — task management with due dates
  - `calendar` — daily note navigation
  - `periodic-notes` — automatic daily/weekly templates
  - `obsidian-pomodoro-timer` — built-in focus timer

### Logseq
- **GitHub**: github.com/logseq/logseq
- Block-based note-taking, non-linear thinking
- Export pages as Markdown → feed to folder watcher → WordPress draft

### Zettlr
- **URL**: zettlr.com
- Academic markdown editor, exports cleanly

---

## Health & Habit Tracking

### Habitica
- **URL**: habitica.com / **GitHub**: github.com/HabitRPG/habitica
- Turns habits and to-dos into an RPG game — gamification helps motivation during low phases

### eMoods
- **URL**: emoodtracker.com
- Mood tracking app designed specifically for bipolar disorder
- Exports CSV for review with your doctor

---

## Image & Banner Automation

### ImageMagick (Batch Banner Creation)
```bash
# Create a blog banner from a title
convert -size 1200x628 gradient:'#1e3a5f-#0a1628' \
  -font DejaVu-Sans-Bold -pointsize 55 -fill white \
  -gravity Center -annotate 0 'Day 32: Listening & Phonology' \
  -font DejaVu-Sans -pointsize 28 -fill '#a8c8f0' \
  -gravity South -annotate '+0+50' 'sourovdeb.com' \
  banner_day32.png
```

### Stable Diffusion WebUI
- **GitHub**: github.com/AUTOMATIC1111/stable-diffusion-webui
- Generate blog header images from text descriptions, runs locally, free

---

## Self-Care Apps

| App | Platform | Cost | Purpose |
|-----|----------|------|---------|
| **Daylio** | iOS/Android | Free | Micro mood journal |
| **Bearable** | iOS/Android | Free | Symptom + mood tracking |
| **Finch** | iOS/Android | Free | Gentle habit building |
| **Woebot** | Web/Mobile | Free | AI-assisted CBT |
| **DBT Coach** | iOS/Android | Free | DBT skills practice |
| **SuperBetter** | iOS/Android | Free | Gamified resilience |
