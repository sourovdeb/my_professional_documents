# Complete WordPress Publishing Automation System

> Your "just write" system. You write once, the system handles tags, categories, SEO, scheduling, and publishing.

---

## Architecture Overview

```
[You write] → [Google Sheets queue] → [Apps Script] → [WordPress API] → [Published post]
                      ↑
              [Logseq folder watcher]
              [Python desktop app]
              [GitHub Actions]
```

All three entry points feed into the same Google Sheets queue or directly call WordPress.

---

## Method 1: Google Sheets + Apps Script (Easiest — Start Here)

Full tutorial in `docs/CSV_GOOGLE_APPS_SCRIPT_TUTORIAL.md`.

Script file: `scripts/sheet_publisher.gs`

Quick setup:
1. Open Google Sheets with your posts
2. Extensions → Apps Script → paste script from `scripts/sheet_publisher.gs`
3. Run `testConnection` once to authorize
4. Set hourly trigger on `publishFromSheet`
5. Add posts to sheet with status `ready` → they publish automatically

---

## Method 2: Logseq + Folder Watcher (Most Natural for Writers)

Script file: `scripts/folder_watcher.js`

```bash
# Prerequisites
npm install  # installs chokidar and node-fetch

# Run the watcher (keep it running in background)
node scripts/folder_watcher.js

# On Mac: autostart via launchd
# On Linux: autostart via systemd service
# On Windows: autostart via Task Scheduler
```

**Logseq workflow:**
1. Write your daily post in Logseq
2. Add `#publish` tag to the page
3. Export as Markdown to `~/wordpress_queue/`
4. Folder watcher detects new file, publishes to WordPress as draft
5. Review draft in WordPress admin, click Publish

---

## Method 3: Python Desktop App (GUI — No Terminal Needed)

Script file: `scripts/wp_publisher.py`

```bash
pip install requests tkinter
python scripts/wp_publisher.py
```

Opens a window where you can:
- Paste title and content
- Select category from dropdown
- Add tags
- Choose Draft / Publish / Schedule
- Click one button to publish

---

## Method 4: GitHub Actions (Auto-Publish on Git Push)

Workflow file: `.github/workflows/publish_on_push.yml`

**How it works:**
1. Write a Markdown file in the `drafts/` folder
2. Run `git add drafts/my-post.md && git commit -m 'new post' && git push`
3. GitHub Action automatically publishes the post to WordPress
4. The file is moved to `published/` in the repo

**Setup:**
1. Go to your GitHub repo → Settings → Secrets and variables → Actions
2. Add secret: `WP_API_KEY` = your WordPress API key
3. Push any `.md` file to the `drafts/` folder

---

## Automatic Categorisation Rules

All methods use the same keyword-based categorisation:

| Keywords in title/content | Category assigned |
|--------------------------|-------------------|
| grammar, tense, verb, syntax | Grammar |
| listen, phonology, pronunciation | Listening & Phonology |
| speak, fluency, conversation | Speaking & Fluency |
| celta, teaching practice, lesson plan | CELTA |
| reading, writing, essay, text | Reading & Writing |
| technology, app, digital | Technology in ELT |
| career, job, certification | Career & Professional Development |
| (default) | ELT Masterclass |

To extend: edit the `guessCategory()` function in whichever script you use.

---

## SEO Auto-Generation

For each post, the system automatically generates:

| Field | How it's generated |
|-------|-------------------|
| SEO Title | Same as post title (or custom in column G) |
| Meta Description | First 155 characters of content (stripped of HTML) |
| Tags | Keywords matched from title (see `suggestTags()`) |
| Category | Keyword-matched from title/content |

For AI-powered generation (much better quality), use DeepSeek:
- See `docs/DEEPSEEK_API_GUIDE.md` — costs $0.004/month for 30 posts

---

## Scheduling Strategy

### Batch Writing (Recommended for Bipolar)

On a good energy day:
1. Write 5-7 posts in one session
2. Add all to Google Sheets queue with status `future`
3. Assign dates one week apart
4. System auto-publishes even if you're resting

This creates a **content buffer** — you can rest for 2 weeks and your blog still publishes regularly.

### Recommended Schedule for ELT Blog

- Monday: Grammar post
- Wednesday: Listening/Speaking post  
- Friday: CELTA reflection or career post
- Saturday: Optional — technology or resource post

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Post published twice | Check status column updates to `published` after posting |
| Wrong category | Edit `guessCategory()` to add your specific keywords |
| HTML shows as raw text | Wrap content in `<p>` tags, or use WordPress editor |
| Images not showing | Add featured image via WordPress admin after auto-posting |
| Schedule not working | Check WordPress timezone matches your timezone setting |
| API 401 error | Verify your API key in the script configuration |
| API 404 error | Verify your WordPress URL and plugin is active |

---

## WordPress Plugin Requirements

Your automation uses the custom plugin `sourov-ai-controller.php`.

Ensure these are active in WordPress Admin → Plugins:
- `sourov-ai-controller` (your custom plugin)
- Any SEO plugin (Rank Math or All in One SEO) — for meta descriptions

The plugin must register the REST route: `POST /wp-json/sourov/v1/ai-post`

Accepted parameters:
```json
{
  "title": "string (required)",
  "content": "string (required)",
  "status": "draft|publish|future",
  "category": "string (category name)",
  "tags": "string (comma-separated tag names)",
  "meta_description": "string (max 155 chars)",
  "seo_title": "string",
  "date": "ISO8601 datetime (for scheduled posts)"
}
```
