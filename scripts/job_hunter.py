#!/usr/bin/env python3
"""
job_hunter.py
Automated job search using Indeed RSS and email alerts.
Also searches for ELT/teaching roles.

Usage:
  python job_hunter.py                   # search and print results
  python job_hunter.py --email           # send email summary
  python job_hunter.py --csv results.csv # save to CSV

Environment variables:
  SMTP_HOST      - SMTP server (default: smtp.gmail.com)
  SMTP_PORT      - SMTP port (default: 587)
  SMTP_USER      - Email username
  SMTP_PASSWORD  - Email password or app password
  EMAIL_TO       - Send results to this address
"""

import os
import csv
import time
import argparse
import smtplib
import xml.etree.ElementTree as ET
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from urllib.request import urlopen
from urllib.parse import urlencode

# ---- Config ----
SMTP_HOST    = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT    = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER    = os.environ.get('SMTP_USER', '')
SMTP_PASS    = os.environ.get('SMTP_PASSWORD', '')
EMAIL_TO     = os.environ.get('EMAIL_TO', 'sourovdeb.is@gmail.com')

# ---- Job Searches ----

SEARCHES = [
    {'query': 'ELT teacher',              'location': 'Reunion'},
    {'query': 'English language teacher', 'location': 'Reunion'},
    {'query': 'CELTA teacher',            'location': 'France'},
    {'query': 'English teacher',          'location': 'Mauritius'},
    {'query': 'content writer ELT',       'location': ''},
    {'query': 'online English tutor',     'location': ''},
]


def fetch_indeed_rss(query: str, location: str = '', max_results: int = 10) -> list:
    params = urlencode({'q': query, 'l': location, 'limit': max_results})
    url = f'https://rss.indeed.com/rss?{params}'
    try:
        with urlopen(url, timeout=15) as resp:
            tree = ET.parse(resp)
    except Exception as e:
        print(f'  RSS fetch failed for "{query}": {e}')
        return []

    jobs = []
    for item in tree.findall('.//item')[:max_results]:
        jobs.append({
            'title':    (item.findtext('title') or '').strip(),
            'company':  (item.findtext('source') or '').strip(),
            'link':     (item.findtext('link') or '').strip(),
            'location': location,
            'summary':  (item.findtext('description') or '')[:200].strip(),
            'date':     (item.findtext('pubDate') or '').strip(),
        })
    return jobs


def search_all() -> list:
    all_jobs = []
    seen_links = set()
    for s in SEARCHES:
        print(f'  Searching: {s["query"]} in {s["location"] or "remote"}')
        jobs = fetch_indeed_rss(s['query'], s['location'])
        for job in jobs:
            if job['link'] not in seen_links:
                seen_links.add(job['link'])
                all_jobs.append(job)
        time.sleep(1)  # Be respectful to the API
    return all_jobs


def jobs_to_text(jobs: list) -> str:
    lines = [f'Job Search Results — {datetime.now().strftime("%Y-%m-%d %H:%M")}',
             f'Found {len(jobs)} unique listings\n', '-'*60]
    for j in jobs:
        lines += [
            f'TITLE:   {j["title"]}',
            f'COMPANY: {j["company"] or "N/A"}',
            f'WHERE:   {j["location"] or "Remote"}',
            f'DATE:    {j["date"][:16] if j["date"] else "N/A"}',
            f'LINK:    {j["link"]}',
            f'SUMMARY: {j["summary"][:150]}...' if j["summary"] else '',
            '-'*60
        ]
    return '\n'.join(lines)


def save_csv(jobs: list, filepath: str):
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title','company','location','link','date','summary'])
        writer.writeheader()
        writer.writerows(jobs)
    print(f'Saved {len(jobs)} jobs to {filepath}')


def send_email(body: str, subject: str = None):
    if not SMTP_USER or not SMTP_PASS:
        print('No SMTP credentials. Set SMTP_USER and SMTP_PASSWORD.')
        return
    subject = subject or f'Job Search Results — {datetime.now().strftime("%Y-%m-%d")}: {len(body.split("TITLE:")) - 1} listings'
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = SMTP_USER
    msg['To']      = EMAIL_TO
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
    print(f'Email sent to {EMAIL_TO}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Job hunting automation')
    parser.add_argument('--email', action='store_true', help='Send email summary')
    parser.add_argument('--csv', metavar='FILE', help='Save results to CSV file')
    args = parser.parse_args()

    print('Searching for jobs...')
    jobs = search_all()
    print(f'Found {len(jobs)} listings')

    text = jobs_to_text(jobs)

    if args.csv:
        save_csv(jobs, args.csv)
    elif args.email:
        send_email(text)
    else:
        print(text)
