#!/usr/bin/env python3
"""
auto_publisher.py

Folder-watching auto-publisher for WordPress.
Runs every 15 minutes via cron. Monitors a folder for new .md files,
auto-generates metadata (category, tags, SEO), publishes as drafts.

Setup:
  pip install requests python-dotenv
  mkdir -p ~/wordpress_queue/archive

Cron (runs every 15 minutes):
  */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py >> /tmp/wp_publisher.log 2>&1

Environment (.env file or system env vars):
  WP_URL=https://sourovdeb.com/wp-json/sourov/v1/ai-post
  WP_API_KEY=your-key
  WATCH_DIR=~/wordpress_queue   (optional, defaults to ~/wordpress_queue)
"""

import os
import sys
import re
import requests
from pathlib import Path
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # .env loading is optional

WATCH_DIR = Path(os.getenv('WATCH_DIR', os.path.expanduser('~/wordpress_queue')))
ARCHIVE_DIR = WATCH_DIR / 'archive'
WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY = os.getenv('WP_API_KEY', '')


def strip_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)


def markdown_to_html(text: str) -> str:
    """Convert basic Markdown to HTML for WordPress."""
    # Headings
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    # Bold, italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    # Wrap non-tag paragraphs
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('<h') or line.startswith('<ul') or line.startswith('<li'):
            result.append(line)
        else:
            result.append(f'<p>{line}</p>')
    return '\n'.join(result)


def suggest_tags(title: str) -> str:
    t = title.lower()
    tag_map = {
        'grammar': 'grammar', 'tense': 'grammar', 'verb': 'grammar',
        'listen': 'listening', 'pronunciat': 'pronunciation', 'phonol': 'phonology',
        'speak': 'speaking', 'fluency': 'fluency', 'conversation': 'conversation',
        'celta': 'CELTA', 'elt': 'ELT', 'efl': 'EFL', 'esl': 'ESL',
        'vocabulary': 'vocabulary', 'reading': 'reading', 'writing': 'writing',
        'teacher': 'teacher training', 'lesson': 'lesson planning'
    }
    found = [v for k, v in tag_map.items() if k in t]
    seen = set()
    unique = [x for x in found if not (x in seen or seen.add(x))]
    return ', '.join(unique) if unique else 'ELT, English teaching'


def guess_category(title: str, body: str) -> str:
    text = (title + ' ' + body).lower()
    if re.search(r'grammar|tense|verb|noun|syntax', text):
        return 'Grammar'
    if re.search(r'listen|pronunciat|phonol|phonics|intonation', text):
        return 'Listening & Phonology'
    if re.search(r'speak|fluency|conversation|oral', text):
        return 'Speaking & Fluency'
    if re.search(r'celta|teaching practice|lesson plan', text):
        return 'CELTA'
    if re.search(r'read|writing|essay|paragraph', text):
        return 'Reading & Writing'
    if re.search(r'technology|app|digital|online|software', text):
        return 'Technology in ELT'
    if re.search(r'career|job|certif|professional', text):
        return 'Career & Professional Development'
    return 'ELT Masterclass'


def process_file(filepath: Path) -> bool:
    """Process one Markdown file and publish it to WordPress."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        print(f'  Read error: {e}')
        return False

    lines = content.split('\n')
    title = lines[0].lstrip('#').strip()
    body_raw = '\n'.join(lines[1:]).strip()
    body_html = markdown_to_html(body_raw)

    tags = suggest_tags(title)
    category = guess_category(title, body_raw)
    meta = strip_html(body_html)[:155].replace('\n', ' ')

    payload = {
        'title': title,
        'content': body_html,
        'status': 'draft',
        'tags': tags,
        'category': category,
        'meta_description': meta,
        'seo_title': title
    }

    try:
        r = requests.post(
            WP_URL,
            json=payload,
            headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
            timeout=30
        )
        if r.status_code == 200:
            result = r.json()
            print(f'  Published: "{title}" → Post ID {result.get("post_id")}')
            return True
        else:
            print(f'  WP error {r.status_code}: {r.text[:200]}')
            return False
    except requests.exceptions.ConnectionError:
        print(f'  Connection error — is {WP_URL} reachable?')
        return False
    except Exception as e:
        print(f'  Request error: {e}')
        return False


def main():
    if not WP_KEY:
        print('ERROR: WP_API_KEY not set. Create a .env file or set the environment variable.')
        sys.exit(1)

    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    files = list(WATCH_DIR.glob('*.md'))
    if not files:
        print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} — No new files in {WATCH_DIR}')
        return

    print(f'{datetime.now().strftime("%Y-%m-%d %H:%M")} — Processing {len(files)} file(s)...')
    for filepath in files:
        print(f'\nProcessing: {filepath.name}')
        success = process_file(filepath)
        if success:
            dest = ARCHIVE_DIR / filepath.name
            filepath.rename(dest)
            print(f'  Archived to: {dest}')
        else:
            print(f'  Kept in queue (will retry next run)')


if __name__ == '__main__':
    main()
