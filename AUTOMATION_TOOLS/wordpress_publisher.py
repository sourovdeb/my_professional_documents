#!/usr/bin/env python3
"""
Push a blog post draft to sourovdeb.com WordPress via REST API.

Setup:
  WP Admin → Users → Profile → Application Passwords → Add New
  Copy the password and set WP_APP_PASSWORD below.

Usage:
  python wordpress_publisher.py blog-drafts/my-post/post.md

The .md file needs YAML front matter:
  ---
  title: Your Post Title
  category: Mental Health & Living
  tags: bipolar, mentalhealth, writing
  meta_description: 160 chars max for SEO.
  status: draft
  ---
  Post body here...
"""

import sys
import re
import json
import base64
import urllib.request
import urllib.error

# --- Set these ---
WP_SITE = "https://www.sourovdeb.com"
WP_USER = "sourov"
WP_APP_PASSWORD = ""  # from WP Admin > Users > Profile > Application Passwords
# -----------------


def parse_frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    meta_raw, body = match.group(1), match.group(2).strip()
    meta = {}
    for line in meta_raw.split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip()
    return meta, body


def md_to_html(text):
    """Minimal markdown to HTML — paragraphs, bold, italic, headings."""
    lines = text.split("\n")
    html = []
    for line in lines:
        line = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
        line = re.sub(r"\*(.+?)\*", r"<em>\1</em>", line)
        if line.startswith("## "):
            html.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("### "):
            html.append(f"<h3>{line[4:]}</h3>")
        elif line.strip() == "":
            html.append("")
        else:
            html.append(f"<p>{line}</p>")
    return "\n".join(html)


def create_draft(meta, body):
    if not WP_APP_PASSWORD:
        print("Set WP_APP_PASSWORD first.")
        print("WP Admin → Users → Profile → Application Passwords")
        return

    creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    }

    tags = [t.strip() for t in meta.get("tags", "").split(",") if t.strip()]

    payload = {
        "title": meta.get("title", "Untitled"),
        "content": md_to_html(body),
        "status": meta.get("status", "draft"),
        "excerpt": meta.get("meta_description", ""),
        "tags": tags,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{WP_SITE}/wp-json/wp/v2/posts",
        data=data,
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            print(f"Draft created: {result.get('link', '')}")
            print(f"Edit: {WP_SITE}/wp-admin/post.php?post={result['id']}&action=edit")
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wordpress_publisher.py post.md")
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()
    meta, body = parse_frontmatter(text)
    create_draft(meta, body)
