---
type: routine
id: trig_01QJbhvkxeV2gR66d611zjU5
name: "Dark Psychology Article Generator (4-hour cycle)"
subject: Psychology & Human Nature
topics: [article-generation, institutional-critique, evolutionary-psychology, wordpress-sync]
tags: [cadence-hourly, artifact-article, devto, artifact-script, research-heavy, wordpress, artifact-config, artifact-lesson, automated, github]
state: active
cron: 58 */4 * * *
created_at: 2026-07-26T09:58:21.579902Z
---

# Dark Psychology Article Generator (4-hour cycle)

| Field | Value |
|---|---|
| Trigger ID | `trig_01QJbhvkxeV2gR66d611zjU5` |
| Subject | **Psychology & Human Nature** |
| Topics | `article-generation` `institutional-critique` `evolutionary-psychology` `wordpress-sync` |
| Tags | `#cadence-hourly` `#artifact-article` `#devto` `#artifact-script` `#research-heavy` `#wordpress` `#artifact-config` `#artifact-lesson` `#automated` `#github` |
| State | active |
| Schedule | every 4 hours at :58 UTC (`58 */4 * * *`) |
| One-shot at | — |
| Next run | 2026-07-31T16:58:00Z |
| Created | 2026-07-26T09:58:21.579902Z |
| Instruction length | 1,260 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Generate a new 1000-1500 word deep-dive article on dark psychology, evolutionary psychology, institutional dynamics, or human nature. 

Requirements:
1. Topic: Select from areas like institutional suppression, obedience dynamics, narrative control, psychological warfare, evolutionary traps, covert operations, state science, power structures, or tribal psychology
2. Frontmatter: Include title, tags (as JSON array), published: false, canonical_url pointing to github repo routine
3. Structure: Hook (narrative/case), Historical Patterns (2-3 documented examples), Modern Echoes (contemporary evidence), Implications & Self-Reflection (actionable insight)
4. Academic rigor: Cite 8-12 sources with author/year, end with source list and research gaps
5. ELT keywords: Naturally integrate 2-3 of: blocking vocabulary, receptive/productive knowledge, lesson plan objective, instructional checking questions, should/can distinction, freer practice, semi-formal greetings, choral drilling, listening for gist

Save as: /home/user/daily-drafts/article_[topic-slug]_[timestamp].md
Then sync to WordPress and dev.to via the sync scripts.

Use the existing pipeline: wordpress-local-sync.py and devto-sync.py with SOUROV_WP_KEY and DEVTO_API_KEY environment variables.
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Psychology & Human Nature | 63 |
| Content Publishing & Web Ops | 25 |
| Infrastructure & Archival | 14 |
| Education & Language Teaching | 7 |
| Research & Trend Monitoring | 2 |
