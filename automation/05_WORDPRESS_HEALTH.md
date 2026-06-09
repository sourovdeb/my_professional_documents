# WordPress Health, Categories & Tags
## Audit, Fix, and Maintain Your Site

---

## Why Categories and Tags Matter

**Categories** are the main sections of your blog (e.g., Grammar, Listening, CELTA).
Every post should have exactly one primary category.

**Tags** are keywords that describe post content (e.g., pronunciation, lesson-plan, beginner).
Ideal: 3–8 tags per post.

**Common problems:**
- Posts stuck in "Uncategorized"
- No tags at all
- Duplicate categories ("ELT" and "ELT Masterclass" both exist)
- Wrong category (grammar post in ELT Masterclass)

---

## Quick Audit — What's Broken

Run `scripts/wordpress_health_check.py` to get a full report:

```bash
python scripts/wordpress_health_check.py
# Output:
# Total posts: 47
# Posts with no tags: 12
# Posts in Uncategorized: 8
# Duplicate categories: ELT, ELT Masterclass
# Posts with no SEO meta: 31
```

---

## Auto-Fix with AI

Run `scripts/wordpress_category_tag_fix.py` to fix all issues:

```bash
python scripts/wordpress_category_tag_fix.py
# Scans all posts
# For each post with missing tags/category:
#   → sends title+content to DeepSeek
#   → gets back: tags, category, SEO title, meta description
#   → updates via WordPress REST API
```

---

## Recommended Category Structure

For an ELT/teaching blog:

```
ELT Masterclass (parent)
├── Grammar
├── Listening & Phonology
├── Speaking & Fluency
├── Writing & Vocabulary
├── CELTA
└── Lesson Planning

About
Health & Wellbeing
Technology
```

Create these via WP Admin → Posts → Categories

---

## WordPress Maintenance Checklist

Run monthly:

```bash
# Via WP-CLI (if SSH access available)
wp core update
wp plugin update --all
wp theme update --all
wp cache flush
wp db optimize
wp cron event run --due-now

# Check for broken links
wp post list --format=csv | python scripts/check_links.py
```

Via admin panel:
- [ ] Dashboard → Updates (update everything)
- [ ] Tools → Site Health → fix all issues
- [ ] Settings → Discussion → disable comments on old posts
- [ ] Media → Regenerate thumbnails after theme changes

---

## Backup Strategy

```bash
# UpdraftPlus plugin (free) — set to backup weekly to Google Drive
# Or via WP-CLI:
wp db export backup_$(date +%Y%m%d).sql
tar -czf wordpress_$(date +%Y%m%d).tar.gz /path/to/wordpress/
```

---

## SEO Meta Fix

If you use Yoast SEO, fix missing meta in bulk:

```python
# Run: python scripts/wordpress_category_tag_fix.py --seo-only
# Updates _yoast_wpseo_metadesc and _yoast_wpseo_title for all posts
# that don't already have them set
```

---

## Monitoring WordPress Health Automatically

Add to crontab (checks site health weekly):
```bash
0 9 * * 1 python /path/to/scripts/wordpress_health_check.py | mail -s "WP Health Report" your@email.com
```

Or use GitHub Actions (see `.github/workflows/publish_on_push.yml`).
