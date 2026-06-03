# Automation Scripts

**Python scripts to handle repetitive tasks. Focus on writing, let scripts handle the rest.**

---

## What's Here

- **wordpress_uploader.py** — Convert markdown essays to WordPress posts (via deploy.php)
- **[Future] email_scheduler.py** — Schedule bulk emails
- **[Future] draft_manager.py** — Organize and version drafts
- **[Future] backup_and_sync.py** — GitHub + local backup automation

---

## Setup (First Time Only)

### 1. Create .env File

Create `.env` in this directory with your WordPress credentials:

```bash
# automation_scripts/.env
DEPLOY_URL=https://www.sourovdeb.com/deploy.php
DEPLOY_KEY=0767044896thevenet_
```

**⚠️ IMPORTANT:** This file is in `.gitignore` — it will NOT be pushed to GitHub

### 2. Install Python Dependencies

```bash
pip install python-dotenv requests
```

Or all at once:
```bash
pip install python-dotenv requests jinja2 pandas
```

---

## WordPress Uploader (The Main Tool)

Convert markdown essays to WordPress posts instantly.

### Basic Usage

```bash
# Save as draft (review before publishing)
python3 wordpress_uploader.py \
  --file ../blog_drafts/2026_06_essays/my_essay.md \
  --status draft \
  --save-only

# Publish directly (careful!)
python3 wordpress_uploader.py \
  --file ../blog_drafts/2026_06_essays/my_essay.md \
  --status publish \
  --category "Mental Health" \
  --tags "bipolar, productivity"
```

### Options

```
--file [PATH]              Required: Markdown file to convert
--status [draft/publish]   Default: draft
--category [NAME]          Default: Uncategorized
--tags [tag1, tag2]        Comma-separated tags
--dry-run                  Preview without uploading
--save-only                Save locally without uploading
```

### Workflow

**Step 1: Save as Draft (First Review)**
```bash
python3 wordpress_uploader.py \
  --file ../blog_drafts/2026_06_essays/email_management.md \
  --status draft \
  --save-only
```
Output: `../wordpress_ready/staging/20260603_email_management.json`

**Step 2: Review on Your Computer**
- Open the JSON file
- Check formatting, links, categories
- Make sure excerpt is compelling

**Step 3: Upload to WordPress**
```bash
python3 wordpress_uploader.py \
  --file ../wordpress_ready/staging/20260603_email_management.json \
  --status draft
```

**Step 4: Review on WordPress Admin**
- Go to WordPress dashboard
- Check "Drafts" section
- Read the preview
- Mobile test: view on phone

**Step 5: Publish**
```bash
python3 wordpress_uploader.py \
  --file ../wordpress_ready/staging/20260603_email_management.json \
  --status publish
```

---

## Markdown → HTML Conversion

The script automatically converts:

| Markdown | HTML |
|----------|------|
| `## Header` | `<h2>Header</h2>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `[link](url)` | `<a href="url">link</a>` |
| `- item` | `<ul><li>item</li></ul>` |

So your markdown essays automatically become properly formatted WordPress posts.

---

## Essay Metadata Format

Your markdown file should have this metadata:

```markdown
# Your Essay Title

**Date:** 2026-06-03
**Status:** Ready
**Category:** [Mental Health]
**Tags:** [bipolar, productivity, email]
**Excerpt:** [Optional 160-character summary]

---

## Hook (1-2 sentences)
...rest of essay...
```

The script extracts:
- Title from `# Your Essay Title`
- Status, category, tags from metadata
- Excerpt (auto-generated if missing)

---

## Dry-Run: Preview First

Nervous about uploading? Test first:

```bash
python3 wordpress_uploader.py \
  --file my_essay.md \
  --dry-run
```

This shows:
- What title will be
- Word count
- Categories & tags
- Everything *except* actually uploading

---

## Troubleshooting

**Error: "DEPLOY_KEY not found in .env"**
- Create `.env` file in this directory
- Add: `DEPLOY_KEY=your_secret_key`
- Restart terminal

**Error: "Connection error"**
- Check internet connection
- Verify DEPLOY_URL is correct
- Try: `curl https://www.sourovdeb.com/deploy.php`

**Error: "Upload failed: server error"**
- Check WordPress is online: https://www.sourovdeb.com
- Check deploy.php is still there
- Look at response error message

**HTML is broken in WordPress**
- Links formatting? Check markdown syntax: `[text](url)`
- Lists broken? Make sure they're on separate lines
- Line breaks weird? WordPress sometimes removes single breaks

---

## Future Scripts (Coming Soon)

### email_scheduler.py
```bash
# Schedule bulk emails for later
python3 email_scheduler.py \
  --csv contacts.csv \
  --send-at "2026-06-10 09:00" \
  --template "job_inquiry"
```

### draft_manager.py
```bash
# Organize and version essays
python3 draft_manager.py --organize    # Auto-sort by date
python3 draft_manager.py --archive     # Move old essays
python3 draft_manager.py --list        # Show all drafts + status
```

### backup_and_sync.py
```bash
# Automatic backup and sync
python3 backup_and_sync.py --backup    # GitHub + local copy
python3 backup_and_sync.py --sync      # Sync across devices
```

---

## Scripts You'll Run Often

**Daily:**
```bash
# After finishing an essay
python3 wordpress_uploader.py --file essay.md --save-only
```

**Weekly:**
```bash
# When ready to publish
python3 wordpress_uploader.py \
  --file staging/essay.json \
  --status draft
```

**Monthly:**
```bash
# Clean up old drafts
python3 draft_manager.py --organize
```

---

## Best Practices

✅ **DO:**
- Write essay first, upload second
- Use `--save-only` to review locally
- Test with `--dry-run` first
- Review on WordPress before publish
- Keep `.env` private (never commit it)

❌ **DON'T:**
- Upload while manic (wait 24h, re-read first)
- Skip review step
- Publish directly without drafting
- Share .env file or DEPLOY_KEY
- Edit essays in WordPress instead of GitHub

---

## Environment Variables

Your scripts can read these from `.env`:

```
DEPLOY_URL=https://www.sourovdeb.com/deploy.php
DEPLOY_KEY=your_secret_key_here
```

Or pass as command-line flags:
```bash
python3 wordpress_uploader.py \
  --file essay.md \
  --env-url https://www.sourovdeb.com/deploy.php
```

---

## Getting Help

If a script breaks:

1. **Check error message** — Python tells you what went wrong
2. **Try --dry-run** — Preview without uploading
3. **Check .env file** — Make sure credentials are there
4. **Check internet** — Can you reach sourovdeb.com?
5. **Check WordPress** — Is https://www.sourovdeb.com/wp-admin online?

---

## Adding New Scripts

When you create a new automation script:

1. Name it clearly: `automation_name.py`
2. Add docstring at top with usage
3. Include `--help` flag
4. Add to this README
5. Commit with message: "Add: [script name]"

Example:
```python
#!/usr/bin/env python3
"""
Script description

Usage:
    python3 script_name.py --option value

Requires:
    pip install package_name
"""
```

---

**Automation saves time. More time = more writing. More writing = your voice heard.**
