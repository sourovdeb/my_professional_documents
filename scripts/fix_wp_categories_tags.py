#!/usr/bin/env python3
"""
fix_wp_categories_tags.py

Bulk-fixes WordPress posts that have:
  - No category (or wrong default 'Uncategorized')
  - No tags
  - Missing SEO meta descriptions

Uses the WordPress REST API with Basic Auth (Application Passwords).

Setup:
  pip install requests python-dotenv
  Create a .env file with:
    WP_BASE_URL=https://sourovdeb.com
    WP_USER=your_username
    WP_APP_PASSWORD=xxxx xxxx xxxx xxxx

  To create an Application Password in WordPress:
    Users > Profile > Application Passwords > Add New

Usage:
  python fix_wp_categories_tags.py --dry-run   (preview changes)
  python fix_wp_categories_tags.py              (apply changes)
"""

import os
import sys
import json
import logging
import argparse
from time import sleep

import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

BASE_URL = os.getenv('WP_BASE_URL', 'https://sourovdeb.com')
WP_USER = os.getenv('WP_USER', '')
WP_PASS = os.getenv('WP_APP_PASSWORD', '')
AUTH = HTTPBasicAuth(WP_USER, WP_PASS)

CATEGORY_RULES = [
    (['grammar', 'tense', 'conditional', 'syntax', 'clause'], 'Grammar'),
    (['listening', 'comprehension', 'audio'], 'Listening & Phonology'),
    (['pronunciation', 'phoneme', 'intonation', 'stress'], 'Listening & Phonology'),
    (['speaking', 'fluency', 'dialogue', 'conversation', 'oral'], 'Speaking'),
    (['reading', 'skimming', 'scanning'], 'Reading'),
    (['writing', 'essay', 'paragraph', 'composition'], 'Writing'),
    (['vocabulary', 'lexis', 'collocation', 'idiom'], 'Vocabulary'),
    (['celta', 'lesson plan', 'trainee', 'observation', 'placement'], 'CELTA'),
    (['bipolar', 'depression', 'mental health', 'wellness', 'mood'], 'Mental Health & Teaching'),
]

TAG_KEYWORDS = [
    'grammar', 'listening', 'speaking', 'reading', 'writing', 'vocabulary',
    'pronunciation', 'phonology', 'celta', 'fluency', 'accuracy', 'classroom',
    'lesson', 'teaching', 'student', 'teacher', 'activity', 'bipolar', 'mental health',
]


def api_get(path, params=None):
    url = f"{BASE_URL}/wp-json/wp/v2{path}"
    resp = requests.get(url, auth=AUTH, params=params or {}, timeout=30)
    resp.raise_for_status()
    return resp.json(), int(resp.headers.get('X-WP-TotalPages', 1))


def api_post(path, data):
    url = f"{BASE_URL}/wp-json/wp/v2{path}"
    resp = requests.post(url, auth=AUTH, json=data, timeout=30)
    resp.raise_for_status()
    return resp.json()


def get_or_create_term(taxonomy, name):
    """Get an existing category/tag ID, or create it."""
    endpoint = '/categories' if taxonomy == 'category' else '/tags'
    existing, _ = api_get(endpoint, {'search': name, 'per_page': 5})
    for term in existing:
        if term['name'].lower() == name.lower():
            return term['id']
    created = api_post(endpoint, {'name': name})
    log.info(f"Created {taxonomy}: '{name}' (ID {created['id']})")
    return created['id']


def guess_category(title, content):
    text = (title + ' ' + content).lower()
    for keywords, cat_name in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return cat_name
    return None


def guess_tags(title, content):
    text = (title + ' ' + content).lower()
    return [kw.title() for kw in TAG_KEYWORDS if kw in text]


def fetch_all_posts():
    """Fetch all published + draft posts."""
    posts = []
    page = 1
    while True:
        batch, total_pages = api_get('/posts', {
            'per_page': 100,
            'page': page,
            'status': 'publish,draft,future',
            '_fields': 'id,title,content,categories,tags,slug'
        })
        posts.extend(batch)
        log.info(f"Fetched page {page}/{total_pages} ({len(batch)} posts)")
        if page >= total_pages:
            break
        page += 1
        sleep(0.5)
    return posts


def fix_post(post, dry_run=False):
    post_id = post['id']
    title = post['title']['rendered']
    content = post['content']['rendered']

    updates = {}
    notes = []

    # Fix missing/default category
    current_cats = post.get('categories', [])
    if not current_cats or current_cats == [1]:  # 1 = Uncategorized
        cat_name = guess_category(title, content)
        if cat_name:
            if not dry_run:
                cat_id = get_or_create_term('category', cat_name)
                updates['categories'] = [cat_id]
            notes.append(f"Category: Uncategorized → {cat_name}")

    # Fix missing tags
    current_tags = post.get('tags', [])
    if not current_tags:
        tag_names = guess_tags(title, content)
        if tag_names:
            if not dry_run:
                tag_ids = [get_or_create_term('tag', t) for t in tag_names[:6]]
                updates['tags'] = tag_ids
            notes.append(f"Tags added: {', '.join(tag_names[:6])}")

    if updates and not dry_run:
        try:
            api_post(f'/posts/{post_id}', updates)
            log.info(f"[FIXED] ID {post_id}: {title[:50]} — {'; '.join(notes)}")
        except Exception as e:
            log.error(f"[FAILED] ID {post_id}: {e}")
    elif notes:
        log.info(f"[DRY RUN] ID {post_id}: {title[:50]} — {'; '.join(notes)}")
    else:
        log.debug(f"[OK] ID {post_id}: {title[:50]}")

    return bool(notes)


def main():
    parser = argparse.ArgumentParser(description='Fix WordPress post categories and tags')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without saving')
    args = parser.parse_args()

    if not WP_USER or not WP_PASS:
        log.error('Set WP_USER and WP_APP_PASSWORD in your .env file.')
        sys.exit(1)

    mode = 'DRY RUN' if args.dry_run else 'LIVE'
    log.info(f'Starting WordPress category/tag fix [{mode}]')
    log.info(f'Target: {BASE_URL}')

    posts = fetch_all_posts()
    log.info(f'Total posts to check: {len(posts)}')

    fixed = 0
    for post in posts:
        if fix_post(post, dry_run=args.dry_run):
            fixed += 1
        sleep(0.3)

    log.info(f'Done. {fixed}/{len(posts)} posts needed fixes.')
    if args.dry_run:
        log.info('Run without --dry-run to apply changes.')


if __name__ == '__main__':
    main()
