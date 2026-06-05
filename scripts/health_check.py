#!/usr/bin/env python3
"""
health_check.py
Daily WordPress health monitor. Run via cron to catch downtime early.

Cron (runs at 7am daily):
  0 7 * * * /usr/bin/python3 /path/to/health_check.py >> /tmp/wp_health.log 2>&1

Setup:
  pip install requests python-dotenv
  WP_URL in .env or environment
"""

import os, requests, smtplib, datetime
from email.mime.text import MIMEText
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass

WP_URL     = os.getenv('WP_URL', 'https://sourovdeb.com')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_TO   = os.getenv('EMAIL_TO', 'sourovdeb.is@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASSWORD', '')


def check(name, url, expected_status=200):
    try:
        r = requests.get(url, timeout=10)
        ok = r.status_code == expected_status
        return {'name': name, 'ok': ok, 'status': r.status_code, 'detail': ''}
    except Exception as e:
        return {'name': name, 'ok': False, 'status': 0, 'detail': str(e)[:100]}


def run_checks():
    return [
        check('Site reachable',          f'{WP_URL}'),
        check('REST API responding',      f'{WP_URL}/wp-json/wp/v2/posts?per_page=1'),
        check('Custom plugin active',     f'{WP_URL}/wp-json/sourov/v1/status', expected_status=200),
        check('XML sitemap exists',       f'{WP_URL}/sitemap.xml'),
        check('Robots.txt accessible',    f'{WP_URL}/robots.txt'),
    ]


def send_alert(checks):
    failures = [c for c in checks if not c['ok']]
    if not failures:
        print('All checks passed.')
        return

    body = f'WORDPRESS HEALTH ALERT\n{datetime.datetime.now()}\n\n'
    body += 'FAILURES:\n'
    for f in failures:
        body += f"  [{f['status']}] {f['name']}: {f['detail']}\n"
    body += '\nAll checks:\n'
    for c in checks:
        body += f"  {'OK' if c['ok'] else 'FAIL':4} {c['name']}\n"

    print(body)

    if EMAIL_FROM and EMAIL_PASS:
        msg = MIMEText(body)
        msg['Subject'] = f'WP Health Alert — {len(failures)} failure(s) — {WP_URL}'
        msg['From'] = EMAIL_FROM
        msg['To'] = EMAIL_TO
        try:
            with smtplib.SMTP('smtp.zoho.com', 587) as s:
                s.starttls(); s.login(EMAIL_FROM, EMAIL_PASS); s.send_message(msg)
            print('Alert email sent.')
        except Exception as e:
            print(f'Email error: {e}')


if __name__ == '__main__':
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'{ts} — Health check: {WP_URL}')
    checks = run_checks()
    for c in checks:
        print(f"  {'OK' if c['ok'] else 'FAIL':4} | {c['name']}")
    send_alert(checks)
