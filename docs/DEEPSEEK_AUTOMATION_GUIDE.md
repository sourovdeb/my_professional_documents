# DeepSeek API Automation Guide
## Complete WordPress Publishing Pipeline Using DeepSeek (Cheaper Than Most AI APIs)

### Why DeepSeek?

| AI Provider | Input (per 1M tokens) | Output (per 1M tokens) | Free Tier |
|-------------|----------------------|------------------------|----------|
| DeepSeek V3 | $0.27 | $1.10 | $5 credit on signup |
| DeepSeek R1 (reasoning) | $0.55 | $2.19 | Yes |
| Anthropic API | $3.00 | $15.00 | No |
| OpenAI GPT-4o | $2.50 | $10.00 | No |
| Mistral Large | $2.00 | $6.00 | Yes (small model) |

DeepSeek is **10x cheaper** than most alternatives for the same quality. For 500-word blog posts, one month of daily posting costs under $1.

---

## Step 1: Get Your DeepSeek API Key

1. Go to [platform.deepseek.com](https://platform.deepseek.com)
2. Register with email
3. Go to API Keys → Create new key
4. Copy the key (starts with `sk-`)
5. Add $5 credit (enough for ~18,000 blog posts)

---

## Step 2: Google Apps Script + DeepSeek (Complete Setup)

This script reads from your Google Sheet and uses DeepSeek to:
- Improve your raw draft title into an SEO title
- Generate a meta description
- Auto-assign tags
- Post to WordPress

Paste this into `Extensions > Apps Script` in your spreadsheet:

```javascript
// ============================================================
// WordPress Auto-Publisher with DeepSeek AI
// Google Sheets → DeepSeek → WordPress
// ============================================================

const CONFIG = {
  WP_API:      'https://sourovdeb.com/wp-json/sourov/v1/ai-post',
  WP_KEY:      PropertiesService.getScriptProperties().getProperty('WP_KEY'),
  DS_KEY:      PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY'),
  DS_MODEL:    'deepseek-chat',
  SHEET_NAME:  'Queue',
};

// Main entry point — called by time trigger every hour
function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.SHEET_NAME);
  const rows  = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date, seoTitle, metaDesc] = rows[i];
    if (!title || status === 'published' || status === 'skip') continue;

    // Use DeepSeek to enhance metadata if SEO title is missing
    let finalSeo  = seoTitle;
    let finalMeta = metaDesc;
    let finalTags = tags;

    if (!seoTitle || !metaDesc) {
      const enhanced = enhanceWithDeepSeek(title, content);
      finalSeo  = enhanced.seoTitle  || title;
      finalMeta = enhanced.metaDesc  || content.substring(0, 160);
      finalTags = enhanced.tags      || tags;
    }

    const postData = {
      title:            title,
      content:          content,
      category:         category || guessCategory(title + ' ' + content),
      tags:             finalTags,
      status:           status === 'future' ? 'future' : 'draft',
      meta_description: finalMeta,
      seo_title:        finalSeo,
    };
    if (status === 'future' && date) postData.date = new Date(date).toISOString();

    const result = postToWordPress(postData);

    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('Published: ' + title + ' → ID ' + result.post_id);
    } else {
      sheet.getRange(i + 1, 5).setValue('error: ' + JSON.stringify(result));
    }

    Utilities.sleep(2000); // stay under API rate limits
  }
}

// Call DeepSeek to generate SEO metadata
function enhanceWithDeepSeek(title, content) {
  const prompt = `Given this blog post title and content snippet, return ONLY valid JSON with these keys:
- seoTitle: SEO-optimized title under 60 characters
- metaDesc: meta description under 160 characters  
- tags: array of 3-5 relevant tags (lowercase, no spaces)

Title: ${title}
Content (first 300 chars): ${content.substring(0, 300)}

Return only JSON, no explanation.`;

  const payload = {
    model: CONFIG.DS_MODEL,
    messages: [
      { role: 'system', content: 'You are an SEO expert. Always respond with valid JSON only.' },
      { role: 'user',   content: prompt }
    ],
    max_tokens: 300,
  };

  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method:           'POST',
    headers:          { 'Authorization': 'Bearer ' + CONFIG.DS_KEY, 'Content-Type': 'application/json' },
    payload:          JSON.stringify(payload),
    muteHttpExceptions: true,
  });

  try {
    const raw = JSON.parse(response.getContentText());
    const text = raw.choices[0].message.content.replace(/```json\n?/g, '').replace(/```/g, '').trim();
    return JSON.parse(text);
  } catch (e) {
    Logger.log('DeepSeek parse error: ' + e);
    return {};
  }
}

// Post to WordPress via your plugin
function postToWordPress(data) {
  const response = UrlFetchApp.fetch(CONFIG.WP_API, {
    method:           'POST',
    headers:          { 'X-Sourov-Key': CONFIG.WP_KEY, 'Content-Type': 'application/json' },
    payload:          JSON.stringify(data),
    muteHttpExceptions: true,
  });
  return JSON.parse(response.getContentText());
}

// Auto-categorise by keyword matching
function guessCategory(text) {
  const t = text.toLowerCase();
  if (t.includes('grammar') || t.includes('tense') || t.includes('verb')) return 'Grammar';
  if (t.includes('listen') || t.includes('pronunciation') || t.includes('phoneme')) return 'Listening & Phonology';
  if (t.includes('celta') || t.includes('teaching practice') || t.includes('lesson plan')) return 'CELTA';
  if (t.includes('vocabulary') || t.includes('idiom') || t.includes('collocation')) return 'Vocabulary';
  if (t.includes('writing') || t.includes('essay') || t.includes('paragraph')) return 'Writing Skills';
  if (t.includes('speaking') || t.includes('fluency') || t.includes('conversation')) return 'Speaking';
  return 'ELT Masterclass';
}

// Store API keys safely (run this ONCE manually, then delete)
function setupKeys() {
  const props = PropertiesService.getScriptProperties();
  props.setProperty('WP_KEY',       'YOUR_WP_PLUGIN_KEY_HERE');
  props.setProperty('DEEPSEEK_KEY', 'YOUR_DEEPSEEK_KEY_HERE');
  Logger.log('Keys saved. Delete this function now.');
}
```

### How to Set Up the Time Trigger
1. In Apps Script: click **Triggers** (clock icon on left sidebar)
2. Click **+ Add Trigger**
3. Function: `publishFromSheet`
4. Event source: **Time-driven**
5. Type: **Hour timer** → every 1 hour
6. Save

Now every hour the script checks for new rows with status `draft` or `future` and posts them.

---

## Step 3: Python Script Using DeepSeek API

```python
# deepseek_publisher.py
import os, json, requests
from pathlib import Path

DEEPSEEK_KEY = os.environ.get('DEEPSEEK_KEY')  # set in .env or environment
WP_URL        = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
WP_KEY        = os.environ.get('WP_KEY')

def call_deepseek(system_prompt: str, user_prompt: str) -> str:
    response = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user',   'content': user_prompt},
            ],
            'max_tokens': 2000,
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def generate_post_from_topic(topic: str) -> dict:
    system = 'You are a WordPress content writer for an ELT blog. Respond ONLY with valid JSON.'
    user   = f'''Write a blog post about: "{topic}"
Return this JSON:
{{
  "title": "compelling blog title",
  "content": "full HTML body with h2/p/ul tags",
  "seo_title": "SEO title under 60 chars",
  "meta_description": "under 160 chars",
  "tags": ["tag1", "tag2", "tag3"],
  "category": "ELT Masterclass"
}}'''
    raw = call_deepseek(system, user)
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)

def publish_to_wordpress(post: dict, status: str = 'draft') -> dict:
    post['status'] = status
    r = requests.post(
        WP_URL,
        headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
        json=post,
        timeout=30
    )
    return r.json()

if __name__ == '__main__':
    import sys
    topic  = sys.argv[1] if len(sys.argv) > 1 else 'English listening strategies for beginners'
    status = sys.argv[2] if len(sys.argv) > 2 else 'draft'
    print(f'Generating post about: {topic}')
    post   = generate_post_from_topic(topic)
    result = publish_to_wordpress(post, status)
    print(f'Result: {json.dumps(result, indent=2)}')
```

Usage:
```bash
export DEEPSEEK_KEY='sk-your-key'
export WP_KEY='your-wp-key'
python deepseek_publisher.py "English phrasal verbs for work" draft
```

---

## Step 4: GitHub Actions Using DeepSeek (Free Automation)

```yaml
# .github/workflows/ai_publish.yml
name: AI-Assisted WordPress Publish
on:
  push:
    paths: ['drafts/*.md']
  schedule:
    - cron: '0 8 * * *'  # 8 AM daily

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      
      - run: pip install requests
      
      - name: Publish drafts
        env:
          DEEPSEEK_KEY: ${{ secrets.DEEPSEEK_KEY }}
          WP_KEY:       ${{ secrets.WP_KEY }}
        run: |
          for file in drafts/*.md; do
            [ -f "$file" ] || continue
            python scripts/deepseek_publisher.py "$(head -1 $file | sed 's/^# //')" draft
          done
```

Add secrets in GitHub: `Settings → Secrets → Actions → New repository secret`.

---

## Cost Estimate for Daily Blogging

| Action | Tokens used | Cost (DeepSeek) |
|--------|------------|------------------|
| Generate 600-word post | ~1,500 | $0.0004 |
| Generate SEO metadata | ~300 | $0.00008 |
| 30 posts/month | ~54,000 | ~$0.015 |
| **Full year** | ~648,000 | **~$0.18** |

That's less than 20 cents per year for daily AI-assisted publishing.
