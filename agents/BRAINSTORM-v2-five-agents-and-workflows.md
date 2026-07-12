# Brainstorm v2 — Five Core Productivity Agents, Email Debrief Routine, Agent-to-Agent Workflow, and Gmail Backup Plan

**Date:** 2026-07-11 · **Status: BRAINSTORM ONLY — no scripts, no IDs yet.**
This document deliberately stops at *design*. Scripts, spreadsheet IDs, folder IDs, and code
come in a later step, once these designs are approved.

Inputs considered: 10-agent fleet (PR #47), `10_integrated_agents_v1.1.md` (health gate +
scheduler), `sourov_deb_cache_and_index.md`, token-optimization best practices, `WORKFLOW_SUMMARY.md`.

> ⚠️ **Security note found during review:** `WORKFLOW_SUMMARY.md` (in the v1.1 zip) contains
> plain-text credentials (FTP password, deploy key, REST API key) that also appear in a public
> audit context. **Rotate them** and store future secrets only in a password manager / Apps
> Script Properties — never in Markdown, Drive docs, or repos. All designs below assume
> secrets-by-reference.

---

## Part 1 — The 5 Core Productivity Agents (generic, intelligent, long-term)

Design constraints, learned from v1.0/v1.1:
- **Generic**: zero personal facts in the agent body; everything personal is fetched at run
  time from the Cache Index (the "brain file"). Life changes → agents don't.
- **Intelligent**: each agent has a *reasoning contract* (what it must think about before
  acting), not just a task list.
- **Efficient**: each agent applies the token rules — consult cache before searching, batch,
  summarize, dedupe tool calls, small-model-first mindset.
- **Long-term**: platform-agnostic wording ("the email system", "the file store") so the same
  instructions run on Claude Code, OpenClaw, Grok, or any future agent runtime.
- **Health gate inherited**: every agent respects the red/yellow/green energy gate from v1.1.

### Agent A — Chief Synthesizer (the daily brain)
**One job:** turn everything that happened (mail, documents, deadlines, events) into ONE
short debrief with decisions attached.
- **Reasoning contract:** never report raw data; always answer *"so what, and what next?"* for
  each item. Rank by Health impact · Irreversibility · Time · Who-is-waiting. Max 3 priorities
  surfaced; everything else goes to the log, not the human.
- **Inputs:** outputs of the other agents; cache index for context.
- **Outputs:** daily/weekly debrief + one-line "if you do only one thing today" + appended rows
  to the master tracking sheet.
- **Efficiency rules:** reuse yesterday's debrief as the diff base (report only changes);
  summarize threads once and cache the summary.

### Agent B — Signal Scanner (email + document intake)
**One job:** scan communication channels (Inbox, Sent, Drafts) and the file store for *signals*:
deadlines, requests, confirmations, risks, opportunities.
- **Reasoning contract:** classify every item into {Action / Wait / Info / Risk / Noise};
  extract dates, amounts, reference numbers **verbatim**; distinguish *what the sender wants*
  from *what the subject line says*. Check Sent + Drafts too — an unanswered sent question and
  a stale unsent draft are both signals.
- **Outputs:** structured signal list (feeds Agent A and the tracking sheet), flagged scams.
- **Efficiency rules:** incremental scans only (since last checkpoint timestamp); never
  re-summarize an already-summarized thread; batch label operations.

### Agent C — Solution Builder (official-source problem solver)
**One job:** for each administrative / legal / medical / professional problem, build a concrete
solution path **using official sources only** (service-public.fr, ameli.fr, urssaf.fr,
impots.gouv.fr, francetravail.fr, legifrance, agency letters themselves).
- **Reasoning contract:** (1) restate the problem, (2) find the official rule and cite it,
  (3) produce steps with the exact form/portal/phone, (4) state deadline + consequence of
  inaction, (5) flag when a human professional is required. Never guess a rule; if the official
  source is ambiguous, say so.
- **Outputs:** "solution cards" — problem, official basis, steps, deadline, artifacts to draft.
- **Efficiency rules:** cache official-rule lookups (rules change slowly, TTL ~ months); one
  solution card template reused everywhere.

### Agent D — Executor & Artifact Maker
**One job:** turn decisions into artifacts — drafts, letters, CSV rows, calendar entries, filled
checklists — ready for one-click human approval.
- **Reasoning contract:** every artifact must be *sendable/usable as-is*; correct language and
  register per recipient; every claim traceable to a source document; **never sends anything**
  itself. Applies the compliance gate concept from v1.1 (e.g. the CELTA wording gate) as a
  generic "blocked-phrases / required-disclosures" pre-flight read from the cache.
- **Outputs:** drafts in the email system's draft folder, files in the file store, rows in
  the tracker.
- **Efficiency rules:** template library; produce batch artifacts in one pass.

### Agent E — Memory & Continuity Keeper
**One job:** keep the brain file (cache index) current, versioned, and **multi-homed** so no
single account loss kills the system.
- **Reasoning contract:** append only durable facts, dated; compress periodically; detect
  contradictions between cache and new evidence and surface them; maintain the *continuity
  kit* (Part 4) — verify backups actually restored, not just saved.
- **Outputs:** updated cache index (Drive + GitHub mirrors), changelog, quarterly "restore
  drill" report.
- **Efficiency rules:** this agent IS the token strategy — all other agents read the cache
  first and search second.

**Mapping to the PR #47 fleet:** A≈01+09, B≈04+05, C≈06+ new official-source discipline,
D≈06/07/08 execution layer, E≈10 extended with continuity. The 5 are the *operating core*;
the 10 remain the specialist bench.

---

## Part 2 — The Email Debrief Routine (instruction spec, runtime-agnostic)

A single instruction any agent (Claude Code, OpenClaw, Grok…) can run on schedule.

**Routine name:** `email-debrief`
**Cadence:** daily (evening, low-energy window per health gate) + lightweight midday delta.

**Steps (the instruction itself):**
1. **Checkpoint.** Read last-run timestamp from the tracker. Scan only newer items.
2. **Scan three views:** Inbox (new/unread), **Sent** (questions I asked that got no reply in
   >N days → follow-up candidates), **Drafts** (stale drafts >N days → finish or delete).
3. **Classify** each thread: Action / Wait / Info / Risk / Noise; tag domain
   (health / legal / admin / professional / personal / financial).
4. **Extract verbatim:** dates, deadlines, amounts, reference numbers, who is waiting.
5. **Solve:** for each Action/Risk item, attach a mini solution card (Agent C rules —
   official sources only, cite the source).
6. **Write the debrief** (≤ 1 screen): Top 3 actions with deadlines → things waiting on others
   → risks → FYI. One line each. Bad-day version: Top 1.
7. **Update the tracker** (CSV/spreadsheet — schema below): one row per open item; update
   status of existing rows; never duplicate.
8. **Create artifacts** where obvious (reply drafts, calendar entries) — draft-only, never send.
9. **Save checkpoint** + append a one-line run log (items scanned, tokens used, anomalies).

**Tracker schema (one sheet, all of life):**
`ID · Date_Detected · Domain · Source(email/doc/link) · What_It_Is · Advice ·
Steps(official-source-based) · Deadline · Owner · Status(Open/Waiting/Done/Dropped) ·
Result · Next_Check_Date · Health_Impact(L/M/H) · Irreversible(Y/N) · Notes`

**Debrief delivery order of preference:** chat message → email-to-self → row in tracker
(always) — so the debrief survives even if the chat session is lost.

---

## Part 3 — Agent-to-Agent + Drive Workflow (trigger chain design)

**Chain (event-driven, not monolithic):**

```
[Schedule / new-mail event]
   → B Signal Scanner  (Gmail: Inbox+Sent+Drafts; incremental)
   → (attachments/docs found) → Drive intake:
        read Google Docs & Sheets natively; PDFs via text-extraction step
   → C Solution Builder (official sources; solution cards)
   → D Executor (drafts, CSV rows, calendar entries — approval-gated)
   → A Chief Synthesizer (debrief to human; Top-3)
   → E Memory Keeper (cache update, backups, checkpoint)
```

**Design rules:**
- **Hand-offs are files, not chat.** Each agent writes its output to a known Drive location /
  repo path; the next agent reads it. This makes the chain restartable, auditable, and
  runtime-independent (any agent platform can pick up mid-chain).
- **One shared state file** (the tracker + checkpoint) prevents double-processing.
- **Drive reading:** Docs and Sheets read directly via Drive tools; scanned PDFs need an OCR/
  text-extraction step — mark items "unreadable, needs OCR" rather than guessing (we hit this
  limitation live today).
- **Pre-made Gmail scripts:** the existing Apps Script assets (job pipeline, campaign sender)
  join the chain as *data producers only* — their outputs land in Drive where Agent B reads
  them. **They keep their compliance gates** (`assertCampaignSafe_()`, TEST_MODE first, blocked
  CV wording) and never gain send authority from this workflow.
- **Health gate wraps the chain:** red flag → only steps 1–2 + a one-line debrief run; nothing
  is created, nothing is urgent-flagged except true irreversibles.

---

## Part 4 — Gmail Outage / Account-Loss Backup Plan (continuity kit)

**Threat model:** Gmail account suspended, locked, or inaccessible while traveling — losing
mail, Drive, and the identity attached to agencies.

**Layer 0 — Prevention (do first):**
- 2FA with **two** methods incl. printed backup codes stored offline; recovery email +
  phone kept current; passkey where possible.
- Rotate the exposed credentials found in `WORKFLOW_SUMMARY.md`.

**Layer 1 — Continuous data escape (nothing exists only in Google):**
- **Google Takeout** on a recurring schedule (Mail + Drive + Contacts + Calendar) to a
  second location.
- Cache index, tracker CSV, agent instructions: **multi-homed by design** — Drive + GitHub
  (already true for PR #47 content) + one offline copy.
- Contacts and the deadline register exported to CSV monthly (they are the hardest to rebuild).

**Layer 2 — Standby identity (ready before it's needed):**
- A second mailbox at an independent provider (e.g. **Proton Mail** — EU, works well from
  France/Réunion; alternative: Zoho Mail / Outlook). Created now, kept warm.
- Optionally a **custom-domain address** (e.g. on sourovdeb.com) used as the *public* address
  with forwarding — then the provider behind it can be swapped without telling anyone.
  This is the single strongest long-term move: agencies learn ONE address you control forever.
- Gmail auto-forwarding of all mail to the standby mailbox = live mirror of new mail.

**Layer 3 — Failover runbook (what to do the day it happens):**
1. Switch to standby mailbox (it already has forwarded history).
2. From the tracker (multi-homed), read the list of agencies/contacts with the address on file
   → notify by their official change-of-contact channels (Ameli, Urssaf, impots.gouv, France
   Travail, banks — each has an in-portal contact setting that does *not* depend on email).
3. Agents repoint: the only change needed is the "email system" connector, because every agent
   is generic and reads addresses from the cache — this is why Part 1 forbids hard-coding.
4. Attempt Google recovery in parallel (recovery codes from Layer 0).

**Layer 4 — Drill:** quarterly, Agent E performs a 15-minute test: restore one Takeout file,
log into standby mailbox, confirm forwarding works, confirm tracker copy opens. Log the result.

---

## Part 5 — Decision list (what to approve before any building)

1. Approve the 5-agent core (Part 1) as the operating layer over the existing 10.
2. Approve the tracker schema (Part 2) — then we create the actual spreadsheet.
3. Approve the chain + file-hand-off rule (Part 3).
4. Choose standby provider (Proton vs Zoho vs Outlook) and whether to adopt the
   custom-domain address strategy (recommended).
5. Rotate the exposed credentials (blocking, independent of everything else).
6. Then, in order: create tracker sheet → write `email-debrief` instruction for the chosen
   runtime → wire Drive hand-off folders → dry-run the chain in read-only mode for 3 days →
   enable artifact creation (still draft-only).

**Nothing in this file is code. Next session: pick items from Part 5 and we build.**
