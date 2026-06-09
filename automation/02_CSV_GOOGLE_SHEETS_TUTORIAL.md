# CSV + Google Apps Script — Complete Beginner Tutorial
## "I never understood how this works" — Explained from scratch

---

## What is a CSV file? (And why should you care?)

CSV stands for **Comma-Separated Values**.

Think of it like this: you have a table of information — blog post titles, their content, categories. Instead of keeping it in a complex database, a CSV file stores it as plain text where **each line is one row** and **commas separate the columns**:

```
Title,Content,Category,Status
Day 32 Listening,"<p>Today we practise listening...</p>",ELT,draft
Grammar Basics,"<p>Subject-verb agreement...</p>",Grammar,future
```

That's it. A CSV is just a text file disguised as a spreadsheet.

**Why this matters for you:** You can edit it in Google Sheets (which looks like Excel), and scripts can read it automatically — no database, no coding knowledge required.

---

## What is Google Sheets in this context?

Google Sheets IS a CSV editor with a pretty interface. When you type in cells:
- Each **row** = one blog post
- Each **column** = one field (title, content, category...)

Google Sheets adds one superpower: **Google Apps Script** — JavaScript code that lives inside your spreadsheet and can talk to the internet.

---

## What is Google Apps Script?

Imagine you could hire a tiny robot that lives inside your Google account. This robot:
- Can read your spreadsheet rows
- Can send HTTP requests to WordPress (or any website)
- Can be set on a timer ("check the sheet every hour")
- Never sleeps, never forgets, costs nothing

That robot is **Google Apps Script**.

You write instructions for the robot in JavaScript. You don't need a server, hosting, or a terminal. It all runs inside Google's servers.

---

## How the Data Flows — Step by Step

```
┌─────────────────────────────────────────────┐
│  YOU: Type a blog post title in row 2       │
│  Column A = Title                           │
│  Column B = Content (HTML)                  │
│  Column C = Category                        │
│  Column E = Status: "draft"                 │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  APPS SCRIPT runs every hour (auto trigger) │
│  It reads each row of your sheet            │
│  Skips rows where Status = "published"      │
│  For each new row: builds a JSON payload    │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  HTTP POST request sent to WordPress        │
│  URL: https://yourdomain.com/wp-json/...    │
│  Headers: { X-Sourov-Key: your-api-key }    │
│  Body: { title, content, category, tags }   │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  WordPress creates the post                 │
│  Returns: { post_id: 42, status: "draft" }  │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│  Apps Script writes "published" back        │
│  into column E of that row                  │
│  So it won't publish the same post twice    │
└─────────────────────────────────────────────┘
```

This entire loop runs **automatically every hour** after you set it up once.

---

## Step-by-Step Setup (No coding background needed)

### Step 1: Create Your Publishing Spreadsheet

1. Go to **sheets.google.com** → Create new spreadsheet
2. Rename it: `WordPress Publishing Queue`
3. Create two tabs at the bottom:
   - Click the `+` button → name it **Queue**
   - Click `+` again → name it **Topics**

### Step 2: Set Up the Queue Tab

In the **Queue** tab, type these headers in row 1:

| A | B | C | D | E | F | G | H | I | J |
|---|---|---|---|---|---|---|---|---|---|
| Title | Content | Category | Tags | Status | Date | SEO Title | Meta Desc | AI Enhance | Result |

Row 2 onwards = your posts. Example:
- **A2:** `Day 32 – Listening Skills`
- **B2:** `<p>Today we explore listening strategies...</p>`
- **C2:** `ELT Masterclass`
- **D2:** `listening, ELT, CELTA`
- **E2:** `draft`
- **I2:** `yes` (DeepSeek will auto-improve SEO)

### Step 3: Open the Script Editor

1. In your spreadsheet: click **Extensions** in the menu bar
2. Click **Apps Script**
3. A new tab opens — this is your code editor
4. Delete the default `function myFunction(){}` text
5. Paste the entire script from `scripts/sheet_publisher.gs`

### Step 4: Store Your API Keys (Important!)

Never type real API keys directly in the code. Instead:

1. In the script editor, find the `setKeys()` function
2. Replace the placeholder values with your real keys:
   ```javascript
   function setKeys() {
     PropertiesService.getScriptProperties().setProperties({
       'DEEPSEEK_KEY': 'sk-your-actual-key',  // ← your real key
       'WP_KEY': 'your-wp-plugin-key',
       'WP_URL': 'https://sourovdeb.com'
     });
   }
   ```
3. Click the **Run** button (▶) at the top
4. Google will ask for permissions — click **Allow**
5. **After it runs:** delete the key values from the code and save
   (The keys are now stored safely in Google's property store)

### Step 5: Test Manually

1. Add one row of data to your Queue sheet
2. In the script editor, select `publishFromSheet` from the function dropdown
3. Click **Run** (▶)
4. Check the **Execution log** at the bottom — you should see "Done — 1 posts sent."
5. Check your WordPress admin → Posts → Drafts

### Step 6: Set Up the Automatic Timer

This makes everything run without you:

1. In the script editor, select `setupHourlyTrigger` from the dropdown
2. Click **Run** (▶)
3. Done. The script now runs every hour automatically.

To verify: Click the **clock icon** (Triggers) in the left sidebar. You should see `publishFromSheet` listed.

---

## What Happens When AI Enhancement Is On

When column I = `yes`, the script calls DeepSeek API before publishing:

1. Sends your title + first 400 chars of content to DeepSeek
2. DeepSeek returns: better SEO title, meta description, relevant tags, correct category
3. These are added to the post automatically
4. You didn't have to think about SEO at all

Cost per post: about $0.001 (one tenth of a cent).

---

## Common Mistakes and Fixes

| Problem | Cause | Fix |
|---|---|---|
| "No Queue tab found" | Tab not named exactly "Queue" | Rename tab to exactly `Queue` (capital Q) |
| Posts send but nothing appears in WP | Wrong API key | Re-run `setKeys()` with correct key |
| Script stops after first post | Rate limit hit | Increase `Utilities.sleep(2000)` to `3000` |
| Same post published twice | Status not updating | Check sheet is not read-only |
| "Authorization required" error | Permissions not granted | Run any function manually once and click Allow |
| Date not scheduling correctly | Wrong date format | Use ISO format: `2026-06-15T09:00:00` |

---

## Using the Topics Tab (AI-Written Posts)

This lets you generate entire posts from just a topic idea:

1. In the **Topics** tab, type topics in column A:
   ```
   A: Topic
   A2: 5 common English pronunciation mistakes
   A3: How to teach phrasal verbs effectively
   A4: CELTA lesson planning tips for beginners
   ```
2. Run `generateFromTopics()` in the script editor
3. DeepSeek writes full 600-word posts for each topic
4. Posts are added to the Queue tab automatically
5. On the next hourly run, they are sent to WordPress

---

## The Complete Data Flow in Plain English

> You write a topic in a Google Sheet cell.  
> An hour later (or immediately if you run manually), a script reads that cell.  
> The script optionally asks an AI to improve the SEO.  
> The script sends the post to your WordPress site.  
> The post appears as a draft in your WP admin.  
> You open WP admin, glance at it, click Publish.  
> Done. No terminal. No code. Just your writing.

That is the entire system.
