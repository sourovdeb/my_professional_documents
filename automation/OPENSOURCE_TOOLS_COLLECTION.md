# Open Source Tools Collection
## Best Tools for Content Automation, Bipolar-Friendly Productivity, and WordPress Management

---

## Category 1: WordPress Automation

### n8n — Visual No-Code Automation
- **GitHub:** github.com/n8n-io/n8n (50k+ stars)
- **What it does:** Visual workflow builder. Connect Google Sheets → WordPress with no code. Has a WordPress node built in.
- **Self-host:** `docker run -p 5678:5678 n8nio/n8n`
- **Best for:** Non-technical automation. Drag-drop interface.
- **Free:** Yes (self-hosted). Cloud has paid plans.

### WP-CLI — Terminal Control for WordPress
- **Site:** wp-cli.org
- **What it does:** Run any WordPress operation from the terminal or scripts.
- **Examples:**
  ```bash
  wp post create --post_title="My Post" --post_status=draft --post_content="$(cat myfile.html)"
  wp post list --post_status=draft
  wp term list category
  wp post term add 123 category "ELT Masterclass"
  ```
- **Best for:** SSH access automation. GitHub Actions pipelines.

### Huginn — Agent-Based Automation
- **GitHub:** github.com/huginn/huginn (40k+ stars)
- **What it does:** Create "agents" that watch RSS feeds, scrape sites, and trigger WordPress posts automatically.
- **Best for:** Job alert monitoring, auto-posting from external sources.

### Strapi — Headless CMS with WordPress Export
- **GitHub:** github.com/strapi/strapi
- **What it does:** Write in Strapi’s clean interface, export/sync to WordPress.
- **Best for:** If you prefer a cleaner writing interface than WordPress admin.

---

## Category 2: Writing & Markdown Tools

### Obsidian — Markdown Knowledge Base
- **Site:** obsidian.md
- **What it does:** Write in Markdown, link ideas like a wiki. Better than Logseq for most users.
- **Plugin:** "WordPress Publish" plugin available in community plugins
- **Free:** Yes (personal use)
- **Best for:** Daily writing that feeds your automation pipeline

### Logseq — Graph-Based Notes
- **GitHub:** github.com/logseq/logseq
- **What it does:** Block-based notes with bidirectional links
- **Free:** Yes (open source)
- **Export to WordPress:** Use folder watcher script (see `scripts/folder_watcher.js`)

### Typora — Clean Markdown Editor
- **Site:** typora.io
- **What it does:** WYSIWYG Markdown editing. Write in clean interface, save as .md
- **Price:** $15 one-time (not free but worth it)

### MarkText — Free Typora Alternative
- **GitHub:** github.com/marktext/marktext
- **What it does:** Same as Typora but free and open source
- **Best for:** Writing drafts that feed your folder watcher

---

## Category 3: Job Hunting Automation

### JobFunnel — Automated Job Scraper
- **GitHub:** github.com/PaulMcInnis/JobFunnel
- **What it does:** Scrapes Indeed, Monster, LinkedIn and saves to a spreadsheet. Filters duplicates.
- **Install:** `pip install jobfunnel`
- **Config:** YAML file with search terms, locations, filters

### JobSpy — Multi-Site Job Search
- **GitHub:** github.com/Bunsly/JobSpy
- **What it does:** Search Indeed, LinkedIn, Glassdoor via Python
- **Install:** `pip install python-jobspy`
- **Example:**
  ```python
  from jobspy import scrape_jobs
  jobs = scrape_jobs(
    site_name=['indeed', 'linkedin'],
    search_term='English teacher',
    location='Reunion Island',
    results_wanted=20
  )
  print(jobs[['title','company','location','job_url']])
  ```

### LinkedIn Job Alerts (No scraping needed)
- Set up email alerts in LinkedIn for your search terms
- Forward those emails to a Gmail label
- Use the Gmail API or Google Apps Script to parse and summarise daily

---

## Category 4: Audio, Video, and Banner Creation

### Audio Tools

| Tool | Purpose | Free? | Link |
|------|---------|-------|------|
| **Audacity** | Record and edit audio, podcast production | Yes | audacityteam.org |
| **Whisper (OpenAI)** | Speech-to-text, transcribe audio to text | Yes | github.com/openai/whisper |
| **ElevenLabs** | Text-to-speech for blog post audio versions | Free tier | elevenlabs.io |
| **Descript** | Record, transcribe, edit audio/video together | Free tier | descript.com |
| **Otter.ai** | Transcribe meetings and voice notes | Free tier | otter.ai |

**Most useful for you:** Whisper + Audacity
- Record a voice note when writing is hard
- Whisper transcribes it automatically
- Result goes into your Google Sheet as content
- System publishes it

```bash
# Whisper usage:
pip install openai-whisper
whisper myrecording.mp3 --language English --output_format txt
```

### Video Tools

| Tool | Purpose | Free? |
|------|---------|-------|
| **OBS Studio** | Screen recording, video capture | Yes |
| **Kdenlive** | Video editing (Linux/Windows/Mac) | Yes |
| **DaVinci Resolve** | Professional video editing | Free version |
| **HandBrake** | Convert and compress video | Yes |
| **yt-dlp** | Download YouTube/other videos for reference | Yes |

### Banner & Image Tools

| Tool | Purpose | Free? |
|------|---------|-------|
| **GIMP** | Full image editing (Photoshop alternative) | Yes |
| **Inkscape** | Vector graphics, blog banner design | Yes |
| **Canva** | Drag-drop templates for banners, social posts | Free tier |
| **Stable Diffusion** | AI image generation (local) | Yes (needs GPU) |
| **DALL-E 3** | AI images via API | Paid |
| **Unsplash** | Free stock photos | Yes |
| **Pexels** | Free stock photos and video | Yes |

**Recommended banner workflow:**
1. Design a base template in Canva (free)
2. Export as PNG
3. Use Python + Pillow to auto-generate variations:

```python
from PIL import Image, ImageDraw, ImageFont

def make_banner(title: str, output_path: str):
    img = Image.open('banner_template.png')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('DejaVuSans-Bold.ttf', 36)
    draw.text((60, 200), title, fill='white', font=font)
    img.save(output_path)
```

---

## Category 5: Productivity Tools for Bipolar & Depression

### Mood & Habit Tracking

| Tool | Purpose | Platform | Free? |
|------|---------|----------|-------|
| **eMoods** | Bipolar mood tracker, medication log | Mobile | Free |
| **Daylio** | Micro journal + mood log | Mobile | Free |
| **Bearable** | Symptom + mood + medication tracking | Mobile | Free tier |
| **Moodpath** | Depression and anxiety screening | Mobile | Free |
| **Loop Habit Tracker** | Habit streaks, no zero days | Android | Free |

### Automation for Low-Energy Days

| Tool | What it saves | How |
|------|--------------|-----|
| **Todoist** | Decision fatigue | Template tasks, recurring items |
| **Notion** | Writing templates | Pre-built post templates |
| **Beeper / Signal** | Communication spoons | Batch replies once/day |
| **Google Calendar** | Energy scheduling | Block "writing time" 9-10 AM daily |
| **f.lux / Night Light** | Sleep regulation | Auto-dim screen after 8 PM |

### Writing When Energy Is Low

- **Google Docs voice typing** (Tools → Voice Typing) — speak your post
- **MarkText + folder watcher** — type, save, system does the rest
- **Telegram to WordPress** — send a Telegram message, bot posts to WordPress draft

### Telegram Bot for Zero-Effort Posting

```python
# Run this on a server or Raspberry Pi
# Send any Telegram message to the bot → it becomes a WordPress draft

import telebot, requests, os

bot = telebot.TeleBot(os.environ['TELEGRAM_TOKEN'])

@bot.message_handler(func=lambda m: True)
def handle_message(msg):
    lines  = msg.text.strip().split('\n', 1)
    title  = lines[0]
    body   = lines[1] if len(lines) > 1 else ''

    result = requests.post(
        'https://sourovdeb.com/wp-json/sourov/v1/ai-post',
        headers={'X-Sourov-Key': os.environ['WP_KEY']},
        json={'title': title, 'content': f'<p>{body}</p>', 'status': 'draft'},
        timeout=15
    )
    bot.reply_to(msg, f'Saved as draft! ID: {result.json().get("post_id")}')

bot.polling()
```

---

## Category 6: Health Information Resources

### Bipolar Disorder
- **NIMH:** nimh.nih.gov/health/topics/bipolar-disorder
- **IBPF:** ibpf.org (International Bipolar Foundation)
- **Bphope:** bphope.com (community + articles)
- **PubMed:** pubmed.ncbi.nlm.nih.gov (search your medication name for clinical data)

### Depression
- **WHO:** who.int/news-room/fact-sheets/detail/depression
- **Mind UK:** mind.org.uk
- **NAMI:** nami.org

### Sleep (critical for bipolar management)
- **CBT-I Coach** — free app, evidence-based sleep therapy
- **Sleepio** — digital CBT for insomnia

### Medication Management Apps
- **Medisafe** — medication reminder and interaction checker
- **MyTherapy** — medication + mood + health tracking

---

## Quick Reference: "What Do I Install First?"

**Day 1 (30 minutes):**
1. Install Ollama + pull Mistral model
2. Set up Google Sheet with Queue tab
3. Paste the Apps Script (from CSV tutorial)
4. Add one row and test

**Day 2 (20 minutes):**
5. Install MarkText or Obsidian
6. Create your `~/wordpress_queue/` folder
7. Run `auto_publisher.py` from `scripts/`

**Day 3 (10 minutes):**
8. Install Daylio or eMoods on phone
9. Set up Telegram bot for zero-effort drafts

**Ongoing:**
- Write daily 9–10 AM (protected time)
- Check WordPress drafts 3×/week
- Review published count on Fridays
