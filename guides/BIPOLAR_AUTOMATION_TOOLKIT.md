# Bipolar & Depression Automation Toolkit
## Tools and Systems Designed for Low-Energy, High-Variance Days

> This guide is for someone who has bipolar disorder or depression and needs their work systems to function even when they can't. The goal is: **minimum daily effort, maximum automated output**.

---

## CORE PRINCIPLE: Design for Your Worst Day

Your system should work on the hardest day, not just the good days. This means:
- **No decisions required daily** — decide once, execute automatically
- **Tiny entry points** — "write 1 sentence" is enough to trigger the system
- **Visible progress** — see what's been done automatically
- **Forgiving queues** — if you miss a day, the queue holds and nothing is lost

---

## SECTION 1: Mood & Health Tracking Tools

### eMoods Bipolar Mood Tracker
- **Platform:** Android, iOS
- **Free:** Basic version free
- **URL:** emoodtracker.com
- **What:** Log mood (0-5), sleep, energy, medications daily. Generates PDF report for psychiatrist.
- **Best feature:** Monthly PDF report showing patterns, episodes, medication effects
- **How to use:** 2 minutes before bed — just tap sliders, no writing required

---

### Daylio — Micro Mood Journal
- **Platform:** Android, iOS
- **Free:** Basic version free
- **URL:** daylio.net
- **What:** Log mood in 10 seconds with emoji + activity tags
- **No writing required** — just tap "good/meh/bad" and which activities you did
- **Best for:** Days when writing is impossible but you still want data
- **Export:** CSV export for analysis

---

### Google Forms + Sheets Mood Log

If you prefer completely free and custom:

```javascript
// Google Apps Script: Auto-send daily mood check-in email
function sendMoodCheckIn() {
  const formUrl = 'https://forms.gle/your-form-link';  // Create a Google Form first
  
  GmailApp.sendEmail(
    'sourovdeb.is@gmail.com',
    '[⏰ Daily Check-In] How are you today?',
    `Quick check-in. Takes 30 seconds.\n\n${formUrl}\n\nLog: mood (1-5), sleep hours, energy (1-5), medication taken (yes/no).`
  );
}
// Set this on a daily 9 AM trigger
```

The responses auto-collect in a Google Sheet. Set up a weekly summary function:

```javascript
function weeklyMoodSummary() {
  const sheet = SpreadsheetApp.openById('your-responses-sheet-id').getActiveSheet();
  const rows = sheet.getDataRange().getValues();
  
  // Get last 7 rows
  const lastWeek = rows.slice(-7);
  const avgMood = lastWeek.reduce((s, r) => s + (r[1] || 0), 0) / 7;
  const avgSleep = lastWeek.reduce((s, r) => s + (r[2] || 0), 0) / 7;
  
  GmailApp.sendEmail(
    'sourovdeb.is@gmail.com',
    '📊 Weekly Mood Report',
    `Week summary:\n\nAverage mood: ${avgMood.toFixed(1)}/5\nAverage sleep: ${avgSleep.toFixed(1)} hours\n\nShare this with your doctor.`
  );
}
// Set on weekly Monday trigger
```

---

### Bearable — Detailed Health Tracker
- **Platform:** Android, iOS
- **Free:** Core features free
- **URL:** bearable.app
- **What:** Track symptoms, medications, mood, energy, side effects with correlations
- **Best feature:** Shows correlations (e.g., "When you sleep under 6 hours, mood drops 40%")

---

## SECTION 2: Low-Effort Writing Systems

### Voice-to-Text Writing (For Low-Energy Days)

**Method 1: Google Docs Voice Typing (Free)**
1. Open Google Docs
2. Tools → Voice Typing (or Ctrl+Shift+S)
3. Click microphone
4. Speak your 500 words
5. Done — the script publishes it automatically

**Method 2: Whisper Transcription (Offline)**
```python
# Record a voice memo on your phone
# Transfer the audio file to your computer
# Run:
import whisper
model = whisper.load_model('small')
result = model.transcribe('voice_memo.m4a', language='en')
with open('draft.md', 'w') as f:
    f.write('# Untitled\n\n' + result['text'])
print('Transcribed to draft.md')
```

---

### Templates for Every Post Type

Create these templates in your Google Sheets Queue. On bad days, just fill the blanks.

**Template A: ELT Tip Post**
```markdown
# [NUMBER]: [SKILL] Tip for English Learners

Today's tip focuses on [SKILL].

## Why This Matters
[ONE SENTENCE about why learners struggle with this.]

## The Technique
[EXPLAIN the technique in 2-3 sentences.]

## Try It Now
[PRACTICAL EXERCISE they can do immediately.]

## Remember
[ONE KEY TAKEAWAY.]
```

**Template B: Lesson Reflection**
```markdown
# Day [NUMBER]: What I Learned Teaching Today

Today in class, [BRIEF DESCRIPTION].

## What Worked
[ONE THING THAT WENT WELL.]

## What I'd Do Differently
[ONE SMALL CHANGE FOR NEXT TIME.]

## Takeaway for Learners
[HOW LEARNERS CAN USE THIS.]
```

Save these templates in a Google Doc called "Blog Templates". On hard days: open template, fill brackets, copy to sheet, done.

---

## SECTION 3: Automation That Runs When You Can't

### The "No-Zero Days" Automation Stack

Goal: Even on the hardest day, the system keeps working.

```javascript
// Morning automation: runs at 8 AM every day regardless of your state
function morningAutomation() {
  // 1. Check if any posts are in queue and not yet sent
  publishFromSheet();
  
  // 2. Check WordPress health
  checkWordPressSiteHealth();
  
  // 3. Send you a gentle daily briefing
  sendDailyBriefing();
}

function sendDailyBriefing() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  const rows  = sheet.getDataRange().getValues();
  const pending = rows.filter((r, i) => i > 0 && r[0] && !r[8]).length;
  
  const message = [
    `Good morning. Here's your status:`,
    ``,
    `Posts in queue: ${pending}`,
    `Today's date: ${new Date().toDateString()}`,
    ``,
    `You only need to do ONE thing today:`,
    `Write 1 sentence about something you noticed.`,
    `That's enough.`,
    ``,
    `Your WordPress is running automatically.`,
    `Your job search alerts are active.`,
    `Everything is handled.`
  ].join('\n');
  
  GmailApp.sendEmail('sourovdeb.is@gmail.com', '🌅 Your Morning Briefing', message);
}
```

---

### Automatic Job Search (No Effort Required)

```python
# job_alert.py — run via cron daily at 7 AM
import requests, smtplib, os
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

def get_elt_jobs():
    feeds = [
        'https://rss.indeed.com/rss?q=ELT+teacher&l=R%C3%A9union',
        'https://rss.indeed.com/rss?q=English+teacher&l=France',
        'https://rss.indeed.com/rss?q=CELTA&l=Europe'
    ]
    
    import feedparser
    all_jobs = []
    for url in feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            all_jobs.append(f"• {entry.title}\n  {entry.link}")
    
    return '\n\n'.join(all_jobs[:10]) if all_jobs else 'No new jobs today.'

def send_job_digest():
    jobs = get_elt_jobs()
    
    msg = MIMEText(f"Today's ELT job listings:\n\n{jobs}")
    msg['Subject'] = '💼 Daily Job Digest'
    msg['From']    = 'sourovdeb.is@gmail.com'
    msg['To']      = 'sourovdeb.is@gmail.com'
    
    # Use Gmail SMTP with App Password
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('sourovdeb.is@gmail.com', os.getenv('GMAIL_APP_PASSWORD'))
        server.send_message(msg)

if __name__ == '__main__':
    send_job_digest()
```

Cron job: `0 7 * * * /usr/bin/python3 /home/user/job_alert.py`

---

## SECTION 4: Cognitive Load Reduction

### Decision Elimination Rules

Write these down and follow them without thinking:

| Situation | Pre-decided Action |
|-----------|-------------------|
| I don't know what to write about | Use today's date as Day N in your series |
| I don't know which category | Default: "ELT Masterclass" |
| I don't know the tags | Let the script guess them |
| I feel too tired to publish | Save as draft, script handles timing |
| I want to quit for the day | Write 1 sentence first, then quit |
| I missed yesterday | Don't catch up, just continue from today |

### Habit Stack (Morning, 15 Minutes)

```
1. Coffee on → open Google Docs
2. Set timer for 25 minutes
3. Write whatever comes to mind about teaching/learning
4. Paste to Google Sheets Queue tab
5. Mark status as 'draft'
6. Timer done? STOP. You're done for the day.
```

The automation handles everything else.

---

## SECTION 5: Crisis Mode Automation

For when you can't function at all (depressive episode, hospitalization, family crisis):

```javascript
// Pre-write 30 posts in advance when feeling well
// Store them in Queue with future dates spread over 60 days
// Set status to 'future' with dates 2-3 per week
// The trigger runs daily and publishes them automatically
// Your blog stays active even when you're not

function scheduleCrisisBuffer() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('CrisisBuffer');
  const queue = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  const rows  = sheet.getDataRange().getValues();
  
  let dayOffset = 1;
  
  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags] = rows[i];
    if (!title) continue;
    
    const postDate = new Date();
    postDate.setDate(postDate.getDate() + (dayOffset * 2));  // Every 2 days
    const dateStr = Utilities.formatDate(postDate, 'UTC', "yyyy-MM-dd'T'09:00");
    
    const nextRow = queue.getLastRow() + 1;
    queue.getRange(nextRow, 1, 1, 9).setValues([[title, content, category || 'ELT Masterclass', tags || 'ELT', 'future', dateStr, title, '', '']]);
    
    dayOffset++;
  }
  
  Logger.log('Crisis buffer scheduled: ' + (dayOffset - 1) + ' posts');
}
```

**Strategy:** Write 30 posts when you're in a good phase. Schedule them across 60 days. Even if you do nothing for 2 months, your blog keeps publishing.

---

## SECTION 6: Official Mental Health Resources

| Resource | URL | Language |
|----------|-----|----------|
| International Bipolar Foundation | ibpf.org | English |
| NIMH (Bipolar) | nimh.nih.gov/health/topics/bipolar-disorder | English |
| WHO Mental Health | who.int/mental_health | Multiple |
| PSYCOM | psycom.net | English |
| UNAFAM (French) | unafam.org | French |
| Psycom (French version) | psycom.net/fr | French |
| PubMed (Research) | pubmed.ncbi.nlm.nih.gov | English |

**Search on PubMed for your medications:** Type `lamotrigine bipolar` or `lithium depression maintenance` to find actual clinical studies.

---

## SECTION 7: Medication & Appointment Automation

```javascript
// In Google Calendar Apps Script: medication reminders
function setMedicationReminders() {
  const calendar = CalendarApp.getDefaultCalendar();
  const now = new Date();
  
  // Set reminders for 30 days
  for (let i = 0; i < 30; i++) {
    const date = new Date(now);
    date.setDate(date.getDate() + i);
    date.setHours(21, 0, 0);  // 9 PM
    
    calendar.createEvent(
      '💊 Medication time',
      date,
      new Date(date.getTime() + 15 * 60000),  // 15 min duration
      { reminders: { minutesBefore: [5, 30] } }
    );
  }
}

// Run once; sets 30 days of reminders
```

---

*This guide is informational, not medical advice. Always follow your psychiatrist's instructions.*

*Last updated: June 2026*
