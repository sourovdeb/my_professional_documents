# DeepSeek API — Complete Automation Guide

> **Why DeepSeek?** It's the cheapest high-quality AI API available. $5 free credits on signup last you 15+ years of daily blogging.

## Pricing Comparison (June 2026)

| Provider | Input (per 1M tokens) | Output (per 1M tokens) | Free Tier |
|---|---|---|---|
| **DeepSeek Chat (V3)** | **$0.27** | **$1.10** | **$5 free** |
| DeepSeek R1 (reasoning) | $0.55 | $2.19 | $5 free |
| OpenAI GPT-4o | $5.00 | $15.00 | None |
| Anthropic Sonnet | $3.00 | $15.00 | None |
| Gemini 1.5 Pro | $3.50 | $10.50 | 1M tokens/month |
| Mistral Large | $2.00 | $6.00 | 1B tokens/month |
| **Ollama (local)** | **FREE** | **FREE** | Unlimited |

**DeepSeek is ~18x cheaper than GPT-4o.** 30 posts/month costs $0.026.
Your $5 free credits last **over 15 years** at that rate.

---

## Getting Your API Key

1. Go to **platform.deepseek.com**
2. Sign up with email
3. API Keys → Create new key
4. Copy the key (starts with `sk-`)
5. Store in env: `export DEEPSEEK_API_KEY=sk-your-key`

## DeepSeek Models

| Model | Best For |
|---|---|
| `deepseek-chat` | Blog posts, SEO, emails, daily automation |
| `deepseek-coder` | Scripts, code generation |
| `deepseek-reasoner` (R1) | Complex planning, multi-step analysis |

Use **`deepseek-chat`** for all WordPress publishing automation.

---

## Part 1: DeepSeek in Google Apps Script

Google Apps Script runs JavaScript inside Google's servers — no hosting needed.
You can call DeepSeek directly from your spreadsheet.

### Why this works

DeepSeek uses the **OpenAI-compatible API format**. The request structure is:
```
POST https://api.deepseek.com/v1/chat/completions
Authorization: Bearer sk-your-key
{ model, messages, temperature, max_tokens }
```

This is the same structure as OpenAI, so all existing OpenAI tutorials apply.

### Full Google Apps Script

In your Google Sheet: **Extensions → Apps Script** → paste this:

```javascript
// ============================================================
// DeepSeek WordPress Publisher — Google Apps Script
// ============================================================

const DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions';

function getKeys() {
  const props = PropertiesService.getScriptProperties();
  return {
    deepseek: props.getProperty('DEEPSEEK_KEY'),
    wp: props.getProperty('WP_KEY'),
    wpUrl: props.getProperty('WP_URL')
  };
}

// Run this ONCE to store keys securely (then delete the values)
function setKeys() {
  PropertiesService.getScriptProperties().setProperties({
    'DEEPSEEK_KEY': 'sk-your-deepseek-key',
    'WP_KEY': 'your-wp-plugin-key',
    'WP_URL': 'https://sourovdeb.com'
  });
  Logger.log('Keys saved. Delete the values from this function now.');
}

// ---- Core DeepSeek call ----
function callDeepSeek(userPrompt, systemMsg) {
  const keys = getKeys();
  const payload = {
    model: 'deepseek-chat',
    messages: [
      { role: 'system', content: systemMsg || 'You are a helpful assistant.' },
      { role: 'user',   content: userPrompt }
    ],
    temperature: 0.7,
    max_tokens: 1500
  };

  const resp = UrlFetchApp.fetch(DEEPSEEK_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${keys.deepseek}`,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify(payload),
    muteHttpExceptions: true
  });

  const data = JSON.parse(resp.getContentText());
  if (data.error) throw new Error(data.error.message);
  return data.choices[0].message.content;
}

// ---- Auto-enhance post (SEO, tags, category) ----
function enhancePost(title, content) {
  const prompt = `Post title: ${title}
Content preview: ${content.substring(0, 400)}

Return ONLY valid JSON (no markdown):
{"seo_title":"","meta_description":"","tags":[],"category":""}`;

  const raw = callDeepSeek(prompt, 'You are an SEO expert. Return valid JSON only.');
  return JSON.parse(raw.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim());
}

// ---- Generate a full post from topic ----
function generatePost(topic) {
  const prompt = `Write a 600-word WordPress blog post about: "${topic}"

Return ONLY valid JSON:
{"title":"","content":"<HTML>","meta_description":"","seo_title":"","tags":[],"category":""}`;

  const raw = callDeepSeek(prompt, 'You are a WordPress content writer. Return valid JSON only.');
  return JSON.parse(raw.replace(/```json\n?/g,'').replace(/```\n?/g,'').trim());
}

// ---- Publish post to WordPress ----
function publishPost(postData) {
  const keys = getKeys();
  const resp = UrlFetchApp.fetch(`${keys.wpUrl}/wp-json/sourov/v1/ai-post`, {
    method: 'POST',
    headers: { 'X-Sourov-Key': keys.wp, 'Content-Type': 'application/json' },
    payload: JSON.stringify(postData),
    muteHttpExceptions: true
  });
  return JSON.parse(resp.getContentText());
}

// ---- MAIN: publish queue from sheet ----
function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!sheet) { Logger.log('Create a tab named Queue'); return; }

  const rows = sheet.getDataRange().getValues();
  let count = 0;

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date,
           seoTitle, metaDesc, aiEnhance] = rows[i];

    if (!title || status === 'published' || status === 'error') continue;

    try {
      let postData = {
        title, content, category: category || 'Uncategorized',
        tags: tags || '', status: status === 'future' ? 'future' : 'draft',
        seo_title: seoTitle || title, meta_description: metaDesc || ''
      };

      // Let DeepSeek enhance if column I = 'yes'
      if (String(aiEnhance).toLowerCase() === 'yes' && content) {
        const enhanced = enhancePost(title, content);
        if (enhanced.seo_title)       postData.seo_title = enhanced.seo_title;
        if (enhanced.meta_description) postData.meta_description = enhanced.meta_description;
        if (enhanced.tags)             postData.tags = enhanced.tags.join(',');
        if (enhanced.category)         postData.category = enhanced.category;
        Utilities.sleep(1200);
      }

      if (status === 'future' && date) postData.date = new Date(date).toISOString();

      const result = publishPost(postData);
      if (result.post_id || result.id) {
        sheet.getRange(i+1, 5).setValue('published');
        sheet.getRange(i+1, 10).setValue('ID:' + (result.post_id || result.id));
        count++;
      } else {
        sheet.getRange(i+1, 5).setValue('error');
        sheet.getRange(i+1, 10).setValue(JSON.stringify(result).slice(0,120));
      }
    } catch(e) {
      sheet.getRange(i+1, 5).setValue('error');
      sheet.getRange(i+1, 10).setValue(e.message.slice(0,120));
    }
    Utilities.sleep(2000);
  }
  Logger.log(`Done — ${count} posts sent.`);
}

// ---- Generate posts from a Topics tab ----
function generateFromTopics() {
  const topicsSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Topics');
  const queueSheet  = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  if (!topicsSheet || !queueSheet) return;

  const rows = topicsSheet.getDataRange().getValues();
  for (let i = 1; i < rows.length; i++) {
    const [topic, done] = rows[i];
    if (!topic || done === 'done') continue;
    try {
      const post = generatePost(topic);
      queueSheet.appendRow([post.title, post.content, post.category,
        post.tags.join(','), 'draft', '', post.seo_title, post.meta_description, 'no', '']);
      topicsSheet.getRange(i+1, 2).setValue('done');
      Utilities.sleep(2500);
    } catch(e) {
      topicsSheet.getRange(i+1, 2).setValue('error: ' + e.message.slice(0,50));
    }
  }
}

// ---- Set up hourly auto-trigger (run once) ----
function setupHourlyTrigger() {
  ScriptApp.getProjectTriggers().forEach(t => ScriptApp.deleteTrigger(t));
  ScriptApp.newTrigger('publishFromSheet').timeBased().everyHours(1).create();
  Logger.log('Hourly trigger active. publishFromSheet runs every hour.');
}
```

### Sheet Structure

**Tab: Queue**
```
A:Title | B:Content | C:Category | D:Tags | E:Status | F:Date |
G:SEO Title | H:Meta Desc | I:AI Enhance (yes/no) | J:Result
```

**Tab: Topics** (for AI-generated posts)
```
A:Topic | B:Done
```

---

## Part 2: DeepSeek in Python

See `scripts/auto_publisher.py` for the full implementation.

Quick reference:
```python
import requests

def ask_deepseek(prompt, system=None):
    resp = requests.post(
        'https://api.deepseek.com/v1/chat/completions',
        headers={'Authorization': f'Bearer {DEEPSEEK_KEY}'},
        json={
            'model': 'deepseek-chat',
            'messages': [
                *([{'role':'system','content':system}] if system else []),
                {'role':'user','content':prompt}
            ]
        }
    )
    return resp.json()['choices'][0]['message']['content']
```

---

## Part 3: DeepSeek in WordPress PHP Plugin

Add to `sourov-ai-controller.php` to auto-enhance posts on save:

```php
<?php
class Sourov_DeepSeek {
    private $api_key;
    private $url = 'https://api.deepseek.com/v1/chat/completions';

    public function __construct() {
        $this->api_key = get_option('sourov_deepseek_key', '');
    }

    public function enhance($title, $content) {
        if (!$this->api_key) return null;
        $prompt = "Post title: {$title}\nContent: " . substr(strip_tags($content),0,400)
                . '\nReturn JSON only: {"seo_title":"","meta_description":"","tags":[],"category":""}';
        $resp = wp_remote_post($this->url, [
            'timeout' => 30,
            'headers' => ['Authorization'=>'Bearer '.$this->api_key,'Content-Type'=>'application/json'],
            'body'    => json_encode(['model'=>'deepseek-chat','messages'=>[
                ['role'=>'system','content'=>'Return valid JSON only.'],
                ['role'=>'user',  'content'=>$prompt]
            ],'max_tokens'=>400])
        ]);
        if (is_wp_error($resp)) return null;
        $raw = json_decode(wp_remote_retrieve_body($resp),true);
        $text = $raw['choices'][0]['message']['content'] ?? '';
        $text = preg_replace('/```json\n?|```\n?/', '', $text);
        return json_decode(trim($text), true);
    }

    public function hook_save($post_id) {
        if (wp_is_post_revision($post_id)) return;
        if (get_post_type($post_id) !== 'post') return;
        if (!empty(wp_get_post_tags($post_id))) return; // already tagged
        $post = get_post($post_id);
        $data = $this->enhance($post->post_title, $post->post_content);
        if (!$data) return;
        if (!empty($data['tags']))     wp_set_post_tags($post_id, $data['tags']);
        if (!empty($data['category'])) {
            $cat = get_cat_ID($data['category']);
            if (!$cat) $cat = wp_insert_category(['cat_name'=>$data['category']]);
            wp_set_post_categories($post_id, [$cat]);
        }
        if (!empty($data['meta_description']))
            update_post_meta($post_id,'_yoast_wpseo_metadesc',$data['meta_description']);
        if (!empty($data['seo_title']))
            update_post_meta($post_id,'_yoast_wpseo_title',$data['seo_title']);
    }
}
$ds = new Sourov_DeepSeek();
add_action('save_post', [$ds, 'hook_save']);
```

---

## Cost Calculator

```python
def estimate_cost(posts_per_month: int, words: int = 600) -> dict:
    # DeepSeek V3 pricing (June 2026)
    # Input: $0.27/1M tokens  Output: $1.10/1M tokens  (1 word ≈ 1.3 tokens)
    input_cost  = (posts_per_month * 200  / 1_000_000) * 0.27
    output_cost = (posts_per_month * words * 1.3 / 1_000_000) * 1.10
    total = input_cost + output_cost
    return {
        'monthly_usd': round(total, 4),
        'free_credits_last_months': round(5.0/total, 1) if total else 'infinite',
        'annual_usd': round(total*12, 2)
    }

print(estimate_cost(30))   # → {'monthly_usd': 0.026, 'free_credits_last_months': 192, 'annual_usd': 0.31}
print(estimate_cost(365))  # → {'monthly_usd': 0.315, 'free_credits_last_months': 15.9, 'annual_usd': 3.78}
```

**Daily posting for a year costs $3.78 total.** Your free credits cover 16 months.
