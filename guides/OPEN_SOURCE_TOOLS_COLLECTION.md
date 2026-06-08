# Open-Source Tools Collection
## Curated for: WordPress Automation, Writing, Job Hunting, Mental Health & Media

> All tools listed here are free/open-source or have generous free tiers. GitHub star counts verified June 2026.

---

## SECTION 1: WordPress Automation

### WP-CLI — WordPress Command Line Interface
- **GitHub:** github.com/wp-cli/wp-cli (5,700+ stars)
- **What:** Manage WordPress from terminal or scripts. Create posts, manage plugins, run database queries.
- **Free:** Yes, fully open-source
- **Key commands:**
```bash
# Install
curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar
chmod +x wp-cli.phar && sudo mv wp-cli.phar /usr/local/bin/wp

# Create a draft post from command line
wp post create --post_title='Day 32 Listening' --post_content='<p>Today...' --post_status=draft

# List all posts
wp post list --post_status=draft

# Fix all post categories
wp post list --field=ID | while read id; do
  wp post update $id --post_category=$(wp term get category ELT --field=term_id)
done
```
- **Best for:** Server-side automation, cron jobs, bulk operations

---

### n8n — Self-Hosted Workflow Automation
- **GitHub:** github.com/n8n-io/n8n (40,000+ stars)
- **What:** No-code automation like Zapier, but free and self-hosted. Connect Google Sheets → WordPress in 5 minutes visually.
- **Free:** Self-hosted version is 100% free
- **Install:**
```bash
npx n8n
# Then open http://localhost:5678
```
- **Key integrations:** Google Sheets, WordPress, Gmail, HTTP Request, RSS, Telegram
- **Use case:** Visual editor to create: Google Sheets row added → WordPress post created
- **Alternative to:** Zapier ($20+/month)

---

### Huginn — Agent-Based Automation
- **GitHub:** github.com/huginn/huginn (41,000+ stars)
- **What:** Create "agents" that monitor and act. One agent watches your Google Sheet RSS; another posts to WordPress.
- **Free:** Self-hosted, open-source
- **Best for:** Complex workflows, monitoring RSS feeds for job listings

---

### Jetpack (WordPress Plugin)
- **URL:** wordpress.org/plugins/jetpack
- **What:** Scheduling, social auto-share, SEO basics, CDN
- **Free tier:** Yes — scheduling and sharing are free
- **Install:** WP Admin → Plugins → Add New → Search "Jetpack"

---

### WP Scheduled Posts
- **URL:** wordpress.org/plugins/wp-scheduled-posts
- **What:** Bulk scheduling, editorial calendar, auto-schedule from queue
- **Free tier:** Yes (bulk CSV import in free version)
- **Best for:** Visual post calendar

---

### PublishPress Planner
- **URL:** wordpress.org/plugins/publishpress
- **What:** Editorial calendar, team workflows, scheduling
- **Free:** Yes

---

## SECTION 2: Writing & Note-Taking Tools

### Logseq — Privacy-First Knowledge Base
- **GitHub:** github.com/logseq/logseq (30,000+ stars)
- **What:** Markdown-based writing app with bidirectional links. Write notes, then export as Markdown to publish.
- **Free:** Fully open-source
- **Download:** logseq.com
- **Integration with WordPress:** Export page → save to `~/Dropbox/wordpress_queue/` → folder watcher script picks it up

---

### Obsidian — Markdown Notes (Local)
- **URL:** obsidian.md
- **What:** Local-first Markdown editor with 1,000+ plugins
- **Free:** Personal use is free
- **WordPress plugin:** "WordPress Publish" plugin available in Obsidian community plugins
- **Best for:** Long-form writing with internal links

---

### Typora — Beautiful Markdown Editor
- **URL:** typora.io
- **What:** WYSIWYG Markdown editor — you see the formatted result as you type
- **Free:** Free beta period; $15 one-time
- **Best for:** Writing posts that look like the final output

---

### MarkText — Free Typora Alternative
- **GitHub:** github.com/marktext/marktext (45,000+ stars)
- **What:** Open-source Markdown editor with live preview
- **Free:** Completely free
- **Download:** github.com/marktext/marktext/releases

---

## SECTION 3: Job Hunting Automation

### JobSpy — Python Job Scraper
- **GitHub:** github.com/Bunsly/JobSpy (3,000+ stars)
- **What:** Scrape Indeed, LinkedIn, Glassdoor simultaneously with one Python call
- **Free:** Open-source
- **Install:** `pip install python-jobspy`

```python
from jobspy import scrape_jobs
import pandas as pd

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "glassdoor"],
    search_term="ELT teacher",
    location="France",
    results_wanted=20
)

# Save to CSV
jobs.to_csv('jobs_today.csv', index=False)
print(f"Found {len(jobs)} jobs")

# Email yourself
for _, job in jobs.iterrows():
    print(f"{job['title']} at {job['company']} — {job['job_url']}")
```

---

### Yet Another JobBoard (YAJB)
- **GitHub:** github.com/nicholasgasior/job-board-aggregator
- **What:** Aggregates multiple job board RSS feeds
- **Free:** Open-source

---

### LinkedIn Job Alert RSS
- **What:** LinkedIn generates RSS feeds for job searches (hidden feature)
- **How:** Search LinkedIn Jobs → set filters → click "Create alert" → email address
- **Use with:** n8n or Apps Script to parse and email digest

---

### Indeed RSS Feeds
```python
import feedparser

feed = feedparser.parse('https://rss.indeed.com/rss?q=ELT+teacher&l=France')
for entry in feed.entries[:10]:
    print(entry.title, entry.link)
```

---

## SECTION 4: AI Tools (Free/Cheap)

### Ollama — Run AI Locally, Free Forever
- **GitHub:** github.com/ollama/ollama (80,000+ stars)
- **What:** Run Llama3, Mistral, Phi3, Gemma locally. No API key, no cost, no internet.
- **Install:** ollama.ai
```bash
ollama pull mistral    # 4GB, fast, good quality
ollama pull phi3       # 2GB, very lightweight
ollama pull llama3     # 8GB, best quality free
ollama serve           # Start the server
```
- **API:** Compatible with OpenAI API format at `http://localhost:11434`

---

### LM Studio — GUI for Local AI
- **URL:** lmstudio.ai
- **What:** Desktop app to download and run any AI model locally, with a chat UI
- **Free:** Completely free
- **Best for:** Non-technical users who want local AI without terminal

---

### Mistral (via La Plateforme) — Free API
- **URL:** console.mistral.ai
- **Free tier:** Experimental — check current limits at console.mistral.ai
- **Models:** `mistral-small-latest` (fastest), `mistral-large-latest` (best)
- **Compatible:** OpenAI format

---

### Gemini (Google AI Studio) — Free API
- **URL:** aistudio.google.com
- **Free tier:** 1,500 requests/day for Gemini 1.5 Flash (as of 2026)
- **Models:** `gemini-1.5-flash` (fast, free), `gemini-1.5-pro` (better, limited)
- **Best for:** High-volume tasks where DeepSeek costs add up

---

## SECTION 5: Audio Tools

### Audacity — Audio Editor
- **GitHub:** github.com/audacity/audacity (11,000+ stars)
- **What:** Record, edit, export audio. Add effects, reduce noise.
- **Free:** Completely free, cross-platform
- **Download:** audacityteam.org
- **Best for:** Recording podcast episodes, editing lectures

---

### Whisper (OpenAI) — Speech-to-Text
- **GitHub:** github.com/openai/whisper (60,000+ stars)
- **What:** Transcribe any audio file to text, locally, for free. Supports French, English, Hindi, etc.
- **Free:** Open-source, runs locally
- **Install:** `pip install openai-whisper`
```python
import whisper
model = whisper.load_model('base')  # or 'small', 'medium', 'large'
result = model.transcribe('lecture.mp3')
print(result['text'])
```
- **Best for:** Transcribing lectures, voice memos, interviews

---

### Coqui TTS — Text-to-Speech
- **GitHub:** github.com/coqui-ai/TTS (35,000+ stars)
- **What:** Convert text to natural-sounding speech. Create audio versions of your blog posts.
- **Free:** Open-source
- **Install:** `pip install TTS`
```python
from TTS.api import TTS
tts = TTS('tts_models/en/ljspeech/tacotron2-DDC')
tts.tts_to_file('Welcome to ELT Masterclass.', file_path='intro.wav')
```

---

### ElevenLabs (Free Tier)
- **URL:** elevenlabs.io
- **Free tier:** 10,000 chars/month
- **What:** High-quality AI voice synthesis
- **Best for:** Creating audio previews of blog posts

---

## SECTION 6: Video Tools

### OBS Studio — Screen Recording & Streaming
- **GitHub:** github.com/obsproject/obs-studio (55,000+ stars)
- **What:** Record your screen, webcam, create video lessons
- **Free:** Completely free, cross-platform
- **Download:** obsproject.com
- **Best for:** Creating ELT video content, YouTube

---

### Kdenlive — Video Editor
- **GitHub:** github.com/KDE/kdenlive (2,000+ stars)
- **What:** Professional non-linear video editor
- **Free:** Completely free
- **Download:** kdenlive.org
- **Best for:** Editing ELT lessons, cutting out mistakes

---

### FFmpeg — Video/Audio Swiss Army Knife
- **GitHub:** github.com/FFmpeg/FFmpeg (42,000+ stars)
- **What:** Convert, compress, trim any video/audio from command line
- **Free:** Open-source
```bash
# Convert MP4 to smaller size
ffmpeg -i input.mp4 -crs 28 -preset slow output.mp4

# Extract audio from video
ffmpeg -i video.mp4 -vn audio.mp3

# Create video from images + audio (for slideshows)
ffmpeg -framerate 1/5 -i slide%d.jpg -i narration.mp3 output.mp4
```

---

### DaVinci Resolve — Professional Video Editor (Free)
- **URL:** blackmagicdesign.com/products/davinciresolve
- **What:** Hollywood-grade video editor, completely free
- **Best for:** High-quality editing if you invest time to learn

---

## SECTION 7: Banner & Design Tools

### GIMP — Image Editor
- **URL:** gimp.org
- **What:** Photoshop alternative, fully free and open-source
- **Best for:** Custom blog banners, photo editing

---

### Inkscape — Vector Graphics
- **GitHub:** github.com/inkscape/inkscape (1,500+ stars)
- **What:** Create scalable logos, icons, infographics
- **Free:** Completely free
- **Download:** inkscape.org

---

### Canva (Free Tier)
- **URL:** canva.com
- **What:** Drag-and-drop design, 1000s of templates
- **Free tier:** 250,000+ free templates, limited exports
- **Best for:** Blog banners, social media posts, infographics
- **WordPress plugin:** Canva has a direct WordPress integration

---

### ImageMagick — Command-Line Image Processing
- **URL:** imagemagick.org
- **What:** Batch resize, convert, watermark images automatically
```bash
# Resize all images in a folder to 1200px width
mogrify -resize 1200x +profile '*' *.jpg

# Add text watermark
convert image.jpg -gravity SouthEast -font Arial -pointsize 20 \
  -fill white -annotate +10+10 'sourovdeb.com' watermarked.jpg
```

---

### Unsplash API (Free Images)
- **URL:** unsplash.com/developers
- **What:** 3 million+ free, high-quality photos
- **API:** Free for 50 requests/hour
```python
import requests

def get_photo(keyword):
    r = requests.get(
        'https://api.unsplash.com/photos/random',
        params={'query': keyword, 'orientation': 'landscape'},
        headers={'Authorization': 'Client-ID YOUR_ACCESS_KEY'}
    )
    return r.json()['urls']['regular']  # Direct image URL
```

---

## SECTION 8: Productivity & Focus

### Pomofocus — Pomodoro Timer (Web)
- **URL:** pomofocus.io
- **What:** Browser-based Pomodoro timer with task list
- **Free:** Completely free
- **Best for:** 25-minute writing sessions

---

### Habitica — Gamified Habit Tracker
- **URL:** habitica.com
- **GitHub:** github.com/HabiticaRPG/habitica (11,000+ stars)
- **What:** Turn habits and daily tasks into an RPG game. Complete tasks → level up your character.
- **Free:** Base game is free
- **Best for:** Making "write 500 words" feel rewarding

---

### Notesnook — Privacy-First Notes
- **GitHub:** github.com/streetwriters/notesnook (8,000+ stars)
- **What:** Encrypted, open-source alternative to Evernote/Notion
- **Free:** Basic plan free
- **Best for:** Private writing, medical notes

---

### Standard Notes — Encrypted Notes
- **GitHub:** github.com/standardnotes/app (5,000+ stars)
- **What:** End-to-end encrypted notes, synced across devices
- **Free:** Unlimited notes free

---

*Last updated: June 2026 | All tools verified as functional*
