# Audio, Video & Banner Tools
## Everything You Need for Content Creation — All Free or Open Source

---

## Audio Tools

### Recording & Editing
| Tool | Best for | Platform | Link |
|------|---------|----------|------|
| **Audacity** | Podcast recording, noise removal, export MP3 | Win/Mac/Linux | audacityteam.org |
| **Ocenaudio** | Simple audio editing, faster than Audacity | Win/Mac/Linux | ocenaudio.com |
| **GarageBand** | Full music/podcast production (free on Mac) | Mac only | Built-in |
| **Reaper** | Professional DAW, discounted for personal use $60 | Win/Mac/Linux | reaper.fm |

### Audacity Quick Workflow for ELT Listening Materials
1. Record → **Effects → Noise Reduction** (first pass removes background hum)
2. **Effects → Compressor** (evens out loud/quiet parts)
3. **Effects → Normalize** (sets consistent volume to -1dB)
4. **File → Export → MP3** (use 128kbps for speech)

### Text-to-Speech (Generate Audio From Your Blog Posts)
| Tool | Quality | Cost |
|------|---------|------|
| **Coqui TTS** | Good, open source, runs locally | Free |
| **piper-tts** | Very fast local TTS | Free |
| **ElevenLabs** | Excellent quality, natural voices | Free tier: 10k chars/month |
| **Google Text-to-Speech** | Part of Google Cloud | Free tier: 1M chars/month |
| **Mozilla TTS** | Open source, many voices | Free |

**Generate audio from your WordPress posts automatically:**
```python
# Uses piper-tts (free, local, fast)
import subprocess
from pathlib import Path

def text_to_mp3(text: str, output_path: str, voice: str = 'en_US-lessac-medium'):
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([
        'piper', '--model', voice,
        '--output_file', output_path
    ], input=text, text=True, check=True)

text_to_mp3("Today we practice English listening skills.", "audio/lesson32.mp3")
```

Install piper: `pip install piper-tts`

### Podcast Hosting (Free)
| Platform | Free Storage | Notes |
|----------|-------------|-------|
| **Anchor / Spotify for Podcasters** | Unlimited | Easiest setup |
| **Buzzsprout** | 2 hours/month free | Good analytics |
| **Podbean** | 5 hours/month free | Clean interface |

---

## Video Tools

### Screen Recording
| Tool | Best for |
|------|----------|
| **OBS Studio** | Screen recording + live streaming (obsproject.com) |
| **SimpleScreenRecorder** | Linux, simple and reliable |
| **ShareX** | Windows, includes annotations and GIF export |
| **Loom** | Share recordings via link (free for 5-min videos) |

### Video Editing
| Tool | Best for | Platform |
|------|---------|----------|
| **Kdenlive** | Full-featured, good for YouTube videos | Win/Mac/Linux |
| **Shotcut** | Simple cuts, quick edits | Win/Mac/Linux |
| **DaVinci Resolve** | Professional quality, free version is powerful | Win/Mac/Linux |
| **OpenShot** | Very simple, good for beginners | Win/Mac/Linux |
| **HandBrake** | Convert/compress videos only (not editing) | Win/Mac/Linux |

### AI Video Tools (Free Tier)
| Tool | What it does | Free tier |
|------|-------------|----------|
| **Clipchamp** | Microsoft's video editor with AI tools | Free (Windows) |
| **Kapwing** | Add subtitles, resize for social media | 7 exports/month |
| **Veed.io** | Auto subtitles, basic editing | Limited free |
| **RunwayML** | AI background removal, motion tracking | 3 projects free |

### FFmpeg — The Swiss Army Knife
FFmpeg is a command-line tool that can convert, trim, and process any audio/video.
```bash
# Install
sudo apt install ffmpeg  # Linux
brew install ffmpeg      # Mac

# Convert video to audio (for podcast)
ffmpeg -i lesson.mp4 -vn -ab 128k output.mp3

# Compress a video for web
ffmpeg -i original.mp4 -vcodec libx264 -crf 28 compressed.mp4

# Extract subtitles
ffmpeg -i video.mkv -map 0:s:0 subtitles.srt

# Add your logo watermark
ffmpeg -i video.mp4 -i logo.png -filter_complex "overlay=10:10" watermarked.mp4
```

---

## Banner & Graphic Tools

### Design Software
| Tool | Best for | Platform | Cost |
|------|---------|----------|------|
| **GIMP** | Photo editing, complex designs | Win/Mac/Linux | Free |
| **Inkscape** | Vector graphics, logos, SVG | Win/Mac/Linux | Free |
| **Penpot** | Figma alternative, design in browser | Web/self-hosted | Free |
| **Canva** | Quick social media graphics, templates | Web/App | Free tier good |
| **Gravit Designer** | Clean vector editor | Web | Free |
| **Photopea** | Photoshop in browser (no install) | photopea.com | Free |

### WordPress Banner Sizes (Quick Reference)
| Use case | Recommended size |
|----------|------------------|
| Featured image | 1200 × 628 px |
| Blog header | 1920 × 400 px |
| Square social | 1080 × 1080 px |
| YouTube thumbnail | 1280 × 720 px |
| Pinterest pin | 1000 × 1500 px |
| LinkedIn banner | 1584 × 396 px |

### Free Image Sources (No Copyright Issues)
| Site | Best for |
|------|----------|
| unsplash.com | Beautiful photography |
| pexels.com | Photos and videos |
| pixabay.com | Photos, vectors, illustrations |
| openverse.org | WordPress.org's own image search |
| undraw.co | Free SVG illustrations, customisable colour |
| storyset.com | Illustrated story graphics |
| iconscout.com | Icons, animations (free tier) |

### Generate AI Images for Banners (Free)
| Tool | Quality | Notes |
|------|---------|-------|
| **Stable Diffusion** (local) | Very good | Runs on your computer, free forever |
| **DALL-E via Bing Image Creator** | Excellent | Free, uses Microsoft credits |
| **Adobe Firefly** | Good | 25 free credits/month |
| **Ideogram** | Good text in images | Free tier available |
| **Craiyon** | OK | Unlimited free |

---

## Complete Content Creation Workflow for ELT Blogger

```
Week's plan (Sunday evening, 30 minutes):
1. Write 5 post outlines in Logseq
2. Add them to Google Sheets queue
3. Apps Script posts them as drafts automatically

Monday–Friday (morning, 30 minutes each):
1. Open one draft in WordPress
2. Add featured image (Canva, 5 minutes)
3. Proofread → Publish

Optional (when energy allows):
- Record 5-minute listening exercise in Audacity
- Upload to Anchor as podcast episode
- Link from the WordPress post
```

This gives you 5 posts + 5 podcast episodes per week from 2.5 hours of work.
