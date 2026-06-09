#!/usr/bin/env python3
"""
wordpress_category_tag_fix.py
Audits all WordPress posts and fixes missing categories and tags using AI.

Usage:
  python wordpress_category_tag_fix.py               # fix categories AND tags
  python wordpress_category_tag_fix.py --dry-run     # preview only, no changes
  python wordpress_category_tag_fix.py --seo-only    # fix only Yoast SEO meta
  python wordpress_category_tag_fix.py --report      # print audit report only

Requires:
  pip install requests
  WP_URL, WP_USER, WP_APP_PASSWORD, DEEPSEEK_API_KEY (or OLLAMA_URL)
"""

import os
import json
import time
import argparse
import requests
from html import unescape
from html.parser import HTMLParser

WP_URL   = os.environ.get('WP_URL', 'https://sourovdeb.com').rstrip('/')
WP_USER  = os.environ.get('WP_USER', '')
WP_PASS  = os.environ.get('WP_APP_PASSWORD', '')
DS_KEY   = os.environ.get('DEEPSEEK_API_KEY', '')
OL_URL   = os.environ.get('OLLAMA_URL', 'http://localhost:11434')

WP_AUTH  = (WP_USER, WP_PASS)


# ---- HTML to text helper ----

class _StripHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self._text = []
    def handle_data(self, data):
        self._text.append(data)
    def get_text(self):
        return ' '.join(self._text)

def strip_html(html: str) -> str:
    p = _StripHTML()
    p.feed(html or '')
    return unescape(p.get_text()[:600])


# ---- AI ----

def ask_ai(prompt: str) -> str:
    system = 'You are an SEO expert for a WordPress ELT/teaching blog. Return ONLY valid JSON.'
    if DS_KEY:
        resp = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {DS_KEY}'},
            json={'model': 'deepseek-chat',
                  'messages': [{'role':'system','content':system},
                               {'role':'user','content':prompt}],
                  'max_tokens': 400},
            timeout=45
        )
        return resp.json()['choices'][0]['message']['content']
    # Fall back to Ollama
    resp = requests.post(f'{OL_URL}/api/generate',
                         json={'model':'mistral','prompt':f'{system}\n{prompt}','stream':False},
                         timeout=90)
    return resp.json()['response']


def get_enhancement(title: str, content: str) -> dict:
    plain = strip_html(content)
    prompt = f'''WordPress post analysis:
Title: {title}
Content: {plain[:400]}

Return ONLY JSON (no markdown):
{{
  "seo_title": "title under 60 chars",
  "meta_description": "description under 160 chars",
  "tags": ["tag1", "tag2", "tag3"],
  "category": "most relevant category from: Grammar, Listening & Phonology, Speaking & Fluency, CELTA, Writing & Vocabulary, ELT Masterclass, Technology, Health & Wellbeing"
}}'''
    raw = ask_ai(prompt).replace('```json','').replace('```','').strip()
    try:
        return json.loads(raw)
    except Exception:
        return {}


# ---- WordPress helpers ----

def get_all_posts(max_pages: int = 10) -> list:
    posts = []
    for page in range(1, max_pages + 1):
        resp = requests.get(
            f'{WP_URL}/wp-json/wp/v2/posts',
            params={'per_page': 100, 'page': page, 'status': 'any'},
            auth=WP_AUTH, timeout=30
        )
        if not resp.ok or not resp.json():
            break
        batch = resp.json()
        posts.extend(batch)
        if len(batch) < 100:
            break
    return posts


def ensure_tag(name: str) -> int:
    resp = requests.post(f'{WP_URL}/wp-json/wp/v2/tags', json={'name': name},
                         auth=WP_AUTH, headers={'Content-Type':'application/json'})
    d = resp.json()
    if 'id' in d:
        return d['id']
    return d.get('data', {}).get('term_id', 0)


def ensure_category(name: str) -> int:
    resp = requests.post(f'{WP_URL}/wp-json/wp/v2/categories', json={'name': name},
                         auth=WP_AUTH, headers={'Content-Type':'application/json'})
    d = resp.json()
    if 'id' in d:
        return d['id']
    return d.get('data', {}).get('term_id', 1)


def update_post(post_id: int, data: dict):
    requests.post(
        f'{WP_URL}/wp-json/wp/v2/posts/{post_id}',
        json=data, auth=WP_AUTH,
        headers={'Content-Type': 'application/json'},
        timeout=30
    )


# ---- Main logic ----

def audit(posts: list) -> list:
    issues = []
    for p in posts:
        probs = []
        if not p.get('tags'):                    probs.append('no tags')
        if p.get('categories', [1]) == [1]:       probs.append('uncategorized')
        if not p.get('meta', {}).get('_yoast_wpseo_metadesc'): probs.append('no SEO meta')
        if probs:
            issues.append({'id': p['id'], 'title': p['title']['rendered'],
                           'problems': probs})
    return issues


def fix_posts(posts: list, dry_run: bool = False, seo_only: bool = False):
    issues = audit(posts)
    print(f'Posts needing attention: {len(issues)}')
    fixed = 0
    for item in issues:
        post = next(p for p in posts if p['id'] == item['id'])
        title   = post['title']['rendered']
        content = post['content']['rendered']
        print(f'  [{item["id"]}] {title[:60]} — {item["problems"]}')
        if dry_run:
            continue
        enh = get_enhancement(title, content)
        if not enh:
            print('    AI failed, skipping')
            continue
        update = {}
        if not seo_only:
            if 'no tags' in item['problems'] and enh.get('tags'):
                update['tags'] = [tid for t in enh['tags'] if (tid := ensure_tag(t))]
            if 'uncategorized' in item['problems'] and enh.get('category'):
                cat_id = ensure_category(enh['category'])
                if cat_id and cat_id != 1:
                    update['categories'] = [cat_id]
        if enh.get('meta_description'):
            update.setdefault('meta', {})['_yoast_wpseo_metadesc'] = enh['meta_description']
        if enh.get('seo_title'):
            update.setdefault('meta', {})['_yoast_wpseo_title'] = enh['seo_title']
        if update:
            update_post(post['id'], update)
            print(f'    Fixed: {list(update.keys())}')
            fixed += 1
        time.sleep(1.5)
    print(f'\nDone. Fixed {fixed} posts.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fix WordPress categories and tags')
    parser.add_argument('--dry-run',  action='store_true', help='Show issues but make no changes')
    parser.add_argument('--seo-only', action='store_true', help='Only update SEO meta fields')
    parser.add_argument('--report',   action='store_true', help='Print audit report and exit')
    args = parser.parse_args()

    print('Fetching posts...')
    posts = get_all_posts()
    print(f'Total posts: {len(posts)}')

    if args.report:
        issues = audit(posts)
        print(f'Issues found: {len(issues)}')
        for item in issues:
            print(f'  [{item["id"]}] {item["title"][:60]} — {item["problems"]}')
    else:
        fix_posts(posts, dry_run=args.dry_run, seo_only=args.seo_only)
