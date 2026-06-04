# Free AI Publishing: Claude, ChatGPT, and Mistral — Complete Guide

**How to use AI assistants to write, edit, and publish to WordPress — for free or near-free**  
**Last updated: June 2026**

---

## Overview: Your Free AI Stack

| AI Tool | Free Tier | Best For | Energy Required |
|---------|-----------|----------|-----------------|
| **Claude (claude.ai)** | Free — Sonnet with daily limits | Long writing, editing, code | Low |
| **Le Chat (Mistral)** | Fully free, no account needed | Quick drafts, multilingual | Very Low |
| **ChatGPT (OpenAI)** | GPT-4o mini, free | Rewriting, formatting | Low |
| **Ollama (local)** | 100% free, runs offline | Private, no internet needed | Medium (setup once) |
| **GitHub Actions** | Free for public repos | Automated publishing | Zero (runs itself) |

---

## Option 1: Claude (Recommended for Writing Quality)

### Free Use via claude.ai

1. Go to **claude.ai** and sign up with your email (free)
2. You get Claude Sonnet — excellent for long-form ELT writing
3. Paste your draft and ask:

> *"Here is my rough draft. Please: 1) Fix grammar and flow. 2) Format it as clean HTML paragraphs. 3) Write an SEO title (max 60 chars). 4) Write a meta description (max 155 chars). 5) Suggest 5 relevant tags."*

4. Copy Claude's output into your Google Sheet (Column B for content, G for SEO title, H for meta description)
5. Your Apps Script publishes it automatically

### Low-Energy Shortcut

On very bad days, just give Claude a topic:

> *"Write a 500-word ELT blog post about why students struggle with the present perfect. Include an SEO title, meta description, and 5 tags. Return as JSON."*

Copy the result into your sheet. Done. You wrote zero words.

### Claude Code CLI (Advanced — Run from Terminal)

Install Claude Code to run it from your computer's terminal:

```bash
npm install -g @anthropic-ai/claude-code
claude
```

Then ask it directly:
> "Read all .md files in my drafts/ folder and run auto_publisher.py on each one."

Claude Code can execute your scripts. You can automate the entire pipeline with one command.

### Claude API (For Automated SEO Generation)

Cost: ~$1–3/month for a blog with daily posts.

```python
# install: pip install anthropic
import anthropic
import json

client = anthropic.Anthropic(api_key="YOUR_ANTHROPIC_API_KEY")

def generate_seo(title, content_preview):
    """Auto-generate SEO title and meta description for any post."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=150,
        messages=[{
            "role": "user",
            "content": f"""Post title: {title}
            Content preview: {content_preview[:300]}
            
            Return ONLY a JSON object:
            {{"seo_title": "(max 60 chars)", "meta_description": "(max 155 chars)"}}"""
        }]
    )
    return json.loads(message.content[0].text)
```

Add this to `auto_publisher.py` — every post automatically gets optimised SEO metadata.

---

## Option 2: Mistral Le Chat (Best Completely Free Option)

**Le Chat** at **chat.mistral.ai** is:
- Completely free
- No account required for basic use
- Fast (Mistral models are very quick)
- Excellent for multilingual writing (French, English, Bengali)

### Daily Writing Workflow with Le Chat

1. Go to **chat.mistral.ai**
2. Type: *"Write a 500-word ELT post about [topic]. Return as HTML with an SEO title and meta description."*
3. Copy output → Google Sheet → Apps Script publishes it

### Mistral Free API

Sign up at **console.mistral.ai** for the free tier:
- 1 billion tokens/month free on certain models
- Mistral Nemo, Mistral 7B — fast and capable

```python
# install: pip install mistralai
from mistralai import Mistral
import json

client = Mistral(api_key="YOUR_MISTRAL_API_KEY")

def generate_post(topic):
    """Generate a full blog post on any ELT topic."""
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=[{
            "role": "user",
            "content": f"""Write a 500-word ELT teaching blog post about: {topic}
            
            Return a JSON object with:
            - "title": engaging blog title
            - "content": full HTML content (p tags)
            - "seo_title": SEO title (max 60 chars)
            - "meta_description": meta (max 155 chars)
            - "tags": comma-separated tags
            - "category": one of: Grammar, Listening & Phonology, CELTA, ELT Masterclass"""
        }]
    )
    text = response.choices[0].message.content
    start = text.find('{')
    end = text.rfind('}') + 1
    return json.loads(text[start:end])
```

---

## Option 3: ChatGPT (OpenAI)

### Free via chat.openai.com

- GPT-4o mini is free with a generous daily limit
- Same workflow as Claude: paste draft, ask for SEO + HTML

### ChatGPT API (Very Cheap)

GPT-4o mini = $0.15 per million input tokens. A 500-word post costs less than $0.001.

```python
# install: pip install openai
from openai import OpenAI

client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

def polish_post(title, draft_content):
    """Improve a draft post using ChatGPT."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an ELT blog editor. Improve grammar, flow, and readability. Return clean HTML."},
            {"role": "user", "content": f"Title: {title}\n\nDraft:\n{draft_content}"}
        ]
    )
    return response.choices[0].message.content
```

---

## Option 4: Ollama — 100% Free, Runs on Your Computer

**Ollama** lets you run AI models locally. No API key. No internet. No cost ever.

### Install Ollama

```bash
# Linux / Mac (one command)
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: download from ollama.ai

# Download and run Mistral 7B (good quality, 4.1GB download)
ollama pull mistral
ollama run mistral
```

Then talk to it in the terminal. Type your topic, get a post.

### Connect Ollama to Your Publisher

```python
import requests, json

def write_post_locally(topic):
    """Use locally-running Mistral to write a post — zero cost."""
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': 'mistral',
        'prompt': f'''Write a 500-word ELT teaching blog post about: {topic}
        
        Return JSON: {{"title": "", "content": "(HTML)", "seo_title": "", "meta_description": "", "tags": "", "category": ""}}''',
        'stream': False
    })
    text = r.json()['response']
    start = text.find('{')
    end = text.rfind('}') + 1
    return json.loads(text[start:end])
```

**Hardware needed:** 8GB RAM for Mistral 7B. 16GB RAM for better models like Llama 3.

---

## Option 5: GitHub Actions — Zero-Effort Automated Publishing

Every time you push a Markdown file to the `drafts/` folder on GitHub, this GitHub Action automatically publishes it to WordPress.

See: `.github/workflows/publish_on_push.yml` in this repository.

**Setup:**
1. Add your API key as a repository secret named `WP_API_KEY`
2. Push any `.md` file to `drafts/`
3. GitHub reads the file and sends it to WordPress
4. Cost: Free (GitHub Actions free tier is very generous)

---

## The "Write While Sleeping" Pipeline

Combine everything for a fully automated system:

```python
# ai_writer_publisher.py
# Reads topics from topics.txt, generates posts with Ollama, publishes to WordPress

import requests, json
from pathlib import Path

WP_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
WP_KEY = 'YOUR_WP_API_KEY_HERE'

def write_post(topic):
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': 'mistral',
        'prompt': f'Write a 500-word ELT blog post about "{topic}". Return JSON: {{"title":"","content":"(HTML)","seo_title":"","meta_description":"","tags":"","category":""}}',
        'stream': False
    })
    text = r.json()['response']
    return json.loads(text[text.find('{'):text.rfind('}')+1])

def publish(post):
    r = requests.post(WP_URL, json=post, headers={'X-Sourov-Key': WP_KEY})
    return r.json()

if __name__ == '__main__':
    topics_file = Path('topics.txt')
    for topic in topics_file.read_text().strip().split('\n'):
        if topic.strip():
            print(f'Generating: {topic}')
            post = write_post(topic)
            result = publish(post)
            print(f'Published: Post ID {result.get("post_id", "FAILED")}')
```

Create `topics.txt`:
```
Day 33 – Why students avoid speaking in class
Day 34 – The grammar of regret (wish + past perfect)
Day 35 – How to teach pronunciation without a phonetics degree
```

Run: `python ai_writer_publisher.py`  
Result: All three posts published to WordPress automatically.

---

## Which AI to Use Based on Your Energy Level

| Energy | Tool | What you do | What the AI does |
|--------|------|-------------|------------------|
| Very low | Le Chat (mistral.ai) | Give a topic (3 words) | Writes everything |
| Low | claude.ai | Paste rough notes | Edits into a post |
| Medium | ChatGPT | Write a first draft | Improves it |
| Good | Claude API + auto_publisher.py | Add topic to topics.txt | Generates + publishes |
| High energy | Full Ollama pipeline | Review published posts | Handles all writing |

---

## Cost Comparison (Monthly, Assuming 30 Posts)

| Service | Cost | Notes |
|---------|------|-------|
| claude.ai free tier | $0 | Rate limited |
| Le Chat (Mistral) | $0 | Unlimited |
| Ollama (local) | $0 | Electricity only |
| Mistral API free tier | $0 | 1B tokens/month free |
| ChatGPT API (GPT-4o mini) | ~$0.05 | 30 × 500-word posts |
| Claude API (Sonnet) | ~$0.90 | 30 × 500-word posts |

**Recommendation:** Use Le Chat or Ollama for volume. Use Claude for quality editing.

---

*Last updated: June 2026 · Maintained in sourovdeb/my_professional_documents*
