# Complete Beginner's Tutorial: CSV + Google Sheets + Google Apps Script → WordPress

**Written for Sourov Deb — assumes zero prior coding knowledge**  
**Last updated: June 2026**

---

## What Problem Are We Solving?

Instead of manually logging into WordPress every time you want to publish, you write your content in a Google Sheet. A small script automatically reads it and creates the post on WordPress. You never touch the WordPress dashboard.

> You write once. The system handles the rest — even while you sleep.

---

## Part 1: What Is a CSV File?

CSV stands for **Comma Separated Values**. Open any CSV file in a text editor and it looks like this:

```
Title,Content,Category,Status
Day 32 – Listening,This is my content.,ELT,draft
Day 33 – Grammar,Grammar is the architecture.,Grammar,publish
```

That's it. Each line is one row. Each comma separates one column. No fonts, no images — just data in a table.

**Why does this matter?** Because every tool in the world can read CSV: Excel, Google Sheets, Python, WordPress import — it is the universal language of tabular data. When people say "CSV-based batch publishing", they mean: put your posts in a table, and software reads that table and creates the posts.

### CSV vs Google Sheets — What's the Difference?

| Feature | CSV (.csv file) | Google Sheets (cloud) |
|---------|----------------|-----------------------|
| Format | Plain text file on your computer | Live spreadsheet in your browser |
| Can run automatic scripts? | No | Yes ✓ |
| Can auto-publish on a timer? | No | Yes ✓ |
| Can track status (published/draft)? | Manually | Automatically ✓ |
| Shared collaboration? | No | Yes ✓ |
| Free? | Yes | Yes ✓ |

**For automation, use Google Sheets** — not a raw CSV file. We import CSV *into* Sheets only when needed.

---

## Part 2: What Is Google Apps Script?

Google Apps Script is **JavaScript that runs inside your Google account** — on Google's computers, not yours.

JavaScript is a programming language used everywhere on the web. Google Apps Script lets you write JavaScript that:
- Reads your Google Sheets
- Sends data to websites (like WordPress)
- Runs automatically every hour (or every day)
- Sends you emails
- Creates Google Docs

**You don't need your own server. You don't need to install anything.** It runs in the cloud for free.

### What Does "JavaScript" Look Like?

Here is the simplest possible JavaScript:

```javascript
// This is a comment (ignored by the computer)
const myName = 'Sourov'; // Store a value
Logger.log('Hello, ' + myName); // Print: Hello, Sourov
```

- `const` = store a value that won't change
- `//` = a comment (human note, ignored by code)
- `Logger.log(...)` = print a message to the log

For this tutorial, **you don't need to write any JavaScript**. You copy the script I've written, fill in your website URL and API key, and press Run.

---

## Part 3: How They All Connect to WordPress

Here is the complete picture, step by step:

```
[You type in Google Sheets]
         ↓
[Apps Script wakes up every hour]
         ↓
[Script reads each row in your sheet]
         ↓
[For each row not yet published:]
  → Guesses category from keywords
  → Suggests tags from content
  → Sends data to WordPress via API
         ↓
[WordPress creates the post]
         ↓
[Script writes "published" in your sheet]
```

The connection point between Apps Script and WordPress is called an **API endpoint** — a special URL on your website that accepts data. Your endpoint is already set up at:

```
https://sourovdeb.com/wp-json/sourov/v1/ai-post
```

Apps Script sends a "request" (a packet of data) to this URL. WordPress reads it and creates the post.

---

## Part 4: Step-by-Step Setup

### Step 1 — Set Up the Google Sheet

1. Open **sheets.google.com** → create a new blank spreadsheet
2. Name it: **WordPress Publisher**
3. In **Row 1**, type these headers exactly (one per cell):

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Title | Content | Category | Tags | Status | ScheduleDate | SEO_Title | Meta_Description |

4. Right-click the tab at the bottom → **Rename** it to: **Queue**

5. In **Row 2**, add a test post:
   - **A2**: `Day 32 – The Power of Listening`
   - **B2**: `<p>Listening is the most underrated skill in language learning...</p>`
   - **C2**: *(leave blank — the script will auto-detect)*
   - **D2**: *(leave blank — the script will auto-suggest)*
   - **E2**: `draft`
   - **F2**: *(leave blank)*
   - **G2**: *(leave blank)*
   - **H2**: *(leave blank)*

---

### Step 2 — Open Apps Script

1. In your Google Sheet, click the top menu: **Extensions → Apps Script**
2. A new browser tab opens — this is the Apps Script editor
3. You will see a default function like `function myFunction() {}` — **select all and delete it**
4. You now have a blank editor

---

### Step 3 — Paste the Publisher Script

Copy this entire block and paste it into the empty editor:

```javascript
// ============================================================
// WordPress Batch Publisher — Sourov Deb Publishing System
// ============================================================
// SETUP:
// 1. Replace YOUR_WP_API_KEY_HERE with your real API key
// 2. Fill the "Queue" tab in your sheet with posts
// 3. Run publishFromSheet manually once to test
// 4. Then set a time trigger for automatic running (see Step 7)
// ============================================================

const WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_SECRET_KEY = 'YOUR_WP_API_KEY_HERE';

// MAIN FUNCTION — runs on a timer or when you click Run
function publishFromSheet() {
  const spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = spreadsheet.getSheetByName('Queue');

  if (!sheet) {
    Logger.log('ERROR: No tab named "Queue". Create one first.');
    return;
  }

  const allData = sheet.getDataRange().getValues(); // Read every row

  for (let i = 1; i < allData.length; i++) { // Start at row 2 (skip headers)
    const title       = allData[i][0]; // Column A
    const content     = allData[i][1]; // Column B
    const category    = allData[i][2]; // Column C
    const tags        = allData[i][3]; // Column D
    const status      = allData[i][4]; // Column E
    const schedDate   = allData[i][5]; // Column F
    const seoTitle    = allData[i][6]; // Column G
    const metaDesc    = allData[i][7]; // Column H

    // Skip rows that are blank or already done
    if (!title || status === 'published') continue;

    // Auto-fill blanks with smart defaults
    const finalCategory = category || guessCategory(title, content);
    const finalTags     = tags     || suggestTags(title, content);
    const finalSeoTitle = seoTitle || title;
    const finalMeta     = metaDesc || stripHtml(content).substring(0, 155);

    const postData = {
      title:            finalSeoTitle,
      content:          content,
      category:         finalCategory,
      tags:             finalTags,
      status:           ['future','publish','draft'].includes(status) ? status : 'draft',
      seo_title:        finalSeoTitle,
      meta_description: finalMeta
    };

    if (status === 'future' && schedDate) {
      postData.date = schedDate.toString();
    }

    Logger.log('Sending: ' + title);
    const result = sendToWordPress(postData);

    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');    // Mark as done
      sheet.getRange(i + 1, 9).setValue(result.post_id); // Save WP post ID
      Logger.log('SUCCESS: Post ID ' + result.post_id);
    } else {
      Logger.log('FAILED: ' + JSON.stringify(result));
    }

    Utilities.sleep(1500); // Wait 1.5 seconds between posts
  }
  Logger.log('Done.');
}

// Sends post data to WordPress. Returns the parsed JSON response.
function sendToWordPress(postData) {
  try {
    const res = UrlFetchApp.fetch(WP_API_URL, {
      method: 'POST',
      headers: {
        'X-Sourov-Key': API_SECRET_KEY,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });
    Logger.log('HTTP ' + res.getResponseCode());
    return JSON.parse(res.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e);
    return { error: e.toString() };
  }
}

// Guesses category based on keywords in title and content
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('grammar') || text.includes('tense') || text.includes('verb'))
    return 'Grammar';
  if (text.includes('listening') || text.includes('pronunciation') || text.includes('phonology'))
    return 'Listening & Phonology';
  if (text.includes('celta') || text.includes('lesson plan') || text.includes('teaching practice'))
    return 'CELTA';
  if (text.includes('speaking') || text.includes('fluency') || text.includes('conversation'))
    return 'Speaking & Fluency';
  if (text.includes('vocabulary') || text.includes('lexis') || text.includes('collocation'))
    return 'Vocabulary';
  if (text.includes('reading') || text.includes('comprehension'))
    return 'Reading Skills';
  if (text.includes('writing') || text.includes('essay') || text.includes('paragraph'))
    return 'Writing Skills';
  return 'ELT Masterclass';
}

// Suggests tags based on keywords found in post text
function suggestTags(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  const map = {
    'grammar':'grammar', 'listening':'listening', 'speaking':'speaking',
    'pronunciation':'pronunciation', 'vocabulary':'vocabulary', 'celta':'CELTA',
    ' elt ':'ELT', ' esl ':'ESL', 'fluency':'fluency', 'lesson':'lesson plan',
    'teacher':'teaching', 'reading':'reading', 'writing':'writing',
    'ielts':'IELTS', 'cambridge':'Cambridge'
  };
  const found = [];
  for (const [keyword, tag] of Object.entries(map)) {
    if (text.includes(keyword)) found.push(tag);
  }
  return found.join(', ') || 'ELT';
}

// Removes HTML tags from a string
function stripHtml(html) {
  return html.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}
```

---

### Step 4 — Enter Your API Key

Find this line in the script:
```javascript
const API_SECRET_KEY = 'YOUR_WP_API_KEY_HERE';
```

Replace `YOUR_WP_API_KEY_HERE` with your actual API key. Keep the quotes.

> **Security note:** Never upload this script to GitHub with your real key. Use a `.env` file or store the key in Google Apps Script's `PropertiesService` for production use.

---

### Step 5 — Save the Project

1. Press **Ctrl+S** (Windows) or **Cmd+S** (Mac)
2. Name it: **WordPress Publisher**
3. Click OK

---

### Step 6 — Run It Manually (Test)

1. In the toolbar dropdown (showing function names), select `publishFromSheet`
2. Click the **▶ Run** button
3. **First time only:** A permissions dialog appears → click **Review Permissions → Allow**
4. Watch the **Execution Log** at the bottom for output
5. Log into your WordPress dashboard and check Posts — you should see a new draft

---

### Step 7 — Set the Automatic Timer

1. Click the **clock icon** in the left sidebar (Triggers)
2. Click **+ Add Trigger** (bottom right corner)
3. Configure:
   - **Function to run:** `publishFromSheet`
   - **Event source:** Time-driven
   - **Type:** Hour timer
   - **Every:** 1 hour
4. Click **Save**

Now the script checks your sheet every hour. Add a row → it publishes within the hour. Zero manual work.

---

## Part 5: The Code Explained — Every Single Line

| Code | Plain English Meaning |
|------|-----------------------|
| `const WP_API_URL = '...'` | Saves your WordPress URL so the script knows where to send posts |
| `SpreadsheetApp.getActiveSpreadsheet()` | Opens this Google Sheet (the one you're working in) |
| `.getSheetByName('Queue')` | Finds the tab named "Queue" specifically |
| `.getDataRange().getValues()` | Reads every row and column into memory as a table |
| `for (let i = 1; i < allData.length; i++)` | Loop through all rows, starting at row 2 (row 1 = headers) |
| `allData[i][0]` | Get column A (index 0) of the current row |
| `if (!title \|\| status === 'published') continue` | Skip blank rows and already-published rows |
| `category \|\| guessCategory(...)` | Use the column value, or if empty, auto-guess |
| `UrlFetchApp.fetch(WP_API_URL, {...})` | Send an HTTP request to WordPress (like clicking a button on a website) |
| `JSON.stringify(postData)` | Convert the JavaScript object to a text string that can travel over the internet |
| `JSON.parse(res.getContentText())` | Convert the WordPress response back into a JavaScript object |
| `sheet.getRange(i+1, 5).setValue('published')` | Write "published" into column E of this row |
| `Utilities.sleep(1500)` | Pause for 1.5 seconds — being polite to your server |

---

## Part 6: Common Errors and How to Fix Them

| Error message | Cause | Fix |
|---------------|-------|-----|
| `No tab named "Queue"` | Tab not renamed | Right-click tab → Rename to exactly `Queue` |
| `401 Unauthorized` | Wrong API key | Check key, remove any spaces, keep the quotes |
| `404 Not Found` | Wrong WordPress URL | Verify the API URL is active by visiting it in a browser |
| `Post created but wrong category` | Category name mismatch | Category must exactly match one in WordPress (capital letters matter) |
| `TypeError: Cannot read property` | Empty required field | Check column B (Content) is not empty |
| `Exception: Response exceeded limit` | Content too large | Split into shorter posts |
| `Daily quota exceeded` | Ran too many requests | Reduce trigger frequency (every 6 hours instead of 1) |

---

## Part 7: Testing Checklist

Do this before trusting the system:

- [ ] Add 1 row with Status: `draft` → run manually → check WordPress for new draft
- [ ] Check the sheet — did Status change to `published`?
- [ ] Check column I — does it show the WordPress post ID?
- [ ] Add a row with Status: `publish` → does it publish immediately?
- [ ] Leave Category blank → does `guessCategory` pick the right one?
- [ ] Add a row with Status: `future` and a date → does it schedule correctly?

---

## Part 8: Adding Your Own Categories and Keywords

Open `guessCategory` in the script. Add your own:

```javascript
if (text.includes('YOUR KEYWORD')) return 'Your Category Name';
```

> The category name must **exactly match** a category in WordPress. Go to Posts → Categories to check.

To add more tag keywords, update the `map` object in `suggestTags`:

```javascript
'your keyword': 'Tag Name',
```

---

## Part 9: Summary — The Whole System in Plain English

1. You type a post title and content into the Google Sheet
2. You set Status to `draft` (or `publish`, or `future`)
3. Every hour, Apps Script wakes up automatically
4. It reads every row in your Queue tab
5. If a row has a title and status is not `published`, it processes it
6. It auto-fills any blank Category and Tags columns
7. It sends the data to your WordPress site
8. WordPress creates the post
9. Apps Script writes `published` in the Status column — so the same post is never sent twice

**That is the entire system.** CSV gave us the data format. Google Sheets gave us the live table. Google Apps Script gave us the automation layer. WordPress received the result.

---

*For support, questions, or to report issues: Sourov Deb · sourovdeb.com*
