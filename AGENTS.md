# AGENTS.md — Operational Governance (Profile 4_job_search)

## Canonical Environment Paths
- **PROFILE_HOME**: `C:/Users/souro/AppData/Local/hermes/profiles/4_job_search/`
- **CORPUS**: `G:/Sourov docume/Sourov documents/00_CORPUS_OFFICIAL/`
- **KEEPERS**: `H:/hermes-session-keepers/`
- **WIKI**: `E:/.sourov_wiki/`

## Mandatory Safety Gates
1. **Email Assertion**: Regex gate `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$` before any DOM input.
2. **Queue Integrity**: Process `queue.confirmed-apply.json` ONLY. Root domains → `queue.recon-needed.json`.
3. **No Credential Entry**: Never input passwords or bypass CAPTCHAs. Hand off to BrowserOS Neo.
4. **Secret Boundary**: Secrets in `.env` only. Never in `config.yaml`, markdown, or memory.
5. **Consent Gate**: `standing-consent.json` required for live submits (scope: no_login_no_captcha_only).
6. **Submit Counter**: Max 3 per session. Stop at ceiling.

## Layer Architecture
```
CORE      → config.yaml, approvals.mode: smart, secret redaction
PROFILE   → SOUL.md (identity), AGENTS.md (governance), PROFILE.md (consolidated)
SKILL     → job-execution-core, job-queue-manager, browser-tool-selection
TOOL      → Camoufox (:9377), BrowserOS Neo (:9010), Indeed MCP, Skyvern MCP
STATE     → state.db, submissions_log.jsonl, form_states.md, standing-consent.json
N8N       → FT API v2 polling (:5678), CSV normalizer, webhook relay
ARCHIVE   → legacy/scripts/ (batch_apply.py, build_*.py, etc.)
```

## Daemon Pre-flight Checklist
Before execution: check `curl -s localhost:9377/health`, `hermes gateway status`, `hermes mcp list`.
All three must return green. Any failure = halt and report blocker.

## Conflict Resolution Rules
- `config.yaml` is source of truth for model/provider routing (override `.hermes.md`).
- `SOUL.md` is source of truth for identity/voice (override any stale boilerplate).
- `PROFILE.md` is consolidated authority for profile-level rules (merge SOUL/RULES when updated).
- When paths conflict, canonical = `C:/Users/souro/AppData/Local/hermes/profiles/4_job_search/`.

## n8n ↔ Hermes Contracts
- Inbound: `POST http://127.0.0.1:8644/webhook/job-dispatch` (max 3 targets/batch)
- Outbound: `POST http://127.0.0.1:5678/webhook/job-complete`
- n8n host: `127.0.0.1:5678`. Hermes webhook receiver: `:8644`.
