# APPLICATION TRACKER v1.0 — Complete User Guide

**Purpose:** Track all job applications, delivery status, responses, prevent duplicates  
**Data source:** Gmail (automatic scan) + Manual entries  
**Storage:** Google Sheet (persistent) + Console logs  
**Time to setup:** 3 minutes  

---

## PART 1: SETUP

### Step 1: Add Script to Google Sheets

1. Open Google Sheet (new or existing)
2. Click `Extensions` → `Apps Script`
3. Copy entire `APPLICATION_TRACKER_v1.gs` file
4. Paste into editor
5. Click Save (Ctrl+S)
6. Reload your Google Sheet (F5)

### Step 2: First Run

1. In Google Sheet, click menu: **`📊 Application Tracker`** → **`🔄 Scan Gmail & Update`**
2. **Authorize Gmail access** when prompted (required once)
3. Wait 30 seconds - script reads all your sent emails
4. Check console for results (Ctrl+` in Apps Script)

---

## PART 2: UNDERSTANDING THE TRACKER SHEET

### Columns

| Column | Meaning | Updated By |
|--------|---------|-----------|
| **A: Date Sent** | When email was sent | Auto (from Gmail) |
| **B: Organization** | Company/institution name | Auto (extracted from subject) |
| **C: Recipient Email** | Who you sent to | Auto (from Gmail) |
| **D: Contact Person** | Name of contact (optional) | Manual |
| **E: Sector** | Industry/field | Manual |
| **F: Subject Line** | Full email subject | Auto (from Gmail) |
| **G: Delivery Status** | ✅ Delivered / ❌ Bounced / ⏳ Pending | Auto |
| **H: Response Status** | No Response / Reply Received / Meeting Scheduled | Manual |
| **I: Response Date** | When you got a reply | Manual |
| **J: Notes** | Any additional info | Manual |
| **K: Campaign Round** | Which batch (Round 1, Round 2, etc) | Manual |

### Delivery Status Legend
```
✅ Delivered    = Email successfully sent (7+ days passed or no bounce)
❌ Bounced      = Delivery failure detected (bounce notification received)
⏳ Pending      = Less than 7 days old, still checking
```

### Response Status Legend
```
No Response           = No reply yet (check after 7 days)
Reply Received        = Person responded to your email
Meeting Scheduled     = Meeting agreed upon
Warm Lead             = Promising contact for follow-up
Call Back Requested   = Person wants to speak by phone
```

---

## PART 3: AUTOMATIC FEATURES

### Feature 1: Auto-Scan Gmail

**Function:** `scanGmailApplications()`

**What it does:**
1. Searches Gmail for emails matching these subjects:
   - "Candidature"
   - "Formateur Anglais"
   - "Cambridge CELTA"
   - "Offre de Services"
2. Extracts recipient email, organization, date
3. Checks for bounce notifications
4. Adds to tracker sheet (prevents duplicates)

**How to use:**
- Menu → `📊 Application Tracker` → `🔄 Scan Gmail & Update`
- Or run manually: `scanGmailApplications()`

**Run frequency:**
- First time: Full scan of all past emails
- Subsequently: Weekly to catch new applications

**What you'll see:**
```
📧 Scanning Gmail for job applications...

📋 Found 5 existing records in tracker

📨 Found 12 matching emails in Gmail

✅ [1] Added: Académie de La Réunion (ce.recteur@ac-reunion.fr)
✅ [2] Added: Région Réunion (formation@regionreunion.com)
...

📊 New records added: 7
```

### Feature 2: Automatic Bounce Detection

**How it works:**
- Script checks for "Delivery Status Notification (Failure)" emails
- Automatically marks as `❌ Bounced`
- Waits 7 days before marking as `✅ Delivered` (if no bounce)

**Manual correction:**
If email shows `⏳ Pending` but you know it bounced:
1. Right-click cell in column G
2. Edit: Change to `❌ Bounced`
3. Note reason in column J

### Feature 3: Automatic Organization Extraction

Script tries to extract organization name from subject line.

**Examples:**
```
Email subject: "Candidature Formateur Anglais CELTA — Académie Réunion — Saint-Denis"
Extracted: "Académie Réunion"

Email subject: "Offre de Services Formateur CELTA — Région Réunion"
Extracted: "Région Réunion"
```

**If extraction fails:**
- Column B shows recipient domain (ce.recteur@ac-reunion.fr → ac-reunion.fr)
- Edit manually to correct organization name

### Feature 4: Automatic Response Detection

**How it works:**
- Checks if recipient replied to your email
- If reply found, marks `Response Status: Reply Received`
- Records response date

**Note:** Gmail API only detects thread responses, not standalone replies

---

## PART 4: MANUAL FEATURES

### Add Entry Manually

**Use when:**
- You sent application outside Gmail (LinkedIn, website form, etc)
- You want to log past applications

**Method 1: Google Sheets Menu**
1. Click menu → `📊 Application Tracker` → `📝 Manual Log Entry`
2. Fill in prompts:
   - Organization: "Koz'Anglais"
   - Email: "contact@kozanglais.com"
   - Contact: "Sarah" (optional)
   - Sector: "Formation Anglais" (optional)
   - Subject: "Candidature Formateur CELTA"
   - Campaign Round: "Round 2" (optional)

**Method 2: Direct Entry in Sheet**
1. Open tracker sheet
2. Click last row
3. Fill in columns A-K manually
4. Press Enter

**Method 3: Apps Script Console**
```javascript
logApplicationManually(
  'Sakoa Boutique Hôtel',              // org
  'direction@sakoa-hotel.re',          // email
  'Directeur RH',                      // contact person
  'Hôtellerie',                        // sector
  'Candidature Formateur Anglais',     // subject
  'Round 1'                            // campaign round
);
```

### Mark Response Received

**Use when:**
- Someone replies to your application
- Meeting is scheduled
- Phone call requested

**Method 1: Google Sheets Menu**
1. Click menu → `📊 Application Tracker` → `✏️ Mark as Responded`
2. Enter recipient email
3. Enter response type:
   - "Reply Received"
   - "Meeting Scheduled"
   - "Call Back Requested"
   - "Warm Lead"
4. Add notes (optional)

**Method 2: Direct Edit in Sheet**
1. Find row with that email (column C)
2. Column H: Enter response status
3. Column I: Enter response date (format: DD/MM/YYYY)
4. Column J: Add notes

**Method 3: Apps Script Console**
```javascript
markApplicationResponse(
  'ce.recteur@ac-reunion.fr',
  'Reply Received',
  'Recteur interested, wants meeting next week'
);
```

### Find an Application

**Use when:**
- You need details about a specific application
- Check if already sent (prevent duplicate)

**Method 1: Google Sheets Menu**
1. Click menu → `📊 Application Tracker` → `🔎 Find by Email`
2. Enter recipient email
3. See full details in console

**Method 2: Apps Script Console**
```javascript
findApplicationByEmail('ce.recteur@ac-reunion.fr');
```

**Result:**
```
📍 FOUND APPLICATION:
Organization: Académie de La Réunion
Email: ce.recteur@ac-reunion.fr
Contact: Recteur
Sector: Education Nationale
Sent: 20/05/2026
Delivery Status: ✅ Delivered
Response Status: No Response
Response Date: 
Notes: 
```

---

## PART 5: ANALYTICS & REPORTS

### View Analytics Dashboard

**Function:** `showApplicationAnalytics()`

**What you get:**
1. Total applications sent
2. Delivery rate (✅ Delivered / ❌ Bounced / ⏳ Pending)
3. Response rate (% of delivered emails with replies)
4. Breakdown by organization
5. Breakdown by sector

**How to access:**
- Menu → `📊 Application Tracker` → `📈 Show Analytics`
- Or run: `showApplicationAnalytics()`

**Sample output:**
```
=======================================================================
📊 JOB APPLICATION TRACKER — ANALYTICS DASHBOARD
=======================================================================

📈 OVERALL STATISTICS
Total Applications Sent: 16
✅ Delivered: 14 (87%)
❌ Bounced: 2 (13%)
⏳ Pending: 0 (0%)

📬 RESPONSE TRACKING
Replies Received: 3 (21% of delivered)
No Response Yet: 11
Meetings Scheduled: 1
Response Rate: 21%

🏢 BY ORGANIZATION
Académie de La Réunion
  Sent: 3 | Delivered: 3 (100%) | Responses: 1 (33%)

Région Réunion
  Sent: 1 | Delivered: 1 (100%) | Responses: 0 (0%)

CCI Réunion
  Sent: 1 | Delivered: 0 (0%) | Responses: 0 (0%)

=======================================================================
```

### Check for Duplicates

**Function:** `checkDuplicateApplications()`

**Why important:**
- Prevents sending same application twice
- Shows if you contacted same person multiple times

**How to use:**
- Menu → `📊 Application Tracker` → `🔍 Check Duplicates`

**Result if duplicates found:**
```
⚠️ FOUND 1 DUPLICATE APPLICATION

ce.recteur@ac-reunion.fr (Académie de La Réunion)
  First: Row 2 | Duplicate: Row 8
```

**Action if found:**
1. Check if intentional (follow-up vs duplicate)
2. If duplicate, delete row
3. Add note about follow-up if intentional

### Analyze Bounces

**Function:** `analyzeBounces()`

**What you get:**
- List of all bounced emails
- Grouped by domain
- Reason for bounce (when detected)

**How to use:**
- Menu → `📊 Application Tracker` → `❌ Analyze Bounces`

**Sample output:**
```
❌ BOUNCE ANALYSIS
Total Bounces: 2

By Domain:
contact@englishworkshop.re: 1 bounces
  - English Workshop (contact@englishworkshop.re)

formation@reunion.cci.fr: 1 bounces
  - CCI Réunion (formation@reunion.cci.fr)
```

**Action:**
1. Invalid domain? → Remove from future sends
2. Wrong email? → Research correct address
3. Temporary issue? → Retry in 1 week

---

## PART 6: DAILY WORKFLOW

### Morning Routine (5 min)

```
1. Open Google Sheet
2. Click: 📊 Application Tracker → 🔄 Scan Gmail & Update
   (Runs automatically, takes 30 sec)

3. Click: 📊 Application Tracker → 📈 Show Analytics
   (Check overnight responses)

4. Check "Response Status" column for changes
   - Any new replies? Mark with notes.
   - Anyone request meeting? Schedule it.
```

### When You Send New Application (1 min)

**Option 1: Via Script (if in Google Apps)**
```
Run: logApplicationManually('Org Name', 'email@org.com', ...)
```

**Option 2: Direct Entry**
```
Add row to tracker sheet manually:
- Date Sent: Today's date
- Organization: Company name
- Recipient Email: Copy from your sent email
- Subject: Copy from your sent email
```

**Option 3: Automatic (if via Gmail)**
```
Wait 5 minutes, then:
Click: 📊 Application Tracker → 🔄 Scan Gmail & Update
Script auto-detects and adds to tracker
```

### Weekly Routine (10 min)

```
Monday morning:
1. Scan Gmail for new applications (2 min)
2. View analytics (2 min)
3. Check "No Response" entries older than 7 days
   - Plan follow-up calls for these (3 min)
4. Review "Response Status" entries
   - Any meetings to confirm? (3 min)
```

### Monthly Routine (15 min)

```
First of month:
1. Export data to CSV (see Part 7)
2. Review all bounced emails
3. Research correct addresses for bounces
4. Update tracker with verified addresses
5. Plan next campaign round
```

---

## PART 7: EXPORT & REPORTING

### Export to CSV

**Function:** `exportTrackerAsCSV()`

**How to use:**
- Menu → `📊 Application Tracker` → `📥 Export to CSV`
- Or run: `exportTrackerAsCSV()`

**Result:**
- CSV data prints in console
- Copy all text
- Paste into Excel or Numbers
- Save as: `Job_Applications_2026-05-20.csv`

**Use for:**
- Backup
- Analysis in Excel
- Sharing with advisors
- Record keeping

### Create Monthly Report

**Suggested template:**

```
═══════════════════════════════════════════
MONTHLY REPORT — May 2026
═══════════════════════════════════════════

STATISTICS
├─ Total sent this month: 8
├─ Total overall: 16
├─ Delivery success: 87% (14/16)
├─ Response rate: 21% (3/14)
└─ Meetings scheduled: 1

RESULTS
├─ Académie de La Réunion — Meeting scheduled (Recteur)
├─ Air Austral — Warm response, follow-up call sent
└─ CCI Réunion — No response yet

NEXT STEPS
├─ Follow up with 11 pending (7+ days old)
├─ Research correct email for 2 bounced
├─ Plan Round 2: CCI + Private sector
└─ Prepare meeting for Académie (date: 30/05)
```

---

## PART 8: INTERPRETATION GUIDE

### What's a Good Response Rate?

```
Cold outreach: 5-10% response rate
Warm outreach: 15-30% response rate
Your target: 20%+ (you're using verified warm contacts)
```

### What if Delivery Rate is Low?

```
Below 85%: 
├─ Review bounce analysis
├─ Check if domains invalid (research correct addresses)
└─ Consider if contact info is stale

Below 95%:
├─ Normal (some addresses change)
├─ Update bad addresses for next batch
└─ No major concern
```

### What if Response Rate is 0% After 14 Days?

```
Options:
1. Check if email actually delivered (delivery status)
2. Call organization instead
3. Try different contact person
4. Research if organization hiring
5. Check if emails went to spam
```

### How to Use Data for Next Campaign

```
Round 1: 5 verified applications (seed data)
Round 2: 8 new applications (expand from good sectors)
Round 3: 5 private sector (based on Round 1 response)

Use analytics to:
├─ Identify best-responding sectors
├─ Skip low-response organizations
├─ Focus on "warm leads" from responses
└─ Build reputation in successful sectors
```

---

## PART 9: TROUBLESHOOTING

### Issue: "Authorization required" error

**Cause:** First run, Gmail access not authorized

**Solution:**
1. Run any function
2. Click "Review permissions"
3. Select your Google account
4. Click "Allow"
5. Try again

### Issue: Script finds 0 emails

**Cause:** Gmail search pattern doesn't match your subject lines

**Solution:**
1. Check your actual sent email subjects
2. Edit line 22-27 with your patterns:
   ```javascript
   const EMAIL_SUBJECT_PATTERNS = [
     'YOUR ACTUAL SUBJECT WORD',
     'ANOTHER WORD YOU USE'
   ];
   ```
3. Run again

### Issue: Organization name shows as domain (ac-reunion.fr)

**Cause:** Subject line doesn't contain organization name

**Solution:**
1. Edit tracker sheet column B manually
2. Replace with full organization name
3. Script will use corrected name for future analytics

### Issue: Can't see menu items

**Cause:** Apps Script not saved properly

**Solution:**
1. Reload Google Sheet (F5)
2. Wait 3 seconds
3. Menu should appear
4. If not, save script again

### Issue: "Duplicate sheet name" error

**Cause:** Tracker sheet already exists

**Solution:**
- Script will use existing sheet
- Click OK
- Continue normally

---

## PART 10: QUICK REFERENCE

### Most Used Functions

```javascript
// Auto-scan Gmail
scanGmailApplications();

// Show dashboard
showApplicationAnalytics();

// Add manual entry
logApplicationManually('Org', 'email@org.com', 'Contact', 'Sector', 'Subject', 'Round');

// Mark response
markApplicationResponse('email@org.com', 'Reply Received', 'Notes');

// Find application
findApplicationByEmail('email@org.com');

// Check duplicates
checkDuplicateApplications();

// See bounce analysis
analyzeBounces();

// Export data
exportTrackerAsCSV();
```

### Target Numbers

```
After 1 month:
├─ 20-30 applications sent
├─ 85%+ delivery success
├─ 15%+ response rate
└─ 1-2 meetings scheduled

After 3 months:
├─ 50-75 applications sent
├─ 80%+ delivery success
├─ 15%+ response rate
└─ 5-10 meetings scheduled
```

---

*Last updated: May 20, 2026*
*For support: Check console logs (Ctrl+` in Apps Script)*
