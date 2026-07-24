# Advertiser Attraction Plan — Step by Step

**Goal:** Make sourovdeb.com earn ad revenue reliably, with content staying free.
**Written for:** working alone, limited energy, small steps. Every step is small, ordered, and checkable. Nothing here requires spending money.

---

## ⚠️ First, the honest part (read this once)

There is **no guaranteed income** from a website — anyone who promises a guarantee is selling you something. What CAN be guaranteed is the **process**: the steps below are the standard, proven path every profitable content site follows. What that realistically looks like:

| Monthly visitors | Realistic AdSense income (ELT niche, EU traffic) |
|---|---|
| 1,000 | €2–10 / month |
| 10,000 | €20–100 / month |
| 50,000 | €100–500 / month |
| 100,000+ | €300–1,500 / month + direct sponsor potential |

**The lever is traffic, not ads.** Ads are a tap on a pipe — the pipe is visitors. Your 800+ posts are a real asset most sites never have; the work is making Google send readers to them. Expect 3–6 months before meaningful income, 12+ months to something steady. That is normal, not failure.

---

## How advertisers actually "find" a site

You don't chase advertisers one by one. There are two routes:

1. **Ad networks (AdSense)** — advertisers bid automatically in Google's auction for space on your pages. They "find" you the moment you're approved and have traffic. **This is Phase 1–3 below.**
2. **Direct sponsors** — companies (ELT publishers, language apps, camera software) pay you directly. They only come once you have traffic numbers to show. **Phase 4.**

So the whole plan reduces to: **compliance → approval → traffic → proof → sponsors.**

---

## Phase 0 — Compliance (Week 1) ✅ prerequisite

Already fully documented in `implementation-manual.md` §1–§5. Do those five sections first:
Privacy Policy → cookie banner → Contact page → fix the photography post → homepage meta tags.

**Done when:** all 5 checkboxes in the implementation manual's checklist are ticked.

---

## Phase 1 — Get measurable (Week 1–2)

You cannot improve what you can't see, and you can't attract sponsors without numbers.

1. **Google Search Console** (free): search-console.google.com → Add property → `sourovdeb.com` → verify (easiest via your SEO plugin or Site Kit).
2. **Submit your sitemap:** in Search Console → Sitemaps → enter `sitemap_index.xml` (Yoast) or `sitemap.xml` (Rank Math).
3. **Install Site Kit by Google** (plugin): connects Search Console + Analytics + later AdSense, all in your WP dashboard.
4. **Google Analytics 4** via Site Kit — consent-gated by your cookie banner (CookieYes integrates with it).

**Done when:** Search Console shows your sitemap "Success" and pages start appearing under "Indexing."

---

## Phase 2 — Apply to AdSense (Week 2)

Follow `implementation-manual.md` §9. Submit, then **keep publishing while you wait** — an active site during review helps.

**If approved:** turn on Auto Ads, then refine per §10.
**If rejected:** the email gives a reason; fix only that and reapply in 2–4 weeks. Rejection is common on round one and means nothing long-term.

**Done when:** ads render on your posts.

---

## Phase 3 — Traffic engine (Month 1–6, the real work)

This is where income is actually created. One small repeating loop, ~2–3 hours per week, in any-size sessions:

### Weekly loop (pick ONE task per session)

1. **Fix metas (15 min/session).** In Search Console → Performance → top pages. Take the top page without a hand-written SEO title/description, write both (formula in `homepage-meta-tags.md` §5). Repeat down the list, a few per week.
2. **Build one hub (1 session/week).** Pick a cluster you have many posts on (e.g. English tenses, phrasal verbs, DXO basics). Write ONE hub post — "The Complete Guide to X" — that briefly introduces the topic and links to 8–15 of your existing posts. Then edit 3–4 of those posts to link back to the hub. Hubs are the single most proven SEO structure for sites with big archives.
3. **Rescue near-winners (30 min/week).** Search Console → Performance → filter positions 5–15. Those posts are almost on page 1. Improve one: better title, add a section answering the query, add 2 internal links, update the date.
4. **One new post per week or two** — ideally targeting a real search phrase ("modal verbs exercises B1", "dxo noise reduction tutorial"). Freshness + coverage.

### Monthly (30 min)

- Log numbers in `microblog/metrics.md`: visitors, indexed pages, AdSense revenue, top 3 pages.
- The weekly audit agent (see `weekly-audit-agent.md`) watches for breakage so you don't have to.

**Done when:** it's never done — this loop IS the business. But the milestone is: 10,000 visits/month.

---

## Phase 4 — Direct sponsors (after ~10k visits/month)

Now you attract advertisers by name, at 5–20× AdSense rates:

1. **Make a media-kit page** (`/advertise/`): who your audience is (English learners + teachers, EU-heavy), monthly visitors (from Analytics — real numbers only), and what you offer: sponsored post, newsletter mention, sidebar placement. State prices or "contact for rates."
2. **Add "Advertise" to the footer.**
3. **Approach 5 relevant companies** politely by email: ELT publishers, language-learning apps, teacher-training providers, DxO-adjacent photo tools. One short email each: audience, numbers, one clear offer.
4. **Always label sponsored content** ("Sponsored" / "Partenariat") — legal requirement (EU) and keeps reader trust, which is your whole asset.

Parallel income streams once traffic exists (details in `global-improvement-manual.md` §3): affiliate links (Amazon books, DxO), a Ko-fi button, and eventually one paid ELT resource pack while the blog stays free.

---

## The whole plan on one line each

- [ ] Phase 0: finish implementation-manual §1–§5 (compliance)
- [ ] Phase 1: Search Console + sitemap + Analytics live
- [ ] Phase 2: AdSense submitted → approved → ads on
- [ ] Phase 3: weekly loop (metas → hubs → rescues → 1 new post), logged monthly
- [ ] Phase 4: at 10k visits/month → media kit + 5 sponsor emails

**Energy rule:** one task per session, always finishable in under an hour, always from this list. If a week is bad, the only mandatory thing is: nothing. The agent keeps watch; the plan waits for you.
