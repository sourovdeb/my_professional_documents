# Two Core Agents — Consolidated System (v1.0, 2026-07-13)

Distilled from the earlier 1-orchestrator + 9-specialist design into the **2 most important
agents**, built for long-term use. Health stability is the non-negotiable gate for both.

| # | Agent | Folder | Hard-coding | Role |
|---|-------|--------|-------------|------|
| 1 | **Life & Health Orchestrator** | `01_life_health_orchestrator/` | **None** — all specifics in `registry.yaml` | One agent for many areas: text/docs, health, doctor appointments, any administrative body. Scans email/Drive/Box + documents, analyses, reminds, and creates drafts/letters/reminders/tracker rows. Owns the Health Gate. |
| 2 | **Professional & Administrative** | `02_professional_admin_agent/` | **Permitted** (the only one) | French auto-entrepreneur admin: URSSAF, DGFiP/impôts, CGSS Réunion, France Travail, BNC regime, SIRET, DSN, PAS, facturation électronique. Defers to Agent 1's Health Gate + shared tracker. |

## Design principles

- **Health first, always.** Neither agent proposes work that risks stability. STOP / PAUSE /
  PROCEED thresholds live in the registry, applied before any planning.
- **No hard-coding except Agent 2.** Agent 1 references roles and registry keys, never literal
  names/agencies/dates — so it keeps working as life changes. Only Agent 2 holds domain rules,
  and even it keeps personal identifiers out of the prompt (registry-only).
- **Long-lived.** Change the `registry.yaml`, not the prompts. Prompts version only when the
  loop or the Health Gate logic itself changes. Cache is append-only and dated.
- **Evidence-based.** Every admin/legal/medical/deadline claim is verified against the
  authority's official URL before it is stated or written into a filing.

## Files

```
agents/
├── TWO_CORE_AGENTS.md                         <- this file
├── 01_life_health_orchestrator/
│   ├── AGENT.md                               <- what it is + the loop + Health Gate
│   ├── PROMPT.md                              <- paste-ready, name-free system prompt
│   └── registry.example.yaml                  <- the ONLY place specifics live (copy -> registry.yaml, private)
├── 02_professional_admin_agent/
│   ├── AGENT.md                               <- French auto-entrepreneur domain map + rules
│   └── PROMPT.md                              <- paste-ready specialist prompt
└── trackers/
    └── two_core_agents_tracker.csv            <- master tracker (mirrored to Drive + Box)
```

## Storage / sync

- **GitHub:** `sourovdeb/my_professional_documents` (this folder).
- **Google Drive:** CSV mirrored to folder `1O9QPObl7_Tls3jMliCoxE-lsUuG9WfTf`.
- **Box:** CSV + agent files backed up.

## Migration note

The previous 10-agent specs remain in their sub-folders for reference. Going forward, the
**two core agents above are the system**: Agent 1 handles everything general (and owns the
Health Gate + tracker); Agent 2 handles the professional/French-admin specialism. Any earlier
specialist's concern is now either a registry entry (Agent 1) or a rule in Agent 2.
