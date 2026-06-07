#!/usr/bin/env python3
"""
fix_wp_categories_tags.py

Fixes common WordPress category and tag problems:
  - Posts stuck in 'Uncategorized'
  - Duplicate tags with different casing (elt, ELT, Elt)
  - Missing tags not created yet
  - Wrong category assignments

Usage:
  export WP_URL=https://sourovdeb.com
  export WP_USER=your-username
  export WP_PASS=your-app-password
  python3 fix_wp_categories_tags.py

Get App Password: WP Admin > Users > Profile > Application Passwords
"""

import os
import re
import requests
from base64 import b64encode


WP_URL  = os.environ.get('WP_URL',  'https://sourovdeb.com')
WP_USER = os.environ.get('WP_USER', '')
WP_PASS = os.environ.get('WP_PASS', '')

API_BASE = WP_URL.rstrip('/') + '/wp-json/wp/v2'
AUTH     = b64encode(f'{WP_USER}:{WP_PASS}'.encode()).decode()
HEADERS  = {
    'Authorization': f'Basic {AUTH}',
    'Content-Type':  'application/json'
}

# Category rules: if post title/content contains keyword -> assign this category
CATEGORY_RULES = [
    (['celta', 'trainee', 'trainer', 'lesson plan', 'input session'], 'CELTA'),
    (['grammar', 'tense', 'conditional', 'modal', 'passive'],         'Grammar'),
    (['pronunciation', 'phonology', 'phoneme', 'minimal pair',
      'stress', 'intonation', 'listening'],                           'Listening & Phonology'),
    (['speaking', 'fluency', 'oral', 'conversation', 'discussion'],   'Speaking'),
    (['writing', 'essay', 'paragraph', 'composition'],                'Writing Skills'),
    (['vocabulary', 'lexis', 'idiom', 'collocation', 'word'],         'Vocabulary'),
    (['reading', 'text', 'comprehension'],                            'Reading'),
]

# Canonical tag forms (lowercase -> proper form)
TAG_NORMALISE = {
    'elt':           'ELT',
    'english':       'English',
    'celta':         'CELTA',
    'efl':           'EFL',
    'esl':           'ESL',
    'tefl':          'TEFL',
    'tesol':         'TESOL',
    'grammar':       'grammar',
    'listening':     'listening',
    'speaking':      'speaking',
    'pronunciation': 'pronunciation',
    'vocabulary':    'vocabulary',
    'reading':       'reading',
    'writing':       'writing',
}


# ---------------------------------------------------------------------------
# WordPress REST API helpers
# ---------------------------------------------------------------------------

def wp_get(endpoint: str, params: dict = None) -> list | dict:
    r = requests.get(f'{API_BASE}{endpoint}', headers=HEADERS,
                     params=params or {}, timeout=20)
    r.raise_for_status()
    return r.json()


def wp_post(endpoint: str, data: dict) -> dict:
    r = requests.post(f'{API_BASE}{endpoint}', headers=HEADERS,
                      json=data, timeout=20)
    r.raise_for_status()
    return r.json()


def wp_patch(endpoint: str, data: dict) -> dict:
    r = requests.patch(f'{API_BASE}{endpoint}', headers=HEADERS,
                       json=data, timeout=20)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Get all categories / tags from WordPress
# ---------------------------------------------------------------------------

def get_all_terms(taxonomy: str) -> dict:
    """Returns {name_lower: id} for all existing terms."""
    terms = {}
    page  = 1
    while True:
        batch = wp_get(f'/{taxonomy}', {'per_page': 100, 'page': page})
        if not batch:
            break
        for t in batch:
            terms[t['name'].lower()] = t['id']
        if len(batch) < 100:
            break
        page += 1
    return terms


def get_or_create_term(taxonomy: str, name: str, cache: dict) -> int:
    """Return term ID, creating it if it doesn't exist."""
    key = name.lower()
    if key in cache:
        return cache[key]
    print(f'  Creating {taxonomy}: "{name}"')
    result     = wp_post(f'/{taxonomy}', {'name': name})
    new_id     = result['id']
    cache[key] = new_id
    return new_id


# ---------------------------------------------------------------------------
# Guess category from post content
# ---------------------------------------------------------------------------

def guess_category(title: str, content: str, categories: dict) -> int | None:
    text = (title + ' ' + content).lower()
    for keywords, cat_name in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return get_or_create_term('categories', cat_name, categories)
    return None


# ---------------------------------------------------------------------------
# Normalise and deduplicate tags
# ---------------------------------------------------------------------------

def normalise_tags(raw_tag_ids: list, existing_tags: dict) -> list:
    """Flip the cache to id->name, normalise names, return deduplicated ID list."""
    id_to_name = {v: k for k, v in existing_tags.items()}
    normalised_ids = set()
    for tid in raw_tag_ids:
        name = id_to_name.get(tid, '').lower()
        canonical = TAG_NORMALISE.get(name, name)
        new_id = get_or_create_term('tags', canonical, existing_tags)
        normalised_ids.add(new_id)
    return list(normalised_ids)


# ---------------------------------------------------------------------------
# Main fix routine
# ---------------------------------------------------------------------------

def fix_uncategorised_posts():
    """Find posts in Uncategorized and assign correct categories."""
    print('\n=== Fixing uncategorised posts ===')

    categories = get_all_terms('categories')
    uncategorised_id = categories.get('uncategorized', 1)

    # Get all posts currently in Uncategorized
    page = 1
    fixed = 0
    while True:
        posts = wp_get('/posts', {
            'categories': uncategorised_id,
            'per_page':   50,
            'page':       page,
            'status':     'any'
        })
        if not posts:
            break

        for post in posts:
            title   = post['title']['rendered']
            content = re.sub(r'<[^>]+>', ' ', post['content']['rendered'])
            new_cat = guess_category(title, content, categories)

            if new_cat and new_cat != uncategorised_id:
                wp_patch(f'/posts/{post["id"]}', {'categories': [new_cat]})
                cat_name = {v: k for k, v in categories.items()}.get(new_cat, str(new_cat))
                print(f'  Fixed: "{title[:60]}" → {cat_name}')
                fixed += 1

        if len(posts) < 50:
            break
        page += 1

    print(f'Fixed {fixed} posts.')


def fix_duplicate_tags():
    """Merge duplicate tags (different case) into canonical form."""
    print('\n=== Fixing duplicate tags ===')

    tags  = get_all_terms('tags')
    merged = 0

    # Find tags that normalise to the same canonical form
    canonical_to_ids = {}
    for name_lower, tid in tags.items():
        canonical = TAG_NORMALISE.get(name_lower, name_lower)
        canonical_to_ids.setdefault(canonical, []).append(tid)

    for canonical, ids in canonical_to_ids.items():
        if len(ids) <= 1:
            continue
        keep_id = ids[0]
        print(f'  Merging {len(ids)} versions of "{canonical}" → ID {keep_id}')

        # Find all posts that have any of these tag IDs
        all_post_ids = set()
        for tid in ids:
            posts = wp_get('/posts', {'tags': tid, 'per_page': 100})
            for p in posts:
                all_post_ids.add(p['id'])

        # Re-assign to canonical tag only
        for pid in all_post_ids:
            post = wp_get(f'/posts/{pid}')
            current_tags = set(post.get('tags', []))
            current_tags -= set(ids)
            current_tags.add(keep_id)
            wp_patch(f'/posts/{pid}', {'tags': list(current_tags)})
        merged += 1

    print(f'Merged {merged} duplicate tag groups.')


def audit_posts_without_tags():
    """Report posts that have no tags at all."""
    print('\n=== Posts with no tags ===')
    page = 1
    count = 0
    while True:
        posts = wp_get('/posts', {'per_page': 50, 'page': page, 'status': 'publish'})
        if not posts:
            break
        for p in posts:
            if not p.get('tags'):
                print(f'  No tags: [{p["id"]}] {p["title"]["rendered"][:60]}')
                count += 1
        if len(posts) < 50:
            break
        page += 1
    print(f'{count} posts have no tags.')


if __name__ == '__main__':
    if not WP_USER or not WP_PASS:
        print('ERROR: Set WP_USER and WP_PASS environment variables.')
        print('  export WP_USER=your-username')
        print('  export WP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"  (App Password)')
        raise SystemExit(1)

    print(f'Connecting to {WP_URL}...')
    try:
        info = wp_get('/').get if callable(getattr(wp_get('/'), 'get', None)) else {}
        print('Connected.')
    except Exception as e:
        print(f'Connection failed: {e}')
        raise SystemExit(1)

    fix_uncategorised_posts()
    fix_duplicate_tags()
    audit_posts_without_tags()

    print('\nDone.')
