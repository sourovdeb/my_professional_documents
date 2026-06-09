#!/usr/bin/env python3
"""
auto_publisher.py
Watches a folder for .md files and publishes them to WordPress as drafts.
Uses DeepSeek/Ollama/Groq to auto-enhance SEO, tags, and category.

Usage:
  python auto_publisher.py                    # watch ~/Dropbox/wordpress_queue
  python auto_publisher.py --folder ~/drafts  # custom folder
  python auto_publisher.py --generate "CELTA lesson planning tips"
  python auto_publisher.py --fix-categories   # fix all posts with missing tags/categories

Environment variables:
  DEEPSEEK_API_KEY   - DeepSeek API key (cheapest option)
  OLLAMA_URL         - Ollama local URL (default: http://localhost:11434)
  WP_URL             - WordPress site URL
  WP_API_KEY         - Plugin API key (X-Sourov-Key header)
  WP_USER            - WordPress username
  WP_APP_PASSWORD    - WordPress app password
"""

import os
import json
import time
import argparse
import requests
from pathlib import Path

# ---- Config from environment ----
DEEPSEEK_KEY = os.environ.get('DEEPSEEK_API_KEY', '')
OLLAMA_URL   = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
WP_URL       = os.environ.get('WP_URL', 'https://sourovdeb.com').rstrip('/')
WP_API_KEY   = os.environ.get('WP_API_KEY', '')
WP_USER      = os.environ.get('WP_USER', '')
WP_APP_PASS  = os.environ.get('WP_APP_PASSWORD', '')

DEEPSEEK_URL = 'https://api.deepseek.com/v1/chat/completions'
WP_ENDPOINT  = f'{WP_URL}/wp-json/sourov/v1/ai-post'


# ---- AI Providers ----

def ask_deepseek(prompt: str, system: str = None) -> str:
    messages = []
    if system:
        messages.append({'role': 'system', 'content': system})
    messages.append({'role': 'user', 'content': prompt})
    resp = requests.post(
        DEEPSEEK_URL,
        headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
        json={'model': 'deepseek-chat', 'messages': messages, 'max_tokens': 1500},
        timeout=60
    )
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content']


def ask_ollama(prompt: str, model: str = 'mistral') -> str:
    resp = requests.post(
        f'{OLLAMA_URL}/api/generate',
        json={'model': model, 'prompt': prompt, 'stream': False},
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()['response']


def ask_ai(prompt: str, system: str = None) -> str:
    """Try DeepSeek first, fall back to Ollama."""
    if DEEPSEEK_KEY:
        try:
            return ask_deepseek(prompt, system)
        except Exception as e:
            print(f'  DeepSeek failed ({e}), trying Ollama...')
    return ask_ollama(f'{system}\n\n{prompt}' if system else prompt)


# ---- SEO Enhancement ----

def enhance_post(title: str, content: str) -> dict:
    system = 'You are an SEO expert. Return ONLY valid JSON, no markdown.'
    prompt = f'''Post title: {title}
Content preview: {content[:400]}

Return JSON:
{{"seo_title":"","meta_description":"","tags":[],"category":""}}'''
    raw = ask_ai(prompt, system)
    raw = raw.replace('```json', '').replace('```', '').strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {}


def generate_post(topic: str) -> dict:
    system = 'You are a WordPress content writer. Return ONLY valid JSON, no markdown.'
    prompt = f'''Write a 600-word WordPress blog post about: "{topic}"

Return JSON:
{{"title":"","content":"<HTML>","meta_description":"","seo_title":"","tags":[],"category":""}}'''
    raw = ask_ai(prompt, system)
    raw = raw.replace('```json', '').replace('```', '').strip()
    return json.loads(raw)


# ---- WordPress API ----

def publish_post(payload: dict) -> dict:
    headers = {'X-Sourov-Key': WP_API_KEY, 'Content-Type': 'application/json'}
    auth = (WP_USER, WP_APP_PASS) if WP_USER and WP_APP_PASS else None
    resp = requests.post(WP_ENDPOINT, json=payload, headers=headers, auth=auth, timeout=30)
    return resp.json()


def get_wp_posts(per_page: int = 100, status: str = 'any') -> list:
    auth = (WP_USER, WP_APP_PASS)
    resp = requests.get(
        f'{WP_URL}/wp-json/wp/v2/posts',
        params={'per_page': per_page, 'status': status},
        auth=auth, timeout=30
    )
    return resp.json() if resp.ok else []


def ensure_tag(name: str) -> int:
    auth = (WP_USER, WP_APP_PASS)
    resp = requests.post(f'{WP_URL}/wp-json/wp/v2/tags', json={'name': name}, auth=auth)
    data = resp.json()
    if 'id' in data:
        return data['id']
    return data.get('data', {}).get('term_id', 0)


def ensure_category(name: str) -> int:
    auth = (WP_USER, WP_APP_PASS)
    resp = requests.post(f'{WP_URL}/wp-json/wp/v2/categories', json={'name': name}, auth=auth)
    data = resp.json()
    if 'id' in data:
        return data['id']
    return data.get('data', {}).get('term_id', 1)


# ---- Fix categories/tags on all posts ----

def fix_all_categories_tags():
    print('Fetching all posts...')
    posts = get_wp_posts()
    fixed = 0
    for post in posts:
        has_tags = bool(post.get('tags'))
        is_uncategorized = post.get('categories', [1]) == [1]
        if has_tags and not is_uncategorized:
            continue
        title = post['title']['rendered']
        content = post['content']['rendered']
        print(f'  Fixing: {title[:60]}')
        enhanced = enhance_post(title, content)
        update = {}
        if not has_tags and enhanced.get('tags'):
            update['tags'] = [ensure_tag(t) for t in enhanced['tags']]
        if is_uncategorized and enhanced.get('category'):
            update['categories'] = [ensure_category(enhanced['category'])]
        if update:
            auth = (WP_USER, WP_APP_PASS)
            requests.post(
                f'{WP_URL}/wp-json/wp/v2/posts/{post["id"]}',
                json=update, auth=auth,
                headers={'Content-Type': 'application/json'}
            )
            fixed += 1
        time.sleep(1)
    print(f'Fixed {fixed} posts.')


# ---- Folder watcher ----

def process_file(filepath: Path, archive_dir: Path):
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')
    title = lines[0].lstrip('#').strip() or filepath.stem
    body = '\n'.join(lines[1:])

    print(f'  Processing: {title}')
    enhanced = enhance_post(title, body)

    payload = {
        'title': enhanced.get('improved_title', title),
        'content': body,
        'status': 'draft',
        'tags': ','.join(enhanced.get('tags', [])),
        'category': enhanced.get('category', 'ELT Masterclass'),
        'meta_description': enhanced.get('meta_description', body[:160].replace('\n', ' ')),
        'seo_title': enhanced.get('seo_title', title),
    }

    result = publish_post(payload)
    post_id = result.get('post_id') or result.get('id')
    if post_id:
        print(f'  Published as draft — ID:{post_id}')
        filepath.rename(archive_dir / filepath.name)
    else:
        print(f'  Failed: {str(result)[:120]}')


def watch_folder(folder: str):
    watch_dir = Path(folder).expanduser()
    archive_dir = watch_dir / 'archive'
    archive_dir.mkdir(parents=True, exist_ok=True)
    md_files = list(watch_dir.glob('*.md'))
    if not md_files:
        print(f'No .md files in {watch_dir}')
        return
    print(f'Found {len(md_files)} files in {watch_dir}')
    for f in md_files:
        process_file(f, archive_dir)
        time.sleep(2)


# ---- Entry point ----

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto-publish markdown drafts to WordPress')
    parser.add_argument('--folder', default='~/Dropbox/wordpress_queue', help='Watch folder')
    parser.add_argument('--fix-categories', action='store_true', help='Fix all posts categories/tags')
    parser.add_argument('--generate', metavar='TOPIC', help='Generate and publish a post on topic')
    args = parser.parse_args()

    if args.fix_categories:
        fix_all_categories_tags()
    elif args.generate:
        print(f'Generating post: {args.generate}')
        post = generate_post(args.generate)
        result = publish_post(post)
        print(f'Done: {result}')
    else:
        watch_folder(args.folder)
