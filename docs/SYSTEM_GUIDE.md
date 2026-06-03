# Automation System — Quick Start Guide

This guide is designed for low cognitive load. Follow one step at a time.

---

## Step 1: Set Your Credentials (Do Once)

```bash
cp scripts/.env.example scripts/.env
```

Open `scripts/.env` in any text editor. Fill in:
- `WP_API_URL` — your WordPress endpoint
- `WP_API_KEY` — your API key
- `WP_BASE_URL` — your site homepage URL

That’s all. The `.env` file is in `.gitignore` — it will never be committed.

---

## Step 2: Install Dependencies (Do Once)

```bash
# Python
make install-py

# Node.js (only if using folder_watcher.js)
make install-node
```

---

## Step 3: Choose Your Workflow

### Option A: GUI App (Easiest — recommended for daily use)
```bash
make publish
# A window opens. Write title, content, click Publish.
```

### Option B: Drop a file, it publishes automatically
```bash
make watch
# In another terminal, copy a .md file to ~/wordpress_queue/
# It publishes automatically and moves to ~/wordpress_queue/archive/
```

### Option C: Google Sheets (batch publishing)
1. Open your Google Sheet
2. Extensions > Apps Script
3. Paste the code from `scripts/google_apps_script/sheet_publisher.gs`
4. Set Script Properties (WP_API_URL, WP_API_KEY)
5. Run `publishFromSheet()` manually, or set an hourly trigger

### Option D: GitHub Actions (write → git commit → auto-publish)
1. Add `WP_API_URL` and `WP_API_KEY` as repository secrets
2. Create a file in `drafts/` e.g. `drafts/2026-06-15-my-post.md`
3. Push to `main` branch
4. GitHub Action fires automatically, publishes the draft

---

## Step 4: Run Health Check

```bash
make health
# Report saved to docs/health_report_YYYY-MM-DD.json
```

---

## Step 5: Daily Job Digest

```bash
make jobs
# Fetches ELT jobs from Indeed RSS and emails them to you
# Or prints to screen if EMAIL credentials not set
```

---

## Repository Layout

```
my_professional_documents/
├── scripts/                    # All automation code
│   ├── wp_publisher.py         # Tkinter GUI app
│   ├── auto_publisher.py       # Folder watcher / cron script
│   ├── wp_health_check.py      # WordPress health monitor
│   ├── job_hunter.py           # Job search + email digest
│   ├── folder_watcher.js       # Node.js real-time watcher
│   ├── google_apps_script/
│   │   └── sheet_publisher.gs  # Paste into Google Apps Script
│   ├── .env.example            # Copy to .env and fill in
│   └── .env                    # Your real credentials (gitignored)
├── drafts/                     # Your daily writing
│   ├── templates/
│   │   ├── ELT_TEMPLATE.md
│   │   └── CELTA_TEMPLATE.md
│   └── archive/                # Published posts (auto-moved here)
├── plugins/                    # WordPress PHP plugins
│   └── wp_health_monitor.php   # Adds /health endpoint
├── docs/                       # Guides and reports
│   ├── OPEN_SOURCE_TOOLS.md    # Curated tool catalogue
│   ├── WORDPRESS_HEALTH.md     # Health monitoring guide
│   ├── WELLBEING_RESOURCES.md  # Mental health resources
│   └── SYSTEM_GUIDE.md         # This file
├── .github/workflows/
│   └── publish_on_push.yml     # Auto-publish on git push
├── Makefile                    # make publish / watch / health / jobs
├── .gitignore                  # Keeps .env and archives out of git
└── [existing folders]          # Biography_and_Medical, CELTA, etc.
```

---

## Credential Safety Rules

1. **Never** paste real keys into any file tracked by git
2. Always use `scripts/.env` for secrets
3. For GitHub Actions: use **repository secrets** (Settings > Secrets)
4. For Google Apps Script: use **Script Properties** (not the code itself)
5. Run `git status` before committing — check nothing secret is staged
