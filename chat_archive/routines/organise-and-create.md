---
type: routine
id: trig_01RVi7rGFr8rjXpYYsdANGaR
name: "Organise and create "
subject: Content Publishing & Web Ops
topics: [wordpress-sync, scheduling-and-cron, seo-and-indexing, storage-sync, repo-organisation, teacher-training]
tags: [cadence-daily, public-facing, wordpress, artifact-config, automated, artifact-script, google-drive, personal-sensitive, youtube, github, gmail]
state: inactive
cron: 0 19 * * *
created_at: 2026-05-30T16:48:42.393272Z
---

# Organise and create 

| Field | Value |
|---|---|
| Trigger ID | `trig_01RVi7rGFr8rjXpYYsdANGaR` |
| Subject | **Content Publishing & Web Ops** |
| Topics | `wordpress-sync` `scheduling-and-cron` `seo-and-indexing` `storage-sync` `repo-organisation` `teacher-training` |
| Tags | `#cadence-daily` `#public-facing` `#wordpress` `#artifact-config` `#automated` `#artifact-script` `#google-drive` `#personal-sensitive` `#youtube` `#github` `#gmail` |
| State | inactive |
| Schedule | daily at 19:00 UTC (`0 19 * * *`) |
| One-shot at | — |
| Next run | 2026-07-04T19:04:23.689522962Z |
| Created | 2026-05-30T16:48:42.393272Z |
| Instruction length | 17,721 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
DO not modify if everything is good. Cheak for any plugin errors. Check speed, check if everything is Google bing compatible. 
Add my YouTube profile and analyse the channel to integrate if necessary. https://m.youtube.com/channel/UC1rs5aY7YdFiADKkhOMPCvQ

Then check "About me" , Home (can we be more creative?), philosophy and mental health or and my blogs, in resources what? All the publicly available website for English, philosophy, mental health and anything else? , and so, all the posts are not back linked . A plugin to YouTube link and podcast to my post? 
# WordPress Remote Control — sourovdeb.com
**Date:** 2026-06-03 | **Author:** Sourov DEB

In wordpress you see any empty sections, eithier complete it or eliminate. . Fix all the areas. If required. Do not break the website. Add tags and categories to the post.
---
## 1. CREDENTIALS MASTER TABLE
| Resource | Value |
|---|---|
| **Site URL** | https://sourovdeb.com |
| **WP Admin** | https://sourovdeb.com/wp-admin |
| **Admin Email** | «REDACTED:account-username» |
| **Deploy Gateway** | https://www.sourovdeb.com/deploy.php |
| **Deploy Secret** | `«REDACTED:deploy-key»` |
| **Custom API Key** | `«REDACTED:deploy-key»` (same) |
| **FTP Host** | ftp.sourovdeb.com |
| **FTP User** | «REDACTED:account-username» |
| **FTP Password** | `«REDACTED:deploy-key»` |
| **FTP Port** | 21 |
| **DB Name** | «REDACTED:account-username»_rUgwv |
| **DB User** | «REDACTED:account-username»_gVGpV |
| **DB Password** | «REDACTED:table-cell-secret» |
| **DB Host** | 127.0.0.1|
| **Server IP** | 92.249.46.84 |
| **PHP** | 8.3.30 |
| **WordPress** | 6.9.4 |
---
## 2. PLUGINS DEPLOYED (What They Are)
Four custom plugins built and deployed on 2026-05-24:
| Plugin File | Role | Auth Method |
|---|---|---|
| `sourov-ai-controller.php` | Creates/schedules/deletes posts | `X-Sourov-Key` header |
| `sourov-automation-agent.php` | Search engine verification meta tags | `X-Sourov-Key` header |
| `sourov-diagnostic-agent.php` | Read-only system monitoring | Public (no auth) |
| `aicu-engine-reach.php` | IndexNow auto-notifier on publish | Automatic (hook-based) |
### API Endpoints (ai-controller — the one you use most)
```
POST https://sourovdeb.com/wp-json/sourov/v1/ai-post ← Create/schedule post
GET https://sourovdeb.com/wp-json/sourov/v1/scheduled ← List scheduled posts
POST https://sourovdeb.com/wp-json/sourov/v1/bulk ← Bulk publish array
DELETE https://sourovdeb.com/wp-json/sourov/v1/post/{id} ← Delete post
GET https://sourovdeb.com/wp-json/sourov/v1/status ← Health check (no auth)
```
**Auth header for all POST/GET/DELETE:**
```
X-Sourov-Key: «REDACTED:deploy-key»

## 3. HOW PLUGINS WERE DEPLOYED (Step by Step Replay)
### Step 1 — Identified deploy.php gateway
The deploy.php file was already present on the server at the WordPress root.
The secret key was extracted from Hostinger hPanel file manager screenshots.
### Step 2 — Confirmed server status
```bash
curl "https://www.sourovdeb.com/deploy.php?action=status&key=«REDACTED:deploy-key»"
# → {"status":"online","php":"8.3.30","server":"LiteSpeed"}
```
### Step 3 — Wrote plugin PHP files locally
Each plugin is a single `.php` file with the WordPress plugin header:
```php
<?php

/**
* Plugin Name: Sourov AI Controller
* Version: 1.1
* ...
*/
```
### Step 4 — Encoded to base64 and uploaded via deploy.php
```bash
CONTENT=$(base64 -w 0 < sourov-ai-controller.php)
curl -X POST "https://www.sourovdeb.com/deploy.php?key=«REDACTED:deploy-key»" \
--data-urlencode "action=upload" \
--data-urlencode "path=wp-content/plugins/sourov-ai-controller/sourov-ai-controller.php" \
--data-urlencode "encoded=true" \
--data-urlencode "content=$CONTENT"
```
Path mapping rule:
```
deploy path=wp-content/X → /public_html/wp-content/X (plugins, themes)
deploy path=wp-config.php → /public_html/wp-config.php (WP root files)
deploy path=. → /public_html/ (WP root = deploy root)
```
### Step 5 — Activated plugin via WordPress options table
Used deploy.php to run a PHP snippet that directly updated the `active_plugins` serialized array in the WordPress database.
### Step 6 — Cleared LiteSpeed cache
```bash
curl -X POST "https://www.sourovdeb.com/deploy.php?key=«REDACTED:deploy-key»" \
--data-urlencode "action=purge_cache"
```
### Step 7 — Verified via REST API
```bash
curl "https://sourovdeb.com/wp-json/sourov/v1/status"
# → {"status":"active","version":"1.1"}
```
---
## 4. SCHEDULED POSTS FIX (Action Required From You)
**Problem:** 10 posts stuck as `future` status — WP-Cron did not fire on LiteSpeed shared hosting.
**Stuck posts confirmed:**
- ID 76 — April 18, 2026 (1 post)
- IDs 69, 71, 81, 85, 93, 95, 97, 100, 148 — May 1, 2026 (9 posts)
**Fix script deployed to:** `https://sourovdeb.com/publish-fixer.php`
**Action: Open this URL in your browser (once):**
```
https://sourovdeb.com/publish-fixer.php?key=«REDACTED:deploy-key»
```
Expected response:
```json
{
"fixed": 10,
"posts": ["Published ID 76: Day 4...", "Published ID 148: Test Post..."],
"deleted_self": true
}
```
The script publishes all past-scheduled posts, then **deletes itself automatically**.
### Permanent WP-Cron Fix (Prevents Recurrence)
Add this to `wp-config.php` via deploy.php or Hostinger hPanel:

```php
define('DISABLE_WP_CRON', true);

This fires WP-Cron every 15 minutes reliably, independent of page visits.
---
## 5. REMOTE CONTROL OPTIONS
---
### OPTION A — REST API (Any AI Agent or HTTP Client)
The simplest and most universal. Any AI agent, script, or tool that can make HTTP requests can control your WordPress.
**Publish a post immediately:**
```bash
curl -X POST "https://sourovdeb.com/wp-json/sourov/v1/ai-post" \
-H "X-Sourov-Key: «REDACTED:deploy-key»" \
-H "Content-Type: application/json" \
-d '{
"title": "My Post Title",
"content": "<p>Post body here. HTML accepted.</p>",
"status": "publish",
"category": "ELT",
"tags": "teaching, CELTA, English",
"meta_description": "SEO description here",
"seo_title": "SEO title here"
}'
```
**Schedule a post for a future date:**
```bash
curl -X POST "https://sourovdeb.com/wp-json/sourov/v1/ai-post" \
-H "X-Sourov-Key: «REDACTED:deploy-key»" \
-H "Content-Type: application/json" \
-d '{
"title": "Scheduled Post",
"content": "<p>Content here.</p>",
"status": "future",
"date": "2026-06-10T09:00:00"
}'
```
**Delete a post:**
```bash
curl -X DELETE "https://sourovdeb.com/wp-json/sourov/v1/post/148" \
-H "X-Sourov-Key: «REDACTED:deploy-key»"
```
**For AI agents (Claude, GPT, Gemini, etc.):**
Give the agent this instruction:
```
Endpoint: POST https://sourovdeb.com/wp-json/sourov/v1/ai-post
Header: X-Sourov-Key: «REDACTED:deploy-key»
Body: JSON with fields: title, content, status (publish|future|draft),
category, tags, meta_description, seo_title, date (ISO for scheduled)
```
---
### OPTION B — Google Apps Script (No Google Sheet)
Pure JavaScript in Apps Script. Can be triggered manually, on a timer, or via webhook.
**Create a new Apps Script project:**
Go to https://script.google.com → New Project → paste this:
```javascript
/**




* Google Apps Script — no Google Sheet dependency
* Trigger: manually or time-based
*/
const WP_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const WP_API_KEY = '«REDACTED:deploy-key»';
// ── SINGLE POST ────────────────────────────────────────────────
function publishSinglePost() {
const post = {
title: 'Day 16 of 60 — Grammar in Context',
content: '<p>Grammar teaching should emerge from meaning, not precede it...</p>',
status: 'publish', // 'publish' | 'future' | 'draft'
category: 'ELT Masterclass',
tags: 'grammar, ELT, CELTA, teaching',
meta_description: '60-day ELT masterclass: grammar in context.',
seo_title: 'Day 16 — Grammar in Context | Sourov DEB'
// date: '2026-06-10T09:00:00' // uncomment to schedule
};
const result = wpPost(post);
Logger.log(result);
}
// ── BULK POSTS ─────────────────────────────────────────────────
function publishBulkPosts() {
const posts = [
{
title: 'Day 17 — Feedback and Error Correction',
content: '<p>When and how to correct learner errors...</p>',
status: 'publish',
tags: 'feedback, error correction, ELT'
},
{
title: 'Day 18 — Task-Based Learning',
content: '<p>TBL puts the task first and language second...</p>',
status: 'future',
date: '2026-06-12T09:00:00'
}
];
posts.forEach((post, i) => {
const result = wpPost(post);
Logger.log(`Post ${i + 1}: ${result}`);
Utilities.sleep(1500);
});
}
// ── LIST SCHEDULED POSTS ───────────────────────────────────────
function listScheduled() {
const response = UrlFetchApp.fetch(
'https://sourovdeb.com/wp-json/sourov/v1/scheduled',
{ headers: { 'X-Sourov-Key': WP_API_KEY }, muteHttpExceptions: true }
);
Logger.log(response.getContentText());
}
// ── DELETE A POST ──────────────────────────────────────────────
function deletePost(postId) {
const response = UrlFetchApp.fetch(
`https://sourovdeb.com/wp-json/sourov/v1/post/${postId}`,
{
method: 'DELETE',
headers: { 'X-Sourov-Key': WP_API_KEY },
muteHttpExceptions: true
}
);
Logger.log(`Deleted ${postId}: ${response.getContentText()}`);
}
// ── CORE HTTP FUNCTION ─────────────────────────────────────────
function wpPost(postData) {
try {
const response = UrlFetchApp.fetch(WP_ENDPOINT, {
method: 'post',
headers: {
'X-Sourov-Key': WP_API_KEY,
'Content-Type': 'application/json'
},
payload: JSON.stringify(postData),
muteHttpExceptions: true
});
const code = response.getResponseCode();
const body = response.getContentText();
return `HTTP ${code}: ${body}`;
} catch (e) {
return `ERROR: ${e.message}`;
}
}
// ── AUTO SCHEDULE TRIGGER ──────────────────────────────────────
// To publish automatically every day at 9AM:
// 1. Go to Apps Script → Triggers → Add Trigger
// 2. Function: publishSinglePost (or your custom function)
// 3. Time-based → Day timer → 9AM-10AM
```
**To set a time-based trigger (no manual action needed):**
Apps Script → Triggers (clock icon) → Add Trigger → select your function → Time-driven → Day timer → 9–10 AM.
---
### OPTION C — VS Code
Two methods:
**Method 1: REST Client Extension**
1. Install extension: `humao.rest-client`
2. Create file `wordpress.http`:
```http
### Publish Post
POST https://sourovdeb.com/wp-json/sourov/v1/ai-post
X-Sourov-Key: «REDACTED:deploy-key»
Content-Type: application/json
{
"title": "My Post",
"content": "<p>Content here.</p>",
"status": "publish",
"tags": "ELT, teaching"
}
### List Scheduled
GET https://sourovdeb.com/wp-json/sourov/v1/scheduled
X-Sourov-Key: «REDACTED:deploy-key»
### Delete Post
DELETE https://sourovdeb.com/wp-json/sourov/v1/post/148
X-Sourov-Key: «REDACTED:deploy-key»
```
Click `Send Request` above each block.
**Method 2: Node.js script (run from VS Code terminal)**
```javascript
// wp-publish.js — run with: node wp-publish.js
const WP_ENDPOINT = 'https://sourovdeb.com/wp-json/sourov/v1/ai-post';
const API_KEY = '«REDACTED:deploy-key»';
async function publish(post) {
const res = await fetch(WP_ENDPOINT, {
method: 'POST',
headers: {
'X-Sourov-Key': API_KEY,
'Content-Type': 'application/json'
},
body: JSON.stringify(post)
});
const data = await res.json();
console.log('Status:', res.status, '| Post ID:', data.post_id || data);
}
// Edit post data below, then run: node wp-publish.js
publish({
title: 'Day 16 — Grammar in Context',
content: '<p>Grammar emerges from meaning...</p>',
status: 'publish',
category: 'ELT Masterclass',
tags: 'grammar, ELT, teaching',
meta_description: 'SEO description here'
});
```
Node.js 18+ required (uses native `fetch`). For older Node: `npm install node-fetch`.
---
### OPTION D — Logseq
Logseq has no native HTTP capability. Two viable approaches:
**Approach 1: Logseq → local script (most practical)**
1. Write your post in Logseq as a page.
2. Export the page as markdown.
3. Run a Node.js or Python script that reads the markdown and posts it via API.
Create `logseq-to-wp.js`:
```javascript
// logseq-to-wp.js
// Usage: node logseq-to-wp.js "My Post Title" path/to/page.md
const fs = require('fs');
const path = require('path');
const [,, title, mdFile] = process.argv;
if (!title || !mdFile) {
console.error('Usage: node logseq-to-wp.js "Title" file.md');
process.exit(1);
}
const content = fs.readFileSync(mdFile, 'utf8')
.replace(/^#+\s.*\n/gm, '') // strip Logseq heading duplicates
.replace(/\[\[(.+?)\]\]/g, '$1'); // strip wiki links
fetch('https://sourovdeb.com/wp-json/sourov/v1/ai-post', {
method: 'POST',
headers: {
'X-Sourov-Key': '«REDACTED:deploy-key»',
'Content-Type': 'application/json'
},
body: JSON.stringify({ title, content, status: 'draft' })
})
.then(r => r.json())
.then(d => console.log('Created post ID:', d.post_id));
```
**Approach 2: Logseq Plugin (advanced)**
Logseq supports JavaScript plugins. A plugin can add a command that posts the current page directly. This requires plugin development
(Logseq API + fetch). Not recommended unless you plan to use Logseq as a primary writing tool long-term.
**Verdict on Logseq:** Use it for notes and drafts. Export to markdown. Push via Apps Script or Node.js. Don't build a direct pipeline —
the tooling cost is not worth it for occasional use.
---
## 6. DEPLOY NEW PLUGINS FROM DISTANCE
Same method used on 2026-05-24. From any terminal (including VS Code terminal):
```bash

# Step 1: Encode plugin file
CONTENT=$(base64 -w 0 < my-new-plugin.php)
# Step 2: Upload to plugins directory
curl -X POST "https://www.sourovdeb.com/deploy.php?key=«REDACTED:deploy-key»" \
--data-urlencode "action=upload" \
--data-urlencode "path=wp-content/plugins/my-new-plugin/my-new-plugin.php" \
--data-urlencode "encoded=true" \
--data-urlencode "content=$CONTENT"
# Step 3: Verify upload
curl "https://www.sourovdeb.com/deploy.php?action=list&key=«REDACTED:deploy-key»"
# Step 4: Activate via WordPress admin
# Go to https://sourovdeb.com/wp-admin → Plugins → Activate
```
For activation via API (no admin access needed): the diagnostic plugin endpoint lists all plugins with activation status. Use the
automation plugin endpoint to activate programmatically if needed.
---
## 7. QUICK REFERENCE — DAILY USE
| Task | Method |
|---|---|
| Publish post now | `curl POST /wp-json/sourov/v1/ai-post` with `"status":"publish"` |
| Schedule post | Same, with `"status":"future"` and `"date":"2026-06-10T09:00:00"` |
| List stuck posts | `curl GET /wp-json/sourov/v1/scheduled` |
| Delete test post | `curl DELETE /wp-json/sourov/v1/post/{id}` |
| Check site health | `curl GET /wp-json/sourov-diagnostic/v1/health` |
| Deploy plugin | base64 encode → POST to deploy.php |
| Fix stuck posts | Browser: `https://sourovdeb.com/publish-fixer.php?key=«REDACTED:deploy-key»` |
---
## 8. IMMEDIATE ACTION LIST
1. **Open in browser now** → `https://sourovdeb.com/publish-fixer.php?key=«REDACTED:deploy-key»`
This publishes 10 stuck posts and deletes the script.
2. **Add WP-Cron job in Hostinger hPanel** → Advanced → Cron Jobs:
`*/15 * * * * wget -q -O /dev/null https://sourovdeb.com/wp-cron.php?doing_wp_cron`
Add to wp-config.php: `define('DISABLE_WP_CRON', true);`
3. **Generate WordPress Application Password** (for native WP REST API access):
wp-admin → Users → Your Profile → Application Passwords → Add New
Name it: `AI-Agent`
Save the generated password — format is `xxxx xxxx xxxx xxxx xxxx xxxx`
Use as: `Authorization: Basic base64(«REDACTED:account-username»:xxxx xxxx...)`
---
*All credentials sourced from MASTER_COMBINED_2026-06-03.md and HANDOVER_AGENT_REFERENCE.md in project knowledge.*


For context and materials go here # Step 1: Encode plugin file
CONTENT=$(base64 -w 0 < my-new-plugin.php)
# Step 2: Upload to plugins directory
curl -X POST "https://www.sourovdeb.com/deploy.php?key=«REDACTED:deploy-key»" \
--data-urlencode "action=upload" \
--data-urlencode "path=wp-content/plugins/my-new-plugin/my-new-plugin.php" \
--data-urlencode "encoded=true" \
--data-urlencode "content=$CONTENT"
# Step 3: Verify upload
curl "https://www.sourovdeb.com/deploy.php?action=list&key=«REDACTED:deploy-key»"
# Step 4: Activate via WordPress admin
# Go to https://sourovdeb.com/wp-admin → Plugins → Activate
```
For activation via API (no admin access needed): the diagnostic plugin endpoint lists all plugins with activation status. Use the
automation plugin endpoint to activate programmatically if needed.
---
## 7. QUICK REFERENCE — DAILY USE
| Task | Method |
|---|---|
| Publish post now | `curl POST /wp-json/sourov/v1/ai-post` with `"status":"publish"` |
| Schedule post | Same, with `"status":"future"` and `"date":"2026-06-10T09:00:00"` |
| List stuck posts | `curl GET /wp-json/sourov/v1/scheduled` |
| Delete test post | `curl DELETE /wp-json/sourov/v1/post/{id}` |
| Check site health | `curl GET /wp-json/sourov-diagnostic/v1/health` |
| Deploy plugin | base64 encode → POST to deploy.php |
| Fix stuck posts | Browser: `https://sourovdeb.com/publish-fixer.php?key=«REDACTED:deploy-key»` |
---
## 8. IMMEDIATE ACTION LIST
1. **Open in browser now** → `https://sourovdeb.com/publish-fixer.php?key=«REDACTED:deploy-key»`
This publishes 10 stuck posts and deletes the script.
2. **Add WP-Cron job in Hostinger hPanel** → Advanced → Cron Jobs:
`*/15 * * * * wget -q -O /dev/null https://sourovdeb.com/wp-cron.php?doing_wp_cron`
Add to wp-config.php: `define('DISABLE_WP_CRON', true);`
3. **Generate WordPress Application Password** (for native WP REST API access):
wp-admin → Users → Your Profile → Application Passwords → Add New
Name it: `AI-Agent`
Save the generated password — format is `xxxx xxxx xxxx xxxx xxxx xxxx`
Use as: `Authorization: Basic base64(«REDACTED:account-username»:xxxx xxxx...)`
---
*All credentials sourced from MASTER_COMBINED_2026-06-03.md and HANDOVER_AGENT_REFERENCE.md in project knowledge.* https://claude.ai/share/4bed4a99-87b0-413b-9857-38dfd65fc61a


Search for materials on GitHub as well. 
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Content Publishing & Web Ops | 139 |
| Education & Language Teaching | 58 |
| Infrastructure & Archival | 51 |
| Health, Wellbeing & Productivity | 23 |
| AI & Agent Engineering | 16 |
