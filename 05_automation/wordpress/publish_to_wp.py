#!/usr/bin/env python3
"""
Push a markdown essay as a WordPress draft via the REST API.

Usage:
    python publish_to_wp.py path/to/essay.md
    python publish_to_wp.py path/to/essay.md --status publish

Reads credentials from .env in the repo root (never hardcoded).
"""

import sys
import os
import re
import json
import base64
import argparse
from pathlib import Path
from urllib import request, error as urlerror

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


def get_credentials(env: dict) -> tuple[str, str, str]:
    wp_url = env.get("WP_URL") or os.environ.get("WP_URL", "")
    wp_user = env.get("WP_USER") or os.environ.get("WP_USER", "")
    wp_pass = env.get("WP_APP_PASSWORD") or os.environ.get("WP_APP_PASSWORD", "")

    missing = [k for k, v in [("WP_URL", wp_url), ("WP_USER", wp_user), ("WP_APP_PASSWORD", wp_pass)] if not v]
    if missing:
        print(f"ERROR: Missing credentials: {', '.join(missing)}")
        print("Copy .env.example to .env and fill in WP_URL, WP_USER, WP_APP_PASSWORD")
        sys.exit(1)

    return wp_url.rstrip("/"), wp_user, wp_pass


# ── Markdown parsing ────────────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Extract YAML-style frontmatter and return (meta, body)."""
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
    """Minimal markdown → HTML. Enough for WordPress drafts."""
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
            # Inline: bold, italic
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


# ── WordPress REST API ──────────────────────────────────────────────────────

def post_draft(wp_url: str, wp_user: str, wp_pass: str, title: str, content: str,
               status: str = "draft", tags: list | None = None) -> dict:
    endpoint = f"{wp_url}/wp-json/wp/v2/posts"

    token = base64.b64encode(f"{wp_user}:{wp_pass}".encode()).decode()
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
    }

    payload = {
        "title": title,
        "content": content,
        "status": status,
    }

    data = json.dumps(payload).encode("utf-8")
    req = request.Request(endpoint, data=data, headers=headers, method="POST")

    try:
        with request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urlerror.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body[:500]}")
        sys.exit(1)
    except urlerror.URLError as e:
        print(f"Connection error: {e.reason}")
        print("Check WP_URL and that your site is reachable.")
        sys.exit(1)


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Publish a markdown essay to WordPress as a draft.")
    parser.add_argument("file", help="Path to the markdown essay file")
    parser.add_argument("--status", default="draft", choices=["draft", "publish", "private"],
                        help="WordPress post status (default: draft)")
    parser.add_argument("--dry-run", action="store_true", help="Parse and show what would be sent, no upload")
    args = parser.parse_args()

    essay_path = Path(args.file).expanduser().resolve()
    if not essay_path.exists():
        print(f"File not found: {essay_path}")
        sys.exit(1)

    # Load env from repo root
    repo_root = Path(__file__).parent.parent.parent
    env = load_env(repo_root / ".env")

    raw = essay_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)

    # Strip HTML comments (template instructions)
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

    wp_url, wp_user, wp_pass = get_credentials(env)

    print(f"\nPushing to {wp_url} ...")
    result = post_draft(wp_url, wp_user, wp_pass, title, html_content, status=args.status)

    post_id = result.get("id")
    post_link = result.get("link", "")
    edit_link = f"{wp_url}/wp-admin/post.php?post={post_id}&action=edit"

    print(f"\nDone.")
    print(f"Post ID   : {post_id}")
    print(f"Edit URL  : {edit_link}")
    if post_link:
        print(f"Public URL: {post_link}")


if __name__ == "__main__":
    main()
