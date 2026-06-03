# Job Automation & Email Outreach

**Automated job searching, company research, and email generation.**

---

## What's Here

- **indeed_scraper.py** — Find jobs matching your profile on Indeed France
- **email_outreach_generator.py** — Create personalized emails to companies, collaborators, and potential partners
- **contacts_db.json** — Your contact database (people + companies to reach out to)

---

## Quick Start

### 1. Search Indeed for Jobs

```bash
python3 indeed_scraper.py --search "English Teacher" --location "France" --limit 25
```

Output: `jobs_tracked_20260603_120000.csv`

Edit the CSV:
- Add your application status: `new` → `applied` → `interviewed` → `rejected` → `hired`
- Add notes for follow-up

### 2. Generate Outreach Emails

Create a batch of personalized emails:

```bash
# Create template
python3 email_outreach_generator.py --create-template

# Generates: email_batch_template.csv

# Edit the CSV with company data, then:
python3 email_outreach_generator.py --batch email_batch_template.csv
```

Output: Email drafts in `email_drafts/` folder

**⚠️ IMPORTANT:** Review every email for 24 hours before sending. Don't send manic emails.

### 3. Single Email (Quick)

```bash
python3 email_outreach_generator.py \
  --type job_inquiry \
  --company "France Langue" \
  --contact-name "Marie" \
  --background "CELTA certified teacher" \
  --specialization "Business English"
```

---

## Email Types Available

1. **job_inquiry** — Applying for a teaching position
2. **collaboration_partnership** — Partner with someone on a project
3. **writing_partnership** — Collaborate on essays/articles
4. **workshop_proposal** — Pitch a workshop to an organization
5. **freelance_pitch** — Offer freelance services

---

## Workflow

```
1. Search Indeed (indeed_scraper.py)
   ↓
2. Review results in CSV
   ↓
3. Generate outreach email (email_outreach_generator.py)
   ↓
4. Save draft for 24h review (don't send immediately!)
   ↓
5. Send from Gmail (keep copy in "Outreach" folder for tracking)
   ↓
6. Update contacts_db.json with follow-up date
   ↓
7. Track status in job CSV
```

---

## Environment Setup

No API keys needed! These tools use:
- **Indeed**: Website scraping (legal, public data)
- **Email**: Templates only (you send via Gmail)

Install dependencies:
```bash
pip install requests beautifulsoup4 pandas
```

---

## Your Contacts Database

Format: `contacts_db.json`

```json
{
  "companies": [
    {
      "name": "France Langue",
      "contact": "Marie Dubois",
      "email": "marie@francelangue.fr",
      "industry": "Language Teaching",
      "status": "applied",
      "applied_date": "2026-06-03",
      "follow_up_date": "2026-06-10",
      "notes": "High interest, waiting for response"
    }
  ],
  "collaborators": [
    {
      "name": "Alex Chen",
      "email": "alex@medium.com",
      "focus": "Mental health writing",
      "status": "pending",
      "last_contact": "2026-06-01",
      "notes": "Potential writing partnership"
    }
  ]
}
```

---

## Tips & Best Practices

### For Job Searching

- **Search 1x per week**, not daily (avoid obsession)
- **Apply to 5-10 jobs per week max** (quality over quantity)
- **Track everything in the CSV** (you'll forget without it)
- **Follow up after 2 weeks** (only if you didn't get response)
- **Don't apply in manic state** (wait 24h, re-read before sending)

### For Email Outreach

- **Use templates** (saves energy, prevents repetition)
- **Personalize the company/contact name** (not "Dear Sir/Madam")
- **Keep to 3 paragraphs max** (people don't read long emails)
- **One clear call to action** (15-min call, feedback on proposal, etc.)
- **Sign with your name + phone + email** (easy for them to reply)
- **Save as draft in Gmail** (review 24h before sending)
- **Track in contacts_db.json** (follow up appropriately)

### Health Considerations

- **Low energy day?** Skip job searching, organize existing CVs instead
- **Manic state?** Don't apply to jobs. Do something creative instead.
- **Depressive state?** Use last month's job search, just edit and resend
- **Rejected?** Wait 48h before analyzing why. It's data, not doom.

---

## Scripts You'll Run Frequently

```bash
# Search every Monday
python3 indeed_scraper.py --search "English Teacher" --location "France" --limit 25

# Generate one email (when you find a promising company)
python3 email_outreach_generator.py --type job_inquiry --company "XYZ" ...

# Batch generate (once a month from CSV)
python3 email_outreach_generator.py --batch monthly_targets.csv
```

---

## Troubleshooting

**"No jobs found"**
- Try different search terms
- Check location spelling
- Indeed might have changed HTML (update scraper)

**"Email generation failed: Missing variable"**
- Check all required fields are in your CSV
- Run with --type to see what variables are needed

**"Can't install requests"**
- Use: `pip3 install requests` (Python 3)
- On Mac: `pip install --upgrade pip` first

---

## Next: Connect to Your Writing

When you get a job interview or collaboration offer:
- Write an essay about it (if comfortable)
- Track in energy_tracker.md
- Share lessons learned in blog_drafts/

Example: "How I Got Hired as a Remote English Teacher" after success

---

**Remember: Consistency beats urgency. One good application beats 20 rushed ones.**
