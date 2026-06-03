#!/usr/bin/env python3
"""
WordPress Publisher - Push content from CSV to WordPress via deploy.php
Reads Google Drive WordPress Publishing Queue, publishes to sourovdeb.com
Usage: python wordpress_publisher.py --file queue.csv --key YOUR_SECRET_KEY
"""

import csv
import requests
import json
from pathlib import Path
from datetime import datetime
import time

# Configuration (store credentials in .env.local, not here)
DEPLOY_URL = "https://www.sourovdeb.com/deploy.php"

def publish_post(title, content, category, tags, meta_description, seo_title, secret_key):
    """
    Publish a post to WordPress via deploy.php gateway
    Returns: (success, post_id, error_message)
    """

    payload = {
        "action": "publish_post",
        "key": secret_key,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags.split(",") if tags else [],
        "meta_description": meta_description,
        "seo_title": seo_title,
    }

    try:
        response = requests.post(
            DEPLOY_URL,
            json=payload,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return True, result.get("post_id"), None
            else:
                return False, None, result.get("error", "Unknown error")
        else:
            return False, None, f"HTTP {response.status_code}: {response.text}"

    except Exception as e:
        return False, None, str(e)

def read_queue(csv_file):
    """Read WordPress Publishing Queue CSV"""
    posts = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Status') == 'Ready' and row.get('Approved') == 'TRUE':
                posts.append(row)
    return posts

def publish_queue(csv_file, secret_key, dry_run=True):
    """
    Publish all ready posts from queue
    dry_run=True: Show what would happen without publishing
    """
    posts = read_queue(csv_file)

    if not posts:
        print("No posts ready to publish")
        return

    print(f"Found {len(posts)} posts ready to publish")
    print("-" * 60)

    for i, post in enumerate(posts, 1):
        title = post.get('Title', 'Untitled')

        if dry_run:
            print(f"\n[DRY RUN] Post {i}: {title}")
            print(f"  Category: {post.get('Catagory', 'N/A')}")
            print(f"  Tags: {post.get('Tags', 'N/A')}")
            print(f"  Would publish: {post.get('Publish Date', 'Now')}")
        else:
            print(f"\n[PUBLISHING] Post {i}: {title}...", end=" ")
            success, post_id, error = publish_post(
                title=post.get('Title'),
                content=post.get('Content'),
                category=post.get('Catagory'),
                tags=post.get('Tags'),
                meta_description=post.get('Meta Description'),
                seo_title=post.get('SEO Titie'),  # Note: keeping misspelling from template
                secret_key=secret_key
            )

            if success:
                print(f"✓ Published (ID: {post_id})")
            else:
                print(f"✗ Failed: {error}")

            time.sleep(1)  # Rate limiting

def update_post_id(csv_file, post_index, post_id):
    """Update post ID in CSV after publishing"""
    rows = []
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if 0 <= post_index < len(rows):
        rows[post_index]['Post ID'] = post_id
        rows[post_index]['Status'] = 'Published'

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WordPress Publisher")
    parser.add_argument("--file", default="wordpress_queue.csv", help="CSV file to publish")
    parser.add_argument("--key", help="Deploy.php secret key (or set DEPLOY_KEY env var)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen")
    parser.add_argument("--live", action="store_true", help="Actually publish (default is dry-run)")

    args = parser.parse_args()

    secret_key = args.key or os.environ.get('DEPLOY_KEY')
    if not secret_key:
        print("ERROR: No secret key provided. Use --key or set DEPLOY_KEY env var")
        exit(1)

    publish_queue(args.file, secret_key, dry_run=not args.live)
