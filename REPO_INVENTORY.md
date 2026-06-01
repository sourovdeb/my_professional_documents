# Repository Inventory and Reorganization Map

## Purpose

This index maps the previous layout into the new structure and defines the first execution baseline.

## Reorganization map

| Previous location | New location | Purpose |
|---|---|---|
| `Biography_and_Medical/` | `02_identity_profile/Biography_and_Medical/` | Core biography and personal reference files |
| `Communications/` | `03_communications/Communications/` | Contact and communication assets |
| `gmail_and_email_tools/` | `03_communications/gmail_and_email_tools/` | Email draft automation assets |
| `Legal_Documents/` | `04_legal_medical/Legal_Documents/` | Legal and administrative records |
| `CELTA_Teaching_Materials/` | `05_jobs_cv_outreach/CELTA_Teaching_Materials/` | Teaching/career training materials |
| `cv_and_applications/` | `05_jobs_cv_outreach/cv_and_applications/` | Job application and CV files |
| `browser_extension/` | `06_automation_assets/browser_extension/` | Browser automation extension |
| `tools_and_scripts/` | `06_automation_assets/tools_and_scripts/` | Scripts, setup guides, automation docs |
| `therapy_and_wellbeing/` | `07_mental_health_support/therapy_and_wellbeing/` | Mental health support records |
| `Story_of_Sourov/` | `08_archive/Story_of_Sourov/` | Historical project snapshot |
| `archives/` | `08_archive/archives/` | Historical archives and extracted bundles |

## Operational status board

### Current baseline

- Intake area created: `01_intake_raw/`
- Functional areas created and populated
- Historical content moved to archive namespace
- 12-hour discovery automation added in:
  - `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/tools_and_scripts/discovery_loop/run_discovery_cycle.py`
- High-priority findings output enabled at:
  - `/tmp/workspace/sourovdeb/my_professional_documents/IMPORTANT_FOR_USER.md`

### Next operating steps (12-hour cadence)

1. Check `01_intake_raw/` and move files to final folders.
2. Add candidate tools/services discovered in last 12 hours.
3. Mark each candidate: `approved`, `deferred`, or `rejected` with reason.
4. Implement one approved automation at a time in `06_automation_assets/`.
5. Record outcomes and reduced manual effort.

## Notes

- Previous root extension README has been preserved at:
  - `/tmp/workspace/sourovdeb/my_professional_documents/06_automation_assets/browser_extension/README_EXTENSION_V2.md`
