# ASSISTIVE TECH FOR ADHD, BIPOLAR & EXECUTIVE FUNCTION
## Apps, software, and OS-level setups — Windows + Arch Linux
### For Sourov Deb | 29 May 2026

> Matched to your documented profile: ADHD (attention, task-initiation, time-blindness), bipolar I (mood/energy tracking), insomnia (sleep/light), depression (low-friction tools). Free/open-source flagged **[FOSS]**. Verify current pricing and availability before installing — software changes.

---

## 1. FOCUS & TASK-INITIATION (the ADHD core problem)

| Tool | Platform | What it does |
|---|---|---|
| **Pomofocus / Pomodoro timers** | Web, all | 25/5 sprint structure; externalises time |
| **Forest** | iOS/Android/Chrome | Gamified focus; grows a tree if you don't switch apps |
| **Goblin.tools** **[FOSS-ish]** | Web | AI "Magic ToDo" breaks a vague task into tiny steps — built for ADHD task-initiation |
| **Cold Turkey / LeechBlock [FOSS]** | Win/Linux/browser | Hard-blocks distracting sites during work blocks |
| **Raise (body-doubling) / Focusmate** | Web | Live co-working with a stranger on camera — body-doubling beats willpower |
| **activitywatch [FOSS]** | Win/Linux | Open-source automatic time-tracking; see where hours actually go |

## 2. TASK / PROJECT CAPTURE (the "external brain")

| Tool | Platform | Why for you |
|---|---|---|
| **Todoist / TickTick** | All | Fast capture; natural-language dates; recurring meds/appointments |
| **Obsidian [FOSS-core]** | Win/Linux | Local markdown notes — fits your existing .md workflow; daily-note + capture |
| **Logseq [FOSS]** | Win/Linux | Outliner + journal; good for scattered ADHD thoughts |
| **Trello / Kanban** | All | Visual three-column board (Today / Week / Parked) |
| **Super Productivity [FOSS]** | Win/Linux | Open-source task manager with built-in pomodoro + time tracking |

## 3. MOOD, ENERGY & SYMPTOM TRACKING (bipolar management)

| Tool | Platform | What it does |
|---|---|---|
| **Daylio** | iOS/Android | Two-tap mood + activity log; charts mood against sleep/activity — useful to show your psychiatrist |
| **eMoods / Bipolar UK Mood Tracker** | mobile | Purpose-built bipolar tracker: mood, sleep hours, meds, episodes |
| **Bearable** | mobile | Tracks symptoms, meds, sleep, energy together; correlations over time |
| **Plain markdown one-liner [FOSS]** | any | Your daily-note state read (from the plan) — zero friction, no app needed |

## 4. SLEEP & CIRCADIAN (your clinical insomnia)

| Tool | Platform | What it does |
|---|---|---|
| **f.lux [free]** | Win/Linux/Mac | Removes blue light after sunset — supports the wind-down protocol |
| **redshift / gammastep [FOSS]** | Linux/Arch | Open-source colour-temperature shifter; scriptable by time |
| **Sleep as Android** | Android | Smart alarm in light sleep phase; tracks sleep debt |
| **Insight Timer / Calm** | mobile | Guided wind-down, body scan, sleep stories |

## 5. MEDICATION & APPOINTMENT REMINDERS

| Tool | Platform | Note |
|---|---|---|
| **Medisafe** | mobile | Pill reminders, refill alerts, missed-dose tracking |
| **Native OS alarms** | all | Two recurring alarms (morning meds + wind-down) — simplest, most reliable |
| **KDE/GNOME calendar + reminders [FOSS]** | Linux | Recurring desktop notifications |

## 6. FOCUS-FRIENDLY WRITING / CONTENT (your income work)

| Tool | Platform | Why |
|---|---|---|
| **FocusWriter [FOSS]** | Win/Linux | Distraction-free full-screen writing |
| **Whisper / whisper.cpp [FOSS]** | Win/Linux | Local speech-to-text — dictate when typing is too much; you already work with voice notes |
| **OBS Studio [FOSS]** | Win/Linux | Screen + camera recording for your YouTube/courses |
| **Kdenlive / Shotcut [FOSS]** | Win/Linux | Open-source video editing (alternatives to your 4 paid tools) |
| **Reaper (cheap) / Audacity [FOSS]** | Win/Linux | Audio for podcast/video |

---

## 7. WINDOWS — SYSTEM-LEVEL MODIFICATIONS

**Reduce friction & distraction**
- **Focus Assist / Focus Sessions** (built-in, Settings → System → Focus): silences notifications, integrates a timer + Spotify + To-Do.
- **Night Light** (Settings → Display): schedule warm screen after sunset.
- **PowerToys [FOSS, Microsoft]**: FancyZones (fixed window layouts = less decision fatigue), Run launcher (keyboard-first), Always-on-Top to pin your task list.
- **Disable notification badges & taskbar flashing**: removes attention hijacks.
- **Single-desktop discipline**: use Virtual Desktops (Win+Tab) — one desktop = "work", one = "everything else".

**Automation**
- **AutoHotkey [FOSS]**: hotkeys to launch your work-block setup (open board + timer + block sites) in one keypress.
- **Task Scheduler**: auto-launch f.lux, mood-log prompt, or a "start work" script at fixed times — externalises routine.
- **Power plan**: schedule a "wind-down" that dims and quietens the machine in the evening.

---

## 8. ARCH LINUX — SYSTEM-LEVEL + AUTOMATION

> Arch's strength for ADHD: you script the discipline **once**, then it runs without willpower. Build the environment to enforce the routine.

**Distraction control**
- **hosts-file / hblock [FOSS]**: block distracting domains system-wide; toggle with a script during work blocks.
- **gammastep / redshift**: scheduled colour-temp via `systemd --user` timer for the insomnia protocol.

**Automation with systemd timers (the key tool)**
- `systemd --user` timers replace willpower: schedule fixed-time prompts —
  - morning: notify "take meds + write today's state"
  - work block: launch terminal + open task board + start blocker
  - evening: trigger wind-down (dim, block sites, notify "screens off in 1h")
- Example pattern: a `.timer` unit fires a `.service` that runs a shell script. Set once, runs daily.

**Window manager for low decision-fatigue**
- **Tiling WM (Hyprland / sway / i3 [all FOSS])**: windows auto-arrange — removes the constant micro-decisions of where to put things. Fixed workspaces: 1=work, 2=comms, 3=media.
- **Workspace rules**: pin specific apps to specific workspaces so the layout is always identical (predictability helps both ADHD and bipolar routine).

**Capture & routine**
- **A single capture script** bound to a hotkey: appends a timestamped line to `~/inbox.md`. Zero-friction idea capture.
- **A `today` script**: opens your daily markdown note pre-filled with the date + state-read template.
- **cron / systemd timer + a notification** for the recurring weekly file ritual (push to Drive/GitHub).

**Notes / knowledge base**
- **Obsidian / Logseq / neovim + markdown [FOSS]**: keep everything in plain `.md` — matches the files you already keep, fully scriptable, no lock-in.

---

## 9. PRINCIPLE BEHIND ALL OF IT

The condition makes *consistent willpower* unreliable. So move the routine **out of your head and into the system**: timers that fire, scripts that launch the right windows, blockers that turn on automatically, prompts that ask for your daily state. On Arch especially — script the discipline once; let the machine carry it on the days you can't.

---

*Tool availability and pricing change. Confirm each on its official site or in the Arch repos/AUR before relying on it. FOSS tags indicate free/open-source as of 2026.*
