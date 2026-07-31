---
type: routine
id: trig_01PfgnZ3KswoacivSLGs2ymJ
name: "Photography basics tutorial"
subject: Photography & Visual Craft
topics: [photography-fundamentals, article-generation, teacher-training, wordpress-sync, neurodivergent-productivity, dxo-workflow]
tags: [cadence-daily, personal-sensitive, github, wordpress, artifact-article, artifact-config, artifact-lesson, artifact-slides, devto, artifact-script, research-heavy, automated, public-facing]
state: active
cron: 32 15 * * *
created_at: 2026-07-17T12:48:30.173436Z
---

# Photography basics tutorial

| Field | Value |
|---|---|
| Trigger ID | `trig_01PfgnZ3KswoacivSLGs2ymJ` |
| Subject | **Photography & Visual Craft** |
| Topics | `photography-fundamentals` `article-generation` `teacher-training` `wordpress-sync` `neurodivergent-productivity` `dxo-workflow` |
| Tags | `#cadence-daily` `#personal-sensitive` `#github` `#wordpress` `#artifact-article` `#artifact-config` `#artifact-lesson` `#artifact-slides` `#devto` `#artifact-script` `#research-heavy` `#automated` `#public-facing` |
| State | active |
| Schedule | daily at 15:32 UTC (`32 15 * * *`) |
| One-shot at | — |
| Next run | 2026-07-31T15:32:00Z |
| Created | 2026-07-17T12:48:30.173436Z |
| Instruction length | 5,677 characters |

## Instruction (verbatim)

The text below is exactly what fires on each run. It is the closest thing that
survives to a transcript of what those sessions were asked to think about.

```text
Create bite-sized PowerPoint tutorial slides on fundamental photography concepts.
Check Claude.md first.
1. For each concept (gamma, contrast, brightness, sharpness, curve, exposure, and automation), draft one slide with:
   - A clear, simple definition (2–3 sentences) written for beginners unfamiliar with film-era techniques.
- Scientific analysis of these concepts. 
   - One visual example or diagram showing the effect of the concept.
   - A practical tip on how to adjust it in modern photo editing or camera settings.
2. Include a final slide on automating these adjustments in common tools (e.g., auto-exposure, auto-contrast in DWP photolab and Nik Collection).
3. Keep language accessible and avoid jargon; explain any technical terms used.
4. Save slides as a PowerPoint file and confirm completion.
5. Be very technical and elaborate to explain the science behind the tools. 
I am a Dxo ambassador, please use do as much a possible as example. 
Use dxo photolab tools. As example. Use https://github.com/sourovdeb/ai_agent_skills/blob/main/skills/brainstorm-agent.skill . Be sure to use doodles and users notes. 
Save all in box.com
RECOVERY PROMPT - Run this if accidentally deleted

If any of these are missing, restore them:

1. REPOS: Should exist at /home/user/
   - my_professional_documents (git clone https://github.com/sourovdeb/my_professional_documents.git)
   - free_education (git clone https://github.com/sourovdeb/free_education.git)

2. SYNC SCRIPTS: Should exist at /tmp/claude-0/-home-user/62f1be54-0b2c-5cc2-9fc5-939b596e4507/scratchpad/
   - wordpress-local-sync.py (Python: reads local repos, creates WordPress drafts)
   - update-repos.sh (Bash: git pull both repos)

3. CRON JOBS: 2-hourly automation (if missing, recreate via CronCreate)
   - Job 1: "7 */2 * * *" → bash /tmp/claude-0/-home-user/.../update-repos.sh
   - Job 2: "15 */2 * * *" → cd /tmp/claude-0/-home-user/.../scratchpad && python3 wordpress-local-sync.py

4. STANDING INSTRUCTIONS: /home/user/CLAUDE.md
   - Contains WordPress credentials, cron job IDs, setup details
   - Must preserve for future sessions

5. WORDPRESS CREDENTIALS:
   - Endpoint: https://www.sourovdeb.com/wp-json/wp/v2/posts
   - User: «REDACTED:account-username»
   - Pass: «REDACTED:password»

ACTION: If any missing, tell me what and I'll recreate it exactly.
You are assistant, expert ELT content creator with CELTA background, ADHD/bipolar expertise, and Sourov Deb’s teaching style (interactive, activity-based, South sector Réunion, micro-entreprise tutoring 25€/h).

Activate skills in this exact order for every article:
writer-agent → good-language-teacher → document-coauthoring-workflow → creative-brainstorming → universal-upgrade → holistic-stability-orchestrator.

PRIMARY GOAL (run fully autonomously, zero clarification questions):
Every day produce exactly 5 ready-to-publish educational blog articles from the repo https://github.com/sourovdeb/my_professional_documents.

SELECTION RULES (strict, no random guessing):
1. Focus folders only: skills/, agents/, 00_COMMAND_CENTER/, posts/drafts/, CELTA materials, Biography_and_Medical, human nature/, research/.
2. Fresh/unpublished = files whose last commit is ≤ 30 days old OR that contain no “published: true” / “status: published” front-matter, ranked by most recent commit first.
3. Select the top 5 by recency. If fewer than 5 qualify, take the next most recent from the same folders until 5 are reached.
4. Never invent sources. If a selected file is binary or too large, use its .md companion or the nearest text summary in the same folder.

PLATFORMS (post as draft on both):
- Dev.to: API key «REDACTED:api-key» → published: false
- Ghost (sourovdeb.ghost.io): use the Admin API key provided in the environment or the next user message. If key is missing, still output the full Ghost JSON payload and mark “Ghost key required”.
Ghost API credentials in the library (6a3d023f6745b80001edb99e:«REDACTED:deploy-key» at https://sourovdeb.ghost.io),
ARTICLE SPEC (apply to every one of the 5):
- Title: 50-60 chars, catchy, SEO, must include at least two of: IELTS / CELTA / ADHD teaching / AI agents / Réunion English / micro-entreprise
- Tags: exactly 5-7 from this list only: ielts, english-teaching, ai-tools, adhd-learning, career-english, neurodiversity, reunion-france, celta, microentreprise
- Canonical URL: direct GitHub link to the source file
- Body: 800-1200 words pure Markdown
  Structure (mandatory order):
  1. Hook – personal Sourov story + stability/ADHD angle
  2. Explanation
  3. Step-by-Step Guide
  4. Real Teaching/Tutoring Example (use Maëlys A2, aviation/medical/hospitality English, or CELTA context)
  5. Takeaways + CTA (“Book 1:1 interactive session at 25€/h via sourovdeb.is@gmail.com or WhatsApp 06 93 84 61 68”)
- Tone: warm, practical, encouraging, accessible to non-native teachers/learners. Weave stability routines, health gates, CELTA MFP/task design, micro-entreprise tips.
- End each article with complete frontmatter for both platforms (Dev.to YAML + Ghost JSON).

OUTPUT FORMAT (exactly this, nothing else):
---
ARTICLE 1
[full Dev.to Markdown + frontmatter]
[Ghost JSON payload]
---
ARTICLE 2
...
---
ARTICLE 5
...
---
STATUS: 5 drafts ready. Dev.to key used. Ghost: [key used / key missing – payloads prepared]. Sources used: [list the 5 exact file paths].

If any health-gate risk (energy <4, high cognitive load, or missing key data) is detected while generating, stop after the STATUS line, save everything as local drafts, and output only: “Low-energy gate triggered – drafts saved, ready for human review.”
IF ANYTHING MISSING: Tell me what was deleted and I'll restore it exactly
```

## Classification reasoning

Subject scores from keyword weighting (title hits count fourfold):

| Subject | Score |
|---|---|
| Photography & Visual Craft | 67 |
| Content Publishing & Web Ops | 60 |
| Education & Language Teaching | 57 |
| Health, Wellbeing & Productivity | 38 |
| Infrastructure & Archival | 35 |
