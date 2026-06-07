# Complete WordPress Automation Guide
## Write Once, Publish Everywhere — The System for Sourov Deb

This guide covers every layer of automation from writing to publishing. Start with Section 1 and add more only when comfortable.

---

## Table of Contents

1. [The Core Workflow](#1-the-core-workflow)
2. [Google Sheets + Apps Script](#2-google-sheets--apps-script)
3. [Fix WordPress Categories & Tags](#3-fix-wordpress-categories--tags)
4. [GitHub Actions Auto-Publish](#4-github-actions-auto-publish)
5. [Scheduling & SEO Automation](#5-scheduling--seo-automation)
6. [Open Source Tools Stack](#6-open-source-tools-stack)
7. [Low-Effort Workflow for Bad Days](#7-low-effort-workflow-for-bad-days)

---

## 1. The Core Workflow

**What you do:** Write a file. Save it. Done.

**What the system does automatically:**
- Detects new file in your watch folder
- Extracts title (first heading) and body
- Guesses category from keywords
- Generates 3–5 tags
- Builds SEO meta description (first 160 chars)
- Sends to WordPress as a **draft** for your review
- Archives the processed file
- (Optional) Sends you a Telegram notification

**The watch folder approach is the most important concept.** Create a folder (local, Dropbox, or Google Drive). Drop a Markdown file in. The system handles the rest.

### File naming convention

```
2026-06-15-listening-skills.md
2026-06-16-grammar-conditionals.md
2026-06-17-celta-reflection.md
```

### Markdown template

```markdown
# Your Post Title Here

Your content starts here. Write naturally.
The first paragraph becomes the meta description.

## Subheading

More content...
```

---

## 2. Google Sheets + Apps Script

This is the **recommended starting point** — no code to install, runs in your browser.

### Sheet Structure (tab named "Queue")

| A: Title | B: Content | C: Category | D: Tags | E: Status | F: ScheduleDate | G: MetaDesc |
|----------|------------|-------------|---------|-----------|-----------------|-------------|
| Day 32 – Listening | `<p>...</p>` | ELT | listening,CELTA | future | 2026-06-15T09:00 | Improve your listening |

**Status values:** `ready` (publishes as draft), `future` (schedules), `published` (skip — already done)

### Apps Script code

Open your spreadsheet → **Extensions → Apps Script** → paste this:

```javascript
const WP_API = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');

function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  const rows  = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status, date, metaDesc] = rows[i];
    if (!title || status === 'published') continue;

    const payload = {
      title,
      content,
      category: category || guessCategory(title, content),
      tags:     tags     || suggestTags(title),
      status:   status === 'future' ? 'future' : 'draft',
      meta_description: metaDesc || content.replace(/<[^>]+>/g, '').slice(0, 160)
    };
    if (status === 'future' && date) payload.date = date;

    const result = callWordPress(payload);
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date());
    }
    Utilities.sleep(1500);
  }
}

function callWordPress(data) {
  try {
    const res = UrlFetchApp.fetch(WP_API, {
      method: 'POST',
      headers: { 'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    });
    return JSON.parse(res.getContentText());
  } catch(e) {
    Logger.log('Error: ' + e.message);
    return null;
  }
}

function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('grammar'))      return 'Grammar';
  if (text.includes('listening'))    return 'Listening & Phonology';
  if (text.includes('pronunciation'))return 'Listening & Phonology';
  if (text.includes('celta'))        return 'CELTA';
  if (text.includes('speaking'))     return 'Speaking';
  if (text.includes('writing'))      return 'Writing Skills';
  return 'ELT Masterclass';
}

function suggestTags(title) {
  const keywords = ['grammar','listening','speaking','CELTA','ELT',
                    'pronunciation','reading','writing','vocabulary'];
  return keywords.filter(k => title.toLowerCase().includes(k.toLowerCase())).join(',');
}
```

### Store your API key safely

In Apps Script: **Project Settings → Script Properties → Add property**
- Key: `WP_KEY`
- Value: your WordPress plugin key

**Never paste the key directly in the code.**

### Set a time trigger

In Apps Script: **Triggers (alarm icon) → Add Trigger**
- Function: `publishFromSheet`
- Event source: Time-driven
- Type: Every hour (or every 6 hours)

---

## 3. Fix WordPress Categories & Tags

See `../scripts/fix_wp_categories_tags.py` for the full script.

### Common problems and fixes

| Problem | Cause | Fix |
|---------|-------|-----|
| Posts in "Uncategorized" | No category sent with post | Use `guessCategory()` function |
| Duplicate tags ("elt", "ELT", "Elt") | Inconsistent case | Script normalises all tags to title case |
| Tags not appearing | Tag doesn't exist in WP yet | Script creates missing tags via REST API |
| Wrong category assigned | Keyword list too short | Extend `guessCategory()` with more rules |

### Quick fix via WP REST API

```bash
# List all categories
curl https://sourovdeb.com/wp-json/wp/v2/categories

# List all tags
curl https://sourovdeb.com/wp-json/wp/v2/tags

# Update a post's category (replace POST_ID and CAT_ID)
curl -X POST https://sourovdeb.com/wp-json/wp/v2/posts/POST_ID \
  -H "Authorization: Basic BASE64_USER_PASS" \
  -H "Content-Type: application/json" \
  -d '{"categories": [CAT_ID]}'
```

---

## 4. GitHub Actions Auto-Publish

Every time you push a Markdown file to the `drafts/` folder, this action publishes it to WordPress automatically.

See `.github/workflows/publish_on_push.yml` (already in this repo).

**Setup:**
1. Go to **Settings → Secrets → Actions** in this repo
2. Add secret: `WP_API_KEY` = your plugin key
3. Push any `.md` file to `drafts/`
4. Action runs, post appears in WordPress as draft

---

## 5. Scheduling & SEO Automation

### Auto-schedule: spread posts over a week

Add this to your Apps Script to auto-assign future dates:

```javascript
function getNextSlot() {
  // Posts Mon/Wed/Fri at 9 AM
  const days = [1, 3, 5];
  const now  = new Date();
  for (let d = 1; d <= 14; d++) {
    const candidate = new Date(now);
    candidate.setDate(now.getDate() + d);
    candidate.setHours(9, 0, 0, 0);
    if (days.includes(candidate.getDay())) return candidate.toISOString();
  }
}
```

### SEO title formula

```javascript
function buildSeoTitle(title) {
  // Keep under 60 chars, add site name if room
  const base = title.slice(0, 50);
  return base.includes('|') ? base : base + ' | Sourov Deb';
}
```

---

## 6. Open Source Tools Stack

| Tool | What it does | Free? |
|------|-------------|-------|
| **n8n** (self-hosted) | Visual no-code automation, connects Sheets→WordPress | Yes |
| **wp-cli** | Terminal control of WordPress | Yes |
| **Huginn** | Agent-based automation (scrape, monitor, post) | Yes |
| **Zapier** | 100 tasks/month free tier | Free tier |
| **Buffer** | Schedule social posts from RSS | Free tier |
| **Ollama** | Local AI, zero cost after install | Yes |
| **DeepSeek API** | Cheapest paid AI (~$0.001/1K tokens) | Pay-as-go |

---

## 7. Low-Effort Workflow for Bad Days

When energy is low (bipolar/depression):

1. **Voice-type** into Google Docs (Tools → Voice Typing)
2. Save the document — don't edit
3. The sheet watcher picks it up automatically
4. Post goes to WordPress as draft
5. Review later when you have energy

**Templates** reduce decisions. Keep `ELT_TEMPLATE.md` in your watch folder and copy it each day:

```markdown
# Day [N] – [Topic]

[ONE sentence about what you learned or taught today.]

## What worked

[2–3 bullet points]

## What to try next

[1 action item]
```

Five minutes of writing produces a publishable post with this template.
