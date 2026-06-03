# Automation Scripts

Free, open source automation for Sourov's writing and job search workflow.

## Scripts

### `job_search_automation.py`
Searches Indeed RSS for teaching, hospitality and writing jobs. Sends a daily digest email.

**Setup:**
```bash
pip install requests beautifulsoup4 feedparser
export GMAIL_APP_PASSWORD="your-gmail-app-password"
python job_search_automation.py
```
**Automate daily:** Add to cron: `0 8 * * * cd /path && python job_search_automation.py`

---

### `wordpress_draft_publisher.py`
Reads all `.md` files from `blog_drafts/` and pushes them as draft posts to WordPress.

**Setup:**
```bash
pip install requests markdown python-frontmatter
# In WordPress Admin → Users → Profile → Application Passwords → Create one
export WP_USER="your-wp-username"
export WP_APP_PASSWORD="xxxx xxxx xxxx xxxx xxxx xxxx"
python wordpress_draft_publisher.py --dry-run  # test first
python wordpress_draft_publisher.py            # publish drafts
```

---

### `partner_finder.py`
Searches Medium and Substack for like-minded writers: mental health, neurodiversity, language, diaspora.

**Setup:**
```bash
pip install requests feedparser beautifulsoup4
python partner_finder.py
# Results saved to partner_search_results.json
```

---

## Tools Stack (All Free/Open Source)

| Tool | Purpose | Cost |
|------|---------|------|
| [n8n](https://n8n.io) | Workflow automation (self-hosted) | Free |
| [Obsidian](https://obsidian.md) | Writing + notes (local files) | Free |
| [Goblin Tools](https://goblin.tools) | Break tasks into micro-steps | Free |
| [LanguageTool](https://languagetool.org) | Multilingual grammar check | Free tier |
| [Tiimo](https://tiimo.app) | Visual daily planner for ADHD | Free tier |
| [Forest](https://forestapp.cc) | Focus timer | Free tier |
| [Otter.ai](https://otter.ai) | Speech-to-text drafting | Free tier |
| [Hemingway Editor](https://hemingwayapp.com) | Clarity / active voice check | Free (browser) |
| [Leantime](https://leantime.io) | ADHD-friendly project management | Free + open source |

## Cron Schedule (Suggested)

```cron
# Job search — every morning at 8am
0 8 * * * cd ~/automation && python job_search_automation.py

# Partner finder — every Sunday
0 9 * * 0 cd ~/automation && python partner_finder.py

# WordPress publisher — manual only (review before publishing)
# Run: python wordpress_draft_publisher.py --dry-run
```
