# Weekly Site Audit Agent — Specification & Checklist

**What it is:** a scheduled Claude agent (a "Routine") that wakes up **every Monday at 06:00 UTC**, opens sourovdeb.com like a visitor, runs the checklist below, and files a dated report in this repository (`monitoring/site-audits/`) via a draft pull request. If the site is fine, the report says so in three lines. If something broke, the report says exactly what and how to fix it.

**What it is NOT:** it never logs into WordPress, never asks for or uses credentials, never changes the live site, and never spends money. It reads the public site and writes reports — nothing else. All fixes remain manual, guided by the report.

**Why this design is the safe one:** an agent that can only *read* the site can't break the site. Guaranteed-harmless beats theoretically-convenient.

---

## The checklist the agent runs (v1)

Each item is marked ✅ PASS / ❌ FAIL / ⚠️ WARN in the report.

### A. Availability
1. Homepage loads over HTTPS with HTTP 200 (no maintenance page, no "coming soon").
2. At least 2 recent posts load correctly.
3. Each main-menu category page loads and shows at least 1 post (no empty categories).

### B. Monetization compliance (AdSense-critical)
4. Privacy Policy page exists and is linked in the footer.
5. Cookie consent banner appears on first load.
6. Contact page reachable from the navigation.

### C. Content quality
7. No obvious typos in post titles on the homepage (spell-check pass on titles).
8. No post filed in a clearly wrong category (e.g. photography under English Teaching).
9. Homepage has a meta description and a meta title (view page source).
10. Recent posts have meta descriptions.

### D. Theme health
11. Exactly ONE "You Might Also Like" / related-posts block per post.
12. Exactly ONE prev/next navigation per post.
13. No broken internal links on the sampled pages.

### E. Trend line
14. Note anything new vs. the previous report in `monitoring/site-audits/` (fixed items, new issues).

---

## Report format

File: `monitoring/site-audits/YYYY-MM-DD-audit.md`

```
# Site Audit — YYYY-MM-DD
**Overall:** 🟢 healthy / 🟡 minor issues / 🔴 action needed

| # | Check | Result | Note |
|---|---|---|---|
| 1 | Homepage 200 | ✅ | — |
| ... |

## Action items (only if any)
1. [what broke] → [exact fix, referencing implementation-manual.md section]

## Changes since last audit
- ...
```

---

## How the Routine is wired

- **Schedule:** every Monday 06:00 UTC (`0 6 * * 1`), each run in a fresh session.
- **Steps per run:** fetch site pages → run checklist → write report → commit on an audit branch → open/refresh a **draft PR** → send a completion notification (push + email).
- **Cost note:** each run uses some Claude usage from the owner's plan. Weekly is a sensible balance; monthly is cheaper, daily is unnecessary.

### Owner controls (no coding needed — just tell Claude in any session)

- **Pause:** "pause the weekly site audit routine" (it can be re-enabled anytime).
- **Change schedule:** "run the site audit monthly instead."
- **Stop forever:** "delete the weekly site audit routine."
- **Run now:** "fire the site audit routine now."

### Evolving the checklist

The agent reads THIS file each run. To change what gets checked, edit the checklist above and merge — the next run picks it up automatically. (v2 ideas once AdSense is live: check ads render, check ad density isn't excessive, check Core Web Vitals via PageSpeed.)
