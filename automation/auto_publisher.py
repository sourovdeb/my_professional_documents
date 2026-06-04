#!/usr/bin/env python3
"""
auto_publisher.py
Folder-watching auto-publisher for WordPress.

Usage:
  python auto_publisher.py

Setup:
  pip install requests watchdog
  Set WP_URL and WP_API_KEY below, or use environment variables.

How it works:
  - Watches ~/Dropbox/wordpress_queue/ for new .md files
  - Extracts title from first heading
  - Auto-detects category and tags from content
  - Creates WordPress draft via REST API
  - Moves processed file to archive/
"""

import os
import re
import time
import json
import shutil
import logging
from pathlib import Path
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration -----------------------------------------------------------
WP_URL   = os.environ.get('WP_URL',   'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY   = os.environ.get('WP_KEY',   'YOUR_WP_API_KEY_HERE')
WATCH_DIR = Path(os.environ.get('WATCH_DIR', Path.home() / 'Dropbox/wordpress_queue'))
ARCHIVE   = WATCH_DIR / 'archive'
LOG_FILE  = WATCH_DIR / 'publisher.log'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# --- Category and tag rules --------------------------------------------------
CATEGORY_RULES = {
    'Grammar':               ['grammar','tense','verb','noun','adjective','modal','syntax','clause'],
    'Listening & Phonology': ['listening','pronunciation','phonology','phoneme','intonation','accent'],
    'Speaking & Fluency':    ['speaking','fluency','conversation','oral','dialogue'],
    'Vocabulary':            ['vocabulary','lexis','lexical','collocation','idiom'],
    'Reading Skills':        ['reading','comprehension','skimming','scanning'],
    'Writing Skills':        ['writing','essay','paragraph','composition'],
    'CELTA':                 ['celta','teaching practice','lesson plan','trainee'],
}

TAG_KEYWORDS = {
    'grammar':'grammar', 'listening':'listening', 'speaking':'speaking',
    'pronunciation':'pronunciation', 'vocabulary':'vocabulary', 'celta':'CELTA',
    ' elt ':'ELT', ' esl ':'ESL', 'fluency':'fluency', 'lesson':'lesson plan',
    'teacher':'teaching', 'reading':'reading', 'writing':'writing',
    'ielts':'IELTS', 'cambridge':'Cambridge', 'classroom':'classroom',
}

# --- Helper functions --------------------------------------------------------
def detect_category(title, content):
    text = (title + ' ' + content).lower()
    scores = {}
    for cat, keywords in CATEGORY_RULES.items():
        score = sum(text.count(kw) for kw in keywords)
        if score:
            scores[cat] = score
    if scores:
        return max(scores, key=scores.get)
    return 'ELT Masterclass'


def detect_tags(title, content):
    text = (title + ' ' + content).lower()
    return ', '.join({tag for kw, tag in TAG_KEYWORDS.items() if kw in text}) or 'ELT'


def strip_html(html):
    return re.sub(r'<[^>]+>', ' ', html).strip()


def parse_frontmatter(content):
    """Parse optional YAML frontmatter block (--- ... ---)."""
    meta = {}
    body = content
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            for line in content[3:end].split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    meta[k.strip().lower()] = v.strip()
            body = content[end + 3:].strip()
    return meta, body


def process_file(filepath):
    filepath = Path(filepath)
    if not filepath.suffix == '.md':
        return

    log.info(f'Processing: {filepath.name}')
    raw = filepath.read_text(encoding='utf-8')

    meta, body = parse_frontmatter(raw)

    # Extract title: frontmatter > first # heading > filename
    if 'title' in meta:
        title = meta['title']
    else:
        m = re.search(r'^#+\s+(.+)', body, re.MULTILINE)
        title = m.group(1).strip() if m else filepath.stem
        body = re.sub(r'^#+\s+.+\n?', '', body, count=1, flags=re.MULTILINE).strip()

    category = meta.get('category') or detect_category(title, body)
    tags      = meta.get('tags')     or detect_tags(title, body)
    status    = meta.get('status', 'draft')
    seo_title = meta.get('seo_title', title)
    meta_desc = meta.get('meta_description', strip_html(body)[:155])

    payload = {
        'title':            seo_title,
        'content':          body,
        'category':         category,
        'tags':             tags,
        'status':           status if status in ('draft','publish','future') else 'draft',
        'seo_title':        seo_title,
        'meta_description': meta_desc,
    }
    if status == 'future' and 'date' in meta:
        payload['date'] = meta['date']

    try:
        r = requests.post(
            WP_URL,
            json=payload,
            headers={'X-Sourov-Key': WP_KEY, 'Content-Type': 'application/json'},
            timeout=30
        )
        result = r.json()
    except Exception as e:
        log.error(f'Network error: {e}')
        return

    if r.status_code == 200 and result.get('post_id'):
        log.info(f'Published \'{title}\' → Post ID {result["post_id"]}')
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        shutil.move(str(filepath), str(ARCHIVE / filepath.name))
    else:
        log.error(f'Failed: HTTP {r.status_code} — {result}')


# --- File watcher ------------------------------------------------------------
class MarkdownHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith('.md'):
            time.sleep(0.5)  # Let the file finish writing
            process_file(event.src_path)


def main():
    WATCH_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)

    # Process any existing files first
    for md in WATCH_DIR.glob('*.md'):
        process_file(md)

    log.info(f'Watching {WATCH_DIR} for new .md files...')
    observer = Observer()
    observer.schedule(MarkdownHandler(), str(WATCH_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
