# Automation Scripts

All scripts are Python 3. All credentials come from `.env` (never hardcoded).

---

## Setup (once)

```bash
# 1. Copy the credentials template
cp .env.example .env
# Edit .env with your real values

# 2. Install Python dependencies
pip install python-jobspy   # for job search
# No other dependencies needed — everything else uses stdlib
```

---

## Scripts

### 1. Publish an Essay to WordPress

```bash
python 05_automation/wordpress/publish_to_wp.py 03_writing/drafts/your-essay.md
```

- Reads your markdown file
- Creates a **draft** on WordPress (not published yet)
- Prints the edit URL so you can review before publishing
- Use `--status publish` to go live immediately
- Use `--dry-run` to preview without uploading

**One-time WordPress setup:** Go to `sourovdeb.com/wp-admin` → Users → Profile → scroll to "Application Passwords" → create one → put it in `.env` as `WP_APP_PASSWORD`.

---

### 2. Search for Jobs

```bash
# Run all default search profiles (English teacher, content writer, hospitality, etc.)
python 05_automation/job_search/search_jobs.py --all-profiles

# Search a specific role
python 05_automation/job_search/search_jobs.py --role "formateur anglais" --location "Paris, France"

# Remote only
python 05_automation/job_search/search_jobs.py --role "content writer" --remote
```

Results save to `05_automation/job_search/results/jobs_YYYY-MM-DD.md`. Track applications in `job_tracker.md`.

---

### 3. Find Like-Minded Writers

```bash
# Search default topics (trauma, immigration, neurodiversity, teaching...)
python 05_automation/outreach/find_writers.py

# Search specific topics
python 05_automation/outreach/find_writers.py --topics "bipolar memoir" "expat France"

# Substack only
python 05_automation/outreach/find_writers.py --platform substack
```

Results save to `05_automation/outreach/results/writers_YYYY-MM-DD.md`.

---

## Daily Routine (10 minutes)

| Time | Task | Script |
|------|------|--------|
| Morning | Push yesterday's draft to WordPress | `publish_to_wp.py` |
| Weekly Monday | Run job search | `search_jobs.py --all-profiles` |
| Weekly Friday | Find 5 new writers, leave 2 comments | `find_writers.py` |
