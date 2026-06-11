# Writing System

**Goal:** One 500-word essay per day. Active voice. One clear idea per piece. Publish to WordPress, then cross-post.

---

## The Rule

Write first. Edit second. Publish third. In that order, every time.

No essay needs to be perfect. It needs to exist.

---

## Directory Layout

```
03_writing/
├── _ideas/          ← Topic backlog — pull from here each morning
├── _templates/      ← Start new essays from these
├── drafts/          ← Work in progress (one file per essay)
└── essays/          ← Finished, published work (dated)
```

Each piece gets **its own git branch**: `essay/YYYY-MM-DD-slug`.

You copy-paste the final text yourself. Git holds the draft history.

---

## Daily Workflow (15 minutes to start, 45 minutes total)

1. **Morning (5 min):** Pick one idea from `_ideas/ideas_backlog.md`. Move it to top of the "In Progress" section.
2. **Write (30–40 min):** Open `_templates/essay_500words.md`. Copy it to `drafts/YYYY-MM-DD-title.md`. Write.
3. **Publish (5 min):** Run `python 05_automation/wordpress/publish_to_wp.py drafts/your-essay.md` to push a WordPress draft.
4. **Commit:** `git add drafts/ && git commit -m "draft: title"`

---

## Topics — Your Six Pillars

These are the categories that come from your life. Rotate between them.

| Pillar | What you cover |
|--------|---------------|
| **The Immigrant Mind** | Moving countries, belonging nowhere and everywhere, language |
| **Rewiring the Brain** | ADHD, Bipolar, trauma recovery, what nobody tells you |
| **The Child Who Survived** | Generational trauma, parenting differently, protection |
| **Work & Worth** | Hospitality, toxic workplaces, disability in the workplace |
| **Language & Teaching** | Learning 5 languages, CELTA, how adults really learn |
| **The Examined Life** | Jung, shadow work, philosophy, what 40 years teaches you |

---

## Where to Publish

| Platform | What goes there | Why |
|----------|----------------|-----|
| **sourovdeb.com** | Everything (WordPress) | Your home base |
| **Medium** | Essays on work, education, recovery | Pays via Partner Program, large audience |
| **Substack** | Personal letters, serialised story | Builds email list — your most valuable asset |
| **LinkedIn** | Professional angles (workplace, teaching, CELTA) | Recruiter visibility |

**Sequence:** Publish WordPress first → wait 3 days → republish on Medium with canonical link → post excerpt to LinkedIn.

---

## Energy-Aware Writing

Some days are hard. Bipolar and ADHD mean energy is not linear.

- **High-energy day:** Write the hard piece, the one that requires research or vulnerability.
- **Medium-energy day:** Write the short piece — one idea, one anecdote, one lesson.
- **Low-energy day:** Edit a draft. Or just write one paragraph and save it. That counts.

You do not skip. You adjust the dose, not the habit.
