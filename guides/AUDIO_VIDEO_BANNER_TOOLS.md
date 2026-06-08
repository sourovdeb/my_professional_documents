# Audio, Video & Banner Tools Guide
## Free & Open-Source Tools for ELT Content Creation

---

## AUDIO TOOLS

### 1. Audacity — Record & Edit Audio
- **Download:** audacityteam.org
- **Free:** Yes (open-source)
- **What you can do:**
  - Record your voice for podcast episodes
  - Remove background noise (Effect → Noise Reduction)
  - Edit out pauses and mistakes
  - Export as MP3, WAV, FLAC

**Quick Start for ELT Podcasts:**
1. Download and install Audacity
2. Click the red Record button
3. Speak your content
4. Select a "noisy" part (where it's silent) → Effect → Noise Reduction → Get Noise Profile
5. Select All (Ctrl+A) → Effect → Noise Reduction → OK
6. File → Export → MP3

**Export settings for web:** 128 kbps mono (half the file size, no quality loss for voice)

---

### 2. Whisper — AI Transcription (Free, Local)
- **GitHub:** github.com/openai/whisper (60,000+ stars)
- **Free:** Completely free, runs locally
- **Supports:** English, French, Hindi + 90 other languages

**Install:**
```bash
pip install openai-whisper
pip install torch  # If not already installed
```

**Transcribe audio:**
```python
import whisper

model = whisper.load_model('base')  # Models: tiny, base, small, medium, large

# Transcribe
result = model.transcribe('my_lecture.mp3')
print(result['text'])

# Save to file
with open('transcript.txt', 'w') as f:
    f.write(result['text'])
```

**Which model to use:**
| Model | Size | Quality | Speed |
|-------|------|---------|-------|
| `tiny` | 39 MB | Basic | Very fast |
| `base` | 74 MB | Good | Fast |
| `small` | 244 MB | Better | Medium |
| `medium` | 769 MB | Great | Slow |
| `large` | 1.5 GB | Best | Very slow |

For transcribing your own voice: `base` or `small` is perfect.

---

### 3. Google Speech-to-Text (Free in Google Docs)
- **URL:** docs.google.com
- **Free:** Yes
- **How:** Tools → Voice Typing → Click microphone → Speak
- **Best for:** Low-energy days when typing is hard — speak your 500 words instead of typing them

---

### 4. ElevenLabs — AI Voice (Free Tier)
- **URL:** elevenlabs.io
- **Free tier:** 10,000 characters/month
- **What:** Convert your blog posts to lifelike audio narration
- **Use case:** Create audio versions of your ELT posts for learners with reading difficulties

**Python API:**
```python
import requests, os

XI_KEY = os.getenv('ELEVENLABS_KEY')

def text_to_audio(text, output_file='output.mp3'):
    voice_id = 'EXAVITQu4vr4xnSDxMaL'  # 'Sarah' voice (natural)
    
    r = requests.post(
        f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}',
        headers={
            'xi-api-key': XI_KEY,
            'Content-Type': 'application/json'
        },
        json={
            'text': text,
            'model_id': 'eleven_monolingual_v1',
            'voice_settings': {'stability': 0.5, 'similarity_boost': 0.75}
        }
    )
    
    with open(output_file, 'wb') as f:
        f.write(r.content)
    print(f'Saved: {output_file}')
```

---

### 5. Coqui TTS — Free Local Text-to-Speech
- **GitHub:** github.com/coqui-ai/TTS (35,000+ stars)
- **Free:** Completely free, open-source, local

```bash
pip install TTS
```

```python
from TTS.api import TTS

# Load model
tts = TTS('tts_models/en/ljspeech/tacotron2-DDC')

# Convert text to audio
tts.tts_to_file(
    text="Welcome to ELT Masterclass. Today we explore listening comprehension.",
    file_path="intro.wav"
)
```

---

## VIDEO TOOLS

### 1. OBS Studio — Screen Recording & Streaming
- **GitHub:** github.com/obsproject/obs-studio (55,000+ stars)
- **Download:** obsproject.com
- **Free:** Yes (completely)

**For ELT Video Lessons:**
1. Add a "Scene" for your lesson
2. Add sources: "Display Capture" (your screen) + "Audio Capture"
3. For webcam overlay: add "Video Capture Device" source
4. Click "Start Recording"
5. Files save as MKV — remux to MP4: Tools → Remux Recordings

**Recommended settings for YouTube:**
- Resolution: 1920x1080
- FPS: 30
- Encoder: x264
- Rate Control: CRF 23
- Keyframe: 2

---

### 2. Kdenlive — Professional Video Editor
- **Download:** kdenlive.org
- **Free:** Yes (open-source)

**Workflow for ELT lessons:**
1. Import your OBS recording
2. Drag to Timeline
3. Use Blade tool (X) to cut out mistakes and long pauses
4. Add title card: Add Effect → Video Effects → Motion → Composite
5. Render: File → Render → Select MP4/H.264 preset

---

### 3. FFmpeg — Command-Line Video Processing
- **URL:** ffmpeg.org
- **Free:** Yes (open-source)

**Essential commands:**
```bash
# Compress video (reduce file size 50-70%)
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4

# Add subtitles to video
ffmpeg -i video.mp4 -vf subtitles=subtitles.srt output.mp4

# Extract frames as images (for thumbnail selection)
ffmpeg -i video.mp4 -vf fps=0.1 frames/thumb%04d.jpg

# Create video from slideshow + audio
ffmpeg -r 1/10 -i slide%d.jpg -i narration.mp3 \
  -c:v libx264 -pix_fmt yuv420p -c:a aac lesson.mp4

# Trim video (from 0:30 to 5:00)
ffmpeg -i input.mp4 -ss 00:00:30 -to 00:05:00 -c copy trimmed.mp4
```

---

### 4. Lossless Cut — Fast Video Trimmer
- **GitHub:** github.com/mifi/lossless-cut (25,000+ stars)
- **Free:** Yes
- **What:** Trim, cut, split videos without re-encoding (instant, no quality loss)
- **Best for:** Quickly cutting the start/end off OBS recordings

---

### 5. CapCut Desktop (Free)
- **URL:** capcut.com
- **Free tier:** Generous free features
- **What:** Easy video editor with auto-captions, templates, trending effects
- **Best for:** Creating short TikTok/Instagram Reels from your ELT content

---

## BANNER & IMAGE TOOLS

### 1. GIMP — Advanced Image Editor
- **URL:** gimp.org
- **Free:** Yes (Photoshop-level, open-source)

**Create WordPress Blog Banner (1200x628px):**
1. File → New → Width: 1200, Height: 628
2. Bucket fill with your brand color
3. Text tool → type your post title
4. File → Export As → banner.jpg (quality: 85)

**Script to batch-create banners:**
```bash
# Install: sudo apt install gimp
# Create banner from template using GIMP Script-Fu
gimp -i -b '(let* \
  ((image (car (gimp-file-load RUN-NONINTERACTIVE "template.xcf" "template.xcf")))\
   (text-layer (car (gimp-text-fontname image -1 50 200 "Day 32: Listening" 10 TRUE 72 UNIT-PIXEL "Sans Bold"))))\
  (gimp-image-flatten image)\
  (file-jpeg-save RUN-NONINTERACTIVE image (car (gimp-image-get-active-drawable image)) "output.jpg" "output.jpg" 0.85 0 0 0 "" 0 1 0 2 0)\
  (gimp-quit 0))'
```

---

### 2. Inkscape — Vector Graphics
- **Download:** inkscape.org
- **Free:** Yes
- **Best for:** Logos, icons, scalable banners that look sharp at any size

**Create post banner:**
1. File → New → Set width=1200px, height=628px
2. Draw rectangle with your background color
3. Text tool (T) → type title
4. File → Export PNG (set DPI to 96 for web)

---

### 3. Canva (Free Tier)
- **URL:** canva.com
- **Free templates:** 250,000+

**Best templates for ELT blog:**
- Blog Banner: search "Blog Banner" → filter by free
- LinkedIn Post: 1200x627px
- Pinterest Pin: 1000x1500px (great for ELT tips)
- Quote Card: 1080x1080px (for social media)

**Canva to WordPress shortcut:**
1. Create banner in Canva
2. Download as JPG (max quality)
3. Upload to WordPress Media Library
4. Set as Featured Image when publishing post

---

### 4. Figma (Free for Personal)
- **URL:** figma.com
- **Free:** Yes for personal use (3 projects)
- **Best for:** Professional-looking UI mockups, presentations, lesson materials

---

### 5. ImageMagick — Batch Image Processing
```bash
# Resize all blog images to web-optimized 1200px width
mogrify -resize 1200x -quality 85 -strip *.jpg

# Add watermark to all images
for img in *.jpg; do
  convert "$img" -gravity SouthEast -font Ubuntu -pointsize 18 \
    -fill 'rgba(255,255,255,0.7)' -annotate +10+10 'sourovdeb.com' \
    "watermarked_$img"
done

# Create thumbnail from each image
for img in *.jpg; do
  convert "$img" -thumbnail 400x300^ -gravity center -extent 400x300 \
    "thumb_$img"
done
```

---

### 6. Remove.bg API (Background Removal)
- **URL:** remove.bg
- **Free tier:** 50 credits/month
- **API:**
```python
import requests

def remove_background(image_path):
    with open(image_path, 'rb') as f:
        r = requests.post(
            'https://api.remove.bg/v1.0/removebg',
            files={'image_file': f},
            data={'size': 'auto'},
            headers={'X-Api-Key': os.getenv('REMOVEBG_KEY')}
        )
    with open('no_bg.png', 'wb') as f:
        f.write(r.content)
```

---

## WORKFLOW SUMMARY

### ELT Video Lesson Workflow
```
Write script          Record with OBS    Edit with Kdenlive
(Google Docs)    →    (screen + mic)   →  (cut, add captions)   →  YouTube
                                                                      ↓
                                                         Embed in WordPress post
```

### Blog Banner Workflow
```
Write post title  →  Open Canva  →  Select template  →  Download JPG  →  Upload to WP
(30 seconds)         (web app)      (free)              (2MB max)        (featured img)
```

### Podcast Episode Workflow
```
Speak into        Record in           Edit in          Export           Upload to
microphone   →   Audacity       →    Audacity    →   128kbps MP3  →   Anchor/Spotify
                  (free)              (noise cut)       (10MB/hr)        (free hosting)
```

---

*Last updated: June 2026*
