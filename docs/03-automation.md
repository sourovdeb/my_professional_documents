# Automation: You Just Write

The machine handles searching, drafting, and scaffolding. You handle the words
and the genuine human contact. Everything here uses **free, official, legal
sources** — no scraping behind logins, no terms-of-service violations.

## What's automated, and what stays human

| Step | Automated | Stays human (always) |
|------|-----------|----------------------|
| Finding jobs | ✅ Indeed connector / official alerts | You choose where to apply |
| Finding writers/partners | ✅ public APIs | You write the real message |
| Email drafts | ✍️ Gmail connector drafts only | You read and send |
| Publishing | ✅ pushes a WordPress *draft* | You press publish |

**Why outreach stays human:** mass automated messages get ignored or blocked, and
they betray the point — real connection. Automate the *finding*. Never automate
the *caring*.

## Tools you already have in this repo (recycle these)

- **Gmail bulk-draft Chrome extension** (`manifest.json`, `background.js`,
  `sidepanel.*` at the repo root) — generates email drafts in bulk. See its README.
- **`Story_of_Sourov/03_TOOLS_SCRIPTS/SMART_EMAIL_COMPOSER_v1.gs`** — Google Apps
  Script email composer.
- **Reusable skills** in `Story_of_Sourov/04_REUSABLE_SKILLS/` —
  `SKILL_google-apps-script-job-automation.md`,
  `SKILL_ai-agent-file-scraper.md`, and more. Reuse before rebuilding.

## Live connectors available in this assistant

You don't need to write scrapers — these are wired in and legal:

- **Indeed connector** — search live job listings, pull job and company details
  directly. Ask: *"Find remote English-teaching / content-writing jobs."*
- **Gmail connector** — create, label, and search **drafts** (never auto-sends).
  Ask: *"Draft a follow-up to {employer} based on my CV."*
- **Google Drive connector** — search and read your Drive documents.
- **GitHub connector** — manage branches and PRs for this repo.

## On Indeed and LinkedIn specifically

- **LinkedIn forbids automated scraping / bulk-applying** in its terms — doing it
  risks your account and can be illegal in some places. Use its **official Job
  Alerts** (saved searches emailed to you). That's the real, free automation.
- **Indeed:** use the connector above, or Indeed's official **email alerts**.
- **Email:** the Gmail connector drafts cover letters and follow-ups; you always
  review and send.

## Adding new automation later

Recycle, don't reinvent. Each new tool should: (1) use a free official source,
(2) write output to a **gitignored** file, (3) never send anything on your behalf
without you confirming. Document it here when you add it.
