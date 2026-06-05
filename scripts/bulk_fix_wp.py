#!/usr/bin/env python3
"""
bulk_fix_wp.py
Retroactively fixes categories and tags on existing WordPress posts.

Setup:
  pip install requests python-dotenv

Create .env file:
  WP_URL=https://sourovdeb.com
  WP_USER=sourov
  WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
  (Get app password: WP Admin → Users → Profile → Application Passwords)

Usage:
  python bulk_fix_wp.py          # dry run (preview only, no changes)
  python bulk_fix_wp.py --apply  # actually apply changes
"""

import os, sys, re, requests
from dotenv import load_dotenv
load_dotenv()

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com')
REST = f"{WP_URL.rstrip('/')}/wp-json/wp/v2"
AUTH = (os.getenv('WP_USER', 'sourov'), os.getenv('WP_APP_PASSWORD', ''))

CATEGORY_KEYWORDS = {
    'Grammar':                       ['grammar','tense','verb','noun','syntax','adjective'],
    'Listening & Phonology':         ['listen','pronunciation','phonology','phonics','intonation','accent'],
    'Speaking & Fluency':            ['speak','fluency','conversation','oral','discuss','talk'],
    'CELTA':                         ['celta','teaching practice','lesson plan','tp ','observed lesson'],
    'Reading & Writing':             ['reading','writing','essay','paragraph','comprehension','text'],
    'Technology in ELT':             ['technology','app','digital','online','software','tool'],
    'Career & Professional Development': ['career','job','certificate','professional','qualification'],
}

TAG_VOCAB = ['grammar','listening','speaking','pronunciation','CELTA','ELT','EFL',
             'ESL','vocabulary','fluency','phonology','reading','writing','teaching']


def get_or_create(endpoint, name):
    name = name.strip()
    r = requests.get(f"{REST}/{endpoint}", params={'search': name, 'per_page': 5}, auth=AUTH, timeout=15)
    items = [x for x in r.json() if isinstance(x, dict) and x.get('name','').lower() == name.lower()]
    if items:
        return items[0]['id']
    r2 = requests.post(f"{REST}/{endpoint}", json={'name': name}, auth=AUTH, timeout=15)
    return r2.json().get('id')


def auto_categorize(title, content):
    text = (title + ' ' + content).lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in text for k in kws):
            return cat
    return 'ELT Masterclass'


def auto_tag(title):
    return [t for t in TAG_VOCAB if t.lower() in title.lower()]


def fix_all_posts(dry_run=True):
    page, fixed, skipped = 1, 0, 0
    print(f'Mode: {"DRY RUN (no changes)" if dry_run else "APPLYING CHANGES"}')
    print(f'WordPress: {WP_URL}\n')

    while True:
        r = requests.get(f"{REST}/posts", params={
            'per_page': 50, 'page': page, 'status': 'publish,draft',
            '_fields': 'id,title,content,tags,categories'
        }, auth=AUTH, timeout=20)

        posts = r.json()
        if not posts or not isinstance(posts, list):
            break

        for post in posts:
            title    = post['title']['rendered']
            content  = re.sub(r'<[^>]+>', '', post['content']['rendered'])[:500]
            has_tags = bool(post.get('tags'))
            has_cat  = bool(post.get('categories')) and post['categories'] != [1]

            if has_tags and has_cat:
                skipped += 1
                continue

            tag_names = auto_tag(title)
            cat_name  = auto_categorize(title, content)

            print(f"Post #{post['id']}: {title[:60]}")
            if not has_cat:
                print(f"  Category: {cat_name}")
            if not has_tags:
                print(f"  Tags: {', '.join(tag_names) or '(none found)'}")

            if not dry_run:
                update = {}
                if not has_cat:
                    cat_id = get_or_create('categories', cat_name)
                    if cat_id: update['categories'] = [cat_id]
                if not has_tags and tag_names:
                    tag_ids = [get_or_create('tags', t) for t in tag_names]
                    update['tags'] = [t for t in tag_ids if t]
                if update:
                    requests.post(f"{REST}/posts/{post['id']}", json=update, auth=AUTH, timeout=15)
                    fixed += 1

        page += 1

    print(f'\nDone. Fixed: {fixed} | Skipped (already OK): {skipped}')
    if dry_run:
        print('\nTo apply these changes: python bulk_fix_wp.py --apply')


if __name__ == '__main__':
    fix_all_posts(dry_run='--apply' not in sys.argv)
