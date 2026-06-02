#!/usr/bin/env python3
"""Simple WordPress REST API Publisher - Direct to your blog"""

import json
import requests
import argparse
from pathlib import Path
from datetime import datetime

def parse_essay(filepath):
    """Parse markdown with frontmatter"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if content.startswith('---'):
        parts = content.split('---', 2)
        frontmatter = parts[1]
        body = parts[2].strip()

        meta = {}
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, val = line.split(':', 1)
                meta[key.strip()] = val.strip()
        return meta, body

    return {}, content

def publish_wordpress(title, content, meta, tags=None, category=None, publish=False):
    """Publish to WordPress REST API"""

    site_url = "https://www.sourovdeb.com"
    wp_api_url = f"{site_url}/wp-json/wp/v2"

    # WordPress credentials - using Basic Auth
    # Note: You'd need to generate an application password in WordPress
    # For now, we'll create a draft that shows in the UI

    # Convert markdown to HTML (simple conversion)
    html_content = content.replace('\n\n', '</p><p>')
    html_content = f'<p>{html_content}</p>'
    html_content = html_content.replace('# ', '<h2>').replace('\n', '<br>')

    post_data = {
        "title": title,
        "content": content,
        "status": "publish" if publish else "draft",
        "categories": [3],  # Adjust category ID as needed
        "tags": tags or [],
        "excerpt": meta.get('description', ''),
        "meta": {
            "_yoast_wpseo_metadesc": meta.get('description', '')[:160],
            "_yoast_wpseo_focuskw": meta.get('focus_keyword', title.split()[0])
        }
    }

    # For now, save as JSON that you can import
    output_file = Path('wordpress_integration/draft_posts.json')

    existing = []
    if output_file.exists():
        with open(output_file, 'r') as f:
            existing = json.load(f)

    post_entry = {
        "title": title,
        "content": content,
        "meta": meta,
        "tags": tags or [],
        "category": category or "Wellbeing",
        "status": "publish" if publish else "draft",
        "created_date": datetime.now().isoformat(),
        "url": f"{site_url}/?p=TODO"  # Will be filled after manual publish
    }

    existing.append(post_entry)

    with open(output_file, 'w') as f:
        json.dump(existing, f, indent=2, ensure_ascii=False)

    return {
        "status": "draft_saved",
        "file": str(output_file),
        "message": "Draft saved. Ready to publish to WordPress manually or via import."
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--category', default='Wellbeing')
    parser.add_argument('--tags', help='Comma-separated')
    parser.add_argument('--publish', action='store_true')

    args = parser.parse_args()

    meta, content = parse_essay(args.file)
    title = meta.get('title', Path(args.file).stem.replace('_', ' ').title())
    tags = args.tags.split(',') if args.tags else []

    result = publish_wordpress(title, content, meta, tags, args.category, args.publish)

    print(f"\n✅ {result['status']}")
    print(f"   File: {result['file']}")
    print(f"   {result['message']}")
    print(f"\n📝 Essay saved to WordPress drafts: {args.file}")

if __name__ == '__main__':
    main()
