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

## 12-hour automation loop

Every 12 hours, run a lightweight cycle:

1. Scan for new tools/services in: writing, reminders, form filling, document collection, auto design, auto contact, WordPress control, and file checking.
2. Triage each candidate for usefulness, cost, privacy, and mental-load reduction.
3. Keep only high-value candidates in an action queue.
4. Implement one small automation improvement at a time.
5. Log what changed and expected daily-life benefit.

See `/tmp/workspace/sourovdeb/my_professional_documents/REPO_INVENTORY.md` for the reorganization map and operational checklist.

## Automation command (execute now)

```bash
python3 /tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py
```

This command updates:

- `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tool_discovery_reports/`
- `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`
