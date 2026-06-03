#!/usr/bin/env python3
"""
Writer & Partner Finder — Sourov Deb
Searches Substack, Medium, and Twitter/X for writers working on:
- Mental health advocacy
- Neurodiversity (ADHD, bipolar)
- Language learning / ELT
- Diaspora / immigrant experience
- Education system critique

Free. Uses RSS and public APIs only.
Dependencies: pip install requests feedparser beautifulsoup4
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
import time

SEARCH_TERMS = [
    "bipolar disorder writer",
    "ADHD author blog",
    "neurodiversity advocacy writer",
    "language learning blog multilingual",
    "CELTA ELT education reform",
    "diaspora mental health writer",
    "generational trauma personal essay",
    "La Réunion expat writer",
    "Bangladesh immigrant writer",
    "mental health lived experience author",
]

PLATFORMS = {
    "Substack": "https://substack.com/search/{query}?type=publication",
    "Medium": "https://medium.com/search?q={query}&source=post_page",
}


def search_medium_rss(query: str) -> list[dict]:
    """Search Medium via their tag RSS feeds."""
    tags = query.replace(" ", "-").lower()
    url = f"https://medium.com/feed/tag/{tags}"
    feed = feedparser.parse(url)
    results = []
    for entry in feed.entries[:5]:
        results.append({
            "platform": "Medium",
            "title": entry.get("title", ""),
            "author": entry.get("author", ""),
            "url": entry.get("link", ""),
            "summary": entry.get("summary", "")[:200],
            "tag": tags,
            "found_via": query,
        })
    return results


def search_substack(query: str) -> list[dict]:
    """Search Substack publications (public search endpoint)."""
    url = f"https://substack.com/api/v1/search/publications?query={query}&limit=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        results = []
        for pub in data.get("publications", [])[:5]:
            results.append({
                "platform": "Substack",
                "name": pub.get("name", ""),
                "author": pub.get("author_name", ""),
                "url": pub.get("base_url", ""),
                "description": pub.get("description", "")[:200],
                "subscriber_count": pub.get("subscriber_count", 0),
                "found_via": query,
            })
        return results
    except Exception as e:
        print(f"  Substack search error: {e}")
        return []


def run():
    print(f"🔍 Partner Finder — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    all_results = {"medium": [], "substack": [], "run_at": datetime.now().isoformat()}
    for query in SEARCH_TERMS:
        print(f"  ↳ Searching: '{query}'")
        # Medium
        med = search_medium_rss(query)
        all_results["medium"].extend(med)
        # Substack
        sub = search_substack(query)
        all_results["substack"].extend(sub)
        time.sleep(1)  # Rate limit
    # Deduplicate by URL
    for platform in ["medium", "substack"]:
        seen = set()
        unique = []
        for item in all_results[platform]:
            url = item.get("url", "")
            if url and url not in seen:
                seen.add(url)
                unique.append(item)
        all_results[platform] = unique
    # Save
    outfile = "partner_search_results.json"
    with open(outfile, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✅ Found:")
    print(f"   Medium: {len(all_results['medium'])} writers")
    print(f"   Substack: {len(all_results['substack'])} publications")
    print(f"📝 Saved to {outfile}")
    # Print top 5 Substack with most subscribers
    top = sorted(all_results["substack"], key=lambda x: x.get("subscriber_count", 0), reverse=True)[:5]
    if top:
        print("\n🏆 Top Substack publications by audience:")
        for p in top:
            print(f"   {p['name']} ({p.get('subscriber_count',0)} subs) — {p['url']}")


if __name__ == "__main__":
    run()
