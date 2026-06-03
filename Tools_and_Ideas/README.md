# Tools & Ideas Inbox

A collection system for scripts, open-source tools, automation ideas, and resources you discover.

---

## 🎯 Purpose

Instead of losing tools and ideas, capture them here:
- Open-source tools (automation, writing, job search)
- Scripts you want to build or adapt
- Service recommendations
- Automation ideas
- Best practices
- Partner/collaborator ideas

---

## 📂 Structure

```
Tools_and_Ideas/
├── README.md (this file)
├── OPEN_SOURCE_TOOLS.md        # Curated list of free tools
├── AUTOMATION_IDEAS.md          # Scripts to build or adapt
├── WRITING_TOOLS.md             # Apps for writing/blogging
├── JOB_SEARCH_RESOURCES.md      # Job sites, newsletters, tools
├── CONTACTS_AND_PARTNERSHIPS.md # People/projects to collab on
├── SCRIPTS/                     # Reusable Python scripts
│   ├── email_template_gen.py
│   ├── wordpress_publisher.py
│   └── daily_prompt_generator.py
└── Collections/
    ├── 2026-06-mental-health-tools.md
    └── 2026-06-automation-favorites.md
```

---

## 🔧 Open Source Tools (Free & Privacy-First)

### Writing & Blogging
| Tool | Purpose | Link | Cost | Notes |
|------|---------|------|------|-------|
| **Obsidian** | Local markdown notes | obsidian.md | Free (optional sync) | Best for personal wiki, works offline |
| **Logseq** | Outlining & daily notes | logseq.com | Free, open-source | Graph-based, good for non-linear thinking |
| **Joplin** | Note sync across devices | joplinapp.org | Free, self-hosted | End-to-end encrypted |
| **Typora** | Minimal markdown editor | typora.io | $14.99 (one-time) | Clean, fast, export to Word/PDF/HTML |
| **VS Code + Markdown Preview** | Free markdown editor | code.visualstudio.com | Free | Lightweight, integrates with git |

### Job Automation & Scraping
| Tool | Purpose | Link | Cost | Setup Time |
|------|---------|------|------|-----------|
| **Selenium** | Web scraping Python lib | selenium.dev | Free, open-source | 2-3 hours |
| **BeautifulSoup** | HTML parsing | beautifulsoup4 | Free, open-source | 1 hour |
| **Scrapy** | Full scraping framework | scrapy.org | Free, open-source | 4-6 hours (learning curve) |
| **N8N** | No-code automation | n8n.io | Free (self-hosted) | 1 hour to set up |
| **Zapier** | No-code automation | zapier.com | Paid ($20+/mo) | 15 min |

### Email Automation
| Tool | Purpose | Link | Cost | Notes |
|------|---------|------|------|-------|
| **Gmail API** | Send emails via Python | developers.google.com | Free | Requires OAuth2 setup |
| **Mailgun** | Email sending service | mailgun.com | Free tier (600/day) | Good for automation |
| **SendGrid** | Email delivery | sendgrid.com | Free tier (100/day) | Reliable, well-documented |

### WordPress Automation
| Tool | Purpose | Link | Cost | Notes |
|------|---------|------|------|-------|
| **WordPress REST API** | Publish posts via code | developer.wordpress.org | Free, built-in | Your deploy.php uses this concept |
| **WP-CLI** | Command-line WordPress | wp-cli.org | Free, open-source | Powerful, learning curve |
| **Zapier/N8N → WordPress** | Connect tools to WordPress | zapier.com | Free tier available | Low-code solution |

### Privacy & Security
| Tool | Purpose | Link | Cost | Notes |
|------|---------|------|------|-------|
| **Bitwarden** | Password manager | bitwarden.com | Free (self-hosted) | Open-source, secure |
| **ProtonMail** | Encrypted email | protonmail.com | Free/paid | Privacy-first |
| **.env files** | Local credential storage | (built-in) | Free | Never commit .env files |

---

## 💡 Automation Ideas to Build

### Priority 1: Ready to Build Now
1. **Blog Auto-Publisher** (`wordpress_publisher.py`)
   - Read markdown from Essays_and_Blogs/
   - Create WordPress post via REST API (or deploy.php)
   - Auto-categorize based on filename/tags
   - ~100 lines of Python

2. **Daily Writing Prompt Generator** (`daily_prompt.py`)
   - Sends you a writing prompt via email
   - Mix of mental health, career, and philosophy topics
   - Runs via cron daily at 7am
   - ~50 lines of Python

3. **Job Application Tracker Dashboard** (`tracker_dashboard.html`)
   - Simple HTML/CSS dashboard
   - Reads job_tracker.csv
   - Shows: applications by status, salary trends, response rates
   - Updates daily
   - ~200 lines HTML/JS

### Priority 2: If You Have Time
4. **LinkedIn Auto-Notifier** (`linkedin_monitor.py`)
   - Monitors job search results weekly
   - Sends email digest
   - Detects roles matching your criteria
   - Uses Selenium for scraping (LinkedIn blocks API)

5. **Mental Health Habit Reminder** (`wellness_reminder.py`)
   - Sends SMS/email reminders
   - "Did you take meds?" "Have you moved today?"
   - Tracks streak (consecutive days of habit)
   - Celebrates wins

6. **Google Drive → GitHub Sync** (`gdrive_sync.py`)
   - Reads Google Drive spreadsheet (job applications)
   - Syncs to this repo as CSV
   - One-way sync (Google Drive is source of truth)
   - Keeps your tracking in one place

### Priority 3: Nice to Have
7. **Email Template Generator** (`email_template_gen.py`)
   - Input: company name, job title, your skills
   - Output: 3 personalized cold email templates
   - Saves in Job_Automation/templates/

8. **Salary Research Bot** (`salary_tracker.py`)
   - Scrapes Glassdoor, PayScale for salary data
   - Tracks by job title, location, experience
   - Generates monthly salary report

---

## 📚 Writing Tools Tested & Recommended

**For Daily 500-Word Essays**:
- ✅ **Obsidian** → write in markdown, sync via git
- ✅ **Typora** → minimal, no distractions, exports easily
- ✅ **VS Code** → if you want git integration + markdown

**For Blog Publishing**:
- ✅ **WordPress** (your site) → via REST API or deploy.php
- ✅ **Medium** → reach wider audience, but less control
- ✅ **Dev.to** → tech community, good for teaching content

**For Scheduling**:
- ✅ **Google Calendar** → simple scheduling
- ✅ **Notion** → templates, databases (overkill for essays)

---

## 🌐 Job Search Resources

### Job Boards
- **Indeed** → largest US board, good for remote
- **LinkedIn Jobs** → network + jobs combined
- **Remote.co** → remote-only jobs
- **FlexJobs** → vetted remote jobs (paid tier)
- **We Work Remotely** → quality remote jobs
- **Teaching Jobs**:
  - Dave's ESL Cafe (teaching.com)
  - International Schools Review (isreview.org)
  - TeachingEnglishAbroad (tefl.com)

### Newsletters (Curated Job Alerts)
- **Remote.co newsletter** (weekly)
- **NoCodeList** (automation tools)
- **Hacker News** (tech jobs)
- **LinkedIn Newsletter** (personalized)

### Salary Research
- **Glassdoor** → employee reviews + salary
- **PayScale** → salary by role, location, experience
- **Indeed Salary** → aggregated data
- **Levels.fyi** → tech industry salaries

---

## 👥 Contacts & Partnerships

### People to Connect With
Track here:
- Potential collaborators
- Writers in your niche
- Hiring managers
- Mentors
- Peers with bipolar/mental health (for solidarity)

**Template**:
```
Name: [Full name]
Title/Role: [What do they do?]
LinkedIn/Email: [Contact]
Common ground: [Why connect?]
Status: Not contacted / Emailed / Following up / Connected
Next step: [What's the ask?]
```

### Potential Projects to Collaborate On
- Writing group for mental health awareness
- Open-source tool for bipolar tracking
- Podcast: "Teaching English While Bipolar"
- Blog series on remote work + mental health
- Job automation tool for neurodivergent folks

---

## 📋 How to Use This System

### Adding a Tool
1. Find a tool you like
2. Add to relevant file (OPEN_SOURCE_TOOLS.md, etc.)
3. Include: name, link, cost, brief review
4. If you use it, document how in a separate file

### Capturing an Idea
1. Create `Ideas/2026-06-03-idea-title.md`
2. Describe: what's the problem? what solves it? how would you build it?
3. Estimate time and complexity
4. Link to any tools that could help

### Building a Script
1. Create in `Scripts/` directory
2. Add docstring with: purpose, requirements, usage example
3. Keep it reusable (use config files, not hard-coded values)
4. Document in README

---

## 🔄 Collections (Theme-Based)

Create monthly collections of tools/ideas relevant to what you're working on:

**June 2026 - Mental Health Automation**:
```
- Tools that help bipolar tracking
- Scripts for wellness reminders
- Blog ideas about mental health + tech
- Researchers/authors to learn from
```

---

## 📈 Recycling & Reuse

**Key principle**: Don't reinvent. Reuse proven tools and scripts.

When you write a script:
- Document it here
- Make it configurable (not hard-coded)
- Test it once, use it many times
- Update this README when you create something useful

---

## 🚀 Start This Week

1. Go through **OPEN_SOURCE_TOOLS.md** and install 1-2 tools you like
2. Add 3 automation ideas to **AUTOMATION_IDEAS.md** (even if you don't build them now)
3. Create `Contacts_and_Partnerships.md` with 5 people you want to connect with
4. Save 1 tool or script you discover in Slack/email to the relevant file

---

**Goal**: This becomes your personal toolkit and idea repository. Over time, you'll have reusable scripts, proven tools, and a network. That's exposure, consistency, and leverage.**
