#!/usr/bin/env python3
"""
Auto Publisher — watches a folder and publishes new Markdown files to WordPress.

Usage:
    # Run once (process existing files then exit):
    python scripts/auto_publisher.py

    # Run continuously every 15 minutes:
    python scripts/auto_publisher.py --interval 900 --status draft

    # Or via cron (recommended):
    # */15 * * * * /usr/bin/python3 /path/to/scripts/auto_publisher.py

File format expected:
    First line = title (# Heading or plain text)
    Remaining lines = body content

Environment variables (set in scripts/.env):
    WP_API_URL    — REST endpoint
    WP_API_KEY    — X-Sourov-Key header value
    WP_WATCH_DIR  — folder to watch (default: ~/wordpress_queue)
    WP_POST_STATUS — draft | publish | future (default: draft)
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    sys.exit("Install requests: pip install requests")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)s  %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)


def _load_env(env_path: Path):
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_env(Path(__file__).parent / ".env")


def _suggest_tags(title: str, body: str) -> str:
    keywords = [
        "grammar", "listening", "speaking", "pronunciation",
        "celta", "elt", "phonology", "vocabulary", "writing", "reading",
    ]
    text = (title + " " + body[:400]).lower()
    return ", ".join(kw for kw in keywords if kw in text)


def _guess_category(title: str, body: str) -> str:
    text = (title + " " + body[:400]).lower()
    if "grammar" in text:                                        return "Grammar"
    if any(w in text for w in ["listening", "pronunciation", "phonology"]):
                                                                 return "Listening & Phonology"
    if "celta"   in text:                                        return "CELTA"
    if "speaking" in text:                                       return "Speaking"
    if "writing"  in text:                                       return "Writing"
    if any(w in text for w in ["vocabulary", "lexis"]):          return "Vocabulary"
    return "ELT Masterclass"


def _parse_file(filepath: Path) -> dict:
    raw   = filepath.read_text(encoding="utf-8")
    lines = raw.split("\n")
    title = lines[0].lstrip("# ").strip() if lines else filepath.stem
    body  = "\n".join(lines[1:]).strip()
    return {"title": title, "body": body}


def _publish(title: str, body: str, status: str, api_url: str, api_key: str) -> dict | None:
    payload = {
        "title":            title,
        "content":          body,
        "status":           status,
        "tags":             _suggest_tags(title, body),
        "category":         _guess_category(title, body),
        "meta_description": body[:160].replace("\n", " "),
        "seo_title":        title,
    }
    try:
        r = requests.post(
            api_url, json=payload,
            headers={"X-Sourov-Key": api_key, "Content-Type": "application/json"},
            timeout=20,
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        log.error("Cannot reach WordPress (%s). Check WP_API_URL.", api_url)
    except requests.exceptions.HTTPError:
        log.error("HTTP %s: %s", r.status_code, r.text[:200])
    except Exception as e:
        log.error("Unexpected error: %s", e)
    return None


def process_folder(watch_dir: Path, archive_dir: Path, api_url: str, api_key: str, status: str):
    md_files = sorted(watch_dir.glob("*.md"))
    if not md_files:
        log.info("No new Markdown files in %s", watch_dir)
        return

    log.info("%d file(s) to process.", len(md_files))
    for filepath in md_files:
        parsed = _parse_file(filepath)
        log.info("Publishing: %s", parsed["title"])
        result = _publish(parsed["title"], parsed["body"], status, api_url, api_key)
        if result and result.get("post_id"):
            log.info("  OK — Post ID %s", result["post_id"])
            archive_dir.mkdir(parents=True, exist_ok=True)
            filepath.rename(archive_dir / filepath.name)
        else:
            log.warning("  FAIL — file left in queue: %s", filepath.name)


def main():
    parser = argparse.ArgumentParser(description="Auto-publish Markdown files to WordPress")
    parser.add_argument("--watch-dir", default=os.environ.get("WP_WATCH_DIR",
                        str(Path.home() / "wordpress_queue")))
    parser.add_argument("--interval",  type=int, default=0,
                        help="Polling interval in seconds (0 = run once and exit)")
    parser.add_argument("--status",    default=os.environ.get("WP_POST_STATUS", "draft"),
                        choices=["draft", "publish", "future"])
    args = parser.parse_args()

    api_url = os.environ.get("WP_API_URL", "")
    api_key = os.environ.get("WP_API_KEY", "")
    if not api_url or not api_key:
        log.error("Set WP_API_URL and WP_API_KEY in scripts/.env or environment.")
        sys.exit(1)

    watch_dir   = Path(args.watch_dir)
    archive_dir = watch_dir / "archive"
    watch_dir.mkdir(parents=True, exist_ok=True)
    log.info("Watch dir: %s | Status: %s", watch_dir, args.status)

    if args.interval > 0:
        log.info("Polling every %ds. Ctrl+C to stop.", args.interval)
        while True:
            process_folder(watch_dir, archive_dir, api_url, api_key, args.status)
            time.sleep(args.interval)
    else:
        process_folder(watch_dir, archive_dir, api_url, api_key, args.status)


if __name__ == "__main__":
    main()
