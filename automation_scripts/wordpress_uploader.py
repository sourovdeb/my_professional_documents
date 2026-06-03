#!/usr/bin/env python3
"""
WordPress Uploader via deploy.php Gateway
Automatically convert markdown essays to WordPress posts

IMPORTANT: Credentials are stored in .env file (NOT in code)

Setup:
    1. Create .env file in this directory:
       DEPLOY_URL=https://www.sourovdeb.com/deploy.php
       DEPLOY_KEY=0767044896thevenet_

    2. Install: pip install python-dotenv requests

    3. Usage:
       python3 wordpress_uploader.py --file essay.md --status draft
       python3 wordpress_uploader.py --file essay.md --status publish --category "Mental Health"
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import requests
from dotenv import load_dotenv
import argparse
import sys

# Load environment variables from .env
load_dotenv()

class WordPressUploader:
    def __init__(self):
        self.deploy_url = os.getenv('DEPLOY_URL', 'https://www.sourovdeb.com/deploy.php')
        self.deploy_key = os.getenv('DEPLOY_KEY', '')

        if not self.deploy_key:
            print("❌ ERROR: DEPLOY_KEY not found in .env")
            print("   Create .env file with: DEPLOY_KEY=your_secret_key")
            sys.exit(1)

    def parse_essay(self, filepath):
        """Parse markdown essay into WordPress post data"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract frontmatter
        frontmatter = {}
        metadata = {
            'title': '',
            'content': '',
            'category': 'Uncategorized',
            'tags': '',
            'status': 'draft',
            'excerpt': ''
        }

        # Parse YAML-style frontmatter
        if content.startswith('#'):
            lines = content.split('\n')

            # Extract title from first H1
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    metadata['title'] = line.replace('# ', '').strip()
                    content = '\n'.join(lines[i+1:])
                    break

        # Extract metadata from markdown comments
        patterns = {
            'Status': r'\*\*Status:\*\*\s*(\w+)',
            'Category': r'\*\*Category:\*\*\s*\[([^\]]+)\]',
            'Tags': r'\*\*Tags:\*\*\s*\[([^\]]+)\]',
            'Excerpt': r'\*\*Excerpt:\*\*\s*(.+?)(?:\n\n|$)'
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                if key == 'Category':
                    metadata['category'] = match.group(1)
                elif key == 'Tags':
                    metadata['tags'] = match.group(1)
                elif key == 'Status':
                    metadata['status'] = match.group(1)
                elif key == 'Excerpt':
                    metadata['excerpt'] = match.group(1).strip()

        # Convert markdown to WordPress HTML
        metadata['content'] = self._markdown_to_html(content)

        # Generate excerpt if not provided
        if not metadata['excerpt']:
            text = re.sub(r'[#*_`]', '', content)
            metadata['excerpt'] = text[:160].strip() + '...'

        return metadata

    def _markdown_to_html(self, markdown):
        """Simple markdown to HTML converter for WordPress"""
        html = markdown

        # Headers
        html = re.sub(r'## (.*)', r'<h2>\1</h2>', html)
        html = re.sub(r'### (.*)', r'<h3>\1</h3>', html)

        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)

        # Links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

        # Lists
        lines = html.split('\n')
        in_list = False
        new_lines = []

        for line in lines:
            if re.match(r'^\s*[-*]\s', line):
                if not in_list:
                    new_lines.append('<ul>')
                    in_list = True
                item = re.sub(r'^\s*[-*]\s', '', line)
                new_lines.append(f'  <li>{item}</li>')
            else:
                if in_list:
                    new_lines.append('</ul>')
                    in_list = False
                new_lines.append(line)

        if in_list:
            new_lines.append('</ul>')

        html = '\n'.join(new_lines)

        # Paragraphs
        html = re.sub(r'\n\n+', '</p><p>', html)
        html = f'<p>{html}</p>'

        return html

    def upload_to_wordpress(self, metadata, dry_run=False):
        """Upload post to WordPress via deploy.php gateway"""
        if dry_run:
            print("🧪 DRY RUN (not actually uploading)")

        print(f"📝 Post Details:")
        print(f"   Title: {metadata['title']}")
        print(f"   Category: {metadata['category']}")
        print(f"   Tags: {metadata['tags']}")
        print(f"   Status: {metadata['status']}")
        print(f"   Content length: {len(metadata['content'])} chars")

        if dry_run:
            return True

        # Prepare payload for deploy.php
        payload = {
            'action': 'create_post',
            'key': self.deploy_key,
            'post_data': {
                'post_title': metadata['title'],
                'post_content': metadata['content'],
                'post_excerpt': metadata['excerpt'],
                'post_status': metadata['status'],
                'post_category': metadata['category'],
                'post_tag': metadata['tags'],
                'post_date': datetime.now().isoformat()
            }
        }

        try:
            print(f"\n🌐 Uploading to: {self.deploy_url}")
            response = requests.post(
                self.deploy_url,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    post_id = result.get('post_id')
                    print(f"✅ Upload successful!")
                    print(f"   Post ID: {post_id}")
                    print(f"   View: https://www.sourovdeb.com/?p={post_id}")
                    return True
                else:
                    print(f"❌ Upload failed: {result.get('message')}")
                    return False
            else:
                print(f"❌ Server error: {response.status_code}")
                print(response.text[:200])
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def save_draft_locally(self, metadata, format='json'):
        """Save post draft locally before uploading"""
        draft_dir = Path('wordpress_ready/staging')
        draft_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{metadata['title'][:30].replace(' ', '_')}"

        if format == 'json':
            filepath = draft_dir / f"{filename}.json"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
        else:
            filepath = draft_dir / f"{filename}.md"
            md = f"""# {metadata['title']}

**Status:** {metadata['status']}
**Category:** {metadata['category']}
**Tags:** {metadata['tags']}
**Excerpt:** {metadata['excerpt']}

---

{metadata['content']}
"""
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(md)

        print(f"💾 Draft saved: {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(
        description='Convert markdown essays to WordPress posts'
    )
    parser.add_argument('--file', required=True, help='Markdown essay file')
    parser.add_argument('--status', choices=['draft', 'publish'], default='draft',
                       help='Post status (default: draft)')
    parser.add_argument('--category', default='Uncategorized', help='WordPress category')
    parser.add_argument('--tags', default='', help='Comma-separated tags')
    parser.add_argument('--dry-run', action='store_true', help='Preview without uploading')
    parser.add_argument('--save-only', action='store_true', help='Save as draft without uploading')

    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    uploader = WordPressUploader()

    # Parse essay
    print(f"📖 Parsing: {args.file}")
    metadata = uploader.parse_essay(args.file)

    # Override with CLI args
    if args.category != 'Uncategorized':
        metadata['category'] = args.category
    if args.tags:
        metadata['tags'] = args.tags
    metadata['status'] = args.status

    # Save draft
    uploader.save_draft_locally(metadata, format='json')

    # Upload
    if not args.save_only:
        print()
        if uploader.upload_to_wordpress(metadata, dry_run=args.dry_run):
            print("\n✅ Done! Check WordPress admin to confirm.")
        else:
            print("\n⚠️  Upload failed. Draft saved locally for manual upload.")


if __name__ == '__main__':
    main()
