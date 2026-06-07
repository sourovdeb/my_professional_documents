# DeepSeek API Automation Guide
## The Cheapest Way to Add AI to Your WordPress Publishing Pipeline

---

## Why DeepSeek?

### Cost comparison (June 2026)

| Provider | Input (per 1M tokens) | Output (per 1M tokens) | Notes |
|----------|----------------------|------------------------|-------|
| DeepSeek V3 | $0.27 | $1.10 | Best value for writing tasks |
| DeepSeek R1 | $0.55 | $2.19 | Reasoning model, better quality |
| Anthropic Sonnet | $3.00 | $15.00 | ~10x more expensive |
| OpenAI GPT-4o | $5.00 | $15.00 | ~18x more expensive |
| Mistral Large | $2.00 | $6.00 | Mid-range |
| Ollama (local) | $0 | $0 | Free but needs your hardware |

**For a 500-word blog post:** DeepSeek costs approximately $0.0003 (less than 1/10th of a cent).

At that price, publishing **100 posts per month** costs roughly **$0.03** in AI fees.

---

## Getting a DeepSeek API Key

1. Go to **platform.deepseek.com**
2. Click **Sign Up** (email or Google)
3. Go to **API Keys** in the left sidebar
4. Click **Create new API key**
5. Name it (e.g., `wordpress-automation`)
6. Copy the key — starts with `sk-`
7. Add $5 credit to start (lasts months at typical usage)

**Store the key** in your environment or script properties. Never in code.

---

## Models Available

| Model | Best for | Speed |
|-------|----------|-------|
| `deepseek-chat` | Blog posts, emails, content | Fast |
| `deepseek-reasoner` | Analysis, structured thinking | Slower but deeper |

For WordPress automation, always use `deepseek-chat`.

---

## Module 1: Google Apps Script + DeepSeek

This replaces the "manual content" column in your sheet. You only need a **title**.

```javascript
// Add this to your existing sheet_publisher.gs
// Requires DEEPSEEK_KEY in Script Properties

function generateAndPublish() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
                  .getSheetByName('Queue');
  const rows  = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, , category, , status] = rows[i];
    if (!title || status === 'published' || status === 'skip') continue;

    // Generate full post from title alone
    const generated = callDeepSeek(
      'You are an expert ELT blogger. Return ONLY a JSON object with these keys: ' +
      'content (HTML string), meta_desc (under 160 chars), tags (array of 5 strings).',
      'Write a 500-word WordPress blog post titled: "' + title + '"'
    );

    if (!generated) continue;

    let post;
    try {
      post = JSON.parse(generated.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim());
    } catch(e) {
      Logger.log('JSON parse failed for: ' + title);
      continue;
    }

    const result = sendToWordPress({
      title,
      content:          post.content,
      category:         category || guessCategory(title, post.content),
      tags:             Array.isArray(post.tags) ? post.tags.join(',') : suggestTags(title),
      meta_description: post.meta_desc,
      seo_title:        buildSeoTitle(title),
      status:           'draft'
    });

    if (result && result.post_id) {
      sheet.getRange(i + 1, 2).setValue(post.content);  // Store content in col B
      sheet.getRange(i + 1, 5).setValue('published');
      Logger.log('AI-generated & published: ' + title);
    }
    Utilities.sleep(2000);
  }
}

function callDeepSeek(systemPrompt, userPrompt) {
  const key = PropertiesService.getScriptProperties().getProperty('DEEPSEEK_KEY');
  if (!key) { Logger.log('DEEPSEEK_KEY missing'); return null; }

  try {
    const res = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Authorization':  'Bearer ' + key,
        'Content-Type':   'application/json'
      },
      payload: JSON.stringify({
        model: 'deepseek-chat',
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user',   content: userPrompt }
        ],
        max_tokens: 1500,
        temperature: 0.7
      }),
      muteHttpExceptions: true
    });
    const data = JSON.parse(res.getContentText());
    return data.choices[0].message.content;
  } catch(e) {
    Logger.log('DeepSeek error: ' + e.message);
    return null;
  }
}
```

---

## Module 2: Python + DeepSeek (Desktop Script)

```python
import os, requests, json

DEEPSEEK_KEY = os.environ.get('DEEPSEEK_KEY', '')

def generate_post(title: str) -> dict:
    """Generate a full WordPress post from a title."""
    headers = {
        'Authorization': f'Bearer {DEEPSEEK_KEY}',
        'Content-Type':  'application/json'
    }
    payload = {
        'model': 'deepseek-chat',
        'messages': [
            {
                'role': 'system',
                'content': (
                    'You are an ELT blogger. Return ONLY valid JSON with keys: '
                    'content (HTML), meta_desc (string <160 chars), '
                    'tags (list of 5 strings), excerpt (2 sentences).'
                )
            },
            {
                'role': 'user',
                'content': f'Write a 500-word WordPress blog post titled: "{title}"'
            }
        ],
        'max_tokens': 2000,
        'temperature': 0.7
    }
    r = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers=headers,
        json=payload,
        timeout=60
    )
    r.raise_for_status()
    raw = r.json()['choices'][0]['message']['content']
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)


def publish_to_wordpress(title: str, post: dict, wp_url: str, wp_key: str) -> dict:
    headers = {'X-Sourov-Key': wp_key, 'Content-Type': 'application/json'}
    payload = {
        'title':            title,
        'content':          post['content'],
        'meta_description': post.get('meta_desc', ''),
        'tags':             ','.join(post.get('tags', [])),
        'status':           'draft'
    }
    r = requests.post(wp_url, headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


if __name__ == '__main__':
    WP_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post'
    WP_KEY = os.environ.get('WP_KEY', '')

    titles = [
        'Day 32 – Mastering Minimal Pairs in English',
        'Why Grammar Rules Are Meant to Be Broken',
        'CELTA Week 3: What No One Tells You About Teaching Adults'
    ]

    for title in titles:
        print(f'Generating: {title}')
        post = generate_post(title)
        result = publish_to_wordpress(title, post, WP_URL, WP_KEY)
        print(f'  Published → ID {result.get("post_id")} | {result.get("link")}')
```

Run with:
```bash
export DEEPSEEK_KEY=sk-your-key
export WP_KEY=your-wordpress-key
python3 deepseek_publisher.py
```

---

## Module 3: GitHub Actions + DeepSeek

Push a file containing only a title. The action generates the full post via DeepSeek and publishes to WordPress.

```yaml
# .github/workflows/ai_publish.yml
name: AI Generate and Publish
on:
  push:
    paths: ['titles/*.txt']

jobs:
  generate-and-publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - run: pip install requests

      - name: Generate and publish
        env:
          DEEPSEEK_KEY: ${{ secrets.DEEPSEEK_KEY }}
          WP_KEY:       ${{ secrets.WP_API_KEY }}
          WP_URL:       https://sourovdeb.com/wp-json/sourov/v1/ai-post
        run: |
          python3 - <<'EOF'
          import os, requests, json, glob

          for f in glob.glob('titles/*.txt'):
            title = open(f).read().strip()
            if not title: continue

            # Call DeepSeek
            r = requests.post('https://api.deepseek.com/v1/chat/completions',
              headers={'Authorization': f'Bearer {os.environ["DEEPSEEK_KEY"]}',
                       'Content-Type': 'application/json'},
              json={'model':'deepseek-chat','messages':[
                {'role':'system','content':'Return only JSON with keys content, meta_desc, tags (list).'},
                {'role':'user','content':f'Write a 500-word ELT blog post: "{title}"'}
              ],'max_tokens':2000},
              timeout=60)
            raw = r.json()['choices'][0]['message']['content']
            post = json.loads(raw.replace('```json','').replace('```','').strip())

            # Publish to WordPress
            requests.post(os.environ['WP_URL'],
              headers={'X-Sourov-Key':os.environ['WP_KEY'],'Content-Type':'application/json'},
              json={'title':title,'content':post['content'],
                    'meta_description':post.get('meta_desc',''),
                    'tags':','.join(post.get('tags',[])),'status':'draft'},
              timeout=30)
            print(f'Published: {title}')
          EOF
```

Workflow: create a file in `titles/` with just the post title, push, done.

---

## Prompts That Work Well for ELT Content

```
System: You are an ELT educator and blogger. Write for B2-C1 English teachers.
Return ONLY valid JSON: {content: "<HTML>", meta_desc: "string", tags: ["array"]}

User: Write a 500-word post: "5 Activities to Teach Minimal Pairs"
```

```
System: You are a CELTA reflective practice writer.
Return ONLY valid JSON: {content: "<HTML>", meta_desc: "string", tags: ["array"]}

User: Write a 400-word CELTA teaching journal entry about: "Teaching pronunciation to anxious learners"
```

---

## Cost Tracking

Add this to track your monthly spend:

```python
def estimate_cost(prompt_tokens: int, completion_tokens: int) -> float:
    # DeepSeek V3 pricing (per 1M tokens)
    input_rate  = 0.27 / 1_000_000
    output_rate = 1.10 / 1_000_000
    return (prompt_tokens * input_rate) + (completion_tokens * output_rate)

# Example: 300 input + 700 output tokens per post
# Cost per post: $0.00085 (less than 0.1 cent)
# 100 posts/month: $0.085
```
