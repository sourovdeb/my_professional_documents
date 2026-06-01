# Automation Guide — let the machine do the repetition, you just write

*Open-source and free. The goal: you spend your scarce energy on writing and human contact, and automate the soul-draining repetition — job hunting, outreach, follow-ups.*

A warning first, because it protects you: **mass auto-applying and auto-spamming gets accounts banned and reputations damaged.** LinkedIn and Indeed both restrict bots. So the strategy here is *assisted, not autonomous* — automate the **finding, drafting, and tracking**; keep a human (you) on the **send** for anything that reaches a real person. Quality over quantity, again. Ten tailored applications beat two hundred blasted ones.

---

## What you already have (recycle these first)

You built real tools. Don't rebuild — reuse:

- **`gmail_and_email_tools/SMART_EMAIL_COMPOSER_v1.gs`** — Google Apps Script that turns a CSV (company, email, sector, city) into personalised Gmail **drafts**. This is your outreach engine. It drafts; you review and send. Perfect — that's the safe pattern.
- **`browser_extension/`** — your multi-model AI side-panel (Ollama/Claude/etc.) that summarises pages and drafts emails. Use it to read a job page and draft a tailored cover letter in one click.
- **`tools_and_scripts/SKILL_google-apps-script-job-automation.md`** — your own documented workflow. Keep it as the spec.
- **`cv_and_applications/`** — your CV variants by sector. The automation's job is to *match the right CV to the right job*, not to write a new one each time.

Consolidate these under `04_AUTOMATION/` per `REPO_ORGANIZATION_PLAN.md` so there's one outreach engine, not four copies.

---

## The job-search pipeline (assisted)

A clean four-stage loop you run on **one stable day a week**:

1. **DISCOVER — find the jobs (automated).**
   - In your Claude Code environment you already have an **Indeed integration** (search jobs, get job details, get company data) — use it to pull a weekly shortlist by keyword + location.
   - Open-source self-hosted option: **[JobSync](https://github.com/Gsync/jobsync)** — a private, self-hosted tracker with AI résumé review and job matching. Your data stays local.
   - RSS/scraper option for the technically inclined: most boards expose RSS; pipe new postings into one list.
2. **MATCH & TAILOR — pick the CV, draft the letter (assisted).**
   - Score each job against your CV (your browser extension or a local Ollama model does this for free, privately).
   - Auto-select the right CV variant from `cv_and_applications/` (aeronautics / hospitality / general).
   - Draft the cover letter from a template; **you** do the final 5-minute human pass. Never send unread.
3. **TRACK — one board, never your memory.**
   - **JobSync** or a single Kanban (Applied → Replied → Interview → Closed). This is the external brain applied to the job hunt.
4. **FOLLOW UP — the step everyone skips (automated reminder, human send).**
   - A reminder fires at day 7 and day 14. The follow-up is where most offers actually come from.

> On the auto-apply bots ([Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn), [ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot)): they exist and are open-source, but they carry real ban risk and produce generic applications. Read them for ideas; prefer *assisted* over *autonomous*. Your edge is that you write like a human — don't throw that away to a bot.

---

## Email & outreach automation (the safe pattern)

**Draft in bulk, send like a human.** That's the whole rule.

- Use your **`SMART_EMAIL_COMPOSER_v1.gs`**: feed it a CSV, it creates personalised **Gmail drafts** (it does not auto-send — good). Review each, send the good ones.
- In this environment you also have a **Gmail integration** to create drafts directly.
- Keep one master CSV: `name, org, email, sector, city, why_them, last_contact, status`. Personalisation lives in `why_them` — one real sentence per contact. That sentence is the difference between "spam" and "a person reached out."
- Throttle: a handful a day, not hundreds at once. Protects deliverability *and* your nervous system.

---

## Finding writers, collaborators & like-minded partners

You want people to build projects with. Automate the **finding**; keep the **connecting** human.

- **GitHub search** (you have it in this environment): search topics like `mental-health`, `adhd`, `accessibility`, `disability`, `writing-tools` to find people building what you care about. Open an issue or email a maintainer with a real offer.
- **Substack / Medium discovery:** follow tags (bipolar, ADHD, C-PTSD, disability, EdTech). Comment thoughtfully on five writers a week. Collaboration starts as genuine engagement, never a cold "let's collab."
- **Reddit & Discord communities** (r/bipolar, r/ADHD, r/CPTSD, r/TEFL, writing servers): be present, be useful; partners emerge from people who already know your work.
- **A simple "people radar":** keep `05_CONTACTS/collaborators.csv` — name, where you found them, what they make, one thing you admire, last contact. Review weekly. Reach out to one. That's it.
- **Automate the watching, not the relationship.** Set up keyword alerts (Google Alerts, RSS, GitHub watch) for your topics so good people surface to you. The outreach itself is always you, human, specific.

---

## The honest boundaries

- **Never** auto-send to a real human's inbox without reading it. Drafts, always.
- **Never** commit API keys, app passwords, or credentials to this repo (see the security notes).
- **Respect every platform's terms** — a banned account costs you more than the time it saved.
- **Match your automation to your energy.** Run the weekly batch on a stable day. On a crash day, the system has already queued the drafts — you just don't touch them. That's by design.

*Sources: [JobSync](https://github.com/Gsync/jobsync), [ApplyPilot](https://github.com/Pickle-Pixel/ApplyPilot), [Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn), GitHub `job-search-automation` topic.*
