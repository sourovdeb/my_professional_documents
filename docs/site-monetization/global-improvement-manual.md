# Global Improvement Manual — Future Roadmap

A living reference for growing sourovdeb.com after the AdSense blockers are cleared. Reviewed quarterly. Sequenced from highest-leverage to nice-to-have.

---

## Guiding principle

**Free content, ad-supported, credible.** Every decision serves one of three goals:
1. **More qualified traffic** (SEO + sharing)
2. **Better ad revenue per visitor** (placement + relevance, never at the cost of trust)
3. **Stronger authority** (so advertisers and Google trust the site)

Never trade reader trust for a short-term revenue bump — it costs you both in the end.

---

## 1. SEO — the biggest lever (ongoing)

You have 800+ posts. The opportunity isn't more posts — it's making the existing ones rank.

**Quarter 1 priorities**
- **Meta everywhere:** every post gets a unique SEO title + description (formula in `homepage-meta-tags.md`). Start with your 20 most-visited posts (check Analytics).
- **Internal linking:** each post should link to 2–3 related posts in the body text (not just the widget). This spreads ranking power and keeps readers on-site. Build "hub" posts that link out to a cluster (e.g. one "Complete Guide to English Tenses" linking to each tense post).
- **Fix thin/duplicate posts:** merge or expand any post under ~300 words. Google ignores thin content and it can drag AdSense approval.
- **XML sitemap:** confirm Yoast/Rank Math is generating one, then submit it in **Google Search Console**.

**Set up Google Search Console** (free) if not already — it shows which queries you rank for, so you optimise what's already close to page 1.

**Schema markup**
- Add **LearningResource** or **Course** schema to ELT posts (Rank Math supports this) — can earn rich results in search.
- Add **Article** schema site-wide (most SEO plugins do this automatically).

---

## 2. Content structure & navigation

- **Rename "Blog"** to something specific ("Essays" or "Notes") so it doesn't compete with English Teaching for reader attention.
- **Promote ELT Masterclass** to a top-level menu item — it's your flagship, don't bury it.
- **Category cleanup:** aim for a clear hierarchy. Too many overlapping categories dilute SEO; too few make navigation hard. Review yearly.
- **Featured images:** add one per post going forward (even a simple templated graphic). Fixes blank social previews and lifts click-through when shared.

---

## 3. Monetization maturity

**Phase 1 — AdSense (now):** get approved, run tasteful auto/manual ads.

**Phase 2 — optimise (3–6 months in):**
- Watch **RPM** (revenue per 1000 views) in AdSense. Experiment with placement, but keep it clean.
- Block low-quality ad categories in AdSense settings to protect your brand.
- Your ELT/IELTS keywords carry decent European CPCs — content targeting "IELTS", "learn English", "English grammar" tends to earn more per click.

**Phase 3 — diversify (6–12 months, only if traffic supports it):**
- **Affiliate links** — cameras/software for photography posts, books for ELT (Amazon Associates, DxO affiliate). Disclose them (add an affiliate-disclosure line to the Privacy Policy / a Disclosure page).
- **Digital products** — a paid ELT resource pack or course, while keeping the blog free. This is the highest-margin path if your audience grows.
- **Ko-fi / "Buy me a coffee"** — voluntary reader support that fits the non-profit ethos.

**Keep the promise:** the *blog* stays free. Paid = optional extras, never a paywall on existing content.

---

## 4. Legal / compliance upkeep

- **Formal non-profit status:** if you ever want it official in France, look into an *association loi 1901*. Not required to run ads or call the content free — it's a separate legal structure. Get local advice before committing.
- **Affiliate disclosure:** required by law once you add affiliate links (add a Disclosure page + line in Privacy Policy).
- **Keep Privacy Policy current:** update it whenever you add a new data-collecting tool (email list, new analytics, comment system).
- **Email list:** if you start one, you need explicit opt-in consent + an unsubscribe link (GDPR + the French RGPD). Use a compliant provider (Mailchimp, Brevo/Sendinblue — Brevo is EU-based).
- **Accessibility:** aim for readable contrast, alt text on images, descriptive links. Good for users, SEO, and increasingly a legal expectation in the EU.

---

## 5. Performance & technical health

- **Core Web Vitals:** check in Search Console. Fast load = better ranking + more ad viewability. A caching plugin (LiteSpeed Cache on Hostinger, or WP Super Cache) helps.
- **Image optimisation:** compress images (ShortPixel/Smush) — biggest speed win for most WordPress sites.
- **Mobile-first:** most traffic and most ad revenue is mobile. Test every template change on a phone.
- **Broken link check:** run a scan (Broken Link Checker plugin, sparingly — it's heavy) quarterly. Dead links hurt SEO and reader trust.
- **Backups:** confirm Hostinger backups are on, or add a plugin (UpdraftPlus). Non-negotiable before you have real traffic.

---

## 6. Analytics & the monthly review loop

Set a recurring 30-minute monthly review:

1. **Top 10 posts** by traffic — can any be updated/expanded to rank higher?
2. **Top queries** in Search Console — any you rank #5–15 for? Those are quick wins: improve the post, jump to page 1.
3. **AdSense RPM & top-earning pages** — do more of what earns.
4. **Bounce/engagement** — are readers reading or leaving? Weak intros and slow pages are the usual culprits.
5. **One experiment** — change one thing (a title, a placement, an internal-link cluster) and measure next month.

Log it in `microblog/metrics.md` so you can see the trend over time.

---

## 7. Consistency engine

Monetization compounds with publishing consistency.

- **Editorial calendar:** 1–2 quality posts/month minimum (you already aim for this in `microblog/editorial-calendar.md`). Consistency signals freshness to Google.
- **Repurpose:** turn strong posts into social snippets, a newsletter issue, or a short video. Same content, more reach.
- **Batch:** draft several posts in one sitting, schedule them out. Protects consistency against busy weeks.

---

## Quarterly review checklist

- [ ] Meta titles/descriptions added to next batch of top posts
- [ ] Internal links added to recent posts
- [ ] Search Console: reviewed top queries, optimised 3 near-page-1 posts
- [ ] AdSense: checked RPM, adjusted one placement
- [ ] Privacy Policy still accurate (any new tools added?)
- [ ] Site speed / Core Web Vitals checked
- [ ] Backups confirmed working
- [ ] One growth experiment run + logged
