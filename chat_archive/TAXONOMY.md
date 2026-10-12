# Taxonomy

Three levels, defined once in `tools/taxonomy.py` and applied by every tool in
this archive. Change the vocabulary there, re-run the tools, and every index
regenerates consistently.

| Level | Cardinality | Purpose |
|---|---|---|
| **Subject** | exactly one per item | Which part of the work this belongs to. The primary filing dimension. |
| **Topic** | zero or more | The specific theme inside that subject. |
| **Tag** | zero or more | Cross-cutting facets — platform, artifact type, cadence, posture. Deliberately cut across subjects. |

An item has one subject so that "where does this live" always has an answer.
Topics and tags are unlimited because real work is cross-cutting; the Photography
tutorial routine is filed under Photography but tagged `#wordpress` because that
is where it publishes.

---

## Subjects

| Subject | Covers |
|---|---|
| **AI & Agent Engineering** | Agent skills, prompts, model parameters, MCP servers, the Claude Code harness itself. |
| **Content Publishing & Web Ops** | Getting content onto the public web and keeping it healthy: WordPress sync, Dev.to, SEO, indexing, monetization. |
| **Psychology & Human Nature** | Research and long-form writing on why people behave as they do — evolutionary drivers, institutional dynamics, influence tactics. |
| **Health, Wellbeing & Productivity** | Health baselines, energy management, neurodivergence-aware productivity scaffolding. |
| **Education & Language Teaching** | ELT craft and free educational material: ELT365, CELTA, learner-facing tutorials. |
| **Photography & Visual Craft** | Photography fundamentals and post-processing, mostly DxO PhotoLab and FilmPack. |
| **Research & Trend Monitoring** | Recurring outward scans: regional trend digests, skills and labour-market shifts, claim audits. |
| **Migration, Law & Admin** | Migration and immigration law content, French administrative navigation. |
| **Career, CV & Job Search** | CV and letter production, portfolio strategy, job sourcing. |
| **Infrastructure & Archival** | Repositories, storage sync, backups, catalogues, scheduling — and this archive. |

## Topics

Grouped by the subject they most often appear under, though any topic may attach
to any item.

**AI & Agent Engineering** — `agent-skill-authoring`, `prompt-engineering`,
`model-parameters`, `mcp-and-connectors`

**Content Publishing & Web Ops** — `wordpress-sync`, `seo-and-indexing`,
`site-monetization`, `article-generation`

**Psychology & Human Nature** — `evolutionary-psychology`,
`institutional-critique`, `mental-health-claims-audit`

**Health, Wellbeing & Productivity** — `neurodivergent-productivity`,
`health-baseline-gating`, `biography-and-life-history`

**Education & Language Teaching** — `elt-lesson-series`, `teacher-training`,
`presentation-decks`, `mindmapping`

**Photography & Visual Craft** — `photography-fundamentals`, `dxo-workflow`

**Research & Trend Monitoring** — `regional-trend-digest`,
`skills-and-labour-trends`

**Migration, Law & Admin** — `migration-policy`, `french-administration`

**Career, CV & Job Search** — `cv-and-letters`, `portfolio-strategy`

**Infrastructure & Archival** — `repo-organisation`, `storage-sync`,
`backup-and-archive`, `scheduling-and-cron`, `pr-and-ci-hygiene`

## Tags

**Platform** — `#wordpress` `#github` `#box` `#google-drive` `#devto` `#gmail`
`#youtube` `#indeed`

**Artifact type** — `#artifact-article` `#artifact-lesson` `#artifact-slides`
`#artifact-script` `#artifact-report` `#artifact-config` `#artifact-mindmap`

**Cadence** — `#cadence-hourly` `#cadence-daily` `#cadence-weekly`
`#cadence-one-shot` (derived from the cron expression, never keyword-matched)

**Posture** — `#automated` `#research-heavy` `#personal-sensitive`
`#public-facing`

`#personal-sensitive` is the one tag worth treating as operational rather than
descriptive: it marks health, medical, therapy and biography material. Both
repositories' WordPress sync already excludes `Biography_and_Medical/`,
`Legal_Documents/`, `therapy_and_wellbeing/` and `Story_of_Sourov/`, and this
tag should be checked before anything is pushed to a public surface.

---

## How classification works

`tools/taxonomy.py` scores an item's title and body against weighted keyword
lists and picks the highest-scoring subject.

Three deliberate design choices:

1. **Word-boundary matching.** Plain substring counting fired `ci` inside
   "social" and `raw` inside "drawn", which was enough to skew whole subjects.
   Needles now match on alphanumeric boundaries.

2. **Titles count fourfold** (`TITLE_WEIGHT = 4`). A title states intent; a body
   drifts into implementation. "Mental health research auditor" names WordPress
   a dozen times because that is where its output lands — not what it is about.

3. **Topics need more than one hit.** A single passing mention is not a topic.
   Subjects and tags have no such floor, since a subject is always assigned and
   tags are cheap.

### When the heuristic is wrong

Some items are genuinely cross-cutting and will land in a defensible-but-wrong
bucket. Rather than bending keyword weights until one item is right and three
others break, record a correction in `overrides.json`:

```json
"trig_011H53zJvL2NN8VuxJ7Nf3ih": {
  "subject": "Psychology & Human Nature",
  "add_topics": ["mental-health-claims-audit"],
  "note": "Why the computed subject was wrong."
}
```

Overrides re-apply on every run, and the `note` is rendered on the item's own
page alongside the subject it replaced — so a correction is visible rather than
silent. Four are currently in force.
