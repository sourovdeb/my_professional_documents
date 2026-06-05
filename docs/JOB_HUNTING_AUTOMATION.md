# Job Hunting Automation Guide

> Automate job searching, email alerts, and application tracking. Focus: ELT/CELTA positions in Réunion and remote teaching roles.

---

## Part 1: RSS-Based Job Alerts (No Scraping, No Account Needed)

Many job sites publish RSS feeds. You can monitor them with Python.

```python
# job_alerts.py
# pip install feedparser requests python-dotenv

import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

EMAIL_FROM = os.getenv('EMAIL_FROM', 'your@email.com')
EMAIL_TO = os.getenv('EMAIL_TO', 'sourovdeb.is@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASSWORD')

JOB_FEEDS = [
    # Indeed RSS (free, no account)
    'https://rss.indeed.com/rss?q=ELT+teacher&l=Reunion',
    'https://rss.indeed.com/rss?q=CELTA+teacher&l=',
    'https://rss.indeed.com/rss?q=English+teacher+online&l=',
    # ProBlogger jobs (writing work)
    'https://problogger.com/jobs/feed/',
]

SEEN_LINKS_FILE = 'seen_jobs.txt'


def load_seen():
    try:
        return set(open(SEEN_LINKS_FILE).read().splitlines())
    except FileNotFoundError:
        return set()


def save_seen(seen):
    with open(SEEN_LINKS_FILE, 'w') as f:
        f.write('\n'.join(seen))


def fetch_new_jobs():
    seen = load_seen()
    new_jobs = []

    for feed_url in JOB_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:10]:
                link = entry.get('link', '')
                if link and link not in seen:
                    new_jobs.append({
                        'title': entry.get('title', 'No title'),
                        'link': link,
                        'summary': entry.get('summary', '')[:300],
                        'published': entry.get('published', 'Unknown date')
                    })
                    seen.add(link)
        except Exception as e:
            print(f'Feed error: {feed_url} — {e}')

    save_seen(seen)
    return new_jobs


def send_job_alert(jobs):
    if not jobs:
        print('No new jobs found.')
        return

    body = f'NEW JOB MATCHES — {datetime.now().strftime("%Y-%m-%d")}\n\n'
    for job in jobs:
        body += f'TITLE: {job["title"]}\n'
        body += f'LINK:  {job["link"]}\n'
        body += f'DATE:  {job["published"]}\n'
        body += f'{job["summary"]}\n'
        body += '-' * 60 + '\n\n'

    msg = MIMEText(body)
    msg['Subject'] = f'{len(jobs)} New Job Matches — {datetime.now().strftime("%a %d %b")}'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        with smtplib.SMTP('smtp.zoho.com', 587) as s:
            s.starttls()
            s.login(EMAIL_FROM, EMAIL_PASS)
            s.send_message(msg)
        print(f'Sent alert: {len(jobs)} new jobs')
    except Exception as e:
        print(f'Email error: {e}')
        print(body)  # print to console as fallback


if __name__ == '__main__':
    jobs = fetch_new_jobs()
    send_job_alert(jobs)
    print(f'Found {len(jobs)} new jobs.')
```

**Set up daily cron job:**
```bash
# Run every morning at 8am
0 8 * * * /usr/bin/python3 /path/to/job_alerts.py
```

---

## Part 2: Google Sheets Job Tracker

Track all applications in a spreadsheet:

**Columns:**
```
A: Company | B: Role | C: Location | D: Salary | E: Status | F: Date Applied
G: Contact | H: Link | I: Notes
```

**Status values:**
- `researching` → `applied` → `interview` → `offer` → `rejected` → `accepted`

**Apps Script: Auto-remind on stale applications**
```javascript
function remindStaleApplications() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Applications');
  var data = sheet.getDataRange().getValues();
  var stale = [];
  var now = new Date();

  for (var i = 1; i < data.length; i++) {
    var status = data[i][4];
    var dateApplied = data[i][5];
    if (!dateApplied || status === 'rejected' || status === 'accepted') continue;
    
    var days = (now - new Date(dateApplied)) / (1000 * 60 * 60 * 24);
    if (days > 14) {  // no response in 2 weeks
      stale.push({ company: data[i][0], role: data[i][1], days: Math.floor(days) });
    }
  }

  if (stale.length > 0) {
    var msg = stale.map(s => s.company + ' — ' + s.role + ' (' + s.days + ' days ago)').join('\n');
    MailApp.sendEmail('sourovdeb.is@gmail.com', 'Follow-up Reminder: ' + stale.length + ' applications', msg);
  }
}
```

Set a weekly trigger on this function.

---

## Part 3: Job Search Sources

### ELT-Specific Boards

| Site | URL | Best For |
|------|-----|----------|
| **Dave's ESL Cafe** | eslcafe.com/jobs | Classic ESL jobs worldwide |
| **TEFL.com** | tefl.com | CELTA/TEFL positions |
| **ELT Base** | eltbase.com | UK + international ELT |
| **Guardian Education** | theguardian.com/education/jobs | UK teaching positions |
| **TES** | tes.com | International teaching |
| **Footprint Recruitment** | footprintrecruit.com | High-quality placements |

### General Boards (With ELT Options)

| Site | RSS? | Notes |
|------|------|-------|
| **Indeed** | Yes | Best RSS coverage |
| **LinkedIn Jobs** | No (use email alerts) | Best for networking |
| **Glassdoor** | No | Good for salary research |
| **WorkInReunion** | Check site | Réunion-specific |
| **Pôle Emploi** | RSS available | French employment service |

### Remote Teaching Platforms

| Platform | Students | Pay | Application |
|----------|---------|-----|-------------|
| **italki** | Adults worldwide | Flexible | Self-employed |
| **Preply** | Adults worldwide | Commission-based | Portfolio needed |
| **VIPKid** | Chinese children | Good hourly | CELTA preferred |
| **Cambly** | Adults worldwide | Per-minute | Easy to start |
| **Outschool** | Kids/teens | Set your rate | US-focused |

---

## Part 4: CV & Cover Letter Automation

### Customising Quickly with Apps Script

```javascript
// Generate custom cover letter from template
function generateCoverLetter(companyName, role, contactName) {
  var template = DriveApp.getFilesByName('COVER_LETTER_TEMPLATE').next();
  var doc = template.makeCopy(companyName + ' — ' + role);
  var body = DocumentApp.openById(doc.getId()).getBody();
  
  body.replaceText('\\{\\{COMPANY\\}\\}', companyName);
  body.replaceText('\\{\\{ROLE\\}\\}', role);
  body.replaceText('\\{\\{CONTACT\\}\\}', contactName || 'Hiring Manager');
  body.replaceText('\\{\\{DATE\\}\\}', new Date().toLocaleDateString('en-GB'));
  
  return doc.getUrl();
}
```

Store your CV on Google Drive, create variations quickly.

---

## Part 5: LinkedIn Without Scraping

LinkedIn does not allow scraping. Instead:

1. **Set up Job Alerts** (LinkedIn → Jobs → Set alert for saved searches) — email alerts are free
2. **Use LinkedIn's Open to Work** feature — recruiters find you
3. **Engage with ELT communities** — comment on ELT posts to appear in feeds
4. **Post your blog articles** as LinkedIn articles (cross-post from WordPress)
5. **Connect with CELTA centres** — they often post jobs first on LinkedIn

---

## Part 6: Freelance & Collaboration Platforms

| Platform | Best For | Free to Join? |
|----------|---------|---------------|
| **Upwork** | Freelance writing, ELT materials creation | Free basic |
| **Fiverr** | Sell lesson plans, teaching resources | Free |
| **Teachers Pay Teachers** | Sell ELT worksheets | Free basic |
| **Reedsy** | Book/content editing | Free for authors |
| **Contently** | Content writing for brands | Free portfolio |

---

## Part 7: Telegram Job Alert Bot (Free Alternative to Email)

```python
# Send job alerts to yourself via Telegram (free)
import requests

TG_TOKEN = 'your-bot-token'  # get from @BotFather on Telegram
TG_CHAT_ID = 'your-chat-id'  # get from @userinfobot

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TG_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': TG_CHAT_ID, 'text': message, 'parse_mode': 'HTML'})

# Use instead of send_job_alert():
send_telegram(f'<b>New Job:</b> {job["title"]}\n{job["link"]}')
```

Setting up Telegram bot:
1. Message **@BotFather** on Telegram → `/newbot`
2. Get your token
3. Message **@userinfobot** to get your chat ID
4. Free, instant, works on mobile
