*Authored during the session. This file exists because the transcript's own
reasoning blocks are empty — see the capture gap note on the session page.
Everything here is a deliberate written record, not a recovered one. It is
inlined into the session page at render time and is never overwritten by
regeneration.*

### Establish what exists before designing anything

The request assumed a body of chat history was sitting somewhere retrievable.
That had to be tested before building a container for it. Four things were
checked in parallel: the filesystem for transcripts, `.claude.json` for a prompt
history, the routine service, and Box.

The filesystem search found exactly one transcript —
`~/.claude/projects/-home-user/5bff9b21-….jsonl`, this session. `.claude.json`
turned out to hold only feature flags and account state; it has no `projects`
key and therefore no prompt history. So the premise did not hold: there was no
back catalogue to archive.

**What settled the shape of the work:** if the history is gone, the deliverable
has to be (a) everything that *is* reachable, classified properly, and (b)
machinery so the loss stops recurring. Building only (a) would have handed back
a snapshot that goes stale the moment the container is reclaimed.

### The reasoning capture problem

The transcript does contain `thinking` blocks, which initially looked like the
answer to "particularly your thought processes." Inspecting them showed
`"thinking": ""` with a populated `signature` — every block, zero characters of
recoverable text.

Options considered:

1. **Reconstruct reasoning from tool-call sequences.** Rejected. It would be
   inference presented as record, and an archive whose reasoning section is
   plausible fiction is worse than one that admits the gap.
2. **Report the gap and stop.** Rejected as too little — the request is
   satisfiable in substance even if not literally.
3. **Record position and absence, and write reasoning deliberately.** Chosen.
   Every unrecovered block is marked in place, and each session page carries a
   reasoning log written by hand. This file is that mechanism used on itself.

Consequence worth noting: because reasoning must be written *during* a session,
it cannot live inside a page that regenerates from the `.jsonl`. First attempt
kept it in the page and parsed it back out on re-run — workable, but one bad
edit away from destroying the only irreplaceable content in the archive. Moved
to a separate sidecar file, which the page inlines at render time.

That turned out not to be enough on its own. The sidecar was first named
`<page>.reasoning.md` and sat next to the page — and a routine
`rm sessions/*.md` during a rebuild matched the glob and deleted it. The fix was
structural rather than a resolution to be careful: sidecars now live in
`sessions/reasoning/`, where no glob over the session pages can reach them.
Worth recording as a small lesson — "keep it in a different file" is only a real
safeguard once the file is somewhere the destructive command cannot name.

### Credentials, found mid-build

Staging the archive for commit, a routine pre-commit scan for secret-shaped
strings hit. The routine prompts carry live credentials pasted inline: a
WordPress deploy key, an FTP password, database credentials, a Google Ads client
secret and developer token. Committing the archive as generated would have
published them.

Three iterations were needed before the archive was actually clean, and each
failure was informative:

1. **Labelled patterns only.** Caught `X-Sourov-Key: …` and `Password: …`,
   missed the same key in markdown table cells, in `?key=` URL parameters, and
   bare on its own line.
2. **More patterns.** Diminishing returns immediately — the bare occurrence has
   no syntactic marker at all, so no pattern can find it. Restructured to
   harvest-then-sweep: patterns find the *values*, then every value is replaced
   everywhere it appears, corpus-wide. A key labelled once in one routine is
   then stripped from every routine that repeats it unlabelled.
3. **Prefixes still leaked.** A grep pattern quoting the first half of a key
   left that half in the transcript. Added prefix sweeping at 10 characters or
   longer — 10 rather than 8 so git short-SHAs are not caught by accident.

Also worth flagging: the first draft of `redact.py` used the real secrets as
illustrative examples in its own docstring. Caught on the verification sweep and
replaced with dummies. The verification step earned its place.

The redaction protects the archive. It does nothing for the originals, which are
still live on the scheduling service — hence the rotation recommendation in the
README and at the top of the PR rather than buried in a footnote.

### Why routines became the centrepiece

27 routines came back from `list_triggers`, several with prompts over 11,000
characters — one at 17,642. Reading them, they are not simple task
descriptions: they carry accumulated corrections, recovery instructions for
deleted files, and in one case ("Content sync and human nature research") an
explicit `This instruction bellow is old one: new objectives:` header layered
over a superseded block.

That makes them the richest surviving statement of intent in the environment,
and they live only in the scheduling service. Committing
`routines/routines.json` to version control was therefore not a nice-to-have.

### Classifier: three corrections during the build

The first classification pass was visibly wrong, and each fix generalised.

1. **Substring matching was firing on fragments.** `ci` matched inside "social"
   and "efficient", `raw` inside "drawn", `box` inside "boxes". Nearly every
   routine was picking up `pr-and-ci-hygiene`. Fixed with alphanumeric word
   boundaries, built to still allow multi-word and punctuated needles like
   `dev.to` and `.mm`.

2. **Bodies were drowning out titles.** "Mental health research auditor" filed
   under Content Publishing because its prompt names WordPress a dozen times —
   WordPress is where its output *lands*, not what it is *about*. Fixed by
   weighting title hits fourfold. The same change corrected "Content strategy
   research" and "back up".

3. **Some items are genuinely cross-cutting.** After the first two fixes, four
   remained debatable. Rather than keep bending weights — where fixing one item
   breaks three — an `overrides.json` layer was added. Each override records a
   written reason that renders onto the item's page next to the subject it
   replaced, so a hand correction is visible rather than silent.

The general principle applied: tune the heuristic while the fixes generalise,
then stop and make the remaining exceptions explicit.

### Why the archive is not mirrored into free_education

Both repositories were in scope. Mirroring the archive into both was considered
and rejected: several routines write to both repos, so a mirrored copy means
either filing those routines twice or letting the two copies drift. Single
source of truth in `my_professional_documents`, with a pointer document in
`free_education` that records what the archive holds *about* that repo — its
inventory entry, the four routines targeting it, its subject mapping.

### What was deliberately not done

- **No attempt to reach other repositories or accounts.** Scope was the two
  in-scope repos and the connected services.
- **No cleanup of the defects found.** The 12-byte failed HTML upload, the five
  files tracked with a literal leading double-quote in their names, the
  duplicate `(1)` scripts in `python_toolkit/`, the twelve Asia/India digests
  under six different naming conventions — all recorded in the inventories, none
  touched. They are real problems, but they are not archival work, and silently
  reorganising a repository during an archive job is the wrong call to make
  unasked.
- **No automatic capture installed.** A `SessionEnd` hook is the right long-term
  answer and is written up in `README.md`, but it changes harness behaviour on
  every future session — that is a decision to take explicitly, not a side
  effect of asking for an archive.
