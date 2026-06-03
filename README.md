# my_professional_documents

Repository reorganized for easier daily execution and lower cognitive load.

## Top-level structure

- `01_intake_raw/` — new incoming files before sorting.
- `02_identity_profile/` — biography, profile, and personal context.
- `03_communications/` — outreach content, contacts, email tooling outputs.
- `04_legal_medical/` — legal and administrative case documents.
- `05_jobs_cv_outreach/` — CVs, letters, teaching/career materials.
- `06_automation_assets/` — scripts, browser extension, setup guides.
- `07_mental_health_support/` — therapy and wellbeing notes.
- `08_archive/` — previous bundles, historical exports, snapshots.

## 6-hour automation loop

Every 6 hours, run a lightweight cycle:

1. Scan for new tools/services in: writing, reminders, form filling, document collection, auto design, auto contact, WordPress control, and file checking.
2. Triage each candidate for usefulness, cost, privacy, and mental-load reduction.
3. Keep only high-value candidates in an action queue.
4. Implement one small automation improvement at a time.
5. Log what changed and expected daily-life benefit.
6. Keep personal and medical documents as internal context only; do not publish them directly.

See `/tmp/workspace/sourovdeb/my_professional_documents/REPO_INVENTORY.md` for the reorganization map and operational checklist.

## Automation command (execute now)

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

This command updates:

- `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tool_discovery_reports/`
- `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`

## Push drafts to WordPress (REST)

Dry-run preview:

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py
```

Execute publish (as drafts):

```bash
WP_API_KEY='<your_key>' python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/push_drafts_to_wordpress.py --execute
```

## Hourly story post automation

Generate chronological story posts from repository files, with a 200-word analysis and one GitHub reference, saved locally and optionally pushed to WordPress:

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/generate_hourly_story_post.py
```

```bash
WP_API_KEY='<your_key>' python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/generate_hourly_story_post.py --execute
```

WordPress REST references:

- `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/WORDPRESS_REST_REFERENCES.md`
