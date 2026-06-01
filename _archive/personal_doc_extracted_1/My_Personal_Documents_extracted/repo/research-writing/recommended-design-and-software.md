# Recommended UI, Design, Software & Navigation System
> Tailored for your life-wiki setup — low energy, memory issues, Arch Linux, Android

---

## Design Philosophy (applies to every tool choice)

One question drives every recommendation here:
> **"Will I still use this when I'm exhausted and can't think?"**

If the answer is no, skip it. Complexity is the enemy of consistency.

Principles:
- **Capture first, organize later.** Never let the system feel like homework.
- **Text/markdown is the universal format.** Works offline, in any app, forever.
- **Dark + low-contrast is kinder to fatigued eyes.** All tool picks below respect this.
- **Keyboard > mouse > touch.** The fewer decisions per action, the better.

---

## 1) Desktop (Arch Linux) — core tools

### File Navigation: `yazi`
- A **terminal file manager** with Vim-style keys. Fast, visual, stays in muscle memory even on low energy days.
- Shows image/file previews in terminal (including your photos).
- Install: `sudo pacman -S yazi`
- Why: replaces clicking through Nautilus or Thunar; you can navigate the entire `life-wiki/` tree in seconds.

### Editor: `neovim` or `Obsidian` (pick one as primary)

| Use case | Best pick |
|---|---|
| Quick edits, terminal-native, keyboard-first | `neovim` with `lazy.nvim` |
| Visual navigation, graph view, wikilinks | `Obsidian` |

**Recommended approach:** Obsidian for the `wiki/` layer; neovim for scripts and quick captures.

### Obsidian setup (wiki viewer/editor)
- Open `life-wiki-template/` as the vault.
- Theme: **Minimal** (install via Community Themes) — clean, low-distraction.
- Font: `iA Writer Mono S` (free) or `JetBrains Mono` — both easy on fatigued eyes.
- Essential plugins:
  - **Dataview** — query your wiki like a database (e.g. "show all pages tagged `adhd`")
  - **Calendar** — click a date to open/create that day's journal
  - **Templater** — auto-fill frontmatter when you create a new page
  - **Omnisearch** — fast full-text search (replaces clicking index.md manually)
  - **Obsidian Git** — auto-commit your wiki on a schedule (set it and forget)

### Terminal: `kitty` or `alacritty`
- Both are GPU-accelerated and render fonts clearly.
- Set font size to 15–16pt. When fatigued, bigger text wins.
- Color scheme: **Catppuccin Mocha** (warm dark palette, very easy on eyes; available for both).

### App launcher: `rofi` or `fuzzel`
- Hit one key → start typing anything (app, file, command).
- Reduces navigation friction to near zero.

### Window manager: `sway` (Wayland) or `i3` (X11)
- Tiling window managers: everything is always in view, no overlapping mess.
- Your typical layout: Obsidian left | terminal right (or browser left | terminal right).
- No need to hunt for windows when your working memory is low.

---

## 2) Font & Color Design System (for your wiki, blog, and any HTML output)

You already have the Anthropic design system in `viewer.html` and `model.html`. Here's a simplified version personalized for your wiki and publishing:

### Palette (warm + readable)
```
Background:   #1e1e2e  (dark, easy on eyes — Catppuccin base)
Surface:      #2a2a3d
Text:         #cdd6f4  (soft white, not stark)
Accent:       #cba6f7  (lavender — Camus, philosophy, reflection)
Accent alt:   #89b4fa  (blue — memory, ocean, Réunion)
Warm orange:  #fab387  (energy, stories, coffee)
Green:        #a6e3a1  (growth, recovery, learning)
Muted:        #6c7086
```

### Typography
- **Headings:** `Lora` (serif, warm — literature feel, matches your love of Dostoyevsky / Camus)
- **Body text:** `iA Writer Duo S` or `Source Serif 4` — long-form reading comfort
- **Code/terminal:** `JetBrains Mono` or `Cascadia Code`
- **Google Fonts equivalent (free, web-safe):** Merriweather + Open Sans

---

## 3) Android (capture-first tools)

| Need | App | Why |
|---|---|---|
| Fast text notes | **Markor** **Tolari,md** (free, open source) | Plain markdown, saves to synced folder, zero friction |
| Wiki browsing | **Obsidian Mobile** (free) | Same vault, wikilinks work, graph view |
| Syncing files | **Syncthing-Fork** (free, no account) | Local P2P sync, no cloud needed, private |
| Voice capture | **RecForge II** (free) or stock recorder | Saves to synced audio folder |
| Web clipping | **Obsidian Web Clipper** (browser extension) | Converts articles to markdown directly into vault |
| Photography notes | **Open Camera** → auto-rename with EXIF | Saves to `raw/photos/` via Syncthing |

**Golden rule for Android:** Only install apps that save files you can see and touch. No proprietary databases. Everything goes to the synced folder.

---

## 4) File Navigation Design (the "where does this live?" answer)

### The mental model (one rule to remember)
```
Did it come from outside?   → raw/
Did the LLM write it?       → wiki/
Is it a working script?     → tools/
Is it ready to publish?     → wiki/outputs/
```

### Naming convention (reduces decision fatigue)
```
Dates:      YYYY-MM-DD-title.md        (easy reverse-sort)
Concepts:   kebab-case.md              (e.g. meaning-of-work.md)
Sources:    src-YYYY-MM-DD-short.md    (in wiki/sources/)
Outputs:    out-blog-title.md          (in wiki/outputs/)
```

### Quick-access aliases (add to `.bashrc` / `.zshrc` on Arch)
```bash
alias lw='cd ~/life-wiki'
alias cap='~/life-wiki/tools/capture.sh'
alias inbox='ls -lt ~/life-wiki/raw/inbox | head -20'
alias wiki='cd ~/life-wiki && nvim wiki/index.md'
```

---

## 5) Software Stack Summary (install order on Arch)

### Phase 0 — survive without energy
```bash
sudo pacman -S git syncthing neovim yazi ripgrep fd fzf obsidian
```

### Phase 1 — make it comfortable
```bash
sudo pacman -S kitty ttf-jetbrains-mono-nerd
# Install Cascadia Code from AUR:
yay -S ttf-cascadia-code
# Set up sway/i3 window manager
sudo pacman -S sway swaybar fuzzel
```

### Phase 2 — local LLM (for ingest automation)
```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2        # 3B — fast, low RAM, good for summary tasks
ollama pull mistral         # 7B — better quality, still fits in 16GB
```

### Phase 3 — voice transcription (offline)
```bash
sudo pacman -S python-pip
pip install openai-whisper   # runs locally, no API key
# Then: whisper raw/audio/your-note.m4a --language fr  (or en/bn)
```

---

## 6) Blog / YouTube / Podcast publishing pipeline

Because you're in Réunion, low-budget, 5 languages — here's the simplest possible path:

| Output type | Free tool | How it fits |
|---|---|---|
| Blog | **Ghost** (self-host, free) or **Bear Blog** (free hosted) | Post from `wiki/outputs/` markdown |
| Podcast | **Ausha** free tier or **Anchor/Spotify for Podcasters** | Upload mp3 from Arch |
| YouTube | OBS Studio (Arch: `sudo pacman -S obs-studio`) | Screen + voice recording |
| Slides (for teaching) | **Marp** in Obsidian | Write markdown → export PDF/HTML |
| Short-form writing | **Substack** free tier | Paste from `wiki/outputs/` |

### Workflow (low-energy publishing)
```
raw/journal → ingest → wiki/themes/ → wiki/outputs/draft.md → publish
```
One direction. One action at a time.

---

## 7) Memory-aid features to configure immediately

Because you mentioned **memory issues and ADHD**:

- **Obsidian Calendar plugin:** shows you what you worked on any day → no "where was I?" panic.
- **Daily note template:** auto-opens today's file on launch. One line is enough for today.
- **Obsidian Git plugin:** commits your work every 30 min automatically. You never lose anything.
- **`wiki/overview.md`:** keep one page that says what matters *right now*. Read this first every session.
- **Rofi/fuzzel quick-launch:** bind it to `Super+Space`. Typing 3 characters launches any app — no hunting.
- **Wallpaper with your current top 3 priorities:** sounds silly, works surprisingly well.

---

## 8) Réunion-specific notes

- Your internet is probably intermittent. **Syncthing (local)** and **Ollama (local LLM)** mean your wiki keeps working even offline.
- All tools recommended here work fully offline after first install.
- For French-language voice notes: Whisper supports `fr` natively. For Bengali: `bn` is supported.

---

## Quick-start checklist for Arch

```
[ ] Install: yazi, neovim, obsidian, syncthing, ripgrep, fd, fzf, kitty
[ ] Set up Syncthing between Arch and Android
[ ] Open life-wiki-template/ in Obsidian as vault
[ ] Install Obsidian plugins: Dataview, Calendar, Templater, Omnisearch, Obsidian Git
[ ] Add aliases to .bashrc / .zshrc
[ ] Install Ollama + pull llama3.2
[ ] Set up Whisper for voice transcription
[ ] Configure Obsidian theme: Minimal + Catppuccin colors
```

---

## 9) Windows 11 — Modifications, UI Overhaul & Tools

> You are on Windows 11 Home (Build 26200, HP laptop, i5-12450H, RTX 3050, 16GB).
> Everything below is **legal, reversible, and free** — no piracy, no license bypassing.

---

### Step 0 — Before anything: create a restore point

```
Start → "Create a restore point" → Create → name it "before-mods"
```

Do this before every phase. Takes 30 seconds and saves hours.

---

### Step 1 — Debloat + Privacy (the foundation)

#### Chris Titus Tech WinUtil (most trusted community tool)
The single most useful Windows tweaking tool. Open PowerShell as Administrator and run:

```powershell
iwr -useb https://christitus.com/win | iex
```

**What to use inside it:**

| Tab | Action |
|---|---|
| Tweaks | "Desktop" preset → removes telemetry, bloatware, ads |
| Privacy | Enable all privacy tweaks |
| Features | Enable WSL2 (lets you run Arch Linux inside Windows) |
| Fixes | Run "Set Up Autologin" and "Clear TEMP files" |

**Result:** Windows stops sending data to Microsoft, removes Candy Crush, Cortana noise, Xbox overlays, etc.

#### Alternatively: `Winget` bulk-remove bloatware
```powershell
# Run as Administrator
winget uninstall "Microsoft 3D Viewer"
winget uninstall "Microsoft Teams"
winget uninstall "Clipchamp"
winget uninstall "Xbox"
winget uninstall "Your Phone"
winget uninstall "Spotify" # if pre-installed
winget uninstall "Disney+"
```

---

### Step 2 — UI Overhaul (make it look and feel different)

#### ExplorerPatcher — restore a sane Windows interface
- Brings back Windows 10-style taskbar, Start menu, and context menus.
- Download: https://github.com/valinet/ExplorerPatcher (free, open source)
- Why: Windows 11's default taskbar is inefficient; this restores full control.
- Key settings to change after install:
  - Taskbar: set to Windows 10 mode
  - Start menu: set to Windows 10 style (or keep Win11 if you prefer)
  - Context menu: disable "Show more options" (the extra click)

#### StartAllBack — optional, polished taskbar replacement
- Free trial, ~$5 to buy permanently
- More polished than ExplorerPatcher; worth it if you want a cleaner look
- Brings back proper right-click context menus immediately

#### Rainmeter — desktop widgets + skin system
- Download: https://www.rainmeter.net (free, open source)
- Use it to put your `wiki/overview.md` top-3 priorities on your desktop
- Recommended skin pack: **Droptop Four** or **Mond** (minimalist dark)

#### Wallpaper Engine alternative (free): **Lively Wallpaper**
- Download: https://github.com/rocksdanister/lively (free, open source, on Windows Store)
- Animated or video wallpapers — use a calm nature scene (calming for ADHD/fatigue)

---

### Step 3 — File Navigation (replace File Explorer)

#### `Files` app — modern File Explorer replacement
- Download: https://files.community (free, open source, on Windows Store)
- Features: tabs, column view, dual-pane, tag support
- Much better for navigating your `life-wiki/` folder structure

#### `Everything` by Void Tools — instant file search
- Download: https://www.voidtools.com (free)
- Indexes your entire drive instantly; find any file by typing 2 characters
- Bind it to `Win+F` to replace the slow Windows search
- **Essential for memory issues** — you never need to remember where a file is

#### `FZF` + Windows Terminal — keyboard-first navigation
Install Windows Terminal (from Microsoft Store, free) then add fzf:
```powershell
winget install junegunn.fzf
winget install BurntSushi.ripgrep.MSVC
```
Then add this function to your PowerShell profile (`$PROFILE`):
```powershell
# Fuzzy-navigate to life-wiki fast
function wiki { Set-Location "C:\Users\souro\Desktop\SKIILS" ; fzf | Invoke-Item }
```

---

### Step 4 — Terminal & Shell upgrade

#### Windows Terminal + PowerShell 7
```powershell
winget install Microsoft.WindowsTerminal
winget install Microsoft.PowerShell
```

#### Oh My Posh — terminal prompt with Git status, time, battery
```powershell
winget install JanDeDobbeleer.OhMyPosh
```
Then add to your PowerShell 7 profile:
```powershell
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/catppuccin_mocha.omp.json" | Invoke-Expression
```

#### Nerd Font (required for the prompt icons)
```powershell
oh-my-posh font install JetBrainsMono
```
Then set Windows Terminal font to `JetBrainsMono Nerd Font`.

---

### Step 5 — Keyboard shortcuts + launcher (reduce cognitive load)

#### PowerToys (official Microsoft tool, free)
```powershell
winget install Microsoft.PowerToys
```

Key features to turn on:

| Feature | What it does | Why you need it |
|---|---|---|
| **PowerToys Run** (`Alt+Space`) | App + file launcher (like Spotlight) | No hunting, works on low energy |
| **FancyZones** | Tiling window layouts | Obsidian left, terminal right, always |
| **Keyboard Manager** | Remap any key | Remap CapsLock → Ctrl or a capture shortcut |
| **Text Extractor** | OCR from any screen area | Good for capturing from PDFs/images |
| **Paste As Plain Text** | Always paste without formatting | Saves frustration constantly |
| **Always On Top** | Pin any window on top | Pin your `wiki/overview.md` |

---

### Step 6 — WSL2 + Arch Linux inside Windows

This is the biggest "modification" — it lets you run your full Arch Linux wiki workflow **inside Windows** without rebooting.

#### Enable WSL2
```powershell
# Run as Administrator
wsl --install
# Reboot, then:
wsl --set-default-version 2
```

#### Install Arch Linux on WSL2
```powershell
# From Microsoft Store: install "Arch Linux" (it's free and official)
# Or via terminal:
winget install "Arch Linux"
```

Then inside WSL Arch:
```bash
# Install your full Arch stack
sudo pacman -Syu
sudo pacman -S git neovim yazi ripgrep fd fzf syncthing
# Mount your SKIILS folder
ls /mnt/c/Users/souro/Desktop/SKIILS/
```

**Result:** Your entire life-wiki toolchain (`yazi`, `nvim`, `ollama`, `whisper`) runs in a real Linux terminal, inside Windows, accessing your Windows files at `/mnt/c/Users/souro/`.

---

### Step 7 — Performance optimizations (for your HP i5-12450H)

#### Disable unnecessary startup programs
```
Task Manager (Ctrl+Shift+Esc) → Startup apps → Disable everything except:
- your antivirus (if any)
- Syncthing
- Obsidian (optional)
```

#### Power plan: use "Balanced" not "Power Saver"
Your RTX 3050 and i5-12450H need headroom. In PowerShell:
```powershell
powercfg /setactive SCHEME_BALANCED
```

#### Disable visual effects (speeds up the GPU for real work)
```
Right-click "This PC" → Properties → Advanced system settings
→ Performance → Settings → "Adjust for best performance"
→ Then manually re-enable "Smooth edges of screen fonts" only
```

---

### Step 8 — Privacy hardening (post-debloat)

After running WinUtil, add these:

#### O&O ShutUp10++ (free, portable)
- Download: https://www.oo-software.com/en/shutup10
- Run it, click "Apply all recommended settings"
- Turns off 50+ telemetry switches in one click
- No install needed — just run the `.exe`

#### DNS: switch to Cloudflare 1.1.1.1 or NextDNS (free)
```
Settings → Network → DNS → Manual → 1.1.1.1 and 1.0.0.1
```
Faster, more private than your ISP's DNS (important in Réunion).

---

### Windows 11 — Quick-start checklist

```
[ ] Create restore point
[ ] Run Chris Titus WinUtil → Desktop tweaks + Privacy
[ ] Install: Everything (file search), Files app, PowerToys
[ ] Install: Windows Terminal + PowerShell 7 + Oh My Posh
[ ] Install ExplorerPatcher (fix taskbar + context menu)
[ ] Install Lively Wallpaper (calm animated wallpaper)
[ ] Enable WSL2 + Arch Linux (run full Linux stack inside Windows)
[ ] Install winget packages: fzf, ripgrep
[ ] Run O&O ShutUp10++ (telemetry off)
[ ] Switch DNS to 1.1.1.1
[ ] Set FancyZones layout: Obsidian left | Terminal right
[ ] Bind Alt+Space to PowerToys Run (replace Windows search)
[ ] Bind a key to capture.sh via Keyboard Manager
```

---

### Tools summary table

| Category | Tool | Free? | Why |
|---|---|---|---|
| Debloat | Chris Titus WinUtil | ✅ | One-click telemetry + bloat removal |
| Privacy | O&O ShutUp10++ | ✅ | 50+ privacy switches |
| UI | ExplorerPatcher | ✅ | Sane taskbar + context menus |
| UI | Lively Wallpaper | ✅ | Calm animated wallpaper |
| File search | Everything | ✅ | Instant, keyboard-driven |
| File manager | Files app | ✅ | Tabs, dual-pane, modern |
| Terminal | Windows Terminal + PS7 | ✅ | Required for everything below |
| Shell theme | Oh My Posh | ✅ | Git-aware prompt |
| Launcher | PowerToys Run | ✅ | Alt+Space → any file/app |
| Window tiling | FancyZones | ✅ | Always same layout |
| Linux stack | WSL2 + Arch | ✅ | Full Arch toolchain inside Windows |

---

*Move this file to `life-wiki-template/wiki/concepts/system-design.md` when you're ready.*
