#!/usr/bin/env python3
"""
WordPress Draft Publisher — Sourov Deb
Reads .md blog post files and pushes them as drafts to WordPress
via the deploy.php gateway on sourovdeb.com.

Dependencies: pip install requests markdown python-frontmatter
"""

import os
import re
import json
import requests
import frontmatter
import markdown as md_lib
from pathlib import Path
from datetime import datetime

# ── CONFIG ────────────────────────────────────────────────────────────────────
DEPLOY_URL = "https://www.sourovdeb.com/deploy.php"
DEPLOY_KEY = os.getenv("DEPLOY_KEY", "0767044896thevenet_")
WP_API_BASE = "https://www.sourovdeb.com/wp-json/wp/v2"
BLOG_DRAFTS_DIR = Path(__file__).parent.parent / "blog_drafts"


def get_wp_application_password() -> tuple[str, str]:
    """Returns (username, app_password). Set env vars."""
    return (
        os.getenv("WP_USER", "sourov"),
        os.getenv("WP_APP_PASSWORD", ""),
    )


def strip_frontmatter_content(text: str) -> str:
    """Remove YAML frontmatter block from markdown body."""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text


def convert_md_to_html(md_text: str) -> str:
    """Convert markdown to WordPress-ready HTML."""
    clean = strip_frontmatter_content(md_text)
    # Remove the H1 (title) — WordPress sets it separately
    clean = re.sub(r"^#\s+.+\n", "", clean, count=1).strip()
    html = md_lib.markdown(clean, extensions=["extra", "nl2br"])
    return html


def publish_draft_via_api(post_data: dict) -> dict:
    """Push a draft post to WordPress via REST API."""
    user, app_pass = get_wp_application_password()
    if not app_pass:
        print("⚠  WP_APP_PASSWORD not set. Run: export WP_APP_PASSWORD='xxxx'")
        print("   To create one: WP Admin → Users → Profile → Application Passwords")
        return {"error": "no_app_password"}
    resp = requests.post(
        f"{WP_API_BASE}/posts",
        auth=(user, app_pass),
        json=post_data,
        timeout=30,
    )
    return resp.json()


def process_draft_file(filepath: Path) -> dict | None:
    """Parse a blog draft .md file and return post data."""
    post = frontmatter.load(filepath)
    if not post.content.strip():
        return None
    html_content = convert_md_to_html(post.content)
    title = post.get("title", filepath.stem)
    tags_raw = post.get("tags", "")
    tags = [t.strip() for t in str(tags_raw).split(",") if t.strip()]
    return {
        "title": title,
        "content": html_content,
        "status": "draft",
        "meta": {
            "_yoast_wpseo_title": post.get("seo_title", title),
            "_yoast_wpseo_metadesc": post.get("meta_description", ""),
        },
        "tags_input": tags,
        "categories_input": [post.get("category", "Uncategorized")],
        "_source_file": str(filepath),
    }


def run(dry_run: bool = False):
    """Process all draft .md files and push to WordPress."""
    drafts = sorted(BLOG_DRAFTS_DIR.glob("*.md"))
    print(f"📂 Found {len(drafts)} draft file(s) in {BLOG_DRAFTS_DIR}")
    results = []
    for filepath in drafts:
        print(f"\n  ▶ Processing: {filepath.name}")
        post_data = process_draft_file(filepath)
        if not post_data:
            print("    ↳ Skipped (empty content)")
            continue
        if dry_run:
            print(f"    ↳ [DRY RUN] Would push: '{post_data['title']}'")
            results.append({"file": filepath.name, "status": "dry_run", "title": post_data["title"]})
            continue
        result = publish_draft_via_api(post_data)
        if "id" in result:
            print(f"    ✅ Draft created: ID {result['id']} — {result.get('link','')}")
            results.append({"file": filepath.name, "post_id": result["id"], "url": result.get("link"), "status": "created"})
        else:
            print(f"    ❌ Error: {result}")
            results.append({"file": filepath.name, "status": "error", "detail": str(result)})
    # Save results log
    log_path = BLOG_DRAFTS_DIR / "publish_log.json"
    with open(log_path, "w") as f:
        json.dump({"run_at": datetime.now().isoformat(), "results": results}, f, indent=2)
    print(f"\n📝 Log saved to {log_path}")


if __name__ == "__main__":
    import sys
    dry = "--dry-run" in sys.argv
    run(dry_run=dry)
