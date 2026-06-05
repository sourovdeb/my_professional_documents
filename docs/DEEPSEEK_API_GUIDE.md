# DeepSeek API — Complete Automation Guide for WordPress Publishing

> **Why DeepSeek?** It is 10× cheaper than GPT-4o, has a generous free tier, and performs excellently on structured tasks like tag generation, categorisation, and SEO meta writing.

---

## Price Comparison (June 2026)

| Provider | Input (per 1M tokens) | Output (per 1M tokens) | Free Tier |
|----------|-----------------------|------------------------|-----------|
| **DeepSeek V3** | **$0.27** | **$1.10** | **500K tokens/day** |
| DeepSeek R1 | $0.55 | $2.19 | Limited |
| GPT-4o | $2.50 | $10.00 | None |
| GPT-4o-mini | $0.15 | $0.60 | $5 one-time credit |
| Gemini 1.5 Flash | $0.075 | $0.30 | 1M tokens/day |
| Gemini 1.5 Pro | $1.25 | $5.00 | 50 req/day |
| Mistral Large | $3.00 | $9.00 | None |
| Mistral 7B (Groq) | $0.06 | $0.06 | 14,400 req/day |

**Cost for 30 WordPress posts/month using DeepSeek:** ~$0.004. Essentially free.

---

## 1. Getting Your API Key

1. Visit **platform.deepseek.com**
2. Sign up with email + password
3. Go to **API Keys** → **Create new secret key**
4. Copy the key (starts with `sk-`)
5. Store it in a `.env` file — never paste it directly in code

Your free tier: **500,000 tokens/day**. One 500-word blog post ≈ 750 tokens.

---

## 2. Quick Connection Test

Run this in your terminal (replace `YOUR_KEY`):

```bash
curl -X POST https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"Say hello in 5 words"}]}'
```

If you get a JSON response with `choices[0].message.content`, it works.

---

## 3. Python: WordPress Auto-Tagger with DeepSeek

This script reads a Markdown file and uses DeepSeek to generate tags, category, and SEO meta — then publishes to WordPress as a draft.

```python
# deepseek_wp_publisher.py
# Install dependencies: pip install requests python-dotenv

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # reads from .env file

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.getenv('WP_API_KEY')


def ask_deepseek(prompt: str) -> str:
    """Send a prompt to DeepSeek and return the text response."""
    resp = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_API_KEY}', 'Content-Type': 'application/json'},
        json={
            'model': 'deepseek-chat',
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': 200,
            'temperature': 0.3
        },
        timeout=30
    )
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content'].strip()


def generate_metadata(title: str, content: str) -> dict:
    tags = ask_deepseek(
        f'Post title: "{title}"\nContent: {content[:800]}\n\n'
        'Generate 5 SEO tags for this ELT/CELTA teaching blog post. '
        'Return ONLY a comma-separated list. Example: grammar, CELTA, listening'
    )
    category = ask_deepseek(
        f'Post title: "{title}"\n'
        'Choose ONE category: Grammar | Listening & Phonology | Speaking & Fluency | '
        'CELTA | Reading & Writing | ELT Masterclass | Technology in ELT | Career & Professional Development\n'
        'Return ONLY the category name.'
    )
    seo = ask_deepseek(
        f'Write a 155-character SEO meta description for an ELT blog post titled "{title}". '
        'Make it compelling. Return ONLY the description.'
    )
    return {'tags': tags, 'category': category.strip(), 'meta_description': seo[:155]}


def publish_markdown_file(filepath: str, status: str = 'draft'):
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    lines = raw.split('\n')
    title = lines[0].lstrip('# ').strip()
    body = '\n'.join(lines[1:]).strip()

    print(f'Generating metadata for: {title}')
    meta = generate_metadata(title, body)
    print(f'  Category: {meta["category"]}')
    print(f'  Tags: {meta["tags"]}')

    resp = requests.post(
        WP_URL,
        json={
            'title': title,
            'content': body,
            'status': status,
            'tags': meta['tags'],
            'category': meta['category'],
            'meta_description': meta['meta_description']
        },
        headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
        timeout=30
    )

    if resp.status_code == 200:
        result = resp.json()
        print(f'Published! Post ID: {result.get("post_id")} | URL: {result.get("url", "")}')
        return result
    else:
        print(f'Error {resp.status_code}: {resp.text}')
        return None


if __name__ == '__main__':
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else 'draft.md'
    publish_markdown_file(path, status='draft')
```

**Run it:**
```bash
pip install requests python-dotenv
# Create .env file with your keys (see section 7)
python deepseek_wp_publisher.py drafts/2026-06-15-listening.md
```

---

## 4. Batch Fix: Add Tags to ALL Existing WordPress Posts

This script retroactively adds categories and tags to posts that are missing them.

```python
# fix_existing_posts.py
# Requires WordPress Application Password (not your login password)
# Go to WP Admin → Users → Your Profile → Application Passwords → Add New

import os
import requests
from dotenv import load_dotenv

load_dotenv()

WP_REST = 'https://sourovdeb.com/wp-json/wp/v2'
WP_USER = os.getenv('WP_USER', 'sourov')
WP_APP_PASS = os.getenv('WP_APP_PASSWORD')  # format: 'xxxx xxxx xxxx xxxx'
AUTH = (WP_USER, WP_APP_PASS)

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')


def ask_deepseek(prompt):
    resp = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_API_KEY}'},
        json={'model': 'deepseek-chat', 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 150},
        timeout=30
    )
    return resp.json()['choices'][0]['message']['content'].strip()


def get_or_create_tag(name):
    name = name.strip()
    r = requests.get(f'{WP_REST}/tags', params={'search': name}, auth=AUTH)
    tags = r.json()
    if tags:
        return tags[0]['id']
    r = requests.post(f'{WP_REST}/tags', json={'name': name}, auth=AUTH)
    return r.json().get('id')


def get_or_create_category(name):
    name = name.strip()
    r = requests.get(f'{WP_REST}/categories', params={'search': name}, auth=AUTH)
    cats = r.json()
    if cats:
        return cats[0]['id']
    r = requests.post(f'{WP_REST}/categories', json={'name': name}, auth=AUTH)
    return r.json().get('id')


def process_posts_batch(limit=20):
    r = requests.get(f'{WP_REST}/posts', params={
        'per_page': limit, 'status': 'publish,draft',
        '_fields': 'id,title,content,tags,categories'
    }, auth=AUTH)
    posts = r.json()

    for post in posts:
        if post.get('tags'):  # already has tags, skip
            continue
        title = post['title']['rendered']
        content = post['content']['rendered'][:500]
        print(f'Processing: {title}')

        tags_str = ask_deepseek(
            f'Generate 4 SEO tags for ELT blog post: "{title}". Comma-separated list only.'
        )
        category_name = ask_deepseek(
            f'One category for ELT post "{title}": Grammar|Listening & Phonology|'
            'Speaking & Fluency|CELTA|ELT Masterclass. Return name only.'
        )

        tag_ids = [get_or_create_tag(t) for t in tags_str.split(',') if t.strip()]
        cat_id = get_or_create_category(category_name)

        requests.post(
            f'{WP_REST}/posts/{post["id"]}',
            json={'tags': tag_ids, 'categories': [cat_id]},
            auth=AUTH
        )
        print(f'  Updated with category "{category_name}" and tags: {tags_str}')


if __name__ == '__main__':
    process_posts_batch(limit=20)
```

---

## 5. Google Apps Script Integration (via WordPress Proxy)

Apps Script cannot call DeepSeek directly due to CORS. Route through your WordPress plugin:

**In your WordPress plugin** (`sourov-ai-controller.php`), add:

```php
add_action('rest_api_init', function () {
    register_rest_route('sourov/v1', '/ai-metadata', [
        'methods' => 'POST',
        'callback' => 'sourov_ai_metadata',
        'permission_callback' => 'sourov_verify_key'
    ]);
});

function sourov_ai_metadata($request) {
    $title   = sanitize_text_field($request->get_param('title'));
    $content = sanitize_textarea_field($request->get_param('content'));
    $ds_key  = get_option('sourov_deepseek_key', '');

    $prompt  = "Generate tags and category for this ELT blog post titled: '$title'. "
             . "Return valid JSON: {\"tags\": \"tag1, tag2, tag3\", \"category\": \"Category Name\", "
             . "\"seo_meta\": \"155-char SEO description\"}";

    $api_resp = wp_remote_post('https://api.deepseek.com/v1/chat/completions', [
        'headers' => ['Authorization' => 'Bearer ' . $ds_key, 'Content-Type' => 'application/json'],
        'body'    => json_encode(['model' => 'deepseek-chat', 'messages' => [['role' => 'user', 'content' => $prompt]], 'max_tokens' => 200]),
        'timeout' => 30
    ]);

    if (is_wp_error($api_resp)) return new WP_Error('deepseek_error', $api_resp->get_error_message());

    $text = json_decode(wp_remote_retrieve_body($api_resp), true)['choices'][0]['message']['content'];
    preg_match('/\{.*\}/s', $text, $m);
    return rest_ensure_response(json_decode($m[0] ?? '{}', true));
}
```

**In Google Apps Script:**

```javascript
function getAIMetadata(title, content) {
  var resp = UrlFetchApp.fetch('https://sourovdeb.com/wp-json/sourov/v1/ai-metadata', {
    method: 'POST',
    headers: { 'X-Sourov-Key': '0767044896thevenet_', 'Content-Type': 'application/json' },
    payload: JSON.stringify({ title: title, content: content.substring(0, 500) }),
    muteHttpExceptions: true
  });
  return JSON.parse(resp.getContentText());
}
```

---

## 6. Monthly Cost Estimate

| Task | Tokens/post | Cost/post | 30 posts/month |
|------|-------------|-----------|----------------|
| Generate tags | ~200 | $0.000054 | $0.0016 |
| Choose category | ~150 | $0.0000405 | $0.0012 |
| Write SEO meta | ~200 | $0.000054 | $0.0016 |
| **TOTAL** | ~550 | **$0.00015** | **~$0.004** |

Even at 300 posts/month: **less than $0.05**.

---

## 7. Environment Variables

Create `.env` in your project root (never commit this file):

```
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WP_URL=https://sourovdeb.com/wp-json/sourov/v1/ai-post
WP_API_KEY=your-wp-key
WP_USER=sourov
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx
```

Install: `pip install python-dotenv`

Load in Python: `from dotenv import load_dotenv; load_dotenv()`

---

## 8. Useful Resources

- DeepSeek API documentation: platform.deepseek.com/api-docs
- DeepSeek pricing: platform.deepseek.com/pricing  
- WordPress REST API reference: developer.wordpress.org/rest-api
- WordPress Application Passwords: WP Admin → Users → Profile → Application Passwords
- Python dotenv: github.com/theskumar/python-dotenv
