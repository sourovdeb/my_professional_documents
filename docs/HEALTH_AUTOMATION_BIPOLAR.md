# Health Automation for Bipolar & Depression — Tools & Systems

> This guide helps automate daily decisions and reduce cognitive load, which is especially important when managing bipolar disorder and depression. All tools are verified, reputable, and free or low-cost.

---

## Official Resources First

| Condition | Trusted Source | URL |
|-----------|---------------|-----|
| Bipolar disorder | National Institute of Mental Health (USA) | nimh.nih.gov/health/topics/bipolar-disorder |
| Bipolar disorder | International Bipolar Foundation | ibpf.org |
| Depression | World Health Organization | who.int/news-room/fact-sheets/detail/depression |
| Both | Black Dog Institute (Australia) | blackdoginstitute.org.au |
| Medication info | PubMed (search your exact drug name) | pubmed.ncbi.nlm.nih.gov |
| Crisis support | International Association for Suicide Prevention | https://www.iasp.info/resources/Crisis_Centres/ |

---

## Part 1: Mood Tracking Apps

Tracking your mood daily takes 30 seconds and gives you and your doctor data.

| App | Platform | Key Feature | Cost |
|-----|----------|-------------|------|
| **eMoods** | Android/iOS | Designed specifically for bipolar | Free basic |
| **Daylio** | Android/iOS | Micro-journal, no writing needed | Free |
| **Bearable** | Android/iOS | Tracks mood, symptoms, medication, sleep | Free |
| **Mood Patrol** | iOS | Simple mood logging | Free |
| **iMoodJournal** | Android/iOS | Detailed mood charts | Free |
| **MoodFit** | Android/iOS | CBT-based mood + habits | Free |
| **Finch** | Android/iOS | Self-care through a virtual pet | Free |

**Recommendation:** Start with **Daylio**. It takes under 10 seconds per entry — just pick a mood emoji and tap activities. Over weeks you can see patterns (e.g., "I'm always low on Mondays").

---

## Part 2: Habit & Routine Automation

The best strategy for bipolar is **zero-decision routines** — automated systems that tell you what to do, so you don't have to decide.

### Apps for Habit Tracking

| App | Best For | Free? |
|-----|----------|-------|
| **Habitica** | Gamify habits (RPG-style) | Free |
| **Loop Habit Tracker** | Android, minimal, open-source | Free |
| **Streaks** | iOS, focuses on small daily actions | Paid |
| **Done** | Simple tracker with flexible scheduling | Free tier |
| **Productive** | iOS, beautiful habit tracking | Free tier |
| **HabitBull** | Android, multiple habit tracking | Free |

### The "No Zero Day" System

The rule: **every single day, do at least ONE productive thing** — even if that's just writing 1 sentence.

This prevents the crash-and-shame cycle common with bipolar. A 1-sentence day is infinitely better than a 0-sentence day.

---

## Part 3: Automated Reminders & Medication

### Medication Reminder Apps

| App | Platform | Notes |
|-----|----------|-------|
| **Medisafe** | Android/iOS | Best medication reminder app, refill alerts | Free |
| **Roundhealth** | Android/iOS | Clean interface | Free |
| **MyTherapy** | Android/iOS | Medication + mood + journal | Free |
| **Pill Reminder** | Android | Simple, reliable | Free |

### Automate Health Logging with Google Forms

Create a daily check-in form that logs to a spreadsheet:

1. Go to **forms.google.com** → Create a form
2. Add questions:
   - "How is your energy today? (1-5)"
   - "How is your mood today? (1-5)"
   - "Did you take your medication? (Yes/No)"
   - "Hours of sleep last night? (number)"
   - "One sentence about today (short text)"
3. Set your form response destination to a Google Sheet
4. Add a bookmark to your phone home screen
5. Fill it every morning — takes 60 seconds

**Then automate weekly reports with Apps Script:**

```javascript
// Runs every Sunday and emails you a weekly summary
function weeklyHealthReport() {
  var sheet = SpreadsheetApp.openById('YOUR_SHEET_ID').getActiveSheet();
  var data = sheet.getDataRange().getValues();
  
  // Get last 7 rows
  var recent = data.slice(-7);
  var avgEnergy = recent.reduce((s, r) => s + (parseFloat(r[1]) || 0), 0) / 7;
  var avgMood = recent.reduce((s, r) => s + (parseFloat(r[2]) || 0), 0) / 7;
  var medCompliance = recent.filter(r => String(r[3]).toLowerCase() === 'yes').length;
  var avgSleep = recent.reduce((s, r) => s + (parseFloat(r[4]) || 0), 0) / 7;
  
  var body = [
    'WEEKLY HEALTH REPORT',
    '===================',
    'Average energy this week: ' + avgEnergy.toFixed(1) + '/5',
    'Average mood this week: ' + avgMood.toFixed(1) + '/5',
    'Medication taken: ' + medCompliance + '/7 days',
    'Average sleep: ' + avgSleep.toFixed(1) + ' hours',
    '',
    'Keep going. One day at a time.'
  ].join('\n');
  
  MailApp.sendEmail({
    to: 'sourovdeb.is@gmail.com',
    subject: 'Your Weekly Health Summary — Week of ' + new Date().toDateString(),
    body: body
  });
}
```

---

## Part 4: Productivity Systems for Low-Energy Days

### The Pomodoro Technique (Best for ADHD & Depression)

**25 minutes work → 5 minutes rest → repeat**

Free Pomodoro tools:
- **Pomofocus** — pomofocus.io (browser-based, clean)
- **Forest App** — gamified, plants virtual trees
- **Focus To-Do** — Pomodoro + task list combined
- **Simple Pomodoro** — Chrome extension

### Energy-Based Scheduling

Instead of scheduling by time, schedule by energy level:

```
HIGH ENERGY (morning, feeling good):
  → Write blog posts
  → Send emails
  → Record audio
  → Learn new techniques

MEDIUM ENERGY (afternoon, stable):
  → Edit and proofread
  → Fill in Google Sheets queue
  → Reply to comments
  → Research topics

LOW ENERGY (evening, tired):
  → Read
  → Listen to podcasts
  → Use speech-to-text to capture rough notes
  → Plan tomorrow's schedule

VERY LOW / CRISIS:
  → Use template (ELT_TEMPLATE.md in drafts/)
  → Write just ONE paragraph
  → That counts. You still showed up.
```

### Writing Templates Reduce Decision Fatigue

The `drafts/ELT_TEMPLATE.md` file in this repository gives you a pre-structured post. You only fill in the blank sections — no blank-page paralysis.

---

## Part 5: Sleep Tracking

Sleep is the most critical variable for bipolar management.

| App | Free? | Notes |
|-----|-------|-------|
| **Sleep as Android** | Free basic | Detects sleep cycles, wakes gently |
| **Pillow** | iOS free | Sleep analysis, smart alarm |
| **Oura Ring** | Hardware purchase | Most accurate, medical-grade data |
| **Whoop** | Subscription | Athletic + recovery tracking |
| **FitBit app** | Needs device | Good sleep stages tracking |
| **SleepWatch** | Free | Works with Apple Watch |

**Log your sleep in your daily health form** (see above) — even a rough estimate is useful data.

---

## Part 6: Crisis Plan Automation

When energy is very low, having a pre-written plan removes the need to think:

### Create a "Low Day" shortcut on your phone:
1. Open Google Docs → Create a document called **"LOW DAY PROTOCOL"**
2. Write in it now (while you feel okay):
   - 3 things that always help (e.g., shower, short walk, call friend)
   - Your doctor/therapist name and number
   - One small task to feel accomplished
   - Permission to rest: "Resting is productive."
3. Bookmark it on your phone home screen

### Emergency contacts automation:
Use **IFTTT (free)** or **Google Assistant routines** to set a phrase like "I'm struggling" that:
- Sends a pre-written text to your support person
- Opens your crisis protocol document
- Starts calming music

---

## Part 7: Automating the Writing System for Low-Energy Days

Specifically for your blogging system:

1. **When energy is high:** Write 3-5 posts and fill the Google Sheets queue
2. **When energy is medium:** Just add to the queue — no need to write from scratch
3. **When energy is low:** The automation publishes what you already wrote — you do nothing
4. **When energy is very low:** Queue is your safety net. Content keeps going out even if you rest for a week

This is why the automation system is important for your mental health — it creates **continuity without daily effort**.

---

## Part 8: Trusted Mental Health Hotlines

| Country | Service | Number |
|---------|---------|--------|
| France/Réunion | Numéro national de prévention du suicide | **3114** |
| France | Fil Santé Jeunes | **0800 235 236** |
| UK | Samaritans | **116 123** |
| USA | 988 Suicide & Crisis Lifeline | **988** |
| International | befrienders.org | Various by country |

> You are not alone. Your writing has value. Rest is not failure.
