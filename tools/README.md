# Automation Tools & Scripts

**Goal:** Eliminate repetitive work so you can focus on writing.

All scripts are designed to be:
- **Health-aware:** Run automatically (no human input)
- **Token-efficient:** Reusable Python scripts
- **Source-verified:** Use official APIs where possible
- **Logged:** Keep records for tracking

---

## Quick Start

### 1. Install Dependencies
```bash
pip install requests beautifulsoup4 gspread google-auth-httplib2 google-auth-oauthlib python-dotenv
```

### 2. Set Up Google API Access
```bash
# Get credentials from Google Cloud Console
# https://console.cloud.google.com/apis/credentials

# Save service account JSON to:
~/.config/google_sheets_config.json

# Or set environment variable:
export GOOGLE_APPLICATION_CREDENTIALS=~/.config/google_sheets_config.json
```

### 3. Run Your First Script
```bash
# Download job opportunities
python3 automation/job_hunter.py --roles "English Teacher" --locations "Paris" --output TRACKING/job_opportunities.csv

# Sync with Google Sheets
python3 google_sheets_sync/sheets_sync.py --sync-all
```

---

## Scripts Overview

### 1. Job Hunter (`automation/job_hunter.py`)

**Purpose:** Auto-scrape job boards weekly  
**Output:** `TRACKING/job_opportunities.csv`

```bash
# Basic usage
python3 automation/job_hunter.py

# Custom search
python3 automation/job_hunter.py \
  --roles "CELTA Trainer,English Teacher" \
  --locations "Paris,Lyon,Remote" \
  --output TRACKING/job_opportunities.csv
```

**What it does:**
- Scrapes Indeed France, Welcome to the Jungle, LinkedIn
- Deduplicates results
- Preserves your "applied" status
- Saves to CSV (Google Sheets syncs automatically)

**Automation:**
```bash
# Add to crontab (runs weekly Monday 8 AM)
0 8 * * 1 cd ~/my_professional_documents && python3 tools/automation/job_hunter.py
```

**Output columns:**
- `title` — Job title
- `company` — Company name
- `location` — Location
- `url` — Job link
- `source` — Where it came from
- `posted_date` — When posted
- `salary` — If available
- `applied` — "Yes" / "No" (you update this)
- `notes` — Your notes

---

### 2. Google Sheets Sync (`google_sheets_sync/sheets_sync.py`)

**Purpose:** Keep local CSVs synced with Google Sheets  
**Direction:** Bidirectional (↔)

```bash
# Sync everything
python3 google_sheets_sync/sheets_sync.py --sync-all

# Sync one tab
python3 google_sheets_sync/sheets_sync.py \
  --tab "Essay Ideas" \
  --csv "TRACKING/essay_ideas.csv" \
  --download

# Upload local CSV to Google Sheets
python3 google_sheets_sync/sheets_sync.py \
  --tab "Job Opportunities" \
  --csv "TRACKING/job_opportunities.csv" \
  --upload
```

**What it does:**
- Downloads Google Sheets tabs as CSV
- Uploads local CSVs to Google Sheets
- Keeps both in sync
- Preserves formatting

**Automation:**
```bash
# Add to crontab (runs weekly Monday 9 AM)
0 9 * * 1 cd ~/my_professional_documents && python3 tools/google_sheets_sync/sheets_sync.py --sync-all
```

**Configuration:** Edit `google_sheets_sync/sync_config.json` to control which sheets sync

---

### 3. Email Drafter (Coming Soon)

**Purpose:** Batch-create personalized emails from CSV  
**Output:** Gmail drafts ready to send

```bash
# Draft emails to companies
python3 automation/email_drafter.py \
  --input TRACKING/job_opportunities.csv \
  --sector-template "Teaching" \
  --gmail-api
```

---

### 4. Writer Discovery (Coming Soon)

**Purpose:** Find writers, editors, collaborators  
**Output:** `TRACKING/contacts_discovered.csv`

```bash
# Find writers in your niche
python3 automation/writer_discovery.py \
  --topics "Bipolar,Mental Health,Writing" \
  --platforms "Medium,Substack,Twitter"
```

---

## File Structure

```
tools/
├── README.md (this file)
├── automation/
│   ├── job_hunter.py          # Scrape job boards
│   ├── email_drafter.py        # Batch email creation
│   ├── writer_discovery.py     # Find collaborators
│   └── utils.py                # Shared utilities
├── google_sheets_sync/
│   ├── sheets_sync.py          # Google Sheets sync
│   └── sync_config.json        # Configuration
├── wordpress_deploy/
│   ├── wp_deploy.py            # Deploy to WordPress
│   ├── ftp_config.json         # FTP details
│   └── deploy.php              # Server gateway
└── scripts/
    ├── run_all_automation.sh    # Run all scripts
    ├── setup.sh                 # First-time setup
    └── cron_setup.sh            # Set up cron jobs
```

---

## Environment Variables

Create `.env` file in repo root:

```bash
# Google API
GOOGLE_APPLICATION_CREDENTIALS=~/.config/google_sheets_config.json
GOOGLE_SHEET_ID=1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE

# Gmail API (for email drafter)
GMAIL_API_KEY=your_key_here
GMAIL_SENDER=your_email@gmail.com

# WordPress
WORDPRESS_HOST=sourovdeb.com
WORDPRESS_USER=u839078121.sourov
WORDPRESS_FTP_PASSWORD=your_ftp_pass_here

# Job search
JOB_ROLES="English Teacher,CELTA Trainer"
JOB_LOCATIONS="Paris,Lyon,Remote"
JOB_SALARY_MIN=1500

# Writer discovery
WRITER_TOPICS="Bipolar,Mental Health,Writing"
WRITER_MIN_FOLLOWERS=100
```

**⚠️ NEVER commit `.env` file. Add to `.gitignore`**

---

## Running Scripts Automatically

### Option 1: Cron Jobs (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add these lines:
0 8 * * 1 cd ~/my_professional_documents && python3 tools/automation/job_hunter.py >> logs/job_hunter.log 2>&1
0 9 * * 1 cd ~/my_professional_documents && python3 tools/google_sheets_sync/sheets_sync.py --sync-all >> logs/sync.log 2>&1
0 10 * * 4 cd ~/my_professional_documents && python3 tools/automation/writer_discovery.py >> logs/writer_discovery.log 2>&1
```

### Option 2: GitHub Actions (Automated on cloud)

Create `.github/workflows/automation.yml`:

```yaml
name: Weekly Automation

on:
  schedule:
    - cron: '0 8 * * 1'  # Monday 8 AM

jobs:
  job-hunter:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r tools/requirements.txt
      - name: Run job hunter
        run: python3 tools/automation/job_hunter.py
      - name: Commit results
        run: |
          git config user.name "Bot"
          git config user.email "bot@example.com"
          git add TRACKING/
          git commit -m "Automated: Job opportunities update" || true
          git push
```

### Option 3: Manual Run Script

```bash
# Run all automation
bash tools/scripts/run_all_automation.sh
```

---

## Logging & Monitoring

All scripts log to `logs/`:

```
logs/
├── job_hunter.log
├── sheets_sync.log
├── email_drafter.log
└── writer_discovery.log
```

View logs:
```bash
tail -f logs/job_hunter.log
```

---

## Health-Aware Automation

**Key principle:** Automation runs when YOU don't have to.

**High Energy Days:**
- Focus on writing essays
- Automation handles job searching
- You review results when ready

**Low Energy Days:**
- Automation publishes pre-written content
- Automation sends emails
- Automation finds opportunities
- You just rest

**Zero-Input Automation:**
- Runs on schedule (cron/GitHub Actions)
- No human decisions needed
- Results added to tracking sheets
- You review at your own pace

---

## Troubleshooting

### "ImportError: No module named 'requests'"
```bash
pip install requests beautifulsoup4
```

### "Google authentication failed"
- Check credentials file: `~/.config/google_sheets_config.json`
- Verify sheet permissions shared with service account email
- Test with: `python3 -c "import gspread; print('OK')"`

### "CSV file not found"
- Check directory exists: `mkdir -p TRACKING/`
- Run scripts from repo root: `cd ~/my_professional_documents`

### Script runs but produces no output
- Check logs: `tail logs/job_hunter.log`
- Verify internet connection
- Check if job boards blocked by firewall

---

## Contributing

Found a bug? Want to improve a script?

1. Create feature branch: `git checkout -b tools/feature-name`
2. Update script and test locally
3. Commit: `git commit -m "Tools: [description]"`
4. Push: `git push origin tools/feature-name`
5. Create pull request

---

## Next Steps

1. **Install dependencies:** Run `pip install -r requirements.txt`
2. **Set up Google API:** Get service account credentials
3. **Test first script:** Run `job_hunter.py`
4. **Set up automation:** Add cron job or GitHub Actions
5. **Monitor results:** Check logs and CSV files weekly

---

**Remember:** Automation is there to support your health, not replace it. Use it as a tool, not a master.

Last updated: 2026-06-02
