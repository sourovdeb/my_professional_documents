#!/usr/bin/env python3
"""
auto_publisher.py  —  Folder Watcher Auto-Publisher

Watches a folder for new Markdown files and publishes them to WordPress.
Run continuously or via cron every 15 minutes.

Usage:
  export WP_URL=https://sourovdeb.com/wp-json/sourov/v1/ai-post
  export WP_KEY=your-plugin-key
  python3 auto_publisher.py

Or cron (every 15 min):
  */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py
"""

import os
import re
import requests
from pathlib import Path


WATCH_DIR   = Path.home() / 'wordpress_queue'
ARCHIVE_DIR = WATCH_DIR / 'published'
WP_URL      = os.environ.get('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY      = os.environ.get('WP_KEY', '')


CATEGORY_RULES = [
    (['celta', 'trainee', 'lesson plan'],                     'CELTA'),
    (['grammar', 'tense', 'conditional', 'passive'],          'Grammar'),
    (['pronunciation', 'phonology', 'listening', 'minimal'],  'Listening & Phonology'),
    (['speaking', 'fluency', 'conversation', 'oral'],         'Speaking'),
    (['writing', 'essay', 'composition', 'paragraph'],        'Writing Skills'),
    (['vocabulary', 'lexis', 'idiom', 'word family'],         'Vocabulary'),
    (['reading', 'text', 'comprehension'],                    'Reading'),
]

TAG_KEYWORDS = [
    'grammar', 'listening', 'speaking', 'pronunciation',
    'vocabulary', 'reading', 'writing', 'CELTA', 'ELT',
    'phonology', 'fluency', 'idioms'
]


def guess_category(title: str, body: str) -> str:
    text = (title + ' ' + body).lower()
    for keywords, cat in CATEGORY_RULES:
        if any(k in text for k in keywords):
            return cat
    return 'ELT Masterclass'


def suggest_tags(title: str, body: str) -> str:
    text  = (title + ' ' + body).lower()
    found = [tag for tag in TAG_KEYWORDS if tag.lower() in text]
    return ','.join(found[:5])


def markdown_to_html(md: str) -> str:
    """Minimal Markdown -> HTML conversion for basic formatting."""
    lines   = md.split('\n')
    html    = []
    in_list = False

    for line in lines:
        line = line.rstrip()
        if line.startswith('## '):
            if in_list: html.append('</ul>'); in_list = False
            html.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('# '):
            pass  # Skip — title extracted separately
        elif line.startswith('- ') or line.startswith('* '):
            if not in_list: html.append('<ul>'); in_list = True
            html.append(f'<li>{line[2:]}</li>')
        elif line.strip() == '':
            if in_list: html.append('</ul>'); in_list = False
        else:
            if in_list: html.append('</ul>'); in_list = False
            # Bold and italic
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', line)
            html.append(f'<p>{line}</p>')

    if in_list:
        html.append('</ul>')
    return '\n'.join(html)


def process_file(filepath: Path) -> bool:
    text  = filepath.read_text(encoding='utf-8').strip()
    lines = text.split('\n')

    # Extract title from first heading
    title = ''
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title      = line[2:].strip()
            body_start = i + 1
            break

    if not title:
        # Use filename as title if no heading found
        title      = filepath.stem.replace('-', ' ').replace('_', ' ').title()
        body_start = 0

    raw_body = '\n'.join(lines[body_start:]).strip()

    # Convert Logseq [[links]] to plain text
    raw_body = re.sub(r'\[\[(.+?)\]\]', r'\1', raw_body)

    # Convert Markdown to HTML if needed
    if '<p>' not in raw_body and '<h2>' not in raw_body:
        body = markdown_to_html(raw_body)
    else:
        body = raw_body

    category  = guess_category(title, raw_body)
    tags      = suggest_tags(title, raw_body)
    meta_desc = re.sub(r'<[^>]+>', ' ', body).strip()[:160]

    payload = {
        'title':            title,
        'content':          body,
        'category':         category,
        'tags':             tags,
        'meta_description': meta_desc,
        'status':           'draft'
    }

    headers = {
        'X-Sourov-Key':  WP_KEY,
        'Content-Type':  'application/json'
    }

    try:
        r = requests.post(WP_URL, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        result = r.json()
        post_id = result.get('post_id') or result.get('id')
        print(f'  Published: "{title}" → ID {post_id}')
        return True
    except Exception as e:
        print(f'  Failed: "{title}" — {e}')
        return False


def main():
    if not WP_KEY:
        print('ERROR: Set WP_KEY environment variable.')
        return

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    md_files = list(WATCH_DIR.glob('*.md'))
    if not md_files:
        print(f'No .md files found in {WATCH_DIR}')
        return

    print(f'Processing {len(md_files)} file(s) from {WATCH_DIR}...')

    for filepath in md_files:
        print(f'\nProcessing: {filepath.name}')
        success = process_file(filepath)
        if success:
            dest = ARCHIVE_DIR / filepath.name
            filepath.rename(dest)
            print(f'  Archived to {dest}')


if __name__ == '__main__':
    main()
