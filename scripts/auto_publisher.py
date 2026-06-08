#!/usr/bin/env python3
"""
auto_publisher.py

Watches a folder for new Markdown files and publishes them to WordPress as drafts.
Run via cron every 15 minutes:
  */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py
"""

import os
import re
import time
import json
import logging
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv  # pip install python-dotenv

# Load .env file (NEVER hardcode credentials)
load_dotenv()

# --- CONFIGURATION (edit these or set in .env) ---
WATCH_DIR   = Path.home() / 'Dropbox' / 'wordpress_queue'
ARCHIVE_DIR = WATCH_DIR / 'archive'
ERROR_DIR   = WATCH_DIR / 'errors'

WP_URL  = os.getenv('WP_API_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY  = os.getenv('WP_API_KEY', '')

DEFAULT_STATUS = os.getenv('DEFAULT_POST_STATUS', 'draft')  # 'draft' or 'publish'

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(WATCH_DIR / 'publisher.log'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)


def process_file(filepath: Path) -> bool:
    """Read a Markdown file and publish it to WordPress."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        log.error(f'Could not read {filepath.name}: {e}')
        return False

    lines = content.split('\n')

    # Extract title (first # heading)
    title = ''
    body_lines = []
    for line in lines:
        if not title and line.startswith('#'):
            title = line.lstrip('#').strip()
        else:
            body_lines.append(line)

    if not title:
        title = filepath.stem.replace('-', ' ').replace('_', ' ').title()
        body_lines = lines

    body = '\n'.join(body_lines).strip()

    # Convert Markdown to basic HTML
    body = convert_markdown_to_html(body)

    # Auto-detect category and tags
    category = guess_category(title, body)
    tags     = suggest_tags(title + ' ' + body)
    meta     = extract_meta_description(body)

    payload = {
        'title':            title,
        'content':          body,
        'status':           DEFAULT_STATUS,
        'category':         category,
        'tags':             tags,
        'meta_description': meta,
        'seo_title':        title[:60]
    }

    log.info(f'Publishing: "{title}" [{category}] tags={tags}')

    try:
        r = requests.post(
            WP_URL,
            headers={
                'X-Sourov-Key': WP_KEY,
                'Content-Type': 'application/json'
            },
            json=payload,
            timeout=30
        )

        if r.status_code in (200, 201):
            data = r.json()
            post_id = data.get('post_id', data.get('id', '?'))
            log.info(f'SUCCESS: Published "{title}" -> Post ID: {post_id}')
            return True
        else:
            log.error(f'WordPress error {r.status_code}: {r.text[:200]}')
            return False

    except requests.RequestException as e:
        log.error(f'Network error: {e}')
        return False


def convert_markdown_to_html(text: str) -> str:
    """Basic Markdown to HTML conversion."""
    lines = text.split('\n')
    html  = []
    in_ul = False

    for line in lines:
        # Headings
        if line.startswith('## '):
            if in_ul: html.append('</ul>'); in_ul = False
            html.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            if in_ul: html.append('</ul>'); in_ul = False
            html.append(f'<h3>{line[4:].strip()}</h3>')
        # List items
        elif line.startswith('- ') or line.startswith('* '):
            if not in_ul: html.append('<ul>'); in_ul = True
            html.append(f'<li>{line[2:].strip()}</li>')
        # Blank line
        elif not line.strip():
            if in_ul: html.append('</ul>'); in_ul = False
        # Paragraph
        else:
            if in_ul: html.append('</ul>'); in_ul = False
            # Bold
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            # Italic
            line = re.sub(r'\*(.+?)\*', r'<em>\1</em>', line)
            html.append(f'<p>{line.strip()}</p>')

    if in_ul:
        html.append('</ul>')

    return '\n'.join(html)


def extract_meta_description(html: str) -> str:
    """Extract first 155 chars from content as meta description."""
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:152] + '...' if len(text) > 155 else text


def guess_category(title: str, content: str) -> str:
    """Auto-assign WordPress category based on keywords."""
    text = (title + ' ' + content).lower()
    if any(w in text for w in ['grammar', 'tense', 'verb', 'conjugat']):
        return 'Grammar'
    if any(w in text for w in ['listen', 'pronunciation', 'phonics', 'phonology']):
        return 'Listening & Phonology'
    if any(w in text for w in ['celta', 'lesson plan', 'classroom', 'teaching']):
        return 'CELTA'
    if any(w in text for w in ['speak', 'fluency', 'conversation', 'oral']):
        return 'Speaking'
    if any(w in text for w in ['reading', 'comprehension', 'skim', 'scan']):
        return 'Reading'
    if any(w in text for w in ['writing', 'essay', 'paragraph', 'draft']):
        return 'Writing'
    if any(w in text for w in ['vocabular', 'idiom', 'phrase', 'collocation']):
        return 'Vocabulary'
    return 'ELT Masterclass'


def suggest_tags(text: str) -> str:
    """Generate comma-separated tags from text."""
    keyword_map = {
        'grammar':        'grammar',
        'listening':      'listening',
        'pronunciation':  'pronunciation',
        'speaking':       'speaking',
        'celta':          'CELTA',
        'elt':            'ELT',
        'phonics':        'phonics',
        'fluency':        'fluency',
        'vocabulary':     'vocabulary',
        'idiom':          'idioms',
        'writing':        'writing',
        'comprehension':  'comprehension',
        'classroom':      'classroom',
    }

    words  = re.findall(r'\b\w+\b', text.lower())
    found  = []
    for keyword, tag in keyword_map.items():
        if any(keyword in w for w in words) and tag not in found:
            found.append(tag)
        if len(found) >= 5:
            break

    return ','.join(found) if found else 'ELT'


def main():
    # Create directories if they don't exist
    for d in (WATCH_DIR, ARCHIVE_DIR, ERROR_DIR):
        d.mkdir(parents=True, exist_ok=True)

    if not WP_KEY:
        log.error('WP_API_KEY not set. Create a .env file with WP_API_KEY=your-key')
        return

    md_files = list(WATCH_DIR.glob('*.md'))

    if not md_files:
        log.info('No new files to process.')
        return

    log.info(f'Found {len(md_files)} file(s) to process.')

    for filepath in md_files:
        success = process_file(filepath)
        if success:
            # Move to archive
            dest = ARCHIVE_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filepath.name}"
            filepath.rename(dest)
            log.info(f'Archived: {filepath.name}')
        else:
            # Move to errors
            dest = ERROR_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filepath.name}"
            filepath.rename(dest)
            log.warning(f'Moved to errors: {filepath.name}')

        time.sleep(1.5)  # Respect rate limits

    log.info('Done.')


if __name__ == '__main__':
    main()
