# SOUROV DEB — SYSTEM HANDOVER
**Site:** sourovdeb.com | **Owner:** Sourov DEB | sourovdeb.is@gmail.com | sourovdeb@zohomail.com
**Date:** 2026-05-25 | **Status:** ✅ Production Ready

---

## 1. FILE MANAGER ACCESS (How to Deploy Anything)

### Primary Gateway — deploy.php (NO FTP client needed)
```
URL:    https://www.sourovdeb.com/deploy.php
Secret: 0767044896thevenet_
```

**Commands:**
```bash
# Upload file
CONTENT=$(base64 -w 0 < file.php)
curl -X POST "https://www.sourovdeb.com/deploy.php?key=0767044896thevenet_" \
  --data-urlencode "action=upload" \
  --data-urlencode "path=wp-content/plugins/filename.php" \
  --data-urlencode "encoded=true" \
  --data-urlencode "content=$CONTENT"

# List directory
curl "https://www.sourovdeb.com/deploy.php?action=list&key=0767044896thevenet_&path=wp-content/plugins/"

# Download file
curl "https://www.sourovdeb.com/deploy.php?action=download&key=0767044896thevenet_&path=wp-content/plugins/filename.php" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Delete file
curl -X POST "https://www.sourovdeb.com/deploy.php?key=0767044896thevenet_" \
  --data-urlencode "action=delete" \
  --data-urlencode "path=public_html/filename.php"

# Status check
curl "https://www.sourovdeb.com/deploy.php?action=status&key=0767044896thevenet_"
```

### Path Mapping (Critical)
```
deploy path=wp-content/X    → /public_html/wp-content/X    (plugins, themes)
deploy path=public_html/X   → /public_html/public_html/X   (WordPress root files)
deploy path=wp-config.php   → /public_html/wp-config.php   (server root)
```

### FTP (Backup — use deploy.php instead)
```
Host:     ftp.sourovdeb.com
User:     u839078121.sourov
Password: 0767044896Thevenet_
Port:     21
```

### Hostinger Server
```
Document Root: /home/u839078121/domains/sourovdeb.com/public_html/
WordPress:     /home/u839078121/domains/sourovdeb.com/public_html/public_html/
IP:            92.249.46.84
PHP:           8.3.30
Memory:        1024M
SSL:           Lifetime (never expires)
```

### Database
```
Name:     u839078121_rUgwv
User:     u839078121_gVGpV
Password: SrVzfCi7jv
Host:     127.0.0.1
Prefix:   wp_
```

### WordPress Admin
```
URL:    https://sourovdeb.com/wp-admin
Email:  sourovdeb@zohomail.com
```

### DNS (Namecheap — not Hostinger)
```
Provider:  namecheap.com
A Record:  @ → 92.249.46.84
CNAME:     www → sourovdeb.com.
TXT:       @ → google-site-verification=8KvpLQQ5kQqr418svxq6YyW... (Google)
```

---

## 2. WORKFLOW — How It All Works

```
CONTENT CREATION (You)
  ↓
Google Sheet: "WordPress Publishing Queue"
Sheet ID: 1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE
Tab: Sheet1
  ↓
Set column "Approved" = TRUE
  ↓
Apps Script (WP_PUBLISHING_QUEUE.gs) triggers
  ↓
REST API call → sourov-ai-controller.php
Endpoint: POST /wp-json/sourov/v1/ai-post
Auth: X-Sourov-Key: 0767044896thevenet_
  ↓
Post created/scheduled in WordPress
  ↓
aicu-engine-reach.php auto-pings IndexNow
(Notifies Bing, Yandex, Naver instantly)
  ↓
Yoast SEO updates sitemap
  ↓
LiteSpeed Cache clears once
  ↓
Post live + indexed within 24-48h
```

### Google Sheet Columns (Sheet1)
```
A: Title          → WordPress post title
B: Content        → Post body (HTML ok)
C: Category       → Category name
D: Tags           → Comma-separated tags
E: Meta Description → Yoast meta description
F: SEO Title      → Yoast SEO title
G: Publish Date   → ISO date (future = scheduled) or blank (immediate)
H: Status         → Written back: Published / Scheduled / ERROR
I: Approved       → TRUE triggers publish ← YOUR TRIGGER
J: Post ID        → Written back by script
K: Result Log     → Timestamp + status written back
```

### Apps Script
```
File: WP_PUBLISHING_QUEUE.gs
Project: https://script.google.com/home/projects/1NCi2zMmZqUtGsEORwx2kjh8CS8inwdcjwnhUagDESfNqIv6T6rDsyK1N/edit
SHEET_NAME: Sheet1
WP_ENDPOINT: https://www.sourovdeb.com/wp-json/sourov/v1/ai-post
WP_API_KEY:  0767044896thevenet_
```

---

## 3. PLUGIN ROLES (What Each Does)

### sourov-ai-controller.php (v1.1) — PUBLISHER
```
Role:    Creates/schedules WordPress posts via REST API
Auth:    X-Sourov-Key header
Endpoints:
  POST   /wp-json/sourov/v1/ai-post     ← Main publishing endpoint
  GET    /wp-json/sourov/v1/scheduled   ← List scheduled posts
  POST   /wp-json/sourov/v1/bulk        ← Bulk publish array
  DELETE /wp-json/sourov/v1/post/{id}   ← Delete post
  GET    /wp-json/sourov/v1/status      ← Health check (public)
Hook priority: 20 (conflict-safe)
```

### aicu-engine-reach.php (v1.0.0) — INDEXER
```
Role:    Auto-notifies search engines on every publish/update/delete
Method:  IndexNow protocol (Bing, Yandex, Naver, Seznam, Yep)
IndexNow key: 61844e81205e89682bc4562b4b690e3a
Key URL: https://sourovdeb.com/61844e81205e89682bc4562b4b690e3a.txt
Also:    Injects JSON-LD schema, manages robots.txt, serves llms.txt
Note:    Google uses Search Console separately (already verified)
```

### sourov-automation-agent.php — VERIFIER
```
Role:    Manages search engine verification meta tags
Admin:   WordPress → Automation → Bing & Other
Status:  Bing tag injected ✅ | Google verified via DNS ✅
Endpoints: /wp-json/sourov-automation/v1/*
```

### sourov-diagnostic-agent.php — MONITOR
```
Role:    Read-only system monitoring (never modifies anything)
Endpoints (all public):
  /wp-json/sourov-diagnostic/v1/health     ← Quick health check
  /wp-json/sourov-diagnostic/v1/wordpress  ← WP version, posts, users
  /wp-json/sourov-diagnostic/v1/plugins    ← All plugins + status
  /wp-json/sourov-diagnostic/v1/cache      ← Cache status
  /wp-json/sourov-diagnostic/v1/errors     ← Last 50 error log lines
  /wp-json/sourov-diagnostic/v1/report     ← Full report (all above)
```

### aicu-engine-reach.php ALSO handles:
- robots.txt AI bot rules (appended to Yoast's block)
- JSON-LD Article/Author/Organization schema
- llms.txt (list of recent posts for AI models)

### Third-party plugins (do not touch):
```
litespeed-cache        → Page caching (LiteSpeed server)
wordpress-seo (Yoast)  → XML sitemaps, meta tags
google-site-kit        → Google Analytics integration
google-analytics       → MonsterInsights Analytics
astra-sites            → Theme starter templates
```

---

## 4. SEARCH ENGINE STATUS

```
Google Search Console: ✅ Verified (DNS TXT record)
  Property: https://sourovdeb.com
  Verification: TXT @ → google-site-verification=8KvpLQQ5kQqr418svxq6YyW...
  Sitemaps: Submitted (sitemap_index.xml + sitemap.xml)
  Indexing: 1+ pages, growing

Bing Webmaster: ✅ Verified (meta tag)
  Meta tag: BF2B5489CAEF5D3D7598D5FD07DF0755
  Injected via: sourov-automation-agent.php
  Sitemaps: Submitted

IndexNow: ✅ Active (auto-pings on every publish)
  Key: 61844e81205e89682bc4562b4b690e3a
  Notifies: Bing, Yandex, Naver, Seznam, Yep (Google excluded by design)

robots.txt: ✅ Live
  URL: https://www.sourovdeb.com/robots.txt
  Allows: All AI bots (ChatGPT, Claude, Perplexity, etc.)
  Blocks: SEO scrapers (AhrefsBot, SemrushBot, etc.)
  Size: 3,900 bytes
```

---

## 5. QUICK DIAGNOSTICS (For Any Agent)

Test everything is alive:
```bash
# WordPress API
curl https://www.sourovdeb.com/wp-json/sourov/v1/status
# Expected: {"online":true,"version":"1.1",...}

# Health check
curl https://www.sourovdeb.com/wp-json/sourov-diagnostic/v1/health
# Expected: {"status":"warning","issue_count":1} (WP_DEBUG warning only, not a blocker)

# Deploy gateway
curl "https://www.sourovdeb.com/deploy.php?action=status&key=0767044896thevenet_"
# Expected: {"status":"online","php":"8.3.30",...}

# Sitemap
curl -o /dev/null -w "%{http_code}" https://www.sourovdeb.com/sitemap_index.xml
# Expected: 200
```

---

## 6. KNOWN ISSUES (Non-Blockers)

```
1. WP_DEBUG = false → Health shows warning. NOT a blocker. Production setting is correct.
2. WordPress 7.0 available → Update when ready. Not urgent.
3. bare domain (sourovdeb.com) returns 403 → Redirects to www. Normal behaviour.
```

---

## 7. TO-DO (Before Regular Use)

```
☐ Paste WP_PUBLISHING_QUEUE.gs into Apps Script
  URL: https://script.google.com/home/projects/1NCi2zMmZqUtGsEOR...
  Action: Delete all → Paste → Save → Authorize → Reload sheet

☐ Test first publish:
  Google Sheet → Sheet1 → Row 2 (Test Post) → Set Approved = TRUE
  Expected: Post ID fills in Column J, Status fills in Column H
```

---

## 8. FILE LOCATIONS ON SERVER

```
WordPress plugins:
  /public_html/wp-content/plugins/sourov-ai-controller.php    (10.8KB)
  /public_html/wp-content/plugins/sourov-diagnostic-agent.php (28.4KB)
  /public_html/wp-content/plugins/sourov-automation-agent.php (41.5KB)
  /public_html/wp-content/plugins/aicu-engine-reach.php
  /public_html/wp-content/plugins/aicu-command-center.php
  /public_html/wp-content/plugins/aicu-idea-inbox/ (folder)
  /public_html/wp-content/plugins/aicu-ollama-uploader.php

WordPress root:
  /public_html/wp-config.php       (6.1KB — WP_CACHE fixed)
  /public_html/public_html/robots.txt  (3.9KB)
  /public_html/deploy.php          (gateway)
```

---

**END OF HANDOVER**
