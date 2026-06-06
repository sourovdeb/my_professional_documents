#!/usr/bin/env python3
"""
fix_wp_categories.py - Audit and fix WordPress categories and tags.

What it does:
  1. Audits current state (prints report)
  2. Moves Uncategorized posts to ELT Masterclass
  3. Merges duplicate/near-duplicate categories
  4. Deletes empty categories
  5. Normalizes tag names

Requirements: pip install requests python-dotenv
Usage: python fix_wp_categories.py [--audit-only]
"""

import requests
import json
import os
import sys
import base64
from dotenv import load_dotenv

load_dotenv()

WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com')
WP_USER = os.getenv('WP_USER', '')
WP_APP_PASSWORD = os.getenv('WP_APP_PASSWORD', '')

DEFAULT_CATEGORY = 'ELT Masterclass'

# Category merges: (from_name, to_name) — edit to match your actual duplicates
CATEGORY_MERGES = [
    ('elt', DEFAULT_CATEGORY),
    ('ELT', DEFAULT_CATEGORY),
    ('Uncategorized', DEFAULT_CATEGORY),
    ('CELTA Course', 'CELTA'),
    ('Listening', 'Listening & Phonology'),
    ('Speaking', 'Speaking & Fluency'),
]


def auth_header() -> dict:
    creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    return {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}


def get_categories() -> list:
    r = requests.get(f'{WP_URL}/wp-json/wp/v2/categories',
                     params={'per_page': 100}, headers=auth_header())
    return r.json() if r.ok else []


def get_tags() -> list:
    r = requests.get(f'{WP_URL}/wp-json/wp/v2/tags',
                     params={'per_page': 100}, headers=auth_header())
    return r.json() if r.ok else []


def find_category_id(name: str) -> int | None:
    cats = get_categories()
    for c in cats:
        if c['name'].lower() == name.lower() or c['slug'] == name.lower():
            return c['id']
    return None


def get_or_create_category(name: str) -> int:
    existing = find_category_id(name)
    if existing:
        return existing
    r = requests.post(f'{WP_URL}/wp-json/wp/v2/categories',
                      headers=auth_header(), json={'name': name})
    return r.json()['id']


def reassign_posts(from_cat_id: int, to_cat_id: int, from_name: str, to_name: str):
    page = 1
    moved = 0
    while True:
        r = requests.get(f'{WP_URL}/wp-json/wp/v2/posts',
                         params={'categories': from_cat_id, 'per_page': 100,
                                 'page': page, 'status': 'any'},
                         headers=auth_header())
        posts = r.json()
        if not posts or not isinstance(posts, list):
            break
        for post in posts:
            new_cats = [c for c in post['categories'] if c != from_cat_id]
            if to_cat_id not in new_cats:
                new_cats.append(to_cat_id)
            requests.post(f'{WP_URL}/wp-json/wp/v2/posts/{post["id"]}',
                          headers=auth_header(), json={'categories': new_cats})
            moved += 1
        if len(posts) < 100:
            break
        page += 1
    print(f'  Moved {moved} post(s): "{from_name}" → "{to_name}"')
    return moved


def delete_category_if_empty(name: str):
    cat_id = find_category_id(name)
    if not cat_id:
        return
    r = requests.get(f'{WP_URL}/wp-json/wp/v2/categories/{cat_id}', headers=auth_header())
    cat = r.json()
    if cat.get('count', 0) > 0:
        print(f'  Skipped deleting "{name}" — still has {cat["count"]} post(s)')
        return
    requests.delete(f'{WP_URL}/wp-json/wp/v2/categories/{cat_id}',
                    headers=auth_header())
    print(f'  Deleted empty category: "{name}"')


def normalize_tags():
    tags = get_tags()
    changed = 0
    for tag in tags:
        normalized = tag['name'].lower().replace(' ', '-').replace('_', '-')
        if normalized != tag['name']:
            requests.post(f'{WP_URL}/wp-json/wp/v2/tags/{tag["id"]}',
                          headers=auth_header(),
                          json={'name': normalized, 'slug': normalized})
            print(f'  Normalized tag: "{tag["name"]}" → "{normalized}"')
            changed += 1
    print(f'  Normalized {changed} tag(s).')


def audit():
    print('=== CATEGORY AUDIT ===')
    cats = get_categories()
    if not cats:
        print('  (Could not fetch categories — check credentials)')
        return
    for c in sorted(cats, key=lambda x: x['count'], reverse=True):
        flag = '  ← EMPTY — consider deleting' if c['count'] == 0 else ''
        print(f"  [{c['count']:3d} posts] {c['name']:40s} (ID:{c['id']}){flag}")

    print('\n=== TAG AUDIT ===')
    tags = get_tags()
    orphans = [t for t in tags if t['count'] <= 1]
    good = [t for t in tags if t['count'] > 1]
    print(f'Healthy tags ({len(good)}):')
    for t in sorted(good, key=lambda x: x['count'], reverse=True)[:15]:
        print(f"  [{t['count']:3d} uses] {t['name']}")
    print(f'\nOrphaned tags to clean ({len(orphans)}):')
    for t in orphans:
        print(f"  [{t['count']:3d} use ] {t['name']:30s} (ID:{t['id']})")
    print(f'\nSummary: {len(cats)} categories, {len(tags)} tags, {len(orphans)} orphaned')


def fix_all():
    print('\n[1/4] Moving Uncategorized posts...')
    unc_id = find_category_id('Uncategorized')
    target_id = get_or_create_category(DEFAULT_CATEGORY)
    if unc_id and unc_id != target_id:
        reassign_posts(unc_id, target_id, 'Uncategorized', DEFAULT_CATEGORY)

    print('\n[2/4] Merging duplicate categories...')
    for from_name, to_name in CATEGORY_MERGES:
        from_id = find_category_id(from_name)
        if not from_id:
            continue
        to_id = get_or_create_category(to_name)
        if from_id != to_id:
            reassign_posts(from_id, to_id, from_name, to_name)

    print('\n[3/4] Deleting empty categories...')
    for from_name, _ in CATEGORY_MERGES:
        delete_category_if_empty(from_name)

    print('\n[4/4] Normalizing tags...')
    normalize_tags()

    print('\nDone! Run with --audit-only to verify.')


if __name__ == '__main__':
    if not WP_USER or not WP_APP_PASSWORD:
        print('ERROR: Set WP_USER and WP_APP_PASSWORD in your .env file')
        sys.exit(1)

    audit()

    if '--audit-only' not in sys.argv:
        print('\nStarting fixes...')
        fix_all()
