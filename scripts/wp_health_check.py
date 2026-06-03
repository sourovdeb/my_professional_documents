#!/usr/bin/env python3
"""
WordPress Health Check — tests REST API, custom endpoint, SSL, sitemap, robots.txt.

Usage:
    python scripts/wp_health_check.py

Outputs a JSON report to docs/health_report_YYYY-MM-DD.json.
Exits with code 1 if any check fails (useful in CI).

Environment variables (set in scripts/.env):
    WP_BASE_URL  — e.g. https://yourdomain.com
    WP_API_KEY   — X-Sourov-Key value
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("Install requests: pip install requests")

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

WP_BASE  = os.environ.get("WP_BASE_URL", "").rstrip("/")
API_KEY  = os.environ.get("WP_API_KEY",  "")
TIMEOUT = 12


def _run(name: str, fn) -> dict:
    start = time.monotonic()
    try:
        detail  = fn()
        elapsed = round((time.monotonic() - start) * 1000)
        log.info("  PASS  %-40s %dms", name, elapsed)
        return {"check": name, "status": "pass", "ms": elapsed, "detail": detail}
    except Exception as exc:
        elapsed = round((time.monotonic() - start) * 1000)
        log.warning("  FAIL  %-40s %s", name, exc)
        return {"check": name, "status": "fail", "ms": elapsed, "detail": str(exc)}


# ─── Individual checks ───────────────────────────────────────────────────────

def check_wp_api():
    r = requests.get(f"{WP_BASE}/wp-json/", timeout=TIMEOUT)
    r.raise_for_status()
    d = r.json()
    return {"name": d.get("name"), "url": d.get("url"), "version": d.get("description", "")[:40]}


def check_custom_endpoint():
    if not API_KEY:
        return "skipped — WP_API_KEY not set"
    r = requests.get(
        f"{WP_BASE}/wp-json/sourov/v1/health",
        headers={"X-Sourov-Key": API_KEY},
        timeout=TIMEOUT,
    )
    if r.status_code == 404:
        return "endpoint not found (plugin inactive?)"
    r.raise_for_status()
    return r.json()


def check_home_page():
    r = requests.get(WP_BASE, timeout=TIMEOUT)
    r.raise_for_status()
    return {"http": r.status_code, "bytes": len(r.content), "has_wp_content": "wp-content" in r.text}


def check_ssl():
    if not WP_BASE.startswith("https://"):
        raise ValueError("Site not using HTTPS")
    r = requests.get(WP_BASE, timeout=TIMEOUT, verify=True)
    return {"ssl_valid": True, "http": r.status_code}


def check_robots():
    r = requests.get(f"{WP_BASE}/robots.txt", timeout=TIMEOUT)
    return {"status": r.status_code, "has_disallow": "Disallow" in r.text}


def check_sitemap():
    for path in ["/sitemap.xml", "/sitemap_index.xml", "/wp-sitemap.xml"]:
        try:
            r = requests.get(f"{WP_BASE}{path}", timeout=TIMEOUT)
            if r.status_code == 200:
                return {"found_at": path, "bytes": len(r.content)}
        except Exception:
            continue
    raise FileNotFoundError("No sitemap found")


def check_feeds():
    r = requests.get(f"{WP_BASE}/feed/", timeout=TIMEOUT)
    r.raise_for_status()
    return {"status": r.status_code, "is_xml": "rss" in r.text[:200].lower()}


def check_login_page():
    r = requests.get(f"{WP_BASE}/wp-login.php", timeout=TIMEOUT)
    return {"status": r.status_code, "accessible": r.status_code == 200}


# ─── Main ────────────────────────────────────────────────────────────────────

def run_all() -> dict:
    if not WP_BASE:
        log.error("WP_BASE_URL not set. Create scripts/.env with WP_BASE_URL=https://yourdomain.com")
        sys.exit(1)

    log.info("WordPress Health Check — %s", WP_BASE)
    checks_to_run = [
        ("WP REST API",            check_wp_api),
        ("Custom /health endpoint", check_custom_endpoint),
        ("Home page",              check_home_page),
        ("SSL certificate",        check_ssl),
        ("robots.txt",             check_robots),
        ("Sitemap",                check_sitemap),
        ("RSS feed",               check_feeds),
        ("Login page accessible",  check_login_page),
    ]

    results = [_run(name, fn) for name, fn in checks_to_run]
    passed  = sum(1 for r in results if r["status"] == "pass")
    total   = len(results)

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "site":      WP_BASE,
        "score":     f"{round(passed/total*100)}% ({passed}/{total})",
        "checks":    results,
    }
    return report


def main():
    report   = run_all()
    out_dir  = Path(__file__).parent.parent / "docs"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / f"health_report_{datetime.now().strftime('%Y-%m-%d')}.json"
    out_file.write_text(json.dumps(report, indent=2))
    log.info("Report: %s", out_file)
    log.info("Score:  %s", report["score"])
    if any(r["status"] == "fail" for r in report["checks"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
