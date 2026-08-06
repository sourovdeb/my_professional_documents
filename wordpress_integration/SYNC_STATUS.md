# WordPress Content Sync Status — 2026-07-21

## Summary

**Status:** ✅ Auth restored, 2 script bugs fixed, 5 drafts pushed live, 1 stray test draft needs manual cleanup

**Live Site (as of 12:39 UTC):** 784 posts, 461 scheduled, 431 drafts | WP 7.0.1 | REST API active

---

## What changed since 2026-07-19

1. **Auth is working again.** The `X-Sourov-Key` bridge (`/wp-json/sourov/v1/ai-post`, `/scheduled`) returned 401 on 2026-07-19; as of this run it returns 200. No credential change was needed.

2. **Fixed: `tags` field bug (silent failure).** `sync_verification.py` in both `my_professional_documents` and `free_education` was still sending `tags` as a string (`"software"`) despite CLAUDE.md claiming this was already fixed on 2026-07-19. Changed to a JSON array (`["software"]`) per the documented API contract.

3. **Fixed: `post_id` vs `id` (misreported failures).** `push_draft()` read `data.get('post_id')` to detect success, but the API actually returns the field as `id`. Every successful push was being logged as a failure and re-queued. **This means the 2026-07-19 "0 pushed, all blocked" status was likely inaccurate for any run that got past auth** — but 07-19's actual blocker was the 401, so no posts were lost that day. Today's run before the fix landed *did* push 5 real drafts while reporting 0 — confirmed via draft count (425→431) and a direct API probe. Fixed now; future runs will log correctly.

4. **Fixed: scan scope was far too broad.** `scan_repositories()` globbed `**/*.md` across entire repos, picking up internal docs (`README.md`, `CLAUDE.md`, `GETTING_STARTED.md`), personal job-search files (`cover-letters-batch-1.md`, `jobs-list.md`), and templates — none of which are blog content. Restricted the scan to the directories CLAUDE.md actually documents as sync sources (`daily_essays/`, `posts/`, `guides/`, `AI_Lessons/`, `Growth_Hub/`, `initiatives/`, etc. for this repo; `elt365_lessons/`, `routines/` for `free_education`), and excluded filenames containing "template".

## Pushed this run (5, batch-limited per existing policy)

| Title (as generated from filename) | Category | Source |
|---|---|---|
| 2026 06 02 Understanding Trauma Treatment | Mental Health | `daily_essays/2026-06-02_understanding_trauma_treatment.md` |
| 2026 05 30 The System Carries The Day | Software | `posts/published/2026-05-30-the-system-carries-the-day.md` |
| 2026 07 05 Chemical Imbalance Audit | Mental Health | `posts/drafts/2026-07-05-chemical-imbalance-audit.md` |
| 2026 06 03 La Reunion Edge | ELT Masterclass | `posts/drafts/2026-06-03-la-reunion-edge.md` |
| 2026 06 02 Teaching Ielts With Adhd | ELT Masterclass | `posts/drafts/2026-06-02-teaching-ielts-with-adhd.md` |

**Known issues with this batch (flagged, not fixed automatically):**
- Titles are auto-generated from filenames (e.g. `2026 05 30 The System Carries The Day`) rather than the actual post titles — lower quality than a human-written title.
- "2026 05 30 The System Carries The Day" is very likely a **duplicate** of existing post ID 88, "The System Carries The Day The Person Can't" — dedup only matches on exact title string, and these differ, so it wasn't caught. Recommend manually deleting one copy in WP admin.
- "2026 07 05 Esketamine Breakthrough Or Marketing" was scanned but not in this batch of 5 — will push next run along with ~52 remaining new items (still batch-limited to 5/run per existing policy).

## Not attempted (by design)

- **FTP and the `deploy.php` gateway were not used.** The 2026-07-06 incident report (`WordPress_Incidents/2026-07-06_Critical_Error/`) documents that uploading PHP files via `deploy.php` directly into `wp-content/` previously caused a ~2-4 hour site outage (critical error + duplicate content) because single-file scripts were misidentified as plugins. The documented REST bridge (`ai-post`) is sufficient for drafting content and carries none of that risk, so it was used exclusively.
- **A stray test draft (ID 3360, "TEST PROBE - delete me - sync diagnostic") was created while diagnosing the `id`/`post_id` bug.** There's no delete endpoint (documented known issue #3) — needs manual removal from WP admin.
- **Open PRs were not merged.** `my_professional_documents` has 4+ open PRs (#83, #82, #81, #80) and `free_education` has 8+ (#48 down to #38) with substantial unmerged content (daily human-nature articles, psychology audits, EU education project). Two are explicitly documented as conflicting with each other (#39 vs #37 in free_education). Merging is a shared-state, hard-to-reverse action with real conflict risk — left for explicit review rather than auto-merged.
- **Note for follow-up:** PRs #82/#83 in `my_professional_documents` describe a separate, out-of-repo automation (cron jobs in `/etc/cron.d/`, credentials stored in `/home/user/skills/writer/references/wordpress-sync-setup.md`, scripts in `/home/user/scripts/wordpress-sync/`) built in an earlier session for dev.to/Ghost/Box publishing. That infrastructure is outside version control and wasn't verified in this run — worth an owner review.

---

**Generated:** 2026-07-21 12:40 UTC
**By:** Claude AI (automated content sync routine)
**Repo branch:** `sourov/epic-bohr-jx4ce4`
