# Job Automation System

Automated job searching, application tracking, and networking for Indeed, LinkedIn, and other platforms.

---

## 🎯 Your Goal

Stop manually checking job boards. Instead:
- ✅ Scrape Indeed/LinkedIn for roles matching your criteria
- ✅ Auto-send networking emails to hiring managers
- ✅ Track applications and follow-ups
- ✅ Collect contact information for partnerships
- ✅ Monitor salary trends

---

## 🛠️ Available Scripts

### 1. `indeed_scraper.py` - Auto Job Monitor
**What it does**: Monitors Indeed for new jobs matching your criteria

```bash
python indeed_scraper.py \
  --job-title "English Teacher" \
  --location "remote" \
  --min-salary 35000 \
  --output jobs.csv
```

**Requirements**:
- `requests`, `beautifulsoup4`, `pandas`
- Install: `pip install -r requirements.txt`

**Output**: CSV with job title, company, salary, link, posting date

**Run frequency**: Daily via cron (see setup below)

---

### 2. `linkedin_email_generator.py` - Networking Automation
**What it does**: Generates personalized emails to hiring managers/recruiters

```bash
python linkedin_email_generator.py \
  --csv indeed_jobs.csv \
  --template networking_template.txt \
  --output outreach_emails.txt
```

**Features**:
- Personalization (job title, company name, your name)
- Multiple templates (cold email, referral follow-up, skill alignment)
- Duplicate detection (don't email same person twice)

---

### 3. `gmail_automation.py` - Auto-Send Emails
**What it does**: Safely sends personalized emails from your Gmail

⚠️ **Setup required**:
1. Enable Gmail API (Google Cloud Console)
2. Create OAuth2 credentials
3. Store `credentials.json` in `.env.local` (git-ignored)

```bash
python gmail_automation.py \
  --mode draft \
  --emails outreach_emails.txt
```

**Important**: Runs in `--draft` mode by default (saves drafts, doesn't send). Change to `--mode send` only when confident.

---

### 4. `job_tracker.py` - Application Tracking
**What it does**: Maintains CSV of all applications, follow-ups, and responses

```bash
python job_tracker.py \
  --add \
  --company "Company X" \
  --position "Senior Teacher" \
  --applied-date "2026-06-03" \
  --status "pending"
```

**Tracks**:
- Application date
- Follow-up dates
- Response status (no response, rejected, interview, offer)
- Interview notes
- Salary offer

---

### 5. `daily_job_digest.py` - Email Digest
**What it does**: Sends you a daily email summary of new jobs

Run daily: `0 9 * * * python daily_job_digest.py`

Example output:
```
Found 12 new jobs today
- Job 1: Company A | Remote | $40k-50k
- Job 2: Company B | Part-time | Freelance

Top match: Company C (92% match score)
```

---

## 📋 Setup Instructions

### Prerequisites
```bash
# Clone repo (if not already)
cd my_professional_documents
git checkout claude/nifty-clarke-06pXm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r Job_Automation/requirements.txt
```

### 1. Configure Your Job Criteria
**File**: `Job_Automation/config.json`
```json
{
  "job_titles": ["English Teacher", "Content Writer", "Technical Writer"],
  "locations": ["remote", "USA"],
  "min_salary": 35000,
  "max_salary": 80000,
  "exclude_keywords": ["part-time", "internship"],
  "include_keywords": ["remote", "flexible", "async"]
}
```

### 2. Set Up Gmail API
```bash
# 1. Go to Google Cloud Console
# 2. Create new project
# 3. Enable Gmail API
# 4. Create OAuth2 credentials (Desktop application)
# 5. Download credentials.json
# 6. Run auth setup:

python Job_Automation/setup_gmail_auth.py
```

This creates `token.pickle` for future authentication.

### 3. Create Email Templates
**File**: `Job_Automation/templates/networking_cold_email.txt`
```
Subject: [Job Title] opening at [Company Name]

Hi [Hiring Manager Name],

I came across [Company Name]'s opening for [Job Title] and was impressed by [specific company detail].

My background in [relevant skill] and experience with [tool/technology] aligns well with your needs.

I'd love to chat about how I can contribute to [Company Name]'s [goal/project].

Best,
Sourov
[Your Phone]
[Your LinkedIn]
```

### 4. Schedule Automation (Cron)
**File**: `crontab -e`
```bash
# Run job scraper daily at 7am
0 7 * * * cd ~/my_professional_documents && python Job_Automation/indeed_scraper.py

# Send daily digest at 9am
0 9 * * * cd ~/my_professional_documents && python Job_Automation/daily_job_digest.py

# Send emails Tuesday & Thursday at 10am
0 10 * * 2,4 cd ~/my_professional_documents && python Job_Automation/gmail_automation.py --mode draft
```

---

## 📊 Workflow

```
1. Scraper runs → finds new jobs → saves to jobs.csv
2. You review CSV (optional filter step)
3. Email generator creates personalized emails
4. Gmail automation sends/drafts emails
5. Job tracker logs all applications
6. You follow up after 1 week if no response
```

---

## ⚠️ Safety & Ethics

**Do**:
- ✅ Personalize every email (include hiring manager name, company details)
- ✅ Research company before applying
- ✅ Use `--draft` mode first, review before sending
- ✅ Respect "no contact" requests
- ✅ Space out emails (max 20/day)

**Don't**:
- ❌ Send to same person twice
- ❌ Use fake references or skills
- ❌ Apply to jobs you're not qualified for
- ❌ Use automation to spam

---

## 🔐 Credentials

**Never commit**:
- `credentials.json` (Gmail API)
- `token.pickle` (Gmail token)
- Email addresses
- API keys

**Store in**:
- `.env.local` (git-ignored)
- Environment variables
- Or OS credential manager

---

## 📊 Tracking & Insights

After 2 weeks, analyze:
- Response rate by job title
- Best performing email templates
- Time to response
- Salary ranges by location
- Companies actively hiring

Use this data to refine your approach.

---

## 🚀 Quick Start

```bash
# 1. Configure
cp Job_Automation/config.template.json Job_Automation/config.json
# Edit config.json with your criteria

# 2. Set up Gmail
python Job_Automation/setup_gmail_auth.py

# 3. Test scraper
python Job_Automation/indeed_scraper.py --test

# 4. Test email generator
python Job_Automation/linkedin_email_generator.py \
  --csv jobs.csv \
  --mode test

# 5. Schedule automation
# Edit crontab with commands above
```

---

## 🆘 Troubleshooting

**Script fails with "Connection error"**
- Check internet connection
- Indeed/LinkedIn may be rate-limiting; retry in 1 hour
- Check firewall/proxy settings

**Gmail API not working**
- Re-run `setup_gmail_auth.py`
- Delete `token.pickle` and re-authenticate
- Check that Gmail API is enabled in Google Cloud Console

**Too many emails being sent**
- Reduce frequency in crontab
- Add more `exclude_keywords` to config
- Manually review before sending

---

## 📈 Next Steps

1. Set up scripts and test locally
2. Refine config.json with your real criteria
3. Schedule automation
4. Monitor first week for any issues
5. Adjust templates based on response rates

---

**Goal**: Spend 30 minutes setting this up once, then let it run. You focus on writing and health; automation handles job searching.
