# Free & Cheap AI Tools for Automation — Complete Guide

> Covers: Ollama (local/free), DeepSeek (nearly free), Mistral (free tier + "vibe mode"), ChatGPT free limits, Gemini free tier, and how to use them for WordPress publishing without spending money.

---

## Price Comparison (June 2026)

| Tool | Free Tier | API Cost | Best For | Runs Locally? |
|------|-----------|----------|----------|--------------|
| **Ollama** | Unlimited | Free forever | Privacy, daily use | Yes |
| **Jan.ai** | Unlimited | Free forever | GUI for local models | Yes |
| **DeepSeek V3** | 500K tok/day | $0.27/M input | Batch automation | No (API) |
| **Groq (Llama/Mixtral)** | 14,400 req/day | $0.06/M | Speed | No (API) |
| **Gemini 1.5 Flash** | 1M tok/day | $0.075/M | Google integration | No (API) |
| **Mistral Le Chat** | Unlimited chat | $0.06/M (API) | Writing, vibe mode | Yes (Ollama) |
| **ChatGPT free** | GPT-4o mini | $0.15/M (API) | Creative writing | No |
| **Hugging Face** | Throttled | Free for small models | Experimentation | Yes (download) |
| **Together AI** | $25 credit | $0.20/M | Model variety | No (API) |
| **LM Studio** | Unlimited | Free forever | GUI + local models | Yes |

---

## 1. Ollama — The Best Free Option

**What it is:** A tool that runs AI models on YOUR computer. No API key. No internet needed. No cost ever. Data never leaves your machine.

**System requirements:** 8GB+ RAM recommended (4GB minimum for small models).

### Setup

```bash
# 1. Download from ollama.com → click Download
# 2. Install normally (like any app)
# 3. Open Terminal and pull a model:
ollama pull mistral       # 4.1 GB — fast, great quality
ollama pull llama3        # 4.7 GB — Meta's best
ollama pull deepseek-r1   # 4.7 GB — best for structured tasks
ollama pull phi3          # 2.3 GB — fast, small footprint

# 4. Start the server:
ollama serve

# 5. Test in browser: http://localhost:11434
```

### Use Ollama for WordPress automation

```python
import requests

def ask_ollama(prompt, model='mistral'):
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': model,
        'prompt': prompt,
        'stream': False
    })
    return r.json()['response']

# Generate SEO tags for a post
tags = ask_ollama(
    'Generate 5 SEO tags for an ELT blog post titled '
    '"Active Listening in the Classroom". Return only a comma-separated list.'
)
print(tags)
# Output: active listening, ELT techniques, language learning, classroom strategies, CELTA
```

### GUI options for Ollama (no terminal required)

| Tool | URL | Description |
|------|-----|-------------|
| **Open WebUI** | github.com/open-webui/open-webui | ChatGPT-like interface, runs in browser |
| **Msty** | msty.app | Beautiful desktop app, easy to use |
| **Jan.ai** | jan.ai | Full offline AI assistant |
| **LM Studio** | lmstudio.ai | Best for trying different models |

---

## 2. DeepSeek — Best Cheap API

Full guide in `docs/DEEPSEEK_API_GUIDE.md`. Summary:

- **Free:** 500,000 tokens/day
- **Paid:** $0.27 per million input tokens
- **30 posts/month cost:** $0.004 (less than one cent)
- **Quality:** Excellent for structured tasks (tags, categories, SEO)
- **Sign up:** platform.deepseek.com

---

## 3. Mistral AI — The Free European Option

### Option A: Mistral Le Chat (Free, No API Needed)

1. Go to **chat.mistral.ai** (free account)
2. Type your rough notes or bullet points
3. Ask: "Write a 500-word ELT blog post about [topic]. Use a warm, direct voice. Structure: hook, 3 teaching points, one exercise, conclusion."
4. Copy output to your Google Sheets queue

This is the "vibe mode" — you write rough notes, Mistral writes the full post, you paste and queue it.

**Mistral Le Chat features (free):**
- Canvas mode (edit documents inline)
- Web search
- Image understanding
- Very good at English writing tasks

### Option B: Mistral via Groq API (Fastest Free API)

Groq runs Mistral models at extraordinary speed (hundreds of tokens/second).

```python
from groq import Groq  # pip install groq

client = Groq(api_key='your-groq-key')  # get key at console.groq.com
response = client.chat.completions.create(
    model='mixtral-8x7b-32768',
    messages=[{'role': 'user', 'content': 'Generate 5 tags for: Day 32 Listening'}]
)
print(response.choices[0].message.content)
```

Free tier: **14,400 requests/day** — more than enough for any blog.

### Option C: Mistral Locally via Ollama (Best Privacy)

```bash
ollama pull mistral  # runs on your computer, completely free
```

---

## 4. Google Gemini — Best Free Tier for Google Users

**Free tier:** 1 million tokens/day on Gemini 1.5 Flash.

Best for: People already in the Google ecosystem (Gmail, Sheets, Drive).

### In Google Apps Script (no API key needed!)

```javascript
// Apps Script has built-in Gemini access
function generateTagsWithGemini(title) {
  var model = LanguageApp.getGenerativeModel({ model: 'gemini-pro' });
  var result = model.generateContent(
    'Generate 5 SEO tags for ELT blog post: "' + title + '". Return comma-separated list only.'
  );
  return result.getResponse().text();
}
```

### In Python

```python
import google.generativeai as genai  # pip install google-generativeai

genai.configure(api_key='your-key')  # get at aistudio.google.com
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content('Generate 5 tags for: Day 32 Listening')
print(response.text)
```

---

## 5. ChatGPT — What Is Actually Free

**ChatGPT.com free tier:**
- GPT-4o mini access (limited)
- No automation API access
- Limited daily messages

**For automation:** You need the API ($5 free credit when you sign up).

```python
from openai import OpenAI  # pip install openai

client = OpenAI(api_key='sk-your-key')
response = client.chat.completions.create(
    model='gpt-4o-mini',  # Cheapest: $0.15/M input
    messages=[{'role': 'user', 'content': 'Generate 5 tags for ELT post about listening'}]
)
print(response.choices[0].message.content)
```

**Verdict:** For automation, DeepSeek or Ollama provide better value. Use ChatGPT manually for creative help.

---

## 6. Recommended Free Stack (Zero Monthly Cost)

```
Writing (notes):      Logseq or Google Docs  — Free
AI writing polish:    Mistral Le Chat         — Free
AI tags/categories:   Ollama (local)          — Free forever
Queue management:     Google Sheets           — Free
Auto-publishing:      Google Apps Script      — Free
Version control:      GitHub                  — Free
Total monthly cost:   $0.00
```

### If you want API-based (more reliable for batch jobs):

```
AI metadata:          DeepSeek V3             — ~$0.004/month
Fast responses:       Groq (Mixtral)          — Free tier
Total monthly cost:   < $0.01
```

---

## 7. Choosing the Right Tool for Each Task

| Task | Best Tool | Why |
|------|-----------|-----|
| Write a blog post | Mistral Le Chat (free) | Best creative writing on free tier |
| Generate tags/categories | Ollama locally | Free, fast, private |
| Batch fix 100 posts | DeepSeek API | Cheap, handles bulk well |
| Research a topic | Perplexity AI (free) | Has web search built in |
| Summarize a PDF | Gemini 1.5 Flash (free) | Huge context window |
| Code assistance | DeepSeek Coder (free local) | Excellent at code |
| Voice to text | Whisper via Ollama | Free, local, accurate |

---

## 8. Setting Up the Full Free Stack (Step by Step)

1. **Install Ollama:** ollama.com → Download → `ollama pull mistral`
2. **Install Open WebUI:** `docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway ghcr.io/open-webui/open-webui:main`
3. **Get DeepSeek free key:** platform.deepseek.com → Sign up
4. **Get Groq free key:** console.groq.com → Sign up
5. **Set up Google Apps Script:** Already in your spreadsheet → Extensions → Apps Script

All steps above are free. You will spend $0/month.
