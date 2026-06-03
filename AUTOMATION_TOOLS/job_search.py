#!/usr/bin/env python3
"""
Job search automation using JobSpy.
Scrapes Indeed, LinkedIn, and Glassdoor simultaneously.

Install: pip install jobspy
Run:     python job_search.py
Output:  jobs_YYYY-MM-DD.csv
"""

from datetime import date
import csv

try:
    from jobspy import scrape_jobs
except ImportError:
    print("Install first: pip install jobspy")
    raise

# --- Configure here ---
SEARCH_TERMS = [
    "English teacher La Reunion",
    "formateur anglais La Reunion",
    "CELTA teacher France",
    "English trainer remote France",
    "language trainer freelance France",
    "formateur langue anglaise",
]

LOCATION = "La Réunion, France"
RESULTS_PER_TERM = 20
HOURS_OLD = 72
# ---------------------

all_jobs = []

for term in SEARCH_TERMS:
    print(f"Searching: {term} ...")
    try:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=term,
            location=LOCATION,
            results_wanted=RESULTS_PER_TERM,
            hours_old=HOURS_OLD,
            country_indeed="France",
        )
        all_jobs.extend(jobs.to_dict("records"))
        print(f"  {len(jobs)} results")
    except Exception as e:
        print(f"  Error: {e}")

# Deduplicate by job URL
seen = set()
unique = []
for job in all_jobs:
    url = job.get("job_url", "")
    if url and url not in seen:
        seen.add(url)
        unique.append(job)

filename = f"jobs_{date.today()}.csv"
if unique:
    keys = unique[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(unique)
    print(f"\nSaved {len(unique)} unique jobs → {filename}")
else:
    print("No jobs found. Try broadening the search terms.")
