#!/usr/bin/env python3
"""
fix_wordpress_categories.py
Bulk-fix missing categories and tags on WordPress posts.

Requires the sourov-category-tag-fixer plugin to be installed and active.

Usage:
  python fix_wordpress_categories.py --preview   # Show what would change
  python fix_wordpress_categories.py --fix        # Apply the fixes
  python fix_wordpress_categories.py --fix-post 123  # Fix one post by ID
"""

import argparse
import json
import os
import requests

WP_BASE = os.environ.get('WP_URL_BASE', 'https://sourovdeb.com/wp-json/sourov/v1')
WP_KEY  = os.environ.get('WP_KEY', 'YOUR_WP_API_KEY_HERE')
HEADERS = {'X-Sourov-Key': WP_KEY}


def preview():
    print('Checking posts for category/tag issues...')
    r = requests.get(f'{WP_BASE}/preview-fixes?limit=200', headers=HEADERS, timeout=30)
    if r.status_code != 200:
        print(f'Error: HTTP {r.status_code}\n{r.text}')
        return
    data = r.json()
    print(f"\nTotal checked:     {data['total_checked']}")
    print(f"Posts needing fix:  {data['posts_needing_fix']}")
    print()
    for item in data.get('details', []):
        print(f"  Post #{item['post_id']}: {item['title'][:60]}")
        if item['needs_category_fix']:
            print(f"    Category: '{item['current_category']}' -> '{item['suggested_category']}'")
        if item['needs_tags_fix']:
            print(f"    Tags: (none) -> {item['suggested_tags']}")


def fix_all(limit=200):
    print(f'Fixing categories and tags on up to {limit} posts...')
    r = requests.post(
        f'{WP_BASE}/fix-posts',
        json={'limit': str(limit)},
        headers={**HEADERS, 'Content-Type': 'application/json'},
        timeout=60
    )
    if r.status_code != 200:
        print(f'Error: HTTP {r.status_code}\n{r.text}')
        return
    data = r.json()
    print(f"\nTotal posts processed: {data['total_posts']}")
    print(f"Posts fixed:           {data['fixed_count']}")
    fixed = [x for x in data.get('results', []) if x.get('category_fixed') or x.get('tags_fixed')]
    if fixed:
        print('\nFixed posts:')
        for item in fixed:
            print(f"  #{item['post_id']}: {item['title'][:60]}")
            if item.get('category_fixed'):
                print(f"    Category -> {item['suggested_category']}")
            if item.get('tags_fixed'):
                print(f"    Tags    -> {item['suggested_tags']}")


def fix_one(post_id):
    print(f'Fixing post #{post_id}...')
    r = requests.post(f'{WP_BASE}/fix-post/{post_id}', headers=HEADERS, timeout=30)
    data = r.json()
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix WordPress post categories and tags')
    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--preview',   action='store_true', help='Show what would change (no writes)')
    group.add_argument('--fix',       action='store_true', help='Apply category and tag fixes')
    group.add_argument('--fix-post',  type=int, metavar='ID', help='Fix a single post by ID')
    parser.add_argument('--limit', type=int, default=200, help='Max posts to process (default 200)')
    args = parser.parse_args()

    if args.preview:
        preview()
    elif args.fix:
        fix_all(args.limit)
    elif args.fix_post:
        fix_one(args.fix_post)
