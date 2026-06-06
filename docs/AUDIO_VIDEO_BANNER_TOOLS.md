# Audio, Video & Banner Production Tools (All Free)

## Audio

### Recording & Editing

**Audacity** — Best free audio editor  
- URL: audacityteam.org | Platform: Windows/Mac/Linux  
- Use: Record voiceovers, remove background noise, export MP3  
- Key shortcut: Space = play/pause, R = record

**Tenacity** — Privacy-focused Audacity fork  
- GitHub: github.com/tenacityteam/tenacity  
- Same features, no telemetry

### Speech-to-Text (Low Energy Writing)

**Whisper** (OpenAI — Free, Local, Best Accuracy)
```bash
pip install openai-whisper
whisper recording.mp3 --language en --output_format txt
whisper note_french.m4a --language fr --output_format txt
```
Supports 100+ languages including French. Runs completely offline.

**Google Docs Voice Typing** (Easiest)
- Tools → Voice Typing → speak → copy text into sheet
- No installation, works in browser

### Text-to-Speech (Blog Post Audio / Accessibility)

**Coqui TTS** — Free, local, converts posts to audio
```bash
pip install TTS
tts --text "Today we practised listening skills..." \
    --model_name tts_models/en/ljspeech/tacotron2-DDC \
    --out_path post_audio.wav
```

**ElevenLabs** — Best quality TTS, free tier: 10,000 chars/month  
- URL: elevenlabs.io
- Use: Convert blog posts to audio for accessibility

### Phonetics (ELT-Specific)

**Praat** — Phonetics analysis and teaching
- URL: praat.org (free)
- Use: Create spectrograms, analyse pronunciation for ELT posts

---

## Video

### Recording

**OBS Studio** — Professional screen recording + streaming
- GitHub: github.com/obsproject/obs-studio (60k+ stars)
- Use: Record teaching sessions, create video lessons
- Free and professional-grade

**ShareX** (Windows) — Screenshots, screen recording, GIFs
- GitHub: github.com/ShareX/ShareX
- One-click recording, auto-upload

### Editing

**Kdenlive** — Best free video editor
- URL: kdenlive.org | Platform: Linux/Windows/Mac
- Multi-track editing, titles, transitions

**OpenShot** — Simpler editing
- GitHub: github.com/OpenShot/openshot-qt

**DaVinci Resolve** — Professional-grade, free tier
- URL: blackmagicdesign.com/products/davinciresolve
- Colour correction, audio, full editing pipeline

---

## Banners & Images

### Canva (Easiest — Web-Based)
- URL: canva.com | Free tier: 250,000+ templates
- Blog banner size: 1200×628px
- Search: "education blog header" → edit text

### GIMP (Most Powerful)
- URL: gimp.org | Full image editor, free

### Inkscape (Vector/SVG)
- URL: inkscape.org
- Create scalable logos, infographics
```bash
# CLI export
inkscape input.svg --export-png=banner.png --export-width=1200
```

### ImageMagick (Batch Automation)
Create banners programmatically for every post:

```python
import subprocess
from pathlib import Path

def create_blog_banner(title: str, output_path: str):
    """Generate a 1200x628 blog banner from a post title."""
    cmd = [
        'convert',
        '-size', '1200x628',
        'gradient:#1a3a5c-#0d2137',
        '-font', 'DejaVu-Sans-Bold',
        '-pointsize', '52',
        '-fill', 'white',
        '-gravity', 'Center',
        '-annotate', '+0-30', title[:70],
        '-font', 'DejaVu-Sans',
        '-pointsize', '26',
        '-fill', '#90b8e0',
        '-gravity', 'South',
        '-annotate', '+0+50', 'sourovdeb.com | ELT Masterclass',
        output_path
    ]
    try:
        subprocess.run(cmd, check=True)
        print(f'Banner: {output_path}')
    except FileNotFoundError:
        print('Install ImageMagick: sudo apt install imagemagick')

# Batch create for all posts in queue
import csv

def batch_banners(csv_path: str):
    Path('banners').mkdir(exist_ok=True)
    with open(csv_path) as f:
        for row in csv.DictReader(f):
            if row.get('Status') == 'published':
                continue
            title = row['Title']
            name = title[:30].replace(' ', '_').replace('/', '_')
            create_blog_banner(title, f'banners/{name}.png')

if __name__ == '__main__':
    batch_banners('queue.csv')
```

Install ImageMagick:
```bash
# Ubuntu/Debian
sudo apt install imagemagick

# Mac
brew install imagemagick

# Windows: download from imagemagick.org
```

### AI Image Generation (Free Tiers)

**Stable Diffusion** (Local, Free Forever)
- GitHub: github.com/AUTOMATIC1111/stable-diffusion-webui
- Generate ELT-themed header images from text prompts

**Bing Image Creator** (Free with Microsoft account)
- URL: bing.com/create
- DALL-E 3 quality, 15 free generations/day

**Ideogram** (Best for Text-in-Images)
- URL: ideogram.ai
- Free tier: 10 images/day
- Best for banners where the title text must be readable
