# CSV + Google Apps Script: Complete Tutorial
## Why It Works, How It Works, Step by Step

This tutorial answers the question you asked: "I never understood how CSV + Google JavaScript works."

---

## Part 1: Why This Combination Exists

### What is CSV?

CSV stands for **Comma-Separated Values**. It is the simplest possible spreadsheet format — plain text where each line is a row and commas separate the columns:

```
Title,Content,Category,Status
Day 32 – Listening,"<p>Listening is...</p>",ELT,ready
Day 33 – Grammar,"<p>Grammar helps...</p>",Grammar,ready
```

**Why CSV instead of Excel?**
- Works everywhere (Google Sheets exports it, Notepad reads it, Python reads it)
- No proprietary format
- Can be generated automatically by any script
- Easy to version-control in GitHub

### What is Google Apps Script?

Google Apps Script is **JavaScript that runs inside Google's servers** — specifically inside your Google Sheets, Docs, or Drive. You write it in your browser. Google runs it for free.

The critical insight: **it can make HTTP requests**. That means it can call your WordPress API. This is the bridge between your spreadsheet and your website.

```
[You type in Google Sheets] → [Apps Script reads the sheet]
                           → [Apps Script calls WordPress API]
                           → [Post appears on your site]
```

### Why not just use WordPress admin directly?

WordPress admin requires:
- Opening a browser
- Logging in
- Clicking "New Post"
- Filling in title, content, category, tags, SEO fields separately
- Clicking Publish

With the Sheet + Script system:
- You type in the sheet
- Everything else is automatic

For someone managing bipolar disorder, **fewer steps = more posts published**.

---

## Part 2: How the Data Flows

```
Step 1: You fill a row in Google Sheets
        Title | Content | Category | Tags | Status
        ──────┼─────────┼──────────┼──────┼───────
        Day 32│<p>...</p>│ELT      │elt   │ready

Step 2: Apps Script reads that row
        const [title, content, category, tags, status] = row;

Step 3: Script builds a JSON object (the "message" to send)
        const payload = {
          title:    "Day 32 – Listening",
          content:  "<p>Listening is...</p>",
          category: "ELT",
          tags:     "elt,listening",
          status:   "draft"
        };

Step 4: Script sends an HTTP POST request to WordPress
        UrlFetchApp.fetch(WP_URL, { method: 'POST', payload: ... });

Step 5: WordPress receives the request, creates the post
        Returns: { post_id: 1234, link: "https://..." }

Step 6: Script marks the row as "published" so it won't run again
        sheet.getRange(rowNumber, 5).setValue('published');
```

---

## Part 3: What is JSON and Why Does It Matter?

JSON (JavaScript Object Notation) is how programs talk to each other. Think of it as a structured letter:

```json
{
  "title": "Day 32 – Listening",
  "content": "<p>Today I focused on minimal pairs...</p>",
  "category": "ELT Masterclass",
  "tags": "listening, pronunciation, ELT",
  "status": "draft"
}
```

Your WordPress plugin reads this letter and creates the post. The keys ("title", "content", etc.) must match exactly what the plugin expects.

---

## Part 4: Step-by-Step Setup

### Step 1: Prepare your Google Sheet

1. Open Google Sheets
2. Create a new spreadsheet
3. Add this header row in row 1:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Title | Content | Category | Tags | Status | ScheduleDate | MetaDesc |

4. Add a sample row:

| Day 32 – Listening | `<p>Today I worked on minimal pairs.</p>` | ELT | listening,elt | ready | (leave blank) | Practice minimal pairs in English |

### Step 2: Open Apps Script

1. In your spreadsheet: **Extensions → Apps Script**
2. A new tab opens with a code editor
3. Delete everything in the editor
4. Paste this complete script:

```javascript
// ============================================================
// WordPress Publisher from Google Sheets
// Setup: Extensions > Apps Script, paste this, save, run once
// ============================================================

const WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

function publishFromSheet() {
  // Get the sheet named "Queue" (or Sheet1 if you haven't renamed it)
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
                  .getSheetByName('Queue') ||
                SpreadsheetApp.getActiveSpreadsheet()
                  .getSheets()[0];

  // Get ALL data (getDataRange = all cells that have content)
  const allRows = sheet.getDataRange().getValues();

  // Start from row index 1 to skip the header row
  for (let rowIndex = 1; rowIndex < allRows.length; rowIndex++) {
    const row = allRows[rowIndex];

    // Destructure columns A through G
    const title       = row[0];  // Column A
    const content     = row[1];  // Column B
    const category    = row[2];  // Column C
    const tags        = row[3];  // Column D
    const status      = row[4];  // Column E
    const schedDate   = row[5];  // Column F
    const metaDesc    = row[6];  // Column G

    // Skip empty rows or already-published rows
    if (!title || status === 'published') continue;

    // Auto-detect category if not provided
    const finalCategory = category || guessCategory(title, content);
    const finalTags     = tags     || suggestTags(title + ' ' + content);
    const finalMeta     = metaDesc || stripHtml(content).slice(0, 160);

    // Build the payload (the JSON message to send to WordPress)
    const payload = {
      title:            title,
      content:          content,
      category:         finalCategory,
      tags:             finalTags,
      status:           status === 'future' ? 'future' : 'draft',
      meta_description: finalMeta,
      seo_title:        buildSeoTitle(title)
    };

    // Add schedule date if provided and status is 'future'
    if (status === 'future' && schedDate) {
      payload.date = schedDate instanceof Date
        ? schedDate.toISOString()
        : schedDate;
    }

    // Send to WordPress
    const result = sendToWordPress(payload);

    if (result && result.post_id) {
      // Mark as published in column E
      sheet.getRange(rowIndex + 1, 5).setValue('published');
      // Log the time in column F (overwrite schedule date)
      if (!schedDate) sheet.getRange(rowIndex + 1, 6).setValue(new Date());
      Logger.log('Published: ' + title + ' → ID ' + result.post_id);
    } else {
      Logger.log('Failed: ' + title);
    }

    // Wait 1.5 seconds between posts to avoid rate limiting
    Utilities.sleep(1500);
  }
}

// ── Send data to WordPress ────────────────────────────────────────────────────
function sendToWordPress(postData) {
  // Get API key from secure Script Properties (never hardcode!)
  const apiKey = PropertiesService.getScriptProperties()
                   .getProperty('WP_KEY');

  if (!apiKey) {
    Logger.log('ERROR: WP_KEY not set in Script Properties');
    return null;
  }

  const options = {
    method:          'POST',
    headers: {
      'X-Sourov-Key':  apiKey,
      'Content-Type':  'application/json'
    },
    payload:          JSON.stringify(postData),
    muteHttpExceptions: true  // Don't crash on HTTP errors
  };

  try {
    const response     = UrlFetchApp.fetch(WP_API_URL, options);
    const responseText = response.getContentText();
    const responseCode = response.getResponseCode();

    Logger.log('HTTP ' + responseCode + ': ' + responseText);

    if (responseCode === 200 || responseCode === 201) {
      return JSON.parse(responseText);
    } else {
      Logger.log('WordPress returned error: ' + responseText);
      return null;
    }
  } catch (error) {
    Logger.log('Network error: ' + error.message);
    return null;
  }
}

// ── Auto-categorisation ───────────────────────────────────────────────────────
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();

  // Order matters: more specific first
  if (text.includes('celta'))              return 'CELTA';
  if (text.includes('grammar'))            return 'Grammar';
  if (text.includes('pronunciation') ||
      text.includes('phonology') ||
      text.includes('listening'))          return 'Listening & Phonology';
  if (text.includes('speaking') ||
      text.includes('fluency'))            return 'Speaking';
  if (text.includes('writing') ||
      text.includes('essay'))              return 'Writing Skills';
  if (text.includes('vocabulary') ||
      text.includes('idiom'))              return 'Vocabulary';
  if (text.includes('reading'))            return 'Reading';

  return 'ELT Masterclass';
}

// ── Auto-tagging ──────────────────────────────────────────────────────────────
function suggestTags(text) {
  const tagMap = {
    'grammar':       'grammar',
    'listening':     'listening',
    'speaking':      'speaking',
    'pronunciation': 'pronunciation',
    'vocabulary':    'vocabulary',
    'reading':       'reading',
    'writing':       'writing',
    'celta':         'CELTA',
    'elt':           'ELT',
    'idiom':         'idioms',
    'fluency':       'fluency',
    'phonology':     'phonology'
  };

  const lower = text.toLowerCase();
  const found = Object.entries(tagMap)
    .filter(([keyword]) => lower.includes(keyword))
    .map(([, tag]) => tag);

  return [...new Set(found)].slice(0, 5).join(',');
}

// ── Helpers ───────────────────────────────────────────────────────────────────
function stripHtml(html) {
  return html.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function buildSeoTitle(title) {
  const clean = title.replace(/^Day \d+\s*[–-]\s*/i, '');
  const short = clean.slice(0, 50);
  return short + ' | Sourov Deb ELT';
}
```

### Step 3: Store your API key securely

In Apps Script:
1. Click the **gear icon** (Project Settings)
2. Scroll to **Script Properties**
3. Click **Add property**
4. Property name: `WP_KEY`
5. Value: your WordPress plugin key
6. Click **Save script properties**

The script reads it with `PropertiesService.getScriptProperties().getProperty('WP_KEY')`. This key is never visible in the code.

### Step 4: Test it manually

1. Add one row to your sheet with `status = ready`
2. In Apps Script, click the **Run** button (▶) next to `publishFromSheet`
3. Authorize the script when prompted (it needs permission to make HTTP requests)
4. Check the **Execution log** (View → Execution log) for output
5. Check WordPress admin → Posts → Drafts for your new post

### Step 5: Set an automatic time trigger

1. Click the **alarm clock icon** (Triggers) in the left sidebar
2. Click **+ Add Trigger** (bottom right)
3. Settings:
   - Function: `publishFromSheet`
   - Deployment: Head
   - Event source: **Time-driven**
   - Type: **Hour timer**
   - Interval: Every hour (or every 4/6 hours)
4. Click **Save**

Now it runs automatically. You fill the sheet, the system publishes.

---

## Part 5: Common Errors and Fixes

| Error message | Cause | Fix |
|---------------|-------|-----|
| `WP_KEY not set` | Script Properties not configured | Follow Step 3 above |
| `HTTP 401` | Wrong API key | Check your plugin key in WordPress |
| `HTTP 404` | Wrong API URL | Check the endpoint URL |
| `SyntaxError in JSON` | Content has unescaped quotes | Use `JSON.stringify()` — already handled |
| Sheet not found | Wrong sheet name | Change `'Queue'` to match your sheet tab name |
| Posts publish twice | Status column not updating | Ensure column E is updating to 'published' |

---

## Part 6: Upgrading to AI-Generated Content

Once the basic sheet-to-WordPress pipeline works, you can add AI:

```javascript
function generateContentWithAI(title) {
  const DEEPSEEK_KEY = PropertiesService.getScriptProperties()
                         .getProperty('DEEPSEEK_KEY');

  const response = UrlFetchApp.fetch('https://api.deepseek.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + DEEPSEEK_KEY,
      'Content-Type': 'application/json'
    },
    payload: JSON.stringify({
      model: 'deepseek-chat',
      messages: [
        { role: 'system', content: 'You are an ELT blog writer. Return only HTML content.' },
        { role: 'user',   content: 'Write a 500-word blog post titled: ' + title }
      ]
    })
  });

  const data = JSON.parse(response.getContentText());
  return data.choices[0].message.content;
}
```

With this, you only need a **title** in your sheet — the AI writes the full post.

---

## Summary: What You Now Know

1. **CSV** = plain text spreadsheet that everything can read
2. **Google Apps Script** = JavaScript running in Google's cloud, free
3. **The flow**: Sheet row → JSON payload → HTTP POST → WordPress post
4. **Security**: API keys in Script Properties, never in code
5. **Automation**: Time triggers run the script every hour without you
6. **AI upgrade**: DeepSeek API generates content from just a title

Start with Step 4 (manual test). Once one post publishes correctly, everything else follows.
