# Automation for Bipolar Disorder & Depression

This guide is written for you specifically — someone living with bipolar disorder and depression who needs automation to reduce decision fatigue and maintain output across unpredictable energy cycles.

---

## The Core Problem Automation Solves

Bipolar creates unpredictable energy. Some days: 3,000 words. Other days: opening a document feels impossible.

Traditional publishing workflows fail because they require consistent daily action.

**Automation decouples creation from publishing:**
- High-energy days: write 3–5 posts, fill the queue
- Low-energy days: the system publishes automatically
- Your audience sees consistent output regardless of your state

---

## Three-State Workflow Design

### High Energy (Hypomania)
- Write 3–5 posts at once
- Fill Google Sheet queue with future dates
- Record voice notes of ideas for later
- **Do not publish everything immediately** — queue it across 2–3 weeks

### Medium Energy (Stable)
- Write 1 post, add to queue
- Review drafts from high-energy phase
- Adjust schedule dates as needed

### Low Energy (Depressive Phase)
- **Do nothing if needed** — the queue handles output
- Optional: Record 2 minutes of voice (Whisper transcribes it)
- Optional: Add one line to the queue sheet from your phone
- The automation protects your publishing record during difficult periods

---

## Low-Cognitive-Load Tools

### 1. Voice-to-Draft Pipeline (Zero Typing)

```python
# voice_to_post.py — record voice → WordPress draft
import os, subprocess, requests

def voice_to_wordpress_draft(audio_file: str):
    # 1. Transcribe with Whisper
    subprocess.run(['whisper', audio_file, '--language', 'en',
                   '--output_format', 'txt', '--output_dir', '/tmp'])
    
    txt_path = '/tmp/' + os.path.splitext(os.path.basename(audio_file))[0] + '.txt'
    with open(txt_path) as f:
        text = f.read().strip()
    
    # 2. First sentence = title, rest = body
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    title = sentences[0][:80] if sentences else 'Voice Note'
    body = '<p>' + '</p>\n<p>'.join(sentences[1:]) + '</p>'
    
    # 3. Send to WordPress as draft
    r = requests.post(
        'https://sourovdeb.com/wp-json/sourov/v1/ai-post',
        headers={'X-Sourov-Key': os.getenv('WP_API_KEY'), 'Content-Type': 'application/json'},
        json={'title': title, 'content': body, 'status': 'draft',
              'category': 'ELT Masterclass', 'meta_description': text[:155]}
    )
    if r.status_code == 200:
        pid = r.json().get('post_id')
        print(f'Draft created! ID: {pid}')
        print(f'Edit: https://sourovdeb.com/wp-admin/post.php?post={pid}&action=edit')
    else:
        print(f'Failed: {r.text}')

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        voice_to_wordpress_draft(sys.argv[1])
```

Usage: `python voice_to_post.py my_voice_note.mp3`

### 2. Template-Based Writing (No Blank Page)

Create this file as `~/templates/ELT_DAILY_POST.md`:

```markdown
# [Day X] – [Topic]: [Specific Angle]

## What We Practised Today
[2–3 sentences about the activity]

## The Key Insight
[1 sentence — the most important takeaway]

## Example
[1–2 concrete examples]

## Why This Matters
[1 paragraph connecting to real-world English]

## Your Task
[Simple practice activity for the reader]

---
*Part of the [ELT Masterclass series](https://sourovdeb.com/elt-masterclass)*
```

On difficult days: copy this file, fill the brackets with 10 words each. Minimum viable post complete.

### 3. Auto-Schedule Queue (No Daily Decisions)

```python
# schedule_queue.py — auto-space your draft posts across weekdays
from datetime import datetime, timedelta
import requests, os

def auto_schedule_queue(post_ids: list, start_date: str = None):
    """Schedule posts one per weekday at 9 AM."""
    current = datetime.strptime(start_date or datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    
    for post_id in post_ids:
        while current.weekday() in (5, 6):  # skip weekends
            current += timedelta(days=1)
        
        schedule_time = current.strftime('%Y-%m-%dT09:00:00')
        
        requests.post(
            f'https://sourovdeb.com/wp-json/wp/v2/posts/{post_id}',
            headers={'Authorization': 'Basic ' + _get_auth()},
            json={'status': 'future', 'date': schedule_time}
        )
        print(f'Post {post_id} scheduled: {schedule_time}')
        current += timedelta(days=1)

def _get_auth():
    import base64
    creds = f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}"
    return base64.b64encode(creds.encode()).decode()
```

---

## Mood Tracking + Publishing Correlation

```javascript
// Google Apps Script: daily mood log
// Add a 'MoodLog' sheet: Date | Mood(1-10) | Energy(1-10) | Posts_Written | Notes
function logMoodToday() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('MoodLog');
  const queueSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  const today = new Date().toDateString();
  const postsToday = queueSheet.getDataRange().getValues()
    .filter(row => row[5] && new Date(row[5]).toDateString() === today).length;
  
  sheet.appendRow([new Date(), '', '', postsToday, '']);
  // Fill Mood and Energy manually each evening — leaves Date and Posts_Written automatic
}
// Set trigger: daily at 8 PM
```

After a month you will see patterns: which mood levels correlate with writing, what time of day is most productive, whether publishing pressure increases or decreases stress.

---

## Mental Health Resources (Official Sources)

| Condition | Resource | URL |
|-----------|----------|-----|
| Bipolar | International Bipolar Foundation | ibpf.org |
| Bipolar | NAMI | nami.org/bipolar |
| Depression | WHO | who.int/mental_health |
| Crisis | Crisis Text Line | crisistextline.org |
| Medication | NLM Drug Database | medlineplus.gov |
| CBT | Centre for Clinical Interventions | cci.health.wa.gov.au/resources |
| DBT | DBT Self-Help | dbtselfhelp.com |

---

## Apps Designed for Neurodivergent Users

| App | Purpose | Platform | Cost |
|-----|---------|----------|------|
| **eMoods** | Bipolar mood tracker | iOS/Android | Free |
| **Bearable** | Symptom + mood log | iOS/Android | Free |
| **Daylio** | Micro mood journal | iOS/Android | Free |
| **Finch** | Gentle self-care | iOS/Android | Free |
| **Woebot** | AI CBT chatbot | Web/Mobile | Free |
| **Moodfit** | CBT mood management | iOS/Android | Free |
| **Headspace** | Meditation | iOS/Android | Free trial |

---

## The One Rule That Matters Most

**On bad days: do less, not nothing.**

- Cannot write 500 words? Write 50.
- Cannot write? Record 2 minutes of voice.
- Cannot record? Add one title to the queue sheet from your phone.
- Cannot do that? The system publishes anyway. Rest.

The automation exists precisely so that zero-effort days do not break your publishing momentum. Your audience continues to receive content. You continue to have an online presence. The system works even when you cannot.
