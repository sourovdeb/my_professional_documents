---
type: routine
id: trig_01YUR1tiRy7S75WfMU2YLvC7
name: "Organise and push Claude Code artifacts to education repo"
subject: Infrastructure & Archival
topics: [repo-organisation, storage-sync]
tags: [cadence-hourly, github, google-drive, artifact-config, box, wordpress]
state: active
cron: 44 */5 * * *
created_at: 2026-07-26T06:44:35.133657Z
---

# Organise and push Claude Code artifacts to education repo

| Field | Value |
|---|---|
| Trigger ID | `trig_01YUR1tiRy7S75WfMU2YLvC7` |
| Subject | **Infrastructure & Archival** |
| Topics | `repo-organisation` `storage-sync` |
| Tags | `#cadence-hourly` `#github` `#google-drive` `#artifact-config` `#box` `#wordpress` |
| State | active |
| Schedule | every 5 hours at :44 UTC (`44 */5 * * *`) |
| One-shot at | — |
| Next run | 2026-07-31T15:44:00Z |
| Created | 2026-07-26T06:44:35.133657Z |
| Instruction length | 1,106 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Collect all artifacts and outputs created by Claude Code routines in the repositories (ai_agent_skills, my_professional_documents, wordpress-control). Organise them into the structured folder hierarchy in sourovdeb/ai_agent_skills: skills/, agents/, guides/, tools/, evaluation/, templates/, config/. Create or update README files and INDEX.md as needed. Push all new/changed files to branch claude/jolly-fermi-gkbw49.

Then save a tracker CSV file named AI_Agent_Skills_Organization_<today's date>.csv with columns: id, category, name, type, description, folder, file_count, status, github_url, branch, created_date, last_updated — listing every organised file.

Save this CSV in ALL THREE of these locations:
1. Google Drive — update the spreadsheet at https://docs.google.com/spreadsheets/d/1NZJtgfVtMKptUr2oxzeIZUnndMkftxiWboq-fvrchPI/edit if possible; otherwise upload the CSV to Google Drive root.
2. Box — upload to the folder "free_education - AI Skills Trends" (folder ID: 401080856469).
3. GitHub — commit the CSV to the ai_agent_skills repo at docs/trackers/ on branch claude/jolly-fermi-gkbw49.
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Infrastructure & Archival | 34 |
| AI & Agent Engineering | 20 |
| Content Publishing & Web Ops | 5 |
