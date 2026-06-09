# Complete Tools Collection
## Everything You Need — Free & Open Source

---

## WordPress Automation Tools

### Must-Have Plugins

| Plugin | What it does | Cost |
|---|---|---|
| **WP Scheduled Posts** | Bulk schedule from CSV import | Free |
| **PublishPress** | Editorial calendar + scheduling | Free tier |
| **Yoast SEO** | Auto SEO fields, meta, sitemaps | Free |
| **Jetpack** | Social auto-share, scheduling, stats | Free |
| **WP-CLI** | Terminal control of WordPress | Free |
| **REST API** | Built into WP — powers all scripts here | Free (built-in) |

### No-Code Automation (Self-Hosted)

| Tool | What it does | Install |
|---|---|---|
| **n8n** | Visual workflow builder — connects Sheets→WP | `docker run n8n` |
| **Huginn** | Agent-based automation (like IFTTT, self-hosted) | GitHub: huginn/huginn |
| **Activepieces** | n8n alternative, very easy UI | activepieces.com |
| **Windmill** | Scripts + workflows + scheduler | windmill.dev |

### No-Code Automation (Cloud Free Tier)

| Tool | Free limit | Good for |
|---|---|---|
| **Zapier** | 100 tasks/month | Sheet → WP trigger |
| **Make (Integromat)** | 1,000 ops/month | Complex workflows |
| **IFTTT** | 5 applets | Simple webhooks |
| **Pabbly Connect** | Unlimited (lifetime deal) | Best free option |

---

## Audio Tools (Free & Open Source)

| Tool | Platform | Best For |
|---|---|---|
| **Audacity** | Win/Mac/Linux | Podcast recording, noise removal, editing |
| **Tenacity** | Win/Mac/Linux | Audacity fork (privacy-focused) |
| **Ocenaudio** | Win/Mac/Linux | Quick editing, spectral view |
| **Ardour** | Mac/Linux | Professional DAW, multi-track |
| **Reaper** | Win/Mac/Linux | $60 (60-day free trial, very fair) |
| **LMMS** | Win/Mac/Linux | Music production |
| **VLC** | All | Convert audio formats |
| **FFmpeg** | CLI | Batch convert, trim, extract audio from video |

### Audio for Content Creators

```bash
# Convert MP3 to WAV (for Audacity)
ffmpeg -i input.mp3 output.wav

# Extract audio from video
ffmpeg -i video.mp4 -vn -q:a 0 audio.mp3

# Noise reduction (Audacity: Effect → Noise Reduction)
# 1. Select a quiet section → Get Noise Profile
# 2. Select all → Apply Noise Reduction
```

**Text-to-Speech (for when energy is low):**
- **Kokoro TTS** (free, local): `pip install kokoro-onnx`
- **Coqui TTS** (open source): github.com/coqui-ai/TTS
- **Edge TTS** (free Microsoft voices): `pip install edge-tts`
- **Balabolka** (Windows, free): reads any text aloud

---

## Video Tools (Free & Open Source)

| Tool | Platform | Best For |
|---|---|---|
| **OBS Studio** | Win/Mac/Linux | Screen recording, live streaming |
| **Kdenlive** | Win/Mac/Linux | Full video editor, timeline-based |
| **Shotcut** | Win/Mac/Linux | Easy video editor, no install needed |
| **OpenShot** | Win/Mac/Linux | Beginner-friendly editor |
| **DaVinci Resolve (Free)** | Win/Mac/Linux | Professional colour grading |
| **HandBrake** | Win/Mac/Linux | Video compression/conversion |
| **VLC** | All | Playback + format conversion |
| **FFmpeg** | CLI | Batch processing, trimming, scaling |

### Quick Video Workflows

```bash
# Record screen on Linux (OBS alternative)
ffmpeg -video_size 1920x1080 -framerate 25 -f x11grab -i :0.0 output.mp4

# Add logo watermark to video
ffmpeg -i input.mp4 -i logo.png -filter_complex "overlay=10:10" output.mp4

# Create slideshow from images
ffmpeg -framerate 1/3 -pattern_type glob -i '*.jpg' -c:v libx264 slideshow.mp4

# Compress for web
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output_small.mp4
```

---

## Banner & Graphics Tools (Free)

| Tool | Type | Best For |
|---|---|---|
| **Canva** (free tier) | Web | Blog banners, social media, professional templates |
| **GIMP** | Desktop | Photo editing, complex composites |
| **Inkscape** | Desktop | Vector graphics, logos, scalable banners |
| **Krita** | Desktop | Digital illustration, painting |
| **Pixlr E/X** | Web | Quick Photoshop-like editing |
| **Photopea** | Web | Full Photoshop alternative, free |
| **Remove.bg** | Web | Remove image backgrounds |
| **Unsplash** | Web | Free high-res photos (no attribution needed) |
| **Pexels** | Web | Free photos and videos |
| **Flaticon** | Web | Free icons (attribution required on free plan) |
| **Freepik** | Web | Free vectors and templates |

### Automated Banner Generation (Python)

```python
# pip install Pillow
from PIL import Image, ImageDraw, ImageFont

def create_blog_banner(title: str, output: str = 'banner.png'):
    img = Image.new('RGB', (1200, 630), color=(30, 30, 60))
    draw = ImageDraw.Draw(img)
    # Add gradient effect
    for y in range(630):
        r = int(30 + (y/630)*40)
        draw.line([(0,y),(1200,y)], fill=(r, r, 80))
    # Add text (use a TTF font file if available)
    draw.text((60, 240), title, fill='white', font_size=48)
    draw.text((60, 540), 'sourovdeb.com', fill=(150,150,200), font_size=24)
    img.save(output)
    return output
```

---

## Writing & Productivity Tools

| Tool | Type | Why It's Good for You |
|---|---|---|
| **Obsidian** | Desktop | Local markdown notes, no internet needed |
| **Logseq** | Desktop/Web | Daily notes, outliner, graph view |
| **Joplin** | Desktop/Mobile | Encrypted notes, sync with Nextcloud |
| **Standard Notes** | All | Encrypted, focused, distraction-free |
| **Focuswriter** | Desktop | Full-screen distraction-free writing |
| **MarkText** | Desktop | Clean markdown editor |
| **Typora** | Desktop | Beautiful markdown with live preview |

---

## Mental Health & Productivity Tools for Bipolar/Depression

### Mood Tracking

| Tool | Platform | Features |
|---|---|---|
| **eMoods** | iOS/Android | Track mood, sleep, medications daily |
| **Bearable** | iOS/Android | Highly customizable symptom tracking |
| **Daylio** | iOS/Android | Micro-diary, mood + activity correlation |
| **Mood Path** | iOS/Android | CBT-based, tracks over 2 weeks |
| **How We Feel** | iOS/Android | Created by Yale researchers, free |

### Productivity for Low-Energy Days

| Tool | What it does |
|---|---|
| **Forest** | Gamified focus timer (plant a tree) |
| **Toggl Track** | Simple time tracking, no pressure |
| **Habitica** | Turns habits into a game |
| **Focusmate** | Virtual co-working, accountability |
| **Brain.fm** | Focus music backed by neuroscience |

### Automation to Reduce Cognitive Load

- **Text expander** (Espanso, free): type `;blog` → expands to your blog post template
- **Voice typing**: Google Docs has built-in voice typing (Tools → Voice Typing)
- **Templates**: Create one `.md` template per post type; never start from blank page
- **Time blocking**: Use Google Calendar blocks for writing (9-9:30 AM daily)
- **Pre-written subject lines**: Keep a list of 20 titles ready; pick one, fill it in

### GitHub Repos for Mental Health + Automation

- **awesome-bipolar**: github.com — search "awesome bipolar" for curated resources
- **pomodoro-cli**: `pip install pomodoro` — terminal timer
- **espanso**: espanso.org — text expansion, reduces typing effort
- **autokey** (Linux): Automate repetitive text tasks
- **activity-watch**: activitywatch.net — track your own computer usage

---

## Job Hunting Tools

| Tool | What it does | Type |
|---|---|---|
| **JobSpy** | Scrapes Indeed, LinkedIn, Glassdoor | Python: `pip install python-jobspy` |
| **linkedin-jobs-scraper** | Node.js LinkedIn job scraper | npm package |
| **Indeed RSS** | Free job alerts via RSS | URL: rss.indeed.com/rss?q=ELT&l=Location |
| **Huntr** | Track job applications visually | Web (free) |
| **Simplify** | Auto-fill job applications | Browser extension |
| **OpenResume** | Free ATS-friendly resume builder | resume.openresume.ai |
| **Resumake** | Open-source resume builder | latexresu.me |

---

## Free Hosting & Deployment

| Service | Free Tier | Best For |
|---|---|---|
| **Railway** | $5/month credit | Python scripts, Node.js apps |
| **Render** | 750 hrs/month | Web services, cron jobs |
| **Fly.io** | 3 shared VMs | Containerised apps |
| **Vercel** | Unlimited (serverless) | Next.js, static sites |
| **GitHub Actions** | 2,000 min/month | Cron scripts, automation |
| **PythonAnywhere** | 1 web app + cron | Python scripts |
| **Glitch** | Always-on apps | Node.js projects |

---

## GitHub Repositories Worth Starring

```
# WordPress automation
vangent/wordpress-to-github        # Export WP to GitHub
wp-cli/wp-cli                      # Command-line WordPress control

# Automation frameworks
n8n-io/n8n                         # No-code automation (self-hosted)
huginn/huginn                      # Agent automation
activepieces/activepieces           # n8n alternative

# AI tools (local/free)
ollama/ollama                      # Local LLM runner
mozilla/TTS                        # Text-to-speech
coqui-ai/TTS                       # Neural TTS

# Writing tools
obsidianmd/obsidian-releases       # Note-taking
logseq/logseq                      # Linked notes

# Job hunting
Culdee/JobSpy                      # Multi-site job scraper
fedecalendino/linkedin-jobs-scraper # LinkedIn scraper

# Productivity
espanso/espanso                    # Text expander
ActivityWatch/activitywatch        # Time tracker
```
