# Automation & Publishing System

> **Your sustainable system for writing, job searching, and WordPress publishing.**
> Built for consistency, mental health first, no burnout.

---

## What's in This System

### 1. **Daily Writing** → `../blog_and_essays/`

- **Prompts**: 18+ daily writing prompts in `daily_prompts/DAILY_WRITING_PROMPTS.md`
- **Template**: Essay template with metadata in `templates/ESSAY_TEMPLATE.md`
- **Workflow**: Draft → Validate → Publish

**Daily time**: 30-60 minutes
**Output**: 500-word essay (5x/week = sustainable)

---

### 2. **Job Search Automation** → `job_search/`

**Files**:
- `INDEED_SEARCH_AUTOMATION.sh` - Daily Indeed searches
- Job tracking (export to CSV + markdown)
- Multiple search queries (customizable)

**How it works**:
```bash
chmod +x job_search/INDEED_SEARCH_AUTOMATION.sh
./job_search/INDEED_SEARCH_AUTOMATION.sh
```

**Output**: Daily job report (markdown file)

**Cron setup** (automatic daily search):
```bash
# Edit crontab
crontab -e

# Add this line (runs at 8 AM daily):
0 8 * * * /path/to/job_search/INDEED_SEARCH_AUTOMATION.sh
```

**Alternative**: LinkedIn API setup (in progress)

---

### 3. **WordPress Publishing** → `wordpress/`

**Important**: This keeps credentials 100% safe.

**Files**:
- `WP_PUBLISH_HELPER.py` - Validates and prepares essays for publishing

**How it works**:

```bash
# After writing your essay in blog_and_essays/drafts/
python3 automation/wordpress/WP_PUBLISH_HELPER.py blog_and_essays/drafts/2026-06-03_my-essay.md
```

**Output**:
- Validates metadata (title, category, tags)
- Counts words (warns if <450 or >550)
- Generates excerpt
- Shows WordPress publishing checklist
- ✓ NO FTP, NO DATABASE—all manual copy-paste

**Publishing steps**:
1. Run the helper script (above)
2. Go to `https://www.sourovdeb.com/wp-admin/post-new.php`
3. Copy-paste content from script output
4. Fill in metadata
5. Publish
6. Update Google Sheet

---

### 4. **Content Tracking** → Google Sheet

**Link**: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/

**Columns to track**:
- Date
- Prompt number/title
- Essay title
- Word count
- Status (draft/ready/published)
- WordPress URL
- Category
- Tags
- Notes

**Why Google Sheet?**
- Real-time, shareable, no database credentials needed
- Can collaborate (if desired)
- Easy to see patterns (productivity, consistency)
- No technical barrier

---

### 5. **Email Automation** → `email/`

(In development)

**Goal**: Auto-send job applications, follow-ups, networking emails

**Future tools**:
- Gmail API integration (safe token-based)
- Email templates
- Tracking (open rates, responses)

---

## Branch Workflow for Drafts

### Principle
Each draft gets its own branch. Clean history, clear intent.

### Workflow

```bash
# Create a branch for your essay
git checkout -b essay/2026-06-03-my-essay-title

# Write your essay
# File: blog_and_essays/drafts/2026-06-03-my-essay-title.md

# Validate with the helper
python3 automation/wordpress/WP_PUBLISH_HELPER.py blog_and_essays/drafts/2026-06-03-my-essay-title.md

# Stage and commit
git add blog_and_essays/
git commit -m "draft: essay title

- Prompt: #X (reference which daily prompt)
- Word count: 497
- Status: ready for review"

# Push to branch
git push -u origin essay/2026-06-03-my-essay-title
```

### Publishing

Once the essay is published to WordPress:

```bash
# Move from drafts to published
mv blog_and_essays/drafts/2026-06-03-my-essay-title.md \
   blog_and_essays/published/2026-06-03-my-essay-title.md

# Add WordPress URL to metadata
# Edit the file and add: wordpress_url: https://...

# Commit
git add blog_and_essays/
git commit -m "published: essay title

WordPress URL: https://www.sourovdeb.com/?p=123
Updated Google Sheet"

# Merge to main (optional)
git checkout main
git pull origin main
git merge essay/2026-06-03-my-essay-title
git push origin main
```

---

## Quick Start Checklist

### Week 1: Setup

- [ ] Read `daily_prompts/DAILY_WRITING_PROMPTS.md`
- [ ] Copy essay template: `templates/ESSAY_TEMPLATE.md`
- [ ] Test WordPress helper: `python3 automation/wordpress/WP_PUBLISH_HELPER.py`
- [ ] Set up job search cron (optional): `crontab -e`
- [ ] Share Google Sheet link with anyone who needs to see progress

### Week 2: First Essays

- [ ] Write essay #1 (pick any prompt)
- [ ] Validate with helper script
- [ ] Publish to WordPress
- [ ] Update Google Sheet
- [ ] Create branch + commit

### Ongoing

- [ ] Pick 1 prompt per day
- [ ] Write 500 words
- [ ] Validate + publish
- [ ] Update sheet
- [ ] Commit to branch
- [ ] (Optional) Merge to main weekly

---

## Mental Health First

This system is designed for consistency **without burnout**.

### If You're Struggling This Week
- Skip a day (no guilt)
- Reuse a prompt from last week
- Write 250 words instead of 500 (still counts)
- Take a full week off if needed

### Sustainable = 4-5 essays/week

Not 7/week. Not 14/week. **4-5**.

### Why This Works
1. Prompts eliminate decision paralysis
2. Template keeps you focused
3. Automation handles the boring parts
4. Your job is just writing (your superpower)
5. Branch workflow keeps things organized
6. Google Sheet shows your progress

---

## Tools Used (All Free & Open Source)

| Tool | Purpose | Install |
|------|---------|---------|
| Git | Version control | Pre-installed |
| Python 3 | WordPress helper | `sudo apt install python3` |
| Bash | Job search automation | Pre-installed |
| curl | API calls (optional) | `sudo apt install curl` |
| jq | JSON parsing (optional) | `sudo apt install jq` |

---

## Troubleshooting

### "Python script won't run"
```bash
chmod +x automation/wordpress/WP_PUBLISH_HELPER.py
python3 automation/wordpress/WP_PUBLISH_HELPER.py [file]
```

### "Job search script does nothing"
Indeed has robots.txt restrictions. The script generates links for you to check manually:
```
https://www.indeed.com/jobs?q=remote+writing&l=remote
```
Click the link to see live results.

### "I forgot my WordPress password"
1. Go to `https://www.sourovdeb.com/wp-login.php`
2. Click "Lost your password?"
3. Check email (check spam folder)

### "Can't remember which prompt I did"
Check `blog_and_essays/drafts/` and `blog_and_essays/published/`
All files are named by date.

---

## Next Steps

1. **Today**: Read `DAILY_WRITING_PROMPTS.md`
2. **Tomorrow**: Write your first essay (any prompt)
3. **This week**: Publish 3 essays
4. **This month**: 15-20 essays (your body of work)

---

## Need Help?

1. **Writing stuck?** → Pick a different prompt
2. **WordPress issue?** → Check WordPress.com support docs
3. **Git issue?** → Check GitHub docs or ask
4. **Automation issue?** → Check script comments or bash docs

---

## Your Goal

> **By the end of 2026, you'll have:**
> - 100+ published essays
> - Clear, credible writing voice
> - Proof of consistency (job interviews love this)
> - A platform for your ideas
> - Your story, in your words, heard

**You're not starting from zero. You're building from your foundation.**

---

Last updated: 2026-06-03
