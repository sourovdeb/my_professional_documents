# Automation — Write Once, Publish Everywhere

One rule: **you write. The system handles categories, tags, SEO, scheduling.**

## Setup (once, 10 minutes)

1. Copy `.env.example` to `.env` and fill in your credentials:
   ```
   WP_SITE=https://sourovdeb.com
   WP_API_KEY=your_key_here
   ```
2. Pick ONE of the six tools below. Use it for one week. Then stop shopping.

## Six ways to publish from a distance

| # | Tool | Best for | Setup | Effort |
|---|---|---|---|---|
| 1 | **Google Sheet + Apps Script** | Daily publishing from your existing sheet | 15 min | One click |
| 2 | **Python Tkinter GUI** | Writing directly in a desktop app | 5 min (pip install) | Write + click |
| 3 | **Logseq → WordPress** | Writing in Logseq, exporting to WP | 10 min (node) | Write + one command |
| 4 | **GitHub Actions** | Committing .md files → auto-publishes | 20 min (add secrets) | Commit + push |
| 5 | **n8n visual workflow** | Full automation, no code | 2 hours | Zero (runs itself) |
| 6 | **WP All Import CSV** | Bulk-fix categories on existing posts | 30 min | One-time |

## For a non-technical person (start here)

**The simplest path:**
1. Your Google Sheet already has the columns. Add the Apps Script from `sheets/WP_PUBLISHER.gs`
2. Set two Script Properties: `WP_SITE` and `WP_API_KEY`
3. A "📝 WordPress" menu appears in your Sheet
4. Mark any row `Approved = TRUE` → click **Publish approved rows** → done

That's it. Everything else (categories, tags, SEO, scheduling) is filled in the sheet
before publishing. You never touch WordPress directly.

## Crash-day mode
On a bad day, open the sheet, type 500 words in the Content column, mark Approved = TRUE,
click the menu button. Two minutes. Done. The streak holds.

## Files in this folder

```
.env.example         ← credentials template (safe to commit — no real secrets)
sheets/WP_PUBLISHER.gs   ← Google Apps Script (Option 1)
python/wp_publisher.py   ← Tkinter desktop GUI (Option 2)
logseq/logseq_to_wp.js   ← Logseq → WordPress via Node.js (Option 3)
github/publish.yml       ← GitHub Actions workflow (Option 4)
tools/OPEN_SOURCE.md     ← pre-built tools: n8n, WP All Import, etc. (Options 5-6)
```
