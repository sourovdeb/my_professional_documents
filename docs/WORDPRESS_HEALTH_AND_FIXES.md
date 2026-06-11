# WordPress Health Guide & Fixes
## Category/Tag Issues, Database Health, Performance

---

## Common Category & Tag Problems (And Fixes)

### Problem 1: Tags Not Saving When You Type Them

This is usually a JavaScript error in the block editor. Check:

**Step 1: Test in a different browser**
If tags save in Firefox but not Chrome, it's a browser extension blocking something.

**Step 2: Check browser console**
1. Open WordPress post editor
2. Press `F12` → Console tab
3. Look for red errors containing words like `rest-api`, `nonce`, `unauthorized`

**Step 3: Fix REST API authentication (most common cause)**
Add to your `wp-config.php` above the line `/* That's all, stop editing! */`:
```php
// Force REST API to use cookie authentication
define('JWT_AUTH_SECRET_KEY', 'your-secret-here-change-this');
define('JWT_AUTH_CORS_ENABLE', true);
```

Also add to `.htaccess`:
```apache
# Allow Authorization header through (required for WP REST API)
RewriteEngine On
RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
SetEnvIf Authorization "(.*)" HTTP_AUTHORIZATION=$1
```

**Step 4: Check if a plugin is blocking tags**
Disable these plugins temporarily and test:
- Wordfence / any security plugin
- Yoast SEO (it modifies the tag input)
- W3 Total Cache / WP Super Cache

---

### Problem 2: Category Not Appearing on Published Posts

Posts might be in `Uncategorized` even when you selected a category. This happens when:

1. The category was set by name but the name doesn't match exactly (case-sensitive)
2. Your custom plugin uses a category slug, not name

**Fix via WP-CLI (SSH):**
```bash
# Check all posts and their categories
wp post list --post_status=publish --fields=ID,post_title,post_category --format=table

# Add ELT Masterclass category to ALL posts that have no category
for id in $(wp post list --post_status=publish --fields=ID --format=ids); do
  cat_count=$(wp post term list $id category --format=count)
  if [ "$cat_count" -le "1" ]; then  # 1 = only Uncategorized
    wp post term add $id category elt-masterclass
    echo "Fixed post ID: $id"
  fi
done
```

**Fix via WordPress admin (no SSH needed):**
1. Go to Posts → All Posts
2. Click **Screen Options** (top right) → enable **Categories** column
3. Use **Bulk Actions** → select all posts without category → Quick Edit → assign category

---

### Problem 3: Your Custom Plugin Not Setting Categories Correctly

Your `sourov-ai-controller.php` plugin accepts `category` as a name string.
WordPress needs a category ID or slug internally.

Check your plugin code has this logic:
```php
// Convert category name to ID
$cat_id = get_cat_ID( sanitize_text_field( $data['category'] ) );
if ( ! $cat_id ) {
    // Category doesn't exist yet — create it
    $cat_id = wp_create_category( sanitize_text_field( $data['category'] ) );
}
wp_set_post_categories( $post_id, [ $cat_id ] );
```

For tags, use:
```php
if ( ! empty( $data['tags'] ) ) {
    $tags = array_map( 'trim', explode( ',', $data['tags'] ) );
    wp_set_post_tags( $post_id, $tags, false ); // false = replace, true = append
}
```

---

## WordPress Health Check Commands (WP-CLI)

```bash
# Check overall WordPress health
wp doctor check --all

# Check for outdated plugins
wp plugin list --update=available

# Update all plugins at once
wp plugin update --all

# Check and repair the database
wp db check
wp db repair

# Clean up spam comments, revisions, transients (speed up the site)
wp comment delete $(wp comment list --status=spam --format=ids)
wp post delete $(wp post list --post_type=revision --format=ids) --force
wp transient delete --expired

# Check file permissions (should be 755 for folders, 644 for files)
find /public_html -type d -exec chmod 755 {} \;
find /public_html -type f -exec chmod 644 {} \;
chmod 600 /public_html/wp-config.php
```

---

## WordPress Performance Monitoring

### Free tools to check your site health

| Tool | What it checks | URL |
|------|---------------|-----|
| Google PageSpeed Insights | Load time, Core Web Vitals | pagespeed.web.dev |
| GTmetrix | Waterfall analysis | gtmetrix.com |
| Pingdom | Uptime monitoring | pingdom.com |
| WP Hive | Plugin impact checker | wphive.com |
| IsItWP Security Scanner | Security issues | isitwp.com/wordpress-security-scanner |

### Uptime Monitor (Free — Know When Your Site Goes Down)
```python
# save as uptime_check.py — run via cron every 5 minutes
import requests, smtplib
from email.mime.text import MIMEText
from datetime import datetime

SITE  = 'https://sourovdeb.com'
EMAIL = 'sourovdeb.is@gmail.com'

try:
    r = requests.get(SITE, timeout=10)
    if r.status_code >= 400:
        raise Exception(f'HTTP {r.status_code}')
    print(f'{datetime.now()} - OK ({r.status_code})')
except Exception as e:
    msg = MIMEText(f'Your site {SITE} is DOWN: {e}')
    msg['Subject'] = 'SITE DOWN ALERT'
    msg['From']    = EMAIL
    msg['To']      = EMAIL
    # configure your SMTP here
    print(f'ALERT: {e}')
```

Cron entry (runs every 5 minutes):
```
*/5 * * * * python3 /path/to/uptime_check.py >> /var/log/uptime.log 2>&1
```

---

## Recommended WordPress Plugins for Health

| Plugin | Why you need it | Cost |
|--------|----------------|------|
| **Wordfence Security** | Blocks malware, login attacks | Free |
| **UpdraftPlus** | Automated backups to Google Drive | Free |
| **WP Super Cache** or **W3 Total Cache** | Speed up the site | Free |
| **Imagify** or **ShortPixel** | Compress images automatically | Free tier |
| **Rank Math SEO** | Category/tag SEO, sitemap | Free |
| **WPS Hide Login** | Change /wp-admin URL to avoid bots | Free |
| **Sucuri Security** | Security audit log | Free |

---

## Backup Strategy

Never lose your content. Set UpdraftPlus to:
- Backup **daily** to Google Drive (your Drive has 15GB free)
- Keep **7 copies** of daily backups
- Include: database + plugins + themes + uploads

Manual backup command (SSH):
```bash
# Database backup
wp db export backup-$(date +%Y%m%d).sql

# Full site backup
tar -czf site-backup-$(date +%Y%m%d).tar.gz /public_html
```
