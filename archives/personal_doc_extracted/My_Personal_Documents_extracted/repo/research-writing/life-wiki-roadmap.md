# Life Wiki Roadmap (Arch Linux + Android)

Generated: 2026-04-29  
Philosophy source: Karpathy “LLM Wiki” idea file (raw sources → wiki → schema)

## 0) What you’re trying to build (in one sentence)
A **personal external memory** that’s cheap to run, easy to capture into (especially on low energy days), and gets *automatically compiled* into a navigable wiki you can use to write/blog/teach/podcast.

## 1) Constraints (design for reality)
- **Low energy + fatigue:** the system must work even when you can only do “capture” and nothing else.
- **Memory issues:** retrieval must be dead-simple; you can’t rely on remembering where things are.
- **Low/no budget:** prefer local/offline + free tooling. Paid LLM calls should be optional and rare.
- **Privacy:** you’ve got deeply personal material. Design for **private-by-default** with an explicit path to publish sanitized outputs.

## 2) The core philosophy (system rules)
This is the “OS-level” mindset:

### Rule A — Raw is sacred
- Everything you capture goes into `raw/`.
- Raw files are **append-only / immutable**. Don’t “fix” them; add a follow-up.

### Rule B — Wiki is compiled
- The wiki is a separate layer of clean pages in `wiki/`.
- A single raw item may update many wiki pages.

### Rule C — Schema is the product
- A single file (`AGENTS.md`) defines:
  - folder structure
  - naming rules
  - page templates
  - ingest/query/lint workflows
- This is what keeps the system consistent across months.

### Rule D — Automation is default
- If a task repeats, you don’t “try harder” — you **script it** or schedule it.

## 3) Your hardware (what this enables)
From `hardware-report-windows.md`: i5-12450H, **16GB RAM**, RTX 3050 **4GB VRAM**.

Implications:
- You can run **small-to-medium local models** (especially quantized) for summarizing, linking, drafting.
- 4GB VRAM is tight for bigger models, but CPU inference on 16GB works for 3B/7B class models.
- You can also run **local transcription** for audio notes (good for low-energy capture).

## 4) Minimal repository layout (start simple)
Create ONE git repo (later you can split private/public):

```
life-wiki/
  AGENTS.md
  raw/
    inbox/
    journal/
    web/
    audio/
    photos/
  wiki/
    index.md
    log.md
    overview.md
    concepts/
    entities/
    themes/
    projects/
    outputs/
  tools/
    capture
    ingest
    lint
    publish
```

### What each folder is for
- `raw/inbox/`: *fast capture*. Anything goes here.
- `raw/journal/`: daily notes (text).
- `raw/web/`: clipped articles (markdown).
- `raw/audio/`: voice notes (m4a/wav).
- `raw/photos/`: photo projects and “memory anchors”.
- `wiki/index.md`: catalog (content-oriented navigation).
- `wiki/log.md`: append-only timeline (what happened when).
- `wiki/overview.md`: your evolving synthesis (what you believe now).
- `wiki/outputs/`: blog drafts, podcast scripts, YouTube outlines.

## 5) Android setup (capture-first, zero-friction)
Pick the simplest capture method that you will *actually use*:

### Option 1 (simple): Obsidian mobile + Syncthing
- Use Obsidian mobile to create notes directly inside `raw/inbox/` and `raw/journal/`.
- Install **Syncthing-Fork** on Android.
- Sync the `life-wiki/raw/` folder to your Arch machine.

### Option 2 (lighter): Markor + Syncthing
- Use Markor for super-fast plain markdown notes.
- Same Syncthing sync.

### Optional: Voice capture
- Record voice notes (any recorder) → save into the synced `raw/audio/` folder.
- Transcribe later on the laptop (automation section).

## 6) Arch Linux setup (the “compiler machine”)
Arch is where the wiki gets compiled.

### Core packages
- `git` (versioning)
- `ripgrep`, `fd`, `fzf` (fast search + navigation)
- `python` (glue scripts)
- `syncthing` (phone sync)

### Enable Syncthing (user service)
- Enable with systemd user services (so it runs even without root):
  - `systemctl --user enable --now syncthing.service`

### Make capture easy (one command)
Create a tiny command called `capture` that appends a timestamped note into `raw/inbox/`.
- The goal: *zero thinking required*.

## 7) The 3 automated loops (ingest / query / lint)

### Loop 1 — Ingest (compile raw → wiki)
Trigger: “new file arrived in `raw/inbox/`”

Output expectations:
- create/update a source summary page in `wiki/`
- update affected concept/entity/theme pages
- update `wiki/index.md`
- append to `wiki/log.md`

### Loop 2 — Query (answer → file back)
Trigger: you ask a question (or you ask for a blog/podcast draft).

Rule: **good answers get filed** into `wiki/outputs/` (so they don’t die in chat).

### Loop 3 — Lint (weekly health check)
Trigger: scheduled (weekly)

Checks:
- contradictions
- stale pages
- orphan pages
- missing pages for frequently mentioned concepts
- “open threads” that never got resolved

Output: a short report file (and a few concrete follow-up tasks).

## 8) LLM strategy (free-first, hybrid when needed)

### Best default (low-cost): local model for drafting + linking
Use a local runner (typical options on Arch):
- **Ollama** (easy local serving)
- **llama.cpp** (direct, efficient)

Model size guidance for your hardware:
- Start with **3B–7B instruct**, quantized (Q4-ish) for day-to-day work.
- Use bigger models only if it’s worth the time cost.

### Occasional “deep synthesis”
If you ever use a paid model, reserve it for:
- merging 10+ sources into one coherent synthesis
- writing polished long-form outputs
- hard reasoning tasks

## 9) Privacy & publishing (two-lane workflow)
Because personal history + health notes can be sensitive:

### Lane A — Private vault (default)
- everything raw
- mental health / trauma / family details
- unfiltered journal

### Lane B — Publish vault (curated)
- sanitized essays
- lessons learned
- book notes that don’t expose personal details

Mechanically:
- publish is **export**, not “the same repo”.
- simplest approach: a second git repo that you copy selected `wiki/outputs/` pages into.

## 10) Automation points (systemd timers + file watching)
These are the “system-level” hooks that make it *live around you*.

### A) Auto-ingest when inbox changes
- Use a systemd **user path unit** watching `raw/inbox/`.
- When a new file appears: run `tools/ingest`.

### B) Daily digest
- A daily timer runs:
  - summarize what was captured today
  - write `wiki/daily-digest/YYYY-MM-DD.md`

### C) Weekly lint
- A weekly timer runs `tools/lint` and writes a report.

### D) Auto-commit
- After ingest/lint, auto-commit with messages like:
  - `ingest: 2026-04-29 inbox sweep`
  - `lint: weekly wiki health check`

## 11) Roadmap (do this in phases)

### Phase 0 (today): make capture real
- Create the repo + folders.
- Set up Syncthing between Android and Arch.
- Create **one** capture habit:
  - text note OR voice note.

### Phase 1 (week 1): index + log
- Create `wiki/index.md` + `wiki/log.md`.
- Do manual ingest (no automation yet).
- Prove you can retrieve information later.

### Phase 2 (week 2–3): local “compiler”
- Install local LLM runner.
- Implement an `ingest` tool that:
  - reads one raw file
  - updates wiki pages
  - updates index + log

### Phase 3 (month 1): publishing pipeline
- Add `tools/publish` to export selected outputs.
- GitHub Actions builds a static site (optional).

### Phase 4 (later): your 5 requested modules
Map your interests into “skills” (agent workflows) you can reuse:
- `/doc-coauthoring`: turn wiki pages → blog/podcast/video scripts in `wiki/outputs/`
- `/algorithmic-art`: maintain p5.js art + essays about process
- `/skill-creator`: create skills that operate on your vault deterministically
- `/mcp-builder`: expose `search_wiki`, `get_page`, `write_page`, `ingest` as MCP tools
- `/internal-comms`: family/team comms pages + decision logs (lightweight)

## 12) Next concrete actions (from this folder)
- Download the original Karpathy idea file (without copy/paste):
  - On Arch: run `download-karpathy-llm-wiki.sh`
  - On Windows: run `download-karpathy-llm-wiki.ps1`
- Already saved here as `llm-wiki-original-karpathy.md`.
- Read your hardware summary in `hardware-report-windows.md`.
- Copy the ready scaffold `life-wiki-template/` onto your Arch machine as `~/life-wiki/`.
- Then follow Phase 0.

---

Template note: A starter scaffold already exists in this workspace at `life-wiki-template/` (includes `AGENTS.md`, `wiki/index.md`, `wiki/log.md`, and `tools/capture.sh`).