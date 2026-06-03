# Controlling WordPress from a distance

Four ways to post and manage WordPress without logging into wp-admin by hand. Pick the
one that fits the moment. All assume **WordPress (self-hosted or WordPress.com)**.

> Security first — the rule that protects you:
> **Never put a password or API key inside a post, a public repo, a Google Sheet you
> share, or a chat message.** Secrets live in ONE place: a private credentials store
> (a `.env` file that is git-ignored, or your password manager). Every method below
> reads the secret from there, never hardcodes it.

---

## 0. The credential you actually need: an Application Password

Forget your main login password for automation. WordPress has a purpose-built mechanism:

1. Log in to `https://YOURSITE/wp-admin`.
2. Go to **Users → Profile** (or **Users → Your Profile**).
3. Scroll to **Application Passwords**.
4. Name it (e.g. "logseq-publisher" or "ai-agent"), click **Add New**.
5. Copy the 24-character password it shows **once** (format: `xxxx xxxx xxxx xxxx xxxx xxxx`).
6. Store it in your password manager. This is what all REST API methods use.

You can revoke any Application Password anytime without changing your real login — so if
one leaks, you kill just that one. This is why we never use the master password.

(On **WordPress.com** specifically, the cleanest route is the official MCP / OAuth — see
section 5 — rather than application passwords.)

---

## 1. REST API directly (any AI agent, any script, from anywhere)

WordPress exposes a full REST API at `https://YOURSITE/wp-json/wp/v2/`. This is the
foundation every other method sits on.

**Create a post (curl example):**
```bash
# Credentials read from environment — never hardcoded
# export WP_USER="sourov"
# export WP_APP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"
# export WP_SITE="https://yoursite.com"

curl -X POST "$WP_SITE/wp-json/wp/v2/posts" \
  -u "$WP_USER:$WP_APP_PASS" \
  -H "Content-Type: application/json" \
  -d '{
    "title":   "The system carries the day",
    "content": "<p>Most productivity advice is built for your best day...</p>",
    "status":  "draft",            // draft | publish | future (scheduled)
    "categories": [5],             // category IDs (see below)
    "tags": [12, 19],              // tag IDs
    "excerpt": "Meta description goes here for SEO."
  }'
```

**Find your category/tag IDs** (so posts land categorised, not uncategorised — your exact
problem):
```bash
curl -s "$WP_SITE/wp-json/wp/v2/categories?per_page=100" -u "$WP_USER:$WP_APP_PASS"
curl -s "$WP_SITE/wp-json/wp/v2/tags?per_page=100"        -u "$WP_USER:$WP_APP_PASS"
```
Map name → ID once, keep the mapping in your Google Sheet, and every automated post is
tagged correctly.

**To give another AI agent control:** hand it the three env vars above (via *its* secret
store, not in the prompt) and these endpoints. It can then create/update/schedule posts.
Endpoints it needs:
- `POST /wp-json/wp/v2/posts` — create
- `POST /wp-json/wp/v2/posts/{id}` — update
- `GET  /wp-json/wp/v2/posts?status=future` — list scheduled
- `POST /wp-json/wp/v2/media` — upload images
- `GET  /wp-json/wp/v2/categories` and `/tags` — taxonomy IDs

**Plugins via REST:** the REST API can *list/activate* plugins
(`/wp-json/wp/v2/plugins`, needs `manage_options` + app password) but it does **not**
upload plugin ZIPs. Uploading a new plugin file requires either (a) WP-CLI over SSH, or
(b) SFTP/FTP to `wp-content/plugins/`, or (c) the wp-admin uploader. That is almost
certainly how the earlier plugins were pushed — SFTP or WP-CLI, not the REST API.

---

## 2. Google Apps Script + Google Sheet (your current workflow, made automatic)

This turns your existing content sheet into a one-click publisher. No server needed —
Google runs it.

**Setup (once):**
1. Open your content Sheet → **Extensions → Apps Script**.
2. Paste the script below. Set credentials in **Project Settings → Script Properties**
   (`WP_SITE`, `WP_USER`, `WP_APP_PASS`) — NOT in the code, so they never appear in a
   shared sheet.
3. Save. Run `publishApprovedRows` once to authorise.

```javascript
function publishApprovedRows() {
  const props = PropertiesService.getScriptProperties();
  const SITE = props.getProperty('WP_SITE');
  const AUTH = 'Basic ' + Utilities.base64Encode(
    props.getProperty('WP_USER') + ':' + props.getProperty('WP_APP_PASS'));

  const sheet = SpreadsheetApp.getActiveSheet();
  const rows = sheet.getDataRange().getValues();
  const head = rows[0];
  const col = name => head.indexOf(name);

  for (let i = 1; i < rows.length; i++) {
    const r = rows[i];
    if (String(r[col('Approved')]).toUpperCase() !== 'TRUE') continue;
    if (r[col('Post ID')]) continue;                 // already published

    const payload = {
      title:   r[col('Title')],
      content: r[col('Content')],
      excerpt: r[col('Meta Description')],
      status:  (r[col('Status')] || 'draft').toLowerCase(),
    };
    // Optional scheduling: if a future Publish Date is set, schedule it
    const date = r[col('Publish Date')];
    if (date && payload.status === 'future') {
      payload.date = new Date(date).toISOString();
    }

    const res = UrlFetchApp.fetch(SITE + '/wp-json/wp/v2/posts', {
      method: 'post',
      contentType: 'application/json',
      headers: { Authorization: AUTH },
      payload: JSON.stringify(payload),
      muteHttpExceptions: true,
    });

    const out = JSON.parse(res.getContentText());
    if (out.id) {
      sheet.getRange(i + 1, col('Post ID') + 1).setValue(out.id);
      sheet.getRange(i + 1, col('Result Log') + 1).setValue('Published ' + out.link);
    } else {
      sheet.getRange(i + 1, col('Result Log') + 1).setValue('ERROR: ' + res.getContentText());
    }
  }
}
```

4. **Add a menu button or a daily trigger:** Apps Script → Triggers → add
   time-driven trigger → `publishApprovedRows` daily. Now any row marked `Approved=TRUE`
   publishes itself.

This matches exactly what you already built — your sheet has the right columns. The
script just reads them.

---

## 3. VS Code

Two flavours:

**A. Quick — REST Client extension:**
1. Install the **REST Client** extension.
2. Create `publish.http`:
```http
@site = https://yoursite.com
@auth = sourov:{{$dotenv WP_APP_PASS}}

POST {{site}}/wp-json/wp/v2/posts
Authorization: Basic {{auth}}
Content-Type: application/json

{ "title": "My post", "content": "<p>Body</p>", "status": "draft" }
```
3. Put `WP_APP_PASS=...` in a git-ignored `.env`. Click "Send Request" above the POST.

**B. Powerful — a small script + WP-CLI over SSH:**
If your host gives SSH (WordPress.com Atomic/Business plans do), VS Code's terminal +
WP-CLI is the most complete control — including **plugin install**:
```bash
wp plugin install my-plugin.zip --activate --ssh=user@yoursite.com
wp post create ./post.md --post_status=publish --ssh=user@yoursite.com
```
WP-CLI is how plugins get *uploaded* remotely (the REST API can't do that).

---

## 4. Logseq → WordPress

Logseq writes plain Markdown, which WordPress understands well. Path of least friction:

**Option A — Export + script:** Write the post in a Logseq page, export the page as
Markdown, and feed the `.md` to the Apps Script (section 2) or a tiny local script that
calls the REST API (section 1). Best if you want Logseq as your *writing* home and a
button to ship.

**Option B — A publishing pipeline:** keep a `#to-publish` tag in Logseq. A small local
script (Node/Python, run on demand) scans your Logseq graph folder for pages tagged
`#to-publish`, converts Markdown → HTML, and POSTs each to the REST API, then changes the
tag to `#published`. This is the Logseq equivalent of your blog branch workflow.

> There is no first-party Logseq→WordPress plugin that's reliable as of 2026, so the
> Markdown-export-then-REST route is the durable one. The conversion step (Markdown → the
> HTML or blocks WordPress wants) is where formatting either stays clean or breaks — keep
> the Markdown simple (headings, bold, lists, links) and it survives the trip.

---

## 5. The cleanest path for you: WordPress.com MCP

You already have the **WordPress.com MCP** connected to this assistant. It uses an
authorized OAuth connection — no password handling — and an AI agent can create/manage
posts directly. To use it:

1. Go to **https://wordpress.com/me/mcp**.
2. Enable the abilities you want — at minimum **User Sites** (to list sites) and
   **Content Authoring** (to create/edit posts). For plugins, enable **Site**.
3. Once enabled, an agent (like me) can list your site, read your scheduled posts, fix
   their dates, set categories/tags, and publish — all without you pasting a credential
   anywhere.

This is the recommended option: most secure, least setup, and it solves the
"uncategorised / wrong schedule" problem directly because the agent sets those fields.

---

## Fixing the "stuck scheduled at 1 May" problem

Most likely causes, in order:

1. **WP-Cron isn't firing.** WordPress publishes scheduled posts via `wp-cron.php`,
   which only runs when someone visits the site. A low-traffic site = posts sit in
   "Missed schedule." **Fix:** set up a real cron job to hit
   `https://yoursite.com/wp-cron.php` every 5–15 min (most hosts have a "Cron Jobs"
   panel), or use a plugin like *WP Crontrol* to inspect and trigger the queue.
2. **Wrong timezone.** Settings → General → Timezone. If it's set to UTC but you
   scheduled in Réunion time (UTC+4), posts can appear stuck or publish at odd times.
3. **The date is in the past.** If "1 May" is *behind* today, WordPress marks them
   "Missed schedule" and won't auto-publish. **Fix:** edit each post, set status to
   *Publish* (now) or a *future* date, and save. Via REST:
   ```bash
   curl -X POST "$WP_SITE/wp-json/wp/v2/posts/POST_ID" \
     -u "$WP_USER:$WP_APP_PASS" -H "Content-Type: application/json" \
     -d '{"status":"publish"}'
   ```
4. **A caching/security plugin blocking wp-cron.** Some plugins disable the default
   cron; check the plugin that was recently added.

To diagnose precisely I need either the WordPress.com MCP abilities enabled (section 5)
or you can run: `GET /wp-json/wp/v2/posts?status=future` and paste the result — that
shows every stuck post and its real scheduled date.
