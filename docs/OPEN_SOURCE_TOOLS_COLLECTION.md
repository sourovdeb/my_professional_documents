# Open Source Tools Collection
## Best Tools for Writing, WordPress, Job Hunting, and Wellbeing

---

## Writing & Note-Taking

| Tool | What it does | Get it |
|------|-------------|--------|
| **Logseq** | Outliner + daily notes, export Markdown | logseq.com |
| **Obsidian** | Linked notes, powerful search | obsidian.md |
| **Joplin** | Simple notes, syncs to Nextcloud/OneDrive | joplinapp.org |
| **Standard Notes** | Encrypted notes, free tier | standardnotes.com |
| **MarkText** | Clean Markdown editor | github.com/marktext/marktext |
| **Typora** | WYSIWYG Markdown (paid but cheap) | typora.io |
| **Zettlr** | Academic writing + Zettelkasten | zettlr.com |
| **CherryTree** | Hierarchical notebook | giuspen.net/cherrytree |

---

## WordPress Automation Tools

### n8n (self-hosted, free)
No-code automation that connects Google Sheets → WordPress without writing code.
- GitHub: github.com/n8n-io/n8n
- Install: `npm install -g n8n && n8n`
- Create a workflow: Google Sheets trigger → HTTP Request node → your WP API

### Huginn (self-hosted)
Powerful agent-based automation. Can monitor RSS feeds, scrape pages, post to WordPress.
- GitHub: github.com/huginn/huginn
- Harder to set up but very powerful

### WP-CLI (command line for WordPress)
If you have SSH access to your server, this is the fastest way to manage WordPress.
```bash
# Install
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp

# Create a post from the command line
wp post create \
  --post_title="Day 33: Grammar" \
  --post_content="<p>Today we studied...</p>" \
  --post_status=draft \
  --post_category="Grammar"

# Fix all posts missing a category
wp post list --post_status=any --fields=ID,post_title | while read id title; do
  wp post term add $id category "ELT Masterclass"
done
```

### Directus (headless CMS)
If you ever want to move away from WordPress but keep your content structured.
- github.com/directus/directus

---

## WordPress Category & Tag Fix Tools

### Problem: Posts Missing Categories
Run this WP-CLI batch command via SSH:
```bash
# List all posts without a category
wp post list --post_type=post --post_status=publish,draft \
  --fields=ID,post_title --format=csv | \
  while IFS=, read id title; do
    cats=$(wp post term list $id category --format=ids)
    if [ -z "$cats" ]; then
      echo "No category: $id - $title"
      wp post term add $id category "ELT Masterclass"
    fi
  done
```

### Problem: Posts Missing Tags
If the tag input in WordPress isn't saving, it's usually one of these:
1. **Plugin conflict** — disable plugins one by one (start with SEO plugins)
2. **Theme conflict** — switch to Twenty Twenty-Four temporarily
3. **JavaScript error** — check browser console (F12) for errors in the tag input
4. **REST API blocked** — your .htaccess might be blocking `/wp-json/` requests

Fix .htaccess REST API:
```apache
# Add to .htaccess BEFORE the WordPress rules:
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
</IfModule>
```

---

## Job Hunting Tools

| Tool | What it does | GitHub |
|------|-------------|--------|
| **JobFunnel** | Scrapes Indeed/LinkedIn/Glassdoor, outputs CSV | github.com/PaulMcInnis/JobFunnel |
| **job-spy** | Multi-site job scraper (Python) | github.com/Bunsly/JobSpy |
| **auto-apply** | Resume + cover letter automation | github.com/madpin/auto-apply |
| **LazyApply** | Browser extension, auto-fills job applications | lazyapply.com |

### JobSpy Quick Start
```bash
pip install python-jobspy
```
```python
from jobspy import scrape_jobs

jobs = scrape_jobs(
    site_name=['indeed', 'linkedin'],
    search_term='ELT teacher',
    location='Réunion',
    results_wanted=20,
)
print(jobs[['title', 'company', 'location', 'job_url']].to_string())
jobs.to_csv('jobs_found.csv', index=False)
```

---

## Productivity for Neurodivergent / Bipolar / Depression

### Task Management
| Tool | Why it helps | Link |
|------|-------------|------|
| **Super Productivity** | Time tracking, task manager, no distractions | super-productivity.com |
| **TaskWarrior** | Terminal-based, fast, keyboard-only | taskwarrior.org |
| **Habitica** | Turns habits into an RPG game (dopamine trick) | habitica.com |
| **Loop Habit Tracker** | Android habit tracking with streaks | github.com/iSoron/uhabits |
| **Planner for ADHD** | Specifically for attention/executive function | productivefish.com |

### Mood & Health Tracking
| Tool | What it does | Platform |
|------|-------------|----------|
| **eMoods** | Bipolar mood tracker, charts, export to PDF | Android/iOS |
| **Daylio** | Micro-journal + mood log | Android/iOS |
| **MoodPath** | Daily mental health check-in | Android/iOS |
| **Bearable** | Tracks mood, symptoms, meds together | bearable.app |
| **Medisafe** | Medication reminder, never miss a dose | medisafe.com |

### Focus Tools
| Tool | What it does |
|------|-------------|
| **Pomotroid** | Pomodoro timer, beautiful, open source |
| **Forest** | Plant a virtual tree while you focus (phone stays down) |
| **Cold Turkey** | Block distracting websites during work sessions |
| **Freedom** | Cross-device website/app blocking |

### Writing When Energy Is Low
- **Speechnotes** (speechnotes.co) — free browser speech-to-text, no login
- **Google Docs Voice Typing** — Tools → Voice typing (Ctrl+Shift+S)
- **oTranscribe** — transcribe audio to text
- **WhisperTranscribe** — local AI transcription (offline, private)

---

## GitHub Automation Tools Worth Knowing

| Repo | What it does |
|------|--------------|
| github.com/n8n-io/n8n | No-code automation (600+ integrations) |
| github.com/huginn/huginn | AI agents that run tasks for you |
| github.com/makeplane/plane | Open-source Jira/Linear alternative |
| github.com/nickvdyck/webbundlr | Package web apps |
| github.com/BerriAI/litellm | Unified API for all LLMs (switch providers instantly) |
| github.com/oobabooga/text-generation-webui | Run any LLM locally with a nice UI |
| github.com/AUTOMATIC1111/stable-diffusion-webui | Generate images locally |
| github.com/yt-dlp/yt-dlp | Download YouTube videos/audio for your content |
| github.com/mifi/lossless-cut | Fast video cutting without re-encoding |
| github.com/nicehash/NiceHashQuickMiner | (not relevant, listed only to avoid) |

---

## Recommended Minimal Stack for Your Use Case

Given your situation (writing, ELT, WordPress, low cognitive load needed):

1. **Write**: Logseq or plain `.md` files in a folder
2. **Automate**: Google Apps Script (no install, runs in browser)
3. **AI**: DeepSeek API for metadata ($0.18/year) or Mistral free tier
4. **Job search**: JobSpy → CSV → email yourself the results daily
5. **Health**: eMoods + Medisafe (non-negotiable)
6. **Focus**: Pomotroid (25-min sessions, 5-min rest)
7. **Version control**: GitHub with your current repo structure
