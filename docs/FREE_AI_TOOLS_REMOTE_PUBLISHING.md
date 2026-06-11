# Free & Cheap AI Tools for Remote WordPress Publishing
## ChatGPT, Mistral, DeepSeek, Ollama — What to Use and How

## The Four Options (Honest Comparison)

### Option 1: DeepSeek API (Recommended — Cheapest Paid)
- **Cost**: ~$0.18/year for daily blogging
- **Quality**: Excellent for content writing, ELT topics
- **Setup time**: 10 minutes
- **Works offline**: No (cloud)
- **Best for**: Anyone who wants AI quality without paying much

**Quick start:**
```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Write a 300-word ELT blog post about phrasal verbs"}]}'
```

---

### Option 2: Mistral API (Free Tier Available)
- **Free tier**: `mistral-small` model is genuinely free
- **Paid models**: Mistral Medium/Large for heavier tasks
- **Setup**: Register at console.mistral.ai
- **Best for**: Trying AI publishing at zero cost

**Python example:**
```python
import requests

def call_mistral(prompt: str, model: str = 'mistral-small-latest') -> str:
    r = requests.post(
        'https://api.mistral.ai/v1/chat/completions',
        headers={'Authorization': 'Bearer YOUR_MISTRAL_KEY', 'Content-Type': 'application/json'},
        json={
            'model': model,
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 1500,
        }
    )
    return r.json()['choices'][0]['message']['content']

result = call_mistral('Write an ELT blog post about teaching listening skills')
print(result)
```

---

### Option 3: Ollama — Completely Free, Runs Locally

Ollama runs AI models on your own computer. No API keys. No costs. No internet needed.

**Install:**
```bash
# Linux / Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Then pull a model (one-time download):
ollama pull llama3      # good quality, 4.7GB
ollama pull mistral     # fast, 4.1GB
ollama pull phi3        # smallest, 2.3GB — works on older computers
```

**Use from Python:**
```python
import requests

def call_ollama(prompt: str, model: str = 'llama3') -> str:
    r = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': model, 'prompt': prompt, 'stream': False}
    )
    return r.json()['response']

post = call_ollama('Write a 500-word blog post about English listening strategies')
print(post)
```

**Pros:** Free forever, private, works without internet
**Cons:** Needs a decent computer (8GB RAM minimum), slightly slower than cloud

---

### Option 4: Groq API (Free Tier — Fastest)

Groq uses special chips that run AI models very fast. Free tier is generous.

- Free: 14,400 requests/day on LLaMA3 70B
- Speed: Noticeably faster than other providers
- Quality: LLaMA3 70B is excellent

```python
import requests

def call_groq(prompt: str) -> str:
    r = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': 'Bearer YOUR_GROQ_KEY', 'Content-Type': 'application/json'},
        json={
            'model': 'llama3-70b-8192',
            'messages': [{'role': 'user', 'content': prompt}],
        }
    )
    return r.json()['choices'][0]['message']['content']
```

Get a free key at: console.groq.com

---

## Universal Wrapper: Switch Between All Providers

This script lets you use any of the above with one function call.

```python
# ai_provider.py
import os, requests

PROVIDER = os.environ.get('AI_PROVIDER', 'ollama')  # default to free local

def generate(prompt: str, system: str = '') -> str:
    if PROVIDER == 'deepseek':
        return _call_openai_compat(
            'https://api.deepseek.com/v1/chat/completions',
            os.environ['DEEPSEEK_KEY'], 'deepseek-chat', system, prompt)

    if PROVIDER == 'mistral':
        return _call_openai_compat(
            'https://api.mistral.ai/v1/chat/completions',
            os.environ['MISTRAL_KEY'], 'mistral-small-latest', system, prompt)

    if PROVIDER == 'groq':
        return _call_openai_compat(
            'https://api.groq.com/openai/v1/chat/completions',
            os.environ['GROQ_KEY'], 'llama3-70b-8192', system, prompt)

    # Default: Ollama (free, local)
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': os.environ.get('OLLAMA_MODEL', 'llama3'),
        'prompt': (system + '\n\n' + prompt) if system else prompt,
        'stream': False
    })
    return r.json()['response']

def _call_openai_compat(url, key, model, system, prompt):
    messages = []
    if system: messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': prompt})
    r = requests.post(url,
        headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'},
        json={'model': model, 'messages': messages, 'max_tokens': 2000},
        timeout=60)
    r.raise_for_status()
    return r.json()['choices'][0]['message']['content']
```

Usage:
```bash
export AI_PROVIDER=deepseek
export DEEPSEEK_KEY=sk-...
python -c "from ai_provider import generate; print(generate('Write a blog post about ELT listening'))"

# Switch to free local:
export AI_PROVIDER=ollama
python -c "from ai_provider import generate; print(generate('Write a blog post about ELT listening'))"
```

---

## Google Apps Script: Which AI to Use?

Apps Script makes HTTPS requests. You can use DeepSeek or Mistral directly.
Ollama doesn't work from Apps Script because it runs locally.

**Recommended for Apps Script:** DeepSeek (cheapest) or Mistral free tier.

---

## Vibe Coding Mode: Using AI to Help You Write Scripts

"Vibe coding" = describing what you want in plain English and having AI write the code.

**How to do it:**
1. Open ChatGPT, Mistral Chat, or DeepSeek Chat (all have free web interfaces)
2. Describe exactly what you need:

> "Write me a Python script that reads markdown files from a folder called wordpress_queue, extracts the first line as the title, sends the rest as content to my WordPress API at https://sourovdeb.com/wp-json/sourov/v1/ai-post using the header X-Sourov-Key, and moves the file to a processed/ folder when done."

3. Copy the generated code
4. Run it — if there's an error, paste the error back and ask AI to fix it

This is how many professionals work now. You don't need to memorise syntax.
