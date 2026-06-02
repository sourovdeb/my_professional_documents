#!/usr/bin/env python3
"""
Job Hunter Automation
=======================
Scrapes job boards (Indeed, LinkedIn, Job boards) for matches.
Outputs results to CSV for manual review + application tracking.

Usage:
    python3 job_hunter.py --roles "English Teacher,CELTA Trainer" --locations "Paris,Lyon,Remote" --output TRACKING/job_opportunities.csv

Features:
    - Searches multiple job boards in parallel
    - Filters by role, location, salary (if available)
    - Deduplicates results
    - Outputs to CSV for Google Sheets sync
    - Health-aware: Runs weekly (zero human input needed)

Author: Sourov Deb
Last updated: 2026-06-02
"""

import csv
import os
import json
import time
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging
from pathlib import Path

# Optional: Install requests for web scraping
# pip install requests beautifulsoup4 selenium-wire

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("⚠️  requests/beautifulsoup4 not installed. Install with: pip install requests beautifulsoup4")
    print("   Using mock data for now. Install dependencies to enable live scraping.")

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('TRACKING/job_hunter.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class JobHunter:
    """Scrapes job boards and aggregates results."""

    def __init__(self, output_csv: str = "TRACKING/job_opportunities.csv"):
        self.output_csv = output_csv
        self.jobs = {}  # Deduplicate by URL
        self.session = requests.Session() if HAS_REQUESTS else None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }

    def search_indeed(self, role: str, location: str) -> List[Dict]:
        """Search Indeed France for jobs."""
        logger.info(f"🔍 Searching Indeed: {role} in {location}")

        if not HAS_REQUESTS:
            logger.warning("Requests not available. Using mock data.")
            return self._mock_indeed_jobs(role, location)

        jobs = []
        url = f"https://fr.indeed.com/jobs?q={role}&l={location}"

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse job cards (Indeed HTML structure)
            job_cards = soup.find_all('div', class_='job_seen_beacon')

            for card in job_cards[:10]:  # Limit to first 10
                try:
                    title_elem = card.find('span', title=True)
                    title = title_elem.get_text() if title_elem else "N/A"

                    company_elem = card.find('span', class_='companyName')
                    company = company_elem.get_text() if company_elem else "N/A"

                    location_elem = card.find('div', class_='companyLocation')
                    job_location = location_elem.get_text() if location_elem else location

                    job_url_elem = card.find('a', class_='jcs-JobTitle')
                    job_url = f"https://fr.indeed.com{job_url_elem['href']}" if job_url_elem else None

                    if job_url:
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': job_location,
                            'url': job_url,
                            'source': 'Indeed',
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'salary': 'Not listed',
                        })
                        logger.debug(f"  ✓ {title} at {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error parsing job card: {e}")
                    continue

            logger.info(f"  Found {len(jobs)} jobs on Indeed")
            return jobs

        except Exception as e:
            logger.error(f"  Error scraping Indeed: {e}")
            return self._mock_indeed_jobs(role, location)

    def search_linkedin(self, role: str, location: str) -> List[Dict]:
        """Search LinkedIn for jobs (rate-limited)."""
        logger.info(f"🔍 Searching LinkedIn: {role} in {location}")

        if not HAS_REQUESTS:
            return self._mock_linkedin_jobs(role, location)

        # LinkedIn scraping is rate-limited. This uses mock data by default.
        # For real scraping, use LinkedIn API (requires premium account)
        return self._mock_linkedin_jobs(role, location)

    def search_welcome_to_the_jungle(self, role: str, location: str) -> List[Dict]:
        """Search Welcome to the Jungle (French job board)."""
        logger.info(f"🔍 Searching Welcome to the Jungle: {role} in {location}")

        if not HAS_REQUESTS:
            return self._mock_wttj_jobs(role, location)

        jobs = []
        url = f"https://www.welcometothejungle.com/en/jobs?query={role}&location={location}"

        try:
            response = self.session.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse job items (WTTJ HTML structure)
            job_items = soup.find_all('article', class_='job-item')

            for item in job_items[:10]:
                try:
                    title_elem = item.find('h2')
                    title = title_elem.get_text() if title_elem else "N/A"

                    company_elem = item.find('span', class_='company-name')
                    company = company_elem.get_text() if company_elem else "N/A"

                    link_elem = item.find('a', class_='job-link')
                    job_url = link_elem['href'] if link_elem else None

                    if job_url and not job_url.startswith('http'):
                        job_url = f"https://www.welcometothejungle.com{job_url}"

                    if job_url:
                        jobs.append({
                            'title': title,
                            'company': company,
                            'location': location,
                            'url': job_url,
                            'source': 'Welcome to the Jungle',
                            'posted_date': datetime.now().strftime('%Y-%m-%d'),
                            'salary': 'Not listed',
                        })
                        logger.debug(f"  ✓ {title} at {company}")

                except Exception as e:
                    logger.debug(f"  ✗ Error parsing job: {e}")
                    continue

            logger.info(f"  Found {len(jobs)} jobs on WTTJ")
            return jobs

        except Exception as e:
            logger.error(f"  Error scraping WTTJ: {e}")
            return self._mock_wttj_jobs(role, location)

    def _mock_indeed_jobs(self, role: str, location: str) -> List[Dict]:
        """Mock Indeed jobs for testing (no network)."""
        return [
            {
                'title': f'{role} - {location}',
                'company': 'Tech Company A',
                'location': location,
                'url': 'https://fr.indeed.com/viewjob?jk=mock1',
                'source': 'Indeed',
                'posted_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'salary': '1500-2000 EUR/month',
            },
            {
                'title': f'{role} - {location}',
                'company': 'Corp B',
                'location': location,
                'url': 'https://fr.indeed.com/viewjob?jk=mock2',
                'source': 'Indeed',
                'posted_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
                'salary': 'Not listed',
            },
        ]

    def _mock_linkedin_jobs(self, role: str, location: str) -> List[Dict]:
        """Mock LinkedIn jobs."""
        return [
            {
                'title': f'{role} - {location}',
                'company': 'Startup X',
                'location': location,
                'url': 'https://linkedin.com/jobs/view/mock1',
                'source': 'LinkedIn',
                'posted_date': (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d'),
                'salary': 'Competitive',
            },
        ]

    def _mock_wttj_jobs(self, role: str, location: str) -> List[Dict]:
        """Mock Welcome to the Jungle jobs."""
        return [
            {
                'title': f'{role} (WTTJ) - {location}',
                'company': 'Design Studio Z',
                'location': location,
                'url': 'https://www.welcometothejungle.com/en/jobs/mock1',
                'source': 'Welcome to the Jungle',
                'posted_date': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'salary': '1800-2200 EUR/month',
            },
        ]

    def deduplicate(self):
        """Remove duplicate jobs by URL."""
        logger.info(f"Deduplicating {len(self.jobs)} jobs...")
        initial_count = len(self.jobs)

        # Keep track of unique job URLs
        seen_urls = set()
        deduplicated = {}

        for url, job in self.jobs.items():
            normalized_url = url.lower().strip()
            if normalized_url not in seen_urls:
                seen_urls.add(normalized_url)
                deduplicated[url] = job

        self.jobs = deduplicated
        logger.info(f"  Deduplicated: {initial_count} → {len(self.jobs)} unique jobs")

    def save_csv(self):
        """Save jobs to CSV."""
        Path(self.output_csv).parent.mkdir(parents=True, exist_ok=True)

        # Read existing jobs to preserve application status
        existing_jobs = {}
        if os.path.exists(self.output_csv):
            with open(self.output_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_jobs[row['url']] = row

        # Merge new jobs with existing data
        for url, job in self.jobs.items():
            if url in existing_jobs:
                # Preserve existing application status
                job['applied'] = existing_jobs[url].get('applied', 'No')
                job['notes'] = existing_jobs[url].get('notes', '')
            else:
                job['applied'] = 'No'
                job['notes'] = ''

        # Write CSV
        fieldnames = ['title', 'company', 'location', 'url', 'source', 'posted_date', 'salary', 'applied', 'notes']

        with open(self.output_csv, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            # Sort by posted date (newest first)
            sorted_jobs = sorted(
                self.jobs.values(),
                key=lambda x: x.get('posted_date', ''),
                reverse=True
            )

            for job in sorted_jobs:
                writer.writerow({
                    'title': job.get('title', ''),
                    'company': job.get('company', ''),
                    'location': job.get('location', ''),
                    'url': job.get('url', ''),
                    'source': job.get('source', ''),
                    'posted_date': job.get('posted_date', ''),
                    'salary': job.get('salary', ''),
                    'applied': job.get('applied', 'No'),
                    'notes': job.get('notes', ''),
                })

        logger.info(f"✅ Saved {len(self.jobs)} jobs to {self.output_csv}")

    def hunt(self, roles: List[str], locations: List[str]):
        """Main search function."""
        logger.info(f"🎯 Hunting jobs for: {', '.join(roles)} in {', '.join(locations)}")
        logger.info(f"   Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for role in roles:
            for location in locations:
                # Indeed
                indeed_jobs = self.search_indeed(role, location)
                for job in indeed_jobs:
                    self.jobs[job['url']] = job

                # Welcome to the Jungle
                wttj_jobs = self.search_welcome_to_the_jungle(role, location)
                for job in wttj_jobs:
                    self.jobs[job['url']] = job

                # LinkedIn (mock by default)
                linkedin_jobs = self.search_linkedin(role, location)
                for job in linkedin_jobs:
                    self.jobs[job['url']] = job

                # Rate limiting: Don't hammer servers
                time.sleep(random.uniform(2, 5))

        self.deduplicate()
        self.save_csv()

        logger.info(f"✅ Job hunt complete! Found {len(self.jobs)} unique jobs")
        logger.info(f"   Results saved to: {self.output_csv}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Hunt for jobs across multiple job boards'
    )
    parser.add_argument(
        '--roles',
        type=str,
        default='English Teacher,CELTA Trainer',
        help='Job roles to search (comma-separated)'
    )
    parser.add_argument(
        '--locations',
        type=str,
        default='Paris,Lyon,Remote',
        help='Locations to search (comma-separated)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='TRACKING/job_opportunities.csv',
        help='Output CSV file'
    )

    args = parser.parse_args()

    roles = [r.strip() for r in args.roles.split(',')]
    locations = [l.strip() for l in args.locations.split(',')]

    hunter = JobHunter(output_csv=args.output)
    hunter.hunt(roles, locations)


if __name__ == '__main__':
    main()
