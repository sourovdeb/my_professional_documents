#!/usr/bin/env python3
"""
Push a markdown essay as a WordPress draft via deploy.php gateway.

Usage:
    python publish_to_wp.py path/to/essay.md
    python publish_to_wp.py path/to/essay.md --status publish
    python publish_to_wp.py path/to/essay.md --dry-run

Reads credentials from .env in the repo root (never hardcoded).
Required in .env:
    DEPLOY_URL=https://www.sourovdeb.com/deploy.php
    DEPLOY_KEY=your_secret_key
"""

import sys
import os
import re
import json
import argparse
import hashlib
import time
from pathlib import Path
from urllib import request, parse, error as urlerror

# ── Credential loading ──────────────────────────────────────────────────────

def load_env(env_path: Path) -> dict:
    env = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        env[key.strip()] = val.strip().strip('"').strip("'")
    return env


def get_credentials(env: dict) -> tuple[str, str]:
    deploy_url = env.get("DEPLOY_URL") or os.environ.get("DEPLOY_URL", "")
    deploy_key = env.get("DEPLOY_KEY") or os.environ.get("DEPLOY_KEY", "")

    missing = [k for k, v in [("DEPLOY_URL", deploy_url), ("DEPLOY_KEY", deploy_key)] if not v]
    if missing:
        print(f"ERROR: Missing credentials: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in DEPLOY_URL and DEPLOY_KEY")
        sys.exit(1)

    return deploy_url, deploy_key


# ── Markdown parsing ────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    meta = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    front = text[3:end].strip()
    body = text[end + 4:].strip()
    for line in front.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


def markdown_to_html(md: str) -> str:
    lines = md.splitlines()
    html_lines = []
    in_para = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            if in_para:
                html_lines.append("</p>")
                in_para = False
            html_lines.append(f"<h1>{stripped[2:]}</h1>")
        elif stripped.startswith("## "):
            if in_para:
                html_lines.append("</p>")
                in_para = False
            html_lines.append(f"<h2>{stripped[3:]}</h2>")
        elif stripped.startswith("### "):
            if in_para:
                html_lines.append("</p>")
                in_para = False
            html_lines.append(f"<h3>{stripped[4:]}</h3>")
        elif stripped.startswith("---"):
            if in_para:
                html_lines.append("</p>")
                in_para = False
            html_lines.append("<hr>")
        elif stripped == "":
            if in_para:
                html_lines.append("</p>")
                in_para = False
        else:
            formatted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", stripped)
            formatted = re.sub(r"\*(.+?)\*", r"<em>\1</em>", formatted)
            formatted = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', formatted)
            if not in_para:
                html_lines.append("<p>")
                in_para = True
            html_lines.append(formatted)

    if in_para:
        html_lines.append("</p>")

    return "\n".join(html_lines)


# ── deploy.php gateway ──────────────────────────────────────────────────────

def deploy_request(deploy_url: str, deploy_key: str, params: dict) -> dict:
    params["key"] = deploy_key
    data = parse.urlencode(params).encode("utf-8")
    req = request.Request(deploy_url, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                return {"raw": raw}
    except urlerror.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body[:300]}")
        sys.exit(1)
    except urlerror.URLError as e:
        print(f"Connection error: {e.reason}")
        sys.exit(1)


def create_post_via_deploy(deploy_url: str, deploy_key: str,
                           title: str, content: str, status: str) -> dict:
    """
    Writes a tiny PHP runner to wp-content/uploads/, calls it once to create
    the post, then deletes it. Requires no Application Password.
    """
    # Unique filename so concurrent runs don't collide
    uid = hashlib.md5(f"{title}{time.time()}".encode()).hexdigest()[:8]
    remote_path = f"/home/u839078121/domains/sourovdeb.com/public_html/wp-content/uploads/wp-post-{uid}.php"
    call_url = f"https://www.sourovdeb.com/wp-content/uploads/wp-post-{uid}.php"

    # Escape values for safe PHP string embedding
    safe_title = title.replace("\\", "\\\\").replace("'", "\\'")
    safe_content = content.replace("\\", "\\\\").replace("'", "\\'")

    php = f"""<?php
define('ABSPATH', dirname(__FILE__) . '/../../../../');
require_once(dirname(__FILE__) . '/../../../../wp-load.php');
$id = wp_insert_post([
    'post_title'   => '{safe_title}',
    'post_content' => '{safe_content}',
    'post_status'  => '{status}',
    'post_type'    => 'post',
]);
echo json_encode(['post_id' => $id, 'edit_url' => admin_url('post.php?post=' . $id . '&action=edit')]);
"""

    print("Uploading post-creator script...")
    upload_result = deploy_request(deploy_url, deploy_key, {
        "action": "upload",
        "path": remote_path,
        "content": php,
    })
    if upload_result.get("error"):
        print(f"Upload failed: {upload_result}")
        sys.exit(1)

    print("Creating post...")
    try:
        with request.urlopen(call_url, timeout=20) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            result = json.loads(raw)
    except Exception as e:
        result = {"error": str(e)}
    finally:
        # Always clean up the temp file
        deploy_request(deploy_url, deploy_key, {
            "action": "delete",
            "path": remote_path,
        })

    return result


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Publish a markdown essay to WordPress via deploy.php.")
    parser.add_argument("file", help="Path to the markdown essay file")
    parser.add_argument("--status", default="draft", choices=["draft", "publish", "private"],
                        help="WordPress post status (default: draft)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be sent, no upload")
    args = parser.parse_args()

    essay_path = Path(args.file).expanduser().resolve()
    if not essay_path.exists():
        print(f"File not found: {essay_path}")
        sys.exit(1)

    repo_root = Path(__file__).parent.parent.parent
    env = load_env(repo_root / ".env")

    raw = essay_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()

    title = meta.get("title", essay_path.stem.replace("-", " ").replace("_", " ").title())
    html_content = markdown_to_html(body)
    word_count = len(body.split())

    print(f"Essay : {title}")
    print(f"Words : {word_count}")
    print(f"Status: {args.status}")
    print(f"Pillar: {meta.get('pillar', 'not set')}")

    if args.dry_run:
        print("\n--- HTML preview (first 500 chars) ---")
        print(html_content[:500])
        return

    deploy_url, deploy_key = get_credentials(env)

    print(f"\nPushing to WordPress via deploy.php ...")
    result = create_post_via_deploy(deploy_url, deploy_key, title, html_content, args.status)

    if result.get("error"):
        print(f"Error creating post: {result['error']}")
        sys.exit(1)

    post_id = result.get("post_id")
    edit_url = result.get("edit_url", f"https://www.sourovdeb.com/wp-admin/post.php?post={post_id}&action=edit")

    print(f"\nDone.")
    print(f"Post ID  : {post_id}")
    print(f"Edit URL : {edit_url}")


if __name__ == "__main__":
    main()
