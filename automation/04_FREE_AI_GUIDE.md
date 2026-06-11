# Free & Cheap AI for WordPress Publishing
## Using DeepSeek, Mistral, Ollama, Groq — Complete Guide

This guide answers: **How can I automate everything without paying for expensive AI?**

---

## The Free AI Landscape (June 2026)

| Provider | Cost | Speed | Quality | Privacy |
|---|---|---|---|---|
| **Ollama (local)** | FREE | Fast (depends on your GPU) | Good | Perfect |
| **Groq** | FREE (dev tier) | Fastest (~500 tok/s) | Good | API |
| **DeepSeek** | ~$0.001/post | Fast | Excellent | API |
| **Mistral (free tier)** | FREE | Fast | Good | API |
| **Google Gemini (free)** | FREE | Fast | Good | API |
| **Together AI** | $1 free credits | Fast | Excellent | API |
| **Anthropic** | $0.013/post | Fast | Best | API |

**Recommendation:**
- Start with **Ollama** (zero cost, totally private)
- Add **DeepSeek** when you want cloud reliability ($5 = 15 years of posts)
- Use **Groq** for speed-critical tasks (it's the fastest free option)

---

## Option 1: Ollama (Completely Free, Local)

Ollama runs AI models on your own computer. No API key, no costs, no data leaving your machine.

### Install

```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: download installer from ollama.ai
```

### Start and Pull a Model

```bash
ollama serve                    # Start server
ollama pull mistral             # 4GB — best quality/speed balance
ollama pull llama3.2:3b         # 2GB — fast on low-spec machines
ollama pull phi3                # 2.3GB — excellent for writing
ollama pull gemma3:4b           # 3GB — good at instruction following
```

### Use in Python

```python
import requests

def ask_ollama(prompt, model='mistral'):
    resp = requests.post('http://localhost:11434/api/generate', json={
        'model': model,
        'prompt': prompt,
        'stream': False
    })
    return resp.json()['response']

# Generate blog post
result = ask_ollama('Write a 500-word post about CELTA lesson planning. Return HTML.')
print(result)
```

### Use in Google Apps Script

```javascript
// Requires Ollama accessible from internet (use ngrok or Cloudflare Tunnel)
// OR run this from a local Python script instead
function callOllama(prompt) {
  const resp = UrlFetchApp.fetch('https://your-ngrok-url.ngrok.io/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({ model: 'mistral', prompt: prompt, stream: false })
  });
  return JSON.parse(resp.getContentText()).response;
}
```

**Expose Ollama publicly (for Apps Script):**
```bash
# Install ngrok (ngrok.com — free tier)
ngrok http 11434
# Copy the https URL → use in Apps Script
```

---

## Option 2: Groq (Free, Fastest)

Groq uses custom AI chips that run models at 500+ tokens/second — much faster than OpenAI.

### Setup

1. Go to **console.groq.com**
2. Sign up → API Keys → Create key
3. Free tier: 14,400 requests/day, 30,000 tokens/minute

### Use in Python

```python
import requests

def ask_groq(prompt, model='llama3-8b-8192'):
    resp = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {GROQ_API_KEY}'},
        json={
            'model': model,
            'messages': [{'role':'user','content':prompt}],
            'max_tokens': 1500
        }
    )
    return resp.json()['choices'][0]['message']['content']
```

Available free models: `llama3-8b-8192`, `llama3-70b-8192`, `mixtral-8x7b-32768`, `gemma-7b-it`

---

## Option 3: Mistral AI (Free API Tier)

Mistral is a French AI company with excellent open-source models. Free tier includes 1B tokens/month.

### Setup

1. **console.mistral.ai** → Sign up → API Keys
2. Free tier: `mistral-small-latest` model included

### Use in Python

```python
def ask_mistral(prompt):
    resp = requests.post(
        'https://api.mistral.ai/v1/chat/completions',
        headers={'Authorization': f'Bearer {MISTRAL_API_KEY}'},
        json={
            'model': 'mistral-small-latest',
            'messages': [{'role':'user','content':prompt}]
        }
    )
    return resp.json()['choices'][0]['message']['content']
```

**Mistral also has open-source models you can run locally with Ollama:**
```bash
ollama pull mistral          # Mistral 7B
ollama pull mixtral          # Mixtral 8x7B (larger, better)
```

---

## Option 4: Google Gemini (Free Tier)

1. **aistudio.google.com** → Get API key (free)
2. Free tier: 1,500 requests/day with `gemini-1.5-flash`

```python
def ask_gemini(prompt):
    resp = requests.post(
        f'https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}',
        json={'contents': [{'parts': [{'text': prompt}]}]}
    )
    return resp.json()['candidates'][0]['content']['parts'][0]['text']
```

---

## Multi-Provider Fallback System

Use multiple free providers in sequence — if one fails or runs out of quota, try the next:

```python
class FreeAIChain:
    """Try providers in order of preference until one works."""

    def __init__(self):
        self.providers = [
            ('ollama',   self._ollama),
            ('groq',     self._groq),
            ('mistral',  self._mistral),
            ('deepseek', self._deepseek),
        ]

    def ask(self, prompt: str) -> str:
        for name, fn in self.providers:
            try:
                result = fn(prompt)
                if result and len(result) > 50:
                    print(f'Used: {name}')
                    return result
            except Exception as e:
                print(f'{name} failed: {e}')
        raise Exception('All AI providers failed')

    def _ollama(self, prompt):
        r = requests.post('http://localhost:11434/api/generate',
                          json={'model':'mistral','prompt':prompt,'stream':False}, timeout=30)
        return r.json()['response']

    def _groq(self, prompt):
        r = requests.post('https://api.groq.com/openai/v1/chat/completions',
                          headers={'Authorization':f'Bearer {GROQ_KEY}'},
                          json={'model':'llama3-8b-8192',
                                'messages':[{'role':'user','content':prompt}]})
        return r.json()['choices'][0]['message']['content']

    def _mistral(self, prompt):
        r = requests.post('https://api.mistral.ai/v1/chat/completions',
                          headers={'Authorization':f'Bearer {MISTRAL_KEY}'},
                          json={'model':'mistral-small-latest',
                                'messages':[{'role':'user','content':prompt}]})
        return r.json()['choices'][0]['message']['content']

    def _deepseek(self, prompt):
        r = requests.post('https://api.deepseek.com/v1/chat/completions',
                          headers={'Authorization':f'Bearer {DEEPSEEK_KEY}'},
                          json={'model':'deepseek-chat',
                                'messages':[{'role':'user','content':prompt}]})
        return r.json()['choices'][0]['message']['content']

# Usage
ai = FreeAIChain()
result = ai.ask('Write a 500-word post about English pronunciation tips. Return HTML.')
```

---

## "Vibe Mode" — AI-Assisted Writing in Real Time

For days when motivation is low, use AI to do the heavy lifting:

1. Open your Google Doc or Logseq
2. Write just your **outline** (3-5 bullet points)
3. Run `generate_post(your_outline)` from the Python script
4. AI produces the full post
5. You edit/approve in 2 minutes
6. Post goes to WordPress as draft

This approach is especially effective for bipolar cycles — you do the creative spark (outline), the machine does the volume work.

---

## Which AI to Use When

| Situation | Best Choice |
|---|---|
| Daily automation, no internet needed | Ollama (local) |
| Best quality, ultra-cheap | DeepSeek |
| Fastest response time | Groq |
| Code generation | DeepSeek Coder or Groq |
| Complex reasoning / planning | DeepSeek R1 |
| Image generation | Stable Diffusion (local) |
| Voice synthesis | Kokoro TTS or Edge TTS |
