#!/usr/bin/env python3
"""Generate an hourly chronological story post, save locally, and optionally publish to WordPress."""

from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable, List
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = Path(__file__).with_name("wordpress_publish_defaults.json")
DEFAULT_ENDPOINT = "https://www.sourovdeb.com/wp-json/sourov/v1/ai-post"
DEFAULT_OUTPUT_DIR = ROOT / "03_communications" / "hourly_story_posts"
DEFAULT_SOURCE_GLOBS = [
    "02_identity_profile/**/*.md",
    "03_communications/**/*.md",
    "05_jobs_cv_outreach/**/*.md",
]
SENSITIVE_PATH_SEGMENTS = {"04_legal_medical", "07_mental_health_support"}


@dataclass
class SourceDocument:
    path: Path
    title: str
    text: str


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def normalize_terms(values: Iterable[str]) -> List[str]:
    output: List[str] = []
    seen = set()
    for raw in values:
        for part in str(raw).split(","):
            value = part.strip()
            if value and value not in seen:
                output.append(value)
                seen.add(value)
    return output


def slugify(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return cleaned[:80] or "story"


def read_source(path: Path) -> SourceDocument:
    text = path.read_text(encoding="utf-8", errors="ignore")
    title = path.stem.replace("_", " ").replace("-", " ").title()
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            title = stripped.lstrip("#").strip()
            break
    return SourceDocument(path=path, title=title, text=text)


def extract_excerpt(text: str, limit_words: int = 70) -> str:
    words = re.findall(r"\S+", text)
    if not words:
        return "No excerpt available from the selected source file."
    return " ".join(words[:limit_words])


def exact_word_count_text(text: str, target_words: int) -> str:
    words = re.findall(r"\S+", text)
    if len(words) >= target_words:
        return " ".join(words[:target_words])
    filler = (
        "The pattern also highlights resilience, adaptation, and practical learning through repeated effort. "
        "This supports continuity, focus, and long term progress."
    )
    while len(words) < target_words:
        words.extend(re.findall(r"\S+", filler))
    return " ".join(words[:target_words])


def build_story(now_local: datetime, source: SourceDocument, run_count: int) -> str:
    excerpt = extract_excerpt(source.text, limit_words=95)
    return (
        f"Hour {run_count}: {now_local.strftime('%Y-%m-%d %H:%M')} marks another chapter in Sourov Deb's evolving journey. "
        f"Today the timeline spotlight comes from '{source.title}', where lived experience and practical intent meet. "
        f"The story moves chronologically: first challenge, then reflection, then structured action. "
        f"Each step shows a person building systems around real constraints while staying anchored to purpose. "
        f"The source record adds texture: {excerpt}. "
        f"Seen in sequence with earlier entries, this moment is not isolated; it belongs to a larger arc of persistence, self-advocacy, "
        f"and methodical progress. The narrative remains forward-looking, turning archived experience into actionable direction for the next hour."
    )


def build_analysis_200_words(source: SourceDocument) -> str:
    path_note = str(source.path.relative_to(ROOT))
    draft = (
        f"This source indicates a consistent pattern of reflective problem solving grounded in documentation and iterative action. "
        f"The file '{source.title}' from '{path_note}' shows that progress is made by converting complex personal and operational realities into "
        f"clear steps, then revisiting those steps over time. The chronology matters because each decision appears linked to prior evidence, "
        f"rather than isolated reactions. That gives the process continuity and makes future decisions easier to justify. "
        f"From an analytical perspective, three strengths stand out: structured tracking, adaptive prioritization, and persistence under pressure. "
        f"Structured tracking preserves context and reduces repeated work. Adaptive prioritization keeps attention on high-impact actions while still "
        f"allowing flexibility when new information appears. Persistence ensures that setbacks are documented, interpreted, and translated into the next plan. "
        f"The combined effect is a self-reinforcing feedback loop: document, interpret, act, and refine. This loop supports both narrative clarity and practical execution. "
        f"Overall, the material reflects an identity-centered workflow where personal history becomes operational intelligence, enabling measurable progress with reduced friction."
    )
    return exact_word_count_text(draft, 200)


def gather_source_files(globs: Iterable[str]) -> List[Path]:
    candidates: List[Path] = []
    for pattern in globs:
        candidates.extend(ROOT.glob(pattern))
    files = []
    for path in candidates:
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".txt"}:
            continue
        if "08_archive" in path.parts:
            continue
        if any(segment in path.parts for segment in SENSITIVE_PATH_SEGMENTS):
            continue
        try:
            if path.stat().st_size > 250_000:
                continue
        except OSError:
            continue
        files.append(path)
    unique = sorted(set(files), key=lambda p: (p.stat().st_mtime, str(p)))
    return unique


def load_state(state_path: Path) -> dict[str, int]:
    if not state_path.exists():
        return {"next_index": 0, "run_count": 0}
    try:
        data = json.loads(state_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"next_index": 0, "run_count": 0}
    return {
        "next_index": int(data.get("next_index", 0)),
        "run_count": int(data.get("run_count", 0)),
    }


def save_state(state_path: Path, next_index: int, run_count: int) -> None:
    state_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"next_index": next_index, "run_count": run_count, "updated_at_utc": datetime.now(timezone.utc).isoformat()}
    state_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def fetch_github_reference(topic: str) -> dict[str, str]:
    query = quote_plus(topic or "automation")
    url = f"https://api.github.com/search/repositories?q={query}&sort=updated&order=desc&per_page=1"
    request = Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "sourov-hourly-story-bot"})
    try:
        with urlopen(request, timeout=15) as response:
            payload = json.loads(response.read().decode("utf-8", errors="ignore"))
        items = payload.get("items") or []
        if items:
            repo = items[0]
            return {
                "name": repo.get("full_name", "Unknown repository"),
                "url": repo.get("html_url", "https://github.com"),
                "description": (repo.get("description") or "No description provided.").strip(),
            }
    except (HTTPError, URLError, TimeoutError, ValueError, json.JSONDecodeError):
        pass
    return {
        "name": "sourovdeb/my_professional_documents",
        "url": "https://github.com/sourovdeb/my_professional_documents",
        "description": "Fallback reference from the current repository.",
    }


def build_markdown(
    title: str,
    generated_at: datetime,
    source: SourceDocument,
    github_reference: dict[str, str],
    story: str,
    analysis_200: str,
) -> str:
    return "\n".join(
        [
            f"# {title}",
            "",
            f"- Generated at (UTC): {generated_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Source file: {source.path.relative_to(ROOT)}",
            "",
            "## Chronological Story",
            "",
            story,
            "",
            "## Analytical Explanation (200 words)",
            "",
            analysis_200,
            "",
            "## GitHub Reference (at least one)",
            "",
            f"- [{github_reference['name']}]({github_reference['url']}) — {github_reference['description']}",
            "",
        ]
    )


def publish_to_wordpress(endpoint: str, api_key: str, payload: dict[str, Any]) -> str:
    request = Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "X-Sourov-Key": api_key,
        },
    )
    with urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="ignore")


def schedule_payload(hours_ahead: int, timezone_name: str) -> dict[str, str]:
    local_zone = ZoneInfo(timezone_name)
    now_local = datetime.now(local_zone)
    scheduled_local = now_local + timedelta(hours=hours_ahead)
    scheduled_utc = scheduled_local.astimezone(timezone.utc)
    return {
        "date": scheduled_local.replace(tzinfo=None).isoformat(timespec="seconds"),
        "date_gmt": scheduled_utc.replace(tzinfo=None).isoformat(timespec="seconds"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate an hourly chronological story draft and optionally publish to WordPress.")
    parser.add_argument("--execute", action="store_true", help="Publish to WordPress after generating local file.")
    parser.add_argument("--api-key", default="", help="WordPress API key (or set WP_API_KEY env).")
    parser.add_argument("--endpoint", default=None, help="WordPress endpoint override.")
    parser.add_argument("--config", default=str(CONFIG_PATH), help="Path to JSON config.")
    parser.add_argument("--output-dir", default=None, help="Directory for generated story markdown files.")
    parser.add_argument("--status", default=None, help="WordPress status override (draft/future/publish).")
    parser.add_argument("--schedule-hours", type=int, default=1, help="Schedule publish this many hours ahead (default: 1).")
    parser.add_argument("--schedule-timezone", default=None, help="Timezone for scheduling (default from config or UTC).")
    parser.add_argument("--tag", action="append", default=[], help="Tag(s), repeatable and comma-separated supported.")
    parser.add_argument("--category", action="append", default=[], help="Category(s), repeatable and comma-separated supported.")
    parser.add_argument("--source-glob", action="append", default=[], help="Source glob(s), repeatable.")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    output_dir = Path(args.output_dir or config.get("hourly_story_output_dir") or DEFAULT_OUTPUT_DIR)
    source_globs = args.source_glob or config.get("hourly_story_source_globs") or DEFAULT_SOURCE_GLOBS
    endpoint = args.endpoint or str(config.get("wordpress_endpoint", DEFAULT_ENDPOINT))
    status = args.status or str(config.get("hourly_story_default_status", "future"))
    schedule_timezone = args.schedule_timezone or str(config.get("schedule_timezone", "UTC"))
    api_key = args.api_key.strip() or str(os.environ.get("WP_API_KEY", "")).strip()
    default_tags = normalize_terms(config.get("hourly_story_default_tags", ["chronological-story", "sourov"]))
    default_categories = normalize_terms(config.get("hourly_story_default_categories", ["life-story"]))
    tags = normalize_terms(args.tag) if args.tag else default_tags
    categories = normalize_terms(args.category) if args.category else default_categories

    files = gather_source_files(source_globs)
    if not files:
        print("No source files matched for hourly story generation.")
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / "hourly_story_state.json"
    state = load_state(state_path)
    index = state["next_index"] % len(files)
    run_count = state["run_count"] + 1

    source = read_source(files[index])
    now_local = datetime.now(ZoneInfo(schedule_timezone))
    title = f"Hourly Chronicle {run_count}: {source.title}"
    story = build_story(now_local, source, run_count)
    analysis = build_analysis_200_words(source)
    github_ref = fetch_github_reference(source.title.split()[0] if source.title.split() else "automation")
    markdown = build_markdown(title, datetime.now(timezone.utc), source, github_ref, story, analysis)

    file_name = f"{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}_{slugify(source.title)}.md"
    output_path = output_dir / file_name
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Generated local story draft: {output_path}")

    save_state(state_path, next_index=index + 1, run_count=run_count)

    if not args.execute:
        print("Dry run complete. Use --execute to publish this generated draft to WordPress.")
        return 0

    if not api_key:
        print("Missing API key. Set WP_API_KEY or pass --api-key.")
        return 1

    payload: dict[str, Any] = {
        "title": title,
        "content": markdown,
        "status": status,
    }
    if tags:
        payload["tags"] = tags
    if categories:
        payload["categories"] = categories
    if args.schedule_hours > 0:
        payload["status"] = "future"
        payload.update(schedule_payload(args.schedule_hours, schedule_timezone))

    try:
        response = publish_to_wordpress(endpoint, api_key, payload)
        print(f"Published to WordPress: {title}")
        print(response[:400])
    except (HTTPError, URLError, TimeoutError, ValueError) as exc:
        print(f"WordPress publish failed: {exc}")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
