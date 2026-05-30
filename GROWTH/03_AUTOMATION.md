# 03 — Automation (so you only have to write)

The deal: machines do the searching, sorting and drafting; you do the writing and the
final human send. Everything below is open-source or free. **Turn on ONE thing at a
time** — an over-built system you don't trust is worse than one alert that works.

> Safety / legal note: auto-*applying* and aggressive scraping can violate LinkedIn and
> Indeed terms of service and can get accounts limited. The safe, durable pattern is
> **automate discovery and drafting, keep the apply/send human.** That's also better for
> you — a tailored human application beats 200 spray-and-pray ones. Quality over quantity.

## A. Find jobs automatically (lowest effort, highest payoff — start here)

**Free, no-code, ToS-safe:**
- **Official job-board alerts** — LinkedIn Jobs, Indeed, France Travail (Pôle emploi), Welcome to the Jungle, and EU/teaching boards (TEFL.com, Cambridge, British Council). Save a search → email alert. Set up once, jobs arrive daily.
- **RSS + a filter** — many boards expose RSS. Pipe into a reader (or n8n) and keyword-filter for "English trainer / CELTA / IELTS / remote / La Réunion / FLE".
- This repo already has a **job MCP / search tool** and a Google Apps Script job-automation skill (`Story_of_Sourov/04_REUSABLE_SKILLS/SKILL_google-apps-script-job-automation.md`). Recycle it.

**Open-source tools (more power, more setup — adopt later, read their ToS):**
| Tool | What it does |
|---|---|
| **JobSync** | Self-hosted job *tracker* + AI resume review + job matching. Your data stays local. Safest pick — tracking, not auto-applying. |
| **career-ops** | Local, agentic (Claude Code + Playwright). Evaluates fit CV-vs-listing, tailors your resume per job. Data stays on your machine. |
| **AIHawk / Auto_Jobs_Applier** | Automates applications. Powerful but ToS-grey on LinkedIn — use for *drafting/tailoring*, send manually. |

**Recommended setup:** Job-board email alerts (today) → **JobSync** to track + AI-match
(week 3) → tailor each application with **Ollama**/Claude using your CV in
`Profile_Documents/`. Send by hand.

## B. Automate email & outreach (recycle what you built)

You already own an **open-source Chrome extension** for AI Gmail draft automation
(`Email_Extension/`): CSV → personalised, sector-specific drafts, batch creation, Ollama
by default. **Use it. Don't rebuild it.**

Pattern:
1. Keep a CSV: schools, language centres, editors, recruiters (name, org, email, hook).
2. Extension generates a tailored *draft* per row.
3. You read, tweak one line, send. Human in the loop = better replies + safe.

This repo's Gmail MCP tools can also create drafts directly — same principle, drafts not
auto-sends.

## C. Find like-minded writers & partners

- **GitHub search** — find people writing about ADHD/bipolar + productivity + EdTech. Star, follow, open issues, propose collaboration. Your repo *is* your portfolio.
- **Substack / Medium** — follow writers in your lane; comment with substance (not "great post"); the recommendation network surfaces you to their readers.
- **Communities** — r/ADHD, r/bipolar, neurodiversity-in-work Discords/Slacks, FLE/ELT teacher groups, IndieHackers (for the build-in-public angle). Show up consistently in one or two, not everywhere.
- **Semi-automate the scan:** you have a `SKILL_ai-agent-file-scraper.md` — point it at these sources to surface people writing on your themes, then reach out *manually* and personally.

## D. The glue: one free automation engine

**n8n** (open-source, self-hostable, free) or **Make**/Zapier free tiers connect it all:
- New job matching keywords → row added to your tracker + a draft email queued.
- New essay published → auto-cross-post hook to LinkedIn + log a line in `GROWTH/log.md`.
- Weekly digest email to yourself: jobs found, drafts pending, who to follow up.

Build **one** flow first (job alert → tracker). Trust it for a week. Then add the next.

## Guardrails (so automation serves your health)
- **Human send, always.** Machines find and draft; you approve. Protects accounts and quality.
- **One new automation per week, max.** Novelty is a dopamine trap; resist building over doing.
- **If a flow breaks and stresses you, delete it.** The streak (file 00) matters more than any pipeline.

## Sources
- [JobSync (self-hosted tracker)](https://github.com/Gsync/jobsync)
- [career-ops (local, agentic)](https://github.com/santifer/career-ops)
- [AIHawk Jobs Applier](https://github.com/feder-cr/jobs_applier_ai_agent_aihawk)
- [job-search-automation topic](https://github.com/topics/job-search-automation)
