#!/usr/bin/env python3
"""Push selected local markdown drafts to WordPress via REST."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DRAFTS = [
    ROOT / "IMPORTANT_FOR_USER.md",
]
DISCOVERY_REPORTS_DIR = ROOT / "06_automation_assets" / "tool_discovery_reports"
DEFAULT_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"


@dataclass
class DraftPost:
    title: str
    content: str
    source: Path


def latest_report_path() -> Path | None:
    if not DISCOVERY_REPORTS_DIR.exists():
        return None
    reports = sorted(DISCOVERY_REPORTS_DIR.glob("discovery_report_*.md"))
    return reports[-1] if reports else None


def markdown_to_post(path: Path) -> DraftPost:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = path.stem.replace("_", " ").replace("-", " ").title()
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            break

    return DraftPost(title=title, content=text, source=path)


def post_to_wordpress(endpoint: str, api_key: str, draft: DraftPost) -> str:
    payload = {
        "title": draft.title,
        "content": draft.content,
        "status": "draft",
    }

    body = json.dumps(payload).encode("utf-8")
    request = Request(
        endpoint,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Sourov-Key": api_key,
        },
    )

    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="ignore")


def collect_draft_paths(extra_paths: Iterable[str]) -> List[Path]:
    paths = list(DEFAULT_DRAFTS)

    latest = latest_report_path()
    if latest is not None:
        paths.append(latest)

    for raw in extra_paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        paths.append(candidate)

    deduped: List[Path] = []
    seen = set()
    for p in paths:
        key = str(p.resolve()) if p.exists() else str(p)
        if key not in seen:
            deduped.append(p)
            seen.add(key)
    return deduped


def main() -> int:
    parser = argparse.ArgumentParser(description="Push local markdown drafts to WordPress")
    parser.add_argument("--execute", action="store_true", help="Actually publish drafts (default is dry-run)")
    parser.add_argument("--endpoint", default=os.getenv("WP_ENDPOINT", DEFAULT_ENDPOINT), help="WordPress REST endpoint")
    parser.add_argument("--api-key", default=os.getenv("WP_API_KEY", ""), help="WordPress API key (or set WP_API_KEY)")
    parser.add_argument("--draft", action="append", default=[], help="Additional markdown draft path (repeatable)")

    args = parser.parse_args()

    draft_paths = collect_draft_paths(args.draft)
    existing = [p for p in draft_paths if p.exists()]

    if not existing:
        print("No draft files found to publish.")
        return 1

    posts = [markdown_to_post(path) for path in existing]

    if not args.execute:
        print("Dry run complete. Drafts that would be pushed:")
        for post in posts:
            print(f"- {post.title} ({post.source})")
        print("Run with --execute and WP_API_KEY to push to WordPress.")
        return 0

    if not args.api_key.strip():
        print("Missing API key. Set WP_API_KEY or pass --api-key.")
        return 1

    failed = False
    for post in posts:
        try:
            response = post_to_wordpress(args.endpoint, args.api_key, post)
            print(f"Pushed draft: {post.title}")
            print(response[:400])
        except (HTTPError, URLError, TimeoutError, ValueError) as exc:
            failed = True
            print(f"Failed to push {post.title}: {exc}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
