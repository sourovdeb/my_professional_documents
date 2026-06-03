# Daily Writing & Automation System

Your personal content hub for essays, automation, job hunting, and wellbeing.

---

## 📝 Structure Overview

```
├── Essays_and_Blogs/          # Your daily 500-word writing practice
├── Tools_and_Ideas/           # Scripts, tools, and collection inbox
├── Job_Automation/            # Indeed, LinkedIn, job search bots
├── Health_and_Wellbeing/      # Bipolar/depression management, self-care
├── WordPress_Drafts/          # Staging before WordPress publication
└── Contacts_and_Partnerships/ # Network, collaborators, writers
```

---

## 🎯 Workflow: Write → Stage → Publish

1. **Write** (Essays_and_Blogs/): Daily 500-word essay on designated branch
2. **Stage** (Google Drive sheet): Enter metadata (category, tags, date)
3. **Push**: Commit and push to branch
4. **Publish**: You copy to WordPress via FTP (or deploy.php automation)

---

## 🤖 Automation Available

- `job_monitor.py` - Scrapes Indeed, LinkedIn for jobs matching criteria
- `email_sender.py` - Auto-send networking emails from template
- `blog_publisher.py` - Direct WordPress publish via deploy.php
- `daily_prompt.py` - Sends you writing prompts daily

---

## 💊 Health-First Approach

All workflows include:
- **Consistency checkpoints** (Did you write today? Take meds?)
- **Energy tracking** (Rate 1-10 daily)
- **Burnout prevention** (Auto-pause if stress > threshold)
- **Backup systems** (If you miss a day, catch-up prompts available)

---

## 🔐 Credentials & Security

**NEVER commit FTP/DB passwords to repo.**

Store in:
- `.env.local` (git-ignored)
- OS credential manager
- Pass reference to credentials via environment variables

Credentials referenced:
```
WORDPRESS_FTP_HOST=ftp.sourovdeb.com
WORDPRESS_FTP_USER=u839078121.sourov
WORDPRESS_DEPLOY_KEY=0767044896thevenet_ (in .env.local only)
```

---

## 📅 Branch Strategy

Each writing session gets its own branch:
```
essays/2026-06-03-mental-health
essays/2026-06-04-automation-tools
automation/job-scraper-v2
tools/email-templates-v1
```

Then merge/PR to `main` when ready.

---

## 📊 Google Drive Integration

Spreadsheet: https://docs.google.com/spreadsheets/d/1fJX0yZNe0tjrQ1YZU0iP0kLWU0r3qwx6-J2ODAUGRIE/edit

Columns:
- Date | Title | Category | Tags | Status | WordPress_ID | Branch

Use this as your staging area before final publication.

---

## 🎓 Quality Standards

- ✅ Active voice, not passive
- ✅ Research from official/legal sources only
- ✅ 500 words target (essays)
- ✅ Token-efficient writing
- ✅ Personalized to your health context
- ✅ Short essays over long ones
- ✅ Reusable tools and scripts

---

## 🚀 Quick Start

1. Create new branch: `git checkout -b essays/YYYY-MM-DD-topic`
2. Use essay template: `Essays_and_Blogs/TEMPLATE.md`
3. Write 500 words on your topic
4. Update Google Drive sheet with metadata
5. Commit: `git add . && git commit -m "Essay: [topic]"`
6. Push: `git push -u origin essays/YYYY-MM-DD-topic`
7. Copy to WordPress manually (or use automation script)

---

## 📚 Next: Build Each Section

See subdirectory READMEs for:
- Essays_and_Blogs/ → Writing guide & templates
- Tools_and_Ideas/ → Collecting & organizing resources
- Job_Automation/ → Job search automation setup
- Health_and_Wellbeing/ → Tracking & self-care
- WordPress_Drafts/ → Publishing workflow
