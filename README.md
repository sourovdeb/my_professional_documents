# AI Hub — Multi-Provider Email & WordPress Automation v2.0

## PROJECT OVERVIEW

Open-source, API-driven Chrome Extension combining multi-model AI assistance with email and WordPress automation.

- Version: 2.0.0
- License: MIT
- All credentials via environment variables — none hardcoded

## FEATURES

**Multi-Model AI Support:**
- Anthropic API (claude-* models)
- Ollama (local, self-hosted — default)
- DeepSeek API (cheapest option)
- Gemini API
- Custom endpoints

**Email Automation:**
- Create Gmail drafts from CSV data
- Sector-specific templates
- Batch draft creation (up to 30/run)

**WordPress Automation:**
- Publish/draft posts via REST API
- Auto-tag and auto-categorise using AI
- Schedule posts from Google Sheets
- Folder-watcher: drop a markdown file → instant WordPress draft

## ARCHITECTURE

```
User writes → Google Docs / Logseq / plain .md file
       ↓
Auto-publisher picks up (cron / Apps Script trigger)
       ↓
DeepSeek / Ollama / Anthropic API enhances SEO, tags, category
       ↓
WordPress REST API receives post as draft
       ↓
You review in WP Admin → click Publish
```

## QUICK START

### 1. Set Environment Variables

```bash
export ANTHROPIC_API_KEY=sk-ant-xxxxx
export DEEPSEEK_API_KEY=sk-xxxxx
export GEMINI_API_KEY=xxxxx
export OLLAMA_URL=http://localhost:11434
export WP_API_KEY=your-wp-plugin-key
export WP_URL=https://yourdomain.com
```

### 2. Install Python Scripts

```bash
pip install requests tkinter
python scripts/wp_publisher_gui.py      # GUI desktop app
python scripts/auto_publisher.py        # CLI watcher
python scripts/wordpress_health_check.py # site audit
```

### 3. Google Apps Script Setup

1. Open your Google Sheet → Extensions → Apps Script
2. Paste contents of `scripts/sheet_publisher.gs`
3. Run `setKeys()` once to store API keys securely
4. Run `setupHourlyTrigger()` — automation is now live

### 4. Chrome Extension

1. Open `chrome://extensions` → Enable Developer Mode
2. Load Unpacked → select `browser_extension/` folder
3. Click extension → Settings → choose AI provider → paste key

## OPTION A — LOCAL AI (OLLAMA, FREE)

```bash
# Install Ollama from ollama.ai
curl -fsSL https://ollama.ai/install.sh | sh
ollama serve
ollama pull mistral
```

Set provider to Ollama in extension settings. No API costs, fully private.

## OPTION B — ANTHROPIC API

Get key at console.anthropic.com. Set `ANTHROPIC_API_KEY`. Select "Anthropic" as provider.

## OPTION C — DEEPSEEK (CHEAPEST)

Get key at platform.deepseek.com. $5 free credits on signup (~18,000 posts worth).
See `automation/01_DEEPSEEK_API_GUIDE.md` for full integration guide.

## REPOSITORY STRUCTURE

```
automation/          # Comprehensive guides (start here)
  01_DEEPSEEK_API_GUIDE.md
  02_CSV_GOOGLE_SHEETS_TUTORIAL.md
  03_TOOLS_COLLECTION.md
  04_FREE_AI_GUIDE.md
  05_WORDPRESS_HEALTH.md
scripts/             # Ready-to-run automation
  auto_publisher.py
  wp_publisher_gui.py
  folder_watcher.js
  sheet_publisher.gs
  job_hunter.py
  wordpress_category_tag_fix.py
  wordpress_health_check.py
.github/workflows/   # GitHub Actions
  publish_on_push.yml
browser_extension/   # Chrome extension source
tools_and_scripts/   # Legacy tools and skills
CELTA_Teaching_Materials/
Biography_and_Medical/
```

## ENVIRONMENT VARIABLES REFERENCE

| Variable | Purpose |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic claude-* models |
| `DEEPSEEK_API_KEY` | DeepSeek chat/coder/reasoner |
| `GEMINI_API_KEY` | Google Gemini |
| `OLLAMA_URL` | Local Ollama (default: http://localhost:11434) |
| `WP_URL` | Your WordPress site URL |
| `WP_API_KEY` | Plugin secret key (`X-Sourov-Key` header) |
| `WP_USER` | WordPress username |
| `WP_APP_PASSWORD` | WordPress application password |

## CHANGELOG

### v2.0.0
- Email automation module
- Ollama local AI integration
- Config-based API management (no hardcoding)
- CSV batch processing
- DeepSeek integration (cheapest AI option)
- Multi-AI support (Anthropic, DeepSeek, Gemini, Ollama)

### v1.0.0
- Multi-AI support (Anthropic, DeepSeek, Gemini)
- Web page summarisation
- Form auto-fill
- Context menus

---

Sourov Deb | MIT License | Updated 2026-06-09
