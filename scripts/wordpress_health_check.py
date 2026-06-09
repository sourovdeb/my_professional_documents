#!/usr/bin/env python3
"""
wordpress_health_check.py
Audits your WordPress site and reports on post quality, categories, tags, SEO.

Usage:
  python wordpress_health_check.py              # print report
  python wordpress_health_check.py --json       # output JSON
  python wordpress_health_check.py --email      # send report by email

Environment: WP_URL, WP_USER, WP_APP_PASSWORD, SMTP_USER, SMTP_PASSWORD, EMAIL_TO
"""

import os
import json
import smtplib
import argparse
import requests
from datetime import datetime
from email.mime.text import MIMEText

WP_URL  = os.environ.get('WP_URL', 'https://sourovdeb.com').rstrip('/')
WP_AUTH = (os.environ.get('WP_USER', ''), os.environ.get('WP_APP_PASSWORD', ''))


def get_posts(status='any', per_page=100) -> list:
    resp = requests.get(f'{WP_URL}/wp-json/wp/v2/posts',
                        params={'per_page': per_page, 'status': status},
                        auth=WP_AUTH, timeout=30)
    return resp.json() if resp.ok else []


def get_site_info() -> dict:
    resp = requests.get(f'{WP_URL}/wp-json', timeout=15)
    return resp.json() if resp.ok else {}


def analyse_posts(posts: list) -> dict:
    total = len(posts)
    no_tags       = [p for p in posts if not p.get('tags')]
    uncategorized = [p for p in posts if p.get('categories', [1]) == [1]]
    no_excerpt    = [p for p in posts if not (p.get('excerpt') or {}).get('rendered', '').strip()]
    published     = [p for p in posts if p.get('status') == 'publish']
    drafts        = [p for p in posts if p.get('status') == 'draft']
    scheduled     = [p for p in posts if p.get('status') == 'future']

    # Word count estimate
    def word_count(p):
        text = (p.get('content') or {}).get('rendered', '')
        return len(text.split())

    short_posts = [p for p in published if word_count(p) < 200]

    return {
        'total': total,
        'published': len(published),
        'drafts': len(drafts),
        'scheduled': len(scheduled),
        'no_tags': len(no_tags),
        'uncategorized': len(uncategorized),
        'no_excerpt': len(no_excerpt),
        'short_posts_under_200w': len(short_posts),
        'health_score': _health_score(total, len(no_tags), len(uncategorized)),
        'posts_needing_tags': [p['title']['rendered'][:60] for p in no_tags[:10]],
        'posts_uncategorized': [p['title']['rendered'][:60] for p in uncategorized[:10]],
    }


def _health_score(total, no_tags, uncategorized) -> str:
    if total == 0:
        return 'N/A'
    score = 100
    score -= min(40, int((no_tags / total) * 40))
    score -= min(30, int((uncategorized / total) * 30))
    if score >= 85: return f'GOOD ({score}/100)'
    if score >= 60: return f'NEEDS WORK ({score}/100)'
    return f'POOR ({score}/100)'


def format_report(site: dict, analysis: dict) -> str:
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    lines = [
        f'WordPress Health Report — {ts}',
        f'Site: {WP_URL}',
        f'WP Version: {site.get("generator", "Unknown")}',
        '',
        f'POSTS SUMMARY',
        f'  Total posts:     {analysis["total"]}',
        f'  Published:       {analysis["published"]}',
        f'  Drafts:          {analysis["drafts"]}',
        f'  Scheduled:       {analysis["scheduled"]}',
        '',
        f'QUALITY ISSUES',
        f'  No tags:                 {analysis["no_tags"]}',
        f'  Uncategorized:           {analysis["uncategorized"]}',
        f'  No excerpt:              {analysis["no_excerpt"]}',
        f'  Short posts (<200 words): {analysis["short_posts_under_200w"]}',
        '',
        f'HEALTH SCORE: {analysis["health_score"]}',
        '',
    ]
    if analysis['posts_needing_tags']:
        lines.append('Posts needing tags (first 10):')
        for t in analysis['posts_needing_tags']:
            lines.append(f'  - {t}')
        lines.append('')
    if analysis['posts_uncategorized']:
        lines.append('Uncategorized posts (first 10):')
        for t in analysis['posts_uncategorized']:
            lines.append(f'  - {t}')
        lines.append('')
    lines.append('To fix: python scripts/wordpress_category_tag_fix.py')
    return '\n'.join(lines)


def send_email(body: str):
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_pass = os.environ.get('SMTP_PASSWORD', '')
    email_to  = os.environ.get('EMAIL_TO', smtp_user)
    if not smtp_user:
        print('No SMTP_USER set. Cannot send email.')
        return
    msg = MIMEText(body)
    msg['Subject'] = f'WP Health Report — {datetime.now().strftime("%Y-%m-%d")}'
    msg['From']    = smtp_user
    msg['To']      = email_to
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)
    print(f'Report sent to {email_to}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='WordPress health check')
    parser.add_argument('--json',  action='store_true')
    parser.add_argument('--email', action='store_true')
    args = parser.parse_args()

    print('Fetching site data...')
    site  = get_site_info()
    posts = get_posts()
    analysis = analyse_posts(posts)

    if args.json:
        print(json.dumps(analysis, indent=2))
    else:
        report = format_report(site, analysis)
        print(report)
        if args.email:
            send_email(report)
