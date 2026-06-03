#!/usr/bin/env python3
"""Run a 6-hour discovery cycle and log important findings for the user."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Tuple
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[3]
CONFIG_PATH = Path(__file__).resolve().parent / "discovery_sources.json"
REPORT_DIR = ROOT / "06_automation_assets" / "tool_discovery_reports"
IMPORTANT_FILE = ROOT / "IMPORTANT_FOR_USER.md"
MAX_ITEMS = 5
REQUEST_TIMEOUT = 15


@dataclass
class Candidate:
    title: str
    link: str
    summary: str
    source: str
    matched_areas: List[str]
    score: int


def read_config() -> Tuple[List[str], Dict[str, List[str]]]:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data.get("sources", []), data.get("areas", {})


def fetch_rss(url: str) -> str:
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 automation-discovery-bot"})
    with urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        return response.read().decode("utf-8", errors="ignore")


def extract_text(node: ET.Element, tag: str) -> str:
    child = node.find(tag)
    return (child.text or "").strip() if child is not None else ""


def parse_items(feed_xml: str, source_url: str) -> Iterable[Tuple[str, str, str, str]]:
    root = ET.fromstring(feed_xml)
    for item in root.findall("./channel/item"):
        yield (
            extract_text(item, "title"),
            extract_text(item, "link"),
            extract_text(item, "description"),
            source_url,
        )


def score_candidate(title: str, summary: str, areas: Dict[str, List[str]]) -> Tuple[int, List[str]]:
    text = f"{title} {summary}".lower()
    score = 0
    matched = []
    for area, keywords in areas.items():
        area_matches = sum(1 for keyword in keywords if re.search(rf"\\b{re.escape(keyword.lower())}\\b", text))
        if area_matches:
            matched.append(area)
            score += area_matches
    return score, matched


def collect_candidates(sources: List[str], areas: Dict[str, List[str]]) -> Tuple[List[Candidate], List[str]]:
    candidates: List[Candidate] = []
    errors: List[str] = []

    for source in sources:
        try:
            feed_xml = fetch_rss(source)
            for title, link, summary, source_url in parse_items(feed_xml, source):
                score, matched = score_candidate(title, summary, areas)
                if score > 0:
                    candidates.append(
                        Candidate(
                            title=title or "(untitled)",
                            link=link or source_url,
                            summary=re.sub(r"<[^>]+>", "", summary).strip(),
                            source=source_url,
                            matched_areas=matched,
                            score=score,
                        )
                    )
        except (URLError, HTTPError, ET.ParseError, TimeoutError, ValueError) as exc:
            errors.append(f"{source}: {exc}")

    candidates.sort(key=lambda c: c.score, reverse=True)
    return candidates[:MAX_ITEMS], errors


def write_report(candidates: List[Candidate], errors: List[str]) -> Path:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    report_path = REPORT_DIR / f"discovery_report_{timestamp}.md"

    lines = [
        "# 6-Hour Discovery Report",
        "",
        f"Generated: {timestamp}",
        "",
        "## Important findings",
        "",
    ]

    if candidates:
        for idx, item in enumerate(candidates, start=1):
            lines.extend(
                [
                    f"{idx}. **{item.title}**",
                    f"   - Link: {item.link}",
                    f"   - Matched areas: {', '.join(item.matched_areas)}",
                    f"   - Relevance score: {item.score}",
                    f"   - Source: {item.source}",
                    f"   - Note: {item.summary[:240] or 'No summary available'}",
                    "",
                ]
            )
    else:
        lines.extend(["No relevant findings were detected in this cycle.", ""])

    lines.extend(["## Source errors", ""])
    if errors:
        lines.extend([f"- {error}" for error in errors])
    else:
        lines.append("- None")

    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def update_important_file(report_path: Path, candidates: List[Candidate]) -> None:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Important Findings for User",
        "",
        "This file is updated by the 6-hour discovery cycle.",
        "",
        f"Last update: {timestamp}",
        f"Latest report: `{report_path.relative_to(ROOT)}`",
        "",
        "## Current top findings",
        "",
    ]

    if candidates:
        for item in candidates:
            lines.append(f"- **{item.title}** ({', '.join(item.matched_areas)}) — {item.link}")
    else:
        lines.append("- No current high-priority findings.")

    IMPORTANT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    sources, areas = read_config()
    candidates, errors = collect_candidates(sources, areas)
    report_path = write_report(candidates, errors)
    update_important_file(report_path, candidates)
    print(f"Report generated: {report_path}")


if __name__ == "__main__":
    main()
