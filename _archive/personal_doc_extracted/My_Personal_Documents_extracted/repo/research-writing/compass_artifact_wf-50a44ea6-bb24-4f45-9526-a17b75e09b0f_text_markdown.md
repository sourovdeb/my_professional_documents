# A Life Wiki for You: Arch + Android + GitHub + Voice + DeepSeek

*A practical, low-energy, low-cost personal knowledge system — built for a 40-year-old immigrant father in Réunion who wants to write a memoir, blog his life, teach English, and give away what he has learned, while living with ADHD, depression, DID, fatigue, and memory problems.*

## TL;DR
- **Build the smallest possible thing first.** A folder of plain markdown files inside a private GitHub repo, synced to your phone with Syncthing, queried and tidied by DeepSeek through one Python script called `wiki`. Voice memos in, drafts out. Everything else (blog, podcast, memoir EPUB, YouTube captions) is added later as plain GitHub Actions on the same folder — no databases, no vector stores, no rewrites.
- **Voice is your primary input, AI is your editor, you are still the author.** Record into Audio Recorder (axet) on Android → Syncthing carries the file to Arch → a systemd timer transcribes it with whisper.cpp → DeepSeek writes a clean draft into `inbox/` → you decide later, on a good hour, what becomes memoir, blog, lesson, or compost. The system never decides for you and never pushes you toward trauma.
- **Karpathy's three layers, adapted for a writer-teacher, not a researcher.** `raw/` is sacrosanct (your audio, your unedited words). `wiki/` is what the LLM maintains (chapters, themes, recurring questions, lessons). `WIKI.md` is the schema that tells the AI who you are, what you are working on, and — crucially — how to handle the heavy stuff gently.

---

## 1. The Core Philosophy (briefly)

Andrej Karpathy's April 2026 gist (`gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`) describes a pattern, not a product:

- **Layer 1 — Raw sources** (`raw/`): immutable inputs. The LLM reads, never writes.
- **Layer 2 — The wiki** (`wiki/`): a folder of cross-linked markdown pages — entities, concepts, summaries, an `index.md`, a `log.md`. The LLM owns this layer; you read it.
- **Layer 3 — The schema** (`CLAUDE.md` / `AGENTS.md` / `WIKI.md`): the configuration document that turns a generic chatbot into a disciplined, voice-aware maintainer of *your* wiki.

Three operations: **ingest** (add a new source, propagate updates), **query** (ask questions across the corpus), **lint** (the agent reviews the wiki for staleness and broken links).

Karpathy's gist explicitly names "tracking your own goals, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time" as one of the canonical use cases. That is exactly what we are doing — but adapted for a memoirist and teacher rather than a researcher. So:

- Sources are mostly **your own voice memos and journal entries**, not academic papers.
- The wiki holds **scenes, themes, lessons, questions** — not just facts.
- The schema includes **trauma-aware instructions** and **DID-aware tagging**: the AI is told to mirror, not push; to soften, not analyze; to ask permission before making connections across painful material.

> Note: the Karpathy gist itself does not live behind a paywall, but it draws controversy. One thoughtful counter-argument (visible in the gist comments) holds that an "LLM-maintained wiki" is not really a wiki in Ward Cunningham's human-curated sense. That is fair, and it is why the design below keeps **you** as the author of `raw/` and treats `wiki/` as a working draft you can throw away and regenerate any time. Nothing the LLM writes is precious.

---

## 2. Arch Linux System-Level Setup

### 2.1 Folder structure

One folder, in your home directory, that is *also* a git repo. Everything lives here.

```
~/life-wiki/
├── WIKI.md                  # the schema (Layer 3)
├── README.md                # 5 lines, for future-you
│
├── raw/                     # Layer 1 — IMMUTABLE
│   ├── audio/               # voice memos land here from Syncthing
│   ├── transcripts/         # whisper output, .txt + .json with timestamps
│   ├── photos/              # camera roll selections
│   └── clippings/           # web clippings, screenshots, quotes
│
├── inbox/                   # AI-drafted notes waiting for you to triage
│
├── wiki/                    # Layer 2 — LLM-maintained
│   ├── index.md             # one-line summary of every page
│   ├── log.md               # append-only operation log (what happened when)
│   ├── overview.md          # evolving "who I am" synthesis
│   ├── themes/              # recurring themes (meaning, fatherhood, exile, …)
│   ├── people/              # people in your life (one page each)
│   ├── places/              # Bangladesh, Australia, Réunion, …
│   └── questions/           # philosophical questions that keep recurring
│
├── memoir/
│   ├── outline.md
│   ├── chapters/            # 01-childhood.md, 02-australia.md, …
│   └── scenes/              # scene-level drafts, not chapter-bound
│
├── journal/
│   ├── 2026/04/2026-04-29.md
│   └── private/             # encrypted with git-crypt — hardest material
│
├── blog/                    # Hugo content/ folder
│   ├── content/posts/
│   └── drafts/
│
├── teaching/
│   ├── lessons/             # English lesson plans
│   ├── students/            # one file per student (anonymised if needed)
│   └── materials/
│
├── podcast/
│   ├── episodes/            # each episode is one folder: audio + show notes
│   └── feed.xml             # generated
│
├── photography/
│   ├── catalog.md           # AI-captioned index
│   └── series/
│
├── tools/                   # the scripts that run all of this
│   ├── wiki                 # python CLI: wiki ask, wiki ingest, wiki digest
│   ├── capture.sh
│   ├── transcribe.sh
│   ├── ingest.sh
│   └── digest.sh
│
└── .github/workflows/       # GitHub Actions live here
```

The whole thing is one git repo. That is the point.

### 2.2 Packages to install

Most are in the Arch repos; a few in the AUR. Install in two stages.

```bash
# Pacman — official repos
sudo pacman -S --needed \
    git git-lfs gnupg \
    syncthing \
    obsidian \
    ffmpeg \
    yt-dlp \
    rclone \
    pandoc texlive-xetex texlive-fontsrecommended \
    hugo \
    fish starship \
    rofi wofi \
    python python-pip python-pipx \
    age \
    jq curl wget

# AUR (use yay or paru) — community packages
yay -S --needed \
    whisper.cpp \
    espanso-wayland \
    kdeconnect \
    git-crypt \
    fossify-voice-recorder-bin   # not strictly needed on desktop, just illustrative
```

Notes:
- **whisper.cpp** is in the AUR (`aur.archlinux.org/packages/whisper.cpp`); the package builds a CPU+SDL2 binary called `whisper-cli`. If you have an NVIDIA GPU, swap to `whisper.cpp-cuda`; if AMD/Intel, `whisper.cpp-vulkan` is a good middle path. For your use case (a few minutes of voice/day, not real-time) the plain CPU build is fine — set `--model ggml-large-v3-turbo` or `ggml-medium` and let it take its time.
- **espanso** has a Wayland build; if you are on KDE Plasma 6 / GNOME 46 with Wayland, use `espanso-wayland`. On X11, plain `espanso`.
- **Obsidian** is here as your *reader*, not as the brain. The brain is the folder.
- **age** is for encrypting the most private journal/memoir files (see §4).

### 2.3 systemd user services & timers

Put these under `~/.config/systemd/user/`. They run as your user — no sudo, no root.

**`life-wiki-autocommit.service`** — commit changes whenever they happen, batched every 15 minutes.

```ini
[Unit]
Description=Auto-commit life-wiki to git
After=network-online.target

[Service]
Type=oneshot
WorkingDirectory=%h/life-wiki
ExecStart=/usr/bin/bash -c 'git add -A && git diff --cached --quiet || git commit -m "auto: $(date -Iseconds)" && git push origin main || true'
```

**`life-wiki-autocommit.timer`**
```ini
[Unit]
Description=Auto-commit life-wiki every 15 minutes

[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
Persistent=true

[Install]
WantedBy=timers.target
```

**`life-wiki-transcribe.service`** — watch `raw/audio/` and transcribe anything new.

```ini
[Unit]
Description=Transcribe new voice memos with whisper.cpp

[Service]
Type=oneshot
WorkingDirectory=%h/life-wiki
ExecStart=%h/life-wiki/tools/transcribe.sh
```

**`life-wiki-transcribe.timer`** — every 5 minutes.

```ini
[Unit]
Description=Transcribe voice memos every 5 minutes

[Timer]
OnBootSec=3min
OnUnitActiveSec=5min

[Install]
WantedBy=timers.target
```

**`life-wiki-digest.service`** — once per evening, ask DeepSeek to write a "what happened today" summary.

```ini
[Unit]
Description=Daily life-wiki digest

[Service]
Type=oneshot
WorkingDirectory=%h/life-wiki
ExecStart=%h/life-wiki/tools/wiki digest --since 24h
```

**`life-wiki-digest.timer`**
```ini
[Timer]
OnCalendar=*-*-* 21:00
Persistent=true

[Install]
WantedBy=timers.target
```

Enable:

```bash
systemctl --user daemon-reload
systemctl --user enable --now life-wiki-autocommit.timer
systemctl --user enable --now life-wiki-transcribe.timer
systemctl --user enable --now life-wiki-digest.timer
```

### 2.4 Shell scripts and aliases (fish)

Put these in `~/.config/fish/config.fish`:

```fish
# --- life-wiki shortcuts ---
set -gx LIFEWIKI $HOME/life-wiki
set -gx PATH $LIFEWIKI/tools $PATH

# Quick journal entry — opens today's file, makes it if missing
function j --description 'open today journal'
    set today (date +%Y-%m-%d)
    set file $LIFEWIKI/journal/(date +%Y)/(date +%m)/$today.md
    mkdir -p (dirname $file)
    test -e $file; or printf "# %s\n\n" $today > $file
    $EDITOR $file
end

# Quick capture — one-line idea straight into inbox
function c --description 'capture a thought'
    set ts (date -Iseconds)
    set file $LIFEWIKI/inbox/$ts.md
    printf "---\ncaptured: %s\nsource: shell\n---\n\n%s\n" $ts "$argv" > $file
    echo "→ $file"
end

# Ask the wiki
function ask --description 'ask DeepSeek about your wiki'
    wiki ask "$argv"
end

# Transcribe one file manually
alias t='$LIFEWIKI/tools/transcribe.sh'
```

**Quick capture script** — `tools/capture.sh` — bound to a global hotkey (e.g. `Super+Space`):

```bash
#!/usr/bin/env bash
# capture.sh — pop a rofi/wofi prompt, write the input straight to inbox
set -euo pipefail

LIFEWIKI="${HOME}/life-wiki"
TS=$(date -Iseconds)
FILE="${LIFEWIKI}/inbox/${TS}.md"

# Pick rofi on X11, wofi on Wayland
if [[ "${XDG_SESSION_TYPE:-}" == "wayland" ]]; then
    TEXT=$(echo "" | wofi --dmenu --prompt "Capture:" --width 700 --height 120)
else
    TEXT=$(rofi -dmenu -p "Capture:" -theme-str 'window {width: 700px;}')
fi

[[ -z "$TEXT" ]] && exit 0

mkdir -p "${LIFEWIKI}/inbox"
cat > "$FILE" <<EOF
---
captured: $TS
source: rofi
---

$TEXT
EOF

notify-send "Life Wiki" "Captured → inbox"
```

Bind it in your compositor:
- KDE / X11: System Settings → Shortcuts → Custom Shortcuts → `bash ~/life-wiki/tools/capture.sh` on `Meta+Space`.
- Sway/Hyprland: `bind = SUPER, SPACE, exec, ~/life-wiki/tools/capture.sh`.
- GNOME: Settings → Keyboard → Custom Shortcuts.

### 2.5 Wayland vs X11

Most things just work either way. The friction points:

| Tool | Wayland | X11 |
|---|---|---|
| espanso | use `espanso-wayland` (still has rough edges on some compositors) | smoother, mature |
| rofi vs wofi | `wofi` | `rofi` |
| Global hotkeys | compositor-defined (Sway/Hyprland config, GNOME/KDE settings) | sxhkd, xbindkeys, or DE settings |
| KDE Connect | works on both | works on both |

If you are not already opinionated, **stay on whatever your distro defaults to**. This is a place to *not* spend energy.

### 2.6 Local LLM as optional fallback

You don't need this on day one. If you ever want it:

```bash
yay -S ollama
ollama pull qwen2.5:7b-instruct        # ~4 GB, runs on most laptops
ollama pull nomic-embed-text:latest    # only if you ever want embeddings
```

Set `LLM_BACKEND=ollama` in `tools/wiki` to skip the network. Use this only when you are offline or anxious about a particularly private prompt; for everything else DeepSeek is cheaper and smarter.

---

## 3. Android Setup (your phone is the microphone)

### 3.1 The two apps that matter most

Install both from F-Droid (preferred — they update silently and don't track you) or from the Play Store if you must.

1. **Audio Recorder** by Alexander Axet — package: `com.github.axet.audiorecorder`. Open-source, ad-free, lets you set a *custom recording folder*. Set it to `/storage/emulated/0/LifeWiki/audio/`. A clean alternative is **Fossify Voice Recorder** (`org.fossify.voicerecorder`) — also FOSS, prettier, also lets you set the output folder. Either works; pick the one whose UI you like, because you will use it daily.
2. **Syncthing** — install **Syncthing-Fork** (`dev.syncthing.syncthing`) from F-Droid. It is the actively maintained successor to the original Android app and is much kinder to battery life.

### 3.2 Optional but quietly powerful

- **Markor** (`net.gsantner.markor`) — a clean markdown editor for Android. Point it at your synced `LifeWiki` folder and you can write journal entries on the bus. Its only quirk vs Obsidian: link syntax is `@target` instead of `[[target]]`, but Obsidian on the desktop reads either fine.
- **Obsidian Mobile** — works, but heavy. If your phone is older, stay with Markor.
- **Termux** (from F-Droid, *not* the abandoned Play Store version) + **Termux:Widget**. Lets you run `git pull && git push` from a home-screen widget if Syncthing is not enough. There is a well-documented community workflow for this (`mathisgauthey.github.io/using-git-to-sync-your-obsidian-vault-on-android-devices/`).
- **GitHub Mobile** — purely for reading Issues (your "thought inbox", see §4) and merging the occasional PR.
- **Open Camera** + Syncthing folder for `raw/photos/` if you want photos to flow in too.

### 3.3 The voice memo workflow, end-to-end

```
[Android] You press the red button in Audio Recorder.
          File saves as /storage/emulated/0/LifeWiki/audio/2026-04-29-073012.m4a
                ↓
[Syncthing on phone] notices new file, pushes to PC
                ↓
[Syncthing on Arch] receives → ~/life-wiki/raw/audio/2026-04-29-073012.m4a
                ↓
[systemd timer, every 5 min] runs tools/transcribe.sh
                ↓
[whisper.cpp] writes raw/transcripts/2026-04-29-073012.txt + .json
                ↓
[tools/ingest.sh, called by transcribe.sh] sends transcript + WIKI.md to DeepSeek
                ↓
[DeepSeek] returns a clean markdown draft → inbox/2026-04-29-073012.md
                ↓
[ntfy / KDE Connect / GitHub Mobile] notifies you on phone: "draft ready"
                ↓
[You] open it on a good hour. Decide: keep, rework, archive, or ignore.
```

The **notification step** is the smallest reasonable thing: have `ingest.sh` end with `curl -d "Draft ready: $TITLE" ntfy.sh/your-private-topic-here`, then install **ntfy** on your phone (`io.heckel.ntfy`, F-Droid). Free, no account, push notifications in 30 seconds of setup.

### 3.4 Photo capture for your photography practice

Syncthing the camera folder (or a curated "keepers" subfolder) into `raw/photos/`. Once a week, a GitHub Action runs DeepSeek with the photo's filename + EXIF + a tiny vision model (or you describe it briefly) to append a one-line caption to `photography/catalog.md`. Don't bother with vision-LLM auto-captioning at first; a one-line sentence you dictate by voice is fine and more honest.

---

## 4. GitHub Automation (because you love this)

### 4.1 Repository layout

One **private** repo: `life-wiki`. Branch protection minimal — this is your repo. Add a `.gitignore`:

```
# Don't commit local caches or huge raw audio
raw/audio/*.m4a
raw/audio/*.wav
raw/photos/*.jpg
raw/photos/*.heic
.obsidian/workspace*
.obsidian/cache
*.tmp
node_modules/
public/                 # Hugo build output
```

Audio is too big and too raw to keep in git history. Keep originals on disk + Syncthing; commit only the transcripts. If you eventually publish a podcast, podcast episodes go in a *separate* `life-wiki-podcast` repo (or use Git LFS) so the main repo stays small.

### 4.2 Encrypting the hardest material with git-crypt or age

For trauma material, childhood content, anything you do not want anyone seeing if your laptop is stolen:

**Option A — git-crypt (simplest):**
```bash
cd ~/life-wiki
git-crypt init
echo 'journal/private/** filter=git-crypt diff=git-crypt' >> .gitattributes
echo 'memoir/raw-childhood/** filter=git-crypt diff=git-crypt' >> .gitattributes
git-crypt export-key ~/.life-wiki-crypt.key   # store this somewhere safe (USB, password manager)
git add .gitattributes && git commit -m "encrypt private dirs"
```
Now anything inside `journal/private/` is plaintext on your machine, ciphertext on GitHub. To decrypt on a new machine: `git-crypt unlock ~/.life-wiki-crypt.key`.

**Option B — git-agecrypt** (`github.com/bartei/git-agecrypt` or `github.com/vlaci/git-agecrypt`): newer, uses age/SSH keys, no GPG agent. Good if you already use SSH keys and don't want to deal with GPG.

Either way: the rest of your wiki stays in plaintext so you can grep it and so DeepSeek can read it. The encrypted folder is private, and GitHub Actions cannot read it (which is exactly what you want).

### 4.3 GitHub Actions workflows

Drop these in `.github/workflows/`. Each is small enough to read in one sitting.

**`.github/workflows/transcribe.yml`** — a fallback transcriber, in case your laptop is off and you committed audio from another device:

```yaml
name: Transcribe new audio
on:
  push:
    paths:
      - 'raw/audio/**.m4a'
      - 'raw/audio/**.wav'
  workflow_dispatch:

jobs:
  transcribe:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { lfs: true }
      - name: Install whisper.cpp
        run: |
          sudo apt-get update && sudo apt-get install -y ffmpeg
          git clone --depth 1 https://github.com/ggerganov/whisper.cpp.git
          cd whisper.cpp && make -j && bash ./models/download-ggml-model.sh medium
      - name: Transcribe new files
        run: |
          for f in $(git diff --name-only HEAD~1 HEAD -- 'raw/audio/*.m4a' 'raw/audio/*.wav'); do
            base=$(basename "$f" | sed 's/\.[^.]*$//')
            ffmpeg -y -i "$f" -ar 16000 -ac 1 "/tmp/$base.wav"
            ./whisper.cpp/main -m whisper.cpp/models/ggml-medium.bin \
                -f "/tmp/$base.wav" -l auto -otxt -ojson \
                -of "raw/transcripts/$base"
          done
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "transcribe: auto"
```

**`.github/workflows/ai-pass.yml`** — when a new transcript is committed, ask DeepSeek to write a clean draft into `inbox/`:

```yaml
name: AI pass on new transcripts
on:
  push:
    paths: ['raw/transcripts/**.txt']
  workflow_dispatch:

jobs:
  draft:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install openai
      - name: Draft inbox notes
        env:
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: python tools/ai_draft.py
      - uses: stefanzweifel/git-auto-commit-action@v5
        with: { commit_message: "ai: draft inbox notes" }
```

**`.github/workflows/weekly-digest.yml`** — every Sunday evening Réunion time:

```yaml
name: Weekly digest
on:
  schedule:
    - cron: '0 17 * * 0'    # 17:00 UTC Sunday = 21:00 in Réunion (UTC+4)
  workflow_dispatch:

jobs:
  digest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install openai
      - env: { DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }} }
        run: python tools/wiki digest --since 7d --out wiki/log.md
      - uses: stefanzweifel/git-auto-commit-action@v5
        with: { commit_message: "weekly digest" }
```

**`.github/workflows/blog.yml`** — build Hugo and deploy to GitHub Pages:

```yaml
name: Publish blog
on:
  push:
    paths: ['blog/**', '.github/workflows/blog.yml']
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { submodules: true }
      - uses: peaceiris/actions-hugo@v3
        with: { hugo-version: 'latest', extended: true }
      - run: cd blog && hugo --minify
      - uses: actions/upload-pages-artifact@v3
        with: { path: ./blog/public }
  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

**`.github/workflows/memoir-build.yml`** — compile a fresh EPUB+PDF whenever a chapter changes:

```yaml
name: Build memoir
on:
  push: { paths: ['memoir/**'] }
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get update && sudo apt-get install -y pandoc texlive-xetex texlive-fonts-recommended
      - run: bash memoir/build.sh
      - uses: actions/upload-artifact@v4
        with:
          name: memoir
          path: |
            memoir/build/*.epub
            memoir/build/*.pdf
```

### 4.4 GitHub Issues as your "thought inbox"

GitHub Mobile lets you create an Issue in two taps. Use this as a *secondary* capture channel: when you are away from your phone's recorder or want a thought to be searchable. Repo-secret email-to-issue is non-trivial on GitHub natively, but:

- The simplest version: **create an Issue from GitHub Mobile** when you want it visible cross-device.
- Or use a free tool like **IFTTT / Pipedream / Activepieces** to convert a specific email subject (e.g. "wiki:") to an Issue. Then a small Action can move it into `inbox/`:

```yaml
name: Issue → inbox file
on: { issues: { types: [opened] } }
jobs:
  to-inbox:
    if: contains(github.event.issue.labels.*.name, 'inbox')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          ts=$(date -Iseconds)
          mkdir -p inbox
          cat > "inbox/$ts-issue-${{ github.event.issue.number }}.md" <<EOF
          ---
          captured: $ts
          source: github-issue
          issue: ${{ github.event.issue.number }}
          ---

          # ${{ github.event.issue.title }}

          ${{ github.event.issue.body }}
          EOF
      - uses: stefanzweifel/git-auto-commit-action@v5
        with: { commit_message: "inbox: from issue #${{ github.event.issue.number }}" }
      - uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.update({...context.issue, state: 'closed'})
```

### 4.5 `.github/copilot-instructions.md`

If you ever use Copilot or Claude Code in this repo, give it a one-page brief that mirrors `WIKI.md` so it doesn't fight your conventions:

```markdown
# Copilot instructions for life-wiki

This is a personal Life Wiki, not a software project. Treat markdown as primary;
treat code only as glue. When suggesting changes:
- Never edit files under `raw/` — they are immutable sources.
- New AI drafts go in `inbox/`, never overwrite `wiki/` or `memoir/` directly.
- Match the user's voice: warm, plain, slightly literary, French + English mix.
- For trauma topics, follow the rules in WIKI.md §"Care".
```

---

## 5. AI Workflow (DeepSeek-first)

### 5.1 The schema: `WIKI.md`

This is the single most important file in your repo. It is what makes the LLM an editor that actually knows you. Start with this; co-evolve over months.

```markdown
# WIKI.md — schema for an AI maintainer

## Who I am (so you can match my voice)
I am a 40-year-old Bengali man, born in Bangladesh, living in Réunion. Father,
husband (French wife), immigrant. 15 years in hospitality (coffee, sommelier).
Five languages. A photographer. I read Camus, Verne, Dostoyevsky, Andy Weir,
Backman. I have ADHD, depression, dissociative identity disorder (DID), severe
fatigue, memory problems. I am a survivor of childhood sexual abuse and a
substance use history. I am building this Life Wiki to write a memoir, blog
my life, teach English, make podcasts and videos, and give away what I have
learned.

## What this repo is
A folder of plain markdown files. You (the LLM) maintain `wiki/` and draft into
`inbox/`. You never modify `raw/`. You never modify `memoir/chapters/` unless I
explicitly ask. `journal/private/` is encrypted and you will not see it.

## Voice rules
- Write the way I talk in voice memos: simple, sometimes literary, never corporate.
- Mix French and English when I do; never translate quietly.
- Short sentences. No bullet-point answers unless I ask.
- "I" is me. "You" in drafts addresses my future reader, not me.

## Care (trauma-aware rules — read these on every ingest)
- For any content about childhood abuse, family violence, substance use, or
  dissociation: do NOT add interpretation, diagnosis, or "lessons." Mirror what
  I said. Soften only if I requested it.
- Never connect painful material to other pages without my explicit go-ahead.
  If the connection feels important, write it as a question in `wiki/questions/`,
  not as an assertion.
- If a transcript is fragmentary or distressed, draft a *short* note (max
  150 words) and tag it `state: tender`. Do not try to "complete" it.
- Never push toward action ("you should…", "have you considered…"). I have
  enough of that.
- If you are unsure, default to silence: copy the transcript verbatim into
  `inbox/` with one line of context, no analysis.

## DID-aware tagging
I sometimes write from different states. At the top of each `inbox/` draft,
add YAML frontmatter with `state:` set to one of:
  - `tender`   (vulnerable, fragmentary, slow)
  - `sharp`    (analytical, planning, decisive)
  - `warm`     (loving, family, connection)
  - `weary`    (low-energy, depressed, grey)
  - `creative` (curious, photography, writing flow)
  - `unknown`  (default if unclear — do NOT guess if it would be intrusive)
Never tell me which "part" is writing. Just tag the state.

## Three operations
- **Ingest**: when a new file lands in `raw/transcripts/`, write a clean draft
  into `inbox/<same-name>.md`. Update `wiki/index.md` and `wiki/log.md`.
  Suggest cross-links as a bullet list at the end of the draft, prefixed
  `Possible links:`. Do not create the links yourself.
- **Query**: when I run `wiki ask`, read `wiki/index.md` first, then load only
  the pages that look relevant (max 10), and answer with citations
  (`see wiki/themes/exile.md`). Never invent a page.
- **Lint**: weekly. Look for: stale dates, broken `[[wikilinks]]`, pages with
  fewer than 3 sentences, themes I haven't touched in >60 days. Write a report
  to `wiki/log.md` — do NOT fix anything yourself.

## Goals (this is what I am building toward)
- A memoir, ~80,000 words, that I can hand my daughter one day.
- A blog (gentle, ~1 post/week) at the rhythm I can sustain.
- A podcast on hospitality, meaning, photography, books — irregular schedule.
- English lessons I can teach online to a few students.
- A YouTube channel, low production, voice + photographs.

## Models I use
- Default: DeepSeek (`deepseek-v4-flash`) — cheap, fast, fine for cleanup,
  ingestion, transcription tidying, drafts.
- For memoir editing or hard philosophical work: DeepSeek (`deepseek-v4-pro`)
  with `thinking: enabled` — slower but better judgment.
- For the rare moment I want a different voice: Claude or Gemini
  (manual, not automated).

## What you should NEVER do
- Diagnose me.
- Push me to write more.
- Rewrite memoir chapters without explicit instruction.
- Modify or delete anything in `raw/` or `journal/private/`.
- Add motivational language ("you've got this!", "great work!"). It is corrosive
  to me.
```

### 5.2 The `wiki` CLI

This is the only piece of code you really need. It is ~100 lines of Python and replaces an entire RAG stack for personal-scale use.

`tools/wiki`:

```python
#!/usr/bin/env python3
"""wiki — minimal CLI to query and maintain a life wiki via DeepSeek."""
import argparse, json, os, pathlib, sys, subprocess, datetime
from openai import OpenAI

ROOT = pathlib.Path(os.environ.get("LIFEWIKI", pathlib.Path.home() / "life-wiki"))
SCHEMA = (ROOT / "WIKI.md").read_text() if (ROOT / "WIKI.md").exists() else ""

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)

def read_relevant(question: str, max_files: int = 10) -> str:
    """Naive: read index.md + recently modified files. Good enough at this scale."""
    index = (ROOT / "wiki" / "index.md")
    parts = []
    if index.exists():
        parts.append(("wiki/index.md", index.read_text()))
    # most recently modified .md files
    candidates = sorted(
        ROOT.glob("**/*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    for p in candidates:
        if "raw/" in str(p) or "private/" in str(p):
            continue
        rel = p.relative_to(ROOT)
        parts.append((str(rel), p.read_text()[:6000]))
        if len(parts) >= max_files:
            break
    return "\n\n".join(f"## {name}\n\n{body}" for name, body in parts)

def ask(question: str, model: str = "deepseek-chat") -> str:
    context = read_relevant(question)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": (
                "Here is the relevant slice of my wiki:\n\n"
                f"{context}\n\n"
                f"Question: {question}\n\n"
                "Answer in my voice. Cite pages by relative path."
            )},
        ],
        temperature=0.3,
    )
    return resp.choices[0].message.content

def ingest(path: pathlib.Path, model: str = "deepseek-chat") -> None:
    text = path.read_text()
    out_dir = ROOT / "inbox"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / (path.stem + ".md")
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": (
                "Below is a raw transcript of a voice memo. Follow the Ingest "
                "rules in WIKI.md. Output the YAML frontmatter (with `state:`), "
                "then a clean markdown draft, then a short `Possible links:` list.\n\n"
                f"---\n\n{text}"
            )},
        ],
        temperature=0.4,
    )
    out.write_text(resp.choices[0].message.content)
    print(f"→ {out.relative_to(ROOT)}")

def digest(since: str = "24h") -> str:
    # gather files modified in window
    seconds = {"24h": 86400, "7d": 604800, "30d": 2592000}.get(since, 86400)
    cutoff = datetime.datetime.now().timestamp() - seconds
    files = [p for p in ROOT.glob("**/*.md")
             if p.stat().st_mtime > cutoff and "raw/" not in str(p)]
    body = "\n\n".join(f"### {p.relative_to(ROOT)}\n{p.read_text()[:2000]}" for p in files)
    resp = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SCHEMA},
            {"role": "user", "content": (
                f"These are my notes from the last {since}. "
                "Write a short digest (300 words max), in my voice, gentle, no advice. "
                "Surface 1–2 recurring themes and 1 question I seem to be asking myself.\n\n"
                f"{body}"
            )},
        ],
        temperature=0.5,
    )
    return resp.choices[0].message.content

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("ask"); a.add_argument("question", nargs="+")
    a.add_argument("--pro", action="store_true", help="use deepseek-v4-pro")
    i = sub.add_parser("ingest"); i.add_argument("path")
    d = sub.add_parser("digest"); d.add_argument("--since", default="24h")
    d.add_argument("--out", default=None)
    args = ap.parse_args()

    if args.cmd == "ask":
        model = "deepseek-reasoner" if args.pro else "deepseek-chat"
        print(ask(" ".join(args.question), model=model))
    elif args.cmd == "ingest":
        ingest(pathlib.Path(args.path))
    elif args.cmd == "digest":
        out = digest(args.since)
        if args.out:
            with open(ROOT / args.out, "a") as f:
                f.write(f"\n\n## Digest {datetime.date.today()}\n\n{out}\n")
        else:
            print(out)

if __name__ == "__main__":
    main()
```

Make it executable, drop your API key in `~/.config/fish/conf.d/secrets.fish`:

```fish
set -gx DEEPSEEK_API_KEY "sk-..."   # from platform.deepseek.com
```

Now you have:

```bash
wiki ask "what philosophical question keeps recurring in my notes?"
wiki ask --pro "help me find a through-line for the Australia chapter"
wiki ingest raw/transcripts/2026-04-29-073012.txt
wiki digest --since 7d
```

### 5.3 Concrete prompts

Keep these as text files in `tools/prompts/` and shell out from small scripts. They are easier to version and easier to tweak when tired.

**`tools/prompts/scene-from-memo.txt`** — memoir scene from a voice memo:

```
You are helping me draft a memoir. I just spoke this voice memo aloud.

[VOICE MEMO TRANSCRIPT below]

Following the rules in WIKI.md (especially §Care), do this:
1. Identify the SCENE — a place, a moment, who was there, what was felt.
2. Write a 250–500 word scene in plain past-tense prose, in my voice.
   Sensory: smell, light, body. No analysis. No moral.
3. Below the scene, list 2–3 questions for me to answer next time
   (under "## Open questions"). Do not answer them.
Output as markdown, with YAML frontmatter including state, location, year (or "?").
```

**`tools/prompts/blog-from-journal.txt`**:

```
Read these recent journal entries. Find ONE small, true thing worth sharing
publicly. Draft a 600–900 word blog post in my voice — Camus' clarity, Backman's
warmth. No takeaways. No "5 lessons." Just one thing said well.

End with a single open question to the reader.
Output as: title, slug, date, tags, body.
```

**`tools/prompts/lesson-plan.txt`**:

```
Generate a 30-minute English lesson for {LEVEL} (A2/B1/B2/C1) on the topic:
{TOPIC}. Include: warm-up (3 min), input (10 min), practice (12 min), output (5 min).
Provide a 1-page student handout below the plan, with a short reading, 5 questions,
3 vocabulary items, and one writing prompt. Output as two markdown sections.
```

**`tools/prompts/recurring-questions.txt`**:

```
Across these notes, find 3–5 questions I keep asking myself in different forms.
For each: state the question in my words, cite 2–3 file paths where it appears,
and note whether it seems to be intensifying, softening, or steady.
Be careful with anything tagged state: tender. Mirror; do not analyze.
```

### 5.4 Which model for what

DeepSeek is cheap enough (see §5.5) that you can use it for almost everything. Use the heavier model only when the work is hard.

| Task | Model | Rough thinking |
|---|---|---|
| Transcription cleanup | `deepseek-v4-flash` (or legacy `deepseek-chat`) | Boring, high-volume, cheap. |
| Inbox drafts from voice memos | `deepseek-v4-flash` | Same. |
| Blog post drafting from a journal week | `deepseek-v4-flash` | Plenty good. |
| Memoir scene editing | `deepseek-v4-pro` with `thinking: enabled` | The harder craft work. |
| Weekly digest, recurring-questions | `deepseek-v4-pro` | Actually wants to think. |
| Teaching lesson plans | `deepseek-v4-flash` | Structured output. |
| One-off "feel" rewrites | manual paste into Claude.ai or Gemini | When DeepSeek's voice isn't quite right. |

> Pricing note (April 2026): DeepSeek's official docs name two current models — `deepseek-v4-flash` (cheaper) and `deepseek-v4-pro` (heavier, currently on a 75% promotional discount until 2026-05-31). The legacy aliases `deepseek-chat` and `deepseek-reasoner` still route to V4-flash modes; DeepSeek announced they will retire after 2026-07-24. The previous V3.2 generation (which set the famous "$0.028 cache hit / $0.28 cache miss / $0.42 output per million tokens" numbers) is widely cited. Treat all numbers as approximate and verify on `api-docs.deepseek.com/quick_start/pricing` before topping up. Sources differ on exact V4 prices; use the official page.

### 5.5 Cost estimate (you have low money — this is honest)

A normal week for this workflow:
- ~30 minutes of voice memo transcription/cleanup.
- ~20 inbox drafts.
- ~5 `wiki ask` queries.
- 1 digest.
- 1 blog draft.

That is roughly **2–3 million input tokens and 200–400k output tokens per month** in a generous month. At V3.2/V4-flash list prices that is single-digit dollars — most reports put light personal use at **$1–$10 per month** on DeepSeek. New accounts also get 5 million free tokens. If you switch to `deepseek-v4-pro` for everything, multiply by ~3–5×, but you don't need to. Set a hard monthly cap on the DeepSeek dashboard.

### 5.6 MCP (optional, for later)

If you ever want Claude Code or Codex CLI to read your vault directly:

- `cyanheads/obsidian-mcp-server` — uses Obsidian's Local REST API plugin.
- `bitbonsai/mcpvault` — pure filesystem, no plugin needed.
- `lucasastorian/llmwiki` — an actual implementation of Karpathy's pattern over MCP.

You do **not** need MCP on day one. The `wiki` Python CLI is simpler, cheaper, and uses the API you already pay for.

---

## 6. Publishing Pipeline

### 6.1 Blog — Hugo on GitHub Pages (free)

```bash
cd ~/life-wiki
hugo new site blog --format yaml
cd blog
git submodule add https://github.com/adityatelange/hugo-PaperMod themes/PaperMod
echo 'theme: PaperMod' >> hugo.yaml
hugo new content posts/hello.md
hugo server   # preview at localhost:1313
```

Push, enable GitHub Pages → Source: GitHub Actions → done. The `blog.yml` workflow above publishes on every push under `blog/`.

PaperMod is suggested because it is famously low-friction and respectful of slow connections. Skip dark-pattern themes that load 50 JS files.

### 6.2 Podcast — RSS on GitHub, audio elsewhere

Two viable paths:

**Path A — Hugo + Cloudflare Pages + Bunny Storage** (cassie.ink's approach, ~$1/month). Hugo's built-in RSS template is extended into a podcast feed; Bunny Storage hosts the mp3s for cents per GB.

**Path B — Castanet theme on GitHub Pages, mp3s on Internet Archive** (free). `mattstratton/castanet` is a Hugo theme designed for podcasts. Internet Archive hosts your audio files for free with a stable URL; your `feed.xml` references those URLs. Acceptable if you are okay with archive.org's listing.

Either way: each episode is one `podcast/episodes/2026-04-29-episode-01/` folder containing `audio.mp3`, `notes.md`, `cover.jpg`. A small Action transcribes the audio with whisper, turns it into show notes, and updates the feed.

```yaml
name: Podcast episode
on:
  push: { paths: ['podcast/episodes/**/audio.mp3'] }
jobs:
  notes:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: sudo apt-get update && sudo apt-get install -y ffmpeg
      - run: |
          # transcribe & write notes.md (whisper + DeepSeek for show notes)
          bash podcast/build-episode.sh
      - uses: stefanzweifel/git-auto-commit-action@v5
```

### 6.3 YouTube

You don't need a YouTube-specific stack on day one. When you make your first video:

- **Captions/subtitles**: same `whisper-cli` you already have. `whisper-cli -f video.mp4 -osrt -of subtitles.srt`. Upload the .srt.
- **Title + description + thumbnail text**: a `wiki` script that takes the script.md and asks DeepSeek for 3 candidate titles, a description with timestamps, and 5 hashtags.
- **Thumbnails**: generate locally with a small tool like **gimp + a template** or, if you want AI-generated thumbnails, use Bing Image Creator (free) or DALL-E via OpenAI's free credits — you don't need to pay a separate service. Honestly, a single still photo from your archive + clean text in GIMP is better than any AI thumbnail in 2026.

### 6.4 Memoir — Pandoc → EPUB + PDF

Use the `wikiti/pandoc-book-template` pattern. Inside `memoir/`:

```
memoir/
├── metadata.yaml
├── chapters/
│   ├── 01-bangladesh.md
│   ├── 02-australia.md
│   └── ...
├── images/
│   └── cover.jpg
├── build/
└── build.sh
```

`memoir/metadata.yaml`:
```yaml
---
title: <your working title>
author: <your name>
lang: en
rights: All rights reserved
cover-image: images/cover.jpg
---
```

`memoir/build.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p build
CHAPTERS=$(ls chapters/*.md | sort)

# EPUB
pandoc metadata.yaml $CHAPTERS \
  --top-level-division=chapter \
  --toc --toc-depth=2 \
  -o build/memoir.epub

# PDF (xelatex, memoir document class for nice chapter pages)
pandoc metadata.yaml $CHAPTERS \
  --top-level-division=chapter \
  --pdf-engine=xelatex \
  -V documentclass=memoir \
  -V geometry:margin=2.5cm \
  -V mainfont="DejaVu Serif" \
  --toc --toc-depth=2 \
  -o build/memoir.pdf
```

For a more polished print-ready book, `jp-fosterson/pandoc-novel` and `mre/pandoc-memoir` are good templates to crib LaTeX from.

---

## 7. Mental Health & Energy-Aware Workflow Design

### 7.1 The "one good hour a day" workflow

The single rule of this system is: **on a good hour, your job is to write or capture; on a bad hour, your job is rest.** The system does the bookkeeping either way.

**Bad day (0–20% energy):**
- Press the red record button on your phone, talk for 90 seconds, stop. Done.
- Or: `c "today is grey"` from the terminal, one line, close laptop.
- Or: nothing. The system keeps the lights on without you.

**Average day (20–60%):**
- Open `inbox/`, read three drafts the AI made for you. Move one to `journal/`, archive two.
- Run `wiki digest --since 24h` and read what the week sounds like.

**Good day (60%+):**
- Pick *one* file in `memoir/scenes/` and rewrite it. One scene. Not a chapter.
- Or: write a blog post directly into `blog/drafts/` and ask `wiki ask "polish this for kindness, keep my voice"`.

### 7.2 DID-aware design

You said different parts/states write different things. The system treats this as an asset, not a problem.

- **Don't separate by folder.** Tagging is gentler and reversible. Use the `state:` frontmatter in `WIKI.md` (`tender`, `sharp`, `warm`, `weary`, `creative`, `unknown`).
- **A "state index" page** (`wiki/states.md`) is updated weekly by the AI: "in the last 7 days, you wrote X tender, Y sharp, Z creative." No interpretation. Just a count. If you ever stop wanting this, delete the file and remove it from the schema.
- **Crucially**: `WIKI.md` instructs the AI to **never** name which "part" is writing or speculate about switching. It only tags the state of the text. You stay in charge of meaning.

### 7.3 Trauma-safe prompts (the §Care block, expanded)

The `WIKI.md` schema above does most of this. The principles, distilled:

1. **Mirror, don't interpret.** When in doubt, the AI quotes you back to yourself.
2. **No motivational language.** "You've got this!" is forbidden. So is "what a beautiful insight." It is corrosive over time.
3. **No connections without consent.** If the AI sees a link between today's voice memo and something painful from last year, it writes it as a *question* in `wiki/questions/`, not as an edit to either source. You decide later if the link is real.
4. **Length cap on tender content.** Drafts over `state: tender` are capped at ~150 words. The AI stops; you continue if you want.
5. **Default to silence.** If the AI is unsure, it copies the transcript verbatim into `inbox/` with no commentary. Better empty than wrong.

### 7.4 Memory aids

You said memory is hard. Three small commands carry most of the weight:

```bash
wiki ask "what was I working on yesterday?"
wiki ask "what did I tell myself I'd do this week?"
wiki ask "summarize my last 5 entries about my daughter"
```

These work because the schema tells DeepSeek to *cite paths* and *answer in your voice*, so the answer feels like yours, not like a chatbot's.

A `tools/morning.sh` you can run on waking:

```bash
#!/usr/bin/env bash
echo "## Today is $(date)"
echo
echo "### What was I working on?"
wiki ask "what was I working on yesterday and the day before? 5 sentences."
echo
echo "### Recurring question this week"
wiki ask "what question keeps surfacing in the last 7 days?"
```

### 7.5 Avoiding the ADHD trap

The danger of this whole project is that **building the system becomes the project, and the memoir never gets written.** Three rules:

1. **MVP in week 1 is just three things**: `~/life-wiki/`, `wiki ask`, voice memos syncing in. That is enough to start writing. Everything in §4–§6 is a future you problem.
2. **One new piece of automation per week, max.** No exceptions. Add `transcribe.yml` or add the blog deploy, not both.
3. **Set a write-vs-tinker ratio.** Aim for 4 hours of writing for every 1 hour of fiddling. Track it in `wiki/log.md`. The AI will tell you (gently, no scolding) when you have flipped the ratio.

### 7.6 Realistic cadence

- **Daily**: 1–10 minutes of voice memo, whenever. Optional `j` to jot.
- **Weekly (Sunday evening, ~30 min)**: read the AI's weekly digest. Move 1 inbox draft to `memoir/scenes/`. Optional: publish 1 blog post.
- **Monthly (1 hour)**: re-read `wiki/overview.md`. Adjust `WIKI.md` if your voice has drifted. Look at `wiki/states.md` if it helps; ignore if not.
- **Quarterly**: rebuild the memoir EPUB just to see it as a book. Hold it. Do not edit during this hour. Just look.

---

## 8. Starter Week Plan

Each task is sized to **15–30 minutes**. If you only do one task a day, you still finish in week 2. That is fine.

### Week 1 — MVP (just write)
- **Day 1 (20 min)** — Make the folder. `mkdir -p ~/life-wiki/{raw/audio,raw/transcripts,inbox,wiki,journal,memoir/chapters}`. `cd ~/life-wiki && git init && gh repo create life-wiki --private --source=. --push`. (Use `gh` from `pacman -S github-cli`.)
- **Day 2 (25 min)** — Write `WIKI.md`. Use the §5.1 template. Edit only the "Who I am" and "What you should NEVER do" sections; leave the rest as written. Commit.
- **Day 3 (15 min)** — Install Audio Recorder + Syncthing on phone. Pair with desktop Syncthing. Set up one shared folder: phone `LifeWiki/audio/` ↔ desktop `~/life-wiki/raw/audio/`.
- **Day 4 (20 min)** — Install whisper.cpp (`yay -S whisper.cpp`), download `ggml-medium.bin`. Test: `whisper-cli -m ~/.cache/whisper/ggml-medium.bin -f raw/audio/<your-first-memo>.m4a -otxt -of raw/transcripts/<name>`.
- **Day 5 (25 min)** — Get a DeepSeek API key. Drop it in fish secrets. Save the `tools/wiki` Python script. `pipx install openai`. Test: `wiki ask "is this working?"`.
- **Day 6 (15 min)** — Record one voice memo about anything. Run it through whisper. Run `wiki ingest raw/transcripts/<name>.txt`. Read the inbox draft. Notice how it sounds.
- **Day 7 (rest day)** — Don't touch the system. Just record one voice memo if you want. Commit nothing manually.

### Week 2 — Automation (so you can stop tinkering)
- **Day 8** — Write `tools/transcribe.sh` (loop whisper over new files). Test by hand.
- **Day 9** — Add the systemd timers (`autocommit`, `transcribe`). Enable them.
- **Day 10** — Wire `tools/transcribe.sh` to call `wiki ingest` automatically. Add ntfy on phone.
- **Day 11** — Set up the rofi/wofi `capture.sh` and bind it to `Super+Space`.
- **Day 12** — Add `git-crypt` for `journal/private/`. Export the key to your password manager + a USB stick.
- **Day 13** — Push to GitHub. Add `DEEPSEEK_API_KEY` as a repo secret. Add the `weekly-digest.yml` Action.
- **Day 14** — Read the first auto-generated weekly digest. Adjust `WIKI.md` if the voice is off.

### Week 3+ — Publishing (only when you want to)
- Pick *one* of: blog, podcast, memoir build, teaching folder. Set it up. Use it for two weeks before adding the next.

---

## 9. What to Ignore (anti-bloat)

- **Vector databases & embeddings.** At your scale (a few thousand markdown files at most), full-text grep + the LLM reading 10 most-recent files is faster, cheaper, and more reliable than any RAG stack. Karpathy's gist explicitly suggests this.
- **Multi-agent orchestration frameworks.** No CrewAI, no Autogen, no LangGraph. One Python script with one API call.
- **Premature MCP setup.** MCP is lovely; you don't need it until you're using Claude Code daily.
- **"Second brain" influencer setups.** Building a Zettelkasten system is not the same as writing a memoir.
- **Local LLMs as your default.** Ollama is wonderful, but on a low-energy laptop it will heat your knees and slow you down. Use cloud DeepSeek; local is a fallback.
- **Obsidian community plugins**, plural. You need maybe two: **Templater** (for daily-note templates) and **Git** (commits from the GUI). Skip Dataview, Tasks, Excalidraw, Calendar, Kanban — at least until they earn their place.
- **Custom domains, analytics, SEO** for your blog year one. Free `username.github.io` is fine.
- **Git LFS** unless you really need it. Audio doesn't belong in git history.
- **Auto-tagging your trauma material.** No.

---

## 10. Resources

### Karpathy's gist & implementations
- The original gist: `gist.github.com/karpathy/442a6bf555914893e9891c11519de94f`
- A working CLI implementation: `github.com/Pratiyush/llm-wiki`
- A Claude Code skill: `github.com/kfchou/wiki-skills`
- A Claude+Obsidian plugin: `github.com/AgriciDaniel/claude-obsidian`
- An MCP-based implementation: `github.com/lucasastorian/llmwiki`

### Arch wiki pages worth bookmarking
- `wiki.archlinux.org/title/Systemd/User` — for the timers above.
- `wiki.archlinux.org/title/Syncthing` — installation and autostart.
- `wiki.archlinux.org/title/Espanso`
- `wiki.archlinux.org/title/Obsidian`
- AUR `whisper.cpp`, `whisper.cpp-vulkan`, `whisper.cpp-cuda`.

### Android apps (with package IDs)
- Audio Recorder (axet): `com.github.axet.audiorecorder`
- Fossify Voice Recorder: `org.fossify.voicerecorder`
- Syncthing-Fork: `dev.syncthing.syncthing` (preferred) or original `com.nutomic.syncthingandroid`
- Markor: `net.gsantner.markor`
- Obsidian: `md.obsidian`
- Termux: `com.termux` (F-Droid only, not Play Store)
- Termux:Widget: `com.termux.widget`
- ntfy: `io.heckel.ntfy`
- KDE Connect: `org.kde.kdeconnect_tp`
- Open Camera: `net.sourceforge.opencamera`

### DeepSeek
- API docs: `api-docs.deepseek.com`
- Pricing (verify before topping up): `api-docs.deepseek.com/quick_start/pricing`
- Console: `platform.deepseek.com`
- The API is OpenAI-compatible; just change `base_url` to `https://api.deepseek.com`.

### Pandoc / memoir
- Official EPUB guide: `pandoc.org/epub.html`
- Book template: `github.com/wikiti/pandoc-book-template`
- Novel/memoir template with LaTeX `memoir` class: `github.com/jp-fosterson/pandoc-novel`
- Pretty PDF memoir template: `github.com/mre/pandoc-memoir`

### Hugo / publishing
- Hugo podcast theme (Castanet): `github.com/mattstratton/castanet`
- Cassie Ink's Hugo-as-podcast guide: `cassie.ink/hugo-podcast/`
- PaperMod (blog theme): `github.com/adityatelange/hugo-PaperMod`

### Encryption
- git-crypt: `github.com/AGWA/git-crypt`
- git-agecrypt (modern, age-based): `github.com/bartei/git-agecrypt` and `github.com/vlaci/git-agecrypt`
- agebox (gitops-style): `github.com/slok/agebox`

### Termux + git on Android (if Syncthing isn't enough)
- David Kopp's scripts: `github.com/davidkopp/termux-scripts`
- Mathis Gauthey's tutorial: `mathisgauthey.github.io/using-git-to-sync-your-obsidian-vault-on-android-devices/`

### Obsidian community plugins (only if you actually need them)
- **Templater** — daily note scaffolds.
- **Obsidian Git** — visual commits if you don't want the terminal every time.
- **Local REST API** (`coddingtonbear/obsidian-local-rest-api`) — only if you want MCP servers later.
- **Obsidian Web Clipper** (Chrome/Firefox) — clip articles straight into `raw/clippings/`.

### MCP servers for Obsidian (later, optional)
- `cyanheads/obsidian-mcp-server`
- `bitbonsai/mcpvault`
- `MarkusPfundstein/mcp-obsidian`

### ADHD / trauma writing references (worth a slow read)
- UNC Writing Center, "ADHD and Graduate Writing" — most ADHD-writing advice elsewhere on the internet is recycled from this page.
- Jane Friedman, "Attention, Please! 7 Drug-Free Concentration Boosters for Writers with ADHD."

---

## Caveats

- **Pricing changes.** DeepSeek pricing has shifted three times in the last year (V3 → V3.2-Exp halved prices in late 2025; V4 launched in 2026 with renamed flash/pro tiers and a 75% promo on pro until 2026-05-31). Treat the dollar figures here as *order-of-magnitude*, not contractual. Always check the official pricing page before topping up. Some third-party trackers are out of date.
- **Karpathy's pattern is one year old.** It is a *pattern*, not an established practice. The "vector DBs are unnecessary at personal scale" claim is true for ≤ ~150 pages of dense markdown; if your wiki ever crosses ~100k tokens of relevant context, you may want a small search layer (grep is enough; `qmd` is named in the gist if you want hybrid BM25+vector — but that is a year-2 problem).
- **AI is not a therapist.** Even with the best `WIKI.md` schema, an LLM can hallucinate, mirror your distress badly, or generate confident nonsense. Keep your human supports — therapist, partner, friends — primary. The wiki is for memory, craft, and rest. Not for crisis.
- **DID is contested clinical territory.** The schema's `state:` tagging is a *practical writing aid*, not a clinical claim, and is intentionally agnostic about parts/alters terminology. If your therapist has a different framework, edit `WIKI.md` to match theirs — the system bends to you.
- **Encryption is only as good as your key management.** `git-crypt` and `age` are excellent, but if you lose the key, the data is gone. Store the key in (a) your password manager, (b) a USB stick in a drawer, and (c) one trusted off-site location. Test recovery once.
- **Wayland espanso has rough edges.** If text expansion misbehaves, fall back to X11 or skip espanso entirely — it is a nice-to-have, not load-bearing.
- **Termux from Play Store is abandoned.** Always install from F-Droid or GitHub Releases.
- **GitHub Actions minutes are not infinite.** Free tier on private repos is 2,000 minutes/month — comfortable for this workflow, but if you transcribe a lot of long audio in CI, it will pinch. Prefer transcribing locally when you can.
- **Syncthing battery drain.** Acceptable on modern phones with the Fork client, but check after a week. If it is too much, fall back to a single Termux git-pull on a home-screen widget.
- **The system can become a hiding place.** When in doubt, write the scene, not the script. The most important file in this whole repo is whichever chapter you are afraid of writing next.

---

*This plan is a draft. It will be wrong in the third week. That is fine. Edit `WIKI.md` first, scripts second, and your memoir always.*