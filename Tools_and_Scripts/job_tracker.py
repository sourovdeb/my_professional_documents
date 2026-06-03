#!/usr/bin/env python3
"""
Job Application Tracker
Track all job applications and follow-ups
Usage: python job_tracker.py --add "Company" "Position" "Remote" "50000-65000"
       python job_tracker.py --update "Company" --status "Interview scheduled"
       python job_tracker.py --list [pending|interviewed|rejected|offered]
"""

import csv
from pathlib import Path
from datetime import datetime, timedelta
import argparse

TRACKER_FILE = Path(__file__).parent.parent / "Job_Automation" / "job_applications_tracker.csv"

def load_jobs():
    """Load job applications from CSV"""
    if not TRACKER_FILE.exists():
        return []

    jobs = []
    with open(TRACKER_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)
    return jobs

def save_jobs(jobs):
    """Save job applications to CSV"""
    if not jobs:
        return

    fieldnames = [
        'Application_Date', 'Company', 'Position', 'Job_Type', 'Location',
        'Salary_Range', 'Applied_Via', 'Contact_Name', 'Contact_Email',
        'Status', 'Response_Date', 'Follow_Up_Date', 'Interview_Date',
        'Offer_Amount', 'Notes'
    ]

    with open(TRACKER_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(jobs)

def add_job(company, position, location, salary_range, job_type="Full-time", applied_via="Manual"):
    """Add a new job application"""
    jobs = load_jobs()

    new_job = {
        'Application_Date': datetime.now().strftime('%Y-%m-%d'),
        'Company': company,
        'Position': position,
        'Job_Type': job_type,
        'Location': location,
        'Salary_Range': salary_range,
        'Applied_Via': applied_via,
        'Contact_Name': '',
        'Contact_Email': '',
        'Status': 'Applied',
        'Response_Date': '',
        'Follow_Up_Date': '',
        'Interview_Date': '',
        'Offer_Amount': '',
        'Notes': ''
    }

    jobs.append(new_job)
    save_jobs(jobs)

    print(f"✓ Added application to {company} for {position}")
    return new_job

def update_job(company, **updates):
    """Update a job application"""
    jobs = load_jobs()

    for job in jobs:
        if job['Company'].lower() == company.lower():
            for key, value in updates.items():
                if key in job:
                    job[key] = value
            save_jobs(jobs)
            print(f"✓ Updated {company}")
            return job

    print(f"✗ Company '{company}' not found")
    return None

def list_jobs(status=None):
    """List all jobs or filter by status"""
    jobs = load_jobs()

    if status:
        jobs = [j for j in jobs if j['Status'].lower() == status.lower()]

    if not jobs:
        print("No jobs found")
        return

    print(f"\n{'Company':<20} {'Position':<25} {'Status':<15} {'Applied':<12}")
    print("-" * 75)

    for job in jobs:
        company = job['Company'][:20]
        position = job['Position'][:25]
        status = job['Status'][:15]
        date = job['Application_Date']
        print(f"{company:<20} {position:<25} {status:<15} {date:<12}")

    print(f"\nTotal: {len(jobs)} applications")

def follow_ups_due():
    """Show follow-ups due (1 week after application)"""
    jobs = load_jobs()
    today = datetime.now()
    one_week_ago = today - timedelta(days=7)

    due = []
    for job in jobs:
        if job['Status'] == 'Applied' and job['Response_Date'] == '':
            try:
                applied_date = datetime.strptime(job['Application_Date'], '%Y-%m-%d')
                if applied_date <= one_week_ago and job['Follow_Up_Date'] == '':
                    due.append(job)
            except:
                pass

    if not due:
        print("No follow-ups due")
        return

    print(f"\n{len(due)} follow-ups due:")
    print("-" * 60)
    for job in due:
        days_ago = (today - datetime.strptime(job['Application_Date'], '%Y-%m-%d')).days
        print(f"{job['Company']} - {job['Position']}")
        print(f"  Applied: {days_ago} days ago")
        print(f"  Contact: {job['Contact_Email'] or 'No email'}")
        print()

def stats():
    """Show application statistics"""
    jobs = load_jobs()

    if not jobs:
        print("No applications yet")
        return

    total = len(jobs)
    by_status = {}

    for job in jobs:
        status = job['Status']
        by_status[status] = by_status.get(status, 0) + 1

    print(f"\nJob Application Statistics")
    print("-" * 40)
    print(f"Total applications: {total}")

    for status, count in sorted(by_status.items()):
        percentage = (count / total) * 100
        print(f"  {status}: {count} ({percentage:.1f}%)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Job Application Tracker")
    subparsers = parser.add_subparsers(dest='command')

    # Add command
    add_parser = subparsers.add_parser('add', help='Add new application')
    add_parser.add_argument('company', help='Company name')
    add_parser.add_argument('position', help='Position title')
    add_parser.add_argument('location', help='Location (Remote/City)')
    add_parser.add_argument('salary', help='Salary range (e.g., 50000-65000)')
    add_parser.add_argument('--via', default='Manual', help='Applied via')
    add_parser.add_argument('--type', default='Full-time', help='Job type')

    # Update command
    update_parser = subparsers.add_parser('update', help='Update application')
    update_parser.add_argument('company', help='Company name')
    update_parser.add_argument('--status', help='New status')
    update_parser.add_argument('--notes', help='Add notes')
    update_parser.add_argument('--follow-up', help='Set follow-up date')

    # List command
    list_parser = subparsers.add_parser('list', help='List applications')
    list_parser.add_argument('--status', help='Filter by status')

    # Follow-ups command
    subparsers.add_parser('follow-ups', help='Show due follow-ups')

    # Stats command
    subparsers.add_parser('stats', help='Show statistics')

    args = parser.parse_args()

    if args.command == 'add':
        add_job(args.company, args.position, args.location, args.salary, args.type, args.via)
    elif args.command == 'update':
        updates = {}
        if args.status:
            updates['Status'] = args.status
        if args.notes:
            updates['Notes'] = args.notes
        if args.follow_up:
            updates['Follow_Up_Date'] = args.follow_up
        update_job(args.company, **updates)
    elif args.command == 'list':
        list_jobs(args.status)
    elif args.command == 'follow-ups':
        follow_ups_due()
    elif args.command == 'stats':
        stats()
    else:
        # Default: show summary
        stats()
        print()
        follow_ups_due()
