# Free AI Tools for Remote WordPress Publishing
## ChatGPT Free, Mistral, DeepSeek — Your Options Without Paying

---

## The Honest Overview

| Tool | Free tier | Quality | API? | Best use |
|------|-----------|---------|------|----------|
| **Ollama (local)** | Unlimited free | Good | Yes | Full automation, private |
| **DeepSeek Chat** | Web UI free | Excellent | Paid (cheap) | Best paid-API value |
| **Mistral Le Chat** | Free web + API trial | Very good | Yes (free tier) | Europe-hosted, privacy |
| **ChatGPT Free** | GPT-4o mini, limited | Good | Paid only | Manual writing |
| **Gemini Free** | Generous free tier | Good | Yes (free tier) | Google Workspace integration |
| **Hugging Face** | Free inference | Variable | Yes | Open models |

---

## Option 1: Ollama (Completely Free Forever)

Ollama runs AI models on your own computer. No API key. No cost. No internet required after install.

### Install

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: download installer from ollama.com
```

### Start and pull a model

```bash
ollama serve                  # Start the server
ollama pull mistral           # 4 GB, excellent quality
ollama pull llama3.2          # 2 GB, faster, slightly lower quality
ollama pull gemma2:2b         # 1.6 GB, lightweight
```

### Use Ollama as your WordPress AI

Replace any DeepSeek/Anthropic API call with:

```python
import requests

def ollama_generate(prompt: str, model: str = 'mistral') -> str:
    r = requests.post('http://localhost:11434/api/generate',
        json={
            'model':  model,
            'prompt': prompt,
            'stream': False
        },
        timeout=120
    )
    return r.json()['response']

# Example
post_content = ollama_generate(
    'Write a 500-word ELT blog post about minimal pairs. Return only HTML.'
)
```

For Google Apps Script (must be on internet, can’t reach localhost):
- Use **ngrok** to expose your local Ollama: `ngrok http 11434`
- Use the ngrok URL in your script
- OR run Ollama on a cheap VPS ($5/month DigitalOcean)

### Recommended models by task

| Task | Recommended model |
|------|------------------|
| Blog posts, emails | `mistral` or `llama3.2` |
| Code generation | `codellama` or `qwen2.5-coder` |
| Structured JSON output | `mistral` (reliable JSON) |
| Fast drafts on slow PC | `gemma2:2b` |

---

## Option 2: Mistral (Free API Tier)

Mistral AI offers a **free API tier** (rate-limited but usable).

### Get a free API key

1. Go to **console.mistral.ai**
2. Sign up
3. Go to API Keys → Create new key
4. Free tier: ~1 request/second, limited tokens per month

### Use Mistral in Apps Script

```javascript
function callMistral(systemPrompt, userPrompt) {
  const key = PropertiesService.getScriptProperties().getProperty('MISTRAL_KEY');

  const res = UrlFetchApp.fetch('https://api.mistral.ai/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + key,
      'Content-Type':  'application/json'
    },
    payload: JSON.stringify({
      model: 'mistral-small-latest',  // Free tier
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user',   content: userPrompt }
      ],
      max_tokens: 1500
    }),
    muteHttpExceptions: true
  });

  const data = JSON.parse(res.getContentText());
  return data.choices[0].message.content;
}
```

### Mistral models on free tier

- `mistral-small-latest` — good for writing
- `open-mistral-7b` — open weights, fastest
- `open-mixtral-8x7b` — better quality

---

## Option 3: Gemini (Google’s Free Tier)

Google gives a generous free tier for Gemini API — currently **1,500 requests/day** on the free plan.

### Get API key

1. Go to **aistudio.google.com**
2. Click **Get API key**
3. Select or create a project
4. Copy the key

### Use in Apps Script (most natural integration)

```javascript
function callGemini(prompt) {
  const key = PropertiesService.getScriptProperties().getProperty('GEMINI_KEY');
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/' +
              'gemini-1.5-flash:generateContent?key=' + key;

  const res = UrlFetchApp.fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }]
    }),
    muteHttpExceptions: true
  });

  const data = JSON.parse(res.getContentText());
  return data.candidates[0].content.parts[0].text;
}
```

---

## Option 4: Using ChatGPT Free for Manual Writing

ChatGPT’s free tier (GPT-4o mini) cannot be automated via API without paying, but you can use it for **template-based manual writing** that feeds your automation:

1. Open ChatGPT free
2. Paste: `Write a 500-word ELT blog post about [topic]. Return HTML with <h2> and <p> tags.`
3. Copy the output
4. Paste into your Google Sheet column B
5. Set status to `ready`
6. Your automation script publishes it

The automation still saves you all the WordPress admin work.

---

## Option 5: Hugging Face Inference API

Free tier: 30,000 tokens/month.

```python
import requests

def huggingface_generate(prompt: str) -> str:
    HF_TOKEN = os.environ.get('HF_TOKEN', '')
    model = 'mistralai/Mistral-7B-Instruct-v0.3'

    r = requests.post(
        f'https://api-inference.huggingface.co/models/{model}',
        headers={'Authorization': f'Bearer {HF_TOKEN}'},
        json={'inputs': prompt, 'parameters': {'max_new_tokens': 800}},
        timeout=60
    )
    return r.json()[0]['generated_text'].replace(prompt, '').strip()
```

---

## The Free Stack Recommendation

For day-to-day use with zero ongoing cost:

```
1. Writing environment:  Google Docs (free)
2. AI generation:        Ollama with Mistral (free, local)
3. Spreadsheet control: Google Sheets + Apps Script (free)
4. Publishing:          Your WordPress REST API (already set up)
5. Version control:     GitHub (free)
6. Job hunting AI:      Mistral free API tier
```

Total monthly cost: **$0**

When you want faster or better quality: upgrade to DeepSeek API (~$1-2/month for your volume).

---

## Quick Comparison: Which to Use When

| Scenario | Use |
|----------|-----|
| Fully automated, zero cost | Ollama (local) |
| Automated, tiny cost | DeepSeek API |
| In Google Apps Script, free | Mistral free tier or Gemini free tier |
| Best quality for important posts | DeepSeek R1 or Anthropic API |
| No API setup, manual writing | ChatGPT free web + copy to sheet |
| Privacy-critical content | Ollama (stays on your machine) |
