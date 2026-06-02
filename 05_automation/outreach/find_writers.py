#!/usr/bin/env python3
"""
Find like-minded writers on Substack and Medium.
Searches by keyword/topic and outputs a contact list in markdown.

No API key needed — uses public search endpoints.

Usage:
    python find_writers.py
    python find_writers.py --topics "trauma recovery" "immigrant experience" "bipolar"
    python find_writers.py --platform substack
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib import request, parse, error as urlerror

OUTPUT_DIR = Path(__file__).parent / "results"

DEFAULT_TOPICS = [
    "trauma recovery writing",
    "immigrant experience essay",
    "bipolar disorder personal essay",
    "ADHD neurodiversity writer",
    "English teaching abroad",
    "expat France writing",
    "mental health memoir",
    "generational trauma essay",
    "language learning culture",
    "hospitality industry writing",
]

# ── Substack search ─────────────────────────────────────────────────────────

def search_substack(query: str, limit: int = 5) -> list[dict]:
    """Search Substack publications by keyword."""
    encoded = parse.quote(query)
    url = f"https://substack.com/api/v1/search/publications?query={encoded}&limit={limit}"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; research-tool)",
        "Accept": "application/json",
    }

    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            pubs = data.get("publications", [])
            results = []
            for p in pubs:
                results.append({
                    "platform": "Substack",
                    "name": p.get("name", ""),
                    "author": p.get("author_name", ""),
                    "url": f"https://{p.get('custom_domain') or p.get('subdomain', '') + '.substack.com'}",
                    "description": (p.get("description") or "")[:200],
                    "subscribers": p.get("subscriber_count", 0),
                    "topic": query,
                })
            return results
    except Exception as e:
        print(f"  Substack search failed for '{query}': {e}")
        return []


# ── Medium search ────────────────────────────────────────────────────────────

def search_medium(query: str, limit: int = 5) -> list[dict]:
    """Search Medium tags for relevant publications."""
    tag = query.lower().replace(" ", "-")
    url = f"https://medium.com/tag/{parse.quote(tag)}/top-writers"

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; research-tool)",
        "Accept": "text/html",
    }

    try:
        req = request.Request(url, headers=headers)
        with request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Extract writer names from the page (basic scrape)
        import re
        # Medium embeds user data in JSON in a script tag
        matches = re.findall(r'"name":"([^"]{5,60})".*?"username":"([^"]+)"', html)
        results = []
        seen = set()
        for name, username in matches[:limit]:
            if username in seen:
                continue
            seen.add(username)
            results.append({
                "platform": "Medium",
                "name": name,
                "author": username,
                "url": f"https://medium.com/@{username}",
                "description": f"Top writer on tag: {tag}",
                "subscribers": 0,
                "topic": query,
            })
        return results
    except Exception as e:
        print(f"  Medium search failed for '{query}': {e}")
        return []


# ── Output ───────────────────────────────────────────────────────────────────

def format_writer(w: dict) -> str:
    lines = [f"### {w['name']} ({w['platform']})"]
    if w.get("author"):
        lines.append(f"**Handle:** @{w['author']}")
    lines.append(f"**URL:** {w['url']}")
    if w.get("subscribers"):
        lines.append(f"**Subscribers:** {w['subscribers']:,}")
    if w.get("description"):
        lines.append(f"**About:** {w['description']}")
    lines.append(f"**Found via:** {w['topic']}")
    lines.append("")
    return "\n".join(lines)


def save_results(writers: list[dict]) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    fname = OUTPUT_DIR / f"writers_{date_str}.md"

    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"# Writer Contacts — {date_str}\n\n")
        f.write(f"Found {len(writers)} writers across {len({w['topic'] for w in writers})} topics.\n\n")
        f.write("**How to use this list:**\n")
        f.write("1. Read their recent work (takes 10 minutes per writer).\n")
        f.write("2. Leave a genuine comment on one piece — specific, not generic.\n")
        f.write("3. If there's a real connection, send a short DM: who you are, what you write, what you noticed.\n")
        f.write("4. Propose collaboration only after 2–3 genuine interactions.\n\n---\n\n")

        for w in writers:
            f.write(format_writer(w))
            f.write("\n")

    return fname


def main():
    parser = argparse.ArgumentParser(description="Find like-minded writers on Substack and Medium.")
    parser.add_argument("--topics", nargs="+", help="Topics to search")
    parser.add_argument("--platform", choices=["substack", "medium", "both"], default="both")
    args = parser.parse_args()

    topics = args.topics or DEFAULT_TOPICS
    all_writers = []

    print(f"Searching {len(topics)} topics on {args.platform}...")

    for topic in topics:
        print(f"  Topic: {topic}")
        if args.platform in ("substack", "both"):
            results = search_substack(topic, limit=3)
            all_writers.extend(results)
            print(f"    Substack: {len(results)} results")

        if args.platform in ("medium", "both"):
            results = search_medium(topic, limit=3)
            all_writers.extend(results)
            print(f"    Medium: {len(results)} results")

        time.sleep(1)  # polite rate limiting

    # Deduplicate by URL
    seen_urls = set()
    unique_writers = []
    for w in all_writers:
        if w["url"] not in seen_urls:
            seen_urls.add(w["url"])
            unique_writers.append(w)

    print(f"\nUnique writers found: {len(unique_writers)}")
    output_file = save_results(unique_writers)
    print(f"Results saved: {output_file}")


if __name__ == "__main__":
    main()
