# 2 — Write: the daily 500-word habit

You asked for "a daily 500-word blog and essay of various topics." Here is the
system that makes it survive bad days. The rule: **500 words, one idea, human
voice, active not passive — but not monotone.**

## The habit, in one screen

1. Open `hub/content/blog/_TEMPLATE_500word.md`.
2. Save a copy as `YYYY-MM-DD_slug.md` in the same folder.
3. Pick one idea from `hub/guides/05_IDEAS.md`.
4. Set a 15-minute timer. Write to the timer, not to perfection.
5. Stop at ~500 words. Read it once aloud. Fix what your mouth stumbles on.
6. Commit it on its own branch (see below). You publish later, on your terms.

If you only have 5 minutes: write the **hook and one paragraph**. That still
counts as showing up. Streaks are built from small days.

## What "good" looks like (your style rules)

- **Active voice.** "I taught the class," not "the class was taught by me."
- **Not monotone.** Vary sentence length. A long, winding sentence that carries
  a thought to its natural end — then a short one. Like that.
- **One idea per piece.** If a second idea shows up, it's tomorrow's post.
- **Show, then tell.** Start with a moment (a student, a street in France, a hard
  morning). Land the point in the last two lines.
- **Cut the throat-clearing.** Delete the first sentence; the second is usually
  your real opening.

## A reliable 500-word shape

- **Hook (1–2 lines):** a scene, a confession, or a sharp claim.
- **Turn (2–3 short paragraphs):** what happened / what you noticed / why it's
  not what people assume.
- **Point (2–3 lines):** the one thing you want the reader to keep.
- **Invitation (1 line):** a question or a "reply if…".

## Per-creation branch workflow (your "stay organised" rule)

You said every creation gets its own branch and you'll copy-paste later. Do this:

```bash
# start a new piece
git checkout main && git pull
git checkout -b draft/2026-05-31-why-i-teach
# ...write your file in hub/content/blog/...
git add hub/content/blog/2026-05-31_why-i-teach.md
git commit -m "draft: why I teach"
git push -u origin draft/2026-05-31-why-i-teach
```

Each draft stays isolated on its branch. You review, copy into WordPress
yourself, then delete the branch. Clean history, nothing half-finished on `main`.

> Note: in *this* assistant session I work on one assigned branch, so I can't
> open a fresh branch per file for you automatically. The command above is the
> 10-second routine to do it yourself — or just tell me the topic and I'll draft
> the file, and you branch it.

## Editing pass (do it the next day, not the same day)

Fresh eyes catch more. One pass for **clarity** (does each sentence earn its
place?), one pass for **voice** (does it sound like a person, not a report?).
Free help: LanguageTool (open-source grammar) — see guide 3.
