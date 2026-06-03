# Deployment Guide - From Blog Queue to Live WordPress

How to use the automated system to publish your blog posts to sourovdeb.com.

---

## 🎯 The System

```
Your Essays (GitHub) 
    ↓
Blog Queue (CSV in repo)
    ↓
WordPress Publishing Script (sync_to_wordpress.py)
    ↓
Your Live Blog (sourovdeb.com)
```

---

## 📋 Prerequisites

1. **Blog posts in CSV** - `wordpress_blog_queue.csv` (already created with 15 posts)
2. **Deploy.php secret key** - `0767044896thevenet_` (DO NOT COMMIT THIS)
3. **Environment variable** - `WORDPRESS_DEPLOY_KEY` set to your secret
4. **Python 3** - For running scripts

---

## 🔐 Step 1: Secure Your Credentials

**NEVER commit credentials to GitHub.**

Create `.env.local` file (git-ignored):

```bash
# .env.local (git-ignored, never commit)
export WORDPRESS_DEPLOY_KEY="0767044896thevenet_"
```

Or set in your shell:

```bash
export WORDPRESS_DEPLOY_KEY="0767044896thevenet_"
```

---

## 🚀 Step 2: Test the System (Dry Run)

```bash
# Load credentials
source .env.local

# Preview what would publish (safe to run)
python Tools_and_Scripts/sync_to_wordpress.py --dry-run
```

**Expected output**:
```
Found 15 posts ready to publish
[DRY RUN MODE] - Will preview, not publish

[1/15] Living with Bipolar While Working Remote
  Category: Mental Health
  Tags: bipolar,remote-work...
  [DRY RUN] Would publish to WordPress

... (11 more posts)

Results: 15 published, 0 failed
```

---

## 🌐 Step 3: Publish to WordPress (LIVE)

**Only run this when you're ready to publish.**

```bash
# Publish all approved posts to WordPress
python Tools_and_Scripts/sync_to_wordpress.py --live
```

**What happens**:
1. Script reads `wordpress_blog_queue.csv`
2. Finds all posts with Status=Ready and Approved=TRUE
3. Posts each to WordPress via deploy.php
4. Updates CSV with WordPress Post IDs
5. Changes Status to Published

**Monitor**:
- Watch for ✓ (success) or ✗ (failed) for each post
- Check sourovdeb.com to verify posts are live

---

## 📝 Step 4: Create Your Own Posts

**Add to the CSV:**

1. Open `wordpress_blog_queue.csv` in spreadsheet or text editor
2. Add new row with:
   - Title: Your post title
   - Content: Full post body (can include markdown or HTML)
   - Catagory: Mental Health / Career / Automation / Writing
   - Tags: comma,separated,tags
   - Meta Description: One sentence summary
   - SEO Titie: SEO-optimized title
   - Publish Date: When to publish
   - Status: Draft / Ready (only "Ready" publishes)
   - Approved: FALSE initially (you approve it)

3. When ready: Change Status to "Ready" and Approved to "TRUE"
4. Run: `python Tools_and_Scripts/sync_to_wordpress.py --live`

---

## 🔄 Workflow: Essay → Blog

### Write in GitHub

```bash
# Create essay
cp Essays_and_Blogs/TEMPLATE.md Essays_and_Blogs/2026/06/2026-06-03-my-essay.md

# Edit and write 500 words
vim Essays_and_Blogs/2026/06/2026-06-03-my-essay.md

# Commit
git add Essays_and_Blogs/
git commit -m "Essay: My Topic"
git push
```

### Add to Blog Queue

1. Copy essay content
2. Add to `wordpress_blog_queue.csv`
3. Fill in: Title, Content, Category, Tags, Meta Description
4. Set Status: Ready
5. Set Approved: TRUE

### Publish to WordPress

```bash
python Tools_and_Scripts/sync_to_wordpress.py --dry-run  # Preview
python Tools_and_Scripts/sync_to_wordpress.py --live      # Publish
```

### Verify

Visit: https://www.sourovdeb.com

See your post live? Success! 🎉

---

## 🎓 Real Example

### Your first post:

**Essays_and_Blogs/2026/06/2026-06-03-why-i-write.md**:
```markdown
---
title: Why I Started Writing
category: Personal
tags: writing, mental-health
---

# Why I Started Writing

I write because my story matters...
[rest of essay]
```

**Add to CSV**:
```
Title: Why I Started Writing
Content: I write because my story matters... [full essay]
Category: Personal Philosophy
Tags: writing,mental-health,bipolar,authenticity
Meta Description: Why sharing your mental health story publicly matters.
SEO Title: Why I Started Writing About Mental Health
Status: Ready
Approved: TRUE
```

**Publish**:
```bash
source .env.local
python Tools_and_Scripts/sync_to_wordpress.py --live
```

**Result**: Post live at sourovdeb.com ✓

---

## 🆘 Troubleshooting

### "WORDPRESS_DEPLOY_KEY not set"
```bash
# Set it
export WORDPRESS_DEPLOY_KEY="0767044896thevenet_"

# Or use .env.local
source .env.local
```

### "Script can't find CSV"
```bash
# Make sure you're in the repo directory
cd ~/my_professional_documents

# Run script from there
python Tools_and_Scripts/sync_to_wordpress.py --live
```

### "HTTP error 401"
Deploy.php secret key is wrong. Check:
```bash
echo $WORDPRESS_DEPLOY_KEY
# Should output: 0767044896thevenet_
```

### "Post not appearing on site"
1. Check https://www.sourovdeb.com/wp-admin/edit.php (drafts)
2. Manually publish from admin if needed
3. Check WordPress for error messages

---

## 📊 Monitoring Posts

**Check published posts**:
```bash
# Opens your WordPress admin
open https://www.sourovdeb.com/wp-admin/
```

**Track in CSV**:
```
Post ID column shows WordPress post ID
Status column shows "Published"
Result Log shows any errors
```

---

## 🔁 Schedule Regular Publishing

**Publish new posts daily**:

```bash
# Add to crontab
crontab -e

# Add this line:
0 8 * * * cd ~/my_professional_documents && source .env.local && python Tools_and_Scripts/sync_to_wordpress.py --live
```

This publishes every morning at 8am. Adjust as needed.

---

## ✅ Checklist

- [ ] `.env.local` created with WORDPRESS_DEPLOY_KEY
- [ ] Test run: `python sync_to_wordpress.py --dry-run` succeeds
- [ ] CSV has at least one post with Status=Ready and Approved=TRUE
- [ ] Live run: `python sync_to_wordpress.py --live` succeeds
- [ ] Post appears on sourovdeb.com
- [ ] CSV updated with Post ID

**Once complete: You have automated publishing!**

---

## 🚀 Next Steps

1. **Test**: Run dry-run, verify it works
2. **Write**: Create more essays in Essays_and_Blogs/
3. **Add**: Put essays in wordpress_blog_queue.csv
4. **Publish**: Run sync script
5. **Automate**: Schedule with cron for daily publishing

---

## 📈 Scaling Up

Once this is working:

1. **Add more essays** (same format, repeat process)
2. **Create job alerts** (use job_tracker.py)
3. **Track health** (use Health_and_Wellbeing/Daily_Checklist.md)
4. **Build network** (use Contacts_and_Partnerships/)

Your blog becomes:
- A portfolio (employers see your work)
- An audience (readers find you)
- An income source (speaking, writing gigs, consulting)

All automated. All sustainable.

---

**Ready? Run the dry-run now and see your posts come to life.**
