# Free AI Remote Publishing Guide
## Use ChatGPT, Mistral, Gemini & Others for Zero-Cost Content Creation

> **Goal:** Publish WordPress posts using AI without paying anything (or paying very little). This guide covers every free AI option and how to connect them to your WordPress.

---

## OPTION 1: Ollama (Completely Free, Forever)

### What It Is
Ollama runs AI models locally on your computer. No internet for inference, no API key, no cost. The models download once and run forever.

### Install
```bash
# Linux/Mac
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: download from ollama.ai

# Start the server
ollama serve
```

### Best Free Models (2026)

| Model | Size | Quality | Use Case |
|-------|------|---------|----------|
| `mistral` | 4.1 GB | Good | General writing, blog posts |
| `phi3` | 2.3 GB | Good | Fast, lightweight |
| `llama3` | 4.7 GB | Very good | Best quality free |
| `gemma2` | 5.4 GB | Very good | Google's model, strong |
| `neural-chat` | 4.1 GB | Good | Optimized for conversation |

```bash
ollama pull mistral
ollama pull phi3    # If computer is slow
ollama pull llama3  # If you want best quality
```

### Use Ollama with Your WordPress Publisher

```python
import requests, json

def generate_with_ollama(topic, model='mistral'):
    prompt = f'''Write a WordPress blog post about: "{topic}"
Length: ~600 words. Tone: educational.
Return ONLY valid JSON:
{{
  "title": "compelling title",
  "content": "full HTML with h2, p, ul tags",
  "meta_description": "under 160 chars",
  "tags": ["3-5 tags"]
}}'''
    
    r = requests.post('http://localhost:11434/api/generate', json={
        'model': model,
        'prompt': prompt,
        'stream': False
    })
    
    raw = r.json()['response']
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)
```

**Tip:** If your computer is old/slow, use `phi3` — it's the lightest model that still writes decent blog posts.

---

## OPTION 2: Google Gemini (Free API, 1500 req/day)

### Get Free API Key
1. Go to **aistudio.google.com**
2. Click "Get API key"
3. Click "Create API key"
4. Copy the key (starts with `AIza`)

### Free Limits (as of June 2026)
- **Gemini 1.5 Flash:** 1,500 requests/day, 1,000,000 tokens/minute
- **Gemini 1.5 Pro:** 50 requests/day (more capable)

### Python Integration

```python
import os, requests, json

GEMINI_KEY = os.getenv('GEMINI_API_KEY')

def generate_with_gemini(topic, model='gemini-1.5-flash'):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_KEY}'
    
    prompt = f'''Write a WordPress blog post about: "{topic}"
Length: ~600 words. Tone: educational for ELT teachers.
Return ONLY valid JSON with: title, content (HTML), meta_description, tags (array).'''
    
    r = requests.post(url, json={
        'contents': [{'parts': [{'text': prompt}]}],
        'generationConfig': {'maxOutputTokens': 2000, 'temperature': 0.7}
    })
    
    raw = r.json()['candidates'][0]['content']['parts'][0]['text']
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)
```

### Google Apps Script Integration

```javascript
function generateWithGemini(topic) {
  const key = PropertiesService.getScriptProperties().getProperty('GEMINI_KEY');
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' + key;
  
  const prompt = `Write a WordPress blog post about: "${topic}"
Return ONLY valid JSON: {"title": "...", "content": "HTML...", "meta_description": "...", "tags": []}`;
  
  const response = UrlFetchApp.fetch(url, {
    method: 'POST',
    contentType: 'application/json',
    payload: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] }),
    muteHttpExceptions: true
  });
  
  const data = JSON.parse(response.getContentText());
  let raw = data.candidates[0].content.parts[0].text;
  raw = raw.replace(/```json\n?/g, '').replace(/```/g, '').trim();
  return JSON.parse(raw);
}
```

---

## OPTION 3: Mistral AI (Free Experimental Tier)

### Get Free API Key
1. Go to **console.mistral.ai**
2. Create account
3. Go to API Keys → Create new key
4. Check current free tier limits (changes frequently)

### Python Integration (Same as DeepSeek format)

```python
import os, requests, json

MISTRAL_KEY = os.getenv('MISTRAL_API_KEY')

def generate_with_mistral(topic):
    r = requests.post(
        'https://api.mistral.ai/v1/chat/completions',
        headers={'Authorization': f'Bearer {MISTRAL_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'mistral-small-latest',  # Free tier model
            'messages': [{'role': 'user', 'content': f'Write an ELT blog post about: {topic}. Return JSON with title, content, meta_description, tags.'}],
            'max_tokens': 1500
        }
    )
    raw = r.json()['choices'][0]['message']['content']
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)
```

---

## OPTION 4: ChatGPT Free Tier (Manual, Browser-Based)

ChatGPT's free tier doesn't have an API, but you can use it manually:

### Template Prompt (Copy-Paste)

Open **chatgpt.com** and paste:

```
Write a WordPress blog post for my ELT teaching blog.

Topic: [YOUR TOPIC HERE]
Tone: Educational and friendly
Length: 500-600 words
Audience: English language teachers and advanced learners

Format your response as ONLY this JSON:
{
  "title": "compelling post title",
  "content": "full HTML content using <h2>, <p>, <ul>, <li> tags",
  "meta_description": "under 160 character SEO description",
  "tags": ["3", "to", "5", "tags"],
  "category": "ELT Masterclass"
}
```

Then copy the JSON output, paste into your Google Sheet, and the publisher script handles the rest.

### Semi-Automation with ChatGPT + Google Sheets

```javascript
// In Apps Script: manually paste ChatGPT output into a 'generated' tab
// Then this function imports it to the Queue tab
function importFromChatGPT() {
  const source = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('ChatGPT_Paste');
  const queue  = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  
  const json = source.getRange('A1').getValue();
  if (!json) return;
  
  const post = JSON.parse(json);
  const nextRow = queue.getLastRow() + 1;
  
  queue.getRange(nextRow, 1, 1, 8).setValues([[
    post.title,
    post.content,
    post.category || 'ELT Masterclass',
    (post.tags || []).join(', '),
    'draft',
    '',
    post.title,
    post.meta_description
  ]]);
  
  // Clear the paste area
  source.getRange('A1').clearContent();
  Logger.log('Imported: ' + post.title);
}
```

---

## OPTION 5: OpenRouter (Access Multiple Free Models)

**OpenRouter** is a gateway that gives you access to 100+ models, many free.

1. Go to **openrouter.ai**
2. Create account (free)
3. Get API key
4. Use models with `:free` suffix (e.g., `meta-llama/llama-3-8b-instruct:free`)

```python
import requests

OR_KEY = os.getenv('OPENROUTER_KEY')

def generate_with_openrouter(topic):
    r = requests.post(
        'https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {OR_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://sourovdeb.com'  # Your site
        },
        json={
            'model': 'meta-llama/llama-3-8b-instruct:free',  # Free model
            'messages': [{
                'role': 'user',
                'content': f'Write an ELT blog post about: {topic}. Return JSON with title, content, meta_description, tags.'
            }]
        }
    )
    raw = r.json()['choices'][0]['message']['content']
    return json.loads(raw.replace('```json','').replace('```','').strip())
```

**Free models on OpenRouter (June 2026):**
- `meta-llama/llama-3-8b-instruct:free`
- `google/gemma-7b-it:free`
- `mistralai/mistral-7b-instruct:free`
- `nousresearch/nous-capybara-7b:free`

---

## Full Free Stack Recommendation

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| You have a decent laptop | Ollama + Mistral | Free, private, offline |
| You want cloud-based | Gemini Flash | 1500 free calls/day |
| You want variety | OpenRouter free tier | Access many models |
| You want best quality free | Gemini 1.5 Pro (50/day) | Strongest free model |
| You want zero setup | ChatGPT (manual) | Paste prompt, copy JSON |

---

## Complete Auto-Publisher (Multi-Provider Fallback)

```python
import os, requests, json, time

class MultiProviderPublisher:
    def __init__(self):
        self.providers = ['ollama', 'gemini', 'openrouter']  # Try in order
    
    def generate(self, topic):
        for provider in self.providers:
            try:
                print(f'Trying {provider}...')
                result = getattr(self, f'_generate_{provider}')(topic)
                print(f'Success with {provider}')
                return result
            except Exception as e:
                print(f'{provider} failed: {e}')
                time.sleep(1)
        raise Exception('All providers failed')
    
    def _generate_ollama(self, topic):
        r = requests.post('http://localhost:11434/api/generate',
            json={'model': 'mistral', 'prompt': self._prompt(topic), 'stream': False},
            timeout=60
        )
        raw = r.json()['response']
        return self._parse(raw)
    
    def _generate_gemini(self, topic):
        key = os.getenv('GEMINI_API_KEY')
        r = requests.post(
            f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}',
            json={'contents': [{'parts': [{'text': self._prompt(topic)}]}]}
        )
        raw = r.json()['candidates'][0]['content']['parts'][0]['text']
        return self._parse(raw)
    
    def _generate_openrouter(self, topic):
        key = os.getenv('OPENROUTER_KEY')
        r = requests.post('https://openrouter.ai/api/v1/chat/completions',
            headers={'Authorization': f'Bearer {key}'},
            json={'model': 'meta-llama/llama-3-8b-instruct:free',
                  'messages': [{'role': 'user', 'content': self._prompt(topic)}]}
        )
        raw = r.json()['choices'][0]['message']['content']
        return self._parse(raw)
    
    def _prompt(self, topic):
        return f'''Write an ELT blog post about: "{topic}"
Return ONLY JSON: {{"title": "...", "content": "HTML...", "meta_description": "...", "tags": []}}'''
    
    def _parse(self, raw):
        raw = raw.replace('```json', '').replace('```', '').strip()
        return json.loads(raw)
```

---

*Last updated: June 2026 | Free tier limits change frequently — check provider sites*
