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
