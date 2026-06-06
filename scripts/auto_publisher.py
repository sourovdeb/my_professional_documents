#!/usr/bin/env python3
"""
auto_publisher.py - Folder Watcher: any .md file dropped in ~/wordpress_queue/
becomes a WordPress draft automatically.

Run: python auto_publisher.py
Schedule: cron */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py

Requirements: pip install requests python-dotenv
"""

import os
import json
import time
import requests
import logging
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configuration
WATCH_DIR  = Path.home() / 'wordpress_queue'
ARCHIVE_DIR = WATCH_DIR / 'archive'
WP_URL     = os.getenv('WP_URL', 'https://sourovdeb.com')
API_KEY    = os.getenv('WP_API_KEY', '')
DEEPSEEK_KEY = os.getenv('DEEPSEEK_API_KEY', '')

API_ENDPOINT = f"{WP_URL.rstrip('/')}/wp-json/sourov/v1/ai-post"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler(WATCH_DIR / 'auto_publisher.log')]
)
log = logging.getLogger(__name__)


def suggest_tags(title: str) -> str:
    keyword_map = {
        'grammar': 'grammar', 'listen': 'listening', 'speak': 'speaking',
        'vocabulary': 'vocabulary', 'idiom': 'idioms', 'celta': 'CELTA',
        'phonology': 'phonology', 'pronunciation': 'pronunciation',
        'write': 'writing', 'fluency': 'fluency', 'english': 'English'
    }
    tags = [tag for kw, tag in keyword_map.items() if kw in title.lower()]
    return ', '.join(tags[:5]) or 'ELT, English'


def guess_category(title: str, body: str) -> str:
    text = (title + ' ' + body).lower()
    if any(k in text for k in ['grammar', 'tense', 'verb', 'article']):
        return 'Grammar'
    if any(k in text for k in ['listen', 'phonology', 'pronunciation']):
        return 'Listening & Phonology'
    if any(k in text for k in ['celta', 'lesson plan']):
        return 'CELTA'
    if any(k in text for k in ['speak', 'fluency']):
        return 'Speaking & Fluency'
    if any(k in text for k in ['vocabulary', 'idiom']):
        return 'Vocabulary'
    return 'ELT Masterclass'


def generate_seo_deepseek(title: str, body: str) -> dict:
    """Call DeepSeek API for SEO metadata. Falls back gracefully if unavailable."""
    if not DEEPSEEK_KEY:
        return {}
    prompt = (f'Return ONLY valid JSON, no markdown:\n'
              f'Title: {title}\nExcerpt: {body[:300]}\n'
              f'{{"seo_title": "", "meta_desc": "", "tags": [], "category": ""}}')
    try:
        r = requests.post(
            'https://api.deepseek.com/v1/chat/completions',
            headers={'Authorization': f'Bearer {DEEPSEEK_KEY}', 'Content-Type': 'application/json'},
            json={'model': 'deepseek-chat',
                  'messages': [{'role': 'user', 'content': prompt}],
                  'temperature': 0.2, 'max_tokens': 250},
            timeout=20
        )
        text = r.json()['choices'][0]['message']['content']
        text = text.replace('```json', '').replace('```', '').strip()
        return json.loads(text)
    except Exception as e:
        log.warning(f'DeepSeek SEO failed: {e}')
        return {}


def process_file(filepath: Path):
    """Read a markdown file and publish it to WordPress as a draft."""
    log.info(f'Processing: {filepath.name}')

    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        log.error(f'Cannot read {filepath}: {e}')
        return

    lines = content.strip().split('\n')
    # First line starting with # is the title
    title = lines[0].lstrip('#').strip() if lines else filepath.stem
    body_md = '\n'.join(lines[1:]).strip()

    # Simple markdown-to-HTML conversion
    body_html = ''
    for paragraph in body_md.split('\n\n'):
        p = paragraph.strip()
        if not p:
            continue
        if p.startswith('## '):
            body_html += f'<h2>{p[3:]}</h2>\n'
        elif p.startswith('# '):
            body_html += f'<h2>{p[2:]}</h2>\n'
        else:
            body_html += f'<p>{p}</p>\n'

    # Remove Logseq [[link]] syntax
    import re
    body_html = re.sub(r'\[\[(.*?)\]\]', r'\1', body_html)

    # Get SEO from DeepSeek (or fallback to local rules)
    seo = generate_seo_deepseek(title, body_md)
    category = seo.get('category') or guess_category(title, body_md)
    tags = ', '.join(seo.get('tags') or []) or suggest_tags(title)
    seo_title = seo.get('seo_title') or title[:60]
    meta_desc = seo.get('meta_desc') or body_md[:155].replace('\n', ' ')

    payload = {
        'title': title,
        'content': body_html,
        'status': 'draft',
        'category': category,
        'tags': tags,
        'seo_title': seo_title,
        'meta_description': meta_desc,
    }

    try:
        r = requests.post(
            API_ENDPOINT,
            headers={'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        if r.status_code == 200:
            post_id = r.json().get('post_id')
            log.info(f'Published draft: "{title}" | ID: {post_id}')
            # Archive the file
            ARCHIVE_DIR.mkdir(exist_ok=True)
            filepath.rename(ARCHIVE_DIR / filepath.name)
        else:
            log.error(f'WordPress error {r.status_code}: {r.text[:200]}')
    except Exception as e:
        log.error(f'Request failed: {e}')


def main():
    WATCH_DIR.mkdir(exist_ok=True)
    ARCHIVE_DIR.mkdir(exist_ok=True)

    md_files = list(WATCH_DIR.glob('*.md'))
    if not md_files:
        log.info('No .md files found in queue.')
        return

    log.info(f'Found {len(md_files)} file(s) to process.')
    for filepath in md_files:
        process_file(filepath)
        time.sleep(1.5)


if __name__ == '__main__':
    main()
