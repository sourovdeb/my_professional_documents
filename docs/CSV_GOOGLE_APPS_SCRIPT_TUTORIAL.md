# CSV + Google Apps Script: Complete Beginner Tutorial
## "I Never Understood How This Works" — Explained Step By Step

### Before We Start: What Are These Things?

**CSV** = Comma-Separated Values. It's the simplest spreadsheet format.
Every row is a line of text. Every cell is separated by a comma.

Example: a file called `posts.csv` might look like this:
```
Title,Content,Category,Status
Day 32 - Listening,"Today we practised...",ELT,draft
Day 33 - Grammar,"The present perfect...",Grammar,draft
```

You can open a CSV in Excel, Google Sheets, or a text editor. It's just text.

**Google Apps Script** = JavaScript that runs inside Google (Sheets, Drive, Gmail).
You don't need to install anything. It runs on Google's servers.
Think of it as a robot that lives inside your spreadsheet.

**Why do they work together?**
Google Sheets can read/write CSV files. Apps Script can read your spreadsheet.
So the path is: `CSV file → Google Sheets → Apps Script → WordPress`.

---

## Part 1: Understanding CSV Files

### Creating a CSV from scratch

Open any text editor (Notepad on Windows, TextEdit on Mac) and type:
```
Title,Content,Tags,Status
My First Post,Hello world this is my content,beginner,draft
My Second Post,"Content with a comma, inside quotes",grammar,draft
```

Save it as `posts.csv`. That's a valid CSV file.

**Important rules:**
- If your content has a comma → wrap the whole cell in `"double quotes"`
- If your content has a quote mark → write it as `"""`
- First row = column headers (these are your column names)
- Each following row = one WordPress post

### Importing CSV into Google Sheets

1. Open Google Sheets (sheets.google.com)
2. Click **File → Import**
3. Upload your CSV file
4. Choose **Comma** as separator
5. Click **Import data**

Now your CSV is a proper spreadsheet.

---

## Part 2: Your First Apps Script (Line by Line Explanation)

### Opening the Script Editor

1. In your Google Sheet: click **Extensions** (top menu)
2. Click **Apps Script**
3. A new tab opens — this is your code editor
4. Delete any existing code
5. Paste the script below

### The Simplest Possible Script — READ THIS CAREFULLY

```javascript
// This is a comment. Comments start with //
// The computer ignores comments. They are notes for humans.

// This function will run when you click "Run" or when a trigger fires
function readMySheet() {
  
  // Step 1: Get the currently open spreadsheet
  // SpreadsheetApp is built into Google - you don't need to install anything
  var spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  
  // Step 2: Get a specific sheet (tab) by its name
  // Change 'Queue' to whatever your tab is named
  var sheet = spreadsheet.getSheetByName('Queue');
  
  // Step 3: Get ALL data from the sheet as a 2D array
  // A 2D array is like a table: rows[0] is the first row, rows[0][0] is cell A1
  var rows = sheet.getDataRange().getValues();
  
  // Step 4: Loop through each row, starting at row 1 (skip row 0 = headers)
  for (var i = 1; i < rows.length; i++) {
    
    // Each row is an array. rows[i][0] = column A, rows[i][1] = column B, etc.
    var title   = rows[i][0];  // Column A
    var content = rows[i][1];  // Column B
    var status  = rows[i][4];  // Column E
    
    // Only process rows that have a title and haven't been published yet
    if (!title || status === 'published') {
      continue;  // 'continue' means: skip this row, go to the next one
    }
    
    // Log to the console so you can see what's happening
    // View logs: click 'Execution log' at the bottom of the script editor
    Logger.log('Processing row ' + i + ': ' + title);
    
  } // end of for loop
  
} // end of function
```

### How to Run It
1. Click the **Save** button (floppy disk icon)
2. Click the **Run** button (triangle / play icon)
3. First time: it will ask for permissions → click **Review permissions → Allow**
4. Click **Execution log** at the bottom to see what happened

You'll see lines like:
```
[19:42:05] Processing row 1: Day 32 - Listening
[19:42:05] Processing row 2: Day 33 - Grammar
```

---

## Part 3: Adding WordPress Publishing

Now we add the part that actually sends data to your WordPress site.

```javascript
// =============================================================
// FULL WORKING SCRIPT: Google Sheets → WordPress
// =============================================================

// These are constants — values that don't change
// IMPORTANT: Never put real passwords here if sharing the script!
var WP_API_URL = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
var WP_API_KEY = 'YOUR_API_KEY_HERE';  // replace with your real key

// The main function
function publishNewPosts() {
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Queue');
  var rows  = sheet.getDataRange().getValues();
  
  // Start at 1 to skip the header row
  for (var i = 1; i < rows.length; i++) {
    
    // Destructure the row into named variables
    var title    = rows[i][0];  // A: Title
    var content  = rows[i][1];  // B: Content (HTML)
    var category = rows[i][2];  // C: Category
    var tags     = rows[i][3];  // D: Tags (comma-separated)
    var status   = rows[i][4];  // E: Status (draft/future/published)
    var date     = rows[i][5];  // F: Schedule date (optional)
    var seoTitle = rows[i][6];  // G: SEO Title
    var metaDesc = rows[i][7];  // H: Meta description
    
    // Skip empty rows or already-published rows
    if (!title || status === 'published') continue;
    
    // Build the data object to send to WordPress
    // This is called a JSON object - it's a set of key:value pairs
    var postData = {
      title:            title,
      content:          content,
      category:         category || 'ELT Masterclass',
      tags:             tags     || '',
      status:           status === 'future' ? 'future' : 'draft',
      seo_title:        seoTitle || title,
      meta_description: metaDesc || content.substring(0, 160),
    };
    
    // If it's a scheduled post, add the date
    if (status === 'future' && date) {
      postData.date = new Date(date).toISOString();
    }
    
    // Send the data to WordPress
    // UrlFetchApp.fetch() is Google's way to make HTTP requests
    var response = UrlFetchApp.fetch(WP_API_URL, {
      method:  'POST',
      headers: {
        'X-Sourov-Key':  WP_API_KEY,
        'Content-Type':  'application/json',
      },
      payload:           JSON.stringify(postData),  // convert object to JSON string
      muteHttpExceptions: true,  // don't crash if there's an error, just return it
    });
    
    // Parse the response
    var result = JSON.parse(response.getContentText());
    
    // Check if it worked
    if (result.post_id) {
      // Success! Update the status cell to 'published'
      sheet.getRange(i + 1, 5).setValue('published');  // row i+1, column 5 (E)
      Logger.log('SUCCESS: ' + title + ' → Post ID ' + result.post_id);
    } else {
      // Something went wrong — write the error in the status cell
      sheet.getRange(i + 1, 5).setValue('ERROR: ' + (result.message || 'unknown'));
      Logger.log('FAILED: ' + title);
    }
    
    // Wait 1.5 seconds between posts so we don't overwhelm the server
    Utilities.sleep(1500);
    
  } // end loop
  
  Logger.log('Done! Check your WordPress drafts.');
}
```

---

## Part 4: Storing API Keys Safely

NEVER put your real API key directly in the script code if you share it.
Use **Script Properties** instead:

```javascript
// Run this function ONCE to save your key, then DELETE it
function saveMyKey() {
  PropertiesService.getScriptProperties().setProperty('WP_KEY', 'your-real-key-here');
  Logger.log('Key saved!');
}

// Then in your main script, read it like this:
var WP_API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
```

Script Properties are stored privately — they don't appear in your code.

---

## Part 5: Setting Up an Automatic Time Trigger

This makes the script run automatically every hour without you clicking anything.

1. In the Apps Script editor, click the **clock icon** on the left (Triggers)
2. Click **+ Add Trigger** (bottom right)
3. Set these options:
   - Function: `publishNewPosts`
   - Deployment: `Head`
   - Event source: `Time-driven`
   - Type of time: `Hour timer`
   - Interval: `Every hour`
4. Click **Save**

Now every hour, Google automatically runs your script. If there are new rows in the sheet with status `draft`, it publishes them. If not, it does nothing.

---

## Part 6: Common Mistakes and Fixes

| Problem | Likely Cause | Fix |
|---------|-------------|-----|
| `Cannot read property of undefined` | Row has empty cells | Add `if (!title) continue;` check |
| `Exception: Request failed` | Wrong API URL or key | Double-check WP_API_URL and key |
| Script runs but nothing posts | Status column already says 'published' | Clear the status cell or add a new row |
| `SyntaxError in JSON` | Content has special characters | Wrap HTML content in `JSON.stringify()` |
| Trigger doesn't fire | Script has an error | Run manually first, fix errors, then re-add trigger |
| `Authorization required` | First run needs permission | Click Run manually once and grant access |

---

## Summary: The Complete Flow

```
You write in Google Docs
        ↓
Copy content into Google Sheet (one row per post)
        ↓
Apps Script runs every hour (automatically)
        ↓
For each row with status = 'draft':
  → Sends title + content to WordPress API
  → Gets back a post_id
  → Updates status cell to 'published'
        ↓
You open WordPress admin and review drafts
        ↓
Click Publish when you're happy
```

You write. Everything else is automatic.
