# Pre-built open-source tools — zero setup needed

If you don't want to run scripts yourself, these tools do it for you.
All free, all open source or free tier. Ranked by ease of use.

## 1. Typebot + Make (easiest — no code)
**What:** Visual chatbot that collects your post (title, content, tags) then sends
it to WordPress via webhook. You talk to a bot, it publishes.
- Typebot: https://typebot.io (open source, self-hostable)
- Make: https://make.com (free tier: 1000 operations/month)
- Setup time: ~1 hour, no coding

## 2. n8n (recommended — most powerful, free)
**What:** Visual workflow editor. Connects Google Sheets → WordPress automatically.
Pre-built WordPress node built in.
- https://n8n.io (self-host free, cloud free tier)
- Template: "Google Sheets → WordPress post on new row"
- What it does: monitors your Sheet, publishes any new row marked "publish"
- Zero code, drag-and-drop
- Setup time: ~2 hours

## 3. Zapier / Pabbly Connect (no code, hosted)
**What:** Zapier (paid) or Pabbly Connect (free, lifetime) — same idea as n8n
but simpler to start.
- Pabbly Connect: https://connect.pabbly.com (free tier)
- Workflow: Google Sheets new row → WordPress create post
- Supports categories, tags, status
- Setup time: 30 min

## 4. Ghost (if you ever migrate)
**What:** If you move your blog to Ghost, it has a built-in content API and
editorial calendar. Much cleaner than WordPress for a solo writer.
- https://ghost.org (open source, self-host free)
- Better writing experience, built-in SEO, owned audience

## 5. Wordable (for Google Docs → WordPress)
**What:** If you write in Google Docs, Wordable converts and publishes it to
WordPress with one click — formatting preserved, images uploaded.
- https://wordable.io (free trial, then paid)
- Easiest path if Google Docs is your writing tool

## 6. WP All Import (bulk import from spreadsheet)
**What:** Import posts from CSV/Google Sheet into WordPress in bulk.
Good for a one-time fix to categorise/tag your existing 32+ posts.
- https://www.wpallimport.com (free version on wordpress.org)
- Upload a CSV with Post ID, Category, Tags → it bulk-updates them all

## 7. Obsidian + GitHub + GitHub Actions (this repo)
**What:** Write in Obsidian (your notes), commit to this repo's `posts/to-publish/`,
GitHub Actions auto-publishes to WordPress as draft.
- Requires the `automation/github/publish.yml` from this repo
- Setup: add `WP_SITE` and `WP_API_KEY` as GitHub Secrets → done
- Best if you're already using Obsidian

## RECOMMENDED STACK for you:
1. **Write** in Obsidian or Logseq
2. **One-click publish** via n8n workflow OR the Google Sheet + Apps Script
3. **Review drafts** in WordPress before publishing live
4. That's it — you write, the system handles the rest
