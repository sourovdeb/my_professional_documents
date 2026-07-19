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
# AI Agents System for Sourov Deb

> **⚠️ SUPERSEDED — v2.0 now lives in [`agents/v2/`](v2/README.md)** (2026-07-11).
> v2.0 applies the review feedback: broader wellbeing agent, no hardcoded dates in agent logic, France Travail merged into Legal Sentinel, Real Estate broadened to Home & Personal Admin, Inbox-to-Action auto-reminder engine, CELTA agent retired, plus new Deep Brainstorm & Research Partner and Tutoring & Learning Designer agents. The specs below are kept for history only.

> **Auto-Entrepreneur Productivity & Health Stability System**
> 
> **Owner**: Sourov Deb  
> **Location**: La Réunion (UTC+4)  
> **Regime**: Auto-Entrepreneur BNC1  
> **Health Priority**: ADHD (Ritalin 20mg LP, ALD) + Bipolar I + Depression  
> **Core Principle**: Health stability is the non-negotiable gate for ALL outputs

---

## 🎯 System Overview

This repository contains **10 integrated AI agents** designed to boost productivity while prioritizing health stability.

### System Architecture
- **1 Central Orchestrator** (Agent 0): Holistic Multi-Area Stability & Admin Orchestrator
- **9 Specialized Agents**: Health, Finance, Legal, Business, Content, France Travail, Real Estate, Documents, CELTA Advocacy

All agents operate with **health/stability as the primary constraint**.

---

## 📁 Repository Structure

```
agents/
├── README.md
├── orchestrator/spec.yaml
├── health_monitor/spec.yaml
├── financial_guardian/spec.yaml
├── legal_sentinel/spec.yaml
├── business_engine/spec.yaml
├── content_publisher/spec.yaml
├── ft_navigator/spec.yaml
├── real_estate_manager/spec.yaml
├── doc_processor/spec.yaml
├── celta_advocate/spec.yaml
└── trackers/sourov_agent_tracker.csv
```

---

## 🚀 Quick Start

### Prerequisites
- GitHub access to `sourovdeb/my_professional_documents`
- Google Drive folder: `1O9QPObl7_Tls3jMliCoxE-lsUuG9WfTf`

### Installation
```bash
git clone https://github.com/sourovdeb/my_professional_documents.git
cd my_professional_documents/agents
# Files are already here
```

---

## 🤖 Agent Inventory

| # | Agent | Role | Priority |
|---|-------|------|----------|
| 0 | Holistic Orchestrator | Central command & control | CRITICAL |
| 1 | Health Stability Monitor | Meds, sleep, energy tracking | CRITICAL |
| 2 | Financial & Tax Guardian | Urssaf, DGFiP, e-invoicing | HIGH |
| 3 | Legal & Compliance Sentinel | CGSS, ALD, France Travail law | HIGH |
| 4 | Business Development Engine | Income streams, partnerships | MEDIUM |
| 5 | Content & WP Publisher | Blog, WordPress, social media | MEDIUM |
| 6 | France Travail Navigator | Contract, ORE, job search | MEDIUM |
| 7 | Real Estate Manager | Copropriete, property law | LOW |
| 8 | Email & Doc Processing Hub | Inbox, PDFs, deadlines | HIGH |
| 9 | CELTA Advocacy Champion | Disability rights, Cambridge | MEDIUM |

---

## 📊 Master CSV Tracker

Location: `trackers/sourov_agent_tracker.csv` and Google Drive `1O9QPObl7_Tls3jMliCoxE-lsUuG9WfTf`

---

## 🛡️ Health Stability Protocol

**NON-NEGOTIABLE**: No task proceeds if it risks health stability.

- **STOP**: >2h focus, <24h deadline, med conflict, sleep debt, energy <4/10
- **PAUSE**: 1-2h focus, <72h deadline, energy 4-6/10
- **PROCEED**: <1h task, >72h deadline, energy >6/10

---

## 📞 Support

For issues, check agent-specific YAML files or contact system administrator.

---

*Repository created: 2026-07-11 | Maintainer: Sourov Deb*
