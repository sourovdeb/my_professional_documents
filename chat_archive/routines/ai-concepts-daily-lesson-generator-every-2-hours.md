---
type: routine
id: trig_01BK6HYTUuhyFQ9o43b2WHU9
name: "AI Concepts Daily Lesson Generator (Every 2 Hours)"
subject: Content Publishing & Web Ops
topics: [prompt-engineering, storage-sync, wordpress-sync, seo-and-indexing]
tags: [cadence-hourly, artifact-lesson, artifact-report, github, box, devto, wordpress, artifact-config, artifact-slides, automated, public-facing]
state: active
cron: 58 */2 * * *
created_at: 2026-07-26T09:58:14.210876Z
---

# AI Concepts Daily Lesson Generator (Every 2 Hours)

| Field | Value |
|---|---|
| Trigger ID | `trig_01BK6HYTUuhyFQ9o43b2WHU9` |
| Subject | **Content Publishing & Web Ops** |
| Topics | `prompt-engineering` `storage-sync` `wordpress-sync` `seo-and-indexing` |
| Tags | `#cadence-hourly` `#artifact-lesson` `#artifact-report` `#github` `#box` `#devto` `#wordpress` `#artifact-config` `#artifact-slides` `#automated` `#public-facing` |
| State | active |
| Schedule | every 2 hours at :58 UTC (`58 */2 * * *`) |
| One-shot at | — |
| Next run | 2026-07-31T14:58:00Z |
| Created | 2026-07-26T09:58:14.210876Z |
| Instruction length | 1,302 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
🤖 **AI LESSON GENERATION ROUTINE**

Your task: Create the next AI concept lesson in the series and sync to all platforms.

**Status Check First:**
1. Read `/home/user/ai-lessons-covered.md` — which concept was last created?
2. Pick the NEXT concept from the list (Model → Prompt → System Prompt → Token → etc.)
3. Check if a lesson file already exists for today's date

**If lesson doesn't exist:**
1. Create comprehensive lesson following the What, Where, How, Why framework
2. Save locally: `/home/user/ai-lessons/[date]-[concept].md`
3. Upload to Box (MCP tool)
4. Push to GitHub branch `claude/ai-concepts-lesson-l9woj3`
5. Prepare WordPress JSON payload
6. Update tracking file (`ai-lessons-covered.md`)

**Format Requirements:**
- ✅ Doodle descriptions (for kids to illustrate)
- ✅ PowerPoint outline (5 slides minimum)
- ✅ User notes & speaker notes
- ✅ Dev.to ready-to-publish version
- ✅ Real-world examples & time savings
- ✅ Mistral console walkthrough
- ✅ SEO keywords from Google Search Console report

**Sync Targets:**
- 📦 Box (backup)
- 🐙 GitHub (daily-drafts/)
- 📝 WordPress DRAFT (X-Sourov-Key header)
- 📱 Dev.to DRAFT (API)

**Output Summary:**
Report which lesson was created, file locations, and sync status.

This is a standing recurring task — keep generating until told to stop.
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Content Publishing & Web Ops | 35 |
| AI & Agent Engineering | 34 |
| Infrastructure & Archival | 21 |
| Education & Language Teaching | 12 |
| Research & Trend Monitoring | 4 |
