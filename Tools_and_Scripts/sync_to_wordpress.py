#!/usr/bin/env python3
"""
Sync WordPress Blog Queue CSV to your WordPress site via deploy.php
Publishes all approved posts not yet published

Usage:
  python sync_to_wordpress.py --dry-run (preview what will publish)
  python sync_to_wordpress.py --live (actually publish to WordPress)

Requires:
  WORDPRESS_DEPLOY_KEY environment variable (store in .env.local)
  CSV file: wordpress_blog_queue.csv
"""

import csv
import requests
import json
import os
from datetime import datetime
import time

# Configuration
DEPLOY_URL = "https://www.sourovdeb.com/deploy.php"
CSV_FILE = "wordpress_blog_queue.csv"

def load_posts_from_csv(filename):
    """Load posts from WordPress Publishing Queue CSV"""
    posts = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            posts = list(reader)
    except FileNotFoundError:
        print(f"ERROR: {filename} not found")
        return []
    return posts

def publish_post_via_deploy(title, content, category, tags, secret_key):
    """
    Publish post to WordPress via deploy.php
    Returns: (success, post_id, error_message)
    """
    payload = {
        "action": "publish_post",
        "key": secret_key,
        "title": title,
        "content": content,
        "category": category,
        "tags": tags.split(",") if tags else [],
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
                return False, None, result.get("error", "Unknown error from server")
        else:
            return False, None, f"HTTP {response.status_code}"

    except Exception as e:
        return False, None, f"Connection error: {str(e)}"

def sync_posts(dry_run=True):
    """
    Sync posts: publish approved posts that aren't yet published
    """
    # Get secret key from environment
    secret_key = os.environ.get('WORDPRESS_DEPLOY_KEY')
    if not secret_key:
        print("ERROR: Set WORDPRESS_DEPLOY_KEY environment variable")
        print("Store in .env.local or set in your shell")
        return False

    # Load CSV
    posts = load_posts_from_csv(CSV_FILE)
    if not posts:
        print("No posts found in CSV")
        return False

    # Filter: approved and not yet published
    ready_posts = [
        p for p in posts
        if p.get('Approved', '').upper() == 'TRUE'
        and p.get('Status', '').lower() == 'ready'
        and not p.get('Post ID', '').strip()
    ]

    if not ready_posts:
        print("No posts ready to publish")
        return True

    print(f"\nFound {len(ready_posts)} posts ready to publish")
    print("-" * 70)

    if dry_run:
        print("\n[DRY RUN MODE] - Will preview, not publish\n")

    published_count = 0
    failed_count = 0

    for i, post in enumerate(ready_posts, 1):
        title = post.get('Title', 'Untitled')
        content = post.get('Content', '')
        category = post.get('Catagory', 'Uncategorized')  # Note: keeping misspelling from original
        tags = post.get('Tags', '')

        print(f"\n[{i}/{len(ready_posts)}] {title}")
        print(f"  Category: {category}")
        print(f"  Tags: {tags[:50]}...")

        if dry_run:
            print(f"  [DRY RUN] Would publish to WordPress")
        else:
            print(f"  Publishing...", end=" ", flush=True)

            success, post_id, error = publish_post_via_deploy(
                title, content, category, tags, secret_key
            )

            if success:
                print(f"✓ (ID: {post_id})")
                # Update CSV with post ID
                post['Post ID'] = str(post_id)
                post['Status'] = 'Published'
                published_count += 1
            else:
                print(f"✗ FAILED: {error}")
                failed_count += 1

            # Rate limiting - don't hammer the server
            time.sleep(2)

    print("\n" + "-" * 70)
    print(f"Results: {published_count} published, {failed_count} failed")

    # Save updated CSV (only if not dry run and something published)
    if not dry_run and published_count > 0:
        save_csv(posts)
        print(f"✓ Updated {CSV_FILE} with post IDs")

    return failed_count == 0

def save_csv(posts):
    """Save updated posts back to CSV"""
    if not posts:
        return

    fieldnames = list(posts[0].keys())

    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(posts)

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Sync WordPress Blog Queue to sourovdeb.com"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would publish (default mode)"
    )
    parser.add_argument(
        "--live",
        action="store_true",
        help="Actually publish to WordPress (use with caution)"
    )

    args = parser.parse_args()

    # Default to dry-run unless --live specified
    dry_run = not args.live

    if dry_run:
        print("\n🔍 DRY RUN MODE - No posts will actually be published")
        print("Run with --live flag to publish for real\n")

    success = sync_posts(dry_run=dry_run)

    if success:
        print("\n✓ Sync completed successfully")
        return 0
    else:
        print("\n✗ Sync had errors")
        return 1

if __name__ == "__main__":
    exit(main())
