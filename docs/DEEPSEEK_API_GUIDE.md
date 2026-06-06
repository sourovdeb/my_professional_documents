# DeepSeek API Guide: The Budget-Friendly AI for WordPress Automation

## Why DeepSeek? Cost Comparison (2026)

| Provider | Model | Input /1M tokens | Output /1M tokens | Free Tier |
|----------|-------|-----------------|-------------------|-----------|
| **DeepSeek** | deepseek-chat (V3) | **$0.07** | **$1.10** | No |
| **Groq** | llama-3.3-70b | $0.59 | $0.79 | **Yes** |
| Anthropic | claude-sonnet-4 | $3.00 | $15.00 | No |
| OpenAI | gpt-4o | $2.50 | $10.00 | No |
| Mistral | mistral-large | $2.00 | $6.00 | Free credits |
| **Ollama** | mistral/llama3 | **$0** | **$0** | **Always free** |

**DeepSeek is 20–40x cheaper than Anthropic for equivalent quality.**

For your use case (~30 posts/month, ~2000 tokens each):
- Anthropic: ~$0.45/month
- DeepSeek-V3: ~$0.024/month
- Annual saving: ~$5 — essentially free

---

## Setting Up DeepSeek

1. Go to **platform.deepseek.com** → Sign Up
2. Dashboard → **API Keys** → Create new key (starts with `sk-`)
3. Copy it immediately — you cannot see it again
4. Store in `.env` file (never commit to GitHub)
5. Optional: add $5 minimum balance (lasts months at this usage level)

---

## DeepSeek in Google Apps Script

```javascript
/**
 * Auto-generate SEO metadata using DeepSeek.
 * Cost per call: ~$0.0008
 */
function generateSEOWithDeepSeek(title, content) {
  const DEEPSEEK_KEY = PropertiesService.getScriptProperties()
    .getProperty('DEEPSEEK_KEY');

  const prompt = `Return ONLY valid JSON, no markdown fences:
Title: ${title}\nContent excerpt: ${content.substring(0, 300)}

{"seo_title": "under 60 chars", "meta_desc": "under 160 chars",
 "tags": ["tag1","tag2","tag3"], "category": "ELT Masterclass"}`;

  try {
    const res = UrlFetchApp.fetch(
      'https://api.deepseek.com/v1/chat/completions',
      {
        method: 'POST',
        headers: {
          'Authorization': 'Bearer ' + DEEPSEEK_KEY,
          'Content-Type': 'application/json'
        },
        payload: JSON.stringify({
          model: 'deepseek-chat',
          messages: [{ role: 'user', content: prompt }],
          temperature: 0.2,
          max_tokens: 250
        }),
        muteHttpExceptions: true
      }
    );
    const data = JSON.parse(res.getContentText());
    if (data.error) throw new Error(data.error.message);
    let text = data.choices[0].message.content;
    text = text.replace(/```json\n?/g, '').replace(/```\n?/g, '').trim();
    return JSON.parse(text);
  } catch (e) {
    Logger.log('DeepSeek error: ' + e.message);
    return { seo_title: title.substring(0,60), meta_desc: '', tags: [], category: 'ELT Masterclass' };
  }
}

// Run ONCE to store key securely, then DELETE this function
function storeAPIKeys() {
  PropertiesService.getScriptProperties().setProperties({
    'DEEPSEEK_KEY': 'sk-paste-your-key-here',
    'WP_KEY': 'your-wordpress-plugin-key'
  });
  Logger.log('Keys stored.');
}
```

---

## DeepSeek in Python

```python
import os, json, requests
from dotenv import load_dotenv
load_dotenv()

def generate_seo_deepseek(title: str, content: str) -> dict:
    prompt = f"""Return ONLY valid JSON, no markdown:
Title: {title}\nExcerpt: {content[:300]}
{{"seo_title": "", "meta_desc": "", "tags": [], "category": ""}}"""

    try:
        r = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={
                'Authorization': f'Bearer {os.getenv("DEEPSEEK_API_KEY")}',
                'Content-Type': 'application/json'
            },
            json={
                'model': 'deepseek-chat',
                'messages': [{'role': 'user', 'content': prompt}],
                'temperature': 0.2,
                'max_tokens': 250
            },
            timeout=30
        )
        r.raise_for_status()
        text = r.json()['choices'][0]['message']['content']
        text = text.replace('```json','').replace('```','').strip()
        return json.loads(text)
    except Exception as e:
        print(f'DeepSeek error: {e}')
        return {'seo_title': title[:60], 'meta_desc': content[:155], 'tags': [], 'category': 'ELT Masterclass'}
```

---

## Free Alternatives

### Groq (Fastest, Free Cloud)
```javascript
// Google Apps Script using Groq free tier
function generateSEOWithGroq(title, content) {
  const GROQ_KEY = PropertiesService.getScriptProperties().getProperty('GROQ_KEY');
  const res = UrlFetchApp.fetch('https://api.groq.com/openai/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': 'Bearer ' + GROQ_KEY, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'llama-3.3-70b-versatile',
      messages: [{ role: 'user', content:
        'Return ONLY JSON: {"seo_title":"","meta_desc":"","tags":[],"category":""} for title: ' + title
      }],
      temperature: 0.2, max_tokens: 200
    })
  });
  const data = JSON.parse(res.getContentText());
  return JSON.parse(data.choices[0].message.content);
}
```
Get free key: **console.groq.com** → API Keys

### Ollama (Completely Free, Local)
```bash
# Install: ollama.ai
ollama pull mistral
ollama serve
```
```python
def generate_seo_ollama(title, content):
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': 'mistral',
        'prompt': f'JSON only: {{"seo_title":"","meta_desc":"","tags":[]}} for: {title}',
        'stream': False
    }, timeout=60)
    return json.loads(r.json()['response'])
```

### Mistral "Vibe Mode" (Free Web Chat)
For zero-setup: open **chat.mistral.ai**, paste your post, ask:
> "Generate SEO title (under 60 chars), meta description (under 160 chars), and 5 tags as JSON."
Copy the JSON into your sheet columns G and H. Done. Completely free.

---

## .env Template

```ini
# Save as .env — add to .gitignore, NEVER commit
DEEPSEEK_API_KEY=sk-your-key
GROQ_API_KEY=gsk_your-key
MISTRAL_API_KEY=your-key
WP_URL=https://sourovdeb.com
WP_API_KEY=your-wordpress-plugin-key
WP_USER=your-wp-email
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

## Decision Guide

| Situation | Use |
|-----------|-----|
| Need free, fast, cloud | Groq free tier |
| Need cheapest paid | DeepSeek-V3 |
| Need privacy / offline | Ollama |
| Batch 100+ posts | DeepSeek (cheapest per token) |
| Quick one-off | Mistral chat.mistral.ai (web) |
