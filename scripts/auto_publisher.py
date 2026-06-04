#!/usr/bin/env python3
"""
auto_publisher.py

Folder watcher that auto-publishes Markdown files to WordPress.
Run this script manually or via cron every 15 minutes.

Setup:
  pip install requests python-dotenv
  Create a .env file with WP_URL and WP_API_KEY
  Place .md files in ~/wordpress_queue/
  Run: python auto_publisher.py

Cron (every 15 min):
  */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py >> /tmp/wp_publisher.log 2>&1
"""

import os
import re
import json
import logging
from pathlib import Path
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
log = logging.getLogger(__name__)

WATCH_DIR = Path(os.getenv('WATCH_DIR', Path.home() / 'wordpress_queue'))
ARCHIVE_DIR = WATCH_DIR / 'archive'
WP_URL = os.getenv('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
API_KEY = os.getenv('WP_API_KEY', '')
DEFAULT_STATUS = os.getenv('DEFAULT_STATUS', 'draft')


CATEGORY_RULES = [
    (['grammar', 'tense', 'syntax', 'clause', 'conditional'], 'Grammar'),
    (['listening', 'comprehension', 'audio', 'podcast'], 'Listening & Phonology'),
    (['pronunciation', 'phoneme', 'intonation', 'stress', 'phonology'], 'Listening & Phonology'),
    (['speaking', 'fluency', 'dialogue', 'conversation'], 'Speaking'),
    (['reading', 'skimming', 'scanning', 'text'], 'Reading'),
    (['writing', 'essay', 'paragraph', 'draft'], 'Writing'),
    (['vocabulary', 'lexis', 'collocation', 'word'], 'Vocabulary'),
    (['celta', 'lesson plan', 'trainee', 'observation'], 'CELTA'),
    (['bipolar', 'depression', 'mental health', 'wellness'], 'Mental Health & Teaching'),
]

TAG_MAP = {
    'grammar': 'grammar',
    'listening': 'listening',
    'speaking': 'speaking',
    'reading': 'reading',
    'writing': 'writing',
    'vocabulary': 'vocabulary',
    'pronunciation': 'pronunciation',
    'phoneme': 'phonology',
    'celta': 'CELTA',
    'lesson plan': 'lesson-plan',
    'student': 'students',
    'teacher': 'teaching',
    'classroom': 'classroom',
    'fluency': 'fluency',
    'accuracy': 'accuracy',
    'bipolar': 'bipolar',
    'depression': 'mental-health',
}


def parse_markdown(filepath: Path) -> dict:
    """Parse a markdown file into post components."""
    text = filepath.read_text(encoding='utf-8')

    # Check for YAML front matter
    front_matter = {}
    if text.startswith('---'):
        end = text.find('---', 3)
        if end != -1:
            fm_block = text[3:end].strip()
            for line in fm_block.splitlines():
                if ':' in line:
                    k, _, v = line.partition(':')
                    front_matter[k.strip().lower()] = v.strip()
            text = text[end + 3:].strip()

    # Extract first H1 heading as title
    title_match = re.match(r'^#\s+(.+)', text, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        body = text[title_match.end():].strip()
    else:
        title = filepath.stem.replace('-', ' ').replace('_', ' ').title()
        body = text.strip()

    # Convert basic Markdown to HTML
    html = markdown_to_html(body)

    return {
        'title': front_matter.get('title', title),
        'content': html,
        'category': front_matter.get('category', guess_category(title, body)),
        'tags': front_matter.get('tags', ','.join(suggest_tags(title + ' ' + body))),
        'status': front_matter.get('status', DEFAULT_STATUS),
        'meta_description': front_matter.get('description', body[:160].replace('\n', ' ')),
        'seo_title': front_matter.get('seo_title', title),
        'date': front_matter.get('date', ''),
    }


def markdown_to_html(text: str) -> str:
    """Minimal Markdown-to-HTML conversion."""
    lines = text.split('\n')
    html_lines = []
    in_list = False

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            html_lines.append('')
            continue

        if stripped.startswith('## '):
            html_lines.append(f'<h2>{stripped[3:]}</h2>')
        elif stripped.startswith('### '):
            html_lines.append(f'<h3>{stripped[4:]}</h3>')
        elif stripped.startswith('- ') or stripped.startswith('* '):
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{stripped[2:]}</li>')
        elif re.match(r'^\d+\.\s', stripped):
            html_lines.append(f'<p>{stripped}</p>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            # Bold and italic
            stripped = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', stripped)
            stripped = re.sub(r'\*(.+?)\*', r'<em>\1</em>', stripped)
            html_lines.append(f'<p>{stripped}</p>')

    if in_list:
        html_lines.append('</ul>')

    return '\n'.join(html_lines)


def guess_category(title: str, body: str) -> str:
    text = (title + ' ' + body).lower()
    for keywords, category in CATEGORY_RULES:
        if any(kw in text for kw in keywords):
            return category
    return 'ELT Masterclass'


def suggest_tags(text: str) -> list:
    lower = text.lower()
    found = []
    for keyword, tag in TAG_MAP.items():
        if keyword in lower and tag not in found:
            found.append(tag)
    return found[:8]


def publish_to_wordpress(post_data: dict) -> dict | None:
    if not API_KEY:
        log.error('WP_API_KEY not set. Add it to your .env file.')
        return None
    try:
        resp = requests.post(
            WP_URL,
            json=post_data,
            headers={'X-Sourov-Key': API_KEY, 'Content-Type': 'application/json'},
            timeout=30
        )
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        log.error(f'WordPress API error: {e}')
        return None


def process_file(filepath: Path):
    log.info(f'Processing: {filepath.name}')
    try:
        post = parse_markdown(filepath)
        result = publish_to_wordpress(post)
        if result and result.get('post_id'):
            ARCHIVE_DIR.mkdir(exist_ok=True)
            dest = ARCHIVE_DIR / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{filepath.name}"
            filepath.rename(dest)
            log.info(f'SUCCESS: "{post["title"]}" → Post ID {result["post_id"]}')
        else:
            log.warning(f'FAILED: {filepath.name} — response: {result}')
    except Exception as e:
        log.error(f'Error processing {filepath.name}: {e}')


def main():
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    md_files = list(WATCH_DIR.glob('*.md'))
    if not md_files:
        log.info('No .md files found in queue.')
        return
    log.info(f'Found {len(md_files)} file(s) to process.')
    for f in md_files:
        process_file(f)


if __name__ == '__main__':
    main()
