# AUTONOMOUS CAMPAIGN ENGINE v4.0 — Setup Guide

**One script. Runs in background. Sends personalized emails. Reports to you. No Google Sheets.**

---

## WHAT THIS SCRIPT DOES (Every 48 Hours)

```
1. Discovers contacts from:
   ├─ 15 curated verified contacts (always available, no API needed)
   ├─ France Travail API (job offers with email, 974 region)
   ├─ La Bonne Boite API (warm hiring companies, 974 region)
   ├─ Indeed RSS feed (latest job postings)
   └─ Google Custom Search (LinkedIn decision-makers proxy)

2. Filters out:
   └─ Anyone you've already emailed (reads your Gmail Sent folder)

3. Generates personalized email per sector:
   ├─ Education → education-focused message
   ├─ Aviation → ICAO/aéronautique message
   ├─ Hôtellerie → VIP service + 18 years Sydney experience
   ├─ Santé → medical English + OPCO Santé
   ├─ Commerce → Business English + CPF
   └─ Government → institutional + CNFPT

4. Sends up to 5 emails with:
   ├─ CV attached (from your Google Drive)
   ├─ Motivation letter attached (from your Google Drive)
   └─ Random 35-60 second pause between emails

5. Saves results to Gmail Drafts:
   └─ "📊 CAMPAIGN RUN — DD/MM/YYYY" → full JSON report

6. Sends you a notification email:
   └─ Subject: "✅ Campaign Engine — Run Complete — X emails sent"
   └─ Tells you: who was contacted, when, success/failure
```

---

## SETUP: STEP BY STEP

### Step 1: Deploy Script (3 min)

```
1. Open Google Sheet (new or existing)
2. Extensions → Apps Script
3. Create new project named: "Campaign Engine v4"
4. DELETE the default empty function
5. Paste entire content of AUTONOMOUS_CAMPAIGN_ENGINE_v4.gs
6. Save (Ctrl+S)
```

### Step 2: Configure Your Drive File IDs (1 min)

Find these lines at the top:
```javascript
CV_FILE_ID:         '1T1OLQScV_lWZIkbDI1O9rrVUsVo7qiKG',
MOTIVATION_FILE_ID: '15H-dnTSWZ_bnFrxR1jLvZD7XfMZy2nuB',
```

**Verify your file IDs are correct:**
1. Open your CV in Google Drive
2. URL = `drive.google.com/file/d/[FILE_ID]/view`
3. Copy the ID between `/d/` and `/view`
4. Paste as `CV_FILE_ID`
5. Repeat for motivation letter

### Step 3: Test Attachments (1 min)

Run function: `checkAPIStatus()`

You should see:
```
CV Drive File ID:         1T1OLQScV_lWZIkbDI1O9rrVUsVo7qiKG
Motivation Drive File ID: 15H-dnTSWZ_bnFrxR1jLvZD7XfMZy2nuB
```

If it shows errors → verify the file IDs.

### Step 4: Install Trigger (1 min) ← THE IMPORTANT STEP

```
1. In Apps Script
2. Click Run (▶) dropdown
3. Select function: installTrigger
4. Click Run
5. Accept permissions when prompted
```

You will see:
```
✅ Trigger installed. Engine runs every 48 hours automatically.
📧 You will receive a notification email after each run.
```

**That's it. The engine now runs automatically every 48h.**

You don't need to do anything else. Close Apps Script and forget it.

---

## OPTIONAL: API KEYS (For Auto-Discovery)

Without API keys, the engine uses **15 verified curated contacts** — this works fine.

With API keys, it also discovers **new contacts automatically** from job boards.

### France Travail API (Free — 10 min setup)

**What you get:** Real job offers in 974 with contact emails + warm hiring companies

**How to get:**
1. Go to: https://francetravail.io/data/api
2. Click "S'inscrire" (register free)
3. Fill in registration form
4. Confirm email
5. Create a new application
6. Add these APIs to your app:
   - "Offres d'emploi v2"
   - "La Bonne Boite v1"
7. Copy your `client_id` and `client_secret`

**Add to script:**
```javascript
FT_CLIENT_ID:     'copy_your_client_id_here',
FT_CLIENT_SECRET: 'copy_your_client_secret_here',
```

### Google Custom Search (Free — 10 min setup)

**What you get:** LinkedIn-style decision-maker search results (name, role, company)

**How to get:**
1. Go to: https://programmablesearchengine.google.com
2. Click "Add" → Create new search engine
3. Under "What to search": select "Search the entire web"
4. Name it: "Job Search Engine"
5. Copy the **Search Engine ID** (looks like: `a1b2c3d4e5:xxxxx`)

6. Go to: https://console.cloud.google.com
7. APIs & Services → Library → Search for "Custom Search JSON API"
8. Enable it
9. APIs & Services → Credentials → Create API Key
10. Copy the API key

**Add to script:**
```javascript
GOOGLE_CSE_ID:  'paste_your_search_engine_id',
GOOGLE_API_KEY: 'paste_your_api_key',
```

**Free tier:** 100 searches/day (more than enough)

---

## RUNNING WITHOUT API KEYS (Immediate Start)

The engine works perfectly without any API keys.

Without keys, per 48h cycle:
- Reads 15 curated verified contacts
- Filters ones already contacted
- Sends 5 personalized emails max
- Reports results to you

This will cover your full database of 15 in 3 cycles (6 days).

After 15, add API keys to discover new contacts automatically.

---

## AFTER INSTALLATION: WHAT TO EXPECT

### Hour 0: Installation
```
You run: installTrigger()
Engine: ✅ Trigger installed.
```

### Hour 0-48: First waiting period
```
Engine runs automatically.
You will receive an email: "✅ Campaign Engine — Run Complete"
Check: Who was contacted, any failures
```

### Hour 48: First run notification email
```
From: Campaign Engine — Sourov DEB
To: sourovdeb.is@gmail.com
Subject: ✅ Campaign Engine — Run Complete — 5 emails sent — 20/05/2026

Bonjour Sourov,

Le moteur de campagne automatique vient de terminer son cycle.

📅 Date du cycle : 20/05/2026 13:41:57

📊 RÉSULTATS :
  Contacts découverts : 15
  Déjà contactés (filtrés) : 0
  Envoyés avec succès : 5
  Échecs : 0

📧 ENVOYÉS CE CYCLE :
  1. Académie de La Réunion — dafco.secretariat@ac-reunion.fr (education)
  2. Région Réunion — formation@regionreunion.com (government)
  3. Air Austral — formation@air-austral.com (aviation)
  4. Blue Margouillat Hôtel — contact@blue-margouillat.com (hotellerie)
  5. Koz'Anglais — contact@kozanglais.com (education)

📝 Rapport complet sauvegardé dans vos Brouillons Gmail.

Prochain cycle automatique dans 48h.
```

### Hour 96: Second run notification
```
Same format.
New contacts (picks up where it left off).
Filters already-contacted addresses.
```

### Week 1-2: Expect responses
```
Some contacts reply → You will see in Gmail inbox.
Reply to them immediately (this is your hot lead).
```

---

## HOW DEDUPLICATION WORKS

**The engine never sends twice to same address.**

How:
1. Before every run, it reads your Gmail Sent folder
2. Extracts all email addresses you've ever sent to with CELTA/Formateur subject
3. Also reads tracker drafts from previous runs
4. Builds a SET of all contacted addresses
5. Removes them from discovered contacts
6. Only sends to addresses NOT in this set

**Result:** Zero duplicate sends, ever.

---

## MANAGING THE ENGINE

### Check Status
```
Run: getTriggerStatus()
→ "✅ Engine is ACTIVE — 1 trigger(s) running."
```

### Check API Status
```
Run: checkAPIStatus()
→ Shows which APIs are configured vs missing
```

### Run Manually Right Now
```
Run: runNow()
→ Executes same logic as automatic trigger
→ Sends 5 emails immediately
→ Sends you notification
```

### See All Past Results
```
Run: readAllReports()
→ Shows all campaign run reports from Gmail drafts
→ Shows who was contacted, when, success/failure
```

### See Cumulative Statistics
```
Run: showCumulativeStats()
→ Total sent across all runs
→ Breakdown by sector
→ Full list of everyone contacted
```

### Pause Engine (Temporary)
```
Run: removeTrigger()
→ Engine stops running automatically
→ Your data in Gmail remains safe
→ To restart: run installTrigger() again
```

### Permanently Stop Engine
```
1. Run: removeTrigger()
2. Engine stops.
3. Run installTrigger() whenever you want to restart.
```

---

## GMAIL DRAFTS STRUCTURE

The engine creates two types of drafts:

### Campaign Run Reports
```
Subject: "📊 CAMPAIGN RUN — 20/05/2026 13:41:57"
Content: Human-readable report + full JSON data

Location: Gmail → Drafts
```

### Sent History Log
```
Subject: "📋 SENT HISTORY — 20/05/2026"
Content: JSON array of all sent contacts (for deduplication)

Location: Gmail → Drafts
```

**Do NOT delete these drafts** — the engine uses them for deduplication.

To back them up: Go to Gmail → Drafts → Label them with "CampaignTracker"

---

## TROUBLESHOOTING

### Error: "Cannot load Drive files"
```
Cause: Wrong file ID in CONFIG
Fix: Verify file IDs are correct
   → Open file in Drive → Copy ID from URL → Paste in CONFIG
```

### Error: "Authorization required"
```
Cause: First run — Gmail not authorized
Fix: 
1. Run any function
2. Click "Review permissions"
3. Select your Google account
4. Click "Allow"
5. Run installTrigger() again
```

### No notification email received after 48h
```
Check:
1. Gmail Drafts → any "📊 CAMPAIGN RUN" drafts? → Engine ran but email failed
2. Apps Script → Run getTriggerStatus() → Is trigger active?
3. Apps Script → View → Executions → Any errors?
```

### Engine sends to same people twice
```
This should NOT happen due to deduplication.
If it does:
1. Run: showCumulativeStats()
2. Check if drafts are intact (don't delete them!)
3. Run: getAllContactedEmails() → check the set
```

### Indeed RSS returns 0 contacts
```
Normal — Indeed doesn't always have emails in job listings.
Engine falls back to curated contacts.
```

---

## EXPECTED OUTCOMES

### Week 1 (Curated contacts, 15 total)
```
Run 1 (Day 0): 5 personalized emails sent
Run 2 (Day 2): 5 personalized emails sent
Run 3 (Day 4): 5 personalized emails sent
→ All 15 curated contacts reached after 6 days
→ Expect: 0-2 replies in week 1
```

### Week 2-3 (With API keys)
```
Engine auto-discovers new contacts from France Travail + Indeed
Adds them to queue
Sends 5/cycle
→ Expect: 1-3 more replies
→ Total: 2-5 warm leads
```

### Month 1+
```
Engine discovers 5-10 new contacts per 48h cycle
Sends 5/cycle
Grows your list automatically
→ Target: 3-5 meetings booked
→ Target: 1-2 contracts
```

---

## CONFIGURATION REFERENCE

```javascript
const CONFIG = {
  MY_EMAIL:           'sourovdeb.is@gmail.com',    // Your notification email
  MY_NAME:            'Sourov DEB',
  MY_PHONE:           '06 93 84 61 68',
  MY_LOCATION:        'Saint-Pierre, La Réunion (97410)',
  
  CV_FILE_ID:         'YOUR_CV_FILE_ID',           // Google Drive file ID
  MOTIVATION_FILE_ID: 'YOUR_MOTIVATION_FILE_ID',   // Google Drive file ID
  
  FT_CLIENT_ID:       'YOUR_FRANCE_TRAVAIL_ID',    // Optional: France Travail API
  FT_CLIENT_SECRET:   'YOUR_FRANCE_TRAVAIL_SECRET',// Optional: France Travail API
  
  GOOGLE_CSE_ID:      'YOUR_CSE_ID',               // Optional: Google Search
  GOOGLE_API_KEY:     'YOUR_API_KEY',              // Optional: Google Search
  
  MAX_EMAILS_PER_RUN: 5,      // Max emails per 48h cycle
  MIN_DELAY_MS:       35000,  // Min pause between emails (ms)
  MAX_DELAY_MS:       60000,  // Max pause between emails (ms)
};
```

---

## LINKEDIN NOTE

**LinkedIn does NOT allow automated scraping.**

The script uses Google Custom Search as a proxy:
- Searches `site:linkedin.com [role] [location]`
- Extracts name, role, company from search snippets
- Does NOT access LinkedIn directly

**This is Google's public index of LinkedIn, not LinkedIn's API.**

For best results with LinkedIn contacts:
1. Visit linkedin.com manually
2. Search: `responsable formation anglais Réunion`
3. Find person → get their institutional email from their company website
4. Add to CONFIG curated contacts list manually

---

## THE ENGINE IN 30 SECONDS

```
1. installTrigger() → ENGINE RUNNING

2. Every 48h automatically:
   ├─ Discovers new contacts (France Travail, Indeed, curated)
   ├─ Skips already-contacted (Gmail dedup)
   ├─ Sends 5 personalized sector-specific emails
   ├─ Attaches CV + letter from Drive
   └─ Emails you a full report

3. You receive notification:
   "5 emails sent to: [org 1], [org 2]... [date]"

4. Check Gmail Drafts for detailed JSON report

5. Done. Repeat in 48h.
```

**One command to start. Runs forever. Reports everything.**

---

*Engine v4.0 — May 20, 2026*  
*Zero Google Sheets. Gmail Drafts only. Fully autonomous.*
