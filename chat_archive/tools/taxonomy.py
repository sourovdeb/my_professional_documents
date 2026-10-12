"""Controlled vocabulary for the chat archive.

One place defines every subject, topic and tag. Both the routine snapshotter and
the session archiver import from here so a term never means two things in two
files.

Structure:
    SUBJECTS  - ten top-level buckets. Every archived item gets exactly one.
    TOPICS    - narrower themes inside a subject. An item may get several.
    TAGS      - cross-cutting facets (tool, artifact type, cadence, state).
                They deliberately cut across subjects.

Matching is keyword-based over the item's title plus body. Rules are ordered by
weight, so a routine mentioning both "WordPress" and "psychology" lands in the
subject whose keywords score highest rather than whichever appeared first.
"""

# --- Subjects: keyword -> weight. Highest total score wins. --------------------

SUBJECTS = {
    "AI & Agent Engineering": {
        "keywords": {
            "agent skill": 5, "agent": 2, "llm": 3, "prompt": 3, "mcp": 4,
            "claude": 2, "mistral": 3, "openclaw": 4, "ai concept": 5,
            "ai lesson": 5, "ai term": 5, "temperature": 3, "token": 3,
            "system prompt": 4, "model": 2, "skill": 2, "subagent": 4,
        },
        "description": (
            "Building and tuning AI systems: agent skills, prompts, model "
            "parameters, MCP servers, the Claude Code harness itself."
        ),
    },
    "Content Publishing & Web Ops": {
        "keywords": {
            "wordpress": 5, "sourovdeb.com": 4, "publish": 3, "draft": 2,
            "seo": 4, "indexnow": 4, "dev.to": 5, "devto": 5, "plugin": 3,
            "css": 2, "sitemap": 4, "search console": 4, "404": 3,
            "schedule post": 4, "site": 1, "blog post": 3, "monetization": 4,
            "advertiser": 4, "traffic": 3, "content strategy": 5,
            "editorial": 4,
        },
        "description": (
            "Getting content onto the public web and keeping it healthy: "
            "WordPress sync, Dev.to, SEO, indexing, site monetization."
        ),
    },
    "Psychology & Human Nature": {
        "keywords": {
            "dark psychology": 5, "evolutionary psychology": 5, "human nature": 5,
            "obedience": 4, "psychology": 3, "shadow": 3, "trauma": 4,
            "dopamine": 4, "self-deception": 4, "institutional": 3,
            "propaganda": 4, "manipulation": 3, "behaviour": 2, "behavior": 2,
            "cognitive bias": 4, "persuasion": 3, "neuroscience": 4,
            "human psychology": 5,
        },
        "description": (
            "Research and long-form writing on why people behave as they do — "
            "evolutionary drivers, institutional dynamics, influence tactics."
        ),
    },
    "Health, Wellbeing & Productivity": {
        "keywords": {
            "adhd": 5, "bipolar": 5, "depression": 4, "chronic fatigue": 5,
            "wellness": 4, "mental health": 4, "health": 2, "stability": 3,
            "neurodivergen": 5, "burnout": 4, "productivity": 3, "routine": 1,
            "sleep": 3, "medication": 4, "therapy": 4,
        },
        "description": (
            "Personal operating system: health baselines, energy management, "
            "neurodivergence-aware productivity scaffolding."
        ),
    },
    "Education & Language Teaching": {
        "keywords": {
            "elt": 5, "celta": 5, "english teaching": 5, "lesson": 2,
            "teaching": 3, "student": 3, "classroom": 4, "pronunciation": 4,
            "curriculum": 4, "tutorial": 2, "course": 3, "learner": 3,
            "elt365": 5, "language teaching": 5,
        },
        "description": (
            "English language teaching craft and free educational material: "
            "ELT365 lessons, CELTA material, learner-facing tutorials."
        ),
    },
    "Photography & Visual Craft": {
        "keywords": {
            "photography": 5, "dxo": 5, "photolab": 5, "filmpack": 5,
            "exposure": 4, "gamma": 4, "contrast": 3, "sharpness": 4,
            "aperture": 4, "shutter": 3, "lightroom": 4, "raw": 2,
        },
        "description": (
            "Photography fundamentals and post-processing workflow, mostly "
            "DxO PhotoLab and FilmPack teaching material."
        ),
    },
    "Research & Trend Monitoring": {
        "keywords": {
            "trend": 4, "digest": 4, "asia": 3, "india": 3, "market": 2,
            "research": 2, "monitor": 3, "scan": 3, "job market": 4,
            "workforce": 4, "report": 2, "audit claims": 4, "survey": 2,
        },
        "description": (
            "Recurring outward scans: regional trend digests, skills and "
            "labour-market shifts, claim audits."
        ),
    },
    "Migration, Law & Admin": {
        "keywords": {
            "migration law": 5, "asylum": 5, "refugee": 5, "visa": 5,
            "immigration": 5, "residence permit": 5, "france travail": 4,
            "french admin": 4, "prefecture": 4, "legal": 2, "statutory": 3,
            "family reunification": 5, "marriage visa": 5,
        },
        "description": (
            "Migration and immigration law content plus French administrative "
            "navigation."
        ),
    },
    "Career, CV & Job Search": {
        "keywords": {
            "cv": 5, "resume": 5, "motivation letter": 5, "cover letter": 5,
            "job search": 5, "indeed": 4, "portfolio": 4, "recruiter": 4,
            "application": 2, "interview": 3, "open source contribution": 4,
            "employer": 3,
        },
        "description": (
            "Employability work: CV and letter production, portfolio strategy, "
            "job sourcing and tracking."
        ),
    },
    "Infrastructure & Archival": {
        "keywords": {
            "backup": 5, "back up": 5, "archive": 5, "repository": 3, "github": 3,
            "commit": 3, "pull request": 3, "sync": 2, "box": 2,
            "google drive": 4, "catalog": 4, "folder structure": 4,
            "organise": 3, "organize": 3, "manifest": 4, "duplicate": 3,
            "cron": 3, "trigger": 3, "pipeline": 3,
        },
        "description": (
            "The plumbing: repositories, storage sync, backups, catalogues, "
            "scheduling, and this archive itself."
        ),
    },
}

# --- Topics: narrower themes. Substring match, no weighting. -------------------

TOPICS = {
    "agent-skill-authoring": ["agent skill", "skill creator", "skill file", "skills library"],
    "prompt-engineering": ["prompt", "system prompt", "few-shot", "chain of thought"],
    "model-parameters": ["temperature", "token", "context window", "top-p", "sampling"],
    "mcp-and-connectors": ["mcp", "connector", "box api", "wordpress rest"],
    "wordpress-sync": ["wordpress", "ai-post", "sourov-key", "wp-json"],
    "seo-and-indexing": ["seo", "indexnow", "sitemap", "search console", "404", "canonical"],
    "site-monetization": ["monetization", "advertiser", "sponsorship", "donation", "ads"],
    "article-generation": ["article", "deep-dive", "essay", "1000-1500 word"],
    "presentation-decks": ["powerpoint", "pptx", "slide", "speaker note", "deck"],
    "mindmapping": ["mindmap", ".mm", "freemind", "mind map"],
    "evolutionary-psychology": ["evolutionary", "primal", "tribal", "ancestral"],
    "institutional-critique": ["institutional", "empire", "suppression", "state science", "narrative capture"],
    "mental-health-claims-audit": ["chemical imbalance", "pharma", "audit claims", "neuroscience claim"],
    "neurodivergent-productivity": ["adhd", "bipolar", "neurodivergen", "executive function"],
    "health-baseline-gating": ["health gate", "stability baseline", "energy check", "wellness check"],
    "elt-lesson-series": ["elt365", "elt 365", "daily english", "lesson series"],
    "teacher-training": ["celta", "teacher training", "lesson plan"],
    "photography-fundamentals": ["gamma", "exposure", "contrast", "sharpness", "curve"],
    "dxo-workflow": ["dxo", "photolab", "filmpack"],
    "regional-trend-digest": ["asia", "india", "trend digest", "trending topic"],
    "skills-and-labour-trends": ["durable skill", "workforce", "job market", "ai disruption"],
    "migration-policy": ["asylum", "refugee", "visa", "residence permit", "family reunification"],
    "french-administration": ["france travail", "french admin", "prefecture", "caf"],
    "cv-and-letters": ["cv", "resume", "motivation letter", "cover letter"],
    "portfolio-strategy": ["portfolio", "open source contribution", "alternative to degree"],
    "repo-organisation": ["folder structure", "organise", "organize", "repository map", "index.md"],
    "storage-sync": ["box", "google drive", "upload", "catalog"],
    "backup-and-archive": ["backup", "archive", "snapshot", "manifest"],
    "scheduling-and-cron": ["cron", "trigger", "routine", "every hour", "daily at"],
    "pr-and-ci-hygiene": ["pull request", "pr #", "ci", "merge", "duplicate issue"],
    "biography-and-life-history": ["biography", "timeline", "life history", "story of sourov"],
}

# --- Tags: cross-cutting facets. Substring match. ------------------------------

TAGS = {
    # Platforms and tools touched
    "wordpress": ["wordpress", "wp-json", "sourovdeb.com"],
    "github": ["github", "repository", "pull request", "commit", "branch"],
    "box": ["box", "app.box.com"],
    "google-drive": ["google drive", "gdrive", "apps script"],
    "devto": ["dev.to", "devto"],
    "gmail": ["gmail", "email", "inbox"],
    "youtube": ["youtube", "channel", "video script"],
    "indeed": ["indeed"],
    # Artifact types produced
    "artifact-article": ["article", "essay", "blog post"],
    "artifact-lesson": ["lesson", "tutorial", "explainer"],
    "artifact-slides": ["powerpoint", "pptx", "slide", "presentation"],
    "artifact-script": ["python", "script", ".py", "automation script"],
    "artifact-report": ["report", "digest", "audit", "summary"],
    "artifact-config": ["json", "yaml", "config", "settings"],
    "artifact-mindmap": ["mindmap", ".mm"],
    # Cadence
    "cadence-hourly": [],   # set programmatically from cron
    "cadence-daily": [],
    "cadence-weekly": [],
    "cadence-one-shot": [],
    # Posture
    "automated": ["routine", "cron", "trigger", "scheduled"],
    "research-heavy": ["research", "scan", "sources", "peer-reviewed", "citation"],
    "personal-sensitive": ["health", "medical", "adhd", "bipolar", "therapy", "biography"],
    "public-facing": ["publish", "post", "website", "audience", "reader"],
}


import functools
import re


@functools.lru_cache(maxsize=4096)
def _pattern(needle: str) -> "re.Pattern[str]":
    """Word-boundary matcher for a keyword.

    Plain substring counting produced false hits that skewed whole subjects —
    "ci" fired inside "social", "raw" inside "drawn", "box" inside "boxes".
    Boundaries are anchored on alphanumerics only, so multi-word needles and
    ones containing punctuation ("dev.to", ".mm", "pr #") still match.
    """
    escaped = re.escape(needle)
    left = r"(?<![a-z0-9])" if needle[0].isalnum() else ""
    right = r"(?![a-z0-9])" if needle[-1].isalnum() else ""
    return re.compile(left + escaped + right)


def _count(low: str, needle: str) -> int:
    return len(_pattern(needle).findall(low))


# A title states intent; a body drifts into implementation detail. "Mental
# health research auditor" mentions WordPress a dozen times because that is
# where its output lands, which is not what it is *about*. Title hits therefore
# count for more.
TITLE_WEIGHT = 4


def _hits(title: str, body: str, needle: str) -> int:
    """Weighted occurrence count across a title and a body."""
    return TITLE_WEIGHT * _count(title, needle) + _count(body, needle)


def score_subject(title: str, body: str = ""):
    """Return (subject, score_table) for the highest-scoring subject."""
    title, body = title.lower(), body.lower()
    scores = {}
    for subject, spec in SUBJECTS.items():
        total = 0
        for kw, weight in spec["keywords"].items():
            hits = _hits(title, body, kw)
            if hits:
                # Repeats matter but with diminishing return, so one stray
                # mention cannot outvote a genuinely central theme.
                total += weight * min(hits, TITLE_WEIGHT + 2)
        if total:
            scores[subject] = total
    if not scores:
        return "Infrastructure & Archival", scores
    best = max(scores.items(), key=lambda kv: kv[1])[0]
    return best, scores


def match_topics(title: str, body: str = "", limit: int = 6):
    title, body = title.lower(), body.lower()
    hits = []
    for topic, needles in TOPICS.items():
        n = sum(_hits(title, body, x) for x in needles)
        if n > 1:  # a single passing mention is not a topic
            hits.append((topic, n))
    hits.sort(key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in hits[:limit]]


def match_tags(title: str, body: str = "", limit: int = 12):
    title, body = title.lower(), body.lower()
    hits = []
    for tag, needles in TAGS.items():
        if not needles:
            continue
        n = sum(_hits(title, body, x) for x in needles)
        if n:
            hits.append((tag, n))
    hits.sort(key=lambda kv: (-kv[1], kv[0]))
    return [t for t, _ in hits[:limit]]


def cadence_tag(cron: str | None, run_once_at: str | None) -> str | None:
    """Translate a schedule into one cadence tag."""
    if run_once_at:
        return "cadence-one-shot"
    if not cron:
        return None
    fields = cron.split()
    if len(fields) != 5:
        return None
    minute, hour, dom, month, dow = fields
    if hour == "*" or hour.startswith("*/"):
        return "cadence-hourly"
    if dow not in ("*", "?"):
        return "cadence-weekly"
    return "cadence-daily"


def classify(title: str, body: str = "", cron: str | None = None,
             run_once_at: str | None = None):
    """Full classification for one archived item.

    `title` carries TITLE_WEIGHT-fold influence over `body`. Callers with no
    meaningful title (a raw transcript, say) should pass the whole text as
    `body` and leave `title` empty.
    """
    subject, scores = score_subject(title, body)
    tags = match_tags(title, body)
    cad = cadence_tag(cron, run_once_at)
    if cad:
        tags = [cad] + tags
    return {
        "subject": subject,
        "subject_scores": dict(sorted(scores.items(), key=lambda kv: -kv[1])),
        "topics": match_topics(title, body),
        "tags": tags,
    }
