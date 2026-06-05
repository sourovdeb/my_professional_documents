# Audio, Video & Banner Creation Tools — Complete Free Guide

> All tools are free (free tier or fully open-source). Tested and verified as of June 2026.

---

## Part 1: Audio Tools

### Recording & Editing

| Tool | OS | Best For | Download |
|------|----|---------|---------|
| **Audacity** | Win/Mac/Linux | Podcast recording, noise removal, trimming | audacityteam.org |
| **Ardour** | Win/Mac/Linux | Professional multitrack audio | ardour.org |
| **Ocenaudio** | Win/Mac/Linux | Quick edits, easier than Audacity | ocenaudio.com |
| **Tenacity** | Win/Mac/Linux | Audacity fork without telemetry | github.com/tenacityteam/tenacity |

### Audacity Quick Start for Podcasters

```
1. Record: Click the red Record button
2. Remove background noise:
   - Select a silent section at the start
   - Effect → Noise Reduction → Get Noise Profile
   - Select all (Ctrl+A) → Effect → Noise Reduction → OK
3. Normalize volume: Effect → Normalize → OK
4. Export: File → Export → Export as MP3
```

### Text-to-Speech (Free)

| Tool | How to use | Quality |
|------|-----------|--------|
| **Kokoro-TTS** | github.com/hexgrad/kokoro — local, excellent | Very high |
| **Piper TTS** | github.com/rhasspy/piper — local, fast | High |
| **Mozilla TTS** | github.com/mozilla/TTS — local | Medium-high |
| **ElevenLabs free** | elevenlabs.io — 10,000 chars/month | Professional |
| **Google TTS** | Built into Google Docs (Tools → Voice typing) | Good |
| **Balabolka** | Windows only, free | Good |

### Speech-to-Text (Transcription)

| Tool | How to use | Free? |
|------|-----------|-------|
| **Whisper (OpenAI)** | `pip install openai-whisper` — runs locally | Free forever |
| **Faster Whisper** | github.com/SYSTRAN/faster-whisper — 4× faster | Free forever |
| **Whisper.cpp** | github.com/ggerganov/whisper.cpp — minimal setup | Free forever |
| **otter.ai** | otter.ai — 300 min/month free | Free tier |
| **Google Docs voice** | Tools → Voice typing | Free |

#### Whisper transcription (converts audio to text for blog posts)

```python
# pip install openai-whisper
import whisper

model = whisper.load_model('base')  # or 'small', 'medium'
result = model.transcribe('my_recording.mp3')
print(result['text'])
# → Converts your spoken words to a blog post draft
```

### Music / Background Audio (Copyright-Free)

| Source | URL | License |
|--------|-----|--------|
| **Free Music Archive** | freemusicarchive.org | Varies (check each track) |
| **ccMixter** | ccmixter.org | Creative Commons |
| **Jamendo** | jamendo.com | CC for non-commercial |
| **Pixabay Music** | pixabay.com/music | Free commercial use |
| **YouTube Audio Library** | studio.youtube.com → Audio Library | Free for any use |
| **BENSOUND** | bensound.com | Free with attribution |

---

## Part 2: Video Tools

### Video Editors (Desktop)

| Tool | OS | Best For | Link |
|------|----|---------|--------------|
| **Kdenlive** | Win/Mac/Linux | Full-featured editing | kdenlive.org |
| **OpenShot** | Win/Mac/Linux | Beginners, simple timeline | openshot.org |
| **Shotcut** | Win/Mac/Linux | Fast, no install needed | shotcut.org |
| **DaVinci Resolve** | Win/Mac/Linux | Professional (free version is powerful) | blackmagicdesign.com |
| **Blender** (video) | Win/Mac/Linux | Advanced editing + 3D | blender.org |
| **Handbrake** | Win/Mac/Linux | Convert/compress videos | handbrake.fr |

### Screen Recording

| Tool | OS | Features | Link |
|------|----|---------|------|
| **OBS Studio** | Win/Mac/Linux | Record + live stream, professional | obsproject.com |
| **VokoscreenNG** | Linux/Win | Simple, lightweight | github.com/vkohaupt/vokoscreenNG |
| **Kooha** | Linux | Clean, minimal screen recorder | github.com/SeaDve/Kooha |
| **ShareX** | Windows | Screenshot + video + annotation | getsharex.com |
| **Flameshot** | Win/Mac/Linux | Screenshot with annotations | github.com/flameshot-org/flameshot |

### AI-Powered Video Tools (Free Tier)

| Tool | Free Tier | Use Case |
|------|-----------|----------|
| **Clipchamp** | Free in Windows 11 | Basic AI trim + captions |
| **CapCut** | Free (desktop) | Auto-captions, TikTok-style edits |
| **Descript** | 1 hour free/month | Transcript-based editing |
| **Runway ML** | 125 credits/month | AI video generation |
| **Luma Dream Machine** | 30 free credits | Text-to-video |

### Video Compression for WordPress

Large videos slow down WordPress. Use these to compress before uploading:

```bash
# FFmpeg (free, command-line): compress any video
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
# -crf 18-28: 18=high quality, 28=smaller file

# Or use HandBrake (GUI version of FFmpeg)
```

For WordPress: **always host videos on YouTube/Vimeo and embed them.** Never upload raw video to WordPress — it wastes storage and slows your site.

---

## Part 3: Banner & Graphics Tools

### Desktop Graphics Editors

| Tool | OS | Skill Level | Best For |
|------|----|---------|---------|
| **GIMP** | Win/Mac/Linux | Intermediate | Photo editing, complex graphics |
| **Inkscape** | Win/Mac/Linux | Beginner/Intermediate | Vector graphics, logos, banners |
| **Krita** | Win/Mac/Linux | Beginner | Digital painting, illustrations |
| **Penpot** | Browser (self-hosted) | Intermediate | UI/UX design, Figma alternative |
| **LibreOffice Draw** | Win/Mac/Linux | Beginner | Simple diagrams and banners |

### Online Design Tools (Free Tier)

| Tool | Free Tier | Best For |
|------|-----------|----------|
| **Canva** | canva.com — very generous free tier | Blog banners, social graphics |
| **Adobe Express** | Free tier available | Quick banners |
| **Photopea** | photopea.com — fully free, browser-based | Photoshop replacement online |
| **remove.bg** | 50 free/month | Remove image backgrounds |
| **Vectorizer.ai** | Limited free | Convert images to vector |
| **Favicon.io** | favicon.io | Create favicons |

### Canva WordPress Banner Workflow

```
1. Go to canva.com → Create a design → Blog Banner (1200×628)
2. Choose a template
3. Edit: title text, background colour, your photo
4. Download as JPG (File → Download → JPG, quality 80%)
5. Upload to WordPress (Media → Add New)
6. Set as Featured Image on your post
```

**Recommended Canva sizes for blog:**
- Featured image: 1200×628px
- Pinterest pin: 1000×1500px
- Twitter/X: 1600×900px
- Instagram square: 1080×1080px

### Stock Photos (Royalty-Free)

| Site | URL | License |
|------|-----|--------|
| **Unsplash** | unsplash.com | Free, no attribution needed |
| **Pexels** | pexels.com | Free, no attribution needed |
| **Pixabay** | pixabay.com | Free commercial use |
| **StockSnap** | stocksnap.io | CC0 public domain |
| **Gratisography** | gratisography.com | Quirky, unique shots |
| **Openverse** | openverse.org | Search CC images across the web |

---

## Part 4: The ELT Blog Content Stack

For creating engaging ELT blog posts, combine these tools:

```
Content:      Write in Logseq/Google Docs
Images:       Canva (blog banner) + Unsplash (body images)
Audio:        Audacity (record pronunciation examples)
Transcribe:   Whisper (turn recorded lessons into text)
Video:        OBS (record your teaching, if applicable)
Publish:      Google Sheets → Apps Script → WordPress
```

This is a complete free content creation pipeline.
