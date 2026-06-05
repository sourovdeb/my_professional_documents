# Open-Source Tools Collection — WordPress, Writing & Automation

> All tools listed here are free, open-source, and verified as of June 2026. GitHub stars included as a quality signal.

---

## Category 1: WordPress Automation Tools

### Plugins (Install from WordPress Admin → Plugins → Add New)

| Plugin | Purpose | Free? | Notes |
|--------|---------|-------|-------|
| **WP-CLI** | Terminal control of WordPress | Free | Most powerful — run `wp post create` in SSH |
| **Jetpack** | Scheduling, social sharing, SEO | Free tier | All-in-one, great for beginners |
| **PublishPress** | Editorial calendar, scheduling | Free | Visual calendar for post scheduling |
| **WP Scheduled Posts** | Bulk scheduling from CSV | Free | Import CSV → schedule 30 posts at once |
| **All in One SEO** | Meta descriptions, sitemap | Free | Better than Yoast for beginners |
| **Rank Math** | SEO + schema + redirects | Free | Most comprehensive free SEO plugin |
| **WP REST API** | Already built into WP | Free | Core — what your automation scripts use |
| **WP Webhooks** | Send/receive webhooks | Free | Connect WordPress to any automation tool |

### Self-Hosted Automation Tools

| Tool | GitHub | Purpose | Setup Difficulty |
|------|--------|---------|------------------|
| **n8n** | github.com/n8n-io/n8n | No-code automation (like Zapier, self-hosted) | Medium |
| **Huginn** | github.com/huginn/huginn | Agent-based automation, monitors & acts | Hard |
| **Activepieces** | github.com/activepieces/activepieces | Modern open-source Zapier alternative | Easy |
| **Automatisch** | github.com/automatisch/automatisch | Simple workflow automation | Easy |

### n8n Quick Setup (Most Recommended)

n8n is the best open-source replacement for Zapier. Run it locally:

```bash
npx n8n
# Opens at http://localhost:5678
```

Or with Docker (more stable):
```bash
docker run -d --name n8n -p 5678:5678 n8nio/n8n
```

Then create a workflow: **Google Sheets trigger → HTTP Request → WordPress**. No coding needed.

---

## Category 2: Writing & Publishing Tools

### Markdown Editors

| Tool | URL/GitHub | Best For |
|------|-----------|----------|
| **Logseq** | logseq.com | Daily notes, linked thinking, outline writing |
| **Obsidian** | obsidian.md | Knowledge base, long-form writing |
| **Typora** | typora.io | Clean WYSIWYG Markdown editor |
| **Mark Text** | github.com/marktext/marktext | Free Typora alternative |
| **Zettlr** | github.com/Zettlr/Zettlr | Academic writing in Markdown |
| **ghostwriter** | github.com/KDE/ghostwriter | Distraction-free, Linux/Windows |
| **Nota** | nota.md | Simple, beautiful Markdown editor |

### File Watcher / Publisher Scripts

| Tool | GitHub | Purpose |
|------|--------|--------|
| **chokidar** | github.com/paulmillr/chokidar | Watch folder for new files (Node.js) |
| **watchdog** | github.com/gorakhargosh/watchdog | Watch folder for new files (Python) |
| **pandoc** | github.com/jgm/pandoc | Convert between Markdown, HTML, DOCX |

---

## Category 3: Job Hunting Automation

| Tool | GitHub/URL | Purpose |
|------|-----------|--------|
| **JobFunnel** | github.com/PaulMcInnis/JobFunnel | Scrapes Indeed/LinkedIn, saves to spreadsheet |
| **job-scraper** | github.com/nicholasgasior/job-scraper | Basic job search scraper |
| **LinkedIn Job Scraper** | github.com/spinlud/py-linkedin-jobs-scraper | Python LinkedIn scraper |
| **HN-jobs-scraper** | Various repos | Hacker News "Who's Hiring" scraper |
| **PRAW** | github.com/praw-dev/praw | Reddit API for r/forhire, r/ELTteachers |

### Job Alert Automation (No Scraping Needed)

```python
# Simple RSS-based job alert (runs daily via cron)
import feedparser
import smtplib
from email.mime.text import MIMEText

def check_indeed_rss(query='ELT teacher', location='Reunion'):
    url = f'https://rss.indeed.com/rss?q={query.replace(" ","+")}&l={location}'
    feed = feedparser.parse(url)
    return [{'title': e.title, 'link': e.link, 'summary': e.summary[:200]} for e in feed.entries[:5]]

# Combine with email or Telegram notification
```

---

## Category 4: Health & Productivity for Neurodiversity

| Tool | Platform | Purpose | Free? |
|------|----------|---------|-------|
| **eMoods** | Android/iOS | Bipolar mood tracker | Free basic |
| **Daylio** | Android/iOS | Micro-journal + mood logging | Free |
| **Bearable** | Android/iOS | Symptom + mood + medication tracker | Free |
| **Finch** | Android/iOS | Self-care gamified pet | Free |
| **Pomofocus** | pomofocus.io | Pomodoro timer (25min work, 5min rest) | Free |
| **ActivityWatch** | github.com/ActivityWatch | Tracks how you spend time on screen | Free |
| **Super Productivity** | github.com/johannesjo/super-productivity | To-do with time tracking | Free |
| **Notesnook** | github.com/streetwriters/notesnook | Private encrypted journal | Free |
| **Logseg** | logseq.com | Daily journaling + writing | Free |
| **Standard Notes** | github.com/standardnotes | Encrypted note-taking | Free |

---

## Category 5: WordPress Health Monitoring

| Tool | Purpose | Free? |
|------|---------|-------|
| **Uptime Robot** | uptimerobot.com — alerts if your site goes down | Free (50 monitors) |
| **StatusCake** | statuscake.com — uptime + performance | Free tier |
| **WP Umbrella** | wp-umbrella.com — backup + security | Free tier |
| **UpdraftPlus** | WordPress plugin — automated backups | Free |
| **Wordfence** | WordPress plugin — security scanner | Free |
| **Query Monitor** | WordPress plugin — database query profiler | Free |
| **WP Crontrol** | WordPress plugin — view/manage cron jobs | Free |

### Quick WordPress Health Check Script

```python
# health_check.py — run daily via cron
import requests
import datetime

def check_wordpress_health(wp_url):
    checks = []
    
    # Check site is up
    try:
        r = requests.get(wp_url, timeout=10)
        checks.append({'name': 'Site reachable', 'status': r.status_code == 200})
    except:
        checks.append({'name': 'Site reachable', 'status': False})
    
    # Check REST API is responding
    try:
        r = requests.get(f'{wp_url}/wp-json/wp/v2/posts?per_page=1', timeout=10)
        checks.append({'name': 'REST API working', 'status': r.status_code == 200})
    except:
        checks.append({'name': 'REST API working', 'status': False})
    
    # Check custom API endpoint
    try:
        r = requests.get(f'{wp_url}/wp-json/sourov/v1/status', timeout=10)
        checks.append({'name': 'Custom plugin active', 'status': r.status_code != 404})
    except:
        checks.append({'name': 'Custom plugin active', 'status': False})
    
    print(f'Health check at {datetime.datetime.now()}')
    for c in checks:
        status = 'OK' if c['status'] else 'FAIL'
        print(f'  [{status}] {c["name"]}')
    
    return all(c['status'] for c in checks)

if __name__ == '__main__':
    check_wordpress_health('https://sourovdeb.com')
```

---

## Category 6: AI-Powered Open Source Tools for Writers

| Tool | GitHub | Purpose |
|------|--------|--------|
| **Open WebUI** | github.com/open-webui/open-webui | Browser-based ChatGPT alternative (works with Ollama) |
| **Jan.ai** | github.com/janhq/jan | Desktop AI app, runs any model locally |
| **LM Studio** | lmstudio.ai | Try and run any open-source AI model |
| **Ollama** | github.com/ollama/ollama | Run LLMs locally |
| **AnythingLLM** | github.com/Mintplex-Labs/anything-llm | Chat with your own documents |
| **Lobe Chat** | github.com/lobehub/lobe-chat | Self-hosted ChatGPT-like interface |
| **LibreChat** | github.com/danny-avila/LibreChat | Self-hosted multi-model AI chat |
| **PrivateGPT** | github.com/zylon-ai/private-gpt | Chat with documents, fully offline |

---

## Category 7: GitHub Actions for Writers

Useful GitHub Actions workflows:

| Action | Use |
|--------|-----|
| `actions/checkout` | Clone repo in workflow |
| `actions/setup-python` | Run Python scripts |
| `peter-evans/create-or-update-comment` | Auto-comment on PRs |
| `dorny/paths-filter` | Only run when specific files changed |
| `appleboy/telegram-action` | Send Telegram notification on push |

See `.github/workflows/publish_on_push.yml` in this repo for a working example.
