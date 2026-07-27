# sourovdeb.com — Monetization & Educator Engagement Audit

**Date:** 2026-07-24
**Method:** Live inspection of the public site — homepage, About, ELT Masterclass, a sample lesson post, the WordPress REST API (categories, pages, posts), `robots.txt`, and the Yoast sitemap index. Plus search-visibility spot checks.
**Not inspected:** Google Analytics / Search Console (owner login required — see §2).

---

## Executive summary — the one thing that matters

The site has **825 published posts** and **no way to make money from any of them.** But the fix isn't ads.

The audit turned up a specific, unusual situation: **you already run a paid teaching business** — the About page lists your CELTA, your IELTS Specialist credential, your email, your WhatsApp, and says sessions are *"available immediately for individuals and groups, either online or in-person."* Meanwhile **813 English lesson posts contain zero mention of it.** A reader finishes your relative-clauses lesson, sees a link to your YouTube channel, and leaves. There is no bridge from "this person teaches well" to "I can hire this person."

That gap is the finding. Everything below is prioritized around it.

**Why this beats ads at your scale:** one student at €30/hour, two hours a week, is **~€240/month**. To earn €240/month from AdSense you'd need roughly **50,000–100,000 visits/month.** You are currently far below that. The teaching funnel is worth more than ads for at least the next 12–18 months, and it works *today*, at your current traffic, with one student.

---

## §1 — Site structure: what's actually there

### Content inventory (from the live REST API, not estimated)

| Category | Slug | Posts | Description set? |
|---|---|---|---|
| **English Teaching** | `english-teaching` | **813** | ❌ empty |
| Mental Health | `mental-health` | 10 | ✅ |
| Resources | `resources` | 2 | ❌ empty |
| Philosophy & Mental Health | `philosophy-mental-health` | **0** | ✅ |
| Creator & Life | `creator-life` | **0** | ✅ |
| Books & Ideas | `books-ideas` | **0** | ✅ |
| Blog | `blog` | **0** | ✅ |
| Photography & Software | `photography-software` | **0** | ❌ empty |
| Travel Journal | `travel-journal` | **0** | ❌ empty |
| Philosophy | `philosophy` | **0** | ✅ |
| Career & Professional Development | `career-professional-development` | **0** | ✅ |
| Learn AI in Mistral Studio | `learn_ai` | **0** | ❌ empty |
| DXO TUTORIAL | `dxo` | **0** | ❌ empty |
| Uncategorized | `uncategorized` | 0 | ❌ empty |

**Structural problem #1 — the menu is mostly dead ends.** Your navigation offers Blog → Mental Health / Philosophy, Resources → Career / Books & Ideas, and Photography & Software → DXO Tutorial / Learn AI in Mistral Studio. Of those eight destinations, **six contain zero posts.** A visitor clicking "Philosophy," "Books & Ideas," "DXO Tutorial," or "Learn AI in Mistral Studio" hits an empty page. This is worse than the earlier audit found — it's not one empty category, it's most of the menu.

Note the earlier "photography post in the wrong category" issue: `photography-software` still shows **0 posts**, and the Silkypix photography review is the only piece of yours currently surfacing in search. It is still not filed where the menu points.

**Structural problem #2 — 98.5% of your content is in one undescribed bucket.** 813 of 825 posts sit in "English Teaching," which has no category description. Google gets no signal about what that archive is.

### Pages that exist

`About Me`, `ELT Masterclass`, `Resources`, `My Daily Journal` (+ 4 journal sub-pages), `My Mental Health Journey`, `Philosophy & Mental Health`.

**Missing entirely:** Privacy Policy, Contact, Advertise, Donate, Courses/Booking. The first two are hard AdSense blockers; the rest are your revenue surfaces.

### The ELT Masterclass — your most valuable and most wasted asset

A structured **60-day teacher-training curriculum**, 12 weeks × 5 days, *"60 Days to Transform Your Teaching."* Roughly **days 1–30 are published; days 31–60 say "Coming soon."**

It has **no pricing, no enrolment, no email capture, no signup of any kind.** The only CTA is "Read Day [#]."

This is a professional-development product being given away with no mechanism to capture the professionals consuming it. For the educator-engagement question in §3, this is the centrepiece.

---

## §2 — Traffic patterns (honest limits + what I could establish)

**I cannot see your analytics** — that needs your Google login, which I won't ask for or use. So I can't report visits, bounce rate, or geography. Here's what I established from outside:

**Search visibility appears close to zero.** A `site:sourovdeb.com` query surfaced only your homepage and the Silkypix photography review. Searches for your exact post titles — *"Modal Verbs for Advice"*, *"Present Perfect vs Past Simple"* — returned British Council, Cambridge, EF, Grammarly, Test-English, FluentU… and **not one result from your domain.**

*Caveat, stated plainly:* third-party `site:` checks are an imperfect proxy for Google's real index. **Confirm in Search Console** (Indexing → Pages) before treating it as settled. But the signal is strong and consistent, and it matches the technical causes found below.

**Technical layer is fine — this is not a crawling failure:**
- ✅ Yoast SEO installed; sitemap index live at `/sitemap_index.xml` with post, page, category, tag, and author sitemaps
- ✅ Post sitemap updated 2026-07-23 — actively maintained
- ✅ `robots.txt` sane: blocks only `/wp-admin/`, `/wp-login.php`, `/xmlrpc.php`, plugins, cache, and search URLs; explicitly allows Googlebot + Bingbot to `/wp-json/`
- ⚠️ `Crawl-delay: 1` is set. Google ignores it; **Bing obeys it** — with 825 URLs that throttles Bing's crawl. Minor, worth removing.

**So why invisible?** Not crawlability. Two content-side causes:

1. **No internal linking.** The sample lesson post contains **zero internal links in its body text.** With 813 posts and no interlinking, every post is an orphan — Google has no path between them and no signal that any is important. This is the single biggest SEO defect on the site.
2. **You're competing head-on with British Council and Cambridge on their own keywords.** "Present perfect vs past simple" is one of the most saturated queries in ELT. A new site cannot win it directly. (Strategy in §5.)

---

## §3 — Attracting educators globally

You have something most ELT sites don't: **a complete 60-day teacher-training curriculum plus 813 lesson resources.** That's a professional-development platform, not a blog. Three specific, non-generic moves:

**a) Turn the Masterclass into a cohort, not a page.** Add one email capture: *"Get the 60-day Masterclass, one lesson a day, free."* Teachers who commit to 60 days of PD are exactly the audience worth having. This costs nothing (MailerLite free tier: 1,000 subscribers) and converts a silent archive into a list you own. **Finish days 31–60** — a half-finished curriculum reads as abandoned; a complete one is citable and shareable.

**b) Give teachers something to *use*, not just read.** The most-shared ELT resources are printables — worksheets, lesson plans, flashcards. Your 813 posts are raw material. Convert your ten strongest lessons into downloadable PDF worksheets, gated behind the email signup. Teachers share worksheets in staffrooms and Facebook groups in a way they never share blog posts.

**c) Go where ELT teachers actually gather** — and they gather in specific places, not "social media":
- **Facebook groups**: *ELT Professionals Around the World*, *Teaching English as a Foreign Language*, *IELTS Teachers* — tens of thousands of members each
- **r/TEFL** and **r/ESLTeachers** on Reddit
- **#ELTchat** on X/Bluesky, and the **IATEFL** community
- **TES / Twinkl** resource marketplaces — upload free worksheets with your site credited; both drive real referral traffic

Rule for all of these: contribute genuinely, link only when it answers the question. Groups ban self-promoters fast.

**d) Educator discounts / partnerships** — realistic sequencing: partnerships come *after* you have numbers. Skip cold outreach for now. The credible first partnership is a **guest post exchange** with another ELT blogger, which also earns your first real backlinks.

**Your unfair advantage, and use it explicitly:** eleven years in luxury hospitality in Australia, plus sommelier and barista certifications, plus aviation and healthcare English. Almost nobody teaching English online can credibly say *"I ran hospitality operations and I'll teach your hotel staff the English they need on shift."* That's a defensible niche where British Council isn't competing — and it's B2B, which pays far better than consumer lessons.

---

## §4 — Links, integrations, and external dependencies

**Outbound links found:** exactly one, repeated on posts — *"Prefer watching over reading? Visit Treasure Hunters Digital on YouTube →"* → `youtube.com/channel/UC1rs5aY7YdFiADKkhOMPCvQ`

**Internal links in post bodies:** none found. (Related-posts widgets exist, but widget links carry far less SEO weight than in-body contextual links.)

**Inbound links:** no evidence of external sites linking to you. This, plus the orphan-post problem, explains the search invisibility.

**Integrations & dependencies:**

| Dependency | Status | Note |
|---|---|---|
| WordPress (self-hosted, Hostinger) | Active | Core platform |
| Yoast SEO | Active | Sitemaps working; homepage meta still needs setting |
| Gravatar | Active | Author avatar/bio |
| YouTube (Treasure Hunters Digital) | Active | Only external property linked |
| WordPress REST API | **Publicly readable** | See risk below |
| Comments | **Enabled, zero comments** | Spam vector |
| Analytics / Search Console | **Not detected** | Blind spot — set up first |
| Cookie consent | **Absent** | GDPR + AdSense blocker |
| Ad network | **None** | Not yet applied |
| Payment / booking system | **None** | The revenue gap |

**Two risks worth flagging:**
- **Comments are open with zero moderation history.** An 825-post site with open comments and no engagement is a spam magnet, and spam links can damage the SEO you're about to build. Either require approval for all comments or disable them on older posts.
- **The REST API is publicly readable** (I used it for this audit). That's WordPress default and not a vulnerability, but `/wp-json/wp/v2/users` can expose author login names. Worth restricting once you're monetizing.

---

## §5 — Prioritized action plan

Ranked by **impact ÷ effort**, for one person with limited energy. Do them in this order.

### 🥇 Tier 1 — Revenue this month (highest impact, lowest effort)

**1. Add a booking CTA to every post — 30 minutes, potentially €100s/month.**
This is the highest-value 30 minutes available to you. Your theme almost certainly supports an "after post content" widget; if not, a plugin like *Ad Inserter* injects a block after every post automatically. Text that converts:

> **Want to practise this with a teacher?**
> I'm Sourov — Cambridge CELTA certified, IELTS Specialist, based in La Réunion. I teach IELTS, TOEIC, Business English and hospitality English online, A1–C2.
> 📧 sourovdeb.is@gmail.com · 💬 WhatsApp +262 6 93 84 61 68
> *First 20-minute consultation free.*

One block, 813 posts, immediately.

**2. Build a real "Work With Me" / booking page — 1 hour.**
Services, levels, your niches (IELTS, TOEIC, hospitality, aviation, healthcare), how to book, and rates. Add it to the main menu. Right now your commercial offer is buried at the bottom of an About page. *This also satisfies the AdSense "Contact page" requirement.*

**3. Add one email capture — 45 minutes.**
MailerLite free tier. One offer: *"The 60-Day ELT Masterclass, delivered daily. Free."* Put it on the Masterclass page and in the post footer block. An email list is the only audience asset you own outright — it survives every Google algorithm change.

### 🥈 Tier 2 — Fix what's broken (this week)

**4. Empty the dead menu.** Remove or repopulate the six empty destinations. Fastest path: point *Photography & Software* at your existing Silkypix review (move it into `photography-software`), and hide the rest from the menu until they have content. Nothing damages trust faster than empty pages.

**5. Internal linking — the SEO unlock.** Start hubs: write *"The Complete Guide to English Tenses"* linking to 10–15 existing tense posts, then edit those posts to link back. Repeat for articles, modals, business English. **This is what turns 813 orphans into a ranking structure.** Budget one hub per week.

**6. Category descriptions + homepage meta.** Both already drafted in `category-descriptions.md` and `homepage-meta-tags.md` — paste them in. English Teaching having no description while holding 813 posts is a wasted signal.

**7. Set up Search Console + Analytics.** You are flying blind. Everything after this depends on seeing real numbers. Submit `sitemap_index.xml`.

**8. Comment moderation on; remove `Crawl-delay: 1`.**

### 🥉 Tier 3 — Compliance & ads (weeks 2–4)

**9. Privacy Policy + cookie banner** — drafted in `privacy-policy.md`; steps in `implementation-manual.md` §2–§3.
**10. Apply to AdSense** — after 9 and after the Contact page from step 2. Set expectations: at current traffic this is **€2–10/month**. It's worth doing because it's passive and compounds, but it is not the plan.

### Tier 4 — Scale (months 2–6)

**11. Finish Masterclass days 31–60.**
**12. Ten downloadable worksheets**, email-gated.
**13. Target long-tail queries you can win** — not "present perfect" but *"present perfect exercises for hospitality staff"*, *"IELTS speaking part 2 healthcare vocabulary"*, *"English for hotel front desk B1"*. Your hospitality/aviation/healthcare angle has almost no competition.
**14. Affiliate links** on photography/software posts (DxO, Silkypix) — disclose them.
**15. Direct sponsors** — only above ~10k visits/month.

---

## §6 — On "non-profit" and keeping content free

You said you want the content free and the site non-profit, and separately that you need income. These aren't in conflict, but one word needs care:

**Keeping content free does not require non-profit status** — and formal non-profit status (*association loi 1901* in France) would actively restrict your ability to take teaching income personally. My recommendation: **don't** formalize non-profit status. Describe the site honestly as *"free resources, funded by teaching and ads."* That's accurate, it's what readers respond well to, and it keeps every revenue door open.

The model that fits your situation:
- **The 825 posts stay free forever.** They're your proof of expertise and your search engine.
- **Your time is what's paid for** — lessons, and later a course.
- **Ads and affiliates** cover hosting in the background.

---

## §7 — Direct answer to "is there a clear monetization path?"

**Yes — and it isn't advertising.**

The most viable starting point is **step 1 above: a booking CTA on all 813 posts.** It requires no traffic growth, no approval from Google, no waiting period, and no money. You have the credentials, the phone number, the availability, and the audience-proof already written. The only missing piece is the sentence that connects them.

Ads are a rounding error until you're at 50k visits/month. **Teaching pays now.** Build the funnel first; let AdSense accumulate quietly in the background while the SEO work in Tier 2 compounds.

---

## Verification checklist

Numbers to confirm yourself once Search Console is live — I'd rather you check than take my word:

- [ ] Indexing → Pages: how many of the 825 are actually indexed?
- [ ] Performance: any impressions at all in the last 3 months?
- [ ] Any query where you rank in positions 5–20? Those are the rescuable ones.
- [ ] Analytics: current monthly visitors — this sets realistic ad expectations.
