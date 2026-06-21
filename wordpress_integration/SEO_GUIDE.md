# 📊 WordPress SEO Guide for sourovdeb.com

How to write essays that rank on Google and get readers.

---

## Before Publishing (SEO Checklist)

### Title (Most Important)
- [x] Includes your main keyword
- [x] Under 60 characters (so it fits in Google)
- [x] Active voice ("5 Ways to..." not "Ways That Can Help...")
- [x] Specific and clear (not vague)

**Good:** "How Disability Shaped My Writing Career"  
**Bad:** "My Life" or "Thoughts on Writing"

### Meta Description (The 160-char Preview)
```yaml
description: "I discovered disability wasn't a barrier to writing—it became my unique voice. Here's how I built my platform while managing my condition."
```

- [x] Under 160 characters
- [x] Includes main keyword early
- [x] Answers a question or creates curiosity
- [x] No keyword stuffing ("disability disability disability...")

**Good:** "Disability taught me resilience. Here's how I built a writing career while managing chronic pain—and how you can too."  
**Bad:** "This article discusses disability and writing and career tips for disabled writers with disability."

### Keywords/Tags
```yaml
tags: "disability, writing, career, chronic pain, accessibility"
focus_keyword: "disability writing"
```

- [x] 3-5 tags per essay
- [x] One main focus keyword
- [x] Related but not identical (long-tail keywords)
- [x] Natural language (as people search)

**Search people actually make:**
- "disability writing career"
- "chronic pain writing"
- "accessible writing tips"
- "disabled writer freelance"

Find these using AnswerThePublic.com (free).

### Content Structure
```markdown
# Main Title (includes keyword)

**First paragraph** — This is your 160-char preview.
Keyword should appear in first 100 words.

## Section 1: The Problem/Hook
## Section 2: Your Angle
## Section 3: Actionable Insight
## Conclusion: Call to Reflection

[Optional: Internal link to another essay]
```

- [x] Keyword in title + first 100 words + conclusion
- [x] Clear headings (H2, H3 hierarchy)
- [x] Short paragraphs (2-3 sentences)
- [x] 1-2 internal links (to other essays on your site)
- [x] Active voice > Passive voice

### Images (Boosts Engagement)
```markdown
![Alt text describing image](image-url)
```

- [x] Add featured image (optional but helps)
- [x] Alt text: "A disabled writer at desk working on laptop"
- [x] Size: 1200x675px (16:9 ratio)
- [x] JPG/PNG, < 100KB file size

**Where to find free images:**
- Unsplash.com
- Pexels.com
- Pixabay.com

### Links (Internal & External)
- [x] Link to 1-2 of your other essays (internal)
- [x] Link to authority sources (external)
- [x] Natural anchor text ("This technique helped me...")
- [x] Links open in new tab for external

**Good:** `[Read my essay on accessibility](https://www.sourovdeb.com/essays/accessibility)`  
**Bad:** `[click here](https://www.sourovdeb.com/essays/accessibility)`

### Readability
Use `wordpress_integration/wp_publisher.py` which checks:
- [x] Sentence length (avg < 20 words)
- [x] Paragraph length (max 5 sentences)
- [x] Passive voice (flag percentage)
- [x] Adverb overuse
- [x] Complex jargon

**Or use:** Hemingway Editor (hemingwayapp.com)

---

## Publishing Command (With SEO)

```bash
python3 wordpress_integration/wp_publisher.py \
  --file daily_essays/2026-06-02_disability_writing.md \
  --category Writing \
  --tags "disability,writing,career,chronic pain" \
  --publish
```

This automatically:
✅ Extracts SEO metadata from frontmatter  
✅ Sets meta description under 160 chars  
✅ Adds focus keyword to Yoast/RankMath  
✅ Categorizes and tags post  
✅ Optimizes for Google  

---

## After Publishing (Post-Optimization)

### Google Search Console
1. Go to search.google.com/search-console
2. Select your site: sourovdeb.com
3. **Performance** tab → See:
   - Which keywords you're ranking for
   - Which essays get impressions
   - Click-through rate (CTR)

### Fix Issues:
- Ranking but low CTR? → Improve meta description
- Not ranking at all? → Better keywords, more backlinks
- 404 errors? → Fix broken internal links

### Action Items:
```
If essay gets 100+ impressions but < 2% CTR:
→ Rewrite meta description (make it more clickable)

If essay gets 0 impressions in 1 month:
→ Improve keyword targeting (search AnswerThePublic)
→ Build backlinks (share on social)
```

### Google Analytics
1. analytics.google.com → Your site
2. Check:
   - Avg. time on page (> 2 mins is good)
   - Bounce rate (< 50% is good)
   - Conversion (if you have CTA like newsletter)

**Top performing essays** → Write more like them  
**Low performing** → Don't delete; wait 3-6 months (SEO is slow)

---

## Backlinks (Get Other Sites to Link to You)

**Why:** Google sees backlinks as "votes of confidence"

### Where to Get Backlinks:
1. **Social media** — Share essays on LinkedIn, Twitter
2. **Guest posts** — Write for other blogs, link back
3. **Comments** — Comment on other blogs with link to relevant essay
4. **Collaborations** — Work with other writers (cross-link)
5. **Directories** — Add to writing directories (Medium, Dev.to)

### Quality > Quantity:
**1 backlink from authority site > 10 from random blogs**

---

## SEO Timeline

**Week 1-2 after publish:**
- No Google traffic expected
- Manual share on social

**Week 3-4:**
- Start appearing in Google for long-tail keywords
- May get 5-20 organic visits

**Month 2-3:**
- Ranking for main keyword
- 50-200 organic visits
- May get backlinks naturally

**Month 4+:**
- Established ranking
- Consistent traffic
- More authority

**Patience:** SEO is not fast. But it's free & compounding.

---

## Common SEO Mistakes (Avoid These)

❌ **Keyword stuffing**
```markdown
# Disability Writing Disability Writing Disability Tips
```
✅ **Natural keyword usage**
```markdown
# How Disability Shaped My Writing Career
```

❌ **Wrong title length**
```markdown
# This is an extremely long title that talks about everything in the article including all the keywords
```
✅ **Good title length**
```markdown
# Disability Writing: Building Your Platform While Managing Your Health
```

❌ **Generic tags**
```yaml
tags: "article, writing, life"  # Too broad
```
✅ **Specific tags**
```yaml
tags: "disability writing, chronic pain, career, accessibility"  # Specific
```

❌ **No internal links**
(Essays isolated from each other)

✅ **Internal linking strategy**
(Each essay links to 1-2 related essays)

---

## Advanced SEO (After 10+ Essays)

### Google Rich Snippets
- Format posts with structured data (schema.org)
- Let WordPress/Yoast handle this automatically
- Helps Google understand your content

### Sitemap
- WordPress auto-generates: sourovdeb.com/sitemap.xml
- Check in Google Search Console
- Manually submit if needed

### Robots.txt
- Tell Google which pages to crawl
- WordPress handles this
- No action needed

### Page Speed
- Most readers on mobile
- Google ranks faster sites higher
- Check: PageSpeed Insights (pagespeed.web.dev)

**If slow:**
- Compress images (TinyPNG.com)
- Use caching plugin (WP Super Cache)
- Remove unused plugins

---

## Monitoring Script

```bash
#!/bin/bash
# Check your blog's SEO health monthly

echo "📊 SEO Check for sourovdeb.com"
echo "Essays published: $(ls daily_essays/*.md | wc -l)"
echo "Keywords tracking: (check Google Search Console)"
echo "Avg CTR: (check Google Search Console)"
echo ""
echo "Action items:"
echo "1. Go to search.google.com/search-console"
echo "2. Check 'Performance' tab"
echo "3. Improve low-CTR pages (rewrite meta desc)"
echo "4. Share high-traffic essays again"
```

---

## Your Competitive Advantage

You're writing about:
- ✅ Disability + tech/writing (niche!)
- ✅ Personal lived experience (authentic)
- ✅ Actionable insights (useful)
- ✅ Consistently (trust signal)

**Why you'll rank:**
- Unique perspective (few disability writers)
- Consistent publishing (Google loves active sites)
- Real audience (people searching for this)
- Growing backlinks (collaborations + sharing)

---

## Checklists

### Pre-Publish Checklist (Use Every Time)
```markdown
Title:
- [ ] Includes main keyword
- [ ] < 60 characters
- [ ] Active voice
- [ ] Clear & specific

Description:
- [ ] < 160 characters
- [ ] Includes keyword
- [ ] Answers a question or creates curiosity

Content:
- [ ] Keyword in title, first 100 words, conclusion
- [ ] 500+ words (Yoast likes length)
- [ ] Clear headings (H2, H3)
- [ ] 1-2 internal links
- [ ] No passive voice heavy sections
- [ ] Active voice > 80%

Tags:
- [ ] 3-5 specific tags
- [ ] One focus keyword
- [ ] Long-tail keywords

Finalization:
- [ ] Hemingway Editor: clear & simple
- [ ] Grammarly: no grammar errors
- [ ] Copyscape: no accidental duplicate content
- [ ] Spellcheck: no typos
```

### Post-Publish Checklist
```markdown
Day 1 after publish:
- [ ] Essay live on WordPress
- [ ] Share on LinkedIn, Twitter, Facebook
- [ ] Add to LATEST.md in daily_essays/
- [ ] git commit + push

Week 2:
- [ ] Check Google Search Console
- [ ] Fix any indexing issues
- [ ] Get backlinks (guest posts, collaborations)

Month 1:
- [ ] Check analytics
- [ ] See if ranking for keywords
- [ ] Read comments (if any)
```

---

## Tools You Need

| Tool | Purpose | Free? |
|------|---------|-------|
| Google Search Console | Monitor rankings | ✅ Yes |
| Google Analytics | Track visitors | ✅ Yes |
| AnswerThePublic | Find keywords | ✅ Free tier |
| Hemingway Editor | Readability | ✅ Yes (web) |
| Yoast SEO | WordPress plugin | ✅ Free version |
| Copyscape | Plagiarism check | ⚠️ Limited free |

---

## Your SEO Goal (6 Months)

**Month 1-2:** Build base (10+ essays)  
**Month 3:** Get first organic traffic (100 visitors)  
**Month 4:** Rank for long-tail keywords (200+ visitors)  
**Month 5:** Build authority (400+ visitors)  
**Month 6:** Establish niche leadership (800+ visitors, backlinks, collaborations)

---

## Remember

> **Quality > Rankings**
>
> Write for humans first, search engines second.
> Good essays rank eventually.
> Bad essays never rank, no matter what.

Focus on: **authentic voice + useful content + consistency**

The SEO will follow.

---

**Last Updated:** 2026-06-02  
**Next Review:** 2026-07-02
