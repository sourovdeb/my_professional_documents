# Sourov Deb — Productivity & Health Agent Fleet

A durable set of **10 agents** designed to boost productivity and protect health
across every dimension of life in Réunion (974): admin/French agencies, health &
stability, income, content, and daily planning.

> Created 2026-07-11. Owner: Sourov Deb (sourovdeb.is@gmail.com).
> Central coordinator: **Agent 01 — Holistic Life Orchestrator**.

## Design principles

1. **Health first, always.** Neurodivergence-friendly (bipolar / ADHD / depression):
   low-energy, low-cognitive-load, micro-steps, no shame, stability over output.
2. **Durable by default.** 9 of the 10 agents contain **no hard-coded personal facts**.
   They read the facts they need at run time from the *Knowledge Cache* (Agent 10),
   from Gmail, or from the Drive document folder. Life changes — the agents don't have
   to be rewritten when it does.
3. **One hard-coded exception.** Only **Agent 01 (Holistic Life Orchestrator)** carries
   concrete professional/administrative reference data (SIRET, account numbers, agency
   contacts, case references), and even that lives in a clearly-marked, editable
   `REFERENCE DATA` block so it stays maintainable.
4. **Scan → Analyze → Remind → Create.** The orchestrator and its helpers watch the
   inbox and the Drive folder, understand what arrived, warn ahead of deadlines, and
   draft/produce whatever is needed (emails, letters, CSVs, plans, posts).
5. **Single source of truth.** All durable facts live in the Knowledge Cache; agents
   update it *sparingly* and only with new, durable facts.

## Shared priority framework (used by every agent)

Score each item on four axes, then order by total (health always wins ties):

| Axis | Question |
|------|----------|
| **Health impact** | Does acting / not acting affect stability, medication, energy? |
| **Irreversibility** | Can this be undone later, or is the door closing (deadline, expiry)? |
| **Time-sensitivity** | How soon is the deadline / échéance? |
| **Communication frequency** | Who is waiting, and how often are they chasing? |

**Domain order when in doubt:** 1. Health → 2. Legal / regulatory / tax →
3. Family & appointments → 4. Income / tutoring → 5. Content / WordPress.

## The fleet

| # | Agent | Type | What it watches | What it produces |
|---|-------|------|-----------------|------------------|
| 01 | Holistic Life Orchestrator | **Hard-coded** | Gmail + Drive folder | Reminders, drafts, CSVs, delegated tasks |
| 02 | Health & Stability Guardian | Generic | Health config, mood/energy logs | Routines, med reminders, check-ins |
| 03 | Appointment & Deadline Sentinel | Generic | Emails, docs, calendars | Deadline register, lead-time alerts |
| 04 | Document Intake Analyst | Generic | New PDFs / letters / attachments | Summaries, extracted facts, filing |
| 05 | Inbox Triage Agent | Generic | Gmail | Triaged/labeled inbox, reply drafts |
| 06 | Admin Correspondence Drafter | Generic | Case threads | Formal FR/EN letters & emails |
| 07 | Income Opportunity Scout | Generic | Job boards, leads | Scored leads, tailored applications |
| 08 | Content Publishing Agent | Generic | Content backlog, WordPress | Drafted & scheduled posts |
| 09 | Weekly Planner & Prioritizer | Generic | All of the above | Realistic daily/weekly plan |
| 10 | Knowledge Cache Curator | Generic | Everything durable | Maintained cache/index |

## How they fit together

```
                 ┌──────────────────────────────┐
                 │ 01 Holistic Life Orchestrator │  (hard-coded facts)
                 └───────────────┬──────────────┘
        scan/analyze/remind/create — delegates to:
   ┌───────┬───────┬───────┬───────┬───────┬───────┬───────┬───────┐
  02Health 03Dline 04Docs 05Inbox 06Letters 07Income 08Content 09Plan
   └───────┴───────┴───────┴───────┴───────┴───────┴───────┴───────┘
                        all read/write:
                 ┌──────────────────────────────┐
                 │ 10 Knowledge Cache Curator     │  (single source of truth)
                 └──────────────────────────────┘
```

## Files

- `01-holistic-life-orchestrator.md` … `10-knowledge-cache-curator.md` — one agent each
  (YAML frontmatter `name` + `description`, then the full system prompt).
- `agents-catalog.csv` — machine-readable index (mirrored to the Drive obligations folder).
