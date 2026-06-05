# WordPress Category & Tag Fix Guide

> Fix missing or incorrect categories and tags on existing WordPress posts — manually, with a plugin, or with Python automation.

---

## Part 1: Understanding the Problem

Common issues:
1. **Posts have no category** — they default to "Uncategorized"
2. **Posts have no tags** — not discoverable in search
3. **Wrong category** — posts in wrong section of your site
4. **Duplicate tags** — "CELTA", "celta", "CELTA training" all mean the same thing
5. **Too many or too few tags** — 2-5 focused tags is ideal

---

## Part 2: Manual Fix (Small Number of Posts)

### Via WordPress Admin

1. Go to **Posts → All Posts**
2. Hover over a post → click **Quick Edit**
3. Change Category in the right panel
4. Add Tags in the Tags field
5. Click **Update**

### Bulk Assign Category

1. Go to **Posts → All Posts**
2. Check all posts you want to change
3. From **Bulk Actions** dropdown → select **Edit** → click **Apply**
4. In the bulk edit panel, select the correct Category
5. Click **Update**

---

## Part 3: Plugin-Based Fix

### Recommended Plugins

| Plugin | What It Does |
|--------|-------------|
| **Bulk Edit Post Titles Slugs & Categories** | Bulk reassign categories |
| **Auto Tag** | Automatically add tags based on post content |
| **WP Term Auto Tag** | Auto-tags from a predefined vocabulary |
| **Simple Tags** | Mass tag editing UI |
| **Category Checklist Tree** | Better category management UI |

### Using Auto Tag Plugin

1. Install and activate **Auto Tag** plugin
2. Go to **Posts → Auto Tag Settings**
3. Define your tag vocabulary (e.g., grammar, CELTA, listening)
4. Run "Apply Auto Tags to all posts"
5. The plugin scans all posts and adds matching tags

---

## Part 4: Python Automation Fix (Best for 50+ Posts)

This uses the WordPress REST API with Application Passwords.

### Step 1: Create an Application Password

1. WordPress Admin → **Users → Your Profile**
2. Scroll to **Application Passwords**
3. Name it: `Python Fixer`
4. Click **Add New Application Password**
5. Copy the password (format: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### Step 2: Create `.env` file

```
WP_URL=https://sourovdeb.com
WP_USER=sourov
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

### Step 3: Run the Bulk Fixer Script

```python
# bulk_fix_wp.py
# Fixes categories and tags on all posts without them
# pip install requests python-dotenv

import os
import requests
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('WP_URL')
AUTH = (os.getenv('WP_USER'), os.getenv('WP_APP_PASSWORD'))
REST = f"{BASE_URL}/wp-json/wp/v2"

# ----------------------------------------------------------
# CATEGORY MAPPING — edit this to match your WordPress
# categories (must match exactly, including capitalization)
# ----------------------------------------------------------
CATEGORY_KEYWORDS = {
    'Grammar': ['grammar', 'tense', 'verb', 'noun', 'syntax', 'adjective'],
    'Listening & Phonology': ['listen', 'pronunciation', 'phonology', 'phonics', 'intonation'],
    'Speaking & Fluency': ['speak', 'fluency', 'conversation', 'oral', 'discuss'],
    'CELTA': ['celta', 'teaching practice', 'lesson plan', 'tp ', 'observed lesson'],
    'Reading & Writing': ['reading', 'writing', 'essay', 'paragraph', 'comprehension'],
    'Technology in ELT': ['technology', 'app', 'digital', 'online', 'software'],
    'Career & Professional Development': ['career', 'job', 'certificate', 'professional'],
    'ELT Masterclass': []  # default fallback
}

TAG_KEYWORDS = [
    'grammar', 'listening', 'speaking', 'pronunciation', 'CELTA', 'ELT', 'EFL',
    'ESL', 'vocabulary', 'fluency', 'phonology', 'reading', 'writing', 'teaching'
]


def get_or_create(endpoint, name):
    """Get or create a tag or category by name. Returns its ID."""
    r = requests.get(f"{REST}/{endpoint}", params={'search': name, 'per_page': 5}, auth=AUTH)
    results = [x for x in r.json() if isinstance(x, dict) and x.get('name', '').lower() == name.lower()]
    if results:
        return results[0]['id']
    r = requests.post(f"{REST}/{endpoint}", json={'name': name}, auth=AUTH)
    return r.json().get('id')


def auto_categorize(title, content):
    text = (title + ' ' + content).lower()
    for cat_name, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return cat_name
    return 'ELT Masterclass'


def auto_tag(title):
    text = title.lower()
    return [t for t in TAG_KEYWORDS if t.lower() in text]


def fix_all_posts(dry_run=True):
    page = 1
    fixed = 0
    skipped = 0

    while True:
        r = requests.get(f"{REST}/posts", params={
            'per_page': 50, 'page': page,
            'status': 'publish,draft',
            '_fields': 'id,title,content,tags,categories'
        }, auth=AUTH)

        posts = r.json()
        if not posts or not isinstance(posts, list):
            break

        for post in posts:
            title = post['title']['rendered']
            content = post['content']['rendered']
            current_tags = post.get('tags', [])
            current_cats = post.get('categories', [])

            needs_tags = len(current_tags) == 0
            needs_category = len(current_cats) == 0 or current_cats == [1]  # 1 = Uncategorized

            if not needs_tags and not needs_category:
                skipped += 1
                continue

            tag_names = auto_tag(title)
            cat_name = auto_categorize(title, content)

            print(f"Post: {title}")
            if needs_category:
                print(f"  → Category: {cat_name}")
            if needs_tags:
                print(f"  → Tags: {', '.join(tag_names)}")

            if not dry_run and (needs_category or needs_tags):
                update = {}
                if needs_category:
                    cat_id = get_or_create('categories', cat_name)
                    update['categories'] = [cat_id]
                if needs_tags and tag_names:
                    tag_ids = [get_or_create('tags', t) for t in tag_names]
                    update['tags'] = tag_ids
                if update:
                    requests.post(f"{REST}/posts/{post['id']}", json=update, auth=AUTH)
                    fixed += 1

        page += 1

    print(f"\nDone. Fixed: {fixed} | Skipped (already had tags/cats): {skipped}")
    if dry_run:
        print("DRY RUN — no changes made. Run with dry_run=False to apply.")


if __name__ == '__main__':
    import sys
    dry_run = '--apply' not in sys.argv
    print('DRY RUN MODE (preview only)' if dry_run else 'APPLYING CHANGES')
    fix_all_posts(dry_run=dry_run)
```

### Run it:

```bash
# Preview first (no changes made):
python bulk_fix_wp.py

# Apply changes:
python bulk_fix_wp.py --apply
```

---

## Part 5: Clean Up Duplicate Tags

If you have `CELTA`, `celta`, `CELTA training` all as separate tags:

1. WordPress Admin → **Posts → Tags**
2. Find duplicates — check which has the most posts
3. Keep the most-used one, delete others
4. Or use plugin: **Term Management Tools** (WordPress.org) to merge tags

Or in Python:
```python
# Find near-duplicate tags
r = requests.get(f"{REST}/tags", params={'per_page': 100}, auth=AUTH)
tags = r.json()

for tag in sorted(tags, key=lambda t: t['name'].lower()):
    print(f"{tag['id']:5} | {tag['count']:3} posts | {tag['name']}")
# Review this list and manually delete duplicates via WP admin
```

---

## Part 6: Prevent Future Category/Tag Problems

1. **Add category to your Google Sheets queue template** — Column C should always be filled
2. **Use the `guessCategory()` function** in your Apps Script — it auto-assigns if blank
3. **Set a "Default Category" in WordPress** — Admin → Settings → Writing → Default Post Category
4. **Use Tag Clouds widget** in your sidebar — it motivates consistent tagging
5. **Monthly audit** — run `python bulk_fix_wp.py` monthly to catch missed tags
