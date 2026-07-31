# Chat & Work Archive

A classified, durable record of the work done through Claude Code in this
environment — routines, sessions, and the artifacts they produced across Box and
GitHub.

Start at **[`INDEX.md`](INDEX.md)**.

```
chat_archive/
├── README.md              ← you are here: scope, limits, how to run it
├── TAXONOMY.md            ← the controlled vocabulary
├── INDEX.md               ← generated master index
├── overrides.json         ← hand corrections to the classifier
├── routines/              ← all 27 scheduled routines, full prompts, classified
│   ├── INDEX.md           ← by subject, by tag, by topic
│   ├── routines.json      ← machine-readable
│   └── <slug>.md          ← one page per routine
├── sessions/              ← archived session transcripts
│   ├── INDEX.md
│   ├── <date>--<id>--<slug>.md    ← readable page (regenerated)
│   ├── <date>--<id>--<slug>.json  ← untruncated sidecar
│   └── reasoning/
│       └── <date>--<id>--<slug>.md  ← hand-written; the one irreplaceable file
├── inventory/
│   ├── box-inventory.md   ← 111 root items, classified
│   └── github-inventory.md
└── tools/
    ├── taxonomy.py        ← vocabulary + classifier (single source of truth)
    ├── redact.py          ← credential stripping; runs before anything is written
    ├── snapshot_routines.py
    ├── archive_session.py
    └── build_index.py
```

---

## Read this first: what could and could not be captured

The request was to archive everything in this environment, "particularly the
thought processes." Three findings shape what this archive actually contains.
They are stated plainly because two of them are losses, not features.

### 1. Reasoning text is not recoverable — the harness never writes it down

Session transcripts live at
`~/.claude/projects/<project-slug>/<session-id>.jsonl`. They do contain
`thinking` blocks. Those blocks look like this on disk:

```json
{"type": "thinking", "thinking": "", "signature": "CAISsAcKhwEIEBgCKkA0kQnn…"}
```

The `thinking` field is an **empty string**. Only an encrypted signature is
persisted. Across every reasoning block in this session, **none contained
recoverable text** — zero characters in total. Each session page reports its own
counts in the Volume table.

This is not a permissions problem or a missing tool — the raw reasoning is never
written to disk, so no tool can retrieve it after the fact. Any archive that
claimed to hold past reasoning traces would be fabricating them.

**What is done instead:** `archive_session.py` records that a reasoning block
occurred and where in the sequence it sat, marks it explicitly as unrecoverable,
and every session page carries a **`Reasoning log`** written deliberately —
decision, options considered, what settled it. Reasoning has to be captured as
it happens. It cannot be mined afterwards.

The log lives in `sessions/reasoning/<same-name>.md` and is inlined into the
page at render time. It is kept in a separate directory, not as a
`<page>.reasoning.md` sibling, because a rebuild that runs `rm sessions/*.md`
matches a sibling and destroys the one file in the archive that cannot be
regenerated. That happened once during this build; the directory is the fix.

### 2. Past sessions are gone — only the current one exists on disk

Claude Code on the web runs each session in an ephemeral container that is
reclaimed after inactivity. On this container, `~/.claude/projects/` holds
exactly **one** transcript: the session that built this archive. Nothing from
2026-05 through 2026-07-30 survived locally, and no API in this environment
serves historical transcripts.

**What survives from those sessions, and is archived here:**

| Surviving evidence | Where | What it tells you |
|---|---|---|
| Routine instructions | `routines/` | Precisely what ~15 recurring sessions are asked to do, verbatim |
| Box artifacts | `inventory/box-inventory.md` | What sessions produced, dated |
| Git commits and PRs | `inventory/github-inventory.md` | What landed, when, on which branch |
| `CLAUDE.md` session-history notes | both repos | Hand-written notes on three 2026-07-19 sync sessions |

That is the *residue* of the conversations, not the conversations. It answers
"what happened" well and "why" barely at all.

### 3. Routines are the strongest record — and they were nearly the only one

27 routines exist, 15 currently active. Their prompt text — some over 17,000
characters, containing accumulated corrections, recovery instructions and
rewritten objectives — is the richest surviving description of intent anywhere
in this environment. All of it is preserved verbatim in `routines/`, one page
each, classified.

They are also fragile: they live only in the scheduling service. A snapshot
belongs in version control, which is now what `routines/routines.json` is.

---

## Credentials: found, redacted, and needing rotation

Archiving the routine prompts surfaced something that was not part of the
request but cannot be left unsaid.

**Several routine definitions contain live credentials in plaintext**, pasted
into the instruction text when the routine was created. The snapshot run
redacted **70 occurrences** before writing anything:

| Kind | Occurrences | Where |
|---|---:|---|
| Deploy key / WordPress `X-Sourov-Key` | 40 | `Organise and create`, `Wp`, `Sync repos to wordpress site.` |
| Account usernames (FTP, database) | 14 | same |
| API keys | 6 | `AI concepts explainer`, `Content sync and human nature research` |
| FTP / database passwords | 5 | `Organise and create`, `Wp` |
| Google Ads client secret | 2 | `AI concepts explainer`, `Content sync and human nature research` |
| Google Ads developer token | 2 | same |

The archive is clean — a literal sweep for every known secret value and any
10-character-or-longer prefix of one returns nothing. But **redacting the copy
does nothing about the original.** Those secrets are still live in the routine
definitions on the scheduling service, they are visible to anyone who can read
the routine list, and they have been echoed into every session those routines
have ever run.

Recommended, in order:

1. **Rotate them all** — the WordPress deploy key, the FTP password, the
   database password, and the Google Ads client secret and developer token.
   Treat them as disclosed.
2. **Move the replacements out of prompt text** into environment variables on
   the environment the routines run in, and edit the routine prompts (via
   `update_trigger`, which preserves each routine's run history) to reference
   the variable instead of the value.
3. **Re-run `snapshot_routines.py`** afterwards so the archive reflects the
   cleaned prompts.

### How the redaction works

`tools/redact.py` runs on every string before it is written, in two passes:

1. **Harvest** — labelled patterns (`X-Sourov-Key:`, `Password:`, markdown
   table cells, `?key=` URL parameters, provider-shaped tokens like `ghp_…`)
   find the secret *values* across the whole corpus.
2. **Sweep** — each harvested value is replaced everywhere it appears, case
   insensitively, plus any prefix of it 10 characters or longer.

The second pass matters because the same key appears bare — on its own line, in
a URL, half-quoted in a grep pattern — where no label exists to match on.
Harvesting corpus-wide means a key labelled once in one routine is stripped from
every other routine that repeats it unlabelled.

Redaction keeps the surrounding key and substitutes only the value, as
`«REDACTED:deploy-key»`, so the page still reads correctly and the reader can
see that a credential was there. It never emits a hash or a prefix of the
original.

**If you add a tool that writes to this archive, route its output through
`redact()`.** That is the only thing standing between a pasted secret and a
public commit.

---

## Running it

Re-snapshot the routines (after adding, editing or disabling any):

```bash
# Fetch via the Claude Code Remote list_triggers tool, save the JSON, then:
python3 tools/snapshot_routines.py /path/to/triggers.json .
```

Archive a session before its container is reclaimed:

```bash
python3 tools/archive_session.py \
    ~/.claude/projects/<project-slug>/<session-id>.jsonl . \
    --title "what the session was about"
```

Rebuild the indexes after either:

```bash
python3 tools/build_index.py .
```

The tools are idempotent — re-running overwrites generated files and reapplies
every entry in `overrides.json`.

### Archiving a session that is still running

The transcript is written incrementally, so it can be archived mid-session; the
page will simply end where the session had reached. Re-run at the end to
capture the rest. Do it **before** ending the session — once the container is
reclaimed the `.jsonl` is gone.

---

## Classification

One subject, any number of topics, any number of tags. Ten subjects, 32 topics,
25 tags — all defined in `tools/taxonomy.py` and documented in
[`TAXONOMY.md`](TAXONOMY.md).

The classifier is a weighted keyword heuristic with word-boundary matching, and
titles count fourfold against bodies. It is right on most items and defensibly
wrong on a few; those few are corrected in `overrides.json`, where each
correction carries a written reason that gets rendered onto the item's page.
Four corrections are currently in force.

---

## Gaps this archive does not close

Stated so they are not mistaken for oversights:

- **No reasoning from before 2026-07-31.** Unrecoverable, per finding 1.
- **No conversational history from before 2026-07-31.** Unrecoverable, per
  finding 2.
- **Routine *outputs* are not linked to routine *runs*.** Box holds twelve
  Asia/India digests; the routine that generated them is archived; nothing
  connects a specific file to a specific run. Fixing that requires the routines
  themselves to write a run ID into what they produce.
- **Nothing captures this automatically.** Archiving a session is currently a
  manual step at the end of a session. Making it automatic needs either a
  `SessionEnd` hook or a scheduled routine — see below.

## Making capture automatic

The archive covers everything reachable today. To stop the same loss recurring,
one of these needs setting up:

1. **A `SessionEnd` hook** in `settings.json` that runs `archive_session.py`
   against the closing session's transcript and commits the result. Closest to
   automatic; the `session-start-hook` skill covers the mechanics.
2. **A routine** that re-runs `snapshot_routines.py` weekly so the routine
   catalogue never drifts from what is actually scheduled.
3. **A habit**: end substantial sessions by asking for the reasoning log to be
   filled in, then archive. Least infrastructure, and the only one that captures
   reasoning — which no amount of tooling can recover after the fact.
