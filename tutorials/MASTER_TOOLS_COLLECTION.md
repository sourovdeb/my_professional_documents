# Master Open-Source Tools Collection

**The best free and open-source tools for WordPress automation, writing, productivity, audio, video, and mental health management.**  
**Curated for Sourov Deb — updated June 2026**

---

## 1. WordPress Automation

| Tool | GitHub | Stars | What It Does |
|------|--------|-------|-------------|
| **n8n** | github.com/n8n-io/n8n | 190k+ | Visual workflow automation — connect Google Sheets to WordPress without code |
| **wp-cli** | github.com/wp-cli/wp-cli | 5k+ | Command-line WordPress management — create posts with one terminal command |
| **Huginn** | github.com/huginn/huginn | 43k+ | Self-hosted automation agents — monitor, scrape, and trigger actions |
| **n8n Templates** | github.com/enescingoz/awesome-n8n-templates | 22k+ | 280+ ready-made automation workflows for Gmail, WP, Telegram, Drive |

**wp-cli quickstart (if you have SSH to your server):**
```bash
# Create a draft post from the terminal
wp post create --post_title="Day 33" --post_content="<p>Content here</p>" --post_status=draft

# Publish all drafts
wp post list --post_status=draft --format=ids | xargs wp post update --post_status=publish

# Fix all post categories in bulk
wp post list --format=ids | xargs -I {} wp post term set {} category "ELT Masterclass"
```

**n8n Google Sheets → WordPress (No-Code Setup):**
```
1. Install n8n (docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n)
2. Create a new workflow
3. Add node: Google Sheets (Trigger — On Row Added)
4. Add node: HTTP Request (POST to your WordPress API)
5. Map columns from Sheets to API fields
6. Activate — every new row in Sheets triggers a WordPress post
```

---

## 2. Content Writing and AI Tools

| Tool | Type | Free? | Best For |
|------|------|-------|----------|
| **claude.ai** | Web | Yes (limited) | Best writing quality |
| **chat.mistral.ai** | Web | Yes (unlimited) | Quick drafts, French |
| **Ollama** | Local | Yes (fully) | Offline AI, no cost |
| **Open WebUI** | Web UI | Yes | Browser interface for Ollama |
| **LM Studio** | Desktop | Yes | Easy local AI with GUI |
| **Obsidian** | Desktop | Yes | Writing + linked notes |
| **Logseq** | Desktop/Web | Yes (open-source) | Daily notes + publish export |
| **Zettlr** | Desktop | Yes | Academic + long-form writing |

**Ollama GitHub:** github.com/ollama/ollama  
**Open WebUI GitHub:** github.com/open-webui/open-webui  
**LM Studio:** lmstudio.ai

**Install Open WebUI (browser interface for all local AI models):**
```bash
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway \
  -v open-webui:/app/backend/data \
  --name open-webui ghcr.io/open-webui/open-webui:main
# Then open: http://localhost:3000
```

---

## 3. Scheduling and Productivity

| Tool | Type | Best For |
|------|------|----------|
| **Logseq** | Desktop notes | Daily journal + writing + task tracking |
| **Obsidian** | Desktop notes | Long-form writing, linked notes |
| **Notion** (free tier) | Web | Project management, templates |
| **Trello** (free tier) | Web | Kanban board for content calendar |
| **Thunderbird** | Desktop | Email management (free, open-source) |
| **calcurse** | Terminal | Calendar and tasks in terminal |

**Content Calendar in Trello (free):**
```
1. Create a Trello board called "Content Calendar"
2. Columns: Ideas | Writing | Ready | Published
3. Create a card for each post idea
4. Move cards across columns as you work
5. Set due dates for scheduled posts
```

---

## 4. Audio and Podcast Tools

| Tool | GitHub | What It Does |
|------|--------|-------------|
| **OpenAI Whisper** | github.com/openai/whisper | Voice-to-text transcription (70k+ stars) |
| **Whisper.cpp** | github.com/ggerganov/whisper.cpp | Fast Whisper on CPU |
| **Coqui TTS** | github.com/coqui-ai/TTS | Text-to-speech, 35k+ stars |
| **Bark** | github.com/suno-ai/bark | High-quality emotive TTS |
| **Piper TTS** | github.com/rhasspy/piper | Lightweight TTS for CPU |
| **ffmpeg** | github.com/FFmpeg/FFmpeg | Audio/video processing Swiss knife |
| **Audacity** | github.com/audacity/audacity | Desktop audio editor |

---

## 5. Video and Screen Recording

| Tool | GitHub | What It Does |
|------|--------|-------------|
| **OBS Studio** | github.com/obsproject/obs-studio | Screen recording + streaming (60k+ stars) |
| **Kdenlive** | invent.kde.org/multimedia/kdenlive | Professional video editor |
| **OpenShot** | github.com/OpenShot/openshot-qt | Simple video editor |
| **Shotcut** | github.com/mltframework/shotcut | Cross-platform video editor |
| **HandBrake** | github.com/HandBrake/HandBrake | Video compression |
| **ffmpeg** | github.com/FFmpeg/FFmpeg | Command-line video processing |
| **yt-dlp** | github.com/yt-dlp/yt-dlp | Download audio/video from many sites |

---

## 6. Graphics and Banner Design

| Tool | Type | What It Does |
|------|------|-------------|
| **GIMP** | Desktop | Full image editor (Photoshop alternative) |
| **Inkscape** | Desktop | Vector graphics (Illustrator alternative) |
| **Krita** | Desktop | Digital painting and illustration |
| **Penpot** | Web | Open-source Figma alternative |
| **Canva** | Web | Templates (free tier, highly recommended) |
| **Photopea** | Browser | Photoshop in the browser |
| **AUTOMATIC1111** | Local | Stable Diffusion AI image generation |
| **ComfyUI** | Local | Node-based AI image generation |

**Penpot GitHub:** github.com/penpot/penpot  
**AUTOMATIC1111 GitHub:** github.com/AUTOMATIC1111/stable-diffusion-webui

---

## 7. Job Hunting Automation

| Tool | What It Does |
|------|--------------|
| **Indeed MCP** (in this system) | Search jobs via API |
| **praw** (Python Reddit API) | Monitor job posts on r/TEFL, r/ELTteachers |
| **feedparser** (Python) | Read RSS feeds from job boards |
| **Beautiful Soup** (Python) | Parse job listings from websites |
| **IFTTT** | Email alert when new jobs match keywords |

**Monitor r/TEFL for job postings (Python):**
```python
import praw

reddit = praw.Reddit(client_id='YOUR_ID', client_secret='YOUR_SECRET', user_agent='jobbot')
for post in reddit.subreddit('TEFL').new(limit=20):
    if any(kw in post.title.lower() for kw in ['hiring', 'job', 'position', 'vacancy']):
        print(post.title, post.url)
```

**Monitor job boards via RSS:**
```python
import feedparser

# Indeed RSS (no API key needed)
feed = feedparser.parse('https://rss.indeed.com/rss?q=ELT+teacher&l=Reunion')
for entry in feed.entries[:5]:
    print(entry.title)
    print(entry.link)
```

---

## 8. Health, Mood Tracking, and Mental Wellness

### Apps (Mobile)

| App | Platform | Best For |
|-----|----------|----------|
| **eMoods** | iOS/Android | Bipolar mood and medication logging |
| **Daylio** | iOS/Android | Daily mood + activity journal |
| **Bearable** | iOS/Android | Symptoms, mood, medication tracking |
| **Insight Timer** | iOS/Android | Meditation (free library of 100k+ sessions) |
| **Finch** | iOS/Android | Self-care goals gamified |

### Apps (Desktop / Self-Hosted)

| Tool | Type | What It Does |
|------|------|-------------|
| **Logseq Journal** | Desktop | Daily notes for mood, tasks, reflections |
| **HedgeDoc** | Self-hosted | Collaborative markdown notes |
| **Outline** | Self-hosted | Knowledge base and personal wiki |

### Automate Mood Logging with Google Forms
```
1. Create a Google Form: "Daily Check-In"
   - Question 1: Mood (1–10 scale)
   - Question 2: Energy (1–10 scale)
   - Question 3: Sleep (hours)
   - Question 4: Notes (short text)
2. Link the form to a Google Sheet (automatic)
3. Add Apps Script: email yourself a weekly summary
4. Optionally: chart your mood over time in the Sheet
```

### Trusted Health Information Sources

| Condition | Source | URL |
|-----------|--------|-----|
| Bipolar disorder | NIMH | nimh.nih.gov |
| Bipolar disorder | International Bipolar Foundation | ibpf.org |
| Depression | WHO | who.int/mental-health |
| Medication info | PubMed | pubmed.ncbi.nlm.nih.gov |
| Self-management | DBSA (Depression Bipolar Support Alliance) | dbsalliance.org |

---

## 9. GitHub Automation

| Tool | What It Does |
|------|--------------|
| **GitHub Actions** | Run scripts automatically on push or schedule |
| **act** (local Actions) | Run GitHub Actions on your computer for testing |
| **pre-commit** | Run code checks before every git commit |
| **ghorg** | Clone entire GitHub organizations |

**GitHub Action templates in this repo:**
- `.github/workflows/publish_on_push.yml` — publish drafts when pushed

---

## 10. Quick Reference: Tool by Use Case

| I want to... | Use this |
|-------------|----------|
| Publish posts automatically from a spreadsheet | Google Apps Script (see tutorial) |
| Generate posts with AI for free | Le Chat at chat.mistral.ai |
| Run AI completely offline | Ollama + Open WebUI |
| Record my voice and transcribe it | OBS Studio + OpenAI Whisper |
| Create a blog banner | Canva (free) |
| Edit a video | Kdenlive or OpenShot |
| Search for ELT jobs automatically | Indeed MCP + praw |
| Track my mood and energy | eMoods or Daylio |
| Bulk-fix WordPress categories and tags | See automation/wordpress-category-tag-fixer.php |
| Publish from GitHub automatically | See .github/workflows/publish_on_push.yml |

---

*Curated by Sourov Deb · June 2026 · github.com/sourovdeb/my_professional_documents*
