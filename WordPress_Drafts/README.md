# WordPress Drafts & Publishing

Staging area for essays before they go live on sourovdeb.com.

---

## 📝 Workflow: From Essay to Published

1. **Write** in Essays_and_Blogs/
2. **Copy** to WordPress_Drafts/ (rename with date/slug)
3. **Review** (formatting, links, images)
4. **Publish** (manual copy-paste to WordPress or automation)
5. **Move** to Archives/ after publishing

---

## 📂 Folder Structure

```
WordPress_Drafts/
├── README.md (this file)
├── PUBLISHING_GUIDE.md
├── Ready_for_Publishing/       # Final drafts, ready to go live
│   ├── 2026-06-03-mental-health.md
│   └── 2026-06-04-automation.md
├── In_Progress/                # Being edited/formatted
│   └── 2026-06-05-draft.md
├── Archives/                   # Published (keep as reference)
│   ├── 2025-12-01-past-essay.md
│   └── published_urls.csv      # Track: essay → live link
└── Templates/
    ├── Blog_Post_Template.md
    ├── Metadata_Template.md
    └── WordPress_HTML_Template.html
```

---

## 📋 Publishing Metadata

Every essay needs this metadata before publishing:

```markdown
---
title: "Your Essay Title"
date: 2026-06-03
author: Sourov
category: Mental Health  # or Automation, Career, Philosophy, Wellbeing
tags: [tag1, tag2, tag3]
slug: mental-health-essay
excerpt: "A short 1-2 sentence summary for the blog preview"
featured_image: [URL or 'none']
status: ready_for_publishing
wordpress_id: [leave blank - will fill after publishing]
---
```

---

## 🔄 Publishing Options

### Option 1: Manual (Safest, 5 minutes)
1. Log in to WordPress admin: sourovdeb.com/wp-admin/
2. Click "Posts" → "Add New"
3. Copy essay title to "Post Title"
4. Copy essay body to editor
5. Set Category (dropdown on right)
6. Add Tags (add from sidebar)
7. Set excerpt (optional)
8. Upload featured image if you have one
9. Click "Publish"
10. Copy published URL to `Archives/published_urls.csv`

**Pros**: Safe, you control every detail
**Cons**: Takes time

### Option 2: WordPress REST API (Faster, requires setup)
**File**: `publish_to_wordpress.py`

```bash
python publish_to_wordpress.py \
  --file WordPress_Drafts/Ready_for_Publishing/2026-06-03-essay.md \
  --category "Mental Health" \
  --tags "bipolar,mental-health,personal"
```

**Setup required**:
1. Enable REST API (WordPress → Settings → Permalinks)
2. Create application password in WordPress user settings
3. Store credentials in `.env.local`:
```
WORDPRESS_URL=https://www.sourovdeb.com
WORDPRESS_USER=your_username
WORDPRESS_APP_PASSWORD=your_app_password
```

**Pros**: Automation, consistent formatting
**Cons**: Requires setup, less control

### Option 3: Your Custom deploy.php Gateway (Most Automated)
You already have a deploy.php with a secret key. We can extend it:

```bash
curl -X POST https://www.sourovdeb.com/deploy.php \
  -H "Content-Type: application/json" \
  -d '{
    "action": "publish_post",
    "key": "0767044896thevenet_",
    "title": "Essay Title",
    "content": "... essay markdown here ...",
    "category": "Mental Health",
    "tags": ["bipolar", "mental-health"]
  }'
```

**Pros**: No setup (you already have it), very fast
**Cons**: Requires custom PHP code in deploy.php

---

## 🎨 Formatting for WordPress

### Markdown → WordPress HTML

WordPress accepts both:
- Plain text with line breaks
- HTML formatting
- Markdown (if plugin installed)

**Convert markdown to WordPress HTML**:
```bash
# Use Pandoc (if installed)
pandoc 2026-06-03-essay.md -t html > essay.html

# Or use online converter: pandoc.org/try
```

### Recommended WordPress Formatting

Use these WordPress blocks:
- **Paragraph** for body text
- **Heading 2** for section headers
- **Quote** for important points
- **List** for bullets/numbers
- **Image** if you have visuals

---

## 🏷️ Categories & Tags

### Categories (pick ONE):
- **Mental Health** - Bipolar, depression, therapy, self-care
- **Career & Jobs** - Remote work, teaching, applications, interviews
- **Automation & Tools** - Scripts, open-source, productivity
- **Personal Philosophy** - Essays on life, learning, growth
- **Wellbeing** - Sleep, exercise, nutrition, habits
- **Technical Writing** - How-to guides, learning resources

### Tags (pick 3-5):
- Personal: `bipolar`, `depression`, `mental-health`, `therapy`
- Career: `remote-work`, `teaching`, `english`, `jobs`, `career-change`
- Tools: `automation`, `open-source`, `python`, `wordpress`, `gmail`
- Topics: `sleep`, `consistency`, `writing`, `networking`, `productivity`

---

## 📸 Featured Images

For each essay, optionally add a featured image:

**Where to find free images**:
- Unsplash (unsplash.com) - High quality, free
- Pexels (pexels.com) - Free stock photos
- Pixabay (pixabay.com) - Free illustrations
- Canva (canva.com) - Design + resize images

**If using images**:
1. Download image
2. Upload to WordPress media library (or Unsplash URL)
3. Set as featured image before publishing

---

## 📊 Post-Publishing Checklist

After publishing:
1. [ ] Click the published link to view live
2. [ ] Check formatting (paragraphs, headings, links)
3. [ ] Verify category and tags appear
4. [ ] Check mobile view (responsive)
5. [ ] Share on social (Twitter, LinkedIn, email)
6. [ ] Update `Archives/published_urls.csv`:

```csv
Date,Title,URL,Category,Tags,Views_Target
2026-06-03,"Mental Health Essay",https://www.sourovdeb.com/mental-health-essay,Mental Health,"bipolar,personal",100
```

---

## 📈 Tracking Performance

After a few posts, analyze:

**File**: `Archives/performance_tracking.csv`

```csv
Title,Date_Published,Views_1Week,Comments,Shares,Category
"Mental Health Essay",2026-06-03,25,2,0,Mental Health
```

Use this to understand:
- Which topics get most views?
- Which categories perform best?
- What time of week gets more traffic?
- Which essays get comments?

---

## 🔐 Credentials (CRITICAL)

**NEVER store in this repo**:
- WordPress username/password
- Application password
- deploy.php secret key

**Store instead**:
- `.env.local` (git-ignored)
- Environment variables
- OS credential manager
- KeePass/Bitwarden

**When copying files to WordPress, remove any credentials from the file content.**

---

## 🆘 Troubleshooting

**WordPress login not working**
- Check caps lock on password
- Reset password from WordPress login page
- Clear browser cookies/cache

**Essay formatting broken in WordPress**
- Copy as plain text, not HTML
- Re-format in WordPress editor
- Use WordPress blocks instead of HTML

**REST API not working**
- Check application password is enabled in WordPress user settings
- Verify permalinks are NOT set to "Plain"
- Test API from WordPress itself: wp-json/wp/v2/posts

**Images not uploading**
- Check WordPress media permissions
- File size < 10MB
- File type: JPG, PNG, GIF only

---

## 📋 Quick Checklists

### Before Publishing
- [ ] Essay is 500 ± 50 words
- [ ] Title is catchy (5-8 words)
- [ ] First paragraph hooks reader
- [ ] Actionable takeaway at end
- [ ] All claims sourced
- [ ] No typos/grammar issues
- [ ] Metadata filled in (category, tags, excerpt)

### Publishing
- [ ] Category selected
- [ ] Tags added (3-5)
- [ ] Featured image set (optional)
- [ ] Excerpt written (one sentence)
- [ ] Publish button clicked
- [ ] View post live
- [ ] Share on social

### After Publishing
- [ ] Add to performance tracking sheet
- [ ] Move file to Archives/
- [ ] Update Google Drive sheet (status: published, add URL)
- [ ] Plan next essay

---

## 🚀 Quick Start

1. **Option 1 (Manual)**: Copy essay to WordPress manually (5 min)
2. **Option 2 (API)**: Set up REST API credentials and run Python script
3. **Option 3 (Deploy.php)**: Extend deploy.php for posting

Choose **Option 1** for now (simplest, safest).

Then start writing. The publishing system exists to support you, not block you.

---

**Remember**: Your story matters. Publish it. Let people hear your voice.**
