# Bipolar-Adapted Productivity and Writing Workflow

**For Sourov Deb — Designed for low cognitive load, minimum decisions, maximum output**  
**Last updated: June 2026**

---

## Understanding Your Three Modes

Bipolar disorder doesn't mean broken. It means your energy and capacity come in cycles. The key is to **design systems that work across all three modes** so nothing falls apart when the cycle shifts.

| Mode | What it feels like | What you can do |
|------|-------------------|------------------|
| **Stable** | Clear, focused, consistent | Write full posts, build systems, plan ahead |
| **Hypomanic** | High energy, ideas rushing, easily distracted | Capture all ideas (voice recorder), do NOT make big decisions, write in sprints |
| **Depressive** | Low energy, brain fog, difficulty starting | Use pre-built templates, voice recording, minimum viable tasks |

**The system in this repository is designed so that even on your worst day, you can still publish.**

---

## The No-Zero Day Protocol

A No-Zero Day means: every day, you do at least one tiny thing toward your work. Not a full post. Not perfect. Just not zero.

| Day type | Minimum task | Time needed |
|----------|-------------|-------------|
| Stable day | Write a full 500-word post | 30–45 min |
| Low energy | Speak 3 minutes into voice recorder | 5 min |
| Very low energy | Open Le Chat, give one topic, copy output to sheet | 3 min |
| Crisis day | Add one idea to your `topics.txt` file | 1 min |
| Rock bottom | Do nothing — the system still runs from yesterday's content | 0 min |

**The automation system ensures that even doing nothing for a week doesn't stop your publishing** — if you have drafts in the queue, they publish automatically.

---

## Decision Fatigue Reduction

Every decision costs energy. Eliminate as many decisions as possible:

### Pre-made decisions (set once, never re-decide):
- **Writing time:** Always 9 AM (or whenever your stable window is)
- **Post length:** Always 500 words (not 300, not 800 — just 500)
- **Banner template:** One Canva template — change only the title text
- **Post structure:** Always the same: 1 intro, 3 main points, 1 conclusion
- **Categories:** Already set in the auto-publisher — never decide manually
- **Tags:** Already auto-generated — never decide manually
- **Publishing time:** Always 9 AM the next morning (Apps Script handles scheduling)

---

## Pomodoro for Bipolar: Modified Version

The standard Pomodoro (25 min work, 5 min break) is too rigid. Use this instead:

| Phase | Duration | Rule |
|-------|----------|------|
| **Micro-sprint** | 10–15 min | Write freely, no editing |
| **Micro-break** | 5–10 min | Mandatory — do not skip |
| **Extended break** | 15–30 min after 2 sprints | Move, eat, drink water |
| **Stop point** | After 3 sprints | Never write for more than 45–60 min total |

**On hypomanic days:** Set a timer to STOP. Hypomanic writing often needs heavy editing later. Write, then stop.

**On depressive days:** Set a timer to START for only 10 minutes. Once you start, the hardest part is over.

---

## Writing Templates (Use These — Never Start from Blank)

### Template A: ELT Lesson Reflection
```
# Day [N] – [Topic]

[One sentence: what you taught or observed today]

## The Problem
[What difficulty were your students facing?]

## What I Tried
[Your approach or technique]

## What Worked
[The result, even if small]

## One Thing for You to Try
[A practical tip for readers]

*Written during my 50-hour ELT Masterclass journey.*
```

### Template B: Teaching Insight (500 words)
```
# [Provocative question or statement as title]

[Paragraph 1: Set the scene — a moment in class, a student's struggle]

[Paragraph 2: The theory behind it — what does research say?]

[Paragraph 3: My approach — what did I do?]

[Paragraph 4: What happened next — result, surprise, learning]

[Paragraph 5: What this means for you — actionable tip]

*Tags: ELT, teaching, [topic]*
```

### Template C: Grammar Explained (for low-energy days)
```
# [Grammar Point]: A Simple Guide

Students often struggle with [grammar point]. Here's why, and here's how to fix it.

**The rule:** [One sentence explanation]

**Common mistake:** [Example of wrong usage]

**Correct version:** [Fixed example]

**How to remember it:** [Memory tip or mnemonic]

**Try this:** [One exercise for readers]

*For my 50-hour ELT Masterclass series.*
```

Save these templates as `.md` files in your `drafts/templates/` folder. Never write from blank again.

---

## App Stack for Mood and Health Tracking

### Phone apps (install all three, use daily):

1. **eMoods** — bipolar-specific mood tracker. Log: mood, sleep, energy, anxiety, medication. Takes 2 minutes per day. Shows charts of your patterns.

2. **Daylio** — quick mood check-in (tap your mood + one emoji). Takes 30 seconds. Best for building the habit.

3. **Insight Timer** — free meditation. Search: "bipolar", "depression anxiety", "low energy". 5 minutes in the morning can stabilize a day.

### Computer tools:

4. **Logseq** (or **Obsidian**) — Daily journal in your writing environment. One page per day:
   ```
   ## Today’s Mood: 6/10
   ## Sleep: 7 hours
   ## One thing I will do: write 200 words
   ## Post idea: [topic]
   ```

5. **Google Sheet mood log** — Add Apps Script to your mood sheet to email you a weekly average. See TUTORIAL_CSV_AND_GOOGLE_APPS_SCRIPT.md for how to set this up.

---

## Emergency Restart Protocol

When you've stopped everything for days or weeks and need to restart:

**Step 1 (Day 1):** Open Le Chat. Type one topic. Copy the post to your sheet. Set status to `draft`. You're back.

**Step 2 (Day 2):** Read yesterday's draft. If it's good, change status to `publish`. If not, ask Claude to improve it.

**Step 3 (Day 3):** Write one paragraph — not a full post. Add it to a draft.

**Step 4 (Day 4+):** You're back in the rhythm.

**Do NOT:** Try to catch up all at once. Do NOT backdate posts to fill gaps. Gaps in publication dates are invisible to readers and fine.

---

## Weekly Review (15 minutes every Sunday)

```
✓ Check Google Sheet — how many posts published this week?
✓ Check WordPress dashboard — any drafts needing review?
✓ Add 5 new topics to topics.txt
✓ Review mood log in eMoods — any pattern?
✓ Check email for job alerts or responses
✓ Plan next week: pick 3 post topics
```

That's it. 15 minutes. No more.

---

## Medication and Routine Notes

This is not medical advice. These are general principles backed by research:

- **Consistency matters more than perfection.** Taking medication at the same time daily (even if you occasionally miss) is better than irregular use.
- **Sleep is a non-negotiable.** For bipolar disorder, irregular sleep is the most common trigger. Set a sleep time and protect it like a meeting.
- **Exercise is the cheapest mood stabilizer.** Even a 15-minute walk counts. Log it in eMoods to see the correlation.
- **Reduce alcohol.** Alcohol disrupts sleep cycles and interacts with most mood stabilizers.
- **Keep a medication log.** Use the Google Sheet mood tracker to log your medication times and doses. This helps your doctor see patterns.

### Trusted Medical Information Sources

| Source | URL | Notes |
|--------|-----|-------|
| NIMH (US National Institute) | nimh.nih.gov | Official, evidence-based |
| WHO Mental Health | who.int/mental-health | Global guidelines |
| IBPF | ibpf.org | Bipolar-specific support |
| DBSA | dbsalliance.org | Peer support network |
| PubMed | pubmed.ncbi.nlm.nih.gov | Search your specific medication |
| Mind (UK) | mind.org.uk | Plain-English guides |

---

## Speech-to-Text on Low-Energy Days

**Google Docs Voice Typing (browser, no setup):**
1. Open Google Docs
2. Tools → Voice Typing
3. Speak. It types for you.
4. Copy text to Google Sheet

**On your phone:** Open any notes app and use your phone's built-in dictation (microphone button on keyboard).

**With Whisper (best quality):** See TUTORIAL_AUDIO_VIDEO_BANNER_TOOLS.md

---

*This guide was written with the understanding that productivity for neurodivergent people looks different — and that's okay. Systems should serve you, not the other way around.*

*For professional support: nimh.nih.gov · ibpf.org · dbsalliance.org*
