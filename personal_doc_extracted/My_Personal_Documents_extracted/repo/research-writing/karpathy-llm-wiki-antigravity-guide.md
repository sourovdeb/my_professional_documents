# Karpathy's LLM Wiki: Complete Implementation Guide
## (Based on Antigravity.codes Deep Dive - April 2026)

**Source:** https://antigravity.codes/blog/karpathy-llm-wiki-idea-file  
**Original Gist:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

---

## Overview

This is a comprehensive summary of Andrej Karpathy's LLM Wiki pattern as explained in depth by the Antigravity team. The original idea file went viral in April 2026, introducing a new "idea file" format for the AI agent era.

**Key Concept:** Instead of sharing specific code/tools, share the idea. Let each person's LLM agent customize it for their needs.

---

## 1. The Core Insight: Wiki Beats RAG

### The RAG Problem
- Traditional RAG: Upload files → Search on query → Generate answer
- Problem: LLM rediscovers knowledge from scratch on **every question**
- No accumulation, no synthesis persisting
- Examples: NotebookLM, ChatGPT file uploads

### The Wiki Solution
- LLM **incrementally builds** a persistent wiki (markdown files)
- When a new source arrives: LLM reads it, extracts info, **integrates into existing wiki**
- Updates entity pages, concept pages, summaries
- Flags contradictions, strengthens synthesis
- **Knowledge compiled once**, then kept current

### The Compounding Effect
- Cross-references pre-built
- Contradictions already flagged
- Synthesis reflects everything read
- Wiki gets richer with every source **and every question**

---

## 2. The Three-Layer Architecture

### Layer 1: Raw Sources (Immutable)
```
raw/
├── articles/
├── papers/
├── repos/
├── data/
├── images/
└── assets/
```
- Your curated collection of source documents
- **NEVER modified by LLM** (source of truth)
- Can trace back any wiki claim to original

### Layer 2: The Wiki (LLM-Owned)
```
wiki/
├── index.md                 # Master catalog
├── log.md                   # Activity record
├── overview.md              # High-level synthesis
├── concepts/                # Concept pages
├── entities/                # Organization/people pages
├── sources/                 # Source summaries
├── comparisons/             # Analysis pages
└── [other custom sections]
```
- LLM-generated markdown files
- Pre-digested, cross-referenced
- What a research assistant would produce after reading everything

### Layer 3: The Schema (Configuration)
```
CLAUDE.md (for Claude Code)
AGENTS.md (for OpenAI Codex)
OPENCODE.md (for OpenCode)
```
- Tells LLM how wiki is structured
- Documents page conventions
- Specifies workflows (ingest, query, lint)
- **Persists across sessions** (key difference!)
- Turns generic chatbot into disciplined wiki maintainer

**Why Schema Matters:**
Without it: Every session starts from zero, re-explain everything  
With it: LLM knows conventions, formats, workflows → consistency maintained

---

## 3. The Three Operations

### Operation 1: Ingest
**What:** Drop source in `raw/`, tell LLM to process

**Process:**
1. LLM reads source
2. Discusses key takeaways
3. Writes summary in `wiki/sources/`
4. Updates relevant entity pages
5. Updates relevant concept pages
6. Flags contradictions
7. Updates `index.md`
8. Appends to `log.md`

**Result:** Single source might touch **10-15 wiki pages**

**Two Approaches:**
- **Incremental (Recommended):** One source at a time, stay involved, guide emphasis
- **Batch:** Many sources at once, less supervision

### Operation 2: Query
**What:** Ask questions against the wiki

**Process:**
1. LLM searches for relevant pages
2. Reads them
3. Synthesizes answer with citations

**Output Formats:**
- Markdown page
- Comparison table
- Slide deck (Marp)
- Chart (matplotlib)
- Canvas visualization

**Key Insight:** File good answers back as wiki pages!
- Your explorations compound
- Insights don't disappear into chat history
- Wiki grows from your own exploration

### Operation 3: Lint
**What:** Periodic health check

**Look for:**
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages (no inbound links)
- Important concepts lacking their own page
- Missing cross-references
- Data gaps (web search candidates)

**Benefits:**
- Keeps wiki healthy as it grows
- LLM suggests new questions/sources
- Strengthens structure

---

## 4. Indexing and Logging

### index.md (Content-Oriented Catalog)
```markdown
# Wiki Index

## Concepts
- [[attention-mechanism]] — Overview (12 sources)
- [[mixture-of-experts]] — MoE architectures (8 sources)
- [[scaling-laws]] — Chinchilla laws (15 sources)

## Entities
- [[openai]] — GPT series (20 sources)
- [[anthropic]] — Claude series (14 sources)

## Source Summaries
- [[summary-attention-revisited]] — 2026-03-15
- [[summary-moe-efficiency]] — 2026-04-01
```

**When answering queries:**
1. LLM reads index first
2. Identifies relevant pages
3. Reads those pages directly
4. Works well at ~100 sources, hundreds of pages
5. Avoids need for expensive embedding pipelines

### log.md (Chronological Activity Record)
```markdown
## [2026-04-04] ingest | MoE Efficiency Article
Source: raw/articles/2026-04-mixture-of-experts-efficiency.md
Pages created: sources/summary-moe-efficiency.md
Pages updated: concepts/mixture-of-experts.md, concepts/scaling-laws.md
Notes: Contradicts dense-vs-sparse claim below 10B params.

## [2026-04-04] query | MoE Routing Comparison
Question: Compare routing strategies in MoE models
Output: Filed as comparisons/moe-routing-strategies.md

## [2026-04-04] lint | Weekly Health Check
Contradictions found: 2
Orphan pages: 3
Missing pages suggested: 4
```

**Pro Tip:** Use consistent prefixes for unix tools:
```bash
grep "^## \[" log.md | tail -5  # Last 5 entries
```

**Benefits:**
- Timeline of wiki evolution
- Helps LLM understand recent state
- Historical context for decisions

---

## 5. The Tool Stack

### Recommended
- **Obsidian** — IDE for browsing wiki
- **Git** — Version control for knowledge (free collaboration)
- **Web Clipper** — Chrome/Firefox extension for article clipping

### Optional (Scale with Wiki Size)
- **qmd** — Local markdown search (BM25 + vector + LLM re-ranking)
- **Marp** — Generate slide decks from wiki
- **Dataview** — Query frontmatter for dashboards

### Obsidian Setup
1. Set "Attachment folder path" to `raw/assets/`
2. Bind "Download attachments" to hotkey (e.g., Ctrl+Shift+D)
3. After clipping: hit hotkey to download images locally
4. Graph view shows wiki structure (hubs, orphans, connections)

### qmd (When Scaling Beyond index.md)
- Hybrid BM25/vector search with LLM re-ranking
- Works locally, offline
- CLI or MCP server
- Useful when wiki grows to hundreds of pages

---

## 6. Implementation: Step-by-Step

### Step 1: Directory Structure
```bash
mkdir -p my-wiki/raw/{articles,papers,repos,assets}
mkdir -p my-wiki/wiki/{concepts,entities,sources,comparisons}
touch my-wiki/wiki/{index.md,log.md,overview.md}
cd my-wiki && git init
```

### Step 2: Create Schema File
Create `CLAUDE.md` (or `AGENTS.md` / `OPENCODE.md`)

Include:
- Project structure (what's immutable vs. owned)
- Page conventions (YAML frontmatter format)
- Ingest workflow (steps when processing sources)
- Query workflow (how to search and synthesize)
- Lint guidelines (what to check)

### Step 3: Open in Obsidian
1. Install Obsidian
2. Open `my-wiki/` as vault
3. Install plugins: Web Clipper, Marp, Dataview
4. Explore graph view

### Step 4: First Ingest
1. Clip article with Web Clipper → `raw/articles/`
2. Download images with hotkey
3. Tell LLM agent: "Ingest raw/articles/[filename].md"
4. Review summary, guide emphasis
5. Check wiki in Obsidian
6. Commit: `git add . && git commit -m "ingest: [title]"`

### Step 5: Build Over Time
- Ingest 10-20 sources on one topic
- Ask synthetic questions
- File good answers back as wiki pages
- Run lint checks weekly

### Step 6: Evolve Schema
- Document what works/doesn't
- Update schema as you learn
- Refine page types, frontmatter, workflows
- "You and the LLM co-evolve this over time"

---

## 7. Why This Works: The Maintenance Problem

### The Human Problem
Maintaining a knowledge base is tedious:
- Update cross-references
- Keep summaries current
- Note contradictions
- Maintain consistency across pages
- **Maintenance burden grows faster than value**
- Result: Humans abandon wikis

### The LLM Solution
- LLMs don't get bored
- Don't forget cross-references
- Can update 15 files in one pass
- Cost of maintenance is **near zero**

### Division of Labor
- **Human:** Curate sources, direct analysis, ask good questions, think about what it means
- **LLM:** Everything else (bookkeeping, consistency, maintenance)

---

## 8. Use Cases

### Personal Knowledge Base
- Goals, health, psychology, self-improvement
- Journal entries, articles, podcast notes
- Build structured self-understanding over time

### Research
- Going deep on topic over weeks/months
- Reading papers, articles, reports
- Build comprehensive wiki with evolving thesis
- ~100 articles, ~400,000 words on one topic (Karpathy's scale)

### Reading a Book
- File chapters as you go
- Pages for characters, themes, plot threads
- Build personal companion wiki like Tolkien Gateway
- By end: rich interlinked analysis

### Business/Team
- Internal wiki fed by Slack, meetings, documents
- Decision logs, project timelines, customer insights
- Humans in loop reviewing updates
- Wiki stays current (no one wants to do maintenance)

### Everything Else
- Competitive analysis
- Due diligence
- Trip planning
- Course notes
- Hobby deep-dives

**Universal Pattern:** If accumulating knowledge over time, organize via wiki.

---

## 9. Historical Context: The Memex (1945)

### Vannevar Bush's Insight
- 1945: "As We May Think" article in The Atlantic
- Memex: desk-sized machine with microfilm, rapid search
- **Associative trails:** User-created paths linking documents
- "Wholly new forms of encyclopedias will appear, ready-made with a mesh of associative trails"

### Historical Influence
- Inspired Douglas Engelbart → computer mouse, personal computing
- Inspired Ted Nelson → coined "hypertext" (1965)
- Inspired Tim Berners-Lee → World Wide Web (1989)

### Why It Failed
Bush's vision was private, curated, personal. The web became public and chaotic. The missing piece: **who maintains the associative trails?**

**LLM Wiki solves it:** The LLM does the maintenance.

---

## 10. The Idea File Concept

### What's New
Karpathy introduced the "idea file" format:
- Instead of sharing code (implementation-specific)
- Share the idea (design-agnostic)
- Agent customizes to your environment

### Why It Works
- Portable across tools (Claude Code, Codex, OpenCode, Cursor, etc.)
- Portable across OS (macOS, Linux, Windows)
- Agent adapts to your preferences
- You get implementation tailored to your needs

### The Call to Action
"Share it with your LLM agent and work together to instantiate a version that fits your needs. The document's only job is to communicate the pattern. Your LLM can figure out the rest."

---

## 11. Key Takeaways

1. **Wiki > RAG** — Persistent structure beats query-time retrieval
2. **Compounding artifact** — Knowledge grows and compounds over time
3. **Three layers** — Immutable sources, LLM-maintained wiki, persistent schema
4. **Three operations** — Ingest (add sources), query (explore), lint (maintain health)
5. **Index + log** — Simple tools (no embedding pipelines needed at moderate scale)
6. **LLM does bookkeeping** — Humans focus on thinking and curation
7. **Schema is memory** — Persistent configuration across sessions
8. **Idea files matter** — Share patterns, not code, in the AI era
9. **Maintenance is the key** — LLMs solve the burden that kills human wikis
10. **Start small** — 10 sources on one topic, then scale

---

## 12. Getting Started

**For First-Time Users:**

1. Copy Karpathy's gist: https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
2. Paste it to your LLM agent
3. Tell agent: "Set up LLM Wiki for [your topic]"
4. Agent creates structure, writes schema, guides you through first ingest
5. Add 10 sources
6. Ask a synthetic question
7. If you get insights you wouldn't have alone, the system is working

**The 10-Source Test:**
Pick a topic, ingest 10 sources, ask one question that requires synthesis. If wiki-based synthesis beats individual source reading, scale up.

---

## 13. Resources

### Core Documents
- **Original Tweet:** Karpathy, April 3, 2026 (LLM Knowledge Bases)
- **Idea File Follow-up:** Karpathy, April 4, 2026
- **Full Gist:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f

### Tools
- **Obsidian:** https://obsidian.md/
- **qmd:** https://github.com/tobi/qmd (local markdown search)
- **Marp:** https://marp.app/ (markdown presentations)
- **Dataview:** https://blacksmithgu.github.io/obsidian-dataview/

### Historical Reference
- **"As We May Think" (1945):** https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/
- **Memex Concept:** https://en.wikipedia.org/wiki/Memex

### Community
- Gist Discussion tab: Contribute ideas, discuss variations
- Multiple implementations now available (Synthadoc, llmwiki-cli, WeKnora, etc.)

---

## Final Thought

> "The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping."

The LLM Wiki pattern solves this by giving the bookkeeping (the boring part) to an LLM. You keep the thinking (the interesting part). The wiki becomes a persistent, compounding artifact that gets richer with every source and every question you ask.

---

*Document compiled April 29, 2026. Based on comprehensive analysis from Antigravity.codes blog article: "Karpathy's LLM Wiki: The Complete Guide to His Idea File"*
