#!/usr/bin/env python3
"""Push selected local markdown drafts to WordPress via REST."""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DRAFTS = [
    ROOT / "IMPORTANT_FOR_USER.md",
]
DISCOVERY_REPORTS_DIR = ROOT / "06_automation_assets" / "tool_discovery_reports"
DEFAULT_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
DEFAULT_CONFIG_PATH = Path(__file__).with_name("wordpress_publish_defaults.json")


@dataclass
class DraftPost:
    title: str
    content: str
    source: Path


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def normalize_terms(values: Iterable[str]) -> List[str]:
    deduped: List[str] = []
    seen = set()
    for raw in values:
        for part in raw.split(","):
            value = part.strip()
            if value and value not in seen:
                deduped.append(value)
                seen.add(value)
    return deduped


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


def next_midnight_payload(timezone_name: str) -> dict[str, str]:
    local_zone = ZoneInfo(timezone_name)
    now_local = datetime.now(local_zone)
    next_day = now_local.date() + timedelta(days=1)
    local_midnight = datetime.combine(next_day, time.min, tzinfo=local_zone)
    utc_midnight = local_midnight.astimezone(timezone.utc)
    return {
        "date": local_midnight.replace(tzinfo=None).isoformat(timespec="seconds"),
        "date_gmt": utc_midnight.replace(tzinfo=None).isoformat(timespec="seconds"),
    }


def post_to_wordpress(endpoint: str, api_key: str, payload: dict[str, Any]) -> str:
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


def build_payload(
    draft: DraftPost,
    status: str,
    tags: List[str],
    categories: List[str],
    schedule_midnight: bool,
    schedule_timezone: str,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "title": draft.title,
        "content": draft.content,
        "status": status,
    }

    if tags:
        payload["tags"] = tags
    if categories:
        payload["categories"] = categories

    if schedule_midnight:
        payload["status"] = "future"
        payload.update(next_midnight_payload(schedule_timezone))

    return payload


def collect_draft_paths(extra_paths: Iterable[str], configured_paths: Iterable[str]) -> List[Path]:
    paths = list(DEFAULT_DRAFTS)

    latest = latest_report_path()
    if latest is not None:
        paths.append(latest)

    for raw in configured_paths:
        candidate = Path(raw)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        paths.append(candidate)

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
    parser.add_argument("--config", default=os.getenv("WP_PUBLISH_CONFIG", str(DEFAULT_CONFIG_PATH)), help="Path to JSON config")
    parser.add_argument("--endpoint", default=None, help="WordPress REST endpoint")
    parser.add_argument("--api-key", default=os.getenv("WP_API_KEY", ""), help="WordPress API key (or set WP_API_KEY)")
    parser.add_argument("--status", default=None, help="Post status (draft, future, publish, etc.)")
    parser.add_argument("--tag", action="append", default=[], help="Post tag (repeatable, comma separated allowed)")
    parser.add_argument("--category", action="append", default=[], help="Post category (repeatable, comma separated allowed)")
    parser.add_argument("--schedule-midnight", action="store_true", help="Schedule post for next midnight")
    parser.add_argument("--no-schedule-midnight", action="store_true", help="Disable midnight scheduling from config")
    parser.add_argument("--schedule-timezone", default=None, help="Timezone for midnight scheduling (default UTC)")
    parser.add_argument("--draft", action="append", default=[], help="Additional markdown draft path (repeatable)")

    args = parser.parse_args()
    config = load_config(Path(args.config))

    endpoint = args.endpoint or os.getenv("WP_ENDPOINT") or str(config.get("wordpress_endpoint", DEFAULT_ENDPOINT))
    status = args.status or str(config.get("default_status", "draft"))
    configured_draft_paths = config.get("draft_paths", [])
    configured_tags = config.get("default_tags", [])
    configured_categories = config.get("default_categories", [])
    configured_schedule = bool(config.get("schedule_midnight", False))
    schedule_timezone = args.schedule_timezone or str(config.get("schedule_timezone", "UTC"))

    tags = normalize_terms(args.tag or configured_tags)
    categories = normalize_terms(args.category or configured_categories)
    schedule_midnight = args.schedule_midnight or (configured_schedule and not args.no_schedule_midnight)

    draft_paths = collect_draft_paths(args.draft, configured_draft_paths)
    existing = [p for p in draft_paths if p.exists()]

    if not existing:
        print("No draft files found to publish.")
        return 1

    posts = [markdown_to_post(path) for path in existing]

    if not args.execute:
        print("Dry run complete. Drafts that would be pushed:")
        for post in posts:
            print(f"- {post.title} ({post.source})")
        print(f"Endpoint: {endpoint}")
        print(f"Status: {'future @ next midnight' if schedule_midnight else status}")
        if tags:
            print(f"Tags: {', '.join(tags)}")
        if categories:
            print(f"Categories: {', '.join(categories)}")
        print("Run with --execute and WP_API_KEY to push to WordPress.")
        return 0

    if not args.api_key.strip():
        print("Missing API key. Set WP_API_KEY or pass --api-key.")
        return 1

    failed = False
    for post in posts:
        try:
            payload = build_payload(post, status, tags, categories, schedule_midnight, schedule_timezone)
            response = post_to_wordpress(endpoint, args.api_key, payload)
            print(f"Pushed draft: {post.title}")
            print(response[:400])
        except (HTTPError, URLError, TimeoutError, ValueError, KeyError) as exc:
            failed = True
            print(f"Failed to push {post.title}: {exc}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
