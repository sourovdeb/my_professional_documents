#!/usr/bin/env python3
"""
Job Hunter — fetches ELT/teaching job listings from Indeed RSS and emails a daily digest.

Usage:
    python scripts/job_hunter.py

Cron (daily at 8 AM):
    0 8 * * * /usr/bin/python3 /path/to/scripts/job_hunter.py

Environment variables (set in scripts/.env):
    EMAIL_FROM      — sender address (your Zoho / Gmail account)
    EMAIL_TO        — where to send the digest
    EMAIL_PASSWORD  — app password (not your main password)
    SMTP_HOST       — default: smtp.zoho.com
    SMTP_PORT       — default: 587

Runs without email credentials — prints HTML to stdout instead.
"""

import json
import logging
import os
import smtplib
import sys
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    sys.exit("Install dependencies: pip install requests beautifulsoup4 lxml")

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
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

EMAIL_FROM     = os.environ.get("EMAIL_FROM",     "")
EMAIL_TO       = os.environ.get("EMAIL_TO",       "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_HOST      = os.environ.get("SMTP_HOST",      "smtp.zoho.com")
SMTP_PORT      = int(os.environ.get("SMTP_PORT",  "587"))

SEARCHES = [
    {"query": "ELT teacher",           "location": "Reunion"},
    {"query": "English language teacher","location": "Reunion Island"},
    {"query": "CELTA trainer",          "location": "France"},
    {"query": "ESL teacher online",     "location": ""},
    {"query": "English teacher remote", "location": ""},
]


def fetch_indeed_rss(query: str, location: str, max_results: int = 8) -> list[dict]:
    url = (
        f"https://rss.indeed.com/rss"
        f"?q={requests.utils.quote(query)}"
        f"&l={requests.utils.quote(location)}"
    )
    try:
        r = requests.get(url, timeout=15,
                         headers={"User-Agent": "Mozilla/5.0 (compatible; JobBot/1.0)"})
        r.raise_for_status()
        soup  = BeautifulSoup(r.content, "xml")
        items = soup.find_all("item")[:max_results]
        jobs  = []
        for item in items:
            desc_raw  = item.description.get_text() if item.description else ""
            desc_text = BeautifulSoup(desc_raw, "html.parser").get_text()[:200]
            jobs.append({
                "title":   item.title.get_text(strip=True)   if item.title   else "Untitled",
                "link":    item.link.get_text(strip=True)    if item.link    else "",
                "company": item.find("source").get_text(strip=True)
                           if item.find("source") else "Unknown",
                "summary": desc_text,
                "date":    item.pubDate.get_text(strip=True) if item.pubDate else "",
            })
        return jobs
    except Exception as exc:
        log.warning("RSS fetch failed (%s / %s): %s", query, location, exc)
        return []


def build_html(all_jobs: dict) -> str:
    today = datetime.now().strftime("%A %d %B %Y")
    total = sum(len(v) for v in all_jobs.values())
    lines = [
        "<html><body style='font-family:sans-serif;max-width:700px;margin:auto'>",
        f"<h2>Job Digest — {today}</h2>",
        f"<p><strong>{total} listings across {len(all_jobs)} searches.</strong></p><hr>",
    ]
    for search_label, jobs in all_jobs.items():
        lines.append(f"<h3>{search_label}</h3>")
        if not jobs:
            lines.append("<p><em>No results.</em></p>")
            continue
        lines.append("<ul>")
        for j in jobs:
            lines.append(
                f'<li><strong><a href="{j["link"]}">{j["title"]}</a></strong>'
                f' — {j["company"]}<br>'
                f'<small style="color:#555">{j["summary"]}</small><br>'
                f'<small style="color:#999">Posted: {j["date"]}</small></li><br>'
            )
        lines.append("</ul>")
    lines.append("</body></html>")
    return "\n".join(lines)


def send_email(subject: str, html_body: str):
    if not all([EMAIL_FROM, EMAIL_TO, EMAIL_PASSWORD]):
        log.info("Email credentials not set — printing digest to stdout.")
        print(html_body)
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = EMAIL_FROM
    msg["To"]      = EMAIL_TO
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.send_message(msg)
    log.info("Digest emailed to %s", EMAIL_TO)


def save_log(all_jobs: dict):
    log_dir = Path(__file__).parent.parent / "docs" / "job_logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    fname = log_dir / f"jobs_{datetime.now().strftime('%Y-%m-%d')}.json"
    fname.write_text(json.dumps(all_jobs, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("Log saved: %s", fname)


def main():
    all_jobs = {}
    for s in SEARCHES:
        label = f"{s['query']} ({s['location'] or 'remote/global'})"
        log.info("Fetching: %s", label)
        jobs = fetch_indeed_rss(s["query"], s["location"])
        log.info("  %d listings", len(jobs))
        all_jobs[label] = jobs

    save_log(all_jobs)
    html = build_html(all_jobs)
    send_email(f"Job Digest {datetime.now().strftime('%Y-%m-%d')}", html)


if __name__ == "__main__":
    main()
