# How CSV + Google Apps Script Works — Complete Tutorial
## (Written for Someone Who Has Never Coded)

---

## Why This Tutorial Exists

You said: *"I never understood how CSV + Google JavaScript works."*

This tutorial explains it from absolute zero. No assumed knowledge. By the end you will:
- Know what CSV *is* and why it matters
- Understand what Google Apps Script *is* (and why it is not scary)
- Have a working publish-from-spreadsheet system
- Know *why* each piece works, not just *how*

This system is specifically designed for someone managing bipolar disorder and depression. The whole point is: **you write, the machine does the rest.**

---

## Part 1: What is a CSV?

### The plain-English answer

CSV stands for **Comma-Separated Values**. It is just a text file where each line is a row of data, and commas separate the columns.

Imagine this spreadsheet:

| Title | Category | Status |
|-------|----------|---------|
| Day 32 – Listening | ELT | draft |
| Grammar Basics | Grammar | publish |

As a CSV file, that exact same data looks like this:

```
Title,Category,Status
Day 32 – Listening,ELT,draft
Grammar Basics,Grammar,publish
```

That is literally it. A CSV is a spreadsheet saved as plain text.

### Why does it matter for you?

Google Sheets **is** a CSV editor with a pretty face. Every Google Sheet can be exported as CSV, or you can work directly in Sheets and never touch the raw CSV file. The reason CSV matters is that **every programming language can read it**. Python can read it. JavaScript can read it. WordPress can read it.

When your Google Sheet becomes your "publishing queue", you are essentially maintaining a CSV database of posts — without ever thinking about databases.

---

## Part 2: What is Google Apps Script?

### The plain-English answer

Google Apps Script is **a small robot that lives inside your Google account**. It can:
- Read and write your Google Sheets
- Send emails from your Gmail
- Call websites (like your WordPress blog)
- Run on a schedule (e.g., every hour, every morning at 9 AM)

It speaks **JavaScript** — but you do not need to be a programmer. You copy a script, paste it in, set a timer, and it runs forever.

### The mental model that makes everything click

Think of it like this:

```
Your Google Sheet = The instruction book
Apps Script      = The robot that reads the book
Your WordPress   = The thing the robot acts on
```

You fill in the instruction book (the sheet). The robot reads it every hour. The robot publishes your posts. You never touch a terminal.

### Why is this better than doing it manually?

| Manual approach | Automated approach |
|-----------------|--------------------|
| Open WordPress admin | (happens automatically) |
| Click New Post | (happens automatically) |
| Type or paste title | (happens automatically) |
| Choose category | (happens automatically) |
| Add tags | (happens automatically) |
| Click Publish | (happens automatically) |
| **6 decisions, 6 clicks, minimum 10 minutes** | **You wrote. Done.** |

For someone managing a mental health condition, removing those 6 decisions is not a luxury — it is a necessity.

---

## Part 3: How They Work Together — The Full Picture

Here is the complete flow, step by step:

```
[You write a post title and content into Google Sheets]
         |
         v
[Apps Script wakes up every hour (automatic)]
         |
         v
[Script reads each row of the sheet]
         |
         v
[For each row where Status = 'ready', it builds a JSON message]
         |
         v
[Script sends that message to your WordPress REST API]
         |
         v
[WordPress creates the post as a draft]
         |
         v
[Script marks the row as 'published' in the sheet]
         |
         v
[You review the draft in WordPress and click Publish when ready]
```

### What is JSON?

JSON is just the language that websites use to talk to each other. When Apps Script sends your post to WordPress, it sends a package that looks like this:

```json
{
  "title": "Day 32 – Listening",
  "content": "<p>Today we practised minimal pairs...</p>",
  "status": "draft",
  "category": "ELT",
  "tags": "listening, phonology"
}
```

That is literally a list of labels and values. The curly braces `{}` are the package. The colons `:` mean "this label has this value". The commas separate items.

You never write JSON manually. The script writes it for you.

---

## Part 4: Step-by-Step Setup (Do This Once, Never Again)

### Step 1: Set up your Google Sheet

1. Open Google Sheets: https://sheets.google.com
2. Create a new spreadsheet
3. Name the first sheet tab **Queue** (click the tab at the bottom and rename it)
4. Add these headers in row 1:

```
A1: Title
B1: Content
C1: Category
D1: Tags
E1: Status
F1: Published Date
G1: SEO Title
H1: Meta Description
```

5. Add your first test row in row 2:
```
A2: My First Automated Post
B2: <p>This is my first post published automatically.</p>
C2: ELT Masterclass
D2: automation, elt
E2: ready
G2: My First Automated Post | Sourov's Blog
H2: A test of my automated WordPress publishing system.
```

### Step 2: Open Apps Script

1. In your Google Sheet, click **Extensions** in the top menu
2. Click **Apps Script**
3. A new tab opens. You will see a blank script editor.
4. Delete everything in the editor (select all, delete)
5. Paste the full script from `scripts/sheet_publisher.gs` in this repository
6. Change the `WP_API` and `API_KEY` values to match your credentials

### Step 3: Test it manually

1. In the script editor, click the **Run** button (triangle/play icon)
2. The first time, Google will ask you to authorise the script — click Allow
3. Wait 5 seconds
4. Go back to your Google Sheet — the row should now say **published** in column E
5. Go to your WordPress dashboard — you should see the draft post

If it worked: congratulations. You just published a blog post without touching WordPress.

### Step 4: Set up the automatic timer

1. In the Apps Script editor, click the **clock icon** on the left (Triggers)
2. Click **Add Trigger** (bottom right)
3. Configure it:
   - Function to run: `publishFromSheet`
   - Deployment: `Head`
   - Event source: `Time-driven`
   - Type: `Hour timer`
   - Every: `1 hour`
4. Click Save

Now the script runs every hour automatically. You never have to touch it again.

---

## Part 5: Common Questions

### "What if I make a typo in the sheet?"

Before the script publishes anything, it checks if `Status = 'ready'`. So:
- Leave the status blank while you are still writing
- Only change status to `ready` when you are confident
- The system will never publish something you did not mark as ready

### "What if the script fails?"

The script marks rows as `published` only after WordPress confirms success. If something fails, the row stays as `ready` and the script tries again next hour.

### "Can I schedule posts for a future date?"

Yes. In column E (Status) write `future`, and in column F (Published Date) write the date and time in this format: `2026-06-15T09:00:00`. The script will tell WordPress to publish it at that exact time.

### "What if I want to add more categories?"

Open the script and find the `guessCategory()` function. Add your category name and the keywords that should trigger it. Example:

```javascript
if (text.includes('pronunciation')) return 'Phonology';
if (text.includes('vocabulary')) return 'Vocabulary';
```

### "Do I need to leave my computer on?"

No. Apps Script runs on Google's servers. Your computer can be off. Your browser can be closed. The robot keeps working.

---

## Part 6: What You Do Each Day (Your Only Job)

```
1. Open Google Sheets (5 seconds)
2. Type your post title in column A
3. Type or paste your content in column B
4. Change column E to 'ready'
5. Close the tab
```

That is your entire publishing workflow. Everything else is automatic.

---

## Part 7: Using AI to Help You Write (Claude, ChatGPT, Mistral — Free)

When you cannot find words, these free AI tools write the first draft for you:

### Claude (by Anthropic) — Best for Long-Form Writing
- **Free access:** https://claude.ai (free tier available)
- **What to say:** "Write a 500-word blog post for ELT teachers about [your topic]. Use a warm, personal tone."
- **Then:** Copy the result into your Google Sheet column B. Done.
- **Why it helps:** Claude writes in full paragraphs with nuance — ideal for thoughtful ELT essays

### ChatGPT (by OpenAI) — Best All-Rounder
- **Free access:** https://chat.openai.com (GPT-4o free tier)
- **What to say:** "Write a 500-word blog post about [topic]. Include a practical classroom activity."
- **Why it helps:** Fastest response, very versatile

### Mistral (by Mistral AI) — Best Free Unlimited Option
- **Free access:** https://chat.mistral.ai (Le Chat — fully free, no rate limits as of 2026)
- **What to say:** Same prompts as above
- **Why it helps:** No account limits, very fast, supports French/English/multilingual — perfect for Réunion context
- **Vibe mode:** Mistral has a "Canvas" mode where you can edit AI text directly — like Google Docs + AI in one place

### Google Gemini — Best When You Are Already in Google Drive
- **Free access:** https://gemini.google.com
- **What to say:** "Help me write a blog post about [topic]" then click "Insert into Doc"
- **Why it helps:** Integrates directly with Google Docs and Sheets — no copy-paste needed

### Your Daily AI Workflow (Zero Energy Required)

```
1. Open Mistral or Claude
2. Type: "Write 500 words about [today's teaching topic]"
3. Copy the output
4. Paste into Google Sheet
5. Mark as ready
6. Done. Total time: 4 minutes.
```

On days when even that is too much:
```
1. Open voice recorder on your phone
2. Speak for 3 minutes about anything
3. Upload recording to https://otter.ai (free transcription)
4. Paste transcript into Mistral: "Clean up this rough transcript into a blog post"
5. Copy result to Google Sheet
```

---

## Summary: The Complete System in One Diagram

```
YOU WRITE (or speak) → AI cleans it up → Paste into Google Sheet
                                                    |
                              Apps Script runs every hour
                                                    |
                         WordPress receives post as DRAFT
                                                    |
                    You review (optional) and it publishes
                                                    |
              Buffer/IFTTT auto-shares to social media
```

**Total daily effort required from you: 5-10 minutes on good days. 0 minutes on bad days (drafts queue up for later).**

---

*Last updated: June 2026. Created for Sourov's automated publishing workflow.*
