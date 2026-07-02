# sourovdeb.com — Site Audit & Changes — 2026-07-02

## Status Summary
All custom plugins: **active and healthy**
Theme: Astra child theme ("Sourov" v1.1)
SEO: Yoast SEO + IndexNow notifier active
LiteSpeed Cache: v7.8.1 active
Google/Bing: dual sitemaps at `/sitemap_index.xml` and `/wp-sitemap.xml`, robots.txt clear

---

## Changes Made

### 1. sourov-site-enhancer upgraded to v2.0.0

**File:** `wp-content/plugins/sourov-site-enhancer/sourov-site-enhancer.php`

**Previous version (1.0.0) had:**
- ELT365 series navigation (prev/next day)
- YouTube/podcast meta box (`_ssd_yt`, `_ssd_pod` fields)
- YouTube/podcast embed above post content
- Simple "Further Reading" list (plain `<ul>`)

**New features in v2.0.0:**
- **YouTube Channel CTA** — appears at the bottom of all English Teaching (cat 9), Philosophy (cat 581), and Mental Health (cat 582) posts when no specific video is set. Links to Treasure Hunters Digital (UC1rs5aY7YdFiADKkhOMPCvQ).
- **Styled related posts grid** — replaced plain list with responsive card grid showing category label, post title, and date. Header changed from "Further Reading" to "You Might Also Like".
- **Podcast audio player** — if the podcast URL is an MP3/audio file, shows a native `<audio>` player instead of just a link.
- **YouTube sidebar widget** — `SSD_YouTube_Widget` class registered. Add via Appearance > Widgets > "Sourov — YouTube Channel".
- **Shortcodes:**
  - `[sourov_youtube video_id="XXXXXXXXXXX"]` — responsive 16:9 embed
  - `[sourov_podcast src="URL" title="Episode Title"]` — native audio player
- **Improved CSS** — all new components styled via the `#ssd-styles` block in `wp_head`.

**No changes to existing meta keys** (`_ssd_yt`, `_ssd_pod`) or series navigation logic.

---

### 2. Page Content Updates

#### About Me (page ID: 35)
- Added "Find Me Online" section with styled card grid (YouTube, WhatsApp, Email)
- Added "Book a Session via WhatsApp" CTA button

#### Resources (page ID: 1077)
Appended new sections:
- **My YouTube Channel** — prominent link to Treasure Hunters Digital
- **More English Resources** — 7 additional tools (Oxford Learner's, Merriam-Webster, EnglishClub, WordReference, News in Levels, ELLLO, Academic Word List)
- **More Philosophy Resources** — 5 additions (Philosophize This! podcast, Aeon Magazine, The School of Life, Philosophy Talk, Plato on Gutenberg)
- **More Mental Health Resources** — 7 additions (Verywell Mind, Psychology Today, ADDitude, CHADD, The Mighty, Crisis Text Line, ADAA)
- **Productivity & Learning Tools** — new section: Anki, Quizlet, DeepL, Hemingway Editor, Natural Reader

#### Philosophy & Mental Health (page ID: 1076)
- Appended index of published Philosophy essays (category 581)
- Appended index of published Mental Health essays (category 582)
- Added link to My Mental Health Journey page

---

### 3. Journal Pages Fixed

| Page | Slug | Action |
|---|---|---|
| Creator & Life (ID 2616) | journal-creator-life | Added 180-word intro about YouTube growth, creator business, personal stories |
| Photography & Software (ID 2614) | journal-photo-software | Added 160-word intro about photo editing and software tools |
| Articles (ID 2752) | articles (sub-page of Europe Travel) | Set to **draft** — thin page (25 words), redundant with parent page |

---

### 4. Plugins Deployed Then Deactivated

Two plugins (`sourov-series-related`, `sourov-youtube-integration`) were initially deployed but deactivated because `sourov-site-enhancer` already covered the same functionality. Their code was merged into the site-enhancer v2 upgrade instead. Plugin files remain on server but are inactive.

---

## What Still Needs Manual Attention

### Homepage creativity
The homepage uses **Latest Posts** mode (not a static page). The theme (Astra child) controls the layout. To make it more creative:
- **Option A**: Switch to a static front page in Settings > Reading and build a custom homepage via the WP admin editor.
- **Option B**: Install Astra Pro's Homepage Builder for drag-and-drop layout.
- **Option C**: Add widgets to the homepage widget area via Appearance > Widgets if the theme supports it.

### YouTube sidebar widget
Go to **Appearance > Widgets** and add the **"Sourov — YouTube Channel"** widget to the sidebar. This was registered by the site-enhancer v2 but must be placed manually from the admin panel.

### Post-specific YouTube videos
In WP Admin, edit any post and fill in the **"YouTube URL"** field in the sidebar meta box (labelled "📺 YouTube · 🎙 Podcast") to embed a specific video at the top of that post. The channel CTA appears automatically on all content posts without a specific video.

---

## YouTube Channel
- **Channel ID:** UC1rs5aY7YdFiADKkhOMPCvQ
- **Channel Name:** Treasure Hunters Digital
- **URL:** https://www.youtube.com/channel/UC1rs5aY7YdFiADKkhOMPCvQ
- **Integration:** Channel CTA appears on all English Teaching, Philosophy, and Mental Health posts automatically (via site-enhancer v2). Sidebar widget available for manual placement.

---

## SEO / Google-Bing Compatibility Check

| Item | Status |
|---|---|
| Yoast SEO plugin | ✅ Active |
| XML Sitemap | ✅ `/sitemap_index.xml` + `/wp-sitemap.xml` |
| IndexNow notifier | ✅ `aicu-engine-reach.php` — fires on every publish |
| robots.txt | ✅ No blocks, both sitemaps declared |
| Internal backlinks | ✅ Fixed — related posts + series nav on all single posts |
| LiteSpeed Cache | ✅ v7.8.1 active |
| WP_DEBUG | ⚠️ Disabled (correct for production — only enable in development) |
| Categories | ✅ All posts have categories assigned |
| Tags | ✅ All published posts have tags |
