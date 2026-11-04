#!/usr/bin/env python3
"""Hourly FT (France Travail) offer harvester.

Scrapes fresh offer IDs/titles from the public search results page for a set
of profile-relevant keywords, dedupes against everything harvested before and
against the applied-IDs blacklist, and writes:
  data/fresh_offers.csv      - current actionable queue (id, title, keyword, first_seen)
  data/all_seen_ids.txt      - every ID ever harvested (append-only)
  data/harvest_log.md        - human-readable hourly log line

Designed to run in GitHub Actions every hour (cron). Zero auth: the FT results
page renders offer links server-side (verified 2026-11-04).
"""
import csv
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import quote

KEYWORDS = [
    "anglais", "english", "FLE", "formateur anglais", "enseignant anglais",
    "professeur anglais", "bilingue", "alphabetisation", "formateur FLE",
    "mediateur", "traduction", "formateur langue",
]
DETAIL_RE = re.compile(r"/offres/recherche/detail/([A-Z0-9]{6,8})")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) job-pipeline/1.0"
BASE = "https://candidat.francetravail.fr/offres/recherche?motsCles={kw}"
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def fetch(keyword: str) -> list[tuple[str, str]]:
    url = BASE.format(kw=quote(keyword))
    req = Request(url, headers={"User-Agent": UA})
    try:
        html = urlopen(req, timeout=30).read().decode("utf-8", "ignore")
    except Exception as exc:  # noqa: BLE001 - log and continue
        print(f"[warn] {keyword}: {exc}")
        return []
    # titles: pair each detail link with its anchor text
    pairs = re.findall(
        r'href="(/offres/recherche/detail/[A-Z0-9]{6,8})"[^>]*>(.*?)</a>',
        html, re.S,
    )
    out = []
    seen = set()
    for href, title in pairs:
        oid = href.rsplit("/", 1)[-1]
        if oid in seen:
            continue
        seen.add(oid)
        clean = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", title)).strip()[:120]
        out.append((oid, clean or "(no title)"))
    return out


def main() -> None:
    DATA.mkdir(exist_ok=True)
    seen_path = DATA / "all_seen_ids.txt"
    applied_path = DATA / "applied_ids_blacklist.txt"
    fresh_path = DATA / "fresh_offers.csv"
    log_path = DATA / "harvest_log.md"

    seen = set(seen_path.read_text().split()) if seen_path.exists() else set()
    blacklist = set()
    if applied_path.exists():
        blacklist = {x.strip() for x in applied_path.read_text().splitlines() if x.strip()}

    harvested: dict[str, tuple[str, str]] = {}
    for kw in KEYWORDS:
        for oid, title in fetch(kw):
            harvested.setdefault(oid, (title, kw))

    new_ids = [i for i in harvested if i not in seen]
    # relevance gate: teaching/language/communication only (regex tier;
    # deeper Agnes/TypeSafe classification runs out-of-band on fresh_offers.csv)
    rel = re.compile(
        r"(?i)(\banglais\b|english|FLE|fran\xe7ais langue|langue \xe9trang\xe8re|"
        r"alphab\xe9t|illettrism|enseignant (fran\xe7ais|anglais)|"
        r"professeur.*(anglais|FLE|fran\xe7ais)|formateur.*(anglais|FLE|fran\xe7ais|langue)|"
        r"bilingue.*bilingual|traduction|traducteur|m\xe9diateur|bilingual)"
    )
    kept = [(i, t, kw) for i, (t, kw) in harvested.items()
            if i not in blacklist and rel.search(t)]
    new_kept = [x for x in kept if x[0] in new_ids]

    if seen_path.exists():
        with seen_path.open("a") as f:
            f.write("\n".join(new_ids) + ("\n" if new_ids else ""))
    else:
        seen_path.write_text("\n".join(new_ids) + ("\n" if new_ids else ""))

    # rebuild fresh queue = all kept rows minus blacklist (titles refreshed)
    with fresh_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "title", "keyword"])
        w.writerows(kept)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    line = (f"- {now}: kw={len(KEYWORDS)} harvested={len(harvested)} "
            f"new={len(new_ids)} queue_total={len(kept)} new_relevant={len(new_kept)}\n")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line)
    print(line.strip())
    if new_kept:
        print("new relevant offers:", ", ".join(i for i, _, _ in new_kept[:15]))


if __name__ == "__main__":
    main()
