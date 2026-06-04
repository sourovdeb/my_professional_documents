# Free Tools for Audio, Video, and Banner Creation

**Every tool listed is free or has a completely usable free tier. Verified open-source options marked ★.**  
**Last updated: June 2026**

---

## Audio Tools

### Recording and Editing

| Tool | Type | Best For | Download |
|------|------|----------|----------|
| **Audacity** ★ | Desktop | Record voice, edit podcasts, remove noise | audacityteam.org |
| **Tenacity** ★ | Desktop | Fork of Audacity without telemetry | tenacityaudio.org |
| **Ardour** ★ | Desktop DAW | Full professional audio production | ardour.org |
| **Reaper** | Desktop DAW | Near-professional quality ($60, but free trial never expires) | reaper.fm |

**Audacity Quickstart for Voice Recording:**
```
1. Download from audacityteam.org and install
2. Plug in your microphone
3. Click the red Record button
4. Speak your content
5. Stop recording
6. Go to: Effect → Noise Reduction → Get Noise Profile (select a silent section first)
7. Apply: Effect → Noise Reduction → OK
8. File → Export → Export as MP3
```

**For bipolar/low-energy days:** Speaking is easier than typing. Record your thoughts, then use Whisper to transcribe.

---

### Speech-to-Text (Voice Typing → Blog Content)

| Tool | Type | Quality | Cost |
|------|------|---------|------|
| **OpenAI Whisper** ★ | Python (local) | Excellent | Free |
| **Whisper.cpp** ★ | C++ (fast, local) | Excellent | Free |
| **WhisperX** ★ | Python (with timestamps) | Excellent | Free |
| **Google Docs Voice Typing** | Browser | Good | Free |
| **Nerd Dictation** ★ | Linux desktop | Good | Free |

**Install and use OpenAI Whisper:**
```bash
pip install openai-whisper

# Transcribe any audio or video file
whisper recording.mp3 --language English --output_format txt

# Output: recording.txt — your spoken words as text
```

**Workflow for low-energy writing:**
```
1. Speak for 5–10 minutes into your phone's voice recorder
2. Transfer the audio file to your computer
3. Run: whisper recording.mp3 --output_format txt
4. Open the .txt file
5. Copy into your Google Sheet as blog content
6. Apps Script publishes it automatically
```

Total active effort: under 10 minutes. The rest is automated.

---

### Text-to-Speech (Convert Your Blog Posts to Audio)

| Tool | Quality | Cost | Notes |
|------|---------|------|-------|
| **Coqui TTS** ★ | Good | Free (local) | Many voices and languages |
| **Piper TTS** ★ | Good | Free (local) | Very fast on CPU |
| **Bark** (by Suno) ★ | Excellent (emotive) | Free (GPU helps) | Most natural-sounding |
| **ElevenLabs** | Outstanding | Free (10,000 chars/month) | Best online option |
| **Microsoft Edge TTS** | Good | Free | Available via Python |

**Install Piper (lightest, works on any CPU):**
```bash
pip install piper-tts

# Convert text to audio
echo "Welcome to Day 32 of my ELT Masterclass." | \
  piper --model en_US-lessac-medium --output_file lesson_intro.wav
```

**Use Microsoft Edge TTS (no install needed, completely free):**
```bash
pip install edge-tts
edge-tts --text "Your blog post text here" --voice en-GB-SoniaNeural --write-media output.mp3
```

---

### Audio for Podcasts

| Tool | Purpose | Cost |
|------|---------|------|
| **Anchor by Spotify** | Host and distribute your podcast | Free |
| **Buzzsprout** | Professional podcast hosting | Free tier |
| **ffmpeg** ★ | Convert, compress, and process audio | Free |
| **mp3DirectCut** | Split and trim MP3 without re-encoding | Free |
| **Auphonic** | Automatic audio leveling and noise reduction | Free (2 hours/month) |

**Common ffmpeg audio commands:**
```bash
# Convert WAV to MP3
ffmpeg -i recording.wav -codec:a libmp3lame -qscale:a 2 podcast.mp3

# Remove first 10 seconds (cut out an intro fumble)
ffmpeg -i recording.mp3 -ss 10 -acodec copy trimmed.mp3

# Normalize audio levels
ffmpeg -i input.mp3 -filter:a "dynaudnorm" normalized.mp3

# Combine intro music with your voice
ffmpeg -i voice.mp3 -i music.mp3 -filter_complex amix=inputs=2:duration=first combined.mp3
```

---

## Video Tools

### Screen Recording

| Tool | Platform | Best For | Cost |
|------|----------|----------|------|
| **OBS Studio** ★ | Win/Mac/Linux | Screen recording + live streaming | Free |
| **SimpleScreenRecorder** ★ | Linux | Lightweight recording | Free |
| **ShareX** ★ | Windows | Recording + screenshots + annotation | Free |
| **Kazam** ★ | Linux | Quick desktop recordings | Free |

**OBS Studio Setup for Teaching Tutorials:**
```
1. Download from obsproject.com
2. Add Source → Display Capture (records your screen)
3. Add Source → Audio Input Capture (records your microphone)
4. Click “Start Recording”
5. Your recording saves to the Videos folder
```

OBS is also used for live streaming (YouTube, Twitch) if you ever want to teach live.

---

### Video Editing

| Tool | Skill Level | Best For | Cost |
|------|-------------|----------|------|
| **OpenShot** ★ | Beginner | Simple cuts, titles, transitions | Free |
| **Kdenlive** ★ | Beginner–Advanced | Full video editing | Free |
| **Shotcut** ★ | Intermediate | Quick edits, good for YouTube | Free |
| **DaVinci Resolve** | Advanced | Professional grade | Free (limited) |
| **HandBrake** ★ | Any | Compress video for web | Free |

**Kdenlive Quick Tutorial Video Workflow:**
```
1. Download from kdenlive.org
2. File → New Project
3. Drag your screen recording into the Project Bin (top left)
4. Drag it from the Bin onto the Timeline
5. Razor tool (R key): cut out mistakes
6. Title clip: Add → Title Clip → type your lesson title
7. Render: File → Render → choose MP4 H.264 → Render to File
```

---

### Video Processing with ffmpeg (Command Line)

ffmpeg is the Swiss Army knife of video/audio. Free, open-source, powerful.

```bash
# Compress video for web upload (reduces file size significantly)
ffmpeg -i input.mp4 -crf 28 -preset fast output_compressed.mp4

# Resize to 720p for YouTube
ffmpeg -i input.mp4 -vf scale=1280:720 output_720p.mp4

# Extract audio from a video
ffmpeg -i video.mp4 -vn -codec:a libmp3lame audio.mp3

# Add subtitles burned into video
ffmpeg -i video.mp4 -vf subtitles=subtitles.srt output_with_subs.mp4

# Speed up a video 2x (good for demo recordings)
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" fast.mp4

# Create a slideshow from images (one image per 5 seconds)
ffmpeg -framerate 1/5 -pattern_type glob -i '*.jpg' -c:v libx264 slideshow.mp4
```

---

### Auto-Subtitling a Video (Free, Fully Automated)

```bash
# Step 1: Extract audio from your video
ffmpeg -i my_lesson.mp4 audio.wav

# Step 2: Transcribe to SRT subtitle format
whisper audio.wav --output_format srt

# Step 3: Burn subtitles permanently into the video
ffmpeg -i my_lesson.mp4 -vf subtitles=audio.srt lesson_with_subs.mp4
```

This creates a subtitled video in about 5 minutes. Completely free.

---

## Banner and Graphics Tools

### Image Editing (Photoshop Alternative)

| Tool | Type | Best For | Cost |
|------|------|----------|------|
| **GIMP** ★ | Desktop | Full image editing, photo work | Free |
| **Krita** ★ | Desktop | Digital illustration | Free |
| **Photopea** | Browser | Photoshop in your browser | Free |
| **Pixlr E** | Browser | Quick edits | Free |

**GIMP: Create a Blog Banner from Scratch**
```
1. File → New → 1200 x 630 pixels → OK
2. Bucket Fill tool: fill background with your brand color (e.g. dark blue #1a237e)
3. Text tool: click the image, type your post title
4. Set font to "Playfair Display" or "Open Sans", size 60
5. Color: white (#ffffff)
6. Position in upper center
7. Add a small subtitle text at the bottom: size 30
8. File → Export As → banner.png
9. Upload to WordPress Media Library as featured image
```

---

### Vector Graphics and Design

| Tool | Type | Best For | Cost |
|------|------|----------|------|
| **Inkscape** ★ | Desktop | Logos, infographics, vector art | Free |
| **Penpot** ★ | Web/Self-hosted | Design + prototyping (open-source Figma) | Free |
| **Canva** | Web | Templates for social media, banners | Free tier |
| **SVGEdit** ★ | Browser | Quick SVG files | Free |

**Canva Quick Setup (Highly Recommended for Non-Designers):**
```
1. Create a free account at canva.com
2. Create a new design → Custom Size → 1200 x 630 px
3. Choose a template or build your own
4. Set your colors and font once
5. Click "Share" button → → → Save as Template
6. Every new post: Duplicate Template → Change title text only → Download PNG
```

This means designing a banner takes under 2 minutes for every post.

---

### AI Image Generation (Create Banner Images with AI)

| Tool | Type | Cost | Notes |
|------|------|------|-------|
| **Bing Image Creator** | Web (no install) | Free | Powered by DALL-E 3 |
| **Adobe Firefly** | Web | Free tier | High quality |
| **Leonardo.ai** | Web | Free (150 credits/day) | Great for banners |
| **AUTOMATIC1111** ★ | Local (Python) | Free (GPU helps) | Full Stable Diffusion |
| **ComfyUI** ★ | Local (Python) | Free (GPU helps) | Node-based SD |
| **Stable Diffusion CPU** | Local (Python) | Free (slow) | Works without GPU |

**Create a Banner in 2 Minutes with Bing Image Creator:**
```
1. Go to bing.com/images/create
2. Type: "Professional ELT teaching blog banner, minimalist flat design,
   blue and white color scheme, large text: 'Day 32: The Power of Listening'"
3. Click Create
4. Download the best result
5. Upload to WordPress as featured image
```

---

### Fonts (Free, Professional Quality)

All available free at **fonts.google.com** — download and install on your computer:

| Font | Style | Best Use |
|------|-------|----------|
| **Open Sans** | Modern sans-serif | Body text |
| **Lato** | Clean sans-serif | Headers |
| **Merriweather** | Readable serif | Long articles |
| **Playfair Display** | Elegant serif | Blog title banners |
| **Nunito** | Rounded, friendly | Modern blog |
| **IBM Plex Sans** | Technical, clean | Professional posts |

---

## Standard Sizes for Blog Graphics

| Use | Width × Height | Notes |
|-----|----------------|-------|
| WordPress featured image | 1200 × 628 | Most themes use this |
| Twitter/X card | 1200 × 675 | Shown in link previews |
| LinkedIn post image | 1200 × 627 | Professional network |
| Pinterest pin | 1000 × 1500 | Vertical format |
| YouTube thumbnail | 1280 × 720 | Required by YouTube |
| Podcast cover art | 3000 × 3000 | Required for Spotify/Apple |

---

## Complete Low-Energy Multimedia Workflow

**Good day (30 minutes):**
```
1. [5 min]  Record yourself speaking about the topic (OBS or phone)
2. [2 min]  Run Whisper to transcribe
3. [3 min]  Paste into Claude.ai, ask to edit into a proper post
4. [3 min]  Duplicate your Canva banner template, change title
5. [2 min]  Add to Google Sheet with content + upload banner
6. [0 min]  Apps Script publishes automatically
Total: ~15 minutes of active work
```

**Low-energy day (8 minutes):**
```
1. [5 min]  Speak a few thoughts into your phone recorder
2. [2 min]  Run Whisper, copy transcript to Google Sheet as draft
3. [1 min]  Set status to 'draft' (review when feeling better)
4. [0 min]  System saves the draft automatically
Total: 8 minutes
```

**Very low energy (2 minutes):**
```
1. Open Le Chat (chat.mistral.ai)
2. Type: "Write 500 words about [topic] for my ELT blog"
3. Copy output to Google Sheet
4. Done
```

---

*Last updated: June 2026 · Maintained in sourovdeb/my_professional_documents*
