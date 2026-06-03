#!/usr/bin/env python3
"""
Indeed Job Scraper & Tracker
Finds jobs matching your profile and logs them to CSV for tracking

Usage:
    python3 indeed_scraper.py --search "English Teacher" --location "France" --limit 25

Requires:
    pip install requests beautifulsoup4 pandas
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import os
import sys
import argparse
import time

class IndeedScraper:
    def __init__(self, search_query, location="France", limit=25):
        self.search_query = search_query
        self.location = location
        self.limit = limit
        self.base_url = "https://www.indeed.fr/jobs"
        self.jobs = []
        self.csv_file = f"jobs_tracked_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    def search(self):
        """Scrape Indeed for jobs"""
        params = {
            'q': self.search_query,
            'l': self.location,
            'limit': min(self.limit, 50)  # Indeed limits per page
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        print(f"🔍 Searching Indeed for: '{self.search_query}' in {self.location}")
        print(f"   URL: {self.base_url}?q={params['q']}&l={params['l']}")

        try:
            response = requests.get(self.base_url, params=params, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            job_cards = soup.find_all('div', class_='job_seen_beacon')

            if not job_cards:
                print("⚠️  No jobs found. Try different search terms.")
                return

            print(f"✓ Found {len(job_cards)} job listings")

            for idx, card in enumerate(job_cards[:self.limit], 1):
                try:
                    job = self._extract_job_info(card, idx)
                    if job:
                        self.jobs.append(job)
                except Exception as e:
                    print(f"  ⚠️  Skipped job {idx}: {str(e)[:50]}")
                    continue

            print(f"✓ Extracted {len(self.jobs)} jobs successfully")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Indeed: {e}")
            sys.exit(1)

    def _extract_job_info(self, card, index):
        """Extract job details from HTML card"""
        try:
            # Title
            title_elem = card.find('h2', class_='jobTitle')
            title = title_elem.get_text(strip=True) if title_elem else None

            # Company
            company_elem = card.find('span', class_='companyName')
            company = company_elem.get_text(strip=True) if company_elem else None

            # Location
            location_elem = card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else None

            # Job URL
            link_elem = card.find('a', class_='jcs-JobTitle')
            url = 'https://www.indeed.fr' + link_elem['href'] if link_elem else None

            # Salary (if available)
            salary_elem = card.find('span', class_='salary-snippet')
            salary = salary_elem.get_text(strip=True) if salary_elem else 'Not listed'

            # Job type
            jobtype_elem = card.find('span', class_='jobType')
            job_type = jobtype_elem.get_text(strip=True) if jobtype_elem else 'Unknown'

            # Posted date
            date_elem = card.find('span', class_='date')
            posted = date_elem.get_text(strip=True) if date_elem else 'Unknown'

            return {
                'index': index,
                'title': title,
                'company': company,
                'location': location,
                'job_type': job_type,
                'salary': salary,
                'posted': posted,
                'url': url,
                'scraped_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'status': 'new',  # Track application status
                'notes': ''
            }
        except Exception as e:
            raise e

    def save_to_csv(self):
        """Save jobs to CSV"""
        if not self.jobs:
            print("No jobs to save.")
            return

        df = pd.DataFrame(self.jobs)
        df.to_csv(self.csv_file, index=False, encoding='utf-8')
        print(f"✓ Saved to: {self.csv_file}")
        return self.csv_file

    def save_to_json(self):
        """Save jobs to JSON"""
        json_file = self.csv_file.replace('.csv', '.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.jobs, f, ensure_ascii=False, indent=2)
        print(f"✓ Saved to: {json_file}")
        return json_file

    def print_summary(self):
        """Print summary of jobs found"""
        if not self.jobs:
            print("No jobs found.")
            return

        print("\n" + "="*80)
        print(f"📊 Job Summary: {len(self.jobs)} positions found")
        print("="*80 + "\n")

        for job in self.jobs:
            print(f"#{job['index']} - {job['title']}")
            print(f"   Company: {job['company']}")
            print(f"   Location: {job['location']}")
            print(f"   Salary: {job['salary']}")
            print(f"   Type: {job['job_type']}")
            print(f"   Posted: {job['posted']}")
            print(f"   Link: {job['url']}")
            print()

    def apply_filters(self, filters=None):
        """Filter jobs by criteria"""
        if not filters:
            return self.jobs

        filtered = self.jobs.copy()

        if filters.get('exclude_keywords'):
            keywords = filters['exclude_keywords'].lower().split(',')
            filtered = [j for j in filtered if not any(k in j['title'].lower() for k in keywords)]

        if filters.get('min_salary'):
            # This is simplified—real salary extraction would be complex
            filtered = [j for j in filtered if j['salary'] != 'Not listed']

        print(f"✓ Filtered from {len(self.jobs)} to {len(filtered)} jobs")
        return filtered


def main():
    parser = argparse.ArgumentParser(
        description='Scrape Indeed for jobs and save to CSV/JSON'
    )
    parser.add_argument('--search', required=True, help='Job search query (e.g., "English Teacher")')
    parser.add_argument('--location', default='France', help='Location (default: France)')
    parser.add_argument('--limit', type=int, default=25, help='Max jobs to scrape (default: 25)')
    parser.add_argument('--format', choices=['csv', 'json', 'both'], default='csv', help='Output format')

    args = parser.parse_args()

    scraper = IndeedScraper(args.search, args.location, args.limit)
    scraper.search()
    scraper.print_summary()

    if args.format in ['csv', 'both']:
        scraper.save_to_csv()
    if args.format in ['json', 'both']:
        scraper.save_to_json()

    print("\n✓ Next step: Update the CSV with your application status!")
    print("  - Change 'status' column: new → applied → interviewed → rejected → hired")
    print("  - Add notes for follow-up")


if __name__ == '__main__':
    main()
