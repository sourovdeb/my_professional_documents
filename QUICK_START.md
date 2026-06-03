# Quick Start: Writing, Automation, and Publishing System

**Get set up in 5 minutes. Then focus on writing.**

---

## What You Now Have

A complete system for:
- 📝 Writing 500-word essays consistently
- 🤖 Automating job search and email outreach
- 📊 Organizing research from official sources
- 💪 Health-aware productivity tracking
- 🌐 Publishing to your WordPress blog
- 📂 Professional repository organization

---

## Step 1: First-Time Setup (5 min)

### 1A. Create .env file

```bash
cd automation_scripts/
cat > .env << 'EOF'
DEPLOY_URL=https://www.sourovdeb.com/deploy.php
DEPLOY_KEY=0767044896thevenet_
EOF
```

**Never commit this file.** It's in `.gitignore` automatically.

### 1B. Install Python dependencies

```bash
pip install python-dotenv requests beautifulsoup4 pandas jinja2
```

### 1C. Create your first branch

```bash
git checkout -b essay/2026-06-03_first-essay
```

---

## Step 2: Write Your First Essay (45 min)

### 2A. Start with the template

```bash
cd blog_drafts/2026_06_essays/
cp ../ESSAY_TEMPLATE.md my_first_essay.md
```

### 2B. Edit the essay

Open `my_first_essay.md` in your editor and:
1. Replace `[Your Title Here]` with a real title
2. Write your 500-word essay following the template structure
3. Add sources from `content_research/sources_database.md`
4. Fill in metadata (category, tags, status)

### 2C. Commit your draft

```bash
git add blog_drafts/2026_06_essays/my_first_essay.md
git commit -m "Essay: [Title] - first draft"
git push -u origin essay/2026-06-03_first-essay
```

---

## Step 3: Edit and Prepare for WordPress (20 min)

### 3A. Save as WordPress draft

```bash
cd automation_scripts/
python3 wordpress_uploader.py \
  --file ../blog_drafts/2026_06_essays/my_first_essay.md \
  --status draft \
  --save-only
```

Output goes to: `wordpress_ready/staging/`

### 3B. Review locally

- Open the JSON file
- Check the HTML conversion
- Verify all metadata is correct

### 3C. Test on WordPress (dry-run)

```bash
python3 wordpress_uploader.py \
  --file ../wordpress_ready/staging/20260603_my_first_essay.json \
  --dry-run
```

---

## Step 4: Publish to WordPress (5 min)

### 4A. Upload to WordPress

```bash
python3 wordpress_uploader.py \
  --file ../wordpress_ready/staging/20260603_my_first_essay.json \
  --status draft
```

### 4B. Review on WordPress admin

1. Go to https://www.sourovdeb.com/wp-admin
2. Check Drafts section
3. Review the preview
4. Test on mobile

### 4C. Publish!

```bash
python3 wordpress_uploader.py \
  --file ../wordpress_ready/staging/20260603_my_first_essay.json \
  --status publish
```

### 4D. Move to published folder

```bash
mv wordpress_ready/staging/20260603_my_first_essay.json wordpress_ready/published/
```

---

## Step 5: Track and Plan (10 min)

### 5A. Update energy tracker

```bash
# Open and fill in:
health_and_productivity/energy_tracker.md
```

Record:
- Today's energy level (1-10)
- Mood
- How many hours you spent writing
- Wins (even small ones!)

### 5B. Update ideas inbox

```bash
# Open and add new ideas you thought of:
content_research/ideas_inbox.md
```

Mark status: Idea → Research → Drafting → Published

### 5C. Update tracking spreadsheet

Add to Google Sheets:
https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/

| Date | Title | Category | Status |
|------|-------|----------|--------|
| 2026-06-03 | First Essay | Mental Health | Published |

### 5D. Merge to main branch

When ready (or after publishing):

```bash
git checkout main
git pull origin main
git merge essay/2026-06-03_first-essay
git push origin main
```

---

## Next: Automate Job Searching (Optional)

### Search Indeed

```bash
cd job_automation/
python3 indeed_scraper.py --search "English Teacher" --location "France" --limit 25
```

This creates a CSV with jobs. Edit it to track:
- Applied status
- Follow-up dates
- Personalized notes

### Generate Email Outreach

```bash
# For one company:
python3 email_outreach_generator.py \
  --type job_inquiry \
  --company "XYZ Company" \
  --contact-name "John" \
  --background "CELTA certified"

# For many companies (batch):
python3 email_outreach_generator.py --create-template
# Edit the CSV, then:
python3 email_outreach_generator.py --batch companies.csv
```

All emails saved to `email_drafts/` for your 24h review before sending.

---

## Daily Routine

### Morning (5 min)

1. Check `health_and_productivity/energy_tracker.md`
2. Rate your energy (1-10)
3. Pick task based on energy level (use `mood_based_tasks.md`)

### Writing Time (45 min)

Follow the template, write 500 words, save

### Editing (15 min)

Fix typos, check links, read aloud

### Commit (2 min)

```bash
git add blog_drafts/
git commit -m "Essay: [Title] - [status]"
git push -u origin essay/YYYY-MM-DD_topic
```

### Optional: Publish (10 min)

Follow Step 3-4 if ready

### Evening (5 min)

Update energy tracker with today's wins

---

## Weekly Routine

### Every Sunday (30 min)

1. Review `health_and_productivity/energy_tracker.md`
2. Answer weekly review questions
3. Plan next week's essay topics
4. Update Google Sheets tracking
5. Commit weekly progress

---

## Monthly Goals

- [ ] Write 4 essays (one per week)
- [ ] Publish 3-4 essays to WordPress
- [ ] Apply to 10-15 jobs (or outreach to collaborators)
- [ ] Research 5-10 new topics
- [ ] Update contacts database
- [ ] Review energy patterns

---

## Important Reminders

✅ **DO:**
- Write daily, even if only 100 words
- Track your energy, not just your output
- Use templates when depleted
- Review everything 24h before publishing
- Celebrate small wins

❌ **DON'T:**
- Push yourself during depressive episodes
- Send emails/apply for jobs while manic (wait 24h)
- Feel guilty about missed days
- Compare your progress to others
- Skip medication or medical appointments

---

## Troubleshooting

**"I don't know what to write about"**
→ Check `content_research/ideas_inbox.md`. Pick an idea. Follow the template.

**"Energy is too low to write"**
→ Check `health_and_productivity/mood_based_tasks.md`. Do a lower-energy task.

**"WordPress upload failed"**
→ Check `.env` has your DEPLOY_KEY. Try `--dry-run` to see what's happening.

**"I missed a week of writing"**
→ That's okay. Write today instead. Update tracker. Keep going.

**"I'm in a manic/depressive episode"**
→ Contact your psychiatrist. Pause this system. Focus on health first.

---

## You're Ready!

This system is built around:
- **Your health** (bipolar, depression = real considerations)
- **Your voice** (active, human, authentic)
- **Your automation** (let scripts handle repetition)
- **Your consistency** (daily writing > perfection)

**Next step: Write your first essay. You've got this.**

---

**Questions? Check the README files in each directory. They have everything.**

**Branch: `essay/2026-06-03_your-topic`**  
**Write → Commit → Push → Publish**
