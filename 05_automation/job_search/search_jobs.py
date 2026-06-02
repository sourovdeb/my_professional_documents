#!/usr/bin/env python3
"""
Automated job search — scrapes Indeed, LinkedIn, and Glassdoor using jobspy.
Outputs results to a markdown file for review.

Install once:
    pip install python-jobspy

Usage:
    python search_jobs.py                        # run with defaults
    python search_jobs.py --role "English teacher" --location "La Réunion"
    python search_jobs.py --role "barista" --location "Paris, France" --days 7
    python search_jobs.py --role "content writer" --location "remote" --remote
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

# ── Default search profiles (customise these) ──────────────────────────────

DEFAULT_SEARCHES = [
    {"role": "English teacher", "location": "La Réunion, France", "remote": False},
    {"role": "English teacher", "location": "France", "remote": True},
    {"role": "content writer", "location": "France", "remote": True},
    {"role": "hospitality manager", "location": "La Réunion, France", "remote": False},
    {"role": "formateur anglais", "location": "France", "remote": True},
    {"role": "freelance writer", "location": "remote", "remote": True},
]

OUTPUT_DIR = Path(__file__).parent / "results"

# ── Main ────────────────────────────────────────────────────────────────────

def check_jobspy():
    try:
        from jobspy import scrape_jobs
        return scrape_jobs
    except ImportError:
        print("jobspy not installed. Run: pip install python-jobspy")
        print("jobspy scrapes Indeed, LinkedIn, Glassdoor for free — no API key needed.")
        sys.exit(1)


def search(scrape_jobs, role: str, location: str, remote: bool = False, days: int = 14) -> list:
    results = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor"],
        search_term=role,
        location=location,
        is_remote=remote,
        results_wanted=30,
        hours_old=days * 24,
        country_indeed="France",
    )
    return results.to_dict("records") if hasattr(results, "to_dict") else []


def format_job(job: dict) -> str:
    title = job.get("title", "Unknown")
    company = job.get("company", "Unknown")
    location = job.get("location", "")
    source = job.get("site", "")
    url = job.get("job_url", "")
    salary = job.get("min_amount", "")
    description = (job.get("description", "") or "")[:300].replace("\n", " ").strip()

    lines = [f"### {title} — {company}"]
    if location:
        lines.append(f"**Location:** {location}")
    if salary:
        lines.append(f"**Salary:** {salary}")
    lines.append(f"**Source:** {source}")
    if url:
        lines.append(f"**Apply:** {url}")
    if description:
        lines.append(f"\n> {description}...")
    lines.append("")
    return "\n".join(lines)


def save_results(all_jobs: list, search_args: dict) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    fname = OUTPUT_DIR / f"jobs_{date_str}.md"

    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"# Job Search Results — {date_str}\n\n")
        f.write(f"Searched for: **{search_args.get('role', 'multiple')}** in **{search_args.get('location', 'multiple')}**\n\n")
        f.write(f"Total results: {len(all_jobs)}\n\n---\n\n")

        if not all_jobs:
            f.write("No results found. Try broadening the search.\n")
        else:
            for job in all_jobs:
                f.write(format_job(job))
                f.write("\n")

    return fname


def main():
    parser = argparse.ArgumentParser(description="Search jobs on Indeed, LinkedIn, Glassdoor.")
    parser.add_argument("--role", help="Job title to search")
    parser.add_argument("--location", help="Location (city, country, or 'remote')")
    parser.add_argument("--remote", action="store_true", help="Remote jobs only")
    parser.add_argument("--days", type=int, default=14, help="Jobs posted within N days (default 14)")
    parser.add_argument("--all-profiles", action="store_true", help="Run all default search profiles")
    args = parser.parse_args()

    scrape_jobs = check_jobspy()

    all_results = []

    if args.all_profiles or (not args.role and not args.location):
        print(f"Running {len(DEFAULT_SEARCHES)} search profiles...")
        for profile in DEFAULT_SEARCHES:
            print(f"  Searching: {profile['role']} in {profile['location']}...")
            try:
                jobs = search(scrape_jobs, profile["role"], profile["location"],
                              profile["remote"], args.days)
                all_results.extend(jobs)
                print(f"    Found {len(jobs)} results")
            except Exception as e:
                print(f"    Error: {e}")

        output_file = save_results(all_results, {"role": "multiple profiles", "location": "multiple"})
    else:
        role = args.role or "English teacher"
        location = args.location or "France"
        print(f"Searching: {role} in {location}...")
        jobs = search(scrape_jobs, role, location, args.remote, args.days)
        print(f"Found {len(jobs)} results")
        output_file = save_results(jobs, {"role": role, "location": location})

    print(f"\nResults saved: {output_file}")
    print(f"Open with: cat {output_file}")


if __name__ == "__main__":
    main()
