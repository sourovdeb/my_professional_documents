# Free and Low-Cost AI Tools for WordPress Automation

## Cloud APIs — Free Tiers

### Groq (Best Free Option — Fastest)
- **URL**: console.groq.com → API Keys
- **Free limits**: 14,400 requests/day, 6,000 tokens/min
- **Models**: Llama 3.3 70B, Mixtral 8x7B, Gemma 2
- **Quality**: High — rivals GPT-4o for SEO and categorisation tasks
- **Speed**: Fastest available (custom LPU chips)

### Google Gemini (Free Tier)
- **URL**: aistudio.google.com → Get API Key
- **Free**: 1,500 requests/day for Gemini 1.5 Flash
- **Best for**: Long documents, multi-language content

### Mistral (Free Credits on Signup)
- **URL**: console.mistral.ai
- **Best for**: French-English bilingual content (ideal for Réunion)
- **GDPR compliant** — European AI
- **Free web chat**: chat.mistral.ai (zero setup, zero cost)

### Together AI ($5 Free Credit)
- **URL**: api.together.xyz
- **Credit**: $5 on signup (lasts months at your usage)
- **Models**: Llama 3.3, Mixtral, Qwen

---

## Local Models — Completely Free

### Ollama (Recommended)
- **URL**: ollama.ai
- **Cost**: $0 forever
- **Privacy**: Data never leaves your machine
- **Requirements**: 8GB RAM minimum

```bash
# Install from ollama.ai, then:
ollama pull mistral      # 4GB, best balance
ollama pull llama3.2     # Good for creative writing
ollama pull phi3         # Lightest (2GB RAM)
ollama serve             # Start the local server
```

Python integration:
```python
import requests, json

def call_ollama(prompt: str, model='mistral') -> str:
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': model, 'prompt': prompt, 'stream': False
    }, timeout=120)
    return r.json()['response']
```

### LM Studio (GUI for Local Models)
- **URL**: lmstudio.ai
- **Best for**: Non-technical users who want local AI with a visual interface

### Jan.ai
- **URL**: jan.ai
- Daily writing assistant, runs offline

---

## Voice to Text (Low-Energy Writing)

When typing is hard, speak instead:

### Whisper (OpenAI — Free, Local, Best Accuracy)
```bash
pip install openai-whisper
whisper recording.mp3 --language en --output_format txt
# Transcribes to recording.txt — paste into your sheet
```
Also transcribes French: `--language fr`

### Google Docs Voice Typing (Easiest)
- Open Google Docs → Tools → Voice Typing
- Click microphone → speak your post
- Copy into your Queue sheet
- Requires Chrome browser, no installation

---

## AI Writing Assistants (Web-Based, Free)

| Tool | URL | Free Tier | Best Use |
|------|-----|-----------|----------|
| **Mistral Le Chat** | chat.mistral.ai | Unlimited | SEO generation, drafts |
| **Perplexity AI** | perplexity.ai | 5 searches/day | Research for posts |
| **Phind** | phind.com | Unlimited | Technical content |
| **You.com** | you.com | Unlimited | Research + writing |

---

## Using AI for Remote Automation (No Local Machine)

### GitHub Actions + DeepSeek (Zero Infrastructure Cost)
```yaml
# .github/workflows/publish_on_push.yml
# Every time you push a .md file to drafts/:
# 1. GitHub Action calls DeepSeek for SEO
# 2. Sends to WordPress as draft
# Total cost: ~$0.01/month
```
See `.github/workflows/publish_on_push.yml` for the complete workflow.

### Google Apps Script + Groq (Zero Infrastructure, Free)
```javascript
// In your sheet_publisher.gs — replace DeepSeek with Groq:
// Change model to 'llama-3.3-70b-versatile'
// Change URL to 'https://api.groq.com/openai/v1/chat/completions'
// Same JSON format (OpenAI compatible)
```

---

## AI Provider Decision Guide

```
Do I need zero cost?
├─ YES → Is my computer available?
│         ├─ YES → Ollama (most private, always free)
│         └─ NO  → Groq free tier (cloud, fast, free)
└─ NO  → What volume?
          ├─ < 100 posts/month → Groq free tier (enough)
          └─ > 100 posts/month → DeepSeek-V3 ($0.07/1M tokens)
```

**Start here**: Get a Groq API key (console.groq.com — free, instant). It handles your entire monthly volume for $0.
