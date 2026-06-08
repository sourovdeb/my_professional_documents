# DeepSeek API Automation Guide
## Why DeepSeek + Full Integration for WordPress, Google Sheets & Scripts

> **Summary:** DeepSeek-V3 costs ~$0.27/1M input tokens — roughly 10–40x cheaper than GPT-4o or Anthropic models. For someone publishing 500 words/day, a full month of AI-assisted publishing costs less than $0.50.

---

## 1. Cost Comparison (June 2026)

| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) | Free Tier |
|----------|-------|----------------------|------------------------|----------|
| **DeepSeek** | deepseek-chat (V3) | **$0.27** | **$1.10** | 2M tokens/day (sometimes) |
| **DeepSeek** | deepseek-reasoner (R1) | **$0.55** | **$2.19** | — |
| OpenAI | GPT-4o | $2.50 | $10.00 | None |
| Anthropic | claude-sonnet-4-5 | $3.00 | $15.00 | None |
| Google | Gemini 1.5 Pro | $1.25 | $5.00 | 50 req/day |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 | 1500 req/day |
| Mistral | Mistral Large | $2.00 | $6.00 | None |
| Mistral | Mistral 7B | Free via Ollama | Free | Unlimited local |

**Real cost for your use case:**
- 1 blog post = ~800 tokens input + ~600 tokens output = 1,400 tokens
- 30 posts/month = 42,000 tokens
- **DeepSeek cost: ~$0.06/month**
- **GPT-4o cost: ~$0.52/month**
- **Anthropic Sonnet cost: ~$1.24/month**

**Verdict:** DeepSeek is the best paid option. Gemini Flash is free (1500 req/day) and good for basic tasks.

---

## 2. Getting Your DeepSeek API Key

1. Go to **platform.deepseek.com**
2. Click "Sign Up" → use Google or email
3. Go to "API Keys" in the left sidebar
4. Click "Create new secret key"
5. Copy the key (starts with `sk-`)
6. Add $5 credit (lasts months for your volume)

**Security:** Store in `.env` file, never in code.

```bash
# .env file (never commit this)
DEEPSEEK_API_KEY=sk-your-key-here
```

---

## 3. DeepSeek API Basics

DeepSeek uses the **same format as OpenAI**. This is huge — any code written for OpenAI works with DeepSeek by changing 2 lines.

### Base URL
```
https://api.deepseek.com/v1
```

### Available Models
| Model ID | Use Case | Speed |
|----------|----------|-------|
| `deepseek-chat` | General writing, blogging, Q&A | Fast |
| `deepseek-reasoner` | Complex reasoning, analysis | Slower but thorough |

### Simple API Call (Python)

```python
import os
import requests

API_KEY = os.getenv('DEEPSEEK_API_KEY')  # from .env

def ask_deepseek(prompt, system="You are a helpful assistant."):
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': system},
                {'role': 'user',   'content': prompt}
            ],
            'max_tokens': 1500,
            'temperature': 0.7
        }
    )
    return response.json()['choices'][0]['message']['content']

# Test it
result = ask_deepseek("Write a 3-sentence intro for an ELT blog about listening skills.")
print(result)
```

### Simple API Call (JavaScript / Apps Script)

```javascript
function callDeepSeek(prompt) {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  
  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are an ELT content writer.' },
        { role: 'user',   content: prompt }
      ],
      max_tokens: 1200
    }),
    muteHttpExceptions: true
  });
  
  const data = JSON.parse(response.getContentText());
  return data.choices[0].message.content;
}
```

**Store your API key in Apps Script:** Go to Project Settings → Script Properties → Add `DEEPSEEK_KEY`.

---

## 4. WordPress Auto-Publishing with DeepSeek

### Full Python Script: Generate + Publish

```python
import os, requests

DEEPSEEK_KEY = os.getenv('DEEPSEEK_API_KEY')
WP_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
WP_KEY = os.getenv('WP_API_KEY')

def generate_post(topic, tone='educational', words=600):
    prompt = f"""Write a WordPress blog post about: \"{topic}\"
    Tone: {tone}. Length: ~{words} words.
    Return ONLY valid JSON:
    {{
      \"title\": \"compelling title\",
      \"content\": \"full HTML body\",
      \"meta_description\": \"under 160 chars\",
      \"tags\": [\"tag1\", \"tag2\"],
      \"category\": \"ELT Masterclass\"
    }}"""
    
    r = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 2000
        }
    )
    import json
    raw = r.json()['choices'][0]['message']['content']
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)

def publish_to_wordpress(post_data, status='draft'):
    post_data['status'] = status
    r = requests.post(
        WP_URL,
        headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
        json=post_data
    )
    return r.json()

# Run
if __name__ == '__main__':
    post = generate_post("5 ways to improve English pronunciation at home")
    result = publish_to_wordpress(post, status='draft')
    print(f"Created post ID: {result.get('post_id')} — {post['title']}")
```

---

## 5. Google Apps Script Integration

### Store Key Securely

1. Open your Apps Script project
2. Click gear icon (⚙️) → **Project Settings**
3. Scroll to **Script Properties**
4. Add: `DEEPSEEK_KEY` = your key

### Auto-Generate SEO Meta from Your Sheet

Add this function to your sheet publisher script:

```javascript
function generateSEOMeta(title, content) {
  const key = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  
  const prompt = `Given this blog post:
Title: ${title}
Content (first 500 chars): ${content.substring(0, 500)}

Generate ONLY a JSON object:
{
  "meta_description": "under 160 chars, compelling",
  "seo_title": "under 60 chars",
  "tags": ["3 to 5 relevant tags"]
}`;
  
  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${key}`, 'Content-Type': 'application/json' },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [{ role: 'user', content: prompt }],
      max_tokens: 300
    }),
    muteHttpExceptions: true
  });
  
  let raw = JSON.parse(response.getContentText()).choices[0].message.content;
  raw = raw.replace(/```json\n?/g, '').replace(/```/g, '').trim();
  return JSON.parse(raw);
}

// Updated publishFromSheet with AI meta generation
function publishFromSheetWithAI() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  const rows = sheet.getDataRange().getValues();
  
  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date] = rows[i];
    if (!title || status === 'published') continue;
    
    // Generate SEO meta with DeepSeek
    let meta = {};
    try {
      meta = generateSEOMeta(title, content);
    } catch(e) {
      Logger.log('AI meta failed, using defaults: ' + e);
      meta = { meta_description: content.substring(0, 155), seo_title: title, tags: [] };
    }
    
    const post = {
      title,
      content,
      category: category || guessCategory(title, content),
      tags: meta.tags ? meta.tags.join(',') : (tags || ''),
      status: status === 'future' ? 'future' : 'draft',
      meta_description: meta.meta_description || '',
      seo_title: meta.seo_title || title
    };
    if (status === 'future' && date) post.date = date;
    
    publishPost(post);
    sheet.getRange(i + 1, 5).setValue('published');
    Utilities.sleep(2000);
  }
}
```

---

## 6. WordPress Plugin Integration

Add DeepSeek to your `sourov-ai-controller.php`:

```php
<?php
// Add to your existing plugin
function sourov_generate_with_deepseek($topic, $tone = 'educational') {
    $api_key = get_option('sourov_deepseek_api_key', '');
    if (empty($api_key)) return new WP_Error('no_key', 'DeepSeek API key not configured');
    
    $prompt = "Write a WordPress blog post about: $topic\nTone: $tone.\nReturn ONLY valid JSON with keys: title, content (HTML), meta_description, tags (array), category.";
    
    $response = wp_remote_post('https://api.deepseek.com/v1/chat/completions', [
        'headers' => [
            'Authorization' => 'Bearer ' . $api_key,
            'Content-Type'  => 'application/json'
        ],
        'body' => json_encode([
            'model'    => 'deepseek-chat',
            'messages' => [['role' => 'user', 'content' => $prompt]],
            'max_tokens' => 2000
        ]),
        'timeout' => 60
    ]);
    
    if (is_wp_error($response)) return $response;
    
    $body = json_decode(wp_remote_retrieve_body($response), true);
    $raw  = $body['choices'][0]['message']['content'];
    $raw  = preg_replace('/```json\n?|```/', '', $raw);
    
    return json_decode(trim($raw), true);
}

// REST endpoint: POST /wp-json/sourov/v1/ai-generate
add_action('rest_api_init', function() {
    register_rest_route('sourov/v1', '/ai-generate', [
        'methods'             => 'POST',
        'callback'            => function($req) {
            $topic = sanitize_text_field($req->get_param('topic'));
            $tone  = sanitize_text_field($req->get_param('tone') ?? 'educational');
            $data  = sourov_generate_with_deepseek($topic, $tone);
            if (is_wp_error($data)) return $data;
            return rest_ensure_response(['success' => true, 'post' => $data]);
        },
        'permission_callback' => function($req) {
            return $req->get_header('X-Sourov-Key') === get_option('sourov_api_key', '');
        }
    ]);
});

// Add DeepSeek key to WP settings
add_action('admin_init', function() {
    register_setting('sourov_settings', 'sourov_deepseek_api_key');
});
?>
```

**Store the key in WP:**
- Go to Settings → your plugin settings page
- Or: `wp option update sourov_deepseek_api_key "sk-your-key"` (via WP-CLI)

---

## 7. Mistral Free Alternative

If you want completely free, use **Mistral via La Plateforme**:

- Free tier: **1B tokens/month** (experimental tier)
- Base URL: `https://api.mistral.ai/v1`
- Same OpenAI-compatible format
- Model: `mistral-small-latest` (fast, free tier)

```python
# Same code, just change URL and key
API_KEY = os.getenv('MISTRAL_API_KEY')
BASE_URL = 'https://api.mistral.ai/v1/chat/completions'
MODEL = 'mistral-small-latest'
```

Get key at: **console.mistral.ai**

---

## 8. Quick Decision Guide

| Situation | Best Option |
|-----------|-------------|
| You're testing, very low volume | Gemini Flash (free, 1500 req/day) |
| You publish 1-5 posts/day | DeepSeek-V3 (~$0.06/month) |
| You want zero cost forever | Ollama local (mistral/phi3) |
| You need best quality | Anthropic Sonnet (expensive but best) |
| You need reasoning/analysis | DeepSeek-R1 or Gemini 1.5 Pro |
| You want privacy | Ollama (stays on your machine) |

---

*Last updated: June 2026 | Prices change — verify at platform.deepseek.com*
