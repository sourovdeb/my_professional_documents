# CSV + Google Apps Script: The Complete Beginner's Tutorial
## How to Automate WordPress Publishing Without Touching Code Daily

> **Who this is for:** Someone who writes but doesn't code. You want to fill a spreadsheet and have WordPress publish automatically. This tutorial explains every single concept from scratch.

---

## PART 1: Understanding CSV — What It Is and Why It Matters

### What is CSV?

CSV stands for **Comma-Separated Values**. It is the simplest possible database format — just a text file where each line is a row and each value is separated by a comma.

**Example CSV file:**
```
Title,Content,Category,Status
Day 32 - Listening,"<p>Listening is...</p>",ELT,draft
Day 33 - Grammar,"<p>Grammar rules...",Grammar,future
```

When you open this in Excel or Google Sheets, it becomes a proper table:

```
| Title            | Content              | Category | Status |
|------------------|----------------------|----------|--------|
| Day 32 Listening | <p>Listening is...</p> | ELT    | draft  |
| Day 33 Grammar   | <p>Grammar rules... | Grammar  | future |
```

**Why CSV matters for you:**
- It's the universal language between spreadsheets and scripts
- Every program (Python, JavaScript, Apps Script) can read CSV
- You write in the spreadsheet → script reads the CSV → WordPress gets the post
- No coding required after setup

### What Does Google Sheets Have to Do With This?

Google Sheets IS a visual CSV editor. When you type data into cells, Sheets is storing it exactly like CSV — rows and columns of data. Your Apps Script reads those rows just like reading a CSV file.

**The mental model:**
```
You type here          Apps Script reads this      WordPress gets this
[Google Sheets]   →   [Your JavaScript code]    →  [Blog post published]
     ↑                         ↑                          ↑
  Your job              Runs automatically          Happens silently
  (just write)          (time trigger = cron)       (no action needed)
```

---

## PART 2: What Is Google Apps Script?

### In Plain Language

Google Apps Script is **Google's built-in automation engine**. It is:
- JavaScript (a programming language) that runs on Google's servers
- Free to use (no server needed)
- Connected to all Google services (Sheets, Gmail, Drive, Calendar)
- Can make HTTP requests to ANY website — including your WordPress

Think of it as a robot that lives inside your Google account, waiting for you to tell it what to do.

### How to Open Apps Script

From your Google Sheet:
1. Click **Extensions** in the top menu
2. Click **Apps Script**
3. A new tab opens — this is your robot's brain

You will see something like:
```javascript
function myFunction() {
  // Your code goes here
}
```

That `function myFunction()` is like naming a task. When you tell the robot "run myFunction", it runs everything between the `{` and `}`.

---

## PART 3: Your Sheet Structure — The Publishing Queue

### Step 1: Set Up the Sheet

Create a Google Sheet. Name the first tab (the tab at the bottom): **Queue**

Set up these column headers in Row 1:

```
A1: Title
B1: Content  
C1: Category
D1: Tags
E1: Status
F1: ScheduleDate
G1: SEO_Title
H1: Meta_Description
I1: Published_At
```

### Step 2: Understand What Each Column Does

| Column | What to Put Here | Example |
|--------|-----------------|--------|
| A — Title | Your blog post title | `Day 32: The Art of Listening` |
| B — Content | The post body (can be plain text or HTML) | `<p>Listening is a skill...</p>` |
| C — Category | WordPress category name | `ELT Masterclass` |
| D — Tags | Comma-separated tags | `listening, pronunciation, CELTA` |
| E — Status | `draft`, `publish`, or `future` | `draft` |
| F — ScheduleDate | Only if Status=future | `2026-06-15T09:00` |
| G — SEO_Title | Title for search engines (under 60 chars) | `Day 32: Listening Skills for ELT` |
| H — Meta_Description | Description for Google (under 160 chars) | `Learn how to improve...` |
| I — Published_At | **Leave blank** — script fills this | (auto) |

### Step 3: Fill in Your First Row

Leave Row 1 as headers. Start filling from Row 2:

```
A2: Day 32 – The Art of Listening
B2: <p>Every language learner struggles with listening...</p>
C2: ELT Masterclass
D2: listening, comprehension, CELTA
E2: draft
F2: (leave blank)
G2: Day 32: Listening for ELT
H2: Discover proven techniques to improve your listening...
I2: (leave blank — script fills this)
```

---

## PART 4: The Apps Script Code — Line by Line

Now go to **Extensions → Apps Script** and paste this code. I'll explain every single line.

```javascript
// ============================================================
// WordPress Auto-Publisher from Google Sheets
// Reads the "Queue" sheet and sends new rows to WordPress
// ============================================================

// --- CONFIGURATION ---
// Replace with your actual values (store in Script Properties for security)
const WP_API = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
// Never put your API key in code — store it in Script Properties (see Part 5)

// ============================================================
// MAIN FUNCTION: publishFromSheet
// This is the function you will trigger with a time trigger
// ============================================================
function publishFromSheet() {
  
  // Step 1: Get the API key from secure storage (not hardcoded)
  const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  
  // Step 2: Open the spreadsheet and find the "Queue" tab
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  
  // Step 3: Read ALL data from the sheet (every row, every column)
  const rows = sheet.getDataRange().getValues();
  // rows is now an array like:
  // rows[0] = ['Title', 'Content', 'Category', ...]  ← header row
  // rows[1] = ['Day 32...', '<p>...</p>', 'ELT', ...]  ← first data row
  // rows[2] = ['Day 33...', '<p>...</p>', 'Grammar', ...]  ← second data row
  
  // Step 4: Loop through each row, starting from row 2 (index 1, skipping header)
  for (let i = 1; i < rows.length; i++) {
    
    // Extract each column from the current row
    const title       = rows[i][0];  // Column A
    const content     = rows[i][1];  // Column B
    const category    = rows[i][2];  // Column C
    const tags        = rows[i][3];  // Column D
    const status      = rows[i][4];  // Column E
    const schedDate   = rows[i][5];  // Column F
    const seoTitle    = rows[i][6];  // Column G
    const metaDesc    = rows[i][7];  // Column H
    const publishedAt = rows[i][8];  // Column I
    
    // SKIP this row if:
    // - Title is empty (blank row)
    // - Already published (we already handled it)
    if (!title || publishedAt) continue;
    
    // Step 5: Build the post object to send to WordPress
    const post = {
      title:            title,
      content:          content,
      category:         category || guessCategory(title, content),
      tags:             tags || suggestTags(title),
      status:           (status === 'future') ? 'future' : 'draft',
      seo_title:        seoTitle || title,
      meta_description: metaDesc || content.toString().substring(0, 155)
    };
    
    // Add schedule date only if status is 'future'
    if (status === 'future' && schedDate) {
      post.date = schedDate;
    }
    
    // Step 6: Send to WordPress
    const result = sendToWordPress(post, API_KEY);
    
    // Step 7: Mark as done in the sheet
    if (result && result.post_id) {
      // Write the publish timestamp in Column I
      sheet.getRange(i + 1, 9).setValue(new Date().toISOString());
      Logger.log('Published: ' + title + ' → ID: ' + result.post_id);
    } else {
      Logger.log('FAILED: ' + title + ' — ' + JSON.stringify(result));
    }
    
    // Pause 1.5 seconds between posts to avoid rate limiting
    Utilities.sleep(1500);
  }
  
  Logger.log('Batch complete.');
}

// ============================================================
// HELPER: sendToWordPress
// Makes the actual HTTP request to your WordPress REST API
// ============================================================
function sendToWordPress(postData, apiKey) {
  try {
    const response = UrlFetchApp.fetch(WP_API, {
      method: 'POST',
      headers: {
        'X-Sourov-Key':  apiKey,
        'Content-Type':  'application/json'
      },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true  // Don't crash on HTTP errors — handle them ourselves
    });
    
    const statusCode = response.getResponseCode();
    const body       = response.getContentText();
    
    if (statusCode === 200 || statusCode === 201) {
      return JSON.parse(body);
    } else {
      Logger.log('WP Error ' + statusCode + ': ' + body);
      return null;
    }
  } catch(e) {
    Logger.log('Network error: ' + e.toString());
    return null;
  }
}

// ============================================================
// HELPER: guessCategory
// Automatically assigns a category based on keywords
// ============================================================
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  
  if (text.includes('grammar') || text.includes('tense') || text.includes('verb'))
    return 'Grammar';
  if (text.includes('listen') || text.includes('pronunciation') || text.includes('phonics'))
    return 'Listening & Phonology';
  if (text.includes('celta') || text.includes('lesson plan') || text.includes('teach'))
    return 'CELTA';
  if (text.includes('speak') || text.includes('fluency') || text.includes('conversation'))
    return 'Speaking';
  if (text.includes('read') || text.includes('comprehension') || text.includes('text'))
    return 'Reading';
  if (text.includes('write') || text.includes('essay') || text.includes('paragraph'))
    return 'Writing';
    
  return 'ELT Masterclass';  // Default
}

// ============================================================
// HELPER: suggestTags
// Automatically suggests tags from the title
// ============================================================
function suggestTags(title) {
  const tagMap = {
    'grammar':      'grammar',
    'listening':    'listening',
    'pronunciation':'pronunciation',
    'speaking':     'speaking',
    'celta':        'CELTA',
    'elt':          'ELT',
    'phonics':      'phonics',
    'fluency':      'fluency',
    'vocabulary':   'vocabulary',
    'idiom':        'idioms',
    'writing':      'writing'
  };
  
  const words = title.toLowerCase().split(/\s+/);
  const found = [];
  
  for (const word of words) {
    if (tagMap[word] && !found.includes(tagMap[word])) {
      found.push(tagMap[word]);
    }
  }
  
  return found.join(',') || 'ELT';
}
```

---

## PART 5: Store Your API Key Securely

**Never put your API key directly in the code.** Here is how to store it safely:

1. In the Apps Script editor, click the **gear icon** (⚙️) in the left sidebar
2. Click **Script Properties**
3. Click **Add property**
4. Name: `WP_KEY`
5. Value: your API key (e.g., `0767044896thevenet_`)
6. Click **Save**

Now the code reads it with:
```javascript
const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
```

This key is stored securely in Google's system, not visible in your code.

---

## PART 6: Setting Up the Time Trigger (The "Cron Job")

A **time trigger** tells Apps Script: "Run this function automatically every X minutes/hours."

Without this, you'd have to manually click "Run" every time. With it, the script runs while you sleep.

### How to Set Up a Trigger

1. In Apps Script, click the **clock icon** (⏰) in the left sidebar
   - It says "Triggers"
2. Click **+ Add Trigger** (bottom right)
3. Fill in the settings:
   - **Which function to run:** `publishFromSheet`
   - **Which deployment:** `Head`
   - **Event source:** `Time-driven`
   - **Type of time trigger:** `Hour timer`
   - **Every:** `1 hour` (or every 30 mins, your choice)
4. Click **Save**
5. Google asks you to grant permissions — click **Allow**

Now every hour, Apps Script will:
1. Open your Google Sheet
2. Read the Queue tab
3. Find any rows without a Published_At date
4. Send them to WordPress as drafts
5. Mark them as published in the sheet

**You only write. Everything else is automatic.**

---

## PART 7: Understanding the Authorization (OAuth) Step

When you set up the trigger, Google shows an authorization screen. Here is what's happening:

**Why Google asks:** Apps Script needs permission to:
- Read your Google Sheets (to get the data)
- Make external HTTP requests (to call WordPress)
- Store data (the Script Properties)

**Is it safe?** Yes — this is your own Apps Script in your own Google account. You're authorizing yourself to access your own data.

**What to click:** "Allow". This is normal.

---

## PART 8: Testing Your Setup

### Manual Test First

Before setting up the trigger, test manually:

1. Fill in row 2 of your Queue sheet with test data
2. In Apps Script, click **Run** → `publishFromSheet`
3. Click **Execution log** to see what happened

If successful, you'll see:
```
[INFO] Published: Day 32 – The Art of Listening → ID: 1234
[INFO] Batch complete.
```

If there's an error, you'll see:
```
[ERROR] WP Error 401: {"message": "Unauthorized"}
```

### Common Errors and Fixes

| Error | Meaning | Fix |
|-------|---------|-----|
| `401 Unauthorized` | Wrong API key | Check WP_KEY in Script Properties |
| `404 Not Found` | Wrong WP_API URL | Verify your WordPress URL |
| `TypeError: Cannot read property` | Empty cell in sheet | Check that title isn't blank |
| `Exception: Request failed` | Network timeout | WordPress might be down; try again |
| Script runs but nothing happens | Status column says 'published' | Clear column I to re-test |

---

## PART 9: Your Daily Workflow (After Setup)

Once everything is configured, your daily routine is:

**Morning (5 minutes):**
1. Open your Google Sheet
2. Add a new row with your post title, content, category, tags
3. Set Status to `draft` (or `future` + date for scheduling)
4. Close the tab

**One hour later (automatic):**
- Script runs
- Your post appears in WordPress drafts
- You get a clean post ready to review

**Review (5 minutes, optional):**
- Open WordPress admin
- Check the draft
- Click Publish when satisfied

**Total effort:** 10 minutes per post. Zero repetitive tasks.

---

## PART 10: Fixing WordPress Categories and Tags Automatically

Your WordPress might have messy categories/tags from manual publishing. The script above uses `guessCategory()` to assign proper categories automatically.

### To Fix Existing Posts via Script

Add this function to your Apps Script:

```javascript
function fixExistingPostCategories() {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  const WP_BASE = 'https://sourovdeb.com/wp-json/sourov/v1';
  
  // Get all drafts
  const r = UrlFetchApp.fetch(WP_BASE + '/scheduled', {
    headers: { 'X-Sourov-Key': API_KEY }
  });
  const posts = JSON.parse(r.getContentText());
  
  for (const post of posts) {
    const correctCategory = guessCategory(post.title, post.excerpt || '');
    
    // Update the post with correct category
    UrlFetchApp.fetch(WP_BASE + '/post/' + post.id, {
      method: 'PATCH',
      headers: { 'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify({ category: correctCategory })
    });
    
    Logger.log('Fixed: ' + post.title + ' → ' + correctCategory);
    Utilities.sleep(500);
  }
}
```

---

## Summary: Why This Works So Well

| Feature | Benefit |
|---------|--------|
| Google Sheets as database | You already know how to use it |
| No-code daily use | Just type in cells and save |
| Time trigger | Runs without you doing anything |
| Auto-categorize | No more wrong categories |
| Auto-tags | Consistent tagging across all posts |
| Draft mode default | Safe — nothing publishes without your review |
| Error logging | You can see exactly what went wrong |
| Free to run | Google's servers, Google's cost |

---

*Tutorial version: June 2026 | Designed for sourovdeb.com publishing workflow*
