# Quick Start Guide - Your Writing & Automation System

Everything you need to start today. 15-minute setup, lifetime of impact.

---

## 🎯 What This System Does

```
You write essays on your own schedule
     ↓
Automation finds jobs + sends outreach
     ↓
You track applications and follow-ups
     ↓
You publish to WordPress
     ↓
You build exposure and get job offers
     ↓
All while managing bipolar + depression with consistency
```

---

## ⏱️ 15-Minute Setup

### Step 1: Read These Files (5 min)
```
1. WRITING_SYSTEM.md       ← Overview of everything
2. Essays_and_Blogs/README.md  ← Your daily writing practice
3. Job_Automation/README.md    ← Job hunting automation
```

### Step 2: Create Your First Essay (10 min)
```bash
# Create essay from template
cp Essays_and_Blogs/TEMPLATE.md Essays_and_Blogs/2026/06/2026-06-03-first-essay.md

# Edit it with your first 500-word essay
# Topic suggestions: "Why I started writing", "Managing bipolar while working remote", etc.

# Commit and push
git add Essays_and_Blogs/
git commit -m "Essay: [Your topic]"
git push -u origin claude/nifty-clarke-06pXm
```

---

## 🗂️ Your Repository Structure

```
my_professional_documents/
│
├── Essays_and_Blogs/
│   ├── TEMPLATE.md                 ← Copy this for every essay
│   ├── 2026/06/
│   │   └── 2026-06-03-topic.md    ← Your first essay
│   └── README.md                   ← Writing guide
│
├── Job_Automation/
│   ├── job_applications_tracker.csv ← Track all applications here
│   ├── README.md                    ← Job automation guide
│   └── [scripts for automation]
│
├── Health_and_Wellbeing/
│   ├── Daily_Checklist.md          ← Copy, update daily (5 min)
│   └── README.md                   ← Mental health system
│
├── WordPress_Drafts/
│   ├── Ready_for_Publishing/       ← Ready to publish
│   └── README.md                   ← Publishing guide
│
├── Tools_and_Ideas/
│   ├── OPEN_SOURCE_TOOLS.md        ← Tools to use
│   ├── AUTOMATION_IDEAS.md         ← Projects to build
│   └── README.md                   ← Ideas system
│
├── Contacts_and_Partnerships/
│   ├── Network_Master.csv          ← Your contacts
│   └── README.md                   ← Networking guide
│
├── Tools_and_Scripts/
│   ├── daily_prompt_generator.py   ← Gets you writing
│   ├── job_tracker.py              ← Tracks applications
│   └── [other automation scripts]
│
└── WRITING_SYSTEM.md               ← Master overview
```

---

## 🚀 Your Daily Routine (Takes ~30 min)

### Morning (7 min)
```
1. Update Health_and_Wellbeing/Daily_Checklist.md
   - Took meds? ✓
   - Slept OK? ✓
   - Energy level? 6/10
   
2. Check daily writing prompt
   python Tools_and_Scripts/daily_prompt_generator.py
```

### Writing Time (30 min)
```
1. Open Essays_and_Blogs/2026/06/TEMPLATE.md
2. Copy to today's essay file
3. Write 500 words (active voice, personal, honest)
4. Save and commit
```

### Evening (5 min)
```
1. Update Daily_Checklist.md with evening reflection
2. Note any mood/energy changes
3. Plan tomorrow
```

---

## 📝 Essay Workflow (One-Time Setup)

### For Your First Essay
```bash
# 1. Create from template
cp Essays_and_Blogs/TEMPLATE.md Essays_and_Blogs/2026/06/2026-06-03-my-first-essay.md

# 2. Edit with your essay content
vim Essays_and_Blogs/2026/06/2026-06-03-my-first-essay.md

# 3. Fill in metadata (title, date, category, tags)
# Example:
# title: "Why I Started Writing"
# category: "Personal Philosophy"
# tags: ["mental-health", "writing", "personal"]

# 4. Write 500 words

# 5. Commit
git add Essays_and_Blogs/2026/06/2026-06-03-my-first-essay.md
git commit -m "Essay: Why I Started Writing"
git push -u origin claude/nifty-clarke-06pXm

# 6. Update Google Drive sheet
# https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/edit

# 7. When ready to publish: Copy to WordPress_Drafts/Ready_for_Publishing/
cp Essays_and_Blogs/2026/06/2026-06-03-my-first-essay.md \
   WordPress_Drafts/Ready_for_Publishing/2026-06-03-my-first-essay.md

# 8. Publish to WordPress (manual for now)
# Log in to sourovdeb.com/wp-admin/ and create post manually
```

---

## 💼 Job Automation Workflow

### Track Applications
```bash
# Add a new application
python Tools_and_Scripts/job_tracker.py add \
  "Company Name" \
  "Position Title" \
  "Remote" \
  "50000-65000"

# Update status after interview
python Tools_and_Scripts/job_tracker.py update "Company Name" --status "Interview scheduled"

# See all applications
python Tools_and_Scripts/job_tracker.py list

# See follow-ups due
python Tools_and_Scripts/job_tracker.py follow-ups

# See statistics
python Tools_and_Scripts/job_tracker.py stats
```

---

## 💊 Health Tracking (Daily, 5 min)

### Daily Checklist Template
**File**: `Health_and_Wellbeing/Daily_Checklist.md`

Copy and use daily (takes 2 minutes):
```markdown
Date: 2026-06-03

## Morning
- [ ] Took medications
- [ ] Slept 7-9 hours (actual: 8)
- [ ] Energy: 6/10
- [ ] Mood: Stable, slight sadness
- [ ] Anxiety: 3/10

## Throughout Day
- [ ] Wrote 500 words (yes)
- [ ] Moved body (20 min walk)
- [ ] Ate 3 meals
- [ ] Social connection (texted friend)
- [ ] No substance use

## Evening
- [ ] Wind down ritual (30 min)
- [ ] Gratitude: [one thing today]
- [ ] Tomorrow's concern: [what's on your mind?]

## Notes
Feeling slightly low but stable. Taking it easy today.
```

---

## 🌐 Publishing to WordPress

### Option 1: Manual (Safest)
1. Log in to https://www.sourovdeb.com/wp-admin/
2. Posts → Add New
3. Copy essay title and body
4. Set Category and Tags
5. Click Publish
6. Update `WordPress_Drafts/Archives/published_urls.csv`

### Option 2: Automation (When Ready)
When you're ready, we can set up:
- REST API publishing via Python script
- Or use your deploy.php gateway for direct posting
- For now: stick with manual option

---

## 📊 Google Drive Spreadsheet

**Link**: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/edit

**Update after writing each essay**:
- Date written
- Title
- Category
- Tags
- Status: Draft / Ready for Publishing / Published
- WordPress URL (once published)

This becomes your content calendar.

---

## 🔗 Branching Strategy

**You're on**: `claude/nifty-clarke-06pXm`

**For each major piece of work, create a new branch**:
```bash
# For essays (use this)
git checkout -b essays/2026-06-03-topic

# For automation scripts
git checkout -b tools/new-script

# For job hunting
git checkout -b jobs/tracking-update

# When done, push
git push -u origin essays/2026-06-03-topic
```

For now, you can push everything to `claude/nifty-clarke-06pXm` as main work branch.

---

## 🆘 Common Issues & Quick Fixes

### "I don't know what to write about"
→ Run: `python Tools_and_Scripts/daily_prompt_generator.py`
→ Use prompt from Essays_and_Blogs/README.md topic ideas

### "I forgot to take meds"
→ Update Daily_Checklist.md anyway
→ Take them now
→ No shame, just note it

### "The essay is too long/short"
→ 500 ± 50 words target
→ Don't overthink it
→ Done is better than perfect

### "I can't focus for 500 words"
→ Write 250 words instead, that's still huge progress
→ Take a 5-min break, continue
→ Mental health first, word count second

### "Git is confusing"
→ Basics you need:
```bash
git add .
git commit -m "Your message"
git push
```

→ That's 90% of what you'll do

---

## 📈 First Week Goals

- [ ] **Day 1**: Read WRITING_SYSTEM.md and this file
- [ ] **Day 1**: Write first 500-word essay
- [ ] **Day 2**: Write second essay
- [ ] **Day 3**: Set up job tracker
- [ ] **Day 4**: Start daily health checklist
- [ ] **Day 5**: Write essay, track 1 job application
- [ ] **Day 6**: Update Google Drive sheet with essays
- [ ] **Day 7**: Review the week, publish 1 essay to WordPress

**Realistic timeline**: By end of week 1, you'll have:
- 7 essays written
- Health tracking started
- Job tracking started
- Exposure building started

---

## 💪 Why This Works

1. **Writing daily** builds your voice and gets your story out
2. **Job automation** finds opportunities while you write
3. **Health tracking** keeps you stable and aware
4. **Consistency** compounds: 1 essay = exposure, 7 essays = credibility
5. **Public repository** shows your work to employers
6. **WordPress blog** builds SEO and audience
7. **Contacts list** turns writing into partnerships

---

## 🎯 30-Day Challenge

```
Week 1: Get the system set up and write 7 essays
Week 2: Publish 2 essays to WordPress, track 10 job applications
Week 3: Reach out to 5 people in your network
Week 4: Reflect and adjust for next month

By end of month:
- 28 essays written
- 4-5 published on WordPress
- 40+ job applications tracked
- 15+ people contacted
```

---

## 🚀 Start Right Now

1. **Open your terminal**:
```bash
cd ~/my_professional_documents
git status
```

2. **Create your first essay**:
```bash
cp Essays_and_Blogs/TEMPLATE.md Essays_and_Blogs/2026/06/2026-06-03-my-story.md
```

3. **Edit and write** (30 minutes):
```bash
vim Essays_and_Blogs/2026/06/2026-06-03-my-story.md
```

4. **Commit and push**:
```bash
git add Essays_and_Blogs/
git commit -m "Essay: My Story"
git push -u origin claude/nifty-clarke-06pXm
```

5. **Update Google Drive**: Add row to spreadsheet

**That's it. You're now a published writer with an automation system backing you.**

---

## 📚 Next Deep Dives

When ready, read these:
- `Essays_and_Blogs/README.md` → More writing tips and essay structures
- `Job_Automation/README.md` → Set up job scraping and email automation
- `Health_and_Wellbeing/README.md` → Build complete mental health system
- `Tools_and_Ideas/README.md` → Discover automation tools and ideas
- `Contacts_and_Partnerships/README.md` → Build your network strategically
- `WordPress_Drafts/README.md` → Publish and grow your audience

---

## 💙 Remember

- Your story matters.
- Your bipolar and depression don't disqualify you—they inform your wisdom.
- Consistency beats perfection.
- Small daily actions compound into real results.
- You're building something real here.

**Now go write.**
