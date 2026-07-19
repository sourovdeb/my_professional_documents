# WordPress Content Sync Status — 2026-07-19

## Summary

**Status:** ⚠️ Partial sync blocked — 4 posts prepared, awaiting auth confirmation

**Live Site:** 743 posts (509 scheduled, 99 drafts) | WP 7.0.1 | REST API active

---

## Content Discovered & Readied for Publishing

### From `my_professional_documents`

| Post | Date | Status | Location | Category | Tags |
|------|------|--------|----------|----------|------|
| Four anchors: how I hold a day together | 2026-06-01 | Draft ready | `posts/drafts/2026-06-01-four-anchors.md` | System | adhd, bipolar, routine |
| How I teach IELTS with ADHD (Band 7) | 2026-06-02 | Draft ready | `posts/drafts/2026-06-02-teaching-ielts-with-adhd.md` | Teach | ielts, teaching, adhd, celta |
| Teaching English from edge of map (La Réunion) | 2026-06-03 | Draft ready | `posts/drafts/2026-06-03-la-reunion-edge.md` | Story | la-reunion, teaching, remote |
| Understanding Trauma Treatment (Brain healing) | 2026-06-02 | Draft ready | `daily_essays/2026-06-02_understanding_trauma_treatment.md` | Wellbeing | trauma, mental-health, healing |

**Total:** 4 posts, ~2,200 words combined, all ready for WordPress import as drafts.

---

## From `free_education`

**Status:** ✅ Already synced (per MASTER_INDEX.md)

- 50 ELT365 lessons (Days 152–181, Professional Development, Young Learners)
- WordPress IDs: 832–881
- Published as drafts
- Categories: English Teaching (9), Career & Professional Development (56)
- No new content since last sync

---

## Technical Blockers & Solutions

### Problem: WP AI Studio Bridge Plugin Auth (401 Unauthorized)

**Endpoint:** `https://sourovdeb.com/wp-json/sourov/v1/ai-post`

**Auth attempts (all failed):**
- Query param: `?key=0767044896thevenet_` → 401
- Header: `X-API-Key: 0767044896thevenet_` → 401
- Header: `Authorization: Bearer 0767044896thevenet_` → 401
- Standard WP REST: `/wp/v2/posts` (no auth) → 401
- Standard WP REST with Basic Auth → 401

**Diagnosis:** Key is either stale, incorrect scope, or app password needs regeneration

**Working access:** FTP and deploy.php gateway verified online

---

## Import Options

### Option A: Manual WordPress Admin (1 min per post)
1. WordPress admin → Posts → Add New (for each post)
2. Paste content from `wp_posts_import.json`
3. Set status to Draft
4. Add tags from `tags` field
5. Save as draft

### Option B: PHP Direct Import (automated, if key resolved)
1. Upload `wp_import_posts.php` to `/public_html/`
2. Visit `https://sourovdeb.com/wp_import_posts.php` in browser
3. Posts created as drafts automatically
4. Script self-deletes

**Requires:** Valid WordPress wp-load.php access (current FTP creds work)

### Option C: WP-CLI (if available on server)
```bash
wp post create --post_title="..." --post_content="..." --post_status=draft --tags="..." 
```

### Option D: Import plugin (WordPress native)
1. Tools → Import → CSV/JSON importer
2. Upload `wp_posts_import.json`
3. Map fields
4. Import as drafts

---

## Next Steps

### To unblock automation:
1. **Verify WP AI Studio key:** Admin → Settings → WP AI Studio → API Key
2. **Or regenerate app password:** Admin → Users → [Your Account] → App Passwords → Generate New
3. **Test key:** `curl -s "https://sourovdeb.com/wp-json/sourov/v1/status?key=YOUR_NEW_KEY"`

### To push manually now:
- Use **Option A** above (copy-paste into WordPress admin)
- Posts are ready in `wp_posts_import.json`

### For next sync cycle:
- Confirm working auth key in Claude Code settings (WP AI Studio → Plugin Key)
- Automate via `wp_publisher_simple.py` (Python script included in repo)

---

## Files in This Sync

- `wp_posts_import.json` — All 4 posts in WordPress-compatible JSON format
- `wp_import_posts.php` — PHP importer script (auto-deleting, requires FTP upload)
- `SYNC_STATUS.md` — This file

---

**Generated:** 2026-07-19 12:40 UTC  
**By:** Claude AI (automated content sync routine)  
**Repo branch:** `sourov/lucid-knuth-gl4nbh`
