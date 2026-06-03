# WordPress Ready: Essays Formatted for Publishing

**Essays that are ready or published to sourovdeb.com**

---

## Directory Structure

```
wordpress_ready/
├── staging/          # Essays ready to review + publish
├── published/        # Essays already on WordPress
└── README.md         # This file
```

---

## Workflow

### 1. Draft in blog_drafts/

Write in `blog_drafts/2026_MM_essays/` using the ESSAY_TEMPLATE.md

### 2. Move to Staging (Ready to Publish)

When essay is done and edited:

```bash
# Run the WordPress uploader with --save-only flag
python3 ../automation_scripts/wordpress_uploader.py \
  --file ../blog_drafts/2026_06_essays/your_essay.md \
  --status draft \
  --save-only

# This saves to: wordpress_ready/staging/
```

### 3. Review in Staging

Before publishing:
- [ ] Read on your phone (mobile formatting)
- [ ] Verify all links work
- [ ] Check category & tags are correct
- [ ] Ensure excerpt is compelling

### 4. Publish to WordPress

```bash
python3 ../automation_scripts/wordpress_uploader.py \
  --file staging/20260603_your_title.json \
  --status publish
```

### 5. Move to Published

After confirmed on WordPress:

```bash
mv staging/20260603_your_title.json published/
```

---

## WordPress Categories

Use these categories to keep posts organized:

- **Mental Health** — Bipolar, depression, therapy, medication
- **Productivity** — Automation, tools, workflow, time management
- **Teaching** — CELTA, language education, student management
- **Career** — Job search, remote work, disability at work
- **Disability & Legal** — France/EU resources, accessibility, RQTH
- **Writing & Publishing** — Blogging, content strategy
- **Technology** — Code, tools, automation scripts
- **Personal** — Life stories, reflection, lessons learned

---

## WordPress Tags

Use tags for discoverability (pick 3-5 per post):

### Mental Health Tags
- bipolar, depression, mental-health, manic-episode, therapy, medication, coping-strategies

### Work Tags
- remote-work, job-search, teaching, disability-at-work, accommodation, burnout

### Location/Specific Tags
- france, eu, disability-law, english-teaching, celta

### Topical Tags
- productivity, automation, self-care, consistency, energy-management

---

## SEO & Excerpt Tips

**Excerpt** (160 characters max):
- Say what the post is about in one sentence
- Include a benefit for the reader
- Make it compelling (this shows in search results)

Example:
```
How to manage email when bipolar disorder makes you either ignore it for weeks 
or send regrettable replies at 3 AM. Three rules that actually work.
```

**Title tips:**
- Active, specific language
- Include main keyword (bipolar, remote, CELTA, etc.)
- Make it personal if relevant
- ~60 characters (displays fully in search results)

---

## Publishing Checklist

Before hitting "Publish" on WordPress:

- [ ] Title is compelling and searchable
- [ ] Excerpt is written (160 chars)
- [ ] Category selected (exactly 1)
- [ ] Tags added (3-5 relevant tags)
- [ ] Featured image added (if desired)
- [ ] Body text is formatted properly (headers, bold, links)
- [ ] All links are clickable and correct
- [ ] Read aloud for flow & tone
- [ ] No typos (spellcheck)
- [ ] Mobile-friendly (tested on phone preview)

---

## Publishing Schedule

**Recommended rhythm:**
- Week 1-2: Write 2 essays (4 total)
- Week 3: Finish editing, publish 2
- Week 4: Publish remaining essays, rest

This gives you:
- 3-4 essays published per month
- Time for editing (quality)
- Buffer for low-energy days
- No burnout

---

## Featured Images

Optional but recommended. Where to get free images:

- **Unsplash** — https://unsplash.com (free, beautiful)
- **Pexels** — https://www.pexels.com (free, diverse)
- **Pixabay** — https://pixabay.com (free, many options)

Tips:
- Use consistent color palette (professional look)
- Include your name or logo if possible
- Make sure it relates to the essay topic
- Download at 1200x630 for best WordPress display

---

## Tracking Spreadsheet

Update your Google Sheets tracker when you publish:

| Date | Title | Category | Tags | Status | Views |
|------|-------|----------|------|--------|-------|
| 2026-06-03 | Email Management When Bipolar | Mental Health | bipolar, email, productivity | Published | |

Sheet link: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/

---

## Troubleshooting

**"Essay looks bad on mobile"**
- Shorten paragraphs (2-3 sentences max)
- Check list formatting
- Verify images aren't too wide
- Test on actual phone

**"Links are broken"**
- Make sure URLs include https://
- Check domain spelling
- Test by clicking before publishing

**"Can't upload to WordPress"**
- Verify .env file has DEPLOY_KEY
- Check internet connection
- Try --dry-run first to see what will happen

**"Forgot to add featured image"**
- Edit post in WordPress admin
- Add image in "Featured Image" panel
- Save/update

---

## Next Steps

1. Finish current essay in blog_drafts/
2. Run: `python3 wordpress_uploader.py --file essay.md --save-only`
3. Review in staging/ folder
4. When ready: `python3 wordpress_uploader.py --file staging/essay.json --status publish`
5. Update tracking spreadsheet

---

**Your voice deserves an audience. Publish with care.**
