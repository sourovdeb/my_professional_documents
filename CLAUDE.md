# Migration Law Microblog — Policy Updates Hub

## Project Summary
Publish timely, accurate updates about migration law and policy changes on your website. Short-form posts summarizing legislative changes, case law, guidance, and practical implications for France, EU, Australia, and Canada—especially refugee options and marriage visas.

## Goals
- Keep Europeans informed of migration law changes
- Surface policy updates that affect asylum seekers, marriage visa applicants, and skilled migrants
- Provide plain-language summaries with actionable checklists
- Help poor and talented people navigate immigration options
- Establish authoritative, legally reviewed content

## Target Audience
- Europeans seeking migration opportunities (Australia, Canada, EU)
- Asylum seekers and refugees within EU
- Marriage visa applicants
- Skilled migrants evaluating options

## Key Initiatives

### 1. First Post & Legal Review
- Draft inaugural post on recent migration law changes
- Plain-language summary (250–400 words)
- Include authoritative source links (government, statutory instruments)
- Get reviewed by immigration lawyer for accuracy & liability

**Status:** Draft due week of July 7

### 2. Content Infrastructure
- Create "What this means for applicants" template
- Create "Practical checklist" template
- Enable rapid publishing when laws change
- Set up disclaimer: informational only, not legal advice

**Status:** Templates to be drafted

### 3. Monitoring & Updates
- Subscribe to official government change alerts (France, EU, Australia, Canada)
- Check weekly for migration law updates
- Maintain editorial calendar with review checkpoints
- Publish at least 1–2 posts per month

**Status:** Monitoring routine to be established

### 4. Analytics & Feedback
- Track post metrics (views, shares, clicks on official links)
- Report findings monthly
- Iterate content based on engagement

**Status:** Analytics setup pending

## Folder Structure
```
my_professional_documents/
├── CLAUDE.md
├── microblog/
│   ├── posts/                    # Published posts archive
│   │   ├── 2026-07-post-001.md
│   │   └── ...
│   ├── drafts/                   # In-review posts
│   ├── templates.md              # Reusable post templates
│   ├── sources.md                # Authoritative source links
│   ├── editorial-calendar.md     # Publishing schedule
│   └── metrics.md                # Engagement tracking
├── legal/
│   ├── disclaimer.md             # Website disclaimer text
│   ├── review-process.md         # Legal review workflow
│   └── liability-notes.md        # Legal considerations
└── monitoring/
    ├── feeds.md                  # Government alert subscriptions
    ├── sources.md                # News & policy sources
    └── alerts-log.md             # Weekly scan log
```

## Immediate Next Steps (Week 1)
- [ ] Draft first post on recent migration law changes
- [ ] Compile authoritative source list (official URLs)
- [ ] Schedule legal review with immigration lawyer
- [ ] Design post templates ("What this means", "Checklist")
- [ ] Set up government alert subscriptions

## Key Content Areas
**France & EU:** Asylum policy, family reunification, refugee resettlement, residence permits, recent court rulings

**Australia & Canada:** Points-based migration, skilled worker visas, family sponsorship, humanitarian intake

**All:** Marriage/partner visas, children in migration, digital nomad visas, recent legislative changes

## Timeline
- **Week 1 (Jul 7):** Draft first post, source list, legal review
- **Week 2 (Jul 14):** Publish first post, templates ready
- **Week 3 (Jul 21):** Set up monitoring, editorial calendar
- **Ongoing:** 1–2 posts per month, weekly monitoring scan

## Definition of Done
- [ ] First post published (legally reviewed)
- [ ] Templates standardized for rapid publishing
- [ ] Government alert subscriptions active
- [ ] Editorial calendar established with review checkpoints
- [ ] Analytics tracking configured
- [ ] Disclaimer & legal text visible on site
# Claude Code Workflow: my_professional_documents

## Overview
This repository stores personal and professional content that feeds into sourovdeb.com via an automated WordPress sync.

## Content Sync to WordPress

### How it works
- **Script**: `wordpress_integration/sync_verification.py` (scheduled hourly or on-demand)
- **Auth**: WordPress REST API with `X-Sourov-Key` header
- **Endpoint**: `https://sourovdeb.com/wp-json/sourov/v1/ai-post`
- **Output**: Draft posts on WordPress (never auto-published)
- **Dedup**: Checks title against existing posts; skips exact matches
- **Batch size**: Up to 5 new drafts per run
- **Categories**: Mental Health, ELT Masterclass, English Teaching, Philosophy, Photography, Software, DXO, Learn AI in Mistral Studio

### API contract (important)
```python
POST /wp-json/sourov/v1/ai-post
Authorization: X-Sourov-Key: [key]
{
    "title": "string",
    "content": "string (markdown or HTML)",
    "status": "draft",
    "category": "string",
    "tags": ["array", "of", "tags"]  # MUST be JSON array, not string
}
```

**Critical bug fixed (2026-07-19)**: Tags field must be JSON array (`["tag"]`), not string (`"tag"`). Old scripts used string format and got HTTP 500.

### Content that gets synced
**Included** (automatically scanned):
- `blog_and_essays/` — essays and blog posts
- `daily_essays/` — reflections
- `posts/` — article drafts
- `guides/` — how-to and reference guides
- `AI_Lessons/`, `AI_Term_Lessons/` — AI learning material
- `CELTA_Teaching_Materials/` — English teaching content
- `presentations/`, `Presentations/` — slide decks and talks
- `Growth_Hub/`, `initiatives/` — project write-ups
- `weekly-briefings/` — trend reports and analysis

**Excluded** (not scanned):
- `Biography_and_Medical/`, `Legal_Documents/`, `therapy_and_wellbeing/`, `Story_of_Sourov/`
- `credentials/`, `tools/`, `scripts/`, `automation/`, `templates/`
- `_archive/`, `*_archive/`, `*_extracted/`
- `.github/`, `docs/`

### Running the sync manually
```bash
python3 wordpress_integration/sync_verification.py
```

### Known issues
1. **Shallow dedup window**: `GET /scheduled` returns 50 posts max. Older published items aren't detected. Recommend WordPress audit.
2. **No delete endpoint**: Test drafts must be deleted from WordPress admin manually.
3. **Post ID not returned**: API returns `200 OK` but no `post_id` in response.

### Session history
- **2026-07-19 06:32 UTC**: First sync, pushed 5 before session ended
- **2026-07-19 09:40 UTC**: Resumed, pushed 26 more (23 main + 3 flagged)
- **2026-07-19 ongoing**: Aggressive push from skipped directories
- **2026-07-21 12:40 UTC**: Auth restored (was 401 on 07-19, now 200). Fixed two script bugs: `tags` sent as string instead of JSON array (silently broke every push despite CLAUDE.md claiming this was already fixed), and `push_draft()` read `post_id` from the API response when the field is actually `id` (successful pushes were being logged as failures). Also restricted `scan_repositories()` to the directories this file documents as sync sources — it was previously globbing every `.md` file in the repo, including internal docs and personal job-search files. Pushed 5 real drafts; see `wordpress_integration/SYNC_STATUS.md` for details, a likely duplicate post, and a stray test draft (ID 3360) that needs manual deletion. Did not touch FTP or `deploy.php` — see the 2026-07-06 incident report for why. Did not merge open PRs (10+ across both repos) — left for owner review.
