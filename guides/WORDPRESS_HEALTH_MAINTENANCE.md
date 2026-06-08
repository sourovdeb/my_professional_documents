# WordPress Health Maintenance Guide
## Fix Categories, Tags, SEO & Performance for sourovdeb.com

---

## PART 1: Fix Categories and Tags (The Common Problem)

### Why Categories and Tags Get Messy

When you publish manually or through different scripts, posts can end up:
- In the wrong category (e.g., "Uncategorized" instead of "ELT Masterclass")
- With no tags at all
- With duplicate categories
- With inconsistent capitalization ("ELT" vs "elt" vs "Elt")

### Method 1: Fix via WordPress Admin (Quick, Manual)

1. Go to **Posts → All Posts**
2. Filter by category: click the dropdown "All Categories" → select "Uncategorized"
3. Select all visible posts (checkbox at top)
4. In "Bulk actions" dropdown: select "Edit"
5. Click "Apply"
6. In the bulk editor, change Category to "ELT Masterclass"
7. Click "Update"

### Method 2: Fix via WP-CLI (Fast, All Posts)

If you have SSH access to your server:

```bash
# List all categories with IDs
wp term list category

# Find ID of 'ELT Masterclass' (let's say it's ID 5)
wp term get category "ELT Masterclass" --field=term_id

# Get all posts in 'Uncategorized' (ID 1)
wp post list --post_status=any --cat=1 --field=ID

# Move all those posts to ELT Masterclass (ID 5)
wp post list --post_status=any --cat=1 --field=ID | xargs -I {} wp post term set {} category 5

# Verify
wp post list --cat=1 --field=ID
```

### Method 3: Fix via Apps Script (Best for Bulk)

Add this to your Google Apps Script:

```javascript
function fixWordPressCategories() {
  const API_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  const WP_BASE = 'https://sourovdeb.com/wp-json/wp/v2';
  const WP_AUTH = 'Basic ' + Utilities.base64Encode('your_user:your_app_password');
  
  // Step 1: Get category IDs
  const catResponse = UrlFetchApp.fetch(WP_BASE + '/categories?per_page=100', {
    headers: { 'Authorization': WP_AUTH }
  });
  const categories = JSON.parse(catResponse.getContentText());
  const catMap = {};
  categories.forEach(c => { catMap[c.name.toLowerCase()] = c.id; });
  Logger.log('Categories found: ' + JSON.stringify(catMap));
  
  // Step 2: Get posts without category (in Uncategorized = ID 1)
  const postResponse = UrlFetchApp.fetch(WP_BASE + '/posts?categories=1&per_page=100&status=any', {
    headers: { 'Authorization': WP_AUTH }
  });
  const posts = JSON.parse(postResponse.getContentText());
  Logger.log('Posts to fix: ' + posts.length);
  
  // Step 3: Fix each post
  for (const post of posts) {
    const title   = post.title.rendered;
    const content = post.content.rendered || '';
    const catName = guessCategory(title, content);
    const catId   = catMap[catName.toLowerCase()];
    
    if (!catId) {
      Logger.log('Category not found in WP: ' + catName + ' (post: ' + title + ')');
      continue;
    }
    
    UrlFetchApp.fetch(WP_BASE + '/posts/' + post.id, {
      method: 'POST',
      headers: { 'Authorization': WP_AUTH, 'Content-Type': 'application/json' },
      payload: JSON.stringify({ categories: [catId] }),
      muteHttpExceptions: true
    });
    
    Logger.log('Fixed: ' + title + ' → ' + catName);
    Utilities.sleep(500);
  }
}

// Reuse this from the CSV tutorial
function guessCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  if (text.includes('grammar') || text.includes('tense')) return 'Grammar';
  if (text.includes('listen') || text.includes('pronunciation')) return 'Listening & Phonology';
  if (text.includes('celta') || text.includes('lesson plan')) return 'CELTA';
  if (text.includes('speak') || text.includes('fluency')) return 'Speaking';
  return 'ELT Masterclass';
}
```

### Fix Tags for All Posts

```javascript
function addMissingTags() {
  const WP_BASE = 'https://sourovdeb.com/wp-json/wp/v2';
  const WP_AUTH = 'Basic ' + Utilities.base64Encode('your_user:your_app_password');
  
  // Get posts with no tags
  const response = UrlFetchApp.fetch(WP_BASE + '/posts?per_page=100&tags_exclude=&status=publish', {
    headers: { 'Authorization': WP_AUTH }
  });
  const posts = JSON.parse(response.getContentText());
  
  for (const post of posts) {
    if (post.tags && post.tags.length > 0) continue; // Skip posts with tags
    
    const suggestedTags = suggestTagIds(post.title.rendered, WP_BASE, WP_AUTH);
    
    if (suggestedTags.length > 0) {
      UrlFetchApp.fetch(WP_BASE + '/posts/' + post.id, {
        method: 'POST',
        headers: { 'Authorization': WP_AUTH, 'Content-Type': 'application/json' },
        payload: JSON.stringify({ tags: suggestedTags }),
        muteHttpExceptions: true
      });
      Logger.log('Tagged: ' + post.title.rendered);
    }
    
    Utilities.sleep(500);
  }
}

function suggestTagIds(title, wpBase, auth) {
  // Map keyword → tag slug
  const keywordMap = {
    'listening': 'listening', 'grammar': 'grammar',
    'pronunciation': 'pronunciation', 'speaking': 'speaking',
    'celta': 'celta', 'elt': 'elt', 'fluency': 'fluency',
    'vocabulary': 'vocabulary', 'writing': 'writing'
  };
  
  const words = title.toLowerCase().split(/\s+/);
  const slugs = [];
  
  for (const [keyword, slug] of Object.entries(keywordMap)) {
    if (words.some(w => w.includes(keyword))) slugs.push(slug);
  }
  
  if (slugs.length === 0) return [];
  
  // Get or create tag IDs
  const ids = [];
  for (const slug of slugs.slice(0, 5)) {  // Max 5 tags
    try {
      const r = UrlFetchApp.fetch(wpBase + '/tags?slug=' + slug, {
        headers: { 'Authorization': auth }
      });
      const tags = JSON.parse(r.getContentText());
      if (tags.length > 0) {
        ids.push(tags[0].id);
      } else {
        // Create the tag
        const create = UrlFetchApp.fetch(wpBase + '/tags', {
          method: 'POST',
          headers: { 'Authorization': auth, 'Content-Type': 'application/json' },
          payload: JSON.stringify({ name: slug, slug: slug })
        });
        ids.push(JSON.parse(create.getContentText()).id);
      }
    } catch(e) { /* skip */ }
  }
  return ids;
}
```

---

## PART 2: WordPress Performance

### Essential Free Plugins

| Plugin | Purpose | Install |
|--------|---------|--------|
| **W3 Total Cache** | Caching (faster page loads) | WP Admin → Plugins |
| **Smush** | Auto image compression | WP Admin → Plugins |
| **Yoast SEO** | SEO, meta descriptions, sitemap | WP Admin → Plugins |
| **Wordfence Security** | Security scanning, firewall | WP Admin → Plugins |
| **UpdraftPlus** | Automatic backups to Google Drive | WP Admin → Plugins |
| **Redirection** | Manage 301 redirects | WP Admin → Plugins |

### Performance Checklist

```bash
# Check WP health from admin
# WP Admin → Tools → Site Health
# Fix everything marked as 'Critical' first

# Via WP-CLI: check for plugin updates
wp plugin list --update=available
wp plugin update --all

# Via WP-CLI: run database cleanup
wp db optimize
wp transient delete --expired
wp post delete $(wp post list --post_status=trash --field=ID) --force
```

---

## PART 3: SEO Health Check

### Yoast SEO Configuration

1. Install Yoast SEO plugin
2. Go to **Yoast SEO → Configuration Wizard**
3. Set your site title and tagline
4. Enable XML sitemaps (auto-submits to Google)
5. Set default meta descriptions for categories

### Fix Missing Meta Descriptions via Script

```python
import requests

WP_URL = 'https://sourovdeb.com/wp-json/wp/v2'
WP_USER = 'your_username'
WP_PASS = 'your_app_password'
AUTH = (WP_USER, WP_PASS)

def fix_meta_descriptions():
    # Get posts with no Yoast meta description
    response = requests.get(f'{WP_URL}/posts?per_page=100', auth=AUTH)
    posts = response.json()
    
    for post in posts:
        title = post['title']['rendered']
        content_text = post['content']['rendered'].replace('<', ' <').replace('>', '> ')
        
        # Strip HTML tags roughly
        import re
        clean = re.sub(r'<[^>]+>', '', content_text).strip()
        meta = clean[:155] + '...' if len(clean) > 155 else clean
        
        # Update Yoast meta via REST API
        requests.post(
            f"{WP_URL}/posts/{post['id']}",
            auth=AUTH,
            json={'meta': {'_yoast_wpseo_metadesc': meta}}
        )
        print(f'Fixed meta: {title[:50]}')

fix_meta_descriptions()
```

---

## PART 4: Automated Backups

### UpdraftPlus (Free Plugin)

1. Install UpdraftPlus
2. Go to **Settings → UpdraftPlus Backups**
3. Set schedule: Daily backups of files + database
4. Connect Google Drive: Click "Google Drive" → follow OAuth flow
5. Set retention: Keep 7 daily backups

### Manual Backup via WP-CLI

```bash
# Full site backup
wp db export backup_$(date +%Y%m%d).sql
tar -czf files_$(date +%Y%m%d).tar.gz wp-content/uploads wp-content/plugins wp-content/themes

# Upload to remote (if rsync available)
rsync -avz backup_*.sql files_*.tar.gz user@backup-server:/backups/
```

---

## PART 5: Security Hardening

```bash
# Via WP-CLI: change table prefix (stops automated attacks)
# WARNING: backup first!
wp config set table_prefix 'sourov_'

# Check for outdated plugins
wp plugin list --update=available

# Check user accounts
wp user list

# Remove test accounts
wp user delete test_user --reassign=1

# Set strong password policy
wp option update users_can_register 0  # Disable registration
```

### Security Checklist
- [ ] WordPress core updated to latest version
- [ ] All plugins updated
- [ ] Delete unused plugins and themes
- [ ] Enable 2FA for admin account
- [ ] Set file permissions: folders 755, files 644
- [ ] Restrict `wp-admin` by IP (if static IP)
- [ ] Enable HTTPS (Let's Encrypt, free)
- [ ] Check `wp-config.php` is not publicly readable

---

## PART 6: Monitoring

### Check WordPress Health Automatically

Add to your Google Apps Script to check site daily:

```javascript
function checkWordPressSiteHealth() {
  try {
    const statusUrl = 'https://sourovdeb.com/wp-json/sourov/v1/status';
    const key = PropertiesService.getScriptProperties().getProperty('WP_KEY');
    
    const response = UrlFetchApp.fetch(statusUrl, {
      headers: { 'X-Sourov-Key': key },
      muteHttpExceptions: true,
      followRedirects: true
    });
    
    if (response.getResponseCode() === 200) {
      const data = JSON.parse(response.getContentText());
      Logger.log('✅ Site healthy: ' + data.site + ' | WP ' + data.wp_version);
    } else {
      // Send yourself an alert email
      GmailApp.sendEmail(
        'sourovdeb.is@gmail.com',
        '⚠️ WordPress Alert: Site Error',
        'Status code: ' + response.getResponseCode() + '\nTime: ' + new Date().toISOString()
      );
    }
  } catch(e) {
    GmailApp.sendEmail(
      'sourovdeb.is@gmail.com',
      '⚠️ WordPress Alert: Site Down',
      'Error: ' + e.toString() + '\nTime: ' + new Date().toISOString()
    );
  }
}
```

Set this on a daily time trigger.

---

*Last updated: June 2026*
