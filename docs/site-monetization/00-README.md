# sourovdeb.com — Monetization & Compliance Package

**Prepared:** 2026-07-24
**Goal:** Get sourovdeb.com compliant and ready for Google AdSense, while keeping all content **free** (ad-supported, non-profit model).
**Owner action required:** Everything here is drafted for you to copy into WordPress. I do not have and will not use your WordPress login — you paste, you publish, you stay in control.

---

## What's in this folder

| File | What it is | Where it goes in WordPress |
|---|---|---|
| `00-README.md` | This index | — (reference only) |
| `privacy-policy.md` | Full GDPR + AdSense-compliant Privacy Policy | New **Page** → `/privacy-policy/` + footer link |
| `homepage-meta-tags.md` | Homepage title tag, meta description, TLDR/summary block | SEO plugin (Yoast/RankMath) homepage settings |
| `category-descriptions.md` | Unique SEO description for every category | WP → Posts → Categories → Edit each |
| `implementation-manual.md` | Step-by-step click-by-click WordPress instructions | — (follow it) |
| `global-improvement-manual.md` | Long-term roadmap: SEO, monetization, growth | — (reference, quarterly review) |

---

## The 4 hard blockers before you can apply to AdSense

AdSense **will reject** the application if any of these are missing. Do these first, in this order:

1. **Privacy Policy page** live and linked in the footer — draft ready in `privacy-policy.md`
2. **Cookie consent banner** (GDPR — La Réunion is EU territory) — install CookieYes (free); steps in `implementation-manual.md` §3
3. **Contact page** in the navigation — a real, reachable human. Steps in `implementation-manual.md` §5
4. **Content coherence** — fix the photography post that's mis-filed under English Teaching. Steps in `implementation-manual.md` §1

Everything else (meta tags, category descriptions, duplicate widgets) improves quality and ranking but does **not** block the AdSense application.

---

## The non-profit / free-content positioning

Your model: **content stays free, ads cover costs.** This is a legitimate, common, AdSense-friendly model. Two things make it credible to both advertisers and Google:

- A clear **"why it's free"** statement on the About page (drafted in `implementation-manual.md` §6)
- **No misleading placements** — ads must be clearly ads, never disguised as content or navigation (AdSense policy)

If you ever want formal non-profit status (association loi 1901 in France), that's a separate legal step outside this package — flagged in the global manual for later.

---

## Suggested order of work

Follow `implementation-manual.md` top to bottom. It's sequenced so the AdSense blockers come first, quality fixes second, and the application itself last.
