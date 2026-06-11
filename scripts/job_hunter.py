#!/usr/bin/env python3
"""
job_hunter.py — Daily job search automation
Finds ELT teaching jobs and emails you a summary

Usage:
  pip install python-jobspy requests
  python job_hunter.py

Set up as daily cron:
  0 8 * * * python3 /path/to/job_hunter.py
"""
import os, csv, smtplib, logging
from io import StringIO
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
log = logging.getLogger(__name__)

# --- Config (set via environment variables) ---
SEARCH_TERMS = os.environ.get('JOB_SEARCH', 'ELT teacher, CELTA teacher, English language teacher').split(',')
LOCATIONS    = os.environ.get('JOB_LOCATION', 'Reunion Island, France, Remote').split(',')
EMAIL_TO     = os.environ.get('EMAIL_TO', 'sourovdeb.is@gmail.com')
EMAIL_FROM   = os.environ.get('EMAIL_FROM', '')
EMAIL_PASS   = os.environ.get('EMAIL_PASS', '')
SMTP_HOST    = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT    = int(os.environ.get('SMTP_PORT', '587'))

def search_jobs(search_term: str, location: str) -> list:
    """Search for jobs using JobSpy (pip install python-jobspy)."""
    try:
        from jobspy import scrape_jobs
        jobs = scrape_jobs(
            site_name=['indeed', 'linkedin', 'glassdoor'],
            search_term=search_term.strip(),
            location=location.strip(),
            results_wanted=10,
            hours_old=24,  # only jobs from last 24 hours
            country_indeed='France',
        )
        return jobs.to_dict('records') if len(jobs) > 0 else []
    except ImportError:
        log.warning('python-jobspy not installed. pip install python-jobspy')
        return []
    except Exception as e:
        log.error(f'Job search failed for "{search_term}" in "{location}": {e}')
        return []

def format_email_body(all_jobs: list) -> str:
    if not all_jobs:
        return '<p>No new jobs found today matching your criteria.</p>'

    rows = ''
    for j in all_jobs[:30]:  # max 30 in email
        title   = j.get('title', 'Unknown')
        company = j.get('company', 'Unknown')
        loc     = j.get('location', '')
        url     = j.get('job_url', '#')
        site    = j.get('site', '')
        date_p  = j.get('date_posted', '')
        salary  = j.get('salary_source', '') or ''
        rows += f'''
        <tr>
          <td><a href="{url}">{title}</a></td>
          <td>{company}</td>
          <td>{loc}</td>
          <td>{salary}</td>
          <td>{site}</td>
          <td>{date_p}</td>
        </tr>'''

    return f'''
    <html><body>
    <h2>Daily Job Matches — {date.today().strftime("%d %B %Y")}</h2>
    <p>Found {len(all_jobs)} matching jobs in the last 24 hours.</p>
    <table border="1" cellpadding="6" cellspacing="0" style="border-collapse:collapse;font-family:Arial,sans-serif;font-size:13px;">
      <tr style="background:#f0f0f0;">
        <th>Title</th><th>Company</th><th>Location</th><th>Salary</th><th>Site</th><th>Posted</th>
      </tr>
      {rows}
    </table>
    <hr>
    <p style="font-size:11px;color:grey;">Automated search. Unsubscribe by removing this cron job.</p>
    </body></html>'''

def send_email(subject: str, html_body: str):
    if not EMAIL_FROM or not EMAIL_PASS:
        log.warning('EMAIL_FROM or EMAIL_PASS not set — printing results instead')
        print(html_body)
        return

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = EMAIL_FROM
    msg['To']      = EMAIL_TO
    msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASS)
            server.send_message(msg)
        log.info(f'Email sent to {EMAIL_TO}')
    except Exception as e:
        log.error(f'Failed to send email: {e}')

def save_to_csv(jobs: list, filename: str = None):
    if not jobs: return
    filename = filename or f'jobs_{date.today().isoformat()}.csv'
    keys = ['title', 'company', 'location', 'salary_source', 'job_url', 'site', 'date_posted']
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(jobs)
    log.info(f'Saved {len(jobs)} jobs to {filename}')

if __name__ == '__main__':
    all_jobs = []
    for term in SEARCH_TERMS:
        for location in LOCATIONS:
            log.info(f'Searching: "{term.strip()}" in "{location.strip()}"')
            found = search_jobs(term, location)
            log.info(f'  Found {len(found)} results')
            all_jobs.extend(found)

    # Remove duplicates by URL
    seen = set()
    unique_jobs = []
    for j in all_jobs:
        url = j.get('job_url', '')
        if url and url not in seen:
            seen.add(url)
            unique_jobs.append(j)

    log.info(f'Total unique jobs: {len(unique_jobs)}')
    save_to_csv(unique_jobs)

    subject = f'Daily Job Matches — {len(unique_jobs)} found — {date.today().strftime("%d %b %Y")}'
    body    = format_email_body(unique_jobs)
    send_email(subject, body)
