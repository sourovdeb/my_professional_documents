# sourovdeb.com — Monetization, AI-Agent & Educator-Engagement Audit

**Prepared:** 2026-07-24 (scheduled audit)
**Method:** Live read-only fetch of sourovdeb.com (homepage, About, ELT Masterclass), review of this repo's existing monetization package (`docs/site-monetization/`), and a review of `free_education/` for content assets not yet surfaced on the site. No WordPress login was used or needed.
**Relationship to existing docs:** This does not replace `advertiser-attraction-plan.md` or `global-improvement-manual.md` — it fills the two gaps they don't cover (AI-agent feasibility, educator-as-audience strategy) and adds a full link/integration inventory. Read this alongside them, not instead of them.

---

## 0. Executive summary — the one thing to act on first

**The site currently has zero analytics installed.** No Google Analytics, no Search Console tag, no tracking script of any kind was found in the homepage source. This means every recommendation below — including the entire `advertiser-attraction-plan.md` traffic phase — is currently unmeasured. **This is the single highest-priority, lowest-effort fix on this page**: install Google Search Console + Site Kit (already Phase 1 in the advertiser plan) before anything else, because right now there is no way to know which of these recommendations would actually move the needle.

**Second finding, not previously documented:** the site already has a live, working monetization channel that the existing package doesn't mention — **1:1 paid tutoring**, booked directly via WhatsApp/email from the About page (IELTS/TOEIC prep, professional English, sector-specific coaching). This is real revenue infrastructure, already built, currently invisible to the rest of the site (no link to it from the homepage, English Teaching category, or ELT Masterclass). It is the most viable near-term revenue lever — more so than AdSense — because it doesn't require traffic thresholds, ad approval, or GDPR ad-tech compliance. See §2.

**Third finding:** the flagship "ELT Masterclass" (a 60-day, 12-week course) is half-built — days 31–60 show "Coming soon." It has no enrollment mechanism and isn't linked to the tutoring service, so it currently converts nobody into anything. It's a large, underused asset.

If the non-profit's real constraint is founder time/energy (confirmed by `Growth_Hub/00_START_HERE.md`'s framing around uneven energy), the highest-leverage sequence is: **instrument → connect existing paid tutoring to existing free content → finish or freeze the Masterclass → then AdSense/traffic** — not the reverse.

---

## 1. Site structure & content audit (live, 2026-07-24)

### Navigation & categories
Home · About Me · English Teaching · ELT Masterclass · Blog · Mental Health · Philosophy · Resources · Career & Professional Development · Books & Ideas · Photography & Software (with DXO Tutorial and "Learn AI in Mistral Studio" sub-categories).

### What's actually there
- English Teaching category is active with real posts (reported speech, relative clauses, articles, passive voice, modal verbs, present perfect) and professional-English content (CV writing, small talk, presentations, job interviews).
- Blog mixes Mental Health and Philosophy under one category — two very different reader intents sharing one nav item (already flagged in `global-improvement-manual.md` §2 as a rename candidate).
- ELT Masterclass: 12-week/60-day structure, roughly half published, no CTA, no pricing, no signup.
- Photography & Software / DXO / "Learn AI in Mistral Studio": a third, unrelated audience (photographers, AI-in-Mistral-Studio learners) sharing the same nav as English learners. This is a content-coherence issue the existing package already flags (§ "photography post filed under English Teaching").

### What's conspicuously absent
- No Contact page distinct from About (blocks AdSense per `00-README.md` blocker #3 — still open).
- No Privacy Policy page found in navigation or footer (blocker #1 — still open).
- No visible cookie consent banner (blocker #2 — still open).
- No newsletter/email capture anywhere on the pages sampled.
- No donation/Ko-fi button.
- No visible "for educators" or "for teachers" section — every page addresses the *learner*, never the *teacher*, despite the repo (`free_education/`) containing teacher-facing material (see §4).

**Conclusion on the 4 AdSense blockers from `00-README.md`:** all four are still open as of this audit. AdSense readiness has not progressed since the package was drafted.

---

## 2. Monetization options — assessed and re-prioritized

| Option | Status today | Feasibility (non-profit, solo founder) | Impact | Priority |
|---|---|---|---|---|
| **1:1 tutoring (existing)** | Live but unlinked from content | High — zero build cost, already works | High — direct revenue, no traffic threshold | **P0 — surface it** |
| Analytics/Search Console | Not installed | Trivial (1 session) | Enables every other decision | **P0 — do first** |
| AdSense | Blocked (4 items open) | Medium — well-documented in `implementation-manual.md` | Low until traffic exists (see income table in `advertiser-attraction-plan.md`) | P1, after P0s |
| Finish/gate ELT Masterclass | Half-built | Medium — 29 lessons remain | High — could become the tutoring funnel | P1 |
| Ko-fi / voluntary support | Not started | Trivial | Low but fits non-profit ethos, adds zero ad-tech/GDPR burden | P1 |
| Affiliate links (ELT books, DxO/photo software) | Not started | Low-medium — needs disclosure page first | Low-medium, compounds with SEO traffic | P2 |
| Institutional/educator licensing (see §4) | Not started | Medium — needs a package to sell | Medium-high, but requires an audience that doesn't exist yet | P2 |
| Direct sponsors | Not viable pre-traffic | N/A until ~10k visits/mo per existing plan | High, later | P3 (unchanged from `advertiser-attraction-plan.md` Phase 4) |

**Why tutoring is P0 and AdSense is P1, reversing the existing plan's implicit order:** AdSense income at current (near-zero, unmeasured) traffic is, per the plan's own table, likely single-digit euros/month for a long time. Tutoring converts at any traffic level and the infrastructure (WhatsApp number, email, credentials) already exists — the only work is adding a visible link from the homepage and each English Teaching post ("Want 1:1 help with this? Book a session →"). This is a same-day fix, not a multi-month SEO campaign.

---

## 3. Could an AI agent help with content delivery, engagement, or support?

Assessed against the site's actual constraints: solo non-profit founder, no dev team, WordPress-hosted, currently zero paid tooling budget mentioned.

**Where an AI agent is a good fit:**
1. **ELT Masterclass navigator / study companion.** The Masterclass is structured (12 weeks, daily lessons) but has no way to track progress or answer "what should I read next / I don't understand X." A lightweight embedded chat widget scoped *only* to the Masterclass content (RAG over the ~30 published lesson pages) could answer learner questions and recommend the next lesson — this both increases content engagement and creates a natural upsell path into paid tutoring ("this needs a human — book a session").
2. **Tutoring booking assistant on WhatsApp.** Since booking already happens via WhatsApp, a scripted/AI-assisted intake flow (availability, level, goal — IELTS vs. professional English vs. sector-specific) would reduce founder back-and-forth before a paying session, which matters for someone managing energy carefully.
3. **Weekly site-health watch.** Already exists and is the right shape — `weekly-audit-agent.md` (Monday 06:00 UTC, read-only, reports via draft PR). No change needed there; it's a good template for scoping any future agent narrowly and safely.

**Where it's not a good fit yet:** a general-purpose site-wide chatbot, or anything requiring WordPress write access/credentials. Given `docs/site-monetization`'s explicit design principle ("read-only, no credentials, no live-site changes"), any agent that posts to WordPress or handles payments should stay out of scope until there's a concrete reason and a human review step — consistent with how the audit routine itself is scoped.

**Cost reality (2026 market rates, from live research):** budget/entry-level chatbot tooling for a small site runs roughly **$0–50/month** for low-traffic sites, rising to $30–150/month for more active SMB use — well inside reach for a non-profit once there's a specific job (the Masterclass navigator) rather than a vague "add AI to the site" goal. Building it as a scoped RAG widget over ~30 known lesson pages is a bounded, cheap build; a general assistant is not.

**Recommendation:** don't add an AI agent to the live site until Section 2's P0 items are done. The immediate ROI is in *linking existing things to each other*, not adding a new surface.

---

## 4. Attracting educators globally — this audience doesn't exist on the site today

Everything on sourovdeb.com currently speaks to the *learner*. Nothing addresses the *teacher* — despite two facts that make this a real gap, not a hypothetical one:

- The founder is CELTA-certified and already produces teacher-facing material.
- The sibling repo `free_education/` contains teacher/trainer-usable content not yet surfaced on the public site: `elt365_lessons/` (a 365-daily-lesson framework) and `routines/01_elt365_lessons_routine/`, `02_python_toolkit_routine/`, `03_human_nature_routine/` — reusable teaching routines and a psychology/behavior primer, roughly 316KB of routine material and 48KB of lesson content, currently living only in git, not on the website.

### Concrete, non-generic strategies (grounded in current 2026 research on what actually draws educators — see sources)

1. **Publish a "For Educators" hub page** that repackages existing `free_education/routines/` content as downloadable lesson plans/frameworks — not new writing, just surfacing what's already written. This is the cheapest possible move (content exists, zero new drafting) and directly targets the audience gap.
2. **Free-access-first positioning.** Research on educator platform adoption consistently shows free tools/resources without added cost is a primary driver of educator uptake (edWeb, NEA educator-resource models). The site already has this — it just needs to be labeled *for teachers* explicitly, not just for learners. [Educator Resources | NEA](https://www.nea.org/weta/educator-resources)
3. **Community/PD framing, not just downloads.** Effective educator communities pair resource-sharing with light professional-development framing — e.g., "how I use this in a CELTA-style lesson," a short rationale note per lesson plan. This costs one paragraph per resource, not a platform build. [edWeb: A professional online community for educators](https://home.edweb.net/)
4. **Institutional/educator discount tier on the eventual paid resource pack** (`global-improvement-manual.md` §3 already floats "a paid ELT resource pack"). When that ships, a teacher/school discount (or a free-for-teachers, paid-for-institutions split) is a standard non-profit-compatible way to grow reach without gating the core mission.
5. **Direct outreach to 3–5 relevant existing communities** (ELT teacher Facebook groups, TEFL/CELTA alumni networks, edWeb-style hubs) once the "For Educators" hub exists — same low-cost-per-contact approach already specified for sponsor outreach in `advertiser-attraction-plan.md` Phase 4, reused for a different audience.

**Feasibility note:** all five items above are content-reuse and linking work, not new infrastructure — they fit the "one task per session, always finishable in under an hour" energy rule already established in `advertiser-attraction-plan.md`.

---

## 5. Inbound/outbound links & integrations — inventory

### Internal site structure (sourovdeb.com)
```
/ (home)
/about-me/
/category/english-teaching/
/elt-masterclass/
/category/blog/
/category/mental-health/
/category/philosophy/
/category/resources/
/category/career-professional-development/
/category/books-ideas/
/category/photography-software/
/category/photography-software/dxo/
/category/photography-software/learn_ai/
/?post_type=post   (all-posts view)
```

### External outbound links (found)
- `secure.gravatar.com` — author avatar (Gravatar/Automattic dependency)
- No other outbound links detected on homepage/About/Masterclass pages sampled — no social media profile links, no YouTube link (channel "Treasure Hunters Digital" is *mentioned* in About-page text but not hyperlinked, worth fixing — free traffic left on the table).

### Contact/booking channels (not hyperlinks, but functional integrations)
- WhatsApp: `+262 693 84 61 68`
- Email: `sourovdeb.is@gmail.com`

### Scripts/tracking/embeds
- **None detected** on the pages fetched — no Google Analytics, no Google Fonts embed, no ad script, no comment system, no newsletter widget, no cookie-consent script. Confirms §0's finding: the site is pre-instrumentation.

### Repo → site integration (from this repo's own docs)
- WordPress REST API sync: `https://sourovdeb.com/wp-json/sourov/v1/ai-post` (draft-only, documented in root `CLAUDE.md`) — the only automated inbound content pipeline. Categories synced: Mental Health, ELT Masterclass, English Teaching, Philosophy, Photography, Software, DXO, Learn AI in Mistral Studio. **No "Educators" category exists in this list** — confirms §4's gap at the pipeline level, not just the nav level.

### Gap vs. what a healthy small content site usually has
Missing entirely: Privacy Policy, Contact page, cookie consent, any analytics, any social proof (social links), any email capture, any donation mechanism. This matches and confirms the 4 open blockers in `00-README.md` — nothing has shipped from that package to the live site yet.

---

## 6. Step-by-step recommendations, prioritized by feasibility × impact

**This week (near-zero effort, do these regardless of anything else):**
1. Install Google Search Console + Site Kit (`advertiser-attraction-plan.md` Phase 1) — you cannot prioritize anything else on this list without this.
2. Add a visible "Book 1:1 tutoring" link/button to the homepage header and to the end of every English Teaching post, pointing to the existing WhatsApp/email contact already on the About page. Zero build cost, activates existing paid infrastructure.
3. Hyperlink the "Treasure Hunters Digital" YouTube channel mention on the About page.

**Next 2–4 weeks (the 4 AdSense blockers, unchanged from existing package — still all open):**
4. Publish Privacy Policy (`privacy-policy.md` is already drafted, just needs pasting into WordPress).
5. Add cookie consent banner (CookieYes, per `implementation-manual.md` §3).
6. Add a real Contact page distinct from About.
7. Fix the mis-filed photography post under English Teaching.

**Next 1–2 months (new from this audit, medium effort):**
8. Build the "For Educators" hub page repackaging `free_education/routines/` content — cheapest high-impact move for educator reach (§4.1).
9. Decide explicitly: finish the ELT Masterclass's remaining ~29 "coming soon" lessons, or cap it at what exists and repurpose it as a lead magnet into tutoring. Half-finished is worse than either choice — it's currently a dead end for readers who reach it.
10. Add "Educators" as a synced content category in the WordPress pipeline (`sync_verification.py`) so future `free_education/` content flows to the site automatically instead of staying repo-only.

**3–6 months (compounding, per existing `advertiser-attraction-plan.md`, unchanged — still correct):**
11. AdSense application once blockers are cleared (Phase 2).
12. Weekly traffic-engine loop — metas, hub posts, near-winner rescues (Phase 3).
13. Scoped ELT-Masterclass AI navigator widget, only once the Masterclass content decision (#9) is made and the widget has a clear, bounded job (§3).

**6–12 months:**
14. Direct sponsor/educator-partnership outreach once traffic and the Educators hub both have real numbers to show (`advertiser-attraction-plan.md` Phase 4, extended to educator communities per §4.5 above).

---

## 7. If there's no clear monetization path — there is one here

There is a clear starting point, and it isn't AdSense: **the site already has a working paid product (1:1 tutoring) that isn't linked from anywhere.** For a non-profit prioritizing impact over ad revenue, the single most viable, lowest-risk, immediately actionable step is #2 above — surface the existing tutoring channel — because it requires no traffic growth, no ad-network approval, no new GDPR surface area, and no new content. Everything else in this report compounds over months; that one is a same-day fix with a direct, testable revenue signal (does the WhatsApp number get more messages after the link goes live).

---

## Sources consulted
- [Educator Resources | NEA](https://www.nea.org/weta/educator-resources)
- [edWeb: A professional online community for educators](https://home.edweb.net/)
- [Recruit and Retain Educators | NEA](https://www.nea.org/student-success/recruit-and-retain-educators)
- [How Much Do AI Chatbots Cost? Estimates for 2026](https://www.crescendo.ai/blog/how-much-do-chatbots-cost)
- [Chatbot Pricing in 2026: What Does It Cost? | WotNot](https://wotnot.io/blog/chatbot-pricing)
- Live fetch of sourovdeb.com homepage, `/about-me/`, `/elt-masterclass/` (2026-07-24)
- This repo: `docs/site-monetization/*`, `free_education/routines/*`, `CLAUDE.md` (both repos)
