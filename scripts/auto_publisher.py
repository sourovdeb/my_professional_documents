#!/usr/bin/env python3
"""
auto_publisher.py — watches a folder for .md files and posts them to WordPress

Usage:
  export WP_KEY='your-key'
  python auto_publisher.py [--folder ~/Dropbox/wordpress_queue] [--status draft]

Set up as a cron job to run every 15 minutes:
  */15 * * * * /usr/bin/python3 /path/to/auto_publisher.py
"""
import os, sys, time, re, logging, argparse, requests
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(Path.home() / 'auto_publisher.log'),
    ]
)
log = logging.getLogger(__name__)

DEFAULT_FOLDER  = Path.home() / 'Dropbox' / 'wordpress_queue'
ARCHIVE_DIR     = DEFAULT_FOLDER / 'archive'
WP_URL          = os.environ.get('WP_URL', 'https://sourovdeb.com/wp-json/sourov/v1/ai-post')
WP_KEY          = os.environ.get('WP_KEY', '')

CATEGORY_MAP = [
    (['grammar', 'tense', 'verb', 'modal'],           'Grammar'),
    (['listen', 'pronunciation', 'phoneme', 'sound'],  'Listening & Phonology'),
    (['celta', 'teaching practice', 'lesson plan'],    'CELTA'),
    (['vocabulary', 'idiom', 'collocation', 'word'],   'Vocabulary'),
    (['writing', 'essay', 'paragraph', 'composition'], 'Writing Skills'),
    (['speaking', 'fluency', 'conversation', 'oral'],  'Speaking'),
]

def guess_category(text: str) -> str:
    text = text.lower()
    for keywords, category in CATEGORY_MAP:
        if any(kw in text for kw in keywords):
            return category
    return 'ELT Masterclass'

def suggest_tags(text: str) -> list:
    TAG_MAP = {
        'grammar': 'grammar', 'tense': 'tenses', 'verb': 'verbs',
        'listen': 'listening', 'pronunciation': 'pronunciation', 'phoneme': 'phonology',
        'celta': 'CELTA', 'elt': 'ELT', 'efl': 'EFL', 'esl': 'ESL',
        'vocabulary': 'vocabulary', 'idiom': 'idioms',
        'writing': 'writing', 'speaking': 'speaking',
    }
    text  = text.lower()
    found = sorted({tag for kw, tag in TAG_MAP.items() if kw in text})
    return found[:5]  # max 5 tags

def parse_markdown(filepath: Path) -> dict:
    """Extract title (first # heading), frontmatter, and body from a .md file."""
    content = filepath.read_text(encoding='utf-8').strip()
    lines   = content.split('\n')

    # Extract title from first heading
    title = filepath.stem.replace('-', ' ').replace('_', ' ').title()
    body_start = 0
    for i, line in enumerate(lines):
        if line.startswith('# '):
            title     = line[2:].strip()
            body_start = i + 1
            break

    body      = '\n'.join(lines[body_start:]).strip()
    # Convert basic Markdown to HTML
    body_html = markdown_to_html(body)

    text_combined = title + ' ' + body
    return {
        'title':            title,
        'content':          body_html,
        'category':         guess_category(text_combined),
        'tags':             ', '.join(suggest_tags(text_combined)),
        'meta_description': re.sub(r'<[^>]+>', '', body_html)[:160].strip(),
    }

def markdown_to_html(text: str) -> str:
    """Minimal Markdown → HTML conversion."""
    lines  = text.split('\n')
    output = []
    in_ul  = False
    for line in lines:
        if line.startswith('## '):
            if in_ul: output.append('</ul>'); in_ul = False
            output.append(f'<h2>{line[3:].strip()}</h2>')
        elif line.startswith('### '):
            if in_ul: output.append('</ul>'); in_ul = False
            output.append(f'<h3>{line[4:].strip()}</h3>')
        elif line.startswith('- ') or line.startswith('* '):
            if not in_ul: output.append('<ul>'); in_ul = True
            output.append(f'<li>{line[2:].strip()}</li>')
        elif line.strip() == '':
            if in_ul: output.append('</ul>'); in_ul = False
        else:
            if in_ul: output.append('</ul>'); in_ul = False
            # Bold and italic
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            line = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', line)
            output.append(f'<p>{line.strip()}</p>')
    if in_ul: output.append('</ul>')
    return '\n'.join(output)

def post_to_wordpress(data: dict, status: str = 'draft', api_key: str = '') -> dict:
    payload = {**data, 'status': status}
    try:
        r = requests.post(
            WP_URL,
            headers={'X-Sourov-Key': api_key or WP_KEY, 'Content-Type': 'application/json'},
            json=payload,
            timeout=30
        )
        return r.json()
    except Exception as e:
        return {'error': str(e)}

def process_folder(watch_dir: Path, status: str = 'draft', api_key: str = '') -> int:
    archive = watch_dir / 'archive'
    archive.mkdir(parents=True, exist_ok=True)
    processed = 0
    for filepath in sorted(watch_dir.glob('*.md')):
        log.info(f'Processing: {filepath.name}')
        try:
            post_data = parse_markdown(filepath)
            result    = post_to_wordpress(post_data, status, api_key)
            post_id   = result.get('post_id') or result.get('id')
            if post_id:
                dest = archive / filepath.name
                filepath.rename(dest)
                log.info(f'Published: {post_data["title"]} → ID {post_id}')
                processed += 1
            else:
                log.error(f'Failed: {filepath.name} → {result}')
        except Exception as e:
            log.error(f'Error processing {filepath.name}: {e}')
    return processed

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto-publish Markdown files to WordPress')
    parser.add_argument('--folder', default=str(DEFAULT_FOLDER), help='Folder to watch')
    parser.add_argument('--status', default='draft', choices=['draft', 'publish', 'future'])
    parser.add_argument('--key',    default=WP_KEY, help='WordPress API key')
    parser.add_argument('--watch',  action='store_true', help='Keep running, check every 15 minutes')
    args = parser.parse_args()

    watch_dir = Path(args.folder).expanduser()
    if not watch_dir.exists():
        watch_dir.mkdir(parents=True)
        log.info(f'Created watch folder: {watch_dir}')

    if args.watch:
        log.info(f'Watching {watch_dir} every 15 minutes...')
        while True:
            n = process_folder(watch_dir, args.status, args.key)
            if n:
                log.info(f'Processed {n} file(s)')
            time.sleep(900)  # 15 minutes
    else:
        n = process_folder(watch_dir, args.status, args.key)
        log.info(f'Done. Processed {n} file(s).')
