# LLM Wiki - Complete Guide

**Source:** Andrej Karpathy's LLM Wiki Pattern  
**Last Updated:** April 2026

---

## Table of Contents

1. [The Core Idea](#the-core-idea)
2. [Architecture](#architecture)
3. [Operations](#operations)
4. [Indexing and Logging](#indexing-and-logging)
5. [Optional CLI Tools](#optional-cli-tools)
6. [Tips and Tricks](#tips-and-tricks)
7. [Why This Works](#why-this-works)
8. [Token Optimization with sqz](#token-optimization-with-sqz)
9. [Use Cases](#use-cases)
10. [Community Implementations](#community-implementations)

---

## The Core Idea

### Problem with Traditional RAG

Most people's experience with LLMs and documents looks like RAG (Retrieval-Augmented Generation):
- Upload a collection of files
- LLM retrieves relevant chunks at query time
- Generates an answer

**The problem:** The LLM is rediscovering knowledge from scratch on every question. There's no accumulation. When you ask a subtle question requiring synthesis of five documents, the LLM has to find and piece together relevant fragments every time. Nothing is built up.

Systems like NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

### The Different Approach: LLM Wiki

Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources.

**When you add a new source:**
- The LLM doesn't just index it for later retrieval
- It reads the source
- Extracts key information
- Integrates it into the existing wiki
- Updates entity pages
- Revises topic summaries
- Notes where new data contradicts old claims
- Strengthens or challenges the evolving synthesis

**Key insight:** The wiki is a persistent, compounding artifact.
- Cross-references are already there
- Contradictions have already been flagged
- Synthesis already reflects everything you've read
- Wiki keeps getting richer with every source
- AND with every question you ask

### How It Works in Practice

You typically have two windows open:
1. **LLM agent** on one side
2. **Obsidian** (or similar) on the other

- LLM makes edits to the wiki based on conversation
- You browse results in real-time
- Follow links, check graph view, read updated pages
- **Obsidian becomes the IDE**
- **LLM becomes the programmer**
- **Wiki becomes the codebase**

---

## Architecture

The system has **three layers:**

### Layer 1: Raw Sources
- Your curated collection of source documents
- Articles, papers, images, data files
- **Immutable** — LLM reads from them but never modifies
- This is your **source of truth**

### Layer 2: The Wiki
- Directory of LLM-generated markdown files
- Summaries, entity pages, concept pages, comparisons, overviews, syntheses
- **LLM owns this layer entirely**
- Creates pages, updates when new sources arrive
- Maintains cross-references
- Keeps everything consistent
- You read it; the LLM writes it

### Layer 3: The Schema
- A document (e.g., `CLAUDE.md`, `AGENTS.md`)
- Tells the LLM how the wiki is structured
- Documents conventions
- Specifies workflows for:
  - Ingesting sources
  - Answering questions
  - Maintaining the wiki
- **This is the key configuration file**
- Makes the LLM a disciplined wiki maintainer rather than a generic chatbot
- You and the LLM co-evolve this over time

---

## Operations

### 1. Ingest
You drop a new source into the raw collection and tell the LLM to process it.

**Example flow:**
1. LLM reads the source
2. Discusses key takeaways with you
3. Writes a summary page in the wiki
4. Updates the index
5. Updates relevant entity and concept pages across the wiki
6. Appends entry to log

A single source might touch **10-15 wiki pages**.

**Two approaches:**
- **Incremental (Recommended):** Process sources one at a time, stay involved, read summaries, check updates, guide the LLM on emphasis
- **Batch:** Ingest many sources at once with less supervision

### 2. Query
You ask questions against the wiki.

**Process:**
1. LLM searches for relevant pages
2. Reads them
3. Synthesizes an answer with citations

**Answer formats can be:**
- Markdown page
- Comparison table
- Slide deck (Marp)
- Chart (matplotlib)
- Canvas visualization

**Important:** Good answers can be filed back into the wiki as new pages. Comparisons you asked for, analyses, connections you discovered — these are valuable and shouldn't disappear into chat history. Your explorations compound in the knowledge base.

### 3. Lint
Periodically, ask the LLM to health-check the wiki.

**Look for:**
- Contradictions between pages
- Stale claims that newer sources have superseded
- Orphan pages with no inbound links
- Important concepts mentioned but lacking their own page
- Missing cross-references
- Data gaps that could be filled with web search

The LLM is good at suggesting:
- New questions to investigate
- New sources to look for
- How to strengthen the wiki structure

This keeps the wiki healthy as it grows.

---

## Indexing and Logging

Two special files help navigate the wiki as it grows. They serve different purposes.

### index.md - Content-Oriented
- Catalog of everything in the wiki
- Each page listed with link, one-line summary, metadata (date, source count)
- Organized by category (entities, concepts, sources, etc.)
- **LLM updates it on every ingest**
- When answering a query, LLM reads index first to find relevant pages, then drills into them
- Works well at moderate scale (~100 sources, ~hundreds of pages)
- Avoids need for embedding-based RAG infrastructure

### log.md - Chronological
- Append-only record of what happened and when
- Records: ingests, queries, lint passes

**Pro tip for parseable logs:**
If each entry starts with consistent prefix, log becomes parseable with unix tools:
```bash
# Example log format
## [2026-04-02] ingest | Article Title
## [2026-04-03] query | Question about X
## [2026-04-03] lint | Wiki health check
```

Then: `grep "^## \[" log.md | tail -5` gives you last 5 entries

**Benefits:**
- Timeline of wiki's evolution
- Helps LLM understand what's been done recently
- Historical context for decisions

---

## Optional CLI Tools

At some point you may want to build small tools for the LLM to operate on the wiki more efficiently.

### Search Engine (Most Obvious)
At small scale, the index file is enough. As wiki grows, you want proper search.

**Recommended:** [qmd](https://github.com/tobi/qmd)
- Local search engine for markdown files
- Hybrid BM25/vector search
- LLM re-ranking
- All on-device
- Both CLI (LLM can shell out to it)
- AND MCP server (LLM can use as native tool)

### Custom Tools
You could build something simpler yourself — the LLM can help you "vibe-code" a naive search script as needs arise.

---

## Tips and Tricks

### Obsidian Web Clipper
- Browser extension that converts web articles to markdown
- Very useful for quickly getting sources into your raw collection

### Download Images Locally
- Obsidian Settings → Files and links
- Set "Attachment folder path" to fixed directory (e.g., `raw/assets/`)
- Obsidian Settings → Hotkeys
- Search "Download" for "Download attachments for current file"
- Bind to hotkey (e.g., Ctrl+Shift+D)
- After clipping article, hit hotkey and all images download locally
- Optional but useful — lets LLM view and reference images directly
- Note: LLMs can't read markdown with inline images in one pass — workaround is LLM reads text first, then views referenced images separately

### Obsidian Graph View
- Best way to see shape of your wiki
- What's connected to what
- Which pages are hubs
- Which are orphans

### Marp for Presentations
- Markdown-based slide deck format
- Obsidian plugin available
- Useful for generating presentations directly from wiki content

### Dataview Plugin
- Runs queries over page frontmatter
- If LLM adds YAML frontmatter to wiki pages (tags, dates, source counts)
- Dataview can generate dynamic tables and lists

### Git Version Control
- Wiki is just a git repo of markdown files
- Get version history, branching, collaboration for free

---

## Why This Works

### The Human Problem with Knowledge Bases

The tedious part of maintaining a knowledge base is **not** reading or thinking — it's the **bookkeeping**:
- Updating cross-references
- Keeping summaries current
- Noting when new data contradicts old claims
- Maintaining consistency across dozens of pages

Humans abandon wikis because **maintenance burden grows faster than value**.

### The LLM Solution

- **LLMs don't get bored**
- **Don't forget to update a cross-reference**
- **Can touch 15 files in one pass**
- **Wiki stays maintained because cost of maintenance is near zero**

### Division of Labor

- **Human's job:** Curate sources, direct analysis, ask good questions, think about what it all means
- **LLM's job:** Everything else (bookkeeping, maintenance, consistency)

### Historical Parallel

Related in spirit to **Vannevar Bush's Memex (1945)**:
- Personal, curated knowledge store
- Associative trails between documents
- Connections between documents as valuable as documents themselves
- Bush's vision was closer to this than what the web became
- Private, actively curated, with connections as valuable as content
- The part he couldn't solve: **who does the maintenance?**
- **The LLM handles that.**

---

## Token Optimization with sqz

**Problem:** Most token waste isn't from verbose content — it's from **repetition**.

A 2,000-token file read 5 times = 10,000 tokens gone.

### sqz Solution

**sqz keeps a SHA-256 content cache:**
- **First read** → compresses normally
- **Every subsequent read** → returns 13-token inline reference instead of full content
- LLM still understands it

### Real Numbers from Sessions

| Category | Savings | Method |
|----------|---------|--------|
| Repeated file reads (5x) | 86% | Dedup cache: 13-token ref after first read |
| JSON API responses with nulls | 7–56% | Strip nulls + TOON encoding |
| Repeated log lines | 58% | Condense stage collapses duplicates |
| Large JSON arrays | 77% | Array sampling + collapse |
| Stack traces | 0% | Intentional — error content is sacred |

### Philosophy

Aggressive compression can save more tokens on paper, but:
- If it strips context from errors
- Drops lines from diffs
- **→ LLM gives worse answers**
- **→ You spend more tokens fixing mistakes**

**sqz compresses what's safe and preserves what's critical.**

### Installation

```bash
cargo install sqz-cli
sqz init
```

### Works Across 4 Surfaces

- Shell hook → auto-compresses CLI output
- MCP server → compiled Rust (not Node)
- Browser extension → Firefox approved (ChatGPT, Claude, Gemini, Grok, Perplexity, GitHub Copilot)
- IDE plugins → JetBrains, VS Code

---

## Use Cases

### Personal

Tracking your own goals, health, psychology, self-improvement:
- Filing journal entries
- Articles, podcast notes
- Building structured picture of yourself over time

### Research

Going deep on a topic over weeks or months:
- Reading papers, articles, reports
- Incrementally building comprehensive wiki
- Evolving thesis with evidence

### Reading a Book

Filing each chapter as you go, building out pages for:
- Characters
- Themes
- Plot threads
- How they connect

By end you have rich companion wiki. Think of fan wikis like Tolkien Gateway — thousands of interlinked pages covering characters, places, events, languages, built by community over years. You could build personally while reading.

### Business/Team

Internal wiki maintained by LLMs:
- Fed by Slack threads
- Meeting transcripts
- Project documents
- Customer calls
- Possibly humans in loop reviewing updates
- Wiki stays current because LLM does maintenance nobody wants

### Other Applications

- Competitive analysis
- Due diligence
- Trip planning
- Course notes
- Hobby deep-dives
- Anything where accumulating knowledge over time and wanting it organized

---

## Community Implementations

The gist has inspired numerous implementations:

### Tools & Projects

1. **Synthadoc** - Production-ready system
2. **llmwiki-cli** - JavaScript CLI tool
3. **WeKnora** - Tencent's implementation with knowledge graphs
4. **Beever Atlas** - For chat memory, Apache 2.0
5. **WikiLoom** - Python CLI with focus on deterministic structure
6. **SwarmVault** - Multi-agent memory with 48+ integrations
7. **ΩmegaWiki** - 23 Claude Code skills, bilingual, ~400 stars
8. **OmegaWiki** - Active development with typed entities and edges
9. **TheKnowledge** - Emphasizes citation grounding and multi-source pipelines
10. **llm-wiki-coordination** - Protocol for multi-AI consensus
11. **Origin** - Desktop app (Tauri + Rust) with background daemon
12. **Link** - MCP-compatible with interactive graph view

### Key Insights from Implementations

- **Scale wall is real** - index.md becomes bottleneck; inverted token index solves it
- **Agents re-derive context** - context packs and graph neighborhoods help
- **MCP makes it composable** - wrap search and graph as tools
- **Quality gate before storage** - filtering noise matters more than retrieval
- **Citation grounding works** - mandatory source citations prevent hallucination
- **Audit trails aid debugging** - git log of operations provides forensics
- **Multi-agent coordination needs protocol** - drift, parallel work, and policy boundaries need explicit handling

---

## Getting Started

### Step 1: Create Your Schema
Define how your wiki should be structured. Create a file like `CLAUDE.md` or `AGENTS.md` that describes:
- Directory structure
- Naming conventions
- What types of pages exist
- Workflows for different operations
- Tools and preferences

### Step 2: Set Up Directory Structure
```
my-wiki/
├── raw/                 # Immutable sources
│   ├── articles/
│   ├── papers/
│   └── ...
├── wiki/                # LLM-generated knowledge
│   ├── entities/
│   ├── concepts/
│   ├── syntheses/
│   └── ...
├── index.md             # Content catalog
├── log.md               # Append-only history
└── CLAUDE.md            # Schema/instructions
```

### Step 3: Start with One Source
- Drop a source into `raw/`
- Tell LLM to ingest it
- Stay involved in the process
- Guide what gets emphasized

### Step 4: Build Incrementally
- Add sources one at a time
- Let wiki grow organically
- Run lint passes periodically
- Answer questions against wiki
- File good answers back as new pages

### Step 5: Refine Your Schema
- As patterns emerge, document them in schema
- Update conventions based on what works
- Share learnings with LLM for future sessions

---

## Key Takeaways

1. **Wiki is a compounding artifact** — knowledge accumulates and gets richer over time
2. **Three-layer architecture** — raw sources, wiki, schema provides clarity
3. **LLM does bookkeeping** — focus on curation and direction, not maintenance
4. **Cross-references are valuable** — maybe more valuable than content itself
5. **Modular and optional** — pick what works for your domain, ignore what doesn't
6. **Works at scale** — can handle hundreds of sources and complex relationships
7. **LLM-friendly** — designed for agents to work with effectively
8. **Git-native** — version control and collaboration come free
9. **Quality gates matter** — don't let noise into the wiki
10. **It's a pattern, not a prescription** — adapt to your needs and context

---

## Reference

- **Original Gist:** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- **Community Hub:** Check gist comments for latest implementations
- **License:** Typically MIT or Apache 2.0 across implementations

---

*Document compiled April 2026. Visit the gist for the latest updates and community implementations.*
