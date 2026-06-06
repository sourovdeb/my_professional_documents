# Your Complete WordPress Automation System

## Quick Start (5 Minutes)

**Goal**: Publish your first automated post without touching code.

### Option A: Google Sheets (No Setup)
1. Open sheets.google.com → create sheet named **Queue**
2. Headers: `Title | Content | Category | Tags | Status | ScheduleDate | SEO_Title | Meta_Description`
3. Add one post in Row 2, set Status = `draft`
4. Open Extensions → Apps Script → paste `scripts/sheet_publisher.gs`
5. Run `publishFromSheet` → check WordPress dashboard

### Option B: Fully Automated (15 min setup, then zero work)
1. Complete Option A
2. Set a time trigger: every hour (clock icon in Apps Script → Add Trigger)
3. Fill sheet → posts appear in WordPress automatically

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   YOUR WRITING                      │
│  (Logseq / Google Docs / Google Sheets / .md files) │
└─────────────┬───────────────────────────────────────┘
              │
    ┌─────────▼─────────────┐
    │   AUTOMATION LAYER    │
    │                       │
    │  A: Google Sheets     │  ← Easiest
    │  B: Folder Watcher    │  ← For Logseq users
    │  C: GitHub Actions    │  ← For version control
    └─────────┬─────────────┘
              │
    ┌─────────▼─────────────┐
    │   AI ENRICHMENT       │
    │  DeepSeek (cheapest)  │
    │  Groq (free tier)     │
    │  Ollama (local/free)  │
    └─────────┬─────────────┘
              │
    ┌─────────▼─────────────┐
    │  WORDPRESS API        │
    │  sourovdeb.com        │
    │  /wp-json/sourov/v1/  │
    └───────────────────────┘
```

---

## Method A: Google Sheets → WordPress

**Best for**: Daily batch publishing, reviewing before publish, scheduling  
**Cognitive load**: Very low — just fill a spreadsheet  
**Script**: `scripts/sheet_publisher.gs`  
**Tutorial**: `docs/CSV_GOOGLE_APPS_SCRIPT_TUTORIAL.md`

---

## Method B: Folder Watcher → WordPress

**Best for**: Logseq users, markdown writers  
**Cognitive load**: Very low — just save a file  
**Scripts**: `scripts/folder_watcher.js` or `scripts/auto_publisher.py`

Any `.md` file dropped in `~/wordpress_queue/` becomes a WordPress draft within 15 minutes.

---

## Method C: GitHub Push → WordPress

**Best for**: Version-controlled publishing  
**Workflow**: `.github/workflows/publish_on_push.yml`

Push a markdown file to `drafts/` → GitHub Action converts it to a WordPress draft automatically.

---

## AI Provider Comparison

| Provider | Cost | Quality | Setup |
|----------|------|---------|-------|
| Groq free tier | $0/month | High | Easy |
| DeepSeek-V3 | ~$0.02/month | High | Easy |
| Ollama local | $0 forever | Good | Medium |
| Mistral free | $0 | High | Easy |

See `docs/DEEPSEEK_API_GUIDE.md` for full setup and code.

---

## WordPress Health

- Monthly: run `scripts/fix_wp_categories.py`
- Weekly: check the WP AI Studio Posts tab
- See `docs/WORDPRESS_HEALTH_GUIDE.md`

---

## File Index

```
docs/
├── MASTER_AUTOMATION_GUIDE.md        ← You are here
├── DEEPSEEK_API_GUIDE.md             ← AI cost comparison + setup
├── CSV_GOOGLE_APPS_SCRIPT_TUTORIAL.md ← Deep tutorial (what & why)
├── FREE_AI_TOOLS_COMPARISON.md       ← All free AI tools
├── OPEN_SOURCE_TOOLS_COLLECTION.md   ← Curated GitHub tools
├── AUDIO_VIDEO_BANNER_TOOLS.md       ← Media production tools
├── MENTAL_HEALTH_AUTOMATION.md       ← Bipolar-friendly workflows
└── WORDPRESS_HEALTH_GUIDE.md         ← Fix categories & tags

scripts/
├── wp_publisher.py      ← Python GUI (Tkinter)
├── auto_publisher.py    ← Automated folder watcher
├── sheet_publisher.gs   ← Google Apps Script
├── folder_watcher.js    ← Node.js watcher
└── fix_wp_categories.py ← WordPress category/tag fixer

.github/workflows/
└── publish_on_push.yml  ← Auto-publish on git push
```
