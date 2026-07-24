# Implementation Manual — Step by Step

**Everything you click, in order.** Follow top to bottom. The first four sections clear the AdSense blockers; the rest are quality fixes; the last section is the application itself.

You'll do all of this yourself in WordPress — I don't have your login and won't ask for it. Where a section pairs with a drafted file, it's named.

**Before you start:** Log in at `sourovdeb.com/wp-admin`. Keep the drafted files (`privacy-policy.md`, `homepage-meta-tags.md`, `category-descriptions.md`) open in another tab to copy from.

---

## § 1 — Fix the mis-filed photography post (5 min) 🔴 BLOCKER

**Problem:** "The Basic Terms in Photograpy Explained !!" has a typo AND is filed under English Teaching.

1. WP → **Posts** → **All Posts**.
2. Find the photography post (search "Photograp").
3. Hover it → click **Quick Edit**.
4. **Title:** change to
   `Photography Basics: 50 Essential Terms Every Photographer Should Know`
   *(fixes the typo and drops the spammy `!!`)*
5. **Do NOT change the Slug/URL.** Leave it as-is so existing links don't break.
6. **Categories:** untick **English Teaching**, tick **Photography & Software** (and **DXO Tutorial** if relevant).
7. Click **Update**.

✅ This also fixes the "empty Photography & Software category" and the "dead menu link" problems at once.

---

## § 2 — Publish the Privacy Policy (10 min) 🔴 BLOCKER

**Source file:** `privacy-policy.md`

1. WP → **Pages** → **Add New**.
2. Title: `Privacy Policy`.
3. Confirm the permalink shows `/privacy-policy/`.
4. Paste the body of `privacy-policy.md` (everything below its instruction block).
5. Fill the four placeholders: `[[CONTACT EMAIL]]`, `[[SITE OWNER NAME]]`, `[[LOCATION]]`, `[[LAST UPDATED]]`.
6. Click **Publish**.
7. Add it to the footer: WP → **Appearance** → **Menus** (or **Widgets** → Footer). Add the Privacy Policy page to the footer menu. Save.

✅ AdSense checks the footer for this link specifically.

---

## § 3 — Install the cookie consent banner (10 min) 🔴 BLOCKER

Required because La Réunion is EU territory → GDPR applies → consent needed *before* AdSense cookies load.

1. WP → **Plugins** → **Add New**.
2. Search **CookieYes** (free) — or **Complianz** if you want a paid, more automated option.
3. **Install** → **Activate**.
4. Run its setup wizard:
   - Region: **EU / GDPR**.
   - Enable **prior consent** (block cookies until the user accepts).
   - Categories: Essential (always on), Analytics, Advertisement.
   - Link the banner's "Privacy Policy" button to your new page.
5. Add a **"Cookie Settings"** link to the footer so users can change their choice (the Privacy Policy references this).
6. Test in an incognito window: the banner should appear on first visit.

✅ For AdSense EU compliance, the banner must let users **reject** as easily as accept.

---

## § 4 — Homepage meta title + description (10 min) 🔴 quality (do before applying)

**Source file:** `homepage-meta-tags.md`

1. WP → **Plugins** → install **Yoast SEO** or **Rank Math** (free) if you don't have one. Activate.
2. Yoast: **Yoast SEO** → **Settings** → **Search appearance** → **Homepage**.
   Rank Math: **Rank Math** → **Titles & Meta** → **Homepage**.
3. Paste your chosen **SEO Title** (Option A recommended).
4. Paste your chosen **Meta Description** (Option A recommended).
5. If there's a **Social** tab, add the Open Graph title/description and upload a 1200×630 image.
6. Save.

---

## § 5 — Add a Contact page to the nav (10 min) 🔴 BLOCKER

AdSense wants a real, reachable human.

1. WP → **Plugins** → install a form plugin (**WPForms Lite** or **Contact Form 7**, both free). Activate.
2. Create a simple form (Name, Email, Message).
3. WP → **Pages** → **Add New** → title `Contact`. Embed the form (WPForms adds a block/shortcode). Add a line like *"Get in touch — I read every message."* Publish.
4. WP → **Appearance** → **Menus** → add the **Contact** page to your main navigation. Save.

---

## § 6 — Add the "why it's free" statement (5 min) 🟡

Reinforces the non-profit positioning for both readers and advertisers.

1. WP → **Pages** → edit your **About Me** page.
2. Add a short paragraph, e.g.:
   > *"Everything on this site is free to read. I keep it that way by running unobtrusive ads, which cover hosting and let me keep publishing without a paywall. If you find something useful, sharing it is thanks enough."*
3. Update.

---

## § 7 — Unique category descriptions (20 min) 🟡

**Source file:** `category-descriptions.md`

1. WP → **Posts** → **Categories**.
2. For each category: hover → **Edit** → paste the matching description into **Description** → **Update**.
3. Repeat for all categories. Use the fill-in formula at the bottom of the file for any not listed.

---

## § 8 — Remove duplicate widgets (15 min) 🟡

Two "You Might Also Like" blocks and double prev/next navigation per post.

1. **First check widgets:** WP → **Appearance** → **Widgets**. Look in the post/single-post widget areas for a duplicate "Related Posts" widget. Remove one.
2. **If both remain, it's the theme + a plugin:** WP → **Appearance** → **Theme Settings** (or **Customize**). Look for a "Related Posts" or "Post Navigation" toggle. Disable the theme's copy if a plugin (e.g. Jetpack, YARPP) provides its own — or vice versa. Keep exactly one of each.
3. Reload any post in an incognito window to confirm a single block + single nav.

*If your theme has no such toggle, tell me the theme name and I'll give exact instructions.*

---

## § 9 — Apply to Google AdSense (5 min) 🟢 LAST

Only after §1–§5 are done and live.

1. Go to **google.com/adsense** → sign in with your Google account.
2. Add your site: `sourovdeb.com`.
3. Choose your country: **France**.
4. AdSense gives you a code snippet or asks you to connect via a plugin (**Site Kit by Google** is the easiest — install it, connect AdSense, it places the code for you).
5. Submit for review. **Review takes a few days to two weeks.**
6. While waiting, keep publishing — active, fresh content helps approval.

**If rejected:** the email states the reason. The two most common are "low value content" (rare for you — you have volume + expertise) and "policy issues" (usually a missing Privacy Policy or consent banner — which §2/§3 prevent). Tell me the exact reason and I'll help you respond.

---

## § 10 — After approval: ad placement

Once approved, use **Auto Ads** to start (Google decides placement), then refine to:

- One **in-content** ad after the 2nd paragraph
- One **sidebar** ad
- One **after post content**, *before* the related-posts block
- **No ads** on the ELT Masterclass / lead-gen pages (those convert readers, don't monetise them)
- **Never** place ads next to buttons or nav where a mis-click looks accidental — that violates AdSense policy and risks a ban

---

## Progress checklist

Copy this into a note and tick as you go:

- [ ] §1 Photography post: title fixed + moved to Photography & Software
- [ ] §2 Privacy Policy published + linked in footer
- [ ] §3 Cookie consent banner live (reject option works)
- [ ] §4 Homepage meta title + description set
- [ ] §5 Contact page created + in nav
- [ ] §6 "Why it's free" note on About page
- [ ] §7 Category descriptions filled
- [ ] §8 Duplicate widgets removed
- [ ] §9 AdSense application submitted
- [ ] §10 Ad placements configured after approval
