# Complete Beginner's Guide: CSV + Google Apps Script for WordPress Publishing

> **Who this is for:** You have never written code. You use Google Docs and Gmail daily. You want blog posts to publish automatically without touching WordPress every day.

---

## Part 1: What Are These Things?

### What Is CSV?

CSV stands for **Comma Separated Values**. It is the simplest possible way to store table data.

Imagine you have a table:

```
Title               | Category    | Tags              | Status
Day 32 Listening    | ELT         | listening, CELTA  | draft
Day 33 Grammar      | Grammar     | grammar, verbs    | ready
```

In CSV format, that same table looks like this:

```
Title,Category,Tags,Status
Day 32 Listening,ELT,"listening, CELTA",draft
Day 33 Grammar,Grammar,"grammar, verbs",ready
```

That is literally all CSV is — data with commas between each column, one row per line.

**Why does this matter?** Because every website, every programming language, and every database in the world can read CSV. It is the universal language of data. When Google Sheets talks to WordPress, it uses this format.

### What Is Google Sheets?

Google Sheets is Google's free online spreadsheet (like Microsoft Excel). When you type data into cells and columns, you are creating CSV data — Sheets just gives it a nice visual interface.

The connection: **Click File → Download → Comma Separated Values (.csv) in any Google Sheet and you get the raw CSV data.**

### What Is Google Apps Script?

Google Apps Script is **JavaScript (a programming language) that runs inside Google products** — Gmail, Sheets, Docs, Drive, Calendar.

Think of it as a robot that lives inside your Google account:
- You give it instructions written in JavaScript
- It follows those instructions automatically on a schedule you set
- It can read your spreadsheet, call websites, send emails
- You do NOT need to install anything — it runs in your browser at **script.google.com**

### How They Work Together

```
You write a post → type it into Google Sheets (your queue)
                           ↓
        Apps Script runs every hour automatically
                           ↓
   For each row marked "ready", it sends data to WordPress
                           ↓
         WordPress creates the blog post
                           ↓
       Script marks the row "published" → won't repeat
```

After setup, **you only ever touch the spreadsheet**. The robot handles everything else.

---

## Part 2: Setting Up Your Publishing Spreadsheet

### Step 1: Create a New Google Sheet

1. Go to **sheets.google.com** (sign in with your Google account)
2. Click the large **+** button (Blank spreadsheet)
3. Click the name "Untitled spreadsheet" at the top and rename it: `WordPress Publishing Queue`

### Step 2: Create the Column Headers

Click cell **A1** (top-left cell). Type these headers, one per cell going right:

```
A1: Title
B1: Content
C1: Category
D1: Tags
E1: Status
F1: Schedule Date
G1: SEO Title
H1: Meta Description
```

**Make the header row bold:** Select row 1, press Ctrl+B.

**What each column does:**

| Column | Purpose | Example |
|--------|---------|----------|
| **Title** | The blog post title | `Day 32 – Active Listening` |
| **Content** | Full post text (HTML OK, plain text OK) | `<p>Listening is the most...</p>` |
| **Category** | ONE category from your WordPress site | `ELT Masterclass` |
| **Tags** | Comma-separated tag list | `listening, CELTA, pronunciation` |
| **Status** | What to do with this post | `draft`, `ready`, or `future` |
| **Schedule Date** | Only for scheduled posts | `2026-06-20T09:00:00` |
| **SEO Title** | Browser tab title (optional) | `Day 32: Active Listening Guide` |
| **Meta Description** | Google search snippet (155 chars max) | `Learn active listening techniques...` |

### Step 3: Name Your Sheet Tab "Queue"

At the bottom of the screen, you see a tab named "Sheet1". Right-click it → **Rename** → type `Queue`.

This is important — the script looks for a tab named exactly "Queue".

### Step 4: Add Your First Test Row

In row 2 (under the headers), add:

```
A2: TEST POST — Delete After Checking
B2: <p>This is a test post. If you see this in WordPress drafts, automation is working!</p>
C2: ELT Masterclass
D2: test, automation
E2: ready
```

Leave F2, G2, H2 empty for now.

---

## Part 3: Writing the Google Apps Script

### Step 1: Open the Script Editor

Inside your spreadsheet:
1. Click **Extensions** in the top menu bar
2. Click **Apps Script**
3. A new browser tab opens — this is the script editor

You'll see some existing code like `function myFunction() { }`. **Select all of it and delete it.**

### Step 2: Paste the Complete Script

Copy everything between the lines below and paste it into the editor:

```javascript
// ============================================================
// WordPress Auto-Publisher from Google Sheets
// Developed for sourovdeb.com | ELT Publishing System
// ============================================================

// === EDIT THESE TWO LINES ONLY ===
var WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
var WP_API_KEY = '0767044896thevenet_';
// ==================================

/**
 * MAIN FUNCTION
 * Reads every row in the "Queue" tab.
 * Publishes rows where Status is "ready", "draft", or "future".
 * Marks published rows with "published" status.
 */
function publishFromSheet() {
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = spreadsheet.getSheetByName('Queue');

  if (!sheet) {
    Logger.log('ERROR: No sheet named "Queue" found. Rename your tab.');
    return;
  }

  var data = sheet.getDataRange().getValues();
  var publishedCount = 0;

  // Start from row 2 (index 1) — row 1 is headers
  for (var i = 1; i < data.length; i++) {
    var row    = data[i];
    var title  = row[0];  // Column A
    var content = row[1]; // Column B
    var category = row[2]; // Column C
    var tags   = row[3];  // Column D
    var status = row[4];  // Column E
    var date   = row[5];  // Column F
    var seoTitle = row[6]; // Column G
    var metaDesc = row[7]; // Column H

    // Skip empty rows and already-published rows
    if (!title) continue;
    var statusStr = String(status).toLowerCase().trim();
    if (statusStr === 'published' || statusStr === 'done' || statusStr === 'skip') continue;
    if (statusStr !== 'ready' && statusStr !== 'draft' && statusStr !== 'future' && statusStr !== 'publish') continue;

    // Auto-fill category and tags if empty
    if (!category) category = guessCategory(String(title), String(content));
    if (!tags) tags = suggestTags(String(title));

    // Build the post object
    var post = {
      title: String(title),
      content: String(content),
      category: String(category) || 'ELT Masterclass',
      tags: String(tags) || 'ELT',
      status: (statusStr === 'future') ? 'future' : 'draft',
      seo_title: seoTitle ? String(seoTitle) : String(title),
      meta_description: metaDesc ? String(metaDesc).substring(0, 155) : String(content).replace(/<[^>]+>/g, '').substring(0, 155)
    };

    // Add scheduled date if status is future
    if (statusStr === 'future' && date) {
      try {
        post.date = Utilities.formatDate(
          new Date(date), Session.getScriptTimeZone(), "yyyy-MM-dd'T'HH:mm:ss"
        );
      } catch(e) {
        Logger.log('Date parse error for row ' + (i+1) + ': ' + e.message);
      }
    }

    // Send to WordPress
    Logger.log('Publishing: ' + title);
    var result = sendToWordPress(post);

    if (result && result.post_id) {
      // Mark as published in column E (5th column)
      sheet.getRange(i + 1, 5).setValue('published');
      // Log time in column F if it was empty
      if (!date) sheet.getRange(i + 1, 6).setValue(new Date());
      publishedCount++;
      Logger.log('SUCCESS: ' + title + ' → Post ID: ' + result.post_id);
    } else {
      Logger.log('FAILED: ' + title + ' (check API key and URL)');
    }

    Utilities.sleep(1500); // wait 1.5s between posts
  }

  Logger.log('Run complete. Published: ' + publishedCount + ' posts.');
}

/**
 * Sends one post to WordPress via your custom plugin endpoint.
 */
function sendToWordPress(postData) {
  try {
    var response = UrlFetchApp.fetch(WP_API_URL, {
      method: 'POST',
      headers: {
        'X-Sourov-Key': WP_API_KEY,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });

    var code = response.getResponseCode();
    var text = response.getContentText();
    Logger.log('WP response ' + code + ': ' + text.substring(0, 200));

    if (code === 200 || code === 201) {
      return JSON.parse(text);
    }
    return null;
  } catch (err) {
    Logger.log('Network error: ' + err.toString());
    return null;
  }
}

/**
 * Guesses the WordPress category based on keywords in the title/content.
 * Extend this list to match your exact WordPress categories.
 */
function guessCategory(title, content) {
  var t = (title + ' ' + content).toLowerCase();
  if (/grammar|tense|verb|noun|adjective|syntax/.test(t)) return 'Grammar';
  if (/listen|phonolog|pronunciat|phonics|intonation|stress|accent/.test(t)) return 'Listening & Phonology';
  if (/speak|fluency|conversation|oral|talk|discuss/.test(t)) return 'Speaking & Fluency';
  if (/celta|teaching practice|lesson plan|tp |observed/.test(t)) return 'CELTA';
  if (/reading|writing|essay|text|comprehension|paragraph/.test(t)) return 'Reading & Writing';
  if (/technolog|app|digital|online|software|tool/.test(t)) return 'Technology in ELT';
  if (/career|job|certif|professional|qualification/.test(t)) return 'Career & Professional Development';
  return 'ELT Masterclass';
}

/**
 * Suggests comma-separated tags from keywords in the post title.
 */
function suggestTags(title) {
  var t = title.toLowerCase();
  var found = [];
  var map = {
    'grammar': 'grammar', 'listen': 'listening', 'speak': 'speaking',
    'pronunciat': 'pronunciation', 'celta': 'CELTA', 'elt': 'ELT',
    'efl': 'EFL', 'esl': 'ESL', 'vocabulary': 'vocabulary',
    'reading': 'reading', 'writing': 'writing', 'fluency': 'fluency',
    'teacher': 'teacher training', 'lesson': 'lesson planning',
    'phonol': 'phonology', 'intonation': 'intonation'
  };
  for (var kw in map) {
    if (t.indexOf(kw) !== -1) found.push(map[kw]);
  }
  return found.length ? found.join(', ') : 'ELT, English teaching';
}

/**
 * TEST FUNCTION — Run this first!
 * Sends a single test post to check the connection.
 */
function testConnection() {
  var result = sendToWordPress({
    title: 'TEST — Automation Check (Delete Me)',
    content: '<p>This test post was created automatically by Google Apps Script. If you see this in your WordPress drafts, the connection is working. Please delete it.</p>',
    category: 'ELT Masterclass',
    tags: 'test, automation',
    status: 'draft'
  });

  var ui = SpreadsheetApp.getUi();
  if (result && result.post_id) {
    ui.alert('CONNECTION WORKS!\n\nTest post created. Post ID: ' + result.post_id + '\n\nCheck WordPress → Posts → Drafts.\nPlease delete the test post when done.');
  } else {
    ui.alert('CONNECTION FAILED.\n\nGo to View → Logs to see the error.\n\nCommon causes:\n- Wrong API key\n- Wrong WordPress URL\n- Plugin not active');
  }
}
```

### Step 3: Save the Script

Press **Ctrl+S** (Windows) or **Cmd+S** (Mac). Name the project: `WordPress Publisher`.

---

## Part 4: Running the Test

### Step 1: Run the Test Function

1. In the toolbar, find the dropdown that shows function names — click it
2. Select **testConnection**
3. Click the **▶ Run** button

**First-time authorization:**
Google will say "This app requires access to your account." This is normal.
1. Click **Review Permissions**
2. Choose your Google account
3. Click **Advanced** → **Go to WordPress Publisher (unsafe)**
4. Click **Allow**

This gives the script permission to make web requests. You only do this once.

### Step 2: Check the Result

- If it worked: A popup says "CONNECTION WORKS!" and a draft post appears in your WordPress admin.
- If it failed: Go to **View → Logs** in the script editor to see the error message.

### Step 3: Common Fixes

| Error in logs | Fix |
|---------------|-----|
| `401 Unauthorized` | Wrong API key in `WP_API_KEY` variable |
| `Connection refused` | Wrong URL in `WP_API_URL` |
| `No sheet named Queue` | Rename your sheet tab to `Queue` |
| `Post keeps reposting` | Make sure column E is being updated to `published` |

---

## Part 5: Setting Up Automatic Hourly Publishing

### Step 1: Go to Triggers

In the Apps Script editor, look at the **left sidebar**. Click the **clock icon** (it says "Triggers" when you hover).

### Step 2: Add a New Trigger

Click **+ Add Trigger** (bottom-right corner of the Triggers page).

Fill in the form:

| Field | Value |
|-------|-------|
| Choose which function to run | `publishFromSheet` |
| Choose which deployment | Head |
| Select event source | Time-driven |
| Select type | Hour timer |
| Select hour interval | Every 1 hour |

Click **Save**.

### Step 3: Confirm

You'll see your trigger listed. From now on, every hour, the script runs automatically and publishes any rows you've marked as `ready`.

---

## Part 6: Your Daily Workflow

After setup, this is ALL you need to do:

### When you finish writing:
1. Open your Google Sheet (bookmark it)
2. Add a new row: title, content, and set Status to `ready`
3. Close the sheet

**Within the next hour, your post appears as a draft in WordPress.**

### Status values you can use:

| Status value | What happens |
|--------------|-------------|
| `ready` | Publishes immediately as a draft |
| `draft` | Same as ready — creates a draft |
| `future` | Schedules the post (requires a date in column F) |
| `publish` | Creates and immediately publishes |
| `published` | Skip this row (already done) |
| `skip` | Skip this row manually |
| (empty) | Skip this row |

### How to schedule a post:

1. Set Status to `future`
2. Set the date in column F: `2026-06-20T09:00:00` (that's June 20, 9am)
3. The script will schedule it in WordPress for that date

---

## Part 7: Frequently Asked Questions

**Q: Do I need to know JavaScript to use this?**
A: No. Just paste the script, change the two configuration lines at the top, and run the test.

**Q: What if I make a mistake in the content column?**
A: Change the status back to `ready` and fix the content — it will re-publish. Then delete the wrong draft from WordPress.

**Q: Can I have multiple spreadsheets?**
A: Yes. Each spreadsheet needs its own Apps Script copy.

**Q: What if a post has HTML but looks weird?**
A: WordPress accepts HTML in the content column. Wrap paragraphs in `<p>...</p>`. Line breaks become `<br>`.

**Q: Can I add a column for images?**
A: Yes — add an Image URL column and modify the script to include `featured_image_url` in the post payload.

**Q: How do I add more categories?**
A: Edit the `guessCategory()` function at the bottom of the script. Add a new `if` statement with your keywords.

**Q: The trigger ran but nothing published — why?**
A: Check `View → Executions` in Apps Script to see the log. Likely the status column doesn't say exactly `ready`.

---

## Part 8: What Is JSON?

You'll see `JSON.stringify(postData)` in the script. JSON stands for **JavaScript Object Notation**. It's the format websites use to talk to each other.

The post data becomes:
```json
{
  "title": "Day 32 – Active Listening",
  "content": "<p>Listening is the most...",
  "category": "ELT Masterclass",
  "tags": "listening, CELTA",
  "status": "draft"
}
```

Your WordPress plugin receives this and creates the post. That's the entire mechanism.

---

## Summary

| Concept | Plain English |
|---------|---------------|
| CSV | Table data saved as plain text with commas |
| Google Sheets | Visual editor for that data |
| Apps Script | A programmable robot inside Google |
| `UrlFetchApp.fetch()` | The robot knocking on your WordPress website's door |
| JSON | The language the robot and WordPress use to communicate |
| Trigger | The clock that tells the robot when to wake up |

**One-sentence summary:** You fill a table in Google Sheets, a robot reads it every hour, and your WordPress blog gets new posts without you opening WordPress.
