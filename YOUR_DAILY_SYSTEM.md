# Your Complete Daily System

Everything integrated. All your tools, scripts, and practices working together. For bipolar, depression, and creating sustainable success.

---

## 🌅 Morning Routine (15 minutes)

### 6:00 AM - Wake Up (Non-Negotiable)
```bash
# Same time every morning, even weekends
# Reset your circadian rhythm
# Immediately get sunlight (5-10 min outside)
```

### 6:10 AM - Wellness Check-In
```bash
python Tools_and_Scripts/bipolar_wellness_tracker.py --checkin
# Questions:
# - Did you take medications? (YES - non-negotiable)
# - How many hours did you sleep?
# - Rate mood 1-10
# - Rate energy 1-10
# - Rate anxiety 1-10
# - Did you move, eat, socialize yesterday?
# - Any warning signs? (racing thoughts, no sleep, spending, isolation)
```

### 6:20 AM - Daily Writing Prompt
```bash
python Tools_and_Scripts/daily_prompt_generator.py
# Get today's writing prompt based on your topic
# (Mental Health / Career / Automation / Philosophy)
```

### 6:25 AM - Review Day Ahead
```
Check calendar for:
- Teaching appointments (if applicable)
- Therapy sessions
- Medication reminders set?
- Stressful meetings?
- Energy level realistic for today?
```

**By 6:30 AM**: You've assessed your stability for the day. This prevents surprises.

---

## 📝 Writing Time (30 minutes)

### 7:00 AM - 7:30 AM (Every Day)
```bash
# Create essay file
cp Essays_and_Blogs/TEMPLATE.md Essays_and_Blogs/2026/06/2026-06-03-prompt-response.md

# Write 500 words to your daily prompt
vim Essays_and_Blogs/2026/06/2026-06-03-prompt-response.md

# Writing checklist:
# - Active voice (I learned, not "it was learned")
# - Personal truth (your experience, your voice)
# - Something useful (reader learns something actionable)
# - No perfection needed (done > perfect)
```

**By 7:30 AM**: You've written 500 words. By Friday, you have 2,500 words toward your weekly essay goal.

---

## 💼 Job Automation (10 minutes)

### 8:00 AM - Job Opportunity Check
```bash
# Check for new relevant jobs
python Tools_and_Scripts/indeed_scraper.py \
  --job-title "English Teacher" \
  --location remote \
  --max-results 10

# Review this week's job tracker
python Tools_and_Scripts/job_tracker.py stats

# Add any interesting jobs
python Tools_and_Scripts/job_tracker.py add \
  "Company Name" \
  "Position Title" \
  "Remote" \
  "Salary Range"
```

**Result**: You know about new opportunities without spending 2 hours searching.

---

## 🎯 Work/Teaching (Your Main Job)

### 9:00 AM - 12:00 PM (Work Hours)
```
If teaching/working full-time:
- Work focused blocks (90 min work, 15 min break)
- No back-to-back meetings (recovery time)
- Hydrate, move, step outside during breaks
- If mood is off, communicate it
```

---

## 🍽️ Midday (Lunch & Recovery)

### 12:00 PM - 1:00 PM
```
Non-negotiable:
- Eat real meal (not snacking)
- 10-20 minute walk (sunlight, movement)
- No screens
- If depressed: be extra kind to yourself
- If hypomanic: slow down, drink water, ground yourself
```

---

## 📊 Health Check (2 minutes)

### 2:00 PM - Energy Check
```
Quick check:
- Still on track?
- Energy holding?
- Need to adjust afternoon?
- Any mood shifts?
```

If you're struggling:
- Take 10-min break
- Call someone
- Do breathing exercise (4-7-8: breathe 4, hold 7, exhale 8)
- Adjust expectations for rest of day

---

## 💌 Networking (5 minutes)

### 3:00 PM - One Connection
```bash
# Reach out to one person in your network
# Could be:
# - Email someone about a job
# - Message a peer (mental health solidarity)
# - Add contact to Contacts_and_Partnerships/Network_Master.csv
# - LinkedIn message to potential collaborator
```

One person per day = 5 per week = 20+ per month = real network.

---

## 🌙 Evening Wind-Down (30 minutes)

### 5:30 PM - Work Ends (Hard Stop)
```
No work after 5:30pm
- Close emails
- Close Slack
- Physically leave workspace (even if home office)
```

### 5:30 PM - 6:00 PM - Transition
```
Activities:
- Light walk or gentle stretch
- Change clothes (work → home)
- Prepare dinner
- Slow your nervous system down
- Review how today went (journal 2 min)
```

### 6:00 PM - 7:00 PM - Dinner & Family Time
```
Eat, connect, enjoy.
No screens for first 30 min of eating.
```

---

## 📱 Evening Check-In (5 minutes)

### 7:00 PM - Update Health Tracking
```
Simple reflection:
- How was my energy today? (1-10)
- Did I do the non-negotiables? (meds, sleep schedule, movement)
- Mood swings? (what triggered them?)
- Tomorrow concern: what's on my mind?
```

Jot in notebook or phone note. This is data for patterns.

---

## 🧘 Wind-Down Ritual (30 minutes)

### 7:30 PM - No Screens
```
Activities (pick one):
- Read fiction (not engaging, soothing)
- Take warm bath
- Gentle yoga or stretching
- Journaling (process emotions)
- Listen to familiar podcast/audiobook
- Chat with friend/therapist (no work talk)
```

### 8:00 PM - Bed Prep
```
Non-negotiable sleep prep:
- Bedroom cool (60-67°F if possible)
- Dark (blackout curtains or eye mask)
- Quiet (white noise if needed)
- Phone out of reach
- Comfy bedding
```

### 8:30 PM - In Bed
```
Lights off. Consistent bedtime ±30 min.
If can't sleep after 20 min: get up and read until tired.
(Don't lay in bed frustrated)
```

---

## 📅 Weekly Ritual (30 minutes, Every Friday)

### Friday 10:00 AM - Weekly Wellness Review
```bash
python Tools_and_Scripts/bipolar_wellness_tracker.py --weekly

# System shows:
# - Average mood, energy, sleep, anxiety
# - Medication adherence (was it 100%?)
# - Social connection days
# - Movement days
# - Danger signs detected
# - Pattern insights

# You assess:
# - Am I stabilizing or cycling?
# - What's one thing to adjust next week?
# - Do I need to contact my therapist/doctor?
# - Am I sleeping enough? (Most important)
```

### Friday 10:30 AM - Blog Content Review
```bash
# Check Essays_and_Blogs/ folder
# Count essays written this week (goal: 5-7)

# Review what's ready to publish:
# - Update Google Drive sheet
# - Move ready essays to wordpress_blog_queue.csv
# - Mark approved=TRUE, status=Ready

# If you have 2-3 posts ready:
python Tools_and_Scripts/sync_to_wordpress.py --dry-run  # Preview
python Tools_and_Scripts/sync_to_wordpress.py --live      # Publish
```

### Friday 11:00 AM - Job Search Review
```bash
python Tools_and_Scripts/job_tracker.py follow-ups

# System shows:
# - Which applications need follow-ups
# - How many applications this week
# - Response rate
# - Any interviews?

# Action:
# - Follow up on 1-week-old applications
# - Plan 3-5 applications for next week
```

### Friday 2:00 PM - Network Check
```
Review Contacts_and_Partnerships/Network_Master.csv
- Any relationships to reconnect with?
- Anyone to follow up with?
- Plan one coffee chat for next week
```

---

## 📊 Monthly Review (1 hour, Last Friday of Month)

### Big Picture Check
```
What went well this month?
- Written how many essays? (goal: 20+)
- Published how many to WordPress? (goal: 4-5)
- Applied to how many jobs? (goal: 40-50)
- New connections made? (goal: 10+)
- Medication adherence? (goal: 100%)
- Stability: episodes, triggers, patterns?
```

### Data Analysis
```bash
python Tools_and_Scripts/bipolar_wellness_tracker.py --stats

# Review mood patterns from month
# Sleep quality trends
# Energy levels over time
# Medication effectiveness
```

### Therapist/Doctor Update
```
Send to your therapist/psychiatrist:
- Monthly wellness summary
- Any episodes or concerning patterns
- Medication effectiveness (good/bad/changes)
- Sleep, exercise adherence
- Stress level
- Anything to adjust for next month?
```

### Next Month Planning
```
Decide:
- Blog topic focus (month 1: mental health, month 2: career, month 3: automation)
- Job search strategy (how many applications, which companies)
- Health goal (sleep consistency, exercise, therapy homework)
- Networking goal (how many new connections)
```

---

## 🚨 When You're Struggling (During Episode)

### Depressive Episode Day
```
Modified schedule (TEMPORARY):
- Morning: Still check-in (sleep, meds, mood)
- Writing: 250 words instead of 500 (or skip if you can't)
- Work: Take it easy, communicate to employer/students
- Job hunting: Pause until stabilized
- Evening: Extra kindness, call someone

✓ Non-negotiable still:
- Medications (especially important)
- Sleep on schedule
- Eat basic meals
- One contact with another person

✗ Give yourself break on:
- Productivity
- Perfection
- Job hunting
- Social obligations
```

### Manic/Hypomanic Episode Day
```
Modified schedule (TEMPORARY):
- Morning: Extra check-in (sleep especially - <5 hours = warning)
- Work: Time-box heavily (stop at 5:30pm hard stop)
- Writing: Shorter sessions, structured time blocks
- Job hunting: PAUSE (hypomanic job seeking leads to bad decisions)
- Spending: Extra safeguards (cash only, ask friend before purchases)

✓ Non-negotiable:
- Medications (follow psychiatrist guidance)
- Sleep (this is THE priority - meds may increase)
- Regular meal times
- Exercise to burn energy (but not excessive)

✗ Do not:
- Make major decisions
- Email anyone while manic (drafts only)
- Start new projects
- Make financial commitments
- Increase caffeine
```

**Contact**: If you're in crisis, call therapist/psychiatrist/crisis line immediately.

---

## 🎯 Weekly Time Investment

```
Morning routine:       15 min/day = 1.75 hrs/week
Writing time:          30 min/day = 3.5 hrs/week
Job automation:        10 min/day = 1 hrs/week
Networking:            5 min/day = 30 min/week
Evening wind-down:     30 min/day = 3.5 hrs/week
Work/teaching:         35 hrs/week
Weekly review:         30 min/week
────────────────────────────
Total: ~50 hours/week
(35 work + 15 self-care/automation)
```

This is sustainable. Not burning out. Not sacrificing mental health for productivity.

---

## 📈 Monthly Results You'll See

### By End of Month 1:
- 20+ essays written
- 1-2 published to WordPress
- 40-50 job applications
- 10+ new network connections
- Consistent mood tracking
- No hospitalizations
- Therapist sees improvement

### By End of Month 3:
- 60+ essays written
- 8-12 published to WordPress
- 120+ job applications (and follow-ups)
- 30+ network connections
- Clear mood patterns identified
- Job interviews happening
- Speaking/writing opportunities emerging

### By End of Month 6:
- Your WordPress blog is a real portfolio
- Job offers coming in
- Writing credibility established
- Support network activated
- Mental health stable and managed
- Income diversified (multiple streams)

---

## 🎯 The Philosophy

This system works because:

1. **Mental health first** - Wellness checks prevent crises
2. **Sustainable pace** - 50 hrs/week is doable long-term
3. **Automated where possible** - Job hunting, mood tracking, blog publishing
4. **Manual where it matters** - Writing, networking, therapy
5. **Feedback loops** - Weekly and monthly reviews keep you on track
6. **Flexibility during struggles** - System adapts when you have episodes
7. **Public accountability** - Blog and GitHub portfolio keep you motivated

---

## 🚀 Start Monday

Choose one:

**Option A** (All-in):
- Do morning routine Monday
- Do wellness check-in Monday
- Do writing time Monday
- See how it feels

**Option B** (Conservative):
- Just do wellness check-in this week
- Add writing next week
- Add job tracking week 3

There's no perfect. Start with what you can sustain.

---

## 💙 Remember

- **Your bipolar isn't a flaw**. Your system adapts to it.
- **Your story matters**. The world needs your perspective.
- **Consistency beats perfection**. Done > perfect.
- **You're building something real**. Not just surviving. Building.
- **This is a marathon**. Pace yourself.

One day at a time.
One essay at a time.
One connection at a time.

By the end, you'll have:
- A portfolio (essays + WordPress blog)
- Job offers
- Network (collaborators, supporters, friends)
- Stability (mental health managed)
- Income (writing, speaking, teaching, freelancing)
- Impact (your story helping others)

But it starts Monday morning.

**First thing**: Set your alarm for 6:00 AM.

Everything else follows from there.

You've got this. 💪
