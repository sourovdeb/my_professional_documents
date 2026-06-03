# Open-Source Tools Catalogue

Curated, verified tools for WordPress automation, writing, job hunting, and wellbeing.
All tools below are free and open-source unless marked *(freemium)*.

---

## 1. WordPress Automation

| Tool | What it does | Install | Stars |
|------|-------------|---------|-------|
| **WP-CLI** | Full WordPress control from terminal: create posts, manage plugins, run cron | `composer global require wp-cli/wp-cli` | 4.9k |
| **Jetpack** | Scheduling, Publicize (auto social share), SEO, related posts | WP plugin repo | — |
| **WP Scheduled Posts** | Visual calendar + bulk CSV import for scheduled publishing | WP plugin repo | — |
| **PublishPress** | Editorial calendar, role-based workflows, content notifications | WP plugin repo | — |
| **n8n** | Node-based workflow automation (Google Sheets → WordPress, etc.) | `npm install n8n -g` | 50k+ |
| **Huginn** | Agent-based automation: scrape, monitor, post | Docker / Ruby | 42k |
| **Activepieces** | n8n alternative, self-hostable, no-code workflow builder | Docker | 10k+ |
| **Automattic/Newspack** | Full publishing infrastructure (for media orgs) | GitHub | — |
| **WordPress REST API** | Built-in — no install needed; all automation in this repo uses it | Built-in WP 4.7+ | — |

### WP-CLI Quick Reference
```bash
# Create a draft post
wp post create --post_title="Day 33: Intonation" --post_status=draft --post_content="<p>Body here</p>"

# Publish a draft (replace 42 with post ID)
wp post update 42 --post_status=publish

# Import posts from CSV (requires WP All Import plugin)
wp all-import process /path/to/posts.xml

# Check site health
wp doctor check --all
```

---

## 2. Writing & Markdown Tools

| Tool | What it does | Platform |
|------|-------------|----------|
| **Obsidian** | Local Markdown notes, graph view, plugin ecosystem | Win/Mac/Linux |
| **Logseq** | Outliner + daily notes, block-based, open-source | Win/Mac/Linux |
| **Zettlr** | Academic Markdown editor, export to DOCX/PDF | Win/Mac/Linux |
| **Mark Text** | Distraction-free Markdown editor | Win/Mac/Linux |
| **Pandoc** | Convert Markdown → DOCX, PDF, HTML, EPUB | CLI |
| **Vale** | Prose linter (grammar, style, tone) — runs in CI | CLI |
| **LanguageTool** | Open-source grammar/spelling checker, self-hostable | API / Docker |
| **Hemingway App** | Readability analysis | Web (free tier) |

### Pandoc: Convert Markdown to WordPress-ready HTML
```bash
# Install
brew install pandoc  # or: sudo apt install pandoc

# Convert
pandoc post.md -o post.html --no-highlight

# Then pipe into your auto_publisher.py content field
```

---

## 3. Scheduling & Publishing Pipelines

| Tool | What it does | Hosting |
|------|-------------|------|
| **Cron** | OS-level job scheduler | Any Linux/Mac |
| **n8n** | Visual workflow editor; Google Sheets → WP webhook | Self-hosted |
| **GitHub Actions** | Free CI/CD; triggers on file push | GitHub (free) |
| **Zapier** | 100 tasks/month free; Google Drive → WordPress | Cloud |
| **IFTTT** | Simple webhook triggers | Cloud |
| **Activepieces** | Zapier alternative, self-hosted | Docker |
| **Windmill** | Script-based workflows (Python/JS), UI included | Self-hosted |

### n8n: Google Sheets → WordPress in 10 minutes
```bash
# Install via npm
npx n8n

# Or Docker
docker run -it --rm -p 5678:5678 n8nio/n8n
# Open http://localhost:5678
# Create workflow: Google Sheets trigger → HTTP Request node → your WP endpoint
```

---

## 4. Social Media Cross-Posting

| Tool | Platforms | Free? |
|------|-----------|-------|
| **Buffer** | Twitter, LinkedIn, Facebook, Instagram | Freemium (3 channels free) |
| **Hootsuite** | All major platforms | Freemium |
| **Publicize (Jetpack)** | Twitter, Facebook, LinkedIn | Free |
| **Medium API** | Cross-post from WP to Medium | Free |
| **IFTTT + RSS** | WP RSS feed → any platform | Free |
| **RSS.app** | Turn blog into newsletter | Freemium |

### Auto-post to Medium from WordPress RSS
1. Install **WP RSS Aggregator** or use native feed: `https://yourdomain.com/feed/`
2. In IFTTT: Trigger = "New item in RSS feed" → Action = "Create a story on Medium"

---

## 5. SEO Tools (Free)

| Tool | Purpose |
|------|--------|
| **Yoast SEO** (WP plugin) | Meta descriptions, XML sitemap, readability |
| **Rank Math** (WP plugin) | Schema markup, keyword tracking |
| **Google Search Console** | Monitor indexing, clicks, errors |
| **Screaming Frog** | Site crawler; detect broken links, missing meta |
| **Ahrefs Webmaster Tools** | Free backlink + health checker |
| **PageSpeed Insights** | Google's performance + Core Web Vitals |

---

## 6. Job Hunting Automation

| Tool | What it does | Links |
|------|-------------|-------|
| **Jobspy** | Scrapes Indeed, LinkedIn, Glassdoor into CSV | `pip install python-jobspy` |
| **Indeed RSS** | Built-in RSS feed for any search query | `rss.indeed.com/rss?q=ELT&l=Reunion` |
| **PRAW** | Reddit API wrapper; monitor r/ELTteachers, r/TEFL | `pip install praw` |
| **LinkedIn API** | Official API for job search (requires app approval) | developers.linkedin.com |
| **Joplin + Email** | Save job listings to local notes via email | Free, self-hosted |
| **ApplicantTracking.io** | Track applications in a spreadsheet | Free template |
| **Huntr** | Kanban board for job applications | Free tier |

### Jobspy — search Indeed + LinkedIn in one command
```bash
pip install python-jobspy

python -c "
import csv
from jobspy import scrape_jobs
jobs = scrape_jobs(
    site_name=['indeed', 'linkedin'],
    search_term='ELT teacher',
    location='Reunion',
    results_wanted=20
)
jobs.to_csv('jobs.csv', index=False)
print(jobs[['title','company','location','job_url']].to_string())
"
```

---

## 7. Image & Design (Free)

| Tool | Use Case |
|------|----------|
| **Canva** (free tier) | Blog headers, Pinterest pins, social cards |
| **GIMP** | Full image editing |
| **Inkscape** | SVG / vector graphics |
| **Unsplash** | Royalty-free photography |
| **Pexels** | Royalty-free photos and videos |
| **Stable Diffusion** (local) | AI image generation, private, no API cost |
| **Squoosh** | Browser-based image compression |

---

## 8. Monitoring & Uptime

| Tool | What it does | Free tier |
|------|-------------|----------|
| **UptimeRobot** | Monitor site uptime, alert via email/SMS | 50 monitors free |
| **StatusCake** | Uptime + page speed monitoring | Free tier |
| **Freshping** | 50 checks, 1-min interval | Free |
| **HetrixTools** | Blacklist monitor + uptime | Free tier |
| **Grafana + Prometheus** | Full metrics dashboard (self-hosted) | Free |
| **Better Uptime** | Incident management + status page | Free tier |

### UptimeRobot setup (2 minutes)
1. Sign up at uptimerobot.com
2. Add monitor: HTTP(s) → `https://yourdomain.com`
3. Set alert contact: your email
4. Done — you get an email if the site goes down

---

## 9. Backup Tools

| Tool | What it does |
|------|-------------|
| **UpdraftPlus** (WP plugin) | Scheduled backups to Google Drive / Dropbox / S3 |
| **BackWPup** | Backup to FTP, S3, Dropbox |
| **Duplicator** | Migrate + clone WordPress sites |
| **rsync** | Command-line file sync / incremental backup |
| **rclone** | Sync to 40+ cloud providers from command line |

### Automated backup with rclone
```bash
# Install
curl https://rclone.org/install.sh | sudo bash

# Configure (interactive)
rclone config

# Sync WordPress files to Google Drive
rclone sync /var/www/html/wp-content gdrive:wp-backup/wp-content

# Add to cron for daily backup at 2 AM
# 0 2 * * * rclone sync /var/www/html/wp-content gdrive:wp-backup/wp-content
```

---

## 10. Productivity (Neurodivergent-Friendly)

| Tool | What it does | Platform |
|------|-------------|----------|
| **Forest** | Focus timer with gamification | Mobile |
| **Pomofocus** | Web-based Pomodoro timer | Web (free) |
| **Focusmate** | Virtual co-working accountability | Web (free tier) |
| **Workflowy** | Infinite outliner for low-cognitive-load planning | Web / Mobile |
| **Notion** | Flexible workspace; templates for writers | Free tier |
| **Trello** | Visual Kanban for managing drafts / tasks | Free tier |
| **TickTick** | Task manager with Pomodoro built in | Free tier |
| **Daylio** | Micro mood journal (5 seconds/day) | Mobile |
| **eMoods** | Bipolar mood tracker | Mobile |
| **Bearable** | Symptom + mood + medication tracking | Mobile |

---

## 11. Local AI (Privacy-First Writing Assistance)

| Tool | What it does | Hardware req |
|------|-------------|------|
| **Ollama** | Run LLMs locally (Llama 3, Mistral, Phi-3) | 8 GB RAM min |
| **LM Studio** | GUI for local models | 8 GB RAM min |
| **Jan.ai** | Open-source ChatGPT alternative, local | 8 GB RAM min |
| **PrivateGPT** | Chat with your documents, fully local | 8 GB RAM min |
| **Whisper.cpp** | Local speech-to-text (dictate your writing) | Any modern CPU |

### Ollama: write with local AI
```bash
# Install
curl -fsSL https://ollama.com/install.sh | sh

# Download a model
ollama pull mistral

# Interactive chat
ollama run mistral

# API call (same interface as this repo's extension)
curl http://localhost:11434/api/generate \
  -d '{"model":"mistral","prompt":"Write a 500-word ELT blog post about pronunciation.","stream":false}'
```

---

*Last updated: 2026-06-03. All tools verified as actively maintained.*
