# WordPress Health Guide: Fix Categories, Tags & Performance

## Why Categories and Tags Break

Over time WordPress accumulates:
- **Duplicate categories**: `ELT`, `ELT Masterclass`, `elt-masterclass` — all separate
- **Orphaned tags**: Tags on only 1–2 posts that should be merged
- **Uncategorized posts**: Posts sitting in the default category
- **Empty categories**: Categories with 0 posts still showing in navigation

This happens because different scripts used different names, or manual posts used different capitalisation.

---

## Step 1: Diagnose Your Current State

### Via WordPress Dashboard
1. **Posts → Categories** — look for duplicates and near-duplicates
2. **Posts → Tags** — sort by Count, look for 1-post tags to merge
3. **Posts → All Posts** — filter by Uncategorized

### Via Python Audit Script

```python
# Run: python audit_wp_taxonomy.py
import requests, os, base64
from dotenv import load_dotenv
load_dotenv()

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com')

def auth_header():
    creds = base64.b64encode(
        f"{os.getenv('WP_USER')}:{os.getenv('WP_APP_PASSWORD')}".encode()
    ).decode()
    return {'Authorization': f'Basic {creds}'}

def audit():
    cats = requests.get(f'{WP_URL}/wp-json/wp/v2/categories?per_page=100',
                        headers=auth_header()).json()
    tags = requests.get(f'{WP_URL}/wp-json/wp/v2/tags?per_page=100',
                        headers=auth_header()).json()

    print('=== CATEGORIES ===')
    for c in sorted(cats, key=lambda x: x['count'], reverse=True):
        flag = '' if c['count'] > 0 else '  ← EMPTY'
        print(f"  [{c['count']:3d}] {c['name']:40s} (ID:{c['id']}){flag}")

    print('\n=== ORPHANED TAGS (count <= 1) ===')
    orphans = [t for t in tags if t['count'] <= 1]
    for t in orphans:
        print(f"  [{t['count']:3d}] {t['name']:30s} (ID:{t['id']})")

    print(f'\nTotal: {len(cats)} categories, {len(tags)} tags, {len(orphans)} orphaned tags')

if __name__ == '__main__':
    audit()
```

---

## Step 2: Fix with Script

The complete fix script is at `scripts/fix_wp_categories.py`. It:
1. Moves all Uncategorized posts to `ELT Masterclass`
2. Merges duplicate categories
3. Deletes empty categories
4. Normalizes tag names to lowercase-hyphen format

---

## Step 3: wp-cli Commands (If You Have SSH)

```bash
# List all categories with post counts
wp term list category --fields=term_id,name,count

# Find uncategorized posts (Uncategorized usually = ID 1)
wp post list --cat=1 --fields=ID,post_title

# Move posts from old category to new
# Replace 5 with old cat ID, elt-masterclass with new slug
wp post list --cat=5 --format=ids | \
  xargs -I{} wp post term set {} category elt-masterclass

# Delete empty category
wp term delete category 5

# List orphaned tags (count = 0 or 1)
wp term list post_tag --fields=term_id,name,count | awk 'NR>1 && $3<=1'

# Full site health check
wp doctor check --all

# Backup before changes
wp export --post_type=post --filename_format=backup_%Y%m%d.xml
```

---

## Step 4: Prevent Future Problems

Add this to your `sheet_publisher.gs` — a canonical category list the script always uses:

```javascript
// Canonical categories — only these are allowed
const CANONICAL_CATEGORIES = {
  'grammar':       'Grammar',
  'listen':        'Listening & Phonology',
  'pronunciation': 'Listening & Phonology',
  'phonology':     'Listening & Phonology',
  'celta':         'CELTA',
  'lesson':        'CELTA',
  'speak':         'Speaking & Fluency',
  'fluency':       'Speaking & Fluency',
  'vocabulary':    'Vocabulary',
  'idiom':         'Vocabulary',
  'write':         'Writing Skills',
  'essay':         'Writing Skills',
};

function canonicalCategory(title, content) {
  const text = (title + ' ' + content).toLowerCase();
  for (const [keyword, category] of Object.entries(CANONICAL_CATEGORIES)) {
    if (text.includes(keyword)) return category;
  }
  return 'ELT Masterclass'; // safe default
}
```

---

## Monthly Health Check (Google Apps Script)

```javascript
// Sends you a monthly email with WordPress health stats
function monthlyHealthCheck() {
  const today = new Date();
  if (today.getDate() !== 1) return; // only run on 1st of month

  const WP_KEY = PropertiesService.getScriptProperties().getProperty('WP_KEY');
  const res = UrlFetchApp.fetch('https://sourovdeb.com/wp-json/sourov/v1/status',
    { headers: { 'X-Sourov-Key': WP_KEY } });
  const status = JSON.parse(res.getContentText());

  MailApp.sendEmail({
    to: 'sourovdeb.is@gmail.com',
    subject: 'WP Health — ' + today.toDateString(),
    body: `WordPress Health Report\n\n` +
          `Site: ${status.site}\n` +
          `WP Version: ${status.wp_version}\n` +
          `Total Posts: ${status.total_posts}\n` +
          `Scheduled: ${status.scheduled_posts}\n\n` +
          `Action: Run fix_wp_categories.py if categories look wrong.`
  });
}
// Trigger: monthly, 1st of month, 9 AM
```
