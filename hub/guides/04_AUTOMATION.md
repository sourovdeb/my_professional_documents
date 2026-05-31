# 4 — Automation: find jobs and people while you rest

The goal: the machine searches, drafts, and tracks; **you only review and press
send.** Everything here uses official APIs or legal methods. You insisted on
"official and legal sources" — this guide holds that line, because a scraping ban
or account block would cost you more energy than it saves.

## What you already have — use it first
- **Indeed (connected here):** search jobs by keyword/location and pull details.
- **Gmail (connected here):** create email drafts in bulk — *drafts, never
  auto-send*, so you stay in control and stay human.
- **Google Drive (connected here):** store your CV variants and tracker.
- **Your Chrome extension** (`sidepanel.js`, `background.js`) and the Gmail Bulk
  Draft skill — already built. Recycle them; don't rebuild.

## The job pipeline (review-only, you stay in the loop)

1. **Search** (Indeed) → English trainer / formateur d'anglais / IELTS / TOEIC /
   Business English, in your cities. Save results to a Google Sheet tracker.
2. **Filter** → drop anything that doesn't fit your energy and accommodations.
3. **Draft** (Gmail) → one tailored draft per role, using your cover-letter
   template. The system fills company + role; you add the human sentence.
4. **Track** (Sheet) → company, date, status, follow-up date.
5. **Follow up** → a reminder 5 days later. Most replies come from the follow-up.

Tell me "run the job search for X in Y" and I can do steps 1, 3, 4 with the tools
already connected — leaving you the final read-and-send.

### LinkedIn — the honest version
LinkedIn's terms **prohibit scraping**, and tools that do it get accounts
banned. Stay legal and effective instead:
- Set **LinkedIn job alerts** (official, free) → they email you matches daily.
- Pull those alert emails into your tracker (Gmail can label/forward them).
- Apply manually to the few that fit; spend the saved energy on a good message.

### Aggregating legally
- **Indeed** here (official). **France Travail (Pôle emploi) API** is official and
  free for French listings: https://francetravail.io
- The open-source **JobSpy** library aggregates several boards — useful, but
  check each board's terms before relying on it. Official APIs first.

## Find writers & like-minded partners (legal, human)
- **Substack** "Recommendations" + Notes — find writers in your themes, reply,
  then propose a collaboration. This is the warmest channel.
- **Indie communities:** dev.to, Hashnode, IndieWeb, Reddit r/TEFL & r/writing —
  search, contribute, *then* reach out. Never cold-spam.
- **Track outreach** in the same tracker as jobs (guide 6).
- Automate the *finding* and *drafting*; keep the *first hello* personal. People
  can tell. A real first line beats a perfect template.

## n8n: your free automation hub (optional, when ready)
Self-host **n8n** (open-source) for "when X then Y" flows you own:
- New job-alert email → add row to tracker → draft a reply.
- New blog post published → share to socials → add to a "sent" log.
Start with one flow. Add the second only when the first runs for a week.

## Secrets — never commit these
WordPress FTP, SMTP, and API keys must never enter a repo (especially a public
one). Keep them in an **untracked** local file:

```
# .env  (this name is already in .gitignore — git will not track it)
WORDPRESS_FTP_HOST=...
WORDPRESS_FTP_USER=...
WORDPRESS_FTP_PASS=...
SMTP_USER=...
SMTP_PASS=...
```

For GitHub Actions, use **repository Secrets** (Settings → Secrets and variables
→ Actions), not files. If a secret ever lands in git history, rotate it
immediately — assume it's compromised.
