---
type: routine
id: trig_016byhp493o4ixVaBchvt1jj
name: "GitHub duplicate flagger"
subject: Infrastructure & Archival
topics: []
tags: [cadence-one-shot, github, public-facing]
state: one-shot (fired)
cron: null
created_at: 2026-07-10T08:52:03.932558Z
---

# GitHub duplicate flagger

| Field | Value |
|---|---|
| Trigger ID | `trig_016byhp493o4ixVaBchvt1jj` |
| Subject | **Infrastructure & Archival** |
| Topics | — |
| Tags | `#cadence-one-shot` `#github` `#public-facing` |
| State | one-shot (fired) |
| Schedule | — (`—`) |
| One-shot at | 2026-07-10T13:48:00Z |
| Next run | 2026-07-11T13:48:07.739354371Z |
| Created | 2026-07-10T08:52:03.932558Z |
| Instruction length | 580 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Review recently opened issues in the repository.

1. Read the title and description of each new issue.
2. Search existing open issues for potential duplicates — look for similar titles, overlapping keywords, or the same underlying problem described differently.
3. For each likely duplicate, post a comment linking to the earlier issue and suggesting the reporter review it before proceeding.
4. If an issue appears to be a genuine duplicate, suggest closing it in favor of the linked issue.
5. Reorgaise branch

If there are no new issues or no duplicates found, confirm briefly.
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Infrastructure & Archival | 33 |
