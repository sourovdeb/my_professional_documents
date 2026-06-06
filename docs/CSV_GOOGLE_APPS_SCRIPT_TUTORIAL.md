# How CSV + Google Apps Script Works: A Complete Tutorial

## Why Read This?

You said: *"I never understood how CSV + Google JavaScript works."*

This guide answers that fully — from what a CSV is, why JavaScript is involved, to step-by-step setup with every click explained. No coding knowledge required.

---

## Part 1: What Is a CSV?

CSV = **Comma-Separated Values**. It is a plain text file where data sits in rows and columns — exactly like a spreadsheet, but saved as simple text:

```
Title,Content,Category,Tags,Status
"Day 32 – Listening","<p>Today we practised...","ELT","listening,celta","draft"
"Grammar: Articles","<p>Using a, an, the...","Grammar","grammar","draft"
```

**Why commas?** It is the universal separator every computer understands. Every spreadsheet (Google Sheets, Excel, LibreOffice) can read and write CSV. Every programming language can read it. It is the common language of data.

**What Google Sheets has to do with it**: When you type data into Google Sheets, you are building a visual spreadsheet. Underneath, Google Sheets can export that data as CSV — just the rows and columns as plain text. More importantly, a script can *read* each row and act on it.

**The whole system in plain English:**
```
You type in Google Sheets
    → Script reads each row
    → Calls WordPress API
    → Post is created
    → Row marked 'published'
```
You never touch code after setup.

---

## Part 2: What Is Google Apps Script? Why JavaScript?

Google Apps Script is **JavaScript that runs inside Google's servers**. When you write a script in Google Sheets, you give Google instructions — Google runs them for free, with no server of your own.

Think of it as a robot living inside your spreadsheet. You write instructions (the script), and the robot reads each row and does something with it.

**Why JavaScript specifically?**
1. It is the language Google chose for Apps Script
2. It is the most widely used language on the internet
3. Google Sheets, Docs, Gmail all use it — one language controls everything
4. Apps Script is sandboxed — it cannot harm your computer

You do not need to learn JavaScript. Copy-paste the scripts from this guide, change your API keys, and it works. But understanding *why* helps you fix problems.

---

## Part 3: How They Connect to WordPress

```
┌─────────────────┐   ┌─────────────────────────┐   ┌──────────────────┐
│  Google Sheets  │──▶│  Google Apps Script     │──▶│  WordPress API   │
│                 │   │                         │   │                  │
│  Row 1: Post A  │   │  1. Reads each row      │   │  Creates post    │
│  Row 2: Post B  │   │  2. Formats as JSON     │   │  in database     │
│  Row 3: Post C  │   │  3. Sends HTTP request  │   │                  │
└─────────────────┘   └─────────────────────────┘   └──────────────────┘
```

The script:
1. Opens your spreadsheet
2. Reads each row (each row = one blog post)
3. Packages the data as JSON (the format WordPress understands)
4. Sends an HTTP POST request to your WordPress site
5. WordPress receives it, creates the post, returns a confirmation
6. The script marks the row as `published`

---

## Part 4: Step-by-Step Setup

### Step 1: Create the Sheet

1. Go to **sheets.google.com** → **+ Blank**
2. In Row 1, type these headers (one per cell):

| A | B | C | D | E | F | G | H |
|---|---|---|---|---|---|---|---|
| Title | Content | Category | Tags | Status | ScheduleDate | SEO_Title | Meta_Description |

3. Right-click the tab at the bottom → **Rename** → type `Queue`

### Step 2: Add Your First Post

- **A2**: `Day 32 – Listening and Phonology`
- **B2**: `<p>Today in class we focused on connected speech...</p>`
- **C2**: `ELT Masterclass`
- **D2**: `listening, phonology, CELTA`
- **E2**: `draft`
- **F2**: *(leave blank)*
- **G2**: `Day 32: Master English Listening`
- **H2**: `How to improve listening comprehension using connected speech techniques`

### Step 3: Open the Script Editor

1. Click **Extensions** (top menu) → **Apps Script**
2. A new tab opens — this is the code editor
3. Delete all default code (the `function myFunction() {}` line)

### Step 4: Paste the Script

Paste the complete script from `scripts/sheet_publisher.gs` into the editor.

Or paste this minimal version:

```javascript
const WP_API = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';

function publishFromSheet() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName('Queue');
  if (!sheet) { Logger.log('No sheet named Queue!'); return; }

  const rows = sheet.getDataRange().getValues();

  for (let i = 1; i < rows.length; i++) {
    const [title, content, category, tags, status,
           scheduleDate, seoTitle, metaDesc] = rows[i];

    if (!title || status === 'published') continue;

    const postData = {
      title, content,
      category:         category || 'ELT Masterclass',
      tags:             tags     || '',
      status:           status === 'future' ? 'future' : 'draft',
      seo_title:        seoTitle  || title.substring(0, 60),
      meta_description: metaDesc  || content.replace(/<[^>]*>/g, '').substring(0, 155)
    };

    if (status === 'future' && scheduleDate)
      postData.date = new Date(scheduleDate).toISOString();

    const result = publishPost(postData);
    if (result && result.post_id) {
      sheet.getRange(i + 1, 5).setValue('published');
      sheet.getRange(i + 1, 6).setValue(new Date().toISOString());
      Logger.log('Published: ' + title);
    } else {
      Logger.log('Failed: ' + title);
    }
    Utilities.sleep(1500);
  }
}

function publishPost(postData) {
  const WP_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY')
    || 'your-api-key-here';
  try {
    const res = UrlFetchApp.fetch(WP_API, {
      method: 'POST',
      headers: { 'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json' },
      payload: JSON.stringify(postData),
      muteHttpExceptions: true
    });
    if (res.getResponseCode() !== 200) {
      Logger.log('HTTP ' + res.getResponseCode() + ': ' + res.getContentText());
      return null;
    }
    return JSON.parse(res.getContentText());
  } catch (e) {
    Logger.log('Error: ' + e.message);
    return null;
  }
}

// Run ONCE to store your key, then DELETE this function
function storeCredentials() {
  PropertiesService.getScriptProperties().setProperty('WP_KEY', 'YOUR-KEY-HERE');
  Logger.log('Key stored.');
}
```

### Step 5: Store Your API Key

1. In the function dropdown (next to the play button), select `storeCredentials`
2. Replace `YOUR-KEY-HERE` with your actual WordPress plugin key
3. Click **Run** → accept permissions popup
4. **Delete** the `storeCredentials` function after it runs

### Step 6: Test

1. Select `publishFromSheet` in the dropdown
2. Click **Run**
3. Watch the **Execution Log** at the bottom
4. Check WordPress dashboard — your post should be a draft

### Step 7: Set Automatic Time Trigger

1. In Apps Script, click the **clock icon** (Triggers) in the left sidebar
2. Click **+ Add Trigger** (bottom right)
3. Set:
   - Function: `publishFromSheet`
   - Event source: `Time-driven`
   - Type: `Hour timer` → Every hour
4. Click **Save**

Now Google runs your script every hour automatically. Fill the sheet → posts appear in WordPress. Nothing else required.

---

## Part 5: Why Does This Work? (The Real Explanation)

### Why JSON?

JSON (JavaScript Object Notation) is the format APIs use to exchange data. When your script sends:
```json
{"title": "Day 32", "content": "<p>...", "status": "draft"}
```
WordPress reads it like a form submission. Your `sourov-ai-controller.php` plugin intercepts this at `/wp-json/sourov/v1/ai-post` and creates the post in the database.

### Why HTTP POST?

The same protocol your browser uses to load web pages. A POST request sends data *to* a server. Your script is doing what a browser does when you submit the WordPress editor — but automatically.

### Why Google Sheets as the Interface?

Because it removes all friction:
- No terminal needed
- Fill it on your phone
- See all posts' status in one view
- Multiple people can add posts
- Works with Zapier/n8n if you want more automation later

### Why Time Triggers?

Because you want zero cognitive load. Google's cron system runs the script for you at set intervals. You fill the sheet → wait → posts appear. No action required on your part.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "No sheet named Queue" | Right-click tab → Rename → `Queue` (exact spelling) |
| Permission popup | Click Review Permissions → Allow |
| `401 Unauthorized` | Your WordPress API key is wrong |
| `400 Bad Request` | Check content column is valid HTML |
| `500 Server Error` | Check plugin is active in WordPress |
| Script times out | Process max 50 rows per run |
| Posts not appearing | Check Execution Log for the error |
